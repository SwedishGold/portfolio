#!/usr/bin/env python3
"""Build a dependency-free portfolio from reviewed case descriptions."""
from pathlib import Path
from html import escape
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
CSS = """
:root{--ivory:#FAF9F5;--white:#FFFFFF;--slate:#141413;--clay:#D97757;--olive:#788C5D;--rust:#B04A3F;--oat:#E3DACC;--gray-150:#F0EEE6;--gray-300:#D1CFC5;--gray-500:#87867F;--gray-700:#3D3D3A;--border:1.5px solid var(--gray-300);--radius-panel:12px;--radius-row:8px;--radius-pill:999px;--serif:ui-serif,Georgia,'Times New Roman',serif;--sans:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;--mono:ui-monospace,'SF Mono',Menlo,Consolas,monospace}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:22px}body{margin:0;background:var(--ivory);color:var(--gray-700);font-family:var(--sans);line-height:1.65;padding:28px 28px 64px}a{color:var(--slate);text-underline-offset:4px}a:hover{color:var(--rust)}:focus-visible{outline:3px solid var(--clay);outline-offset:5px}.page{max-width:1120px;margin:0 auto}.top{display:flex;align-items:center;justify-content:space-between;border-bottom:var(--border);padding-bottom:20px;gap:20px}.top a{font:12px var(--mono)}.signature{font-size:15px;letter-spacing:.03em;color:var(--slate)}.eyebrow,.tag,.number{font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase}.eyebrow{margin:0 0 18px}.hero{padding:68px 0 56px;display:grid;grid-template-columns:1.5fr 1fr;gap:60px;align-items:end}h1,h2,h3{font-family:var(--serif);font-weight:500;letter-spacing:-.025em;color:var(--slate)}h1{font-size:clamp(42px,5.4vw,70px);line-height:1.03;margin:0}.intro{font-size:17px;max-width:38em}.intro p{margin:0 0 16px}.intro .small{font-size:13px}.section-title{display:flex;justify-content:space-between;align-items:baseline;gap:20px;border-top:var(--border);padding-top:24px;margin-bottom:24px}.section-title h2{font-size:30px;margin:0}.section-title span{font:11px var(--mono)}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}.card{background:var(--white);border:var(--border);border-radius:var(--radius-panel);padding:28px;min-width:0}.card.primary{border-top:4px solid var(--clay)}.card header{display:flex;justify-content:space-between;gap:16px;align-items:baseline}.number{color:var(--gray-700)}.tag{background:var(--gray-150);border-radius:var(--radius-pill);padding:5px 9px;line-height:1.5;font-size:10px;letter-spacing:.02em}.card h3{font-size:32px;margin:20px 0 4px;line-height:1.18}.subtitle{font-size:15px;margin:0 0 18px;color:var(--gray-700)}.summary{margin:0 0 22px}.tech{display:flex;flex-wrap:wrap;gap:7px;list-style:none;padding:0;margin:18px 0 0}.tech li{font:11px var(--mono);border:1px solid var(--gray-300);border-radius:4px;padding:5px 7px}.flow{display:flex;align-items:stretch;gap:5px;margin:24px 0}.flow span{flex:1;padding:9px 5px;background:var(--gray-150);font:10px/1.45 var(--mono);text-align:center;overflow-wrap:anywhere;display:flex;align-items:center;justify-content:center}.flow b{align-self:center;font-size:12px;font-weight:400}details{border-top:var(--border);margin-top:24px;padding-top:14px}summary{cursor:pointer;color:var(--slate);font-size:13px;font-weight:600;padding:6px 0}details h4{font-size:13px;margin:22px 0 4px}details p{font-size:14px;margin:0}.limit{border-left:3px solid var(--clay);padding:10px 14px;background:var(--ivory);margin-top:18px!important}.links{display:flex;flex-wrap:wrap;gap:16px;margin-top:20px;font-size:13px}.method{margin:64px 0 32px;display:grid;grid-template-columns:1fr 1fr;gap:40px;border-top:var(--border);padding-top:30px}.method h2{font-size:30px;margin:0 0 14px}.method p{font-size:15px;max-width:42em}.method ol{padding-left:20px}.method li{margin-bottom:12px}.english{border-top:var(--border);padding-top:26px}.english h2{font-size:28px;margin:0}.english p{max-width:70ch;font-size:14px}.english ul{columns:2;gap:34px;padding-left:18px;font-size:13px}.english li{break-inside:avoid;margin-bottom:14px}footer{margin-top:38px;border-top:var(--border);padding-top:18px;display:flex;justify-content:space-between;gap:20px;font-size:12px}.skip{position:absolute;top:-80px}.skip:focus{top:12px;background:var(--white);padding:12px}code{font-family:var(--mono);font-size:.9em}p,li{overflow-wrap:break-word}@media(max-width:760px){body{padding:20px 18px 40px}.hero{grid-template-columns:1fr;gap:28px;padding:42px 0}.grid{grid-template-columns:1fr}.card{padding:22px}.flow{display:grid;grid-template-columns:1fr 1fr;gap:6px;counter-reset:step}.flow b{display:none}.flow span{min-height:44px;overflow-wrap:normal;counter-increment:step;justify-content:flex-start;text-align:left;padding:10px;font-size:11px}.flow span::before{content:counter(step);font-size:10px;margin-right:10px;color:var(--gray-700)}.method{grid-template-columns:1fr;gap:20px}.english ul{columns:1}.section-title{align-items:flex-start;flex-direction:column;gap:8px}footer{flex-direction:column;gap:8px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{body{padding:0}.hero{padding:24px 0}.grid{display:block}.card{break-inside:avoid;margin-bottom:20px}details{display:block}details>*{display:block}.top,.skip{display:none}a{color:var(--slate)}}
"""


