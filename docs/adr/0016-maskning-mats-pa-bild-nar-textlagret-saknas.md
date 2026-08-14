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

**Golvet metoden inte ser förbi ska alltid följa med siffran:** en skanning av
en sida vars text togs bort före utskrift är omöjlig att skilja från en sida som
aldrig bar texten. `masked` falskt på en skanning betyder att ingen balk
hittades, inte att ingenting undanhållits. Ett fotografi i skannat material kan
dessutom räknas som maskning om ett tillräckligt stort parti är mörkt; ett
sådant fall finns i valideringen och är utskrivet där.
