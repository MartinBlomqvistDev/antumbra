# DG SANTE-korpusen

Kommissionens direktorat för hälso- och livsmedelsrevision granskar
**medlemsstaternas kontrollsystem**, inte enskilda anläggningar. Det gör
korpusen till projektets jämförelselager: samma revisor, samma rättsliga grund,
samma rapportmall för alla medlemsstater, alltså **jämförbara till sin
konstruktion**.

Allt nedan är verifierat 2026-08-01 och 2026-08-02 med faktiska anrop.

## Åtkomst

Ingen inloggning. `robots.txt` på ec.europa.eu spärrar `/food/archive/` men inte
`/food/audits-analysis`, och sätter ingen crawl-delay.

| Vad | URL |
| --- | --- |
| Sökformulär | `ec.europa.eu/food/audits-analysis/audit-report` |
| Detaljsida | `.../audit-report/details/<detail_id>` |
| Rapportfil | `.../audit-report/download/<id>` |
| Bilaga | `.../audit-report/annex/download/<id>` |
| Landprofil | `.../country/profile/download/<id>` |

Sökningen är ett **serverrenderat Symfony-formulär**, inte en SPA. En POST per
årtal med färsk CSRF-token ger en strukturerad träfflista. Se
`pipeline/01_harvest_index.py`.

## Vad som hämtats

`data/dgsante_index.json`: **4 690 rader**, 1998 till 2027, 165 länder. Fält:
`ref`, `country`, `period`, `subject`, `detail_id`, `year`.

`data/dgsante_details.jsonl`: en rad per revision, **4 690 av 4 690, noll fel**.
Tillägger `title`, `audit_period`, `published_date`, `reports[]` (id, språk,
storlek) och `annexes[]` (id, titel, etikett, storlek).

## Vad korpusen innehåller

| | Antal |
| --- | --- |
| Revisioner totalt | 4 690 |
| EU-27 | 3 020 |
| EU-27 om djurskydd eller kött, slakt, gris, fjäderfä | 538 |
| varav "welfare" i ämnesraden | 229 |
| Sverige, alla ämnen | 98 |
| Sverige, djurskydd | 8 |
| EU-27 från 2017 (förordning 2017/625) | 758 |

Djurskyddsrevisionerna fördelar sig jämnt över de stora producentländerna:
Frankrike 18, Tyskland 17, Spanien 15, Italien 14, Grekland och Nederländerna 13.

**Sverige har 98 rapporter, varav 8 om djurskydd.** Det är inte en parallell
till den svenska mätningen utan samma objekt sett uppifrån: kommissionen har
granskat den svenska djurskyddskontrollen och skrivit ner sina iakttagelser.
Avvikelser mellan deras revision uppifrån och mätningen underifrån är i sig ett
resultat.

## Språk

13 542 språkversioner totalt. **Engelska finns på 4 563 av 4 690.** Franska
(3 950) och tyska (3 880) finns på nästan allt men är översättningar av samma
text och tillför inget analytiskt. Övriga språk är enstaka: nederländska 114,
italienska 97, spanska 96.

**127 revisioner saknar engelsk version** och behöver hanteras separat.
26 saknar rapportfil helt. 3 501 av 4 690 har publiceringsdatum.

## Bilagor

7 576 bilagor totalt.

| Klass | Antal |
| --- | --- |
| Numrerade, "1", "2", "3" (äldre era) | 2 904 |
| Action plan | 2 331 |
| CA comments | 2 083 |
| Övriga varianter av "competent authority response" | ~60 |

**1 747 revisioner har en åtgärdsplan, alltså 37 procent**, varav 1 084 i EU-27.
Praktiken börjar 2011: enstaka 2010, 80 år 2011, 190 år 2012, därefter stabilt
mellan 60 och 180 om året.

**Kedjan rekommendation till åtagande går alltså att sluta för cirka 1 700
revisioner från 2011 och framåt.** Före det finns den inte.

De 2 904 numrerade bilagorna från den äldre eran är av okänt slag och **måste
öppnas för att klassas**; räkna dem inte som åtgärdsplaner.

Titeln på åtgärdsplaner varierar: "Action plan", "Action Plan", "CA Action
Plan", "Updated action plan", "Competent Authority response to the report
recommendations". Matcha skiftlägesokänsligt på delsträngen `action`.

## Rapporternas struktur

Fast mall, verifierad på 2024-8071 (Danmark, foderhygien):

1. INTRODUCTION
2. LEGAL BASIS
3. OBJECTIVES AND SCOPE
4. BACKGROUND
5. FINDINGS AND CONCLUSIONS (med underavsnitt 5.1, 5.2, ...)
6. OVERALL CONCLUSION
7. CLOSING MEETING
8. RECOMMENDATIONS

**Varje stycke i hela dokumentet är löpnumrerat**, och rekommendationerna är
korsrefererade:

```
1    To ensure that official controls consistently check that feed business
     operators implement and maintain effective procedures based on HACCP...
     Legal basis: Articles 6 and 7 of Regulation (EC) No 183/2005.
     Recommendation based on conclusion: 31.
     Associated findings: 22 and 23.
```

Det är **en färdig graf i textform**: iakttagelse → slutsats → rekommendation →
rättslig grund, allt med stycknummer. Ingen NLP behövs för kopplingarna, bara
parsning. Åtgärdsplanen sluter kedjan med medlemsstatens egna åtaganden och
tidsfrister, och uppföljande revisioner bedömer om åtgärderna vidtogs.

## Två format

4 568 rapporter har referensformatet `2024-8071`. **122 rapporter från 2024 till
2026 har formatet `CT-2025-0121`**, med färre språkversioner och andra
bilagenamn ("Report Comments Table"). De behöver egen hantering och ska inte
tvingas in i samma parser.

## Nedladdningsvolym

| Delmängd | GB |
| --- | --- |
| Engelska rapporter | 1,52 |
| Alla språkversioner | 2,93 |
| Bilagor | 1,82 |

**Ladda ned engelska plus bilagor, alltså cirka 3,3 GB.** Franska och tyska
tillför ingenting. PDF:erna ligger i `.gitignore` och committas aldrig.

## Nästa steg

1. Ladda ned engelska rapporter och åtgärdsplaner för EU-27, alltså den
   delmängd som bär analysen.
2. Klassa de 2 904 numrerade äldre bilagorna genom stickprov.
3. Designa parsningen av citatgrafen mot verklig korpus, alltså kopplingen
   iakttagelse till slutsats till rekommendation till åtgärdsplan.
