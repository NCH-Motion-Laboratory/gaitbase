# -*- coding: utf-8 -*-
"""

Python template for the text report.

The template must define a variable called _text_blocks, which must be an
iterable of text blocks (strings). The report is built by concatenating the
blocks. Each block may contain fields written as {field_name}. They will be
replaced by the corresponding data values. If a block contains fields and ALL of
the fields are at their default values, the block will be discarded. Any columns
in the SQL 'roms' and 'patients' tables are valid field names.

Besides a string, a block may consist of a "smart end-of-line" (Constants.end_line).
It prints a dot & linefeed, if the preceding character in the result text is not
a line feed. It will also erase any preceding commas at the end of line. The
smart end-of-line should be used to terminate lines consisting of multiple text
blocks, since it's not known in advance which blocks will be printed.

If a block begins a new line in the resulting report, its first letter will be
automatically capitalized. This is necessary, since we may not know in advance
which block will begin a line.

The code in this file is executed by exec(). In principle, any Python logic may
be used to build the _text_blocks variable. However for readability, it may be a
good idea to minimize the amount of code and keep the template as "textual" as
possible. Currently, some strings are pre-evaluated, and _text_blocks is then
defined as a simple explicit list of strings.

The data variables are brought into the global module namespace of this module
by exec(), so it's also possible to refer to them explicitly. This can used to
e.g. conditionally print certain items that are difficult to handle otherwise,
by using Python conditional logic or f-strings. Note that the evaluation of
f-strings differs from regular strings: f-strings are evaluated immediately at
definition time.

NOTE: before filling in the fields, certain values may be replaced according to
the dictionary cfg.report.replace_data. For example, 'Ei mitattu' gets
translated into '-' for brevity.

NOTE: don't forget the comma after block definitions, otherwise the Python
parser will merge them, i.e. don't write

"block1"
"block2"

NOTE: the exec() mechanism will use the latest copy of report template from the
disk. Thus, modifications will be immediately visible in new reports, and it's
not necessary to restart the program when debugging the template.


@author: Jussi (jnu@iki.fi)
"""

# relative imports may not work here, since the template can be located anywhere;
# it's safer to explicitly import from gaitbase
from gaitbase.constants import Constants

end_line = Constants.end_line  # constant indicating a 'smart' end-of-line

# pre-evaluate some strings to avoid cluttering the report text
str_NilkkaDorsifPolvi0AROMEversioOik = ' (eversio)' if NilkkaDorsifPolvi0AROMEversioOik == Constants.checkbox_yestext else ''
str_NilkkaDorsifPolvi0AROMEversioVas = ' (eversio)' if NilkkaDorsifPolvi0AROMEversioVas == Constants.checkbox_yestext else ''
str_NilkkaDorsifPolvi90AROMEversioOik = ' (eversio)' if NilkkaDorsifPolvi90AROMEversioOik == Constants.checkbox_yestext else ''
str_NilkkaDorsifPolvi90AROMEversioVas = ' (eversio)' if NilkkaDorsifPolvi90AROMEversioVas == Constants.checkbox_yestext else ''
str_NilkkaGastroKlonusOik = ' (klonus)' if NilkkaGastroKlonusOik == Constants.checkbox_yestext else ''
str_NilkkaGastroKlonusVas = ' (klonus)' if NilkkaGastroKlonusVas == Constants.checkbox_yestext else ''
str_NilkkaSoleusKlonusOik = ' (klonus)' if NilkkaSoleusKlonusOik == Constants.checkbox_yestext else ''
str_NilkkaSoleusKlonusVas = ' (klonus)' if NilkkaSoleusKlonusVas == Constants.checkbox_yestext else ''

# compose a string of active EMG channels, names separated by comma
_emg_desc = {'soleus': EMGSol,
            'gastrocnemius': EMGGas,
            'peroneus': EMGPer,
            'tibialis anterior': EMGTibA,
            'rectus': EMGRec,
            'hamstring': EMGHam,
            'vastus': EMGVas,
            'gluteus': EMGGlut
            }
_list_emg_active = ', '.join(name for name, val in _emg_desc.items() if val == Constants.checkbox_yestext)
if _list_emg_active:
    # add a header
    str_emg_active = 'Alaraajojen lihasaktivaatio mitattiin pintaelektrodeilla seuraavista lihaksista:\n'
    str_emg_active += _list_emg_active
