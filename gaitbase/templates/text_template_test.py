# -*- coding: utf-8 -*-
"""
Python template for the text report. This is a Python file called by exec().

@author: Jussi (jnu@iki.fi)
"""

from gaitbase.constants import Constants

conditional_dot = Constants.conditional_dot

text_blocks = [
"""
LIIKELAAJUUDET JA VOIMAT

Patient code: {TiedotID}
Patient name: {TiedotNimi}
Social security number: {TiedotHetu}
Diagnosis: {TiedotDiag}
Date of gait analysis: {TiedotPvm}
""",

"""
Kommentit: {cmtTiedot}
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

"""
Kommentit: {cmtAntrop}
""",

"""
MITTAAJAT: {TiedotMittaajat}
""",

"""
TULOSYY:


PÄÄTULOKSET KÄVELYANALYYSIN POHJALTA:


TESTAUS- JA ARVIOINTITULOKSET:


OHEISMITTAUSTEN TULOKSET:

""",

"""
Nivelten passiiviset liikelaajuudet (oikea/vasen), NR = normaalin rajoissa:
""",

'Lonkka:',
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
"""
Kommentit {cmtLonkkaPROM}

""",

'Polvi:',
'Ojennus (vapaasti) {PolviEkstensioVapOik}/{PolviEkstensioVapVas}. ',
'Ojennus (avustettuna) {PolviEkstensioAvOik}/{PolviEkstensioAvVas}. ',
'Koukistus (vatsamakuu) {PolviFleksioVatsamakuuOik}/{PolviFleksioVatsamakuuVas}. ',
'Koukistus (selinmakuu) {PolviFleksioSelinmakuuOik}/{PolviFleksioSelinmakuuVas}. ',
'Popliteakulma {PolviPopliteaVastakkLonkka0Oik}/{PolviPopliteaVastakkLonkka0Vas}, '\
'popliteakulma (true) {PolviPopliteaVastakkLonkka90Oik}/{PolviPopliteaVastakkLonkka90Vas}.',
 """
'Kommentit: {cmtPolviPROM}

""",
'Nilkka:',
'Koukistus (polvi 90°) {NilkkaDorsifPolvi90PROMOik}/{NilkkaDorsifPolvi90PROMVas}. ',
'Koukistus (polvi 0°) {NilkkaDorsifPolvi0PROMOik}/{NilkkaDorsifPolvi0PROMVas}. ',
'Ojennus {NilkkaPlantaarifleksioPROMOik}/{NilkkaPlantaarifleksioPROMVas}.',
 """
'Kommentit: {cmtNilkkaPROM}\n'

""",

]

