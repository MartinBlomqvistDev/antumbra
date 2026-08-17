# Verifierat

Allt här är kontrollerat mot primärkälla med angivet datum och faktiska anrop.
**Härled inte om det och sök inte på nytt.** Är något osäkert står det utskrivet.

---

## Kravkorpusen: Jordbruksverkets tillstånd och domar

Verifierat 2026-08-01 mot
`jordbruksverket.se/kontroller-och-tillsyn/miljo/stora-anlaggningar-for-uppfodning-av-fjaderfa-och-gris/tillstand-och-domar-for-stora-gris--och-fjaderfaanlaggningar`

- **237 länkar men 235 unika beslut**, 2013 till 2026. Totalt 0,85 GB hämtat 2026-08-17.
  Rättelse mot den ursprungliga räkningen: sidan listar samma URL två gånger
  (Gullspång, Ivarhag Lantbruk AB), och två skilda URL:er levererar byteidentiskt
  innehåll (Kungsbacka, Dotetorps Ägg AB, 2015-11-19, den ena med "(1)" i
  filnamnet). 236 filer ligger på disk, varav två med samma innehåll.
- Beslut före 2013 publiceras inte; då hänvisas man till kommunen.
- Listan är sorterad på **miljöprövningsdelegation, inte län**. Tolv MPD täcker
  21 länsstyrelser.

**Täckning per prövningsgrupp:**

| Grupp | Beslut |
| --- | --- |
| Skåne och Blekinge | 68 |
| Västra Götaland | 56 |
| Kalmar och Kronoberg | 30 |
| Östergötland och Jönköping | 28 |
| Halland | 26 |
| Uppsala, Västmanland, Södermanland | 13 |
| Örebro och Värmland | 12 |
| Dalarna och Gävleborg | 2 |
| Norrbotten | 1 |
| Stockholm och Gotland | 1 |
| Västernorrland och Jämtland | 0 |
| Västerbotten | 0 |

**Fem grupper bär 208 av 237, alltså 88 procent.** Nationell jämförelse går
inte att göra. Gris- och fjäderfäbältet går, och det är nästan hela branschen.

**Dokumenttyper:** 160 tillstånd, cirka 38 ändringstillstånd (stavat på fem sätt
i länktexterna, ett litet parsningsproblem), 15 förlängningar, 14 domar MMD/MÖD,
plus slutliga villkor, igångsättningsbeslut och upphävanden.

**Textlager, hela korpusen mätt 2026-08-17 efter hämtningen:** 236 filer,
5 357 sidor, varav **164 filer digitalt födda** (3 884 sidor) och **72 utan
textlager** (1 473 sidor). Filstorleken avslöjar vilket: median 0,69 MB digitalt
mot 7,51 MB skannat. **OCR krävs för 31 procent av filerna, inte för halva
korpusen.** Den tidigare siffran kom från ett stickprov om elva filer testade
med `pdftotext -layout` den 2026-08-02, och stickprovet överskattade andelen
skannade.

**Filnamnen är gratis metadata:** `Kommun_Bolag_Djurslag_Typ_Datum`. Inte helt
konsekvent, men kommun, verksamhetsutövare och beslutsdatum går att läsa utan
att öppna filen. **Flera filnamn innehåller privatpersoners namn**
i formen `Kommun_Förnamn_o_Förnamn_Efternamn`; minst tre av de 237 gör det.
Namnen återges inte i repot, och källfilerna ligger utanför versionshanteringen.

Räknat 5 357 sidor. Villkorsantalet är inte längre en uppskattning; se
avsnittet om baselinetestet nedan. Inte stor data i volym, men **hela
populationen, inte ett urval.**

---

## DG SANTE-korpusen: nedladdningen

Verifierat 2026-08-02 med faktiska anrop; volymer och format i `docs/DGSANTE.md`.

- **Komplett: 7 963 av 7 963 filer, noll fel.** EU-27, engelska rapporter
  (2 940) plus samtliga bilagor (5 023), 2,2 GB på disk.
- Ett ogiltigt fil-id ger **HTTP 404**. Nedladdningsendpointen svarar aldrig
  200 med en felsida, så varje 200-svar är dokumentinnehåll.
- Allt är inte PDF: 838 bilagor är GIF och 6 är jpg/tif, samtliga med
  numrerade titlar, alltså den äldre oklassade eran. Stickprov visar
  inskannade A4-sidor, 816x1153 pixlar. **OCR krävs för bildformaten.**
  87 bilagor är Word-exporterad HTML.
