# -*- coding: utf-8 -*-
"""
Gait database utils.

"""

import random
from pathlib import Path
import os
import tempfile


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


def validate_code(code):
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
