# 0007: Bilagor klassas på dokumentets egna ord, inte på position

Datum: 2026-08-02. Status: beslutad.

## Beslut

De numrerade bilagorna klassas av `pipeline/05_classify_annexes.py` på hur
dokumentet presenterar sig i sina inledande tecken, inte på var i listan det
ligger. Varje klassad rad bär den fras som avgjorde och ett citat runt den.
Det som inte går att läsa eller inte namnger sig lämnas oklassat.

Åtgärdsplaner matchas bara i dokumentets titelzon, de första 200 tecknen.

## Skäl

Ett brev som skriver att en åtgärdsplan **kommer att lämnas in** är inte en
åtgärdsplan. Med hela dokumentet som sökyta blev två sådana brev klassade som
planer, och felet upptäcktes bara för att klassningen mättes mot handläst
stickprov. Kedjan rekommendation till åtagande är projektets bärande fynd i
DG SANTE-lagret; en klassning som räknar omnämnanden som planer skulle
överdriva just den kedjan.

Detsamma gäller åt andra hållet: dokument som redovisar redan vidtagna
åtgärder hålls i egen klass, eftersom flera av dem uttryckligen skriver att
planen kommer senare.

## Konsekvenser

Träffsäkerheten mäts mot `data/dgsante_annex_labels.jsonl`, 40 bilagor lästa
för hand i stickprov dragna efter att reglerna skrivits: 85 procent, och noll
dokument felaktigt kallade plan. Testsviten fäller både om överensstämmelsen
faller under 80 procent och om något handläst dokument klassas som plan utan
att vara det.

Priset är låg täckning: 189 dokument lämnas oklassade och 1 018 kräver OCR.
Det är avsiktligt. Ett försiktigt fel går att rätta senare; ett dokument som
felaktigt räknats som åtagande är ett publicerat påstående som inte håller.
