# 0013: Länken mäts som containment, inte som likhet

Datum: 2026-08-03. Status: beslutad. Ersätter måttet i ADR-0011.

## Beslut

Om en åtgärdsplan svarar på en viss rekommendation avgörs av **hur mycket av
rapportens lydelse som återfinns i planens återgivning**, inte av hur lika de
två texterna är i sin helhet. Tröskeln är 0,6.

Planer skrivna på annat språk än rapporten markeras och räknas inte som
jämförbara.

## Skäl

Frågan lagret ställer är om planen återger rekommendationen. Ett symmetriskt
likhetsmått besvarar en annan fråga: om texterna är lika långa och lika
formulerade. Skillnaden är inte akademisk. Planerna är tvåspaltiga tabeller och
svarskolumnen läcker in ord mitt i den återgivna rekommendationen:

> To align the system of supervision of the facilities with the **MINISTERIO DE
> SANIDAD, SERVICIOS** requirements laid down in Article 4.6

Varje ord i rekommendationen finns där, men det symmetriska måttet gav 0,11.
136 länkar underkändes på den grunden. Handläsning av stickprov visade att
samtliga var korrekta.

Att en översättning inte kan bekräftas genom ordjämförelse är lika enkelt, och
lika viktigt att skriva ut: 108 svar är på medlemsstatens eget språk. Att räkna
dem som missade matchningar vore att skylla en översättning på parsern.

## Konsekvenser

Bekräftade länkar: **2 747 av 3 140 jämförbara, 87 procent**, mot 1 981 med det
gamla måttet. Rapporter utan en enda bekräftad rad föll från 186 till 118.

Båda måtten sparas per rad, `text_similarity` och `text_containment`, så
bytet går att granska i efterhand i stället för att behöva tros på.
Enhetstesterna behåller ett fall som visar varför bytet gjordes: samma text med
inläckta ord ger lågt symmetriskt värde och högt containment-värde.

Måttet kan i princip överskatta korta och generiska rekommendationer. Därför
prövades det mot handläst stickprov innan det byttes, och tröskeln lämnades
oförändrad på 0,6.

**Ett nollresultat, 2026-08-03.** Eftersom containment mäter hur väl en
uppdelning återger rapporten låg det nära till hands att låta måttet välja
mellan de två möjliga kolumnrännorna i steg 09. Mätt på 180 planer blev det
**sämre**: 0,678 mot 0,695 i genomsnittlig containment. Att välja per plan
överanpassar, eftersom en plan vars numrering glidit belönar den uppdelning som
råkar fånga flest tecken. Ändringen återställdes och resultatet står som
kommentar i koden, så att idén inte prövas om i tron att den är oprövad.
