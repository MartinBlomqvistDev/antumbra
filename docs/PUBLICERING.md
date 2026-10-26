# Publiceringen: vad som ska vara gjort, i vilken ordning, och hur ytorna ser ut

Skriven 2026-10-06, fyra dagar efter att P12-paketen gick och arton dagar före
tidigaste publiceringsdag. Den skrivs nu, innan något svar på paketen har kommit
med en invändning mot en siffra, så att listan inte formas av vad myndigheterna
råkar svara.

Tidigaste publiceringsdag är **lördag 2026-10-24**, dagen efter svarstidens
slut. **Vald dag är måndag 2026-10-26**, två dagar senare. Not 8 säger tidigast,
så en senare dag kräver ingen annan motivering än att den loggas, och tre skäl
talar för måndagen: mottagarna är myndigheter och journalister som läser på
vardagar, nämnarens läge redovisas ändå den 26:e så materialet blir
fullständigt på dag ett i stället för att kompletteras två dagar senare, och en
lördagslansering lägger materialet på den enda dag ingen läser det. Regeln är tillämpningsnot 8: publicering enligt P12 är varje åtgärd som
gör en berörd myndighets egna resultat läsbara för någon utanför projektet, och
ingen sådan yta öppnas förrän tre veckor gått sedan paketen nådde samtliga
berörda myndigheter. Paketen gick 2026-10-02 mellan 13:12:22 och 13:15:24, med
svarsdatum den 23 oktober utskrivet i varje brev.

Listan nedan är inte en önskelista. Den är vad de 22 avsända breven utfäster,
vad protokollet förregistrerade, och vad som i dag saknas för att det ska gå att
infria.

---

## 0. Vad som byggdes den 6 oktober

Listan nedan skrevs samma dag och är redan delvis infriad. Det som landade:

- **Resultatytan per myndighet.** Sidan Handlingar bär en tavla per myndighet
  med talen myndigheten själv fick, intervallet, platsen i jämförelsen och
  myndighetens eget svar ordagrant, eller noteringen att svar inte kommit.
- **Siffrorna och jämförelsen på sidan Sverige**, med båda klassernas tal,
  kontrastmåttet, båda jämförelsetabellerna med intervall och ett avsnitt om vad
  sidan inte visar. Engelsk spegel på plats för sidan Sverige.
- **Svarsregistret** `data/p12_svar.jsonl`: samtliga femton svar som kommit in,
  ordagrant, med meddelande-id, roll i stället för namn och en utskriven rad om
  vad som inte återges.
- **Arkivet över de avsända breven**, `data/p12_avsant/` med kontrollsumma per
  brev, eftersom steg 36 är rättat två gånger sedan utskicket och alltså inte
  längre skriver de brev som gick.
- **Avvikelserna från förregistreringen** på metodsidan, på båda språken.
- **Oktoberfelen i `docs/VERIFIERAT.md`**, tillsammans med jämförelsens
  upplösning: måttet skiljer 39 av 136 länspar i klass A och 28 av 153 i klass B.
- **Steg 41**, som bygger webbens underlag ur samma funktioner som skrev
  paketen, så att en siffra på sidan är den siffra myndigheten fick.
- **Ett fel på en publik yta**, rättat: sidan Sverige räknade 45 avsända
  begäranden, eftersom de två senare begärandena till kammarrätterna också är
  loggade som avsändningar. Talet är 43.

Kvar står korrespondensloggen, de fyra oräknade måtten i avsnitt 2 och de tre
besluten i avsnitt 7.

*Tillägg 2026-10-26.* Svarsregistret bär 18 rader på publiceringsdagen och inte
femton: svaren fortsatte komma in efter den 6 oktober, och en rad lades till i
dag sedan Jordbruksverkets mottagningsbesked den 5 oktober visat sig saknas just
där, fast det hela tiden legat ordagrant i protokollloggen och i
korrespondensregistret. Skälet att rätta det före snittet var inte
fullständigheten utan likabehandlingen: Gävleborgs likartade manuella svar låg i
registret och Jordbruksverkets inte. Ingen publicerad siffra rör sig av
tillägget, eftersom raden är ett besked och inte ett svar i sak.

