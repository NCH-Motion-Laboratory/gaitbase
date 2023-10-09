# -*- coding: utf-8 -*-
"""

Python template for the text report.

The template must define a variable called _text_blocks that specifies how the
report is formatted. _text_blocks is a tree with leaves being strings and
inner nodes - lists or tuples. Ther report is build by recursively translating
each vertex to text; the text for the root vertex is the report.

Each leaf may contain data fields written as {field_name}. They will be
replaced by the corresponding data values. If a leaf contains fields and ALL of
the fields are at their default values, the leaf will be discarded.

If a node has children leaves that contain data fields, and ALL of the
childrens' fields are at their default values, the whole node will be discarded.

Any columns in the SQL 'roms' and 'patients' tables are valid field names.

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

NOTE: instead of modifying the package default template, it's better to keep and
modify a local copy, so the template will not be overwritten when updating the
package. The template path can be configured in the package configuration.


@author: Jussi (jnu@iki.fi)
"""

# relative imports may not work here, since the template can be located anywhere;
# it's safer to explicitly import from gaitbase
from gaitbase.constants import Constants

# pre-evaluate some strings to avoid cluttering the report text
str_NilkkaDorsifPolvi0AROMEversioOik = '(eversio)' if NilkkaDorsifPolvi0AROMEversioOik == Constants.checkbox_yestext else ''
str_NilkkaDorsifPolvi0AROMEversioVas = '(eversio)' if NilkkaDorsifPolvi0AROMEversioVas == Constants.checkbox_yestext else ''
str_NilkkaDorsifPolvi90AROMEversioOik = '(eversio)' if NilkkaDorsifPolvi90AROMEversioOik == Constants.checkbox_yestext else ''
str_NilkkaDorsifPolvi90AROMEversioVas = '(eversio)' if NilkkaDorsifPolvi90AROMEversioVas == Constants.checkbox_yestext else ''
str_NilkkaGastroKlonusOik = '(klonus)' if NilkkaGastroKlonusOik == Constants.checkbox_yestext else ''
str_NilkkaGastroKlonusVas = '(klonus)' if NilkkaGastroKlonusVas == Constants.checkbox_yestext else ''
str_NilkkaSoleusKlonusOik = '(klonus)' if NilkkaSoleusKlonusOik == Constants.checkbox_yestext else ''
str_NilkkaSoleusKlonusVas = '(klonus)' if NilkkaSoleusKlonusVas == Constants.checkbox_yestext else ''

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

##-------------------------------------------------------------------------
# Header
#
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

##-------------------------------------------------------------------------
# Antropometriset mitat
#
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
"Kommentit: {cmtAntrop}\n",
"Mittaajat: {TiedotMittaajat}\n",

##-------------------------------------------------------------------------
# EMG
#
[
"""
Dyn EMG:
""",
str_emg_active,
"""
Kommentit (EMG): {cmtEMG}
"""],

##-------------------------------------------------------------------------
# Fixed text block
#
"""

Alaraajan liikelaajuus- ja spastisuusmittaukset (oikea/vasen):
Modified Tardieu Scale (R1=catch, R2=passiivinen liikelaajuus)
Modified Ashworth Scale (MAS), asteikko 0-4
NR = Normaalirajoissa
""",

