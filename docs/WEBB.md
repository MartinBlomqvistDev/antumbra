# Webbplatsen: från siffra till källa på två klick

Plan beslutad 2026-08-05.

## Tesen

Det som skiljer Antumbra från varje annan tillsynssida är kedjan: varje
aggregat vilar på rader, varje rad på ett ordagrant stycke, varje stycke på
ett dokument med sha256. Sidans bärande princip är att läsaren alltid kan
klicka sig från ett tal till den exakta meningen hos källan. Principen är
samtidigt användarvänlighetens (läsaren behöver aldrig lita, bara klicka),
slagkraftens (ingen annan gör det) och ärlighetens (varje påstående bär sitt
belägg).

## Struktur

| Sida | Innehåll |
| --- | --- |
| Hem | En mening om mätbarhet, tre levande tal, ett klickbart kedje-exempel |
| /jamforelse | BI-vyn: EU-lagret först, länsjämförelsen när den finns; tabellvy vid varje diagram; "visa underlaget" vid varje stapel |
| /uppslag | Retrieval som uppslagsverk, inte chatt: sökruta, land- och årsfilter, klickbara exempelfrågor; svar är alltid ordagranna citat med land, referens och styckenummer; stående banderoll om att sökningen hittar var ett ämne behandlas, aldrig vad som konstaterats |
| /metod | Protokollet, händelseloggen i sin helhet, ADR-indexet, AI-deklarationen, de förskrivna nollresultaten |
| /handlingar | Leveransmanifest, avgiftsstopp, vad som inte lämnats ut och varför |

## Avfärdade utformningar

**Portal med verktygen i flikar:** tre verktyg utan berättelse är ingens
sida, och en chatt-UI bjuder in till den läsning retrievallagret inte tål,
eftersom modellen matchar ämne och inte polaritet (docs/DGSANTE.md).

**Berättelsedriven scrollsida:** berättelsen får inte skrivas före datan; de
svenska svaren är inte inne och analysen inte gjord. Hemsidans berättelse
skrivs i fas 2, efter resultaten.

## Form

Inga kakor, ingen spårning, ljust och mörkt läge, den validerade paletten
(#2A78D6/#EB6834 med mörklägesvarianter), tabellalternativ till varje
visualisering, och "Vad sidan inte visar" på varje resultatsida. Frånvaron
av spårning och närvaron av begränsningar är trovärdighetssignaler mot
myndighetsläsaren, inte bara etik.

## Teknik

Next.js statiskt på Cloudflare för allt utom söket. Retrieval som FastAPI på
Cloud Run scale-to-zero med embeddingsmatrisen och all-MiniLM-L6-v2 i
containern; CPU räcker. Exempelfrågornas svar bakas statiskt så att en kall
start aldrig möter första besöket. Vilokostnad noll.

## Fasning, låst till protokollet

1. **Fas 0, nu:** byggs lokalt i privata repot; ingenting publiceras.
2. **Fas 1, tidigast dag 40:** EU-lagret, /uppslag och /metod med loggen;
   antumbra.org registreras först här.
3. **Fas 2, när den svenska analysen är klar:** /jamforelse får
   länsdimensionen, och först därefter skrivs hemsidans berättelse.

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
