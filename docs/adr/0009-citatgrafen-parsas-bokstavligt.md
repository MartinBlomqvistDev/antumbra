# 0009: Citatgrafen parsas bokstavligt, och dess omfattning redovisas

Datum: 2026-08-02. Status: beslutad.

## Beslut

`pipeline/07_parse_recommendations.py` läser rekommendationer och deras
korsreferenser bara där rapporten skriver ut dem. Referenslistor matchas med
en grammatik för listor, inte med en teckenklass. En rapport som säger att den
saknar rekommendationer registreras som just det, skilt från de rapporter där
parsningen misslyckats.

Grafens storlek redovisas som antalet rapporter som faktiskt bär den, inte som
korpusens storlek.

## Skäl

`docs/DGSANTE.md` beskrev citatgrafen som korpusens bärande struktur, verifierad
mot en rapport. Mätningen visar något annat: korsreferenserna börjar 2014 och
finns i 489 av 2 940 rapporter. Att beskriva 4 690 revisioner som en graf hade
varit en överdrift som en granskare kan slå hål på med tre stickprov.

Teckenklassen som först användes för referenslistorna åt sig förbi punkten och
in i lagcitat, så att "2017/625" blev kanterna 201, 7 och 625. Felet syntes
bara för att antalet kanter per rekommendation kontrollerades mot mallen: tio
slutsatser per rekommendation är orimligt när dokumenten skriver en.

## Konsekvenser

Kanterna pekar i dag på stycknummer, inte på noder: iakttagelserna och
slutsatserna i avsnitt 5 och 6 är ännu inte parsade. Grafen är alltså halv, och
det står i `docs/DGSANTE.md` i stället för att antydas.

Testsviten fäller om täckningen på de graf-bärande rapporterna faller under 85
procent, om en referens hamnar utanför intervallet 1 till 300, eller om det
äkta nollresultatet slutar synas. Enhetstesterna i
`tests/test_recommendation_parser.py` kör utan korpus och bevakar varje
meningsform som en tidigare version gick bet på.
