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

NOTE: instead of modifying the package default template, it's better to keep and
modify a local copy, so the template will not be overwritten when updating the
package. The template path can be configured in the package configuration.


@author: Jussi (jnu@iki.fi)
"""

# relative imports may not work here, since the template can be located anywhere;
# it's safer to explicitly import from gaitbase
from gaitbase.constants import Constants

end_line = Constants.end_line  # constant indicating a 'smart' end-of-line

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
"""
Dyn EMG:
""",
str_emg_active,
"""
Kommentit (EMG): {cmtEMG}
""",

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
"""
Nilkka:
""",
# the f-string is used to immediately evaluate the local _str variables and pass
# on the remaining variable names (in double braces) without evaluation; this
# way, the block can still be discarded if the variables are at default values
f"soleus catch (R1): {{NilkkaSoleusCatchOik}}{str_NilkkaSoleusKlonusOik}/{{NilkkaSoleusCatchVas}}{str_NilkkaSoleusKlonusVas}\n",
f"nilkan koukistus polvi koukussa: pass. (R2) {{NilkkaDorsifPolvi90PROMOik}}/{{NilkkaDorsifPolvi90PROMVas}}, akt. {{NilkkaDorsifPolvi90AROMOik}}{str_NilkkaDorsifPolvi90AROMEversioOik}/{{NilkkaDorsifPolvi90AROMVas}}{str_NilkkaDorsifPolvi90AROMEversioVas}\n",
f"gastrocnemius catch (R1): {{NilkkaGastroCatchOik}}{str_NilkkaGastroKlonusOik}/{{NilkkaGastroCatchVas}}{str_NilkkaGastroKlonusVas}\n",
f"nilkan koukistus polvi suorana: pass. (R2) {{NilkkaDorsifPolvi0PROMOik}}/{{NilkkaDorsifPolvi0PROMVas}}, akt. {{NilkkaDorsifPolvi0AROMOik}}{str_NilkkaDorsifPolvi0AROMEversioOik}/{{NilkkaDorsifPolvi0AROMVas}}{str_NilkkaDorsifPolvi0AROMEversioVas}\n",
"ojennus: pass. {NilkkaPlantaarifleksioPROMOik}/{NilkkaPlantaarifleksioPROMVas}, akt. {NilkkaPlantaarifleksioAROMOik}/{NilkkaPlantaarifleksioAROMVas}\n",
"Confusion-testi: oikea {NilkkaConfusionOik}, vasen {NilkkaConfusionVas}\n",
"MAS soleus: {NilkkaSoleusModAOik}/{NilkkaSoleusModAVas}\n", 
"MAS gastrocnemius: {NilkkaGastroModAOik}/{NilkkaGastroModAVas}\n",
"Kommentit (PROM): {cmtNilkkaPROM}\n",
"Kommentit (AROM): {cmtNilkkaAROM}\n",
"Kommentit (spastisuus): {cmtNilkkaSpast}\n",

##-------------------------------------------------------------------------
# Polvi
#
"""
Polvi:
""",
"hamstring catch (R1): {PolviHamstringCatchOik}/{PolviHamstringCatchVas}\n",
"popliteakulma: {PolviPopliteaVastakkLonkka0Oik}/{PolviPopliteaVastakkLonkka0Vas}\n",
"popliteakulma (true): {PolviPopliteaVastakkLonkka90Oik}/{PolviPopliteaVastakkLonkka90Vas}\n",
"rectus catch (R1): {PolviRectusCatchOik}/{PolviRectusCatchVas}\n",
"polven ojennus: pass. {PolviEkstensioAvOik}/{PolviEkstensioAvVas}, vapaasti {PolviEkstensioVapOik}/{PolviEkstensioVapVas}\n",
"polven koukistus pass. (vatsamakuu) (R2): {PolviFleksioVatsamakuuOik}/{PolviFleksioVatsamakuuVas}\n",
"polven koukistus pass. (selinmakuu): {PolviFleksioSelinmakuuOik}/{PolviFleksioSelinmakuuVas}\n",
"Extensor lag: {LonkkaExtLagOik}/{LonkkaExtLagVas}\n",
"MAS (hamstring): {PolviHamstringModAOik}/{PolviHamstringModAVas}\n",
"MAS (rectus): {PolviRectusModAOik}/{PolviRectusModAVas}\n",
"Kommentit (PROM): {cmtPolviPROM}\n",
"Kommentit (spastisuus): {cmtPolviSpast}\n",

##-------------------------------------------------------------------------
# Lonkka
#
"""
Lonkka:
""",
"thomasin testi pass.: {LonkkaEkstensioAvOik}/{LonkkaEkstensioAvVas}\n",
"thomasin testi polvi koukussa: {LonkkaEkstensioPolvi90Oik}/{LonkkaEkstensioPolvi90Vas}\n",
"thomasin testi vapaasti: {LonkkaEkstensioVapOik}/{LonkkaEkstensioVapVas}\n",
"lonkan koukistus: {LonkkaFleksioOik}/{LonkkaFleksioVas}\n",
"adduktor catch (R1): {LonkkaAdduktoritCatchOik}/{LonkkaAdduktoritCatchVas}\n",
"lonkan loitonnus polvi suorana (R2): {LonkkaAbduktioLonkka0Oik}/{LonkkaAbduktioLonkka0Vas}\n",
"lonkan loitonnus lonkka suorana ja polvi koukussa (R2): {LonkkaAbduktioLonkka0Polvi90Oik}/{LonkkaAbduktioLonkka0Polvi90Vas}\n",
"lonkka koukussa: {LonkkaAbduktioLonkkaFleksOik}/{LonkkaAbduktioLonkkaFleksVas}\n",
"lonkan lähennys: {LonkkaAdduktioOik}/{LonkkaAdduktioVas}\n",
"sisäkierto: {LonkkaSisakiertoOik}/{LonkkaSisakiertoVas}\n",
"ulkokierto: {LonkkaUlkokiertoOik}/{LonkkaUlkokiertoVas}\n",
"MAS, lonkan adduktorit: {LonkkaAdduktoritModAOik}/{LonkkaAdduktoritModAVas}\n",
"MAS, lonkan ojentajat: {LonkkaEkstensioModAOik}/{LonkkaEkstensioModAVas}\n",
"MAS, lonkan koukistajat: {LonkkaFleksioModAOik}/{LonkkaFleksioModAVas}\n",
"MAS, lonkan sisäkiertäjät: {LonkkaSisakiertoModAOik}/{LonkkaSisakiertoModAVas}\n",
"MAS, lonkan ulkokiertäjät: {LonkkaUlkokiertoModAOik}/{LonkkaUlkokiertoModAVas}\n",
"ober test: oikea {LonkkaOberOik} vasen {LonkkaOberVas}\n",
"Kommentit (lonkka PROM): {cmtLonkkaPROM}\n",
"Kommentit (lonkka, spatisuus): {cmtLonkkaSpast}\n",
"Kommentit (lonkka, muut): {cmtLonkkaMuut}\n",

##-------------------------------------------------------------------------
# Luiset asennot
#
"""
Luiset asennot:
""",
"jalkaterä-reisi -kulma: {VirheasJalkaReisiOik}/{VirheasJalkaReisiVas}\n",
"jalkaterän etu-takaosan kulma: {VirheasJalkateraEtuTakaOik}/{VirheasJalkateraEtuTakaVas}\n",
"bimalleoli-akseli: {VirheasBimalleoliOik}/{VirheasBimalleoliVas}\n",
"2nd toe -testi: {Virheas2ndtoeOik}/{Virheas2ndtoeVas}\n",
"patella alta: {VirheasPatellaAltaOik}/{VirheasPatellaAltaVas}\n",
"polven valgus: {PolvenValgusOik}/{PolvenValgusVas}\n",
"Q-kulma: {QkulmaOik}/{QkulmaVas}\n",
"Lonkan anteversio: {VirheasAnteversioOik}/{VirheasAnteversioVas}\n",
"Alaraajojen pituus: {AntropAlaraajaOik}/{AntropAlaraajaVas}\n",
"Jalkaterien pituus: {AntropJalkateraOik}/{AntropJalkateraVas}\n",
"Kommentit (luiset asennot): {cmtVirheas}\n",

##-------------------------------------------------------------------------
# Jalkaterä kuormittamattomana
#
"""
Jalkaterä kuormittamattomana (oikea/vasen; + = lievä, ++ = kohtalainen, +++ = voimakas):
""",
"subtalar neutraali-asento: {JalkatSubtalarOik}/{JalkatSubtalarVas}\n",
"takaosan asento: {JalkatTakaosanAsentoOik}/{JalkatTakaosanAsentoVas}\n",
"takaosan liike eversioon: {JalkatTakaosanLiikeEversioOik}/{JalkatTakaosanLiikeEversioVas}\n",
"takaosan liike inversioon: {JalkatTakaosanLiikeInversioOik}/{JalkatTakaosanLiikeInversioVas}\n",
"med. holvikaari: {JalkatHolvikaariOik}/{JalkatHolvikaariVas}\n",
"midtarsaalinivelen liike: {JalkatKeskiosanliikeOik}/{JalkatKeskiosanliikeVas}\n",
"etuosan asento 1: {JalkatEtuosanAsento1Oik}/{JalkatEtuosanAsento1Vas}\n",
"etuosan asento 2: {JalkatEtuosanAsento2Oik}/{JalkatEtuosanAsento2Vas}\n",
"1. säde: {Jalkat1sadeOik}/{Jalkat1sadeVas}\n",
"1. MTP ojennus: {Jalkat1MTPojennusOik}/{Jalkat1MTPojennusVas}\n",
"vaivaisenluu: {JalkatVaivaisenluuOik}/{JalkatVaivaisenluuVas}\n",
"kovettumat oikea: {JalkatKovettumatOik}\n",
"kovettumat vasen: {JalkatKovettumatVas}\n",
"Kommentit (jalkaterä kuormittamattomana): {cmtJalkateraKuormittamattomana}\n",

##-------------------------------------------------------------------------
# Jalkaterä kuormitettuna
#
"""
Jalkaterä kuormitettuna (oikea/vasen; + = lievä, ++ = kohtalainen, +++ = voimakas):
""",
"takaosan (kantaluun) asento: {JalkatTakaosanAsentoKuormOik}/{JalkatTakaosanAsentoKuormVas}\n"
"takaosan kierto: {JalkatTakaosanKiertoKuormOik}/{JalkatTakaosanKiertoKuormVas}\n",
"keskiosan asento: {JalkatKeskiosanAsentoKuormOik}/{JalkatKeskiosanAsentoKuormVas}\n",
"etuosan asento 1: {JalkatEtuosanAsento1KuormOik}/{JalkatEtuosanAsento1KuormVas}\n",
"etuosan asento 2: {JalkatEtuosanAsento2KuormOik}/{JalkatEtuosanAsento2KuormVas}\n",
"takaosan kierto: {JalkatTakaosanKiertoKuormOik}/{JalkatTakaosanKiertoKuormVas}\n",
"Feissin linja: {JalkatFeissinLinjaOik}/{JalkatFeissinLinjaVas}\n",
"navicular drop istuen: {JalkatNavDropIstuenOik}/{JalkatNavDropIstuenVas}\n",
"navicular drop seisten: {JalkatNavDropSeistenOik}/{JalkatNavDropSeistenVas}\n",
"Jackin testi: {JalkatJackTestiOik}/{JalkatJackTestiVas}\n",
"Colemanin block -testi: {JalkatColemanOik}/{JalkatColemanVas}\n",
"Kommentit (jalkaterä kuormitettuna): {cmtJalkateraKuormitettuna}\n",

##-------------------------------------------------------------------------
# Manuaalisesti mitattu lihasvoima
#
"""
Manuaalisesti mitattu lihasvoima (asteikko 0-5, missä 5 on vahvin, ja 3 voittaa painovoiman koko potilaan liikelaajuudella):
""",
"nilkan koukistus: {VoimaTibialisAnteriorOik}/{VoimaTibialisAnteriorVas}\n",
"nilkan ojennus (gastrocnemius): {VoimaGastroOik}/{VoimaGastroVas}\n",
"nilkan ojennus (soleus): {VoimaSoleusOik}/{VoimaSoleusVas}\n",
"inversio: {VoimaTibialisPosteriorOik}/{VoimaTibialisPosteriorVas}\n"
"eversio: {VoimaPeroneusOik}/{VoimaPeroneusVas}\n",
"isovarpaan ojennus: {VoimaExtHallucisLongusOik}/{VoimaExtHallucisLongusVas}\n",
"isovarpaan koukistus: {VoimaFlexHallucisLongusOik}/{VoimaFlexHallucisLongusVas}\n",
"varpaiden (2-5) ojennus: {Voima25OjennusOik}/{Voima25OjennusVas}\n",
"varpaiden (2-5) koukistus: {Voima25KoukistusOik}/{Voima25KoukistusVas}\n",
"polven ojennus: {VoimaPolviEkstensioOik}/{VoimaPolviEkstensioVas}\n",
"polven koukistus: {VoimaPolviFleksioOik}/{VoimaPolviFleksioVas}\n",
"lonkan ojennus: {VoimaLonkkaEkstensioPolvi0Oik}/{VoimaLonkkaEkstensioPolvi0Vas}\n",
"lonkan ojennus polvi koukussa: {VoimaLonkkaEkstensioPolvi90Oik}/{VoimaLonkkaEkstensioPolvi90Vas}\n",
"lonkan koukistus: {VoimaLonkkaFleksioOik}/{VoimaLonkkaFleksioVas}\n",
"lonkan loitonnus: {VoimaLonkkaAbduktioLonkka0Oik}/{VoimaLonkkaAbduktioLonkka0Vas}\n",
"lonkan loitonnus lonkka koukussa: {VoimaLonkkaAbduktioLonkkaFleksOik}/{VoimaLonkkaAbduktioLonkkaFleksVas}\n",
"lonkan lähennys: {VoimaLonkkaAdduktioOik}/{VoimaLonkkaAdduktioVas}\n",
"lonkan sisäkierto: {VoimaLonkkaSisakiertoOik}/{VoimaLonkkaSisakiertoVas}\n",
"lonkan ulkokierto: {VoimaLonkkaUlkokiertoOik}/{VoimaLonkkaUlkokiertoVas}\n",
"suorat vatsalihakset: {VoimaVatsaSuorat}\n",
"vinot vatsalihakset: {VoimaVatsaVinotOik}/{VoimaVatsaVinotVas}\n",
"selkälihakset: {VoimaSelka}\n",
"Kommentit (voima): {cmtVoima1} {cmtVoima2}\n",

##-------------------------------------------------------------------------
# Selektiivisyys
#
"""
Selektiivisyys (asteikko 0-2, missä 0=kokonaisliikemalli, 1=osittain eriytynyt ja 2=eriytynyt koko liikelaajuudella):
""",
"nilkan koukistus: {SelTibialisAnteriorOik}/{SelTibialisAnteriorVas}\n",
"nilkan ojennus (gastrocnemius): {SelGastroOik}/{SelGastroVas}\n",
"nilkan ojennus (soleus): {SelSoleusOik}/{SelSoleusVas}\n",
"inversio: {SelTibialisPosteriorOik}/{SelTibialisPosteriorVas}\n",
"eversio: {SelPeroneusOik}/{SelPeroneusVas}\n",
"isovarpaan ojennus: {SelExtHallucisLongusOik}/{SelExtHallucisLongusVas}\n",
"isovarpaan koukistus: {SelFlexHallucisLongusOik}/{SelFlexHallucisLongusVas}\n",
"varpaiden (2-5) ojennus: {Sel25OjennusOik}/{Sel25OjennusVas}\n",
"varpaiden (2-5) koukistus: {Sel25KoukistusOik}/{Sel25KoukistusVas}\n",
"polven ojennus: {SelPolviEkstensioOik}/{SelPolviEkstensioVas}\n",
"polven koukistus: {SelPolviFleksioOik}/{SelPolviFleksioVas}\n",
"lonkan ojennus: {SelLonkkaEkstensioPolvi0Oik}/{SelLonkkaEkstensioPolvi0Vas}\n",
"lonkan ojennus polvi koukussa: {SelLonkkaEkstensioPolvi90Oik}/{SelLonkkaEkstensioPolvi90Vas}\n",
"lonkan koukistus: {SelLonkkaFleksioOik}/{SelLonkkaFleksioVas}\n",
"lonkan loitonnus: {SelLonkkaAbduktioLonkka0Oik}/{SelLonkkaAbduktioLonkka0Vas}\n",
"lonkan lähennys: {SelLonkkaAdduktioOik}/{SelLonkkaAdduktioVas}\n",
"lonkan sisäkierto: {SelLonkkaSisakiertoOik}/{SelLonkkaSisakiertoVas}\n",
"lonkan ulkokierto: {SelLonkkaUlkokiertoOik}/{SelLonkkaUlkokiertoVas}\n",
]
