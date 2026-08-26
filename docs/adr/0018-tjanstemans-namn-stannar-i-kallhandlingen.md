# 0018: Tjänstemäns namn stannar i källhandlingen, repot bär rollen

Datum: 2026-08-25. Status: beslutad.

## Beslut

Ett beslut från en myndighet namnger beslutsfattare och föredragande. Namnen
stannar i källhandlingen, som ligger utanför git med sin kontrollsumma. I repot
skrivs rollen: `enhetschef`, `djurskyddshandläggare`. Utelämnandet skrivs ut
där det sker, så att det är deklarerat och inte tyst.

Regeln gäller alla ytor: `data/beslut.jsonl`, protokollloggen, `docs/`, koden
och webben. Den gäller oavsett att handlingen är offentlig.

## Sammanhang

Det första överklagbara beslutet kom in från Länsstyrelsen i Kalmar den 25
augusti 2026. Det namnger, som beslut gör, en enhetschef som beslutsfattare och
en djurskyddshandläggare som föredragande. Namnen fördes först in i
beslutsregistret, i protokollloggen och i `docs/VERIFIERAT.md`. De var då de
enda två personnamnen i hela loggen, och loggen publiceras i sin helhet.

Fem ytterligare beslut kan komma, eftersom sex P8-skrivelser är avsända. Regeln
måste därför sättas nu och inte när namnen är ett mönster i historiken.

## Skäl

**Projektets subjekt är myndigheten.** README slår fast att projektet inte
innehåller någon värderande mening om djurhållning, och att ingen publicering
sker på annat än aggregerad nivå. En handläggares namn är inte myndigheten.

**Rollen bär det som mäts.** Att beslutet fattades på enhetschefsnivå är en
uppgift om myndighetens handläggning och kan behövas i en jämförelse mellan
län. Vem enhetschefen är kan inte behövas i någon mätning projektet gör.

**Spårbarheten går inte förlorad.** Ett beslut citeras med diarienummer och
datum, och källhandlingen finns kvar med sin sha256 i leveransmanifestet. Den
som vill se namnen begär ut beslutet, precis som projektet gjorde.

**Asymmetrin i konsekvens.** Ett namn i ett publicerat material om
maskningspraxis gör en enskild sökbar i ett sammanhang hon inte valt. Det
saknade namnet kostar läsaren ingenting.

## Motargumentet, och varför det inte fäller

Beslutet är en offentlig handling, och att namnge beslutsfattare i tjänsten är
normal juridisk citering. Det är riktigt, och det är därför regeln formuleras
som ett val och inte som ett förbud som skulle följa av dataskyddsregler. Valet
är projektets eget: citeringen som bär mätningen är diarienummer och datum, och
namnet tillför inget utöver dem.

## Följder

`CONTRIBUTING.md` bär regeln under "Vad som aldrig committas". Två invarianter
i `tests/test_repository_invariants.py` håller den: `beslutsfattare` och
`foredragande` i `data/beslut.jsonl` måste vara rolltitlar ur en förtecknad
lista, och e-postadresser skannas nu även i de svenska protokollfilerna,
eftersom den tidigare skanningen hoppade över `.jsonl` och det är just där
myndighetskorrespondens landar. DG SANTE-datasetet ligger medvetet utanför den
skanningen: det citerar publicerade kommissionsrapporter som namnger
myndigheters kontaktadresser, och att redigera en publicerad källa vore en
annan sorts ohederlighet.

De fem commits som redan bar namnen skrevs om innan de pushades, med trädet och
samtliga commit-ämnen verifierat oförändrade.
