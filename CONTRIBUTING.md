# Arbetssätt

## Kodstandard

Python 3.12. Typannoteringar överallt, Google-style docstrings. `ruff` med
konfigurationen i `pyproject.toml` ska passera utan anmärkning.

```bash
pip install -e ".[dev]"
ruff check .
ruff format --check .
pytest
```

Alla tre grindarna körs i CI; kör dem lokalt före varje commit.

**All kod skrivs på engelska**: klasser, fält, enum-medlemmar och enum-värden,
docstrings och kommentarer, filnamn och strängar. Svenska förvaltningstermer
utan ren motsvarighet behålls som lånord (`dnr`, `mpd`, `orgnr`) och förklaras
i docstring. Prosan i `docs/` och ordagranna citat ur besluten är svenska,
eftersom källmaterialet och mottagaren är det.

`src/schema.py` genereras ur kodblocket i `docs/VILLKORSSCHEMA.md`. Ändra
dokumentet och regenerera; ändra aldrig bara filen, då glider de isär.

## Commit-meddelanden

Conventional Commits, på engelska, en rad i imperativ utan avslutande punkt.

```
docs: record the two-request design and its case law
feat: parse the citation graph in DG SANTE recommendations
fix: correct the validity proxy direction for superseded conditions
test: cover the point-in-time join against inspection dates
chore: pin pydantic and add ruff configuration
data: refresh the DG SANTE index for 2027
```

Prefixen som används: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`,
`data`. Kroppstext bara när valet behöver motiveras, och då med skälet, inte
med en beskrivning av diffen.

## Vad som aldrig committas

**Personuppgifter.** Källfilernas namn innehåller fysiska personers namn, och
besluten innehåller privata mejladresser. Ingetdera går in i repot, i data
eller i dokumentation. Publicering sker aggregerat på län och juridisk person.

**Källdokumenten.** PDF:er, OCR-utdata och stora härledda binärfiler ligger i
`.gitignore`. Pipelinen hämtar dem, och `data/` innehåller bara härledd
metadata som går att granska.

## Metodregler som gäller i kod och text

- Karaktärisera aldrig, citera alltid, med sidhänvisning.
- Baseline före modell. Den triviala förklaringen körs först.
- Nollresultat publiceras överst.
- Varje härlett fält bär hur det utvanns och med vilken säkerhet.
- Begränsningar redovisas i löptext, inte i fotnot.
