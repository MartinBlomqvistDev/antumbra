# Antumbra

[![CI](https://github.com/MartinBlomqvistDev/antumbra/actions/workflows/ci.yml/badge.svg)](https://github.com/MartinBlomqvistDev/antumbra/actions/workflows/ci.yml)
[![License: AGPL v3](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](pyproject.toml)

*Att göra tillsynen mätbar.*

Antumbra är halvskuggans yttre zon: platsen man ställer sig på när något skymmer
ljuskällan, tillräckligt långt bort för att se en ring runt kanten av det som
blockerar. Det är projektets metod. Den raka blicken är skymd, så mätningen sker
runt kanten.

## Frågan

Svenska staten ställer detaljerade krav på stora djurhållande anläggningar och
publicerar kraven fritt. Utfallet av sina egna kontroller lämnar den ut maskat,
olika mycket beroende på vilken länsstyrelse och vilken handläggare som svarar.

Jordbruksverket redovisar samtidigt att andelen kontroller med konstaterade
brister skiljer sig med **51 procentenheter** mellan den länsstyrelse som ligger
lägst och den som ligger högst, och skriver i sin egen rapport att skillnaden
"inte går att utläsa av statistiken".

Ingen har mätt gapet, och ingen har prövat någon förklaring till det.

## Tre lager

**Kravlagret.** 237 miljötillståndsbeslut för stora gris- och
fjäderfäanläggningar, 2013 till 2026, publicerade av Jordbruksverket. Uppskattat
3 000 enskilda villkor, strukturerade till ett dataset. Hela populationen, inte
ett urval.

**Öppenhetslagret.** Tre likalydande begäranden om allmän handling, avsända
samma morgon. A avser fristående kontrollrapporter, där kammarrättspraxis har
godtagit maskning. B avser beslut om föreläggande med bilagor, där sekretessen
enligt bilagepunkt 30 till 9 § OSF inte gäller beslut. Kontrasten mellan A och B
är mätvärdet. C är en registerfråga till Jordbruksverket om fördelningen anmälda
mot oanmälda kontroller, vilken aldrig publicerats.

**Jämförelselagret.** 4 690 revisionsrapporter från kommissionens direktorat för
hälsa och livsmedelsrevision, 1998 till 2027, 165 länder. Samma revisor, samma
rättsliga grund, samma rapportmall för alla medlemsstater, alltså jämförbara till
sin konstruktion. Sverige har 98 rapporter, varav 8 om djurskydd.

## Metod

- **Subjektet är staten, inte djuren och inte djurhållaren.** Ingen värderande
  mening om djurhållning skrivs i projektet.
- **Karaktärisera aldrig, citera alltid.** Myndighetens egna ord, ordagrant.
- **Baseline först.** Den triviala förklaringen körs innan den intressanta.
- **Förregistrering.** Hypoteser och analysplan tidsstämplas i repot innan data
  samlas in.
- **Nollresultat publiceras överst.** Håller inte hypotesen är det resultatet.
- **Jämför villkor bara inom Sverige**, där systemet är ett. Jämför kontrollregim
  mellan länder via DG SANTE, som är byggd för att jämföras.
- **Inga personuppgifter publiceras.** Aggregerat på län och juridisk person.

## Vad mätningen inte kan visa

Redovisas här och inte i en fotnot, eftersom det avgör hur resultaten får läsas.

**Kravlagret är inte nationellt.** Fem av tolv prövningsgrupper bär 208 av de
237 besluten. Tre grupper har noll. Slutsatser om villkor gäller gris- och
fjäderfäbältet, inte riket.

**Ungefär halva kravkorpusen saknar textlager** och kräver OCR. Felfrekvensen
mäts mot de dokument som har textlager och redovisas; den antas inte.

**Giltighetsdatum är delvis proxy.** Ett tillstånd ersätts först när det nya tas
i anspråk, och det datumet finns hos tillsynsmyndigheten, inte i besluten.
Beslutsdatum används som proxy, felet går alltid åt samma håll, och varje rad
bär sin egen datumkälla.

**Rättsläget om maskning är oavgjort.** Kammarrätterna har dömt åt olika håll
och Högsta förvaltningsdomstolen har inte prövat frågan. Skillnader mellan
myndigheter är därför inte i sig bevis på felaktig rättstillämpning.

**Observationella data kan inte skilja alla förklaringar.** Riskbaserat urval,
djurslagsmix, kontrolltypsmix och registreringspraxis kan var för sig ge samma
mönster som den prövade hypotesen. De redovisas som olöst konfundering.

**Tillsynsanläggningar under tröskeln ingår inte i kravlagret.** IED-gränsen går
vid 40 000 fjäderfän, 2 000 slaktsvin eller 750 suggor, och mindre anläggningar
har inga publicerade tillstånd att jämföra med.

## Reproducera

Kräver Python 3.12. Skörden av DG SANTE använder enbart standardbiblioteket;
`pydantic` behövs för datakontrakten.

```bash
pip install -e ".[dev]"
python pipeline/01_harvest_index.py        # en sökning per år, 1998 till 2027
python pipeline/02_harvest_details.py      # en detaljsida per revision
python pipeline/03_download_reports.py     # EU-27, engelska rapporter och bilagor
python pipeline/04_build_manifest.py       # sha256 och källänk per fil
python pipeline/05_classify_annexes.py     # bilagorna klassade på egna ord
python pipeline/06_ocr_annexes.py          # OCR på det som är skannat
python pipeline/07_parse_recommendations.py  # rekommendationer och citatgrafens kanter
python pipeline/08_parse_paragraphs.py     # de citerade styckena, grafens noder
python pipeline/09_link_action_plans.py    # åtagandena kopplade till rekommendationerna
python pipeline/10_build_warehouse.py      # stjärnschemat i Parquet
```

Stegen skriver till `data/`. De som tar tid är återupptagbara och hoppar över
det som redan hämtats, så en avbruten körning startas om utan att arbetet görs
på nytt. Steg 03 laddar ned 2,2 GB till `pdf/`, som aldrig committas. Steg 06
kräver Tesseract som binär plus `pip install -e ".[ocr]"`, och steg 10 kräver
`pip install -e ".[warehouse]"`.

Kvalitetskontroll:

```bash
ruff check . && ruff format --check .
pytest
```

Testsviten bär tre garantier utöver vanliga enhetstester: den genererade
schemamodulen måste stämma med sitt designdokument, siffrorna i dokumentationen
måste hålla mot datafilerna, och inga personuppgifter får finnas i repot. Samma
kontroller körs i CI vid varje push, tillsammans med en kontroll av att
källorna uppströms fortfarande svarar.

## Struktur

```
docs/VERIFIERAT.md     kontrollerade fakta med datum och källa
docs/BEGARANMALL.md    tre begäranmallar, rättslig motivering, protokoll
docs/VILLKORSSCHEMA.md datakontrakt med motivering och verifieringskontroller
docs/DGSANTE.md        jämförelselagrets korpus, struktur och volym
docs/adr/              daterade beslut om avgränsningar och metod
CONTRIBUTING.md        kodstandard, commit-konvention, vad som aldrig committas
data/                  härledda dataset, ingen råtext och inga PDF:er
src/                   datakontrakt (Pydantic v2)
pipeline/              numrerade steg, körs i ordning
tests/                 enhetstester och repo-invarianter
```

## Status

Under uppbyggnad. Ingen datainsamling påbörjad hos svenska myndigheter, inget
publicerat resultat.

## Licens

AGPL-3.0.
