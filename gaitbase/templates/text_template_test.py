# -*- coding: utf-8 -*-
"""
Python template for the text report. This is a Python file called by exec() and
works by modifying an existing variable called 'self' (instance of Report
class).

The idea is to add 'text blocks' containing text and fields to the Report()
instance (self) one by one. The field values are automatically filled in by the
Report class. If all variables for the block have default values (i.e. were not
measured) the Report instance will discard that block.

@author: Jussi (jnu@iki.fi)
"""
# %%
report_blocks = ([
"""
LIIKELAAJUUDET JA VOIMAT

Patient code: {TiedotID}
Patient name: {TiedotNimi}
Social security number: {TiedotHetu}
Diagnosis: {TiedotDiag}
Date of gait analysis: {TiedotPvm}
""",
"""
ANTROPOMETRISET MITAT:
Alaraajat: {AntropAlaraajaOik} / {AntropAlaraajaVas}
Nilkat: {AntropNilkkaOik} / {AntropNilkkaVas}
Polvet: {AntropPolviOik} / {AntropPolviVas}
Paino: {AntropPaino}
Pituus: {AntropPituus}
SIAS: {AntropSIAS}
Kengännumero: {AntropKenganNumeroOik} / {AntropKenganNumeroVas}
""",
"""Kommentit: {cmtAntrop}
""",
"""
MITTAAJAT:
{TiedotMittaajat}
""",
"""
TULOSYY:


PÄÄTULOKSET KÄVELYANALYYSIN POHJALTA:


TESTAUS- JA ARVIOINTITULOKSET:


OHEISMITTAUSTEN TULOKSET:

"""


])

