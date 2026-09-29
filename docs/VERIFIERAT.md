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
födda; talet 155 är alltså ett annat än klass A:s 155. *Tillägg 2026-09-28: de
digitalt födda är nu 283, sedan Kalmars fem förelägganden och sjutton beslut,
avgiftshandlingar och domstolsmeddelanden arkiverats. Steg 26 är omkört över
alla 283: 236 dolda tecken i 42 handlingar, precis som förut, noll av dem i
brödtext och noll bakom en ljus täckning.*

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

**Tillägg 2026-09-28: talen ovan är inaktuella, och klass B rör sig.** Fem
förelägganden från Länsstyrelsen i Kalmar län lämnades ut den 13 augusti 2026
och upptäcktes den 28 september; leveransen hade aldrig loggats eller
arkiverats. Samtliga fem är digitalt födda och bedöms som maskade med sorten
`text_removed`. Populationen växer från 290 till 295 handlingar och de nya
talen är:

| Klass | Digitalt födda | Skannade | Totalt |
| --- | --- | --- | --- |
| A | 78 av 125, 62 % | 30 av 30, 100 % | 108 av 155, 70 % |
| B | 23 av 125, 18 % | 11 av 15, 73 % | **34 av 140, 24 %** |

Klass A är oförändrad. Kontrasten mellan klasserna kvarstår och byter inte
tecken; den smalnar från 70 mot 21 till 70 mot 24 procentenheter. Att just
Kalmar saknades är det som gör felet allvarligt: länets fem kontrollrapporter i
klass A är maskade och beslutet om dem är överklagat som mål 3249-26, så länet
bär A/B-kontrasten och stod utanför den.

**Tillägg 2026-09-29: klass A rör sig, och en del av måttet är mätt med fel
instrument.** Länsstyrelsen i Blekinge och Länsstyrelsen i Norrbotten besvarade
dag 40-påminnelsen med de kontrollrapporter de haft att lämna sedan den 4
augusti: Blekinge fem handlingar den 29 september 08:12, Norrbotten tio 09:27,
båda utan avgift. Populationen i klass A växer från 155 till 170 handlingar och
de nya talen är:

| Klass | Digitalt födda | Skannade | Totalt |
| --- | --- | --- | --- |
| A | 79 av 140, 56 % | 30 av 30, 100 % | **109 av 170, 64 %** |
| B | 23 av 125, 18 % | 11 av 15, 73 % | 34 av 140, 24 % |

Blekinge maskade en av fem, den handling vars filnamn slutar på
`_Bortredigerad`, med 9,92 procent maskerad yta. **Norrbotten maskade ingen av
tio.** Klass B är oförändrad, och kontrasten smalnar från 70 mot 24 till 64 mot
24 procentenheter.

**Gränsen, deklarerad innan något av talen används.** Sex av de femton nya
handlingarna är sidbilder med ett OCR-textlager under bilden: Norrbottens fyra
diarienumrerade handlingar, dess fotobilaga, och Blekinges maskade handling,
alla med 69 till 100 procent av sidan täckt av bild. Steg 18 väljer metod efter
om ett textlager finns, så alla sex bedömdes med textmetoden, och en balk ritad
i bilden är osynlig för den. Talen ovan står som mätta, men klass A:s andel är
preliminär till dess utlösaren för bildmetoden är avgjord; villkoret för en
ändring skrivs före körningen, som i ADR-0020.

**Jämförelsemängden för P9:s kriterium (b) växer till åtta län.** Minst ett helt
omaskat dokument i klass A finns nu hos Blekinge, Dalarna, Gävleborg, Jämtland,
Norrbotten, Södermanland, Uppsala och Västerbotten, tillsammans 61 dokument.
Uppräkningen om fem län och 17 dokument längre ned i detta dokument är från den
23 augusti och gäller inte längre: Västerbotten tillkom vid rättelsen den 1
september, Blekinge och Norrbotten den 29 september. Kriteriet kräver tre.

**Kontrastmåttet enligt P1 räknat om:** sjutton län har levererat i båda
klasserna, inte femton. Medianskillnaden är **1,95 procentenheter maskerad yta**
och **55,89 procentenheter andel maskade dokument**, och inget av de sjutton har
högre maskad yta i B än i A. Blekinges egen cell är den starkaste motsägelsen
hittills mellan de två måtten: andelen maskade dokument är 80 procentenheter
**lägre** i A än i B, eftersom en av fem är maskad i A mot fem av fem i B, medan
den maskade ytan är 1,82 procentenheter högre i A. Tre län vänder nu på
andelsmåttet, Blekinge, Dalarna och Gävleborg. Norrbottens cell är noll i båda
måtten och vilar på en enda B-handling.

**Steg 26 om, och nollresultatet får sin första namngivna avvikelse.** Korpusen
är 298 handlingar med textlager. De 236 dolda tecknen står kvar, och 258 nya
tillkommer i tre av Norrbottens handlingar. De är inte maskning: OCR-lagret
ligger under sidbilden, så varje tecken i det räknas som dolt av konstruktion,
och de tre handlingarna bär ingen maskning alls. En av dem,
`8535-2024(27706259)`, får därmed flaggan dold av ljus täckning, och den
namnges i invarianten i stället för att tystas. Handlästa körningar ur den är
rapportens egen prosa, som bilden visar i klartext. För de 297 övriga står
nollresultatet oförändrat.

Meningen ovan om att `data/maskning.jsonl` rymmer 16 dokument utanför klasserna
gäller inte längre heller, och det beror inte på Kalmar. De är 33, fördelade på
20 mappar: myndighetsbeslut, avgiftsbeslut och en avgiftsriktlinje, Gotlands
och Kronobergs omprövade leveranser, kammarrättens meddelanden i de tre egna
målen och de åtta praxisavgöranden som lästs i fulltext. Samtliga ligger
utanför måttets population enligt P8, som förut. Filen har alltså 328 rader,
varav 295 i klass A och B.

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

*Tillägg 2026-09-28, efter Kalmars B-leverans:* femton län har levererat i
båda klasserna, inte fjorton. Medianskillnaden är **2,12 procentenheter
maskerad yta** och **60 procentenheter andel maskade dokument**. Inget av de
femton har högre maskad yta i B än i A, vilket står kvar. Kalmars egen cell
drar medianerna åt olika håll: andelen maskade dokument är 100 procent i båda
klasserna, alltså noll skillnad, medan den maskade ytan är 10,16
procentenheter högre i A. Det är den största ytskillnaden efter Västra
Götalands 11,69 och det enda länet där andelsmåttet och ytmåttet säger helt
olika saker.

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

*Tillägg 2026-09-28:* med Kalmars B-leverans blir nötraden tio län med median
+78 procentenheter andel och +3,08 procentenheter maskad yta, och cellerna med
minst tre dokument i båda klasserna blir tolv i stället för elva.
Fjäderfäraden och grisraden är oförändrade. Av de tolv cellerna pekar åtta åt
samma håll, två visar ingen skillnad alls, en är negativ, och den nya,
Kalmar nöt, visar ingen skillnad i andel men den näst största i yta.

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
25 OCR-läst de 72 skannade besluten saknar ingen fil text. Segmenterade efter rättelsen den 4
september 2026: **180 filer av 236, alltså 76 procent, och 2 347 villkor**,
median 12,5 villkor per beslut. Rubrikträffen är nästan lika god i båda
källorna: 123 av 164 digitalt födda och 57 av 72 OCR-lästa, alltså 75 respektive
79 procent. Före rättelsen var talen 173 filer och 2 264 villkor, och bortfallet
beskrevs som 60 filer utan villkorsrubrik som gick att hitta och 3 med rubrik men
inget numrerat villkor. Verifiering är kontroll 1 i `VILLKORSSCHEMA.md` avsnitt 5,
sifferserien 1..N, och varje beslut bär utfallet som `series_ok` och sin källa
som `källa`.

**Täckningen för själva huvudsiffran är däremot oförändrad.** Täckningstalet
gäller segmenteringen, inte återanvändningsmåttet. Huvudsiffran räknades då på
de 120 digitalt födda besluten, alltså 51 procent av korpusen, precis som före
OCR:n, och det som tillkom var en andra, separat mätning på 53 andra beslut.
Talen i det här stycket är från augusti; efter rättelsen den 4 september är de
123 respektive 57.

**OCR-läst text segmenteras sämre, och det är utskrivet i stället för utjämnat.**
Obruten serie fås för 106 av 120 digitalt födda beslut, 88 procent, men bara 21
av 53 OCR-lästa, 40 procent. OCR bryter dessutom ord över radslut, så två
identiska villkor överlever sällan som identiska strängar när ett av dem lästs
med OCR. Därför poolas källorna aldrig i huvudsiffran; det poolade talet skrivs
ut men bär ingen slutsats.

**Resultatet, och det står sig i varje delmängd:**

| Underlag | Villkor | Beslut | Olika texter | Delad text | Egna villkor, median per beslut |
| --- | --- | --- | --- | --- | --- |
| **huvudsiffra, ur textlagret** | 1 762 | 123 | 1 269 | 746 (42 %) | 62 % |
| ur textlagret, obruten serie | 1 602 | 108 | 1 157 | 676 (42 %) | 62 % |
| enbart OCR-lästa | 585 | 57 | 501 | 136 (23 %) | 75 % |
| poolat, bär ingen slutsats | 2 347 | 180 | 1 712 | 951 (41 %) | 64 % |

