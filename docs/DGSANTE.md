# DG SANTE-korpusen

Kommissionens direktorat för hälso- och livsmedelsrevision granskar
**medlemsstaternas kontrollsystem**. Enskilda anläggningar granskas inte. Det gör
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

Sökningen är ett **serverrenderat Symfony-formulär** utan SPA. En POST per
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
stickprov dragna **efter** att reglerna skrivits, utan att någonsin ha använts
för att justera dem: **34 av 40 rätt, 85 procent.** Facit ligger i
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

**Två filer går inte att läsa, och båda är trasiga hos kommissionen.** Hos oss
är de hela. `annex/download/2603` är en avkortad GIF som avkodar till en helsvart
sida; den nedladdade filen är byte-identisk med vad servern levererar, så
skadan finns i källan. `annex/download/3339` heter `.pdf` men innehåller ett
OLE-dokument från Office.

**OCR avslöjade inga nya åtgärdsplaner.** Bland de 1 017 nylästa filerna finns
noll dokument som namnger sig som plan. Slutsatsen ovan står alltså kvar efter
att materialet lästs, utöver att det räknats.

## Bilagorna är sidor snarare än dokument

Klassningen träffar bara 45 procent av filerna, och det beror inte i första
hand på OCR-kvaliteten: även bland filer med konfidens över 90 klassas bara
41 procent. Förklaringen syns i texten. **41 procent av de OCR-lästa
bilagorna inleds med ett faxhuvud**, och de numrerade bilagorna till en
revision från den äldre eran är i regel **sidorna i en och samma faxade
inlaga**. Separata dokument är de inte. Bara sida ett bär rubriken som säger vad
inlagan är; sida fyra fortsätter mitt i en mening.

**Rätt analysenhet är därför revisionen.** Filen duger inte som enhet. Räknat per revision
namnger minst en bilaga dokumentet i **831 av 1 034 fall, alltså 80 procent.**
Den siffran är den som ska stå i metoden, där 45 procent förut stod, och parsningen
ska sätta ihop bilagorna per revision innan den läser dem.

## Citatgrafen: vad den faktiskt täcker

Kört 2026-08-02 med `pipeline/07_parse_recommendations.py` över samtliga
2 940 engelska EU-27-rapporter. Resultat i `data/dgsante_recommendations.jsonl`
(en rad per rekommendation) och `data/dgsante_report_parse.jsonl` (en rad per
rapport med utfallet).

**11 999 rekommendationer ur 2 341 rapporter, 27 länder.** Tre layouter läses:
6 757 poster ur flat numrering, 3 451 ur tvåspaltiga tabeller och 1 791 ur den
hierarkiska numrering de äldre rapporterna använder ("7.1.1", "7.1.2").

| Utfall per rapport | Antal |
| --- | --- |
| Parsad till rekommendationer | 2 341 |
| Avsnitt hittat men inga poster | 354 |
| Inget rekommendationsavsnitt | 225 |
| Rapporten säger att den saknar rekommendation | 20 |

De 20 sista är ett **äkta nollresultat, inte ett parsningsfel**, och hålls
isär i utdatat just därför.

**Korsreferenserna är den knappa resursen.** Bara 673 av 2 940 rapporter, 23
procent, skriver ut vilken slutsats en rekommendation vilar på. Praktiken
börjar 2014 och blir aldrig heltäckande:

| År | Rapporter | Med korsreferenser |
| --- | --- | --- |
| före 2014 | 1 849 | 0 |
| 2014 | 113 | 23 |
| 2015 | 112 | 72 |
| 2016 | 110 | 60 |
| 2017 | 103 | 52 |
| 2018 | 109 | 76 |
| 2019 | 93 | 65 |
| 2020 | 53 | 42 |
| 2021 | 88 | 66 |
| 2022 | 74 | 56 |
| 2023 | 71 | 53 |
| 2024 | 82 | 59 |
| CT-formatet | 83 | 47 |

**Grafen omfattar 2 010 rekommendationer med 2 614 kanter till slutsatser och
5 207 kanter till iakttagelser.** Det är storleksordningen som ska stå i
metoden, inte 4 690 och inte 11 999.

