# -*- coding: utf-8 -*-
"""
Gait database utils.

"""

import subprocess
import sys
import os
import datetime

from ulstools.env import make_shortcut

from gaitbase.constants import Constants


def make_my_shortcut():
    """Make a desktop shortcut"""
    make_shortcut('gaitbase', 'run_gaitbase.py', title='Gait database')


def validate_code(code):
    """Check if patient code is valid.
    
    Currently we accept patient codes of the form:
    XNNNN_FMS or XNNNN_FS

    where X is a code corresponding to the diagnosis:
    D : diplegic CP
    H : hemiplegic CP
    C : unspecified CP
    M : meningomyelocele
    E : other diagnosis

    NNNN is running number that should be unique for each code (but not between
    codes), and FMS (or FS) are initials of the patient (front, middle, surname).
    """
    # TODO: might be nicer via regex
    if not code:
        return False
    if code[0] not in Constants.patient_code_prefixes:
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


def _startfile(target):
    """Linux compatible version of os.startfile"""
    if sys.platform == 'win32':
        os.startfile(target)
    else:
        subprocess.call(['xdg-open', target])


def isnumeric(x):
    """Test for numeric values (float or integer)"""
    return isinstance(x, int) or isinstance(x, float)


def _validate_date(datestr):
    """Validate a date in form of dd.mm.yyyy"""
    try:
        datetime.datetime.strptime(datestr, '%d.%m.%Y')
        return True
    except ValueError:
        return False