else:
    # if no active EMG channels, don't output any text
    str_emg_active = ''


# begin report text
_text_blocks = [
"""
LIIKELAAJUUDET JA VOIMAT

Patient code: {patient_code}
Patient name: {firstname} {lastname}
Social security number: {ssn}
Diagnosis: {diagnosis}
Date of gait analysis: {TiedotPvm}
""",

"""
Kommentit: {cmtTiedot}
""",

"""
Antropometriset mitat:

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
Mittaajat: {TiedotMittaajat}
""",

"""
Alaraajan liikelaajuus- ja spastisuusmittaukset (oikea/vasen):
Modified Tardieu Scale (R1=catch, R2=passiivinen liikelaajuus) *
Modified Ashworth Scale (MAS) *
""",

"""
Nilkka:

""",
# the f-string is used to immediately evaluate the local _str variables and pass
# on the remaining variable names (in double braces) without evaluation; this
# way, the block can still be discarded if the variables are at default values
f"soleus (R1) {{NilkkaSoleusCatchOik}}{str_NilkkaSoleusKlonusOik}/{{NilkkaSoleusCatchVas}}{str_NilkkaSoleusKlonusVas}, ",
"polvi koukussa nilkan koukistus pass. (R2) {NilkkaDorsifPolvi90PROMOik}/{NilkkaDorsifPolvi90PROMVas}, ",
f"akt. {{NilkkaDorsifPolvi90AROMOik}}{str_NilkkaDorsifPolvi90AROMEversioOik}/{{NilkkaDorsifPolvi90AROMVas}}{str_NilkkaDorsifPolvi90AROMEversioVas}, ",
end_line,
f"gastrocnemius (R1) {{NilkkaGastroCatchOik}}{str_NilkkaGastroKlonusOik}/{{NilkkaGastroCatchVas}}{str_NilkkaGastroKlonusVas}, ",
"polvi suorana nilkan koukistus pass. (R2) {NilkkaDorsifPolvi0PROMOik}/{NilkkaDorsifPolvi0PROMVas}, ",
f"akt. {{NilkkaDorsifPolvi0AROMOik}}{str_NilkkaDorsifPolvi0AROMEversioOik}/{{NilkkaDorsifPolvi0AROMVas}}{str_NilkkaDorsifPolvi0AROMEversioVas}, ",
end_line,
"ojennus pass. {NilkkaPlantaarifleksioPROMOik}/{NilkkaPlantaarifleksioPROMVas}, "
"akt. {NilkkaPlantaarifleksioAROMOik}/{NilkkaPlantaarifleksioAROMVas}, ",
end_line,
"Confusion-testi oikea: {NilkkaConfusionOik}, vasen: {NilkkaConfusionVas}, ",
"MAS: soleus {NilkkaSoleusModAOik}/{NilkkaSoleusModAVas}, gastrocnemius {NilkkaGastroModAOik}/{NilkkaGastroModAVas}, ",
end_line,
"""
Kommentit (PROM): {cmtNilkkaPROM}
""",
"""
Kommentit (AROM): {cmtNilkkaAROM}
""",
"""
Kommentit (spastisuus): {cmtNilkkaSpast}
""",

"""
Polvi:

""",
"hamstring (R1) {PolviHamstringCatchOik}/{PolviHamstringCatchVas}, ",
"popliteakulma {PolviPopliteaVastakkLonkka0Oik}/{PolviPopliteaVastakkLonkka0Vas}, true {PolviPopliteaVastakkLonkka90Oik}/{PolviPopliteaVastakkLonkka90Vas}, ",
"MAS {PolviHamstringModAOik}/{PolviHamstringModAVas}, ",
end_line,
"rectus (R1) {PolviRectusCatchOik}/{PolviRectusCatchVas}, ",
"polven koukistus pass. (vatsamakuu) (R2) {PolviFleksioVatsamakuuOik}/{PolviFleksioVatsamakuuVas}, ",
"MAS {PolviRectusModAOik}/{PolviRectusModAVas}, ",
end_line,
"polven koukistus (selinmakuu) {PolviFleksioSelinmakuuOik}/{PolviFleksioSelinmakuuVas}, ",
"polven ojennus {PolviEkstensioAvOik}/{PolviEkstensioAvVas}, ",
"vapaasti {PolviEkstensioVapOik}/{PolviEkstensioVapVas}, ",
end_line,
"Extensor lag {LonkkaExtLagOik}/{LonkkaExtLagVas}, ",
end_line,
"""
Kommentit (PROM): {cmtPolviPROM}
""",
"""
Kommentit (spastisuus): {cmtPolviSpast}
""",
"""
Lonkka:

""",
"thomasin testi: pass. {LonkkaEkstensioAvOik}/{LonkkaEkstensioAvVas}, ",
"polvi koukussa {LonkkaEkstensioPolvi90Oik}/{LonkkaEkstensioPolvi90Vas}, ",
"vapaasti {LonkkaEkstensioVapOik}/{LonkkaEkstensioVapVas}, ",
end_line,
"lonkan koukistus {LonkkaFleksioOik}/{LonkkaFleksioVas}, ",
end_line,
"adduktor (R1) {LonkkaAdduktoritCatchOik}/{LonkkaAdduktoritCatchVas}, ",
"lonkan loitonnus polvi suorana (R2) {LonkkaAbduktioLonkka0Oik}/{LonkkaAbduktioLonkka0Vas}, ",
"lonkka suorana ja polvi koukussa {LonkkaAbduktioLonkka0Polvi90Oik}/{LonkkaAbduktioLonkka0Polvi90Vas}, ",
"lonkka koukussa {LonkkaAbduktioLonkkaFleksOik}/{LonkkaAbduktioLonkkaFleksVas}, ",
end_line,
"lonkan lähennys {LonkkaAdduktioOik}/{LonkkaAdduktioVas}, ",
end_line,
"sisäkierto {LonkkaSisakiertoOik}/{LonkkaSisakiertoVas}, ",
"ulkokierto {LonkkaUlkokiertoOik}/{LonkkaUlkokiertoVas}, ",
end_line,
"MAS: lonkan adduktorit {LonkkaAdduktoritModAOik}/{LonkkaAdduktoritModAVas}, ",
"lonkan ojentajat {LonkkaEkstensioModAOik}/{LonkkaEkstensioModAVas}, ",
"lonkan koukistajat {LonkkaFleksioModAOik}/{LonkkaFleksioModAVas}, ",
"lonkan sisäkiertäjät {LonkkaSisakiertoModAOik}/{LonkkaSisakiertoModAVas}, ",
"lonkan ulkokiertäjät {LonkkaUlkokiertoModAOik}/{LonkkaUlkokiertoModAVas}, ",
end_line,
"ober test: oikea: {LonkkaOberOik} vasen: {LonkkaOberVas}, ",
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
"2nd toe -testi {Virheas2ndtoeOik}/{Virheas2ndtoeVas}, ",
end_line,
"patella alta {VirheasPatellaAltaOik}/{VirheasPatellaAltaVas}, ",
"polven valgus {PolvenValgusOik}/{PolvenValgusVas}, ",
"Q-kulma {QkulmaOik}/{QkulmaVas}, ",
"Lonkan anteversio {VirheasAnteversioOik}/{VirheasAnteversioVas}, ",
end_line,
"Alaraajojen pituus {AntropAlaraajaOik}/{AntropAlaraajaVas}, ",
"Jalkaterien pituus {AntropJalkateraOik}/{AntropJalkateraVas}, ",
end_line,
"""
Kommentit (luiset asennot): {cmtVirheas}
""",
"""
Jalkaterä kuormittamattomana:

""",
"subtalar neutraali-asento {JalkatSubtalarOik}/{JalkatSubtalarVas}, ",
"takaosan asento {JalkatTakaosanAsentoOik}/{JalkatTakaosanAsentoVas}, ",
"takaosan liike eversioon {JalkatTakaosanLiikeEversioOik}/{JalkatTakaosanLiikeEversioVas}, ",
"takaosan liike inversioon {JalkatTakaosanLiikeInversioOik}/{JalkatTakaosanLiikeInversioVas}, ",
end_line,
"med. holvikaari {JalkatHolvikaariOik}/{JalkatHolvikaariVas}, ",
"midtarsaalinivelen liike {JalkatKeskiosanliikeOik}/{JalkatKeskiosanliikeVas}, ",
"etuosan asento 1 {JalkatEtuosanAsento1Oik}/{JalkatEtuosanAsento1Vas}, ",
"etuosan asento 2 {JalkatEtuosanAsento2Oik}/{JalkatEtuosanAsento2Vas}, ",
end_line,
"1. säde {Jalkat1sadeOik}/{Jalkat1sadeVas}, ",
"1. MTP ojennus {Jalkat1MTPojennusOik}/{Jalkat1MTPojennusVas}, ",
end_line,
"vaivaisenluu oikea: {JalkatVaivaisenluuOik} vasen: {JalkatVaivaisenluuVas}, ",
"kovettumat oikea: {JalkatKovettumatOik}/{JalkatKovettumatVas}, ",
end_line,
"""
Kommentit (jalkaterä kuormittamattomana): {cmtJalkateraKuormittamattomana}
""",

"""
Jalkaterä kuormitettuna:

""",
"takaosan (kantaluun) asento {JalkatTakaosanAsentoKuormOik}/{JalkatTakaosanAsentoKuormVas}, "
"takaosan kierto {JalkatTakaosanKiertoKuormOik}/{JalkatTakaosanKiertoKuormVas}, ",
"keskiosan asento {JalkatKeskiosanAsentoKuormOik}/{JalkatKeskiosanAsentoKuormVas}, ",
end_line,
"etuosan asento 1 {JalkatEtuosanAsento1KuormOik}/{JalkatEtuosanAsento1KuormVas}, ",
"etuosan asento 2 {JalkatEtuosanAsento2KuormOik}/{JalkatEtuosanAsento2KuormVas}, ",
end_line,
"takaosan kierto {JalkatTakaosanKiertoKuormOik}/{JalkatTakaosanKiertoKuormVas}, ",
"Feissin linja {JalkatFeissinLinjaOik}/{JalkatFeissinLinjaVas}, ",
"navicular drop istuen {JalkatNavDropIstuenOik}/{JalkatNavDropIstuenVas}, ",
"navicular drop seisten {JalkatNavDropSeistenOik}/{JalkatNavDropSeistenVas}, ",
end_line,
"Jackin testi {JalkatJackTestiOik}/{JalkatJackTestiVas}, ",
"Colemanin block -testi {JalkatColemanOik}/{JalkatColemanVas}",
end_line,
"""
Kommentit (jalkaterä kuormitettuna): {cmtJalkateraKuormitettuna}
""",

"""
Manuaalisesti mitattu lihasvoima (asteikko 0-5):

""",
"nilkan koukistus {VoimaTibialisAnteriorOik}/{VoimaTibialisAnteriorVas}, ",
"nilkan ojennus (gastrocnemius) {VoimaGastroOik}/{VoimaGastroVas}, ",
"nilkan ojennus (soleus) {VoimaSoleusOik}/{VoimaSoleusVas}, ",
"inversio {VoimaTibialisPosteriorOik}/{VoimaTibialisPosteriorVas}, "
"eversio {VoimaPeroneusOik}/{VoimaPeroneusVas}, ",
end_line,
"isovarpaan ojennus {VoimaExtHallucisLongusOik}/{VoimaExtHallucisLongusVas}, ",
"isovarpaan koukistus {VoimaFlexHallucisLongusOik}/{VoimaFlexHallucisLongusVas}, ",
"varpaiden (2-5) ojennus {Voima25OjennusOik}/{Voima25OjennusVas}, ",
"varpaiden (2-5) koukistus {Voima25KoukistusOik}/{Voima25KoukistusVas}, ",
end_line,
"polven ojennus {VoimaPolviEkstensioOik}/{VoimaPolviEkstensioVas}, ",
"polven koukistus {VoimaPolviFleksioOik}/{VoimaPolviFleksioVas}, ",
end_line,
"lonkan ojennus {VoimaLonkkaEkstensioPolvi0Oik}/{VoimaLonkkaEkstensioPolvi0Vas}, ",
"lonkan ojennus polvi koukussa {VoimaLonkkaEkstensioPolvi90Oik}/{VoimaLonkkaEkstensioPolvi90Vas}, ",
"lonkan koukistus {VoimaLonkkaFleksioOik}/{VoimaLonkkaFleksioVas}, ",
end_line,
"lonkan loitonnus {VoimaLonkkaAbduktioLonkka0Oik}/{VoimaLonkkaAbduktioLonkka0Vas}, ",
"lonkan loitonnus lonkka koukussa {VoimaLonkkaAbduktioLonkkaFleksOik}/{VoimaLonkkaAbduktioLonkkaFleksVas}, ",
end_line,
"lonkan lähennys {VoimaLonkkaAdduktioOik}/{VoimaLonkkaAdduktioVas}, ",
"lonkan sisäkierto {VoimaLonkkaSisakiertoOik}/{VoimaLonkkaSisakiertoVas}, ",
"lonkan ulkokierto {VoimaLonkkaUlkokiertoOik}/{VoimaLonkkaUlkokiertoVas}, ",
end_line,
"suorat vatsalihakset {VoimaVatsaSuorat}, ",
"vinot vatsalihakset {VoimaVatsaVinotOik}/{VoimaVatsaVinotVas}, "
"selkälihakset {VoimaSelka}",
end_line,
"""
Kommentit (voima): {cmtVoima1} {cmtVoima2}
""",
"""
Selektiivisyys:

""",
"nilkan koukistus {SelTibialisAnteriorOik}/{SelTibialisAnteriorVas}, ",
"nilkan ojennus (gastrocnemius) {SelGastroOik}/{SelGastroVas}, ",
"nilkan ojennus (soleus) {SelSoleusOik}/{SelSoleusVas}, ",
"inversio {SelTibialisPosteriorOik}/{SelTibialisPosteriorVas}, "
"eversio {SelPeroneusOik}/{SelPeroneusVas}, ",
end_line,
"isovarpaan ojennus {SelExtHallucisLongusOik}/{SelExtHallucisLongusVas}, ",
"isovarpaan koukistus {SelFlexHallucisLongusOik}/{SelFlexHallucisLongusVas}, ",
"varpaiden (2-5) ojennus {Sel25OjennusOik}/{Sel25OjennusVas}, ",
"varpaiden (2-5) koukistus {Sel25KoukistusOik}/{Sel25KoukistusVas}, ",
end_line,
"polven ojennus {SelPolviEkstensioOik}/{SelPolviEkstensioVas}, ",
"polven koukistus {SelPolviFleksioOik}/{SelPolviFleksioVas}, ",
end_line,
"lonkan ojennus {SelLonkkaEkstensioPolvi0Oik}/{SelLonkkaEkstensioPolvi0Vas}, ",
"lonkan ojennus polvi koukussa {SelLonkkaEkstensioPolvi90Oik}/{SelLonkkaEkstensioPolvi90Vas}, ",
"lonkan koukistus {SelLonkkaFleksioOik}/{SelLonkkaFleksioVas}, ",
"lonkan loitonnus {SelLonkkaAbduktioLonkka0Oik}/{SelLonkkaAbduktioLonkka0Vas}, ",
end_line,
"lonkan lähennys {SelLonkkaAdduktioOik}/{SelLonkkaAdduktioVas}, ",
"lonkan sisäkierto {SelLonkkaSisakiertoOik}/{SelLonkkaSisakiertoVas}, ",
"lonkan ulkokierto {SelLonkkaUlkokiertoOik}/{SelLonkkaUlkokiertoVas}, ",
end_line,
str_emg_active,
"""
Kommentit (EMG): {cmtEMG}
""",
"""

* Lyhenteet ja asteikot:
R1=catch, R2=passiivinen liikelaajuus, MAS = Modified Ashworth Scale, asteikko 0-4.
Jalkaterä: NEU=neutraali, TYYP=tyypillinen, RAJ=rajoittunut, VAR=varus, VALG=valgus, + = lievä, ++ = kohtalainen, +++ = voimakas.
Manuaalinen lihasvoima: asteikko 0-5, missä 5 on vahvin, ja 3 voittaa painovoiman koko potilaan liikelaajuudella.
Selektiivisyys: asteikko 0-2, missä 0=kokonaisliikemalli, 1=osittain eriytynyt ja 2=eriytynyt koko liikelaajuudella.
"""
]
