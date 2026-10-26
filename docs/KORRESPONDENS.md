# Korrespondensregistret: allt som styr det, på ett ställe

Registret är `data/korrespondens.jsonl`. Den här filen finns för att reglerna
annars ligger i fem: projektets CLAUDE.md, `BEGARANMALL.md` avsnitt 7,
`VERIFIERAT.md`, ADR-0003 och ADR-0018. **Läs den här filen, inte de fem, när
du arbetar i registret.** Ändras en regel ändras den här och på sitt
ursprungliga ställe.

## Vad registret är och vad som binder det

P12-breven, avsända 2026-10-02, lovar att det publicerade materialet rymmer
*"hela handläggningsprotokollet och hela korrespondensloggen, alltså också de
mejl ni har skickat i de här ärendena, ordagrant"*. Två ord i den meningen
styr allt annat.

*I de här ärendena* avgränsar till begäran A, B och C och de fyra
överklagandena. Förarbete ligger utanför, markerat i förteckningen med skäl.

*Hela* är ett löfte om fullständighet. Ett ofullständigt register kan inte
publiceras under den rubriken, och hur långt det är kommet står i
`VERIFIERAT.md`, läst ur filerna av en invariant. Sedan den 9 oktober 2026 bär
registret samtliga inkomna meddelanden förteckningen känner. Arbetsgången nedan
gäller ändå oförändrad: nya meddelanden kommer in så länge ärendena lever, och
de förs in på samma sätt.

## Utgående register, 2026-10-26: mina egna brev på samma villkor

Registret ovan bär bara inkommande. Myndigheternas brev stod därmed i sin
helhet medan mina egna fanns som mallar i `BEGARANMALL.md`, som de 22
arkiverade P12-paketen och i övrigt som noteringar i protokollloggen. På en
mätning av öppenhet är det den asymmetri en kritiker namnger först, och den
är inte försvarbar: den som begär ut andras handlingar och publicerar dem
ordagrant ska tåla samma sak om sina egna.

**Avgränsningen är densamma.** Begäran A, B och C och de fyra överklagandena.
155 av mina utskick är knutna till en myndighet och en begäran i loggen.

**Källan är Sent och ingenting annat.** En fil som pipelinen byggde före
avsändningen är inte brevet som gick: steg 36 är rättat två gånger sedan
P12-utskicket, vilket är hela skälet till att `data/p12_avsant/` finns med
kontrollsumma per brev. Varje rad hämtas därför ur meddelandet som faktiskt
skickades, råsvaret sparas orört i `data/korrespondens_raw_utgaende/` som är
gitignorerat, och manifestet bär sha256 per råsvar.

**Vad som utelämnas, och varför det skiljer sig från inkommande.**

1. **Mottagarens adress återges aldrig när den är en namngiven tjänstemans.**
   Flera av mina brev gick till handläggare som svarat från en personlig
   adress, och att jag skrev till dem gör inte adressen till min att
   publicera. Fältet `mottagare` bär därför samma tvåvärdesvokabulär som
   `avsandare` gör för inkommande: `funktionsbrevlåda` eller
   `namngiven tjänsteman`, aldrig adressen.
2. **Den citerade historiken kapas**, alltså myndighetens meddelande under
   mitt svar och min egen tidigare text. Den står redan i registren.
3. **Länkmålen kapas**, och en rad som inte var annat än en länk.
4. **Min egen signatur står kvar.** Namnet är mitt och adressen
   cm.blomqvist@gmail.com är den avsändaradress hela mätningen vilar på; att
   maska den vore att dölja vem som frågade.

**Vad som aldrig görs.** Ingen uppgift om en enskild djurhållare förs in, och
ingen tjänstemans namn återges, inte heller i en hälsningsfras där jag själv
har skrivit ut det. Där jag tilltalat en handläggare med namn skrivs rollen i
stället, på samma sätt som ADR-0018 föreskriver åt andra hållet, och raden
säger i `utelamnat` att det gjorts.

## Stegen som gör arbetet

Fyra steg i `pipeline/` sedan den 9 oktober 2026, och de låg i en temporär mapp
innan dess, vilket var samma kostnad ADR-0024 skrevs för att slippa:

- `44_build_correspondence.py` räknar tid, kapar och skriver manifestet.
- `46_build_correspondence_row.py` bygger en rads nyttolast ur ett sparat
  råsvar, med omdömesfälten som argument.
- `45_append_correspondence.py` granskar och lägger till raden, eller lägger en
  förekomst hos sin bärare.
- `47_append_standing_autoreply.py` hittar bäraren åt ett stående autosvar och
  skriver förekomstens nyttolast, och vägrar när ingen bärare har identisk text.
- `48_write_register_progress.py` skriver talen i `VERIFIERAT.md` ur filerna.

## Arbetsgången, i ordning

