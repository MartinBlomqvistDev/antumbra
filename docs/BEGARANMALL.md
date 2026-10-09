# Antumbra: begäranmallar och handläggningsprotokoll

Projektnamn beslutat 2026-08-02. **Antumbra**, domän `antumbra.org`, registreras
när det finns något att visa. Produkten heter fortfarande öppenhetsindexet.
Undertitel utåt: *att göra tillsynen mätbar*. Formuleringen "tillsyn över
tillsynen" är projektets analytiska kärna och stannar i interna anteckningar;
den gör dig till motpart innan någon läst en rad.

Skriven 2026-08-01, ombyggd 2026-08-02 i två steg: först till en
tvåbegärandedesign, sedan breddad till tre djurslag och utökad med begäran C.
Paragrafhänvisningarna är kontrollerade ordagrant mot Regeringskansliets
rättsdatabaser 2026-08-01 och 2026-08-02, inklusive 2 kap. 6 och 7 §§ TF.
Koderna 1.10-i och 1.11 är verifierade mot miljöprövningsförordningen (2013:251)
2026-08-02, och siffrorna ur Nationell djurskyddsrapport 2024 (Jordbruksverket,
OVR737) är kontrollerade mot rapporten samma dag. Kammarrättsavgörandena i
avsnitt 11 är inte kontrollerade i fulltext; källan och förbehållet står där.
Ändringsloggen står i avsnitt 13.

---

## 1. Designen: tre begäranden

Projektet skickar tre begäranden samma dag. A och B går till samtliga 21
länsstyrelser, C till Jordbruksverket.

**Begäran A** avser fristående kontrollrapporter, där kammarrättspraxis har
godtagit maskning av brister som affärs- och driftförhållanden. **Begäran B**
avser beslut om föreläggande i djurskyddsärenden med bilagor, där bilagepunkt 30
till 9 § OSF uttryckligen undantar beslut från sekretessen och där KR Sundsvall
2682-21 fann att även bilagorna delar beslutets status. Kontrasten är mätvärdet:
samma myndighet, samma dokumentinnehåll, två rättsliga statusar. En myndighet
som maskar beslutshandlingarna i B lika hårt som rapporterna i A avviker från
den kammarrättspraxis som finns för beslutsbilagor. Starkast blir jämförelsen
när samma kontrolltillfälle förekommer i båda: en gång som fristående rapport i
A, en gång som bilaga till beslutet i B. Sådana par redovisas separat.

**Begäran C** avser räknetal ur djurskyddskontrollregistret: antal kontroller
fördelade på oanmälda och föranmälda, och hur många av vardera som gav minst en
konstaterad brist. C mäter nämnaren till det A och B mäter täljaren till, och
den prövar en förregistrerad hypotes (avsnitt 10). Jordbruksverket publicerar
ett gap på 51 procentenheter i andel kontroller med brister mellan
länsstyrelser, skriver att skillnaden inte går att utläsa av statistiken, och
gissar på olika fokusområden. Andelen oanmälda kontroller publiceras inte för
lantbrukets djur, trots att fältet finns per kontroll. C begär ut det.

**Djurslagen är nötkreatur, gris och fjäderfä i A, B och C.** Utfallslagret
breddades från gris och fjäderfä eftersom djurskyddskontrollen är
djurslagsoberoende och merparten av kontrollerna görs på nötkreatur. Kravlagret
förblir gris och fjäderfä, och asymmetrin är regelverkets egen: kod 1.10-i i
miljöprövningsförordningen (2013:251) är IED-nivån, mer än 40 000 platser
fjäderfä, 2 000 växande grisar över 30 kg eller 750 suggor, och Jordbruksverkets
centrala publicering stannar där. Nötkreatur är tillståndspliktiga på B-nivå
enligt kod 1.11, stadigvarande djurhållning av nötkreatur, hästar eller minkar
med mer än 400 djurenheter, men de besluten publiceras inte centralt.
Nötbesluten finns alltså men får sökas hos varje myndighet; det är ett senare
och separat spår, och asymmetrin skrivs ut i metodavsnittet.

---

## 2. Begäran A

Skickas med e-post till myndighetens officiella brevlåda (registraturen). Ämnesrad
och brödtext identiska till alla 21. Enda platshållare: myndighetens namn.

**Ämnesrad:** `Begäran om allmän handling: kontrollrapporter från djurskyddskontroll`

```
Till Länsstyrelsen i [län]

Hej!

Jag begär kopior av kontrollrapporter från djurskyddskontroller av
anläggningar som håller nötkreatur, grisar eller fjäderfä.

Begäran avser de 20 senast genomförda kontrollerna, räknat efter
kontrolldatum, under perioden 1 januari 2024 till och med 31 december
2025. Har färre än 20 sådana kontroller genomförts under perioden avser
begäran samtliga. Med kontrollrapport avser jag den rapport som
upprättas efter genomförd kontroll enligt djurskyddslagen (2018:1192).
Begäran omfattar även bilagor till rapporterna, till exempel
fotobilagor.

Jag önskar handlingarna i elektronisk form, som PDF, till denna
e-postadress. Om en uppgift i en handling inte kan lämnas ut önskar jag
handlingen i övriga delar.

Om en avgift tas ut önskar jag besked om beloppet innan handlingarna
skickas.

Med vänliga hälsningar,
Martin Blomqvist
cm.blomqvist@gmail.com
```

---

## 3. Begäran B

Skickas samma morgon som A, som ett separat e-brev, utan hänvisning till A.
Samma avsändare, samma mottagare, egen ämnesrad.

**Ämnesrad:** `Begäran om allmän handling: beslut om föreläggande i djurskyddsärenden`

```
Till Länsstyrelsen i [län]

Hej!

Jag begär kopior av beslut om föreläggande i djurskyddsärenden som
gäller hållning av nötkreatur, grisar eller fjäderfä. Med föreläggande
avser jag beslut enligt 8 kap. 9 § djurskyddslagen (2018:1192) eller
enligt de EU-bestämmelser som lagen kompletterar.

Begäran avser de 10 senast meddelade besluten, räknat efter
beslutsdatum, under perioden 1 januari 2022 till och med 31 december
2025. Har färre än 10 sådana beslut meddelats under perioden avser
begäran samtliga. Begäran omfattar även bilagor till besluten, till
exempel kontrollrapporter och fotobilagor. Beslut om omhändertagande av
djur och beslut om djurförbud ingår inte i begäran.

Jag önskar handlingarna i elektronisk form, som PDF, till denna
e-postadress. Om en uppgift i en handling inte kan lämnas ut önskar jag
handlingen i övriga delar.

Om en avgift tas ut önskar jag besked om beloppet innan handlingarna
skickas.

Med vänliga hälsningar,
Martin Blomqvist
cm.blomqvist@gmail.com
```

---

## 4. Begäran C

Skickas till Jordbruksverkets officiella brevlåda samma måndag, efter A och B.
En mottagare, ingen platshållare.

**Ämnesrad:** `Begäran om allmän handling: statistikuppgifter ur djurskyddskontrollregistret`

```
Till Statens jordbruksverk

Hej!

Jag begär en sammanställning av uppgifter ur
djurskyddskontrollregistret om djurskyddskontroller av nötkreatur,
grisar och fjäderfä under åren 2024 och 2025.

Jag önskar antal genomförda fysiska kontroller per länsstyrelse, år och
djurslag, fördelat på

1. oanmälda respektive föranmälda kontroller,
2. kontrolltyp, till exempel rutinkontroll, kontroll efter anmälan och
   uppföljande kontroll,
3. kontroller med minst en konstaterad brist respektive utan
   konstaterad brist.

Jag begär endast antalsuppgifter, inga uppgifter om enskilda
kontrollobjekt. Kan någon del inte tas fram med rutinbetonade åtgärder
önskar jag besked om vilken del, och de delar som kan tas fram.

Jag önskar sammanställningen i elektronisk form, till exempel som
Excel eller CSV, till denna e-postadress.

Om en avgift tas ut önskar jag besked om beloppet innan
sammanställningen skickas.

Med vänliga hälsningar,
Martin Blomqvist
cm.blomqvist@gmail.com
```

---

## 5. Rättslig motivering

**Rätten till kopia.** 2 kap. 16 § första stycket TF: den som önskar ta del av en
allmän handling har rätt att mot en fastställd avgift få en avskrift eller kopia,
till den del handlingen får lämnas ut. A och B begär kopior, eftersom mätningen
kräver dokument som kan analyseras maskinellt.

**C:s rättsliga konstruktion, och varför den håller.** En myndighet är inte
skyldig att skapa nya handlingar på begäran, men 2 kap. 6 § andra stycket TF
gör en sammanställning till en förvarad handling på ett villkor: "En
sammanställning av uppgifter ur en upptagning för automatiserad behandling
anses dock förvarad hos myndigheten endast om myndigheten kan göra
sammanställningen tillgänglig med rutinbetonade åtgärder och inte annat följer
av 7 §." Begränsningen i 2 kap. 7 § TF gäller endast sammanställningar som
innehåller personuppgifter; C begär uttryckligen bara antalsuppgifter, så 7 §
är inte tillämplig. Det som återstår att pröva är rekvisitet rutinbetonade
åtgärder. C är formulerad för att hamna på rätt sida på tre sätt: fälten som
efterfrågas finns per kontroll i registret, sammanställningen är en korstabell
av registerfält utan bedömningsmoment, och delbarhetsmeningen gör att ett
delvis rutinbetonat uttag ger ett delvis bifall i stället för ett helt avslag.
Om Jordbruksverket ändå avslår med hänvisning till att uttaget kräver ny
bearbetning är det ett överklagbart beslut, och det är samtidigt ett resultat:
myndigheten som ansvarar för den nationella kontrollstatistiken kan då inte
rutinmässigt ta fram fördelningen oanmält mot föranmält ur sitt eget register.

**C:s mottagare.** C går till Jordbruksverket ensamt. Syftet är nämnardata och
hypotesprövning; ett nationellt uttag ur ett register ger enhetligt format,
medan 21 lokala uttag ger 21 lokala tolkningar av samma fråga. Valet skyddar
också A och B: ett tredje brev till länsstyrelserna samma morgon hade höjt
granskningssignalen i det utskick där signalen ska vara låg. Om Jordbruksverket
avslår och överklagandet inte når fram finns en reservväg: samma fråga till de
21 länsstyrelserna som en egen senare våg, tidigast efter dag 40, så att den
inte kan påverka A- och B-handläggningen.

**Åtalsanmälningar ingår inte i C.** Hypotesen gäller konstaterade brister, och
där är åtalsanmälan fel mått: den är sällsynt, styrs av annan praxis och bär
brottsmisstanke mot enskilda. Att ta med den hade ökat sekretessytan och gjort
en ren räknetalsbegäran svårare att bifalla. Den kan begäras separat senare om
bristmåttet visar sig behöva valideras.

**Skyndsamheten.** 2 kap. 16 § andra stycket TF: "En begäran att få en avskrift
eller kopia av en allmän handling ska behandlas skyndsamt." Detta är klockan som
mäts, för C såväl som för A och B. Mallarna åberopar inte paragrafen; en
ordinarie begäran gör inte det, och skyndsamhetskravet gäller oavsett.

**Ingång via registraturen.** 2 kap. 17 § TF: begäran görs hos den myndighet som
förvarar handlingen, och den myndigheten prövar den. Den officiella brevlådan är
den enda ingång som garanterat finns och fungerar likadant hos alla. Intern
routning är en del av den praxis som mäts, och att A och B kan routas till olika
funktioner internt är i så fall också praxis.

**Djurslagsavgränsningen.** Nötkreatur, gris och fjäderfä är produktionsdjuren
där kontrollvolymen ligger, och avgränsningen är körbar direkt mot
ärendesystemens djurslagsfält. Den utesluter hästar, sällskapsdjur, får och
anhopningsfall utan att kräva ett storleksfält som ärendesystemen sannolikt
saknar. Ett storlekskriterium hade också smugit in en bedömning hos
registratorn, och varje bedömningsmoment är en källa till tolkningsspridning.

**Artmixen hanteras i analysen, inte i urvalsregeln.** De 20 senaste
kontrollerna ger olika djurslagsmix i olika län; Skåne blir grisdominerat och
Norrland nötdominerat. Om maskningspraxis skiljer sig åt mellan djurslag blir
länsjämförelsen då förväxlad med mixen. Stratifiering med fast antal per djurslag
förkastades av tre skäl. Tomma celler gör den utlovade identiska mixen
ouppnåelig ändå; fjäderfäkontrollerna är för få i stora delar av landet. Tre
separata sökningar per registrator tredubblar tolkningsytan i den risk som
redan är rankad högst. Och B kan inte stratifieras alls på sina volymer, så
A och B hade fått olika urvalslogik. Den deterministiska regeln förblir därför:
de 20 senaste kontrollerna oavsett djurslag, sorterade på kontrolldatum.
Djurslag registreras per handling, maskningsgrad redovisas per djurslag,
länsjämförelser görs inom djurslag eller justerade för mix, och C levererar
just den fördelning per län och djurslag som justeringen behöver.

