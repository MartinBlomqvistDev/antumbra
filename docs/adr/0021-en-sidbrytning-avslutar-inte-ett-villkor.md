# 0021: En sidbrytning avslutar inte ett villkor

Datum: 2026-09-05. Status: beslutad.

## Beslut

Steg 24 behandlar en tomrad i textlagret som en möjlig sidbrytning i stället för
som en gräns. Sidhuvudet efter brytningen identifieras som ett block och hoppas
över i varje läge, och ett villkor vars egen mening inte är avslutad fortsätter
på andra sidan blocket. Ett villkor som slutat på en fullständig mening stängs
där, och blocket hoppas över ändå, så att en löpande sidrubrik inte kan
registreras som rubrik för det som följer.

En rad räknas som sidhuvud bara när varje ord i den är ett huvudord, ett tal
eller ett diarienummer, och ett block hoppas över bara när minst en av dess
rader bar ett huvudord. Orden står i `PAGE_HEAD_WORDS`, taket för blockets höjd
i `MAX_HEAD_LINES`. Som avslutad mening räknas bara punkt, utropstecken,
frågetecken och avslutande citattecken; kolon och parentes gör det inte.

## Sammanhang

Kontroll 3 i VILLKORSSCHEMA avsnitt 5 kördes för första gången den 5 september
2026, i steg 34, och läste varje lagrat villkor tillbaka mot dokumentet läst med
ett annat bibliotek. Två av de förregistrerade villkoren föll direkt.

Det första fyndet var stort. En tomrad i pymupdfs textlager är en sidbrytning
lika ofta som ett mellanrum mellan två villkor, och segmenteraren stängde alltid
villkoret där. Allt som stod efter brytningen föll då bort utan spår, i **209
villkor i 126 beslut**, alltså i mer än två tredjedelar av korpusen, och varje
gång mitt i en mening. Ett exempel ur `0927347cbc18` villkor 4: den lagrade
texten slutade "ska minst motsvara det totala" och dokumentet fortsatte
"behovet av spridningsareal för den mängd stallgödsel som djurhållningen ger
upphov till."

Tre fel i samma familj kom fram när det första lagades. Sidhuvudet kommer
ibland utan tomrad före sig och lästes då som villkorstext. Sidhuvudets länsnamn
stod inte i ordlistan, så överhoppningen slutade mitt i huvudet och tog
länsnamnet, datumet och diarienumret med sig in i texten. Ett villkorsnummer
sist på en sida gav en tom text som lästes som en avslutad mening, vilket
lämnade själva villkoret utan hem i sju OCR-lästa beslut.

Det andra av dessa fel hade en följd som inte är statistisk. I `1c8347c55318`
villkor 4 följdes villkorstexten av ett bifogat rättelsebeslut med två
namngivna tjänstemän. Den texten nådde aldrig git: den uppstod i en
mellanversion under själva rättningen och var borta innan något skrevs till
`data/villkor.jsonl`. Ett filnamn i en sidfot i `097f049b82b6` gjorde det
däremot. Där stod en handläggares för- och efternamn inne i villkor 2, och
raden är committad och pushad i a32fda2.

## Skäl

**En tomrad bär ingen information om var ett villkor slutar.** Den skrivs av
textlagret mellan två sidor och av layouten mellan två stycken, och de två går
inte att skilja åt på raden själv. Meningen går däremot att läsa: en text som
inte nått punkt har inte slutat. Det är den enda upplysning som finns på
platsen, och regeln använder den.

**Ett block hoppas över bara när det säger sitt eget namn.** En rad med enbart
siffror är sidfot i en löpande rubrik och tabellrad överallt annars, så ett
block utan ett enda huvudord hoppas inte över. Utan den regeln skulle en
bullertabell med värdena på egna rader kunna läsas som en sidrubrik.

**Kolon avslutar ingen mening.** Ett villkor som slutar på kolon har en lista
efter sig, och listan står ofta på nästa sida. Att läsa kolon som slut stängde
villkor som inte var slut, och en av dem blev så kort att den föll bort under
längdfiltret.

