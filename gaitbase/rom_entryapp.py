# -*- coding: utf-8 -*-
"""
Gaitbase app for entering ROM values.

@author: Jussi (jnu@iki.fi)
"""

import datetime
import json
import logging

import sip
from pkg_resources import resource_filename
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtSql import QSqlQuery

from . import reporter
from .config import cfg
from .constants import Constants, Finnish
from .widgets import DegLineEdit, MyLineEdit, message_dialog, keyPressEvent_resetOnEsc
from .utils import isint

logger = logging.getLogger(__name__)


def pyqt_disable_autoconv(func):
    """Decorator to disable Qt type autoconversion for a function.

    PyQt functions decorated with this will return QVariants from many Qt
    functions, instead of native Python types. The QVariants then need to be
    converted manually, often using value().
    """

    def wrapper(*args, **kwargs):
        sip.enableautoconversion(QtCore.QVariant, False)
        res = func(*args, **kwargs)
        sip.enableautoconversion(QtCore.QVariant, True)
        return res

    return wrapper


class EntryApp(QtWidgets.QMainWindow):
    """Data entry application"""

    # this signal will be emitted when the window is closing
    closing = QtCore.pyqtSignal(object)

    def __init__(self, database=None, rom_id=None, newly_created=None):
        super().__init__()
        # load user interface made with Qt Designer
        uifile = resource_filename('gaitbase', 'rom_entryapp.ui')
        uic.loadUi(uifile, self)
        self.confirm_close = True  # used to implement force close
        self.input_widgets = dict()
        self._init_widgets()
        self.data = dict()
        self.read_forms()  # read default data from widgets
        self.data_empty = self.data.copy()
        # whether to update internal dict of variables on input changes
        self.do_update_data = True
        self.database = database
        self.rom_id = rom_id
        self.newly_created = newly_created
        if database is not None:
            # the read only fields are uneditable, they reside in the patients table
            self.init_readonly_fields()
        if newly_created:
            # automatically set the date field
            datestr = datetime.datetime.now().strftime('%d.%m.%Y')
            self.dataTiedotPvm.setText(datestr)
            # for a newly created entry, initialize the database row w/ default values
            self.values_changed(self.dataTiedotPvm)
        elif database is not None:
            # for existing entry, read values from database
            self._read_data()
        self.BACKUP_NEW_ROMS = True  # also dump new ROMs into JSON files

    def force_close(self):
        """Force close without confirmation"""
        self.confirm_close = False
        self.close()

    def db_failure(self, query, fatal=True):
        """Handle database failures"""
        err = query.lastError().databaseText()
        if err:
            msg = f'Got a database error: "{err}"\n'
            msg += 'In case of a locking error, close all other applications '
            msg += 'that may be using the database, and try again.'
        else:
            # empty error seems to occur when all table columns can not be read
            msg = 'Could not read all variables from database. '
            msg += 'This may be due to a mismatch between the UI widgets '
            msg += 'and the database schema.'
        if fatal:
            raise RuntimeError(msg)
        else:
            message_dialog(msg)

    @pyqt_disable_autoconv
    def select(self, thevars):
        """Do select() on current ROM row to get data.

        thevars is a list of desired variables. Returns a tuple of QVariant
        objects. Afterwards, use QVariant.value() to get the actual values.
        """
        query = QSqlQuery(self.database)
        # form a SQL query for desired variables
        varlist = ','.join(thevars)
        query.prepare(f'SELECT {varlist} FROM roms WHERE rom_id = :rom_id')
        query.bindValue(':rom_id', self.rom_id)
        if not query.exec() or not query.first():
            self.db_failure(query, fatal=True)
        results = tuple(query.value(k) for k in range(len(thevars)))
        return results

    def update_rom(self, thevars, values):
        """Update ROM row with a list of fields and corresponding values"""
        if not len(thevars) == len(values):
            raise ValueError('Arguments need to be of equal length')
        query = QSqlQuery(self.database)
        varlist = ','.join(f'{var} = :{var}' for var in thevars)
        query.prepare(f'UPDATE roms SET {varlist} WHERE rom_id = :rom_id')
        query.bindValue(':rom_id', self.rom_id)
        for var, val in zip(thevars, values):
            query.bindValue(f':{var}', val)
        if not query.exec():
            # it's possible that locking failures may occur here, so make them non-fatal
            self.db_failure(query, fatal=False)

    def init_readonly_fields(self):
        """Fill the read-only patient info widgets"""
        patient_id = self.select(['patient_id'])[0].value()  # SQL id of current patient
        thevars = ['firstname', 'lastname', 'ssn', 'patient_code', 'diagnosis']
        varlist = ','.join(thevars)
        query = QSqlQuery(self.database)
        query.prepare(f'SELECT {varlist} FROM patients WHERE patient_id = :patient_id')
        query.bindValue(':patient_id', patient_id)
        if not query.exec() or not query.first():
            self.db_failure(query, fatal=True)
        for k, var in enumerate(thevars):
            val = query.value(k)
            widget_name = 'rdonly_' + var
            self.__dict__[widget_name].setText(val)
            self.__dict__[widget_name].setEnabled(False)

    def get_patient_data(self):
        """Get patient id data from the read-only fields as a dict.

        In the SQL version, the patient data is not part of ROM measurements
        anymore, instead residing in the patients table. The returned keys are
        identical to the old (standalone) version. This is mostly for purposes
        of reporting, which expects the ID data to be available.
        """
        return {
            'TiedotID': self.rdonly_patient_code.text(),
            'TiedotNimi': f'{self.rdonly_firstname.text()} {self.rdonly_lastname.text()}',
            'TiedotHetu': self.rdonly_ssn.text(),
            'TiedotDiag': self.rdonly_diagnosis.text(),
        }

    def eventFilter(self, source, event):
        """Captures the FocusOut event for text widgets.

        The idea is to perform data updates when widget focus is lost.
        """
        if event.type() == QtCore.QEvent.FocusOut:
            self.values_changed(source)
        return super().eventFilter(source, event)

    @staticmethod
    def get_value(widget):
        """Get the value from a data input widget"""
        widget_class = widget.__class__.__name__

        if widget_class in ('QSpinBox', 'QDoubleSpinBox'):
            if widget.value() == widget.minimum():
                val = widget.no_value_text
            else:
                val = widget.value()

        elif widget_class == 'QLineEdit':
            val = widget.text().strip()

        elif widget_class == 'QCheckBox':
            state = int(widget.checkState())
            if state == 0:
                val = widget.no_text
            elif state == 2:
                val = widget.yes_text
            else:
                raise RuntimeError('unexpected checkbox value')

        elif widget_class == 'QComboBox':
            val = widget.currentText()

        elif widget_class == 'QTextEdit':
            val = widget.toPlainText().strip()

        elif widget_class == 'CheckableSpinBox':
            val = widget.value()

        else:
            raise RuntimeError(f'Invalid class of input widget: {widget_class}')
        return val

    @staticmethod
    def set_value(widget, value):
        """Set the value of a data input widget"""
        widget_class = widget.__class__.__name__

        if widget_class in ('QSpinBox', 'QDoubleSpinBox'):
            if value == widget.no_value_text:
                value = widget.minimum()
            widget.setValue(value)

        elif widget_class == 'QLineEdit':
            widget.setText(value)

        elif widget_class == 'QCheckBox':
            if value == widget.yes_text:
                widget.setCheckState(2)
            elif value == widget.no_text:
                widget.setCheckState(0)
            else:
                raise RuntimeError(f'Unexpected checkbox value: {value}')

        elif widget_class == 'QComboBox':
            idx = widget.findText(value)
            if idx >= 0:
                widget.setCurrentIndex(idx)
            else:
                raise RuntimeError(f'Invalid combobox value: {value}')

        elif widget_class == 'QTextEdit':
            widget.setPlainText(value)

        elif widget_class == 'CheckableSpinBox':
            widget.setValue(value)

        else:
            raise RuntimeError(f'Invalid class of input widget: {widget_class}')

    def _init_widgets(self):
        """Init and record the input widgets.

        Also installs some convenience methods, etc.
        """

        # collect all widgets (whether data input widgets or something else)
        allwidgets = self.findChildren(QtWidgets.QWidget)
        # data input widgets
        data_widgets = [w for w in allwidgets if w.objectName()[:4] == 'data']

        def _weight_normalize(widget):
            """Auto calculate callback for weight normalized widgets"""
            val, weight = (self.get_value(w) for w in widget._autoinputs)
            noval = Constants.spinbox_novalue_text
            if val == noval or weight == noval:
                self.set_value(widget, noval)
            else:
                self.set_value(widget, val / weight)

        # Autowidgets are special widgets with automatically computed values.
        # They must have an ._autocalculate() method which updates the widget
        # and ._autoinputs list which lists the necessary input widgets.
        self.autowidgets = list()
        weight_widget = self.dataAntropPaino
        for widget in data_widgets:
            wname = widget.objectName()
            # handle the 'magic' autowidgets with weight normalized data
            if wname[-4:] == 'Norm':
                self.autowidgets.append(widget)
                # corresponding unnormalized widget
                wname_unnorm = wname.replace('Norm', 'NormUn')
                w_unnorm = self.__dict__[wname_unnorm]
                widget._autoinputs = [w_unnorm, weight_widget]
                widget._autocalculate = lambda w=widget: _weight_normalize(w)

        # autowidget values cannot be directly modified
        for widget in self.autowidgets:
            widget.setEnabled(False)

        # set various widget convenience methods/properties, collect input
        # widgets into a dict
        # NOTE: this loop will implicitly cause destruction of certain widgets
        # (e.g. QLineEdits) by replacing them with new ones. Do not reuse the
        # 'allwidgets' variable after this loop.
        for widget in data_widgets:
            wname = widget.objectName()
            # w.unit returns the unit for each input (may change dynamically)
            widget.unit = lambda: ''
            widget_class = widget.__class__.__name__
            if widget_class in ('QSpinBox', 'QDoubleSpinBox'):
                # -lambdas need default arguments because of late binding
                # -lambda expression needs to consume unused 'new value' arg,
                # therefore two parameters (except for QTextEdit...)
                widget.valueChanged.connect(lambda x, w=widget: self.values_changed(w))
                widget.no_value_text = Constants.spinbox_novalue_text
                widget.unit = (
                    lambda w=widget: w.suffix() if isint(self.get_value(w)) else ''
                )
                widget.setLineEdit(MyLineEdit())
                widget.keyPressEvent = lambda event, w=widget: keyPressEvent_resetOnEsc(
                    w, event
                )
            elif widget_class == 'QLineEdit':
                # for text editors, do not perform data updates on every value change...
                # w.textChanged.connect(lambda x, w=w: self.values_changed(w))
                # instead, update values when focus is lost (editing completed)
                widget.installEventFilter(self)
            elif widget_class == 'QComboBox':
                widget.currentIndexChanged.connect(
                    lambda x, w=widget: self.values_changed(w)
                )
            elif widget_class == 'QTextEdit':
                # for text editors, do not perform data updates on every value change...
                # w.textChanged.connect(lambda w=w: self.values_changed(w))
                # instead, update values when focus is lost (editing completed)
                widget.installEventFilter(self)
            elif widget_class == 'QCheckBox':
                widget.stateChanged.connect(lambda x, w=widget: self.values_changed(w))
                widget.yes_text = Constants.checkbox_yestext
                widget.no_text = Constants.checkbox_notext
            elif widget_class == 'CheckableSpinBox':
                widget.valueChanged.connect(lambda w=widget: self.values_changed(w))
                widget.unit = (
                    lambda w=widget: w.getSuffix() if isint(self.get_value(w)) else ''
                )
                widget.degSpinBox.setLineEdit(DegLineEdit())
            else:
                raise RuntimeError(f'Invalid type of data input widget: {widget_class}')
            self.input_widgets[wname] = widget

        # slot called on tab change
        self.maintab.currentChanged.connect(self.page_change)

        # Set first widget (top widget) of each page. This is used to do
        # focus/selectall on the 1st widget on page change, so that data can be
        # entered immediately.
        self.firstwidget = dict()
        self.firstwidget[self.tabTiedot] = self.rdonly_firstname
        self.firstwidget[self.tabKysely] = self.dataKyselyPaivittainenMatka
        self.firstwidget[self.tabAntrop] = self.dataAntropAlaraajaOik
        self.firstwidget[self.tabLonkka] = self.dataLonkkaFleksioOik
        self.firstwidget[self.tabNilkka] = self.dataNilkkaSoleusCatchOik
        self.firstwidget[self.tabPolvi] = self.dataPolviEkstensioVapOik
        self.firstwidget[self.tabIsokin] = self.dataIsokinPolviEkstensioOik
        self.firstwidget[self.tabVirheas] = self.dataVirheasAnteversioOik
        self.firstwidget[self.tabTasap] = self.dataTasapOik
        self.total_widgets = len(self.input_widgets)

        # widget to varname translation dict
        self.widget_to_var = dict()
        for wname in self.input_widgets:
            varname = wname[4:]
            self.widget_to_var[wname] = varname

        self.statusbar.showMessage(Finnish.ready.format(n=self.total_widgets))

        # try to increase font size
        self.setStyleSheet(f'QWidget {{ font-size: {cfg.visual.fontsize}pt;}}')

        # FIXME: make sure we always start on 1st tab

    @property
    def units(self):
        """Return dict indicating the units for each variable. The units may change dynamically depending on the values entered"""
        units = dict()
        for wname, widget in self.input_widgets.items():
            varname = self.widget_to_var[wname]
            units[varname] = widget.unit()
        return units

    @property
    def vars_default(self):
        """Return a list of variables that are at their default (unmodified)
        state."""
        return [key for key in self.data if self.data[key] == self.data_empty[key]]

    def do_close(self, event):
        """The actual closing ritual"""
        # XXX: we may want to undo the database entry, if no values were entered
        # if self.n_modified() == 0:
        # XXX: if ROM was newly created, we also create JSON for backup purposes
        # this is for the "beta phase"  only
        if self.BACKUP_NEW_ROMS and self.newly_created:
            # XXX: this will overwrite existing files, but they should be uniquely named due to
            # timestamp in the filename
            fname = self._compose_json_filename()
            try:
                self.dump_json(fname)
            except IOError:  # ignore errors for now
                pass
        self.closing.emit(self.rom_id)
        event.accept()

    def closeEvent(self, event):
        """Confirm and close application."""
        # Since some widgets update only when losing focus, we want to make sure
        # they lose focus before closing the app, so that data is updated.
        self.setFocus()
        if not self.confirm_close:  # force close
            self.do_close(event)
        else:  # closing via ui
            status_ok, msg = self._validate_outputs()
            if status_ok:
                self.do_close(event)
            else:
                message_dialog(msg)
                event.ignore()

    def _validate_date(self, datestr):
        """Validate a date of dd.mm.yyyy"""
        try:
            datetime.datetime.strptime(datestr, '%d.%m.%Y')
            return True
        except ValueError:
            return False

    def _validate_outputs(self):
        """Validate inputs before closing"""
        date = self.data['TiedotPvm']
        if not self._validate_date(date):
            return False, 'Päivämäärän täytyy olla oikea ja muodossa pp.kk.vvvv'
        else:
            return True, ''

    def values_changed(self, widget):
        """Called whenever value of a widget changes.

        This does several things, most importantly updates the database.
        """
        # find autowidgets that depend on w and update them
        autowidgets_this = [
            widget for widget in self.autowidgets if widget in widget._autoinputs
        ]
        for widget in autowidgets_this:
            widget._autocalculate()
        if self.do_update_data:
            # update internal data dict
            wname = widget.objectName()
            varname = self.widget_to_var[wname]
            newval = self.get_value(widget)
            self.data[varname] = newval
            # perform the corresponding SQL update
            self.update_rom([varname], [newval])

    @property
    def data_with_units(self):
        """Append units to values"""
        return {key: f'{self.data[key]}{self.units[key]}' for key in self.data}

    def _read_data(self):
        """Read input data from database"""
        thevars = list(self.data.keys())
        # get data as QVariants, and ignore NULL ones (which correspond to missing data in database)
        qvals = self.select(thevars)
        record_di = {
            var: qval.value() for var, qval in zip(thevars, qvals) if not qval.isNull()
        }
        self.data = self.data_empty | record_di
        self.restore_forms()

    def _compose_json_filename(self):
        """Make up a JSON filename"""
        pdata = self.get_patient_data() | self.data
        fname = pdata['TiedotID']
        fname += '_'
        fname += ''.join(reversed(pdata['TiedotNimi'].split()))
        fname += '_'
        fname += datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        fname += '.json'
        return Constants.json_backup_path / fname

    def dump_json(self, fname):
        """Save data into given file in utf-8 encoding"""
        # ID data is not updated from widgets in the SQL version, so get it separately
        rdata = self.data | self.get_patient_data()
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(json.dumps(rdata, ensure_ascii=False, indent=True, sort_keys=True))

    def make_txt_report(self, template, include_units=True):
        """Create text report from current data"""
        data = self.data_with_units if include_units else self.data
        # ID data is not updated from widgets in the SQL version, so get it separately
        rdata = data | self.get_patient_data()
        rep = reporter.Report(rdata, self.vars_default)
        return rep.make_text_report(template)

    def make_excel_report(self, xls_template):
        """Create Excel report from current data"""
        # ID data is not updated from widgets in the SQL version, so get it separately
        rdata = self.data | self.get_patient_data()
        rep = reporter.Report(rdata, self.vars_default)
        return rep.make_excel_report(xls_template)

    def n_modified(self):
        """Count modified values."""
        return len([x for x in self.data if self.data[x] != self.data_empty[x]])

    def page_change(self):
        """Callback for tab change"""
        newpage = self.maintab.currentWidget()
        # focus / selectAll on 1st widget of new tab
        if newpage in self.firstwidget:
            widget = self.firstwidget[newpage]
            if widget.isEnabled():
                widget.selectAll()
                widget.setFocus()

    def restore_forms(self):
        """Restore widget input values from self.data. Need to disable widget
        callbacks and automatic data saving while programmatic updating of
        widgets is taking place."""
        self.do_update_data = False
        for wname, widget in self.input_widgets.items():
            varname = self.widget_to_var[wname]
            self.set_value(widget, self.data[varname])
        self.do_update_data = True

    def read_forms(self):
        """Read self.data from widget inputs. Usually not needed, since
        it's updated automatically."""
        for wname, widget in self.input_widgets.items():
            varname = self.widget_to_var[wname]
            self.data[varname] = self.get_value(widget)