**Preciseringen av A.** Avgränsningen är dokumenttyp (kontrollrapport), rättslig
grund (kontroll enligt djurskyddslagen), djurslag, period (två kalenderår) och
ett tak (20 senaste, sorterade på kontrolldatum). Det räcker för att
handlingarna ska kunna identifieras direkt i ärendesystemet. Kravet på
precisering framgår inte av någon enskild paragraf utan av praxis om att
myndigheten inte behöver göra omfattande efterforskningar; den praxisen har
inte verifierats mot rättsfall här, men begäran ligger med god marginal på rätt
sida.

**Preciseringen av B.** Föremålet är beslut om föreläggande, med 8 kap. 9 §
djurskyddslagen (2018:1192) som huvudgrund; paragrafen är verifierad 2026-08-02
och täcker även förelägganden enligt de EU-bestämmelser lagen kompletterar.
Formuleringen "eller enligt de EU-bestämmelser som lagen kompletterar" finns med
för att en registrator inte ska sortera bort förelägganden som beslutats direkt
på EU-grund. Beslut om djurförbud (9 kap. 1 §) och omhändertagande (9 kap. 5 §)
är uttryckligen undantagna. De riktas i hög grad mot fysiska personer i utsatta
situationer, och projektets subjekt är staten; att dra in sådana handlingar vore
både utanför syftet och en onödig integritetsrisk. Rättsligt är undantaget också
en renodling: kontrastmätningen gäller verksamhetsriktade beslut där bilagepunkt
30 och KR Sundsvall 2682-21 är direkt tillämpliga.

**B:s längre period och lägre tak.** Förelägganden är ovanligare än kontroller.
Breddningen till nötkreatur gör B väsentligt mindre gles, men fyraårsfönstret
2022 till 2025 och taket 10 behålls: det kostar inget i jämförbarhet, och det
försäkrar kontrollgruppen även i län där förelägganden är sällsynta. Asymmetrin
mot A:s tvåårsperiod redovisas öppet. B ska ge en rättslig kontrast mellan två
handlingsklasser, och det kräver att det finns beslut att jämföra med.
Perioderna behöver därför inte matcha varandra.

**Bilagorna ingår i A och B, och det är ett medvetet val.** En tidigare version
av mallen undantog fotobilagor. Det var fel av tre skäl.

Rättspraxis behandlar text och bild lika. KR Sundsvall 2682-21 gällde en
kontrollrapport **och en fotobilaga** som bilagor till ett beslut, och båda
ansågs falla utanför sekretessen. Utan bilderna täcker mätningen bara hälften
av rättsfrågan.

**Rättelse 2026-09-09.** Här stod tidigare att i den motsatta linjen, KR
Jönköping 549-19 med flera, skyddades uttryckligen "beskrivningar och bilder
av konstaterade brister". Alla tre avgörandena i den linjen är nu lästa i
fulltext och ordet bilder finns inte i något av dem; formuleringen kom ur
referatet. Motiveringen ovan vilar därför på 2682-21 ensam, som är verifierad,
och det räcker: den domen gällde uttryckligen en fotobilaga.

**Tillägg 2026-09-10.** Formuleringen finns, i en annan dom än referatet angav.
KR Göteborg 2605-18 skriver att klaganden *"efterfrågat uppgifter i form av
beskrivningar och bilder på konstaterade brister"* och håller de maskade delarna
hemliga; se avsnitt 11. Det andra benet står därmed åter, med rätt källa.

Uteslutningen skulle dessutom radera varians. Att undanhålla en hel bilaga är
den kraftigaste maskning som finns, och en myndighet som gör det skulle få
samma utfall som en som lämnar ut, eftersom ingen av dem tillfrågats.

Kostnadsskälet finns inte längre. Enligt P5 godtas ingen avgift oavsett
sidantal, så bilagornas omfång påverkar inte budgeten.

**Bilagor mäts som en egen klass.** Andel svärtad yta fungerar på textsidor men
inte på bilder, där maskning normalt sker genom att hela bilagan undanhålls
eller att bilden suddas. Bilagor får därför två egna mått: **andel bilagor helt
undanhållna** och **andel bilagor levererade i bearbetat skick**. De redovisas
skilt från textmåttet, per begäran A och B, och slås aldrig ihop med ytmåttet.
Ett beslut som saknar bilaga trots att beslutstexten hänvisar till en flaggas
`utan_bilaga`.

**Bilder publiceras aldrig.** Mätningen gäller om myndigheten lämnade ut dem,
inte vad de föreställer. Samma disciplin gäller som vid återvinningsbar
maskning: fyndet redovisas och innehållet stannar hos mig.

**Taken.** Taken gör omfånget identiskt över myndigheter med olika
verksamhetsvolym och håller begärandena lätta att bifalla. Ett tak är en
frivillig begränsning av det egna anspråket och behöver ingen rättslig grund.

**Delutlämnande.** Meningen om att få handlingen i övriga delar speglar 2 kap.
16 § TF ("till den del handlingen får lämnas ut") och förebygger att en enstaka
sekretessbedömd uppgift leder till avslag på hela handlingen. Den signalerar
ingen granskning; det är en standardformulering. C:s delbarhetsmening fyller
samma funktion för sammanställningen.

**Elektronisk form.** 2 kap. 16 § första stycket TF: en myndighet är inte skyldig
att "i större utsträckning än vad som följer av lag lämna ut en upptagning för
automatiserad behandling i annan form än utskrift". Ingen ovillkorlig rätt till
PDF eller CSV finns alltså. Mallarna uttrycker ett önskemål utan krav, vilket i
praktiken bifalls eftersom handlingarna är digitalt födda och maskning sker
digitalt. Reservplanen vid pappersleverans finns i P7.

**Avgiftsbeskedet.** 6 kap. 1 a § andra stycket OSL: myndigheten får i ett
enskilt fall besluta att avgiften ska betalas innan kopian lämnas ut. Beskedet i
förväg är förutsättningen för nollavgiftslogiken i P5: inget expedieras mot
avgift utan att det fasta svaret först har gått ut. Avgiftsnivån enligt 16 §
avgiftsförordningen (1992:191): avgift först från tio sidor, 50 kronor för tio
sidor och 2 kronor per sida därutöver. Mallarna nämner inte att avgift inte kan
betalas; ett sådant tillägg kunde få enskilda myndigheter att efterge en avgift
de annars tagit ut, och då förstörs avgiften som mätvärde.

**Namngiven avsändare.** 2 kap. 18 § TF ger rätt att vara anonym; myndigheten får
inte efterforska identitet eller syfte mer än sekretessprövningen kräver. Rätten
utnyttjas inte, av tre skäl. En e-postbegäran är ändå inte anonym i praktiken.
Ett avslag som ska överklagas enligt 2 kap. 19 § TF och 6 kap. 7-8 §§ OSL kräver
en adressat som kan vara part. Och identisk identitet överallt tar bort
avsändaren som variabel.

**Inga rättshänvisningar utöver definitionerna, och inget ändamål.** En begäran
behöver inte motiveras. Lagrummen i mall B och uttrycket rutinbetonade åtgärder
i mall C är definitioner av föremålet, inte argument. Ett oombett ändamål vore
extra information som skiljer begäran från en ordinarie sådan; frågan besvaras i
stället med den förskrivna texten i avsnitt 6 och loggas som händelse.

