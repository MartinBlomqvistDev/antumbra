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

Rättningen av tvåspaltiga tabeller gav 978 fler rekommendationer och lyfte
antalet textbekräftade länkar från 956 till 1 353. Kvar står 119 rapporter
där numrerade fotnoter läses som rekommendationer; de är kända, räknade och
utskrivna i `docs/DGSANTE.md` i stället för utjämnade.

Enhetstesterna i `tests/test_recommendation_parser.py` bevakar tabellfallet
utan att korpusen behöver finnas, inklusive regeln att kolumner som inte går
ihop lämnas oparsade i stället för att paras på en gissning.
