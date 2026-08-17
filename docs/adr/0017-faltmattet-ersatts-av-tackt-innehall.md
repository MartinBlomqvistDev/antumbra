# 0017: Fältmåttet ersätts av täckt innehåll, och avvikelsen deklareras

Datum: 2026-08-17. Status: beslutad.

## Beslut

Förregistreringen definierar maskningsgrad som **andel maskerad yta plus andel
maskerade fält** (`docs/BEGARANMALL.md`, risk 6). Andelen maskerad yta mäts i
steg 18. Andelen maskerade fält går inte att beräkna på det material som
faktiskt levererats, och ersätts därför av ett mått på **täckt innehåll**: ett
tecken räknas som dolt när det finns i textlagret men inte syns i den renderade
sidan, och ett dokument räknas som maskat av ljus täckning när minst tio
sammanhängande dolda tecken ligger i brödtexten. Steg 26,
`data/dold_text.jsonl`.

Avvikelsen från förregistreringen deklareras här i stället för att lösas genom
att tolka ordet fält tillräckligt löst.

## Skäl

**Handlingarna är inte formulär.** Fältmåttet förutsätter en handling med
namngivna fack som var för sig kan vara ifyllda eller maskade. Kontrollrapporter
och förelägganden är löpande prosa. Mätt över 40 digitalt födda dokument har
mediandokumentet **sex** rader på formen `Etikett: värde`, och de är
`Diarienummer`, `Datum`, `Sida` och liknande sidhuvudsuppgifter, inte
rapportens innehåll. Ett fältmått räknat på dem hade mätt sidhuvudet.

**Syftet med det förregistrerade fältmåttet är däremot precist och går att
uppfylla.** Risk 6 säger varför det finns: maskning som inte är svart syns inte
i ett ytmått. Måttet som ersätter det svarar på exakt den frågan, och gör det
utan att anta något om vad som täcker: jämförelsen sker mellan textlagret och
den renderade sidan, så en vit rektangel, en ljus bild och en täckande annotering
fångas av samma test. Ingen resonemangskedja om ritordning behövs.

**Mätningen har en inbyggd negativ kontroll.** Mallen till kontrollrapporterna
ritar en vit bottenplatta bakom brödtexten, och 39 av de första 60 dokumenten
lägger mörka tecken innanför den. Samtliga renderas synligt, alltså läses plattan
rätt som liggande bakom texten. Ett färgbaserat mått hade flaggat alla 39; det
gjordes först, och 27 av de 39 gav exakt samma tal, 2 701 tecken, i skilda län.
Den identiska siffran var det som avslöjade mallelementet.

## Följder

**Utfallet är ett nollresultat och publiceras som ett.** Av 249 levererade
dokument med textlager har 41 minst ett dolt tecken, sammanlagt 232 tecken av
2,9 miljoner. Samtliga ligger i övre marginalen och bär teckenklasser som svarar
mot diarienummer, datum och sidnumrering; myndighetens egen sidhuvudruta täcker
dem. **Noll dokument döljer brödtext bakom en ljus täckning.** Alla 41 tillhör
klass B, inget dokument i klass A är berört, och det följer av att
föreläggandenas mall ritar sidhuvudrutan och kontrollrapporternas inte gör det.
Talet mäter mallar och inte myndighetsbeteende.

Tröskeln på tio tecken kan inte ha skapat utfallet. Den längsta dolda strängen i
brödtext över hela materialet är noll tecken, så varje tröskel från ett och
uppåt ger samma nollresultat.

Tillsammans med steg 18:s resultat att noll dokument har läsbar text kvar under
en svärtad ruta blir bilden entydig: maskningen i den här korpusen är tekniskt
äkta, och ingen myndighet har dolt innehåll med en teknik som ytmåttet missar.

**Golvet ska alltid följa med siffran.** Text som helt enkelt raderats före
utlämnandet lämnar ingenting kvar att jämföra mot och är omöjlig att upptäcka ur
handlingen ensam. Risk 6 nämner också undanhållna bilagor, som har egna mått för
undanhållande och bearbetning och inte berörs här. Måttet visar alltså att
ingenting *täcks* utan att synas, aldrig att ingenting *saknas*.

Skannade handlingar ingår inte: utan textlager finns ingen text att jämföra
renderingen mot, vilket är samma gräns som ADR-0016 redan drar för bildmetoden.
