# -*- coding: utf-8 -*-
"""

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
from .widgets import CheckableSpinBox, DegLineEdit, MyLineEdit, message_dialog
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
        uifile = resource_filename('gaitbase', 'tabbed_design_sql.ui')
        uic.loadUi(uifile, self)
        self.confirm_close = True  # used to implement force close
        self.init_widgets()
        self.data = {}
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
            self.lnTiedotPvm.setText(datestr)
            # for a newly created entry, initialize the database row w/ default values
            self.values_changed(self.lnTiedotPvm)
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
            msg = 'Could not read all variables from database. '
            msg += 'This may be due to a mismatch between the UI widgets ' 
            msg += 'and the database schema.'
        if fatal:
            raise RuntimeError(msg)
        else:
            message_dialog(msg)

    @pyqt_disable_autoconv
    def select(self, thevars):
        """Perform select on current ROM row to get data.
        thevars is a list of desired variables.
        Will return a list of QVariant objects.
        Use QVariant().value() to get the values.
        """
        query = QSqlQuery(self.database)
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
        patient_id = self.select(['patient_id'])[0].value()
        query = QSqlQuery(self.database)
        thevars = ['firstname', 'lastname', 'ssn', 'patient_code', 'diagnosis']
        varlist = ','.join(thevars)
        query.prepare(f'SELECT {varlist} FROM patients WHERE patient_id = :patient_id')
        query.bindValue(':patient_id', patient_id)
        if not query.exec() or not query.first():
            self.db_failure(query, fatal=True)
        for k, var in enumerate(thevars):
            val = query.value(k)
            widget_name = 'rdonly_' + var
            self.__dict__[widget_name].setText(val)
            self.__dict__[widget_name].setEnabled(False)

    def get_patient_id_data(self):
        """Get patient id data from the read-only fields as a dict.

        In the SQL version, the patient data is not part of ROM measurements
        anymore, instead residing in the patients table. The returned keys are
        identical to the old (standalone) version. Mostly for purposes of
        reporting, which expects the ID data to be available.
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

    def init_widgets(self):
        """Make a dict of our input widgets and install some callbacks and
        convenience methods etc."""
        self.input_widgets = {}

        def spinbox_getval(widget):
            """Return spinbox value"""
            return widget.no_value_text if widget.value() == widget.minimum() else widget.value()

        def spinbox_setval(widget, val):
            """Set spinbox value"""
            val = widget.minimum() if val == widget.no_value_text else val
            widget.setValue(val)

        def checkbox_getval(widget):
            """Return yestext or notext for checkbox enabled/disabled,
            respectively."""
            val = int(widget.checkState())
            if val == 0:
                return widget.no_text
            elif val == 2:
                return widget.yes_text
            else:
                raise RuntimeError(
                    f'Unexpected checkbox value: {val} for {widget.objectName()}'
                )

        def checkbox_setval(widget, val):
            """Set checkbox value to enabled for val == yestext and
            disabled for val == notext"""
            if val == widget.yes_text:
                widget.setCheckState(2)
            elif val == widget.no_text:
                widget.setCheckState(0)
            else:
                raise RuntimeError(
                    f'Unexpected checkbox entry value: {val} for {widget.objectName()}'
                )

        def combobox_getval(widget):
            """Get combobox current choice as text"""
            return widget.currentText()

        def combobox_setval(widget, val):
            """Set combobox value according to val (unicode) (must be one of
            the combobox items)"""
            idx = widget.findText(val)
            if idx >= 0:
                widget.setCurrentIndex(idx)
            else:
                raise ValueError(f'Tried to set combobox to invalid value {val}')

        def keyPressEvent_resetOnEsc(obj, event):
            """Special event handler for spinboxes. Resets value (sets it
            to minimum) when Esc is pressed."""
            if event.key() == QtCore.Qt.Key_Escape:
                obj.setValue(obj.minimum())
            else:
                # delegate the event to the overridden superclass handler
                super(obj.__class__, obj).keyPressEvent(event)

        # Change lineEdit to custom one for spinboxes. This cannot be done in
        # the main widget loop below, because the old QLineEdits get destroyed in
        # the process (by Qt) and the loop then segfaults while trying to
        # dereference them (the loop collects all QLineEdits at the start).
        # Also install special keypress event handler. """
        for widget in self.findChildren((QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox)):
            wname = widget.objectName()
            if wname[:2] == 'sp':
                widget.setLineEdit(MyLineEdit())
                widget.keyPressEvent = lambda event, w=widget: keyPressEvent_resetOnEsc(w, event)

        # CheckableSpinBoxes get a special LineEdit that catches space
        # and mouse press events

        for widget in self.findChildren(CheckableSpinBox):
            widget.degSpinBox.setLineEdit(DegLineEdit())

        allwidgets = self.findChildren(QtWidgets.QWidget)

        def _weight_normalize(widget):
            """Auto calculate callback for weight normalized widgets"""
            val, weight = (w.getVal() for w in widget._autoinputs)
            noval = Constants.spinbox_novalue_text
            widget.setVal(noval if val == noval or weight == noval else val / weight)

        # Autowidgets are special widgets with automatically computed values.
        # They must have an ._autocalculate() method which updates the widget
        # and ._autoinputs list which lists the necessary input widgets.
        self.autowidgets = list()
        weight_widget = self.spAntropPaino
        for widget in allwidgets:
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

        # set various widget convenience methods/properties
        # input widgets are specially named and will be automatically
        # collected into a dict
        for widget in allwidgets:
            wname = widget.objectName()
            wsave = True
            # w.unit returns the unit for each input (may change dynamically)
            widget.unit = lambda: ''
            if wname[:2] == 'sp':  # spinbox or doublespinbox
                # -lambdas need default arguments because of late binding
                # -lambda expression needs to consume unused 'new value' arg,
                # therefore two parameters (except for QTextEdit...)
                widget.valueChanged.connect(lambda x, w=widget: self.values_changed(w))
                widget.no_value_text = Constants.spinbox_novalue_text
                widget.setVal = lambda val, w=widget: spinbox_setval(w, val)
                widget.getVal = lambda w=widget: spinbox_getval(w)
                widget.unit = lambda w=widget: w.suffix() if isint(w.getVal()) else ''
            elif wname[:2] == 'ln':  # lineedit
                # for text editors, do not perform data updates on every value change...
                # w.textChanged.connect(lambda x, w=w: self.values_changed(w))
                widget.setVal = widget.setText
                widget.getVal = lambda w=widget: w.text().strip()
                # instead, update values when focus is lost (editing completed)
                widget.installEventFilter(self)
            elif wname[:2] == 'cb':  # combobox
                widget.currentIndexChanged.connect(lambda x, w=widget: self.values_changed(w))
                widget.setVal = lambda val, w=widget: combobox_setval(w, val)
                widget.getVal = lambda w=widget: combobox_getval(w)
            elif wname[:3] == 'cmt':  # comment text field
                # for text editors, do not perform data updates on every value change...
                # w.textChanged.connect(lambda w=w: self.values_changed(w))
                widget.setVal = widget.setPlainText
                widget.getVal = lambda w=widget: w.toPlainText().strip()
                # instead, update values when focus is lost (editing completed)
                widget.installEventFilter(self)
            elif wname[:2] == 'xb':  # checkbox
                widget.stateChanged.connect(lambda x, w=widget: self.values_changed(w))
                widget.yes_text = Constants.checkbox_yestext
                widget.no_text = Constants.checkbox_notext
                widget.setVal = lambda val, w=widget: checkbox_setval(w, val)
                widget.getVal = lambda w=widget: checkbox_getval(w)
            elif wname[:3] == 'csb':  # CheckableSpinBox
                widget.valueChanged.connect(lambda w=widget: self.values_changed(w))
                widget.getVal = widget.value
                widget.setVal = widget.setValue
                widget.unit = lambda w=widget: w.getSuffix() if isint(w.getVal()) else ''
            else:
                wsave = False
            if wsave:
                self.input_widgets[wname] = widget

        # slot called on tab change
        self.maintab.currentChanged.connect(self.page_change)

        """ First widget of each page. This is used to do focus/selectall on
        the 1st widget on page change so that data can be entered immediately.
        Only needed for spinbox / lineedit widgets. """
        self.firstwidget = dict()
        # TODO: check/fix
        self.firstwidget[self.tabTiedot] = self.rdonly_firstname
        self.firstwidget[self.tabKysely] = self.lnKyselyPaivittainenMatka
        self.firstwidget[self.tabAntrop] = self.spAntropAlaraajaOik
        self.firstwidget[self.tabLonkka] = self.csbLonkkaFleksioOik
        self.firstwidget[self.tabNilkka] = self.csbNilkkaSoleusCatchOik
        self.firstwidget[self.tabPolvi] = self.csbPolviEkstensioVapOik
        self.firstwidget[self.tabIsokin] = self.spIsokinPolviEkstensioOik
        self.firstwidget[self.tabVirheas] = self.spVirheasAnteversioOik
        self.firstwidget[self.tabTasap] = self.spTasapOik
        self.total_widgets = len(self.input_widgets)

        self.statusbar.showMessage(Finnish.ready.format(n=self.total_widgets))

        """ Set up widget -> varname translation dict. Variable names
        are derived by removing 2-3 leading characters (indicating widget type)
        from widget names (except for comment box variables cmt* which are
        identical with widget names).
        """
        self.widget_to_var = dict()
        for wname in self.input_widgets:
            if wname[:3] == 'cmt':
                varname = wname
            elif wname[:3] == 'csb':  # custom widget
                varname = wname[3:]
            else:
                varname = wname[2:]
            self.widget_to_var[wname] = varname

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
            newval = widget.getVal()
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
        pdata = self.get_patient_id_data() | self.data
        fn = pdata['TiedotID']
        fn += '_'
        fn += ''.join(reversed(pdata['TiedotNimi'].split()))
        fn += '_'
        fn += datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        fn += '.json'
        return Constants.json_backup_path / fn

    def dump_json(self, fname):
        """Save data into given file in utf-8 encoding"""
        # ID data is not updated from widgets in the SQL version, so get it separately
        rdata = self.data | self.get_patient_id_data()
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(json.dumps(rdata, ensure_ascii=False, indent=True, sort_keys=True))

    def make_txt_report(self, template, include_units=True):
        """Create text report from current data"""
        data = self.data_with_units if include_units else self.data
        # ID data is not updated from widgets in the SQL version, so get it separately
        rdata = data | self.get_patient_id_data()
        rep = reporter.Report(rdata, self.vars_default)
        return rep.make_text_report(template)

    def make_excel_report(self, xls_template):
        """Create Excel report from current data"""
        # ID data is not updated from widgets in the SQL version, so get it separately
        rdata = self.data | self.get_patient_id_data()
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
            widget.setVal(self.data[varname])
        self.do_update_data = True

    def read_forms(self):
        """Read self.data from widget inputs. Usually not needed, since
        it's updated automatically."""
        for wname, widget in self.input_widgets.items():
            var = self.widget_to_var[wname]
            self.data[var] = widget.getVal()
