"""Append rows to data/korrespondens.jsonl from a payload file.

Run as: python pipeline/45_append_correspondence.py <payload.json>

A payload row is either a message, which becomes its own row, or an occurrence
of a mailbox's standing automatic reply, written as {"samma_som": "<message id
of the row that carries the text>", ...}, which is appended to that row instead
of repeating the text.

Every row is screened before it is written: a named sender must carry a role, a
personal address must never appear, and the row must say what it leaves out.
"""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "korrespondens.jsonl"

FIELDS = (
    "datum",
    "klockslag",
    "myndighet",
    "avsandare",
    "roll",
    "amnesrad",
    "meddelande",
    "text",
    "bilagor",
    "utelamnat",
)
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+\.\w{2,}")
FUNCTIONAL = re.compile(
    r"^(blekinge|dalarna|gotland|gavleborg|halland|jamtland|jonkoping|kalmar|"
    r"kronoberg|norrbotten|skane|stockholm|sodermanland|uppsala|varmland|"
    r"vasterbotten|vasternorrland|vastmanland|vastragotaland|orebro|ostergotland|"
    r"lansstyrelsen\.\w+|djurskydd\.[\w.]+|arkiv\.\w+|arkivfragor\.\w+|"
    r"expediering\.\w+|u-rb-djurskydd|no_reply)@lansstyrelsen\.se$",
    re.IGNORECASE,
)
OTHER_OK = {
    "jordbruksverket@jordbruksverket.se",
    "djurvalfard@jordbruksverket.se",
    "cm.blomqvist@gmail.com",
    "kammarrattenisundsvall@dom.se",
    "kammarratten.goteborg@dom.se",
    "kammarrattenijonkoping@dom.se",
    "avd3.kst@dom.se",
    "noreply@dom.se",
}


def read_rows() -> list[dict]:
    """The register as it stands."""
    if not OUT.exists():
        return []
    return [
        json.loads(line) for line in OUT.read_text("utf-8").splitlines() if line.strip()
    ]


def write_rows(rows: list[dict]) -> None:
    """The register, one JSON object per line, LF endings."""
    body = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
    OUT.write_bytes((body + "\n").encode("utf-8"))


def screen(row: dict) -> None:
    """Fail loudly on anything a published register must not carry."""
    for field in FIELDS:
        if field not in row:
            raise SystemExit(f"faltet {field} saknas i {row.get('meddelande')}")
    haystack = (row["text"] or "") + " " + (row["amnesrad"] or "")
    for found in EMAIL.findall(haystack):
        if found.lower() in OTHER_OK or FUNCTIONAL.match(found):
            continue
        raise SystemExit(f"{row['meddelande']}: adressen {found} far inte sta kvar")
    if row["avsandare"] not in ("funktionsbrevlåda", "namngiven tjänsteman"):
        raise SystemExit(
            f"{row['meddelande']}: {row['avsandare']!r} ar inte en av de tva avsandarna"
        )
    if row["avsandare"] == "namngiven tjänsteman" and not row["roll"]:
        raise SystemExit(f"{row['meddelande']}: namngiven avsandare utan roll")
    if not row["utelamnat"]:
        raise SystemExit(f"{row['meddelande']}: raden sager inte vad den utelamnar")


def main() -> int:
    """Write every payload row that is not already in the register."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", type=Path, help="the rows to append")
    args = parser.parse_args()
    payload = json.loads(args.payload.read_text("utf-8"))
    rows = read_rows()
    known = {row["meddelande"] for row in rows}
    known |= {item["meddelande"] for row in rows for item in row.get("forekomster", [])}

    added = 0
    written = 0
    for row in payload:
        if row["meddelande"] in known:
            continue
        if row.get("samma_som"):
            # A repeat is only a repeat when the text is identical character for
            # character. The tool compares it instead of trusting that it was
            # checked: on 8 October 2026 an occurrence was written without its
            # text having been read, and it happened to be right, which is the
            # kind of luck that hides a fault.
            if "text" not in row:
                raise SystemExit(
                    f"{row['meddelande']}: en forekomst maste bara sin egen text, "
                    "sa att verktyget kan jamfora den mot bararens"
                )
            # The text alone proves nothing: it can be copied from the carrier
            # without the message having been fetched, and on 8 October 2026 it
            # was. sizeEstimate comes out of the API answer and cannot be known
            # without fetching, so it is required and stored with the occurrence.
            if not isinstance(row.get("storlek"), int):
                raise SystemExit(
                    f"{row['meddelande']}: en forekomst maste bara sizeEstimate "
                    "ur API-svaret, som bevis pa att meddelandet ar hamtat"
                )
            for existing in rows:
                if existing["meddelande"] == row["samma_som"]:
                    if row["text"] != existing["text"]:
                        raise SystemExit(
                            f"{row['meddelande']}: texten skiljer sig fran "
                            f"{row['samma_som']} och ar alltsa en egen rad"
                        )
                    existing.setdefault("forekomster", []).append(
                        {
                            "datum": row["datum"],
                            "klockslag": row["klockslag"],
                            "meddelande": row["meddelande"],
                            "amnesrad": row["amnesrad"],
                            "storlek": row["storlek"],
                        }
                    )
                    added += 1
                    break
            else:
                raise SystemExit(f"{row['samma_som']} finns inte i registret")
            continue
        screen(row)
        ordered = {key: row[key] for key in FIELDS}
        ordered["kalla"] = "Gmail, meddelandets plaintext-del"
        rows.append(ordered)
        written += 1

    write_rows(rows)
    print(f"{written} nya rader, {added} forekomster, {len(rows)} totalt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