- Proveniensmanifest med sha256, källänk och hämtdatum per fil:
  `data/dgsante_manifest.jsonl`, byggt av `pipeline/04_build_manifest.py`,
  spikat mot detaljdatat av invarianttesterna.

**Kedjan når fram till åtagandet för 3 248 rekommendationer.** Verifierat
2026-08-02 med `pipeline/09_link_action_plans.py`: 1 459 åtgärdsplaner finns
för 1 084 EU-27-revisioner, 1 068 av dem läses, och de ger 5 710 svar som
täcker 3 248 av 10 039 parsade rekommendationer i 844 revisioner. Länken vilar
inte på ett delat nummer: planen återger rekommendationens lydelse och den
jämförs med rapportens. Måttet är hur mycket av rapportens lydelse som
återfinns i planen, inte hur lika texterna är i sin helhet: planerna är
tvåspaltiga och svarskolumnen läcker in ord, vilket ett symmetriskt mått
straffar hårt trots att varje ord finns där. **2 747 av 3 140 jämförbara svar,
87 procent, bekräftas.** 108 svar är inte jämförbara därför att planen är
skriven på ett annat språk än rapporten.

**Låg textlikhet pekar på fel i rapportparsningen, inte på fel länk.** Använt
som facit 2026-08-02 och det gav ett mätt resultat: 134 rapporter, mest 2011
till 2013, hade rekommendationerna i en tvåspaltig tabell vars vänsterkolumn
bara innehåller numren, och vid sidbrytning skildes numren från sin text.
Radvis läsning fann då **en** rekommendation där rapporten har fem. Efter att
steg 07 läser sådana tabeller kolumnvis, och efter ytterligare rättningar ur
samma facit (se nedan) steg rekommendationerna från 8 365 till 11 999, textbekräftade
länkar från 956 till 1 981, och rapporter där varje rad är fel föll från 134
till 50.

**Sidbrytningens form feed dolde en tredjedel av grafen.** Verifierat
2026-08-02: `pdftotext` skriver `` först på varje sidas första rad, och
samtliga elva radankrade mönster i steg 07 till 09 tillät bara blanksteg och
tabb där. Varje rubrik, post, tabell och stycke som öppnade en sida var
osynligt för parsern. Efter rättningen skriver **671 rapporter i stället för
489** ut korsreferenser, och grafens resolvering steg från 90 till 96 procent.

**Citatgrafen är sluten till 96 procent.** Verifierat 2026-08-02 med
`pipeline/08_parse_paragraphs.py`: 81 292 numrerade stycken ur 2 724
rapporter, och **7 484 av 7 821 citerade stycknummer resolverar till ett
faktiskt stycke**. Den slutna kedjan ligger i `data/dgsante_graph.jsonl`;
den fulla styckekorpusen är 66 MB, gitignorerad och återskapbar.
Styckenumreringen löper genom hela dokumentet, inte per avsnitt.

**Klassningen iakttagelse eller slutsats görs på rubriken, inte på avsnittet.**
Avsnitt 5 heter "FINDINGS AND CONCLUSIONS" och rymmer båda. Rubrikklassningen
och rapportens eget citat är två oberoende läsningar och de är oense om en
verklig minoritet: av de kanter som citerar en slutsats träffar 78 procent ett
stycke under en slutsatsrubrik, 13 procent motsäger och 8 procent är omärkta.
Oenigheten redovisas per rad i stället för att jämkas ihop.

**Citatgrafen är mycket mindre än korpusen.** Verifierat 2026-08-02 genom att
parsa samtliga 2 940 engelska EU-27-rapporter. **11 999 rekommendationer ur
2 341 rapporter**, men bara **673 rapporter, 23 procent, skriver ut vilken
slutsats en rekommendation vilar på.** Praktiken börjar **2014**; före det
finns noll korsreferenser. Grafen omfattar 2 010 rekommendationer, 2 614
kanter till slutsatser och 5 207 till iakttagelser. Det är storleksordningen
som gäller, inte 4 690 och inte 11 999. 20 rapporter skriver att de saknar
rekommendation, vilket är ett nollresultat och inte ett parsningsfel.
Mallen i `docs/DGSANTE.md` var verifierad på en rapport och gäller inte alla
eror: rekommendationerna ligger under rubrik 9 i äldre rapporter och rubrik 8
från omkring 2007, och de äldre numrerar rekommendationerna hierarkiskt
("7.1.1") i stället för flackt. Parsern läser tre layouter och täcker 94
procent av de rapporter som bär grafen, 88 procent av alla med ett avsnitt.

