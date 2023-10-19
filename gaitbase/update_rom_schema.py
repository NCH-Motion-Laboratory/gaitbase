# -*- coding: utf-8 -*-
"""
Update the ROM table schema. Necessary when new ROM variables are introduced.

"""

import argparse
from pathlib import Path
import sqlite3

from dump_varlist import get_vars_and_affinities
from constants import Constants


def check_ui_vs_sql(db_fname, update=False):
    """Check UI variables vs. SQL columns"""

    db_fname = Path(db_fname)
    if not db_fname.is_file():
        raise RuntimeError('DB file needs to exist!')
    conn = sqlite3.connect(db_fname)
    conn.execute('PRAGMA foreign_keys = ON;')

    # Compare DB version vs the version the application expects
    db_ver = list(conn.execute('PRAGMA user_version'))[0][0]
    if db_ver != Constants.db_version:
        print(f'*** NOTE: DB schema version mismatch: DB version is {db_ver}, ' + \
              f'but the application expects version {Constants.db_version}')

        if update:
            print(f"*** Changing the DB schema version to '{Constants.db_version}'...")
            conn.execute(f'PRAGMA user_version = {Constants.db_version}')
        else:
            print('Use -u to update the DB schema version.')

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
            if update:
                print(f"*** Creating column for '{var}'...")
                aff = var_affs_ui[var]
                conn.execute(f'ALTER TABLE roms ADD COLUMN {var} {aff}')
            else:
                print('Use -u to add it automatically.')
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
        '-u',
        '--update',
        help='automatically update the database (add missing columns and more)',
        action='store_true',
    )
    args = parser.parse_args()

    check_ui_vs_sql(args.db_fname, args.update)
