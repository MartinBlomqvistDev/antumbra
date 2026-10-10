# 0026: Utlösaren mäts på villkoren, inte på sidan

Datum: 2026-10-09. Status: beslutad. Ersätter beslutet i
[ADR-0025](0025-ett-textlager-utan-diakriter-ar-ingen-lasning.md), vars regel
mättes och inte infördes.

## Beslut

Steg 24:s val av källa får en andra utlösare, mätt på villkoren. Ett beslut läses
ur projektets egen OCR i stället för ur textlagret när de villkor som steget
segmenterar ur textlagret bär minst 200 bokstäver och inte en enda å, ä eller ö.
Teckenräkningen per sida står kvar som förut och avgör de övriga besluten.

Slår utlösaren till utan att projektet har en egen OCR av beslutet avbryter
steget med ett felmeddelande. Det tysta utfallet, att beslutet lämnar registret
utan att någon ser det, är värre än ett stopp.

Regeln är skriven innan den kördes, och villkoren för att behålla den står
nedan. Faller ett villkor rullas ändringen tillbaka och den här posten får ett
tillägg om utfallet, som ADR-0023 och ADR-0025 fick.

## Sammanhang

Felet är det ADR-0025 beskriver, och den beskrivningen bärs vidare hit:
`13df613f9802` bär inte en enda å, ä eller ö i sina fyra villkor, 981 bokstäver,
därför att producenten klistrat in en teckenläsning över fjorton inskannade
sidor. 58 av 178 ord i de fyra villkoren är fel i registret.

Det som är nytt är var utlösaren mäts. ADR-0025 mätte den på sidorna, och en
sida är fel ställe av två skäl som båda är mätta den 9 oktober 2026:

- **Den träffar beslut vars villkor är felfria.** Sidregeln träffar också
  `3d59186a51bc`, vars åtta villkor bär 4 till 17 diakriter var och alltså är en
  läsning av sidan. Steg 24 väljer källa för hela beslutet, så en träff på en
  sida längst bak flyttar också villkoren längst fram.
- **Den missar den sida felet sitter på.** Alla fyra villkoren i `13df613f9802`
  sitter på sida 20, och den sidan bär 0,23 procent diakriter. Noll-regeln
  träffar sidorna 21 till 33, inte sida 20. Sidmåttet pekar alltså ut rätt
  handling av fel skäl.

Villkoren är dessutom det registret publicerar som citat, så det är den texten
måttet ska läggas på.

**Svepet över korpusen, kört före beslutet.** Av de 236 besluten har 123 ett
textlager och villkor som går att segmentera ur det. Utlösaren träffar ett enda
av dem, `13df613f9802`, med 0,0000 diakriter på 981 bokstäver. Nästa beslut i
ordningen ligger på 0,0426, `f61b323aa3c2`, och korpusens median på 0,0540. Det
finns alltså ingen gränsdragningsfråga i intervallet: varje tröskel mellan noll
och fyra procent väljer ut samma enda handling.

## Skäl

Registret lovar ordagrannhet. Ett villkor där var tredje ord är felstavat är
inte ett citat, och det kan inte heller matcha ett likalydande villkor i ett
annat beslut, vilket är vad måttet på delad text mäter. Valet står mellan två
läsningar som båda har fel, och de är fel i olika storleksordning: textlagret i
58 ord av 178, OCR i en handfull tecken.

Regeln är formulerad som en utlösare och inte som ett undantag för en fil.
Projektet har ingen hand-lagd lista över filer som ska läsas annorlunda, och en
sådan lista hade varit omöjlig att granska utifrån. Att måttet nu ligger på
villkoren gör den smalare än ADR-0025:s, inte vidare: den rör bara den text
steget faktiskt lagrar.

## Förregistrerade villkor

1. Exakt fyra villkor i registret byter text, alla i `13df613f9802`. Byter något
   annat besluts villkor text rullas ändringen tillbaka.
2. Antalet villkor i `13df613f9802` är fyra före och efter. Blir de fler eller
   färre segmenterar OCR-texten annorlunda, och då är det en egen fråga som ska
   mätas innan registret byter källa.
3. De fyra texterna bär å, ä och ö efter bytet.
4. Inget annat beslut byter fält `källa`.
5. Summorna 2 347 villkor och 1 655 med rubrik rör sig bara om villkor 2 faller,
   och i så fall redovisas de nya talen i `VERIFIERAT.md` tillsammans med skälet.