**Parserns täckning mäts på den delmängd som bär grafen:** av de 673
rapporterna parsas 636, alltså **94 procent**. Räknat på alla rapporter med
ett rekommendationsavsnitt parsas 2 341 av 2 695, alltså 87 procent. Testsviten fäller om andelen
faller under 85 procent.

Kända begränsningar, utskrivna i stället för utjämnade: 354 rapporter har ett
rekommendationsavsnitt vars numrering inte går att följa, oftast tvåspaltiga
tabeller där sidnummer och radnummer blandas med rekommendationsnumren. 167
rekommendationer bär flaggan `multiple_reference_blocks`, vilket betyder att
flera rekommendationer runnit ihop till ett block och att länkarna tillhör den
första av dem.

## Noderna: styckena som citeras

Kört 2026-08-02 med `pipeline/08_parse_paragraphs.py`. Rapporternas stycken är
löpnumrerade genom hela dokumentet, och steg 08 läser dem så att kanterna från
steg 07 får något att peka på.

**81 292 stycken ur 2 724 rapporter.** Den fulla styckekorpusen är 66 MB och
ligger i `.gitignore`; den återskapas genom att köra steget. Det som committas
är `data/dgsante_graph.jsonl`: **en rad per kant med det citerade stycket
bredvid**, alltså den slutna kedjan och 3,4 MB.

**7 484 av 7 821 citerade stycknummer resolverar, alltså 96 procent.**

Tre fel i vägen dit är värda att minnas, eftersom de alla gav tyst dataförlust:

- **Innehållsförteckningen startade numreringen.** Raderna `1. INTRODUCTION
  .... 1` ser ut som numrerade stycken. De åt upp numren 1 och 2, varefter
  brödtextens riktiga stycke 1 inte längre fortsatte sekvensen. Medianrapporten
  slutade på stycke 12.
- **Ett krav på obruten följd kapade resten.** Textextraktion tappar enstaka
  stycken vid sid- och spaltbrytningar, och ett tappat stycke kastade allt
  efter det. Sekvensen tillåter nu hopp om högst tre.
- Tillsammans lyfte de resolveringen **från 26 till 90 procent**.

## Två oberoende läsningar, och var de inte håller med varandra

Klassningen av ett stycke som iakttagelse eller slutsats görs på den rubrik
som gäller där stycket står, aldrig på avsnittet: avsnitt 5 heter "FINDINGS
AND CONCLUSIONS" och rymmer båda. Att läsa hela avsnitt 5 som iakttagelser var
en karaktärisering, och **rapporternas egna citat motsade den.**

Det ger ett ovanligt starkt kvalitetsmått: rubriken och citatet är två
oberoende källor om samma stycke.

| Kanten citerar | Träffar rubrikklass | Motsäger | Omärkt | Resolverar inte |
| --- | --- | --- | --- | --- |
| slutsats (2 606) | 78 % | 13 % | 8 % | 1 % |
| iakttagelse (5 201) | 67 % | 8 % | 19 % | 6 % |

**Oenigheten reconcilieras inte.** Båda läsningarna ligger kvar i varje rad,
tillsammans med rubriken som avgjorde, så att den som granskar ser var de
skiljer sig. Rapporternas citat är den starkare källan; rubrikklassningen är
en heuristik och redovisas som en sådan.

## Åtagandena: åtgärdsplanerna kopplade till rekommendationerna

Kört 2026-08-02 med `pipeline/09_link_action_plans.py`. En medlemsstat svarar
på en revision med en tabell: rekommendationens nummer, rekommendationen som
staten återger den, och den åtgärd staten åtar sig. Kolumnerna delas på den
position rubrikraden anger, eftersom en rad annars blandar kommissionens ord
med medlemsstatens.

**1 459 planer finns för 1 084 revisioner.** Av dem läses 1 068, och de ger
**5 710 svar som täcker 3 248 av 10 039 parsade rekommendationer i 844
revisioner.** Resterande planer har en layout som inte känns igen och
registreras som sådana i `data/dgsante_plan_parse.jsonl`; de gissas inte.

**Länken vilar inte på ett delat nummer.** Planen återger rekommendationens
lydelse, och den jämförs med rapportens egen.