def render_case(c, index):
    e = escape
    flow = '<b aria-hidden="true">→</b>'.join(f'<span>{e(s)}</span>' for s in c['flow'])
    tech = ''.join(f'<li>{e(s)}</li>' for s in c['tech'])
    detail = ''.join(f'<h4>{label}</h4><p>{e(c[key])}</p>' for key, label in [('problem','Behovet'),('approach','Lösningen'),('role','Min insats'),('evidence','Verifiering')])
    links = ''.join(f'<a href="{e(link["url"], quote=True)}">{e(link["label"])}</a>' for link in c['links'])
    return f'''<article class="card {'primary' if index < 4 else ''}" id="{e(c['id'])}">
<header><span class="number">{index+1:02d}</span><span class="tag">{e(c['status'])}</span></header>
<h3>{e(c['title'])}</h3><p class="subtitle">{e(c['subtitle'])}</p>
<p class="summary">{e(c['summary'])}</p>
<div class="flow" aria-label="Förenklad arkitektur">{flow}</div><ul class="tech" aria-label="Teknik">{tech}</ul>
<details><summary>Insats, teknik och verifiering</summary>{detail}<p class="limit"><strong>Avgränsning.</strong> {e(c['limits'])}</p><p lang="en" style="margin-top:18px">{e(c['english'])}</p>
<div class="links">{links}<a href="cases/{e(c['id'])}.md">Läs case som Markdown</a></div></details></article>'''


