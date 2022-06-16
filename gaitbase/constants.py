# -*- coding: utf-8 -*-
"""
Configuration for gaitbase ROM entry app
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Constants:
    """Some constants"""

    dialog_title: str = 'Gaitbase'
    # The 'not measured' value for spinboxes. For regular spinboxes, this is the
    # value that gets written to data files, but it does not affect the value
    # shown next to the spinbox (which is set in Qt Designer). For the
    # CheckableSpinBox class, this is also the value shown next to the widget in
    # the user interface.
    spinbox_novalue_text: str = 'Ei mitattu'
    # 'yes' and 'no' values for checkboxes. Written to data files.
    checkbox_yestext: str = 'Kyllä'
    checkbox_notext: str = 'EI'
    # the (hacky) idea here is that by virtue of case sensitivity, 'EI' can be
    # changed in the reports by search&replace without affecting other 'Ei'
    # where to write backup JSON files
    json_backup_path: str = Path('Z:/Misc/ROM_backup')
    # conditional separator
    conditional_dot = 1


@dataclass
class Finnish:
    """Some English->Finnish translations"""

    yes_button: str = 'Kyllä'
    no_button: str = 'Ei'
    ok_button: str = 'Ok'
    ready: str = 'Valmis, {n} syötekenttää käytössä.'
    status_cleared: str = 'Kaikki lomakkeet tyhjennetty.'
    keys_not_found: str = (
        'Seuraavia ohjelman käyttämiä muuttujia ei löytynyt tiedostosta:\n{keys}\n'
    )
    keys_extra: str = (
        'Seuraavat tiedostossa olevat muuttujat ovat tuntemattomia: {keys} \n'
    )