**Måttet är hur mycket av rapportens lydelse som återfinns i planen**, inte hur
lika de två texterna är i sin helhet. Skälet är mätt: planerna är tvåspaltiga
tabeller, och svarskolumnen läcker in ord mitt i den återgivna rekommendationen
("To align the system of supervision of the facilities with the MINISTERIO DE
SANIDAD, SERVICIOS requirements laid down in Article 4.6"). Ett symmetriskt
likhetsmått straffar sådana inskott hårt trots att varje ord i rekommendationen
finns där. 136 länkar som det gamla måttet underkände visade sig vid handläsning
vara korrekta, och alla sex i stickprovet var samma rekommendation.

**2 747 av 3 140 jämförbara svar, 87 procent, bekräftas av texten.** 108 svar
räknas inte som jämförbara därför att **planen är skriven på ett annat språk**
än rapporten; en översättning kan inte bekräftas genom att jämföra ordalydelse,
och att räkna den som en missad matchning vore att skylla en översättning på
parsern.

| Andel av rapportens lydelse som finns i planen | Rader |
| --- | --- |
| 0,9 till 1,0 | 3 003 |
| 0,6 till 0,9 | 574 |
| 0,3 till 0,6 | 209 |
| under 0,3 | 304 |

Räknat per rapport föll antalet utan en enda bekräftad rad **från 186 till
118**, varav 15 har en plan på annat språk.

**Låg likhet betyder oftast att rapportparsningen är fel, inte länken.**
Stickprov i det lägsta skiktet visar planer som återger en korrekt
rekommendation medan rapportsidan innehåller förkortningslistor eller
bakgrundstext, alltså fel från steg 07. Mittskiktet är korrekta länkar med
spaltläckage i extraktionen. **Åtgärdsplanerna är därmed också ett
felfinnarverktyg för rapportparsningen**, och det är nästa uppgift att använda
dem så.

## Planerna som facit: ett mätt fel i rapportparsningen

Åtgärdsplanerna återger rekommendationerna, och den återgivningen kan användas
som facit mot rapportparsningen. Gjort 2026-08-02, och det pekade ut ett enda
mönster bakom 134 systematiskt felparsade rapporter, mest 2011 till 2013.

**Rekommendationerna står i en tvåspaltig tabell vars vänsterkolumn bara
innehåller numren.** Vid en sidbrytning skriver textextraktionen ut nästa sidas
nummer i en egen klump, skild från texten de hör till, och radvis läsning fann
då en rekommendation där rapporten har fem. Steg 07 läser numera sådana
tabeller kolumnvis och fogar ihop en rekommendation som brutits över en sida.

Effekten är mätt mot planerna, inte uppskattad:

| Mått | Före | Efter |
| --- | --- | --- |
| Rekommendationer | 8 365 | 11 999 |
| Rapporter med parsade poster | 1 699 | 2 341 |
| Rapporter som skriver ut korsreferenser | 489 | 671 |
| Länkar bekräftade av matchande text | 956 | 1 981 |
| Rader med likhet 0,9 eller högre | 459 | 1 076 |
| Citerade stycknummer som resolverar | 90 % | 96 % |
| Rapporter där varje rad är fel | 134 | 50 |

**Ett tredje fel, i mitt eget brusfilter.** Filtret som tar bort tabellens
upprepade rubrik matchade `No. Recommendation` men inte `N°. Recommendation`,
samma miss som redan rättats på annat håll. Rubriken låg därför kvar mitt i
rekommendationstexten: "...to verify the 17 N°. Recommendation 2. 3.
effectiveness of...".

**Sidbrytningen dolde en tredjedel av grafen.** Den andra rättningen kom ur
samma facit och var enklare än väntat: `pdftotext` skriver ett **form feed**
först på varje sidas första rad, och alla radankrade mönster i steg 07 till 09
tillät bara blanksteg och tabb där. Varje rubrik, post, tabell och stycke som
öppnade en sida var därmed osynligt. Elva mönster rättade; se tabellen ovan.

**Kvarvarande:** 118 rapporter utan en enda bekräftad rad, mot 186 innan
måttet byttes. 15 av dem har en plan på annat språk. Resten är i huvudsak
spaltläckage i planen som är kraftigare än containment-tröskeln tål.

## Dimensionsmodellen

Byggd med `pipeline/10_build_warehouse.py`. Det parsade lagret är format efter
hur dokumenten läser; modellen är format efter hur frågorna ställs.

| Tabell | Rader | Kornighet |
| --- | --- | --- |
| `dim_country` | 165 | ett land |
| `dim_audit` | 4 690 | en revision |
| `dim_paragraph` | 81 292 | ett numrerat stycke |
| `fact_recommendation` | 11 999 | en rekommendation |
| `fact_citation` | 7 821 | en kant i citatgrafen |
| `fact_commitment` | 5 710 | ett svar i en åtgärdsplan |

`dim_country` och `dim_audit` är konformerade: alla tre faktatabeller hänger på
dem, så en fråga kan gå från land till åtagande utan omvägar.

**Parquet-filerna är en byggartefakt** och ligger i `.gitignore`. Det som
committas är `data/dgsante_warehouse_manifest.json`, som beskriver varje tabell,
varje kolumn och varje radantal, så modellens form går att granska och testa i
CI utan binärerna.

**En olöst kant är fortfarande en rad.** Kanter som inte kunde knytas till ett
stycke behåller en tom styckenyckel i stället för att tas bort, och 1 453 svar i
åtgärdsplanerna saknar rekommendationsnyckel därför att numret inte finns i den
parsade rapporten. Att kasta dem hade fått modellen att se bättre ut än den är.

En fråga modellen gör möjlig, EU-27 från 2014, andel rekommendationer som anger
sin grund och andel som besvarats:

| År | Rekommendationer | Anger grund | Besvarade |
| --- | --- | --- | --- |
| 2015 | 303 | 75 % | 80 % |
| 2018 | 273 | 86 % | 67 % |
| 2021 | 283 | 80 % | 71 % |
| 2024 | 201 | 86 % | 50 % |
| 2025 | 140 | 81 % | 0 % |

Nollan för 2025 är inget fel: åtgärdsplanerna för de nyaste revisionerna är
ännu inte publicerade.

## Två fält som inte mäter vad namnen antyder

**`based_on_conclusions` är noll i varje rapport till och med 2013.** Fältet bär
måttet `states_its_basis` i dimensionsmodellen och rubriken "anger sin grund" på
dashboarden, och det fylls av ett mönster som bara finns i den nyare
rapportmallen: 0 av 9 033 rekommendationer till och med 2013, 50 av 440 under
2014, och 65 till 87 procent per år därefter. Andelen får därför bara redovisas
för 2014 och framåt. Tabellen ovan bär den avgränsningen, och sida 2 i
`docs/POWERBI.md` filtrerar på `Revision[year] >= 2014` av samma skäl.

Utan avgränsningen mäter talet rapportens ålder före kommissionens formulering.
Sverige har 70 av 369 rekommendationer som anger sin grund, 19 procent, och alla
70 ligger från 2014 och framåt, där andelen är 70 av 100. De åtta svenska
djurskyddsrevisionerna har 1 av 19, och 17 av de 19 är från tiden då fältet är
noll av konstruktion. Ett land med gamla rapporter ser därför sämre ut än ett
land med nya, utan att någon skillnad i formulering behöver finnas.

**`legal_basis` bär inget mått.** Fältet är ifyllt i 340 av 11 999
rekommendationer, 2,8 procent, medan 8 179 av texterna, 68,2 procent, innehåller
orden Article, Annex, Directive eller Regulation. Av de 340 ifyllda slutar 110 i
en siffra, och de värden som kommer först i filen är fragment av löpande text:
"FOR THE MISSION The mission was carried out under the general provisions of
Community legi" och "for quarantine measures to be imposed in the case of an
outbreak. Such possible new Commun". Inget mått i modellen och ingenting på
dashboarden läser fältet. Den som sätter etiketten "anger sin grund" på det får
2,8 procent där måttet för 2014 och framåt ger 68.

## Retrieval: semantisk sökning som citatapparat

Steg 14 beräknar embeddingar för samtliga 81 292 stycken med en lokal modell
(`all-MiniLM-L6-v2`, 384 dimensioner) och `src/retrieval.py` besvarar frågor
mot dem: brute force med numpy över en normaliserad matris om cirka 125 MB,
inga API-nycklar, ingen vektordatabas (ADR-0015 avfärdar de alternativen
uttryckligen). Vektorerna är härledda och ligger utanför git; det committade
är manifestet med modellnamn, radantal och sha256 per shard.

Svarslagret får bara välja och återge. Varje svar är ett stycke ordagrant,
med land, rapportreferens och styckenummer, och svarsmontören vägrar
returnera text som inte är teckenidentisk med källstycket. Matchar ingenting
frågan är svaret att ingenting i korpusen svarar. Regeln vaktas av tester:
en väljare som skriver om ett citat fälls, och mot den riktiga korpusen
verifieras att varje returnerad text finns ordagrant i källfilen.

Skälet att lagret finns är projektets egen fråga: vad kommissionen sagt om
samma typ av brist i olika länder och år. Styckena är rapporternas egna
citeringsenheter, så sökningen återanvänder exakt den struktur citatgrafen
redan vilar på.

**Vad sökningen inte kan:** modellen matchar ämne. Polaritet matchar den inte. Frågan
"kontroller utfördes men dokumenterades inte" returnerar även stycken som
berömmer dokumentationen, eftersom en bi-encoder inte skiljer ett
konstaterande från dess negation. Lagret är därför en uppslagsapparat som
hittar var ett ämne behandlas utan att ge något facit över vad som konstaterats;
läsningen av citaten är alltid människans. En väljare som förstår polaritet
kan sättas in i Selector-protokollet utan att retrieval ändras.

## Publika lager ovanpå korpusen

**HTTP-tjänsten.** `src/webapi.py` är ett tunt skal runt `src/retrieval`:
korpus, matris och modell laddas en gång, varje fråga besvaras av samma
`ask()` som ovan, och garantierna följer med oförändrade. Testerna
verifierar att en manipulerande väljare kraschar tjänsten i stället för
att servera, och att en för lång fråga avvisas före retrieval. Sökfrågor
loggas inte; containern (`Dockerfile.retrieval`) kör uvicorn utan
accesslogg och bakar in modell och shards så att en kallstart inte behöver
nätet. Driftmålet är Cloud Run scale-to-zero, tidigast dag 40.

**Webbexporten, steg 15.** Sajten frågar aldrig BigQuery: steget läser de
dbt-testade marts en gång, räknar om samma tal lokalt ur Parquet-lagret,
och vägrar skriva något de två inte är överens om. Det som committas under
`web/public/data/` är aggregat per land och år, underlag per land på
styckenivå med dokumentens sha256, och ett manifest över filerna.

**Bakade exempelsvar, steg 16.** Exempelfrågorna på /uppslag besvaras vid
byggtid genom exakt samma kodväg som tjänsten kör, så en kallstart aldrig
möter första besöket och de bakade svaren inte kan glida ifrån de levande.

**Paketering för Hugging Face, steg 17.** Warehouse-tabellerna,
källmanifestet och datasetkortet (`docs/HF_DATASET.md`) samlas i
`data/hf/` utanför git. Publiceringen är ett separat, manuellt steg som
väntar på protokollets dag 40, eftersom ett publikt dataset som beskriver
projektet skulle avslöja den svenska mätningen mitt i insamlingen.

## Nästa steg

1. **Svansen är i huvudsak äkta.** Något fel är den inte. Stickprov om 60 av de rapporter
   som saknar igenkänt avsnitt visar att 87 procent nämner rekommendationer
   bara i löptext eller i förbigående, och 8 procent inte alls. Att pressa
   dem vidare vore att gissa, vilket projektets metod förbjuder. Kvar som
   åtgärdbart står kolumndelningen i steg 09, där ett försök att låta
   rapportens lydelse välja ränna **gjorde det sämre** (0,678 mot 0,695 mätt
   på 180 planer) och återställdes.
2. Sätt ihop bilagorna per revision före parsning, enligt avsnittet om
   bilagorna som sidor.
3. Ta reda på varför 6 procent av de iakttagelse-citerade numren inte
   resolverar; hypotesen är stycken som tappats vid spaltbrytning.
