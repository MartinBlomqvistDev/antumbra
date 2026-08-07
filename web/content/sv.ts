import type { Copy } from "./types";

const wordingItems = [
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
    tagline: "Från siffra till källa på två klick.",
    description:
      "En mätning av den svenska djurskyddstillsynen, med EU:s " +
      "revisioner av medlemsstaternas kontrollsystem som " +
      "jämförelsegrund. Varje tal kan klickas ned till den exakta " +
      "meningen i källdokumentet.",
    navLabel: "Huvudnavigering",
  },
  nav: [
    { href: "/", label: "Hem" },
    { href: "/sverige/", label: "Sverige" },
    { href: "/jamforelse/", label: "EU-jämförelsen" },
    { href: "/uppslag/", label: "Uppslag" },
    { href: "/metod/", label: "Metod" },
    { href: "/handlingar/", label: "Handlingar" },
    { href: "/data/", label: "Data" },
  ],
  languageSwitch: { href: "/en/", label: "English" },
  themeToggle: "Byt färgläge",
  footer: {
    privacy: "Inga kakor, ingen spårning. Sökfrågor loggas inte.",
    source: "Källdata: DG SANTE:s publicerade revisionsrapporter.",
  },
  home: {
    title: "Antumbra",
    kicker: "En mätning av den svenska djurskyddstillsynen",
    lead:
      "Tre likalydande begäranden om allmänna handlingar till samtliga " +
      "21 länsstyrelser, förda efter ett förskrivet protokoll: " +
      "skillnaderna i svar är måttet. Som jämförelsegrund står EU:s " +
      "revisioner av medlemsstaternas kontroll, där varje tal kan " +
      "klickas ned till den exakta meningen i källdokumentet.",
    swedenHeading: "Sverige, pågående insamling",
    euHeading: "EU-jämförelsen, 1998–2026",
    swedenLabels: {
      sent: "begäranden avsända 3 augusti 2026",
      files: "filer mottagna, verifierade med sha256",
      paid: "betald avgift",
      paidValue: "0 kr",
    },
    numberLabels: {
      audits: "revisioner",
      recommendations: "rekommendationer",
      citationsResolved: "av citeringarna upplösta till sitt stycke",
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
        "hanteringen förutbestämd speglar skillnaderna i utfall " +
        "myndigheterna, inte frågorna.",
    },
    processNote:
      "Insamlingen pågår. Det som visas här är processen i realtid, " +
      "hämtad ur händelseloggen; resultaten och jämförelsen mellan länen " +
      "publiceras när insamlingen är stängd.",
    overview: {
      heading: "Läget i siffror",
      sent: "begäranden avsända",
      files: "filer mottagna, verifierade med sha256",
      deliveringAuthorities: "myndigheter har levererat handlingar",
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
        "begärs, och utfallet dokumenteras. Ingen avgift har betalats.",
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
          "den. Allt annat räknas som en delvis kedja, aldrig uppåt.",
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
      "Sök i 81 292 stycken ur DG SANTE:s revisionsrapporter. Svaren är " +
      "alltid ordagranna citat med land, referens och styckenummer.",
    banner:
      "Sökningen hittar var ett ämne behandlas, aldrig vad som " +
      "konstaterats. Läs alltid citatet.",
    examplesHeading: "Exempelfrågor",
    similarity: "likhet",
    noAnswers:
      "Inget stycke över likhetströskeln. Ett tomt svar är ett tomt " +
      "svar, aldrig en gissning.",
    search: {
      label: "Sök i korpusen",
      button: "Sök",
      searching: "Söker",
      error: "Söket kunde inte nås. Exempelfrågorna nedan fungerar ändå.",
      note:
        "Livesöket öppnar tillsammans med sajten. Exempelsvaren nedan är " +
        "förberäknade genom samma kod som livesöket kör.",
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
  handlingar: {
    title: "Handlingar",
    lead:
      "Vad som begärts ut, vad som lämnats ut, vad som inte lämnats ut " +
      "och varför. Dokumenten innehåller personuppgifter och publiceras " +
      "inte; förteckningen gör leveranserna verifierbara utan dem.",
    deliveries: {
      heading: "Levererade handlingar",
      note:
        "Varje mottagen fil registreras med sin sha256-kontrollsumma i " +
        "ett manifest som är beständigt: en post kan läggas till men " +
        "aldrig ändras.",
      filesWord: "filer",
      headers: { file: "Fil", bytes: "Byte", sha256: "sha256" },
    },
  },
  data: {
    title: "Data",
    lead:
      "Nedladdningsbara aggregat och schemadokumentation. Granskningsbar " +
      "utifrån betyder att vem som helst kan räkna om.",
  },
  building: "Sidan är under uppbyggnad.",
};
