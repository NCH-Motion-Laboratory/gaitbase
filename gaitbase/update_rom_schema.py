# -*- coding: utf-8 -*-
"""
Update the ROM table schema. Necessary when new ROM variables are introduced.

"""

import argparse
from pathlib import Path
import sqlite3

from .dump_varlist import get_vars_and_affinities


def check_ui_vs_sql(db_fname, create_sql_columns=False):
    """Check UI variables vs. SQL columns"""

    db_fname = Path(db_fname)
    if not db_fname.is_file():
        raise RuntimeError('DB file needs to exist!')
    conn = sqlite3.connect(db_fname)
    conn.execute('PRAGMA foreign_keys = ON;')

    # get database columns and affinities
    var_affs_sql = dict()
    for varinfo in conn.execute("PRAGMA table_info('roms');"):
        varname = varinfo[1]
        affinity = varinfo[2]
        var_affs_sql[varname] = affinity

    # get UI variable names and affinities
    var_affs_ui = get_vars_and_affinities()
    # variables that appear in either UI or database
    allvars = set(var_affs_sql).union(var_affs_ui)

    # compare
    for var in allvars:
        if var not in var_affs_sql:
            print(f"*** NOTE: '{var}' has a UI element but is missing from SQL schema!")
            if create_sql_columns:
                print(f"*** Creating column for '{var}'...")
                aff = var_affs_ui[var]
                conn.execute(f'ALTER TABLE roms ADD COLUMN {var} {aff}')
            else:
                print('Use -a to add it automatically.')
        if var not in var_affs_ui:
            print(f"NOTE: SQL column '{var}' does not have a corresponding UI element")
            print('This may be OK (e.g. database id column, or a deprecated variable)')
        # check that affinity matches
        if var in var_affs_sql and var in var_affs_ui:
            if var_affs_ui[var] != var_affs_sql[var]:
                print(f"'{var}' affinity mismatch between SQL schema and UI, how come?")

    conn.commit()
    conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('db_fname', help='path to the database file')
    parser.add_argument(
        '-a',
        '--add-columns',
        help='automatically add missing SQL columns',
        action='store_true',
    )
    args = parser.parse_args()

    check_ui_vs_sql(args.db_fname, args.add_columns)
