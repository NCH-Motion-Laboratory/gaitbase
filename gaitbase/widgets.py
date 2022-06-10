# -*- coding: utf-8 -*-
"""
Custom widgets, dialogs and related Qt code.
"""

from PyQt5 import QtWidgets, QtCore
from .constants import Constants, Finnish
from .utils import isint


def confirm_dialog(msg):
    """Show yes/no dialog."""
    dlg = QtWidgets.QMessageBox()
    dlg.setText(msg)
    dlg.setWindowTitle(Constants.dialog_title)
    dlg.addButton(
        QtWidgets.QPushButton(Finnish.yes_button), QtWidgets.QMessageBox.YesRole
    )
    dlg.addButton(
        QtWidgets.QPushButton(Finnish.no_button), QtWidgets.QMessageBox.NoRole
    )
    dlg.exec()
    return dlg.buttonRole(dlg.clickedButton())


def message_dialog(msg):
    """Show message with an 'OK' button."""
    dlg = QtWidgets.QMessageBox()
    dlg.setWindowTitle(Constants.dialog_title)
    dlg.setText(msg)
    dlg.addButton(
        QtWidgets.QPushButton(Finnish.ok_button), QtWidgets.QMessageBox.YesRole
    )
    dlg.exec()


def keyPressEvent_resetOnEsc(obj, event):
    """Special event handler for spinboxes. Resets value (sets it
    to minimum) when Esc is pressed."""
    if event.key() == QtCore.Qt.Key_Escape:
        obj.setValue(obj.minimum())
    else:
        # delegate the event to the overridden superclass handler
        super(obj.__class__, obj).keyPressEvent(event)


def get_widget_value(widget):
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


def set_widget_value(widget, value):
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


def get_widget_units(widget):
    """Get units of data associated with widget.
    
    We only return a unit if the widget has a numeric value.
    """
    widget_class = widget.__class__.__name__
    if widget_class in ('QSpinBox', 'QDoubleSpinBox'):
        if isint(get_widget_value(widget)):
            units = widget.suffix()
        else:
            units = ''
    elif widget_class == 'CheckableSpinBox':
        if isint(get_widget_value(widget)):
            units = widget.getSuffix()
        else:
            units = ''
    else:
        # currently no units for other widget types
        units = ''
    return units




class MyLineEdit(QtWidgets.QLineEdit):
    """Custom line edit that selects the input on mouse click."""

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.selectAll()

    def mouseReleaseEvent(self, event):
        """Make drag & release select all too (prevent selection
        of partial text)"""
        super().mouseReleaseEvent(event)
        self.selectAll()


class DegLineEdit(QtWidgets.QLineEdit):
    """Custom line edit for CheckableSpinBox class. Catches space key and
    passes it to CheckableSpinBox."""

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.selectAll()

    def mouseReleaseEvent(self, event):
        """Make drag & release select all too (prevent selection of
        partial text)"""
        super().mouseReleaseEvent(event)
        self.selectAll()

    def keyPressEvent(self, event):
        # pass space key to grandparent (CheckableSpinBox)
        if event.key() == QtCore.Qt.Key_Space:
            self.parent().parent().keyPressEvent(event)
        else:
            super().keyPressEvent(event)


