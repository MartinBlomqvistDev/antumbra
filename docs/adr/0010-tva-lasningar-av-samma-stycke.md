# 0010: Två läsningar av samma stycke, och oenigheten redovisas

Datum: 2026-08-02. Status: beslutad.

## Beslut

Ett stycke klassas som iakttagelse eller slutsats bara på den rubrik som
gäller där stycket står. Avsnittsnamnet får inte avgöra, och där ingen rubrik
säger något registreras stycket som omärkt.

Rapportens eget citat, alltså om en rekommendation kallar stycket slutsats
eller iakttagelse, sparas som en egen uppgift bredvid rubrikklassningen.
**Där de två är oense jämkas de inte ihop.** Båda ligger kvar i raden,
tillsammans med rubriken som avgjorde.

Den fulla styckekorpusen på 66 MB committas inte. Den slutna grafen,
`data/dgsante_graph.jsonl`, committas.

## Skäl

Avsnitt 5 heter "FINDINGS AND CONCLUSIONS" och rymmer båda sorterna. Första
versionen läste hela avsnittet som iakttagelser, och rapporternas egna citat
motsade den: av de stycken som en rekommendation kallade slutsats hade bara
15 procent klassats som slutsats. Efter att klassningen bundits till rubriker
steg andelen till 65 procent.

Att välja den ena läsningen och kasta den andra vore att dölja ett mått som
kostar ingenting att behålla: rubriken och citatet är oberoende källor om
samma stycke, och avvikelsen mellan dem är det bästa kvalitetsmått lagret har.
Ett projekt som ska tåla granskning ska visa var dess två läsningar skiljer
sig, inte välja en och tiga.

## Konsekvenser

Rubrikklassningen är en heuristik och redovisas som en sådan i
`docs/DGSANTE.md`, med hela fördelningen utskriven. Citatet är den starkare
källan när de två är oense.

Testsviten fäller om under 85 procent av de citerade stycknumren resolverar,
om en oresolverad kant bär en påhittad styckelydelse, eller om
överensstämmelsen mellan de två läsningarna faller under 55 procent.
