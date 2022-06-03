# -*- coding: utf-8 -*-
"""
Python template for the text report. This is a Python file called by exec() and
works by modifying an existing variable called 'self' (instance of Report
class).

The idea is to add 'text blocks' containing text and fields to a Report()
instance (called report) one by one. The field values are automatically filled
in by the Report class. If all variables for the block have default values (i.e.
were not measured) the Report instance will discard that block.

The philosophy is to have the template as text-like as possible for maximum
readability, and minimize the use of Python code inside the template.

@author: Jussi (jnu@iki.fi)
"""
from gaitbase.constants import Constants

self += """

LIIKELAAJUUDET JA VOIMAT

Patient code: {TiedotID}
Patient name: {TiedotNimi}
Social security number: {TiedotHetu}
Diagnosis: {TiedotDiag}
Date of gait analysis: {TiedotPvm}
"""
self += 'Kommentit: {cmtTiedot}\n'

self += """
ANTROPOMETRISET MITAT:
Alaraajat: {AntropAlaraajaOik} / {AntropAlaraajaVas}
Nilkat: {AntropNilkkaOik} / {AntropNilkkaVas}
Polvet: {AntropPolviOik} / {AntropPolviVas}
Paino: {AntropPaino}
Pituus: {AntropPituus}
SIAS: {AntropSIAS}
Kengännumero: {AntropKenganNumeroOik} / {AntropKenganNumeroVas}
"""
self += 'Kommentit: {cmtAntrop}\n'

self += """
MITTAAJAT:
{TiedotMittaajat}
"""

self += """
TULOSYY:


PÄÄTULOKSET KÄVELYANALYYSIN POHJALTA:


TESTAUS- JA ARVIOINTITULOKSET:


OHEISMITTAUSTEN TULOKSET:

"""

self += """
Nivelten passiiviset liikelaajuudet (oikea/vasen), NR = normaalin rajoissa:
"""
self += 'Lonkka: '
self += 'Thomasin testi (vapaasti) {LonkkaEkstensioVapOik}/{LonkkaEkstensioVapVas}. '
self += 'Thomasin testi (avustettuna) {LonkkaEkstensioAvOik}/{LonkkaEkstensioAvVas}. '
self += 'Thomasin testi (polvi 90°) {LonkkaEkstensioPolvi90Oik}/{LonkkaEkstensioPolvi90Vas}. ' 
self += 'Koukistus {LonkkaFleksioOik}/{LonkkaFleksioVas}. '
self += 'Loitonnus (lonkka 0°, polvi 90°) {LonkkaAbduktioLonkka0Polvi90Oik}/{LonkkaAbduktioLonkka0Polvi90Vas}. '
self += 'Loitonnus (lonkka 0°, polvi 0°) {LonkkaAbduktioLonkka0Oik}/{LonkkaAbduktioLonkka0Vas}. '
self += 'Loitonnus (lonkka 90°) {LonkkaAbduktioLonkkaFleksOik}/{LonkkaAbduktioLonkkaFleksVas}. '
self += 'Lähennys {LonkkaAdduktioOik}/{LonkkaAdduktioVas}. '
self += 'Sisäkierto {LonkkaSisakiertoOik}/{LonkkaSisakiertoVas}. '
self += 'Ulkokierto {LonkkaUlkokiertoOik}/{LonkkaUlkokiertoVas}. '
self += '\n'
self += 'Kommentit: {cmtLonkkaPROM}\n'
self += '\n'
self += 'Polvi: '
self += 'Ojennus (vapaasti) {PolviEkstensioVapOik}/{PolviEkstensioVapVas}. '
self += 'Ojennus (avustettuna) {PolviEkstensioAvOik}/{PolviEkstensioAvVas}. '
self += 'Koukistus (vatsamakuu) {PolviFleksioVatsamakuuOik}/{PolviFleksioVatsamakuuVas}. '
self += 'Koukistus (selinmakuu) {PolviFleksioSelinmakuuOik}/{PolviFleksioSelinmakuuVas}. '
self += 'Popliteakulma {PolviPopliteaVastakkLonkka0Oik}/{PolviPopliteaVastakkLonkka0Vas}, popliteakulma (true) {PolviPopliteaVastakkLonkka90Oik}/{PolviPopliteaVastakkLonkka90Vas}.'
self += '\n'
self += 'Kommentit: {cmtPolviPROM}\n'
self += '\n'
self += 'Nilkka: '
self += 'Koukistus (polvi 90°) {NilkkaDorsifPolvi90PROMOik}/{NilkkaDorsifPolvi90PROMVas}. '
self += 'Koukistus (polvi 0°) {NilkkaDorsifPolvi0PROMOik}/{NilkkaDorsifPolvi0PROMVas}. '
self += 'Ojennus {NilkkaPlantaarifleksioPROMOik}/{NilkkaPlantaarifleksioPROMVas}.'
self += '\n'
self += 'Kommentit: {cmtNilkkaPROM}\n'

