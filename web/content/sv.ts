import type { Copy } from "./types";

export const wordingItems = [
  {
    label: "Begäran A: kontrollrapporter",
    text:
      "Jag begär kopior av kontrollrapporter från " +
      "djurskyddskontroller av anläggningar som håller nötkreatur, " +
      "grisar eller fjäderfä.\n\nBegäran avser de 20 senast " +
      "genomförda kontrollerna, räknat efter kontrolldatum, under " +
      "perioden 1 januari 2024 till och med 31 december 2025. Har " +
      "färre än 20 sådana kontroller genomförts under perioden " +
      "avser begäran samtliga. Med kontrollrapport avser jag den " +
      "rapport som upprättas efter genomförd kontroll enligt " +
      "djurskyddslagen (2018:1192). Begäran omfattar även bilagor " +
      "till rapporterna, till exempel fotobilagor.\n\nJag önskar " +
      "handlingarna i elektronisk form, som PDF, till denna " +
      "e-postadress. Om en uppgift i en handling inte kan lämnas " +
      "ut önskar jag handlingen i övriga delar.\n\nOm en avgift " +
      "tas ut önskar jag besked om beloppet innan handlingarna " +
      "skickas.",
  },
  {
    label: "Begäran B: beslut om föreläggande",
    text:
      "Jag begär kopior av beslut om föreläggande i " +
      "djurskyddsärenden som gäller hållning av nötkreatur, grisar " +
      "eller fjäderfä. Med föreläggande avser jag beslut enligt 8 " +
      "kap. 9 § djurskyddslagen (2018:1192) eller enligt de " +
      "EU-bestämmelser som lagen kompletterar.\n\nBegäran avser de " +
      "10 senast meddelade besluten, räknat efter beslutsdatum, " +
      "under perioden 1 januari 2022 till och med 31 december " +
      "2025. Har färre än 10 sådana beslut meddelats under " +
      "perioden avser begäran samtliga. Begäran omfattar även " +
      "bilagor till besluten, till exempel kontrollrapporter och " +
      "fotobilagor. Beslut om omhändertagande av djur och beslut " +
      "om djurförbud ingår inte i begäran.\n\nJag önskar " +
      "handlingarna i elektronisk form, som PDF, till denna " +
      "e-postadress. Om en uppgift i en handling inte kan lämnas " +
      "ut önskar jag handlingen i övriga delar.\n\nOm en avgift " +
      "tas ut önskar jag besked om beloppet innan handlingarna " +
      "skickas.",
  },
  {
    label: "Begäran C: statistikuppgifter, Jordbruksverket",
    text:
      "Jag begär en sammanställning av uppgifter ur " +
      "djurskyddskontrollregistret om djurskyddskontroller av " +
      "nötkreatur, grisar och fjäderfä under åren 2024 och " +
      "2025.\n\nJag önskar antal genomförda fysiska kontroller " +
      "per länsstyrelse, år och djurslag, fördelat på\n\n1. " +
      "oanmälda respektive föranmälda kontroller,\n2. " +
      "kontrolltyp, till exempel rutinkontroll, kontroll efter " +
      "anmälan och uppföljande kontroll,\n3. kontroller med minst " +
      "en konstaterad brist respektive utan konstaterad " +
      "brist.\n\nJag begär endast antalsuppgifter, inga uppgifter " +
      "om enskilda kontrollobjekt. Kan någon del inte tas fram " +
      "med rutinbetonade åtgärder önskar jag besked om vilken " +
      "del, och de delar som kan tas fram.\n\nJag önskar " +
      "sammanställningen i elektronisk form, till exempel som " +
      "Excel eller CSV, till denna e-postadress.\n\nOm en avgift " +
      "tas ut önskar jag besked om beloppet innan " +
      "sammanställningen skickas.",
  },
];

