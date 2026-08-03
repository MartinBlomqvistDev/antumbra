# 0014: AI-assistansen deklareras i metoden

Datum: 2026-08-03. Status: beslutad.

## Beslut

Projektet är byggt med AI-assistans, och det redovisas öppet i metodavsnittet
vid publicering. Redovisningen anger vad verktyget gjorde, vad människan
gjorde, och vad som gör resultaten kontrollerbara oberoende av vem som skrev
koden. Ingen del av arbetsprocessen utelämnas ur metodbeskrivningen.

Arbetsfördelningen, som den faktiskt sett ut:

**AI-agenten (Claude, via Claude Code) har** skrivit pipelinekoden och
testerna, itererat parsningen mot de tre oberoende facit-mätningarna, byggt
dimensionsmodellen, dashboarden och dbt-projektet, verifierat
mottagaradresser mot myndigheternas egna kontaktsidor, förberett utkasten av
begärandena ur den fastställda mallen, och fört protokollloggen.

**Människan har** fattat varje avgränsningsbeslut i ADR-loggen, formulerat
och efter tre iterationer fastställt begäranmallarna och protokollet, läst
KR Sundsvall 2682-21 i fulltext och godkänt att designen håller, läst varje
begäran innan den avsändes, och själv avsänt samtliga 43. Regeln i
projektets styrdokument, att ingen begäran, inget mejl och inget publicerat
material går ut utan att människan läst det först, har gällt utan undantag
och fortsätter gälla.

## Skäl

Projektets metodologiska position är att ingenting ska behöva tas på ordet:
korpusen verifieras mot proveniensmanifestets sha256-summor, varje
dokumenterad siffra hålls av tester som fäller CI om den glider, protokollet
är förregistrerat i append-only-historik, och nollresultat publiceras överst.
Ett projekt med den positionen kan inte ha sin egen arbetsprocess som enda
odeklarerade komponent. Asymmetrin vore den enda angreppsvinkel som kan skada
förtroendet utan att röra siffrorna: inte att AI användes, utan att det inte
stod någonstans.

Redovisningen är också sakligt nödvändig för att tidslinjen ska läsas rätt.
DG SANTE-lagret byggdes på två dygn, och det syns i historiken. Det är inte
en svaghet att förklara bort utan ett mätbart faktum om arbetssättet: koden
gick fort att skriva eftersom den skrevs av en agent under mänsklig ledning,
och den går att lita på av skäl som inte har med nedlagd tid att göra. Fyra
tysta parsningsfel hittades inte genom att någon stirrade länge på koden,
utan genom oberoende mätningar: handlästa stickprov, rapportens eget citat
mot rubrikklassningen, och åtgärdsplanernas återgivning som facit. Den
kontrollen är dokumenterad i ADR-0007, 0010 och 0011 och är samma oavsett
författare.

Verifierbarhet ersätter förtroende för processen. Det är en starkare grund
än arbetstid, som inte går att verifiera alls.

## Konsekvenser

- Metodavsnittet vid publicering innehåller en AI-deklaration med samma
  uppdelning som ovan. Den skrivs innan någon frågar, inte som svar på en
  fråga.
- Beslutsansvaret är odelat mänskligt. Att ett verktyg förberett ett utkast
  flyttar inte ansvaret för vad som skickats eller publicerats.
- Loggen och git-historiken är förstahandskällan till vad som gjordes när.
  Historiken skrivs inte om (ADR-0003), så deklarationen kan kontrolleras
  mot den.
- Om arbetsfördelningen ändras i senare faser, till exempel i analysen av
  inkomna svar, uppdateras deklarationen med en daterad not i stället för
  omskrivning, i samma stil som övriga ADR:er.
