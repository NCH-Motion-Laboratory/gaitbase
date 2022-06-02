# -*- coding: utf-8 -*-
"""
Template for text report.

This is called by exec() and works by modifying an existing variable
called 'report' (instance of Report class)

The idea is to avoid putting the template code inside a function
call, which would lead to messy indentation.

@author: Jussi (jnu@iki.fi)
"""

report += """

LIIKELAAJUUDET JA VOIMAT

Patient code: {TiedotID}
Patient name: {TiedotNimi}
Social security number: {TiedotHetu}
Diagnosis: {TiedotDiag}
Date of gait analysis: {TiedotPvm}
"""
report += 'Kommentit: {cmtTiedot}\n'

report += """
ANTROPOMETRISET MITAT:
Alaraajat: {AntropAlaraajaOik} / {AntropAlaraajaVas}
Nilkat: {AntropNilkkaOik} / {AntropNilkkaVas}
Polvet: {AntropPolviOik} / {AntropPolviVas}
Paino: {AntropPaino}
Pituus: {AntropPituus}
SIAS: {AntropSIAS}
Kengännumero: {AntropKenganNumeroOik} / {AntropKenganNumeroVas}
"""
report += 'Kommentit: {cmtAntrop}\n'

report += """
MITTAAJAT:
{TiedotMittaajat}
"""

report += """
TULOSYY:


PÄÄTULOKSET KÄVELYANALYYSIN POHJALTA:


TESTAUS- JA ARVIOINTITULOKSET:


OHEISMITTAUSTEN TULOKSET:

"""

report += """
Nivelten passiiviset liikelaajuudet (oikea/vasen), NR = normaalin rajoissa:
"""
report += 'Lonkka: '
report += 'Thomasin testi (vapaasti) {LonkkaEkstensioVapOik}/{LonkkaEkstensioVapVas}. '
report += 'Thomasin testi (avustettuna) {LonkkaEkstensioAvOik}/{LonkkaEkstensioAvVas}. '
report += 'Thomasin testi (polvi 90°) {LonkkaEkstensioPolvi90Oik}/{LonkkaEkstensioPolvi90Vas}. ' 
report += 'Koukistus {LonkkaFleksioOik}/{LonkkaFleksioVas}. '
report += 'Loitonnus (lonkka 0°, polvi 90°) {LonkkaAbduktioLonkka0Polvi90Oik}/{LonkkaAbduktioLonkka0Polvi90Vas}. '
report += 'Loitonnus (lonkka 0°, polvi 0°) {LonkkaAbduktioLonkka0Oik}/{LonkkaAbduktioLonkka0Vas}. '
report += 'Loitonnus (lonkka 90°) {LonkkaAbduktioLonkkaFleksOik}/{LonkkaAbduktioLonkkaFleksVas}. '
report += 'Lähennys {LonkkaAdduktioOik}/{LonkkaAdduktioVas}. '
report += 'Sisäkierto {LonkkaSisakiertoOik}/{LonkkaSisakiertoVas}. '
report += 'Ulkokierto {LonkkaUlkokiertoOik}/{LonkkaUlkokiertoVas}. '
report += '\n'
report += 'Kommentit: {cmtLonkkaPROM}\n'
report += '\n'
report += 'Polvi: '
report += 'Ojennus (vapaasti) {PolviEkstensioVapOik}/{PolviEkstensioVapVas}. '
report += 'Ojennus (avustettuna) {PolviEkstensioAvOik}/{PolviEkstensioAvVas}. '
report += 'Koukistus (vatsamakuu) {PolviFleksioVatsamakuuOik}/{PolviFleksioVatsamakuuVas}. '
report += 'Koukistus (selinmakuu) {PolviFleksioSelinmakuuOik}/{PolviFleksioSelinmakuuVas}. '
report += 'Popliteakulma {PolviPopliteaVastakkLonkka0Oik}/{PolviPopliteaVastakkLonkka0Vas}, popliteakulma (true) {PolviPopliteaVastakkLonkka90Oik}/{PolviPopliteaVastakkLonkka90Vas}.'
report += '\n'
report += 'Kommentit: {cmtPolviPROM}\n'
report += '\n'
report += 'Nilkka: '
report += 'Koukistus (polvi 90°) {NilkkaDorsifPolvi90PROMOik}/{NilkkaDorsifPolvi90PROMVas}. '
report += 'Koukistus (polvi 0°) {NilkkaDorsifPolvi0PROMOik}/{NilkkaDorsifPolvi0PROMVas}. '
report += 'Ojennus {NilkkaPlantaarifleksioPROMOik}/{NilkkaPlantaarifleksioPROMVas}.'
report += '\n'
report += 'Kommentit: {cmtNilkkaPROM}\n'