**Rättelse 2026-09-05: avsnittsrubriken låg i villkorstexten.** Tabellen är
omräknad. Före rättelsen stod huvudsiffran på 615 delade villkor, 35 procent,
och 206 av 220 delade texter inom en prövningsgrupp. Rubriken mellan två villkor
lades till det föregående villkorets text, i 471 av 2 347 villkor, och två
likalydande villkor i olika beslut matchade därför inte när det ena följdes av
en rubrik. Rubrikerna är dessutom det fält VILLKORSSCHEMA avsnitt 2.2 vill ha
bevarat, så de gick förlorade två gånger om. Regeln som infördes är strukturell:
en kort rad inne i avsnittet som inte inleder ett villkor, inte slutar som en
mening och följs av ett numrerat villkor tillhör det som kommer efter den.
**1 655 av 2 347 villkor bär sin rubrik, 148 olika.** Talet var 1 691 under 161
rubriker fram till kontroll 3 samma dag, som visade att 36 av dem var sidhuvuden
och inte rubriker: Miljöprövningsdelegationen, Anläggningsnummer, Örebro län,
Aktbilaga 23 och Skåne. En genomläsning av de 155 som blev kvar, gjord innan
typologin byggs på dem, hittade sju till: ett läns löpande sidrubrik i genitiv,
VÄSTRA GÖTALANDS LÄN, och sex rubriker med föregående menings slut klistrat
framför sig, som `uppstår.Lagring av gödsel och spolvatten`. Förledet hör till
villkoret ovanför och läggs nu tillbaka där, vilket gav femton villkor sitt
meningsslut åter, och rubriken blir det som står efter punkten. **Delegation
framträdde först då som egen rubrik**, tio villkor plus fem under formen med
parentes, och det är den rubrik VILLKORSSCHEMA avsnitt 2.4 gett en egen tabell.
Inget ord som beslutet självt skrev försvann med något av detta.

**Vad som inte rättas är OCR:ns egna felläsningar av riktiga rubriker.**
`Ålbhnänt`, `Allnänt`, `Alhnänt` och `Allmant` är alla Allmänt, och `Lagring av
godsel` och `Sk yddszoner` är lika genomskinliga. De står kvar som registret
läste dem, eftersom fältet ska bära vad textlagret säger och en tyst
omskrivning av källan är en annan sorts fel. De hanteras i typkartan i stället,
deklarerat där.

**Båda de förregistrerade villkoren höll.** Inget beslut tappade villkor, och
det okulära stickprovet på 25 av de 823 borttagna raderna innehöll ingen
villkorstext: alla var antingen rubriker eller sidfotselement. Stickprovet
fällde däremot en första version av regeln, som räknade sidnummer, diarienummer
och anläggningsnummer som rubriker; 58 av 231 kandidater var sådana. Att ta bort
raderna ur villkorstexten är rätt oavsett, så borttagningen behölls och en andra
regel avgör vad som också får sparas som rubrik. Efter den finns noll
identifierare bland rubrikerna.

**Förutsägelsen slog in.** Antalet villkor och beslut står oförändrat, andelen
delad text steg märkbart, och koncentrationen inom prövningsgrupp håller både
riktning och p-värde.

**Rättelse 2026-09-04: segmenteringen kände inte igen två sätt att öppna
villkorsavsnittet.** Tabellen ovan är omräknad. Före rättelsen stod huvudsiffran
på 1 704 villkor i 120 beslut med 36 procent delad text, och det poolade talet på
2 264 villkor i 173 beslut. Orsaken hittades genom att läsa de sju tillstånd som
saknade villkor, se avsnittet om kontroll 2 längre ned: fyra av dem inleder
avsnittet med en mening i stället för med en rubrikrad, och ett har ett textlager
som klistrar ihop rubriken med nästa ord. Segmenteraren fick två reservregler som
bara används när ingen rubrikrad finns i dokumentet, så att inget beslut som
redan segmenterade kan förlora ett villkor på dem.

**Villkoret för att behålla ändringen skrevs innan den kördes** och står i
protokollloggen som en egen rad: inget beslut fick tappa villkor. Utfallet
blev sju nya beslut och noll som tappade. Fyra av de sju bär bruten sifferserie
och är därmed flaggade av instrumentet självt, alltså utanför den rena
delmängden. En av förutsägelserna slog fel och redovisas som sådan: andelen
beslut med obruten serie väntades sjunka, eftersom en inledande mening bär det
första villkoret på samma rad, men den steg från 106 till 108 av de digitalt
födda.

**Huvudsiffran rörde sig inte när OCR-mängden tillkom.** Samtliga tal i första
raden är identiska före och efter att 53 beslut lades till underlaget, vilket de
ska vara, eftersom raden räknas på oförändrade dokument. Det är kontrollen på
att OCR-tillskottet är additivt och inte har rört det som redan var mätt.

**Nollhypotesen faller.** 1 016 av 1 762 villkor, 58 procent, förekommer i ett
enda beslut, och medianbeslutet har egen text i 62 procent av sina villkor. Ett
villkorsregister mäter alltså något som varierar, och arbetet med att bygga det
är motiverat. Måttet är exakt likhet efter gemener och kollapsat blanktecken,
ingenting annat normaliserat, siffervärden avsiktligt bevarade: **det kan bara
underskatta återanvändningen**, aldrig överskatta den. Ett segmenteringsfel som
delar ett villkor i två drar åt samma håll, alltså mot mer skenbar egenart, så
båda felkällorna gör slutsatsen försiktigare och ingen av dem gör den starkare.

**Den delade texten är inte korta fragment.** Delade texter har median 223
tecken mot 264 för de egna, och 10 av 253 ligger under 80 tecken. Det är hela
villkor som återanvänds, inte gemensamma formuleringar som halkat med.

**Den återanvändning som finns är gruppintern, och det är inte en
storlekseffekt.** Av de 253 texter som förekommer i mer än ett beslut stannar
**238 inom en enda prövningsgrupp**. Under slumpmässig omfördelning av besluten,
med prövningsgruppernas faktiska storlekar bevarade, väntas 28,7 och den 95:e
percentilen ligger på 37; noll av 2 000 permutationer nådde 238 (`p < 0,0005`).
Koncentrationen är alltså inte en följd av att Skåne med Blekinge och Västra
Götaland bär hälften av korpusen.

**Koncentrationen replikerar på en oberoende dokumentmängd.** De 57 OCR-lästa
besluten delar inga dokument med de 123 digitalt födda och är lästa med ett
annat instrument. Där stannar **50 av 52 delade texter inom en enda
prövningsgrupp** mot 6,5 väntat under samma permutation, och noll av 2 000
omfördelningar nådde 50. Att andelen delad text är lägre i den mängden, 23 mot
42 procent, är väntat och pekar åt rätt håll: exakt matchning missgynnar OCR-text
och kan bara underskatta återanvändningen där.

**Den konkurrerande förklaringen prövad.** Ett ändringsbeslut upprepar
originalets villkor, och det skulle ge gruppintern återanvändning utan att någon
mall finns. Den förklaringen räcker för par, som är 157 av de 253 klustren, men
inte för de breda: den vidaste texten delas av **28 beslut, varav 24 i Västra
Götalands län**, och den näst vidaste av 13 beslut, varav 7 i Örebro med
Värmland. Ändringskedjor hos en och samma verksamhetsutövare blir inte 24
beslut.
Omvänt gäller att de allra vidaste texterna är de som korsar gruppgränser,
medan den typiska delade texten stannar; av de 27 klustren med minst fem beslut
ligger 23 inom en enda grupp.

Mallar finns alltså, de är prövningsgruppens snarare än landets, och de
förklarar drygt fyra tiondelar av villkoren. Det är i sig ekvivalensfrågan ställd
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

## Samma uppgift lämnas ut av de flesta och maskas av några, 2026-09-05

Tillämpningsnot 6 säger att ett beslut överklagas enligt P9:s kriterium (b)
endast om beslutet självt namnger den maskerade uppgiftstypen, så att
jämförelsen kan göras på fältnivå mot de län som lämnat ut helt omaskade
dokument i klass A. Kronobergs beslut namnger två typer: "Länsstyrelsen har
maskerat uppgifter om djurbesättningens storlek och vissa uppgifter om de
brister som framkom vid kontrolltillfällena." Om jämförelsen går att göra var
en mätfråga som ingen ställt, och villkoret för den skrevs före körningen.

**Jämförelsemängden är 47 helt omaskade A-dokument i sex län**, Dalarna,
Gävleborg, Jämtland, Södermanland, Uppsala och Västerbotten. Not 6 räknade 17
dokument i fem län den 23 augusti; mängden har vuxit med senare leveranser och
med Västerbotten, som ADR-0019 lade till.

| Uppgiftstyp | Län med minst ett dokument i klartext | Dokument |
| --- | --- | --- |
| djurbesättningens storlek | **5 av 6** | 23 av 47 |
| brister vid kontrollen | **6 av 6** | 45 av 47 |

Villkoret var minst tre län per typ, samma tal som kriteriet självt använder.
Båda klarar det. Uppsala är det enda länet utan besättningsstorlek i klartext.

**Förutsägelsen slog in för brister och bara delvis för besättningsstorlek.**
Före körningen skrevs att båda typerna skulle finnas i de flesta län, eftersom
en kontrollrapport som lämnas ut hel med nödvändighet innehåller de brister den
är skriven för att redovisa. Brister finns i 45 av 47 dokument. Besättningens
storlek står däremot i under hälften, 23 av 47, alltså svagare på dokumentnivå
än väntat, medan länsnivån är den villkoret gällde.