##-------------------------------------------------------------------------
# Nilkka
#
[
"""
Nilkka:
""",
# the f-string is used to immediately evaluate the local _str variables and pass
# on the remaining variable names (in double braces) without evaluation; this
# way, the block can still be discarded if the variables are at default values
f"Soleus catch (R1): {{NilkkaSoleusCatchOik}}{str_NilkkaSoleusKlonusOik}/{{NilkkaSoleusCatchVas}}{str_NilkkaSoleusKlonusVas}\n",
f"Nilkan koukistus polvi koukussa: pass. (R2) {{NilkkaDorsifPolvi90PROMOik}}/{{NilkkaDorsifPolvi90PROMVas}}, akt. {{NilkkaDorsifPolvi90AROMOik}}{str_NilkkaDorsifPolvi90AROMEversioOik}/{{NilkkaDorsifPolvi90AROMVas}}{str_NilkkaDorsifPolvi90AROMEversioVas}\n",
f"Gastrocnemius catch (R1): {{NilkkaGastroCatchOik}}{str_NilkkaGastroKlonusOik}/{{NilkkaGastroCatchVas}}{str_NilkkaGastroKlonusVas}\n",
f"Nilkan koukistus polvi suorana: pass. (R2) {{NilkkaDorsifPolvi0PROMOik}}/{{NilkkaDorsifPolvi0PROMVas}}, akt. {{NilkkaDorsifPolvi0AROMOik}}{str_NilkkaDorsifPolvi0AROMEversioOik}/{{NilkkaDorsifPolvi0AROMVas}}{str_NilkkaDorsifPolvi0AROMEversioVas}\n",
"Ojennus: pass. {NilkkaPlantaarifleksioPROMOik}/{NilkkaPlantaarifleksioPROMVas}, akt. {NilkkaPlantaarifleksioAROMOik}/{NilkkaPlantaarifleksioAROMVas}\n",
"Confusion-testi: oikea {NilkkaConfusionOik}, vasen {NilkkaConfusionVas}\n",
"MAS soleus: {NilkkaSoleusModAOik}/{NilkkaSoleusModAVas}\n", 
"MAS gastrocnemius: {NilkkaGastroModAOik}/{NilkkaGastroModAVas}\n",
"Kommentit (PROM): {cmtNilkkaPROM}\n",
"Kommentit (AROM): {cmtNilkkaAROM}\n",
"Kommentit (spastisuus): {cmtNilkkaSpast}\n",
],

##-------------------------------------------------------------------------
# Polvi
#
[
"""
Polvi:
""",
"Hamstring catch (R1): {PolviHamstringCatchOik}/{PolviHamstringCatchVas}\n",
"Popliteakulma: {PolviPopliteaVastakkLonkka0Oik}/{PolviPopliteaVastakkLonkka0Vas}\n",
"Popliteakulma (true): {PolviPopliteaVastakkLonkka90Oik}/{PolviPopliteaVastakkLonkka90Vas}\n",
"Rectus catch (R1): {PolviRectusCatchOik}/{PolviRectusCatchVas}\n",
"Polven ojennus: pass. {PolviEkstensioAvOik}/{PolviEkstensioAvVas}, vapaasti {PolviEkstensioVapOik}/{PolviEkstensioVapVas}\n",
"Polven koukistus pass. (vatsamakuu) (R2): {PolviFleksioVatsamakuuOik}/{PolviFleksioVatsamakuuVas}\n",
"Polven koukistus pass. (selinmakuu): {PolviFleksioSelinmakuuOik}/{PolviFleksioSelinmakuuVas}\n",
"Extensor lag: {LonkkaExtLagOik}/{LonkkaExtLagVas}\n",
"MAS (hamstring): {PolviHamstringModAOik}/{PolviHamstringModAVas}\n",
"MAS (rectus): {PolviRectusModAOik}/{PolviRectusModAVas}\n",
"Kommentit (PROM): {cmtPolviPROM}\n",
"Kommentit (spastisuus): {cmtPolviSpast}\n",
],

