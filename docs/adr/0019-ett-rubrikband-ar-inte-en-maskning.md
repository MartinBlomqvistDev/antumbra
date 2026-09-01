# 0019: Ett rubrikband är inte en maskning

Datum: 2026-09-01. Status: beslutad.

## Beslut

Textmetoden i steg 18 utesluter två sorters fyllda svarta rektanglar ur
maskningsmåttet. Den första är rubrikbandet: en mörk ruta som innehåller ljus
text och ingen mörk text alls. Den andra är linjen: en ruta lägre än tre
punkter. Båda uteslutningarna står i koden med sin motivering, och båda
tröskelvärdena är satta mot materialets egen fördelning innan talen räknades
om.

Uteslutningarna gäller bara textlagret. Bildmetoden kan inte skilja ett vitt
ord i ett svart band från en svärtad rad, eftersom den läser pixlar där
textmetoden läser tecken. Vad som händer med den frågan står i tillägget till ADR-0016.

## Sammanhang

Kammarrätten i Jönköping registrerade den 1 september 2026 överklagandet av
Länsstyrelsen i Kalmars beslut som mål 3249-26 och skickade ett meddelande om
det. Handlingen arkiverades som alla andra, steg 18 kördes om, och steget
bedömde ett domstolsmeddelande utan en enda maskning som maskat. Träffarna var
tre vågräta linjer, 435 till 478 punkter breda och en halv punkt höga, som
klarade detektorns ytgolv på bredden.

Samma detektor gav en annan träff i länsstyrelsernas material, och den var
vanlig. Länsstyrelsernas kontrollrapportmall avslutas med en förteckning över
tillämpad lagstiftning under ett svart tabellhuvud med vit text: `Saknr`,
`Föreskriftens namn`, `Författningssamling` och `Utgivningsnummer`. Bandet är
fyra celler i rad, tillsammans 432 punkter breda och 32,7 eller 21,2 punkter
höga. Funktionen som räknar tecken under en ruta räknar bara mörka tecken,
eftersom ljus text i en mörk ruta är avsedd att läsas, så bandet fick noll
tecken under sig och hamnade i kategorin `text_removed`.

I materialet finns 456 sådana band. 105 av de 124 digitalt födda handlingarna i
klass A och B som över huvud taget har rutor bär minst ett, och för 33 av dem
var bandet den enda grunden för maskningsdomen: Jämtland A 16, Gävleborg A 4,
Västerbotten A 4, Dalarna A 2, Södermanland A 2, Uppsala A 2, Västmanland B 2
och Södermanland B 1.

## Skäl

**Ett band med vit text i döljer ingenting.** Den som läser handlingen läser
orden i bandet. En maskning har antingen ingenting under sig, för att texten
tagits bort, eller kvarliggande mörk text, för att rutan bara lagts ovanpå.
Rutan som bär ljusa tecken och inga mörka hör därför till sidans möbler.

**En halv punkt kan inte täcka en textrad.** Golvet på tre punkter ligger
långt under den lägsta verkliga maskningen i materialet, som är 13,83 punkter,
och långt över de vågräta linjerna, som är 0,48. Mellan de två talen finns
ingen enda ruta i materialet, så gränsen är dragen genom ett tomrum.

**Ingen av uteslutningarna kan träffa en verklig maskning här.** Ingen
utesluten ruta har mörk text under sig. Det är kontrollerat på materialets samtliga
3 465 rutor.

**Handkontrollen avgjorde saken.** En av Jämtlands kontrollrapporter renderades
och lästes. Handlingen är utlämnad utan en enda maskning, med djurhållarens
namn, adress och fastighetsbeteckning i klartext. Regeln säger alltså samma sak
om det dokumentet som ögat gör.

## Följder

Andelen dokument med minst en maskning går från 138 av 155 till **108 av 155** i
begäran A, och från 32 av 135 till **29 av 135** i begäran B. Kontrasten mellan
klasserna står kvar: medianskillnaden mellan de fjorton län som levererat i
båda klasserna går från 80 till 68 procentenheter i dokumentandel och från 2,3
till 2,04 procentenheter i maskerad yta, och inget län har mer maskad yta i B än
i A.

Jämförelsemängden för P9:s kriterium (b) växer från fem län till sex, med
Västerbotten tillagt. Kriteriet står därmed starkare än förut.
Rangordningen efter maskad yta bland de sex län som fått en P8-skrivelse ändras
inte, så beslutet om Kronoberg den 14 september vilar på samma ordning som
förut.

Två rader i sekretessgrundsregistret, Gävleborg A och Jämtland A, hör inte
längre till någon maskad leverans. Raderna står kvar, eftersom var och en är en
myndighets egen följebrevsmening och båda saknar åberopad bestämmelse, vilket är
precis vad en leverans utan maskning ser ut som. Invarianten som höll registret
slutet bär nu den skillnaden utskriven.

**Vad rensningen inte visar.** Att instrumentet saknar belägg för maskning i de
33 handlingarna är inte detsamma som att de är omaskade. En text som strukits
utan att en ruta ritats syns inte alls för textmetoden, och det golvet gällde
redan tidigare för skanningar. Efter den här ändringen gäller det uttalat för
digitalt födda handlingar också.
