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

**Rättelse 2026-09-01: två sorters svarta rektanglar var inte maskningar.**
Här stod att en fylld rektangel i textlagret är en maskning, utan förbehåll. Den
1 september 2026 arkiverades Kammarrätten i Jönköpings meddelande i mål 3249-26,
och steg 18 bedömde ett domstolsbrev utan en enda maskning som maskat. Två
felkällor kom fram, båda beskrivna i ADR-0019. Den ena är kontrollrapportmallens
svarta tabellhuvud med vit text, som finns i 105 av de 124 digitalt födda A- och
B-handlingar som över huvud taget har rutor, och som för 33 av dem var den enda
grunden för maskningsdomen. Den andra är vågräta linjer om en halv punkt, som
klarar ytgolvet på sin bredd. Textmetoden utesluter numera båda. En av Jämtlands
kontrollrapporter är läst för hand som kontroll och är utlämnad utan en enda
maskning, med djurhållarens namn och adress i klartext.

**Rättelse 2026-09-01: valideringens rena rad går inte att reproducera.**
Tabellen ovan står kvar som den redovisades. Dess maskade rad kommer tillbaka
dokument för dokument när jämförelsen körs om mot exakt samma 248 handlingar och
samma facit: 122 med balk och 1 utan. Den rena raden kommer inte tillbaka. Av
de 118 omaskade handlingarna ger 30 balk, där tabellen redovisar 1, och
markörraden blir 4 och 3 där tabellen har 3 och 4. Detektorn är oförändrad sedan
valideringen, vilket är kontrollerat i git. Den vanligaste felkällan är
verifierad okulärt: länsstyrelsens vapen på sidan ett är en solid svart sköld,
49 gånger 9 bildpunkter vid 100 dpi, och den klarar varje krav detektorn ställer
på en balk. Mot det rättade facit ger bildmetoden balk i 64 av de 155
handlingar som textmetoden bedömer som omaskade, av materialets 261 digitalt
födda; talet 155 är alltså ett annat än klass A:s 155.

**Åtgärdat samma kväll, till hälften.** Villkoret för att anta en
uteslutningsregel skrevs i protokollloggen innan utfallet var känt, och
utfallet står i ADR-0020. Vapnet och rubrikbandet utesluts numera även ur
bildmetoden. Falsklarmen faller från 64 av 155 till **30 av 155**, alltså från
41 till 19 procent, medan missarna står kvar på 1 av 88. Resten är fotografier:
varje kvarvarande handling har minst en balk inuti en rasterbild, och det är den
felkälla ADR-0016 skrev ut från början. En regel för fotografier är avvisad med
skäl, eftersom Halland har lämnat en fotobilaga där maskningarna är ritade
ovanpå bilderna.

**Ingen siffra nedan rör sig av den regeln.** Ingen skannad handling byter dom,
eftersom var och en som bär de två elementen också bär andra balkar. Därför står
uppdelningen på metod kvar, och därför gäller reservationen om den skannade
halvan fortfarande. Vad `masked` sant betyder
på en skanning är därför en öppen fråga, och den ligger i ADR-0016:s tillägg.

**Utfallet, räknat på de 290 handlingarna i klass A och B.** De övriga 16
dokumenten i `data/maskning.jsonl` är myndighetsbeslut, Gotlands omprövade
leverans och kammarrättens meddelande, alla utanför måttets population enligt
P8. Två mått hålls isär, och bara det andra är protokollets:

*Andel dokument med minst en maskning*, poolat över landet: begäran A **108 av
155**, 70 procent; begäran B **29 av 135**, 21 procent. Talen ska läsas
uppdelade på metod, eftersom de två halvorna är olika säkra:

| Klass | Digitalt födda | Skannade | Totalt |
| --- | --- | --- | --- |
| A | 78 av 125, 62 % | 30 av 30, 100 % | 108 av 155, 70 % |
| B | 18 av 120, 15 % | 11 av 15, 73 % | 29 av 135, 21 % |

Att varenda skannad A-handling bedöms som maskad är förenligt med bildmetodens
falsklarmsfrekvens om 19 procent, och det är inte prövat mot handläsning för en
enda av dem. Den digitalt födda halvan vilar på ett instrument som är prövat på
det sättet.

Det tal som stod här före bildmetoden, 86 procent mot 17 räknat på 244 bedömbara
dokument, vilar på den oreviderade rutregeln och kan inte jämföras med talen
ovan.

*Kontrastmåttet enligt P1*, alltså skillnaden i maskningsgrad mellan A och B
inom samma myndighet: 14 län har levererat i båda klasserna. Medianskillnaden
är **2,04 procentenheter maskerad yta** och **68 procentenheter andel maskade
dokument**. Inget av de fjorton länen har högre maskad yta i B än i A. Två
vänder på andelsmåttet: Dalarna med 20 procent av A mot 80 procent av B, och
Gävleborg med 0 mot 25 procent.

**Det förregistrerade måttets två öppna delar är sedan dess avgjorda, båda på
annat sätt än planerat.** Maskningsgrad är förregistrerad som andel maskerad yta
**plus andel maskerade fält**, och ska enligt avsnitt 4 och P1 redovisas per
djurslag. Fältmåttet visade sig inte gå att beräkna bokstavligt, eftersom
handlingarna är prosa och inte formulär, och ersattes 2026-08-17 av ett mått på
täckt innehåll enligt ADR-0017; utfallet blev ett nollresultat. Djurslag krävde
klassning per handling, och den finns sedan steg 20, prövad mot handläsning
2026-08-25. Talen i det här avsnittet är ändå poolade över djurslag, eftersom de
mäter något annat än den djurslagsuppdelade tabellen längre ned; vilket som
avses ska sägas när talen används.

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
anpassa klassificeraren efter samma dokument som ska bedöma den. **Det handlästa
stickprovet gjordes 2026-08-25**, se avsnittet om djurslagsregeln prövad mot
handläsning: 18 dokument, noll fel djurslag. Fram till dess var klassningen
prövad bara mot filnamnen.

**Kontrastmåttet inom djurslag, P1:s definition.** 62 celler av myndighet,
djurslag och klass; 22 har både A och B, varav 11 har minst tre dokument i
båda:

| Djurslag | Län | Median, andel maskade | Median, maskad yta | Negativa |
| --- | --- | --- | --- | --- |
| nöt | 9 | +80 procentenheter | +2,59 procentenheter | 1 |
| fjäderfä | 2 | +50 procentenheter | +0,46 procentenheter | 0 |
| gris | 0 | går inte att beräkna | går inte att beräkna | - |

Talen är omräknade 2026-09-01 efter rättelsen längre upp. Före den stod +2,74
och +0,73 procentenheter maskerad yta och +100 procentenheter andel för
fjäderfä.

**Kontrasten är alltså inte en djurslagsartefakt.** Av de elva cellerna pekar
åtta åt samma håll, två visar ingen skillnad alls och en är negativ. Den
negativa är Dalarna nöt, med tre dokument i A, och där pekar sedan rättelsen
båda måtten åt samma håll: 88 procentenheter lägre andel maskade dokument i A
och 0,02 procentenheter lägre maskad yta. De två utan skillnad är Jämtland nöt
och Västerbotten fjäderfä, där båda klasserna är helt omaskade. För gris saknas underlag
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
korpusen, och den ligger i dokumenttypen snarare än i texttillgången. Deras egna
korta rader handlar om att ändra enstaka villkor och inte om att meddela en
uppsättning: "villkorsändring" på tio, "ändring av villkor i tillstånd" på åtta,
"villkoret ska ha följande ändrade lydelse" och "villkor N ändras till följande
lydelse" på fyra vardera. Femton av de 60 nämner inte ordet villkor på någon
kort rad alls. Filnamnen kan inte avgöra saken: de bär ingen läsbar dokumenttyp
för 43 av de 60.

