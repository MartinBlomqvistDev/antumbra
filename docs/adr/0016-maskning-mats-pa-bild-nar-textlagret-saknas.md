# 0016: Maskning mäts på renderad bild när textlagret saknas

Datum: 2026-08-14. Status: beslutad.

## Beslut

Maskningsmåttet får två metoder i stället för en. Digitalt födda handlingar
bedöms som förut ur textlagret: en fylld rektangel är en maskning, och om mörk
text ligger kvar under den är maskningen kosmetisk. Skannade handlingar, som
saknar textlager helt, bedöms i stället på den renderade sidan genom solida
mörka rektanglar i bilden. Vilken metod som använts skrivs per dokument i
`data/maskning.jsonl` som fältet `method`, och båda metoderna rapporterar samma
två storheter: om dokumentet är maskat och hur stor andel av sidytan som täcks.

Bildmetoden fick gälla först efter att den prövats mot textmetodens facit på
**samtliga 248 digitalt födda dokument**, alltså där ett oberoende svar redan
fanns. Utfallet: 122 av 123 maskade hittades, 117 av 118 omaskade förblev rena.
Tre parameteruppsättningar prövades mot samma facit och den valda är strikt
bättre än de två andra. Resultatet och de två felkällorna står i
`docs/VERIFIERAT.md`.

## Skäl

**Utan den här metoden mättes inte 15 procent av materialet.** Länen svarar i
olika form: vissa skickar digitalt födda PDF:er, andra skannar papper. Den 14
augusti 2026 var 45 av 293 mottagna dokument skannade, och för dem kunde
maskningsgraden inte bedömas alls. Ett mått som systematiskt saknar de län som
skannar mäter inte bara maskning utan också leveransform, och leveransformen är
en egen observerad dimension i projektet, inte en slump. Att lämna hålet öppet
hade varit att låta en teknisk begränsning bestämma vilka län som ingår i
kärnmätningen.

**Varför bild och inte OCR för just det här.** OCR körs numera också, i steg 19,
men den svarar på en annan fråga. En maskning är en svärtad yta, och OCR
återger text, inte frånvaron av den. Balkarna syns direkt i pixlarna och kräver
varken språkmodell eller teckentolkning. OCR behövs för djurslag och fält, inte
för att se att någonting är övertäckt.

**Varför prövningen mot textmetoden är avgörande.** Bildmetoden kunde ha införts
som ett rimligt antagande. I stället finns 248 dokument där två oberoende
metoder kan jämföras, och det underlaget kostade ingenting extra att använda.
Den ordningen, baseline och facit före tillämpning, är samma standard som
bilageklassningen och länkkontrollen i DG SANTE-lagret vilar på.

## Följder

Kategorin `scanned` som slutdom försvinner ur `data/maskning.jsonl`; en skanning
får numera `bars_on_scan` eller `none`, och fältet `masked` gör räkningen
entydig. Det gamla talet, 86 procent maskat i begäran A mot 17 i B räknat på
244 bedömbara dokument, ersätts av 89 mot 23 över alla 293.

*Tillägg 2026-08-21:* Södermanlands andra leverans den 17 augusti lade till ett
dokument i klass B, och steg 18 kördes om. Talet är sedan dess 89 mot 24 över
294 dokument. Beslutet i denna ADR är oförändrat; siffran står kvar som den var
när beslutet fattades, och den gällande finns i `docs/VERIFIERAT.md`.

**Golvet metoden inte ser förbi ska alltid följa med siffran:** en skanning av
en sida vars text togs bort före utskrift är omöjlig att skilja från en sida som
aldrig bar texten. `masked` falskt på en skanning betyder att ingen balk
hittades, inte att ingenting undanhållits. Ett fotografi i skannat material kan
dessutom räknas som maskning om ett tillräckligt stort parti är mörkt; ett
sådant fall finns i valideringen och är utskrivet där.

*Tillägg 2026-09-01:* **valideringens rena rad går inte att reproducera.**
Sedan textmetodens facit rättats enligt ADR-0019 kördes jämförelsen om med
detektorn som den står i repot, mot exakt de 248 dokumenten och exakt det facit
som gällde den 14 augusti. Den maskade raden kommer tillbaka dokument för
dokument: 122 med balk och 1 utan. Den rena raden gör det inte. Av de 118
omaskade handlingarna ger 30 balk, där tabellen ovan redovisar 1. Markörraden
blir 4 och 3 där tabellen har 3 och 4.

Detektorn är oförändrad sedan valideringen. Den enda senare ändringen i steg 18
den dagen lade till ytmätningen, och ingen ändring efter det rörde geometrin.
Att den maskade raden återkommer exakt talar också emot att renderingen skulle
ha ändrat sig under tiden, eftersom en sådan ändring hade rubbat båda raderna.
Kvar står frågan hur den rena raden räknades fram, och den går inte att avgöra
ur repot.

**Den vanligaste felkällan är verifierad.** Länsstyrelsens vapen på sidan ett är
en solid svart sköld, 49 gånger 9 bildpunkter vid 100 dpi med 93 procents
fyllnad, och den klarar varje krav detektorn ställer på en balk. Mallens svarta
tabellhuvud är den andra källan. Att utesluta tabellhuvudet räcker inte: av de
64 handlingar som mot det rättade facit ger balk utan att vara maskade blir
ingen enda ren av den uteslutningen, eftersom vapnet ligger kvar.
Jämförelsen körs om med `python src/validate_image_method.py`, som skrevs i dag
just därför att den förra kördes utan att lämna något spår.

**Följden för talen.** Mot det rättade facit ger bildmetoden balk i 64 av de
155 handlingar som textmetoden bedömer som omaskade, räknat över materialets 261
digitalt födda. Samtliga 30
skannade handlingar i klass A bedöms som maskade, liksom 11 av 15 i klass B.
Ett `masked` sant på en skanning bär därför mycket mindre än det såg ut att
göra, och dokumentandelen ska tills vidare redovisas uppdelad på metod, med
den skannade delen försedd med den här reservationen.

Beslutet i denna ADR står kvar: två metoder behövs, och alternativet att lämna
15 procent av materialet omätt är sämre. Det som faller är påståendet om
metodens falsklarmsfrekvens.

Frågan om en regel för bildsidan prövades samma kväll, mot ett villkor som
skrevs innan utfallet var känt, och utfallet står i ADR-0020: vapnet och
rubrikbandet utesluts numera även ur bildmetoden, falsklarmen faller från 64 av
155 till 30, och ingen ytterligare verkligt maskad handling blir blind. Ingen
publicerad siffra rör sig av det, eftersom varje skannad handling som bär de två
elementen också bär andra balkar. Resten är fotografier, alltså den felkälla den
här ADR:n skrev ut från början.
