# 0024: Råsvaren sparas och korrespondensregistret byggs av ett steg

Datum: 2026-10-08

## Beslut

Varje inkommet meddelande sparas som sitt orörda API-svar i
`data/korrespondens_raw/`, utanför git. Ett proveniensmanifest med
meddelande-id, meddelandehuvudets tid, storlek, sha256 och antal tecken
committas som `data/korrespondens_manifest.jsonl`. Steg 44 bygger registrets
mekaniska delar ur råsvaren: svensk tid ur UTC, borttagna länkmål, kapad
citerad historik och kapat signaturblock där signaturen namnger en person.

## Skäl

Registret byggdes för hand, meddelande för meddelande, i samtalet. Det gjorde
tre saker dyra och ömtåliga, alla tre observerade den 7 och 8 oktober 2026.

Reglerna lästes om varje session, ur fem olika filer. Meddelanden hämtades om
när svaret hade rullat ur samtalet; Kronoberg, Västerbotten och Västra Götaland
hämtades två eller tre gånger var. Och texten jämfördes mot bärarens för hand
varje gång en förekomst skrevs, vilket två gånger gjordes utan att texten var
hämtad, med rätt utfall av tur och inte av metod.

Ett steg som läser sparade råsvar kör om sig självt gratis. Det är samma
ordning som resten av projektet redan följer: numrerade steg som skriver till
`data/` och är återupptagbara.

## Varför råsvaren inte committas

De bär tjänstemännens namn, deras direktnummer och personliga adresser, alltså
just det ADR-0018 och P12-breven håller utanför det publicerade materialet.
Mönstret är ADR-0004:s: källan stannar utanför git och manifestet med sha256
per fil committas, så att varje rad i registret går att kontrollera mot den
text som faktiskt kom utan att texten sprids.

## Vad steget inte gör

Hämtningen. Den kräver brevlådan och sker därför i samtalet, ett meddelande i
taget, och råsvaret sparas direkt. Steget avgör inte heller myndighet, roll
eller vad som är ett substantiellt besked; det är omdömesfrågor som ska läsas
ur brevets egna ord.

## Validering

Steget mättes mot rader som redan var skrivna för hand, och reproducerade dem
tecken för tecken: Jönköpings autosvar den 3 augusti, där länkmål är det enda
som utelämnas, och Örebros avgiftsbesked den 6 augusti, som har både citerad
historik och en signatur med en namngiven tjänsteman. I det andra fallet
kapades namnet, vilket är det villkor beslutet står och faller på.

## Vad som gäller de rader som redan finns

De 124 rader som skrevs före beslutet har inget sparat råsvar och kan inte
byggas om utan att hämtas igen. De står kvar som de är. Manifestet säger därför
vilka rader som har proveniens och vilka som inte har det, och skillnaden
redovisas i stället för att jämnas ut.

## Tillägg 2026-10-08: en signatur på ett enda ord bedöms, inte gissas

Steget kapar en signatur vars första rad är två versalinledda ord, eftersom det
nästan alltid är en person som skriver under. Ett enda ord går inte att avgöra
på formen. Brevlådan rymmer tre fall, alla från samma vecka: Södermanland
skriver under med titeln *Djurskyddshandläggare*, Halland med enheten
*Veterinärenheten* och Gävleborg med ett förnamn. Ett försök att skilja dem med
en lista över ändelser kapade Södermanlands titel, alltså myndighetens egna ord,
och hade släppt igenom ett förnamn som råkat sakna en sådan ändelse.

Beslutet är att steget inte avgör frågan. Bedömningen läses per meddelande ur
`data/korrespondens_signaturer.jsonl`, där fältet `signaturen` är antingen
`namn` eller `befattning eller enhet`, och ett meddelande utan rad stoppar
steget med sitt id. Filen bär bedömningen och aldrig ordet, så inget namn når
repot, och körningen blir ändå deterministisk: samma råsvar och samma bedömning
ger samma text.

Det här är samma hållning som resten av steget: det som går att räkna räknas i
kod, och det som kräver en läsare lämnas till läsaren och skrivs ner.