# for 'eversio' extra info and similar things later:
# we have to add item separators in a 'smart' way since we do not know
# which items actually get printed
self += """
Nivelten aktiiviset liikelaajuudet: 
"""
self += 'Nilkka: '
self += 'Koukistus (polvi 90°) {NilkkaDorsifPolvi90AROMOik}/{NilkkaDorsifPolvi90AROMVas}'
self += ' (pyrkii lisäksi eversioon {NilkkaDorsifPolvi90AROMEversioOik}/{NilkkaDorsifPolvi90AROMEversioVas})'
self.item_sep()
self += 'Koukistus (polvi 0°) {NilkkaDorsifPolvi0AROMOik}/{NilkkaDorsifPolvi0AROMVas}'
self += ' (pyrkii lisäksi eversioon {NilkkaDorsifPolvi0AROMEversioOik}/{NilkkaDorsifPolvi0AROMEversioVas})'
self.item_sep()
self += 'Ojennus {NilkkaPlantaarifleksioAROMOik}/{NilkkaPlantaarifleksioAROMVas}. '
self += '\n'
self += 'Kommentit: {cmtNilkkaAROM}\n'

self += """
Alaraajojen spastisuus:
"""
self += 'Catch: Lonkan adduktorit {LonkkaAdduktoritCatchOik}/{LonkkaAdduktoritCatchVas}. '
self += 'Hamstringit {PolviHamstringCatchOik}/{PolviHamstringCatchVas}. '
self += 'Rectus femorikset {PolviRectusCatchOik}/{PolviRectusCatchVas}. '
self += 'Soleukset {NilkkaSoleusCatchOik}/{NilkkaSoleusCatchVas}'
self += ' (klonus {NilkkaSoleusKlonusOik}/{NilkkaSoleusKlonusVas})'
self.item_sep()
self += 'Gastrocnemiukset {NilkkaGastroCatchOik}/{NilkkaGastroCatchVas}'
self += ' (klonus {NilkkaGastroKlonusOik}/{NilkkaGastroKlonusVas})'
self.item_sep()
self += '\n'
self += 'Kommentit (lonkka): {cmtLonkkaSpast}\n'
self += 'Kommentit (nilkka): {cmtNilkkaSpast}\n'
self += 'Kommentit (polvi): {cmtPolviSpast}\n'

self += """
Luiset virheasennot: 
"""
self += 'Lonkan anteversio {VirheasAnteversioOik}/{VirheasAnteversioVas}. '
self += 'Jalkaterä-reisi -kulma {VirheasJalkaReisiOik}/{VirheasJalkaReisiVas}. '
self += 'Jalkaterän etu- takaosan kulma {VirheasJalkateraEtuTakaOik}/{VirheasJalkateraEtuTakaVas}. '
self += 'Bimalleoli -akseli {VirheasBimalleoliOik}/{VirheasBimalleoliVas}. '
self += '2nd toe test {Virheas2ndtoeOik}/{Virheas2ndtoeVas}. '
self += 'Patella alta {VirheasPatellaAltaOik}/{VirheasPatellaAltaVas}. '
self += 'Polven valgus {PolvenValgusOik}/{PolvenValgusVas}. '
self += 'Q-kulma {QkulmaOik}/{QkulmaVas}.'
self += '\n'
self += 'Kommentit: {cmtVirheas}\n'