**Mätningen läser inga svärtningar.** Not 6 skriver att ett tidigare försök att
härleda uppgiftstyp ur texten runt varje svärtning övergavs sedan det visat sig
dra enskildas namn genom analysen. Den här mätningen går den andra vägen och
läser bara dokument som lämnats ut hela, och den redovisar enbart antal. Ingen
mening ur något dokument är utskriven, eftersom kringtexten kan namnge en
enskild.

**Fyndet är större än den fråga som ställdes.** För protokollet betyder det att
kriterium (b) är drivbart på fältnivå mot Kronoberg. För öppenhetslagret
betyder det något som står oberoende av om något överklagas: **samma
uppgiftstyp, i samma handlingsklass, under samma bestämmelse, lämnas ut i
klartext av de flesta länen och maskas av andra.** Det är olikvärdighet mätt i
stället för påstådd, och det är den formen av påstående projektet finns för att
kunna göra.

---

## Instansen och prövningstillståndet, verifierade i författningstext 2026-09-22

Överklagandet av Länsstyrelsen i Gotlands läns beslut dnr 3287-2026 vilar på
båda frågorna, och den andra var rättsfråga 5 i `docs/BEGARANMALL.md` avsnitt
11, öppen sedan 2026-08-02. Båda författningarna är lästa i Regeringskansliets
fulltext via riksdagen.se, förordningen i lydelse till och med SFS 2026:798.

### Vilken kammarrätt ett länsstyrelsebeslut går till

Förordningen (1977:937) om allmänna förvaltningsdomstolars behörighet m.m.
1 § ordagrant, inledningen och första punkten: *"Överklagande till kammarrätt
tas upp 1. av Kammarrätten i Stockholm när beslut i närmast föregående instans
har meddelats av Förvaltningsrätten i Stockholm, Förvaltningsrätten i Uppsala
eller av en förvaltningsmyndighet som är belägen inom dessa förvaltningsrätters
domkretsar"*. Kriteriet är alltså var myndigheten är belägen. 5 § lägger
Gotlands län i Förvaltningsrätten i Stockholms domkrets.

Härlett för de sex län som fått en P8-skrivelse:

| Länsstyrelse | Förvaltningsrätt enligt 5 § | Kammarrätt enligt 1 § |
| --- | --- | --- |
| Gotland | Stockholm | **Stockholm** |
| Kalmar | Växjö | Jönköping |
| Kronoberg | Växjö | Jönköping |
| Södermanland | Linköping | Jönköping |
| Halland | Göteborg | Göteborg |
| Västra Götaland | Göteborg | Göteborg |

Två av raderna är bekräftade av var målen faktiskt ligger:
Kalmaröverklagandet som mål 3249-26 i Jönköping och Hallandsöverklagandet som
mål 5937-26 i Göteborg.

**Två rader avgörs av myndighetens säte.** 5 § delar två av
länen. Kalmar län är delat mellan Växjö och Linköping, där Vimmerby och
Västervik hör till Linköping, och Västra Götalands län är delat mellan Göteborg
och Jönköping, där bland annat Mariestad, Skövde och Borås hör till Jönköping.
Båda raderna hålls av att länsstyrelsen har sitt säte i Kalmar respektive
Göteborg, som båda ligger i den förstnämnda domkretsen. För Kalmar är
läsningen bekräftad av att målet togs upp i Jönköping. För Västra Götaland är
den inte prövad, eftersom det beslutet inte överklagas enligt tillämpningsnot
6, och raden är därför en härledning och ingenting mer.

**Detta ersätter en svagare kontroll.** Avsnittet om HFD-praxis skriver att
Kronobergs domkrets är kontrollerad mot två andrahandskällor och inte mot
domstolens egen förteckning. Den frågan är nu avgjord i primärkällan, och
svaret är detsamma.

**Följden för öppenhetslagret.** Gotland ger en tredje kammarrätt med ett av
projektets egna mål, utöver Jönköping som har Kalmar 3249-26 och
Jordbruksverkets 3339-26 och Göteborg som har Halland 5937-26. Sverige har fyra
kammarrätter, och den fjärde, Sundsvall, är den som meddelade 2682-21 i ett mål
som inte är projektets. Avsnitt 11 slår fast att kammarrätterna gått åt olika
håll och att inget HFD-avgörande finns om A/B-frågan; en tredje domstol breddar
den kartan oavsett hur målet slutar.

**Tillägg 2026-09-23: härledningen är bekräftad av utfallet.** Överklagandet
gavs in till Länsstyrelsen i Gotlands län den 22 september och registrerades
dagen därpå av Kammarrätten i Stockholm som mål 6901-26, avdelning 03. Tre av
tabellens sex rader är därmed bekräftade av var målen faktiskt ligger, och
ingen av dem motsäger 1 §.

**Samma meddelande flyttar en risk in i projektet.** Med det följer
informationsbladet om förenklad delgivning, vars regel lyder ordagrant: *"Du är
delgiven två veckor efter att domstolen skickade handlingarna. Tiden för att
till exempel svara eller överklaga räknas från den dagen."* I de tre pågående
målen löper alltså frister utan att någon bekräftelse behöver lämnas, till
skillnad från länsstyrelsernas e-delgivningar, som alla har begärt kvitto.
Bladet ålägger mottagaren att kontrollera posten *"minst varannan vecka"*.
Avvikelsen den 22 september, där ett beslut låg oläst i 25 dagar, hade under
den regeln kostat hela fristen utan att något påminnelsemejl kommit.

### Prövningstillstånd krävs inte, och rättsfråga 5 är därmed besvarad

34 a § förvaltningsprocesslagen (1971:291) ordagrant, första stycket: *"För de
mål där det är särskilt föreskrivet krävs prövningstillstånd för att
kammarrätten ska pröva ett överklagande av ett beslut som förvaltningsrätten
har meddelat i målet. Detsamma gäller förvaltningsrättens beslut i en fråga som
har ett direkt samband med ett sådant mål."*

Bestämmelsen gäller alltså överklagande av ett beslut som en förvaltningsrätt
har meddelat. Ett beslut av en länsstyrelse att inte lämna ut en allmän
handling överklagas enligt 6 kap. 8 § OSL direkt till kammarrätt och är inte
ett sådant beslut. Något prövningstillstånd krävs därför inte, vilket är den
gängse ordning som avsnitt 11 antog utan att kontrollera den.

Ett steg upp gäller det motsatta. 35 § ordagrant: *"Ett överklagande av
kammarrättens beslut i ett mål som har inletts i kammarrätten genom
överklagande, underställning eller ansökan prövas av Högsta
förvaltningsdomstolen endast om prövningstillstånd har meddelats."* Förloras
något av målen är nästa steg alltså villkorat.

**Vad verifieringen inte säger.** Ingenting om utsikterna i sak. Åtagandet
noterade att tre ingivna och upptagna överklaganden är en indikation och inte
en verifiering; det är fortfarande riktigt, och det är författningstexten och
inte handläggningen som avgör frågan.

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
dokument ska ha en rad. **Täckningen är 25 av 25.** *Tillägg 2026-09-28: talet
gällde registret den dag det slöts och har varit inaktuellt sedan rättelsen den
1 september, som tog bort Gävleborg A och Jämtland A ur populationen utan att
den här meningen lästes om. Med Kalmars B-leverans står registret på 26 rader
och 24 maskade leveranser, alltså täckning 24 av 24, och steg 29 rapporterar
registret som slutet.* En enda rad saknar sitt
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

**Tillägg 2026-09-28: prövat en gång till, mot Kalmars B-leverans, och (c) är
fortfarande noll.** Elva län maskar nu i klass B i stället för tio, och sex i
stället för fem gör det utan att ange någon grund alls, eftersom Kalmar
tillkommit i båda uppräkningarna. Följebrevet lyder i sin helhet: *"Här kommer
de fem senaste föreläggande, se bifogad fil."* Ingen bestämmelse åberopas, och
(c) kräver uttryckligen 30 kap. 23 § OSL, så kriteriet kan inte träffa
leveransen. Ingen P8-skrivelse följer heller, eftersom not 4 är konjunktiv och
det första ledet saknas. Två omständigheter hör till bilden och redovisas i
stället för att vägas: leveransen följde myndighetens eget erbjudande om
avgiftsfri elektronisk leverans om personuppgifter maskas, ett erbjudande som
accepterades utan att maskningen beställdes, och samma sak är sagd till
Kammarrätten i Jönköping i yttrandet den 8 september i mål 3249-26, som inte
bestrider att maskad elektronisk leverans accepterats. Vad de tre till sex
rutorna per handling döljer går inte att läsa, eftersom texten under dem är
borttagen; ytan är 0,07 till 0,17 procent per handling, vilket är samma
storleksordning som Blekinges fyra digitalt födda B-handlingar och två
tiopotenser under länets egna A-handlingar.

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
fältstruktur. *Tillägg 2026-09-28: talet 124 av 294 är mätt före rättelsen den
1 september, då mallens rubrikband ännu räknades som en ruta, och det går inte
att reproducera i dagens data. Måttet i dag: 88 av 295 handlingar i klass A och
B bär minst en ruta, och i ingen av dem står det text kvar under en ruta.
Skälet som meningen bär står kvar, eftersom en ruta utan text under sig inte
kan tillskrivas någon uppgiftstyp på fältnivå.* Ett försök att härleda typen ur omgivande text övergavs sedan det
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
enda län som maskat samtliga sina B-dokument. *Tillägg 2026-09-28: inte längre.
Kalmars fem förelägganden är också maskade, alla fem, så de är två län.*

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

