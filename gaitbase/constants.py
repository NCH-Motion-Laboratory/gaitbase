# -*- coding: utf-8 -*-
"""
Configuration for gaitbase ROM entry app
"""

from dataclasses import dataclass


@dataclass
class Constants:
    """Some constants"""

    # allowable patient code prefixes
    patient_code_prefixes = 'CDEHMT'
    # magic prefix for data entry widgets
    input_widget_prefix = 'data'
    # window title
    dialog_title: str = 'Gaitbase'
    # The 'not measured' value for spinboxes. For regular spinboxes, this is the
    # value that gets written to data files, but it does not affect the value
    # shown next to the spinbox (which is set in Qt Designer). For the
    # CheckableSpinBox class, this is also the value shown next to the widget in
    # the user interface.
    spinbox_novalue_text: str = 'Ei mitattu'
    # 'yes' and 'no' values for checkboxes. Written to data files.
    checkbox_yestext: str = 'Kyllä'
    # the 'no' value should really be 'Ei' but is capitalized for historical
    # reasons; it's automatically uncapitalized for reports
    checkbox_notext: str = 'EI'
    # smart linefeed (a sentinel that only compares equal with itself)
    end_line = object()


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
