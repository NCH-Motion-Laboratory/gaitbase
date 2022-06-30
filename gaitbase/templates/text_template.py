# -*- coding: utf-8 -*-
"""
Python template for the text report.

The template must define a variable called text_blocks, which must be an
iterable of text blocks (strings). Each block may contain fields, denoted by
curly braces. The fields will be replaced by their corresponding values. If a
block contains fields and ALL of the fields are at their default values, the
block will be discarded. Any columns in the SQL 'patients' and 'roms' tables are
valid field names.

In addition to text, a block may consist of a "smart end-of-line"
(Constants.end_line). This is a linefeed that will only be printed if the
previous character wa s not a linefeed. It will also cause any commas at the end
of line to be erased.

If a block begins a new line in the resulting report, its first letter will be
automatically capitalized.

The code in this file is executed by exec(). Any Python logic may be used to
build the text_blocks variable. However for readability, it may be a good idea
to minimize the amount of code and keep the template as "textual" as possible.

@author: Jussi (jnu@iki.fi)
"""

from gaitbase.constants import Constants

end_line = Constants.end_line

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
Alaraajan liikelaajuus- ja spastisuusmittaukset (oikea/vasen):
Modified Tardieu Scale (R1=catch, R2=passiivinen liikelaajuus) *
Modified Ashworth Scale (MAS) *
""",

"""
Nilkka:
""",
"soleus (R1) {NilkkaSoleusCatchOik}/{NilkkaSoleusCatchVas}, ",
"koukistus pass. (R2) {NilkkaDorsifPolvi90PROMOik}/{NilkkaDorsifPolvi90PROMVas}, ",
"akt. {NilkkaDorsifPolvi90AROMOik}/{NilkkaDorsifPolvi90AROMVas}, ",
"MAS {NilkkaSoleusModAOik}/{NilkkaSoleusModAVas}",
end_line,
"gastrocnemius (R1) {NilkkaGastroCatchOik}/{NilkkaGastroCatchVas}, ",
"koukistus pass. (R2) {NilkkaDorsifPolvi0PROMOik}/{NilkkaDorsifPolvi0PROMVas}, "
"akt. {NilkkaDorsifPolvi0AROMOik}/{NilkkaDorsifPolvi0AROMVas}, ",
"MAS {NilkkaGastroModAOik}/{NilkkaGastroModAVas}",
end_line,
"ojennus pass. {NilkkaPlantaarifleksioPROMOik}/{NilkkaPlantaarifleksioPROMVas}, "
"akt. {NilkkaPlantaarifleksioAROMOik}/{NilkkaPlantaarifleksioAROMVas}",
end_line,
"Confusion-testi oikea: {NilkkaConfusionOik}, vasen: {NilkkaConfusionVas}",
end_line,
"""
Kommentit (nilkka PROM): {cmtNilkkaPROM}
"""
"""
Kommentit (nilkka AROM): {cmtNilkkaAROM}
""",
"""
Kommentit (nilkka, spastisuus): {cmtNilkkaSpast}
""",

"""
Polvi:
""",
"hamstring (R1) {PolviHamstringCatchOik}/{PolviHamstringCatchVas}, ",
"popliteakulma {PolviPopliteaVastakkLonkka0Oik}/{PolviPopliteaVastakkLonkka0Vas}, true {PolviPopliteaVastakkLonkka90Oik}/{PolviPopliteaVastakkLonkka90Vas}, ",
"MAS {PolviHamstringModAOik}/{PolviHamstringModAVas}",
end_line,
"rectus (R1) {PolviRectusCatchOik}/{PolviRectusCatchVas}, ",
"polven koukistus pass. (vatsamakuu) (R2) {PolviFleksioVatsamakuuOik}/{PolviFleksioVatsamakuuVas}, ",
"MAS {PolviRectusModAOik}/{PolviRectusModAVas}",
end_line,
"polven koukistus (selinmakuu) {PolviFleksioSelinmakuuOik}/{PolviFleksioSelinmakuuVas}, ",
"polven ojennus {PolviEkstensioAvOik}/{PolviEkstensioAvVas}, vapaasti {PolviEkstensioVapOik}/{PolviEkstensioVapVas}",
end_line,
"""
Kommentit (polvi PROM): {cmtPolviPROM}
""",
"""
Kommentit (polvi, spastisuus): {cmtPolviSpast}
""",


]