**De 60 är till största delen en annan dokumenttyp, uppmätt 2026-08-22:**
27 ändringsbeslut, 16 förlängningar eller igångsättningsbeslut, 5 domar, 3 som
inte nämner ordet villkor på någon kort rad, och 9 övriga. Endast
ändringsbesluten bär villkorstext, och bara 10 av dem anger ett villkorsnummer
som går att läsa maskinellt.

**En segmenterare för ändringsbeslut prövades i tanken och byggdes inte.** Den
skulle lyfta beslutstäckningen med omkring åtta procentenheter men bara
villkorstäckningen med ungefär en procent, och skälet att avstå är starkare än
så: **ett ändrat villkor är per definition unikt för sin ändring.** Att föra in
dem i återanvändningsmåttet skulle mekaniskt sänka andelen delad text och
blanda två populationer, den stående kravuppsättningen och ändringarna av den.
Hålls de i stället strikt åtskilda tillför de en liten sidomängd utan eget
värde för frågan. Bedömningen är gjord efter mätning och redovisas här i
stället för att luckan beskrivs som ett förbiseende.

**En utvidgad rubriklista är också mätt och medvetet inte införd.** Formen "för
tillståndet gäller följande villkor:" är en äkta villkorsrubrik som mönstret
missar, och den skulle lägga till **fyra beslut**, alltså 1,7 procent av
korpusen. Ändringen görs inte, eftersom den skulle vara en justering av
instrumentet efter att utfallet setts och vinsten är för liten för att motivera
att ett publicerat tal räknas om.

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

---

## Begäran C: den rättade leveransen och omräkningen ur radnivådata

**Uttaget för 2024 var ofullständigt och rättades efter en fråga.** Leveransen
den 17 augusti 2026 hade 1 577 rader i bladet Nötkreatur 2024 mot 2 916 för
2025, saknade Norrbotten och Uppsala helt och gav nio län en handfull rader där
året borde bära hundratals. Frågan om bladet var fullständigt ställdes samma dag
12:34, med talen utskrivna. Svaret kom **samma dag 17:19** med en rättad fil:
**2 451 rader och samtliga 21 län**, sha256 734bc8359c62, bilagans storlek
11 454 946 byte enligt e-posthuvudet. Myndigheten skriver ordagrant: *"Vi ber om
ursäkt för att innehållet i fliken Nötkreatur 2024 inte verkat ha blivit
fullständig. Vi har gjort om det utdraget ur systemen och lagt in uppdaterad
data i den fliken."*

| Län | Rader före | Rader efter |
| --- | --- | --- |
| Jönköping | 12 | 154 |
| Kronoberg | 4 | 135 |
| Västerbotten | 6 | 136 |
| Östergötland | 2 | 102 |
| Kalmar | 57 | 143 |
| Södermanland | 2 | 85 |
| Stockholm | 4 | 67 |
| Norrbotten | 0 | 65 |
| Uppsala | 0 | 49 |

Övriga tolv län ändrades med noll till tio rader, och **de sju andra bladen är
innehållsidentiska**. Felet träffade alltså ett blad och inom det vissa län, inte
materialet jämnt.

**Spridningen omräknad ur raderna, steg 22.** Rutinkontroller enligt
myndighetens egen kategorisering, län med minst 20 kontroller:

| År | Län | Lägst | Högst | Spridning |
| --- | --- | --- | --- | --- |
| 2024 | 21 av 21 | Södermanland 31 % | Västmanland 88 % | 57 procentenheter |
| 2025 | 19 av 21 | Södermanland 28 % | Jönköping 73 % | 45 procentenheter |

**Detta reproducerar inte rapportens 33 och 84 procent, och ska inte påstås
göra det.** Tre definitioner av rutinkontroll prövades mot 2024 års nötdata:
myndighetens egen lista ger 27 till 91 procent, samma lista utan Ansökan
tillstånd ger likaså 27 till 91, och enbart Rutinkontroll risk och slump ger 28
till 74. Ingen träffar 33 och 84. Den mest närliggande förklaringen är att
rapportens mening gäller all djurskyddskontroll medan begäran C bara omfattar
nötkreatur, gris och fjäderfä, alltså två skilda populationer; **den
förklaringen är inte verifierad mot myndigheten**. Definitionen justerades inte
för att träffa talen, eftersom en definition vald efter facit inte mäter något.

Rapportens 51 procentenheter står därför kvar som myndighetens egen uppgift,
ordagrant citerad ovan, och omräkningen redovisas bredvid som en annan mätning
på ett annat underlag.

**Dimensionen föranmäld mot oanmäld finns fortfarande bara nationellt.**
Myndigheten har skriftligen svarat att den inte går att ta fram per län med
rutinbetonade åtgärder. Den förregistrerade hypotesen i avsnitt 10, som ska
prövas per länsstyrelse, kan alltså inte prövas på C-datat som det ser ut.

**Beslutsspåret är öppet, och det påverkar när insamlingen kan kallas stängd.**
Prövning och skriftligt överklagbart beslut enligt 6 kap. 3 § OSL begärdes den
17 augusti 2026 för just den sammanställningen. I samma brev som den rättade
filen svarar myndigheten ordagrant: *"Vi kommer återkomma till dig i frågan
kring beslut kring föranmälda och ej föranmälda kontroller uppdelat per län och
år."* Begäran C är alltså levererad till de delar den kunnat levereras, men
beslutsspåret löper.

Tillämpningsnot 3 kräver att varje begäran nått slutstatus innan publicering.
`src/open_items.py` räknade tidigare C som avslutad enbart på att en leverans
fanns, och det är rättat 2026-08-18: **ett begärt men inte meddelat beslut
hindrar slutstatus, oavsett hur mycket som levererats.** Effekten är avgränsad
och kontrollerad: fyra begäranden har öppet beslutsspår, men Kalmar B, Örebro A
och Örebro B var redan öppna som avgiftsstoppade, så bara Jordbruksverket C
byter status. Avslutade går från 35 till 34.

---

## P9:s kriterier prövade, 2026-08-20

Not 4 gör P9:s kriterier till utlösaren för varje P8-skrivelse, och prövningen
hade aldrig gjorts. Underlaget är `data/sekretessgrunder.jsonl`, som citerar
varje myndighets egen lydelse om vad som maskats och med vilket stöd, med
meddelande-id och en flagga för om citatet är fullständigt i källan.

**Registret är handkurerat men slutet sedan 2026-08-22.** Ingen kod skapar
filen; varje rad är avskriven för hand ur ett följebrev, på samma villkor som det
handlästa facit som bär bilageklassningen. Populationen är maskinellt definierad
av `pipeline/29_check_grounds.py`: varje län och klass med minst ett maskat
dokument ska ha en rad. **Täckningen är 25 av 25.** En enda rad saknar sitt
citat, Kalmar A, vars följebrev inte går att hämta ur brevlådan trots att
leveransen är loggad och filerna ligger på disk; raden finns ändå och bär
flaggan `kalla_ej_atkomlig` i stället för att utelämnas.

