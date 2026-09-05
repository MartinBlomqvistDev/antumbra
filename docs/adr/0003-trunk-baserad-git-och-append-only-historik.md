# 0003: Trunk-baserad git och append-only-historik

Datum: 2026-08-02. Status: beslutad.

## Beslut

Trunk-baserat arbetsflöde: main är alltid grön, kortlivade grenar för
sammanhängande ändringar, direktcommit för småsaker, taggar för milstolpar.
Historiken är append-only; force-push och historieomskrivning används inte.

## Skäl

Projektets förregistreringsargument vilar på att git-historiken är
tidsstämplad före datainsamlingen. En omskriven historik är detekterbar och
skulle underminera exakt det bevisvärde repot ska bära. CI:n, med lint,
formatkontroll och tester av repo-invarianterna, ersätter kollegagranskning
för en ensam utvecklare.

## Konsekvenser

Misstag rättas med nya commits, inte med omskrivning. Enda undantaget är
personuppgifter eller hemligheter i historiken; i så fall saneras de och
händelsen dokumenteras öppet.

## Tillägg 2026-09-05: undantaget används inte

Undantagsmeningen ovan står kvar som den skrevs, men den tillämpas inte.
Historiken skrivs aldrig om, och ingen force-push görs, oavsett vad en commit
råkar bära. Martin fastställde det den 5 september 2026, sedan ett
tjänstemannanamn hittats i ett filnamn inne i `data/villkor.jsonl` i a32fda2,
som redan var pushad.

Skälet är att undantaget äter upp regeln det står i. Bevisvärdet ligger i att
ingen kan ha rört tidsstämplarna, och ett projekt som skriver om sin historik
när innehållet blir obekvämt har inte längre den egenskapen; en granskare kan
inte skilja en sanering från vad som helst annat. Att undantaget finns skrivet
gör saken sämre snarare än bättre, eftersom det är just den mening som en
efterhandskonstruktion skulle luta sig mot.

Kvar av undantaget är dess andra halva, att händelsen dokumenteras öppet. Den
gäller fullt ut: felet, dess omfattning och den regel som hindrar att det
upprepas skrivs ut i `docs/VERIFIERAT.md` och i protokollloggen.

De fem commits som ADR-0018 nämner som omskrivna är inget undantag från detta.
De hade aldrig pushats och var alltså aldrig historik. Gränsen går vid push:
före den är en commit ett utkast, efter den är den en tidsstämpel någon annan
kan ha sett.

Vad som återstår är att felet får en följd som inte går att ta tillbaka. Blir
repot publikt blir namnet läsbart i historiken. Det är priset för regeln, och
det är ett medvetet pris.