## Följder

`13df613f9802` flyttar från den digitalfödda halvan till OCR-halvan, och därmed
från ett mått med två oberoende läsningar till ett med en. Det är samma läge som
de 72 övriga OCR-besluten står i, och kontroll 3 redovisar den halvan som den
svagare kontrollen den är. Steg 39:s mätning av just det här beslutet blir
samtidigt en jämförelse av OCR mot sig själv och upphör att vara ett oberoende
prov; talet står kvar som det mättes, med den reservationen.

Kontroll 3, avhuggningen och talen om delad text räknas om, och de tal som rör
sig skrivs ut i `VERIFIERAT.md`. Åtagandet om sidfoten i villkor 4 faller ut av
bytet: sidfotens rader är förvanskade av det inklistrade lagret, och ur
projektets OCR träffar tre av fem rader befintliga markörer.

## Alternativ som avvisas

**Sidregeln i ADR-0025.** Mätt och inte införd, av skälen i tillägget till den
posten.

**En regel på helsidesbild.** Fjorton av de 236 besluten har minst en sida som
är helt täckt av en bild och ändå bär text, och 163 villkor kommer från dem. För
elva av de fjorton går det inte att avgöra med det svepet om textlagret är
producentens teckenläsning eller filens eget: en helsidesbild kan också vara ett
inskannat brevhuvud eller en stämpel under ett äkta textlager. En regel på den
grunden hade bytt källa för 163 villkor på ett underlag som inte räcker. Frågan
är värd ett eget mått och står öppen.

**Att rätta de fyra raderna för hand.** Det ger rätt text och fel metod:
registret byggs av ett steg, och en hand-lagd rad går inte att bygga om.

**Att låta det stå.** Då publicerar registret 58 felstavade ord som citat ur ett
myndighetsbeslut, och måttet på delad text räknar fyra villkor som unika av ett
skäl som ligger i filen och inte i besluten.

## Tillägg 2026-10-10: villkor 2 faller, och orsaken är mätt

Regeln kördes natten till den 10 oktober 2026, och fyra av de fem
förregistrerade villkoren håller:

- Fyra rader i registret byter text, alla fyra i `13df613f9802`, och inget
  annat beslut byter vare sig text eller fält `källa`. Villkor 1 och 4 håller
  som de är skrivna; det som tillkommer är tolv nya rader, och det är villkor 2
  som fångar dem.
- De fyra texterna bär 8, 10, 21 och 24 diakriter efter bytet. Villkor 3 håller.

**Villkor 2 faller.** `13df613f9802` har fyra villkor före bytet och sexton
efter: numren 1 till 15, och en rad numrerad 20 på 2 981 tecken. Registret växer
från 2 347 till 2 359 villkor och från 1 655 till 1 667 med rubrik, vilket är de
tal villkor 5 kräver att få se.

Orsaken är inte OCR-segmentering, utan att textlagret var en **stympad** läsning
och inte bara en felstavad. Villkorsfönstret ur textlagret är 39 rader och slutar
i beslutets egen sidfot, läst som `Ostqotaqatan 3` och `E-DOSt:`. ADR-0021:s
regel bär ett villkor över en sidbrytning genom att känna igen sidhuvudet som
block, och ett huvud vars ord är förvanskade känns inte igen. Fönstret stängde
därför vid den första sidbrytningen, och läsningen slutade vid villkor 4 av ett
tjugotal. Numrerade radstarter finns i textlagret på sidorna 14, 21, 22 och 34,
så villkoren fanns i filen men utanför fönstret.

Raden numrerad 20 bär texten i villkoren mellan 16 och 20 i ett stycke. Den
formen är inte ny i registret: 51 av 180 beslut har en bruten serie, 36 av dem
OCR-lästa, 79 rader har ett nummer som hoppar över minst ett steg, 62 av dem i
OCR-lästa beslut, och 32 rader är längre än 1 500 tecken, den längsta 3 192
tecken i ett annat OCR-läst beslut.

Villkor 2 säger att ett ändrat antal är en egen fråga som ska mätas innan
registret byter källa. Frågan är mätt ovan och avgörs i
[ADR-0027](0027-den-stympade-lasningen-forklarar-villkorsantalet.md).