self += """
Muita mittauksia:
"""
self += 'Alaraajat: {AntropAlaraajaOik} / {AntropAlaraajaVas}. '
self += 'Extensor lag {LonkkaExtLagOik}/{LonkkaExtLagVas}. '
self += 'Confusion test: {NilkkaConfusionOik}/{NilkkaConfusionVas}. '
self += 'Ober test {LonkkaOberOik}/{LonkkaOberVas}. '
self += 'Tasapaino: yhdellä jalalla seisominen {TasapOik}/{TasapVas}. '
self += '\n'
self += 'Kommentit (lonkka): {cmtLonkkaMuut}\n'
self += 'Kommentit (tasapaino): {cmtTasap}\n'

self += """
Jalkaterä kuormittamattomana (+ = lievä, ++ = kohtalainen, +++ = voimakas)
Lyhenteet: NEU=neutraali, TYYP=tyypillinen, RAJ=rajoittunut, VAR=varus, VALG=valgus:
"""
self += 'Subtalar neutraali-asento: {JalkatSubtalarOik}/{JalkatSubtalarVas}. '
self += 'Takaosan asento {JalkatTakaosanAsentoOik}/{JalkatTakaosanAsentoVas}. '
self += 'Takaosan liike eversioon {JalkatTakaosanLiikeEversioOik}/{JalkatTakaosanLiikeEversioVas}. '
self += 'Takaosan liike inversioon {JalkatTakaosanLiikeInversioOik}/{JalkatTakaosanLiikeInversioVas}. '
self += 'Med. holvikaari {JalkatHolvikaariOik}/{JalkatHolvikaariVas}. '
self += 'Keskiosan liike {JalkatKeskiosanliikeOik}/{JalkatKeskiosanliikeVas}. '
self += 'Etuosan asento 1: {JalkatEtuosanAsento1Oik}/{JalkatEtuosanAsento1Vas}. '
self += 'Etuosan asento 2: {JalkatEtuosanAsento2Oik}/{JalkatEtuosanAsento2Vas}. '
self += '1. säde: {Jalkat1sadeOik}/{Jalkat1sadeVas}. '
self += '1 MTP dorsifleksio {Jalkat1MTPojennusOik}/{Jalkat1MTPojennusVas}. '
self += 'Vaivaisenluu {JalkatVaivaisenluuOik}/{JalkatVaivaisenluuVas}. '
self += 'Kovettumat: {JalkatKovettumatOik}/{JalkatKovettumatVas}.'
self += '\n'
self += 'Kommentit (jalkaterä): {cmtJalkateraKuormittamattomana}\n'

self += """
Jalkaterä kuormitettuna: (+ = lievä, ++ = kohtalainen, +++ = voimakas):
"""
self += 'Takaosan (kantaluun) asento {JalkatTakaosanAsentoKuormOik}/{JalkatTakaosanAsentoKuormVas}. '
self += 'Keskiosan asento {JalkatKeskiosanAsentoKuormOik}/{JalkatKeskiosanAsentoKuormVas}. '
self += 'Etuosan asento 1: {JalkatEtuosanAsento1KuormOik}/{JalkatEtuosanAsento1KuormVas}, etuosan asento 2: {JalkatEtuosanAsento2KuormOik}/{JalkatEtuosanAsento2KuormVas}. '
self += 'Takaosan kierto: {JalkatTakaosanKiertoKuormOik}/{JalkatTakaosanKiertoKuormVas}. '
self += "Coleman's block test: {JalkatColemanOik}/{JalkatColemanVas}. "
self += 'Feissin linja: {JalkatFeissinLinjaOik} / {JalkatFeissinLinjaVas}. '
self += 'Navicular drop, istuen: {JalkatNavDropIstuenOik}/{JalkatNavDropIstuenVas}. '
self += 'Navicular drop, seisten: {JalkatNavDropSeistenOik}/{JalkatNavDropSeistenVas}. '
self += '\n'
self += 'Painelevymittaus: {Painelevy}\n'
self += 'Painelevymittaus, lisätietoja: {JalkatPainelevyTiedot}\n'
self += 'Kommentit (jalkaterä): {cmtJalkateraKuormitettuna}\n'