**Kriterium (c), maskning i klass B med stöd av 30 kap. 23 §: noll, nu prövat
mot varje maskad B-leverans i stället för mot sökningar.** Tio län maskade i
klass B och inget av dem åberopar bestämmelsen. Västra Götaland undanhåller två
beslut helt med stöd av 18 kap. 1 och 3 §§. Stockholm, Dalarna och Halland
maskar personuppgifter, Dalarna och Halland uttryckligen med stöd av
dataskyddsförordningen och inte av OSL; enligt avsnitt 11 i mallen är sådan
maskning i ett B-svar ingen avvikelse enligt P9 och får inte räknas som en.
Blekinge anger sekretess utan bestämmelse. **Fem län maskade i klass B utan att
ange någon grund alls:** Gävleborg, Kronoberg, Södermanland, Uppsala och
Västmanland. Det är ett fynd i sig, och det visar en egenskap hos kriteriet: ett
län som inte anger grund kan aldrig träffas av (c), hur omfattande maskningen än
är.

**Kriterium (b) är uppfyllt, och det var det jag först trodde var omöjligt.**
Sju län maskade klass A med stöd av 30 kap. 23 §: Gotland, Kronoberg, Värmland,
Västernorrland, Södermanland, Halland och Västra Götaland. Jämförelsemängden finns: **fem län har
minst ett helt omaskat A-dokument**, sammanlagt 17 dokument, nämligen Dalarna,
Gävleborg, Jämtland, Södermanland och Uppsala. Fem är fler än de tre kriteriet
kräver.

Uppgiftstypen tas ur myndigheternas egna ord. Kronoberg är den enda som namnger
den: *"uppgifter om enskilds affärs- och driftförhållanden maskerade, med hänsyn
till sekretess enligt 30 kap. 23 § OSL"*. För de övriga följer typen av den
bestämmelse de själva åberopat, eftersom 30 kap. 23 § skyddar just enskilds
affärs- eller driftförhållanden.

**Läsningen är grov, och det ska stå.** Uppgiftstyp tolkas här på
bestämmelsenivå. En striktare läsning på fältnivå, alltså exakt vilken uppgift
varje svärtning döljer, går inte att göra: i 124 av 294 dokument är texten under
rutan borttagen, och ADR-0017 slog fast att handlingarna är prosa utan
fältstruktur. Ett försök att härleda typen ur omgivande text övergavs sedan det
visat sig dra enskildas namn genom analysen.

**Följden för P8 är liten, eftersom not 4 är konjunktiv.** Skrivelse skickas bara
när ett kriterium är uppfyllt **och** myndigheten själv erbjudit ett
överklagbart beslut. **Fyra län**, sedan samtliga avhuggna citat lästs i fulltext 2026-08-21.
Gotland: *"Önskar du ett överklagningsbart beslut om detta så får du höra av
dig."* Kronoberg: *"Återkom till länsstyrelsen om du önskar att vi fattar ett
överklagbart beslut."* Halland: *"Är du inte nöjd med detta svar får du begära
ett överklagbart beslut av Länsstyrelsen i Halland."* Södermanland: *"Om ni
önskar ett formellt beslut med överklagandehänvisning vänligen kontakta
Länsstyrelsen."*

**Rättelse.** Den 20 augusti stod här att de avhuggna citaten inte kunde lägga
till något län, eftersom inget av dem innehöll ett erbjudande. Det påstods utan
att citaten lästs, och det var fel: två av dem, Halland och Södermanland,
innehåller var sitt uttryckligt erbjudande.

**Blekinge erbjuder också ett beslut**, i klass B och med den utförligaste
lydelsen av alla: *"Om du är missnöjd med att Länsstyrelsen inte lämnar ut
handlingarna i sin helhet kan du begära myndighetens prövning i frågan. Ändrar
inte Länsstyrelsen sin bedömning så får du då ett skriftligt, överklagbart
beslut med en överklagandehänvisning."* Blekinge faller ändå utanför, eftersom
inget P9-kriterium är uppfyllt: de anger ingen bestämmelse alls för sin maskning
i klass B, och kriterium (c) kräver uttryckligen 30 kap. 23 §. **Det är en
egenskap hos kriteriet värd att notera: ett län som maskar utan att ange grund
kan inte träffas av (c), hur omfattande maskningen än är.** Blekinge är det
enda län som maskat samtliga sina B-dokument.

**Slutsats: fem P8-skrivelser är utlösta, och femtaket i P9 binder nätt och
jämnt inte.** Västra Götaland tillkom när registret slöts den 22 augusti och
åberopar både bestämmelsen och erbjuder ett beslut ordagrant: *"Om du inte är
nöjd med detta besked så kan du återkomma och begära ett skriftligt
avslagsbeslut från Länsstyrelsen."* Kalmar tillkom den 22 augusti sedan dess följebrev lästs: myndigheten åberopar
OSL 30:23 och skriver *"Om du önskar ett överklagningsbart beslut så återkom
till oss."* **Sex skrivelser är utlösta och samtliga sex är avsända**, till
Gotland och Kronoberg den 21 augusti, Halland och Södermanland den 22 augusti,
Västra Götaland och Kalmar den 23 augusti. Kriterium (b) slår mot sex län, men bara de som själva erbjudit beslut
går vidare. Det är inte ett nollresultat, vilket jag först skrev, och inte
heller de tio överklaganden en läsning av enbart kriteriet skulle antyda.

**Lästa i fulltext 2026-08-21:** Södermanland A, Halland A, Västra Götaland B
och Blekinge B. Västra Götaland undanhåller två beslut helt med stöd av 18 kap.
1 och 3 §§ OSL och har dessutom tagit bort uppgifter *"enligt
dataskyddsförordningen"*, alltså inte med stöd av OSL. Samma mejl uppger ett
nämnartal som hör till P11: *"Totalt har 86 antal beslut/ föreläggande fattats
enligt 8 kap 9 § Djurskyddslagen under perioden 1 januari 2022 till och med 31
december 2025"*. Kvar oläst är endast Dalarna A, som inte gäller en
sekretessgrund utan beskedet att ingen kontrollrapport för gris påträffats.

---

## Gotland omprövar och lämnar ut mer, 2026-08-27

P8-skrivelsen till Gotland gick den 21 augusti. Svaret kom den 27 augusti från
myndighetens chefsjurist, och det är inte ett avslag utan en delvis ändrad
bedömning. Ordagrant: *"I denna prövning har jag beslutat att delvis ändra
tidigare bedömning."* En kontrollrapport, 5132-25, lämnas ut i sin helhet. Tre
andra maskas fortfarande med stöd av 30 kap. 23 § OSL, *"dock i mindre omfattning
än tidigare"*. Ett överklagbart beslut aviseras för de delar som fortfarande
maskas. 5027-2025 saknades i den första försändelsen och kom dagen efter, sedan chefsjuristen själv uppmärksammat att en rapport fallit bort; omprövningen omfattar därmed samtliga fem.

**En bilaga lämnas ut därför att den är ett beslut.** Ordagrant: *"Bilaga 3 till
kontrollrapport 5296-25 lämnas ut i sin helhet då den utgör ett beslut."* Det är
A/B-designens rättsliga tes, tillämpad av myndigheten själv och utan att någon
domstol behövt säga det: bilagepunkt 30 till 9 § OSF undantar beslut från
sekretessen, och KR Sundsvall 2682-21 fann att bilagor delar beslutets status.
Handlingen är ett föreläggande med vite enligt 8 kap. 9 § djurskyddslagen, och
den är levererad utan en enda maskning.

**Talen ligger utanför maskningsmåttet, med avsikt.** P8 föreskriver att
maskningsgraden mäts på den första leveransen, före skrivelsen, så att skrivelsen
inte kan påverka måttet. De omprövade handlingarna ligger därför i
`data/leveranser/gotland_X`, utanför klass A och B. Klass A stod oförändrad på
138 maskade av 155; efter rättelsen 2026-09-01 är samma tal 108 av 155, och
omprövningen ligger fortfarande utanför.