##-------------------------------------------------------------------------
# Lonkka
#
[
"""
Lonkka:
""",
"Thomasin testi pass.: {LonkkaEkstensioAvOik}/{LonkkaEkstensioAvVas}\n",
"Thomasin testi polvi koukussa: {LonkkaEkstensioPolvi90Oik}/{LonkkaEkstensioPolvi90Vas}\n",
"Thomasin testi vapaasti: {LonkkaEkstensioVapOik}/{LonkkaEkstensioVapVas}\n",
"Lonkan koukistus: {LonkkaFleksioOik}/{LonkkaFleksioVas}\n",
"Adduktor catch (R1): {LonkkaAdduktoritCatchOik}/{LonkkaAdduktoritCatchVas}\n",
"Lonkan loitonnus polvi suorana (R2): {LonkkaAbduktioLonkka0Oik}/{LonkkaAbduktioLonkka0Vas}\n",
"Lonkan loitonnus lonkka suorana ja polvi koukussa (R2): {LonkkaAbduktioLonkka0Polvi90Oik}/{LonkkaAbduktioLonkka0Polvi90Vas}\n",
"Lonkka koukussa: {LonkkaAbduktioLonkkaFleksOik}/{LonkkaAbduktioLonkkaFleksVas}\n",
"Lonkan lähennys: {LonkkaAdduktioOik}/{LonkkaAdduktioVas}\n",
"Sisäkierto: {LonkkaSisakiertoOik}/{LonkkaSisakiertoVas}\n",
"Ulkokierto: {LonkkaUlkokiertoOik}/{LonkkaUlkokiertoVas}\n",
"MAS, lonkan adduktorit: {LonkkaAdduktoritModAOik}/{LonkkaAdduktoritModAVas}\n",
"MAS, lonkan ojentajat: {LonkkaEkstensioModAOik}/{LonkkaEkstensioModAVas}\n",
"MAS, lonkan koukistajat: {LonkkaFleksioModAOik}/{LonkkaFleksioModAVas}\n",
"MAS, lonkan sisäkiertäjät: {LonkkaSisakiertoModAOik}/{LonkkaSisakiertoModAVas}\n",
"MAS, lonkan ulkokiertäjät: {LonkkaUlkokiertoModAOik}/{LonkkaUlkokiertoModAVas}\n",
"Ober test: oikea {LonkkaOberOik} vasen {LonkkaOberVas}\n",
"Kommentit (lonkka PROM): {cmtLonkkaPROM}\n",
"Kommentit (lonkka, spatisuus): {cmtLonkkaSpast}\n",
"Kommentit (lonkka, muut): {cmtLonkkaMuut}\n",
],

##-------------------------------------------------------------------------
# Luiset asennot
#
[
"""
Luiset asennot:
""",
"Jalkaterä-reisi -kulma: {VirheasJalkaReisiOik}/{VirheasJalkaReisiVas}\n",
"Jalkaterän etu-takaosan kulma: {VirheasJalkateraEtuTakaOik}/{VirheasJalkateraEtuTakaVas}\n",
"Bimalleoli-akseli: {VirheasBimalleoliOik}/{VirheasBimalleoliVas}\n",
"2nd toe -testi: {Virheas2ndtoeOik}/{Virheas2ndtoeVas}\n",
"Patella alta: {VirheasPatellaAltaOik}/{VirheasPatellaAltaVas}\n",
"Polven valgus: {PolvenValgusOik}/{PolvenValgusVas}\n",
"Q-kulma: {QkulmaOik}/{QkulmaVas}\n",
"Lonkan anteversio: {VirheasAnteversioOik}/{VirheasAnteversioVas}\n",
"Alaraajojen pituus: {AntropAlaraajaOik}/{AntropAlaraajaVas}\n",
"Jalkaterien pituus: {AntropJalkateraOik}/{AntropJalkateraVas}\n",
"Kommentit (luiset asennot): {cmtVirheas}\n",
],

##-------------------------------------------------------------------------
# Jalkaterä kuormittamattomana
#
[
"""
Jalkaterä kuormittamattomana (oikea/vasen; + = lievä, ++ = kohtalainen, +++ = voimakas):
""",
"Subtalar neutraali-asento: {JalkatSubtalarOik}/{JalkatSubtalarVas}\n",
"Takaosan asento: {JalkatTakaosanAsentoOik}/{JalkatTakaosanAsentoVas}\n",
"Takaosan liike eversioon: {JalkatTakaosanLiikeEversioOik}/{JalkatTakaosanLiikeEversioVas}\n",
"Takaosan liike inversioon: {JalkatTakaosanLiikeInversioOik}/{JalkatTakaosanLiikeInversioVas}\n",
"Med. holvikaari: {JalkatHolvikaariOik}/{JalkatHolvikaariVas}\n",
"Midtarsaalinivelen liike: {JalkatKeskiosanliikeOik}/{JalkatKeskiosanliikeVas}\n",
"Etuosan asento 1: {JalkatEtuosanAsento1Oik}/{JalkatEtuosanAsento1Vas}\n",
"Etuosan asento 2: {JalkatEtuosanAsento2Oik}/{JalkatEtuosanAsento2Vas}\n",
"1. säde: {Jalkat1sadeOik}/{Jalkat1sadeVas}\n",
"1. MTP ojennus: {Jalkat1MTPojennusOik}/{Jalkat1MTPojennusVas}\n",
"Vaivaisenluu: {JalkatVaivaisenluuOik}/{JalkatVaivaisenluuVas}\n",
"Kovettumat oikea: {JalkatKovettumatOik}\n",
"Kovettumat vasen: {JalkatKovettumatVas}\n",
"Kommentit (jalkaterä kuormittamattomana): {cmtJalkateraKuormittamattomana}\n",
],