1. **Nästa meddelande** läses ur `data/korrespondens_forteckning.jsonl`, äldst
   först. Förteckningen är brevlådan gången igenom tråd för tråd, och den är
   byggd om en gång sedan en arbetslista visade sig avhuggen.
2. **Hämta det** med `get_message` och `PLAIN_TEXT`. `MINIMAL` räcker för att
   se vad ett meddelande är, men inte för att återge det ordagrant.
3. **Spara råsvaret** till `data/korrespondens_raw/<id>.json`, orört. Det är
   gitignorerat och bär personuppgifter (ADR-0024).
4. **Kör steg 44.** Det räknar svensk tid ur meddelandehuvudet, tar bort
   länkmål, kapar citerad historik och kapar signaturblocket där signaturen
   namnger en person. Står det ett enda ord under hälsningen stannar
   steget: ordet kan vara ett förnamn, en titel eller enheten själv, och
   bedömningen skrivs som en rad i `data/korrespondens_signaturer.jsonl`
   med `signaturen` satt till `namn` eller `befattning eller enhet`. Filen
   bär bedömningen och aldrig ordet (ADR-0024).
5. **Skriv raden** med det som är omdöme: myndighet, roll, bilagor och de
   anmärkningar som bara en läsare kan göra, till exempel att en felstavning
   står som myndigheten skrev den.
6. **Logga** eventuella autosvar som saknas i protokollloggen. Bär brevet
   ett besked som hör i en egen tabell, till exempel länets tal på
   nämnarfrågan, förs det in där också och det steg som läser tabellen
   körs om.
7. **Uppdatera talet** i `VERIFIERAT.md`.
8. **Grindarna**, var och en som sitt eget kommando med exitkoden läst:
   `ruff check .`, `ruff format --check .`, `pytest`. Aldrig i ett rör och
   aldrig i en kedja som låter commit följa oavsett utfall.
9. **Commit och push**, och läs CI efteråt. Stega hela arbetskopian, aldrig
   en enskild sökväg: steg 5 skriver i `data/` och steg 7 i `docs/`, så en
   `git add data/` lämnar talet kvar och CI faller på invarianten fast
   pytest var grön lokalt.

   *Tillägg 2026-10-26.* **Kör `git add -A -N` före grindarna när en ny fil
   har tillkommit.** Invarianterna läser `git ls-files`, alltså bara spårade
   filer, så en nyskapad datafil är osynlig för dem tills den är stegad.
   Första gången det utgående registret committades var pytest grön lokalt
   och CI röd en minut senare, på en funktionsbrevlåda som stod kvar i en
   avhuggen citatmarkör. En grön grind som inte läste filen du nyss skrev är
   ingen grind.

## Reglerna per fält

**`datum` och `klockslag`** är meddelandehuvudets tid omräknad till svensk,
alltså UTC plus två timmar för hela perioden augusti till oktober 2026. Tid
läses ur källan och hittas aldrig på.

**`myndighet`** läses ur brevets eget adressblock. Den härleds aldrig ur en
personlig adress förnamn.efternamn, eftersom det är att gissa.

**`avsandare`** är antingen `funktionsbrevlåda` eller `namngiven tjänsteman`
och ingenting annat.

**`roll`** är den befattning eller funktion brevet självt undertecknas med, med
brevets egen lydelse. Den översätts inte till närmaste befattning: Västmanland
skriver *Administrativ handläggare*, inte *administratör*. Namnges ingen person
är rollen ändå myndighetens egen uppgift om vem som hanterar ärendet.

**`text`** är ordagrann. Ingen sammanfattning, ingen karaktärisering, ingen
rättning av stavning eller av myndighetens egna tal.

**`utelamnat`** säger vad raden lämnar ute och varför. Fyra saker utelämnas
regelmässigt: den citerade historiken, signaturblockets personuppgifter enligt
ADR-0018, länkmålen, och en rad som inte var något annat än en länk.
Myndighetens egen funktionsbrevlåda, växel och webbadress står kvar när de står
som text, eftersom de är publicerade kontaktuppgifter och inte en enskilds.

Den fjärde regeln kom den 8 oktober 2026 och den har ett skäl som väger mer än
prydlighet. En rad som bara bar en länk, till exempel `Central e-post` med sitt
mejlmål efter sig, blir en lös etikett när målet tas bort, och den ser ut som en
mening myndigheten skrivit. Registrets handskrivna rader kapade sådana rader
från början, medan steg 44 lät dem stå, och samma stående autosvar kom därför
att bäras i två former: Örebros autosvar på 639 tecken som handskriven rad och
på 719 tecken genom steget. Nu kapar steget dem, tretton rader är skrivna om
efter samma regel, och tre rader som bar ett autosvar som redan fanns i
registret är inlagda som förekomster hos sin bärare i stället. En naken
webbadress som myndigheten själv skrivit som text är inte en länk och står kvar.

