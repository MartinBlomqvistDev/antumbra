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

# Who moved. An event name that is in neither set is a hole in this mapping,
# and the report says so rather than guessing a side.
OURS = frozenset(
    {
        "avsändning",
        "avsmalningssvar",
        "avstående",
        "avstående från överklagande",
        "överklagande",
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
    }
)
THEIRS = frozenset(
    {
        "arbetsbesked",
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
        # The authority passing an appeal on to the court after finding it in
        # time. It ends the authority's own part of the appeal and asks
        # nothing of us, so it starts no clock here.
        "överlämnande till kammarrätten",
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
        "tillämpningsnot skriven",
    }
)

# Aggregate rows describe a batch or the project itself, not one request.
# "länsstyrelserna" is the same thing under a word invented on 5 September 2026
# for seven rows about the conditions layer. The log is append-only, so the word
# stays and is read here; new internal rows use "samtliga".
NOT_A_REQUEST = frozenset({"flera", "länsstyrelserna", "samtliga"})

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


def unmapped(rows: list[dict]) -> set[str]:
    """Event names that belong to no side, which the report must not guess."""
    known = OURS | THEIRS | INTERNAL
    return {row["handelse"] for row in rows if row["handelse"] not in known}


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
        if row["myndighet"] in NOT_A_REQUEST:
            continue
        for klass in row["begaran"].split("+"):
            tracks.setdefault((row["myndighet"], klass), []).append(row)
    return {
        key: events
        for key, events in tracks.items()
        if any(event["handelse"] not in INTERNAL for event in events)
    }


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
    delivered = bool(deliveries)
    partial = any(PARTIAL_MARK in (e.get("notering") or "").lower() for e in deliveries)
    fee_stopped = any("avgiftsstoppad" in (e.get("notering") or "") for e in events)
    decision_closed = any(
        e["handelse"] in DECISION_CLOSERS for e in events if e["handelse"] in THEIRS
    )
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
    appeal = appeal_deadline(last_theirs["handelse"])
    appeal_closed = any(
        e["handelse"] in APPEAL_CLOSERS
        and (e["datum"], e["klockslag"])
        > (last_theirs["datum"], last_theirs["klockslag"])
        for e in events
    )
    deadline = answer_deadline(last_theirs["handelse"])
    if appeal and not appeal_closed:
        days, step = appeal
        item["waiting_on"] = "dig"
        item["step"] = step
        item["due"] = date.fromisoformat(last_theirs["datum"]) + timedelta(days=days)
        item["note"] = "avslagsbeslut, pröva P9:s kriterier"
        # The decision is what requires the move, so it is what the line
        # names, however many acknowledgements have been logged since.
        item["last_event"] = last_theirs
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
    return lines


def main() -> int:
    """Print the report for today."""
    rows = load()
    for line in report(rows, date.today()):
        print(line)
    return 1 if unmapped(rows) else 0


if __name__ == "__main__":
    sys.exit(main())
