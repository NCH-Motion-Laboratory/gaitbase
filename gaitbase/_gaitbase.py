# -*- coding: utf-8 -*-
"""
Gait database.


TODO:

    -deployment
        -asap
        -package gaitbase
            -supplementary stuff into separate private repo
            -needs desktop icon etc.
        -update liikelaaj package to include SQL version
            -subsequently can run both old version and SQL version
            -old one is for emergencies only
    
    -presentation

    -check Excel and text reports
        -compare Excel reports from SQL vs. from JSON

    -check multiple simultaneous readers/writers

    -could disable patient/ROM buttons if nothing selected

    -proper exception handling (e.g. database locks)
        -also handler for unexpected exceptions

    -check no values entered condition for ROM

    -ROM comparison funcs? (taste of the future)

"""

from PyQt5 import QtWidgets, QtSql, QtCore, uic
import sys
from pathlib import Path
from dataclasses import dataclass, fields
from copy import copy
import datetime
import os
import traceback
from pkg_resources import resource_filename
import configdot
import sys

from liikelaaj.sql_entryapp import EntryApp
from liikelaaj.widgets import message_dialog
from ulstools.num import check_hetu
from ulstools.env import make_shortcut

from .utils import _named_tempfile, validate_code
from .config import cfg


def qt_message_dialog(msg):
    """Show message with an 'OK' button."""
    dlg = QtWidgets.QMessageBox()
    dlg.setWindowTitle('Message')
    dlg.setText(msg)
    dlg.addButton(QtWidgets.QPushButton('Ok'), QtWidgets.QMessageBox.YesRole)
    dlg.exec_()


def make_my_shortcut():
    """Make a desktop shortcut"""
    make_shortcut('gaitbase', 'run_gaitbase.py', title='Gait database')


@dataclass
class PatientData:
    """A patient record"""

    firstname: str = ''
    lastname: str = ''
    ssn: str = ''
    patient_code: str = ''
    diagnosis: str = ''

    def is_valid(self):
        """Check whether the patient info is valid.

        Returns a tuple of (is_valid, reason).
        """
        #return (True, '')  # DEBUG insertion
        if not check_hetu(self.ssn):
            return (False, 'Invalid SSN')
        elif not validate_code(self.patient_code):
            return (False, 'Invalid patient code')
        elif not self.firstname.isalpha():
            return (False, 'Invalid first name')
        elif not self.lastname.isalpha():
            return (False, 'Invalid last name')
        return (True, '')


