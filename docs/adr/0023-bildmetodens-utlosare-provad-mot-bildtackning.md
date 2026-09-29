# 0023: Bildmetodens utlösare prövad mot bildtäckning, och regeln införs inte

Datum: 2026-09-29. Status: beslutad.

## Beslut

Bildmetoden i steg 18 utlöses även i fortsättningen av att textlagret saknas,
som ADR-0016 bestämde. Regeln som prövades i dag, att en handling vars
bildtäckning på någon sida når minst 50 procent får både textläsningen och
bildläsningen, **införs inte.** Den föll på ett av de tre villkor som skrevs
innan den kördes.

Mätningen av bildtäckning införs inte heller som fält i `data/maskning.jsonl`.
Provet kördes, utvärderades och rullades tillbaka, och filen är teckenidentisk
med läget före provet.

## Sammanhang

Den 29 september 2026 lämnade Länsstyrelsen i Blekinge och Länsstyrelsen i
Norrbotten ut femton handlingar, och sex av dem visade sig vara sidbilder med
ett OCR-textlager under bilden. ADR-0016 skickar en handling till bildmetoden
när den *"saknar textlager helt"*, vilket den sortens handling inte gör. Följden
är att textmetoden läser OCR-lagret och aldrig ser en balk som är ritad i
bilden.

**Villkoret skrevs före körningen** och står i protokollloggen 2026-09-29. Tre
krav, alla tvingande:

1. Ingen handling vars största bildtäckning ligger under tröskeln får byta metod
   eller dom, vilket skyddar de 248 handlingar bildmetoden validerades mot och
   varje publicerat tal.
2. För de handlingar regeln träffar ska båda läsningarna stå i raden, och
   oenighet ska vara läsbar på fältnivå i stället för upplöst.
3. Faller någon handling i materialet mellan 1,4 och 69 procents bildtäckning
   antas tröskeln inte, eftersom avståndet då inte är tomt och talet 50 blir en
   anpassad parameter i stället för en gräns mellan två skilda sorter.

## Utfallet

| Villkor | Utfall |
| --- | --- |
| 1, ingenting under tröskeln rör sig | håller, ingen handling under tröskeln bytte metod eller dom |
| 2, båda läsningarna i raden | håller, 82 handlingar fick två läsningar |
| 3, tomt avstånd mellan sorterna | **faller, 210 av 343 handlingar ligger i avståndet** |

**Premissen bakom tröskeln var mätt på för litet underlag.** Talen 0 till 1,4
procent mot 69 till 100 kom från sidan ett i de femton handlingar som kom in
samma dag. Över hela materialet är bildtäckning ett kontinuum: Hallands två
B-handlingar ligger på 0,59, fem av Södermanlands på 0,547, tre av Jämtlands
A-rapporter mellan 0,52 och 0,56, och 210 handlingar hamnar mellan de två
gränserna. Det finns alltså ingen skarv att lägga en tröskel i, och varje tal
mellan 1,4 och 69 procent hade varit lika motiverat som 50.

**Provet gav ändå en upplysning som ska stå.** Av de 82 handlingar som låg över
tröskeln var de två läsningarna oense om 13. Fem är kammarrättsavgöranden och
ligger utanför måttets population; de bär markören men ingen balk. Åtta ligger i
klass A: tre kontrollrapporter från Jämtland och fem handlingar från Norrbotten,
alla bedömda som omaskade av textmetoden och som maskade av bildmetoden, med 16
till 94 balkar var. Samtliga åtta är fotografitunga, och ett fotografi som är
mörkt nog att räknas som balk är den felkälla ADR-0016 skrev ut från början och
som ADR-0020 avvisade en regel för, eftersom Halland har lämnat en fotobilaga
där maskningarna är ritade ovanpå bilderna. Oenigheten är därför inget belägg
för dold maskning, och den publiceras inte som ett sådant.

## Följder

**Klass A:s tal står kvar som textläsningen ger dem**, 109 av 170 handlingar med
minst en maskning, och gränsen redovisas i löptext i `docs/VERIFIERAT.md`: för de
sex handlingar som är sidbilder med OCR-lager kan textmetoden inte se en balk i
bilden, och ingen prövad regel finns som fångar dem utan att samtidigt räkna
fotografier som maskning.

**Golvet från ADR-0016 gäller nu också dem:** att `masked` är falskt betyder att
ingen balk hittades, inte att ingenting undanhållits.

**Vad som skulle avgöra frågan.** Handläsning av de åtta handlingarna i klass A
där läsningarna är oense, alltså samma väg som djurslagsregeln och
villkorsregistret prövats på. Det är åtta dokument och kostar en eftermiddag.
Till dess är frågan öppen och redovisad som öppen, vilket är billigare än en
regel som flyttar ett publicerat tal på en tröskel som materialet inte stöder.