##-------------------------------------------------------------------------
# Jalkaterä kuormitettuna
#
[
"""
Jalkaterä kuormitettuna (oikea/vasen; + = lievä, ++ = kohtalainen, +++ = voimakas):
""",
"Takaosan (kantaluun) asento: {JalkatTakaosanAsentoKuormOik}/{JalkatTakaosanAsentoKuormVas}\n"
"Takaosan kierto: {JalkatTakaosanKiertoKuormOik}/{JalkatTakaosanKiertoKuormVas}\n",
"Keskiosan asento: {JalkatKeskiosanAsentoKuormOik}/{JalkatKeskiosanAsentoKuormVas}\n",
"Etuosan asento 1: {JalkatEtuosanAsento1KuormOik}/{JalkatEtuosanAsento1KuormVas}\n",
"Etuosan asento 2: {JalkatEtuosanAsento2KuormOik}/{JalkatEtuosanAsento2KuormVas}\n",
"Takaosan kierto: {JalkatTakaosanKiertoKuormOik}/{JalkatTakaosanKiertoKuormVas}\n",
"Feissin linja: {JalkatFeissinLinjaOik}/{JalkatFeissinLinjaVas}\n",
"Navicular drop istuen: {JalkatNavDropIstuenOik}/{JalkatNavDropIstuenVas}\n",
"Navicular drop seisten: {JalkatNavDropSeistenOik}/{JalkatNavDropSeistenVas}\n",
"Jackin testi: {JalkatJackTestiOik}/{JalkatJackTestiVas}\n",
"Colemanin block -testi: {JalkatColemanOik}/{JalkatColemanVas}\n",
"Kommentit (jalkaterä kuormitettuna): {cmtJalkateraKuormitettuna}\n",
],

