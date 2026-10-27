# Hope

**Från lokala dokument till svar med synliga källor**

En fristående prototyp som kombinerar lokal dokumentsökning, källkort och webb-/mobilgränssnitt. Frågan är inte bara om AI kan svara, utan om användaren kan kontrollera underlaget.

## Behov

Viktig kunskap finns utspridd i dokument. Ett lättläst svar behöver gå att följa tillbaka till sin källa och säga ifrån när underlaget saknas.

## Lösning

Markdown-dokument indexeras och söks lokalt. En Node-baserad tjänst förmedlar resultat till webb och Android. Röst och avatar är separata presentationslager; en extern modell kan användas för syntes. Lokal sökning betyder därför inte att all behandling är lokal.

## Min insats

Eget initiativ med verksamhetsförståelse, produktinriktning, källstruktur och iterativ återkoppling. Implementation och testarbete sker med AI-stöd; jag beskriver inte varje kodrad som handskriven.

## Verifiering

Omkörda kontroller 2026-10-27: 10 Node-tester och 10 Python-tester passerade med syntetiska testdata. Android hade 8 godkända JVM-tester per byggvariant (debug, pairing, release); debug-APK byggdes utan privat signering. Offlinedemon visade källsvar i webbläsare utan externa anrop. Release-lint gav 19 varningar och inga fel. Detta var inte fysisk Android- eller avatarprovning.

## Avgränsning

Inte kliniskt beslutsstöd eller en produktionsleverans. Inte ett uppdrag från eller officiellt samarbete med Region Västernorrland eller KTH. Källkod, interna dokument och konfiguration delas inte i detta publika case.

## Förenklat flöde

```text
Fråga → Lokal dokumenthämtning → Svar + källkort → Webb / Android
```

**Teknik:** Node.js, JavaScript, Markdown, Android, Python / TLS.

**Status:** Privat, fristående prototyp.

## English

An independent, source-grounded knowledge prototype with local document retrieval, source cards and web/Android clients. External synthesis and speech are separate layers; this is not a clinical product.


[Tillbaka till urvalet](../README.md)
