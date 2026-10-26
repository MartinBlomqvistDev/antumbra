"""The address line each authority is written to, read out of the sent mail.

Shared by every step that writes a letter. Step 37 kept the map to itself while
it was the only sender; step 40 writes the P12 letters to the same recipients,
and a second copy of the same map is what went wrong on 1 October 2026, when the
packet builder's own list of what ends a request had drifted from the measure's.
"""

# The county in the file name, and the authority exactly as the address line
# of 3 August 2026 wrote it. The two differ: the protocol log calls the track
# "Länsstyrelsen i Blekinge", the letter that went out said "Länsstyrelsen i
# Blekinge län". Decision 9 makes the letters fixed and alike, so a later
# letter in the same correspondence cannot address the authority by another
# name than the first one did, and the quoted request must carry the line the
# recipient actually holds. Every line below is read out of the sent mail.
# Kalmar's line was read from the copy quoted inside the reply of 4 August,
# because the 3 August message was thought to be missing from the mailbox. It
# is not: it is message 19fc6a3d539a4541, the first in thread 19fc690073e9ee8d,
# found on 26 October 2026 while the outgoing register was being built. A search
# listing shows at most five messages per thread, and the earliest drop out of a
# longer thread; the claim of a gap rested on such a listing rather than on
# get_thread. The line itself was right, and is now read from the message.
COUNTIES = {
    "Blekinge": "Länsstyrelsen i Blekinge län",
    "Dalarna": "Länsstyrelsen i Dalarnas län",
    "Gotland": "Länsstyrelsen i Gotlands län",
    "Gävleborg": "Länsstyrelsen i Gävleborgs län",
    "Halland": "Länsstyrelsen i Hallands län",
    "Jämtland": "Länsstyrelsen i Jämtlands län",
    "Jönköping": "Länsstyrelsen i Jönköpings län",
    "Kalmar": "Länsstyrelsen i Kalmar län",
    "Kronoberg": "Länsstyrelsen i Kronobergs län",
    "Norrbotten": "Länsstyrelsen i Norrbottens län",
    "Skåne": "Länsstyrelsen i Skåne län",
    "Stockholm": "Länsstyrelsen i Stockholms län",
    "Södermanland": "Länsstyrelsen i Södermanlands län",
    "Uppsala": "Länsstyrelsen i Uppsala län",
    "Värmland": "Länsstyrelsen i Värmlands län",
    "Västerbotten": "Länsstyrelsen i Västerbottens län",
    "Västernorrland": "Länsstyrelsen i Västernorrlands län",
    "Västmanland": "Länsstyrelsen i Västmanlands län",
    "Västra Götaland": "Länsstyrelsen i Västra Götalands län",
    "Örebro": "Länsstyrelsen i Örebro län",
    "Östergötland": "Länsstyrelsen i Östergötlands län",
}


# Jordbruksverket is not a county board and was never sent P11's denominator
# question, so it is kept out of COUNTIES, which steps iterate to reach the 21.
# Its own line is read out of the request of 3 August 2026, 08:03, message
# 19fc6a6265841e53, which opens "Till Statens jordbruksverk".
OTHERS = {"Jordbruksverket": "Statens jordbruksverk"}


def address(myndighet: str) -> str:
    """The authority as the first letter addressed it, from its track name."""
    county = myndighet.removeprefix("Länsstyrelsen i ")
    if county in COUNTIES:
        return COUNTIES[county]
    if myndighet in OTHERS:
        return OTHERS[myndighet]
    raise SystemExit(f"okänd myndighet i loggen: {myndighet}")