def build_outputs(cases):
    cards = '\n'.join(render_case(c, i) for i, c in enumerate(cases))
    en = ''.join(f'<li><strong>{escape(c["title"])}.</strong> {escape(c["english"])}</li>' for c in cases)
    page = f'''<!doctype html>
<html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Andreas Hillborgh: utvalda prototyper inom källbunden AI, interaktiva miljöer och hårdvaruintegration."><meta name="referrer" content="no-referrer"><title>Andreas Hillborgh — utvalda projekt</title><style>{CSS}</style></head><body>
<a class="skip" href="#projekt">Till projekten</a><div class="page">
<div class="top"><strong class="signature">Andreas Hillborgh</strong><nav aria-label="Snabblänkar"><a href="#english" lang="en">English summary</a> · <a href="https://github.com/SwedishGold/portfolio">GitHub</a></nav></div>
<header class="hero"><div><p class="eyebrow">Utvalda projekt / AI-assisterad utveckling</p><h1>Från verkligt behov<br>till något som<br>går att prova.</h1></div><div class="intro"><p>Jag förenar erfarenhet från vården med ett praktiskt intresse för AI, kunskapsbanker och kreativa digitala miljöer.</p><p>Här visar jag vad jag bygger med AI-stöd — och är tydlig med vad som faktiskt har testats.</p><p class="small">Egna initiativ och prototyper. Inte en lista över färdiga kommersiella produkter.</p></div></header>
<main><section id="projekt" aria-labelledby="projects-title"><div class="section-title"><h2 id="projects-title">Arbetsproven</h2><span>{len(cases)} utvalda case · problem / lösning / evidens</span></div><div class="grid">{cards}</div></section>
<section class="method" id="arbetssatt"><div><p class="eyebrow">Så arbetar jag</p><h2>AI som byggpartner.<br>Ansvar för resultatet.</h2><p>Min styrka ligger i att formulera ett konkret behov, styra utvecklingen, prova lösningen och förbättra den utifrån vad som faktiskt händer. AI används för kod, analys och tester; det gör inte granskning eller egen förståelse mindre viktigt.</p></div><ol><li><strong>Avgränsa.</strong> Välj en användare, ett problem och ett testbart flöde.</li><li><strong>Bygg.</strong> Koppla samman befintliga verktyg och små, tydliga komponenter.</li><li><strong>Verifiera.</strong> Håll isär kodtest, integration, fysisk observation och användaracceptans.</li><li><strong>Var transparent.</strong> Visa begränsningar, källor och vad som återstår.</li></ol></section>
<section class="english" id="english" lang="en"><h2>Selected work — in English</h2><p>I build AI-assisted prototypes around source-grounded knowledge, interactive experiences and hardware integrations. My background in care informs the problems I choose. The work below distinguishes implemented functionality, bounded test evidence and remaining limitations.</p><ul>{en}</ul></section></main>
<footer><span>Andreas Hillborgh · självständiga projekt</span><span><a href="NOTICE.md">Avgränsning och attribution</a> · <a href="https://www.linkedin.com/in/andreas-hillborgh-51581371/">LinkedIn</a></span></footer></div></body></html>'''
    readme = '''# Andreas Hillborgh — utvalda projekt

**AI-assisterad utveckling · källbunden kunskap · kreativa upplevelser · integrationer**

Jag kombinerar erfarenhet från vården med ett praktiskt intresse för att bygga användbara AI-lösningar. Jag använder AI som byggpartner och arbetar med behov, produktflöde, integration och verifiering. Projekten är egna initiativ i olika mognadsgrad — inte påståenden om färdiga produkter eller officiella kunduppdrag.

[Öppna portföljen](https://swedishgold.github.io/portfolio/) · [English overview](#english) · [Avgränsning och attribution](NOTICE.md)

## Välj ett spår

| Projekt | Vad arbetsprovet visar | Status |
|---|---|---|
'''
    for c in cases:
        readme += f'| [{c["title"]}](cases/{c["id"]}.md) | {c["subtitle"]} | {c["status"]} |\n'
    readme += '''
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

'''
    for c in cases:
        readme += f'- **[{c["title"]}](cases/{c["id"]}.md):** {c["english"]}\n'
    readme += '\n[LinkedIn](https://www.linkedin.com/in/andreas-hillborgh-51581371/)\n'
    outputs = {'index.html': page, 'README.md': readme}
    for c in cases:
        text = f'# {c["title"]}\n\n**{c["subtitle"]}**\n\n{c["summary"]}\n\n'
        for key, title in [('problem','Behov'),('approach','Lösning'),('role','Min insats'),('evidence','Verifiering'),('limits','Avgränsning')]:
            text += f'## {title}\n\n{c[key]}\n\n'
        text += '## Förenklat flöde\n\n```text\n' + ' → '.join(c['flow']) + '\n```\n\n'
        text += '**Teknik:** ' + ', '.join(c['tech']) + '.\n\n**Status:** ' + c['status'] + '.\n\n'
        text += '## English\n\n' + c['english'] + '\n\n'
        for link in c['links']:
            text += f'- [{link["label"]}]({link["url"]})\n'
        text += '\n[Tillbaka till urvalet](../README.md)\n'
        outputs[f'cases/{c["id"]}.md'] = text
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    cases = json.loads((ROOT / 'cases.json').read_text(encoding='utf-8'))
    outputs = build_outputs(cases)
    bad = []
    for relative, text in outputs.items():
        target = ROOT / relative
        if args.check:
            if not target.exists() or target.read_text(encoding='utf-8') != text:
                bad.append(relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding='utf-8')
    if bad:
        raise SystemExit('Generated files differ: ' + ', '.join(bad))
    print(f'{len(outputs)} generated files {"verified" if args.check else "written"}; {len(cases)} cases')


if __name__ == '__main__':
    main()