##-------------------------------------------------------------------------
# Manuaalisesti mitattu lihasvoima
#
[
"""
Manuaalisesti mitattu lihasvoima (asteikko 0-5, missä 5 on vahvin, ja 3 voittaa painovoiman koko potilaan liikelaajuudella):
""",
"Nilkan koukistus: {VoimaTibialisAnteriorOik}/{VoimaTibialisAnteriorVas}\n",
"Nilkan ojennus (gastrocnemius): {VoimaGastroOik}/{VoimaGastroVas}\n",
"Nilkan ojennus (soleus): {VoimaSoleusOik}/{VoimaSoleusVas}\n",
"Inversio: {VoimaTibialisPosteriorOik}/{VoimaTibialisPosteriorVas}\n"
"Eversio: {VoimaPeroneusOik}/{VoimaPeroneusVas}\n",
"Isovarpaan ojennus: {VoimaExtHallucisLongusOik}/{VoimaExtHallucisLongusVas}\n",
"Isovarpaan koukistus: {VoimaFlexHallucisLongusOik}/{VoimaFlexHallucisLongusVas}\n",
"Varpaiden (2-5) ojennus: {Voima25OjennusOik}/{Voima25OjennusVas}\n",
"Varpaiden (2-5) koukistus: {Voima25KoukistusOik}/{Voima25KoukistusVas}\n",
"Polven ojennus: {VoimaPolviEkstensioOik}/{VoimaPolviEkstensioVas}\n",
"Polven koukistus: {VoimaPolviFleksioOik}/{VoimaPolviFleksioVas}\n",
"Lonkan ojennus: {VoimaLonkkaEkstensioPolvi0Oik}/{VoimaLonkkaEkstensioPolvi0Vas}\n",
"Lonkan ojennus polvi koukussa: {VoimaLonkkaEkstensioPolvi90Oik}/{VoimaLonkkaEkstensioPolvi90Vas}\n",
"Lonkan koukistus: {VoimaLonkkaFleksioOik}/{VoimaLonkkaFleksioVas}\n",
"Lonkan loitonnus: {VoimaLonkkaAbduktioLonkka0Oik}/{VoimaLonkkaAbduktioLonkka0Vas}\n",
"Lonkan loitonnus lonkka koukussa: {VoimaLonkkaAbduktioLonkkaFleksOik}/{VoimaLonkkaAbduktioLonkkaFleksVas}\n",
"Lonkan lähennys: {VoimaLonkkaAdduktioOik}/{VoimaLonkkaAdduktioVas}\n",
"Lonkan sisäkierto: {VoimaLonkkaSisakiertoOik}/{VoimaLonkkaSisakiertoVas}\n",
"Lonkan ulkokierto: {VoimaLonkkaUlkokiertoOik}/{VoimaLonkkaUlkokiertoVas}\n",
"Suorat vatsalihakset: {VoimaVatsaSuorat}\n",
"Vinot vatsalihakset: {VoimaVatsaVinotOik}/{VoimaVatsaVinotVas}\n",
"Selkälihakset: {VoimaSelka}\n",
"Kommentit (voima): {cmtVoima1} {cmtVoima2}\n",
],

##-------------------------------------------------------------------------
# Selektiivisyys
#
[
"""
Selektiivisyys (asteikko 0-2, missä 0=kokonaisliikemalli, 1=osittain eriytynyt ja 2=eriytynyt koko liikelaajuudella):
""",
"Nilkan koukistus: {SelTibialisAnteriorOik}/{SelTibialisAnteriorVas}\n",
"Nilkan ojennus (gastrocnemius): {SelGastroOik}/{SelGastroVas}\n",
"Nilkan ojennus (soleus): {SelSoleusOik}/{SelSoleusVas}\n",
"Inversio: {SelTibialisPosteriorOik}/{SelTibialisPosteriorVas}\n",
"Eversio: {SelPeroneusOik}/{SelPeroneusVas}\n",
"Isovarpaan ojennus: {SelExtHallucisLongusOik}/{SelExtHallucisLongusVas}\n",
"Isovarpaan koukistus: {SelFlexHallucisLongusOik}/{SelFlexHallucisLongusVas}\n",
"Varpaiden (2-5) ojennus: {Sel25OjennusOik}/{Sel25OjennusVas}\n",
"Varpaiden (2-5) koukistus: {Sel25KoukistusOik}/{Sel25KoukistusVas}\n",
"Polven ojennus: {SelPolviEkstensioOik}/{SelPolviEkstensioVas}\n",
"Polven koukistus: {SelPolviFleksioOik}/{SelPolviFleksioVas}\n",
"Lonkan ojennus: {SelLonkkaEkstensioPolvi0Oik}/{SelLonkkaEkstensioPolvi0Vas}\n",
"Lonkan ojennus polvi koukussa: {SelLonkkaEkstensioPolvi90Oik}/{SelLonkkaEkstensioPolvi90Vas}\n",
"Lonkan koukistus: {SelLonkkaFleksioOik}/{SelLonkkaFleksioVas}\n",
"Lonkan loitonnus: {SelLonkkaAbduktioLonkka0Oik}/{SelLonkkaAbduktioLonkka0Vas}\n",
"Lonkan lähennys: {SelLonkkaAdduktioOik}/{SelLonkkaAdduktioVas}\n",
"Lonkan sisäkierto: {SelLonkkaSisakiertoOik}/{SelLonkkaSisakiertoVas}\n",
"Lonkan ulkokierto: {SelLonkkaUlkokiertoOik}/{SelLonkkaUlkokiertoVas}\n",
],
]