## Villkorstexten screenad, och sidfoten som låg i den, 2026-09-04

Innan villkorstext får läggas i repot måste påståendet i VILLKORSSCHEMA avsnitt
2.7 prövas. Där står att texten "innehåller i underlaget inga personuppgifter",
och underlaget var då fyra lästa beslut. Samtliga 2 347 villkorstexter är nu
sökta efter e-postadresser, personnummer och telefonnummer, och varje enskild
träff är läst i sitt sammanhang.

**Påståendet håller.** Träffarna är 5 e-postadresser, 5 tal som liknar
personnummer och 69 telefonnummer, och varenda en är länsstyrelsens egen:
adresserna är länsstyrelsernas registratorsadresser, alltså länets namn följt
av myndighetens domän, de personnummerliknande talen är organisationsnummer som
202100-2270, och telefonnumren är myndigheternas växlar. Ingen enskild person förekommer i någon villkorstext.

**Rättelse 2026-09-10: påståendet höll inte.** Screeningen sökte adresser med
snabel-a, och i OCR-läst text har tecknet blivit en vänsterparentes följd av Q.
Sex villkor i sex OCR-lästa beslut bar länsstyrelsens kontaktrad med två
namngivna tjänstemän och deras e-postadresser, och ingen av dem gav träff. De
hittades den 9 september; se avsnittet om textlager som inte läser sidan nedan och
ADR-0022. Meningen står kvar som den skrevs.

### Men screeningen hittade något annat

Alla dessa uppgifter kom in samma väg: **länsstyrelsens sidfot ligger inuti
villkorstexten.** Ett villkor som löper över en sidbrytning sväljer den blocket
med postadress, besöksadress, växel, telefax, bankgiro och webbadress. Det satt
i 54 av 2 347 villkor, ett per drabbat beslut, och 147 rader i
villkorsavsnitten bar en sidfotsmarkör.

**Åtgärd och utfall, med villkoret skrivet före körningen.** Sidfotsrader
utesluts när avsnittet läses. Villkoret var detsamma som vid segmenteringen
tidigare i dag: inget beslut fick tappa villkor. Utfallet: noll borta, noll
tillkomna, och exakt 54 villkor blev kortare, median 149 tecken borttagna och
som mest 263.

**Förutsägelsen slog in på ena halvan och inte på den andra.** Jag väntade att
andelen delad text skulle stiga något, eftersom 54 villkor kommer närmare sina
motsvarigheter. Huvudsiffran rörde sig inte alls och står kvar på 1 762 villkor,
615 delade, 35 procent, 206 av 220 inom en prövningsgrupp. Den OCR-lästa
mängden rörde sig: delade texter går från 44 till 45, gruppinterna från 42 till
43, upprepade villkor från 118 till 120 och andelen från 20 till 21 procent.

Riktningen är den väntade och skälet är begripligt. Sidfoten är samma block i
varje beslut från samma län, men OCR läser den olika varje gång, så den bröt
matchningar just där. I textlagret är de 54 villkoren unika ändå. Föroreningen
gav alltså en liten skevhet, och den låg i den mängd som redan var svagast.

### En tredje gräns, mindre och utskriven

Tio par av beslut och villkorsnummer förekommer två gånger, i åtta beslut, och
texten skiljer sig varje gång. En numrerad rad inne i ett villkor läses alltså
ibland som ett nytt villkor med samma nummer. Schemat är byggt för det, med
`number` som sträng och `position` som heltal, men baselinemåttet skiljer dem
inte åt. Ingen åtgärd i dag; gränsen står här i stället för att upptäckas när
registret byggs.

---

## Textlager som inte läser sidan, och två tjänstemän i en sidfot, 2026-09-10

Kontroll 3 lämnade ett beslut utanför sitt mått, `361be3bd133c`, eftersom
pdfplumber får ut 40 tecken ur dess 34 sidor. Att stänga det gapet ledde till
tre fynd, och det tredje är en personuppgift.

### Två beslut vars textlager inte är en läsning av sidan

`källa: text` i registret betyder bara att pymupdf fick ut minst 200 tecken per
sida. Det betyder inte att texten återger sidan, och två beslut visar skillnaden.

**`361be3bd133c` deklarerar inget typsnitt.** Sidan har ingen `/Font` i sina
resurser och `get_fonts` ger tom lista, men pymupdf får ut 73 459 tecken medan
pdfplumber, pypdf och pdfminer alla får ut några punkttecken. Ordrutorna är
orimliga, ett ord på 81 punkters höjd, och ord bryts mitt itu. Ett svep över
alla 236 tillstånds-PDF:er ställde pymupdf mot pdfplumber: **ett enda beslut
ligger under tio procent**, detta på 0,0005, och nästa ligger på 0,882, med
medianen 0,983. Sikten efter sidor med text men utan typsnitt träffar samma
beslut på 21 av 34 sidor och ingen annan fil på en enda sida.

**`13df613f9802` har tappat å, ä och ö.** Inte ett av 981 bokstäver. Medianbeslutet
ligger på 5,4 procent och det näst lägsta på 4,3. Texten passerar steg 24:s
teckenräkning, och ett andra bibliotek läser samma stympade tecken, så inget
före detta kunde se det.

**Andra vägen är den tryckta sidan.** Steg 39 renderar sidorna och läser dem med
Tesseract på samma villkor som steg 25, och mäter varje lagrat villkor mot den
läsningen med kontroll 3:s egen uppdelning, med å, ä och ö vikta till a, a och o
på båda sidor. Villkoret skrevs före körningen: median minst 0,90 och inget
villkor under 0,50. Golvet är lägre än kontroll 3:s 0,99 med avsikt, eftersom
en teckenström jämförs med en läsning av en bild.

| Beslut | Villkor | Konfidens | Median | Lägsta | Rak median |
| --- | --- | --- | --- | --- | --- |
| `361be3bd133c` | 31 | 95,0 | 0,989 | 0,636 | 0,988 |
| `13df613f9802` | 4 | 95,3 | 0,922 | 0,743 | 0,320 |

**Villkoret håller för båda. Orden i registret är riktiga; tecknen är det inte
överallt.** I `361be3bd133c` handlästes de tre svagaste. I två av dem är det OCR
som läst fel, `NH 4 - N` som `nf4l-n` och `timmar` som `tummar`. I det tredje
är registret riktigt i ord men bär mellanslag inne i ord, `f å r` och `hel g
dagsaftnar`, vilket är vad trasig glyfgeometri ger. 15 av 31 villkor bär minst
en sådan lös bokstav. Fem av de 31 matchar ett villkor i ett annat beslut, och
de är fortfarande fem när lösa bokstäver limmas ihop på båda sidor, så felet
flyttar inte måttet på delad text. I `13df613f9802` är varje ord med å, ä eller
ö fel i registret; den raka täckningen ligger under 0,5 för alla fyra villkor,
som förutsagt. Frågan om beslutet ska läsas ur OCR i stället står som öppet
åtagande.

Första versionen av steg 39 läste domen på fel kolumn, den gemena i stället för
den vikta, och skrev ut att villkoret föll för `13df613f9802`. Koden är rättad
till det som förregistrerades. Måttet är dessutom girigt och kan ge olika tal
för samma korta villkor beroende på skiftläge: för villkor 8 i `361be3bd133c`
ger den raka läsningen 0,945 och den vikta 0,636.

### Två namngivna tjänstemän i registret

**Sex villkor i `data/villkor.jsonl` bar två tjänstemäns för- och efternamn och
deras e-postadresser.** Sikten som hittade dem letade efter webbadresser i
sidfoten, inte efter namn. Alla sex är OCR-lästa beslut från Länsstyrelsen i
Halland, och alla bar raden `Kontakta i detta ärende:` som tredje rad i
sidfotsblocket. De två raderna ovanför den fångas av befintliga markörer; den
tredje saknar postnummer och telefonnummer, och OCR har läst snabel-a som
vänsterparentes följd av Q, så varken sidfotsmarkören i steg 24 eller
screeningen i steg 33 såg den. Kontroll 3 kan inte se felet, eftersom den
OCR-lästa halvan mäts mot samma fil som segmenteringen läste.

Raderna kom in med `a32fda2` och är pushade. Historiken skrivs inte om. Beslutet
och skälen står i ADR-0022: en markör för kontaktraden och för en adress som OCR
läser den, samma form i screeningen, och en invariant över registret och
facitfilerna.

**Rättningen ändrar exakt de sex villkoren.** Inget beslut tappar ett villkor:
2 347 villkor i 180 beslut och 1 655 med rubrik, före och efter. Förutsägelsen
att texterna skulle bli längre föll; de blev 465 tecken kortare sammanlagt,
eftersom kontaktraden avslutade sidan. Huvudsiffran rör sig inte: 42 procent
delad text i den digitalfödda halvan och 238 av 253 texter inom en
prövningsgrupp. Den OCR-lästa halvan går från 136 till 137 delade villkor,
eftersom `Utgödsling av stallarna ska ske minst två gånger per vecka.` står i
tre beslut men matchade i två så länge det tredje bar kontaktraden.

### Kontroll 3 omkörd, och ett tal som var inaktuellt