# for 'eversio' extra info and similar things later:
# we have to add item separators in a 'smart' way since we do not know
# which items actually get printed
report += """
Nivelten aktiiviset liikelaajuudet: 
"""
report += 'Nilkka: '
report += 'Koukistus (polvi 90°) {NilkkaDorsifPolvi90AROMOik}/{NilkkaDorsifPolvi90AROMVas}'
report += ' (pyrkii lisäksi eversioon {NilkkaDorsifPolvi90AROMEversioOik}/{NilkkaDorsifPolvi90AROMEversioVas})'
report.item_sep()
report += 'Koukistus (polvi 0°) {NilkkaDorsifPolvi0AROMOik}/{NilkkaDorsifPolvi0AROMVas}'
report += ' (pyrkii lisäksi eversioon {NilkkaDorsifPolvi0AROMEversioOik}/{NilkkaDorsifPolvi0AROMEversioVas})'
report.item_sep()
report += 'Ojennus {NilkkaPlantaarifleksioAROMOik}/{NilkkaPlantaarifleksioAROMVas}. '
report += '\n'
report += 'Kommentit: {cmtNilkkaAROM}\n'

report += """
Alaraajojen spastisuus:
"""
report += 'Catch: Lonkan adduktorit {LonkkaAdduktoritCatchOik}/{LonkkaAdduktoritCatchVas}. '
report += 'Hamstringit {PolviHamstringCatchOik}/{PolviHamstringCatchVas}. '
report += 'Rectus femorikset {PolviRectusCatchOik}/{PolviRectusCatchVas}. '
report += 'Soleukset {NilkkaSoleusCatchOik}/{NilkkaSoleusCatchVas}'
report += ' (klonus {NilkkaSoleusKlonusOik}/{NilkkaSoleusKlonusVas})'
report.item_sep()
report += 'Gastrocnemiukset {NilkkaGastroCatchOik}/{NilkkaGastroCatchVas}'
report += ' (klonus {NilkkaGastroKlonusOik}/{NilkkaGastroKlonusVas})'
report.item_sep()
report += '\n'
report += 'Kommentit (lonkka): {cmtLonkkaSpast}\n'
report += 'Kommentit (nilkka): {cmtNilkkaSpast}\n'
report += 'Kommentit (polvi): {cmtPolviSpast}\n'

report += """
Luiset virheasennot: 
"""
report += 'Lonkan anteversio {VirheasAnteversioOik}/{VirheasAnteversioVas}. '
report += 'Jalkaterä-reisi -kulma {VirheasJalkaReisiOik}/{VirheasJalkaReisiVas}. '
report += 'Jalkaterän etu- takaosan kulma {VirheasJalkateraEtuTakaOik}/{VirheasJalkateraEtuTakaVas}. '
report += 'Bimalleoli -akseli {VirheasBimalleoliOik}/{VirheasBimalleoliVas}. '
report += '2nd toe test {Virheas2ndtoeOik}/{Virheas2ndtoeVas}. '
report += 'Patella alta {VirheasPatellaAltaOik}/{VirheasPatellaAltaVas}. '
report += 'Polven valgus {PolvenValgusOik}/{PolvenValgusVas}. '
report += 'Q-kulma {QkulmaOik}/{QkulmaVas}.'
report += '\n'
report += 'Kommentit: {cmtVirheas}\n'

