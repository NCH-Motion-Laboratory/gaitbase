# -*- coding: utf-8 -*-
"""

Dump gaitbase variable names. Variables are defined by specially named widgets in the UI.

@author: jussi (jnu@iki.fi)
"""

import json
import sys
import io
from PyQt5 import QtWidgets

from gaitbase.sql_entryapp import EntryApp



def _type_affinity(wname):
    """Return type affinity (sqlite) for each widget"""
    if wname[:2] == 'sp':  # spinbox or doublespinbox
        return 'NUMERIC'
    elif wname[:2] == 'ln':  # lineedit
        return 'TEXT'
    elif wname[:2] == 'cb':  # combobox
        return 'TEXT'
    elif wname[:3] == 'cmt':  # comment text field
        return 'TEXT'
    elif wname[:2] == 'xb':  # checkbox
        return 'TEXT'
    elif wname[:3] == 'csb':  # CheckableSpinBox
        return 'NUMERIC'
    else:
        raise RuntimeError('Invalid widget name')

def _get_var_affs():
    """Get a dict of variable names and their type affinities"""
    app = QtWidgets.QApplication(sys.argv)  # needed for Qt stuff to function
    eapp = EntryApp()
    return {val: _type_affinity(key) for key, val in eapp.widget_to_var.items()}


if __name__ == '__main__':

    FN_OUT = "variable_affinity.txt"
    var_affs = _get_var_affs()
    print(f'{len(var_affs)} variables')
    with io.open(FN_OUT, 'w', encoding='utf-8') as f:
        f.write(json.dumps(var_affs, ensure_ascii=False, indent=True, sort_keys=True))
