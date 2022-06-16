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

from gaitbase.constants import Constants

conditional_dot = Constants.conditional_dot


# %%
blocks = ([
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


Nivelten passiiviset liikelaajuudet (oikea/vasen), NR = normaalin rajoissa:

Lonkka:
""",

'Thomasin testi (vapaasti) {LonkkaEkstensioVapOik}/{LonkkaEkstensioVapVas}. ',
'Thomasin testi (avustettuna) {LonkkaEkstensioAvOik}/{LonkkaEkstensioAvVas}. ',
'Thomasin testi (polvi 90°) {LonkkaEkstensioPolvi90Oik}/{LonkkaEkstensioPolvi90Vas}. ',
'Koukistus {LonkkaFleksioOik}/{LonkkaFleksioVas}. ',
'Loitonnus (lonkka 0°, polvi 90°) {LonkkaAbduktioLonkka0Polvi90Oik}/{LonkkaAbduktioLonkka0Polvi90Vas}. ',
'Loitonnus (lonkka 0°, polvi 0°) {LonkkaAbduktioLonkka0Oik}/{LonkkaAbduktioLonkka0Vas}. ',
'Loitonnus (lonkka 90°) {LonkkaAbduktioLonkkaFleksOik}/{LonkkaAbduktioLonkkaFleksVas}. ',
'Lähennys {LonkkaAdduktioOik}/{LonkkaAdduktioVas}. ',
'Sisäkierto {LonkkaSisakiertoOik}/{LonkkaSisakiertoVas}. ',
'Ulkokierto {LonkkaUlkokiertoOik}/{LonkkaUlkokiertoVas}. ',
'Kommentit {cmtLonkkaPROM}'




])