report += """
Muita mittauksia:
"""
report += 'Alaraajat: {AntropAlaraajaOik} / {AntropAlaraajaVas}. '
report += 'Extensor lag {LonkkaExtLagOik}/{LonkkaExtLagVas}. '
report += 'Confusion test: {NilkkaConfusionOik}/{NilkkaConfusionVas}. '
report += 'Ober test {LonkkaOberOik}/{LonkkaOberVas}. '
report += 'Tasapaino: yhdellä jalalla seisominen {TasapOik}/{TasapVas}. '
report += '\n'
report += 'Kommentit (lonkka): {cmtLonkkaMuut}\n'
report += 'Kommentit (tasapaino): {cmtTasap}\n'

report += """
Jalkaterä kuormittamattomana (+ = lievä, ++ = kohtalainen, +++ = voimakas)
Lyhenteet: NEU=neutraali, TYYP=tyypillinen, RAJ=rajoittunut, VAR=varus, VALG=valgus:
"""
report += 'Subtalar neutraali-asento: {JalkatSubtalarOik}/{JalkatSubtalarVas}. '
report += 'Takaosan asento {JalkatTakaosanAsentoOik}/{JalkatTakaosanAsentoVas}. '
report += 'Takaosan liike eversioon {JalkatTakaosanLiikeEversioOik}/{JalkatTakaosanLiikeEversioVas}. '
report += 'Takaosan liike inversioon {JalkatTakaosanLiikeInversioOik}/{JalkatTakaosanLiikeInversioVas}. '
report += 'Med. holvikaari {JalkatHolvikaariOik}/{JalkatHolvikaariVas}. '
report += 'Keskiosan liike {JalkatKeskiosanliikeOik}/{JalkatKeskiosanliikeVas}. '
report += 'Etuosan asento 1: {JalkatEtuosanAsento1Oik}/{JalkatEtuosanAsento1Vas}. '
report += 'Etuosan asento 2: {JalkatEtuosanAsento2Oik}/{JalkatEtuosanAsento2Vas}. '
report += '1. säde: {Jalkat1sadeOik}/{Jalkat1sadeVas}. '
report += '1 MTP dorsifleksio {Jalkat1MTPojennusOik}/{Jalkat1MTPojennusVas}. '
report += 'Vaivaisenluu {JalkatVaivaisenluuOik}/{JalkatVaivaisenluuVas}. '
report += 'Kovettumat: {JalkatKovettumatOik}/{JalkatKovettumatVas}.'
report += '\n'
report += 'Kommentit (jalkaterä): {cmtJalkateraKuormittamattomana}\n'

report += """
Jalkaterä kuormitettuna: (+ = lievä, ++ = kohtalainen, +++ = voimakas):
"""
report += 'Takaosan (kantaluun) asento {JalkatTakaosanAsentoKuormOik}/{JalkatTakaosanAsentoKuormVas}. '
report += 'Keskiosan asento {JalkatKeskiosanAsentoKuormOik}/{JalkatKeskiosanAsentoKuormVas}. '
report += 'Etuosan asento 1: {JalkatEtuosanAsento1KuormOik}/{JalkatEtuosanAsento1KuormVas}, etuosan asento 2: {JalkatEtuosanAsento2KuormOik}/{JalkatEtuosanAsento2KuormVas}. '
report += 'Takaosan kierto: {JalkatTakaosanKiertoKuormOik}/{JalkatTakaosanKiertoKuormVas}. '
report += "Coleman's block test: {JalkatColemanOik}/{JalkatColemanVas}. "
report += 'Feissin linja: {JalkatFeissinLinjaOik} / {JalkatFeissinLinjaVas}. '
report += 'Navicular drop, istuen: {JalkatNavDropIstuenOik}/{JalkatNavDropIstuenVas}. '
report += 'Navicular drop, seisten: {JalkatNavDropSeistenOik}/{JalkatNavDropSeistenVas}. '
report += '\n'
report += 'Painelevymittaus: {Painelevy}\n'
report += 'Painelevymittaus, lisätietoja: {JalkatPainelevyTiedot}\n'
report += 'Kommentit (jalkaterä): {cmtJalkateraKuormitettuna}\n'

