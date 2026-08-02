# 0011: Åtgärdsplanerna används som facit mot rapportparsningen

Datum: 2026-08-02. Status: beslutad.

## Beslut

Medlemsstaternas åtgärdsplaner återger rekommendationerna med egna ord, och
den återgivningen används som facit mot vad steg 07 läser ur rapporten. Där
texterna inte liknar varandra behandlas det som ett misstänkt fel i
parsningen, inte som en trasig länk.

Effekten av varje rättning mäts mot planerna före och efter, och siffrorna
skrivs ut.

## Skäl

Ett parsningsfel syns inte i utfallet. Steg 07 rapporterade 1 699 parsade
rapporter och såg friskt ut; 134 av dem hade i själva verket läst en enda
rekommendation där rapporten hade fem. Det upptäcktes bara för att en annan
handling, skriven av en annan part i ett annat syfte, säger samma sak och
kunde ställas emot.

Det är samma princip som redan används i lagret: rubriken mot citatet i
ADR-0010, och den handlästa facit-mängden i ADR-0007. En mätning mot en
oberoende källa är det enda som fäller tysta fel.

## Konsekvenser

Facit gav två rättningar. Den första läser tvåspaltiga tabeller kolumnvis.
Den andra kom ur samma mätning: sidbrytningens form feed gjorde varje rubrik,
post och stycke som öppnade en sida osynlig för elva radankrade mönster i steg
07 till 09.

Tillsammans: 10 067 rekommendationer i stället för 8 365, 1 981 textbekräftade
länkar i stället för 956, och grafens resolvering 96 procent i stället för 90.
Kvar står 50 rapporter som avviker helt från planernas lydelse; de är kända,
räknade och utskrivna i `docs/DGSANTE.md` i stället för utjämnade.

**Tillägg 2026-08-03:** en tredje parsväg lades till för de äldre rapporternas
hierarkiska numrering ("7.1.1" i stället för "1."), som 337 rapporter använder.
Talen ovan gäller före den ändringen; aktuella tal står i `docs/DGSANTE.md`.
Rekommendationerna är nu 11 829 ur 2 312 rapporter.

Enhetstesterna i `tests/test_recommendation_parser.py` bevakar tabellfallet
utan att korpusen behöver finnas, inklusive regeln att kolumner som inte går
ihop lämnas oparsade i stället för att paras på en gissning.
