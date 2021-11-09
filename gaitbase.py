# -*- coding: utf-8 -*-
"""
Gait database.

TODO:

    -testing

    -deployment
        -asap
        -package gaitbase
            -supplementary stuff into separate private repo
            -needs desktop icon etc.
        -update liikelaaj package to include SQL version
        -subsequently can run both old version and SQL version
        -old one is for emergencies

    -do we need q.finish() for queries?
"""

from os import stat
import random
from PyQt5 import QtWidgets, QtSql, QtCore, uic
import sys
from pathlib import Path
from dataclasses import dataclass, fields
from copy import copy

from liikelaaj.sql_entryapp import EntryApp
from ulstools.num import check_hetu


def _random_hetu():
    """Generate random Finnish SSN"""
    d = random.randint(1, 28)
    m = random.randint(1, 12)
    y = random.randint(0, 99)
    chr = random.choice('A+-')
    n = random.randint(0, 999)
    ssn = f'{d:02d}{m:02d}{y:02d}{chr}{n:03d}'
    chrs = "0123456789ABCDEFHJKLMNPRSTUVWXY"
    chk = chrs[(int(ssn[:6] + ssn[7:10])) % 31]
    return ssn + chk


def qt_message_dialog(msg):
    """Show message with an 'OK' button."""
    dlg = QtWidgets.QMessageBox()
    # dlg.setWindowTitle(ll_msgs.message_title)
    dlg.setText(msg)
    dlg.addButton(QtWidgets.QPushButton('Ok'), QtWidgets.QMessageBox.YesRole)
    dlg.exec_()


def valid_code(code):
    """Check if patient code is valid"""
    # TODO: might be nicer via regex
    if not code:
        return False
    if code[0] not in 'CDEHM':
        return False
    if '_' not in code:
        return False
    ns, initials = code.split('_')
    try:
        n = int(ns[1:])
    except ValueError:
        return False
    if not 0 <= n <= 9999:
        return False
    if not len(initials) in [2, 3] or not initials.isalpha():
        return False
    return True


@dataclass
class PatientData:
    """A patient record"""

    firstname: str = ''
    lastname: str = ''
    ssn: str = ''
    patient_code: str = ''

    def is_valid(self):
        """Check whether the patient info is valid.

        Returns a tuple of (is_valid, reason).
        """
        if not check_hetu(self.ssn):
            return (False, 'Invalid SSN')
        elif not valid_code(self.patient_code):
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
        inds = (model.index(source_row, k, source_parent) for k in range(1, 5))
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
        uifile = 'edit_patient.ui'
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

    @property
    def patient(self):
        """Return current patient record"""
        self._patient.firstname = self.lnFirstName.text()
        self._patient.lastname = self.lnLastName.text()
        self._patient.ssn = self.lnSSN.text()
        self._patient.patient_code = self.lnPatientCode.text()
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


def _debug_print(msg):
    print(msg)
    sys.stdout.flush()


