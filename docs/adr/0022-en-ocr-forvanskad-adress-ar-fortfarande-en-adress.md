# 0022: En OCR-förvanskad adress är fortfarande en adress

Datum: 2026-09-09. Status: beslutad.

## Beslut

Steg 24 behandlar länsstyrelsens tredje sidfotsrad, `Kontakta i detta ärende:
<namn>, <adress>`, som sidfot och inte som villkorstext, och samma markör
fångar en e-postadress i den form OCR lämnar den, där snabel-a lästs som
vänsterparentes följd av Q, O eller noll. Screeningen i steg 33 vägrar skriva
registret om den formen förekommer, och en invariant i
`tests/test_repository_invariants.py` håller `data/villkor.jsonl` och
facitfilerna fria från både adressformen och kontaktraden.

Historiken skrivs inte om. ADR-0003 gör den append-only och regeln bekräftades
utan undantag den 5 september 2026.

## Sammanhang

En sikt av registret den 9 september 2026, gjord för en helt annan fråga, fann
**sex villkor som bär två namngivna tjänstemäns för- och efternamn och deras
e-postadresser**: `4d6a7564223c` villkor 3, `7291b07d9ace` villkor 6,
`78681974f707` villkor 5, `80a607999316` villkor 4, `a7529f8c30ee` villkor 7
och `f7b9b63ef249` villkor 3. Alla sex är OCR-lästa beslut från Länsstyrelsen i
Halland.

Sidfoten ser ut så här i den igenkända texten:

```
Postadress Besöksadress E-post Telefon
301 86 HALMSTAD Slottsgatan 2 halland(Qlansstyrelsen.se 010-224 30 00
Kontakta i detta ärende: <förnamn> <efternamn>, <förnamn>.<efternamn>(Qlansstyrelsen.se
```

Namnen och adresserna står här med platshållare, enligt ADR-0018.

Den första raden fångas av markören `postadress` och den andra av markören för
postnummer. Den tredje bär varken postnummer, telefonnummer eller, sedan OCR
läst tecknet som `(Q`, något snabel-a, så ingen markör nådde den och raden lades
till villkoret ovanför.

Raderna kom in med `a32fda2`, samma commit som filnamnet i ADR-0021, och ligger
i varje commit sedan dess. De är pushade.

## Skäl

**En screening skriven mot ren text screenar inte OCR.** Mönstret för
e-postadress i steg 33 kräver ett snabel-a. Tecknet överlever inte igenkänning
av en 300-punkters rendering: Tesseract läser det som en vänsterparentes och ett
Q. Screeningen såg alltså ingen adress i något av de sex villkoren, och den
skrev registret utan invändning. Det som saknades var inte ett strängare
mönster utan **ett mönster för hur uppgiften ser ut efter det steg som ligger
före screeningen**.

**Kontrollen som borde ha sett det kan inte se det.** Kontroll 3 läser varje
villkor tillbaka mot dokumentet. För den digitalfödda halvan sker det med ett
annat bibliotek, men för den OCR-lästa halvan finns ingen andra väg, och
registret mäts mot samma fil som segmenteringen läste. Ett sidfotsblock som
svalts av ett villkor matchar då perfekt. Kontroll 3 redovisar den svagheten i
klartext sedan den skrevs; det här är första gången den kostat något.

**Namnet var också ett mätfel.** Villkoret `Utgödsling av stallarna ska ske
minst två gånger per vecka.` står i tre beslut. Före rättningen matchade bara
två av dem varandra, eftersom det tredje bar kontaktraden i sin text. Gruppen
går från två till tre. Personuppgiften låg alltså inuti det som mäts och drog
måttet på delad text nedåt.

## Följder

Sex villkorstexter ändras och inget beslut tappar ett villkor: 2 347 villkor i
180 beslut före och efter, 1 655 med rubrik i båda. Förutsägelsen att texterna
skulle bli längre föll: de blir kortare, från 217, 310, 226, 138, 213 och 373
tecken till 138, 238, 147, 59, 136 och 294, eftersom kontaktraden avslutade
sidan och villkoret faktiskt slutade där.

Huvudsiffran rör sig inte. Den digitalfödda halvan står oförändrad på 1 762
villkor, 42 procent delad text, 253 texter i mer än ett beslut och 238 av dem
inom en enda prövningsgrupp. Den OCR-lästa halvan går från 136 till 137 delade
villkor, 23,2 till 23,4 procent, och från 501 till 500 olika texter. Kontroll 1
och kontroll 2 är oförändrade.

**Namnen står kvar i trädet** för varje commit från `a32fda2` till och med den
här rättningen, och de commitarna är pushade. Skillnaden mot de fem commits som
skrevs om enligt ADR-0018 är densamma som i ADR-0021: de hade aldrig pushats.
Det som återstår är ADR-0003:s andra halva, att händelsen dokumenteras öppet,
och den här filen är den dokumentationen. Följden att ta ställning till före
publicering är att två tjänstemannanamn då blir sökbara ur en sidfot, vilket är
precis det ADR-0018 valde bort.

Det är tredje gången ett personnamn nått registret: en gång ur ett filnamn i en
sidfot, en gång ur ett bifogat rättelsebeslut som aldrig nådde git, och nu ur
en kontaktrad i en sidfot. Alla tre kom in samma väg, som text på en sida som
inte är villkorstext, och ingen av dem kom in genom ett fält som är avsett att
bära ett namn. Sikten som hittade dessa sex letade inte efter namn utan efter
webbadresser, och det är värt att notera: **den screening som fångar
personuppgifter i det här materialet är den som letar efter sidfot, inte den som
letar efter person.**
