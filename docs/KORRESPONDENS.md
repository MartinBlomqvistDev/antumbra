# Korrespondensregistret: allt som styr det, på ett ställe

Registret är `data/korrespondens.jsonl`. Den här filen finns för att reglerna
annars ligger i fem: projektets CLAUDE.md, `BEGARANMALL.md` avsnitt 7,
`VERIFIERAT.md`, ADR-0003 och ADR-0018. **Läs den här filen, inte de fem, när
du arbetar i registret.** Ändras en regel ändras den här och på sitt
ursprungliga ställe.

## Vad registret är och vad som binder det

P12-breven, avsända 2026-10-02, lovar att det publicerade materialet rymmer
*"hela handläggningsprotokollet och hela korrespondensloggen, alltså också de
mejl ni har skickat i de här ärendena, ordagrant"*. Två ord i den meningen
styr allt annat.

*I de här ärendena* avgränsar till begäran A, B och C och de fyra
överklagandena. Förarbete ligger utanför, markerat i förteckningen med skäl.

*Hela* är ett löfte om fullständighet. Ett ofullständigt register kan inte
publiceras under den rubriken, och hur långt det är kommet står i
`VERIFIERAT.md`, läst ur filerna av en invariant.

## Arbetsgången, i ordning

1. **Nästa meddelande** läses ur `data/korrespondens_forteckning.jsonl`, äldst
   först. Förteckningen är brevlådan gången igenom tråd för tråd, och den är
   byggd om en gång sedan en arbetslista visade sig avhuggen.
2. **Hämta det** med `get_message` och `PLAIN_TEXT`. `MINIMAL` räcker för att
   se vad ett meddelande är, men inte för att återge det ordagrant.
3. **Spara råsvaret** till `data/korrespondens_raw/<id>.json`, orört. Det är
   gitignorerat och bär personuppgifter (ADR-0024).
4. **Kör steg 44.** Det räknar svensk tid ur meddelandehuvudet, tar bort
   länkmål, kapar citerad historik och kapar signaturblocket där signaturen
   namnger en person. Står det ett enda ord under hälsningen stannar
   steget: ordet kan vara ett förnamn, en titel eller enheten själv, och
   bedömningen skrivs som en rad i `data/korrespondens_signaturer.jsonl`
   med `signaturen` satt till `namn` eller `befattning eller enhet`. Filen
   bär bedömningen och aldrig ordet (ADR-0024).
5. **Skriv raden** med det som är omdöme: myndighet, roll, bilagor och de
   anmärkningar som bara en läsare kan göra, till exempel att en felstavning
   står som myndigheten skrev den.
6. **Logga** eventuella autosvar som saknas i protokollloggen. Bär brevet
   ett besked som hör i en egen tabell, till exempel länets tal på
   nämnarfrågan, förs det in där också och det steg som läser tabellen
   körs om.
7. **Uppdatera talet** i `VERIFIERAT.md`.
8. **Grindarna**, var och en som sitt eget kommando med exitkoden läst:
   `ruff check .`, `ruff format --check .`, `pytest`. Aldrig i ett rör och
   aldrig i en kedja som låter commit följa oavsett utfall.
9. **Commit och push**, och läs CI efteråt. Stega hela arbetskopian, aldrig
   en enskild sökväg: steg 5 skriver i `data/` och steg 7 i `docs/`, så en
   `git add data/` lämnar talet kvar och CI faller på invarianten fast
   pytest var grön lokalt.

## Reglerna per fält

**`datum` och `klockslag`** är meddelandehuvudets tid omräknad till svensk,
alltså UTC plus två timmar för hela perioden augusti till oktober 2026. Tid
läses ur källan och hittas aldrig på.

**`myndighet`** läses ur brevets eget adressblock. Den härleds aldrig ur en
personlig adress förnamn.efternamn, eftersom det är att gissa.

**`avsandare`** är antingen `funktionsbrevlåda` eller `namngiven tjänsteman`
och ingenting annat.

**`roll`** är den befattning eller funktion brevet självt undertecknas med, med
brevets egen lydelse. Den översätts inte till närmaste befattning: Västmanland
skriver *Administrativ handläggare*, inte *administratör*. Namnges ingen person
är rollen ändå myndighetens egen uppgift om vem som hanterar ärendet.

**`text`** är ordagrann. Ingen sammanfattning, ingen karaktärisering, ingen
rättning av stavning eller av myndighetens egna tal.

**`utelamnat`** säger vad raden lämnar ute och varför. Tre saker utelämnas
regelmässigt: den citerade historiken, signaturblockets personuppgifter enligt
ADR-0018, och länkmålen. Myndighetens egen funktionsbrevlåda, växel och
webbadress står kvar, eftersom de är publicerade kontaktuppgifter och inte en
enskilds.

**`forekomster`** bär en brevlådas stående autosvar när texten är identisk
tecken för tecken. En förekomst måste bära meddelandets `sizeEstimate` ur
API-svaret, som bevis på att meddelandet är hämtat och inte antaget identiskt.

## Vad som aldrig görs

Ingen enskild tjänstemans namn återges, varken i signaturen eller i brödtexten;
en invariant i `tests/` fäller en rad där ett namn står kvar. Ingen uppgift om
en enskild djurhållare förs in. Och ingen slutsats dras ur en förteckning över
källan i stället för ur källan: det felet gjordes den 7 oktober 2026 i en
rättelse av protokollloggen, och rättelsen fick återtas dagen därpå.

## Invarianterna som vaktar registret

Fem i `tests/test_repository_invariants.py`:

1. Varje rad bär meddelande-id och säger vad den utelämnar; inget namn utan
   roll och ingen personlig adress.
2. Avsändarfältet håller sig till de två tillåtna värdena.
3. Ingen rad bär en rad som ser ut som en persons namn.
4. Varje registrerat meddelande, förekomsterna inräknade, paras mot en loggad
   händelse i protokollloggen.
5. Registret mäts mot förteckningen, ingenting utanför avgränsningen står i
   det, och talet i `VERIFIERAT.md` stämmer med filerna.
