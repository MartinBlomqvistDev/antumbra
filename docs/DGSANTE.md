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
öppnas för att klassas**; räkna dem inte som åtgärdsplaner. Klassningen är
gjord för EU-27-delmängden, se nedan, och bekräftar varningen.

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

**Men mallen ovan är verifierad på en rapport, och gäller inte hela korpusen.**
Se avsnittet om citatgrafens omfattning nedan; korsreferenserna börjar 2014 och
blir aldrig heltäckande. Rapporternas avsnittsnumrering skiljer sig dessutom
mellan eror: rekommendationerna ligger under rubrik 9 i de äldre rapporterna
och under rubrik 8 från omkring 2007.

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

## Nedladdad korpus

Hämtad 2026-08-02 med `pipeline/03_download_reports.py`: EU-27, engelska
rapporter plus samtliga bilagor. **7 963 filer, 2,2 GB: 2 940 rapporter och
5 023 bilagor, noll fel.** Proveniensmanifest med sha256, källänk, storlek
och hämtdatum per fil i `data/dgsante_manifest.jsonl`, byggt av
`pipeline/04_build_manifest.py`; dokumenten själva ligger utanför git.

Allt är inte PDF:

| Format | Antal |
| --- | --- |
| pdf | 7 025 |
| gif | 838 |
| html/htm | 87 |
| doc/docx | 7 |
| jpg | 5 |
| tif | 1 |

Ett dött fil-id svarar HTTP 404, så varje 200-svar är dokumentinnehåll.
GIF-filerna är inskannade A4-sidor från den äldre eran (stickprov 816x1153
pixlar) och kräver OCR. HTML-filerna är Word-exporterade äldre bilagor.

## De numrerade bilagorna, klassade

1 974 av de numrerade bilagorna ligger i EU-27 och är nedladdade. Varje fil
öppnades av `pipeline/05_classify_annexes.py`, som klassar dokumentet på hur
det **presenterar sig själv** i sina inledande tecken och sparar det citat
klassningen vilar på. Resultat i `data/dgsante_annex_classes.jsonl`.

| Klass | Antal |
| --- | --- |
| Oklassad text | 882 |
| Kommentarer på rapportutkastet | 808 |
| Korrespondens | 155 |
| Åtgärdsplan | 89 |
| Redovisning av vidtagna åtgärder | 13 |
| Kräver OCR | 13 |
| Lagtext | 11 |
| Datatabell | 2 |
| Kräver konvertering (äldre Word) | 1 |

**Svaret på frågan är nej: de numrerade bilagorna är inte åtgärdsplaner.** De
är i huvudsak medlemsstaternas kommentarer på rapportutkastet, plus brev som
följer med dem. Åtgärdsplaner utgör 89 av 1 974, alltså 4,5 procent, och 86 av
dem är inte planer utan **HTML-stubbar som pekar på en plan** via gamla
adresser under `ec.europa.eu/food/fvo/ap/`. De adresserna svarar 404 i dag,
verifierat 2026-08-02: **själva planen är borta, bara pekaren finns kvar.**

"Redovisning av vidtagna åtgärder" hålls isär från "åtgärdsplan" därför att
dokumenten själva gör det; flera skriver uttryckligen att planen kommer senare.
Att slå ihop dem skulle överdriva hur ofta kedjan rekommendation till åtagande
faktiskt sluts.

**Träffsäkerhet.** Klassningen mättes mot 40 bilagor som lästes för hand, i
stickprov dragna **efter** att reglerna skrivits och aldrig använda för att
justera dem: **34 av 40 rätt, 85 procent.** Facit ligger i
`data/dgsante_annex_labels.jsonl` och kontrolleras av testsviten. Fem av de sex
avvikelserna är dokument som lämnats oklassade fast de går att klassa, alltså
ett försiktigt fel; **noll dokument klassades som plan utan att vara det.**
Gränsfallet som återstår är brev som bifogar kommentarer: brevet och dess
innehåll är olika saker och klassningen väljer innehållet.

## OCR på de skannade bilagorna

Kört 2026-08-02 med `pipeline/06_ocr_annexes.py`: Tesseract 5.4 i
medlemsstatens språk plus engelska, 21 språkpaket. **1 017 av 1 018 lästa,
1 886 sidor, 568 905 ord.** Konfidens per fil i `data/dgsante_ocr_index.jsonl`;
texten ligger under `ocr/`, som är gitignorerad.