**De numrerade bilagorna är sidor, inte dokument.** Verifierat 2026-08-02 mot
OCR-texten: 41 procent av de skannade bilagorna inleds med ett faxhuvud, och
bilagorna till en revision från den äldre eran är sidorna i en och samma
faxade inlaga. Bara sida ett bär rubrik. Klassning per fil träffar därför 45
procent, medan minst en bilaga namnger dokumentet i **831 av 1 034 revisioner,
alltså 80 procent**. Analysenheten är revisionen, inte filen.

**OCR kört på 1 017 av 1 018 filer**, 1 886 sidor, 568 905 ord, med Tesseract
5.4 i medlemsstatens språk plus engelska. Konfidens per fil i
`data/dgsante_ocr_index.jsonl`; 715 filer ligger på 80 eller över, 123 under
70. **Två filer är trasiga hos kommissionen:** `annex/download/2603` är en
avkortad GIF som avkodar till en svart sida och är byte-identisk med vad
servern levererar, och `annex/download/3339` heter `.pdf` men är ett
OLE-dokument från Office. OCR-text används för klassning och sökning, aldrig
för ordagranna citat; citat hämtas ur källdokumentet med sidhänvisning.

**De numrerade bilagorna är inte åtgärdsplaner.** Verifierat 2026-08-02 genom
att öppna samtliga 1 974 i EU-27, se `docs/DGSANTE.md` för fördelningen. De är
i huvudsak medlemsstaternas kommentarer på rapportutkastet. Åtgärdsplaner är
89 av 1 974, och 86 av dem är HTML-stubbar vars länkmål under
`ec.europa.eu/food/fvo/ap/` svarar **404**; planerna är alltså borta från
kommissionens webb. Klassningen träffar 85 procent mot 40 handlästa bilagor
(`data/dgsante_annex_labels.jsonl`), med noll dokument felaktigt kallade plan.
**Slutsatsen står kvar efter OCR:** bland de 1 017 nylästa filerna namnger sig
noll som åtgärdsplan.

---

## Verksamhetskoder, miljöprövningsförordningen (2013:251)

Verifierat ordagrant 2026-08-02.

- **1.10-i**, IED-nivån: mer än 40 000 platser för fjäderfän, 2 000 platser för
  växande grisar tyngre än 30 kg, eller 750 platser för suggor.
- **1.11**, tillståndsplikt B: "anläggning med stadigvarande djurhållning av
  nötkreatur, hästar eller minkar med mer än 400 djurenheter, dock inte
  inhägnad". En djurenhet är en mjölkko eller sinko inklusive kalv upp till en
  månads ålder.

**Konsekvensen:** nötkreatur är tillståndspliktiga i Sverige över 400
djurenheter, men Jordbruksverkets publiceringsskyldighet följer IED-klassningen
och stannar vid 1.10-i. Nötbesluten finns hos varje länsstyrelse men publiceras
inte centralt. Det är samma transparensasymmetri projektet mäter, och
1.11-besluten är ett planerat senare spår.

**IED 2.0**, direktiv (EU) 2024/1785: nötkreatur ströks ur den slutliga texten.
Kvar blev gris vid 350 djurenheter, värphöns vid 300 och blandad produktion vid
380, infasat **från 2030**. Kommissionen ska lämna en rapport om jordbrukets
utsläpp under 2026 som kan öppna nötfrågan igen. Källa är sekundär
(Landsbygdens Folk); trösklarna bör verifieras mot direktivtexten före
publicering.

---

## Nationell djurskyddsrapport 2024 (Jordbruksverket, OVR737, 156 s)

Verifierat 2026-08-02 i fulltext.

- 7 840 fysiska kontroller under 2024, ned från 8 333 år 2023.
- **5,4 procent** av djurhållande anläggningar kontrollerade mot ett mål på
  10 procent. 2 501 planerade kontroller, varav **26 på kycklinganläggningar**.
- Ordagrant: *"Under 2024 rapporterade en länsstyrelse brister vid 33 procent av
  rutinkontrollerna, medan en annan rapporterade brister vid 84 procent av
  rutinkontrollerna."* Gapet är **51 procentenheter**, upp från 43 år 2023.
- Persistent över tid: en länsstyrelse ligger på 32 procent i tioårsmedel, en
  annan på 62.
- Ordagrant: *"Vad skillnaden i andel kontroller med brister beror på går inte
  att utläsa av statistiken, men den kan bero på att länsstyrelser haft olika
  fokusområden och kontrollerat olika typer av djurhållningar."*