**Vad omprövningen ändrade, mätt.** Sidantalet är identiskt i alla fem
handlingarna, och antalet tecken i textlagret har stigit i var och en:

| Handling | Tecken före | Tecken efter | Ändring | Maskad yta före | Efter |
| --- | --- | --- | --- | --- | --- |
| 5027-2025 | 9 525 | 10 307 | +782 | 0,0514 | 0,0317 |
| 5132-2025 | 5 838 | 6 511 | +673 | 0,0438 | 0,0094 |
| 5215-2025 | 7 211 | 9 067 | +1 856 | 0,1287 | 0,0569 |
| 5238-2025 | 6 244 | 7 973 | +1 729 | 0,0335 | 0,0806 |
| 5296-2025 | 5 891 | 7 812 | +1 921 | 0,0043 | 0,1444 |

**Och det ger en metodisk lärdom som väger tyngre än talen.** Mer text har
lämnats ut i samtliga fem, mellan 8 och 33 procent fler tecken. Den maskade
ytan sjunker ändå bara i tre av dem och stiger i två. Gotlands maskning har
sorten `text_removed`, alltså att texten under svärtningen är borttagen, och då
mäter ytmåttet hur rutorna ritats och inte hur mycket som hålls inne. **För den
maskningstekniken är antalet tecken det bättre måttet, och ytmåttet kan peka åt
fel håll.** Det gäller det förregistrerade ytmåttet i P1 och ska stå som en
gräns när ytsiffror används. Ingen siffra räknas om här: omprövningen ligger
utanför måttets population, och lärdomen gäller tolkningen.

---

## Det första överklagbara beslutet, Kalmar 2026-08-25

Länsstyrelsen i Kalmar avslår begäran om de maskade uppgifterna i de fem
kontrollrapporterna, dnr 6666-2026, beslutat av en enhetschef med en
djurskyddshandläggare som föredragande. **Deras namn står i beslutet men
inte här.** Projektets subjekt är myndigheten, rollnivån bär det som mäts,
att beslutet fattades på enhetschefsnivå, och beslutet självt ligger kvar
med sin kontrollsumma. Utelämnandet är alltså deklarerat och inte tyst. Skickat som elektronisk
delgivning 2026-08-25 kl. 13:46 med begäran om mottagningsbekräftelse. Det är
svaret på P8-skrivelsen den 23 augusti kl. 22:00, alltså två dagar. Registrerat
i `data/beslut.jsonl`.

**Grunderna anges, till skillnad från i följebreven.** Ordagrant: *"30 kap. 23 §
offentlighets- och sekretesslagen (2009:400), 9 § offentlighets- och
sekretessförordningen (2009:641) samt punkten 30 i bilagan till förordningen"*.
Kriterium (a) i P9 är därmed inte uppfyllt.

**Uppgiftstypen namnges.** Ordagrant: *"Av begärda handlingar framgår uppgifter
om verksamheternas djurhållning och bedömda brister i dessa. Uppgifterna rör
därmed den enskildes affärs- och driftförhållanden."* Det är vad tillämpningsnot
6 kräver för att kriterium (b) ska kunna drivas: beslutet självt måste namnge den
maskerade uppgiftstypen, annars redovisas saken som en gräns i mätningen.

**Kriterium (b) är uppfyllt.** Maskningen är i klass A med stöd av 30 kap. 23 §,
och jämförelsemängden är de fem län som lämnat ut klass A helt omaskad, Dalarna,
Gävleborg, Jämtland, Södermanland och Uppsala, alltså fler än de tre som
kriteriet kräver. De handlingarna är kontrollrapporter i samma handlingsklass och
innehåller därmed både djurhållning och konstaterade brister, de uppgiftstyper
beslutet namnger. Detta är det första beslutet, så femtaket är inte i spel.

**Beslutet medger att prövningen inte är gjord uppgift för uppgift.** Ordagrant:
*"Länsstyrelsen bedömer att de maskerade uppgifterna i handlingen till
övervägande del är av sådan karaktär att det kan antas att den enskilde lider
skada om uppgifterna lämnas ut."* Skaderekvisitet i 30 kap. 23 § är rakt, alltså
med presumtion för offentlighet, och gäller varje uppgift. En bedömning som
stannar vid *"till övervägande del"* säger att en del av det maskerade inte bär
rekvisitet. Formuleringen är myndighetens egen och citeras oförändrad; vad den
innebär rättsligt är en fråga för ett överklagande, inte för den här filen.

**Besvärshänvisningen anger fel instans.** Beslutet skriver *"Om du inte är nöjd
med Länsstyrelsens beslut, kan du skriftligen överklaga beslutet hos
förvaltningsrätten."* P9, skrivet före insamlingen, anger kammarrätten, vilket
följer av 6 kap. 8 § OSL och av att KR Sundsvall 2682-21 är ett kammarrättsmål.
Skillnaden redovisas som den står och förs inte samman till ett påstående om vem
som har rätt; vilken domstol ett beslut pekar ut är i sig en mätpunkt i
öppenhetslagret.

**Ärendebeskrivningens datum stämmer inte med brevlådan.** Beslutet skriver att
begäran inkom den 4 augusti 2026 och begränsades till fem rapporter den 13
augusti. Loggen och brevlådan visar begäran 2026-08-03 kl. 10:00 och
begränsningen till fem 2026-08-04 kl. 12:36; den 13 augusti upprepades att
begäran varit begränsad sedan den 4 augusti, tillsammans med frågan om
elektroniskt utlämnande. Båda avvikelserna förskjuter ärendet framåt i tiden och
berör T1 i P1.

**Frister.** Delfående 2026-08-25. P9 sätter 14 kalenderdagar, alltså
2026-09-08. Lagens frist är tre veckor enligt 44 § förvaltningslagen, alltså
2026-09-15. `src/open_items.py` räknar den första och visar begäran under KRÄVER
DIG till dess att ett överklagande eller ett avstående loggats.

---

## Begäran C: dimensionen oanmäld mot föranmäld, levererad per län

Levererad 2026-08-21 kl. 09:29 via filöverföringslänk, **336 rapporter**, en per
län, djurslag, år och aviseringsstatus. Parsad av `pipeline/27_parse_announced.py`
till `data/foranmalda.jsonl`. Detta är den dimension myndigheten den 12 augusti
uppgav *"går dessvärre inte att få ut med rutinbetonade åtgärder per län utan
endast per år för hela landet"*, och den kom dagen efter att begäran upprepats,
trots beskedet att arbetet skulle ta flera dagar.

**Formatet begränsar vad dimensionen kan bära.** Varje rapport anger
Kontrolltypgrupp *"Alla kontrolltypgrupper"*, alltså ingen korsning med
kontrolltyp eller med brist. Avsnitt 10 prövar hypotesen på två sätt, och bara
det första blir möjligt: sambandet mellan andelen oanmälda och andelen med brist
över länen. Skillnaden i bristandel mellan oanmälda och föranmälda **inom** samma
län, djurslag och kontrolltyp går inte att räkna, och det ska stå som en gräns i
redovisningen.

**Tre källor, och de säger inte samma sak.**

