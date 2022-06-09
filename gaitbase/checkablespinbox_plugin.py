# -*- coding: utf-8 -*-
"""
Qt Designer plugin for CheckableSpinBox.
Makes it possible to properly see the widget in Qt Designer.
Also required to properly write the .ui file containing custom widgets.
This is a bare minimum implementation - Designer will complain about some
methods not being provided, but it works. Before running Qt Designer, do
'export PYQTDESIGNERPATH=path' where path is the path to the plugin.


@author: Jussi (jnu@iki.fi)
"""

from gaitbase.widgets import CheckableSpinBox
from PyQt5 import QtDesigner


class CheckableSpinBoxPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return

        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return CheckableSpinBox(parent)

    def name(self):
        return "CheckableSpinBox"

    def group(self):
        return "Gaitbase"

    def isContainer(self):
        return False

    def includeFile(self):
        return "gaitbase.widgets"