self += """
Modified Ashworth:
"""
self += 'Lonkan koukistajat {LonkkaFleksioModAOik}/{LonkkaFleksioModAVas}. '
self += 'Lonkan ojentajat {LonkkaEkstensioModAOik}/{LonkkaEkstensioModAVas}. '
self += 'Lonkan lähentäjät {LonkkaAdduktoritModAOik}/{LonkkaAdduktoritModAVas}. '
self += 'Hamstringit {PolviHamstringModAOik}/{PolviHamstringModAVas}. '
self += 'Rectus femoris {PolviRectusModAOik}/{PolviRectusModAVas}. '
self += 'Lonkan sisäkierto {LonkkaSisakiertoModAOik}/{LonkkaSisakiertoModAVas}. '
self += 'Lonkan ulkokierto {LonkkaUlkokiertoModAOik}/{LonkkaUlkokiertoModAVas}. '
self += 'Soleus {NilkkaSoleusModAOik}/{NilkkaSoleusModAVas}. '
self += 'Gastrocnemius {NilkkaGastroModAOik}/{NilkkaGastroModAVas}.'
self += '\n'
self += 'Kommentit (lonkka): {cmtLonkkaSpast}\n'

self += """
Manuaalisesti mitatut lihasvoimat ja selektiivisyys (oikea lihasvoima/vasen lihasvoima, (oikea selekt./vasen selekt.)):
Asteikko: 0-5, missä 5 on vahvin ja 3 voittaa painovoiman koko potilaan liikelaajuudella.
Selektiivisyys: 0-2, missä 0=kokonaisliikemalli, 1=osittain eriytynyt ja 2=eriytynyt koko liikelaajuudella:
"""
self += 'Lonkan ojennus (polvi 0°) {VoimaLonkkaEkstensioPolvi0Oik}/{VoimaLonkkaEkstensioPolvi0Vas}'
self += ' ({SelLonkkaEkstensioPolvi0Oik}/{SelLonkkaEkstensioPolvi0Vas})'
self.item_sep()
self += 'Lonkan ojennus (polvi 90°) {VoimaLonkkaEkstensioPolvi90Oik}/{VoimaLonkkaEkstensioPolvi90Vas}'
self += ' ({SelLonkkaEkstensioPolvi90Oik}/{SelLonkkaEkstensioPolvi90Vas})'
self.item_sep()
self += 'Lonkan koukistus {VoimaLonkkaFleksioOik}/{VoimaLonkkaFleksioVas}'
self += ' ({SelLonkkaFleksioOik}/{SelLonkkaFleksioVas})'
self.item_sep()
self += 'Loitonnus (lonkka 0°) {VoimaLonkkaAbduktioLonkka0Oik}/{VoimaLonkkaAbduktioLonkka0Vas}'
self += ' ({SelLonkkaAbduktioLonkka0Oik}/{SelLonkkaAbduktioLonkka0Vas})'
self.item_sep()
self += 'Loitonnus, lonkka fleksiossa {VoimaLonkkaAbduktioLonkkaFleksOik}/{VoimaLonkkaAbduktioLonkkaFleksVas}. '
self += 'Lähennys {VoimaLonkkaAdduktioOik}/{VoimaLonkkaAdduktioVas}'
self += ' ({SelLonkkaAdduktioOik}/{SelLonkkaAdduktioVas})'
self.item_sep()
self += 'Lonkan ulkokierto {VoimaLonkkaUlkokiertoOik}/{VoimaLonkkaUlkokiertoVas}'
self += ' ({SelLonkkaUlkokiertoOik}/{SelLonkkaUlkokiertoVas})'
self.item_sep()
self += 'Lonkan sisäkierto {VoimaLonkkaSisakiertoOik}/{VoimaLonkkaSisakiertoVas}'
self += ' ({SelLonkkaSisakiertoOik}/{SelLonkkaSisakiertoVas})'
self.item_sep()
self += 'Polven ojennus {VoimaPolviEkstensioOik}/{VoimaPolviEkstensioVas}'
self += ' ({SelPolviEkstensioOik}/{SelPolviEkstensioVas})'
self.item_sep()
self += 'Polven koukistus {VoimaPolviFleksioOik}/{VoimaPolviFleksioVas}'
self += ' ({SelPolviFleksioOik}/{SelPolviFleksioVas})'
self.item_sep()
self += 'Nilkan koukistus {VoimaTibialisAnteriorOik}/{VoimaTibialisAnteriorVas}'
self += ' ({SelTibialisAnteriorOik}/{SelTibialisAnteriorVas})'
self.item_sep()
self += 'Nilkan ojennus (gastrocnemius) {VoimaGastroOik}/{VoimaGastroVas}'
self += ' ({SelGastroOik}/{SelGastroVas})'
self.item_sep()
self += 'Nilkan ojennus (soleus) {VoimaSoleusOik}/{VoimaSoleusVas}'
self += ' ({SelSoleusOik}/{SelSoleusVas})'
self.item_sep()
self += 'Inversio {VoimaTibialisPosteriorOik}/{VoimaTibialisPosteriorVas}'
self += ' ({SelTibialisPosteriorOik}/{SelTibialisPosteriorVas})'
self.item_sep()
self += 'Eversio {VoimaPeroneusOik}/{VoimaPeroneusVas}'
self += ' ({SelPeroneusOik}/{SelPeroneusVas})'
self.item_sep()
self += 'Isovarpaan ojennus {VoimaExtHallucisLongusOik}/{VoimaExtHallucisLongusVas}'
self += ' ({SelExtHallucisLongusOik}/{SelExtHallucisLongusVas})'
self.item_sep()
self += 'Isovarpaan koukistus {VoimaFlexHallucisLongusOik}/{VoimaFlexHallucisLongusVas}'
self += ' ({SelFlexHallucisLongusOik}/{SelFlexHallucisLongusVas})'
self.item_sep()
self += 'Varpaiden (2-5) ojennus {Voima25OjennusOik}/{Voima25OjennusVas}'
self += ' ({Sel25OjennusOik}/{Sel25OjennusVas})'
self.item_sep()
self += 'Varpaiden (2-5) koukistus {Voima25KoukistusOik}/{Voima25KoukistusVas}'
self += ' ({Sel25KoukistusOik}/{Sel25KoukistusVas})'
self.item_sep()
self += 'Suorat vatsalihakset {VoimaVatsaSuorat}. '
self += 'Vinot vatsalihakset {VoimaVatsaVinotOik}/{VoimaVatsaVinotVas}. '
self += 'Selkälihakset {VoimaSelka}.'
self += '\n'
self += 'Kommentit (voimat): {cmtVoima1} {cmtVoima2} \n'

# some extra logic to add the names of EMG electrodes
emg_chs = {'EMGSol': 'soleus',
           'EMGGas': 'gastrocnemius',
           'EMGPer': 'peroneous',
           'EMGTibA': 'tibialis anterior',
           'EMGRec': 'rectus',
           'EMGHam': 'hamstring',
           'EMGVas': 'vastus',
           'EMGGlut': 'gluteus'}

emgs_in_use = [desc for ch, desc in emg_chs.items()
               if self.data[ch] == Constants.checkbox_yestext]
emgs_str = ', '.join(emgs_in_use)

if emgs_str:
    self += """
Dynaaminen EMG:
Alaraajojen lihasaktivaatio mitattiin pintaelektrodeilla seuraavista lihaksista:
"""
    self += emgs_str
    self += '\n'

self += 'Kommentit (EMG): {cmtEMG}\n'

self += """
SUUNNITELMA/POHDINTA:
"""
