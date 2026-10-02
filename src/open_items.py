"""What each request is waiting for, derived from the protocol log alone.

The log records events. This module turns them into obligations: for every
request, who moved last, whether the protocol puts the next move on us, and
when that move is due. It exists because a list carried in someone's head
fails silently, and because an event that was never logged is invisible to
any check that starts from the log.

That last point is the limitation to keep in view: this reads the log, not the
mailbox. It answers "given what is logged, what is open", never "is the log
complete". Completeness is established by walking the authority's threads and
comparing them against the log, which is a human step.

Deadlines follow docs/BEGARANMALL.md: P2 at day 5 and P3 at day 10 for a
request with no contact at all, P4 within one working day of a clarifying
question, P5 within three working days of a fee notice, and P10 at day 40 for
everything still open. Tillämpningsnot 4 made P8 selective, so a masked
delivery is reported as information and never as a due item. Tillämpningsnot 5
turns on conduct that cannot be read off an event name, so a general policy
document sent instead of a decision is flagged for judgement, not scheduled.

Tillämpningsnot 3 also decides when a request is finished, and a request whose
decision has been asked for and not answered is not: delivery of the part that
could be delivered does not settle the part that was refused.

Working days are Monday to Friday. Public holidays are not modelled, which
matters from Christmas onwards and not at all in August; the effect is that a
deadline can be reported one or two days earlier than it truly falls.

Usage:
    python src/open_items.py
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "data" / "protokoll_logg.jsonl"

DAY_ZERO = date(2026, 8, 3)
PUBLICATION_DAY = 40
# What the protocol and the ADRs tell the project to do, and has not been
# done. The log records what happened; this records what was promised. It
# exists because KR Jönköping 549-19 was to be requested "samtidigt" with the
# Sundsvall ruling on 2 August 2026, the instruction was rewritten to "before
# publication" the next day without the deferral being declared, and nothing
# surfaced it for 36 days. The report shows what authorities owe us; without
# this it shows nothing of what we owe ourselves.
PLEDGES = LOG.parent / "atagande.jsonl"
# The decisions we have appealed. The register carries the case number the
# court gave it, so the running cases are derivable and do not have to be
# remembered.
DECISIONS = LOG.parent / "beslut.jsonl"

# A court that uses förenklad delgivning deems a document served two weeks
# after it was sent, whether or not it was read, so a letter nobody opens still
# starts a deadline. Kammarrätten i Stockholm's leaflet in case 6901-26 says it
# in those words and instructs the recipient to check the post "minst varannan
# vecka". The report cannot read the mailbox, so it watches the one thing it
# can: when a sweep of it was last logged. The rule exists because Länsstyrelsen
# i Gotlands decision of 28 August 2026 sat unread for 25 days and only surfaced
# through the authority's reminder, which a court under förenklad delgivning
# would never have sent.
SWEEP_EVENT = "brevlådan genomgången"
SWEEP_DAYS = 14

# Who moved. An event name that is in neither set is a hole in this mapping,
# and the report says so rather than guessing a side.
OURS = frozenset(
    {
        "avsändning",
        # Our answer to an authority's question about the denominator. It sits
        # on the P11 track and not on a request, since note 7 keeps the two
        # apart, but it is still ours and must be placeable.
        "svar på förtydligandefråga om nämnaren",
        "avsmalningssvar",
        "avstående",
        "avstående från överklagande",
        "överklagande",
        # Our written comment in a pending case, filed on the court's own
        # invitation. The court's deadline is not a protocol deadline and is
        # tracked in data/atagande.jsonl.
        "yttrande till kammarrätten",
        "beslutsbegäran",
        "beslutsbegäran och fråga om uttagets fullständighet",
        "beslutsbegäran upprepad",
        "delgivningskvitto",
        "förfrågan om beskedets innebörd",
        "förfrågan om fjäderfätäckning",
        "förfrågan om länsuppdelning",
        "förfrågan om elektroniskt utlämnande",
        "förnyad begäran om avgiftsbeslut",
        "förtydligande",
        "påminnelse",
        "svar på förtydligande",
        "svar på förtydligandefråga",
        "svar på förtydligandefråga och accept av elektronisk leverans",
        # P11's denominator question, sent on day 40 to all 21 county boards.
        # It is not one of the 43 requests and carries no deadline of its own;
        # tillämpningsnot 7 gives it one reminder and then records the
        # denominator as missing.
        "nämnarfråga",
        # A request for a decision that lapsed on a condition we set in writing
        # ourselves. Kalmar B is the case: on 13 August 2026 the letter said the
        # request for a fee decision lapses if the documents are released
        # electronically without a fee, and they were, an hour and fifty-five
        # minutes later. It ends the decision track without a decision.
        "beslutsbegäran förfallen",
        # A letter that withdraws an incorrect statement in an earlier letter of
        # ours. It asks the authority for nothing and starts no clock.
        "rättelse",
        # Our answer to an authority that says the documents were already sent.
        "svar på besked om tidigare leverans",
    }
)
THEIRS = frozenset(
    {
        "arbetsbesked",
        # An authority's question about the denominator, kept apart from a P4
        # question about the requests themselves.
        "förtydligandefråga om nämnaren",
        "autosvar",
        "avgift kvarstår",
        "avgiftsbesked",
        "avgiftsbesked och erbjudande om maskad elektronisk leverans",
        "avgiftsbesked och förtydligande",
        # A plain statement of what the register can and cannot produce,
        # with no question attached, so no P4 clock starts.
        "besked om uttagets omfattning",
        "besked om uttagets omfattning och förtydligandefråga",
        "avgiftsbeslut mottaget",
        "avgiftsbeslut vägrat",
        "besked",
        "besked om att dimension 1 inte kan tas fram",
        "delvis avslag och kompletterande leverans",
        "diarieföringsbesked",
        "förnyat avgiftserbjudande",
        "förtydligandefråga",
        "förtydligandefråga och avgiftsbesked",
        "förtydligandefråga upprepad",
        "leverans",
        "manuellt svar",
        # The court registering an appeal and giving it a case number. The
        # sender is the kammarrätt, not the county, but the event belongs to
        # the request whose decision was appealed, and nothing is asked of us.
        "målregistrering i kammarrätten",
        # The court sending in what it has received and offering a chance to
        # comment. It does ask something of us, but not on any protocol clock:
        # the deadline is the court's own and is tracked in data/atagande.jsonl
        # with the other obligations the project owes rather than owes to it.
        "underrättelse från kammarrätten",
        # The authority passing an appeal on to the court after finding it in
        # time. It ends the authority's own part of the appeal and asks
        # nothing of us, so it starts no clock here.
        "överlämnande till kammarrätten",
        # The authority asking again for a delgivningskvitto it has not
        # had. It puts the receipt on us, but on the authority's own date
        # and not on any protocol clock.
        "påminnelse om delgivning",
        # An authority answering that the documents were already sent, in
        # response to P10's last reminder. It asks nothing on a protocol clock.
        "besked om tidigare leverans",
        # An answer to P11's denominator question.
        "svar på nämnarfrågan",
        "mottagningsbesked",
        # A delivery that replaces a defective one. Distinct from "leverans"
        # because it does not start the collection, it repairs it, and the
        # distinction has to survive in the published log.
        "rättad leverans",
        # A written, appealable refusal, which is what P8 asks for. It ends
        # the decision track and starts P9's own clock.
        "avslagsbeslut mottaget",
        # The same thing where the authority also released more: it ends the
        # decision track and starts P9's clock exactly as a plain refusal does.
        "delvis avslagsbeslut mottaget",
        "riktlinje bifogad",
        # The authority explaining how its own extract is built, here that a
        # row is one animal keeper and not one control. It answers nothing that
        # was asked, so it closes no open question, but it is their move.
        "svar om uttagets uppbyggnad",
        "taxebeslut bifogat",
    }
)
INTERNAL = frozenset(
    {
        "kompletterande leverans arkiverad",
        "leverans arkiverad",
        # Our own finding that nothing is outstanding on a track, written with
        # the authority's own words and what lies in data/leveranser.
        "leverans fullgjord",
        # A test condition written down before its outcome is known, so that
        # the bar cannot be moved to meet the result. "förregistrering" is the
        # same event under a shorter name, used from 5 September 2026; the
        # longer one stays because rows already carry it and the log is never
        # rewritten.
        "förregistrerat prövningsvillkor",
        "förregistrering",
        # What such a condition resolved to, kept apart from the condition
        # itself so that the two can be read against each other.
        "utfall",
        # Personal data found inside the repository, and what was done about
        # it. Internal, since no authority owes anything on it.
        "personuppgift",
        "protokollavvikelse",
        # P0b's flag, recorded as an event so that it is readable by field and
        # not only as prose inside a notering. It marks an authority that
        # handles both requests as one; the response time is then attributed to
        # both, while the class measures stay per document class.
        "sammanslagning enligt P0b",
        # A full pass through the mailbox, thread by thread, logged so that the
        # interval between passes is visible. Internal: nothing is owed to
        # anyone by it.
        SWEEP_EVENT,
        # An open legal question in BEGARANMALL section 11 read against the
        # statute itself and written into docs/VERIFIERAT.md. Internal: it
        # closes a pledge of ours and asks nothing of any authority.
        "rättsfråga verifierad",
        # A letter built and checked but not yet sent, logged so that the day
        # the text was fixed is readable apart from the day it went out.
        # Internal: nothing has reached an authority yet.
        "förberedelse",
        "tillämpningsnot skriven",
    }
)

# Aggregate rows describe a batch or the project itself, not one request.
# "länsstyrelserna" is the same thing under a word invented on 5 September 2026
# for seven rows about the conditions layer. The log is append-only, so the word
# stays and is read here; new internal rows use "samtliga".
# The last two are my own slip of 28 September 2026: the class belongs in
# begaran and the aggregate word alone in myndighet, and two internal rows
# carry it the other way. The log is append-only, so the reader absorbs the
# spelling instead of the rows being rewritten.
NOT_A_REQUEST = frozenset(
    {"flera", "länsstyrelserna", "samtliga", "samtliga B", "samtliga A+B"}
)

# An authority event that puts the next move on us, with its deadline in
# working days. Longest key first, so a compound name matches its own rule.
ANSWER_DUE = (
    ("besked om uttagets omfattning och förtydligandefråga", 1, "P4"),
    ("förtydligandefråga och avgiftsbesked", 1, "P4"),
    ("avgiftsbesked och förtydligande", 1, "P4"),
    ("förtydligandefråga upprepad", 1, "P4"),
    ("förtydligandefråga", 1, "P4"),
    ("avgiftsbesked och erbjudande om maskad elektronisk leverans", 3, "P5"),
    ("avgiftsbesked", 3, "P5"),
    ("avgift kvarstår", 3, "P5"),
    ("förnyat avgiftserbjudande", 3, "P5"),
)

# Conduct that tillämpningsnot 5 covers. Whether the note applies depends on
# what came before and on whether a jurist has the question, so this is a
# prompt for judgement rather than a deadline.
JUDGEMENT = frozenset({"riktlinje bifogad", "taxebeslut bifogat"})

# Events that end the decision track behind a declined request, so that
# tillämpningsnot 3 counts it as finished rather than as still running.
DECISION_CLOSERS = frozenset(
    {
        "avgiftsbeslut mottaget",
        "avgiftsbeslut vägrat",
        "avslagsbeslut mottaget",
        "delvis avslagsbeslut mottaget",
        "beslutsbegäran förfallen",
    }
)

# P9 runs on calendar days, not working days: the appeal is sent within 14
# calendar days of delfåendet although the statutory limit is three weeks.
# Kept apart from ANSWER_DUE so that neither rule can borrow the other's
# clock, which would move a deadline without anyone editing it.
APPEAL_DUE = (
    ("avslagsbeslut mottaget", 14, "P9"),
    ("delvis avslagsbeslut mottaget", 14, "P9"),
)

# What actually ends an appeal window. Acknowledging service does not: the
# authority asks for a receipt, the receipt is our event, and treating any
# event of ours as an answer made the P9 deadline disappear from the report
# the moment the receipt was logged. Only appealing, or deciding not to,
# closes the window.
APPEAL_CLOSERS = frozenset({"överklagande", "avstående från överklagande"})

# Asking the authority to try the question and issue an appealable decision
# opens a track of its own. Tillämpningsnot 3 requires every request to have
# reached a slutstatus before publication, and a request whose decision is
# still owed has not. Delivery does not settle it: a sammanställning can be
# handed over in part while the refused part is under decision, which is
# exactly where Jordbruksverket C stood on 2026-08-17.
DECISION_REQUESTS = frozenset(
    {
        "beslutsbegäran",
        "beslutsbegäran och fråga om uttagets fullständighet",
        "beslutsbegäran upprepad",
        "förnyad begäran om avgiftsbeslut",
    }
)

# A delivery whose own note says more is coming is not a finished delivery.
PARTIAL_MARK = "inte avslutad"

# What lifts that mark again. The log is append-only, so a row written while
# more was expected keeps its wording for ever, and the arrival of the rest is
# a later row. Without this the flag could only ever be set, which would make
# a closed collection unreadable from the instrument: on 30 September 2026 two
# of Södermanland's tracks and Västmanland's class A still counted as open
# although every document was on disk. The event also carries the case where
# an authority merged A and B under P0b, so one class holds every delivery row
# and the other has none of its own.
DELIVERY_COMPLETED = frozenset({"leverans fullgjord"})


def working_days_between(start: date, end: date) -> int:
    """Working days after start up to and including end."""
    if end <= start:
        return 0
    days = 0
    current = start
    while current < end:
        current += timedelta(days=1)
        if current.weekday() < 5:
            days += 1
    return days


def add_working_days(start: date, count: int) -> date:
    """The date count working days after start."""
    current = start
    while count:
        current += timedelta(days=1)
        if current.weekday() < 5:
            count -= 1
    return current


def load(path: Path = LOG) -> list[dict]:
    """Every logged event, in logged order."""
    return [json.loads(line) for line in path.read_text("utf-8").splitlines()]


def pledges(path: Path = PLEDGES) -> list[dict]:
    """Every obligation the project has written down for itself."""
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


def unmapped(rows: list[dict]) -> set[str]:
    """Event names that belong to no side, which the report must not guess."""
    known = OURS | THEIRS | INTERNAL
    return {row["handelse"] for row in rows if row["handelse"] not in known}


# P11 is a follow-up question and not one of the 43 requests: tillämpningsnot 7
# says so in as many words, and adds that it carries no deadline of its own.
# Logged under begaran "A+B" its events landed on the request tracks, where they
# reopened requests that were delivered weeks ago and invented a P4 deadline the
# note denies: Halland's question on 29 September and Västerbotten's on
# 30 September each took two finished requests back to "kräver dig", which is
# the very reading that decides when the collection is closed.
P11_EVENTS = frozenset(
    {
        "nämnarfråga",
        "svar på nämnarfrågan",
        "förtydligandefråga om nämnaren",
        "svar på förtydligandefråga om nämnaren",
    }
)

# The two rows written before the event names above existed. The log is
# append-only, so the reader carries the exception rather than the rows being
# rewritten, the same way the malformed aggregate names are absorbed above.
# Each is matched on authority, date and time, so no later row can slip in.
P11_SUPERSEDED = frozenset(
    {
        ("Länsstyrelsen i Halland", "2026-09-29", "09:59"),
        ("Länsstyrelsen i Västerbotten", "2026-09-30", "10:42"),
    }
)


def is_p11(row: dict) -> bool:
    """Whether an event belongs to the denominator question rather than a request."""
    if row["handelse"] in P11_EVENTS:
        return True
    return (row["myndighet"], row["datum"], row["klockslag"]) in P11_SUPERSEDED


def denominator_track(rows: list[dict]) -> dict[str, list[dict]]:
    """The P11 events per authority, kept apart from the 43 requests."""
    track: dict[str, list[dict]] = {}
    for row in rows:
        if row["myndighet"] in NOT_A_REQUEST or not is_p11(row):
            continue
        track.setdefault(row["myndighet"], []).append(row)
    return track


def by_request(rows: list[dict]) -> dict[tuple[str, str], list[dict]]:
    """Events per request, expanding rows that cover more than one class.

    A track whose events are all internal is not a request. Every request opens
    with an avsändning, so nothing real is lost, and without this a row about
    the project's own work builds a request that nobody ever sent: on
    5 September 2026 seven such rows produced a phantom item under a P3 deadline
    19 days overdue, at the top of the list that says what to do next.
    """
    tracks: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        if row["myndighet"] in NOT_A_REQUEST or is_p11(row):
            continue
        for klass in row["begaran"].split("+"):
            tracks.setdefault((row["myndighet"], klass), []).append(row)
    return {
        key: events
        for key, events in tracks.items()
        if any(event["handelse"] not in INTERNAL for event in events)
    }


def decisions(path: Path = DECISIONS) -> list[dict]:
    """The decision register, or an empty list before the first decision."""
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


def running_cases(path: Path = DECISIONS) -> list[dict]:
    """Appealed decisions whose case has a number and no ruling yet.

    A case leaves this list when its row gets an `avgorande_datum`, so the
    report never asks about a case that is over, and a ruling cannot be left
    out of the register without the case staying on the list.
    """
    return [
        row
        for row in decisions(path)
        if row.get("malnummer") and not row.get("avgorande_datum")
    ]


def last_sweep(rows: list[dict]) -> date | None:
    """The date of the most recently logged pass through the mailbox."""
    dates = [row["datum"] for row in rows if row["handelse"] == SWEEP_EVENT]
    return max((date.fromisoformat(d) for d in dates), default=None)


def answer_deadline(handelse: str) -> tuple[int, str] | None:
    """Working days allowed and the protocol step, for an event we must answer."""
    for name, days, step in ANSWER_DUE:
        if handelse == name:
            return days, step
    return None


def appeal_deadline(handelse: str) -> tuple[int, str] | None:
    """Calendar days allowed and the step, for a refusal we may appeal."""
    for name, days, step in APPEAL_DUE:
        if handelse == name:
            return days, step
    return None


def state(events: list[dict], today: date) -> dict:
    """What one request is waiting for."""
    deliveries = [e for e in events if e["handelse"] == "leverans"]
    completed = any(e["handelse"] in DELIVERY_COMPLETED for e in events)
    delivered = bool(deliveries) or completed
    partial = (
        any(PARTIAL_MARK in (e.get("notering") or "").lower() for e in deliveries)
        and not completed
    )
    fee_stopped = any("avgiftsstoppad" in (e.get("notering") or "") for e in events)
    # Not filtered on THEIRS: a decision track also ends when the request for a
    # decision lapses on a condition the applicant set in writing, which is our
    # own event and not theirs.
    decision_closed = any(e["handelse"] in DECISION_CLOSERS for e in events)
    # A decision that has been asked for and not answered leaves the request
    # running, however much of it was delivered.
    asked = [e for e in events if e["handelse"] in DECISION_REQUESTS]
    answered_at = [
        (e["datum"], e["klockslag"])
        for e in events
        if e["handelse"] in DECISION_CLOSERS
    ]
    decision_pending = bool(asked) and not any(
        when > (asked[-1]["datum"], asked[-1]["klockslag"]) for when in answered_at
    )
    contacted = any(
        e["handelse"] in THEIRS and e["handelse"] != "autosvar" for e in events
    )
    theirs = [e for e in events if e["handelse"] in THEIRS]
    ours = [e for e in events if e["handelse"] in OURS]
    substantive = [e for e in events if e["handelse"] not in INTERNAL]
    last_theirs = theirs[-1] if theirs else None
    last_ours = ours[-1] if ours else None

    item: dict = {
        "delivered": delivered and not partial,
        "partial": partial,
        "fee_stopped": fee_stopped,
        # Tillämpningsnot 3: a request is finished when it is delivered in
        # full, or the copies were declined and the decision track has ended.
        "closed": ((delivered and not partial) or (fee_stopped and decision_closed))
        and not decision_pending,
        "decision_pending": decision_pending,
        "last_event": substantive[-1] if substantive else events[-1],
        "waiting_on": "myndigheten",
        "due": None,
        "step": None,
        "note": None,
    }

    if last_theirs is None:
        item["silent_since"] = date.fromisoformat(events[0]["datum"])
        if not contacted:
            day = working_days_between(DAY_ZERO, today)
            item["step"] = "P3" if day >= 10 else "P2"
            item["due"] = add_working_days(DAY_ZERO, 10 if day >= 10 else 5)
            item["waiting_on"] = "dig"
            item["note"] = "ingen kontakt alls för denna begäran"
        return item

    answered = last_ours is not None and (
        (last_ours["datum"], last_ours["klockslag"])
        > (last_theirs["datum"], last_theirs["klockslag"])
    )
    # The appeal clock belongs to the decision, not to whatever the authority
    # happened to send last. A delgivningspåminnelse or an autosvar logged
    # after a refusal would otherwise stand as the last event and silence P9's
    # deadline: Gotland 3287-2026 was received on 28 August 2026, read on
    # 22 September, and the report said the decision had not been issued.
    last_decision = next(
        (e for e in reversed(theirs) if appeal_deadline(e["handelse"])), None
    )
    appeal = appeal_deadline(last_decision["handelse"]) if last_decision else None
    appeal_closed = last_decision is not None and any(
        e["handelse"] in APPEAL_CLOSERS
        and (e["datum"], e["klockslag"])
        > (last_decision["datum"], last_decision["klockslag"])
        for e in events
    )
    deadline = answer_deadline(last_theirs["handelse"])
    if appeal and not appeal_closed:
        days, step = appeal
        item["waiting_on"] = "dig"
        item["step"] = step
        item["due"] = date.fromisoformat(last_decision["datum"]) + timedelta(days=days)
        item["note"] = "avslagsbeslut, pröva P9:s kriterier"
        # The decision is what requires the move, so it is what the line
        # names, however many acknowledgements have been logged since.
        item["last_event"] = last_decision
    elif deadline and not answered:
        days, step = deadline
        item["waiting_on"] = "dig"
        item["step"] = step
        item["due"] = add_working_days(date.fromisoformat(last_theirs["datum"]), days)
    elif last_theirs["handelse"] in JUDGEMENT and not answered:
        item["waiting_on"] = "dig"
        item["note"] = "generellt styrdokument i stället för beslut, bedöm not 5"
    elif last_theirs["handelse"] == "leverans" and "mask" in (
        last_theirs.get("notering") or ""
    ):
        item["note"] = "maskad leverans, P8 tillämpas urvalsvis enligt not 4"

    # A request is not finished while the protocol owes a move on it. P9's
    # appeal window is the only case where a delivered request whose decision
    # has arrived still requires something from us, and a request listed as
    # finished is a request nobody looks at again.
    if item["waiting_on"] == "dig":
        item["closed"] = False

    item["silent_since"] = date.fromisoformat(events[-1]["datum"])
    return item


# Tillämpningsnot 7 for P11: one reminder ten working days after the question,
# and if the answer still fails to come, ten more before the denominator is
# recorded as missing. The note adds that it is never estimated.
P11_REMINDER_DAYS = 10
P11_SILENCE_DAYS = 10


def denominator_lines(rows: list[dict], today: date) -> list[str]:
    """The state of the denominator question, which has no deadline of its own."""
    track = denominator_track(rows)
    if not track:
        return []
    asked = {
        authority: events[0]["datum"]
        for authority, events in track.items()
        if any(e["handelse"] == "nämnarfråga" for e in events)
    }
    answered = {
        authority
        for authority, events in track.items()
        if any(e["handelse"] == "svar på nämnarfrågan" for e in events)
    }
    ours = {
        authority
        for authority, events in track.items()
        if events[-1]["handelse"] in {"förtydligandefråga om nämnaren"}
        or (authority, events[-1]["datum"], events[-1]["klockslag"]) in P11_SUPERSEDED
    }
    outstanding = sorted(
        authority.replace("Länsstyrelsen i ", "")
        for authority in asked
        if authority not in answered and authority not in ours
    )
    lines = ["", f"NÄMNAREN, P11 ({len(answered)} av {len(asked)} svar inne)"]
    if ours:
        for authority in sorted(ours):
            lines.append(
                f"  {authority.replace('Länsstyrelsen i ', '')}: frågar tillbaka, "
                "svaret följer tillämpningsnot 9"
            )
    if outstanding:
        first = min(asked.values())
        due = add_working_days(date.fromisoformat(first), P11_REMINDER_DAYS)
        missing = add_working_days(due, P11_SILENCE_DAYS)
        lines.append(f"  utan svar ({len(outstanding)}): {', '.join(outstanding)}")
        lines.append(
            f"  påminnelse tidigast {due.isoformat()}, saknad nämnare "
            f"{missing.isoformat()}. Frågan saknar frist enligt not 7 och "
            "skjuter inte upp publiceringen."
        )
    return lines


def report(rows: list[dict], today: date) -> list[str]:
    """The report, most urgent first."""
    lines: list[str] = []
    holes = unmapped(rows)
    if holes:
        lines.append(
            f"OKÄNDA HÄNDELSETYPER, sidan går inte att avgöra: {sorted(holes)}"
        )
        lines.append("")

    tracks = by_request(rows)
    items = {key: state(events, today) for key, events in sorted(tracks.items())}
    day = working_days_between(DAY_ZERO, today)
    publication = add_working_days(DAY_ZERO, PUBLICATION_DAY)
    lines.append(
        f"Dag {day} av {PUBLICATION_DAY}. {len(tracks)} begäranden, "
        f"{sum(1 for i in items.values() if i['closed'])} avslutade enligt not 3, "
        f"{sum(1 for i in items.values() if i['partial'])} delleveranser, "
        f"{sum(1 for i in items.values() if i['fee_stopped'] and not i['closed'])} "
        f"avgiftsstoppade. "
        f"Publiceringsgräns {publication.isoformat()}."
    )

    lines.extend(denominator_lines(rows, today))

    cases = running_cases()
    if cases:
        swept = last_sweep(rows)
        since = (today - swept).days if swept else None
        lines.append("")
        if since is None:
            lines.append(
                f"BREVLÅDAN: ingen genomgång är loggad, och {len(cases)} mål löper "
                "under förenklad delgivning. GÖR EN GENOMGÅNG OCH LOGGA DEN."
            )
        elif since > SWEEP_DAYS:
            lines.append(
                f"BREVLÅDAN: senast genomgången {swept.isoformat()}, {since} dagar "
                f"sedan, alltså över {SWEEP_DAYS}. GÖR EN GENOMGÅNG NU: en handling "
                "i ett mål är delgiven två veckor efter att domstolen skickat den, "
                "oavsett om den lästs."
            )
        else:
            nxt = (swept + timedelta(days=SWEEP_DAYS)).isoformat()
            lines.append(
                f"BREVLÅDAN: senast genomgången {swept.isoformat()}, {since} dagar "
                f"sedan. Nästa senast {nxt}."
            )
        for row in sorted(cases, key=lambda r: r["malnummer"]):
            court = row.get("instans_dit_det_stalldes") or "?"
            lines.append(
                f"  mål {row['malnummer']} i {court}, {row['myndighet']} "
                f"{row['klass']}, dnr {row['diarienummer']}"
            )

    due = sorted(
        ((key, i) for key, i in items.items() if i["waiting_on"] == "dig"),
        key=lambda pair: (pair[1]["due"] or date.max, pair[0]),
    )
    lines.append("")
    lines.append(f"KRÄVER DIG ({len(due)})")
    if not due:
        lines.append("  inget")
    for (authority, klass), item in due:
        if item["due"]:
            late = (today - item["due"]).days
            when = f"frist {item['due'].isoformat()}"
            when += f", {late} dagar sen" if late > 0 else ""
        else:
            when = item["note"] or ""
        lines.append(
            f"  {authority} {klass}: {item['last_event']['handelse']} "
            f"{item['last_event']['datum']} ({item['step'] or '-'}) {when}"
        )

    waiting = [
        (key, i)
        for key, i in items.items()
        if i["waiting_on"] == "myndigheten" and not i["closed"]
    ]
    lines.append("")
    lines.append(f"VÄNTAR PÅ MYNDIGHETEN ({len(waiting)})")
    for (authority, klass), item in sorted(
        waiting, key=lambda pair: pair[1]["silent_since"]
    ):
        silence = working_days_between(item["silent_since"], today)
        quiet = "i dag" if silence == 0 else f"tyst {silence} arbetsdag"
        if silence > 1:
            quiet += "ar"
        notes = [n for n in (item["note"],) if n]
        if item["decision_pending"]:
            notes.append("begärt beslut inte meddelat, inte slutstatus enligt not 3")
        flag = f"  [{'; '.join(notes)}]" if notes else ""
        lines.append(
            f"  {authority} {klass}: {item['last_event']['handelse']} "
            f"{item['last_event']['datum']}, {quiet}{flag}"
        )

    delivered = [key for key, i in items.items() if i["closed"]]
    lines.append("")
    lines.append(f"AVSLUTADE ({len(delivered)})")
    lines.append(
        "  "
        + ", ".join(f"{a.replace('Länsstyrelsen i ', '')} {k}" for a, k in delivered)
    )

    own = [p for p in pledges() if p["status"] != "gjort"]
    dated = [p for p in own if p.get("frist")]
    open_now = [p for p in own if p["status"] == "öppet" and not p.get("frist")]
    waiting = [p for p in own if p["status"] == "väntar" and not p.get("frist")]
    lines.append("")
    lines.append(f"EGNA ÅTAGANDEN ({len(own)})")
    # A pledge with a deadline is not a pledge any more, it is a deadline, so it
    # is printed first and with the days left.
    for pledge in sorted(dated, key=lambda p: p["frist"]):
        left = (date.fromisoformat(pledge["frist"]) - today).days
        lines.append(f"  FRIST {pledge['frist']}, om {left} dagar")
        lines.append(f"      {pledge['atagande']}")
        lines.append(f"      {pledge['kalla']}")
    for pledge in sorted(open_now, key=lambda p: p["oppnat"]):
        age = (today - date.fromisoformat(pledge["oppnat"])).days
        lines.append(f"  {pledge['atagande']}")
        lines.append(
            f"      {pledge['kalla']}, öppet sedan {pledge['oppnat']}, {age} dagar"
        )
    for pledge in sorted(waiting, key=lambda p: p["oppnat"]):
        lines.append(f"  [väntar] {pledge['atagande']}")
        lines.append(f"      {pledge['kalla']}")
    return lines


def main() -> int:
    """Print the report for today."""
    rows = load()
    for line in report(rows, date.today()):
        print(line)
    return 1 if unmapped(rows) else 0


if __name__ == "__main__":
    sys.exit(main())
