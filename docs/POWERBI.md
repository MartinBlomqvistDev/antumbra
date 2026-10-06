# Power BI: så byggs .pbix

Den här filen är en byggbeskrivning, inte en idéskiss. `docs/dashboard.html` är
redan byggd ur samma data med samma mått och samma formuleringar, så arbetet i
Power BI är att återskapa något som finns, inte att bestämma vad som ska visas.

Öppna `docs/dashboard.html` i en flik bredvid medan du bygger.

## Innan du börjar

Kör pipelinen så att modellen finns på disk:

```bash
python pipeline/10_build_warehouse.py
```

Det skriver sex Parquet-filer till `data/warehouse/`. De ligger i `.gitignore`
och är en byggartefakt; `.pbix` ska heller inte committas förrän den är
granskad, se avsnittet sist.

## 1. Hämta data

**Hämta data → Parquet**, en fil i taget från `data/warehouse/`:

| Fil | Tabellnamn i modellen |
| --- | --- |
| `dim_country.parquet` | `Land` |
| `dim_audit.parquet` | `Revision` |
| `dim_paragraph.parquet` | `Stycke` |
| `fact_recommendation.parquet` | `Rekommendation` |
| `fact_citation.parquet` | `Citat` |
| `fact_commitment.parquet` | `Åtagande` |

Byt inte datatyper i Power Query. Modellen är redan typad; varje omvandling här
är ett ställe till där lagren kan glida isär.

## 2. Relationer

Skapa dem i modellvyn. Alla är **en till många**, med enkelriktad filtrering
från dimension till fakta:

```
Land[country_key]        1 → *  Revision[country_key]
Revision[audit_key]      1 → *  Rekommendation[audit_key]
Revision[audit_key]      1 → *  Stycke[audit_key]
Rekommendation[recommendation_key] 1 → * Citat[recommendation_key]
Rekommendation[recommendation_key] 1 → * Åtagande[recommendation_key]
Stycke[paragraph_key]    1 → *  Citat[paragraph_key]
```

**Relationen Stycke till Citat måste tåla tomma nycklar.** En kant som inte
kunde knytas till ett stycke behåller sin rad med tom nyckel, och det är ett
resultat: 4 procent av kanterna hittar inte sitt stycke. Ta inte bort dem och
filtrera dem inte tyst.

## 3. Mått

Skriv dem i tabellen `Rekommendation`. Namnen är desamma som rubrikerna på
HTML-sidan.

```dax
Rekommendationer = COUNTROWS('Rekommendation')

Anger sin grund =
CALCULATE([Rekommendationer], 'Rekommendation'[states_its_basis] = TRUE())

Andel anger sin grund =
DIVIDE([Anger sin grund], [Rekommendationer])

Besvarade =
CALCULATE([Rekommendationer], 'Rekommendation'[is_answered] = TRUE())

Andel besvarade = DIVIDE([Besvarade], [Rekommendationer])

Kanter = COUNTROWS('Citat')

Kanter som resolverar =
CALCULATE([Kanter], 'Citat'[resolved] = TRUE())

Andel kanter som resolverar = DIVIDE([Kanter som resolverar], [Kanter])

Åtaganden = COUNTROWS('Åtagande')

Revisioner = DISTINCTCOUNT('Rekommendation'[audit_key])
```

`DIVIDE` och inte snedstreck: en division med noll ska ge tomt, inte ett fel,
och tomt är rätt svar för ett land utan rekommendationer det året.

## 4. Sidor

### Sida 1: Översikt

- **Kort** med `[Rekommendationer]` som stor siffra, rubrik "Rekommendationer
  utlästa ur revisionsrapporterna".
- **Fyra kort** i rad: `Revisioner i korpusen` (4 690, från `Revision`),
  `Rapporter lästa`, `[Kanter]`, `[Åtaganden]`.
- **Liggande stapeldiagram**: axel `Land[country]`, värde
  `[Rekommendationer]`, filtrerat på `Land[in_eu27] = True`, sorterat fallande.

### Sida 2: Kedjan över tid

- **Linjediagram**: axel `Revision[year]`, två värden,
  `[Andel anger sin grund]` och `[Andel besvarade]`. Filtrera på
  `Revision[year] >= 2014` och `<= 2024`.
- **Textruta** under diagrammet med noten från HTML-sidan om varför de två
  senaste åren utelämnas.

### Sida 3: Vad sidan inte visar

En sida med enbart text, ordagrant från avsnittet "Vad sidan inte visar" i
`docs/dashboard.html`. **Den sidan är inte valfri.** Begränsningarna avgör hur
siffrorna får läsas, och en dashboard som visar resultat utan dem inbjuder till
en läsning materialet inte bär.

## 5. Färger

Använd samma två som HTML-sidan, validerade för färgblindhet i båda lägen:

| Roll | Ljust | Mörkt |
| --- | --- | --- |
| Serie 1 | `#2A78D6` | `#3987E5` |
| Serie 2 | `#EB6834` | `#D95926` |

En serie får en färg. Färga aldrig staplar efter sin egen längd: det dubblar
det stapeln redan visar och bränner den enda fria kanalen.

## 6. Innan .pbix committas

- Filen sparas som `docs/antumbra.pbix`. `.gitignore` ignorerar `*.pbix` och
  gör ett undantag för exakt den sökvägen, så en fil som ligger någon
  annanstans försvinner tyst ur `git add`.
- Ta bort alla dataanslutningar som pekar på absoluta sökvägar utanför repot.
- Kontrollera att ingen personuppgift följt med. Lagret innehåller inga, men
  kontrollen görs ändå.
- `.pbix` är en binärfil och kan inte granskas i en diff. Committa den bara när
  innehållet är stabilt, och lägg skärmbilder bredvid i `docs/` så att en
  läsare ser resultatet utan att öppna Power BI.

## Vad Power BI tillför utöver HTML-sidan

HTML-sidan är fristående och publik. Power BI-versionen finns för att korsfilter
och drillthrough är svåra att bygga för hand: klicka ett land och se dess
revisioner, klicka en revision och se dess rekommendationer med det stycke var
och en vilar på. Det är den interaktionen som gör lagret till ett verktyg i
stället för en bild.
