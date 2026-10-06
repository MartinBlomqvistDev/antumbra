# Webbplatsen: från siffra till källa på två klick

Plan beslutad 2026-08-05, utökad till fullt omfång 2026-08-06.

## Tesen

Det som skiljer Antumbra från varje annan tillsynssida är kedjan: varje
aggregat vilar på rader, varje rad på ett ordagrant stycke, varje stycke på
ett dokument med sha256. Sidans bärande princip är att läsaren alltid kan
klicka sig från ett tal till den exakta meningen hos källan. Principen är
samtidigt användarvänlighetens (läsaren behöver aldrig lita, bara klicka),
slagkraftens (ingen annan gör det) och ärlighetens (varje påstående bär sitt
belägg).

Kedjan är inte en finess per sida utan en komponent som byggs en gång:
underlagets JSON-form och interaktionen siffra → rad → stycke → hash
designas före varje diagram, och återanvänds på Hem, /jamforelse och
/handlingar. Varje ny visualisering blir därmed billig och automatiskt
belagd.

## Struktur

Omdisponerad 2026-08-07: den svenska undersökningen är sajtens fokus och
fick en egen sida näst först i menyn; EU-lagret heter uttryckligen
EU-jämförelsen. Hem leder med den svenska mätningen och visar två
sifferrader, Sverige först. Ingen svensk analys publiceras i förtid:
/sverige visar mätningens uppbyggnad och processen i realtid ur loggen,
resultaten kommer när insamlingen är stängd.

| Sida | Innehåll |
| --- | --- |
| Hem | Svensk kicker, tesen, två sifferrader: den svenska insamlingen (levande ur loggen) och EU-lagret; kedjeexemplet interaktivt: klicka talet, se raderna, klicka raden, se stycket markerat med referens och hash |
| /sverige | Undersökningens uppbyggnad (tre likalydande begäranden, protokollstyrd hantering), läget i siffror ur loggen, begärandenas exakta lydelser, avgiftsstoppen; länsjämförelsens resultat när insamlingen stängts |
| /jamforelse | Hela BI-vyn: land/år/ämnes-matris, small multiples, citeringsgrafen som egen vy (96 % upplösta citeringar över 4 690 revisioner, uppföljningskedjor land för land); tabellvy, "visa underlaget" och "Vad sidan inte visar" vid varje diagram; länsdimensionen läggs ovanpå samma komponenter i fas 2 |
| /uppslag | Retrieval som uppslagsverk, inte chatt: sökruta, land- och årsfilter, bakade exempelfrågor; svar är alltid ordagranna citat med land, referens och styckenummer, och länkar vidare till revisionens post; omgivande stycken på begäran, fortfarande ordagrant; stående banderoll om att sökningen hittar var ett ämne behandlas, aldrig vad som konstaterats |
| /metod | Protokollet, händelseloggen renderad som filtrerbar tidslinje per län, ADR-indexet, AI-deklarationen, de förskrivna nollresultaten, korrigeringsloggen |
| /handlingar | Leveransmanifestet, och en statustavla per län: dagar till leverans, avgiftshållning, maskningspraxis, bilagepraxis; tavlan är mätningen, och blir i fas 2 det svenska resultatets hemvist |
| /data | Nedladdningsbara aggregat, schemadokumentation, licens, länk till HF-datasetet; granskningsbar utifrån betyder att vem som helst kan räkna om |

**Språk:** svenska primärt. Engelsk spegel av EU-lagrets sidor (Hem,
/jamforelse, /uppslag, /metod) med content-filer per språk som aldrig
redigeras enskilt. De svenska resultatsidorna förblir svenska; mottagarna är
svenska myndigheter.

## Avfärdade utformningar

**Portal med verktygen i flikar:** tre verktyg utan berättelse är ingens
sida, och en chatt-UI bjuder in till den läsning retrievallagret inte tål,
eftersom modellen matchar ämne och inte polaritet (docs/DGSANTE.md).

**Berättelsedriven scrollsida:** berättelsen får inte skrivas före datan; de
svenska svaren är inte inne och analysen inte gjord. Hemsidans berättelse
skrivs i fas 2, efter resultaten.

**Nedskalad fas 1** (färre sidor, bantad BI-vy, avvägd mot jobbsökandets
kalender): avfärdad 2026-08-06. Sajten byggs på projektets premisser i full
omfattning; jobb- och nätverksmålen följer av det, inte tvärtom.

## Form

