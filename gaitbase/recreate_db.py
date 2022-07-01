# -*- coding: utf-8 -*-
"""
Recreate the gait database. Currently, this will create the patients table and
the table for ROM measurements. When new measurement modalities are introduced,
the script needs to be adapted to create the corresponding tables.

"""
from pathlib import Path
import sqlite3

from .dump_varlist import get_vars_and_affinities

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

# Create the table for ROM measurements. For this, we need a list of variables
# and their type affinities.
query = """CREATE TABLE roms (
    rom_id integer NOT NULL PRIMARY KEY,
    filename text,
    patient_id integer NOT NULL REFERENCES patients (patient_id) ON DELETE CASCADE,
    """

# add columns for the ROM vars and their type affinities
var_affs = get_vars_and_affinities()
for k, (varname, affinity) in enumerate(var_affs.items(), 1):
    # insert comma, unless at last item
    SEP = ',' if k < len(var_affs) else ''
    query += f'{varname} {affinity}{SEP}\n'
query += ');'

conn.execute(query)
conn.commit()

print(f'created an empty database at {DB_FILEPATH.resolve()}')
