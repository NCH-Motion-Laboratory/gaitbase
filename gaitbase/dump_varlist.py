# -*- coding: utf-8 -*-
"""

Dump gaitbase variable names and their SQLite affinities.

@author: jussi (jnu@iki.fi)
"""
import json
import sys
import argparse

from PyQt5 import QtWidgets

from .rom_entryapp import EntryApp


def _type_affinity(widget):
    """Return type affinity (sqlite) for each widget"""
    widget_class = widget.__class__.__name__
    if widget_class in ('QSpinBox', 'QDoubleSpinBox', 'CheckableSpinBox'):
        return 'NUMERIC'
    else:
        return 'TEXT'


def get_vars_and_affinities():
    """Get a dict of variable names and their SQLite type affinities"""
    app = QtWidgets.QApplication(sys.argv)  # needed for Qt stuff to function
    eapp = EntryApp()
    affs = dict()
    for wname, widget in eapp.input_widgets.items():
        varname = eapp.widget_to_var[wname]
        affs[varname] = _type_affinity(widget)
    return affs


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--affinities',
        help='also print out variable affinities',
        action='store_true',
    )
    parser.add_argument(
        '-j',
        '--json',
        help='dump in JSON format',
        action='store_true',
    )
    args = parser.parse_args()
    var_affs = get_vars_and_affinities()

    if args.affinities:
        if args.json:
            out = json.dumps(var_affs, ensure_ascii=False, indent=True, sort_keys=True)
        else:
            aff_list = sorted(
                [f'{varname}: {aff}' for varname, aff in var_affs.items()]
            )
            out = '\n'.join(aff_list)
    else:
        sorted_vars = sorted(var_affs.keys())
        if args.json:
            out = json.dumps(sorted_vars, ensure_ascii=False, indent=True)
        else:
            out = '\n'.join(sorted_vars)
    print(out)
