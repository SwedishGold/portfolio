# Hermes Wrist

**En avgränsad mobilkontroll för en lokal AI-agent**

En Android-kontrollpanel som visar agentstatus och förmedlar ett begränsat urval handlingar till en Mac. Klockan är en kompletterande notifieringsyta, inte en fristående AI-klient.

## Behov

Få överblick och hantera tydliga åtgärder utan att skicka privata samtal eller ge en mobilklient en fri kommandokanal.

## Lösning

En Python-brygga filtrerar statusfält. Certifikatpinning och autentisering skyddar den privata Wi-Fi-vägen; USB/localhost är separat reservväg. Kommandon använder en fast tillåten lista, replay-skydd och begränsad anropsfrekvens.

## Min insats

Produktflöde, prioritering av vad som ska synas och krav på begränsad åtkomst, genom iterativ AI-assisterad implementation och återkoppling.

## Verifiering

53 utvalda tester för status- och kommandobryggor passerade i en isolerad testmiljö 2026-10-27.

## Avgränsning

Detta är inte en ny verifiering av installerad telefon, notifieringsspegling eller klocka. Modellsimuleringar ersätter inte fysisk testning. Ingen APK, pairinginformation eller maskinspecifik konfiguration publiceras här.

## Förenklat flöde

```text
Agentstatus → Filtrerad lokal brygga → Android → Notifiering / klocka
```

**Teknik:** Android, Python, Pinned TLS, SQLite, macOS.

**Status:** Privat integrationsprototyp.

## English

An Android control surface for a local agent, with filtered status, pinned TLS and allowlisted actions. Selected bridge tests are separate from physical phone/watch verification.


[Tillbaka till urvalet](../README.md)