---

## 0b. Beslut 2026-10-07: vad som får namnge ett län

De tre mått som räknades den 6 oktober fanns inte i P12-paketen den 2 oktober,
och P12 ger varje myndighet dess egna resultat före publicering. Inga fler brev
skickas; myndigheterna har fått ett paket och i två fall en rättelse. Frågan
avgjordes därför mått för mått.

**Avgiftsutfallet namnger län.** Varje händelse i avgiftsspåret ligger i
protokollloggen, och paketen säger själva att hela loggen publiceras ordagrant
med myndighetens namn. Måttet räknar rader som redan är utlovade som publika,
och tillför ingen ny uppgift om länet.

**Parmåttet namnger länet.** Länets eget paket redovisade 22 dokument och 100
procent maskade i klass A mot 26 dokument och 0 procent i klass B. Parläsningen
är en delmängd av samma dokument åt samma håll.

**Bilagemåttet namnger ingen, eftersom det inte mäter något.** En räkning av
meningarna bakom träffarna visade att den vanligaste hänvisningen är en mening
ur den nationella kontrollrapportmallen, som står där oavsett om något foto
togs. Materialet skiljer alltså inte en undanhållen bilaga från en som aldrig
fanns. Måttet redovisas som en lucka, och `data/bilagor.jsonl` stannar utanför
git: den bär en flagga per län som inget påstående vilar på, och som skulle läsas
som ett påstående ändå.

---

## 1. Vad de avsända breven binder projektet till

Breven är skickade och kan inte ändras. Fem meningar i dem är utfästelser, och
var och en har en yta som måste finnas den 24 oktober.

1. *"Ett svar publiceras oavkortat vid sidan av siffrorna. Uteblir svar
   publiceras siffrorna som de står, och det antecknas att svar inte kommit."*
   Det kräver en yta per myndighet där talen och myndighetens eget svar står
   bredvid varandra, och där tystnad skrivs ut som tystnad.
2. *"Den omfattar ett publikt kodarkiv på GitHub, en webbplats och ett
   dataset."* Tre ytor, inte en.
3. *"I materialet ingår hela handläggningsprotokollet och hela
   korrespondensloggen, alltså också de mejl ni har skickat i de här ärendena,
   ordagrant."* Handläggningsprotokollet finns committat i
   `data/protokoll_logg.jsonl`, 542 rader den 7 oktober 2026. En korrespondenslogg med
   myndigheternas egna meddelanden i sin helhet finns inte; loggens noteringar
   bär ordagranna utdrag, inte hela meddelanden.
4. *"Namn på enskilda tjänstemän återges inte någonstans: där ett beslut
   namnger beslutsfattare och föredragande skrivs rollen i stället."* ADR-0018,
   bevakad av en invariant i testsviten. Den invarianten måste gälla även varje
   ny yta, inklusive en korrespondenslogg.
5. *"Måttet är maskinellt och har kända gränser, som redovisas i
   dokumentationen tillsammans med de fel som rättats under arbetet."*
   `docs/VERIFIERAT.md` slutar vid citatprövningen den 2 oktober. Felen som
   hittades den 2 till 6 oktober står bara i protokollloggen.

Därtill ett stående erbjudande: *"Vill ni läsa metodbeskrivningen innan den
publiceras skickar jag de delar som rör er myndighet om ni hör av er."* Hör en
myndighet av sig före den 23 oktober ska det gå att skicka samma dag.

---

## 2. Mått som är förregistrerade men inte räknade

Fyra mått står i protokollet och finns inte i kod eller data. Ett mått som inte
räknas redovisas som en lucka med skälet utskrivet; det uppskattas aldrig och
utelämnas aldrig i tysthet.

**Bilagemåtten.** Avsnitt 5: *"andel bilagor helt undanhållna"* och *"andel
bilagor levererade i bearbetat skick"*. **Prövade 2026-10-06 och redovisade som
en lucka den 7 oktober.** Sex bilagefiler kom in i hela insamlingen, och av de
114 dokument som hänvisar till innehåll i en bilaga gör 42 det med en mening ur
den nationella kontrollrapportmallen, som står där oavsett om något foto togs.
Materialet skiljer därför inte en undanhållen bilaga från en som aldrig fanns.
Skälet och talen står i `docs/VERIFIERAT.md`.

