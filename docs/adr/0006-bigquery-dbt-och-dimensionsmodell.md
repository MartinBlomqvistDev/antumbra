# 0006: BigQuery, dbt och dimensionsmodell

Datum: 2026-08-02. Status: beslutad.

## Beslut

Analyslagret byggs som ett dimensionsmodellerat datalager i BigQuery med
dbt för transformationer och tester. Dashboard i Power BI Desktop med
publicerade skärmbilder, plus Looker Studio som publik vy.

## Skäl

Korpusen är en graf av revisioner, rekommendationer och åtaganden över tid
och land, och frågorna är aggregerande med point-in-time-join mot beslut
som ersätts. Ett dimensionslager med explicita nycklar gör varje publicerad
siffra till en testad query i stället för ett skript, och dbt-testerna
speglar repo-invarianterna på datalagret. BigQuerys fria nivå räcker för
volymen.

## Konsekvenser

Parquet är källformatet och alltid återskapbart lokalt; molnlagret är en
vy, inte sanningskällan. Ingen betald nivå får bli ett beroende, och
Power BI Pro köps inte.
