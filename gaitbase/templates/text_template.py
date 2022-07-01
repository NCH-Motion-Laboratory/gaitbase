# -*- coding: utf-8 -*-
"""
Python template for the text report.

The template must define a variable called text_blocks, which must be an
iterable of text blocks (strings). Each block may contain fields written as
{field}. They will be replaced by their corresponding values. If a block
contains fields and ALL of the fields are at their default values, the block
will be discarded. Any columns in the SQL 'patients' and 'roms' tables are valid
field names.

Besides text, a block may consist of a "smart" end-of-line (Constants.end_line).
It prints a dot & linefeed, if the previous character in the processed text is
not a line feed. It will also erase any preceding commas at the end of line.
This extra logic is needed for clean output, since we do not know in advance
which blocks on a given line will get printed. 

If a block begins a new line in the resulting report, its first letter will be
automatically capitalized. This is necessary, since we may not know in advance
which block begins a line.

The code in this file is executed by exec(). Any Python logic may be used to
build the text_blocks variable. However for readability, it may be a good idea
to minimize the amount of code and keep the template as "textual" as possible.

NOTE: don't forget the comma after single-quoted strings, otherwise the Python
parser will merge the strings. I.e. don't write

"block1"
"block2"

TODO: utf-8 handling?

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
"koukistus pass. (R2) {NilkkaDorsifPolvi0PROMOik}/{NilkkaDorsifPolvi0PROMVas}, ",
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
"polven ojennus {PolviEkstensioAvOik}/{PolviEkstensioAvVas}, ",
"vapaasti {PolviEkstensioVapOik}/{PolviEkstensioVapVas}",
end_line,
"Extensor lag {LonkkaExtLagOik}{LonkkaExtLagVas}",
end_line,
"""
Kommentit (polvi PROM): {cmtPolviPROM}
""",
"""
Kommentit (polvi, spastisuus): {cmtPolviSpast}
""",
"""
Lonkka:
""",
"thomasin testi: pass. {LonkkaEkstensioAvOik}/{LonkkaEkstensioAvVas}, ",
"polvi koukussa {LonkkaEkstensioPolvi90Oik}/{LonkkaEkstensioPolvi90Vas}, ",
"vapaasti {LonkkaEkstensioVapOik}/{LonkkaEkstensioVapVas}, ",
"lonkan koukistus {LonkkaFleksioOik}/{LonkkaFleksioVas}",
end_line,
"adduktor (R1) {LonkkaAdduktoritCatchOik}/{LonkkaAdduktoritCatchVas}, ",
"loitonnus polvi suorana (R2) {LonkkaAbduktioLonkka0Oik}/{LonkkaAbduktioLonkka0Vas}, ",
"lonkka suorana ja polvi koukussa {LonkkaAbduktioLonkka0Polvi90Oik}/{LonkkaAbduktioLonkka0Polvi90Vas}, ",
"lonkka koukussa {LonkkaAbduktioLonkkaFleksOik}/{LonkkaAbduktioLonkkaFleksVas}, ",
"MAS {LonkkaFleksioModAOik}/{LonkkaFleksioModAVas}",
end_line,
"lähennys {LonkkaFleksioModAOik}/{LonkkaFleksioModAVas}",
end_line,
"sisäkierto {LonkkaSisakiertoOik}/{LonkkaSisakiertoVas}, ",
"ulkokierto {LonkkaUlkokiertoOik}/{LonkkaUlkokiertoVas}, ",
end_line,
"ober test: oikea: {LonkkaOberOik} vasen: {LonkkaOberVas}",
end_line,
"""
Kommentit (lonkka PROM): {cmtLonkkaPROM}
""",
"""
Kommentit (lonkka, spatisuus): {cmtLonkkaSpast}
""",
"""
Kommentit (lonkka, muut): {cmtLonkkaMuut}
""",
"""
Luiset asennot:
""",
"jalkaterä-reisi -kulma {VirheasJalkaReisiOik}/{VirheasJalkaReisiVas}, ",
"jalkaterän etu-takaosan kulma {VirheasJalkateraEtuTakaOik}/{VirheasJalkateraEtuTakaVas}, ",
"bimalleoli-akseli {VirheasBimalleoliOik}/{VirheasBimalleoliVas}, ",
"2nd toe -testi {Virheas2ndtoeOik}/{Virheas2ndtoeVas}",
end_line,
"patella alta {VirheasPatellaAltaOik}/{VirheasPatellaAltaVas}, ",
"polven valgus {PolvenValgusOik}/{PolvenValgusVas}, ",
"Q-kulma {QkulmaOik}/{QkulmaVas}, ",
"Lonkan anteversio {VirheasAnteversioOik}/{VirheasAnteversioVas}, ",
"Alaraajojen pituus {AntropAlaraajaOik}/{AntropAlaraajaVas}, ",
"Jalkaterien pituus {AntropJalkateraOik}/{AntropJalkateraVas}",
end_line,
"""
Kommentit (luiset asennot): {cmtVirheas}
""",
"""
Jalkaterä kuormittamattomana
""",
"subtalar neutraali-asento {JalkatSubtalarOik}/{JalkatSubtalarVas}, ",
"takaosan asento {JalkatTakaosanAsentoOik}/{JalkatTakaosanAsentoVas}, ",
"takaosan liike eversioon {JalkatTakaosanLiikeEversioOik}/{JalkatTakaosanLiikeEversioVas}, ",
"takaosan liike inversioon {JalkatTakaosanLiikeInversioOik}/{JalkatTakaosanLiikeInversioVas}",
end_line,
"med. holvikaari {JalkatHolvikaariOik}/{JalkatHolvikaariVas}, ",
"midtarsaalinivelen liike {JalkatKeskiosanliikeOik}/{JalkatKeskiosanliikeVas}, ",
"etuosan asento 1 {JalkatEtuosanAsento1Oik}/{JalkatEtuosanAsento1Vas}, ",
"etuosan asento 2 {JalkatEtuosanAsento2Oik}/{JalkatEtuosanAsento2Vas}",
end_line,
"1. säde {Jalkat1sadeOik}/{Jalkat1sadeVas}, ",
"1. MTP ojennus {Jalkat1MTPojennusOik}/{Jalkat1MTPojennusVas}, ",
"vaivaisenluu oikea: {JalkatVaivaisenluuOik} vasen: {JalkatVaivaisenluuVas}, ",
"kovettumat oikea: {JalkatKovettumatOik}/{JalkatKovettumatVas}",
end_line,
"""
Kommentit (jalkaterä kuormittamattomana): {cmtJalkateraKuormittamattomana}
""",
"""
Jalkaterä kuormitettuna
""",
"takaosan (kantaluun) asento {JalkatTakaosanAsentoKuormOik}/{JalkatTakaosanAsentoKuormVas}, "
"takaosan kierto {JalkatTakaosanKiertoKuormOik}/{JalkatTakaosanKiertoKuormVas}, ",
"keskiosan asento {JalkatKeskiosanAsentoKuormOik}/{JalkatKeskiosanAsentoKuormVas}, ",
"etuosan asento 1 {JalkatEtuosanAsento1KuormOik}/{JalkatEtuosanAsento1KuormVas}, ",
"etuosan asento 2 {JalkatEtuosanAsento2KuormOik}/{JalkatEtuosanAsento2KuormVas}",
end_line,
"takaosan kierto {JalkatTakaosanKiertoKuormOik}/{JalkatTakaosanKiertoKuormVas}, ",
"Feissin linja {JalkatFeissinLinjaOik}/{JalkatFeissinLinjaVas}, ",
"navicular drop istuen {JalkatNavDropIstuenOik}/{JalkatNavDropIstuenVas}, "
"navicular drop seisten {JalkatNavDropSeistenOik}/{JalkatNavDropSeistenVas}, "
"Jackin testi {JalkatJackTestiOik}/{JalkatJackTestiVas}",
end_line,
"""
Manuaalisesti mitattu lihasvoima (asteikko 0-5):
"""
]
