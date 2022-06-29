# -*- coding: utf-8 -*-
"""
Python template for the text report.

The template must define a variable called text_blocks, which must be an
iterable of text blocks (strings). Each block may contain fields, denoted by
curly braces. The fields will be replaced by their corresponding values. If a
block contains fields and ALL of the fields are at their default values, the
block will be discarded.

Any columns in the SQL 'patients' and 'roms' tables are valid field names.

The code in this file is executed by exec(). Any Python logic may be used to
build the text_blocks variable. However for readability, it may be a good idea
to minimize the amount of code and keep the template as "textual" as possible.

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
Jalkaterän pituus: {AntropJalkateraOik} / {AntropJalkateraVas}
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