| Checklista och år | 336 rapporter | Excel v2, rader | Mejl 14 och 17 aug |
| --- | --- | --- | --- |
| Nötkreatur 2025 | 2 768 | 2 916 | 2 768 |
| Gris 2025 | 269 | 288 | 269 |
| Värphöns 2025 | 52 | 55 | 52 |
| Slaktkyckling 2025 | 19 | 26 | 19 |
| Nötkreatur 2024 | 2 302 | 2 451 | 2 302 |
| Gris 2024 | 249 | 241 | 222 |
| Värphöns 2024 | 61 | 43 | 42 |
| Slaktkyckling 2024 | 27 | 30 | 27 |

**Rapporterna och mejlen är samma fråga mot registret.** De stämmer exakt i sex
av åtta celler, vilket är kontrollen på att skörden är komplett och att inget
län fallit bort.

**Rättelse 2026-08-24: risk 2 var inte bekräftad.** Här stod tidigare att
förregistreringens risk 2, ett inkonsekvent ifyllt aviseringsfält, var bekräftad,
och skillnaden mellan radantalet och summan av aviserade och oaviserade angavs
som belägg. Myndigheten har därefter uppgett en annan förklaring till samma
skillnad, och den förklaringen gäller filens uppbyggnad: en kontroll med två
djurhållare blir två rader. Överskottet är alltså dubbletter i excelfilen, inte
kontroller som fallit ur både JA och NEJ. Talen står kvar som mätning: summan
ligger under radantalet i sex celler, för nötkreatur med 148 rader 2025 och 149
rader 2024, omkring 5 till 6 procent, och för slaktkyckling 2025 med 7 av 26,
alltså 27 procent. Vad de mäter är antalet extra djurhållare. Risk 2 är därmed
varken bekräftad eller utesluten, och den går inte att pröva mot det här
materialet.

**Nämnaren är fortfarande summan av aviserade och oaviserade**, men av ett annat
skäl än det som stod här: radantalet är inte ett antal kontroller, och var därför
aldrig en giltig nämnare.

**Rättelse 2026-08-25: excelbladen är inte ofullständiga, avvikelsen sitter i
rapporterna.** Här stod att bladen Gris 2024 och >350 värphöns 2024 sannolikt
saknade kontroller, med de 336 rapporterna som måttstock. Jämförelsen gjordes mot
fel källa. Ställd mot myndighetens egna nationella tal i mejlen den 14 och 17
augusti ligger excelfilen **över i samtliga åtta celler**, från +1 till +149,
vilket är precis vad en rad per djurhållare förutsäger. Inget blad går åt andra
hållet.

| Djurslag och år | Mejlen | Excel, rader | Diff | 336 rapporter |
| --- | --- | --- | --- | --- |
| Nötkreatur 2024 | 2 302 | 2 451 | +149 | 2 302 |
| Nötkreatur 2025 | 2 768 | 2 916 | +148 | 2 768 |
| Gris 2024 | 222 | 241 | +19 | **249** |
| Gris 2025 | 269 | 288 | +19 | 269 |
| Värphöns 2024 | 42 | 43 | +1 | **61** |
| Värphöns 2025 | 52 | 55 | +3 | 52 |
| Slaktkyckling 2024 | 27 | 30 | +3 | 27 |
| Slaktkyckling 2025 | 19 | 26 | +7 | 19 |

**Det är i stället två av rapporterna som avviker, och båda i det oaviserade
talet.** Rapporterna stämmer mot mejlen i sex av åtta celler. Gris 2024 ger 114
oaviserade mot mejlens 87, och värphöns 2024 ger 30 mot 11.

**Värphöns 2024 går att spåra till en enda rapport.** Filen
`AC_2024_Vhöns_oanmälda.skv` anger 19 oaviserade kontroller för Västerbotten, ett
tal som ensamt överstiger mejlets nationella 11 och som saknar motsvarighet i
radnivåuttaget, där länet har en enda rad för djurslaget och året. Utan den
rapporten summerar de övriga till 11, alltså exakt mejlets tal.

**Gris 2024 bär ett dokumenterbart fel och en oförklarad rest.** Filen
`K_2024_oanmalda_gris.skv` innehåller `Länsbokstav;W`, och dess innehåll är
identiskt med `W_2024_oanmalda_gris.skv`. Dalarna räknas därmed två gånger och
Blekinges tal saknas helt i leveransen, vilket förklarar 4 av de 27. Resterande
23 är oförklarade. Filantalet stämmer, 336, så felet syns bara i innehållet:
läst per länsbokstav har K femton rapporter och W sjutton.

Detta är slutsatser av jämförelsen mellan källorna och inte besked från
myndigheten.

---

## Begäran C: vad en rad i uttaget är, besked 2026-08-24

**En rad är en djurhållare vid en kontroll, inte en kontroll.** Frågorna om de
två avvikelserna ställdes 2026-08-22 kl. 09:21 och besvarades 2026-08-24 kl.
09:09. Myndigheten skriver ordagrant: *"Anledningen till att det skiljer sig är
att i den sammanställda Excelfilen du fick del av först kan det finnas dubbletter
eftersom i de fall det är fler än en djurhållare på kontrollplatsen så blir varje
djurhållare en egen rad (dvs. en kontroll där det finns två djurhållare blir två
rader i Excelfilen). Vi glömde informera dig om det, så det var bra att du
uppmärksammade det."*

**Dubbletterna går inte att hitta.** Uttaget har fyra kolumner, LÄN,
KONTROLLTYP, CHECKLISTA och FINNS_BRISTER, och ingen identifierare, inget datum
och ingen plats. Två rader från samma kontroll är därmed inte skiljbara från två
rader från två kontroller, och raderna går inte att lägga ihop till kontroller.
Steg 22 räknar alltså djurhållarrader, vilket är varför fältet i
`data/bristandel.jsonl` heter `rader` och inte `kontroller`.

**Vad det gör med måtten.** Andelen med brist över raderna är lika med andelen
över kontrollerna endast där dubblerade djurhållare bär samma bristmarkering, och
hur ofta de gör det går inte att mäta ur filen. Spridningen mellan länen
förskjuts bara om dubblettfrekvensen skiljer sig mellan län. Prövningen i steg 28
jämför rangordningar och tål därför en konstant dubblettfrekvens, men inte en som
varierar. Ingen av de publicerade siffrorna ändras av beskedet; det är enheten de
uttrycks i som ändras, från kontroller till djurhållarrader.

**Rapporternas tal heter något annat än kontroller.** Varje rapport bär ett enda
tal, och etiketten i filen är *"Antal gånger checklista använd"*. Om en
checklistanvändning är detsamma som en kontroll står ingenstans i leveransen, och
frågan är ställd till myndigheten. Indicierna talar för att de följs åt:
radnivåuttaget bär en rad per djurhållare, och om en checklista användes en gång
per djurhållare skulle de två källorna stämma överens i stället för att uttaget
ligger 5 till 6 procent högre. Det är ett argument och inte ett besked, så fältet
i `data/foranmalda.jsonl` heter `anvandningar` tills det finns ett.

**Uttaget svarar därmed inte på begäran som den är formulerad.** Begäran C i
avsnitt 4 av `docs/BEGARANMALL.md` gäller *"antal genomförda fysiska kontroller
per länsstyrelse, år och djurslag"*. Excelfilen ger antal djurhållare vid
kontroller. De 336 rapporterna räknar däremot kontroller, vilket är varför de två
källorna skiljer sig åt.

**Beskedet besvarar ingen av de två frågorna, men täcker riktningen i den ena.**
Fråga 2 gällde om aviseringsfältet saknas för en del kontroller. Förklaringen om
flera djurhållare gäller den riktningen, men säger bara att skillnaden inte
behöver bero på tomma aviseringsfält, inte att fältet är fullständigt ifyllt.
Fråga 1 gällde de två blad där rapporterna anger fler kontroller än bladet har
rader, alltså den motsatta riktningen, och den frågan är obesvarad.