- **Andelen oanmälda kontroller publiceras inte** för lantbrukets djur.
  Avvägningen oanmäld eller föranmäld görs per kontroll och registreras i
  **djurskyddskontrollregistret (DSK)**.
- Rapporten skriver att *"Jordbruksverket har hämtat uppgifter ur DSK"*. Det är
  myndighetens eget belägg för att registeruttag är rutin, och det argumentet
  bär begäran C:s rättsliga grund.

---

## Statskontorets pågående uppdrag

Verifierat 2026-08-01. Diarienummer **LI2026/00608**, redovisas **31 mars 2027**.
Uppdraget ska bland annat *"analysera hur samverkan mellan länsstyrelserna
fungerar för att djurskyddskontrollen ska vara likvärdig i hela landet"* och
analysera om handläggningen tillgodoser kraven på rättssäkerhet, objektivitet
och proportionalitet. Det är projektets kända mottagare och dess deadline.

---

## Tidigare arbete: precedens och replikationsmål, aldrig datakälla

**Guardian och Lighthouse Reports, 2025.** Kartlade över 24 000 industriella
gris- och fjäderfäanläggningar i 23 medlemsstater plus UK med FOI, EU-register
och satellitkartering. **De mätte tillståndets existens, inte dess innehåll**;
verifierat i deras egen text. Inga utsläppsgränser, inga lagringskrav, ingen
kontrollfrekvens. Ingen metodsida publicerad trots att Lighthouse normalt gör
det, och kartan har varken nedladdningsbar data eller metodnot. Sverige ingick
inte. Det är luckan projektet arbetar i.

**Djurrättsalliansen och Djurens Rätt.** Begär ut kontrollrapporter via
offentlighetsprincipen och räknar. **Rutten fungerar, det är bevisat.**

- Slakterigranskningen (underlag t.o.m. augusti 2021): 117 registrerade
  slakterier, 96 kontrollerade, 21 aldrig kontrollerade, 85 hade brutit mot
  djurskyddslagen minst en gång, 11 hade aldrig haft en brist.
- 2022: 83 av 88 kontrollerade slakterier, över 900 konstaterade brister.
- Slaktstatistik 2024: 117 881 540 landdjur.
- Djurens Rätt begär årligen ut kontrollrapporterna från djurskyddskontroller
  på de fyra stora kycklingslakterierna (Kronfågel, Guldfågeln, Torsåsens
  Fågelprodukter och Atria) och sammanställer dem i Kycklingkartläggningen.
  Deras egen slutsats för 2024 är att **minst 56 000 kycklingar** utsattes för
  behandling som ledde till smärta, stress eller tidig död fram till slakt.
  Talet är alltså deras bedömning av antal drabbade djur, inte antal
  kontroller, anläggningar eller granskade rapporter. Sekundärkälla
  (djurensratt.se); underlaget är inte publicerat, och talet ska inte
  återanvändas som datapunkt, bara som precedens. Se regeln nedan.

**Båda publicerar slutsatser och siffror, aldrig underlaget.** Ingen
nedladdningsbar data, ingen metodbeskrivning, ingen baseline.

**Regeln:** använd dem som precedens för att rutten fungerar, och som
replikationsmål. **Använd dem aldrig som datakälla.** Djurrättsalliansen har ett
uttalat mål att avveckla djurindustrin. Bygger projektet på deras tal ärver det
deras slutsats och avfärdas utan sakprövning.

**Kalmarfallet**, deras bästa berättelse, passar inte i materialet. Februari
2024 filmade Dagens Vimmerby en container med döda och döende hönor. April 2024
konstaterade länsstyrelsen "omfattande och allvarliga brister" och
"oacceptabelt". April 2025 dokumenterade Djurrättsalliansen sjuka och döda
hönor igen. Juni 2025 återvände länsstyrelsen: ventilationen trasig i tio dagar,
gödselbandet sönder, ammoniak, och de beordrade omedelbar slakt. Februari 2026
visste länsstyrelsen inte om anläggningen var i drift. **Men anläggningen har
cirka 10 000 hönor och IED-tröskeln går vid 40 000.** Det värst dokumenterade
fallet ligger under tröskeln och finns inte i tillståndsmaterialet. Det ska stå
i metoden i stället för att upptäckas av någon annan.

---

## Maskningsmätningen: bildmetoden mot textlagret

Verifierat 2026-08-14 genom körning över hela leveransmaterialet, steg 18.

