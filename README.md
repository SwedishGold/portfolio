# Andreas Hillborgh — utvalda projekt

**AI-assisterad utveckling · källbunden kunskap · kreativa upplevelser · integrationer**

Jag kombinerar erfarenhet från psykiatri och omsorg med ett särskilt intresse för lokala AI-lösningar, kunskapsbanker och integrationer. Jag använder AI som byggpartner och arbetar med behov, produktflöde, integration och verifiering. Projekten är egna initiativ i olika mognadsgrad — inte påståenden om färdiga produkter eller officiella kunduppdrag.

[Öppna portföljen](https://swedishgold.github.io/portfolio/) · [English overview](#english) · [Avgränsning och attribution](NOTICE.md)

## Välj ett spår

| Projekt | Vad arbetsprovet visar | Status |
|---|---|---|
| [Hope](cases/hope.md) | Från lokala dokument till svar med synliga källor | Privat, fristående prototyp |
| [Dust Lord](cases/dust-lord.md) | En fysisk robot med händelsestyrd personlighet | Publikt integrationsprojekt |
| [Hermes Wrist](cases/hermes-wrist.md) | En avgränsad mobilkontroll för en lokal AI-agent | Privat integrationsprototyp |
| [Mellumo](cases/mellumo.md) | Visuellt vardagsstöd, från Androidplan till liten handledsskärm | Fysiskt prövad prototyp, inte färdig produkt |
| [Medan du är här](cases/museum.md) | Ett museum där besökarens närvaro blir en del av verket | Pågående interaktivt konstprojekt |
| [Codex Weekly / ESP32](cases/codex-weekly.md) | Gör en digital veckokvot synlig på skrivbordet | Dokumenterad D5-hårdvaruprototyp |

## Hur jag arbetar

1. Utgå från ett konkret behov och definiera ett litet testbart flöde.
2. Bygg med AI-stöd och befintliga ramverk, men håll egen insats och tredjepartsarbete tydliga.
3. Testa logik, integration och verkligt beteende på rätt nivå; ett automatiskt test är inte en fysisk acceptans.
4. Dokumentera begränsningar och nästa beslut, inte bara en lyckad skärmbild.

## Köra portföljen lokalt

Öppna `index.html` direkt i en webbläsare. Sidan är statisk: inga beroenden, spårare, externa typsnitt eller automatiska provideranrop.

```sh
python3 tools/build.py --check
python3 -m unittest discover -s tests -v
```

Ändra `cases.json` och kör `python3 tools/build.py` för att återskapa sidan och casefilerna. Detta repo innehåller casebeskrivningar och portföljens egen källkod. Privata produktimplementationer och firmware publiceras inte här.

## English

I build AI-assisted prototypes around source-grounded knowledge, interactive environments and hardware integration. My contribution is problem framing, product direction, iterative implementation with AI support and evidence-led evaluation. These are independent projects at different stages of maturity, not claims of clinical validation or production deployments.

- **[Hope](cases/hope.md):** An independent, source-grounded knowledge prototype with local document retrieval, source cards and web/Android clients. External synthesis and speech are separate layers; this is not a clinical product.
- **[Dust Lord](cases/dust-lord.md):** A local smart-home experiment connecting robot events to a stateful persona, speech synthesis and an external Cast speaker, without replacing the robot firmware.
- **[Hermes Wrist](cases/hermes-wrist.md):** An Android control surface for a local agent, with filtered status, pinned TLS and allowlisted actions. Selected bridge tests are separate from physical phone/watch verification.
- **[Mellumo](cases/mellumo.md):** A visual everyday-support prototype combining a native Android planner with an ESP32-S3 wearable. It uses shared C++ preview logic and explicit transfer/readback boundaries. Documented adult trials are not evidence of clinical benefit, battery endurance or readiness for intended users.
- **[Medan du är här](cases/museum.md):** While You Are Here is an interactive Minecraft art installation: eight connected zones, five authored language editions and personal visitor sequences. I lead the concept, curation and iteration; AI assists implementation. The runtime uses programmed logic, not free-form LLM conversation.
- **[Codex Weekly / ESP32](cases/codex-weekly.md):** A desktop ESP32-C6 device for Codex weekly quota, current time and reset time. It preserves the provider’s integer precision and explicitly handles stale data. Three isolated C test programs were rerun; historical physical acceptance is separate from today’s device state.

[LinkedIn](https://www.linkedin.com/in/andreas-hillborgh-51581371/)
