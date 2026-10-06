# Publiceringen: vad som ska vara gjort, i vilken ordning, och hur ytorna ser ut

Skriven 2026-10-06, fyra dagar efter att P12-paketen gick och arton dagar före
tidigaste publiceringsdag. Den skrivs nu, innan något svar på paketen har kommit
med en invändning mot en siffra, så att listan inte formas av vad myndigheterna
råkar svara.

Tidigaste publiceringsdag är **lördag 2026-10-24**, dagen efter svarstidens
slut. Regeln är tillämpningsnot 8: publicering enligt P12 är varje åtgärd som
gör en berörd myndighets egna resultat läsbara för någon utanför projektet, och
ingen sådan yta öppnas förrän tre veckor gått sedan paketen nådde samtliga
berörda myndigheter. Paketen gick 2026-10-02 mellan 13:12:22 och 13:15:24, med
svarsdatum den 23 oktober utskrivet i varje brev.

Listan nedan är inte en önskelista. Den är vad de 22 avsända breven utfäster,
vad protokollet förregistrerade, och vad som i dag saknas för att det ska gå att
infria.

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
   `data/protokoll_logg.jsonl`, 539 rader. En korrespondenslogg med
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
bilagor levererade i bearbetat skick"*, redovisade skilt från textmåttet, per
begäran, plus flaggan `utan_bilaga` när beslutstexten hänvisar till en bilaga
som inte följde med. Varken flaggan eller måtten finns i någon fil. Den
maskningsmätning som är gjord mäter dokument och sidyta, inte bilagor.

**Utlämningsgraden.** P11: *"levererade handlingar delat med det lägre av taket
och antalet som fanns"*. Nämnarna ligger i `data/namnare.jsonl` för 19 av 21
län, täljarna i leveransmanifestet, och kvoten beräknas inte någonstans. Not 9
slår fast att storleksläsningen inte rör utlämningsgraden, eftersom taket binder
i praktiskt taget varje län.

**Dubbelförekomsten.** P1 och ombyggnad 1 varv 2: par där samma
kontrolltillfälle förekommer både som fristående rapport i A och som bilaga i B
är kontrastens starkaste jämförelse och ska redovisas separat. Ingen kod letar
par. Utfallet kan bli noll identifierade par, och noll är då resultatet.

**Avgiftsskrivelsemåttet.** Tillämpningsnot 5 deklarerar måttet samtidigt som
regeln: antal skrivelser i avgiftsfrågan fram till ett överklagbart beslut i
ärendet, och utfall i fyra klasser, *"för samtliga 21 länsstyrelser oavsett
utfall, inklusive de län där noll skrivelser behövdes"*. Händelserna finns i
loggen, sexton län har minst en, och sammanställningen finns inte.

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

**Före snittet, den 22 och 23 oktober**

1. Sista brevlådegenomgången, från posten till loggen och aldrig tvärtom, tråd
   för tråd per myndighet. Ett svar som kommer den 23 oktober är ett svar i tid
   och ska vara inne i materialet innan något öppnas.
2. PII-svep över hela ytlistan, inte bara repot: varje committad `data/*.jsonl`,
   varje fil i `docs/`, webbplatsens exporterade JSON, dataset-kortet, README.
   Sökningen gäller namn, adresser, telefonnummer, personnummer och filnamn.
3. Författarskapsrevision över **hela** historiken, inte sessionens commitar:
   `git log --format='%an <%ae>' | sort -u` ska ge en enda rad.
4. De tre grindarna körda var för sig med varje avslutskod läst, aldrig i samma
   kedja som en commit. Webbygget körs separat.
5. `antumbra.org` registreras. Domänen är en förberedelse och ingen yta.

**Snittet, den 24 oktober**

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
12. Den 26 oktober redovisas saknad nämnare för de län som inte svarat, som en
    lucka och aldrig som ett avslag, enligt not 7 och not 9.
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

**Datasetet.** Aggregaten som filer med schemadokumentation och licens, så att
vem som helst kan räkna om. Mottagna myndighetsdokument sprids aldrig vidare;
det publicerade är manifestet med kontrollsumma per fil.

**Språket på varje yta.** Aldrig en karaktärisering, alltid ett ordagrant citat
med källa. Inget påstående om lagbrott. Nollresultaten överst.

---

## 7. Beslut som återstår

1. **Korrespondensloggens omfång.** Antingen byggs en logg med myndigheternas
   meddelanden i sin helhet, ordagrant och screenad, eller så står det på den
   publicerade ytan vilka delar som inte återges, nämligen logistik, länkar och
   signaturer. Brevens lydelse pekar på det första.
2. **Vad som är datasetet** i brevens mening: de svenska aggregaten, DG
   SANTE-korpusen hos Hugging Face, eller båda.
3. **Om publiceringen sker den 24 oktober eller senare.** Datumet är ett golv
   och inget tak. Skjuts det upp loggas uppskjutandet, enligt not 3.