report += """
Modified Ashworth:
"""
report += 'Lonkan koukistajat {LonkkaFleksioModAOik}/{LonkkaFleksioModAVas}. '
report += 'Lonkan ojentajat {LonkkaEkstensioModAOik}/{LonkkaEkstensioModAVas}. '
report += 'Lonkan lähentäjät {LonkkaAdduktoritModAOik}/{LonkkaAdduktoritModAVas}. '
report += 'Hamstringit {PolviHamstringModAOik}/{PolviHamstringModAVas}. '
report += 'Rectus femoris {PolviRectusModAOik}/{PolviRectusModAVas}. '
report += 'Lonkan sisäkierto {LonkkaSisakiertoModAOik}/{LonkkaSisakiertoModAVas}. '
report += 'Lonkan ulkokierto {LonkkaUlkokiertoModAOik}/{LonkkaUlkokiertoModAVas}. '
report += 'Soleus {NilkkaSoleusModAOik}/{NilkkaSoleusModAVas}. '
report += 'Gastrocnemius {NilkkaGastroModAOik}/{NilkkaGastroModAVas}.'
report += '\n'
report += 'Kommentit (lonkka): {cmtLonkkaSpast}\n'

report += """
Manuaalisesti mitatut lihasvoimat ja selektiivisyys (oikea lihasvoima/vasen lihasvoima, (oikea selekt./vasen selekt.)):
Asteikko: 0-5, missä 5 on vahvin ja 3 voittaa painovoiman koko potilaan liikelaajuudella.
Selektiivisyys: 0-2, missä 0=kokonaisliikemalli, 1=osittain eriytynyt ja 2=eriytynyt koko liikelaajuudella:
"""
report += 'Lonkan ojennus (polvi 0°) {VoimaLonkkaEkstensioPolvi0Oik}/{VoimaLonkkaEkstensioPolvi0Vas}'
report += ' ({SelLonkkaEkstensioPolvi0Oik}/{SelLonkkaEkstensioPolvi0Vas})'
report.item_sep()
report += 'Lonkan ojennus (polvi 90°) {VoimaLonkkaEkstensioPolvi90Oik}/{VoimaLonkkaEkstensioPolvi90Vas}'
report += ' ({SelLonkkaEkstensioPolvi90Oik}/{SelLonkkaEkstensioPolvi90Vas})'
report.item_sep()
report += 'Lonkan koukistus {VoimaLonkkaFleksioOik}/{VoimaLonkkaFleksioVas}'
report += ' ({SelLonkkaFleksioOik}/{SelLonkkaFleksioVas})'
report.item_sep()
report += 'Loitonnus (lonkka 0°) {VoimaLonkkaAbduktioLonkka0Oik}/{VoimaLonkkaAbduktioLonkka0Vas}'
report += ' ({SelLonkkaAbduktioLonkka0Oik}/{SelLonkkaAbduktioLonkka0Vas})'
report.item_sep()
report += 'Loitonnus, lonkka fleksiossa {VoimaLonkkaAbduktioLonkkaFleksOik}/{VoimaLonkkaAbduktioLonkkaFleksVas}. '
report += 'Lähennys {VoimaLonkkaAdduktioOik}/{VoimaLonkkaAdduktioVas}'
report += ' ({SelLonkkaAdduktioOik}/{SelLonkkaAdduktioVas})'
report.item_sep()
report += 'Lonkan ulkokierto {VoimaLonkkaUlkokiertoOik}/{VoimaLonkkaUlkokiertoVas}'
report += ' ({SelLonkkaUlkokiertoOik}/{SelLonkkaUlkokiertoVas})'
report.item_sep()
report += 'Lonkan sisäkierto {VoimaLonkkaSisakiertoOik}/{VoimaLonkkaSisakiertoVas}'
report += ' ({SelLonkkaSisakiertoOik}/{SelLonkkaSisakiertoVas})'
report.item_sep()
report += 'Polven ojennus {VoimaPolviEkstensioOik}/{VoimaPolviEkstensioVas}'
report += ' ({SelPolviEkstensioOik}/{SelPolviEkstensioVas})'
report.item_sep()
report += 'Polven koukistus {VoimaPolviFleksioOik}/{VoimaPolviFleksioVas}'
report += ' ({SelPolviFleksioOik}/{SelPolviFleksioVas})'
report.item_sep()
report += 'Nilkan koukistus {VoimaTibialisAnteriorOik}/{VoimaTibialisAnteriorVas}'
report += ' ({SelTibialisAnteriorOik}/{SelTibialisAnteriorVas})'
report.item_sep()
report += 'Nilkan ojennus (gastrocnemius) {VoimaGastroOik}/{VoimaGastroVas}'
report += ' ({SelGastroOik}/{SelGastroVas})'
report.item_sep()
report += 'Nilkan ojennus (soleus) {VoimaSoleusOik}/{VoimaSoleusVas}'
report += ' ({SelSoleusOik}/{SelSoleusVas})'
report.item_sep()
report += 'Inversio {VoimaTibialisPosteriorOik}/{VoimaTibialisPosteriorVas}'
report += ' ({SelTibialisPosteriorOik}/{SelTibialisPosteriorVas})'
report.item_sep()
report += 'Eversio {VoimaPeroneusOik}/{VoimaPeroneusVas}'
report += ' ({SelPeroneusOik}/{SelPeroneusVas})'
report.item_sep()
report += 'Isovarpaan ojennus {VoimaExtHallucisLongusOik}/{VoimaExtHallucisLongusVas}'
report += ' ({SelExtHallucisLongusOik}/{SelExtHallucisLongusVas})'
report.item_sep()
report += 'Isovarpaan koukistus {VoimaFlexHallucisLongusOik}/{VoimaFlexHallucisLongusVas}'
report += ' ({SelFlexHallucisLongusOik}/{SelFlexHallucisLongusVas})'
report.item_sep()
report += 'Varpaiden (2-5) ojennus {Voima25OjennusOik}/{Voima25OjennusVas}'
report += ' ({Sel25OjennusOik}/{Sel25OjennusVas})'
report.item_sep()
report += 'Varpaiden (2-5) koukistus {Voima25KoukistusOik}/{Voima25KoukistusVas}'
report += ' ({Sel25KoukistusOik}/{Sel25KoukistusVas})'
report.item_sep()
report += 'Suorat vatsalihakset {VoimaVatsaSuorat}. '
report += 'Vinot vatsalihakset {VoimaVatsaVinotOik}/{VoimaVatsaVinotVas}. '
report += 'Selkälihakset {VoimaSelka}.'
report += '\n'
report += 'Kommentit (voimat): {cmtVoima1} {cmtVoima2} \n'

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
               if report.data[ch] == checkbox_yes]
emgs_str = ', '.join(emgs_in_use)

if emgs_str:
    report += """
Dynaaminen EMG:
Alaraajojen lihasaktivaatio mitattiin pintaelektrodeilla seuraavista lihaksista:
"""
    report += emgs_str
    report += '\n'

report += 'Kommentit (EMG): {cmtEMG}\n'

report += """
SUUNNITELMA/POHDINTA:
"""