En femte sak utelämnas sedan den 8 oktober 2026, och den gäller bara
domstolarna: engångslänken i aviseringen från tjänsten Säker e-post. Den
öppnar meddelandet som adressat och är alltså en personlig åtkomstlänk, inte
en publicerad adress. Länkarna upphör att gälla 30 dagar efter meddelandet,
men ett publicerat register ska inte bära dem ens utgångna, och en invariant
fäller en rad som gör det.

**`forekomster`** bär en brevlådas stående autosvar när texten är identisk
tecken för tecken. En förekomst måste bära meddelandets `sizeEstimate` ur
API-svaret, som bevis på att meddelandet är hämtat och inte antaget identiskt.

## Vad som aldrig görs

Ingen enskild tjänstemans namn återges, varken i signaturen eller i brödtexten;
en invariant i `tests/` fäller en rad där ett namn står kvar. Ingen uppgift om
en enskild djurhållare förs in. Och ingen slutsats dras ur en förteckning över
källan i stället för ur källan: det felet gjordes den 7 oktober 2026 i en
rättelse av protokollloggen, och rättelsen fick återtas dagen därpå.

## Invarianterna som vaktar registret

Fem i `tests/test_repository_invariants.py`:

1. Varje rad bär meddelande-id och säger vad den utelämnar; inget namn utan
   roll och ingen personlig adress.
2. Avsändarfältet håller sig till de två tillåtna värdena.
3. Ingen rad bär en rad som ser ut som en persons namn.
4. Varje registrerat meddelande, förekomsterna inräknade, paras mot en loggad
   händelse i protokollloggen.
5. Registret mäts mot förteckningen, ingenting utanför avgränsningen står i
   det, och talet i `VERIFIERAT.md` stämmer med filerna.

### Tillagt 2026-10-26: mina egna identitetsuppgifter stannar utanför registret

Ett överklagande till kammarrätt måste bära partsuppgifter. De fyra
överklagandena bär därför mitt personnummer, min bostadsadress och mitt
telefonnummer, skrivna till en domstol. Registret publicerar mina brev som de
skrevs, och det första överklagandet var på väg in i registret med alla tre.

Regeln är nu densamma som för alla andra: de tre uppgifterna klipps av steg 52,
och klippet står i radens `utelamnat`. Det som står kvar är namnet och den
e-postadress jag skrev från, eftersom det är vad samtliga 22 myndigheter såg,
och mätningen vilar på vem som frågade.

En rad som gäller för mig själv är lika bindande som den som gäller
tjänstemännen. Skillnaden är bara att ADR-0018 skrevs om någon annans namn.

Spärren ligger på två ställen, eftersom en regel som bara finns i det steg som
råkar köras gäller till dess att någon skriver en rad på ett annat sätt. Steg 52
klipper, och en invariant i `tests/test_repository_invariants.py` fäller varje
spårad fil som bär ett personnummer. Invariantens första version matchade sex
siffror och en skiljetecken och rapporterade sex myndigheters
organisationsnummer, bland dem 202100-2270. Ett personnummer inleds med ett
datum, och statens egna nummer bär månadssiffra 20 eller högre just för att
kunna skiljas från personnummer, så mönstret kräver giltig månad och dag.

### Tillagt 2026-10-26: avstämningen frågade inte efter alla brev

Steg 53 stämmer av registret mot protokollloggen. Den filtrerade loggen på en
lista över avsända händelsetyper, och listan var ofullständig. Tre slag av brev
stod utanför den: `avstående`, alltså de åtta brev som avstår från kopior när en
avgift kvarstår efter avsmalningen, `beslutsbegäran och fråga om uttagets
fullständighet`, alltså P8:s sju skrivelser, och det ena av femton
`rättelse`-brev som faktiskt gick till en myndighet. Nämnaren var därför 160 när
den skulle vara 176, och steget rapporterade myndigheter som klara vars brev det
aldrig frågat efter.

Steget hade en docstring som påstod att en ny typ skulle visa sig som okänd.
Ingenting genomförde det. Nu står varje händelsetyp i loggen i en av två
mängder, `SENDS` eller `NOT_SENDS`, och en typ i ingen av dem avbryter steget med
exit 1. Den kontrollen hittade omedelbart sex interna typer som det första
svepet missade, eftersom svepet filtrerade bort raderna med myndighet
`samtliga`.

`rättelse` står som icke-avsänd trots att ett av breven gick. Typen betecknar en
rättelse, och fjorton av de femton rättar projektets egna anteckningar, loggen
eller en oavsänd läskopia. En typ kan inte vara till hälften en avsändning, så
typen är det inte, och det enskilda brevet står namngivet i `EXTRA`.

Samma fel i en annan skepnad: nyckeln som parar en loggrad mot en registerrad
bestod av datum och händelse. De två begärandena gick ut en minut isär den 3
augusti, så en B-rad bockade av A-raden, och Gotlands saknade A-begäran
rapporterades som närvarande. Nyckeln bär nu även begäran.
