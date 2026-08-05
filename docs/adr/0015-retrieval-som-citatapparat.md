# 0015: Retrieval över styckekorpusen, som citatapparat och aldrig som författare

Datum: 2026-08-05. Status: beslutad.

## Beslut

Ett retrievallager byggs över de 81 292 styckena ur rapportkorpusen:
embeddingar beräknas lokalt i pipelinesteg 14, och en frågemodul hämtar de
stycken som liknar en fråga semantiskt. Ett genereringssteg får finnas ovanpå,
men det får bara **välja och återge**: det returnerar stycken ordagrant med
land, rapportreferens och styckenummer, eller beskedet att ingenting i
korpusen svarar. Det får aldrig parafrasera, sammanfatta eller komplettera ur
modellens eget minne. Garantin ligger i tre lager: svarsmontören vägrar
returnera text som inte är teckenidentisk med källstycket, ett enhetstest
fäller varje väljare som ändrar text, och ett lokalt test verifierar utdata
mot den riktiga korpusen ordagrant.

## Skäl

**Varför retrieval hör hemma i projektet.** Jämförelsen är projektets kärna:
vad kommissionen sagt om samma typ av brist i olika länder och olika år.
Styckena är redan rapporternas egna numrerade citeringsenheter, samma enheter
som citatgrafen bygger på, så semantisk sökning över dem är en förlängning av
lagret som redan finns, inte ett nytt påhitt. Att korpusen dessutom är den
enda dokumentmängd i Martins projekt som är värd att hämta ur är ett ärligt
biskäl: retrieval är ett återkommande krav i de tjänster han söker, och det
redovisas här i stället för att låtsas bort.

**Varför generatorn inte får skriva om något.** Projektets regel är att aldrig
karaktärisera och alltid citera ordagrant med källhänvisning, därför att varje
omskrivning av en revisionstext är en tolkning som läsaren inte kan skilja
från källan. En språkmodell som sammanfattar stycken bryter regeln i exakt
den punkt där den är som viktigast: i mötet med läsare som själva inte öppnar
rapporterna. Ett urval av ordagranna citat kan däremot kontrolleras av vem som
helst mot källan, och ett tomt svar är ett ärligt svar.

**Modell och lagring.** Embeddingar med sentence-transformers
`all-MiniLM-L6-v2`: engelsk korpus, lokal körning utan API-nyckel, 384
dimensioner, den mest väldokumenterade referensmodellen i sin klass. 81 292
vektorer om 384 float32 är cirka 125 MB; en normaliserad matris i minnet och
en skalärprodukt med numpy besvarar en fråga på millisekunder. En
vektordatabas (FAISS, Qdrant, pgvector med flera) avfärdas uttryckligen: de
löser problem som uppstår vid miljontals vektorer, hög frekvens av
uppdateringar eller flera samtidiga klienter, och inget av detta föreligger.
Att införa en sådan här vore infrastruktur utan fråga, och den skulle dölja
att hela behovet ryms i en npy-fil.

**Härledda filer committas inte.** Embeddingshärden är stor och reproducerbar
ur korpusen; den gitignoreras som styckefilen själv. Det committade är
manifestet med modellnamn, dimension, radantal och sha256 per shard, så att en
körning kan verifieras utan att vektorerna distribueras, samma mönster som
proveniensmanifestet i ADR-0004.

## Not 2026-08-05: granskningen fann två sätt att ljuga

Efter första implementationen prövades garantin med angreppsförsök i stället
för med välvilja, och två hål fanns:

1. **Rätt citat under falsk källa gick igenom.** Kontrollen jämförde bara
   texten, så en väljare kunde returnera Ungerns ord tillskrivna Danmark.
   Det är en värre feltyp än en parafras: läsaren kan kontrollera citatet
   mot korpusen och få rätt, men mot fel land. Dessutom delar 801 stycken
   text med ett annat stycke, så textjämförelsen kunde inte ens placera ett
   citat entydigt. Kontrollen validerar nu hela stycket, inte dess text.
2. **Föråldrade embeddingar accepterades tyst.** Byggdes styckekorpusen om i
   steg 08 utan att steg 14 kördes om, kopplades verkliga citat till fel
   rapporter utan att något såg fel ut i utdatan. Radantalen jämförs nu
   före varje fråga, och avvikelse stoppar svaret.

Båda är samma feltyp som projektet i övrigt jagar: fel som inte syns i
resultatet. Bägge fälls nu av egna tester.

## Konsekvenser

- Steg 14 är återupptagbart: embeddingar skrivs i shards och färdiga shards
  hoppas över vid omkörning.
- Frågemodulen tar sin embedder och sin väljare som utbytbara beroenden, så
  tester kör med syntetisk korpus och deterministisk embedder utan
  modellnedladdning, och en LLM-baserad väljare kan läggas till senare utan
  att retrieval ändras.
- CI kör enhetstesterna; testet mot den riktiga korpusen hoppar över sig
  självt där korpusen saknas.
- Svarslagret är engelskspråkigt som korpusen; översättning av citat är
  omskrivning och görs inte av maskinen.
