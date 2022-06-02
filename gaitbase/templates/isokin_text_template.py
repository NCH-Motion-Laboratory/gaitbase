# -*- coding: utf-8 -*-
"""
Template for text report (isokinetic data)
see text_template.py
NB: here the units are not included along with data, and have to be
written out explicitly

@author: Jussi (jnu@iki.fi)
"""

report += """

LIIKELAAJUUDET JA VOIMAT

Potilaskoodi: {TiedotID}
Potilaan nimi: {TiedotNimi}
Henkilötunnus: {TiedotHetu}
Diagnoosi: {TiedotDiag}
Mittauksen päivämäärä: {TiedotPvm}
Paino: {AntropPaino} kg
"""
report += 'Kommentit: {cmtTiedot}\n'

report += """
ISOKINEETTINEN VOIMAMITTAUS
"""

report += """
Polven liikelaajuus: {IsokinPolviFleksioOik}...{IsokinPolviEkstensioOik}° / {IsokinPolviFleksioVas}...{IsokinPolviEkstensioVas}°  
Polven ekstensiomomentti: {IsokinPolviEkstensioMomenttiOikNormUn} / {IsokinPolviEkstensioMomenttiVasNormUn} Nm
Polven ekstensiomomentti (norm.): {IsokinPolviEkstensioMomenttiOikNorm} / {IsokinPolviEkstensioMomenttiVasNorm} Nm/kg
Polven liikenopeus, ekstensio: {IsokinPolviLiikenopeusEkstensioOik} / {IsokinPolviLiikenopeusEkstensioVas} °/s
Polven fleksiomomentti: {IsokinPolviFleksioMomenttiOikNormUn} / {IsokinPolviFleksioMomenttiVasNormUn} Nm
Polven fleksiomomentti (norm.): {IsokinPolviFleksioMomenttiOikNorm} / {IsokinPolviFleksioMomenttiVasNorm} Nm/kg
Polven liikenopeus, fleksio: {IsokinPolviLiikenopeusFleksioOik} / {IsokinPolviLiikenopeusFleksioVas} °/s
"""

report += """
Nilkan liikelaajuus: {IsokinNilkkaPlantaarifleksioOik}...{IsokinNilkkaDorsifleksioOik}° / {IsokinNilkkaPlantaarifleksioVas}...{IsokinNilkkaDorsifleksioVas}°
Nilkan plantaarifleksiomomentti: {IsokinNilkkaPlantaarifleksioMomenttiOikNormUn} / {IsokinNilkkaPlantaarifleksioMomenttiVasNormUn} Nm 
Nilkan plantaarifleksiomomentti (norm.): {IsokinNilkkaPlantaarifleksioMomenttiOikNorm} / {IsokinNilkkaPlantaarifleksioMomenttiVasNorm} Nm/kg
Nilkan liikenopeus, plantaarifleksio: {IsokinNilkkaLiikenopeusPlantaarifleksioOik} / {IsokinNilkkaLiikenopeusPlantaarifleksioVas} °/s
Nilkan dorsifleksiomomentti: {IsokinNilkkaDorsifleksioMomenttiOikNormUn} / {IsokinNilkkaDorsifleksioMomenttiVasNormUn} Nm
Nilkan dorsifleksiomomentti (norm.): {IsokinNilkkaDorsifleksioMomenttiOikNorm} / {IsokinNilkkaDorsifleksioMomenttiVasNorm} Nm/kg
Nilkan liikenopeus, dorsifleksio: {IsokinNilkkaLiikenopeusDorsifleksioOik} / {IsokinNilkkaLiikenopeusDorsifleksioVas} °/s
"""
