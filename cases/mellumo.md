# Mellumo

**Visuellt vardagsstöd, från Androidplan till liten handledsskärm**

En digital vardagskompis som visar en aktivitet i taget och låter användaren själv markera KLAR. Den runda pixelfiguren Mint knyter ihop planeringsappen och klockans upplevelse.

## Behov

Ett vardagsstöd behöver vara begripligt i stunden. Planering, förhandsvisning och överföring måste också gå att förstå utan att användaren behöver tänka som en utvecklare.

## Lösning

Native Android/Java planerar aktiviteter och visar en lokal förhandsvisning med delad C++-logik via JNI. Guidad Bluetoothöverföring följs av återläsning och separat tidsaktivering. Klockprototypen använder ESP-IDF och LVGL på Waveshare ESP32-S3-Touch-AMOLED-2.06. Sparat i mobilen skiljs från bekräftat på klockan.

## Min insats

Produktinitiativ, prioriteringar och konkreta UX-krav i AI-assisterad utveckling. Jag har styrt mot aktivitetskort, fokuserade val, samma Mint-identitet och tydliga nästa steg i stället för utvecklarorienterade formulär.

## Verifiering

Ett dokumenterat vuxenprov omfattar fem sammanhängande aktiviteter med scener, hörbart tal, KLAR-övergångar och återgång till Hem. Sparat testunderlag för appversion 0.5.23 redovisar 427 tester utan testfel och 99 lintvarningar. Dessa tester har inte körts om för portföljen.

## Avgränsning

Batteriuthållighet, fysisk säkerhet, självständig användbarhet och validering med avsedda användare återstår. En historisk överförings-/journalavvikelse är inte slututredd. Inga medicinska effekter, haptik eller live-LLM i klockan utlovas. Inga privata planer, bilder eller enhetsfiler publiceras.

## Förenklat flöde

```text
Planera + förhandsvisa → Granska → Överför + återläs → Separat aktivering
```

**Teknik:** Android / Java, C++ / JNI, ESP32-S3, ESP-IDF / LVGL, Bluetooth.

**Status:** Fysiskt prövad prototyp, inte färdig produkt.

## English

A visual everyday-support prototype combining a native Android planner with an ESP32-S3 wearable. It uses shared C++ preview logic and explicit transfer/readback boundaries. Documented adult trials are not evidence of clinical benefit, battery endurance or readiness for intended users.


[Tillbaka till urvalet](../README.md)