| | Digitalfödd, pdfplumber | OCR, samma fil |
| --- | --- | --- |
| publicerat 2026-09-05 | 0,9914 av 544 793 | 0,9990 av 227 860 |
| före dagens rättning | | 0,9970 av 227 734 |
| efter dagens rättning | 0,9914 av 546 284 | 0,9974 av 227 269 |

Avhuggningen står på 121 av 2 347, 5,2 procent, och villkoret för kontroll 3 är
uppfyllt. **Talet 0,9990 i avsnittet om kontroll 3 och i ADR-0021 mättes före
tillägget i ADR-0021 samma dag**, och kontroll 3 kördes inte om efter det. Mätt
på registret som det stod före dagens rättning är talet 0,9970, så fallet kom
med tillägget och dagens ändring höjde talet igen. Vad i tillägget som sänkte
det är inte undersökt och står som öppet åtagande. Talen i de äldre avsnitten
står kvar som de mättes.

---

## Facit för rubrik mot sak: rubriken bär typen i tre fall av fem, 2026-09-09

Beslutsloggen i VILLKORSSCHEMA avsnitt 3 förkastar alternativet att härleda
villkorstypen ur rubriken med skälet att den "klassar fel och kraschar på
rubriklösa beslut". Belägget var ett enda exempel: Motala 2021 villkor 12 står
under Övrigt och är i sak ett avvecklingsvillkor. Registret bär nu 2 347
villkor, så skälet går att mäta i stället för att åberopas.

**Upplägget står i protokollloggen före körningen.** 120 villkor i fyra strata
om 30, korsat på källa, textlager mot OCR, och på om villkoret har rubrik.
Stratifieringen är avsiktligt inte proportionell mot korpusen, eftersom facit
ska vara precist där instrumentet är svagast. Urvalet dras med fast frö,
20260909, och ordningen slumpas över beslut. **Blindheten är mekanisk och inte
en avsikt:** steg 38 skriver identifierare, position och villkorstext till fil,
aldrig rubriken, och rubriken fogas till först av `--score`. Samtliga 120 svar
låg skrivna i `data/villkor_facit.jsonl` innan sammanställningen kördes en enda
gång.

**Tre lästolkningsregler formulerades under de första trettio villkoren och
innan något svar skrevs till fil.** Den första: typen följer det som regleras
och inte verbet, så ett villkor om analys av gödselns växtnäring är gödsel och
inte kontroll, medan kontroll används för kontrollprogram, besiktning och
journalföring som saknar eget ämne. Den andra: ett block som segmenteringen
fogat samman av flera villkor med olika ämne och utan ett som dominerar får
svaret kan inte avgöra. Den tredje: ett ämne som vokabulären inte namnger får
Övrigt med ämnet antecknat, eftersom det är ett fynd om typologin och inte om
texten. Inget av de trettio första svaren berördes av den tredje regeln, så
inget svar har skrivits om.

**Villkoret för att facit skulle vara användbart höll.** Det skrevs före
körningen att jag ska kunna sätta en typ ur texten ensam för minst 90 procent
av de 120. Utfallet är **118 av 120, alltså 98,3 procent**. De två som föll är
båda sammanfogade block: `097f049b82b6` villkor 10, som bär gödsel, aska,
tvättvatten, stoft och kemikalier i ett stycke, och `073b890ef134` villkor 7,
där en gödselanalys och ett kontrollprogram är två villkor i ett.

**Förutsägelsen om överensstämmelsen föll.** Före körningen skrevs minst 80
procent för de 60 med rubrik. Av de 59 som fick en typ satt ur texten stämmer
rubrikens typ i **36, alltså 61,0 procent**. Delat på källa är det 19 av 29 för
de OCR-lästa och 17 av 30 för de digitalfödda, och vägt med korpusens egen
fördelning av villkor med rubrik, 361 OCR mot 1 294 text, blir talet **58,6
procent**. Urvalet överviktar alltså det stratum som stämmer bäst, och
korpustalet är sämre än stickprovets.

**Förutsägelsen om Övrigt bekräftades inte.** Det skrevs att Övrigt blir den
enskilda rubrik som stämmer sämst. Övrigt föll i 1 av 1, vilket inte skiljer
den från Stallar som föll i 2 av 2. Den rubrik som bär massan av felen är i
stället **Allmänt: 6 av 9**, följd av Djurstall med 3 av 4.

**De 23 oenigheterna delar sig i två familjer.** Den uppdelningen gjordes med
rubrikerna synliga och är därför inte blind; den redovisas som en efterhandsläsning
av utfallet och inte som en del av mätningen. I tio fall namnger rubriken en
plats eller ett kapitel och texten ett annat ämne: en gödslingsplan under
Allmänt, en skyddszon under Ålbhnänt, en gödselstuka under Stallarna, ett
avvecklingsvillkor under Övrigt. I tretton fall är båda placeringarna
försvarbara och tvisten gäller typologins egna gränser: tvättvatten från
stallrengöring under gödsel eller vatten, en bevuxen skyddszon under gödsel
eller vatten, markkartering under kontroll eller gödsel, ventilation som
motiveras med både lukt och buller. **Hårda rubrikfel är alltså 10 av 59, 17
procent, och gränsdragningar 13 av 59, 22 procent.** Den andra siffran är ett
fynd om schemat och inte om rubriken.

**Allmänt är inte instrumentets fel.** Rubriken kunde ha släpat efter i
segmenteringen, och det prövades: i `486f0758082c`, `c357ac195bc7`,
`0fe92f8e7486`, `777f4fcb9746` och `9327fb75e98f` bryter senare rubriker igenom
korrekt, Utsläpp till vatten, Buller, Egenkontroll och Övrigt. Besluten lägger
själva tolv villkor i rad under Allmänt: gödselhantering, lagring, spridning,
skyddszoner, spridningsavtal och tvättvatten. **297 villkor i korpusen står
under en rubrik ur Allmänt-familjen, i 103 beslut, och exakt 103 av dem står på
position 1.** De övriga **194 är alltså inte det allmänna villkoret**, och en
rubrikhärledd typ skulle kalla vart och ett av dem allmänt. 28 beslut lägger
fler än tre villkor under Allmänt, tillsammans 180 villkor. Formuleringarna
återkommer ordagrant mellan besluten, så felet är en mall som upprepas och inte
brus: det skulle blåsa upp allmänt och krympa gödsel systematiskt över en hel
prövningsgrupp.

**Den andra halvan av skälet mäts på de rubriklösa.** Där ger rubrikvägen inget
alls. Ur texten ensam fick **59 av 60** en typ, och fördelningen liknar
korpusens: 23 gödsel, 8 kemikalier och avfall, 6 kontroll, 5 vatten, 5 allmänt,
4 buller, 3 luft, 3 avveckling. **692 av 2 347 villkor, 29,5 procent, saknar
rubrik helt.**

**Beslutsloggens rad står kvar och vilar nu på en mätning.** Båda leden i skälet
håller: rubriken klassar fel i minst 17 procent av fallen där den finns, och den
saknas för nästan vart tredje villkor, medan texten räcker för 98 procent.

**Vad facit inte säger.** Det är en läsare och ingen andra läsare, så det finns
inget mått på hur två bedömare skulle skilja sig åt. Mina egna svar är
referensen, och i de tretton gränsfallen kan de vara fel utan att någon
upptäcker det. 120 villkor av 2 347 är 5,1 procent, och talen ovan bär
stickprovets osäkerhet. Bedömningarna är MANUAL enligt avsnitt 2.8, aldrig RULE.

---

## Villkorstypologin mot korpusen: nio typer räcker inte, 2026-09-05

VILLKORSSCHEMA avsnitt 2.2 fastställer nio villkorstyper, satta utifrån fyra
beslut. Registret bär nu 148 olika rubriker ur 180 beslut, så frågan om nio
räcker går att ställa mot underlaget i stället för mot fyra dokument. Steg 35
placerar **varje rubrik för hand**, ingen av dem med en ordmatchning, och
kartan ligger i koden så att en läsare kan vara oense om en enskild placering
utan att först behöva lista ut en regel.

**Så fördelar sig de 1 655 villkoren med rubrik över schemats nio:**

| Typ | Villkor | Andel |
| --- | --- | --- |
| gödsel | 592 | 35,8 % |
| allmänt | 297 | 17,9 % |
| kemikalier och avfall | 155 | 9,4 % |
| kontroll | 140 | 8,5 % |
| buller | 82 | 5,0 % |
| vatten | 71 | 4,3 % |
| övrigt | 56 | 3,4 % |
| luft | 40 | 2,4 % |
| avveckling | 33 | 2,0 % |
| **summa** | **1 466** | **88,6 %** |

**Sex ämnen återkommer som ingen av de nio namnger**, och alla sex har nio
villkor eller fler: djurstall 64, förbränning och energi 69, transporter 13,
biotopskydd och naturvärden 10, döda djur 9, markarbeten i förorenad mark 9.
Tillsammans 174 villkor, 10,5 procent. De föreslås som tillägg i stället för
att läggas i övrigt, eftersom övrigt är dit ett ämne går för att sluta räknas.
Schemat säger att vokabulären är additiv och att en befintlig typ aldrig byter
betydelse, så ett tillägg kostar ingen omextraktion.

**Förutsägelsen höll till hälften.** Före körningen skrevs att minst fyra
sådana ämnen skulle saknas och att över 15 procent av villkoren med rubrik
skulle falla till övrigt om bara de nio används. Det blev sex ämnen, alltså mer
än förutsagt, men 13,9 procent, alltså under tröskeln. Riktningen höll och
tröskeln föll.

