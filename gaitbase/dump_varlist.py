# -*- coding: utf-8 -*-
"""

Dump current variable list

@author: jussi (jnu@iki.fi)
"""

import imp
import json
import sys
import io
from PyQt5 import QtWidgets

from .sql_entryapp import EntryApp

fn_out = "variable_affinity.txt"


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
    elif wname[:3] == 'csb':  # checkdegspinbox
        return 'NUMERIC'
    else:
        raise RuntimeError('Invalid widget name')


app = QtWidgets.QApplication(sys.argv)  # needed for Qt stuff to function
eapp = EntryApp(check_temp_file=False)
with io.open(fn_out, 'w', encoding='utf-8') as f:
    widget_aff = {val: _type_affinity(key) for key, val in eapp.widget_to_var.items()}

    f.write(json.dumps(widget_aff, ensure_ascii=False, indent=True, sort_keys=True))