**Villkoret för att behålla ändringen var att inget beslut fick tappa ett
villkor**, och det skrevs i protokollloggen före körningen. Det föll tre gånger
under arbetet, en gång med sju beslut och två gånger med ett, och varje fall
handlästes innan regeln ändrades igen. Två av de tre visade sig vara andra fel
som rättningen hade avslöjat i stället för orsakat: ett villkor som redan svalt
avsnittet Uppskjutna frågor växte förbi taket på 4 000 tecken, och sju
OCR-beslut hade sitt villkorsnummer sist på en sida.

## Följder

Talen rör sig, och rörelsen går åt andra hållet än förutsagt. Före körningen
skrevs att andelen delad text skulle falla, eftersom längre texter är mindre
troliga att matcha exakt. Den steg, från 40 till **42 procent**, och
koncentrationen inom en enda prövningsgrupp från 222 av 237 till **238 av 253**
mot 28,7 väntat under permutation. Skälet är att två beslut med samma villkor
kapades på olika ställen, så avhuggningen dolde matchningar. Instrumentets fel
drog alltså mot att underskatta likheten mellan olika besluts villkor, vilket är
den försiktiga riktningen.

Rubrikerna blir färre och renare: 1 655 villkor under 155 rubriker mot 1 691
under 161. De 36 som försvann var löpande sidrubriker,
Miljöprövningsdelegationen, Anläggningsnummer, Örebro län, Aktbilaga 23 och
Skåne, som tidigare stod kvar som rader mellan två villkor. Inget ord som ett
beslut självt skrev försvann.

Andelen villkor som slutar utan skiljetecken faller från 11,4 till **5,7
procent**, och täckningen mot den andra textutvinningen står på 0,9914 för den
digitalfödda halvan och 0,9990 för den OCR-lästa.

Två gränser står kvar. `361be3bd133c` ligger utanför måttet, eftersom pdfplumber
får ut 40 tecken ur 34 sidor, och dess 31 villkor är därmed inte kontrollerade
på någon andra väg. `13df613f9802` villkor 4 bär en sidfot som OCR förvanskat så
att ingen markör träffar den.

Namnet är borta ur registret och steg 33 screenar nu även filändelser, men det
står kvar i trädet för varje commit från a32fda2 till och med rättningen, och de
commitarna är pushade. **Historiken skrivs inte om.** ADR-0003 gör den
append-only och Martin bekräftade regeln utan undantag den 5 september 2026, så
undantagsmeningen i ADR-0003 om personuppgifter används inte; se tillägget där.
Skillnaden mot de fem commits som skrevs om enligt ADR-0018 är att de aldrig
hade pushats, alltså aldrig var historik. Det som återstår är den andra halvan
av ADR-0003:s konsekvens, att händelsen dokumenteras öppet, och den här raden
är den dokumentationen. Följden att ta ställning till före publicering är att
ett tjänstemannanamn då blir sökbart ur ett filnamn i en sidfot, vilket är
precis det ADR-0018 valde bort.

## Tillägg 2026-09-05, senare samma dag: sju rubriker till

Talen om rubriker ovan gäller utfallet av den här ändringen och står kvar som
de mättes. De stod sig några timmar. Genomläsningen av de 155 rubriker som blev
kvar, gjord innan villkorstypologin byggdes på dem, hittade sju fel till i samma
familj: ett läns löpande sidrubrik i genitiv, VÄSTRA GÖTALANDS LÄN, som
ordlistan inte kände igen, och sex rubriker med föregående menings slut
klistrat framför sig, som `uppstår.Lagring av gödsel och spolvatten`.

Två regler kom ur det. Ett ord i sidhuvudet prövas även utan avslutande s, och
en rad som är sidhuvud kan aldrig vara rubrik, oavsett var i segmenteringen den
möts. Förledet före punkten läggs tillbaka på villkoret ovanför, vilket gav
femton villkor sitt meningsslut åter och sänkte avhuggningen från 133 till 125
av 2 347, alltså 5,3 procent.

**Aktuella tal är därmed 1 655 villkor under 148 rubriker**, inte 155.
Delegation framträdde först då som egen rubrik, femton villkor, och det är den
rubrik VILLKORSSCHEMA avsnitt 2.4 gett en egen tabell. Baselinens tal rörde sig
inte alls av den här ändringen. Utfallet står i `docs/VERIFIERAT.md`.