Leveranserna kommer i två former. Digitalt födda filer bedöms ur textlagret:
en fylld rektangel är en maskning, och om text ligger kvar under den avgör om
maskningen är verklig. Skannade filer saknar textlager och bedöms i stället på
den renderade sidan, genom solida mörka rektanglar i bilden.

**Bildmetoden är prövad mot textmetoden på samtliga 248 digitalt födda
dokument**, alltså där ett facit redan fanns:

| Facit ur textlagret | Antal | Balk hittad | Ingen balk |
| --- | --- | --- | --- |
| maskade (`text_removed`) | 123 | 122 | 1 |
| omaskade (`none`) | 118 | 1 | 117 |
| endast markör (`marker_only`) | 7 | 3 | 4 |

Tre parametersättningar prövades mot samma facit innan en valdes; den valda är
strikt bättre än de två andra. **De två avvikelserna är kända och förklarade:**

- Det missade maskade dokumentet är `kronoberg_A`, där maskningen är 13 gånger
  15 punkter, alltså under detektorns minsta balk om 40 gånger 6 bildpunkter
  vid 100 dpi. En maskning så liten som två tecken hittas inte.
- Den falska träffen är `jamtland_A`, ett dokument med fotografier, där ett
  mörkt parti i ett foto uppfyller balkkriterierna. Fotografier i skannat
  material kan alltså räknas som maskning.

**Golvet metoden inte ser förbi:** en skanning av en sida vars text togs bort
före utskrift ser likadan ut som en sida som aldrig bar texten. `masked` falskt
på en skanning betyder att ingen balk hittades, inte att ingenting undanhållits.

**Utfallet över hela materialet, 293 dokument, inga uteslutna.** Två mått
hålls isär, och bara det andra är protokollets:

*Andel dokument med minst en maskning*, poolat över landet: begäran A 138 av
155, 89 procent; begäran B 31 av 134, 23 procent. Före bildmetoden var 45
dokument omätbara och samma tal var 86 mot 17 räknat på 244 dokument.

*Kontrastmåttet enligt P1*, alltså skillnaden i maskningsgrad mellan A och B
inom samma myndighet: 14 län har levererat i båda klasserna. Medianskillnaden
är **2,3 procentenheter maskerad yta** och **80 procentenheter andel maskade
dokument**. Inget av de fjorton länen har högre maskad yta i B än i A. Dalarna
är det enda som vänder på andelsmåttet, 60 procent av A mot 80 procent av B,
medan ytan där pekar åt samma håll som i övriga län.

**Det som ännu inte är byggt av det förregistrerade måttet:** maskningsgrad är
förregistrerad som andel maskerad yta **plus andel maskerade fält**, och ska
enligt avsnitt 4 och P1 redovisas per djurslag. Fältmåttet kräver att
handlingarnas fältstruktur parsas, och djurslag kräver klassning per handling.
Ingetdera finns; ytdelen och dokumentandelen är det som mäts i dag, och det ska
sägas när talen används.

---

## Djurslag och kontrastmåttet inom djurslag

Verifierat 2026-08-14 genom körning av stegen 19 till 21 över hela
leveransmaterialet.

**OCR på de skannade leveranserna.** 45 dokument, 378 sidor, 58 305 ord,
Tesseract med svenskt språkpaket i 300 dpi. Medelkonfidensen är 82,9 med
median, lägst 28,9 och högst 95,2. Åtta läsningar ligger under 70 i konfidens
eller under 30 ord och ska inte behandlas som lika säkra som de övriga;
konfidensen står per dokument i `data/leveranser_ocr_index.jsonl`. Texten
ligger utanför git eftersom den namnger enskilda.

**Djurslagsklassningen är prövad mot ett oberoende facit.** Flera län skriver
djurslaget i filnamnet, till exempel "Föreläggande ... nöt, kalv" och
"... gris". 23 dokument bär en sådan etikett från myndigheten själv, och två
test har körts mot den. **Mjukt test, finns filnamnets djurslag i texten: 22 av
23. Strikt test, är klassningens utpekade dominerande djurslag detsamma som
filnamnets: 21 av 23.** Avvikelserna är ett hullvärderingsschema för nötkreatur
där djurslaget står i titeln men inte i blankettexten, och ett föreläggande vars
filnamn säger nöt men vars text nämner fjäderfä oftare.

40 dokument nämner inget djurslag: fyra är inte leveranser utan avgiftsbeslut
och riktlinjer, fyra är fotobilagor, en är en blankett, och 31 är rapporter
eller beslut med 400 till 2 500 ord text, alltså inte ett extraktionsfel.
Flera av de 31 är administrativa bilagor som rimligen inte nämner djurslag,
såsom underrättelser, kopior av klagomål och tjänsteanteckningar.
**Ordlistan har medvetet inte justerats mot de 31**, eftersom det vore att
anpassa klassificeraren efter samma dokument som ska bedöma den. Ett handläst
stickprov återstår, och till dess är klassningen prövad bara mot filnamnen.

