# Verifierat

Allt här är kontrollerat mot primärkälla med angivet datum och faktiska anrop.
**Härled inte om det och sök inte på nytt.** Är något osäkert står det utskrivet.

---

## Kravkorpusen: Jordbruksverkets tillstånd och domar

Verifierat 2026-08-01 mot
`jordbruksverket.se/kontroller-och-tillsyn/miljo/stora-anlaggningar-for-uppfodning-av-fjaderfa-och-gris/tillstand-och-domar-for-stora-gris--och-fjaderfaanlaggningar`

- **237 PDF-beslut**, 2013 till 2026. Totalt 0,87 GB, median 1,6 MB.
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

**Textlager, stickprov om elva testade med `pdftotext -layout`:** ungefär hälften
digitalt födda och extraherar rent, hälften inskannade och ger noll tecken.
Filstorleken avslöjar vilket: digitala 150 kB till 650 kB, skannade 5 till
9,5 MB. 42 procent av alla ligger under 1 MB. **OCR krävs för ungefär halva
korpusen.** Ingen OCR-motor installerad lokalt per 2026-08-02.

**Filnamnen är gratis metadata:** `Kommun_Bolag_Djurslag_Typ_Datum`. Inte helt
konsekvent, men kommun, verksamhetsutövare och beslutsdatum går att läsa utan
att öppna filen. **Flera filnamn innehåller privatpersoners namn**
i formen `Kommun_Förnamn_o_Förnamn_Efternamn`; minst tre av de 237 gör det.
Namnen återges inte i repot, och källfilerna ligger utanför versionshanteringen.

Uppskattat cirka 7 000 sidor och i storleksordningen 3 000 enskilda villkor.
Inte stor data i volym, men **hela populationen, inte ett urval.**

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
- Djurens Rätt gör motsvarande årligen i Kycklingkartläggningen på Kronfågel,
  Guldfågeln, Torsåsens och Atria. 2024: minst 56 000 kycklingar.

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
