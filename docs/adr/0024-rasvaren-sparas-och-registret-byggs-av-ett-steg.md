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

## Tillägg 2026-10-08, senare samma dag: en rad som bara var en länk kapas

De 124 handskrivna raderna kapade de rader som inte bar något annat än en länk,
alltså en etikett som `Central e-post` med sitt mejlmål efter sig. Steget tog
bara bort målet och lät etiketten stå. Skillnaden syntes först när Örebros
stående autosvar kom in en gång till den 28 augusti: bäraren i registret var
639 tecken, steget gav 719, och samma autosvar hade då burits i två former i
stället för som en bärare med förekomster.

Steget kapar nu en rad vars hela innehåll var en eller flera länkar, och säger
det i `utelamnat`. Tretton rader byggda av steget är skrivna om efter samma
regel, och tre rader som bar ett autosvar som redan fanns i registret är lagda
som förekomster hos sin bärare. En naken webbadress som myndigheten skrivit som
text är inte en länk och står kvar, eftersom den är myndighetens egna tecken och
inte e-postklientens återgivning av en länk.

Regeln är inte en prydlighetsfråga. Ett register som bär samma text i två former
beroende på vilket år raden skrevs låter löftet om ordagrannhet se ut som en
smaksak.

## Tillägg 2026-10-09: läget när registret blev komplett

Registret bär nu 260 av 260 inkomna meddelanden på 196 rader. 107 av
meddelandena har sitt råsvar sparat och sin sha256 i manifestet; de övriga 153
skrevs för hand innan det här beslutet fattades. Talet 124 ovan var antalet
sådana rader den 8 oktober och är alltså inte aktuellt; det aktuella talet står
i `VERIFIERAT.md` och går att räkna ur filerna.

Fem mekaniska regler kom till under införandet, alla av ett brev som inte
passade den förra: en rad som inte bar något annat än en länk, domstolarnas
engångslänk till tjänsten Säker e-post, en hälsning som bär underskriften på
samma rad, en rad av understreck mellan hälsning och underskrift, och ett
signaturblock utan hälsning över sig. Mönstret är tydligt nog att skriva ner:
varje ny regel kom inte av ett principiellt resonemang utan av ett brev som
visade att den förra regeln inte räckte, och varje gång gav manifestets diff
svaret på om den nya regeln rörde något som redan var skrivet. En gång gjorde
den det av misstag, när ett bindestreck mitt i en teckenklass öppnade ett
intervall som matchade varje bokstav och kapade fyra signaturer som inte namnger
någon. Felet syntes i diffen och aldrig i registret.
