# 0027: Den stympade läsningen förklarar villkorsantalet, och källbytet står

Datum: 2026-10-10. Status: beslutad. Avgör den fråga tillägget till
[ADR-0026](0026-utlosaren-mats-pa-villkoren-inte-pa-sidan.md) lämnade öppen.

## Beslut

Källbytet i ADR-0026 står, trots att förregistrerat villkor 2 föll.
`13df613f9802` läses ur projektets egen OCR, och dess rader i villkorsregistret
går från fyra till sexton. Beslutets serie är bruten, så det faller utanför den
rena delmängd som bär talen, och de nya summorna skrivs ut i `VERIFIERAT.md`.

Villkor 2 krävde att ett ändrat antal mäts innan registret byter källa. Det är
mätt, och mätningen ändrar frågan: antalet steg inte av att OCR segmenterar
annorlunda, utan av att textlagrets läsning var stympad vid villkor 4 av ett
tjugotal.

## Sammanhang

Mätningen står i tillägget till ADR-0026 och sammanfattas här i det som avgör:

- Textlagrets villkorsfönster är 39 rader och slutar i beslutets egen sidfot,
  läst som `Ostqotaqatan 3` och `E-DOSt:`. ADR-0021:s regel känner igen
  sidhuvudet som block och bär villkoret över sidbrytningen; ett huvud vars ord
  är förvanskade känns inte igen, så fönstret stängde vid den första brytningen.
- Ur projektets egen OCR läser steget numren 1 till 15 med rubriker ur beslutets
  egna ord, och en rad numrerad 20 på 2 981 tecken som bär texten i villkoren
  mellan 16 och 20 i ett stycke.
- Den brutna serien är inte ny i registret: 51 av 180 beslut har en, 36 av dem
  OCR-lästa, och 62 av de 79 rader vars nummer hoppar över ett steg sitter i
  OCR-lästa beslut.

## Skäl

**Att behålla textlagret är det sämsta av de tre lägena.** Fyra villkor numrerade
1 till 4 ger en obruten serie, så `series_ok` blir sant och ingenting i registret
visar att ett tjugotal villkor saknas. Felstavningen är synlig för den som
läser texten; stympningen är osynlig för alla.

**Felet som står kvar efter bytet är ett fel registret redan bär och deklarerar.**
En OCR-läsning som smälter samman några villkor till ett stycke är läget i 36
andra beslut. Fältet `series_ok` märker beslutet, talen redovisas över den rena
delmängden, och det är den konstruktion projektet valde för just den här
osäkerheten. Att behandla det här beslutet strängare än de 36 andra hade krävt
en regel som inget annat beslut hålls till.

**Femton av sexton rader är ordagranna citat ur beslutet.** Att kasta dem för
den sextondes skull byter ett deklarerat fel mot en odeklarerad lucka.

## Följder

Kontroll 3, avhuggningen och talen om delad text räknas om, och de tal som rör
sig skrivs ut i `VERIFIERAT.md` tillsammans med skälet. `13df613f9802` flyttar
från den digitalfödda halvan till OCR-halvan och från den rena delmängden till
den brutna, vilket sänker antalet beslut med obruten serie med ett.

Beslutet faller samtidigt utanför kontroll 3:s mått. Registertexten kommer nu ur
`ocr/tillstand_kontroll/`, och den andra vägen för ett OCR-läst beslut är steg
25:s OCR, som inte finns för en fil som bär ett textlager. Utanför måttet står
därmed två beslut med 47 villkor av 2 359, det här och `361be3bd133c`. Att i
stället låta kontrollen läsa samma fil registertexten kommer ur vore en
jämförelse med sig själv, och den mäter ingenting.

Steg 39:s sikt 2 slutar träffa beslutet, eftersom den läser diakriterna i
registrets villkorstext och de finns där efter bytet. Talet 0 beslut av 180 är
siktens egen bekräftelse på att felet är borta ur registret, och mätningen av
beslutet mot en OCR-läsning, vikt median 0,922, står kvar som den gjordes den 9
oktober 2026 på den text som då låg i registret.

Åtagandet om sidfoten i villkor 4 faller ut av bytet: sidfotens rader är
förvanskade i det inklistrade lagret, och ur projektets OCR träffar tre av fem
rader befintliga markörer.

## Alternativ som avvisas

**Att rulla tillbaka och låta textlagret stå.** Det är rollbacken ADR-0026 pekar
på, och den är avvisad av skälet ovan: den publicerar fyra felstavade villkor som
ser obrutna ut och gömmer sexton.

**Att utesluta beslutet ur registret.** Det ger en deklarerad lucka i stället för
en deklarerad bruten serie, kostar femton ordagranna villkor, och kräver en
uteslutningsregel som de 36 andra OCR-lästa besluten med bruten serie inte hålls
till.

**Att kasta raden som bryter serien.** Regeln hade träffat 79 rader i 51 beslut,
de flesta i beslut som inte har någon andra läsning att falla tillbaka på. Den
osäkerheten hör i `series_ok`, inte i en tystad rad.

**Att rätta de fyra raderna för hand.** Samma svar som i ADR-0026: registret
byggs av ett steg, och en hand-lagd rad går inte att bygga om.

## Tillägg 2026-10-10, efter en granskning av talen

**Kontexttalen räknar in beslutet självt.** Posten skriver 51
beslut med bruten serie, 36 av dem OCR-lästa, och talar på två ställen om "de 36
andra". Talen är mätta efter bytet och räknar in `13df613f9802` självt. Före
bytet var de 50 och 35, så jämförelsemängden är 50 andra beslut med bruten serie
och 35 andra OCR-lästa. Att kasta raden som bryter serien hade träffat 79 rader i
51 beslut, och där är talet rätt, eftersom regeln skulle gälla registret som det
står nu.

**En mening i skälen tar i för mycket.** Där står att felstavningen är synlig för
den som läser texten och stympningen osynlig för alla. Det senare gäller den som
läser registret. Den som läser beslutet ser att villkoren fortsätter, och steg
24:s egen utskrift räknade dem aldrig som saknade, eftersom den inte kan veta hur
många som finns. Påståendet är alltså sant om registret och inte om handlingen.

**Var beslutet går in i talen, och var det inte gör det.** Huvudsiffran räknas på
beslut ur textlagret, och efter bytet ligger `13df613f9802` utanför den helt. Den
OCR-lästa delmängden tar in dess sexton villkor, och replikeringen av
koncentrationen rör sig från 50 av 52 delade texter inom en prövningsgrupp till
52 av 54. De två nya klustren delas av det här beslutet och `486f0758082c`, båda
i prövningsgruppen Östergötlands län och Jönköpings län, alltså båda inom en
grupp: andelen går från 96,2 till 96,3 procent. Kontroll 3 lämnar beslutet
utanför sitt mått. Ingen publicerad huvudsiffra vilar alltså på det bytet, och
den delmängd som gör det redovisar sin rörelse här.
