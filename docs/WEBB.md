# Webbplatsen: från siffra till källa på två klick

Plan i tre iterationer, 2026-08-05. De två första varven redovisas eftersom
deras fel formade det tredje; att stryka dem vore att dölja hur beslutet
fattades.

## Varv 1, fällt: portalen

Dashboard, sökruta och metodsida i var sin flik. Fälldes för att tre verktyg
utan berättelse är ingens sida, och för att en chatt-UI bjuder in till den
läsning retrievallagret inte tål: modellen matchar ämne, inte polaritet
(docs/DGSANTE.md), och en fråga om brister kan få beröm till svar.

## Varv 2, fällt: berättelsen först

En lång scrollberättelse med verktygen som fördjupning. Fälldes för att
berättelsen inte får skrivas före datan: de svenska svaren är inte inne och
analysen inte gjord, och en story före resultat bryter projektets egen regel.
Arvet från varvet: sidan måste ha en tes, inte bara innehåll.

## Varv 3, beslutat: kedjan som tes

Det unika är kedjan: varje aggregat vilar på rader, varje rad på ett
ordagrant stycke, varje stycke på ett dokument med sha256. Sidans princip är
att läsaren alltid kan klicka sig från ett tal till den exakta meningen hos
källan.

| Sida | Innehåll |
| --- | --- |
| Hem | En mening om mätbarhet, tre levande tal, ett klickbart kedje-exempel |
| /jamforelse | BI-vyn; EU-lagret först, länsjämförelsen när den finns; tabellvy vid varje diagram; "visa underlaget" vid varje stapel |
| /uppslag | Retrieval som uppslagsverk, inte chatt: sökruta, land- och årsfilter, klickbara exempelfrågor; svar är alltid ordagranna citat med land, referens och styckenummer; stående banderoll om att sökningen hittar ämnen, aldrig slutsatser |
| /metod | Protokollet, händelseloggen i sin helhet, ADR-indexet, AI-deklarationen, de förskrivna nollresultaten |
| /handlingar | Leveransmanifest, avgiftsstopp, vad som inte lämnats ut och varför |

**Form:** inga kakor, ingen spårning, ljust och mörkt läge, validerad palett
(#2A78D6/#EB6834 med mörklägesvarianter), "Vad sidan inte visar" på varje
resultatsida. Frånvaron av spårning och närvaron av begränsningar är
trovärdighetssignaler mot myndighetsläsaren, inte bara etik.

**Teknik:** Next.js statiskt på Cloudflare för allt utom söket; retrieval
som FastAPI på Cloud Run scale-to-zero med embeddingsmatrisen och
all-MiniLM-L6-v2 i containern. Exempelfrågornas svar bakas statiskt så att
kall start aldrig möter första besöket. Vilokostnad noll.

**Fasning, låst till protokollet:**

1. Fas 0, nu: byggs lokalt i privata repot; ingenting publiceras.
2. Fas 1, tidigast dag 40: EU-lagret, /uppslag, /metod med loggen;
   antumbra.org registreras först här.
3. Fas 2, när den svenska analysen är klar: /jamforelse får
   länsdimensionen, och först därefter skrivs hemsidans berättelse.

**Hero-exemplet:** en förifylld riktig fråga ("cattle were not stunned
effectively before slaughter") som ger tre länders ordagranna svar; besökaren
gör själv den verifikation som är projektets poäng.