**Kontrastmåttet inom djurslag, P1:s definition.** 62 celler av myndighet,
djurslag och klass; 22 har både A och B, varav 11 har minst tre dokument i
båda:

| Djurslag | Län | Median, andel maskade | Median, maskad yta | Negativa |
| --- | --- | --- | --- | --- |
| nöt | 9 | +80 procentenheter | +2,74 procentenheter | 1 |
| fjäderfä | 2 | +100 procentenheter | +0,73 procentenheter | 0 |
| gris | 0 | går inte att beräkna | går inte att beräkna | - |

**Kontrasten är alltså inte en djurslagsartefakt.** Den enda negativa cellen är
Dalarna, där andelen maskade dokument är lägre i A än i B, med tre dokument i
A; ytmåttet pekar där åt samma håll som i övriga län. För gris saknas underlag
helt, vilket stämmer med att Dalarna uttryckligen svarat att någon
kontrollrapport för gris inte påträffats, och det ska redovisas som en gräns
för mätningen och inte döljas.

---

## Villkorslagret: baselinetestet mot standardtext

Mätt 2026-08-17 med `pipeline/24_condition_baseline.py` över de 236 hämtade
filerna, som är 235 unika beslut, och om 2026-08-18 sedan de skannade besluten
OCR-lästs. Testet ligger före all extraktion av ett skäl:
om villkoren är standardtext som återanvänds mellan anläggningar beskriver ett
villkorsregister en mall, och då är det resultatet. Nollhypotesen är alltså att
villkoren är mall.

**Instrumentet räknar bara inom villkorsavsnittet.** En första version
segmenterade på varje rad som inleds med siffra och punkt var som helst i
dokumentet, och då gav bara 12 beslut av 144, **8 procent**, en obruten
sifferserie 1..N. Numrerade listor finns över hela besluten, i redogörelsen och i
upplysningarna, så det måttet togs över en blandning av villkor och annan text.
Den version som gäller söker villkorsrubriken, läser till nästa avsnittsrubrik
och segmenterar bara innanför det fönstret: då ger **88 procent** av de digitalt
födda besluten en obruten serie, 106 av 120. Att rubriken inte alltid går att
hitta stämmer med att `VILLKORSSCHEMA.md` avsnitt 2.2 redan skriver att rubriker
varierar och kan saknas.

**Täckningen, räknad så som en kritisk läsare skulle räkna den.** Efter att steg
25 OCR-läst de 72 skannade besluten saknar ingen fil text. Kvar som bortfall: 60
filer utan villkorsrubrik som går att hitta och 3 med rubrik men inget numrerat
villkor. Segmenterade: **173 filer av 236, alltså 73 procent, och 2 264
villkor**, median 13 villkor per beslut. Rubrikträffen är nästan lika god i båda
källorna: 122 av 164 digitalt födda och 54 av 72 OCR-lästa, alltså 74 respektive
75 procent. Verifiering är kontroll 1 i `VILLKORSSCHEMA.md` avsnitt 5,
sifferserien 1..N, och varje beslut bär utfallet som `series_ok` och sin källa
som `källa`.

**Täckningen för själva huvudsiffran är däremot oförändrad.** 73 procent gäller
segmenteringen, inte återanvändningsmåttet. Huvudsiffran räknas på de 120
digitalt födda besluten, alltså 51 procent av korpusen, precis som före OCR:n.
Det som tillkommit är en andra, separat mätning på 53 andra beslut.

**OCR-läst text segmenteras sämre, och det är utskrivet i stället för utjämnat.**
Obruten serie fås för 106 av 120 digitalt födda beslut, 88 procent, men bara 21
av 53 OCR-lästa, 40 procent. OCR bryter dessutom ord över radslut, så två
identiska villkor överlever sällan som identiska strängar när ett av dem lästs
med OCR. Därför poolas källorna aldrig i huvudsiffran; det poolade talet skrivs
ut men bär ingen slutsats.

**Resultatet, och det står sig i varje delmängd:**

