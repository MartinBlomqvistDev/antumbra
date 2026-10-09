"""Write the register's progress into docs/VERIFIERAT.md from the files.

The invariant in tests/ reads the same sentence and fails when the prose and
the files disagree, so the number is never typed by hand.

Run as: python uppdatera_talet.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    """Set the count in the docs to what the two files hold."""
    register = [
        json.loads(line)
        for line in (ROOT / "data" / "korrespondens.jsonl")
        .read_text("utf-8")
        .splitlines()
        if line.strip()
    ]
    done = {row["meddelande"] for row in register}
    done |= {
        item["meddelande"] for row in register for item in row.get("forekomster", [])
    }
    total = sum(
        1
        for line in (ROOT / "data" / "korrespondens_forteckning.jsonl")
        .read_text("utf-8")
        .splitlines()
        if line.strip() and json.loads(line)["inom_avgransningen"]
    )

    path = ROOT / "docs" / "VERIFIERAT.md"
    text = path.read_text("utf-8")
    # The sentence is wrapped in the prose, so the pattern allows a line break
    # wherever a space stands and only the numbers are written back. Three
    # numbers are kept true: the messages carried, the messages the inventory
    # knows, and the rows they lie on, since a standing autoreply is one row
    # with its repeats as occurrences.
    pattern = (
        r"(Registret\s+bär\s+)\d+( av de )\d+"
        r"( inkomna meddelanden\s+förteckningen\s+känner, alltså )\d+"
        r"( kvar, på\s+)\d+( rader)"
    )
    new, count = re.subn(
        pattern,
        lambda m: (
            f"{m.group(1)}{len(done)}{m.group(2)}{total}{m.group(3)}"
            f"{total - len(done)}{m.group(4)}{len(register)}{m.group(5)}"
        ),
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit("hittade inte meningen om hur langt registret ar kommet")
    path.write_bytes(new.encode("utf-8"))
    print(f"{len(done)} av {total}, {total - len(done)} kvar, {len(register)} rader")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