---

## Djurslagsregeln prövad mot handläsning, 2026-08-25

Steg 20 säger om sig självt att termräkningen är en baslinje och inte en
klassificerare, och att den måste kontrolleras mot handlästa dokument innan
någon djurslagsuppdelad siffra publiceras. Steg 30 drar den kontrollen: tre
dokument ur var och en av regelns fyra utfallsklasser, sorterade på sökväg, utan
att läsaren ser vad regeln svarat eller vilken klass dokumentet kom ur. Frö
20260825, därefter sex nötdokument till med frö 20260826 av skäl som står nedan.
Sammanlagt 18 handlästa dokument.

**Regeln gjorde inget fel i något av de arton dokumenten.**

| Fråga | Utfall |
| --- | --- |
| Namngav regeln fel art? | **0 av 11** dokument där läsaren namngav en art |
| En art, sedd som en art | **15 av 15** |
| Flera arter, sedda som flera | **3 av 3** |

**Rättelse 2026-08-25 av den första redovisningen.** Här stod först att regeln
såg blandbesättningar i endast 3 av 6 fall, och att tre dokument var missar. Det
var fel, och felet satt i läsformuläret och inte i regeln: svarsordet *flera* var
tillåtet utan att läsaren behövde skriva vilka djur, och fyra av de sju
blandbesättningarna visade sig blanda med djurslag projektet inte mäter. Steg 30
avvisar numera ett flera-svar som inte namnger djuren.

**Fyra blandningar ligger utanför de tre djurslagen.** Ett gävleborgsdokument
gäller fjäderfä och häst, ett uppsaladokument gris tillsammans med kanin, häst
och får, ett västerbottendokument fjäderfä inklusive gås tillsammans med häst,
och ett västernorrlandsdokument nöt och får. Steg 20 har inget mönster för häst,
får, get eller kanin och skulle inte kunna se ett. Inom de tre djurslag projektet
jämför håller var och en av anläggningarna ett djurslag, och regeln namngav det
rätta i samtliga fyra.

**De tre äkta blandningarna fångades allihop.** Två hallandsdokument med nöt och
gris, och ett värmlandsdokument med nöt tillsammans med höns, ankor och tuppar.
I alla tre registrerade regeln båda djurslagen och avstod från att utse ett
dominerande.

**Klassen `ingen` är alltså inget fel utan regeln som fungerar.** Namnet är
missvisande: `ingen` betyder inget dominerande djurslag, inte inget djurslag.

**Stickprovet drogs ur 293 dokument och dras inte om.** Ett södermanlandsdokument
som kom in den 17 augusti saknades i steg 20 när dragningen gjordes, och kom in
först när steget kördes om 2026-08-26; populationen är därefter 294 och
fjäderfäklassen 42 i stället för 41. Dokumentet var alltså inte valbart. Att dra
om stickprovet med det inlagt vore att ändra ett stickprov efter att svaren är
kända, vilket är en större skada än den kända gränsen att ett av 294 dokument
inte kunde dras.

**Nöt bär populationen och är rätt i alla nio.** Nöt är 190 av 293 dokument.
Efter utökningen vilar klassen på nio handlästa i stället för tre. Utökningen
gjordes efter att de första tolv besvarats, med skälet att klassen var
underdimensionerad och som enda klass saknade avvikelser; de första tolv lämnades
orörda och inget dokument ströks.

**En begränsning som handläsningen avslöjade, och som ingen letade efter.** I
gävleborgsdokumentet fanns ingen anmärkning på de 60 fåglarna; bristerna gällde
hästutrymmena. Fältet `FINNS_BRISTER` sitter på kontrollen och inte på
djurslaget, så en djurslagsuppdelad bristandel kan skriva en hästbrist på
fjäderfäkontot. Det gäller både radnivåuttaget i begäran C och varje uppdelning
byggd på steg 20, och det går inte att åtgärda ur materialet. Redovisas som
gräns.

**Två observationer ur läsningen som inte bär någon slutsats.** Uppsaladokumentet
gäller en 4H-gård med små bestånd, alltså inte produktionsdjurhållning, och i
värmlandsdokumentet förefaller antalet getter vara maskat i en handling som i
övrigt är hårt maskad.

**Följden.** Tilldelningen till djurslag håller, och djurslagsuppdelade siffror
får publiceras. Kvar står att bristmarkeringen inte är djurslagsuppdelad, och det
är en annan sak än att djurslaget skulle vara fel.

---

## Kontroll 2 körd, och de sju undantagen handlästa, 2026-09-04

Kontroll 2 i `docs/VILLKORSSCHEMA.md` avsnitt 5 lyder att "noll villkor är bara
tillåtet för förlängningar, igångsättningsbeslut, upphävanden och domar. Ett
tillstånd med noll villkor är per definition en tyst trasig extraktion." Den har
inte kunnat köras tidigare, eftersom typen per beslut saknades. Steg 32 kör den
mot steg 31:s typer.

**Täckningstalet 73 procent var sant och oanvändbart.** Steg 24 rapporterar att
173 av 236 filer gick att segmentera. Uppdelat på typ säger materialet något
annat:

| Typ | Med villkor | Utan | Totalt | Noll tillåtet |
| --- | --- | --- | --- | --- |
| tillstånd | 155 | 7 | 162 | nej |
| ändring | 8 | 32 | 40 | nej |
| förlängning | 0 | 15 | 15 | ja |
| dom | 10 | 4 | 14 | ja |
| villkor | 0 | 2 | 2 | nej |
| igångsättning | 0 | 2 | 2 | ja |
| upphävande | 0 | 1 | 1 | ja |

**Förlängningarna bekräftar dokumentets egen förutsägelse exakt.** Noll av
femton bär villkor, vilket är vad VILLKORSSCHEMA säger att en förlängning ska
göra och vad Lidfarmbeslutet visar. I det poolade täckningstalet räknades de
femton som misslyckanden.

### De sju tillstånden utan villkor, ett i taget

Samtliga sju är öppnade och lästa. Två av dem har rätt i att sakna villkor.

**Två där noll är riktigt.** `fccfef166252` är rubricerat "Förlängning av
igångsättningstid" i sin egen text och skriver att det inte finns behov av nya
eller strängare villkor; utgivarens länktext kallar det ändå "Tillstånd", så
etiketten är fel och extraktionen rätt. `e181f70f9cda` är ett beslut som ändrar
enskilda villkor, med raderna "Villkor 6 ändras till följande lydelse:" och
"Villkor 7 ändras till följande lydelse:", alltså ingen serie 1..N att
segmentera.

**Fem segmenteringsmissar, fyra av dem med samma orsak.** Segmenteraren letar
efter en rubrikrad som består av ordet villkor och ingenting annat. I
`686fac957352`, `85f59705885d`, `876e9df5fd03` och `aee6ec54ed25` införs
villkoren av en mening i stället. Alla fyra bär den ordagrant likadant: "För
tillståndet gäller följande villkor: 1. Om inte annat framgår av övriga villkor
eller föreskrifter ska verksamheten i huvudsak bedrivas ...". Alla fyra är
OCR-lästa, och raden bär både inledningen och det första villkoret.

Den femte, `361be3bd133c`, är digitalt född och har rubriken kvar, men
textlagret klistrar ihop den med nästa mening: "Villkor för
verksamhetenMiljöprövningsdelegationen fastställer med stöd av". En rubrikrad
som inte är en egen rad matchar inte heller.

