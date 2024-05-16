# -*- coding: utf-8 -*-
"""
Gait database.

"""

import sys
import traceback
from copy import copy
from dataclasses import dataclass, fields
from pathlib import Path

import sqlite3
from pkg_resources import resource_filename
from PyQt5 import QtCore, QtSql, QtWidgets, uic
from ulstools.env import named_tempfile
from ulstools.num import check_hetu

from config import cfg
from rom_entryapp import EntryApp
from utils import _startfile, validate_code
from widgets import qt_message_dialog, qt_confirm_dialog
from constants import Constants


@dataclass
class PatientData:
    """A patient record"""

    firstname: str = ''
    lastname: str = ''
    ssn: str = ''
    # lab internal patient code; note that this is different from the SQL
    # patient id, which is automatically assigned by the SQL engine
    patient_code: str = ''
    diagnosis: str = ''

    def is_valid(self):
        """Check whether the patient info is valid.

        Returns a tuple of (is_valid, reason).
        """
        if not check_hetu(self.ssn):
            return (False, 'Invalid SSN')
        elif not validate_code(self.patient_code):
            return (False, 'Invalid patient code')
        return (True, '')


class NonLazyQSqlTableModel(QtSql.QSqlTableModel):
    """QSqlTableModel without the lazy fetch feature.

    Initially, QSqlTableModel will only fetch 256 first rows from a table, to
    speed up access to large tables. It then reads further rows as necessary. In
    case of SQLite, this behavior results in a SHARED lock to the database being
    held indefinitely, preventing writes. This class disables the lazy fetch
    feature.
    """

    def fetchMore(self, parent: QtCore.QModelIndex = ...) -> None:
        """Whenever fetchMore is called, we fetch everything"""
        while super().canFetchMore():
            super().fetchMore()


class MultiColumnFilter(QtCore.QSortFilterProxyModel):
    """Filter proxy that returns textual match on given columns"""

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        # range defines the columns to include in the matching
        inds = (model.index(source_row, k, source_parent) for k in range(1, 6))
        return any(
            self.filterRegExp().indexIn(str(model.data(ind))) != -1 for ind in inds
        )


class PatientEditor(QtWidgets.QDialog):
    """Dialog to edit a patient"""

    def __init__(self, check_patient, patient=None, parent=None):
        """Init the patient edit window.

        check_patient is a callback which will check that the
        Patient record is ok and can be inserted into the database.
        It should accept one argument (the patient record).
        If a patient record is provided, its values will be displayed for
        editing. Otherwise, a new patient will be created.
        """
        uifile = resource_filename('gaitbase', 'edit_patient.ui')
        super().__init__(parent)
        uic.loadUi(uifile, self)
        self.setStyleSheet('QWidget { font-size: %dpt;}' % cfg.visual.fontsize)
        self.btnSave.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.patient_check_callback = check_patient
        self._patient = patient or PatientData()
        self._original_patient = copy(self._patient)
        # set widget default values
        self.lnFirstName.setText(self._patient.firstname)
        self.lnLastName.setText(self._patient.lastname)
        self.lnSSN.setText(self._patient.ssn)
        self.lnPatientCode.setText(self._patient.patient_code)
        self.lnDiagnosis.setText(self._patient.diagnosis)

    @property
    def patient(self) -> PatientData:
        """Return a patient record corresponding to current input data"""
        self._patient.firstname = self.lnFirstName.text()
        self._patient.lastname = self.lnLastName.text()
        self._patient.ssn = self.lnSSN.text()
        self._patient.patient_code = self.lnPatientCode.text()
        self._patient.diagnosis = self.lnDiagnosis.text()
        return self._patient

    def accept(self):
        """Guard for superclass accept - check patient first"""
        patient_ok, result = self.patient_check_callback(self.patient)
        if patient_ok:
            super().accept()
        else:
            msg = f'Please fix the following errors: {result}'
            qt_message_dialog(msg)

    def reject(self):
        """Guard for superclass reject"""
        if self.patient == self._original_patient or qt_confirm_dialog(
            'Are you sure you want to cancel changes?'
        ):
            super().reject()


