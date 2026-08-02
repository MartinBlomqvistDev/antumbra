# 0004: Proveniensmanifest i stället för committade dokument

Datum: 2026-08-02. Status: beslutad.

## Beslut

Källdokument committas aldrig. I stället committas ett proveniensmanifest,
`data/dgsante_manifest.jsonl`, med sökväg, källänk, storlek, sha256 och
hämtdatum per fil. Invarianttesterna håller manifestet i exakt bijektion
med detaljdatat.

## Skäl

Korpusen ska vara verifierbar utan att distribueras om: vem som helst kan
hämta samma fil från kommissionen och jämföra hashen, så frågan om
materialet ändrats får ett kryptografiskt svar. Repot förblir samtidigt
litet och fritt från upphovsrätts- och personuppgiftsrisk.

## Konsekvenser

Ändrar kommissionen en fil syns det som hashavvikelse vid ombyggnad av
manifestet. Manifestet är den enda garanti CI har för korpusens
fullständighet, eftersom dokumenten inte finns i repot.