class NonLazyQSqlTableModel(QtSql.QSqlTableModel):
    """QSqlTableModel without the prefetch feature.

    This works for small tables. The purpose is to prevent SQL locking that
    occurs with prefetch.
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
        """check_patient is a callback which will check that the
        Patient instance is ok and can be inserted into the database.
        If patient is provided, its values will be displayed for editing.
        Otherwise a new patiewt will be created.
        """
        uifile = resource_filename('gaitbase', 'edit_patient.ui')
        super().__init__(parent)
        uic.loadUi(uifile, self)
        self.btnSave.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.patient_check_callback = check_patient
        self._patient = patient or PatientData()
        self._orig_patient = copy(self._patient)
        # set widget default values
        self.lnFirstName.setText(self._patient.firstname)
        self.lnLastName.setText(self._patient.lastname)
        self.lnSSN.setText(self._patient.ssn)
        self.lnPatientCode.setText(self._patient.patient_code)
        self.lnDiagnosis.setText(self._patient.diagnosis)

    @property
    def patient(self):
        """Return current patient record"""
        self._patient.firstname = self.lnFirstName.text()
        self._patient.lastname = self.lnLastName.text()
        self._patient.ssn = self.lnSSN.text()
        self._patient.patient_code = self.lnPatientCode.text()
        self._patient.diagnosis = self.lnDiagnosis.text()
        return self._patient

    def accept(self):
        """Guard for superclass accept - check patient first"""
        p_ok, result = self.patient_check_callback(self.patient)
        if p_ok:
            super().accept()
        else:
            msg = f'Please fix the following errors: {result}'
            qt_message_dialog(msg)

    def reject(self):
        """Guard for superclass reject"""
        if self.patient == self._orig_patient or qt_confirm_dialog(
            'Are you sure you want to cancel changes?'
        ):
            super().reject()


def qt_confirm_dialog(msg):
    """Show dialog with message and Yes and No buttons, return True if confirmed"""
    dlg = QtWidgets.QMessageBox()
    dlg.setWindowTitle('Confirm')
    dlg.setText(msg)
    dlg.addButton(QtWidgets.QPushButton('Yes'), QtWidgets.QMessageBox.YesRole)
    dlg.addButton(QtWidgets.QPushButton('No'), QtWidgets.QMessageBox.NoRole)
    dlg.exec_()
    return dlg.buttonRole(dlg.clickedButton()) == QtWidgets.QMessageBox.YesRole


def db_failure(query, fatal=False):
    """Handle database failures"""
    err = query.lastError().databaseText()
    msg = f'Got a database error: "{err}"'
    msg += '\nIn case of a locking error, close all other applications '
    msg += 'that may be using the database, and try again.'
    if fatal:
        raise RuntimeError(msg)
    else:
        message_dialog(msg)





def _debug_print(msg):
    print(msg)
    sys.stdout.flush()


class PatientDialog(QtWidgets.QMainWindow):
    """Visualize patients and measurements in table views"""

    def __init__(self, parent=None):
        super().__init__(parent)
        uifile = resource_filename('gaitbase', 'patients.ui')
        uic.loadUi(uifile, self)
        self.editors = dict()

        # some configurable stuff
        self.CONFIRM_EXIT = False

        self.database = QtSql.QSqlDatabase('QSQLITE')
        if not Path(cfg.database.database).is_file():
            msg = f'The database {cfg.database.database} does not exist. '
            msg += 'Please set the correct location in the config.'
            message_dialog(msg)
            sys.exit()
        self.database.setDatabaseName(cfg.database.database)
        self.database.open()

        # patient table
        #self.patient_model = QtSql.QSqlTableModel(db=self.database)
        self.patient_model = NonLazyQSqlTableModel(db=self.database)
        # turn on foreign key support (necessary for cascade)
        self.patient_model.database().exec('PRAGMA foreign_keys = ON')
        self.patient_model.setTable('patients')
        self.patient_model.select()
        # set more readable column headers; order must match SQL schema
        col_hdrs = ['ID', 'First name', 'Last name',
                    'SSN', 'Patient code', 'Diagnosis']
        for k, hdr in enumerate(col_hdrs):
            self.patient_model.setHeaderData(k, QtCore.Qt.Horizontal, hdr)
        # filter
        self.patient_filter = MultiColumnFilter(self)
        self.patient_filter.setFilterCaseSensitivity(False)
        self.patient_filter.setSourceModel(self.patient_model)
        # rom table
        #self.rom_model = QtSql.QSqlTableModel(db=self.database)
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
        self.lineEdit.textChanged.connect(
            self.patient_filter.setFilterFixedString)
        self.btnOpenROM.clicked.connect(lambda x: self._edit_rom())
        self.btnOpenROMExcel.clicked.connect(self._rom_excel_report)
        self.btnOpenROMText.clicked.connect(self._rom_text_report)
        self.btnNewROM.clicked.connect(self._new_rom)
        self.btnDeleteROM.clicked.connect(self._delete_rom)
        self.btnEditPatient.clicked.connect(self._edit_patient)
        self.btnDeletePatient.clicked.connect(self._delete_current_patient)
        self.btnNewPatient.clicked.connect(self._new_patient)
        self.lineEdit.setClearButtonEnabled(True)
        self.tvROM.doubleClicked.connect(lambda x: self._edit_rom())
        self.tvPatient.doubleClicked.connect(self._edit_patient)
        self.cbShowAllROM.stateChanged.connect(self._rom_show_all)
        # the patient view
        self.tvPatient.setModel(self.patient_filter)
        # don't show the internal record id
        self.tvPatient.setColumnHidden(0, True)
        self.tvPatient.resizeColumnsToContents()
        self.tvPatient.selectionModel().selectionChanged.connect(
            self._patient_row_selected
        )
        self.tvROM.resizeColumnsToContents()
        self.tvPatient.selectRow(0)


    def _rom_show_all(self, show_all):
        """If show_all is True, show all ROM vars in table"""
        for k in range(self.rom_model.columnCount()):
            if show_all:
                if self.rom_model.headerData(k, QtCore.Qt.Horizontal) not in self.rom_show_never:
                    self.tvROM.setColumnHidden(k, False)
            else:  # show limited
                if self.rom_model.headerData(k, QtCore.Qt.Horizontal) not in self.rom_show_always:
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
            rec.value('diagnosis')
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
            message_dialog('Select a patient first')
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
        id = self._insert_patient(dlg._patient)
        if id is None:
            return
        self.patient_model.select()
        # clear the filter so that the newly inserted patient is visible
        self.lineEdit.clear()
        # select the newly created patient
        # this is surprisingly hard to do
        for k in range(self.patient_model.rowCount()):
            if self.patient_model.record(k).value('patient_id') == id:
                idx = self.patient_model.index(k, 1, QtCore.QModelIndex())
                idx_filter = self.patient_filter.mapFromSource(idx)
                self.tvPatient.selectionModel().select(
                    idx_filter, QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)
                self.tvPatient.selectionModel().setCurrentIndex(
                    idx_filter, QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)
                self.tvPatient.scrollTo(idx_filter)
                break

    def _check_new_patient(self, p):
        """Check whether p is valid and can be inserted into database.
        Returns tuple of (status, msg) where status is True or False.
        If status is False, msg gives a reason why the patient is not ok.
        """
        q = self.database.exec('SELECT ssn, patient_code FROM patients')
        while q.next():
            if q.value(0) == p.ssn:
                return(False, 'Patient with this SSN already exists in database')
            elif q.value(1) == p.patient_code:
                return (False, 'Patient with this patient code already exists in database')
        return p.is_valid()

    def _update_patient(self, p, patient_id):
        """Update an existing patient record"""
        q = QtSql.QSqlQuery(self.database)
        q.prepare('UPDATE patients SET firstname = :firstname, lastname = :lastname, ssn = :ssn, patient_code = :patient_code, diagnosis = :diagnosis WHERE patient_id = :patient_id')
        for field in fields(p):
            q.bindValue(':' + field.name, getattr(p, field.name))
        q.bindValue(':patient_id', patient_id)
        if not q.exec():
            db_failure(q, fatal=False)
        self.patient_model.select()

    def _insert_patient(self, p):
        """Insert a Patient instance into the database."""
        q = QtSql.QSqlQuery(self.database)
        q.prepare(
            'INSERT INTO patients (firstname, lastname, ssn, patient_code, diagnosis) VALUES (:firstname, :lastname, :ssn, :patient_code, :diagnosis)')
        for field in fields(p):
            q.bindValue(':' + field.name, getattr(p, field.name))
        if not q.exec():
            db_failure(q, fatal=False)
            return None
        return q.lastInsertId()

    def _delete_current_patient(self):
        if self._current_patient_row is None:
            message_dialog('Select a patient first')
            return
        rec = self.patient_model.record(self._current_patient_row)
        patient_id = rec.value('patient_id')
        firstname, lastname, ssn = rec.value(
            'firstname'), rec.value('lastname'), rec.value('ssn')
        msg = f"WARNING: are you sure you want to delete the patient\n\n"
        msg += f"{firstname} {lastname}, {ssn}\n\n"
        msg += f"and ALL associated measurements? There is no undo."
        if not qt_confirm_dialog(msg):
            return
        # close any ROM dialogs related to this patient
        q = QtSql.QSqlQuery(self.database)
        q.prepare('SELECT (rom_id) FROM roms WHERE patient_id = :patient_id')
        q.bindValue(':patient_id', patient_id)
        q.exec()
        while q.next():
            rom_id = q.value(0)
            if rom_id in self.editors:
                self.editors[rom_id].force_close()
        self.patient_model.removeRow(self._current_patient_row)
        # need to update, otherwise empty rows appear in the view
        self.patient_model.select()
        self.rom_model.select()

    def _edit_rom(self, rom_id=None, newly_created=False):
        """Open a ROM measurement in an editor.

        If rom_id is None, will open the currently selected ROM.
        """
        if rom_id is None and (rom_id := self.current_rom_id) is None:
            message_dialog('Please select a ROM first')
            return
        if rom_id in self.editors:
            message_dialog('This ROM is already open')
            return
        app = EntryApp(self.database, rom_id, newly_created)
        app.closing.connect(self._editor_closing)
        # keep tracks of editor windows (keyed by rom id number)
        self.editors[rom_id] = app
        app.show()

    def _rom_excel_report(self):
        """Create an Excel report of the current ROM"""
        if (rom_id := self.current_rom_id) is None:
            message_dialog('Please select a ROM first')
            return
        # we use an EntryApp instance to create the report
        # the instance is not shown as a window
        app = EntryApp(self.database, rom_id, False)
        fn = _named_tempfile(suffix='.xls')
        app.make_excel_report().save(fn)
        os.startfile(fn)
        app.force_close()

    def _rom_text_report(self):
        """Create a text report of the current ROM"""
        if (rom_id := self.current_rom_id) is None:
            message_dialog('Please select a ROM first')
            return
        # we use an EntryApp instance to create the report
        # the instance is not shown as a window
        app = EntryApp(self.database, rom_id, False)
        fn = _named_tempfile(suffix='.txt')
        report_txt = app.make_txt_report(app.text_template)
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(report_txt)
        os.startfile(fn)
        app.force_close()

    def _new_rom(self):
        """Create a new ROM measurement"""
        if (rec := self.patient_model.record(self._current_patient_row)) is None:
            return
        patient_id = rec.value('patient_id')
        # autoinsert current date
        datestr = datetime.datetime.now().strftime('%d.%m.%Y')
        q = QtSql.QSqlQuery(self.database)
        q.prepare(
            'INSERT INTO roms (patient_id, TiedotPvm) VALUES (:patient_id, :datestr)')
        q.bindValue(':patient_id', patient_id)
        q.bindValue(':datestr', datestr)
        if not q.exec():
            db_failure(q, fatal=False)
        else:
            self._edit_rom(q.lastInsertId(), newly_created=True)

    def _editor_closing(self, id):
        """Callback for a closing a ROM editor"""
        self.editors.pop(id)
        self.rom_model.select()

    def _delete_rom(self):
        """Delete the selected ROM measurement from database"""
        if (rom_idx := self.current_rom_index) is None:
            message_dialog('Please select a ROM first')
            return
        msg = f"WARNING: are you sure you want to delete this ROM measurement? There is no undo."
        if qt_confirm_dialog(msg):
            if (rom_id := self.current_rom_id) in self.editors:
                self.editors[rom_id].force_close()
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
            for ed in list(self.editors.values()):
                ed.force_close()
            event.accept()
        else:
            event.ignore()


def main():
    app = QtWidgets.QApplication(sys.argv)
    pdi = PatientDialog()

    def my_excepthook(type, value, tback):
        """ Custom exception handler for fatal (unhandled) exceptions:
        report to user via GUI and terminate program. """
        tb_full = ''.join(traceback.format_exception(type, value, tback))
        msg = f'Oops! An unhandled exception occurred: {tb_full}'
        msg += '\nThe application will be closed now.'
        message_dialog(msg)
        sys.__excepthook__(type, value, tback)
        app.quit()

    sys.excepthook = my_excepthook

    pdi.show()
    app.exec()



if __name__ == '__main__':
    main()
