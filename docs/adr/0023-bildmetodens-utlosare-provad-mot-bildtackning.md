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
villkorsregistret prövats på.

*Tillägg 2026-09-29, samma dag: handläsningen är gjord, och domen är fotografi
för alla åtta.* Kriteriet skrevs i protokollloggen före första sidan och gav tre
möjliga domar, maskning, fotografi eller osäker. Instrumentet var sidan renderad
med varje balk bildmetoden hittat inramad, två sidor per handling, de med flest
balkar. Ingen av de sedda balkarna ligger i eller över en textrad; de ligger på
mörka djur, mörk gödsel, skugga under tak, mörkt nät och mörka plank. Facit står
i `data/bildlasning_facit.jsonl` med sidnummer och skäl per handling.

En andra, maskinell läsning täcker varje balk och inte bara de sedda sidorna:
**439 av 445 balkar ligger innanför en rasterbild.** De sex övriga löper över
gränsen mellan två intilliggande bilder, och alla sex är handkontrollerade var
för sig, en svart kos flank, mörkt nät, ett mörkt djurs rygg, mörka plank, ett
mörkt stall och en mörk ladugårdsöppning. Den läsningen krävde att sidans
rotation räknades in; utan den jämförde den två koordinatsystem och gav 108
falska avvikare, vilket är nedtecknat eftersom talet syntes i en körning innan
felet hittades.

*Jämfört mot de tidigare analyserna, samma dag.* Handläsningen är ett stickprov
ur en mängd som redan var mätt, och jämförelsen hör hit. `validate_image_method`
ger nu **35 falsklarm av 176 omaskade digitalt födda handlingar, 20 procent**,
mot ADR-0020:s 30 av 155 och 19 procent; missarna står kvar på 1. Korpusen har
växt från 261 till 298 digitalt födda handlingar, och andelen höll. De åtta
handlästa är alltså inte en egen sort utan **8 av 35 handlingar i samma
kategori**, de med störst bildtäckning, vilket dagens tröskel valde ut.

Containmenttestet är därför kört över alla 35: **1 217 balkar, varav 1 210
innanför en rasterbild och 7 utanför.** De sju ligger i tre handlingar och är
handlästa var för sig; alla sju löper över skarven mellan två intilliggande
bilder. Sex fanns i de åtta, och den sjunde, `vasterbotten_A/11096-2025`, låg
utanför dagens urval och är nu läst och förd till facit. Därmed är
`docs/VERIFIERAT.md`:s tidigare påstående, att varje kvarvarande falsklarm har
minst en balk inuti en rasterbild, mätt och inte bara antaget, och i en starkare
form: nästan varje balk ligger där, och varje undantag är granskat.

**Följden.** Textmetodens utfall står för alla nio handlästa, klass A:s tal står kvar på
109 av 170, och ADR:ns bedömning att oenigheten är falsklarm är nu belagd av
handläsning i stället för antagen. Kvar står golvet från ADR-0016: en balk som
är ritad i en skannad sida är osynlig för textmetoden, och ingen prövad regel
fångar den utan att samtidigt räkna fotografier som maskning. Att i stället
bortse från balkar som ligger innanför en rasterbild vore en regel som fungerar
här men blindar Halland, som ritar sina maskningar ovanpå fotografierna, vilket
är samma skäl som ADR-0020 avvisade en fotografiregel på.