**Utlämningsgraden.** P11: *"levererade handlingar delat med det lägre av taket
och antalet som fanns"*. **Prövad 2026-10-06 och redovisad som en lucka.**
Nämnaren finns för 19 av 21 län, men täljaren finns inte i takets enhet: taket
räknar kontroller och beslut, leveransen kommer som filer, och nio län och
klasser har fler filer än taket tillåter kontroller. Skälet och underlaget står
i `docs/VERIFIERAT.md` och `data/utlamningsgrad.jsonl`.

**Dubbelförekomsten.** P1 och ombyggnad 1 varv 2: par där samma
kontrolltillfälle förekommer både som fristående rapport i A och som bilaga i B
är kontrastens starkaste jämförelse och ska redovisas separat. **Räknad
2026-10-06.** Paren går att läsa ur myndighetens eget ärendenummer i filnamnet,
och bara ett län, Västernorrland, har nummer som överlappar mellan klasserna:
20 ärenden, 20 av 20 dokument maskade i klass A och 0 av 20 i klass B.

**Avgiftsskrivelsemåttet.** Tillämpningsnot 5 deklarerar måttet samtidigt som
regeln: antal skrivelser i avgiftsfrågan fram till ett överklagbart beslut i
ärendet, och utfall i fyra klasser, *"för samtliga 21 länsstyrelser oavsett
utfall, inklusive de län där noll skrivelser behövdes"*. **Räknat 2026-10-06**
av steg 42: 41 skrivelser, och sex utfallsklasser i stället för fyra. Talen och
skälet till de två tillagda klasserna står i `docs/VERIFIERAT.md`. **Ställt på en
publicerad yta den 10 oktober 2026:** avsnittet om avgiftsstoppade begäranden på
sidan Sverige bär nu de 41 skrivelserna, de 16 län som aviserade en avgift, de
tre länen med flest skrivelser och alla sex utfallsklasserna, i båda
språkversionerna.

---

## 3. Avvikelserna från förregistreringen som ska stå i den publicerade metoden

Beslutslogg rad 10: nollresultat publiceras överst, i förskriven text. Tre delar
av förregistreringen gick inte att genomföra som skrivet, och de ska stå i
metoden, inte i en fotnot.

1. **Fältmåttet gick inte att räkna bokstavligt.** Maskningsgrad
   förregistrerades som andel maskerad yta plus andel maskerade fält.
   Handlingarna är löpande prosa utan fältstruktur, så fältdelen går inte att
   beräkna. Den ersattes 2026-08-17 av ett mått på täckt innehåll enligt
   ADR-0017, och utfallet blev ett nollresultat: noll dokument döljer brödtext
   bakom en ljus täckning, och de 236 dolda tecknen är sidhuvud under
   myndighetens egen vita ruta.
2. **Ytmåttet pekar fel för en av maskningsteknikerna.** Där texten under
   svärtningen är borttagen mäter ytan hur rutorna ritats, inte hur mycket som
   hålls inne; för den tekniken är antalet tecken det bättre måttet. Gränsen
   gäller det förregistrerade ytmåttet och ska läsas tillsammans med varje
   ytsiffra.
3. **Halva oanmäld-hypotesen går inte att pröva.** Avsnitt 10 begär både
   sambandet över län och skillnaden i bristandel mellan oanmälda och
   föranmälda kontroller inom samma län, djurslag och kontrolltyp. Den andra
   delen kräver aviseringsfältet korsat med bristfältet, och det uttaget
   lämnades inte ut. Den förskrivna nollresultatstexten påstår utfallet av just
   den prövningen och **stryks därför i stället för att återges**. Den del som
   gick att pröva skiljer inte ett svagt positivt samband från inget samband,
   och det enda signifikanta sambandet ligger i måttet över alla
   kontrolltypgrupper, där fem kontrolltyper bär utfallet i sitt eget namn,
   alltså i konkurrerande förklaring 2, kontrolltypsmix.