| Genomsnittlig ordkonfidens | Filer |
| --- | --- |
| 90 och över | 277 |
| 80 till 89 | 438 |
| 70 till 79 | 178 |
| 50 till 69 | 99 |
| under 50 | 24 |

**Två filer går inte att läsa, och båda är trasiga hos kommissionen, inte hos
oss.** `annex/download/2603` är en avkortad GIF som avkodar till en helsvart
sida; den nedladdade filen är byte-identisk med vad servern levererar, så
skadan finns i källan. `annex/download/3339` heter `.pdf` men innehåller ett
OLE-dokument från Office.

**OCR avslöjade inga nya åtgärdsplaner.** Bland de 1 017 nylästa filerna finns
noll dokument som namnger sig som plan. Slutsatsen ovan står alltså kvar efter
att materialet lästs, inte bara efter att det räknats.

## Bilagorna är sidor, inte dokument

Klassningen träffar bara 45 procent av filerna, och det beror inte i första
hand på OCR-kvaliteten: även bland filer med konfidens över 90 klassas bara
41 procent. Förklaringen syns i texten. **41 procent av de OCR-lästa
bilagorna inleds med ett faxhuvud**, och de numrerade bilagorna till en
revision från den äldre eran är i regel **sidorna i en och samma faxade
inlaga**, inte separata dokument. Bara sida ett bär rubriken som säger vad
inlagan är; sida fyra fortsätter mitt i en mening.

**Rätt analysenhet är därför revisionen, inte filen.** Räknat per revision
namnger minst en bilaga dokumentet i **831 av 1 034 fall, alltså 80 procent.**
Den siffran, inte 45 procent, är den som ska stå i metoden, och parsningen
ska sätta ihop bilagorna per revision innan den läser dem.

## Citatgrafen: vad den faktiskt täcker

Kört 2026-08-02 med `pipeline/07_parse_recommendations.py` över samtliga
2 940 engelska EU-27-rapporter. Resultat i `data/dgsante_recommendations.jsonl`
(en rad per rekommendation) och `data/dgsante_report_parse.jsonl` (en rad per
rapport med utfallet).

**8 365 rekommendationer ur 1 699 rapporter, 27 länder.**

| Utfall per rapport | Antal |
| --- | --- |
| Parsad till rekommendationer | 1 699 |
| Avsnitt hittat men inga poster | 909 |
| Inget rekommendationsavsnitt | 315 |
| Rapporten säger att den saknar rekommendation | 17 |

De 17 sista är ett **äkta nollresultat, inte ett parsningsfel**, och hålls
isär i utdatat just därför.

**Korsreferenserna är den knappa resursen.** Bara 489 av 2 940 rapporter, 17
procent, skriver ut vilken slutsats en rekommendation vilar på. Praktiken
börjar 2014 och blir aldrig heltäckande:

| År | Rapporter | Med korsreferenser |
| --- | --- | --- |
| före 2014 | 2 043 | 0 |
| 2014 | 113 | 17 |
| 2015 | 112 | 47 |
| 2016 | 110 | 46 |
| 2017 | 103 | 36 |
| 2018 | 109 | 53 |
| 2019 | 93 | 48 |
| 2020 | 53 | 35 |
| 2021 | 88 | 47 |
| 2022 | 74 | 39 |
| 2023 | 71 | 42 |
| 2024 | 82 | 50 |
| CT-formatet | 83 | 29 |

**Grafen omfattar 1 133 rekommendationer med 1 450 kanter till slutsatser och
3 221 kanter till iakttagelser.** Det är storleksordningen som ska stå i
metoden, inte 4 690 och inte 8 365.

**Parserns täckning mäts på den delmängd som bär grafen:** av de 489
rapporterna parsas 441, alltså **90 procent**. Testsviten fäller om andelen
faller under 85 procent.

Kända begränsningar, utskrivna i stället för utjämnade: 909 rapporter har ett
rekommendationsavsnitt vars numrering inte går att följa, oftast tvåspaltiga
tabeller där sidnummer och radnummer blandas med rekommendationsnumren. 167
rekommendationer bär flaggan `multiple_reference_blocks`, vilket betyder att
flera rekommendationer runnit ihop till ett block och att länkarna tillhör den
första av dem.

## Nästa steg

1. Sätt ihop bilagorna per revision före parsning, enligt avsnittet ovan.
2. Parsa iakttagelser och slutsatser ur avsnitt 5 och 6, så att kanterna får
   noder att peka på; i dag är grafen kanter mot stycknummer.
3. Koppla åtgärdsplanerna till rekommendationerna och slut kedjan.
