"""Save a raw reply and, if its text matches a carrier, write an occurrence payload.

A standing automatic reply is written once and its repeats are appended to that
row. This tool does the mechanical half: it saves the raw answer, runs step 44
over it, and looks for a row from the same authority whose text is identical
character for character. It never guesses: no match means the message needs its
own row, and the tool says so.

Run as: python pipeline/47_append_standing_autoreply.py <raw.json> <myndighet>
    --ut <payload.json>
"""

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "korrespondens_raw"

spec = importlib.util.spec_from_file_location(
    "step44", Path(__file__).with_name("44_build_correspondence.py")
)
step = importlib.util.module_from_spec(spec)
spec.loader.exec_module(step)


def main() -> int:
    """Save the raw answer and write an occurrence payload when one fits."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rasvar", type=Path, help="the saved API answer")
    parser.add_argument("myndighet", help="the authority, as the register writes it")
    parser.add_argument(
        "--ut", required=True, type=Path, help="where to write the payload"
    )
    args = parser.parse_args()
    raw = json.loads(args.rasvar.read_text("utf-8"))
    myndighet = args.myndighet
    (RAW / f"{raw['id']}.json").write_text(
        json.dumps(raw, ensure_ascii=False), encoding="utf-8"
    )
    text, taken = step.normalise(
        raw["plaintextBody"], step.load_judgements().get(raw["id"]), raw["id"]
    )
    datum, klockslag = step.swedish_time(raw["date"])
    rows = [
        json.loads(line)
        for line in (ROOT / "data" / "korrespondens.jsonl")
        .read_text("utf-8")
        .splitlines()
        if line
    ]
    carriers = [
        row for row in rows if row["myndighet"] == myndighet and row["text"] == text
    ]
    print(f"{raw['id']} {datum} {klockslag} | {len(text)} tecken | utelamnat: {taken}")
    if not carriers:
        print("  ingen barare med identisk text; raden maste skrivas for sig")
        return 1
    carrier = carriers[0]
    args.ut.write_text(
        json.dumps(
            [
                {
                    "samma_som": carrier["meddelande"],
                    "datum": datum,
                    "klockslag": klockslag,
                    "meddelande": raw["id"],
                    "amnesrad": raw["subject"],
                    "storlek": raw["sizeEstimate"],
                    "text": text,
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(
        f"  forekomst av {carrier['meddelande']} "
        f"{carrier['datum']} {carrier['klockslag']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
