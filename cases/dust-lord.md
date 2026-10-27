# Dust Lord

**En fysisk robot med händelsestyrd personlighet**

Ett agentlager runt en robotdammsugare: statusförändringar väljer beteende och repliker som spelas via en extern högtalare, utan att flasha robotens firmware.

## Behov

Hur kan ett vardagsföremål reagera begripligt och karaktärsfullt på vad det faktiskt gör, utan att röstupplevelsen blandas ihop med robotens styrning?

## Lösning

Robotstatus går genom en watcher och en tillstånds-/beteendemodell till ett repliksbibliotek. TTS och Cast sköter extern uppläsning. Fysisk styrning har en separat RPC-väg och kräver uttrycklig avsikt.

## Min insats

Personakoncept, önskat beteende och integration utvecklade med AI-stöd. Ett konkret experiment i att förena kreativa beslut med befintliga API:er, lokala skript och testning.

## Verifiering

Två avgränsade offline-tester av repliksbiblioteket passerade vid granskningen 2026-10-27. GitHub CI verifierades för den granskade committen. Repot innehåller en publicerad demofilm.

## Avgränsning

Offline-testerna verifierar inte robotrörelse, nätverk, rösttjänst eller ljudåtergivning. Ingen ny fysisk körning gjordes för portföljen. Lösningen är anpassad till en lokal miljö.

## Förenklat flöde

```text
Robotstatus → Händelse / beteende → Replik + TTS → Extern högtalare
```

**Teknik:** Python, Roborock RPC, TTS, Google Cast, macOS launchd.

**Status:** Publikt integrationsprojekt.

## English

A local smart-home experiment connecting robot events to a stateful persona, speech synthesis and an external Cast speaker, without replacing the robot firmware.

- [Kod och befintlig demo](https://github.com/SwedishGold/dustlord)

[Tillbaka till urvalet](../README.md)
