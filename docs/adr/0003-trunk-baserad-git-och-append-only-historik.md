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
