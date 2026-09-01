# 0020: Mallens fasta element utesluts ur bildmetoden

Datum: 2026-09-01. Status: beslutad.

## Beslut

Bildmetoden i steg 18 utesluter två element som tillhör myndighetens blankett
snarare än något den lämnat ut. Det första är länsvapnet i brevhuvudet: en ruta på
sidan ett vars högerkant ligger inom 130 punkter från sidans vänsterkant och
vars underkant ligger inom 80 punkter från dess överkant. Det andra är samma
svarta rubrikband som ADR-0019 utesluter ur textlagret, funnet som en rad av
block som tillsammans når från 81 till 513 punkter med högst 36 punkters höjd.

Måtten anges i punkter på sidan och räknas om till den renderade rutan när de
används, så att de går att kontrollera mot en linjal i en pdf-läsare.

## Sammanhang

Rättelsen av textmetoden tidigare samma dag gav ett rättat facit, och mot det
gav bildmetoden balk i 64 av de 155 digitalt födda handlingar som textmetoden
bedömer som omaskade, alltså 41 procent falsklarm. Tillägget till ADR-0016
lämnade den frågan öppen samma förmiddag, eftersom ingen regel fanns som var
prövad.

**Villkoret skrevs innan utfallet var känt** och står i protokollloggen
2026-09-01 kl. 17:30. En regel fick antas bara om den uppfyllde båda kraven:
inte en enda ytterligare verkligt maskad handling får bli blind, alltså missarna
får inte stiga över den enda som redan fanns, och minst hälften av de 64
falsklarmen ska försvinna. En regel som klarade det första men inte det andra
skulle redovisas som otillräcklig och inte införas.

## Utfallet

Prövat med `python src/validate_image_method.py` över materialets 261 digitalt
födda handlingar, med textlagret som facit:

| Facit ur textlagret | Antal | Balk före | Balk efter |
| --- | --- | --- | --- |
| maskade (`text_removed`) | 88 | 87 | 87 |
| omaskade (`none`) | 155 | 64 | 30 |
| endast markör (`marker_only`) | 18 | 12 | 11 |

Missarna står kvar på 1 av 88, och falsklarmen faller från 64 till 30 av 155,
alltså från 41 till 19 procent. Båda villkoren är uppfyllda, det andra med
liten marginal: 34 av 64 är 53 procent.

**Vad de 30 kvarvarande är.** Fotografier. Varje kvarvarande handling har minst
en balk inuti en rasterbild, och de tre som lästes okulärt visar mörka foton av
en röd träbyggnad i vinterljus, ett mörkt fordonsutrymme och ett markparti.
Det är den felkälla ADR-0016 skrev ut från början, och den går inte att lösa med
en position, eftersom ett foto kan ligga var som helst på sidan.

## Skäl

**Elementen tillhör blanketten.** Vapnet och rubrikbandet finns i varje läns
mall, på samma plats, och ingendera kan dölja en uppgift. Att räkna dem som
maskning mäter formulärets utformning.

**Villkoret skrevs först.** Det är samma ordning som gäller den förregistrerade
hypotesen och bilageklassningen: måttstocken sätts före mätningen, så att den
inte kan formas efter resultatet.

**En regel för fotografier avvisas, trots att den skulle ta resten.** En balk
som ligger inuti en rasterbild går att utesluta mekaniskt. Halland har lämnat en
fotobilaga, `4728-2026-fotografier_Bortredigerad.pdf`, där en svart rektangel är
ritad tvärs över mitten av ett foto på en hage; den är kontrollerad okulärt. En
sådan regel skulle göra just den maskningen blind. Den kan inte heller prövas
mot det här facit, eftersom facit bara innehåller digitalt födda handlingar och
fotobilagan är skannad. Hålet deklareras hellre än täcks med en oprövad
regel.

## Följder

**Ingen publicerad siffra ändras av den här regeln, och det ska stå tydligt.**
Sju handlingar i `data/maskning.jsonl` får ett annat balkantal, och Södermanlands
maskade yta i klass A går från 0,0363 till 0,0358. Ingen skannad handling byter
dom: samtliga 30 i klass A bedöms fortfarande som maskade, och 11 av 15 i klass
B. Skälet är att varje skannad handling som bär vapnet eller rubrikbandet också
bär andra balkar, oftast fotografier. Regeln förbättrar alltså instrumentet
utan att flytta utfallet, och rangordningen efter maskad yta bland de sex
P8-länen är oförändrad.

Uppdelningen på metod i `docs/VERIFIERAT.md` står därför kvar. En
falsklarmsfrekvens på 19 procent är fortfarande för hög för att de två halvorna
ska kunna slås ihop utan förbehåll, och för de skannade handlingarna finns
ingen handläsning alls.

Jämförelsen går att köra om med ett kommando. Att den förra kördes för hand och
inte lämnade något spår är hela skälet till att den inte gick att granska när
den behövde granskas.