class PatientDialog(QtWidgets.QMainWindow):
    """Visualize patients and measurements in table views"""

    def __init__(self, parent=None):
        uifile = 'patients.ui'
        super().__init__(parent)
        uic.loadUi(uifile, self)

        self.database = QtSql.QSqlDatabase('QSQLITE')
        self.db_name = r'Y:\patients.db'
        self.database.setDatabaseName(self.db_name)
        self.database.open()

        # patient table
        #self.patient_model = QtSql.QSqlTableModel(db=self.database)
        self.patient_model = NonLazyQSqlTableModel(db=self.database)
        # turn on foreign key support (necessary for cascade)
        self.patient_model.database().exec('PRAGMA foreign_keys = ON')
        self.patient_model.setTable('patients')
        self.patient_model.select()
        # set more readable column headers
        col_hdrs = ['ID', 'First name', 'Last name', 'SSN', 'Patient code']
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
        self._show_limited_rom()
        # connect signals
        self.lineEdit.textChanged.connect(
            self.patient_filter.setFilterFixedString)
        self.btnOpenROM.clicked.connect(lambda x: self._open_rom())
        self.btnNewROM.clicked.connect(self._new_rom)
        self.btnDeleteROM.clicked.connect(self._delete_rom)
        self.btnEditPatient.clicked.connect(self._edit_patient)
        self.btnDeletePatient.clicked.connect(self._delete_current_patient)
        self.btnNewPatient.clicked.connect(self._new_patient)
        self.lineEdit.setClearButtonEnabled(True)
        self.tvROM.doubleClicked.connect(lambda x: self._open_rom())
        self.tvPatient.doubleClicked.connect(self._edit_patient)
        self.cbShowAllROM.stateChanged.connect(self._rom_show_toggle)
        # the patient view
        self.tvPatient.setModel(self.patient_filter)
        # don't show the internal record id
        self.tvPatient.setColumnHidden(0, True)
        self.tvPatient.resizeColumnsToContents()
        self.tvPatient.selectionModel().currentRowChanged.connect(
            self._patient_row_selected
        )
        self.tvROM.resizeColumnsToContents()
        self.tvPatient.selectRow(0)
        self.editors = dict()

    def _rom_show_toggle(self, state):
        if state:
            self._show_all_rom()
        else:
            self._show_limited_rom()

    def _show_all_rom(self):
        """Show all ROM vars"""
        for k in range(self.rom_model.columnCount()):
            if self.rom_model.headerData(k, QtCore.Qt.Horizontal) not in self.rom_show_never:
                self.tvROM.setColumnHidden(k, False)
        self.tvROM.resizeColumnsToContents()

    def _show_limited_rom(self):
        """Show limited ROM vars"""
        for k in range(self.rom_model.columnCount()):
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
        )

    @property
    def _current_rom_index(self):
        """Return QModelIndex for currently selected ROM"""
        try:
            return self.tvROM.selectedIndexes()[0]
        except IndexError:
            return None

    def _edit_patient(self):
        """Edit an existing patient"""
        if (rec := self.patient_model.record(self._current_patient_row)) is None:
            return
        patient = self._record_to_patient(rec)
        dlg = PatientEditor(PatientData.is_valid, patient)
        if dlg.exec():
            # pass id to uniquely identify the patient
            self._update_patient(dlg._patient, rec.value('patient_id'))

    def _new_patient(self):
        """Create a new patient"""
        dlg = PatientEditor(self._check_new_patient)
        if dlg.exec():
            self._insert_patient(dlg._patient)

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
        q.prepare('UPDATE patients SET firstname = :firstname, lastname = :lastname, ssn = :ssn, patient_code = :patient_code WHERE patient_id = :patient_id')
        for field in fields(p):
            q.bindValue(':' + field.name, getattr(p, field.name))
        q.bindValue(':patient_id', patient_id)
        if not q.exec():
            err = q.lastError().databaseText()
            raise RuntimeError(
                f'Could not update patient record. SQL error: {err}')
        self.patient_model.select()

    def _insert_patient(self, p):
        """Insert a Patient instance into the database"""
        q = QtSql.QSqlQuery(self.database)
        q.prepare(
            'INSERT INTO patients (firstname, lastname, ssn, patient_code) VALUES (:firstname, :lastname, :ssn, :patient_code)')
        for field in fields(p):
            q.bindValue(':' + field.name, getattr(p, field.name))
        if not q.exec():
            err = q.lastError().databaseText()
            raise RuntimeError(
                f'Could not insert patient record. SQL error: {err}')
        self.patient_model.select()

    def _delete_current_patient(self):
        if (rec := self.patient_model.record(self._current_patient_row)) is None:
            return
        patient_id = rec.value('patient_id')
        msg = f"WARNING: are you sure you want to delete the patient and ALL associated measurements? There is no undo."
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

    def _open_rom(self, rom_id=None):
        """Open the selected ROM measurement in an editor.

        If rom_id is None, will open the currently selected ROM.
        """
        if rom_id is None:
            if self._current_rom_index is None:
                return
            rom_idx = self._current_rom_index
            rom_id = self.rom_model.record(rom_idx.row()).value('rom_id')
        app = EntryApp(self.database, rom_id)
        app.closing.connect(self._editor_closing)
        # keep tracks of editor windows (keyed by rom id number)
        self.editors[rom_id] = app
        app.show()

    def _new_rom(self):
        """Create a new ROM measurement"""
        if (rec := self.patient_model.record(self._current_patient_row)) is None:
            return
        patient_id = rec.value('patient_id')
        q = QtSql.QSqlQuery(self.database)
        q.prepare(
            'INSERT INTO roms (patient_id) VALUES (:patient_id)')
        q.bindValue(':patient_id', patient_id)
        if not q.exec():
            err = q.lastError().databaseText()
            raise RuntimeError(
                f'Could not insert ROM record. SQL error: {err}')
        self._open_rom(q.lastInsertId())

    def _editor_closing(self, id):
        """Callback for a closing a ROM editor"""
        self.editors.pop(id)
        self.rom_model.select()

    def _delete_rom(self):
        """Delete the selected ROM measurement from database"""
        if (rom_idx := self._current_rom_index) is None:
            return
        msg = f"WARNING: are you sure you want to delete this ROM measurement? There is no undo."
        if qt_confirm_dialog(msg):
            rom_id = self.rom_model.record(rom_idx.row()).value('rom_id')
            if rom_id in self.editors:
                self.editors[rom_id].force_close()
            self.rom_model.removeRow(rom_idx.row())
            self.rom_model.select()

    def _patient_row_selected(self, index):
        """Callback for row selected on the patient table"""
        # data may sometimes be None, probably due to invalid selection
        if (patient_id := index.siblingAtColumn(0).data()) is None:
            return
        self.rom_model.setFilter(f'{patient_id=}')
        self.rom_model.select()
        self.tvROM.resizeColumnsToContents()

    def closeEvent(self, event):
        """Confirm and close application."""
        if qt_confirm_dialog('Do you want to exit?'):
            # close all ROM editor windows
            for ed in list(self.editors.values()):
                ed.force_close()
            event.accept()
        else:
            event.ignore()


def main():
    app = QtWidgets.QApplication(sys.argv)
    pdi = PatientDialog()
    pdi.show()
    app.exec()


if __name__ == '__main__':
    main()