**Vad en rättelse skulle ge, mätt utan att röra måttet.** Två kandidatregler är
prövade mot de sju i en fristående körning. En regel som känner igen den
inledande meningen hittar avsnittets början i fyra av dem. En regel som matchar
rubriken som radprefix i stället för som hel rad hittar den i den femte,
`361be3bd133c`. Tillsammans når de alla fem som saknar villkor av
segmenteringsskäl.

Vad körningen visar är att avsnittets början går att hitta. Om villkoren därefter
segmenterar till en obruten serie är inte prövat, och det avgörs först av en
körning över hela materialet. Ingen ändring är gjord i
`data/villkor_baseline.jsonl`, eftersom en ny segmentering flyttar
återanvändningsmåttet och permutationstestet, och de talen är publicerade.

### Två frågor kontrollen inte svarar på

**Trettiotvå av fyrtio ändringsbeslut saknar villkor.** Regeln uttalar sig inte
om ändringar. Om ett ändringsbeslut bär egna villkor eller bara ändrar ett
villkor i det underliggande tillståndet är en fråga om dokumenten, och att
avgöra den ur frånvaron av en rubrik vore en gissning. `e181f70f9cda` ovan visar
att den andra formen finns.

**Två beslut heter "Villkor" respektive "Slutliga villkor" och saknar villkor.**
Namnet gör dem till de sista man väntar sig hitta tomma. De är inte lästa än.

---

## Tillståndskorpusens typfördelning, verifierad 2026-09-04

Kontroll 2 i `docs/VILLKORSSCHEMA.md` kräver att korpusen delas upp på
beslutstyp och anger den väntade fördelningen som "länktexternas cirka
160/38/15/14". Talet stod i prosa och fanns ingenstans i repot: manifestet från
steg 23 bär identifierare, prövningsgrupp, storlek och kontrollsumma, men ingen
typ. Steg 31 hämtar typen där dokumentet självt anger den, i länktexten på
Jordbruksverkets sida, enligt samma princip som ADR-0007 tillämpar på bilagor.

**Sidan och skörden stämmer exakt.** 236 beslut ligger på sidan och 236 finns i
manifestet, identifierarna är desamma i båda, och ingenting har tillkommit eller
försvunnit sedan hämtningen den 17 augusti 2026. Sidan listar 237 länkar,
eftersom ett beslut förekommer två gånger under samma adress, vilket steg 23
redan noterat.

**Fjorton skrivningar, sju sorters beslut.**

| Typ | Antal | Dokumenterat |
| --- | --- | --- |
| tillstånd | 162 | cirka 160 |
| ändring | 40 | cirka 38 |
| förlängning | 15 | 15 |
| dom | 14 | 14 |
| villkor | 2 | inte räknat |
| igångsättning | 2 | inte räknat |
| upphävande | 1 | inte räknat |

Samtliga fyra dokumenterade tal håller, två av dem exakt. Skillnaderna på
tillstånd och ändring beror på var gränsfallen läggs: en länk heter "Tillstånd
samt återkallelse av del av tidigare tillstånd" och räknas som tillstånd, och
fyra skrivningar utöver "Ändringstillstånd" betecknar ändringar, däribland en
som delas av ett mjukt bindestreck och en som heter "Ändringsbeslut".

**Tre typer som dokumentet inte räknade.** Två beslut om igångsättning, ett om
upphävande av del av tillstånd och två som bara heter "Villkor" respektive
"Slutliga villkor". Avsnitt 5 i VILLKORSSCHEMA nämner igångsättningsbeslut och
upphävanden bland de typer som får sakna villkor, men räknar dem inte, och de
två villkorsbesluten nämns inte alls. De är nu utskrivna, så att populationen
är fullständigt deklarerad innan villkorsregistret byggs ovanpå den.

**Vad steget inte gör.** Det säger ingenting om vad som står i dokumenten. Typen
är utgivarens ord om handlingen, och den finns här för att kontroll 2 ska kunna
köras och för att en textklassificerare senare ska ha ett oberoende facit att
prövas mot.

**En gräns som är värd att skriva ut.** Steget läser en levande sida vid varje
körning, och korpusen växer när nya beslut publiceras. En avvikelse mot talen
ovan är därför ett fynd om källan och inte ett trasigt test. Rätt åtgärd är att
läsa de nya dokumenten och flytta talet, aldrig att vidga påståendet.

---

## HFD-praxis som Kronoberg åberopar, prövad 2026-09-04

Länsstyrelsen i Kronobergs beslut den 31 augusti 2026 åberopar fem avgöranden
från Högsta förvaltningsdomstolen. Avsnitt 11 i `docs/BEGARANMALL.md` skriver
att inget sådant avgörande finns. Påståendet måste prövas innan det upprepas,
och innan beslutet om överklagande fattas den 14 september.

**Ett av de fem är läst i primärtext, fyra i referat.** RÅ 2010 ref. 77 är hämtad
i fulltext från lagen.nu och läst i sin helhet. RÅ 1994 not. 506, RÅ 1994 not.
624, RÅ 2005 ref. 87 och RÅ 2007 ref. 45 är lästa genom ett sammanfattande
verktyg, alltså i referat. Skillnaden står här därför att projektets regel är
citat, aldrig karaktärisering, och ett referat är en karaktärisering.

| Avgörande | Bestämmelse | Vem begärde | Uppgift | Utfall |
| --- | --- | --- | --- | --- |
| RÅ 1994 not. 506 | 8 kap. 6 § p. 1 sekretesslagen | miljönämnden i Falu kommun | djursammansättning, antal djur, spridningsareal ur lantbruksregistret | ej utlämnat |
| RÅ 1994 not. 624 | 8 kap. 6 § p. 1 sekretesslagen | miljönämnden i Lunds kommun | samma tre uppgifter | ej utlämnat |
| RÅ 2005 ref. 87 | 8 kap. 6 § första stycket 1 | enskild, av Jordbruksverket | försöksdata om GMO | delvis utlämnat |
| RÅ 2007 ref. 45 | 8 kap. 6 § andra stycket | enskild, av Jordbruksverket | försöksdata om GMO | ej utlämnat |
| RÅ 2010 ref. 77 | 30 kap. 23 § första stycket 1 OSL | miljöinspektör i Aneby kommun | vilka djur som är registrerade på en viss produktionsplats | ej utlämnat |

### RÅ 2010 ref. 77, läst i fulltext

Målnummer 1653-10, avgjort 2010-10-19 av Regeringsrätten. Rubriken lyder:
"En miljöinspektör i en kommun har ansetts inte ha rätt att ta del av uppgifter
från det centrala nötkreaturregistret (CDB) hos Jordbruksverket om vilka djur
som är registrerade på en viss produktionsplats."

Domskälen ordagrant i den del som bär avgörandet: "Eftersom dessa uppgifter
behandlar enskilds affärs- och driftsförhållanden samt används bl.a. för
kontroll av stöd kan den enskilde lida skada om uppgifterna lämnas ut.
Regeringsrätten finner i likhet med underinstanserna att sekretess gäller för
dessa uppgifter enligt 30 kap. 23 § första stycket 1 OSL och 9 § första stycket
1 OSF (jfr t.ex. RÅ 1994 not. 506 och RÅ 1994 not. 624)." Om undantaget för
allmänintresse: "Enligt Regeringsrättens bedömning är de begärda uppgifterna
inte av den karaktären att intresset av allmän kännedom har sådan vikt att
sekretessen inte ska gälla."