class CheckableSpinBox(QtWidgets.QWidget):
    """Custom widget: Spinbox (degrees) with checkbox, which indicates
    a 'default' value. If the checkbox is checked, disable spinbox, in which
    case value() will return the default value shown next to checkbox
    (defaultText property). Otherwise value() will return the spinbox value.
    setValue() takes either the default value, the 'special value' (not
    measured) or an integer.
    """

    # signal has to be defined here for unclear reasons
    # note that currently the value is not returned by the signal
    # (unlike in the Qt spinbox)
    valueChanged = QtCore.pyqtSignal()
    # for Qt designer
    __pyqtSignals__ = 'valueChanged'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.degSpinBox = QtWidgets.QSpinBox()
        self.degSpinBox.valueChanged.connect(self.valueChanged.emit)
        self.degSpinBox.setMinimumSize(100, 0)

        self.normalCheckBox = QtWidgets.QCheckBox()
        self.normalCheckBox.stateChanged.connect(
            lambda state: self.setSpinBox(not state)
        )

        # default text
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.addWidget(normalLabel, 0, 0)
        layout.addWidget(self.degSpinBox)
        layout.addWidget(self.normalCheckBox)

        # needed for tab order
        self.degSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.normalCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocusProxy(self.degSpinBox)

        # Widget defaults are tailored for this program. For some instances
        # of the widget, these values will be modified already by Qt Designer
        # (in the .ui file), so we set them only here and do not touch them
        # later in the code. If exporting the widget, these can be deleted or
        # set to some other constants.
        self.setDefaultText('NR')
        self.setSuffix('°')
        # the minimum is also the "special" value, which causes the widget to
        # display the SpecialValueText instead of a number
        self.setMinimum(-181)
        self.setMaximum(180)
        self.degSpinBox.setValue(-181)
        self.specialtext = Constants.spinbox_novalue_text
        # this indicates the "not measured" state
        self.degSpinBox.setSpecialValueText(self.specialtext)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.setValue(self.degSpinBox.minimum())
        elif event.key() == QtCore.Qt.Key_Space:
            self.toggleCheckBox()
        else:
            super().keyPressEvent(event)

    """ Set some values as Qt properties, mostly so that they can be easily
    changed from Qt Designer. """

    def setDefaultText(self, text):
        self.normalCheckBox.setText(text)

    def getDefaultText(self):
        return self.normalCheckBox.text()

    def setSuffix(self, text):
        self.degSpinBox.setSuffix(text)

    def getSuffix(self):
        return self.degSpinBox.suffix()

    def setMinimum(self, minval):
        self.degSpinBox.setMinimum(minval)

    def getMinimum(self):
        return self.degSpinBox.minimum()

    def setMaximum(self, maxval):
        self.degSpinBox.setMaximum(maxval)

    def getMaximum(self):
        return self.degSpinBox.maximum()

    defaultText = QtCore.pyqtProperty('QString', getDefaultText, setDefaultText)
    suffix = QtCore.pyqtProperty('QString', getSuffix, setSuffix)
    minimum = QtCore.pyqtProperty('int', getMinimum, setMinimum)
    maximum = QtCore.pyqtProperty('int', getMaximum, setMaximum)

    def value(self):
        if self.normalCheckBox.checkState() == 0:
            val = self.degSpinBox.value()
            if val == self.degSpinBox.minimum():
                return str(self.specialtext)
            else:
                return val
        elif self.normalCheckBox.checkState() == 2:
            return str(self.getDefaultText())

    def setValue(self, val):
        if val == self.getDefaultText():
            self.normalCheckBox.setCheckState(2)
        else:
            self.normalCheckBox.setCheckState(0)
            if val == self.specialtext:
                self.degSpinBox.setValue(self.degSpinBox.minimum())
            else:
                self.degSpinBox.setValue(val)

    def selectAll(self):
        self.degSpinBox.selectAll()

    def setFocus(self):
        self.degSpinBox.setFocus()

    def setSpinBox(self, state):
        """Enables or disables spinbox input. Also emit valueChanged."""
        if state and not self.isEnabled():
            self.degSpinBox.setEnabled(True)
            self.degSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.valueChanged.emit()
        elif not state and self.isEnabled():
            self.degSpinBox.setEnabled(False)
            self.degSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)
            self.valueChanged.emit()

    def toggleCheckBox(self):
        if self.normalCheckBox.checkState() == 2:
            self.normalCheckBox.setCheckState(0)
        else:
            self.normalCheckBox.setCheckState(2)

    def isEnabled(self):
        return self.degSpinBox.isEnabled()

    # not sure if useful
    # def sizeHint(self):
    #    return QSize(150,20)