**Två placeringar är rena bedömningar och står utskrivna i koden.** Skyddszoner
ligger under vatten och inte under gödsel, eftersom villkoret läggs på marken
intill vattnet och motiveras med vattnet, trots att det reglerar spridning.
Biogasanläggningen ligger under energi och inte under gödsel, trots att
substratet är gödsel. Båda går att invända mot, och det är därför de står som
kommentarer på sina rader.

**Aska hör till kemikalier och avfall.** Schemat avgör det uttryckligen med
Motala 2021 villkor 9 som belägg. Min första placering var luft och var fel mot
schemats egen text; rättad. Där rubriken nämner rökgasrening och aska
tillsammans är rökgasen ämnet, och de raderna ligger kvar under luft.

**Femton villkor bär rubriken Delegation** och räknas inte som en typ, eftersom
avsnitt 2.4 ger de delegerade frågorna en egen tabell: en delegation är
myndigheten som håller en fråga öppen, inte ett krav på verksamhetsutövaren.
Rubriken syntes först sedan de påklistrade meningsförleden lossats samma dag.

**Kartan säger ingenting om innehållet.** Schemat säger själv att rubrik och sak
skiljer sig: Motala 2021 villkor 12 står under Övrigt men är i sak samma
avvecklingsvillkor som Stora Markies villkor 13 under Avveckling. Att mäta det
kräver handläst facit och är nästa steg. **692 villkor saknar dessutom rubrik
helt** och når ingen typ den här vägen.

---

## Kontroll 3: registret läst tillbaka mot dokumenten, 2026-09-05

Kontroll 1 prövar att villkorsnumren bildar serien 1..N. Kontroll 2 prövar att
antalen stämmer mot korpusen. Ingen av dem kan se ett villkor vars text är fel,
eftersom en förvanskad sträng numreras rätt och räknas rätt. Steg 34 läser
texten tillbaka.

**Den digitalfödda halvan läses av ett annat bibliotek.** Registret är
segmenterat ur pymupdfs textlager; här läses varje digitalfött beslut om med
pdfplumber, och varje lagrat villkor söks i den utskriften. Att två bibliotek
är överens om en sträng säger något om dokumentet; att ett bibliotek är överens
med sig självt säger ingenting. Den OCR-lästa halvan har ingen andra väg,
eftersom den igenkända texten är den enda text som finns, och mäts därför mot
samma fil som segmenteringen läste. Den kontrollen är svagare och redovisas som
sådan: den kan fånga fel i hopfogningen och i sidfotsbortfallet, men den
replikerar ingen läsning.

**Ett villkor matchas i delar.** En sidfot som tagits bort
mitt i ett villkor lämnar den lagrade texten som två bitar av dokumentet med ett
hål emellan, så ett vanligt delsträngstest skulle falla just på de beslut där
sidfotsregeln gjorde sitt jobb. Texten konsumeras i stället glupskt: längsta
prefix som finns kvar i råströmmen tas, sökningen fortsätter efter det, och
antalet bitar redovisas.

**Utfall.** 0,9914 av 544 793 tecken återfanns i den digitalfödda halvan och
0,9990 av 227 860 i den OCR-lästa. Ett beslut, `361be3bd133c`, ligger utanför
måttet: pdfplumber får ut 40 tecken ur 34 sidor, vilket mäter biblioteket och
inte registret, och att sådana beslut redovisas för sig skrevs in i
förregistreringen före körningen. Det beslutets 31 villkor är alltså ännu inte
kontrollerade på någon andra väg. 44 villkor ligger under 95 procent och är
genomgångna ett och ett. Nästan alla är nedsänkta tecken som de två biblioteken
läser i olika ordning, `Leq`, `NH4-N`, `CO2`, `O2`, plus radavstånd i
bullertabellerna. Ett är en verklig rest: `13df613f9802` villkor 4, där OCR
förvanskat sidfoten så illa att ingen markör träffar den.

**Fyra fel som ingen tidigare kontroll kunde se.** Det första var det stora: en
tomrad i textlagret är en sidbrytning lika ofta som ett mellanrum mellan två
villkor, och den stängde alltid villkoret. Resten av texten efter tomraden föll
då bort helt, i **209 villkor i 126 beslut**, varje gång mitt i en mening. Det
andra: sidhuvudet kommer ibland utan tomrad före sig och lästes då som
villkorstext. Det tredje: sidhuvudets länsnamn stod inte i ordlistan, så
överhoppningen slutade mitt i huvudet och tog länsnamnet, datumet och
diarienumret med sig in i texten. Det fjärde: ett villkorsnummer sist på en sida
gav en tom text som lästes som en avslutad mening, vilket lämnade själva
villkoret utan hem.

**Ett personnamn hade nått ett committat register.** Ett filnamn i en sidfot, i
`097f049b82b6` villkor 2, bar en handläggares för- och efternamn, och raden är
committad och pushad i a32fda2. Det andra sidhuvudsfelet lade dessutom ett
bifogat rättelsebeslut med två namngivna tjänstemän i `1c8347c55318` villkor 4,
men den texten uppstod i en mellanversion under själva rättningen och nådde
aldrig git. Båda är borta ur registret, och steg 33 screenar nu även
filändelser: ett filnamn hör aldrig hemma i en villkorstext, så formen är
entydig på ett sätt som ett par versaler aldrig blir, och namnkontrollen kan
därför fortsatt utebli.

**Historiken skrivs inte om.** Namnet står kvar i trädet för varje commit från
a32fda2 till och med rättningen, och de commitarna är pushade. ADR-0003 gör
historiken append-only, och Martin bekräftade regeln utan undantag den
5 september 2026, så undantagsmeningen där om personuppgifter används inte.
Skillnaden mot de fem commits som skrevs om enligt ADR-0018 är att de aldrig
hade pushats och alltså aldrig var historik. Kvar står den andra halvan av
ADR-0003:s konsekvens, att händelsen dokumenteras öppet, vilket är vad det här
avsnittet gör. Före publicering finns en följd att ta ställning till: ett
tjänstemannanamn blir då sökbart ur ett filnamn i en sidfot, vilket är precis
det ADR-0018 valde bort.

*Tillägg 2026-09-10:* frågan är inte öppen. Tillägget till ADR-0003, skrivet
samma dag, avgör den: historiken skrivs aldrig om, oavsett vad en commit bär, och
namnet blir läsbart som ett medvetet pris. Avsnittet om villkorsregistret nedan
beskriver dessutom en adress som OCR gjort oigenkännlig och som stoppades bara
därför att ett telefonnummer stod på samma rad. Formen blev då ingen egen regel,
och sex villkor utan telefonnummer passerade senare på just den; se ADR-0022.

**Sidfotsmarkörerna utökades med två former.** Den engelska sidmarkören `Page N
of M`, 72 rader i 30 beslut, satt där den svenska sitter och missades för att
korpusen är svensk. Filändelser, 4 rader i 4 beslut, är den andra.

**Förutsägelsen slog fel, och det är i sig ett resultat.** Före körningen skrevs
att andelen delad text skulle falla, eftersom längre texter är mindre troliga
att matcha exakt. Den steg, från 40 till 42 procent, och koncentrationen inom
prövningsgrupp från 222 av 237 till 238 av 253. Skälet är att två beslut med
samma villkor kapades på olika ställen, så avhuggningen dolde matchningar.
**Instrumentets fel drog alltså mot att underskatta likheten mellan olika
besluts villkor**, vilket är den försiktiga riktningen.

**Avhuggningen, kanariet för det containment inte kan se.** Ett villkor som
kapats finns fortfarande i dokumentet, så delsträngstestet ser det aldrig.
Måttet är i stället sista tecknet: 133 av 2 347 villkor slutar utan
skiljetecken, 5,7 procent, mot 268 av 2 347 och 11,4 procent när kontrollen
började. Taket i förregistreringen var 10 procent.

**Kanarie 1, villkor per beslut, OCR mot digitalfött inom samma
prövningsgrupp.** Riktningen var förutsagd: OCR lägre, eftersom OCR bryter rader
och tappar nummer. Den håller i fem av åtta jämförbara grupper, Skåne med
Blekinge 13 mot 7, Örebro med Värmland 16 mot 7, Västra Götaland 17 mot 12,
Kalmar med Kronoberg 21 mot 18 och Uppsala med flera 10 mot 6. Två grupper är
lika, och Halland går åt andra hållet, 11 mot 13. Kanariet larmar alltså inte,
men det visar att OCR-halvan inte är utbytbar mot den digitalfödda.

**Kanarie 2, bullervärdena, är nu stängt.** VILLKORSSCHEMA öppnade mängden som
40, 45 och 50 dB(A) ekvivalent samt 55 momentant utifrån fyra dokument och sade
att den fastställs mot hela korpusen i första fullkörningen. Den körningen är
gjord: 504 förekomster och sju värden, 37, 40, 42, 45, 47, 50 och 55. De tre nya
kommer alla ur ett och samma beslut, `aa2cbc78989b` villkor 9, som skriver
"47 dB(A) vardagar kl. 07.00 - 18.00 42 dB(A) lördagar, söndagar och helgdagar
kl. 07.00 - 18.00 42 dB(A) kvällstid kl. 18.00 - 22.00 37 dB(A) nattetid kl.
22.00 - 07.00", alltså tre decibel under den vanliga trappan hela vägen. Mängden
står nu som invariant, så att en OCR-läsning av 40 som 49 faller direkt.

