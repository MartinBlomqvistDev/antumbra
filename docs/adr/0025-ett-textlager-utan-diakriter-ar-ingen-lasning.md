# 0025: Ett textlager utan å, ä och ö är ingen läsning av sidan

Datum: 2026-10-09. Status: beslutad.

## Beslut

Steg 24:s val av källa får en andra utlösare. Ett beslut läses ur projektets
egen OCR i stället för ur textlagret när textlagret på någon sida bär minst 200
bokstäver och inte en enda å, ä eller ö. Teckenräkningen per sida står kvar som
förut och avgör de övriga besluten.

Regeln är skriven innan den kördes, och villkoren för att behålla den står
nedan. Faller ett villkor rullas ändringen tillbaka och den här posten får ett
tillägg om utfallet, som ADR-0023 fick.

## Sammanhang

`13df613f9802` bär inte en enda å, ä eller ö i sina fyra villkor, 981 bokstäver.
Steg 24 valde textlagret, eftersom teckenräkningen per sida är uppfylld, och ett
andra bibliotek läser samma stympade tecken, så varken kontroll 3 eller steg 33
kunde se felet. Steg 39 mätte i stället villkoren mot en OCR-läsning av den
tryckta sidan och visade att orden håller: vikt median 0,922 och ingen rad under
0,50, mot ett villkor som skrevs före körningen.

Den 9 oktober 2026 mättes orsaken, och den är inte ett typsnitt utan en annan
handling inne i filen:

- Sidorna 20 till 33 bär var sin bild som täcker hela sidan, bildytan 1,00 av
  sidan. Sidorna 1 till 19 och 34 ligger på 0,00 till 0,02.
- Diakriterna följer samma gräns: 5,4 till 7,3 procent på de digitalfödda
  sidorna, 0,23 procent på sida 20 och noll på sidorna 21 till 33.
- Felen är en teckenläsares: sju ord i blocket bär q där svenska har g, och ett
  av dem bär tre fel på en gång, `bedornnlnq` för *bedömning*, med rn för m, l
  för i och q för g.
- Alla fyra villkoren sitter på sida 20, alltså på en inskannad sida.

Textlagret på de sidorna är därmed en teckenläsning som producenten klistrat in,
inte filens egen. Av 178 ord i de fyra villkoren är 58 fel i registret, nämligen
varje ord som bär en diakrit, och två av felen är grövre: `rar` för *får* och
`jarnn` för *jämn*. Projektets egen OCR av beslutet ligger på 6,02 procent
diakriter, vid korpusens median, och har egna fel: `(>2594` för `(>25%` och punkt
för komma på tre ställen.

**Svepet över korpusen, kört före beslutet.** Utlösaren träffar två av de 236
besluten: `13df613f9802` med tretton sidor och 30 140 bokstäver, och
`3d59186a51bc` med fem sidor och 1 674 bokstäver. I det andra beslutet sitter
alla åtta villkoren på sidorna 1 och 2, som är digitalfödda, så där byter
registret ingen text även om beslutet byter källa. Skadan i registret är alltså
fyra villkor av 2 347.

## Skäl

Registret lovar ordagrannhet. Ett villkor där var tredje ord är felstavat är
inte ett citat, och det kan inte heller matcha ett likalydande villkor i ett
annat beslut, vilket är vad måttet på delad text mäter. Valet står mellan två
läsningar som båda har fel, och de är fel i olika storleksordning: textlagret i
58 ord av 178, OCR i en handfull tecken.

Regeln är formulerad som en utlösare och inte som ett undantag för en fil.
Projektet har ingen hand-lagd lista över filer som ska läsas annorlunda, och en
sådan lista hade varit omöjlig att granska utifrån.

## Förregistrerade villkor

1. Exakt fyra villkor i registret byter text, alla i `13df613f9802`. Byter något
   annat besluts villkor text är orsaken okänd och ändringen rullas tillbaka.
2. Antalet villkor i `13df613f9802` är fyra före och efter. Blir de fler eller
   färre segmenterar OCR-texten annorlunda, och då är det en egen fråga som ska
   mätas innan registret byter källa.
3. De fyra texterna bär å, ä och ö efter bytet.
4. Summorna 2 347 villkor och 1 655 med rubrik rör sig bara om villkor 2 faller,
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

**Att rätta de fyra raderna för hand.** Det ger rätt text och fel metod:
registret byggs av ett steg, och en hand-lagd rad går inte att bygga om.

**En regel på helsidesbild i stället för på diakriter.** Fjorton av de 236
besluten har minst en sida som är helt täckt av en bild och ändå bär text, och
163 villkor kommer från dem. För elva av de fjorton går det inte att avgöra med
det här svepet om textlagret är producentens teckenläsning eller filens eget: en
helsidesbild kan också vara ett inskannat brevhuvud eller en stämpel under ett
äkta textlager. En regel på den grunden hade bytt källa för 163 villkor på ett
underlag som inte räcker. Frågan är värd ett eget mått och står öppen.

**Att låta det stå.** Då publicerar registret 58 felstavade ord som citat ur ett
myndighetsbeslut, och måttet på delad text räknar fyra villkor som unika av ett
skäl som ligger i filen och inte i besluten.