**Sekretessgrunden som väntas åberopas mot A och B.** 30 kap. 23 § OSL ger
sekretess i statlig tillsynsverksamhet över näringslivet, i den utsträckning
regeringen föreskriver: punkt 1 för affärs- eller driftförhållanden med rakt
skaderekvisit ("om det kan antas att den enskilde lider skada om uppgiften
röjs"), punkt 2 för den som trätt i affärsförbindelse med tillsynsobjektet, utan
skaderekvisit. Föreskriften är 9 § offentlighets- och sekretessförordningen
(2009:641) med bilagan; punkt 30 omfattar "utredning, tillståndsgivning och
tillsyn enligt lagstiftningen om djurskydd" och har en uttrycklig begränsning:
**"sekretessen gäller inte beslut i ärenden."** Rakt skaderekvisit betyder
presumtion för offentlighet. Mot C har 30 kap. 23 § lite att bita i: rena
antalsuppgifter per län röjer inga enskildas affärsförhållanden.

**Överklagandevägen.** 2 kap. 19 § TF: avslag och förbehåll får överklagas,
beslut av annan myndighet än statsråd överklagas till domstol, och överklagandet
ska alltid prövas skyndsamt. 6 kap. 7 § OSL: en enskild får överklaga beslut att
inte lämna ut en handling eller att lämna ut med förbehåll. 6 kap. 8 § OSL:
sådana beslut överklagas till kammarrätt. 43 § förvaltningslagen (2017:900):
överklagandet ställs till överinstansen men ges in till beslutsmyndigheten. 44 §
samma lag: fristen är tre veckor från delfåendet. Förutsättningen är ett
myndighetsbeslut; 6 kap. 3 § OSL ger rätt att begära myndighetens prövning och
ett skriftligt beslut, och myndigheten ska informera om den möjligheten.

---

## 6. Förskrivet svar på fråga om identitet och ändamål

Skickas ordagrant, inom en arbetsdag, endast om myndigheten frågar. Samma text
oavsett om frågan gäller A, B eller C, och oavsett om den kommer från en
länsstyrelse eller Jordbruksverket. Frågan och svaret loggas som händelser.

```
Hej!

Tack för er fråga. Jag heter Martin Blomqvist och är privatperson.
Ändamålet är att sammanställa och analysera uppgifter om hur
djurskyddskontrollen genomförs och redovisas. Uppgifter som kan hänföras
till enskilda djurhållare kommer inte att publiceras; eventuell
publicering sker i aggregerad form.

Med vänliga hälsningar,
Martin Blomqvist
```

Svaret är sant, komplett i det prövningen behöver och identiskt överallt. Det
nämner inte att myndigheters praxis jämförs, eftersom 2 kap. 18 § TF begränsar
frågerätten till vad sekretessprövningen kräver; prövningen enligt 30 kap. 23 §
OSL gäller risken för skada för den enskilde djurhållaren, och det är den risken
svaret uttalar sig om. Utfästelsen om aggregerad publicering är bindande: inga
utdrag knyts till identifierbara företag, och bilder publiceras aldrig.

---

## 7. Handläggningsprotokollet

Alla tidsangivelser i arbetsdagar från avsändningsdagen (dag 0) om inget annat
anges. Varje händelse loggas med datum, klockslag, kanal, myndighet, begäran (A,
B eller C) och händelsetyp. Loggen publiceras i sin helhet.

**Loggen förs i den ordning händelser loggas, inte i den ordning de inträffade.** Raderna läggs till och ändras aldrig, så en händelse som loggas i efterhand hamnar sist även om dess datum är tidigare, och en rättelse av en tidigare notering skrivs som en egen rad. Det gör loggföringen granskbar i sig: när något fördes in syns lika väl som när det hände. En läsare som vill ha kronologi sorterar på datum och klockslag.

**P0. Avsändning.** Alla 43 begäranden skickas samma dag, en måndag, från
cm.blomqvist@gmail.com. Begäran A till alla 21 länsstyrelser mellan 08.00 och
08.30, begäran B till alla 21 mellan 08.30 och 09.00, begäran C till
Jordbruksverket mellan 09.00 och 09.30. Separata e-brev utan korshänvisningar.
Ordningen är fast. Att C går till en annan myndighet är en del av
sekvenseringslösningen: den kan inte slås ihop med A eller B och den höjer inte
granskningssignalen hos länsstyrelserna.

**P0b. Sammanslagning.** Om en länsstyrelse hanterar A och B som ett ärende,
svarar samlat eller ger ett gemensamt diarienummer flaggas myndigheten
`sammanslagen`. Ingen begäran om särskiljning skickas; att kräva delning vore en
signal som inte alla myndigheter får. Svarstiden tillskrivs då båda
begärandena, och alla klassmått beräknas ändå per handlingsklass, eftersom
handlingarna är åtskiljbara i efterhand. Sammanslagningen redovisas som egen
praxisobservation.

**P1. Mått.** T1 = arbetsdagar till första substantiella besked per begäran
(leverans, avgiftsbesked, förtydligandefråga eller beslut; autosvar räknas
inte). T2 = arbetsdagar till fullgjort utlämnande eller slutligt beslut per
begäran. Kontrastmåttet = skillnaden i maskningsgrad mellan klass A och klass B
inom samma myndighet, beräknad inom djurslag där underlaget räcker; par där
samma kontrolltillfälle förekommer i både A och B redovisas separat. C har inga
maskningsmått; C:s mått är svarstid, leveransstatus och datainnehåll.

**P2. Påminnelse 1, dag 5.** Skickas per begäran om ingen kontakt alls skett för
den begäran:

```
Hej!

Den [datum] skickade jag nedanstående begäran om allmän handling. Jag
har ännu inte fått något besked och vill därför påminna om den. Jag ber
om besked om när handlingarna kan lämnas ut.

Med vänliga hälsningar,
Martin Blomqvist

[ursprunglig begäran citerad]
```

**P3. Påminnelse 2, dag 10.** Per begäran, om fortfarande ingen kontakt:

```
Hej!

Jag återkommer om min begäran av den [datum], se nedan, som ännu inte
besvarats. Enligt 2 kap. 16 § tryckfrihetsförordningen ska en begäran om
kopia av allmän handling behandlas skyndsamt. Jag ber om besked snarast.

Med vänliga hälsningar,
Martin Blomqvist

[ursprunglig begäran citerad]
```

**P4. Förtydligandefråga från myndigheten.** Besvaras inom en arbetsdag. Svaret
får endast bestå av den förskrivna ändamålstexten (avsnitt 6) om frågan gäller
identitet eller syfte, eller en ordagrann upprepning av den aktuella begärans
avgränsningar om frågan gäller omfånget. För C gäller därtill: om frågan avser
formatet eller uttagets delar hänvisas till delbarhetsmeningen i begäran, utan
nya dimensioner och utan att någon dimension släpps. Omfånget ändras aldrig i
detta steg.

**P5. Avgiftsbesked. Ingen avgift godtas, oavsett belopp.** Budgeten för
projektet är noll kronor, och det går inte att förhandla om i det enskilda
fallet. Regeln är därför deterministisk och likadan mot alla.

Vid varje avgiftsbesked, oavsett belopp, skickas inom tre arbetsdagar:

    Tack för beskedet. Jag har inte möjlighet att betala en avgift.

    Jag begränsar därför min begäran till [avsmalningen], och önskar
    handlingarna i elektronisk form som PDF till denna e-postadress.

    Kvarstår en avgift även för den begränsade begäran avstår jag från
    kopior. Jag ber i så fall om besked om det, och om beslut i frågan
    om avgiften.

Avsmalningen per begäran: för A "de fem senast genomförda kontrollerna under
samma period", för B "de fem senast meddelade besluten under samma period", för
C "uppgifterna för år 2024". Gäller ett samlat besked flera begäranden skickas
svaret för var och en, med respektive avsmalning.

Kvarstår avgift efter avsmalningen: **inga kopior hämtas ut.** Begäran flaggas
`avgiftsstoppad` i datasetet, bidrar med svarstid, utlämningsgrad och
avgiftsuppgift, men saknar maskningsgrad. Bortfallet redovisas öppet i
analysen; det får aldrig döljas genom att nämnaren tystas ned.

**Avgiften är ett eget mätvärde.** Belopp, grund, vilken begäran den avsåg och
om den gällde elektroniskt utlämnande loggas. Att en myndighet tar betalt för
samma handling som en annan mailar utan avgift är i sig en observation, och den
hör hemma i öppenhetsindexet.

Ingen annan avsmalning görs, oavsett vad myndigheten föreslår.

**P6. Fullständig leverans.** Loggas per begäran med datum, antal handlingar,
antal sidor, antal bilagor och leveransform. För C loggas vilka dimensioner som
levererades och vilka som saknades. Ingen ytterligare åtgärd mot myndigheten.

**P7. Pappersleverans.** Handlingarna skannas med fast profil, 300 dpi gråskala,
samma skanner för allt material. Leveransformen loggas som variabel och
maskningsmåttets känslighet för leveransform redovisas i analysen.

**P8. Maskerad eller delvis leverans av A eller B.** Inom tre arbetsdagar
skickas, per begäran, oavsett maskningens omfattning eller angiven grund:

```
Hej!

Tack för handlingarna som lämnades ut den [datum]. Delar av innehållet
har maskerats. Jag begär att frågan om utlämnande prövas av myndigheten
och att jag får ett skriftligt beslut som kan överklagas, i enlighet med
6 kap. 3 § offentlighets- och sekretesslagen (2009:400). Jag ber att
beslutet anger vilka bestämmelser som har tillämpats.

Med vänliga hälsningar,
Martin Blomqvist
```

Undanhållen bilaga räknas som maskning och utlöser samma skrivelse.
Maskningsgraden mäts på den första leveransen, före denna skrivelse; skrivelsen
kan därför inte påverka det måttet. Avslås C helt eller delvis begärs på samma
sätt myndighetens prövning och ett skriftligt beslut, med samma brevstomme och
med "handlingarna" utbytt mot "sammanställningen".

**P9. Överklagande.** Ett beslut om A eller B överklagas när minst ett av
följande är uppfyllt: (a) beslutet anger ingen tillämplig bestämmelse; (b)
maskning i klass A med stöd av 30 kap. 23 § OSL träffar en uppgiftstyp som
minst tre andra länsstyrelser lämnat ut omaskad i samma handlingsklass; (c)
maskning eller undanhållande i klass B, alltså i beslut eller beslutsbilagor,
med stöd av 30 kap. 23 § OSL, i strid med undantaget i bilagepunkt 30 till 9 §
OSF och med KR Sundsvall 2682-21. Högst fem överklaganden för A och B totalt;
kriterium (c) har företräde, därefter (a), därefter (b) i fallande
avvikelsestorlek. Ett avslag på C överklagas alltid och räknas utanför
femtaket; frågan om rutinbetonade åtgärder är billig att driva och värd ett
avgörande i sig. Överklagandet ställs till kammarrätten, ges in till
beslutsmyndigheten (43 § förvaltningslagen) och skickas inom 14 kalenderdagar
från delfåendet; fristen är tre veckor (44 § förvaltningslagen).

**P10. Uteblivet svar.** Ingen JO-anmälan görs under mätperioden. Dag 40 stängs
datainsamlingen för svarstidsmåttet; begäranden utan leverans och utan beslut
redovisas som uteblivet svar. Därefter skickas en sista påminnelse. Eventuell
JO-anmälan övervägs först efter publicering, enhetligt för alla myndigheter som
då fortfarande inte svarat.

**P11. Nämnare för utlämningsgrad.** Efter leverans, tidigast dag 40, ställs en
identisk uppföljningsfråga till samtliga länsstyrelser: "Hur många
djurskyddskontroller av anläggningar med nötkreatur, grisar respektive fjäderfä
genomförde ni under perioden 1 januari 2024 till 31 december 2025, och hur
många beslut om föreläggande i djurskyddsärenden som gäller hållning av
nötkreatur, grisar eller fjäderfä meddelade ni under perioden 1 januari 2022
till 31 december 2025?" Svaren jämförs med C-datat och med Jordbruksverkets
officiella kontrollstatistik; avvikelser mellan källorna redovisas.
Utlämningsgrad per begäran = levererade handlingar delat med det lägre av taket
och antalet som fanns.

**P11b. Reservväg för C.** Om Jordbruksverket avslår C och överklagandet inte
ger utlämnande skickas samma begäran, anpassad till "era djurskyddskontroller",
till de 21 länsstyrelserna som en egen våg, tidigast dag 40. Vågen flaggas
`c_reserv` och dess svar jämförs aldrig med huvudutskickets svarstider.

**P12. Genmäle.** Varje berörd myndighet får sina egna resultat före
publicering, med tre veckors svarstid. Svaren publiceras oavkortade.

---

## 8. Beslutslogg

| # | Vägval | Beslut | Avgörande skäl | Förkastat alternativ och varför |
| --- | --- | --- | --- | --- |
| 1 | Omfång A | Kontrollrapporter med bilagor, nöt/gris/fjäderfä, 2024-2025, tak 20 | Identisk definition som fungerar i alla ärendesystem; taket ger lika omfång | Namngiven anläggningslista ur Jordbruksverkets 237 beslut: starkare koppling krav-utfall, men kräver platshållare per län, ser ut som kartläggning av utpekade företag och ger noll i tre län |
| 2 | Län utan IED-anläggningar | Alla 21 ingår, alla mått | Begäran är djurslagsbaserad; djurhållning med kontroller finns i alla län | Utesluta de tre: hade gjort indexet till ett 18-länsindex utan skäl, eftersom IED-status inte styr begäran |
| 3 | Anonymitet | Namngiven, endast namn och e-post | Överklagande kräver part; e-post är ändå inte anonym; identisk identitet tar bort avsändarvariabeln | Anonym begäran: grundlagsskyddad möjlighet, men gör avslagsgrenen av mätningen omöjlig att driva |
| 4 | Ändamål | Anges inte oombedd; förskrivet identiskt svar vid fråga | Oombett ändamål skiljer begäran från en ordinarie och kan påverka prövningen; frågan i sig är en mätpunkt | Ändamål i begäran: kunde minska frågor och därmed spara tid, men flyttar försöksbetingelsen |
| 5 | Överklagbart beslut | Begärs först efter maskad leverans, enhetligt | Första leveransens maskning sker då opåverkad; beslutskravet i förväg riskerar försiktigare maskning | Kravet i begäran: juridiskt verkningslöst i förväg och maximal observatörseffekt |
| 6 | Leveransform | Önskemål om PDF/CSV utan krav; skanningsprotokoll som reserv | Ingen rätt till elektroniskt finns (2 kap. 16 § TF); önskemål bifalls i praktiken då handlingarna är digitala | Kräva elektroniskt: saknar rättsgrund och ger en invit till avslag på formfråga |
| 7 | Avgifter | **Noll kronor godtas.** Vid avgiftsbesked: fast avsmalning, därefter avstående och flaggan `avgiftsstoppad` | Budgeten är noll och går inte att förhandla om i det enskilda fallet. Regeln är deterministisk och lika mot alla, så avståendet blir en mätpunkt i stället för en tillfällighet | Godkännande upp till ett takbelopp: gav en maximal exponering om cirka 7 350 kronor som sökanden inte kan bära, och gjorde omfånget beroende av betalningsförmåga |
| 8 | Informera om mätningen | Nej; motivering publiceras (avsnitt 9) | Förannonsering mäter annonserad granskning; genmäle före publicering ger myndigheten sin röst | Informera i förväg: etiskt enklast men förstör mätobjektet |
| 9 | Protokoll | Fasta brev, fasta frister, logg som publiceras | Likabehandling är mätningens giltighetsvillkor | Bedömning fall för fall: flexibelt men gör handläggaren av projektet till en variabel |
| 10 | Nollresultat | Förskrivna texter, publiceras överst (avsnitt 9 och 10) | Skrivna innan data finns kan de inte anpassas efter utfallet | Skriva efteråt: inbjuder till efterhandsrationalisering |
| 11 | Adressering | Officiella brevlådor, egna ämnesrader per begäran | Enda garanterat likformiga ingången; intern routning är del av praxis som mäts | Direkt till sakenhet: kräver kartläggning av interna organisationer och gör ingången olik |
| 12 | Tvåbegärandedesign A/B | A (rapporter) och B (förelägganden med bilagor) till alla 21 | Bilagepunkt 30 och KR Sundsvall 2682-21 ger klasserna olika rättslig status; skillnaden i behandling blir mätvärdet | En begäran: mäter bara spridningen i en laglig skönsbedömning och saknar kontrollgrupp |
| 13 | Sekvensering A/B | Samtidig avsändning samma morgon, två separata brev, ingen korshänvisning, fast ordning A före B | Varje myndighet möter båda begärandena i identiskt utgångsläge; förskjutning hade gett B olika betingelser beroende på hur långt A-handläggningen hunnit | Fast förskjutning: kontaminerar B olika mycket per myndighet. Uttrycklig begäran om skild handläggning: pekar ut parningen och höjer signalen |
| 14 | Avgränsning B | Endast förelägganden (8 kap. 9 § djurskyddslagen eller EU-grund); djurförbud och omhändertaganden uteslutna | Verksamhetsriktade beslut bär kontrasten; djurförbud och omhändertaganden rör enskilda i utsatthet och ligger utanför projektets subjekt | "Beslut i djurskyddsärenden" brett: fler handlingar, men drar in integritetstunga beslut mot fysiska personer utan mätvärde |
| 15 | B:s period och tak | 2022-2025, tak 10; A behåller 2024-2025, tak 20 | Förelägganden är sällsynta; fönstret försäkrar kontrollgruppen även i glesa län | Symmetrisk period: elegantare design men riskerar tomma celler, och en tom kontrollgrupp är värre än en dokumenterad asymmetri |
| 16 | Djurslag | Nötkreatur, gris och fjäderfä i A, B och C | Kontrollvolymen ligger på nöt; breddningen åtgärdar risken för tomt B och avgränsningen är körbar mot ärendesystemens djurslagsfält | Bara gris/fjäderfä: symmetri med kravlagret men gles empiri. Alla djurslag: drar in häst, sällskapsdjur och anhopningsfall utan mätvärde och med integritetslast |
| 17 | Artmix | Fri mix, djurslag registreras, analys inom och justerat för djurslag | Tomma fjäderfäceller gör stratifierad mix ouppnåelig ändå; en enkel regel minimerar tolkningsspridning; B kan inte stratifieras på sina volymer | Stratifierat urval med fast antal per djurslag: identisk mix på papperet, tre sökningar per registrator och omöjligt i B |
| 18 | C:s mottagare | Jordbruksverket ensamt; länsstyrelserna endast som flaggad reservväg efter dag 40 | Syftet är nämnardata: ett registeruttag ger enhetligt format, och ett tredje brev till länsstyrelserna hade höjt granskningssignalen på A/B | C till alla 21: mäter myndighetsbeteende men ger 21 tolkningar av samma fråga och kontaminerar huvudutskicket |
| 19 | Åtalsanmälningar i C | Ingår inte | Hypotesen gäller brister; åtalsanmälan är sällsynt, styrs av annan praxis och bär brottsmisstanke mot enskilda | Ta med dem: mer data på papperet men större sekretessyta och svårare bifall för en ren räknetalsbegäran |
| 20 | C:s rättsliga form | Sammanställningsbegäran riktad mot registerfält, med delbarhetsmening | 2 kap. 6 § andra stycket TF kräver rutinbetonade åtgärder; korstabell av befintliga fält utan personuppgifter ligger på rätt sida, och delbarheten gör delvis bifall möjligt | Be om "statistik" i allmänna ordalag: inbjuder till svaret att sammanställningen inte finns |
| 21 | Sekvensering med C | C samma måndag, till Jordbruksverket, efter A och B | C kan inte slås ihop med A/B hos länsstyrelserna och signalen där påverkas inte; nämnaren samlas parallellt med täljaren | C senare som egen våg: onödig fördröjning, eftersom C går till en annan myndighet och inte kan kontaminera |

Vägval 1 var jämnt mellan kategoribegäran och anläggningslista; kravet på mallar
utan andra platshållare än myndighetsnamnet fällde avgörandet. Vägval 13 var det
svåraste i den andra ombyggnaden; argumentet som fällde det står i raden.

---

## 9. Text till metodavsnittet om förhandsinformation

Publiceras om slutsatsen står sig. Skriven för att kunna försvaras offentligt.

> Länsstyrelserna informerades inte i förväg om att svarstider och maskningspraxis
> skulle mätas. Skälet är metodologiskt. Offentlighetsprincipen ger var och en
> rätt att få en begäran prövad på samma villkor oavsett avsändare, och 2 kap.
> 18 § tryckfrihetsförordningen förbjuder myndigheten att efterforska syftet
> utöver vad sekretessprövningen kräver. Det som mäts är hur en ordinarie begäran
> faktiskt hanteras. En förannonserad mätning hade mätt hur myndigheter hanterar
> en annonserad granskning, vilket är en annan sak. Begäran innehöll därför inget
> utöver vad en ordinarie begäran innehåller, och all korrespondens efter
> avsändningen följde ett i förväg fastställt protokoll som publiceras i sin
> helhet tillsammans med begäran. På myndighetens direkta frågor svarade jag
> sanningsenligt enligt en förskriven text, även den publicerad. Varje
> länsstyrelse har före publiceringen fått del av resultaten för den egna
> myndigheten med tre veckors svarstid, och svaren publiceras oavkortade. Metoden
> att pröva öppenhet genom ordinarie begäranden är etablerad inom granskande
> journalistik; det som tillkommer här är att urval, korrespondens och mått
> förregistrerades, så att mätningen kan upprepas av vem som helst.
>
> Ingenting i mätningen var dolt. Varje begäran blev en allmän handling hos
> mottagande myndighet i samma stund den kom in, och var därmed tillgänglig för
> vem som helst att begära ut, inbegripet de granskade myndigheterna själva. Att
> en mätning pågick gick alltså att ta reda på under hela insamlingen. Det
> påpekades bara inte för myndigheterna, eftersom en förannonserad mätning mäter
> något annat.

### Förskriven text vid konsekvent maskning

> Maskningen visade sig konsekvent över länsstyrelserna. Det är mätningens
> resultat, och det publiceras överst. Därmed finns för första gången ett
> systematiskt belägg för att maskningspraxis är enhetlig för denna dokumenttyp
> och period; den variation som tidigare rapporterats anekdotiskt återfanns inte
> i data. Indexet levererar oförändrat svarstider, utlämningsgrad och en
> förregistrerad baslinje som gör om-mätning kommande år trivial. För
> Statskontorets pågående uppdrag om likvärdig djurskyddskontroll (LI2026/00608)
> är ett belagt likvärdighetsresultat direkt användbart underlag.

---

## 10. Förregistrerad hypotes: oanmälda kontroller

Förregistreras och tidsstämplas i repot innan någon begäran skickas.

**Hypotesen:** oanmälda kontroller ger oftare konstaterade brister än
föranmälda, och andelen oanmälda kontroller förklarar en del av spridningen
mellan länsstyrelser i andel kontroller med brister.

**Bakgrunden, ur Nationell djurskyddsrapport 2024 (OVR737), verifierad
2026-08-02:** 7 840 fysiska kontroller 2024, ned från 8 333 år 2023. Ordagrant:
"Under 2024 rapporterade en länsstyrelse brister vid 33 procent av
rutinkontrollerna, medan en annan rapporterade brister vid 84 procent av
rutinkontrollerna." Gapet är 51 procentenheter, upp från 43 året före, och
persistent: en länsstyrelse ligger på 32 procent i tioårsmedel, en annan på 62.
Rapportens egen slutsats, ordagrant: "Vad skillnaden i andel kontroller med
brister beror på går inte att utläsa av statistiken, men den kan bero på att
länsstyrelser haft olika fokusområden och kontrollerat olika typer av
djurhållningar." Andelen oanmälda kontroller publiceras inte för lantbrukets
djur, trots att avvägningen oanmäld eller föranmäld görs per kontroll och
registreras i djurskyddskontrollregistret.

**Prövningen:** med C-datat beräknas per länsstyrelse andelen oanmälda
kontroller och andelen kontroller med brist, inom djurslag och kontrolltyp.
Hypotesen prövas som samband mellan de två andelarna över länsstyrelser, och
som skillnad i bristandel mellan oanmälda och föranmälda kontroller inom samma
län, djurslag och kontrolltyp.

**Konkurrerande förklaringar som redovisas och inte kan uteslutas:**

1. **Artmix:** län med olika fördelning mellan nöt, gris och fjäderfä kan få
   olika bristandel av det skälet; C:s djurslagsdimension justerar delvis.
2. **Kontrolltypsmix:** rutinkontroller, kontroller efter anmälan och
   uppföljande kontroller har olika förväntad bristandel; C:s
   kontrolltypsdimension justerar delvis.
3. **Riskbaserat urval och fokusområden:** Jordbruksverkets egen gissning. En
   länsstyrelse som riktar kontrollerna mot riskobjekt får högre bristandel
   utan att djurhållningen skiljer sig. Kan inte skiljas från hypotesen med
   C-datat ensamt; redovisas som olöst konfundering.
4. **Registreringspraxis:** vad som registreras som brist kan skilja mellan
   länsstyrelser och handläggare. Observationell data kan inte utesluta det;
   maskningsmätningen i A och B belyser angränsande praxisvariation men mäter
   inte detta.

**Förskriven text vid nollresultat för hypotesen:**

> Oanmäldhypotesen fick inget stöd. Andelen oanmälda kontroller samvarierar
> inte med andelen kontroller med konstaterade brister, och skillnaden i
> bristandel mellan oanmälda och föranmälda kontroller är liten eller
> obefintlig inom län, djurslag och kontrolltyp. Det publiceras överst. Två
> saker består: fördelningen oanmält mot föranmält per länsstyrelse är nu
> offentlig och replikerbar, och gapet på 51 procentenheter i bristandel står
> kvar oförklarat även efter kontroll för anmälningsform. Frågan om vad som
> förklarar gapet skärps därmed, och den ligger på den myndighet som förfogar
> över registret.

---

## 11. Rättspraxis och rättsfrågor

### Kammarrättspraxis som A/B-designen vilar på

**Källkritiskt förbehåll:** samtliga referat nedan kommer från allmanhandling.se,
en specialistsajt som följer utlämnandemål. **KR Sundsvall 2682-21 är kontrollerad
i fulltext 2026-08-03** och **KR Jönköping 549-19, 1491-19 och 3900-18 den
9 september 2026**, se verifieringarna under respektive referat. KR Göteborg
6077-19, 4309-20 och 3503-19 är fortfarande bara referat. *Tillägg 2026-09-10:*
de tre är nu lästa i fulltext, liksom 2605-18 och 2803-18, se verifieringen
efter referatet om 3503-19. Inget kammarrättsavgörande i avsnittet vilar
längre på ett referat.

Fristående kontrollrapport, maskning har hållit:

- KR Jönköping 549-19, 1491-19, 3900-18 (2019): tre kontrollrapporter från
  djurskyddskontroller på gårdar. Beskrivningar och bilder av konstaterade
  brister skyddades som affärs- och driftförhållanden.

**Verifierade i fulltext 2026-09-09.** Kopior begärda samma dag och
expedierade av kammarrätten fyrtiosex minuter senare. Referatet håller inte,
och fyra saker skiljer sig från det.

1. **1491-19 är inget domslut.** Det är ett slutligt beslut. Referatet och
   texten ovan kallar alla tre domar.
2. **Två av tre saknar egna skäl.** 549-19:s hela motivering är
   *"Kammarrätten instämmer i länsstyrelsens bedömning. Vad [klaganden] anfört
   i kammarrätten föranleder inte något annat ställningstagande. Överklagandet
   ska således avslås."* 1491-19:s är *"Kammarrätten instämmer i
   länsstyrelsens bedömning. Överklagandet ska således avslås."* Sakskälen står
   i bilaga A, alltså i länsstyrelsens eget beslut. En ettmeningsbekräftelse
   är svagare auktoritet än ett resonerat avgörande, och den fastställer just
   den sorts beslut projektet bestrider.
3. **3900-18 gick delvis klagandens väg**, vilket referatet inte nämner.
   Kammarrätten upphävde beslutet och visade målet åter i fråga om sidorna 5
   till 7, med skälet att *"Länsstyrelsen har på fråga från kammarrätten
   uppgett att myndigheten inte längre har tillgång till den maskerade version
   som lämnats ut"*. Domstolen var därför förhindrad att pröva den delen.
   Myndigheten kunde inte visa vad den själv hade lämnat ut. Endast i 3900-18
   är skälen kammarrättens egna, och de är avgränsade: *"Visserligen finns även
   ett mindre antal uppgifter som inte omfattas av sekretess, men det rör sig
   då om enstaka ord som det inte vore meningsfullt att lämna ut."*
4. **3900-18 gällde ingen gård.** Verksamheten var en försöksdjursanläggning
   med kaniner, och personuppgiftsmaskningen vilade på 21 kap. 3 § OSL med
   hänvisning till *"den generella hotbilden mot försöksdjursverksamhet"*. Det
   sammanhanget bär en del av utfallet och finns inte i referatet.

**Ordet bilder finns inte i någon av de tre.** Klagandena talar om vilka
brister som uppmärksammats. Formuleringen om att beskrivningar och bilder
skyddades uttryckligen kommer ur referatet och inte ur avgörandena, och den
används i avsnitt 5 som andra ben i motiveringen till att fotobilagor ingår i
A och B; det benet faller. Beslutet att ta med bilagor står ändå kvar på det
första benet, KR Sundsvall 2682-21, som gällde en kontrollrapport **och en
fotobilaga** och är läst i fulltext. Vad som inte lästs: sista bilagesidan i
549-19, två bilagesidor i 1491-19, en i 3900-18 och
överklagandehänvisningarna.

**Ett nytt avgörande att begära ut.** Länsstyrelsen i Västra Götalands beslut
i 3900-18 tar stöd i *"Kammarrättens domar från 10 september 2018, mål nr
2605-18 och mål 2803-18"*. Det första är samma dom myndigheten åberopar i sitt
beslut mot detta projekt den 4 september 2026. Det andra, 2803-18, står
ingenstans i det här avsnittet.
- KR Göteborg 6077-19 (2020): tillsynsrapport om banveterinärverksamhet, brister
  i djurhållning bedömda som affärshemligheter.
- KR Göteborg 4309-20 (2021): delvis utlämnande; diarienummer och veterinärs
  kontaktuppgifter offentliga, brister hemliga.

Kontrollrapport som bilaga till beslut, inte hemlig:

- KR Sundsvall 2682-21, meddelad 2021-12-17, Länsstyrelsen i Gävleborg. En
  kontrollrapport och en fotobilaga som bilagor till ett beslut i ett
  djurskyddsärende omfattades inte av sekretess, eftersom sekretessregeln inte
  gäller uppgifter i beslut. Bilagorna delade beslutets status.

**Verifierad i fulltext 2026-08-03.** Kopia begärd 2026-08-02, expedierad av
kammarrätten påföljande arbetsdag; dokumentet ligger utanför git eftersom det
namnger klaganden med personnummer. Referatet stämmer i sak. Domskälen ordagrant:
"Eftersom båda bilagorna har fogats till beslutet omfattas de av beslutet i
ärendet. Då beslutet inte omfattas av sekretess ska beslutet och dess
tillhörande bilagor lämnas ut i sin helhet." Slutet lyder "i omaskerat skick".
Ett fel i referatet: datumet 2022-02-13 var inte avgörandedagen; domen är
meddelad 2021-12-17.

Fulltexten ger dessutom tre saker referatet inte bar:

1. **Samma dom håller båda linjerna.** Överklagandet avslogs i övrigt: maskningen
   av de fristående kontrollrapporterna, tjänsteanteckningarna och
   utredningsmaterialet stod fast som affärs- och driftförhållanden enligt
   30 kap. 23 § första stycket 1 OSL. A/B-kontrasten finns alltså inom en och
   samma dom, hos en och samma länsstyrelse, inte bara mellan olika kammarrätters
   praxis.
2. **Nedläggning saknar betydelse.** Att verksamheten upphört ändrade inte
   skadebedömningen. En länsstyrelse kan därför inte förväntas släppa äldre
   handlingar med hänvisning till att verksamheten är borta.
3. **21 kap. 3 §-maskning av personuppgifter prövades aldrig**, eftersom
   klaganden avstått uppgifterna, precis som mallarna A och B gör. Sådan maskning
   i ett B-svar är därmed ingen avvikelse enligt P9 och får inte räknas som en.

Allt innehåll är inte affärshemlighet:

- KR Göteborg 3503-19 (2019): cirkuskontroll; vilka djur som fanns på plats var
  inga företagshemligheter och hela rapporten lämnades ut.

**Verifierade i fulltext 2026-09-10: de fem avgörandena från Kammarrätten i
Göteborg.** Kopior begärda samma dag och expedierade sexton minuter senare, alla
fem betecknade dom. Inget av dem gäller en kontroll av nötkreatur, gris eller
fjäderfä: två gäller en minkfarm, ett en cirkus, ett en travbana och ett
besiktning inför slakt. Av de tre referaten håller ett, 3503-19; de två andra
missar något som bär. 2605-18 och 2803-18 var bara kända som hänvisningar.

1. **2605-18 och 2803-18 gäller en minkfarm i Hallands län.** Båda är
   överklaganden av Länsstyrelsen i Hallands läns beslut från juni 2018,
   meddelade samma dag av samma avdelning och samma tre ledamöter, och båda
   avslås. Skälen är kammarrättens egna men korta. I 2605-18: *"Kammarrätten
   anser att de delar av handlingarna som omfattar brister hos minkfarmen är
   sådana uppgifter som rör den enskildes affärs- och driftförhållanden. Enligt
   kammarrättens bedömning kan det antas att den enskilde lider skada om
   uppgifterna lämnas ut."* 2803-18 är i sak likalydande. 2605-18 är den dom
   Länsstyrelsen i Västra Götaland åberopar mot projektet i beslutet den 4
   september 2026, och båda åberopas i länsstyrelsens beslut i 3900-18. Att
   2803-18 hör till Kammarrätten i Göteborg var tidigare bara härlett.
2. **Formuleringen om beskrivningar och bilder kommer ur 2605-18.** Klaganden
   hade begärt *"beskrivningar och bilder avseende konstaterade brister"*, och
   kammarrätten skriver att klaganden *"efterfrågat uppgifter i form av
   beskrivningar och bilder på konstaterade brister. Länsstyrelsen har i de
   handlingar som lämnats ut maskerat bl.a. dessa uppgifter."* Det referatet
   knöt till KR Jönköping står alltså i en dom från Göteborg, och där omfattade
   det som hölls hemligt även bilder.
3. **6077-19 vägde in sökandens ändamål.** Handlingen var en rapport över
   banveterinärverksamheten på en travbana, Länsstyrelsen i Skåne län.
   Kammarrätten prövar om uppgiften *"typiskt sett"* kan skada, enligt
   förarbetena, och skriver sedan: *"Kammarrätten bedömer med hänsyn härtill samt
   vad som angetts om ändamålet med den aktuella begäran att enskild kan lida
   skada om uppgifterna lämnas ut."* Referatet kallar bristerna affärshemligheter;
   domen säger affärs- och driftförhållanden.
4. **4309-20 är meddelad 2020-10-01, inte 2021, och gick längre än referatet
   säger.** Handlingarna var iakttagelser vid besiktning inför slakt, översända
   från Livsmedelsverket, och Länsstyrelsen i Värmlands län hade maskat dem.
   Bristerna på sidan 2 hölls hemliga. Resten ska lämnas ut, nämligen
   *"information i handlingarna som gäller djurägare och djur, uppgifter om
   slakteriet och transport till detsamma, datum och diarienummer för aktuell
   kontroll samt namn och kontaktuppgifter för den veterinär som utfört
   kontrollen"*, med skälet *"Kammarrätten anser inte att den enskilde kan antas
   lida skada av ett utlämnande av dessa uppgifter."*
5. **3503-19 stämmer med referatet.** Överklagandet gällde Länsstyrelsen i
   Hallands läns beslut och bifölls. De maskade uppgifterna, *"bl.a. information
   om vilka djur som finns på den kontrollerade cirkusverksamheten"*, är enligt
   kammarrätten *"inte av sådan karaktär att det finns skäl att anta att den
   enskilde lider skada om de röjs."*

**Underinstansernas beslut ligger i bilaga A** och är lästa, i fyra av fem
genom OCR eftersom sidorna är inskannade. De tre besluten från Länsstyrelsen i
Hallands län, från 2018 och 2019, bär samma bedömningsmening ordagrant: *"samt
att det kan antas att sökanden/bolaget som tillsynen gäller lider ska om
uppgiften röjs."* Meningen är kontrollerad mot sidbilden i 2605-18, och
skrivfelet står i originalet. Vad som inte lästs: överklagandehänvisningarna.

**Inget avgörande från Högsta förvaltningsdomstolen finns.** Kammarrätterna har
gått åt olika håll, rättsläget är oavgjort, och det är i sig en slutsats
projektet ska kunna dra. I publicerad text beskrivs en myndighet som maskar
klass B som att den avviker från befintlig kammarrättspraxis för beslutsbilagor;
den beskrivs inte som lagbrytare, eftersom prejudikat saknas.

### Rättsfrågor som inte kunnat avgöras

1. **Avgift vid elektroniskt utlämnande.** 15-16 §§ avgiftsförordningen nämner
   kopior, utskrifter och telefax; e-post nämns inte i nu gällande lydelse. Om en
   myndighet får ta betalt för PDF per sida är därmed oreglerat i
   förordningstexten, och praxis varierar. ESV:s vägledning har inte
   kontrollerats. P5 är skriven för att fungera under båda tolkningarna.
   *Tillägg 2026-10-09:* vägledningen är nu kontrollerad, och den säger nej. På
   frågan *"Kan en myndighet ta ut avgifter med stöd av 15-23 §§
   avgiftsförordningen för utlämnande av allmänna handlingar i elektronisk
   form?"* svarar ESV: *"Nej det är inte möjligt. I 15-24 §§
   avgiftsförordningen finns stöd för uttag av avgifter för utlämnande av
   allmänna handlingar på annat sätt än i elektronisk form. [...] Regleringen
   handlar framförallt om kopior av allmänna handlingar som lämnas ut på
   papper."* Om den elektroniska formen: *"Stödet för avgiftsuttag för
   utlämnande av allmänna handlingar i elektronisk form finns i 4 § punkt 8 i
   avgiftsförordningen. Här är det ekonomiska målet upp till full
   kostnadstäckning, vilket innebär att det finns ett utrymme för att inte ta ut
   någon avgift alls."* Lydelserna är kontrollerade mot regeringens egen
   författningssamling: 4 § första stycket 8 gäller *"automatisk
   databehandlingsinformation i annan form än utskrift"* och andra stycket
   begränsar det till verksamhet *"av tillfällig natur eller av mindre
   omfattning"*, medan 16 § avslutas med att dess stycken *"gäller även när en
   handling sänds till beställaren via telefax"* och inte nämner någon annan
   överföringsform. HFD 2013 ref. 21 är läst i original och avgör något annat än
   avgiftens storlek: *"En tingsrätts beslut om avgift för utlämnande av allmän
   handling i elektronisk form har ansetts vara ett sådant administrativt beslut
   som kan överklagas hos Domstolsverket."* Avgiften i det målet togs ut med stöd
   av 4 §, och den motsvarade beloppsmässigt vad papperskopior hade kostat.
   Vägledningen är inte ett prejudikat, men den är den myndighets vägledning som
   förordningen vilar på, och frågan är därmed inte längre oundersökt. P5 står
   kvar oförändrad, eftersom den redan var skriven för att fungera under båda
   tolkningarna.
2. **Gränsen för "beslut i ärenden" i det enskilda fallet.** Kammarrättspraxis
   ger nu en delning mellan fristående rapport och beslutsbilaga, men den bygger
   på referat, inte fulltext, och HFD har inte prövat frågan. *Tillägg
   2026-09-10:* samtliga kammarrättsavgöranden i avsnittet är nu lästa i
   fulltext, och delningen står kvar; inget av de fem från Göteborg gäller
   dock en kontroll av nötkreatur, gris eller fjäderfä. Var gränsen går
   för en rapport som beslutstexten hänvisar till utan att bilägga är oklart.
3. **Vad som är rutinbetonade åtgärder i registrets fall.** 2 kap. 6 § andra
   stycket TF är verifierad ordagrant, men om just korstabellen i C kan tas fram
   rutinbetonat beror på registrets uttagsverktyg, och det kan bara myndigheten
   svara på. Bedömningen att en fältkorstabell är rutinbetonad är ett antagande;
   faller det avgörs frågan i kammarrätt via P9.
4. **Grunden för maskning av kontrollpersonals namn.** 9 b § OSF ger sekretess i
   personaladministrativ verksamhet för länsstyrelsepersonal i
   djurskyddskontroll. Om den grunden, eller någon annan, bär namnmaskning i
   utlämnade handlingar är inte verifierat; KR Göteborg 4309-20 antyder enligt
   referatet att veterinärs kontaktuppgifter är offentliga. Åberopad grund
   loggas per maskning och redovisas empiriskt. *Tillägg 2026-09-10:* 4309-20
   är läst i fulltext. Veterinärens namn och kontaktuppgifter ska lämnas ut,
   men prövningen gällde 30 kap. 23 § OSL och skadan för den enskilde, inte
   9 b § OSF. Den frågan är fortfarande oprövad.
5. **Prövningstillstånd i kammarrätten.** Enligt gängse ordning krävs inte
   prövningstillstånd när ett myndighetsbeslut överklagas direkt dit, men det
   har inte verifierats mot förvaltningsprocesslagen här. *Tillägg 2026-09-22:*
   verifierat. 34 a § förvaltningsprocesslagen (1971:291) gäller överklagande
   av ett beslut "som förvaltningsrätten har meddelat i målet", alltså inte ett
   länsstyrelsebeslut som enligt 6 kap. 8 § OSL överklagas direkt till
   kammarrätt. Prövningstillstånd krävs därför inte. Enligt 35 § krävs det
   däremot i Högsta förvaltningsdomstolen. Frågan är därmed avgjord och
   åtagandet stängt; underlaget står i `docs/VERIFIERAT.md`.
6. **JO:s skyndsamhetspraxis.** Att besked normalt ska lämnas samma dag och att
   endast några dagars dröjsmål godtas vid sekretessprövning är väletablerat,
   men specifika JO-beslut har inte verifierats. Fristerna i P2 och P3 är satta
   med marginal och vilar inte på enskilda beslut.

---

## 12. Risker, i ordning efter vad som sänker mätningen först

0. **Begärandena är själva allmänna handlingar.** Upptäckt 2026-08-02 via
   Kammarrätten i Sundsvalls autosvar: "I princip blir all post till domstolen
   allmän handling. Det innebär bland annat att allmänheten och massmedier
   normalt har rätt att ta del av innehållet i ditt meddelande." Samma sak gäller
   hos varje länsstyrelse. **Varje myndighet kan alltså begära ut korrespondensen
   med de tjugo andra och se att den ingår i en jämförelse.** Sannolikheten är
   låg; en registrator har ingen anledning att leta. Konsekvensen om det ändå
   sker är att observatörseffekten slår igenom brett i stället för hos en
   myndighet. Motmedel finns inte, och ska inte sökas: att försöka dölja
   parningen vore både omöjligt och fel. Hanteras i stället genom att
   upptäckten redovisas i metodavsnittet, och genom loggning av eventuella
   tecken på att en myndighet känner till utskicket, till exempel att den
   hänvisar till en annan länsstyrelses handläggning.

1. **Tolkningsspridning i urvalet.** Myndigheter kan räkna "de senaste" olika,
   blanda handlingsklasser, tolka djurslagsavgränsningen olika eller missa
   äldre ärenden. Då jämförs olika korpusar och både maskningsgrad och kontrast
   blir skenbara, och felet är tyst tills materialet granskas. Motmedel:
   deterministiska sorteringsregler i mallarna, loggning av exakt vad som
   levererades, klassning per dokumenttyp och djurslag före analys,
   nämnarkontrollen i P11 och korskontrollen mot C.
2. **Oanmäld-fältets kvalitet i registret.** Att avvägningen görs per kontroll
   betyder inte att fältet är konsekvent ifyllt; att andelen aldrig publiceras
   för lantbrukets djur kan bero på just det. Då kan C levereras och ändå inte
   bära hypotesprövningen. Motmedel: C:s delbarhetsmening tvingar fram besked
   om vad som finns; bortfall per dimension loggas i P6 och redovisas; en gles
   serie publiceras som gles i stället för att interpoleras.
3. **C avslås som icke rutinbetonad.** Då saknar hypotesprövningen data tills
   överklagandet är avgjort. Motmedel: C:s konstruktion mot registerfält,
   delbarhetsmeningen, obligatoriskt överklagande utanför femtaket, och
   reservvägen P11b. Ett lagakraftvunnet avslag är samtidigt ett publicerbart
   resultat om registrets faktiska tillgänglighet.
4. **Sammanslagning av A och B.** En gemensam handläggning suddar
   svarstidsgränsen och kan ge en klumpleverans. Kontrasten överlever, eftersom
   den beräknas per handlingsklass, men P0b-flaggan krävs för att bortfallet i
   svarstidsmåttet ska synas. Motmedel: separata brev, egna ämnesrader, ingen
   korshänvisning, P0b.
5. **Artmixkonfundering.** Maskningspraxis kan skilja mellan djurslag, och
   länens mix skiljer sig. Motmedel: djurslag per handling, jämförelser inom
   djurslag, justering med C:s fördelningsdata; kvarstående konfundering
   redovisas i stället för att antas bort.
6. **Maskningsteknik som inte är svart.** Vita rutor eller borttagen text syns
   inte i ett ytmått, och bilagor maskas genom undanhållande. Motmedel:
   maskningsgrad förregistreras som andel maskerad yta plus andel maskerade
   fält, och bilagorna har egna mått för undanhållande och bearbetning.
7. **Avgifter som bortfall.** Projektets budget är noll kronor och ingen avgift
   godtas. Risken är därför inte kostnad utan **bortfall**: en myndighet som
   kräver betalt bidrar inte med maskningsgrad. Motmedel: P5:s fasta avsmalning,
   flaggan `avgiftsstoppad` och öppen redovisning. Utfallsrisken bedöms som låg
   eftersom elektroniskt utlämnande i praktiken oftast sker utan avgift, men den
   kan inte uteslutas och den ska inte döljas om den inträffar.

   **Mallarna nämner inte att avgift inte kan betalas.** Ett sådant tillägg
   skulle kunna få enskilda myndigheter att efterge en avgift de annars tagit
   ut, vilket förstör avgiften som mätvärde. Betalningsförmågan hanteras därför
   först i P5, efter att beskedet lämnats.
8. **Observatörseffekt av dubbla begäranden.** Två begäranden samma morgon från
   samma person signalerar systematiskt intresse tydligare än en. Effekten är
   identisk för alla 21, så jämförbarheten mellan myndigheter står. För
   kontrasten verkar ökad noggrannhet på båda klasserna och tar delvis ut sig
   själv; leder den till att B korrekt lämnas ut omaskad underskattar mätningen
   felaktig maskning, och resultatet blir konservativt. C ligger hos en annan
   myndighet och bidrar inte till signalen hos länsstyrelserna.
9. **Blandad leveransform.** Papper hos några myndigheter gör ytmåttet känsligt
   för skanning. Motmedel: P7, fast skanningsprofil, leveransform som variabel,
   känslighetsredovisning.
10. **Små tal i små län.** Få handlingar ger breda osäkerhetsintervall per
    myndighet. Motmedel: intervall redovisas alltid; indexet rangordnar inte
    myndigheter vars intervall överlappar.
11. **Personuppgifter i mottaget material.** Handlingarna innehåller namn på
    djurhållare och personal, och B-besluten är ostrukna om praxis följs.
    Motmedel: lokal lagring, ingen publicering av uppgifter som kan hänföras
    till enskilda, aggregerad redovisning, bilder publiceras aldrig. C
    innehåller inga personuppgifter alls.

---

## 13. Ändringslogg

### Ombyggnad 1, 2026-08-02: tvåbegärandedesignen, tre varv

**Varv 1, utkast.** Tvåbegärandedesignen byggdes in: mall B skriven med
föremålet "beslut om föreläggande enligt djurskyddslagen", samma period och
liknande tak som A, samtidig avsändning, kontrastmått, rättspraxisavsnitt med
källförbehåll, P0-P12 utbyggt med per-begäran-logik.

**Varv 2, efter fientlig granskning av varv 1.** Mall B:s föremål breddades
till att uttryckligen täcka förelägganden på EU-grund, efter verifiering av
8 kap. 9 § djurskyddslagen. "Riktar sig mot anläggningar" byttes mot "gäller
hållning av", eftersom förelägganden riktas mot djurhållaren. Dubbelförekomsten,
samma rapport fristående i A och som bilaga i B, uppgraderades till kontrastens
starkaste jämförelse, och flaggan `utan_bilaga` infördes.

**Varv 3, efter fientlig granskning av varv 2.** B:s period förlängdes till
2022-2025, eftersom föreläggandevolymerna gjorde en symmetrisk tvåårsperiod till
en sannolikt tom kontrollgrupp. Sekvenseringen slutfördes: förskjutning
förkastades för att den kontaminerar B olika mycket per myndighet; samtidig
avsändning utan korshänvisning valdes, med P0b för sammanslagning. Publicerbart
språk skärptes till "avviker från befintlig kammarrättspraxis", och
riskordningen skrevs om.

### Ombyggnad 2, 2026-08-02: tre djurslag och begäran C

A och B breddades till nötkreatur, gris och fjäderfä; kravlagrets asymmetri mot
utfallslagret (1.10-i mot 1.11 i miljöprövningsförordningen) skrevs in i
avsnitt 1. Artmixfrågan avgjordes till fri mix med djurslag som registrerad
variabel; stratifiering förkastades (beslutslogg 17). Begäran C skrevs som
sammanställningsbegäran mot djurskyddskontrollregistrets fält, förankrad i
2 kap. 6 § andra stycket och 7 § TF, verifierade ordagrant; mottagare
Jordbruksverket ensamt, med flaggad reservväg till länsstyrelserna efter dag 40
(P11b). Åtalsanmälningar uteslöts ur C. Oanmäld-hypotesen förregistrerades med
prövningsplan, fyra konkurrerande förklaringar och förskriven nollresultattext
(avsnitt 10). Protokollet fick C-grenar i P0, P1, P4, P5, P6, P8, P9 och P11b,
och P11:s uppföljningsfråga utökades med nötkreatur. Riskordningen skrevs om:
tolkningsspridning överst, följd av två C-specifika risker.

### Tillämpningsnot 1, 2026-08-04: hur P4-svaren komponerats i praktiken

Skriven dag 1, efter de första 22 svaren, som dokumentation av tre tolkningar
av protokollet. Ingen ändrar omfång eller ger någon myndighet annan behandling
i sak; de skrivs ned för att likabehandlingen ska vara granskningsbar mot de
faktiskt avsända breven.

1. **Komponerad upprepning.** P4 föreskriver att svar på omfångsfrågor endast
   består av ordagrann upprepning av begärans avgränsningar. I praktiken har
   svaren komponerats av ordagranna fragment ur begäran, ibland inledda med
   "Ja" när myndighetens fråga var en ja-eller-nej-läsning av begäran. Exempel:
   "de fem senast genomförda kontrollerna, räknat efter kontrolldatum, under
   samma period, av anläggningar som håller nötkreatur, grisar eller fjäderfä".
2. **Följdriktig sifferändring.** När avsmalningen enligt P5 ändrat antalet
   från tjugo eller tio till fem har färre-än-klausulen återgetts som "har
   färre än fem beslut meddelats under perioden avser begäran samtliga".
3. **Särskiljande ord vid samlade besked.** När en myndighet lämnat ett samlat
   besked i en tråd utan ärendekoppling har svaren per begäran försetts med
   orden "om kontrollrapporter" respektive "om beslut om föreläggande", så att
   två i övrigt identiska svar till samma mottagare kan hållas isär.

Avvikelsen från P0:s klockslagsfönster (avsändning 10:00 till 10:03 i stället
för 08:00 till 09:30, lika för alla mottagare) är loggad i protokollloggen.

### Tillämpningsnot 2, 2026-08-04: förnyad begäran om avgiftsbeslut

När en myndighet inte agerar på formuleringen "beslut i frågan om avgiften"
utan i stället upprepar sitt erbjudande, lyder den förnyade begäran:

    Jag begär ett särskilt skriftligt beslut om avgiften enligt 23 §
    avgiftsförordningen (1992:191).

Samma text används mot varje myndighet i samma läge. Första tillämpning:
Jönköping, efter tre likalydande erbjudanden om nio handlingar i stället
för beslut.

### Tillämpningsnot 3, 2026-08-07: definition av stängd insamling

Skriven dag 4, innan något villkor i den kan vara uppfyllt, så att beslutet
om publicering blir mekaniskt och inte skön.

Insamlingen är stängd när varje begäran har nått ett slutstatus och inga
frister löper. Slutstatus per begäran är ett av följande:

1. **Levererad.** Handlingarna eller sammanställningen har mottagits och
   arkiverats med kontrollsumma.
2. **Avgiftsstoppad med avslutat beslutsspår.** Kopior har avståtts, beslut
   i avgiftsfrågan har begärts, och spåret är avslutat genom mottaget
   beslut, uttrycklig vägran att meddela beslut, eller utebliven reaktion
   på den förnyade begäran enligt tillämpningsnot 2 vid dag 40.
3. **Uttryckligen vägrad**, med myndighetens besked arkiverat.

Repot förblir privat till minst dag 40 (måndag 2026-09-28) oavsett om
insamlingen stängs tidigare; regeln lyder minst, och en tidigareläggning
skulle själv vara en protokollavvikelse. Publicering dag 40 eller senare
förutsätter dessutom stängd insamling enligt definitionen ovan. Löper
något spår fortfarande vid dag 40 skjuts publiceringen upp tills det är
avslutat, och uppskjutandet loggas.

### Tillämpningsnot 4, 2026-08-12: P8 tillämpas urvalsvis och avvikelsen redovisas

P8 föreskriver att myndighetens prövning och ett skriftligt överklagbart beslut
begärs inom tre arbetsdagar efter varje maskerad eller delvis leverans, per
begäran, oavsett maskningens omfattning eller angiven grund. Regeln har inte
följts. Den 12 augusti 2026, dag 7, hade ingen sådan skrivelse skickats för
någon av de 31 leveranser som då var loggade, och fristen för den första
leveransen, Stockholm B den 3 augusti, gick ut den 6 augusti.

Avvikelsen rättas inte genom ett massutskick i efterhand. Fyra skäl:

1. Maskningsgraden mäts enligt P8 på den första leveransen, före skrivelsen.
   Måttet är därmed oskadat, och steg 18 i pipelinen mäter det maskinellt ur
   handlingarna: maskningens typ, om text ligger kvar under en svärtad ruta,
   och andelen maskade dokument per begäran.
2. Skrivelsens enda funktion utöver måttet är att framkalla det beslut som P9
   förutsätter. P9 medger högst fem överklaganden för A och B tillsammans, så
   antalet beslut som behövs är långt mindre än antalet leveranser.
3. P9:s kriterium (b) är definierat av jämförelsen mellan län. Skrivelserna kan
   därför inte skickas innan maskningsanalysen är gjord utan att kriteriet blir
   omöjligt att tillämpa.
4. Länsstyrelserna har svarat snabbt, och flera har lämnat ut utan avgift trots
   att de aviserat en. Administrativt arbete som mätningen inte kräver är en
   kostnad projektet väljer att inte lägga på dem.

Härefter gäller: P8 skickas när maskningsanalysen visar att en leverans
uppfyller något av P9:s kriterier, och när myndigheten själv har erbjudit ett
överklagbart beslut. För övriga leveranser skickas ingen skrivelse. C-grenen
berörs inte; avslås C helt eller delvis begärs prövning och skriftligt beslut
som P8 föreskriver.

Följden för mätningen redovisas öppet. Om myndigheten fattar ett överklagbart
beslut när det begärs, och hur snabbt, upphör att vara en enhetlig variabel
över alla 21 länsstyrelser och blir en variabel för det urval som skrivelserna
går till. Enhetligheten offras därför att den hade kostat myndigheterna arbete
som mätningen inte behöver.

### Tillämpningsnot 5, 2026-08-13: när en begäran om avgiftsbeslut besvaras med ett generellt styrdokument

Anledningen deklareras. Örebro besvarade den 6 augusti 2026 en begäran om ett
särskilt skriftligt beslut om avgiften med en riktlinje om avgiftsuttag från
2023, och Kalmar besvarade den 12 augusti samma begäran med länsstyrelsens
generella beslut om avgifter av den 9 december 2025, som enligt sin egen
lydelse gäller alla utlämnanden från den 1 januari 2026. Situationen finns
varken i P5 eller i tillämpningsnot 2, som förutsätter att myndigheten
upprepar sitt erbjudande, inte att den skickar ett dokument den själv kallar
beslutet.

Noten skrivs innan något ytterligare svar inkommit från någon av de två, av
samma skäl som tillämpningsnot 3: avslutet ska vara mekaniskt och inte bero på
hur trött sökanden hunnit bli på en viss myndighet. Tidsföljden går att
kontrollera i den append-only historiken.

**Utlösande omständighet**, definierad av myndighetens handlande och inte av
antalet skrivelser: myndigheten har fått besked om att ett generellt
styrdokument inte är ett beslut i ärendet, eller den förnyade begäran enligt
tillämpningsnot 2, och svarar därefter på nytt med något som inte är ett
beslut i det egna ärendet. Ligger frågan hos myndighetens jurist enligt
myndighetens eget besked är omständigheten inte uppfylld, och ingenting
skickas medan den ligger där.

**Åtgärd**, en gång per myndighet, i den tråd där styrdokumentet kom:

```
Hej!

Jag har begärt ett särskilt skriftligt beslut om avgiften i mitt ärende
enligt 23 § avgiftsförordningen (1992:191). Det jag har fått är ett
generellt styrdokument, inte ett beslut i ärendet.

Med ett beslut i ärendet avser jag en handling med en beslutsmening som
avser min begäran, en motivering enligt 32 § förvaltningslagen
(2017:900) och en underrättelse om hur beslutet överklagas enligt 33 §
samma lag.

Jag ber att frågan hänskjuts till myndighetens jurist.

Med vänliga hälsningar,
Martin Blomqvist
```

**Stopp.** Därefter skickas ingenting mer i avgiftsfrågan till den
myndigheten. Att skrivelsen är den sista sägs inte i brevet. Dels kan ett
sådant tillägg läsas som ett ultimatum, dels ska myndighetens fortsatta
handlande inte formas av vetskapen att sökanden slutat skriva; det senare
skulle vara en störning av det som mäts.

**Måttet, deklarerat samtidigt som regeln.** Antal skrivelser i avgiftsfrågan
fram till ett överklagbart beslut i ärendet, samt utfall i fyra klasser:
beslut meddelat, beslut vägrat, generellt styrdokument i stället för beslut,
och uteblivet svar. Redovisas för samtliga 21 länsstyrelser oavsett utfall,
inklusive de län där noll skrivelser behövdes.

**Avgränsning.** Jönköpings uttryckliga vägran den 6 augusti hör inte hit. Den
är ett slutstatus enligt tillämpningsnot 3, uttryckligen vägrad, och besvaras
inte.

### Tillämpningsnot 6, 2026-08-23: hur uppgiftstyp läses i P9 (b), och vad som krävs för att överklaga

Skriven innan något beslut har kommit in, av samma skäl som not 3 och not 5:
tröskeln för ett rättsligt steg ska vara satt innan den kan bli bekväm eller
obekväm i det enskilda fallet. Sex P8-skrivelser är avsända den 21 till 23
augusti och kan ge upp till sex beslut. P9:s överklagandeskyldighet utlöses av
beslutet, inte av skrivelsen, och fristen är tre veckor från delfåendet.

**Problemet.** Kriterium (b) lyder att maskning i klass A med stöd av 30 kap.
23 § OSL ska träffa "en uppgiftstyp som minst tre andra länsstyrelser lämnat ut
omaskad i samma handlingsklass". Kriteriet förutsätter alltså att den maskerade
uppgiftstypen går att fastställa. Det gör den inte på fältnivå: i 124 av 294
levererade dokument är texten under svärtningen borttagen (*tillägg 2026-09-28:
88 av 295 efter rättelsen den 1 september och Kalmars leverans; ingen av dem
har text kvar under en ruta*), och ADR-0017 slog
fast att handlingarna är löpande prosa utan fältstruktur. Ett försök att härleda
typen ur texten runt varje svärtning övergavs sedan det visat sig dra enskildas
namn genom analysen.

**Läsningen som gäller.** Uppgiftstyp läses på **bestämmelsenivå**, alltså den
kategori den åberopade regeln skyddar. Åberopar en myndighet 30 kap. 23 § är den
maskerade uppgiftstypen enskilds affärs- eller driftförhållanden, vilket är vad
bestämmelsen skyddar och vad Kronoberg som enda län också skriver ut i klartext.
Jämförelsemängden är de län som lämnat ut minst ett helt omaskat dokument i
klass A, eftersom ett omaskat dokument per definition släpper varje uppgiftstyp
det innehåller. De är fem: Dalarna, Gävleborg, Jämtland, Södermanland och
Uppsala, tillsammans 17 dokument. Fem är fler än de tre kriteriet kräver.

**Vad läsningen inte gör.** Den avgör ingen sekretessfråga och den påstår inte
att två län maskat samma konkreta uppgift. Den fastställer att kriteriet är
uppfyllt i protokollets mening, ingenting mer.

**Överklagande följer inte automatiskt av den grova läsningen.** Ett beslut
överklagas enligt kriterium (b) endast om beslutet självt namnger den maskerade
uppgiftstypen så att jämförelsen kan göras på fältnivå mot de fem länens
omaskade dokument. Gör beslutet inte det saknas underlag för att driva saken,
och det redovisas som en gräns i mätningen i stället för att drivas på svag
grund. Skälet är att ett förlorat mål ger ett avgörande om att maskningen var
laglig, vilket är sämre för öppenhetslagret än tystnad, och att kammarrätten
skulle ställa just den fråga den grova läsningen inte kan besvara.

**Maskning av personuppgifter ligger utanför kriterierna.** Avsnitt 11 slår fast
att sådan maskning i ett B-svar inte är en avvikelse enligt P9 och inte får
räknas som en. Detsamma gäller i klass A: maskning med stöd av 21 kap. OSL eller
dataskyddsförordningen berör inte (b), som är skriven mot 30 kap. 23 §.

**Följden i siffror, per 2026-08-23.** Åtta län maskade klass A med stöd av
30 kap. 23 §: Gotland, Halland, Kalmar, Kronoberg, Södermanland, Värmland,
Västernorrland och Västra Götaland. Sex av dem har själva erbjudit ett
överklagbart beslut och har därför fått en P8-skrivelse enligt not 4:s
konjunktion; Värmland och Västernorrland har inte erbjudit något och får ingen.
Kriterium (c) är noll, prövat mot varje maskad B-leverans. *Tillägg 2026-09-28:
prövat en gång till, sedan en maskad B-leverans från Kalmar den 13 augusti
upptäckts oarkiverad och ologgad den 28 september. Den åberopar ingen
bestämmelse, så (c) träffar den inte, och not 4:s första led saknas därmed
också, alltså ingen P8-skrivelse. Underlaget står i `docs/VERIFIERAT.md`.*
Kommer fler än fem
kvalificerade beslut in gäller P9:s ordning: (c) först, därefter (a), därefter
(b) i fallande avvikelsestorlek, mätt som skillnaden i maskad yta mot
jämförelsemängden.

**Tillägg 2026-10-02: två av notens tal är fel, och två P8-skrivelser uteblev
av det.** Samtliga 27 rader i sekretessgrundsregistret är lästa mot sina
källmejl sedan ett citat visat sig avhugget mitt i en mening. Sex rader bar
samma fel: registret hade lagrat följebrevets första stycke och inte brevets
övriga egna stycken. Två av dem ändrar den här noten.

**Länsstyrelsen i Dalarna maskade klass A med stöd av 30 kap. 23 §.** Länets
rad slutade mitt i meningen *"I en"*, och fortsättningen lyder *"I en av
kontrollrapporterna har en angiven brist i djurtillsyn och verksamhet
maskerats, och nekas således att bli utlämnad, med hänsyn till offentlighets-
och sekretesslagen, 30 kap. 23 §."* Uppräkningen ovan om åtta län ska därmed
vara nio.

**Länsstyrelsen i Värmland erbjöd ett överklagbart beslut.** Noten skriver att
Värmland och Västernorrland inte erbjudit något. Det stämmer för
Västernorrland, vars brev slutar där citatet slutar, men inte för Värmland,
vars brev fortsätter *"Är du inte nöjd kan du vända dig till länsstyrelsen och
få ett skriftligt beslut som du kan överklaga."* Dalarna skriver på samma sätt
*"Du kan begära ett överklagbart beslut om du inte är nöjd."*

**Följden, utskriven i stället för hopräknad i tysthet.** Not 4:s konjunktion
kräver att maskningsanalysen visar ett av P9:s kriterier och att myndigheten
själv erbjudit ett överklagbart beslut. Åtta län uppfyller båda leden, inte
sex: de sex som fick en P8-skrivelse den 21 till 23 augusti, plus Dalarna och
Värmland. De två fick ingen skrivelse, och orsaken var inte en bedömning utan
att erbjudandet låg i den del av brevet som aldrig lagrades.

**Skrivelserna skickas inte i efterhand.** Samma fyra skäl som noten själv
ställde upp 2026-08-12 gäller oförändrade: maskningsgraden mäts på första
leveransen och är oskadd, P9:s femtak behöver långt färre beslut än antalet
leveranser, kriterium (b) kräver jämförelsen som redan är gjord, och arbete
som mätningen inte kräver läggs inte på myndigheterna. Till dem kommer ett
femte som inte fanns i augusti: insamlingen är stängd enligt not 3 sedan den
30 september, och en ny beslutsbegäran skulle öppna ett spår och skjuta
publiceringen framför sig utan att tillföra måttet något. Utfallet redovisas
som det är, nämligen att två län som uppfyllde villkoret inte tillfrågades på
grund av ett fel i projektets eget register, och att det upptäcktes den
2 oktober 2026 vid en genomgång av samtliga citat mot källan.

### Tillämpningsnot 7, 2026-08-31: när insamlingen är stängd trots att någon inte svarat

Skriven dag 20, innan det är känt vilka myndigheter som förblir tysta, av samma
skäl som not 3, not 5 och not 6: villkoret för att avsluta ska vara satt medan
det ännu inte gynnar eller missgynnar någon bestämd myndighet. Tre begäranden
har vid skrivandet varit utan leverans sedan den 4 augusti, men noten avgörs
inte av dem och gäller lika för varje begäran som hamnar i samma läge.

**Problemet.** Tillämpningsnot 3 säger att insamlingen är stängd när *"varje
begäran har nått ett slutstatus och inga frister löper"*, och räknar upp tre
slutstatus: levererad, avgiftsstoppad med avslutat beslutsspår, och uttryckligen
vägrad. P10 skapar en fjärde utgång: *"Dag 40 stängs datainsamlingen för
svarstidsmåttet; begäranden utan leverans och utan beslut redovisas som uteblivet
svar."* Kvalifikationen *"för svarstidsmåttet"* sitter i den meningen på
stängningen. Om den också styr redovisningskategorin står inte skrivet, och det
är just den oklarheten som gör att uteblivet svar inte går att läsa in bland not
3:s slutstatus. Not 3 säger vidare
att *"Löper något spår fortfarande vid dag 40 skjuts publiceringen upp tills det
är avslutat"*. Läst bokstavligt kan en myndighet som aldrig svarar skjuta upp
publiceringen utan bortre gräns, vilket ger den som inte svarar ett veto över
redovisningen av att den inte svarat.

**Vad protokollet självt säger om saken.** P10 avslutas: *"Eventuell JO-anmälan
övervägs först efter publicering, enhetligt för alla myndigheter som då
fortfarande inte svarat."* Den meningen förutsätter att publicering sker medan
någon ännu inte svarat. Luckan i not 3 är därför ett skrivfel, och noten sluter den i
den riktning protokollets egen text redan pekar.

**Fjärde slutstatus: uteblivet svar.** En begäran har nått slutstatus när
samtliga tre villkor är uppfyllda:

1. ingen leverans och inget beslut har kommit in,
2. den sista påminnelsen enligt P10 har skickats, tidigast dag 40, och
3. tio arbetsdagar har gått sedan den påminnelsen.

Tio arbetsdagar är ett val och inget härlett tal. P3:s tio är ett dagnummer
räknat från dag 0 och inte en väntetid efter en påminnelse, så noten lånar
siffran utan att kunna åberopa den. Valet motiveras så här: fem arbetsdagar är
kortare än den tid myndigheterna i den här insamlingen faktiskt behövt för
enklare besked, och tjugo skjuter publiceringen en månad utan att tillföra något
när tystnaden redan varat sedan augusti. Det avgörande är att talet står skrivet
i förväg, så att datumet blir räknebart och inte en bedömning. Utfallet redovisas som uteblivet svar, per begäran och myndighet, och
räknas aldrig som ett utlämnande eller som ett avslag.

**P11 utan svar.** P11 är en uppföljningsfråga och inte en av de 43
begärandena, så P2 och P3 gäller den inte och den saknar frist. Samma ordning
tillämpas: en påminnelse tio arbetsdagar efter frågan, och om svar uteblir
ytterligare tio arbetsdagar därefter redovisas nämnaren som saknad för den
myndigheten. **Nämnaren uppskattas aldrig.** Utlämningsgrad beräknas inte för
ett län vars nämnare saknas, och luckan redovisas som en lucka.

**Överklaganden skjuter inte upp publiceringen.** En begäran vars handlingar
levererats har nått slutstatus enligt not 3 punkt 1, även när maskningen i dem är
överklagad. P9 skrevs i vetskap om att överklaganden förekommer, och not 3 gör
ingenstans publiceringen beroende av ett avgörande. Ett mål i kammarrätten kan
löpa i månader, och att vänta in det hade gjort publiceringsdatumet till en
funktion av domstolens kölista. Pågående mål redovisas som pågående, med
diarienummer och yrkande, och avgörandet publiceras när det kommer. Att
publicera innan målen avgjorts skärper avsnitt 11:s regel om hur en maskande
myndighet får beskrivas: som avvikande från befintlig kammarrättspraxis för
beslutsbilagor, aldrig som lagbrytare, eftersom prejudikat saknas och frågan i
två fall dessutom ligger hos domstol.

**Vad noten inte gör.** Den flyttar inte dag 40, den förkortar inte P12:s tre
veckor, och den låter ingen begäran med löpande frist nå slutstatus. Den ger
heller ingen myndighet en sämre redovisning: uteblivet svar redovisas som just
det, och P10:s bestämmelse att en eventuell JO-anmälan övervägs först efter
publicering, enhetligt för alla, står oförändrad.

**Tillägg 2026-09-29: en leverans som kommer efter dag 40.** Läget uppstod dag
41, när Länsstyrelsen i Blekinge och Länsstyrelsen i Norrbotten besvarade P10:s
påminnelse med de kontrollrapporter de haft att lämna sedan den 4 augusti. Noten
skrivs innan något svarstidstal är räknat.

Frågan är inte vilken slutstatus begäran får, eftersom den är avgjord: notens
fjärde slutstatus kräver att ingen leverans och inget beslut kommit in, och en
begäran som levererat faller på det första villkoret. Den når slutstatus
levererad enligt not 3 punkt 1. Kvar står bara vad som händer med
svarstidsmåttet, som P10 stängde dag 40.

**Regeln.** En leverans efter dag 40 öppnar inte det stängda måttet. T2
redovisas som censurerad vid dag 40, med leveransens faktiska dag utskriven
bredvid, och begäran räknas aldrig som uteblivet svar, eftersom handlingarna
kommit in. Dokumentmåtten är en annan sak: maskningsgrad, dokumentandel och
kontrastmått har ingen dag 40 i sig, utan följer insamlingen enligt not 3, så
handlingarna ingår i dem fullt ut.

**Skälet till att måttet inte öppnas igen.** P10:s mening lyder att
datainsamlingen för svarstidsmåttet stängs dag 40, och ett mått som stängs och
öppnas när ett sent svar kommer in är inte stängt. Det skulle dessutom göra
svarstiderna till en funktion av när sista brevet råkar komma, medan hela poängen
med en fast dag är att varje myndighet mäts mot samma klocka. En censurerad
observation är den hederliga formen för det som inte hänt när mätningen slutade.

**Utfallet redovisas som det som hände.** Att påminnelsen gav två leveranser
inom en arbetsdag efter trettionio arbetsdagars tystnad hör till resultatet, inte
till en fotnot om metoden.

**Vad tillägget inte gör.** Det flyttar inte dag 40, ändrar inte not 3:s
slutstatus och rör inte P12:s tre veckor. Det säger heller ingenting om
begäranden som fortfarande är tysta; för dem gäller notens tre villkor
oförändrade.

### Tillämpningsnot 8, 2026-09-05: att öppna repot är publicering enligt P12

Skriven dag 24, innan publiceringsdatumet är valt och innan det är känt vilka
myndigheter som förblir tysta, av samma skäl som not 3, not 5, not 6 och not 7:
regeln ska sättas medan den varken gynnar eller missgynnar någon bestämd
myndighet, och medan den fortfarande är obekväm åt båda hållen.

**Problemet.** P12 lyder att *"Varje berörd myndighet får sina egna resultat
före publicering, med tre veckors svarstid."* Not 3 och ADR-0005 säger att
repot är privat till minst dag 40 och att publicering dag 40 eller senare
förutsätter stängd insamling. De två reglerna handlar om olika saker. Not 3 och
ADR-0005 skyddar mätningen mot observatörseffekt; P12 ger myndigheten rätt att
se sitt eget resultat innan någon annan gör det. Ingenstans står vad som händer
när repot växlas till publikt, och repot innehåller `docs/VERIFIERAT.md` med
varje myndighets egna tal, `data/maskning.jsonl`, `data/beslut.jsonl` och hela
protokollloggen. Läst som enbart en metodgräns kunde dag 40 därför bli det
datum då tjugotvå myndigheters resultat blir läsbara för vem som helst utan att
någon av dem fått den svarstid P12 ger dem.

**Vad protokollet självt säger om saken.** P12 knyter svarstiden till
publicering och inte till någon viss kanal. Not 7 slår fast att den *"förkortar
inte P12:s tre veckor"*, alltså att tre veckor är ett golv som andra regler inte
äter upp. Avsnitt 9 motiverar hela upplägget med att ingenting hålls undan från
myndigheterna. Luckan är därför inte ett val mellan två läsningar utan en
oskriven följd, och noten sluter den i den riktning protokollets egen text redan
pekar.

**Regeln.** Publicering enligt P12 är varje åtgärd som gör en berörd myndighets
egna resultat läsbara för någon utanför projektet. Att växla repot till publikt
är en sådan åtgärd, och det är också en publik dashboard, en webbplats, ett
dataset hos en tredje part, ett inlägg i sociala medier och att visa resultaten
för en journalist eller en tilltänkt arbetsgivare. Ingen sådan yta öppnas förrän
tre veckor gått sedan P12-utskicket nått samtliga berörda myndigheter.

**När P12 skickas.** När insamlingen är stängd enligt not 3 och not 7. Paketet
ska innehålla det som kommer att publiceras om myndigheten, inklusive dess plats
i jämförelsen mellan län, och den platsen rör sig med varje leverans som ännu
kan komma in. Att skicka tidigare vore att be om genmäle på tal som fortfarande
kan ändras.

**Följden i datum, räknad och inte bedömd.** Dag 40 är måndag 2026-09-28. Går
P10:s sista påminnelse ut den dagen når en tyst begäran slutstatus tio
arbetsdagar senare, måndag 2026-10-12, enligt not 7. Skickas P12 då löper
svarstiden ut måndag 2026-11-02, och det är tidigast repot kan öppnas. Stängs
insamlingen tidigare flyttas alla tre datumen framåt i samma takt; noten
fastställer regeln och inte datumet.

**Vad noten inte gör.** Den flyttar inte dag 40 och ändrar inte skälet i
ADR-0005. Den hindrar inte att arbetet fortsätter i det privata repot, och den
hindrar inte att resultat delas med en myndighet som redan fått sitt eget paket.
Den ger ingen myndighet veto över publiceringen: not 7 kapar tystnaden vid tio
arbetsdagar efter P10-påminnelsen, och P12:s tre veckor löper oavsett om ett
genmäle kommer. Den rör inte not 7:s regel att ett pågående mål i kammarrätten
inte skjuter upp publiceringen. Den säger heller ingenting om vad paketet ska
innehålla utöver att det är det som kommer att publiceras om myndigheten.

### Tillämpningsnot 9, 2026-09-29: nämnarens storleksläsning registreras, den föreskrivs inte

Skriven dag 41, samma dag som frågan ställdes och innan något svar på den gått
ut. Till skillnad från noterna 3, 5, 6 och 7 kunde den här inte skrivas i
förväg, eftersom ingenting pekade på att storlek skulle bli en fråga. Det som
håller den neutral är i stället att de åtta nämnarsvar som redan kommit in gavs
utan att jag sagt ett ord om storlek, och att ingen läsning föreskrivs för
någon.

**Problemet.** Länsstyrelsen i Hallands län frågar den 29 september, innan de
svarar på P11:s nämnarfråga, *"om du även vill att hobbybesättningar ingår i
statistiken"*. Frågan har inget svar i protokollet. Begäran A gäller
*"anläggningar som håller nötkreatur, grisar eller fjäderfä"* och P11 frågar om
*"anläggningar med nötkreatur, grisar respektive fjäderfä"*; ingen av dem har en
storleksgräns, och avsaknaden är ett val med skälet utskrivet i avsnitt 5, att
ett storlekskriterium smyger in en bedömning hos registratorn.

**Tre saker är mätta i materialet, och de drar isär.** Hobbybesättningar ligger
redan i täljaren: två levererade handlingar beskriver själva djurhållningen som
hållen för hobby och sällskap, en kontrollrapport i Jämtland A och ett
föreläggande i Norrbotten B. C:s nämnare räknar dem inte, eftersom
djurskyddskontrollregistrets checklistor delar fjäderfä i över 350 värphöns och
slaktkyckling, och de nationella talen för värphöns är 42 kontroller 2024 och 52
år 2025. Och länen svarar på olika läsningar utan att ha tillfrågats: Västra
Götaland anger *"värphöns fler än 350 st 18, värphöns färre än 350 st 425"*,
Gotland att *"checklistan för över 350 värphöns har använts 4 gånger"* och
ingenting under, medan Blekinges *"9 kontroller av fjäderfän"* inte säger vilken
läsning som använts.

**Regeln, i fyra led.**

1. **Svaret till en myndighet som frågar upprepar frågans egna ord och lägger
   ingen gräns till.** Det följer av P4: omfånget ändras aldrig i det steget.
   Samma text till var och en som frågar.
2. **Läsningen registreras per län och per djurslag**, i `data/namnare.jsonl`,
   med myndighetens egna ord som källa: *utan storleksgräns*, *över 350
   värphöns*, *okänd* när svaret inte säger något, eller *kan inte tas fram*.
   En läsning som inte framgår gissas inte.
3. **Bara lika jämförs med lika.** Ett läns tal för över 350 värphöns ställs mot
   C:s kategori över 350 värphöns. Läsningar summeras aldrig, och ett tal utan
   storleksgräns ställs aldrig mot ett nationellt tal som har en.
4. **Fjäderfänämnaren publiceras som läsningsberoende.** Där läsningen är okänd
   redovisas nämnaren som okänd, aldrig uppskattad, vilket är samma ordning som
   not 7 föreskriver för en nämnare som saknas.

**Vad regeln inte rör.** Utlämningsgraden. P11 definierar den per begäran, som
levererade handlingar delat med det lägre av taket och antalet som fanns, och
taket binder i praktiskt taget varje län. Storleksläsningen rör jämförelsen mot
C och Jordbruksverkets officiella statistik samt mixjusteringen, ingenting
annat.

**Det förkastade alternativet.** Att fastställa en läsning nu och skicka den till
samtliga tjugoen. Den hade gett en gemensam nämnare på papperet, men bara för de
nio län som ännu inte svarat, och de åtta som redan svarat hade fått en ny fråga
om samma sak. P11 är en identisk fråga till alla; att dela upp mottagarna i två
grupper efter vem som hunnit svara vore en större skada på jämförbarheten än den
som regeln ovan redovisar öppet.