export const sv: Copy = {
  locale: "sv",
  site: {
    name: "Antumbra",
    tagline: "Ett kunskapsunderlag om djurskyddskontrollens likvärdighet.",
    repo: "https://github.com/MartinBlomqvistDev/antumbra",
    description:
      "En mätning av den svenska djurskyddstillsynen, med EU:s " +
      "revisioner av medlemsstaternas kontrollsystem som " +
      "jämförelsegrund. Varje tal går att följa till sin källa, och i " +
      "EU-lagret hela vägen till den exakta meningen i " +
      "revisionsrapporten.",
    navLabel: "Huvudnavigering",
    cardAlt:
      "Antumbra, en mätning av den svenska djurskyddskontrollens " +
      "likvärdighet. 64,1 % av kontrollrapporterna bär minst en " +
      "maskning, av besluten om föreläggande 22,9 %.",
  },
  nav: [
    { href: "/", label: "Hem" },
    { href: "/sverige/", label: "Sverige" },
    { href: "/jamforelse/", label: "EU-jämförelsen" },
    { href: "/uppslag/", label: "Uppslag" },
    { href: "/metod/", label: "Metod" },
    { href: "/handlingar/", label: "Handlingar" },
    { href: "/data/", label: "Data" },
    { href: "/om/", label: "Om" },
  ],
  languageSwitch: { href: "/en/", label: "English" },
  themeToggle: "Byt färgläge",
  footer: {
    privacy: "Inga kakor, ingen spårning. Sökfrågor loggas inte.",
    source:
      "Källdata: myndigheternas egna handlingar, begärda enligt " +
      "offentlighetsprincipen, och DG SANTE:s publicerade " +
      "revisionsrapporter.",
    repo: { label: "Kodarkiv", text: "github.com/MartinBlomqvistDev/antumbra" },
    dataset: {
      label: "Dataset",
      text: "huggingface.co/datasets/MartinBlomqvist/djurskyddstillsyn",
      href: "https://huggingface.co/datasets/MartinBlomqvist/djurskyddstillsyn",
    },
  },
  home: {
    title: "Antumbra",
    kicker: "En mätning av den svenska djurskyddstillsynen",
    lead:
      "Två likalydande begäranden om allmänna handlingar till samtliga " +
      "21 länsstyrelser och en tredje till Jordbruksverket, förda efter " +
      "ett förskrivet protokoll: skillnaderna i svar är måttet. Som " +
      "jämförelsegrund står EU:s revisioner av medlemsstaternas kontroll. " +
      "Varje tal på sajten går att följa till sin källa, och i EU-lagret " +
      "hela vägen till den exakta meningen i revisionsrapporten.",
    swedenHeading: "Sverige, insamlingen stängd",
    euHeading: "EU-jämförelsen, 1998–2026",
    swedenLabels: {
      classA:
        "av kontrollrapporterna bär minst en maskning, " +
        "{dokument} dokument från {lan} län",
      classB:
        "av besluten bär minst en maskning, " +
        "{dokument} dokument från {lan} län",
      paid: "betald avgift i hela insamlingen",
      paidValue: "0 kr",
    },
    numberLabels: {
      audits: "revisioner",
      recommendations: "rekommendationer",
      citationsResolved: "av citeringarna upplösta till sitt stycke",
    },
    chain: {
      heading: "Kedjan i ett exempel",
      intro:
        "Samma väg finns bakom varje tal på sajten: från aggregatet, via " +
        "raderna, till det ordagranna stycket och dokumentets " +
        "kontrollsumma. Den svenska halvan slutar i kontrollsumman. De " +
        "handlingarna bär personuppgifter och publiceras aldrig, så det " +
        "som står öppet är manifestet med sha256 per fil och " +
        "myndigheternas egna svar ordagrant.",
      steps: {
        figure: "Siffran",
        rows: "Raderna bakom den",
        paragraph: "Stycket, ordagrant",
        document: "Källdokumentet",
      },
      figureLead: "rekommendationer till Sverige i EU:s revisioner",
      toCountry: "Hela underlaget för Sverige",
    },
  },
  sverige: {
    title: "Sverige",
    lead:
      "Granskas djurskyddet likvärdigt över landet, och går tillsynen " +
      "att granska utifrån? Undersökningen mäter det med länsstyrelsernas " +
      "egna svar.",
    design: {
      heading: "Mätningens uppbyggnad",
      body:
        "Två begäranden gick till samtliga 21 länsstyrelser med samma " +
        "lydelse: A avser de senaste kontrollrapporterna, B de senaste " +
        "besluten om föreläggande. En tredje begäran, C, avser " +
        "statistikuppgifter ur Jordbruksverkets " +
        "djurskyddskontrollregister. Varje svar hanteras efter ett i " +
        "förväg skrivet protokoll: samma avsmalning vid avgift, samma " +
        "begäran om beslut, samma frist. När frågorna är identiska och " +
        "hanteringen förutbestämd är det myndigheterna som skillnaderna i " +
        "utfall speglar.",
    },
    processNote:
      "Insamlingen är stängd. Samtliga 43 begäranden har nått ett " +
      "slutstatus, och varje berörd myndighet fick sina egna tal den 2 " +
      "oktober 2026 med tre veckors svarstid. Registertabellen på sidan " +
      "Sverige tillkom efter det, och metodsidan redovisar det. " +
      "Myndigheternas svar står " +
      "ordagrant vid sidan av siffrorna på sidan Handlingar, och uteblivet " +
      "svar skrivs ut som uteblivet svar. Jordbruksverkets avslag på " +
      "korsningen i begäran C, avisering mot brist, är överklagat och " +
      "prövas av Kammarrätten i Jönköping som " +
      "mål 3339-26, registrerat den 10 september 2026 och ännu inte " +
      "avgjort.",
    resultat: {
      heading: "Maskningen i de två handlingsklasserna",
      note:
        "Ett dokument räknas som maskat när en fylld rektangel täcker text " +
        "eller när text saknas under rektangeln. Måttet är maskinellt och " +
        "beskrivet i sin helhet i metoden. Det mäter om myndigheten lämnade " +
        "ut uppgiften. Vad uppgiften säger ligger utanför måttet.",
      classLabel: "Klass",
      documents: "Dokument",
      masked: "Med minst en maskning",
      authorities: "Myndigheter",
      classes: {
        A: "A, kontrollrapporter med bilagor",
        B: "B, beslut om föreläggande med bilagor",
      },
      contrast:
        "Kontrastmåttet enligt protokollets punkt P1 är skillnaden inom " +
        "samma myndighet. För de {counties} län som levererat i båda " +
        "klasserna är medianskillnaden {share} procentenheter i andel " +
        "maskade dokument och {area} procentenheter i maskad yta.",
      contrastException:
        "Två mått drar isär, och det redovisas i stället för att utjämnas " +
        "av medianen: {names} maskar en större andel av sina dokument i " +
        "klass B än i klass A. Inget län maskar en större yta i klass B.",
      contrastNoException:
        "Inget län maskar mer i klass B än i klass A, i något av de två " +
        "måtten.",
    },
    kontrastDiagram: {
      heading: "Skillnaden mellan handlingstyperna, län för län",
      note:
        "En rad per län som levererat i båda klasserna. Pricken är andelen " +
        "dokument med minst en maskning, den grå staven bakom den är " +
        "95-procentigt Wilson-intervall, och raderna står sorterade efter " +
        "hur stort gapet mellan klasserna är. Sorteringen följer alltså " +
        "gapet och inte maskningsgraden: en ordning efter andel vore en " +
        "rangordning av län, och den bär mätningen inte.",
      reports: "kontrollrapporter",
      decisions: "beslut om föreläggande",
      countsNote:
        "Andel dokument med minst en maskning per län och klass. Talen till " +
        "höger är maskade av utlämnade, kontrollrapporter först.",
      rowTitle:
        "{county}: {reportsShare} av kontrollrapporterna ({reports}), " +
        "{decisionsShare} av besluten ({decisions})",
      versus: "mot",
      limit:
        "Vad diagrammet inte säger: vilket län som maskar mest. Ett län med " +
        "få dokument får ett brett intervall, och två rader vars intervall " +
        "överlappar hålls isär av ingenting. Diagrammet visar skillnaden " +
        "mellan handlingstyper inom samma myndighet, vilket är den " +
        "jämförelse mätningen kan belägga.",
    },
    lanJamforelse: {
      heading: "Länen i den ordning måttet ger",
      note:
        "Ordningen är den varje myndighet fick i sitt eget underlag före " +
        "publicering. Myndigheter med samma andel delar plats, eftersom " +
        "mätningen inte skiljer dem åt, och ordningen innebär ingen " +
        "bedömning av handläggningen.",
      classHeading: {
        A: "Klass A, kontrollrapporter",
        B: "Klass B, beslut om föreläggande",
      },
      caption:
        "Andelen dokument med minst en maskning, per myndighet. Antalet " +
        "dokument skiljer sig mellan myndigheter, eftersom begäran hade ett " +
        "tak och några myndigheter tog ut en avgift som ledde till en " +
        "avsmalning.",
      intervalNote:
        "Ett län med fem dokument och fem maskningar och ett län med " +
        "tjugotre har båda hundra procent på raden, men intervallen i " +
        "kolumnen bredvid skiljer sig kraftigt, och samma hundra betyder " +
        "därför olika saker. Intervallet är ett 95-procentigt " +
        "Wilson-intervall och dessutom ett golv: ett läns dokument är inte " +
        "oberoende dragningar utan ärenden i följd, ofta hos samma " +
        "handläggare, så den verkliga osäkerheten är större än den som står.",
      separated:
        "Måttet skiljer bara {separated} av {pairs} länspar. För de övriga " +
        "går det inte att säga vilket län som maskar mest, eftersom " +
        "intervallen överlappar.",
      headers: {
        place: "Plats",
        authority: "Myndighet",
        documents: "Dokument",
        share: "Med minst en maskning",
        interval: "Intervall",
      },
    },
    par: {
      heading: "Samma ärenden i båda klasserna",
      note:
        "Protokollets punkt P1 pekar ut den starkaste jämförelsen: ärenden där " +
        "samma kontrolltillfälle finns både som fristående rapport i klass A " +
        "och som handling i klass B. Då är myndigheten, perioden och ärendena " +
        "desamma, och det som skiljer är handlingens rättsliga status.",
      finding:
        "{counties} län har myndighetens egna ärendenummer i filnamnen i båda " +
        "klasserna, och i ett av dem, {county}, förekommer samma ärenden i " +
        "båda. Där finns {pairs} sådana ärenden: {maskedA} av {documentsA} " +
        "kontrollrapporter i klass A är maskade, mot {maskedB} av " +
        "{documentsB} dokument ur samma ärenden i klass B. Klasserna bär " +
        "olika handlingar ur samma ärende. Samma handling är aldrig mätt " +
        "två gånger.",
      limit:
        "Jämförelsen går inte att göra i övriga län. {unnumbered} av {files} " +
        "filer saknar ärendenummer i namnet, och utan det finns ingenting som " +
        "knyter en rapport till ett beslut.",
    },
    bilagor: {
      heading: "Bilagorna",
      note:
        "Begäran omfattade bilagor, och att undanhålla en hel bilaga är den " +
        "kraftigaste maskning som finns. Bilagor mäts därför för sig och slås " +
        "aldrig ihop med ytmåttet.",
      finding:
        "{files} bilagefiler kom in i hela insamlingen, från {counties} län. " +
        "{refers} dokument hänvisar till innehåll i en bilaga, och {template} " +
        "av dem gör det med en mening ur den nationella kontrollrapportmallen: " +
        "att foton som togs finns i bilaga. Den meningen står i mallen oavsett " +
        "om något foto togs.",
      limit:
        "Därför går de förregistrerade bilagemåtten inte att beräkna, och de " +
        "redovisas som en lucka med skälet utskrivet. Materialet skiljer inte " +
        "en bilaga som hållits inne från en som aldrig fanns, ingenting knyter " +
        "en bilagefil till sitt dokument, bilagefilen läses ur filnamnet och " +
        "är därmed ett golv, och {unreadable} filer saknar läsbart textlager. " +
        "Att ta reda på vilket som gäller kräver en fråga till myndigheterna, " +
        "och den ställs inte.",
    },
    register: {
      heading:
        "Jordbruksverkets register: oanmälda kontroller och andel med brist",
      tablesHeading: "Alla fyra djurslag, per län och år",
      lead:
        "Andelen oanmälda kontroller av nötkreatur skiljer stort mellan länen, " +
        "och skillnaden följer tätt hur stor del av länets kontroller som låg " +
        "utanför rutin. Den ska därför inte läsas som hur ofta länet väljer " +
        "att komma oanmält.",
      note:
        "Begäran C gällde antalsuppgifter ur djurskyddskontrollregistret: " +
        "kontroller per län, år och djurslag, fördelade på oanmälda och " +
        "föranmälda, på kontrolltyp och på om en brist konstaterades. " +
        "Jordbruksverket lämnade uttaget i två delar: en excelfil med " +
        "kontrolltyp och brist, och {reports} rapporter med aviseringen per " +
        "län, djurslag och år, levererade den 21 augusti 2026 efter beskedet " +
        "att den uppgiften inte gick att få ut per län. Korsningen mellan " +
        "avisering och brist avslogs i beslut, med skälet att den kräver " +
        "bearbetning utöver rutinbetonade åtgärder, och avslaget är " +
        "överklagat.",
      reading:
        "Tabellen bär två tal per län och år. Andelen oanmälda räknas över " +
        "alla kontrolltyper, eftersom varje rapport avser alla " +
        "kontrolltypgrupper. Andelen med brist räknas över rutinkontroller, " +
        "eftersom fem kontrolltyper bär utfallet i sitt eget namn, till " +
        "exempel klagomål med brister, och skulle låta kontrolltypsmixen " +
        "avgöra länets bristandel. Talen bredvid är underlaget: användningar " +
        "av checklistan för aviseringen, djurhållarrader för bristen.",
      hypothesis:
        "Hypotesen skrevs innan någon begäran gick: oanmälda kontroller ger " +
        "oftare konstaterade brister än föranmälda, och andelen oanmälda " +
        "förklarar en del av spridningen mellan länen. Bara den andra halvan " +
        "gick att pröva, som ett rangsamband över länen, och bara för " +
        "nötkreatur når tillräckligt många län golvet på båda måtten.",
      outcome:
        "I det rena måttet, rutinkontroller, finns inget stöd: 2024 ger " +
        "ingenting och 2025 ett positivt samband som inte når signifikans. " +
        "Det enda signifikanta sambandet ligger i måttet över alla " +
        "kontrolltyper, där kontrolltypsmixen kan ge mönstret mekaniskt. " +
        "Prövningen skiljer inte ett svagt positivt samband från inget " +
        "samband. Andelen oanmälda är dessutom räknad över alla kontrolltyper " +
        "och följer kontrollmixen, så prövningen mäter i praktiken mest hur " +
        "stor del av länets kontroller som låg utanför rutin. Den säger därför " +
        "lite om vad en oanmäld rutinkontroll hittar.",
      limits: [
        "En rad i uttaget är en djurhållare vid en kontroll. En kontroll med två djurhållare blir två rader, och filen bär ingen identifierare som gör att de kan läggas ihop. Andelen med brist är en andel över djurhållarrader.",
        "Bristflaggan sitter på kontrollen. En kontroll som rör flera djurslag kan bära en brist som gäller ett annat djur än det raden räknas på.",
        "Skillnaden i bristandel mellan oanmälda och föranmälda kontroller inom samma län går inte att räkna, eftersom aviseringen aldrig korsades med bristen i uttaget.",
        "Inga intervall redovisas här, eftersom raderna inte är oberoende kontroller. Två län med olika andel ska inte läsas som åtskilda bara för att talen skiljer sig.",
        "Rapporternas tal heter i filen Antal gånger checklista använd. Om det är samma sak som antalet kontroller står inte i leveransen, och frågan är ställd till myndigheten utan att något besked kommit.",
        "Kontrollmixen räknas på djurhållarrader ur excelfilen och aviseringen på rapporterna. Spannet för rutinkontroller förutsätter att dubbletterna fördelar sig jämnt mellan kontrolltyperna, och det går inte att kontrollera här.",
      ],
      mix: {
        heading: "Andelen oanmälda följer kontrollmixen",
        reading:
          "Varje punkt är ett län. Den vågräta axeln visar hur stor del av " +
          "nötkreaturskontrollerna som låg utanför rutin, alltså klagomål, " +
          "uppföljningar och övriga typer. Den lodräta visar andelen oanmälda. " +
          "Ett län på den streckade linjen har lika många oanmälda kontroller " +
          "som kontroller utanför rutin. Mixen kommer ur excelfilen och " +
          "aviseringen ur rapporterna, två skilda fält. Läsningen var inte " +
          "förregistrerad: den gjordes den 30 oktober 2026, efter " +
          "publiceringen, och redovisas som utforskande.",
        swing:
          "Mixen kan ändras mycket på ett år. I Skåne gick rutinraderna från " +
          "{routineFrom} till {routineTo} mellan 2024 och 2025, medan andelen " +
          "oanmälda föll från {shareFrom} till {shareTo}.",
        bounds:
          "Uttaget säger inte hur ofta just rutinkontroller var oanmälda, " +
          "eftersom rapporterna inte delar aviseringen på kontrolltyp. Ett " +
          "spann går ändå att räkna: det lägsta talet gäller om alla kontroller " +
          "utanför rutin var oanmälda, det högsta om ingen av dem var det. " +
          "Spannet är oftast brett. Det skiljer {parted2024} av {pairs} länspar " +
          "2024 och {parted2025} år 2025, och om övriga par säger det ingenting.",
        direction:
          "Mönstret kommer mer från uppföljningar än från klagomål, och " +
          "uppföljningar följer på tidigare kontroller. Sambandet kan därför " +
          "gå åt motsatt håll mot hypotesen: ett län som hittar fler brister " +
          "kan behöva fler uppföljningar, och uppföljningar kan oftare vara " +
          "oanmälda. Bristandelen och uppföljningsandelen hänger ihop olika " +
          "starkt de två åren, så förklaringen är en möjlighet som uppgifterna " +
          "inte kan avgöra.",
        axisX: "Andel kontroller utanför rutin",
        axisY: "Andel oanmälda",
        line: "lika andelar",
        chartLabel:
          "{year}: andelen oanmälda mot andelen kontroller utanför rutin, ett " +
          "län per punkt. Punkterna följer den streckade linjen. Alla tal står " +
          "i tabellen under diagrammet.",
        dotTitle: "{county}: {outside} utanför rutin, {unannounced} oanmälda",
        summary: "Talen per län, nötkreatur",
        headers: {
          county: "Län",
          routine: "Rutin",
          unannounced: "Oanmälda",
          range: "Oanmälda bland rutin",
          n: "n",
        },
        rangeFormat: "{low} till {high} %",
        associations: {
          heading: "Sambanden över länen, nötkreatur",
          note:
            "Spearmans rho mäter om länen står i samma ordning på två listor: " +
            "1 betyder samma ordning och 0 ingen koppling. Talet p visar hur " +
            "lätt slumpen ger ett lika starkt samband, i endera riktningen. Det " +
            "lägsta värde 2 000 permutationer kan ge är 0,0005.",
          headers: {
            measure: "Jämförelse",
            year: "År",
            counties: "Län",
            rho: "Spearmans rho",
            p: "p, permutation",
          },
          measures: {
            ej_rutin: "Andel utanför rutin mot andel oanmälda",
            klagomal: "Andel klagomål mot andel oanmälda",
            uppfoljning: "Andel uppföljningar mot andel oanmälda",
            brist_uppfoljning: "Andel med brist, rutin, mot andel uppföljningar",
          },
        },
      },
      species: {
        nötkreatur: "Nötkreatur",
        gris: "Gris",
        ">350 värphöns": "Värphöns, fler än 350",
        slaktkyckling: "Slaktkyckling",
      },
      categories: { rutin: "rutinkontroller", alla: "alla kontrolltyper" },
      headers: {
        county: "Län",
        unannounced: "Oanmälda",
        deficiency: "Med brist, rutin",
        n: "n",
      },
      associations: {
        heading: "Sambandet över länen, som steg 28 prövade det",
        headers: {
          species: "Djurslag",
          year: "År",
          category: "Kategori",
          counties: "Län",
          rho: "Spearmans rho",
          p: "p, permutation",
        },
      },
    },
    notShown: {
      heading: "Vad sidan inte visar",
      items: [
        "Handlingarna själva. De innehåller personuppgifter och publiceras aldrig; förteckningen med kontrollsumma per fil står på sidan Handlingar.",
        "Något påstående om att en myndighet brutit mot lag. Rättsläget är oavgjort och Högsta förvaltningsdomstolen har inte prövat frågan. Fyra beslut är överklagade, och det första avgjordes den 23 oktober 2026: Kammarrätten i Stockholm avslog överklagandet av Gotlands beslut och fann ingen anledning att göra någon annan bedömning än länsstyrelsens. Tre mål är oavgjorda.",
        "Tre län som avstod från kopiorna sedan en avgift kvarstod efter avsmalningen. De bär en avgiftsuppgift men inga dokument i maskningsmätningen, och bortfallet räknas aldrig som ett utlämnande eller som ett avslag.",
        "Gris som jämförelse. Sexton dokument har gris som dominerande djurslag, utspridda på tio län, så inget län har underlag på båda sidor.",
        "Vad ett dokument är när en myndighet buntar flera i en fil. Måttet räknar den levererade filen, och två av materialets 343 filer rymmer fem handlingar var. Den ena är Norrbottens leverans i klass B, som därför står på ett dokument där länet lämnade ut fem beslut; andelen maskade påverkas inte, eftersom alla fem är omaskade. Den andra ligger utanför klassernas tal.",
        "De gränser måttet har. De står i metoden, tillsammans med avvikelserna från förregistreringen och de fel som rättats under arbetet.",
      ],
    },
    overview: {
      heading: "Läget i siffror",
      sent: "begäranden avsända",
      files: "filer mottagna, verifierade med sha256",
      deliveringAuthorities:
        "av 22 myndigheter har levererat handlingar eller uppgifter",
      feeNotices: "myndigheter aviserade en avgift",
      feeStopped: "begäranden avgiftsstoppade",
      paid: "betald avgift",
      paidValue: "0 kr",
    },
    wordings: {
      heading: "Begärandenas exakta lydelse",
      note:
        "Samma text skickades till samtliga 21 länsstyrelser den 3 " +
        "augusti 2026, en begäran per mejl. Begäran C gick till " +
        "Jordbruksverket samma dag.",
      items: wordingItems,
    },
    feeStopped: {
      heading: "Avgiftsstoppade begäranden",
      note:
        "Begäranden där en avgift kvarstod efter protokollets " +
        "avsmalning. Kopior avstås då, ett skriftligt beslut om avgiften " +
        "begärs, och utfallet dokumenteras. Ingen avgift har betalats. " +
        "Avgiftsfrågan krävde 41 skrivelser, fördelade på de 16 län som " +
        "aviserade en avgift, flest i Jönköping, Kalmar och Örebro med " +
        "fem var. Utfallen: avgiften föll efter avsmalningen i 12 län, " +
        "ingen avgift aviserades i 5, beslut meddelades i 2, beslut " +
        "vägrades i 1, ett län svarade med ett generellt styrdokument, " +
        "och inget län lämnade frågan obesvarad.",
      noCopies: "inga kopior hämtades ut",
      laterDelivered: "handlingarna kom in senare, utan avgift",
    },
    toHandlingar:
      "Varje mottagen fil är förtecknad med kontrollsumma på sidan " +
      "Handlingar.",
  },
  jamforelse: {
    title: "EU-jämförelsen",
    lead:
      "EU:s revisioner av medlemsstaternas kontrollsystem, land för land " +
      "och år för år. Varje diagram har en tabellvy och ett underlag ned " +
      "till stycket.",
    table: {
      caption:
        "Rekommendationer i DG SANTE:s revisioner per land, hela " +
        "perioden. Klicka på ett land för underlaget ned till stycket.",
      country: "Land",
      audits: "Revisioner",
      recommendations: "Rekommendationer",
      shareBasis: "Anger sin grund",
      shareAnswered: "Besvarade",
    },
    notShown: {
      title: "Vad sidan inte visar",
      body:
        "Sidan omfattar EU-länderna, vars rapporter är hämtade i " +
        "fulltext; övriga länders revisioner finns i registret men är " +
        "inte styckeindexerade här. Andelar visas alltid tillsammans med " +
        "sina antal: en andel över fyra rekommendationer är inte samma " +
        "sak som en andel över fyrahundra.",
    },
    charts: {
      tableView: "Tabellvy",
      of: "av",
      byYear: {
        title: "Rekommendationer per år",
        note:
          "Samtliga rekommendationer i EU-ländernas revisionsrapporter, " +
          "efter revisionens år.",
      },
      basis: { title: "Anger sin grund, per land" },
      answered: { title: "Besvarade av medlemsstaten, per land" },
      chain: {
        title: "Kedjan sluts, per land",
        note:
          "Kedjan sluts när rekommendationen anger sin grund, grunden " +
          "upplöses till ett ordagrant stycke och en åtgärdsplan besvarar " +
          "den. Allt annat räknas som en delvis kedja, och en delvis kedja " +
          "räknas nedåt.",
      },
      yearHeader: "År",
      shareHeader: "Andel",
    },
  },
  chain: {
    sourceDocument: "Källdokument",
    checksum: "sha256",
    recommendationLabel: "Rekommendation",
    recommendationsCount: "rekommendationer",
    legalBasis: "Rättslig grund",
    citesHeading: "Rekommendationen anger som grund",
    unresolved:
      "Citeringen kunde inte upplösas till ett numrerat stycke i " +
      "rapporten.",
    responseHeading: "Medlemsstatens svar",
    backToTable: "Till jämförelsen",
  },
  uppslag: {
    title: "Uppslag",
    lead:
      "Sex frågor körda mot 81 292 stycken ur DG SANTE:s revisionsrapporter. " +
      "Svaren är alltid ordagranna citat med land, referens och styckenummer.",
    banner:
      "Hämtningen hittar var ett ämne behandlas. Vad som konstaterats " +
      "framgår bara av citatet, så läs det.",
    examplesHeading: "Exempelfrågor",
    similarity: "likhet",
    noAnswers:
      "Inget stycke över likhetströskeln. Ett tomt svar står som ett tomt " +
      "svar och fylls aldrig med en gissning.",
    matning: {
      heading: "Varför sökrutan är borta",
      body: [
        "Hämtningen mättes den 26 oktober 2026 mot 2 115 frågor byggda ur " +
          "citatgrafen, där varje fråga i snitt har 3,54 rätta stycken. Tre " +
          "metoder prövades. BM25 hittar minst ett rätt stycke bland tio för " +
          "49,6 procent av frågorna. Den täta vektorsökningen klarar 31,4 " +
          "procent. Den hybrid som låg här klarade 45,2 procent, alltså sämre " +
          "än ren BM25 på varje mått, och en omrankare ovanpå gjorde den " +
          "sämre än så.",
        "Villkoret skrevs före mätningen: en sökruta som inte slår ren BM25 " +
          "ska bort. Den är borta, och tjänsten som svarade är raderad. De " +
          "sex exempelsvaren nedan står kvar, eftersom de är körda genom " +
          "samma kod och går att kontrollera mot källan.",
        "Ett konkret utfall: ordet debeaking står i tre stycken i korpusen, " +
          "och rutan gav noll träffar på det. Talen ligger i " +
          "data/retrieval_matning.json och data/retrieval_omrankning.json, " +
          "och frågorna i data/retrieval_eval.jsonl.",
      ],
    },
  },
  metod: {
    title: "Metod",
    lead:
      "Protokollet, händelseloggen, besluten och deras skäl. Allt som " +
      "krävs för att göra om mätningen.",
    ai: {
      heading: "AI-assistans",
      body:
        "Insamling, loggföring och analys sker med AI-assistans. Varje " +
        "brev, loggrad och publicerad siffra granskas av en människa " +
        "innan den skickas eller committas, och rollen är dokumenterad " +
        "med datum i ADR-0014. Ingen uppgift på sajten har en " +
        "språkmodell som källa; allt spåras till källdokument med " +
        "kontrollsumma.",
    },
    avvikelser: {
      heading: "Avvikelser från förregistreringen",
      note:
        "Måtten och hypotesen tidsstämplades i repot innan någon begäran " +
        "skickades. Tre delar gick inte att genomföra som de var skrivna. " +
        "De står här, överst, med vad som gjordes i stället.",
      items: [
        {
          title: "Fältmåttet gick inte att räkna bokstavligt",
          body:
            "Maskningsgrad förregistrerades som andel maskerad yta plus " +
            "andel maskerade fält. Handlingarna är löpande prosa utan " +
            "fältstruktur, så fältdelen går inte att beräkna. Den ersattes " +
            "den 17 augusti 2026 av ett mått på täckt innehåll enligt " +
            "ADR-0017, och utfallet blev ett nollresultat: noll dokument " +
            "döljer brödtext bakom en ljus täckning, och de 236 dolda tecken " +
            "som finns är sidhuvud under myndighetens egen vita ruta.",
        },
        {
          title: "Ytmåttet pekar fel för en av maskningsteknikerna",
          body:
            "Där texten under svärtningen är borttagen mäter ytan hur " +
            "rutorna ritats. Hur mycket som hålls inne säger den ingenting om. " +
            "För den " +
            "tekniken är antalet tecken det bättre måttet. Gränsen gäller " +
            "det förregistrerade ytmåttet och ska läsas tillsammans med " +
            "varje ytsiffra.",
        },
        {
          title: "Halva oanmäld-hypotesen går inte att pröva",
          body:
            "Förregistreringen begär både sambandet över län och skillnaden " +
            "i bristandel mellan oanmälda och föranmälda kontroller inom " +
            "samma län, djurslag och kontrolltyp. Den andra delen kräver " +
            "aviseringsfältet korsat med bristfältet, och det uttaget " +
            "lämnades inte ut. Den förskrivna nollresultatstexten påstår " +
            "utfallet av just den prövningen och är struken i stället för " +
            "återgiven. Den del som gick att pröva skiljer inte ett svagt " +
            "positivt samband från inget samband.",
        },
        {
          title: "Registertabellen fanns inte i paketen",
          body:
            "Uttaget ur Jordbruksverkets register lades på sidan Sverige den " +
            "27 oktober 2026, dagen efter publiceringen, och läsningen av " +
            "kontrollmixen tillkom den 30 oktober. Datafilerna låg publika från " +
            "första dagen. Paketen den 2 oktober sade att de bar det som skulle " +
            "publiceras om varje myndighet. Länens rader ur registret fanns " +
            "inte med, så länen har inte fått dem med svarstid. Talen kommer ur " +
            "Jordbruksverkets eget uttag, tabellen bär ingen bedömning av något " +
            "län, och beslutet är loggat. Hör ett län av sig publiceras svaret " +
            "oavkortat.",
        },
      ],
    },
    adr: {
      heading: "Beslutslogg (ADR)",
      note:
        "Varje metod- och arkitekturbeslut är daterat och dokumenterat " +
        "med sina skäl och förkastade alternativ.",
    },
    log: {
      heading: "Händelselogg",
      note:
        "Loggen förs löpande under insamlingen. Varje rad är en händelse " +
        "med verifierat klockslag; ingenting skrivs i efterhand.",
      countLabel: "händelser till och med",
      filterLabel: "Filtrera på myndighet",
      all: "Alla myndigheter",
      headers: {
        date: "Datum",
        time: "Kl.",
        channel: "Kanal",
        authority: "Myndighet",
        request: "Begäran",
        event: "Händelse",
        note: "Notering",
      },
    },
  },
  om: {
    title: "Om mätningen och vem som gjort den",
    lead:
      "Varje begäran bar mitt namn och min e-postadress, så myndigheterna " +
      "har vetat vem som frågade sedan den 3 augusti 2026.",
    body: [
      "Jag heter Martin Blomqvist och arbetar som data scientist. Jag " +
        "skickade de 43 begärandena, läste och undertecknade varje brev innan " +
        "det gick, och hanterade varje svar efter protokollet. Insamlingen, " +
        "loggföringen och analysen har skett med AI-assistans, deklarerad med " +
        "datum på metodsidan. Ingen uppgift i materialet har en språkmodell som " +
        "källa.",
      "Namngiven begäran står som vägval 3 i beslutsloggen, skrivet innan " +
        "något brev gick. Ett överklagande kräver en part, en e-postadress " +
        "är ändå inte anonym, och samma avsändare till alla 22 myndigheter " +
        "tar bort avsändaren som variabel. Anonyma begäranden är " +
        "grundlagsskyddade, men hade gjort avslagsgrenen av mätningen " +
        "omöjlig att driva.",
      "Ingen har beställt eller finansierat arbetet. Budgeten är noll kronor, " +
        "och därför godtogs ingen avgift oavsett belopp. Ingen avgift har " +
        "betalats. Tjänstemän namnges aldrig i materialet; där ett beslut " +
        "namnger beslutsfattare och föredragande skrivs rollen i stället.",
      "Fel i materialet vill jag veta av. Skicka den rättade uppgiften och " +
        "var den kommer ifrån, så att rättelsen görs i underlaget och syns i " +
        "texten därifrån, och loggas med datum.",
    ],
    linksHeading: "Annat jag gjort",
    links: [
      {
        label: "github.com/MartinBlomqvistDev",
        href: "https://github.com/MartinBlomqvistDev",
        note: "Kodarkiven, inklusive det här projektets.",
      },
      {
        label: "linkedin.com/in/martin-blomqvist",
        href: "https://www.linkedin.com/in/martin-blomqvist",
        note: "Yrkesbakgrund och tidigare arbeten.",
      },
      {
        label: "kattochkod.se",
        href: "https://kattochkod.se",
        note: "Konsultbolaget jag driver. Det har inget med den här mätningen att göra.",
      },
      {
        label: "huggingface.co/MartinBlomqvist",
        href: "https://huggingface.co/MartinBlomqvist",
        note: "Dataset och modeller, bland dem den här mätningens aggregat.",
      },
    ],
    photoAlt: "Martin Blomqvist",
    contactHeading: "Kontakt",
    contact: "cm.blomqvist@gmail.com",
  },
  handlingar: {
    title: "Handlingar",
    lead:
      "Vad som begärts ut, vad som lämnats ut, vad som inte lämnats ut " +
      "och varför. Dokumenten innehåller personuppgifter och publiceras " +
      "inte; förteckningen gör leveranserna verifierbara utan dem.",
    tavla: {
      heading: "Myndigheterna, en i taget",
      note:
        "Raden visar vad myndigheten lämnade ut och hur mycket av det som " +
        "är maskat. Arton av de tjugoen länsstyrelserna levererade " +
        "handlingar in i mätningen; tre avstod sedan en avgift kvarstod " +
        "efter avsmalningen, och de bär en avgiftsuppgift men " +
        "inga dokument. Talen är de som myndigheten själv fick före " +
        "publicering, och där ett svar har kommit in står det ordagrant " +
        "under dem. Därunder står hela brevväxlingen i ärendena i " +
        "tidsföljd och ordagrant, både myndighetens meddelanden och mina " +
        "egna brev, vilket är vad breven inför publicering utfäste. " +
        "Namn på enskilda tjänstemän återges inte: där ett svar är " +
        "undertecknat skrivs rollen i stället.",
      classWord: "Klass",
      documents: "Dokument",
      masked: "Maskade",
      rowDocuments: "dokument",
      rowMasked: "maskade",
      utanMatning: {
        avgiftsstoppad: {
          short: "kopiorna avstods sedan avgiften kvarstod",
          long:
            "Myndigheten aviserade en avgift, och den kvarstod efter " +
            "protokollets avsmalning. Kopiorna avstods då enligt punkt P5, " +
            "och ett skriftligt beslut om avgiften begärdes. Begäran bär " +
            "en avgiftsuppgift men inga dokument i " +
            "maskningsmätningen, och bortfallet räknas aldrig som ett " +
            "utlämnande eller som ett avslag.",
        },
        statistik: {
          short: "begäran C avser antalsuppgifter och inga handlingar",
          long:
            "Begäran C avser antalsuppgifter ur " +
            "djurskyddskontrollregistret och inga handlingar, så " +
            "myndigheten ingår inte i maskningsmätningen. Uttaget " +
            "levererades i två delar, den andra som 336 rapporter om " +
            "aviseringen per län, djurslag och år; korsningen mellan " +
            "avisering och brist avslogs, och avslaget är överklagat och " +
            "prövas av Kammarrätten i Jönköping som mål 3339-26. Talen " +
            "står på sidan Sverige.",
        },
      },
      merged:
        "Myndigheten hanterar de två begärandena som ett ärende och svarade " +
        "samlat, så leveransen ligger i sin helhet under klass B. P0b säger " +
        "att ingen begäran om särskiljning skickas, eftersom det vore en " +
        "signal som inte alla myndigheter får.",
      area: "Maskad yta",
      interval: "Intervall",
      place: "Plats",
      placeOf: "i jämförelsen",
      reply: {
        heading: "Myndighetens svar på underlaget",
        none: "Inget svar har kommit in",
        kinds: {
          autosvar: "autosvar",
          besked: "besked om handläggningen",
          substantiellt: "svar i sak",
        },
        from: "från",
        subject: "Ämnesrad:",
        attachments: "Bilagor:",
        omitted: "Återges inte:",
        message: "Meddelande",
        context:
          "Hänvisar svaret till ett tal eller ett förlopp som inte står " +
          "ovan? Varje händelse i ärendet, med datum och klockslag, står i " +
          "händelseloggen, och måttens gränser i metoden.",
        contextLink: "Metod och händelselogg",
      },
      thread: {
        heading: "Brevväxlingen i ärendena, i tidsföljd",
        note:
          "Allt som skrevs i begäran A, B och C och i överklagandena, " +
          "ordagrant och i den ordning det skickades: {messages} meddelanden " +
          "från myndigheten och {sent} brev från mig. Ett stående autosvar " +
          "bärs av en rad och dess upprepningar listas under den. " +
          "Myndighetens signaturblock återges inte, och inte heller " +
          "adressen till en namngiven tjänsteman jag skrivit till; min egen " +
          "signatur står kvar, eftersom mätningen vilar på vem som " +
          "frågade. Paketen och dagtalen i mina brev står i kodarkivet, " +
          "eftersom ingen svarstid per län publiceras på webbplatsen. Varje " +
          "rad säger själv vad den lämnar ute.",
        none: "Inget meddelande i de här ärendena finns i registret.",
        fromAuthority: "Från myndigheten",
        fromMe: "Från mig",
      },
      letters: {
        subject: "Ämnesrad:",
        omitted: "Återges inte:",
        message: "Meddelande",
        attachments: "Bilagor:",
        repeats: "Samma text återkom:",
        messagesWord: "meddelanden",
      },
      sent: {
        missing:
          "Brevet går inte att återge ordagrant och gissas inte. Att det " +
          "gick framgår av källan, och raden står därför som en lucka:",
        packet: "Brevet står i kodarkivet, eftersom det bär tidsförlopp per län.",
        days: "dagtal per län, som står i kodarkivet.",
        request: "begäran",
        to: "till",
        subject: "Ämnesrad:",
        omitted: "Återges inte:",
        message: "Meddelande",
      },
      packet: {
        heading: "Underlaget myndigheten fick",
        note:
          "Brevet som gick ligger i kodarkivet, och kontrollsumman nedan visar " +
          "att det är samma brev. Det står inte på den här sidan, eftersom det " +
          "bär tidsförlopp per län och ingen svarstid per län publiceras på " +
          "webbplatsen. Koden som bygger breven är rättad två gånger sedan " +
          "utskicket, så ett brev byggt i dag är inte brevet som gick. " +
          "Rättelserna står i händelseloggen.",
        sent: "Avsänt",
        read: "Läs brevet i kodarkivet",
      },
    },
    domstolar: {
      heading: "Domstolarna",
      note:
        "Fyra av besluten om maskning är överklagade, och kammarrätternas egna " +
        "meddelanden i de målen hör till samma korrespondenslogg som " +
        "myndigheternas. De bär inga maskningstal, eftersom en domstol inte är " +
        "mätt här. Målen redovisas som pågående; ett pågående mål skjuter inte " +
        "upp publiceringen.",
    },
    deliveries: {
      heading: "Levererade handlingar",
      note:
        "Varje mottagen fil registreras med sin sha256-kontrollsumma i " +
        "ett manifest som är beständigt: en post kan läggas till men " +
        "aldrig ändras. Förteckningen räknar filer, och mätningen räknar " +
        "dokument. " +
        "Maskningsmätningen läser mapparna med ändelsen _A och _B; övriga " +
        "mappar bär det som också kom in i ärendena utan att mätas: " +
        "avgiftsbeslut, avslagsbeslut, Jordbruksverkets statistikuttag, " +
        "nämnarsvar och korrespondensen med kammarrätterna. Två av de " +
        "mätta mapparna rymmer en fil mer än sitt antal dokument, " +
        "Uppsalas 28 mot 27 och Kalmars 6 mot 5: Uppsalas extra post är " +
        "zip-arkivet som handlingarna kom i, och Kalmars är länets " +
        "avslagsbeslut i samma mapp.",
      fileWord: "fil",
      filesWord: "filer",
      headers: { file: "Fil", bytes: "Byte", sha256: "sha256" },
    },
  },
  data: {
    title: "Data",
    lead:
      "Varje härledd fil projektet publicerar, med radantal mätt i bygget. " +
      "Granskningsbar utifrån betyder att vem som helst kan räkna om.",
    note:
      "Filerna ligger i kodarkivets katalog data/ och är radvis JSON. " +
      "Handlingarna själva publiceras aldrig: de innehåller personuppgifter, " +
      "och det som publiceras om dem är förteckningen med kontrollsumma per " +
      "fil. Namn på enskilda tjänstemän återges ingenstans; där en källa " +
      "namnger en person skrivs rollen i stället.",
    repo: {
      before: "Kodarkivet är",
      label: "github.com/MartinBlomqvistDev/antumbra",
      href: "https://github.com/MartinBlomqvistDev/antumbra",
      after: ", och varje filnamn nedan länkar till filen där.",
    },
    headers: {
      file: "Fil",
      rows: "Rader",
      bytes: "Byte",
      description: "Innehåll",
    },
    missing: "ligger utanför kodarkivet, se metoden",
    groups: [
      {
        heading: "Öppenhetslagret",
        note:
          "De tre begärandena, handläggningen och maskningsmätningen. " +
          "Händelseloggen är den fullständiga redovisningen av vad som " +
          "hänt i ärendena, i den ordning det loggades.",
        files: [
          {
            path: "data/protokoll_logg.jsonl",
            beskrivning:
              "Händelseloggen. En rad per händelse med datum, klockslag, " +
              "kanal, myndighet, begäran och notering.",
          },
          {
            path: "data/korrespondens.jsonl",
            beskrivning:
              "Myndigheternas egna meddelanden, ordagrant, med " +
              "meddelande-id. Varje rad säger själv vad den utelämnar: " +
              "den citerade historiken, signaturblockets personuppgifter, " +
              "länkmålen, en rad som inte var annat än en länk, och " +
              "domstolarnas engångslänkar. Myndighetens egen " +
              "funktionsbrevlåda och växel står kvar.",
          },
          {
            path: "data/korrespondens_utgaende.jsonl",
            beskrivning:
              "Mina egna brev i samma ärenden, ordagrant, med meddelande-id " +
              "ur brevlådan. Mottagaren står som funktionsbrevlåda eller " +
              "namngiven tjänsteman och aldrig som adress; den citerade " +
              "historiken och länkmålen är kapade, och min egen signatur " +
              "står kvar. Två rader är redovisade luckor utan meddelande-id.",
          },
          {
            path: "data/p12_avsant_manifest.jsonl",
            beskrivning:
              "De 22 paket som skickades före publicering, med kontrollsumma " +
              "per brev.",
          },
          {
            path: "data/leveranser_manifest.jsonl",
            beskrivning:
              "Varje mottagen fil med sha256. Append-only: en post läggs " +
              "till och ändras aldrig.",
          },
          {
            path: "data/maskning.jsonl",
            beskrivning:
              "Maskningsmätningen per dokument: rutor, balkar, tecken under " +
              "rutorna, maskad yta och vilken metod som läst sidan.",
          },
          {
            path: "data/kontrast.jsonl",
            beskrivning:
              "Kontrastmåttet per myndighet, djurslag och handlingsklass.",
          },
          {
            path: "data/djurslag.jsonl",
            beskrivning:
              "Vilket djurslag varje dokument handlar om, och hur det avgjordes.",
          },
          {
            path: "data/dold_text.jsonl",
            beskrivning:
              "Täckt innehåll: text som ligger kvar under något som inte är " +
              "svart. Måttet som ersatte det förregistrerade fältmåttet.",
          },
          {
            path: "data/sekretessgrunder.jsonl",
            beskrivning:
              "De bestämmelser myndigheterna åberopat, med följebrevets egna " +
              "ord och meddelande-id.",
          },
          {
            path: "data/namnare.jsonl",
            beskrivning:
              "Länens egna tal om antal kontroller och förelägganden, med " +
              "citatet och hur storleksfrågan lästs.",
          },
          {
            path: "data/beslut.jsonl",
            beskrivning:
              "De överklagbara besluten: diarienummer, delfående, åberopad " +
              "grund och roll i stället för namn.",
          },
          {
            path: "data/avgiftsskrivelser.jsonl",
            beskrivning:
              "Avgiftsmåttet: antal skrivelser och utfall per länsstyrelse, " +
              "för alla 21 oavsett utfall.",
          },
          {
            path: "data/utlamningsgrad.jsonl",
            beskrivning:
              "Taket, nämnaren och antalet filer per län och klass. Kvoten " +
              "är en lucka, och raden bär skälet.",
          },
          {
            path: "data/dubbelforekomst.jsonl",
            beskrivning:
              "Ärenden som förekommer i båda handlingsklasserna, och hur de " +
              "maskats i vardera.",
          },
          {
            path: "data/bristandel.jsonl",
            beskrivning:
              "Andelen kontroller med brist per län, år och djurslag.",
          },
          {
            path: "data/foranmalda.jsonl",
            beskrivning:
              "Aviserade och oaviserade kontroller per län, år och djurslag, " +
              "ur myndighetens eget uttag.",
          },
          {
            path: "data/oanmald_samband.jsonl",
            beskrivning:
              "Sambandet över länen mellan andelen oanmälda kontroller och " +
              "andelen med brist: Spearmans rho per djurslag, år och " +
              "kontrollkategori, med p ur permutation.",
          },
          {
            path: "data/kontrollmix.jsonl",
            beskrivning:
              "Kontrollmixen per län och år för nötkreatur, bredvid aviseringen, " +
              "med spannet för oanmälda bland rutinkontroller. Utforskande.",
          },
          {
            path: "data/kontrollmix_samband.jsonl",
            beskrivning:
              "Sambanden över länen mellan kontrollmix, avisering och brist, " +
              "med tvåsidigt p ur permutation. Utforskande.",
          },
          {
            path: "data/oanmald_hypotes.jsonl",
            beskrivning:
              "Prövningen av den förregistrerade hypotesen, med varje " +
              "delmått och dess utfall.",
          },
          {
            path: "data/atagande.jsonl",
            beskrivning:
              "Projektets egna åtaganden: vad som lovats, när det öppnades " +
              "och när det stängdes.",
          },
        ],
      },
      {
        heading: "Kravlagret",
        note:
          "Tillståndsbesluten för stora gris- och fjäderfäanläggningar, och " +
          "villkoren lästa ordagrant ur dem.",
        files: [
          {
            path: "data/villkor.jsonl",
            beskrivning:
              "Varje villkor ordagrant, med rubriken beslutet självt skrev.",
          },
          {
            path: "data/villkor_baseline.jsonl",
            beskrivning:
              "Baselinetestet: delar villkoret text med ett annat beslut?",
          },
          {
            path: "data/villkor_facit.jsonl",
            beskrivning:
              "Handläst facit för rubrik mot sak, läst blint mot rubriken.",
          },
          {
            path: "data/tillstand_manifest.jsonl",
            beskrivning:
              "Varje hämtad tillståndshandling med sha256 och källänk.",
          },
          {
            path: "data/tillstand_typ.jsonl",
            beskrivning: "Vad utgivaren själv kallar varje beslut.",
          },
          {
            path: "data/tillstand_ocr_index.jsonl",
            beskrivning:
              "OCR-körningen över de inskannade besluten, med konfidens per fil.",
          },
        ],
      },
      {
        heading: "Jämförelselagret",
        note:
          "Kommissionens revisioner av medlemsstaternas kontrollsystem, " +
          "parsade till rekommendationer, citeringar och åtaganden.",
        files: [
          {
            path: "data/dgsante_details.jsonl",
            beskrivning: "En rad per revision: land, år, ämne, länkar.",
          },
          {
            path: "data/dgsante_recommendations.jsonl",
            beskrivning:
              "11 999 rekommendationer ordagrant, med nummer och rapport.",
          },
          {
            path: "data/dgsante_graph.jsonl",
            beskrivning:
              "Citeringsgrafen: en rad per kant, med det citerade stycket bredvid.",
          },
          {
            path: "data/dgsante_action_plans.jsonl",
            beskrivning:
              "Medlemsstaternas svar, kopplade till rekommendationen de svarar på.",
          },
          {
            path: "data/dgsante_manifest.jsonl",
            beskrivning: "Varje nedladdad fil med sha256 och källänk.",
          },
          {
            path: "data/dgsante_annex_classes.jsonl",
            beskrivning:
              "Bilagorna klassade på sina egna ord, med citatet som bär klassningen.",
          },
          {
            path: "data/dgsante_ocr_index.jsonl",
            beskrivning:
              "OCR över de skannade bilagorna, med språk och konfidens per fil.",
          },
        ],
      },
    ],
    licence: {
      heading: "Licens och återanvändning",
      body:
        "Koden är AGPL-3.0 och de härledda datafilerna CC BY 4.0. Mottagna " +
        "myndighetshandlingar sprids inte vidare i någon form. Kommissionens " +
        "dokument är återanvändbara med attribution enligt beslut " +
        "2011/833/EU. Schemat för varje fil framgår av stegen i pipelinen, " +
        "som är numrerade och körs i ordning.",
      dataset: {
        before: "De svenska aggregaten ligger också som ett eget dataset på HuggingFace,",
        label: "huggingface.co/datasets/MartinBlomqvist/djurskyddstillsyn",
        href: "https://huggingface.co/datasets/MartinBlomqvist/djurskyddstillsyn",
        after: ", med schema per fil och de deklarerade luckorna utskrivna.",
      },
    },
  },
};