---

## Villkorsregistret skrivet, och screeningen som stoppade det, 2026-09-05

Steg 33 skriver villkoren själva till `data/villkor.jsonl`: 2 347 rader med
texten som beslutet skrev den, numret, positionen i avsnittet, rubriken,
prövningsgruppen, beslutstypen och samma `text_hash` som baselinen. Det är
första gången källtext går in i repot, och VILLKORSSCHEMA avsnitt 2.7 tillåter
just det, eftersom villkorstexten är mätobjektet.

**Steget vägrade skriva första gången, och det var meningen.** Screeningen mot
e-postadresser, personnummer och telefonnummer sitter före skrivningen och
avbryter på träff i stället för att varna. Den fann 23 villkor med
telefonnummer, alla sidfotsrader som den tidigare markörlistan inte kände igen,
och ett av dem bar en namngiven handläggare med personlig adress som OCR gjort
oigenkännlig för e-postmönstret. **Utan den spärren hade en tjänstemans namn
och adress gått in i repot.**

**Fyra markörer till, var och en mätt och stickprovad före beslut.** Bart
telefonnummer 24 rader, postnummer med ort 26, fax i tre former 3, och
sidnummer 418. Ett stickprov på 22 av de 418 innehöll uteslutande sidnummer och
sidhuvuden. Effekten på måttet blev liten, eftersom de flesta sidnummer redan
föll bort som rader mellan två villkor: huvudsiffran gick från 697 till 698
delade villkor och den OCR-lästa mängden från 48 av 50 till 49 av 51
gruppinterna texter.

**Registret och baselinen är en och samma segmentering.** Steg 33 importerar
steg 24 i stället för att upprepa dess regler, och hashen är det som visar att
de beskriver samma villkor. En invariant håller de två filerna mot varandra rad
för rad, och en andra invariant söker registret efter samma tre sorters
uppgifter som steget gör, så att garantin inte vilar på att någon körde
screeningen en gång.

**Vad registret bär och inte bär.** Det bär texten, rubriken och
proveniensfälten. Det bär ännu ingen villkorstyp, inga kvantifierade krav, ingen
tidsdimension och inga länkar mellan beslut. De fyra är nästa steg i schemat och
kräver var för sig samma ordning som allt annat i dag: villkoret skrivet före
körningen och ett handläst facit innan en siffra får publiceras.

---

## Prövotidsbesluten, en femte beslutsform, 2026-09-04

De två beslut som utgivaren kallar "Villkor" och "Slutliga villkor" är lästa,
och de visade sig höra ihop med ett av de nio ändringsbesluten. Alla tre är
samma sak: ett beslut som avslutar en prövotid och fastställer de slutliga
villkoren. En sökning på beslutsmeningen över hela korpusen ger fyra sådana
beslut.

| Id | Utgivarens etikett | Villkor beslutet sätter | Extraherade |
| --- | --- | --- | --- |
| `017a452fb59c` | Slutliga villkor | 14 och 15 | 1 |
| `35ca1f69b1b1` | Villkor | 20 till 23 | 0 |
| `af6b7fcd9ed7` | Ändringstillstånd | 33 och 34 | 0 |
| `b3d95df7257f` | Ändringstillstånd | 30 till 32 | 0 |

Besluten säger själva vad de gör: "Miljöprövningsdelegationen beslutar att
fastställa följande slutliga villkor avseende rening av spol- och tvättvatten",
"Utöver tidigare lämnade slutliga villkor gäller följande villkor: 14.",
"Miljöprövningsdelegationen godkänner ingiven utredning och avslutar
prövotiden". Alla fyra nämner prövotiden.

**Formen är osynlig i projektets alla klassificeringar.** Utgivarens etiketter
delar de fyra på tre olika namn. VILLKORSSCHEMA avsnitt 5 räknar upp vilka
beslutstyper som får sakna villkor och nämner inte prövotidsbeslut. Steg 31:s
sju typer har ingen plats för dem, så två hamnar under `villkor` och två under
`ändring`.

**Betydelsen är större än volymen.** Fyra av 236 beslut är lite, men ett
prövotidsvillkor är det bindande villkoret: prövotiden finns för att frågan
inte kunde avgöras när tillståndet gavs, och det slutliga villkoret ersätter
den provisoriska föreskriften. Ett register som missar dem bär den provisoriska
lydelsen där den gällande borde stå. Det gör felet till ett giltighetsfel.

**Numreringen fortsätter grundtillståndets, precis som i ändringsbesluten.**
Villkoren heter 14, 20 till 23, 30 till 32 och 33 till 34. Det bekräftar för
tredje gången i dag att serien 1..N är fel kontroll för allt utom tillstånd och
domar.

**Minst tio villkor saknas i materialet av det här skälet.** Ett av fjorton
extraheras. Ingen ändring är gjord; villkoret för en rättelse skrivs innan den
körs, och den bör tas tillsammans med ändringsbesluten eftersom orsaken är
densamma.

---

## De nio sista ändringsbesluten lästa, och en rättelse av mitt eget svar

De 31 ändringsbesluten utan extraherade villkor delades tidigare samma dag i
fyra grupper med ett sökuttryck, och nio blev oplacerade. De nio är nu lästa,
alla i sin helhet. Samtliga tio citat nedan är verifierade ordagrant mot
källdokumenten.

**Rättelse av slutsatsen om de sju handlästa ändringsbesluten.** Där står
att en villkorsändring saknar numrerad serie och att "noll extraherade villkor är rätt svar". Det är riktigt
för baselinemätningen, som mäter återanvändning av hela villkorsuppsättningar,
och fel för registret. En villkorsändring skriver ut den ändrade lydelsen i sin
helhet: "Miljöprövningsdelegationen bifaller delvis yrkandet om ändring av
villkor 6 ... Villkoret ges följande lydelse: 6. Lagring av stallgödsel ska ske
i gödselhus med tak, väggar och stängningsbara portar ...". Det är ett villkor
med en ny lydelse och ett datum, alltså precis vad ett register med
tidsdimension enligt VILLKORSSCHEMA avsnitt 2.5 ska bära. Rätt formulering är
att besluten ligger utanför vad segmenteraren är byggd att hitta, inte att de
saknar villkor.

**Åtta av nio skriver ut minst ett villkors text.** Bara ett gör det inte.

| Form | Antal | Beslutets egna ord |
| --- | --- | --- |
| ändrar ett namngivet villkor och skriver ut den nya lydelsen | 5 | "beslutar att ändra del av villkor 7 ... till följande lydelse" |
| för över grundtillståndets villkor och ändrar samtidigt ett | 1 | "ska även gälla för ändringstillståndet. Villkor 2 ska dock ändras och ha nedanstående lydelse, samt ett nytt villkor" |
| fastställer slutliga villkor efter prövotid | 1 | "godkänner ingiven utredning och avslutar prövotiden ... beslutar att fastställa följande slutliga villkor" |
| meddelar ett enda villkor i löpande text | 1 | "Ändringen avser täckning vid lagring av gödsel" |
| för över grundtillståndets villkor utan egna | 1 | "ska gälla även för detta tillstånd" |

**Två av dem numrerar högt, som de föregående gjorde.** Prövotidsbeslutet sätter
villkor 33 och 34. Det bekräftar mönstret från kontroll 1-avsnittet ovan och
lägger till en form som inte var känd: ett beslut som avslutar en prövotid och
fastställer slutliga villkor är inte ett ändringstillstånd i vanlig mening,
men utgivaren har etiketterat det som ett.

**Ett villkor skrivet i löpande text går inte att segmentera med nummerregeln.**
I `28816f85c4d7` står villkoret som "Villkor 4, Gödsel från fjäderfä ska lagras
på tät platta under tät täckning", alltså med komma efter numret i stället för
punkt. Regeln `CONDITION_START` kräver punkt eller högerparentes. Gränsen är därmed
känd och mätt.

**Vad detta betyder för registret.** Av de 40 ändringsbesluten bär 9 en
segmenterbar villkorsuppsättning. Av de 31 övriga är nu 16 lästa för hand, sju
tidigare i dag och nio här, och **14 av de 16 skriver ut minst ett villkors
lydelse**. De två som inte gör det för båda över grundtillståndets villkor utan
att lägga till egna. De återstående 15 är placerade enbart med sökuttryck och
inte lästa. Ett register som bara tar 1..N-listor missar varje ändrad lydelse i
materialet. Ingen ändring är gjord i extraktionen; villkoret för en sådan ska
skrivas innan den körs.

---

## Kontroll 1 säger inte något om ändringsbeslut, 2026-09-04

Handläsningen av ändringsbesluten visade att kontroll 1 tillämpas på handlingar
den inte kan uttala sig om. Ett ändringsbeslut som ändrar villkor 1, 3 och 8 i
ett tidigare tillstånd extraheras rätt som 1, 3 och 8, och luckan är då det
riktiga svaret. Att räkna det som en trasig serie gör två saker fel samtidigt:
segmenteraren ser sämre ut än den är, och det döljs att kontrollen inte vet
något alls om just den handlingens fullständighet.

**Tre former förekommer bland de nio ändringsbeslut som har extraherade
villkor.** Fyra bär en full serie från 1, alltså hela villkorsuppsättningen
omtryckt. Tre bär en obruten löpande serie som börjar högt, 35 till 40, 7 till 8
och ett ensamt 18, alltså villkor som lagts till efter grundtillståndets sista
nummer. Två bär en spridd mängd, 1, 3, 8, 9, 15 respektive 3, 4, 6, 12 till 16,
alltså de villkor som ändras. Bara den första formen är prövbar med en serie.