| Underlag | Villkor | Beslut | Olika texter | Delad text | Egna villkor, median per beslut |
| --- | --- | --- | --- | --- | --- |
| **huvudsiffra, ur textlagret** | 1 704 | 120 | 1 316 | 605 (36 %) | 68 % |
| ur textlagret, obruten serie | 1 545 | 106 | 1 200 | 544 (35 %) | 70 % |
| enbart OCR-lästa | 560 | 53 | 489 | 112 (20 %) | 83 % |
| poolat, bär ingen slutsats | 2 264 | 173 | 1 762 | 771 (34 %) | 70 % |

**Huvudsiffran rörde sig inte när OCR-mängden tillkom.** Samtliga tal i första
raden är identiska före och efter att 53 beslut lades till underlaget, vilket de
ska vara, eftersom raden räknas på oförändrade dokument. Det är kontrollen på
att OCR-tillskottet är additivt och inte har rört det som redan var mätt.

**Nollhypotesen faller.** 1 099 av 1 704 villkor, 64 procent, förekommer i ett
enda beslut, och medianbeslutet har egen text i 68 procent av sina villkor. Ett
villkorsregister mäter alltså något som varierar, och arbetet med att bygga det
är motiverat. Måttet är exakt likhet efter gemener och kollapsat blanktecken,
ingenting annat normaliserat, siffervärden avsiktligt bevarade: **det kan bara
underskatta återanvändningen**, aldrig överskatta den. Ett segmenteringsfel som
delar ett villkor i två drar åt samma håll, alltså mot mer skenbar egenart, så
båda felkällorna gör slutsatsen försiktigare och ingen av dem gör den starkare.

**Den delade texten är inte korta fragment.** Delade texter har median 210
tecken mot 260 för de egna, och 6 av 217 ligger under 80 tecken. Det är hela
villkor som återanvänds, inte gemensamma formuleringar som halkat med.

**Den återanvändning som finns är gruppintern, och det är inte en
storlekseffekt.** Av de 217 texter som förekommer i mer än ett beslut stannar
**204 inom en enda prövningsgrupp**. Under slumpmässig omfördelning av besluten,
med prövningsgruppernas faktiska storlekar bevarade, väntas 25,3 och den 95:e
percentilen ligger på 33; noll av 2 000 permutationer nådde 204 (`p < 0,0005`).
Koncentrationen är alltså inte en följd av att Skåne med Blekinge och Västra
Götaland bär hälften av korpusen.

**Koncentrationen replikerar på en oberoende dokumentmängd.** De 53 OCR-lästa
besluten delar inga dokument med de 120 digitalt födda och är lästa med ett
annat instrument. Där stannar **39 av 41 delade texter inom en enda
prövningsgrupp** mot 4,2 väntat under samma permutation, och noll av 2 000
omfördelningar nådde 39. Att andelen delad text är lägre i den mängden, 20 mot
36 procent, är väntat och pekar åt rätt håll: exakt matchning missgynnar OCR-text
och kan bara underskatta återanvändningen där.

**Den konkurrerande förklaringen prövad.** Ett ändringsbeslut upprepar
originalets villkor, och det skulle ge gruppintern återanvändning utan att någon
mall finns. Den förklaringen räcker för par, som är 141 av de 217 klustren, men
inte för de breda: den vidaste texten delas av **26 beslut, varav 24 i Västra
Götalands län**, och tio beslut i Kalmar med Kronoberg delar en annan.
Ändringskedjor hos en och samma verksamhetsutövare blir inte 24 beslut.
Omvänt gäller att de allra vidaste texterna är de som korsar gruppgränser,
medan den typiska delade texten stannar; av de 18 klustren med minst fem beslut
ligger 14 inom en enda grupp.

Mallar finns alltså, de är prövningsgruppens snarare än landets, och de
förklarar drygt en tredjedel av villkoren. Det är i sig ekvivalensfrågan ställd
på kravsidan.

**OCR på tillståndskorpusen, körd 2026-08-17 och om 2026-08-18.** Steg 25 läste
samtliga 72 skannade beslut, 1 473 sidor och 436 515 ord, med Tesseract i
svenska. Talen är identiska i båda körningarna. Mediankonfidens
91,5, tionde percentilen 76,6, och fyra beslut ligger under 70 med lägst 46,7.
Tre beslut föll på ett övergående fel i första körningen och lästes felfritt vid
omförsök, varefter omförsök byggdes in i steget.

**Ett fel i steget som resultatet självt avslöjade.** Första OCR-körningen gav
noll villkor ur samtliga 72 beslut medan texten uppenbart innehöll dem.
Orsaken: funktionen kopierades från steg 19, som slår ihop varje sidas ord till
en enda sträng, vilket räcker för djurslagstermer men inte här. Ett beslut blev
34 815 tecken på 31 rader, en per sida, och steg 24 ankrar på radbörjan.
Radstrukturen återskapas nu ur Tesseracts block-, stycke- och radnummer; samma
beslut blev då 642 rader och gav femton villkor.

