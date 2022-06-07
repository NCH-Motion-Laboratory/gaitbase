# -*- coding: utf-8 -*-
"""
Update the ROM table schema. Necessary when new ROM variables are introduced.

"""

# %%
from pathlib import Path
import sqlite3

from gaitbase.dump_varlist import _get_var_affs


DB_FILEPATH = Path(r'C:\Temp\patients.db')
DB_FILEPATH = Path('/tmp/patients.db')

if not DB_FILEPATH.is_file():
    raise RuntimeError('DB file needs to exist!')
conn = sqlite3.connect(DB_FILEPATH)
conn.execute('PRAGMA foreign_keys = ON;')

# get the SQL varnames and affinities
var_affs_sql = dict()
for varinfo in conn.execute("PRAGMA table_info('roms');"):
    varname = varinfo[1]
    affinity = varinfo[2]
    var_affs_sql[varname] = affinity

# get UI varnames and affinities
var_affs_ui = _get_var_affs()

allvars = set(var_affs_sql).union(var_affs_ui)

# compare
for var in allvars:
    if var not in var_affs_sql:
        print(f'variable {var} missing from SQL schema, adding it...')
        conn.execute(f'ALTER TABLE roms ADD COLUMN {var} {aff}')
    if var not in var_affs_ui:
        print(f"note: SQL var '{var}' does not appear in UI")
    if var in var_affs_sql and var in var_affs_ui:
        if var_affs_ui[var] != var_affs_sql[var]:
            print(f"'{var}' affinity mismatch between SQL schema and UI, how come?")

conn.commit()