Avsnitt 9:s andra förskrivna text, den vid konsekvent maskning, publiceras inte,
eftersom dess villkor inte är uppfyllt: maskningen är inte konsekvent. Att
texten var skriven i förväg och inte utlöstes skrivs ut, så att läsaren ser
vilken av de två som gällde.

---

## 4. Osäkerheten i jämförelsetabellen

Risk 10 i avsnitt 12 har ett motmedel: *"intervall redovisas alltid; indexet
rangordnar inte myndigheter vars intervall överlappar."* P12-breven bär en ordnad
tabell över de län som levererat i klassen, utan intervall. Tabellen säger själv
att ordningen följer måttet och inte innebär någon bedömning, och att
myndigheter med samma andel delar plats.

Den publicerade tabellen ska därför vara **samma tabell som breven bär**, så att
varje myndighet ser exakt det den fått, **plus intervallet** och en mening om
att måttet inte skiljer myndigheter vars intervall överlappar. Att lägga till
intervallet ändrar ingen siffra och infriar motmedlet; att byta ut ordningen
hade gjort breven osanna.

---

## 5. Ordningen på publiceringsdagen

Ytorna öppnas i ett enda snitt. Skälet är not 8: den första yta som öppnas är
publicering för samtliga myndigheter, så en utspridd öppning ger de myndigheter
som ligger sent i ordningen en kortare faktisk svarstid än de tidiga.

**Före snittet, den 22 och 23 oktober, och en sista kontroll den 26:e**

1. Sista brevlådegenomgången, från posten till loggen och aldrig tvärtom, tråd
   för tråd per myndighet. Ett svar som kommer den 23 oktober är ett svar i tid
   och ska vara inne i materialet innan något öppnas. Genomgången görs om på
   morgonen den 26:e, eftersom helgen ligger mellan fristen och snittet.
2. PII-svep över hela ytlistan, inte bara repot: varje committad `data/*.jsonl`,
   varje fil i `docs/`, webbplatsens exporterade JSON, dataset-kortet, README.
   Sökningen gäller namn, adresser, telefonnummer, personnummer och filnamn.
3. Författarskapsrevision över **hela** historiken, inte sessionens commitar:
   `git log --format='%an <%ae>' | sort -u` ska ge en enda rad.
4. De tre grindarna körda var för sig med varje avslutskod läst, aldrig i samma
   kedja som en commit. Webbygget körs separat.
5. **`antumbraprojektet.se` är registrerad 2026-10-23** hos One.com, med
   namnservrarna ns01 och ns02 hos One.com och utgång 2027-10-23. Domänen är
   en förberedelse och ingen yta. `antumbra.org` stod i planen till samma dag,
   då den visade sig tagen sedan den 23 augusti, och `antumbra.se` är tagen
   sedan 2025-10-22. Kvar att göra före snittet: flytta zonen till Cloudflare,
   eftersom en Worker med egen domän kräver att zonen ligger där, och lägg in
   de två routerna i `web/wrangler.jsonc`.

**Snittet, måndag den 26 oktober**

6. Repot växlas till publikt. Historiken publiceras orörd enligt ADR-0005 och
   ADR-0003; ingen force-push, ingen omskrivning.
7. Webbplatsen deployas.
8. Datasetet publiceras.
9. Varje steg loggas som en egen rad med klockslag läst ur systemet i samma
   åtgärd som raden skrivs, aldrig ur minnet.
10. Först därefter inlägget på LinkedIn. Ett inlägg före de andra ytorna är
    publicering utan att det finns något att läsa.

**Efter snittet**

11. Ett svar som kommer efter den 23 oktober publiceras också, oavkortat, som en
    egen rad med sitt datum. Svarstiden löper inte om.
12. Den 26 oktober redovisas nämnarens läge, som en lucka och aldrig som ett
    avslag, enligt not 7 och not 9. **Mätt 2026-10-10 har samtliga 21 län
    svarat**, nitton med tal och två med att talet inte går att ta fram: Skåne
    därför att djurskyddskontrollerna inte registreras kopplat till djurslag, och
    Norrbotten med hänvisning till serviceskyldigheten i förvaltningslagen. Vad
    som redovisas är alltså inte uteblivna svar utan två nämnare som myndigheten
    själv säger inte finns sammanställda, med svaren ordagrant i
    `data/namnare.jsonl`.