**Rättelse av en första läsning samma dag.** Här stod först, i ett svar till
Martin, att fyra av de fem avgörandena gäller en myndighet som begär uppgifter
av en annan, och att de därför prövas mot generalklausulen snarare än mot en
enskilds rätt. För RÅ 2010 ref. 77 är det fel. Målet är ett utlämnandemål: begäran
avslogs av Jordbruksverket, överklagades till kammarrätt och därefter till
Regeringsrätten, och prövades mot skaderekvisitet i 30 kap. 23 § första stycket
1 och mot den sekretessbrytande regeln i punkt 107. Att R.E. begärde uppgifterna
i egenskap av miljöinspektör vägde in i intresseavvägningen, inte i valet av
rättslig ram. Den procedurella vägen är alltså densamma som projektets egen.

### Vad avgörandet gör med avsnitt 11

**Påståendet står i sin egen mening och faller utanför den.** Meningen "Inget
avgörande från Högsta förvaltningsdomstolen finns" avslutar genomgången av
kammarrättspraxis om kontrollrapport som bilaga till beslut, alltså A/B-frågan.
Inget av de fem avgörandena rör den frågan, så påståendet är riktigt i sitt
sammanhang. Men det har i projektet lästs bredare än så, som att ingen
HFD-praxis alls finns om maskning av uppgifter om djurhållning, och den
läsningen är fel: RÅ 2010 ref. 77 tillämpar exakt den bestämmelse projektet
mäter mot på exakt den sortens uppgift.

### Vad avgörandet gör med P9 (b) för Kronoberg

Kronoberg namnger uppgiftstypen: "Länsstyrelsen har maskerat uppgifter om
djurbesättningens storlek och vissa uppgifter om de brister som framkom vid
kontrolltillfällena." Det är två uppgiftstyper, och de står olika starkt.

**Djurbesättningens storlek ligger nära det RÅ 2010 ref. 77 höll hemligt.**
Inte identiskt: avgörandet gäller vilka djur som är registrerade i CDB, alltså
en registerförteckning, medan Kronoberg maskat ett antal i en kontrollrapport.
Men en kammarrätt skulle behöva skilja dem åt, och det är den svåra riktningen.

**Bristuppgifterna ligger inte nära.** Skadebedömningen i RÅ 2010 ref. 77 vilar
uttryckligen på att CDB-uppgifterna används för kontroll av stöd, alltså att ett
utlämnande kan leda till avdrag på lantbrukarens stöd. En kontrollrapport från
djurskyddstillsyn är inte det registret. Den skiljaktige i kammarrätten skrev
dessutom om just bristuppgifter: "uppgifterna, som anknyter till iakttagna
missförhållanden vid den aktuella djurhållningen, till sin natur är sådana att
det finns ett allmänt intresse av att uppgifterna lämnas ut."

**Föreskriften är en annan punkt i samma bilaga.** RÅ 2010 ref. 77 gäller
punkt 107, Jordbruksverkets tillsyn. Kronobergs beslut åberopar punkt 30,
"utredning, tillståndsgivning och tillsyn enligt lagstiftningen om djurskydd",
som till skillnad från punkt 107 bär den uttryckliga begränsningen "sekretessen
gäller inte beslut i ärenden". Avgörandet säger ingenting om punkt 30 och
ingenting om A/B-designens tes.

**Domstolen är densamma.** Kronobergs län ligger i Kammarrätten i Jönköpings
domkrets, samma domstol som redan har Kalmaröverklagandet som mål 3249-26 och
som får Jordbruksverkets. Det är också den kammarrätt vars dom i 2010 års mål
Regeringsrätten fastställde. Domkretsen är kontrollerad mot två andrahandskällor
som är eniga om Kronoberg, inte mot domstolens egen förteckning, som inte gick
att nå; att Kalmar ligger i samma domkrets är däremot bekräftat av att
Kalmaröverklagandet togs upp där.

### Vad som återstår att kontrollera

De två notiserna från 1994 är inte lästa i fulltext. De är det underlag
Regeringsrätten själv hänvisar till, och om de visar sig gälla uppgiftslämnande
mellan myndigheter enligt generalklausulen bär de mindre mot en enskilds
begäran än vad hänvisningen antyder. Slutsatserna ovan vilar inte på dem.

---

## Den förregistrerade oanmäld-hypotesen, prövad 2026-08-21

Avsnitt 10 i `docs/BEGARANMALL.md`, tidsstämplat innan någon begäran skickades:
oanmälda kontroller ger oftare konstaterade brister än föranmälda, och andelen
oanmälda förklarar en del av spridningen mellan länen. Prövad med
`pipeline/28_unannounced_hypothesis.py` sedan de 336 rapporterna gjort andelen
oanmälda tillgänglig per län.

**Halva den förregistrerade prövningen går inte att göra.** Avsnitt 10 begär
både sambandet över länen och skillnaden i bristandel mellan oanmälda och
föranmälda **inom** samma län, djurslag och kontrolltyp. Den andra kräver att
aviseringsfältet är korsat med bristfältet, och de 336 rapporterna avser alla
"Alla kontrolltypgrupper". Den delen är alltså inte svag, den saknas, och
ingenting sätts i dess ställe.

**Bara nötkreatur bär prövningen.** Gris, värphöns och slaktkyckling har för få
län som når tjugo kontroller i båda måtten.

| Djurslag | År | Kategori | Län | Spearman rho | p, permutation |
| --- | --- | --- | --- | --- | --- |
| nötkreatur | 2024 | rutin | 20 | 0,009 | 0,4755 |
| nötkreatur | 2024 | alla kontrolltyper | 21 | 0,314 | 0,0840 |
| nötkreatur | 2025 | rutin | 19 | 0,344 | 0,0755 |
| nötkreatur | 2025 | alla kontrolltyper | 21 | 0,514 | 0,0080 |

**Läsningen, och den går åt hypotesens nackdel.** Det enda sambandet som når
signifikans ligger i måttet över alla kontrolltyper, och det är just det måttet
steg 22 undviker: fem kontrolltyper bär utfallet i sitt eget namn, till exempel
"Klagomål, offentlig kontroll med brister", och bristflaggan sammanfaller med
typnamnet i 96 till 100 procent av de raderna. Ett län med fler klagomålsdrivna
kontroller får därför både högre bristandel och fler oanmälda kontroller utan
att hypotesen behöver vara sann. Det är konkurrerande förklaring 2 i
förregistreringen, kontrolltypsmix, och den kan producera exakt det observerade
sambandet mekaniskt.

**I det rena måttet, rutinkontroller, finns inget stöd.** 2024 ger rho 0,009,
alltså ingenting. 2025 ger 0,344 med p = 0,0755, alltså positivt men inte
signifikant. De två åren är dessutom inte förenliga med varandra, vilket i sig
talar mot ett stabilt samband.

**Nollresultatet ska inte överdrivas heller.** Nitton till tjugoen län är ett
litet underlag, och 0,344 är inte samma sak som noll. Det korrekta beskedet är
att prövningen inte kan skilja ett svagt positivt samband från inget samband,
inte att sambandet är motbevisat.

**Den förskrivna nollresultatstexten går inte att använda ordagrant.** Avsnitt
10 skrev före datainsamlingen att *"skillnaden i bristandel mellan oanmälda och
föranmälda kontroller är liten eller obefintlig inom län, djurslag och
kontrolltyp"*. Den satsen påstår resultatet av just den prövning som visade sig
omöjlig, och den måste strykas ur den publicerade texten i stället för att
återges. Det är en brist i förregistreringen: den förutsatte att den korstabell
som begärdes också skulle levereras.
