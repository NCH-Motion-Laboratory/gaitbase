# -*- coding: utf-8 -*-
"""
Recreate the gait database.

"""
from pathlib import Path
import sqlite3

from gaitbase.dump_varlist import _get_var_affs

DB_FILEPATH = Path('patients.db')

if DB_FILEPATH.is_file():
    raise RuntimeError(f'File {DB_FILEPATH} already exists!')
conn = sqlite3.connect(DB_FILEPATH)
conn.execute('PRAGMA foreign_keys = ON;')

# create the patient table
conn.execute(
    """CREATE TABLE patients (
    patient_id integer NOT NULL PRIMARY KEY,
    firstname text NOT NULL,
    lastname text NOT NULL,
    ssn text NOT NULL UNIQUE,
    patient_code text NOT NULL UNIQUE,
    diagnosis text
    );"""
)

# Create the table for ROM measurements. For this, we need a list of variables and their
# type affinities.
s = """CREATE TABLE roms (
    rom_id integer NOT NULL PRIMARY KEY,
    filename text,
    patient_id integer NOT NULL REFERENCES patients (patient_id) ON DELETE CASCADE,
    """

# add the ROM vars and their type affinities
var_affs = _get_var_affs()
for k, (varname, affinity) in enumerate(var_affs.items(), 1):
    # insert comma, unless at last item
    SEP = ',' if k < len(var_affs) else ''
    s += f'{varname} {affinity}{SEP}\n'
s += ');'

conn.execute(s)

conn.commit()

