# 0008: OCR med konfidens per fil, inte som enhetlig text

Datum: 2026-08-02. Status: beslutad.

## Beslut

Skannade bilagor läses med Tesseract 5.4, i medlemsstatens språk plus
engelska, av `pipeline/06_ocr_annexes.py`. Texten hamnar under `ocr/`, som är
gitignorerad. Varje fil får sin **genomsnittliga ordkonfidens** sparad i
`data/dgsante_ocr_index.jsonl`, och den siffran följer med i allt som byggs
vidare på texten.

Språkfilerna ligger i `%LOCALAPPDATA%\antumbra\tessdata`, inte under
`Program Files`, eftersom installationen där kräver administratörsrättigheter.
Tesseract pekas dit med `--tessdata-dir`.

## Skäl

Materialet är faxade sidor från 1998 till 2006 och kvaliteten spänner från
rena maskinskrivna sidor till nästan oläsliga transmissioner. Ett stickprov
gav 93, 86 och 73 i konfidens på tre filer. **Att behandla den texten som
enhetlig vore att låtsas att den är lika tillförlitlig överallt**, och
projektets regel är att varje härlett fält bär hur det utvanns och med vilken
säkerhet. Konfidensen är det måttet.

Tesseract valdes framför ONNX-baserade motorer därför att Python 3.14 ännu
saknar hjul för dem, och framför molntjänster därför att korpusen ska gå att
återskapa offline utan konto hos någon.

## Konsekvenser

OCR-text är underlag för klassning och sökning, inte för ordagranna citat.
**Ett citat som ska publiceras hämtas ur källdokumentet, med sidhänvisning**,
aldrig ur OCR-utdata. Låg konfidens är ett skäl att öppna originalet, inte att
kasta filen.

`pymupdf` tillkommer som beroende, isolerat i extran `ocr` så att de tidigare
stegen förblir rena mot standardbiblioteket plus Pydantic.
