# Codex Weekly / ESP32

**Gör en digital veckokvot synlig på skrivbordet**

En liten enhet med LCD och åtta RGB-lysdioder visar Codex veckokvot. Två programmerbara knappar växlar vy eller begär en ny avläsning; aktuell tid och nästa återställning har egna vyer.

## Behov

En användningsgräns behöver vara lätt att uppfatta utan ännu en öppen kontrollpanel. Samtidigt måste skärmen skilja färska uppgifter från gamla eller okända värden.

## Lösning

En lokal Python-brygga läser Codex app-server och väljer det uttryckliga sjudagarsfönstret. C/ESP-IDF, LVGL och leverantörens BSP driver Waveshare ESP32-C6-LCD-0.85. Kontoinloggningen stannar på datorn. Statuskontrakt kontrolleras, gammalt underlag visas som offline och BLE erbjuder separat skrivskyddad status.

## Min insats

Ett eget AI-assisterat hårdvaruprojekt kring ett tydligt informationsbehov: kvot, tid, återställning och felåterkoppling ska gå att skilja åt. Utvecklingen dokumenterar kandidater, testgränser och verifiering i stället för att bara visa en lyckad skärm.

## Verifiering

D5 har dokumenterad fysisk funktionskontroll och byteverifierad firmwareavläsning från augusti 2026. Under portföljgranskningen kompilerades och kördes tre fristående C-testprogram med godkänt resultat; 13 D5 C/H-källhashar matchade manifestet. Ett av testprogrammen gäller en äldre referensmodell, inte D5:s renderer.

## Avgränsning

Procenten följer leverantörens rapporterade heltal, inte beräknade token eller påhittade decimaler. Ingen aktuell kvot eller ny hårdvarustatus har lästs. Transportkryptering och produktionshärdning återstår. Ursprunglig källkod och firmware ingår inte i det publika caset.

## Förenklat flöde

```text
Codex app-server → Lokal statusbrygga → Validerat kontrakt → LCD / LED / BLE
```

**Teknik:** ESP32-C6, C / ESP-IDF, LVGL, Python, Read-only BLE.

**Status:** Dokumenterad D5-hårdvaruprototyp.

## English

A desktop ESP32-C6 device for Codex weekly quota, current time and reset time. It preserves the provider’s integer precision and explicitly handles stale data. Three isolated C test programs were rerun; historical physical acceptance is separate from today’s device state.


[Tillbaka till urvalet](../README.md)