def db_failure(query, fatal=False):
    """Handle database failures"""
    err = query.lastError().databaseText()
    msg = f'Got a database error: "{err}"'
    msg += '\nIn case of a locking error, close all other applications '
    msg += 'that may be using the database, and try again.'
    if fatal:
        raise RuntimeError(msg)
    else:
        qt_message_dialog(msg)


class PatientDialog(QtWidgets.QMainWindow):
    """Visualize patients and measurements in table views"""

    def __init__(self, parent=None):
        super().__init__(parent)
        uifile = resource_filename('gaitbase', 'gaitbase_main.ui')
        uic.loadUi(uifile, self)
        self._rom_windows = dict()

        # some configurable stuff
        self.CONFIRM_EXIT = False

        self.database = QtSql.QSqlDatabase('QSQLITE')
        if not Path(cfg.database.database).is_file():
            msg = f'The database {cfg.database.database} does not exist. '
            msg += 'Please set the correct location in the config.'
            qt_message_dialog(msg)
            sys.exit()

        # Check the DB schema version
        try:
            conn = sqlite3.connect(cfg.database.database)
            db_ver = list(conn.execute('PRAGMA user_version'))[0][0]
            conn.close()
        except:
            msg = f'Error reading the schema version from the database ' + \
                  f'{cfg.database.database}. Is that a valid gitbase DB file?'
            qt_message_dialog(msg)
            sys.exit()

        if db_ver > Constants.db_version:
            msg = f'The application is too old to read the database ' + \
                  f'{cfg.database.database}. The database schema version is {db_ver}, ' + \
                  f'but the application can only handle version {Constants.db_version}. ' + \
                  f'You probably should update your application.'
            qt_message_dialog(msg)
            sys.exit()

        if db_ver < Constants.db_version:
            msg = f'The database {cfg.database.database} is too old. The database schema ' + \
                  f'version is {db_ver}, but the application can only handle version ' + \
                  f'{Constants.db_version}. Your probably should update the database schema.'
            qt_message_dialog(msg)
            sys.exit()

        self.database.setDatabaseName(cfg.database.database)
        self.database.open()

        # patient table
        # self.patient_model = QtSql.QSqlTableModel(db=self.database)
        self.patient_model = NonLazyQSqlTableModel(db=self.database)
        # turn on foreign key support (necessary for cascade)
        self.patient_model.database().exec('PRAGMA foreign_keys = ON')
        self.patient_model.setTable('patients')
        self.patient_model.select()
        # set more readable column headers; order must match SQL schema
        col_hdrs = ['ID', 'First name', 'Last name', 'SSN', 'Patient code', 'Diagnosis']
        for k, hdr in enumerate(col_hdrs):
            self.patient_model.setHeaderData(k, QtCore.Qt.Horizontal, hdr)
        # filter
        self.patient_filter = MultiColumnFilter(self)
        self.patient_filter.setFilterCaseSensitivity(False)
        self.patient_filter.setSourceModel(self.patient_model)
        # rom table
        # self.rom_model = QtSql.QSqlTableModel(db=self.database)
        self.rom_model = NonLazyQSqlTableModel(db=self.database)
        # turn on foreign key support (necessary for cascade)
        self.rom_model.database().exec('PRAGMA foreign_keys = ON')
        self.rom_model.setTable('roms')
        self.rom_model.select()
        # the ROM view
        # NB: lot of view properties are set in Qt Designer
        self.tvROM.setModel(self.rom_model)
        # set nicer headers for the ROM columns we want to display, and hide the rest
        self.rom_headers = {
            'TiedotPvm': 'Date of measurement',
            'TiedotMittaajat': 'Personnel',
        }
        self.rom_show_always = ['Date of measurement', 'Personnel']
        self.rom_show_never = ['rom_id', 'patient_id', 'filename']
        # set headers for some ROM columns
        for k in range(self.rom_model.columnCount()):
            if (
                col := self.rom_model.headerData(k, QtCore.Qt.Horizontal)
            ) in self.rom_headers:
                self.rom_model.setHeaderData(
                    k, QtCore.Qt.Horizontal, self.rom_headers[col]
                )
        self._rom_show_all(False)

        # connect signals
        self.lineEdit.textChanged.connect(self.patient_filter.setFilterFixedString)
        self.btnOpenROM.clicked.connect(lambda x: self._edit_rom())
        self.btnOpenROMExcel.clicked.connect(self._rom_excel_report)
        self.btnOpenROMText.clicked.connect(self._rom_text_report)
        self.btnNewROM.clicked.connect(self._new_rom)
        self.btnDeleteROM.clicked.connect(self._delete_rom)
        self.btnEditPatient.clicked.connect(self._edit_patient)
        self.btnDeletePatient.clicked.connect(self._delete_current_patient)
        self.btnNewPatient.clicked.connect(self._new_patient)
        self.actionQuit.triggered.connect(self.close)
        self.lineEdit.setClearButtonEnabled(True)
        self.tvROM.doubleClicked.connect(lambda x: self._edit_rom())
        self.tvPatient.doubleClicked.connect(self._edit_patient)
        self.cbShowAllROM.stateChanged.connect(self._rom_show_all)
        # the patient view
        self.tvPatient.setModel(self.patient_filter)
        # don't show the internal record id
        self.tvPatient.setColumnHidden(0, True)
        # increase font size (best to do before table resizing)
        self.setStyleSheet('QWidget { font-size: %dpt;}' % cfg.visual.fontsize)
        self.tvPatient.resizeColumnsToContents()
        self.tvPatient.selectionModel().selectionChanged.connect(
            self._patient_row_selected
        )
        self.tvROM.resizeColumnsToContents()
        self.tvPatient.selectRow(0)

        self.msg_db_ready = f'Ready, using database {cfg.database.database}'
        self.statusbar.showMessage(self.msg_db_ready)

    def _rom_show_all(self, show_all):
        """If show_all is True, show all ROM vars in table"""
        for k in range(self.rom_model.columnCount()):
            if show_all:
                if (
                    self.rom_model.headerData(k, QtCore.Qt.Horizontal)
                    not in self.rom_show_never
                ):
                    self.tvROM.setColumnHidden(k, False)
            else:  # show limited
                if (
                    self.rom_model.headerData(k, QtCore.Qt.Horizontal)
                    not in self.rom_show_always
                ):
                    self.tvROM.setColumnHidden(k, True)
        self.tvROM.resizeColumnsToContents()

    @property
    def _current_patient_index(self):
        """Return the source model QModelIndex for currently selected patient"""
        try:
            idx = self.tvPatient.selectedIndexes()[0]
            # data is filtered, so map back to source model
            return idx.model().mapToSource(idx)
        except IndexError:
            return None

    @property
    def _current_patient_row(self):
        """Return the source model row number for currently selected patient"""
        if (idx := self._current_patient_index) is not None:
            return idx.row()

    @staticmethod
    def _record_to_patient(rec):
        """Convert a SQL patient record to a Patient instance"""
        return PatientData(
            rec.value('firstname'),
            rec.value('lastname'),
            rec.value('ssn'),
            rec.value('patient_code'),
            rec.value('diagnosis'),
        )

    @property
    def current_rom_index(self):
        """Return QModelIndex for currently selected ROM"""
        try:
            return self.tvROM.selectedIndexes()[0]
        except IndexError:
            return None

    @property
    def current_rom_id(self):
        """Return the ROM ID value for currently selected ROM"""
        if (rom_idx := self.current_rom_index) is None:
            return None
        return self.rom_model.record(rom_idx.row()).value('rom_id')

    def _edit_patient(self):
        """Edit an existing patient"""
        if self._current_patient_row is None:
            qt_message_dialog('Select a patient first')
            return
        rec = self.patient_model.record(self._current_patient_row)
        patient = self._record_to_patient(rec)
        dlg = PatientEditor(PatientData.is_valid, patient)
        if dlg.exec():
            # pass id to uniquely identify the patient
            self._update_patient(dlg._patient, rec.value('patient_id'))

    def _new_patient(self):
        """Create a new patient"""
        dlg = PatientEditor(self._check_new_patient)
        if not dlg.exec():
            return
        patient_id = self._insert_patient(dlg._patient)
        if patient_id is None:
            return
        self.patient_model.select()
        # clear the filter so that the newly inserted patient is visible
        self.lineEdit.clear()
        # select the newly created patient
        # this is surprisingly hard to do
        for k in range(self.patient_model.rowCount()):
            if self.patient_model.record(k).value('patient_id') == patient_id:
                idx = self.patient_model.index(k, 1, QtCore.QModelIndex())
                idx_filter = self.patient_filter.mapFromSource(idx)
                self.tvPatient.selectionModel().select(
                    idx_filter,
                    QtCore.QItemSelectionModel.ClearAndSelect
                    | QtCore.QItemSelectionModel.Rows,
                )
                self.tvPatient.selectionModel().setCurrentIndex(
                    idx_filter,
                    QtCore.QItemSelectionModel.ClearAndSelect
                    | QtCore.QItemSelectionModel.Rows,
                )
                self.tvPatient.scrollTo(idx_filter)
                break

    def _check_new_patient(self, patient):
        """Check whether patient is valid and can be inserted into database.
        Returns tuple of (status, msg) where status is True or False.
        If status is False, msg gives a reason why the patient is not ok.
        """
        query = self.database.exec('SELECT ssn, patient_code FROM patients')
        while query.next():
            if query.value(0) == patient.ssn:
                return (False, 'Patient with this SSN already exists in database')
            elif query.value(1) == patient.patient_code:
                return (
                    False,
                    'Patient with this patient code already exists in database',
                )
        return patient.is_valid()

    def _update_patient(self, patient: PatientData, patient_id):
        """Update an existing patient record.

        patient is a patient record containing the updated information.
        patient_id is the SQL id of the patient to update.
        """
        query = QtSql.QSqlQuery(self.database)
        query.prepare(
            'UPDATE patients SET firstname = :firstname, lastname = :lastname, '
            'ssn = :ssn, patient_code = :patient_code, diagnosis = :diagnosis '
            'WHERE patient_id = :patient_id'
        )
        for field in fields(patient):
            query.bindValue(':' + field.name, getattr(patient, field.name))
        query.bindValue(':patient_id', patient_id)
        if not query.exec():
            db_failure(query, fatal=False)
        self.patient_model.select()

    def _insert_patient(self, patient: PatientData):
        """Insert a new patient record into the database."""
        query = QtSql.QSqlQuery(self.database)
        query.prepare(
            'INSERT INTO patients (firstname, lastname, ssn, patient_code, diagnosis) '
            'VALUES (:firstname, :lastname, :ssn, :patient_code, :diagnosis)'
        )
        for field in fields(patient):
            query.bindValue(':' + field.name, getattr(patient, field.name))
        if not query.exec():
            db_failure(query, fatal=False)
            return None
        return query.lastInsertId()

    def _delete_current_patient(self):
        if self._current_patient_row is None:
            qt_message_dialog('Select a patient first')
            return
        rec = self.patient_model.record(self._current_patient_row)
        patient_id = rec.value('patient_id')
        firstname, lastname, ssn = (
            rec.value('firstname'),
            rec.value('lastname'),
            rec.value('ssn'),
        )
        msg = "WARNING: are you sure you want to delete the patient\n\n"
        msg += f"{firstname} {lastname}, {ssn}\n\n"
        msg += "and ALL associated measurements? There is no undo."
        if not qt_confirm_dialog(msg):
            return
        # close any ROM dialogs related to this patient
        q = QtSql.QSqlQuery(self.database)
        q.prepare('SELECT (rom_id) FROM roms WHERE patient_id = :patient_id')
        q.bindValue(':patient_id', patient_id)
        q.exec()
        while q.next():
            rom_id = q.value(0)
            if rom_id in self._rom_windows:
                self._rom_windows[rom_id].force_close()
        self.patient_model.removeRow(self._current_patient_row)
        # need to update, otherwise empty rows appear in the view
        self.patient_model.select()
        self.rom_model.select()

    def _edit_rom(self, rom_id=None, newly_created=False):
        """Open a ROM measurement in an instance of the ROM editor.

        Note that multiple ROMs may be open at the same time.
        If rom_id is None, will open the currently selected ROM.
        """
        if rom_id is None and (rom_id := self.current_rom_id) is None:
            qt_message_dialog('Please select a ROM first')
            return
        if rom_id in self._rom_windows:
            qt_message_dialog('This ROM is already open')
            return
        app = EntryApp(self.database, rom_id, newly_created)
        app.closing.connect(self._editor_closing)
        # keep track of editor windows (keyed by rom id number)
        self._rom_windows[rom_id] = app
        app.show()

    def _rom_excel_report(self):
        """Create an Excel report of the current ROM"""
        if (rom_id := self.current_rom_id) is None:
            qt_message_dialog('Please select a ROM first')
            return
        # we use an EntryApp instance to create the report
        # the instance is not shown as a window
        app = EntryApp(self.database, rom_id, False)
        fname = named_tempfile(suffix='.xls')
        try:
            report = app.make_excel_report(cfg.templates.xls)
            report.save(fname)
            self.statusbar.showMessage('Opening report in Excel...')
            _startfile(fname)
        except KeyError as e:
            qt_message_dialog(f'The Excel report template refers to an unknown variable:\n{e}')
        finally:
            app.force_close()
        self.statusbar.showMessage(self.msg_db_ready)

    def _rom_text_report(self):
        """Create a text report of the current ROM"""
        if (rom_id := self.current_rom_id) is None:
            qt_message_dialog('Please select a ROM first')
            return
        # we use an EntryApp instance to create the report
        # the instance is not shown as a window
        app = EntryApp(self.database, rom_id, False)
        fname = named_tempfile(suffix='.txt')
        try:
            report_txt = app.make_text_report(cfg.templates.text)
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(report_txt)
            self.statusbar.showMessage('Opening report in text editor...')
            _startfile(fname)
        except (SyntaxError, NameError) as e:
            qt_message_dialog(f'The report template contains syntax errors:\n{e}')
        except KeyError as e:
            qt_message_dialog(f'The report template refers to an unknown variable:\n{e}')
        finally:
            app.force_close()
        self.statusbar.showMessage(self.msg_db_ready)

    def _new_rom(self):
        """Create a new ROM measurement"""
        if (rec := self.patient_model.record(self._current_patient_row)) is None:
            return
        patient_id = rec.value('patient_id')
        query = QtSql.QSqlQuery(self.database)
        query.prepare('INSERT INTO roms (patient_id) VALUES (:patient_id)')
        query.bindValue(':patient_id', patient_id)
        if not query.exec():
            db_failure(query, fatal=False)
        else:
            self._edit_rom(query.lastInsertId(), newly_created=True)

    def _editor_closing(self, rom_id):
        """Callback for a closing a ROM editor"""
        self._rom_windows.pop(rom_id)
        self.rom_model.select()

    def _delete_rom(self):
        """Delete the selected ROM measurement from database"""
        if (rom_idx := self.current_rom_index) is None:
            qt_message_dialog('Please select a ROM first')
            return
        msg = 'WARNING: are you sure you want to delete this ROM measurement? There is no undo.'
        if qt_confirm_dialog(msg):
            if (rom_id := self.current_rom_id) in self._rom_windows:
                self._rom_windows[rom_id].force_close()
            self.rom_model.removeRow(rom_idx.row())
            self.rom_model.select()

    def _patient_row_selected(self, sel):
        """Callback for row selected on the patient table"""
        # data may sometimes be None, probably due to invalid selection
        if not sel.indexes():
            return
        index = sel.indexes()[0]
        row = index.row()
        if (patient_id := index.sibling(row, 0).data()) is None:
            return
        self.rom_model.setFilter(f'{patient_id=}')
        self.rom_model.select()
        self.tvROM.resizeColumnsToContents()

    def closeEvent(self, event):
        """Confirm and close application."""
        if not self.CONFIRM_EXIT or qt_confirm_dialog('Do you want to exit?'):
            # close all ROM editor windows
            for editor in list(self._rom_windows.values()):
                editor.force_close()
            event.accept()
        else:
            event.ignore()


def main():

    app = QtWidgets.QApplication(sys.argv)
    pdi = PatientDialog()


    def my_excepthook(exc_type, value, tback):
        """Custom exception handler for fatal (unhandled) exceptions.

        Report the exception to the user by a GUI dialog and terminate.
        """
        tb_full = ''.join(traceback.format_exception(exc_type, value, tback))
        msg = f'Oops! An unhandled exception occurred:\n{tb_full}'
        msg += '\nThe application will be closed now.'
        qt_message_dialog(msg)
        sys.__excepthook__(exc_type, value, tback)  # call the default exception handler
        app.quit()

    sys.excepthook = my_excepthook

    pdi.show()
    app.exec()


if __name__ == '__main__':
    main()