13. JO-anmälan övervägs först nu, enhetligt för alla myndigheter som fortfarande
    inte svarat, enligt P10. Ingen anmälan under mätperioden.
14. Målen i kammarrätterna redovisas som pågående med diarienummer och yrkande.
    Ett pågående mål skjuter inte upp publiceringen, och en maskande myndighet
    beskrivs som avvikande från befintlig kammarrättspraxis för beslutsbilagor,
    aldrig som lagbrytare.

---

## 6. Hur ytorna ser ut

**Kodarkivet.** README leder med vad mätningen är, vad den visade och vad den
inte kan visa. Statusavsnittet daterar sig till publiceringsdagen och säger
insamlingen stängd, 43 av 43 med slutstatus, P12 avsänt och svarstiden ute.
Avsnittet om vad mätningen inte kan visa bär de tre avvikelserna i avsnitt 3
ovan och bilagemåtten som lucka.

**Webbplatsen.** Varje resultatsida har en tabellvy, ett underlag ned till
källan och ett avsnitt *Vad sidan inte visar*. Sidan Sverige bär mätningens
uppbyggnad, talen och jämförelsen. Sidan Handlingar bär en tavla per myndighet:
svarstid, avgiftshållning, maskningspraxis, bilagepraxis, och myndighetens eget
svar oavkortat eller noteringen att svar inte kommit. Sidan Metod bär
protokollet, händelseloggen som filtrerbar tidslinje, ADR-indexet,
AI-deklarationen, de förskrivna nollresultaten och avvikelserna från
förregistreringen. Inga kakor, ingen spårning, ljust och mörkt läge, WCAG 2.1
AA, allt utom livesöket utan JavaScript.

**Datasetet.** De svenska aggregaten som filer med schemadokumentation och
licens, så att vem som helst kan räkna om. Kortet ligger i `docs/DATASET.md`:
24 filer med radantal, kornighet per fil, metod, licens och de deklarerade
luckorna. Mottagna myndighetsdokument sprids aldrig vidare; det publicerade är
manifestet med kontrollsumma per fil.

**Språket på varje yta.** Aldrig en karaktärisering, alltid ett ordagrant citat
med källa. Inget påstående om lagbrott. Nollresultaten överst.

---

## 7. Beslut som återstår

1. **Korrespondensloggens omfång. Avgjort 2026-10-10, och båda leden är
   uppfyllda.** Registret `data/korrespondens.jsonl` bär samtliga 260 meddelanden
   på 196 rader, ordagrant och screenade, och varje rad säger i fältet
   `utelamnat` vad den lämnar ute. Datasidan säger numera samma sak i text: den
   citerade historiken, signaturblockets personuppgifter enligt ADR-0018,
   länkmålen, en rad som inte var annat än en länk, och domstolarnas
   engångslänkar, medan myndighetens egen funktionsbrevlåda och växel står kvar.
   Reglerna står i `docs/KORRESPONDENS.md` och i ADR-0024.
2. **Vad som är datasetet. Avgjort 2026-10-12: de svenska aggregaten.**
   Breven säger ett kodarkiv, en webbplats och *ett* dataset, i singular, och
   det de berörda myndigheterna fick siffror om är den svenska mätningen. DG
   SANTE-korpusen är kommissionens eget publicerade material; projektets bidrag
   där är parsningen och modellen, och den ligger kvar som ett eget dataset med
   eget kort i `docs/HF_DATASET.md`, publicerat på egna villkor och inte bundet
   till snittet. Följden för den 26:e: de svenska aggregaten behöver ett eget
   kort med schema per fil och licens, så att vem som helst kan räkna om talen.
3. **Publiceringsdagen. Avgjord 2026-10-12: måndag den 26 oktober.** Den 24:e
   är golvet enligt not 8, och måndagen var redan vald dag i avsnitt 0; nu är
   den bekräftad och ingen uppskjutning ska loggas enligt not 3.