**Gränserna, oförkortade.** Rubrik- och stopplistorna är heuristik över de
layouter som faktiskt finns i korpusen, inte en specifikation. De 14 digitalt
födda beslut som faller på seriekontrollen gör det av tre skäl som gått att läsa
i texten: ett strönummer mitt i serien, en andra numrerad lista efter villkoren
som stoppordet missar, och ändringsbeslut som lagligen börjar på villkor 35
eller 12. Bland de OCR-lästa faller 32 av 53, och där är orsaken en annan:
tecken och hela nummerrader går förlorade i inläsningen. Den största kvarvarande
luckan är nu de 60 filer där ingen villkorsrubrik hittas, alltså 25 procent av
korpusen, och den ligger i rubrikmönstret och inte i texttillgången.

---

## Fältmåttet: text som döljs utan att svärtas

Mätt 2026-08-17 med `pipeline/26_hidden_text.py` över de 249 levererade
dokument som har textlager. Beslutet att ersätta det förregistrerade fältmåttet
med ett mått på täckt innehåll, och skälen till det, står i ADR-0017.

**Instrumentet jämför textlagret mot den renderade sidan.** Ett tecken är dolt
när dess glyfruta, renderad i 150 dpi gråskala, inte innehåller en enda pixel
mörkare än 200. Ingenting antas om vad som täcker, så en vit rektangel, en ljus
bild och en täckande annotering fångas av samma test.

**Den negativa kontrollen kom före resultatet.** Ett färgbaserat mått prövades
först och gav mörk text under en ljus ruta i 39 av 60 dokument. **27 av dem gav
exakt samma tal, 2 701 tecken**, i skilda län och skilda ärenden. Den identiska
siffran avslöjade ett mallelement: kontrollrapporten ritar en vit bottenplatta
bakom brödtexten. Samtliga dessa tecken renderas synligt, alltså ligger plattan
bakom texten och inte över den, och det färgbaserade måttet hade flaggat alla 39
fel.

**Utfallet är ett nollresultat.**

| Klass | Dokument | Med minst ett dolt tecken | Med dold brödtext |
| --- | --- | --- | --- |
| A | 125 | 0 | 0 |
| B | 120 | 41 | 0 |
| övrigt | 4 | 0 | 0 |

Sammanlagt 232 dolda tecken av 2 947 869. Den längsta dolda strängen i ett
enskilt dokument är 13 tecken, och fördelningen är 28 dokument med fyra tecken,
elva med fem eller sex, ett med åtta och ett med tretton. **Samtliga ligger i
övre marginalen**, och teckenklasserna svarar mot diarienummer, datum och
sidnumrering: myndighetens egen vita sidhuvudruta täcker sitt eget sidhuvud.
Noll dokument döljer brödtext bakom en ljus täckning.

**Att alla 41 ligger i klass B är inget maskningsfynd.** Det följer av att
föreläggandenas mall ritar den vita sidhuvudrutan och kontrollrapporternas inte
gör det. Talet mäter mallar, inte myndighetsbeteende, och får inte läsas som att
B skulle vara mer maskat än A; kontrasten går åt andra hållet och mäts i steg 18
och 21.

**Nollresultatet beror inte på tröskeln.** Gränsen på tio sammanhängande tecken
valdes för att en maskning täcker en sträng och inte ett tecken, men den längsta
dolda strängen i brödtext över hela materialet är **noll tecken**. Utfallet blir
alltså detsamma för varje tröskel från ett och uppåt, och tröskelvalet kan inte
ha skapat resultatet.

Tillsammans med steg 18:s resultat att noll dokument har läsbar text kvar under
en svärtad ruta är bilden entydig i en avgränsad fråga: **den maskning som
gjorts är tekniskt äkta, och ingen myndighet har dolt innehåll med en teknik som
ytmåttet missar.** Påståendet gäller maskningens teknik, aldrig dess omfattning;
hur mycket som maskats mäts på annat håll och är det som skiljer länen åt.

**Gränsen, utskriven.** Text som raderats före utlämnandet lämnar ingenting kvar
att jämföra mot och kan inte upptäckas ur handlingen ensam. Måttet visar att
ingenting täcks utan att synas, aldrig att ingenting saknas. Skannade handlingar
ingår inte, eftersom de saknar textlager att jämföra renderingen mot.