Inga kakor, ingen spårning, ljust och mörkt läge, den validerade paletten
(#2A78D6/#EB6834 med mörklägesvarianter), tabellalternativ till varje
visualisering, och "Vad sidan inte visar" på varje resultatsida. Frånvaron
av spårning och närvaron av begränsningar är trovärdighetssignaler mot
myndighetsläsaren, inte bara etik.

Kvalitetsribbor utöver detta: WCAG 2.1 AA uttryckligen, eftersom en sajt
riktad till myndigheter som själv uppfyller DOS-lagens nivå är en
trovärdighetssignal i sig; palettvalidatorn körd för både ljust och mörkt
läge; allt utom livesöket fungerar utan JavaScript; utskriftsstilmall,
eftersom läsekretsen skriver ut; sökfrågor loggas inte, och det sägs på
sidan.

## Teknik

Next.js statiskt på Cloudflare för allt utom söket, enligt samma mönster som
kattochkod (statisk export, assets-only Worker, bygge vid push). Retrieval
som FastAPI på Cloud Run scale-to-zero; tjänsten importerar `src/retrieval`
rakt av så att verbatimgarantin och stale-vakten gäller även via HTTP.
Embeddingsmatrisen och all-MiniLM-L6-v2 i containern; CPU räcker.
Exempelfrågornas svar bakas statiskt genom samma kodväg så att en kall start
aldrig möter första besöket. Vilokostnad noll. Billing aktiveras på
antumbra-504411, vilket samtidigt lyfter BigQuery-sandlådans
60-dagarsutgång.

## Det övriga publika avtrycket

- **README på engelska** med tvåminuterstestet som färdigkriterium: vad och
  varför i ett stycke, kedjeprincipen, resultaten hittills,
  arkitekturskiss, stacken, reproducerbarhet steg för steg, skärmdumpar av
  Power BI och sajten.
- **CITATION.cff** så att projektet är citerbart som forskningsartefakt.
- **Licenser:** AGPL-3.0 för kod, CC BY 4.0 för data.
- **GitHub-metadata** svept enligt ytlistan: reponamn, beskrivning, topics,
  pinnad plats.
- **Power BI:** `.pbix` i repot enligt docs/POWERBI.md över EU-lagret,
  skärmdumpar i README. Står i projektets stackdeklaration och byggs
  därefter.
- **HF-dataset:** korpusen som `MartinBlomqvist/dgsante` med styckena,
  rekommendationerna och citeringsgrafen, dataset-kort enligt
  hewb-standarden. Kommissionens dokument är återanvändbara med attribution
  (beslut 2011/833/EU); licensraden verifieras före publicering.

## Byggplan

Två klockor styr ordningen: BigQuery-sandlådan går ut runt 2 oktober, så
exporten görs först och siten är därefter GCP-fri i bygget; protokollet
tillåter ingenting publikt före dag 40 (måndag 28 september).

**Tillägg 2026-10-06: båda klockorna har ändrats, och ingen av dem står
kvar som den skrevs.** Faktureringen aktiverades 2026-08-06 och samma dag
verifierades att inget dataset och ingen tabell i `antumbra-504411` har
någon utgångstid, så sandlådans sextio dagar gäller inte och exporten är
inte längre tidsstyrd. Publiceringsgolvet flyttades av tillämpningsnot 8,
som slår fast att öppnandet av en yta är publicering enligt P12: dag 40 är
inte längre datumet, utan dagen efter att P12:s tre veckor löpt ut. P12
gick 2026-10-02 med svarstid till den 23 oktober, så varje *tidigast dag
40* i det här dokumentet ska läsas som tidigast lördag 2026-10-24.
Ordningen på publiceringsdagen står i `docs/PUBLICERING.md`.

1. **AP1 Dataexport:** aggregat per land/år/ämne, underlag per land på
   styckenivå som separata filer, korpusartefakterna för HF-datasetet;
   committad JSON med manifest och radantal, rerunnbar.
2. **AP2 Skelett:** `web/`, sv/en-contentstruktur, sex sidor ruttade,
   palett-tokens, ljust/mörkt läge.
3. **AP3 Kedjekomponenten:** siffra → rad → stycke → hash, byggd en gång,
   testad mot exporten.
4. **AP4 /uppslag:** FastAPI-tjänsten, bakade exempelsvar,
   end-to-end-testet återanvänt mot tjänsten, frontend med banderoll.
5. **AP5 /jamforelse:** diagramkomponenter i egen SVG enligt
   dataviz-proceduren, citeringsgrafvyn, validerad palett.
6. **AP6 /metod och /handlingar:** tidslinjen, statustavlan.
7. **AP7 Hem:** plockar ur allt ovan.
8. **AP8 Power BI.**
9. **AP9 README på engelska, CITATION.cff, licenser, GitHub-metadata.**
10. **AP10 HF-dataset med kort.**
11. **Lanseringschecklista, tidigast dag 40:** PII-svep över hela ytlistan,
    författarskapsrevision på hela historiken, antumbra.org registreras,
    Cloudflare- och Cloud Run-deploy, LinkedIn-post.
12. **Fas 2:** länsdimensionen på /jamforelse och /handlingar, den svenska
    berättelsen, outreach till journalister och Statskontoret i god tid
    före 31 mars 2027.

Omfattning: fem till sju veckors arbete i lugn takt, vilket landar färdigt
ungefär vid dag 40 om AP1 startar nu.

## Fasning, låst till protokollet

1. **Fas 0, nu:** byggs lokalt i privata repot; ingenting publiceras.
2. **Fas 1, tidigast dag 40:** EU-lagret i full bredd enligt byggplanen;
   antumbra.org registreras först här.
3. **Fas 2, när den svenska analysen är klar:** länsdimensionen, den
   svenska berättelsen, outreach.

## Hero-exemplet

En förifylld fråga i ämnesform: **"advance notice of farm inspections"**.
Den ger bland annat Lettland ("it is standard practice to provide farmers
with brief advance notice of the inspection, typically on the morning it is
scheduled", CT-2025-0182 §82) och Frankrike ("inspections are usually
announced unless there are specific grounds", 2019-6651 §70) ordagrant.

Valet är motiverat i tre led: frågan är ämnesformad och modellerar därmed
rätt användning av sökningen i stället för att exponera polaritetsgränsen;
ämnet är administrativt neutralt så att första intrycket är mätning och inte
agenda; och den kopplar rakt till projektets svenska fråga om föranmälda
kontroller, där Jordbruksverkets siffror den dag de finns kan stå bredvid
EU-citaten. En påståendeformad och laddad kandidat ("cattle were not stunned
effectively before slaughter") avfärdades på samtliga tre grunder.