**Åtgärden ändrar ingen publicerad siffra.** Varje rad bär nu `serie_prövas`
vid sidan av `series_ok`, och det råa utfallet står kvar oförändrat, så inget
mått som räknas på den rena delmängden rör sig. Det som tillkommer är att steget
också redovisar kontrollen över de handlingar den är skriven för:

| Underlag | Obruten serie |
| --- | --- |
| digitalt födda, alla | 108 av 123, 88 % |
| digitalt födda, prövbara | **105 av 114, 92 %** |
| OCR-lästa, alla | 22 av 57, 39 % |

De nio ändringsbesluten ligger utanför kontrollen. Ändringsbesluten flyttas
alltså inte in i den rena delmängden, eftersom kontrollen inte kan visa att de
är fullständiga; de lyfts ut ur nämnaren, eftersom den inte kan visa att de är
trasiga heller. Vad som är känt om deras fullständighet är ingenting, och det
är den ärliga redovisningen.

**Fyra tillstånd vars serie inte börjar på 1 är däremot verkliga fynd.** Tre är
OCR-lästa med luckor, och ett av dem bär ett villkor numrerat 98, vilket är en
felläsning. Det fjärde, `e8009d9f51c0`, är digitalt fött och börjar på 11.
Kontroll 1 gör där precis det den ska.

---

## Ändringsbesluten handlästa, 2026-09-04

Kontroll 2 lämnade en fråga öppen: 31 av 40 ändringsbeslut saknar extraherade
villkor, och VILLKORSSCHEMA uttalar sig inte om ändringar. Sju är lästa för
hand. Urvalet är var femte av de 31 sorterade på identifierare, alltså en
reproducerbar regel och inget plock.

**Ändringsbesluten är tre olika saker, och bara den ena sorten ska bära
villkor.**

**Villkorsändring, fem av sju.** Beslutet ändrar eller upphäver ett eller ett
par namngivna villkor i ett tidigare tillstånd, med stöd av 24 kap. 8 § eller
13 § miljöbalken. Formen är genomgående densamma: "Miljöprövningsdelegationen
ändrar villkor 10 i tillståndet från den 8 oktober 2020", "Villkor 5 ändras till
följande lydelse", "Miljöprövningsdelegationen upphäver villkor 4 och 18".
Någon numrerad serie finns inte, och noll extraherade villkor är rätt svar för
baselinemätningen. **Rättat samma dag:** för registret är det fel svar, eftersom
besluten skriver ut den ändrade lydelsen i sin helhet. Se avsnittet om de nio
sista ändringsbesluten.

**Ändringstillstånd som lägger till villkor, en av sju.** Beslutet meddelar nya
villkor och numrerar dem vidare från grundtillståndet. I `982fb8530a1b` heter de
17 till 21, och beslutet skriver ut varför: "Villkor som meddelats för
grundtillståndet i beslut ... ska de ytterligare villkor gälla som fastställs i
detta beslut." Det är en verklig miss i extraktionen.

**Ändringstillstånd som för över befintliga villkor, en av sju.**
`50e5f7f6ec2d` beslutar att grundtillståndets villkor ska omfatta även den
utökade verksamheten: "Miljöprövningsdelegationen förordnar att de villkor som
föreskrivs för verksamheten i Miljöprövningsdelegationens tidigare beslut
daterat 2009-10-23 ... ska omfatta den samlade verksamheten." Inga egna villkor,
och noll är rätt.

**Fördelningen över alla 31, mekaniskt räknad och därför indikativ.** Formerna
ovan går att känna igen på beslutets egna ord, och en räkning som söker dem ger
15 villkorsändringar, 1 som för över befintliga villkor, 6 som ser ut att bära
egna villkor och 9 som inte går att placera med de mönstren. Räkningen är ett
sökuttryck och ingen läsning; den säger var de återstående läsningarna ska
göras.

**Det viktigaste fyndet gäller kontroll 1, inte täckningen.** De sex som ser ut
att bära egna villkor numrerar dem 7 till 11, 12 till 15, 17 till 21 och 30 till
32. **Inget av dem börjar på 1.** Kontroll 1 i VILLKORSSCHEMA avsnitt 5 kräver en
obruten serie 1 till N, och det kravet är rätt för ett tillstånd och fel för ett
ändringsbeslut som fortsätter grundtillståndets numrering. Ett korrekt
extraherat ändringsbeslut skulle med dagens kontroll flaggas som trasigt.

Schemat är redan byggt för det: `number` är en sträng och `position` ett heltal,
motiverat i beslutsloggen med suffixnummer i ändringsbeslut. Vad som saknas är
att kontrollen skiljer på beslutstyp. Ingen ändring är gjord här; fyndet är
diagnosen, och villkoret för en rättelse ska skrivas innan den körs, på samma
sätt som segmenteringens gjorde.

---

## Kontroll 2 körd, och de sju undantagen handlästa, 2026-09-04

Kontroll 2 i `docs/VILLKORSSCHEMA.md` avsnitt 5 lyder att "noll villkor är bara
tillåtet för förlängningar, igångsättningsbeslut, upphävanden och domar. Ett
tillstånd med noll villkor är per definition en tyst trasig extraktion." Den har
inte kunnat köras tidigare, eftersom typen per beslut saknades. Steg 32 kör den
mot steg 31:s typer.

**Täckningstalet 73 procent var sant och oanvändbart.** Steg 24 rapporterade då
att 173 av 236 filer gick att segmentera; efter rättelsen samma dag är talet 180
av 236. Uppdelat på typ säger materialet något
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

Talen ovan är körningen före rättelsen samma dag, och de står kvar eftersom det
är de som ledde till handläsningen. Efter rättelsen har tillstånd 160 med och 2
utan, ändring 9 med och 31 utan, och villkor 1 med och 1 utan; övriga rader är
oförändrade.

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

**Rättelsen är gjord samma dag, efter att villkoret för den skrivits ned.**
Steg 24 har fått två reservregler: en för den inledande meningen och en som
matchar rubriken som radprefix. Båda används bara när ingen rubrikrad finns i
dokumentet, så inget beslut som redan segmenterade kan förlora ett villkor på
dem. Villkoret för att behålla ändringen skrevs i protokollloggen innan
körningen: inget beslut fick tappa villkor. Utfallet blev sju nya beslut och noll
som tappade.

**Täckningen för tillstånd är därmed 160 av 162.** De två som återstår är just de
två som handläsningen visade riktigt saknar villkor. Tre av de fem återvunna
tillstånden får bruten sifferserie, vilket är instrumentets eget sätt att säga
att extraktionen är ofullständig; de ligger utanför den rena delmängden och kan
inte bära huvudsiffran. De två andra är rena: `361be3bd133c` ger 31 villkor och
`aee6ec54ed25` tolv. Räknat på alla sju nya beslut är fyra brutna, eftersom även
villkorsbeslutet med sitt enda villkor är det.

Vad rättelsen gjorde med de publicerade talen står i avsnittet om
villkorslagrets baseline längre upp, med den gamla tabellen utskriven bredvid
den nya.

### Två frågor kontrollen inte svarar på

**Trettioen av fyrtio ändringsbeslut saknar villkor**, ett färre efter
rättelsen. Regeln uttalar sig inte
om ändringar. Om ett ändringsbeslut bär egna villkor eller bara ändrar ett
villkor i det underliggande tillståndet är en fråga om dokumenten, och att
avgöra den ur frånvaron av en rubrik vore en gissning. `e181f70f9cda` ovan visar
att den andra formen finns.

**Ett beslut som heter "Villkor" eller "Slutliga villkor" saknar villkor.**
Efter rättelsen segmenterar det ena av de två, med ett enda villkor och bruten
sifferserie. Namnet gör dem till de sista man väntar sig hitta tomma. Inget av
dem är läst än.

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

*Tillägg 2026-09-10, efter beslutet att inte överklaga:* KR Göteborg 4309-20,
läst i fulltext i dag, lät lämna ut *"information i handlingarna som gäller
djurägare och djur"* ur handlingar från besiktning inför slakt, med skälet att
den enskilde inte kan antas lida skada. Det försvagar det andra av de tre
skälen mot ett överklagande av Kronoberg, att besättningsstorlek ligger nära
det RÅ 2010 ref. 77 höll hemligt. Avgörandet är från en annan kammarrätt och
en annan sorts handling. Det första skälet, att P9 rangordnar Kronoberg sist
av de sex, och det tredje, not 6:s hellre tystnad än ett förlorat mål, rörs
inte.

**Domstolen är densamma.** Kronobergs län ligger i Kammarrätten i Jönköpings
domkrets, samma domstol som redan har Kalmaröverklagandet som mål 3249-26 och
som får Jordbruksverkets. Det är också den kammarrätt vars dom i 2010 års mål
Regeringsrätten fastställde. Domkretsen är kontrollerad mot två andrahandskällor
som är eniga om Kronoberg, inte mot domstolens egen förteckning, som inte gick
att nå; att Kalmar ligger i samma domkrets är däremot bekräftat av att
Kalmaröverklagandet togs upp där.

*Tillägg 2026-09-22:* domkretsen är nu läst i primärkällan, 1 § och 5 §
förordningen (1977:937), och svaret är detsamma. Se avsnittet om instansen och
prövningstillståndet.

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
