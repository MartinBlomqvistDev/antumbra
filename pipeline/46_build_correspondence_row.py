"""Build a register payload from a saved raw reply.

The mechanical fields come out of the raw answer through step 44: the Swedish
time, the letter's own text, and what was taken out of it. What is passed in is
the judgement: the authority, the role the letter signs with, the attachments
and any remark only a reader can make.

Run as: python pipeline/46_build_correspondence_row.py <id> <myndighet>
    <roll|-> <avsandare> --ut <payload.json> [--bilagor ...] [--anmarkning ...]
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
    """Write the payload for one message."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("meddelande", help="the message id")
    parser.add_argument("myndighet", help="the authority, as the register writes it")
    parser.add_argument("roll", help="the role the letter signs with, or - for none")
    parser.add_argument("avsandare", help="funktionsbrevlåda or namngiven tjänsteman")
    parser.add_argument(
        "--ut", required=True, type=Path, help="where to write the payload"
    )
    parser.add_argument("--bilagor", default="-", help="the attachments, or - for none")
    parser.add_argument("--anmarkning", default="", help="what only a reader can say")
    args = parser.parse_args()
    mid, myndighet, roll, avsandare = (
        args.meddelande,
        args.myndighet,
        args.roll,
        args.avsandare,
    )
    bilagor = args.bilagor if args.bilagor != "-" else None
    anmarkning = args.anmarkning

    raw = json.loads((RAW / f"{mid}.json").read_text("utf-8"))
    datum, klockslag = step.swedish_time(raw["date"])
    judgement = step.load_judgements().get(mid)
    text, taken = step.normalise(raw.get("plaintextBody") or "", judgement, mid)

    utelamnat = "; ".join(taken) if taken else ""
    if anmarkning:
        utelamnat = f"{utelamnat}. {anmarkning}" if utelamnat else anmarkning

    row = {
        "datum": datum,
        "klockslag": klockslag,
        "myndighet": myndighet,
        "avsandare": avsandare,
        "roll": None if roll == "-" else roll,
        "amnesrad": raw["subject"],
        "meddelande": mid,
        "text": text,
        "bilagor": bilagor,
        "utelamnat": utelamnat,
    }
    args.ut.write_text(json.dumps([row], ensure_ascii=False), encoding="utf-8")
    print(f"{mid} {datum} {klockslag} | {len(text)} tecken | utelamnat: {taken}")
    print(f"  text slutar: ...{text[-70:]!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
