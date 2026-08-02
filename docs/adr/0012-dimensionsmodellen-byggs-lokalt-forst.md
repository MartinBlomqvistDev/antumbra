# 0012: Dimensionsmodellen byggs lokalt först, molnet är en vy

Datum: 2026-08-02. Status: beslutad.

## Beslut

`pipeline/10_build_warehouse.py` bygger stjärnschemat lokalt till Parquet med
enbart `pyarrow`. Ingen molntjänst, ingen dbt och inga uppgifter krävs för att
köra det. Parquet-filerna är en byggartefakt och committas inte; manifestet
som beskriver varje tabell, kolumn och radantal committas i deras ställe.

Konformerade dimensioner: `dim_country` och `dim_audit` delas av alla tre
faktatabeller.

## Skäl

ADR-0006 slog fast att Parquet är källformatet och molnlagret en vy. Att bygga
BigQuery först hade vänt på det och gjort modellen omöjlig att köra, testa
eller granska utan konto. Med modellen lokal kan CI kontrollera dess form vid
varje push, och en läsare kan återskapa den från de committade dataseten.

Radantalen härleds ur de committade JSONL-filerna, så testsviten kan fälla en
modell som glidit isär från sitt underlag utan att binärerna finns.

## Konsekvenser

Rader som inte gick att knyta ihop behålls med tom nyckel: 335 kanter som inte
resolverade och 1 453 svar i åtgärdsplaner vars nummer saknas i den parsade
rapporten. Ett test kräver uttryckligen att citatfakta rymmer fler rader än den
löste, så att en framtida ändring inte kan snygga till modellen genom att kasta
det som inte gick ihop.

dbt och BigQuery ligger kvar som nästa steg, och de blir en publicering av den
här modellen snarare än en ombyggnad av den.
