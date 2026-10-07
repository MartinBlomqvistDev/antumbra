"""Guards for invariants that would otherwise break silently.

Three things can drift without anyone noticing: the generated schema module
against its source document, the figures quoted in the documentation against
the data they describe, and the rule that no personal data enters the
repository. Each is asserted here so it fails in CI rather than in public.
"""

import ast
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import ClassVar

import pytest

ROOT = Path(__file__).resolve().parent.parent
EU27 = {
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
}


def tracked_under_pdf() -> list[Path]:
    """Tracked files under pdf/, which must always be empty."""
    return [p for p in tracked_files() if p.as_posix().find("/pdf/") != -1]


def tracked_files() -> list[Path]:
    """List files under version control, or every file when git is absent."""
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        return [p for p in ROOT.rglob("*") if p.is_file()]
    return [ROOT / line for line in result.stdout.split()]


@pytest.fixture(scope="module")
def index() -> list[dict]:
    """The DG SANTE audit index."""
    return json.loads((ROOT / "data" / "dgsante_index.json").read_text("utf-8"))


@pytest.fixture(scope="module")
def details() -> list[dict]:
    """One record per harvested audit detail page."""
    path = ROOT / "data" / "dgsante_details.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def manifest() -> list[dict]:
    """One record per downloaded corpus file."""
    path = ROOT / "data" / "dgsante_manifest.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def annex_classes() -> list[dict]:
    """One record per numbered annex from the older era."""
    path = ROOT / "data" / "dgsante_annex_classes.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def recommendations() -> list[dict]:
    """One record per recommendation parsed out of a report."""
    path = ROOT / "data" / "dgsante_recommendations.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def action_plans() -> list[dict]:
    """One record per recommendation answered in an action plan."""
    path = ROOT / "data" / "dgsante_action_plans.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def warehouse() -> dict:
    """The manifest describing the dimensional model."""
    path = ROOT / "data" / "dgsante_warehouse_manifest.json"
    return json.loads(path.read_text("utf-8"))


@pytest.fixture(scope="module")
def image_reading() -> list[dict]:
    """The hand-read verdict on each document where the two methods disagreed."""
    path = ROOT / "data" / "bildlasning_facit.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def denominators() -> list[dict]:
    """One hand-copied record per authority that answered P11."""
    path = ROOT / "data" / "namnare.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def dashboard() -> str:
    """The generated dashboard page."""
    return (ROOT / "docs" / "dashboard.html").read_text("utf-8")


@pytest.fixture(scope="module")
def graph() -> list[dict]:
    """One record per citation edge, with the paragraph it points at."""
    path = ROOT / "data" / "dgsante_graph.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def report_parse() -> list[dict]:
    """One record per report with the outcome of parsing it."""
    path = ROOT / "data" / "dgsante_report_parse.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def ocr_index() -> list[dict]:
    """One record per annex put through OCR."""
    path = ROOT / "data" / "dgsante_ocr_index.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def grounds() -> list[dict]:
    """One record per authority statement about what was masked and why."""
    path = ROOT / "data" / "sekretessgrunder.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def masking() -> list[dict]:
    """One record per delivered document judged by step 18."""
    path = ROOT / "data" / "maskning.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def species() -> list[dict]:
    """One record per delivered document with its animal counts."""
    path = ROOT / "data" / "djurslag.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def contrast() -> list[dict]:
    """One record per authority, species and request class."""
    path = ROOT / "data" / "kontrast.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def species_sample() -> list[dict]:
    """The hand-read sample the species rule was checked against."""
    path = ROOT / "data" / "djurslag_facit.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def protocol() -> list[dict]:
    """Every logged event in the collection protocol."""
    path = ROOT / "data" / "protokoll_logg.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def decisions() -> list[dict]:
    """One record per appealable decision received under P8."""
    path = ROOT / "data" / "beslut.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def announced() -> list[dict]:
    """One record per report on announced and unannounced controls."""
    path = ROOT / "data" / "foranmalda.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def deficiency() -> list[dict]:
    """One record per county, year, species and control category."""
    path = ROOT / "data" / "bristandel.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def unannounced() -> list[dict]:
    """One record per cell of the pre-registered association test."""
    path = ROOT / "data" / "oanmald_hypotes.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def hidden_text() -> list[dict]:
    """One record per delivered document with a text layer."""
    path = ROOT / "data" / "dold_text.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def conditions() -> list[dict]:
    """One record per condition segmented out of a permit decision."""
    path = ROOT / "data" / "villkor_baseline.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def register() -> list[dict]:
    """One record per condition, with the text as the decision wrote it."""
    path = ROOT / "data" / "villkor.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def permit_types() -> list[dict]:
    """One record per decision on the publisher's listing, with its own label."""
    path = ROOT / "data" / "tillstand_typ.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def permits() -> list[dict]:
    """One record per downloaded permit decision."""
    path = ROOT / "data" / "tillstand_manifest.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def annex_labels() -> list[dict]:
    """Hand-read classes for the held-out samples."""
    path = ROOT / "data" / "dgsante_annex_labels.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


class TestSchemaIsInSyncWithItsDocument:
    """src/schema.py is generated from the code block in the design document."""

    def test_generated_module_matches_document(self):
        doc = (ROOT / "docs" / "VILLKORSSCHEMA.md").read_text("utf-8")
        blocks = re.findall(r"```(?:python)?\n(.*?)```", doc, re.S)
        expected = "\n\n".join(blocks).strip()
        actual = (ROOT / "src" / "schema.py").read_text("utf-8").strip()
        assert actual == expected, (
            "src/schema.py has drifted from docs/VILLKORSSCHEMA.md. "
            "Edit the document and regenerate the module."
        )


class TestNoPersonalDataIsCommitted:
    """The project measures authorities, never named individuals."""

    EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}")
    # Martin's own address, and the courts' registry addresses. The latter are
    # institutional, published on the courts' own websites, and they enter the
    # repository without anyone typing them: a court that answers by secure
    # e-mail names the attachment after the address it came from, and the
    # delivery manifest records file names verbatim. A natural person's address
    # has no such route in and stays forbidden.
    ALLOWED_EMAILS: ClassVar[set[str]] = {
        "cm.blomqvist@gmail.com",
        "kammarrattenisundsvall@dom.se",
        "Kammarratten.Goteborg@dom.se",
    }

    def test_no_third_party_email_addresses(self):
        offenders = []
        for path in tracked_files():
            if path.suffix not in {".md", ".py", ".toml", ".cff", ".yml", ".yaml"}:
                continue
            for found in self.EMAIL.findall(path.read_text("utf-8", errors="ignore")):
                if found not in self.ALLOWED_EMAILS:
                    offenders.append(f"{path.name}: {found}")
        assert not offenders, f"third-party e-mail addresses committed: {offenders}"

    # The Swedish collection's own files. The DG SANTE datasets are excluded on
    # purpose: they quote published Commission audit reports, which name
    # authority contact addresses, and redacting a published source would be a
    # different kind of dishonesty.
    PROTOCOL_DATA: ClassVar[tuple[str, ...]] = (
        "protokoll_logg.jsonl",
        "beslut.jsonl",
        "sekretessgrunder.jsonl",
        "maskning.jsonl",
        "leveranser_manifest.jsonl",
        "dold_text.jsonl",
    )
    ROLES: ClassVar[set[str]] = {
        "administratör",
        "arkivarie",
        "avdelningschef",
        "chefsjurist",
        "enhetschef",
        "länsjurist",
        "djurskyddshandläggare",
        "länsveterinär",
        "jurist",
        "handläggare",
        "verksjurist",
        "registrator",
        # Jordbruksverket's decision of 2 September 2026 names its presenter
        # without a title. Writing a plausible one would be an invention, and
        # leaving the field empty would look like an omission, so the register
        # says what the source says.
        "titel anges inte",
    }

    def test_no_addresses_in_the_swedish_protocol_data(self):
        # The e-mail scan above skips .jsonl, and the protocol log is exactly
        # where an authority's correspondence lands.
        offenders = []
        for name in self.PROTOCOL_DATA:
            path = ROOT / "data" / name
            if not path.exists():
                continue
            for found in self.EMAIL.findall(path.read_text("utf-8")):
                if found not in self.ALLOWED_EMAILS:
                    offenders.append(f"{name}: {found}")
        assert not offenders, f"e-mail addresses in the protocol data: {offenders}"

    # The condition register is built from recognised text, and OCR reads an
    # at sign as a left parenthesis followed by Q. The EMAIL pattern above
    # therefore does not see an address in it. On 9 September 2026 six
    # conditions in the register carried two officials' names and their
    # addresses in that shape, committed since a32fda2. See ADR-0022.
    OCR_EMAIL: ClassVar[re.Pattern[str]] = re.compile(
        r"[\w.]+ ?[\(\[][QO0][\w.-]*\.(?:se|com|nu)", re.IGNORECASE
    )
    CONTACT_LINE: ClassVar[re.Pattern[str]] = re.compile(
        r"kontakta i detta [äa]rende", re.IGNORECASE
    )
    CONDITION_DATA: ClassVar[tuple[str, ...]] = (
        "villkor.jsonl",
        "villkor_facit_urval.jsonl",
        "villkor_facit.jsonl",
    )

    def test_no_contact_block_in_the_condition_register(self):
        offenders = []
        for name in self.CONDITION_DATA:
            path = ROOT / "data" / name
            if not path.exists():
                continue
            text = path.read_text("utf-8")
            offenders += [f"{name}: {m}" for m in self.OCR_EMAIL.findall(text)]
            if self.CONTACT_LINE.search(text):
                offenders.append(f"{name}: the county board's contact line")
        assert not offenders, (
            f"a footer contact block reached the register: {offenders}"
        )

    def test_a_decision_names_a_role_and_never_a_person(self):
        # CONTRIBUTING: the names stay in the source document, the repo carries
        # the role. A new decision pasted in with its names fails here.
        path = ROOT / "data" / "beslut.jsonl"
        if not path.exists():
            return
        for line in path.read_text("utf-8").splitlines():
            if not line:
                continue
            record = json.loads(line)
            for field in ("beslutsfattare", "foredragande"):
                assert record[field] in self.ROLES, (
                    f"{field} is {record[field]!r}; write the role alone, and "
                    "leave the name in the source document"
                )
            assert record["namn_utelamnade"] is True

    # The P12 replies are published verbatim, so the authorities' own functional
    # mailboxes stand in them: those are published contact details for a public
    # body. A named official's address is a different thing, and the packets
    # promised it would appear nowhere, which is what these two tests hold. The
    # local parts are listed without the domain, so this file does not itself
    # become a list of committed addresses.
    FUNCTIONAL_LOCAL_PARTS: ClassVar[set[str]] = {
        "dalarna",
        "gavleborg",
        "kronoberg",
        "lansstyrelsen.vasternorrland",
        "orebro",
        "skane",
        "uppsala",
        "varmland",
        "vasterbotten",
        "vasternorrland",
        "vastmanland",
        "vastragotaland",
    }
    FUNCTIONAL_DOMAINS: ClassVar[set[str]] = {
        "lansstyrelsen.se",
        "jordbruksverket.se",
    }

    def test_only_functional_mailboxes_in_the_reply_register(self):
        path = ROOT / "data" / "p12_svar.jsonl"
        if not path.exists():
            return
        offenders = []
        for line in path.read_text("utf-8").splitlines():
            if not line:
                continue
            record = json.loads(line)
            # The decoded text, not the raw line: a JSONL escape would otherwise
            # glue an n onto the local part and hide what is really there.
            fields = " ".join(
                str(record.get(key) or "")
                for key in ("text", "avsandare", "amnesrad", "bilagor", "utelamnat")
            )
            for found in self.EMAIL.findall(fields):
                if found in self.ALLOWED_EMAILS:
                    continue
                local, _, domain = found.rpartition("@")
                if (
                    domain.lower() in self.FUNCTIONAL_DOMAINS
                    and local.lower() in self.FUNCTIONAL_LOCAL_PARTS
                ):
                    continue
                if (
                    domain.lower() == "jordbruksverket.se"
                    and local.lower() == domain.split(".")[0]
                ):
                    continue
                offenders.append(found)
        assert not offenders, (
            f"an address that is not a published functional mailbox: {offenders}"
        )

    def test_a_reply_names_a_role_and_never_a_person(self):
        path = ROOT / "data" / "p12_svar.jsonl"
        if not path.exists():
            return
        for line in path.read_text("utf-8").splitlines():
            if not line:
                continue
            record = json.loads(line)
            if record["avsandare"] == "namngiven tjänsteman":
                assert record["roll"], "a named sender must carry its role instead"
            if record["roll"]:
                first = record["roll"].split()[0]
                assert first in self.ROLES, (
                    f"the role {record['roll']!r} starts with {first!r}, which is "
                    "not one of the roles the repository writes"
                )
            assert record["meddelande"], "every reply carries its message id"

    def test_the_sent_packets_still_hash_to_what_was_sent(self):
        import hashlib

        manifest = ROOT / "data" / "p12_avsant_manifest.jsonl"
        if not manifest.exists():
            return
        rows = [
            json.loads(line)
            for line in manifest.read_text("utf-8").splitlines()
            if line
        ]
        assert len(rows) == 22, "one archived letter per authority that got one"
        for row in rows:
            letter = ROOT / row["path"]
            assert letter.exists(), f"{row['path']} is missing"
            raw = letter.read_bytes()
            assert hashlib.sha256(raw).hexdigest() == row["sha256"], (
                f"{row['path']} no longer hashes to what was sent"
            )
            assert len(raw) == row["bytes"]

    def test_the_sweden_export_agrees_with_the_masking_register(self):
        export = ROOT / "web" / "public" / "data" / "sverige.json"
        masking = ROOT / "data" / "maskning.jsonl"
        if not export.exists():
            return
        rows = [
            json.loads(line) for line in masking.read_text("utf-8").splitlines() if line
        ]
        data = json.loads(export.read_text("utf-8"))
        for authority in data["myndigheter"]:
            for klass, figures in authority["klasser"].items():
                prefix = f"{authority['slug']}_{klass}/"
                own = [row for row in rows if row["path"].startswith(prefix)]
                assert figures["dokument"] == len(own), authority["slug"]
                assert figures["maskade"] == sum(1 for row in own if row["masked"]), (
                    authority["slug"]
                )

    def test_every_authority_in_the_export_has_a_reply_or_says_it_has_none(self):
        export = ROOT / "web" / "public" / "data" / "sverige.json"
        if not export.exists():
            return
        data = json.loads(export.read_text("utf-8"))
        assert len(data["myndigheter"]) == 22
        for authority in data["myndigheter"]:
            substantive = [
                reply for reply in authority["svar"] if reply["typ"] == "substantiellt"
            ]
            assert authority["svar_saknas"] == (not substantive), authority["slug"]

    # Tillämpningsnot 5 declares the fee measure for all 21 counties, whatever
    # the outcome, and tillämpningsnot 7 forbids estimating a figure that is
    # missing. These two hold both halves: every county is in the register, and
    # the release rate stays an open gap with its reason until something in the
    # material converts files into controls.
    FEE_OUTCOMES: ClassVar[set[str]] = {
        "beslut meddelat",
        "beslut vägrat",
        "generellt styrdokument",
        "uteblivet svar",
        "avgiften föll efter avsmalningen",
        "ingen avgift aviserad",
    }

    def test_the_fee_measure_covers_every_county(self):
        path = ROOT / "data" / "avgiftsskrivelser.jsonl"
        if not path.exists():
            return
        rows = [
            json.loads(line) for line in path.read_text("utf-8").splitlines() if line
        ]
        assert len(rows) == 21, (
            "the measure is reported for all 21, whatever the outcome"
        )
        assert len({row["myndighet"] for row in rows}) == 21
        for row in rows:
            assert row["utfall"] in self.FEE_OUTCOMES, row["utfall"]
            if row["avgiftsbesked"] == 0:
                assert row["utfall"] == "ingen avgift aviserad", row["myndighet"]
                assert row["skrivelser"] == 0

    def test_the_release_rate_stays_a_gap_with_its_reason(self):
        path = ROOT / "data" / "utlamningsgrad.jsonl"
        if not path.exists():
            return
        rows = [
            json.loads(line) for line in path.read_text("utf-8").splitlines() if line
        ]
        assert len(rows) == 42, "one row per county and class"
        for row in rows:
            assert row["utlamningsgrad"] is None, (
                "P11's rate is not computed; filling it in silently would put a "
                "count of files over a cap that counts controls"
            )
            assert row["skal"], "a gap carries the reason it is a gap"

    def test_the_annex_register_reads_both_kinds_of_reference(self):
        path = ROOT / "data" / "bilagor.jsonl"
        if not path.exists():
            return
        rows = [
            json.loads(line) for line in path.read_text("utf-8").splitlines() if line
        ]
        for row in rows:
            # A folder cannot have more annex files than files, and the flag is
            # the conjunction it is defined as: a reference to content, and no
            # annex file at all.
            assert row["bilagefiler"] <= row["filer"], row["myndighet"]
            assert row["utan_bilaga"] == (
                row["hanvisar_till_bilaga"] > 0 and row["bilagefiler"] == 0
            ), f"{row['myndighet']} {row['begaran']}"
            assert (
                sum(row["hanvisningens_slag"].values()) == row["hanvisar_till_bilaga"]
            ), f"{row['myndighet']} {row['begaran']}"
            assert row["lasning"], "the reading carries what it cannot see"

    def test_a_pair_is_the_same_case_in_both_classes(self):
        path = ROOT / "data" / "dubbelforekomst.jsonl"
        if not path.exists():
            return
        rows = [
            json.loads(line) for line in path.read_text("utf-8").splitlines() if line
        ]
        for row in rows:
            assert row["par"] <= min(row["arenden_i_a"], row["arenden_i_b"])
            assert len(row["arendenummer"]) == row["par"]
            if row["par"]:
                assert row["parade_dokument_a"] >= row["par"], row["myndighet"]
                assert row["parade_maskade_a"] <= row["parade_dokument_a"]
                assert row["parade_maskade_b"] <= row["parade_dokument_b"]

    def test_the_readme_states_the_number_of_tests_there_are(self, request):
        # The figure has gone stale twice, 152 against 240 and 249 against 250,
        # because nothing counted it. pytest knows the number during the run, so
        # the claim is checked against the run itself rather than against memory.
        config = request.config
        if config.option.keyword or config.option.markexpr:
            pytest.skip("a filtered run collects a subset")
        if any("::" in str(arg) for arg in config.args):
            pytest.skip("a single test was selected")
        collected = request.session.testscollected
        if not collected:
            pytest.skip("nothing collected")
        text = (ROOT / "README.md").read_text("utf-8")
        found = re.search(r"The (\d+) tests carry", text)
        assert found, "the README no longer states a test count"
        assert int(found.group(1)) == collected, (
            f"the README says {found.group(1)} tests, the suite collects {collected}"
        )

    def test_no_source_pdfs_are_tracked(self):
        pdfs = [p.name for p in tracked_files() if p.suffix.lower() == ".pdf"]
        assert not pdfs, (
            f"source PDFs are tracked: {pdfs}. Their file names carry the names "
            "of natural persons and belong outside version control."
        )


class TestThePipelineStaysOrdered:
    """The numbered steps are how docs and ADRs refer to the work."""

    def test_step_numbers_are_unique(self):
        steps = (ROOT / "pipeline").glob("[0-9][0-9]_*.py")
        numbers = [path.name[:2] for path in steps]
        duplicates = sorted({n for n in numbers if numbers.count(n) > 1})
        assert not duplicates, (
            f"two pipeline scripts share a step number: {duplicates}. The number "
            "is how docs and ADRs cite a step, so a collision makes every such "
            "reference ambiguous."
        )


class TestOpenItemsKnowsEveryEvent:
    """The open-items report must never guess which side an event came from."""

    def test_every_logged_event_is_mapped_to_a_side(self):
        from open_items import load, unmapped

        holes = unmapped(load())
        assert not holes, (
            f"event types missing from src/open_items.py: {sorted(holes)}. Until "
            "they are placed in OURS, THEIRS or INTERNAL the report cannot say "
            "who owes the next move, and a new event type would silently drop "
            "out of the check."
        )

    def test_the_projects_own_pledges_are_readable_and_placed(self):
        """The register of what the project owes itself, guarded like the log.

        It exists because an instruction in the protocol sat unexecuted for 36
        days: KR Jönköping 549-19 was to be requested at the same time as the
        Sundsvall ruling on 2 August 2026, the wording was changed to "before
        publication" the next day without the deferral being declared, and
        nothing surfaced it. A register nobody can trust surfaces nothing
        either, so the shape is checked here.
        """
        from datetime import date as _date

        from open_items import pledges

        rows = pledges()
        assert rows, "data/atagande.jsonl är tom"
        fields = {
            "id",
            "kalla",
            "atagande",
            "status",
            "oppnat",
            "stangt",
            "frist",
            "notering",
        }
        seen = set()
        for row in rows:
            assert set(row) == fields, sorted(set(row) ^ fields)
            assert row["status"] in {"öppet", "väntar", "gjort"}, row["status"]
            assert row["id"] not in seen, row["id"]
            seen.add(row["id"])
            _date.fromisoformat(row["oppnat"])
            if row["status"] == "gjort":
                assert row["stangt"], f"{row['id']} är gjort utan datum"
                _date.fromisoformat(row["stangt"])
            else:
                assert row["stangt"] is None, f"{row['id']} är öppet med slutdatum"
            if row["frist"]:
                _date.fromisoformat(row["frist"])

    def test_every_authority_name_is_one_the_report_can_place(self):
        # An invented myndighet builds a request nobody sent. On 5 September
        # 2026 seven internal rows about the conditions layer were logged under
        # "länsstyrelserna", and the report answered with a phantom item under a
        # P3 deadline 19 days overdue, first in the list of what to do next.
        # The log is append-only, so the guard belongs here and in the code that
        # reads it, never in the rows.
        from open_items import NOT_A_REQUEST, load

        allowed = re.compile(r"^(Länsstyrelsen i .+|Jordbruksverket)$")
        strays = {
            row["myndighet"]
            for row in load()
            if row["myndighet"] not in NOT_A_REQUEST
            and not allowed.match(row["myndighet"])
        }
        assert not strays, (
            f"myndighet values the report cannot place: {sorted(strays)}. Add a "
            "real authority to the pattern deliberately, or an aggregate word to "
            "NOT_A_REQUEST, so that the choice is made and not inherited from a "
            "typo."
        )

    def test_no_request_is_built_out_of_internal_rows_alone(self):
        from open_items import INTERNAL, by_request, load

        phantom = {
            key
            for key, events in by_request(load()).items()
            if all(event["handelse"] in INTERNAL for event in events)
        }
        assert not phantom, sorted(phantom)

    def test_the_publication_floor_follows_the_packets_and_not_day_40(self):
        # Tillämpningsnot 8: publication is any surface that makes an authority's
        # own results readable, and no surface opens until P12's three weeks have
        # run. The instrument printed day 40 as the floor until 7 October 2026,
        # which is the date the protocol stopped meaning.
        from datetime import date

        from open_items import publication_lines

        rows = [
            {
                "datum": "2026-10-02",
                "klockslag": "13:12:22",
                "myndighet": "Länsstyrelsen i Uppsala",
                "begaran": "A+B",
                "handelse": "P12-paket avsänt",
                "notering": "",
            }
        ]
        printed = " ".join(publication_lines(rows, date(2026, 10, 7)))
        assert "2026-10-24" in printed, printed
        assert "2026-10-23" in printed, printed

        empty = " ".join(publication_lines([], date(2026, 9, 1)))
        assert "2026-09-28" in empty, empty
        assert "not 8" in empty, empty

    def test_acknowledging_service_does_not_close_the_appeal_window(self):
        # The authority asks for a receipt, so the receipt is an event of ours.
        # Counting any event of ours as an answer made the P9 deadline vanish
        # from the report the moment the receipt was logged, which is the one
        # failure this report exists to prevent.
        from datetime import date as _date

        from open_items import state

        events = [
            {
                "datum": "2026-08-23",
                "klockslag": "22:00",
                "myndighet": "x",
                "begaran": "A",
                "handelse": "beslutsbegäran och fråga om uttagets fullständighet",
                "notering": "",
            },
            {
                "datum": "2026-08-25",
                "klockslag": "13:46",
                "myndighet": "x",
                "begaran": "A",
                "handelse": "avslagsbeslut mottaget",
                "notering": "",
            },
            {
                "datum": "2026-08-25",
                "klockslag": "14:10",
                "myndighet": "x",
                "begaran": "A",
                "handelse": "delgivningskvitto",
                "notering": "",
            },
        ]
        item = state(events, _date(2026, 8, 26))
        assert item["waiting_on"] == "dig"
        assert item["step"] == "P9"
        assert item["due"] == _date(2026, 9, 8)
        assert item["last_event"]["handelse"] == "avslagsbeslut mottaget"
        assert not item["closed"]

        events.append(
            {
                "datum": "2026-09-01",
                "klockslag": "09:00",
                "myndighet": "x",
                "begaran": "A",
                "handelse": "avstående från överklagande",
                "notering": "",
            }
        )
        after = state(events, _date(2026, 9, 2))
        assert after["waiting_on"] == "myndigheten"


class TestDocumentationMatchesData:
    """Figures quoted in docs/DGSANTE.md must hold against the data files."""

    def test_index_and_details_cover_the_same_audits(self, index, details):
        assert len(index) == len(details) == 4690
        assert {r["detail_id"] for r in index} == {r["detail_id"] for r in details}

    def test_harvest_recorded_no_errors(self, details):
        assert [r for r in details if r.get("error")] == []

    def test_eu27_and_sweden_counts(self, index):
        assert sum(1 for r in index if r["country"] in EU27) == 3020
        assert sum(1 for r in index if r["country"] == "Sweden") == 98

    def test_english_coverage(self, details):
        with_english = sum(
            1 for r in details if any(x["language"] == "English" for x in r["reports"])
        )
        assert with_english == 4563

    def test_action_plan_coverage(self, details):
        with_plan = [
            r
            for r in details
            if any("action" in (a["title"] or "").lower() for a in r["annexes"])
        ]
        assert len(with_plan) == 1747
        assert sum(1 for r in with_plan if r["country"] in EU27) == 1084

    def test_two_reference_formats(self, index):
        assert sum(1 for r in index if r["ref"].startswith("CT-")) == 122
        assert sum(1 for r in index if re.fullmatch(r"\d{4}-\d{4}", r["ref"])) == 4568


class TestAnnexClassificationHoldsAgainstHandReading:
    """The numbered annexes are classified, and the call is checkable.

    The claim these guard is the one the project would be attacked on: that
    the numbered annexes are overwhelmingly member state comments and only
    rarely action plans. A classifier that quietly drifted into counting
    mentions of a plan as a plan would invert that finding.
    """

    RESPONSES: ClassVar[set[str]] = {"action_plan", "actions_taken_response"}
    AGREEMENT_FLOOR = 0.80

    def test_every_numbered_annex_is_accounted_for(self, manifest, annex_classes):
        numbered = {
            m["path"]
            for m in manifest
            if m["kind"] == "annex" and str(m.get("title", "")).strip().isdigit()
        }
        assert {r["path"] for r in annex_classes} == numbered
        assert len(annex_classes) == 1974

    def test_a_classified_annex_always_quotes_its_evidence(self, annex_classes):
        undecided = {"unclassified_text", "needs_ocr", "needs_conversion"}
        classified = [r for r in annex_classes if r["class"] not in undecided]
        assert classified
        assert all(r["evidence"].strip() for r in classified)
        assert all(r["method"] for r in annex_classes)

    def test_agreement_with_hand_read_labels(self, annex_classes, annex_labels):
        predicted = {r["path"]: r["class"] for r in annex_classes}
        assert {r["path"] for r in annex_labels} <= set(predicted)
        agreed = sum(1 for r in annex_labels if predicted[r["path"]] == r["label"])
        assert agreed / len(annex_labels) >= self.AGREEMENT_FLOOR

    def test_no_document_is_called_a_plan_that_is_not_one(
        self, annex_classes, annex_labels
    ):
        predicted = {r["path"]: r["class"] for r in annex_classes}
        wrong = [
            r["path"]
            for r in annex_labels
            if predicted[r["path"]] in self.RESPONSES
            and r["label"] not in self.RESPONSES
        ]
        assert not wrong, f"classified as a plan or response but is not: {wrong}"

    def test_action_plans_stay_a_small_minority(self, annex_classes):
        plans = sum(1 for r in annex_classes if r["class"] in self.RESPONSES)
        assert plans / len(annex_classes) < 0.10


class TestTheCitationGraphIsWhatTheReportsSay:
    """Parsed recommendations must stay tied to the documents they came from.

    The graph is the analytic payload of the DG SANTE layer, so the numbers
    quoted about its size have to hold, and an audit that made no
    recommendation has to stay visible as a zero rather than a gap.
    """

    def test_every_report_has_an_outcome(self, manifest, report_parse):
        reports = {m["path"] for m in manifest if m["kind"] == "report"}
        assert {r["path"] for r in report_parse} == reports
        assert len(report_parse) == 2940

    def test_recommendations_belong_to_parsed_reports(
        self, recommendations, report_parse
    ):
        parsed = {r["ref"] for r in report_parse if r["outcome"] == "parsed"}
        assert {r["ref"] for r in recommendations} <= parsed
        assert len(recommendations) > 8000

    def test_numbering_runs_from_one_without_gaps(self, recommendations):
        """Grouped by file, not by audit: 15 audits have two English reports.

        Where an audit was reissued, both files carry their own numbering
        from one, so grouping by reference would look like a gap.
        """
        by_file: dict[str, list[int]] = {}
        for row in recommendations:
            by_file.setdefault(row["path"], []).append(row["number"])
        for path, found in by_file.items():
            assert found == list(range(1, len(found) + 1)), path

    def test_no_recommendation_is_empty(self, recommendations):
        assert all(len(r["text"]) >= 40 for r in recommendations)

    def test_cross_references_are_paragraph_numbers_not_citations(
        self, recommendations
    ):
        """Article and regulation numbers must never enter the graph.

        A regulation is cited as "2017/625", and a pattern that read digits
        greedily once turned that into edges numbered 201, 7 and 625.
        """
        for row in recommendations:
            for number in row["based_on_conclusions"] + row["associated_findings"]:
                assert 1 <= number <= 300, row["ref"]
            assert len(row["based_on_conclusions"]) <= 10

    def test_an_audit_without_recommendations_stays_visible(self, report_parse):
        stated = [r for r in report_parse if r["outcome"] == "states_no_recommendation"]
        assert stated, "an explicit zero must never be folded into a parse failure"

    def test_recall_on_the_reports_that_carry_the_graph(self, report_parse):
        stating = [r for r in report_parse if r.get("section_states_links")]
        parsed = [r for r in stating if r["outcome"] == "parsed"]
        assert len(parsed) / len(stating) >= 0.85


class TestTheGraphClosesOntoRealParagraphs:
    """Every edge must name a paragraph, and say when it cannot find one."""

    def test_every_edge_belongs_to_a_parsed_recommendation(
        self, graph, recommendations
    ):
        known = {(r["path"], r["number"]) for r in recommendations}
        assert {(e["path"], e["recommendation"]) for e in graph} <= known

    def test_edge_counts_match_the_recommendations(self, graph, recommendations):
        expected = sum(
            len(r["based_on_conclusions"]) + len(r["associated_findings"])
            for r in recommendations
        )
        assert len(graph) == expected

    def test_an_unresolved_edge_carries_no_invented_paragraph(self, graph):
        for edge in graph:
            if edge["resolved"]:
                assert edge["paragraph_text"]
            else:
                assert edge["paragraph_text"] is None
                assert edge["paragraph_kind"] is None

    def test_most_cited_paragraphs_resolve(self, graph):
        resolved = sum(1 for e in graph if e["resolved"])
        assert resolved / len(graph) >= 0.85

    def test_the_two_readings_agree_more_often_than_not(self, graph):
        """The paragraph's heading and the citation are separate evidence.

        They disagree on a real minority of edges, which is recorded rather
        than reconciled; this guards the rate against silent decay.
        """
        cited = [e for e in graph if e["resolved"] and e["cites"] == "conclusion"]
        agreeing = sum(1 for e in cited if e["paragraph_kind"] == "conclusion")
        assert agreeing / len(cited) >= 0.55


class TestActionPlansAnswerRealRecommendations:
    """A commitment must be tied to a recommendation that exists."""

    def test_every_response_names_a_plan_and_a_number(self, action_plans):
        assert action_plans
        for row in action_plans:
            assert row["plan_path"].startswith("pdf/dgsante/annexes/")
            assert 1 <= row["recommendation"] <= 40
            assert row["response"] or row["restated_recommendation"]

    def test_responses_mostly_match_a_parsed_recommendation(
        self, action_plans, recommendations
    ):
        known = {(r["ref"], r["number"]) for r in recommendations}
        matched = sum(
            1 for r in action_plans if (r["ref"], r["recommendation"]) in known
        )
        assert matched / len(action_plans) >= 0.4

    def test_the_restated_text_is_kept_so_the_link_can_be_checked(self, action_plans):
        """The plan restates the recommendation; that is the check on the link.

        A link resting on a shared number alone cannot be verified, so the
        restatement has to survive into the output for most rows.
        """
        with_text = sum(1 for r in action_plans if r["restated_recommendation"])
        assert with_text / len(action_plans) >= 0.8

    def test_a_confirmed_link_really_does_have_matching_text(self, action_plans):
        """Confirmation rests on containment, not on a symmetric ratio.

        The plans are two-column tables whose response column bleeds words
        into the restatement. A symmetric ratio punished that heavily even
        where every word of the recommendation was present, so what is
        measured is how much of the report's wording the plan holds.
        """
        for row in action_plans:
            if row["link_confirmed_by_text"]:
                assert row["text_containment"] >= 0.6
                assert row["restated_recommendation"]

    def test_a_plan_in_another_language_is_marked_as_such(self, action_plans):
        """A translated plan cannot be confirmed by comparing wording.

        Counting it as a failed match would blame the parser for a
        translation, so the language is recorded and reported apart.
        """
        judged = [r for r in action_plans if r["restated_reads_as_english"] is not None]
        assert judged
        foreign = [r for r in judged if r["restated_reads_as_english"] is False]
        assert foreign, "no plan was found in another language, which is implausible"
        assert len(foreign) / len(judged) < 0.2


class TestTheWarehouseDescribesWhatWasBuilt:
    """The Parquet tables are a build artefact; the manifest is the record.

    These run without the binaries, so CI checks that the model still has
    the shape the documentation claims and that its row counts still follow
    from the committed datasets.
    """

    EXPECTED: ClassVar[set[str]] = {
        "dim_country",
        "dim_audit",
        "dim_paragraph",
        "fact_recommendation",
        "fact_citation",
        "fact_commitment",
    }

    def test_the_star_has_its_dimensions_and_facts(self, warehouse):
        assert {t["table"] for t in warehouse["tables"]} == self.EXPECTED

    def test_every_table_declares_its_key(self, warehouse):
        for table in warehouse["tables"]:
            names = {column["name"] for column in table["columns"]}
            if table["table"].startswith("dim_"):
                assert f"{table['table'][4:]}_key" in names, table["table"]
            else:
                assert "audit_key" in names, table["table"]

    def test_row_counts_follow_from_the_committed_datasets(
        self, warehouse, recommendations, graph, action_plans, index
    ):
        rows = {t["table"]: t["rows"] for t in warehouse["tables"]}
        assert rows["fact_recommendation"] == len(recommendations)
        assert rows["fact_citation"] == len(graph)
        assert rows["fact_commitment"] == len(action_plans)
        assert rows["dim_audit"] == len(index)

    def test_the_measures_agree_with_the_facts(self, warehouse, recommendations):
        measures = warehouse["measures"]
        assert measures["recommendations"] == len(recommendations)
        stating = sum(1 for r in recommendations if r["based_on_conclusions"])
        assert measures["recommendations_stating_their_basis"] == stating
        assert measures["citations_resolved"] <= measures["citations"]

    def test_a_citation_that_did_not_resolve_is_still_a_row(self, warehouse):
        """Dropping the unresolved would flatter the model.

        The count of what could not be joined is part of the result, so the
        citation fact must hold more rows than it resolved.
        """
        measures = warehouse["measures"]
        assert measures["citations"] > measures["citations_resolved"]


class TestTheDashboardSaysWhatTheDataSays:
    """The published page is generated, so its figures must still hold.

    A dashboard that drifts from its source is worse than none: it is the
    surface a reader trusts without being able to check it.
    """

    def test_the_page_is_present_and_self_contained(self, dashboard):
        assert "<svg" in dashboard
        for forbidden in ("http://", "https://cdn", "<script src", '<link rel="style'):
            assert forbidden not in dashboard, forbidden

    def test_the_headline_figures_come_from_the_warehouse(self, dashboard, warehouse):
        measures = warehouse["measures"]
        for value in (measures["recommendations"], measures["citations"]):
            assert f"{value:,}".replace(",", chr(0x2009)) in dashboard

    def test_every_chart_has_a_table_view(self, dashboard):
        assert dashboard.count("<svg") == dashboard.count("Visa som tabell")

    def test_the_limitations_are_on_the_page(self, dashboard):
        assert "Vad sidan inte visar" in dashboard
        assert "inget betyg" in dashboard

    def test_both_themes_are_declared(self, dashboard):
        assert "prefers-color-scheme: dark" in dashboard
        assert 'data-theme="dark"' in dashboard


class TestOcrIndexIsHonestAboutQuality:
    """OCR output is evidence of varying quality, and says so per file."""

    def test_every_ocr_record_belongs_to_a_known_annex(self, annex_classes, ocr_index):
        known = {r["path"] for r in annex_classes}
        assert {r["path"] for r in ocr_index} <= known
        assert len(ocr_index) == 1018

    def test_confidence_is_recorded_and_plausible(self, ocr_index):
        readable = [r for r in ocr_index if not r["error"]]
        assert readable
        assert all(0.0 <= r["mean_confidence"] <= 100.0 for r in readable)
        assert all(r["words"] > 0 for r in readable)

    def test_an_unreadable_file_is_reported_not_hidden(self, ocr_index):
        for record in ocr_index:
            if record["error"]:
                assert record["words"] == 0
            else:
                assert record["text_path"]


class TestManifestCoversTheDownloadedCorpus:
    """The committed manifest must mirror the EU-27 subset of the details.

    The corpus itself lives outside version control, so the manifest is the
    only guard CI has that the download was complete and attributable.
    """

    @staticmethod
    def expected_stems(details) -> tuple[set[str], set[str]]:
        reports: set[str] = set()
        annexes: set[str] = set()
        for rec in details:
            if rec["country"] not in EU27:
                continue
            for report in rec["reports"]:
                if report["language"] == "English":
                    reports.add(f"{rec['ref']}_{report['id']}_en")
            for annex in rec["annexes"]:
                annexes.add(f"{rec['ref']}_{annex['id']}")
        return reports, annexes

    def test_manifest_matches_the_details_exactly(self, details, manifest):
        reports, annexes = self.expected_stems(details)
        got_reports = {Path(m["path"]).stem for m in manifest if m["kind"] == "report"}
        got_annexes = {Path(m["path"]).stem for m in manifest if m["kind"] == "annex"}
        assert got_reports == reports
        assert got_annexes == annexes

    def test_headline_counts_hold(self, manifest):
        assert len(manifest) == 7963
        assert sum(1 for m in manifest if m["kind"] == "report") == 2940
        assert sum(1 for m in manifest if m["kind"] == "annex") == 5023

    def test_manifest_is_the_only_committed_trace_of_the_corpus(self, manifest):
        assert all(m["path"].startswith("pdf/") for m in manifest)
        assert not (ROOT / "pdf").exists() or not tracked_under_pdf()

    def test_every_row_is_hashed_and_nonempty(self, manifest):
        assert all(re.fullmatch(r"[0-9a-f]{64}", m["sha256"]) for m in manifest)
        assert all(m["bytes"] > 0 for m in manifest)
        assert all(m["kind"] in {"report", "annex"} for m in manifest)


class TestTheConditionRegisterCarriesTextAndNothingElse:
    """The register is the only file in the repository holding source text.

    VILLKORSSCHEMA section 2.7 allows it, because the condition text is the
    measurement object, and forbids everything around it: names of natural
    persons, officials and agents, and the contact details in the decision
    heads. Step 33 screens before it writes and refuses on a hit; these make the
    guarantee outlive that one run. The screen earned its place on 4 September
    2026, when it stopped the first write over 23 conditions that had swallowed
    a page footer, one of them naming an official with a private address.
    """

    FORBIDDEN: ClassVar[dict[str, str]] = {
        "e-postadress": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
        "personnummer": r"\b(?:19|20)\d{6}[-+]\d{4}\b",
        "telefonnummer": r"\b0\d{1,3}[-\s]\d{2,3}\s?\d{2}\s?\d{2}\b",
    }

    def test_no_contact_details_reached_the_register(self, register):
        offenders = []
        for record in register:
            for label, pattern in self.FORBIDDEN.items():
                if re.search(pattern, record["text"]):
                    offenders.append(
                        f"{record['id']} {record['villkorsnummer']}: {label}"
                    )
        assert not offenders, offenders[:10]

    def test_the_register_and_the_baseline_are_one_segmentation(
        self, register, conditions
    ):
        # Step 33 imports step 24 rather than repeating its rules, and the hash
        # is what proves the two files describe the same conditions.
        assert len(register) == len(conditions) == 2347
        assert {r["id"] for r in register} == {r["id"] for r in conditions}
        assert Counter(r["text_hash"] for r in register) == Counter(
            r["text_hash"] for r in conditions
        )

    def test_every_row_carries_its_provenance(self, register):
        fields = {
            "id",
            "prövningsgrupp",
            "beslutstyp",
            "villkorsnummer",
            "position",
            "rubrik",
            "text",
            "tecken",
            "källa",
            "text_hash",
        }
        for record in register:
            assert set(record) == fields
            assert record["text"].strip()
            assert record["källa"] in {"text", "ocr"}

    def test_the_headings_are_the_documents_own_words(self, register):
        # 1 655 of the conditions sit under a heading the decision wrote, and
        # the vocabulary is what VILLKORSSCHEMA section 2.2 predicted from four
        # decisions: the general condition, manure, air, chemicals, noise,
        # monitoring. A drop here means the heading rule stopped firing. It was
        # 1 691 under 161 headings until check 3 showed that 36 of them were
        # running heads: Miljöprövningsdelegationen, Anläggningsnummer, Örebro
        # län, Aktbilaga 23, Skåne. Reading all 155 that survived, before the
        # typology could be built on them, found seven more: a county's running
        # head in the genitive, and six headings with the tail of the previous
        # sentence glued in front of them. 148 now, and no document word lost.
        headings = [r["rubrik"] for r in register if r["rubrik"]]
        assert len(headings) == 1655
        assert len(set(headings)) == 148
        assert Counter(headings).most_common(1)[0] == ("Allmänt", 269)
        junk = {"Miljöprövningsdelegationen", "Skåne", "VÄSTRA GÖTALANDS LÄN"}
        assert not junk & set(headings)
        # The delegated matters, which VILLKORSSCHEMA section 2.4 gives a table
        # of their own, only became visible as a heading once the glued tails
        # were split off.
        assert Counter(headings)["Delegation"] == 10

    def test_every_heading_is_placed_in_the_typology(self, register):
        """Step 35's map and the register must not drift apart.

        The map places all 148 headings by hand, which is the point: a reader
        can disagree with one placement without reverse-engineering a rule. A
        heading that appears in a later delivery and is not placed would
        otherwise be counted as nothing at all.
        """
        import importlib.util

        path = ROOT / "pipeline" / "35_condition_types.py"
        spec = importlib.util.spec_from_file_location("condition_types", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        headings = {r["rubrik"] for r in register if r["rubrik"]}
        assert headings == set(module.HEADING_TYPE)
        placed = set(module.HEADING_TYPE.values())
        allowed = (
            set(module.SCHEMA_TYPES) | set(module.PROPOSED_TYPES) | set(module.ROUTED)
        )
        assert placed <= allowed, sorted(placed - allowed)

    def test_the_noise_values_are_the_set_the_corpus_closed_on(self, register):
        # Canary 2 of VILLKORSSCHEMA section 5. The schema opened the set as
        # {40, 45, 50} equivalent plus 55 momentary from four documents and
        # said it would be fixed against the whole corpus in the first full
        # run. That run was 5 September 2026 and added three values, 37, 42 and
        # 47, all of them from one decision, aa2cbc78989b condition 9, which
        # sets every level three decibels below the usual 50/45/45/40. Read by
        # hand in the source. The set is closed now, so an OCR reading of 40 as
        # 49 has to fail here.
        pattern = re.compile(r"(\d{2,3})\s*dB\s*\(?A\)?", re.IGNORECASE)
        values = Counter(
            int(match.group(1))
            for record in register
            for match in pattern.finditer(record["text"])
        )
        assert set(values) == {37, 40, 42, 45, 47, 50, 55}
        assert sum(values.values()) == 504
        assert values[45] == 174


class TestThePermitCorpusDecomposesAsDocumented:
    """Check 2 in VILLKORSSCHEMA needs the corpus split by decision type.

    The document states the expected split as "cirka 160/38/15/14" and the
    figure sat in prose with nothing holding it: the harvest manifest carries a
    hash and a permit division and no type at all. Step 31 takes the type from
    the publisher's own link text, which is the same principle ADR-0007 applies
    to annexes, and these pin what it found on 4 September 2026.

    The corpus grows as decisions are published, so a difference here is a
    finding about the source and not a broken test. The right response is to
    read the new documents and move the number, never to widen the assertion.
    """

    def test_every_listed_decision_was_harvested(self, permit_types, permits):
        assert len(permit_types) == 236
        assert {r["id"] for r in permit_types} == {r["id"] for r in permits}
        assert all(r["i_manifestet"] for r in permit_types)

    def test_every_permit_that_should_have_conditions_has_them(
        self, permit_types, conditions
    ):
        # After the widened segmentation of 4 September 2026 the only permits
        # without conditions are the two that were read by hand and found to
        # have none: one is an extension of a start-up deadline that the
        # publisher labelled a permit, the other amends single conditions in an
        # earlier decision. VILLKORSSCHEMA calls any other permit with zero
        # conditions a silent broken extraction, so this must stay at two.
        with_conditions = {r["id"] for r in conditions}
        permits = [r["id"] for r in permit_types if r["typ"] == "tillstånd"]
        assert len(permits) == 162
        assert sum(1 for p in permits if p not in with_conditions) == 2

    def test_the_four_documented_types_hold(self, permit_types):
        counted = Counter(r["typ"] for r in permit_types)
        assert counted["tillstånd"] == 162
        assert counted["ändring"] == 40
        assert counted["förlängning"] == 15
        assert counted["dom"] == 14

    def test_the_three_types_the_document_did_not_count(self, permit_types):
        # VILLKORSSCHEMA section 5 names igångsättning and upphävande among the
        # kinds allowed to carry zero conditions but never counted them, and it
        # does not mention the two condition decisions at all. They are pinned
        # here so that the population is fully declared.
        counted = Counter(r["typ"] for r in permit_types)
        assert counted["villkor"] == 2
        assert counted["igångsättning"] == 2
        assert counted["upphävande"] == 1
        assert sum(counted.values()) == 236

    def test_no_label_fell_outside_the_mapping(self, permit_types):
        assert [r["id"] for r in permit_types if r["typ"] == "annat"] == []

    def test_an_unknown_wording_is_never_written_down(self, permit_types):
        # The label is kept only where the mapping recognised it. An unknown
        # wording is where a party's name could enter, so it is withheld.
        for record in permit_types:
            if record["typ"] == "annat":
                assert record["etikett"] is None
            else:
                assert record["etikett"]


class TestTheConditionBaselineHoldsItsClaim:
    """The boilerplate null hypothesis fell, and the numbers must stay checkable.

    docs/VERIFIERAT.md states that 40 per cent of conditions share text with
    another decision and that reuse concentrates inside a permit division. If
    the segmenter drifts, those figures move and the claim silently changes,
    which is exactly the failure the retrain of Site Sentinel taught. The
    figures are pinned here, and a change to them has to be a deliberate edit
    of both the data and the document.

    They moved once, on 4 September 2026, when the segmenter learned two more
    ways a conditions section can open. Seven decisions entered the corpus and
    none lost a condition, which was the condition written down before the run.
    The share of shared text fell from 36 to 35 per cent, and the concentration
    inside one permit division held.
    """

    def test_the_corpus_is_the_one_the_document_describes(self, conditions, permits):
        assert len(permits) == 236
        assert len({p["sha256"] for p in permits}) == 235
        assert len(conditions) == 2347
        assert len({r["id"] for r in conditions}) == 180

    def test_the_two_sources_are_kept_apart(self, conditions):
        # The published figure is the born-digital one. OCR text loses
        # characters and breaks words at line ends, so pooling the two moves
        # the reuse share for an instrument reason. Both counts are pinned so
        # that a pooled headline cannot appear unnoticed.
        by_source = Counter(r["källa"] for r in conditions)
        assert by_source == {"text": 1762, "ocr": 585}
        assert len({r["id"] for r in conditions if r["källa"] == "text"}) == 123
        assert len({r["id"] for r in conditions if r["källa"] == "ocr"}) == 57

    def test_no_condition_row_carries_text(self, conditions):
        # The corpus is outside version control because the file names carry
        # private individuals' names; the hash is the only thing that may leave.
        fields = {
            "id",
            "prövningsgrupp",
            "villkorsnummer",
            "tecken",
            "källa",
            "rubrik",
            "series_ok",
            "serie_prövas",
        }
        for record in conditions:
            assert set(record) == fields | {"text_hash"}
            assert len(record["text_hash"]) == 16

    def test_every_condition_belongs_to_a_manifested_decision(
        self, conditions, permits
    ):
        groups = {p["id"]: p["prövningsgrupp"] for p in permits}
        for record in conditions:
            assert record["prövningsgrupp"] == groups[record["id"]]

    def test_the_series_check_still_passes_on_most_decisions(self, conditions):
        per_decision = {}
        source = {}
        for record in conditions:
            per_decision.setdefault(record["id"], []).append(record["villkorsnummer"])
            source[record["id"]] = record["källa"]
        clean = {
            i
            for i, ns in per_decision.items()
            if sorted(ns) == list(range(1, max(ns) + 1))
        }
        # OCR segments worse, and the gap is the reason the sources stay apart.
        assert sum(1 for i in clean if source[i] == "text") == 108
        assert sum(1 for i in clean if source[i] == "ocr") == 22

    def test_the_series_check_reports_what_it_can_speak_about(self, conditions):
        # An amendment changes named conditions in an earlier permit, so a gap
        # in its numbering is the right answer. Counting those as failures made
        # the segmenter look worse than it is and hid that the check says
        # nothing at all about them. The scoped figure is the one that measures
        # the segmenter, and both are pinned so neither can drift into the
        # other's place.
        tested = {r["id"] for r in conditions if r["serie_prövas"]}
        born = {r["id"] for r in conditions if r["källa"] == "text"}
        clean = {r["id"] for r in conditions if r["series_ok"]}
        assert len(born - tested) == 9
        assert len(born & tested) == 114
        assert len(born & tested & clean) == 105
        for record in conditions:
            assert record["series_ok"] == (record["id"] in clean)

    @staticmethod
    def owners(rows) -> dict[str, set[str]]:
        """Which decisions carry each condition text."""
        found: dict[str, set[str]] = {}
        for record in rows:
            found.setdefault(record["text_hash"], set()).add(record["id"])
        return found

    def test_the_headline_share_of_shared_text(self, conditions):
        rows = [r for r in conditions if r["källa"] == "text"]
        owners = self.owners(rows)
        shared = {h: ids for h, ids in owners.items() if len(ids) > 1}
        repeated = sum(1 for r in rows if len(owners[r["text_hash"]]) > 1)
        # The figures moved on 5 September 2026, when check 3 found that a
        # page break threw away the rest of 209 conditions. Repairing it raised
        # measured reuse rather than lowering it, against the prediction
        # written down before the run: two decisions that carried the same
        # condition had been cut at different points, so the truncation was
        # hiding matches.
        assert len(owners) == 1269
        assert len(shared) == 253
        assert repeated == 746
        assert round(repeated / len(rows), 2) == 0.42

    def test_reuse_stays_inside_a_permit_division(self, conditions):
        groups = {r["id"]: r["prövningsgrupp"] for r in conditions}
        inside = {}
        for source in ("text", "ocr"):
            rows = [r for r in conditions if r["källa"] == source]
            shared = [ids for ids in self.owners(rows).values() if len(ids) > 1]
            inside[source] = (
                sum(1 for ids in shared if len({groups[i] for i in ids}) == 1),
                len(shared),
            )
        # The OCR set shares no document with the born-digital one, so its own
        # concentration is a replication and not a restatement.
        assert inside["text"] == (238, 253)
        assert inside["ocr"] == (50, 52)


class TestNoDocumentHidesBodyTextBehindALightCover:
    """The pre-registered field measure resolved to a null, and nulls drift too.

    ADR-0017 replaced "andel maskerade fält" with a covered-content measure and
    published the result: no delivered document hides body text behind anything
    light. A null result is the easiest kind of finding to lose, because an
    instrument that quietly stops detecting produces the same number as an
    instrument that correctly detects nothing. These pin both sides.
    """

    def test_the_corpus_is_the_one_the_document_describes(self, hidden_text):
        # 249 until late August 2026. Since then Gotland's re-examination
        # delivered five re-masked reports and one annex under gotland_X, four
        # authority decisions were filed under their own folders, and the
        # appeals began producing documents of their own: two kammarrätter's
        # notices of a case number and Halland's transfer of the appeal to the
        # court. None of them belongs to request A or B, so all sit in "övrigt"
        # and none touches the A-against-B contrast, which stands at 109 of 170
        # and 32 of 140 after the marker was given a word boundary on 1 October
        # 2026.
        assert len(hidden_text) == 298
        by_class = Counter(r["klass"] for r in hidden_text)
        assert by_class == {"A": 140, "B": 125, "övrigt": 33}

    def test_the_measure_still_sees_the_header_boxes(self, hidden_text):
        # The detector must keep finding the known true positives. Were it to
        # return nothing at all, the null below would be vacuous.
        with_hidden = [r for r in hidden_text if r["dolda"]]
        assert len(with_hidden) == 45
        # 236 of these characters are the header the template's own white box
        # covers. The other 258 arrived on 29 September 2026 with Norrbotten's
        # class A delivery, in three documents that are page images carrying an
        # OCR text layer underneath: every glyph of that layer sits under the
        # picture, so the detector calls it hidden by construction. They are a
        # property of the layer, not a redaction, and the documents carry no
        # redaction at all.
        assert sum(r["dolda"] for r in hidden_text) == 494
        assert max(r["längsta_körning"] for r in hidden_text) == 24

    # The one document that trips the flag is named here rather than excluded
    # quietly. It is an OCR text layer under a page image, described above, and
    # the finding it would otherwise report does not exist: the document has no
    # redaction, and the hidden run is report prose the picture shows in full.
    OCR_LAYER_UNDER_AN_IMAGE = "norrbotten_A/8535-2024(27706259) (0) (1).pdf"

    def test_no_body_text_is_hidden(self, hidden_text):
        flagged = [r for r in hidden_text if r["dold_av_ljus_täckning"]]
        assert [r["path"] for r in flagged] == [self.OCR_LAYER_UNDER_AN_IMAGE]
        rest = [r for r in hidden_text if r["path"] != self.OCR_LAYER_UNDER_AN_IMAGE]
        assert max(r["längsta_i_brödtext"] for r in rest) == 0

    def test_hidden_text_is_only_ever_counted_never_stored(self, hidden_text):
        fields = {
            "path",
            "mapp",
            "klass",
            "tecken",
            "dolda",
            "längsta_körning",
            "längsta_i_brödtext",
            "körningar",
            "dold_av_ljus_täckning",
        }
        for record in hidden_text:
            assert set(record) == fields
            assert isinstance(record["dolda"], int)


class TestThePublishedMaskingSharesHoldAgainstTheData:
    """The headline of the openness layer is two fractions, so both are pinned.

    They moved once already, on 1 September 2026, when the text method stopped
    counting the control report template's black table header as a redaction:
    A fell from 138 of 155 to 108 of 155 and B from 32 of 135 to 29 of 135. A
    figure that has been wrong once is a figure worth holding still.

    B moved a second time on 28 September 2026, from 29 of 135 to 34 of 140,
    when five förelägganden that Länsstyrelsen i Kalmar län had released on
    13 August were found in the mailbox unlogged and unarchived. All five are
    masked, so the class B share rose from 21 to 24 per cent. The reason it
    mattered more than five documents usually would: Kalmar's class A reports
    are masked and their decision is under appeal, so the county carries the
    A/B contrast and was standing outside the measure.

    B moved a third time on 1 October 2026, from 34 of 140 to 32 of 140, when
    the text marker was required to start where a word starts. Matched anywhere
    in a word, "maskat" is also the end of "avmaskat", the Swedish for
    deworming, and two förelägganden about deworming cattle were counted as
    redacted on that word alone: one in Gävleborg B and one in Kronoberg B.
    Neither carries a redaction box, a bar or a marker in its file name. Two
    further documents lost the same marker without changing verdict, Halland A
    and Kalmar B, because each is masked on removed text independently of it.

    Class A moved again on 29 September 2026, from 108 of 155 to 109 of 170,
    when Länsstyrelsen i Blekinge and Länsstyrelsen i Norrbotten answered the
    day 40 reminder with the reports they had owed since 4 August. Blekinge
    masked one of five, Norrbotten none of ten, so the pooled class A share
    fell from 70 to 64 per cent. **The new figure is provisional.** Six of the
    fifteen documents are page images with an OCR text layer, and the method
    column calls them text because a text layer exists; a bar drawn in the
    picture is invisible to that instrument. The figure stands as measured
    until the trigger for the image method is decided, and the decision is
    recorded in docs/VERIFIERAT.md before any of it is published.

    The split by method is pinned with them, because it is the part that says
    how much weight each fraction can carry. Every scanned class A document is
    judged masked, which is what a detector with a known false positive rate
    produces when it is pointed at a template with a logo on page one, and the
    born-digital half is the half measured by an instrument checked by hand.
    """

    def shares(self, masking) -> dict[tuple[str, str], tuple[int, int]]:
        counted: dict[tuple[str, str], list[int]] = {}
        for record in masking:
            klass = record["path"].split("/")[0].rpartition("_")[2]
            if klass not in {"A", "B"}:
                continue
            key = (klass, record["method"])
            cell = counted.setdefault(key, [0, 0])
            cell[0] += 1
            cell[1] += bool(record["masked"])
        return {k: (v[1], v[0]) for k, v in counted.items()}

    def test_the_two_published_fractions(self, masking):
        found = self.shares(masking)
        pairs = zip(found[("A", "text")], found[("A", "image")], strict=True)
        a = tuple(sum(x) for x in pairs)
        pairs = zip(found[("B", "text")], found[("B", "image")], strict=True)
        b = tuple(sum(x) for x in pairs)
        assert a == (109, 170)
        assert b == (32, 140)

    # ADR-0019 and ADR-0020 state these numbers, and the ADRs are what a reader
    # checks the measure against. A threshold quietly retuned in the code would
    # move a published figure while both documents still read as if nothing had
    # changed.
    THRESHOLDS: ClassVar[dict[str, float]] = {
        "MIN_BOX_HEIGHT": 3.0,
        "ARMS_X": 130.0,
        "ARMS_Y": 80.0,
        "BAND_LEFT": 81.0,
        "BAND_RIGHT": 513.0,
        "BAND_MAX_HEIGHT": 36.0,
        "BAND_MIN_SPAN": 400.0,
    }

    def test_the_exclusions_keep_the_thresholds_their_decisions_name(self):
        # Read out of the source rather than imported: step 18 needs pdfplumber
        # and pymupdf, which the test environment deliberately does not install.
        source = (ROOT / "pipeline" / "18_analyse_masking.py").read_text("utf-8")
        found: dict[str, float] = {}
        for node in ast.parse(source).body:
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                # Some of them are written as one tuple assignment per pair,
                # because the pair is what the decision names.
                names = target.elts if isinstance(target, ast.Tuple) else [target]
                values = (
                    node.value.elts
                    if isinstance(node.value, ast.Tuple)
                    else [node.value]
                )
                if len(names) != len(values):
                    continue
                for name, value in zip(names, values, strict=True):
                    if isinstance(name, ast.Name) and name.id in self.THRESHOLDS:
                        found[name.id] = ast.literal_eval(value)
        assert found == self.THRESHOLDS

    def test_the_split_between_the_two_methods(self, masking):
        found = self.shares(masking)
        assert found[("A", "text")] == (79, 140)
        assert found[("A", "image")] == (30, 30)
        assert found[("B", "text")] == (21, 125)
        assert found[("B", "image")] == (11, 15)


class TestTheP9CriteriaRestOnQuotedGrounds:
    """P9 turns on which provision each authority invoked, so it is quoted.

    Criterion (c) is a null: no authority masked class B under 30 kap. 23 §.
    A null that lives in someone's memory is a null that drifts, and this one
    decides whether an appeal is required, so it is pinned against the quoted
    grounds rather than against a recollection.
    """

    GROUND_30_23 = "30 kap. 23 § OSL"

    def test_every_ground_is_traceable_to_a_message(self, grounds):
        for record in grounds:
            if record["kalla_ej_atkomlig"]:
                continue
            assert record["meddelande_id"]
            assert record["citat"].strip()
            assert record["klass"] in {"A", "B"}
            assert isinstance(record["citat_fullstandigt"], bool)

    def test_criterion_c_is_empty(self, grounds):
        klass_b = [
            r
            for r in grounds
            if r["klass"] == "B" and self.GROUND_30_23 in r["bestammelser"]
        ]
        assert klass_b == []

    def test_criterion_b_has_a_comparison_set(self, masking):
        # (b) needs at least three other counties releasing class A unmasked.
        # Five until 1 September 2026, when the header band was excluded from
        # the text method and Västerbotten's reports turned out to carry no
        # redaction at all. The set may grow again as the image method is
        # repaired; it is pinned so that it cannot shrink unnoticed, because a
        # shrinking comparison set weakens every appeal resting on (b).
        clean = set()
        for record in masking:
            folder = record["path"].split("/")[0]
            county, _, klass = folder.rpartition("_")
            if klass == "A" and not record["masked"]:
                clean.add(county)
        assert len(clean) == 8
        # Blekinge and Norrbotten joined on 29 September 2026 with their own
        # class A deliveries, four and ten unmasked documents.
        assert clean == {
            "blekinge",
            "dalarna",
            "gavleborg",
            "norrbotten",
            "jamtland",
            "sodermanland",
            "uppsala",
            "vasterbotten",
        }

    def test_the_counties_invoking_30_23_in_class_a(self, grounds):
        # Dalarna joined on 2 October 2026, when every quote in the register was
        # read against its source e-mail. Its row had been cut off mid-sentence
        # at "I en", and the rest of the county's own letter invokes 30 kap.
        # 23 § and offers an appealable decision. Tillämpningsnot 6 names eight
        # counties; the correction makes it nine, and the note carries a dated
        # addition saying so.
        counties = {
            r["myndighet"]
            for r in grounds
            if r["klass"] == "A" and self.GROUND_30_23 in r["bestammelser"]
        }
        assert counties == {
            "Dalarna",
            "Gotland",
            "Halland",
            "Kalmar",
            "Kronoberg",
            "Södermanland",
            "Värmland",
            "Västernorrland",
            "Västra Götaland",
        }

    def test_the_p8_list_is_the_intersection(self, grounds):
        # Not 4 is conjunctive: the criterion and the authority's own offer.
        # Six counties were sent a P8 letter in August 2026. Two more meet the
        # conjunction and were not: Dalarna and Värmland, whose offers of an
        # appealable decision sat in the part of the covering letter the
        # register had not stored. The set below is therefore what qualified,
        # not what was sent, and the difference is reported as a deviation in
        # the dated addition to tillämpningsnot 6.
        triggered = {
            r["myndighet"]
            for r in grounds
            if r["klass"] == "A"
            and self.GROUND_30_23 in r["bestammelser"]
            and r["erbjudet_beslut"]
        }
        assert triggered == {
            "Dalarna",
            "Gotland",
            "Halland",
            "Kalmar",
            "Kronoberg",
            "Södermanland",
            "Värmland",
            "Västra Götaland",
        }
        sent = {
            "Gotland",
            "Halland",
            "Kalmar",
            "Kronoberg",
            "Södermanland",
            "Västra Götaland",
        }
        assert triggered - sent == {"Dalarna", "Värmland"}


class TestTheGroundsRegisterKnowsItsOwnGaps:
    """The register of cited grounds is hand-curated, so its holes are pinned.

    Every row is one authority's own sentence, copied out of a covering e-mail
    by hand. Nothing generates it, which is legitimate, as it is for the
    hand-read annex labels, but only if the population is declared and the gap
    is visible. Criterion (c) of P9 is a negative claim, and a negative claim
    over a set nobody has bounded is worth nothing. These tests bound it.

    Coverage is asserted as a number and as a list. The list is the point: it
    can only shrink by someone reading the missing e-mail and adding the row,
    never by the population quietly changing underneath.
    """

    COUNTIES: ClassVar[dict[str, str]] = {
        "blekinge": "Blekinge",
        "dalarna": "Dalarna",
        "gotland": "Gotland",
        "gavleborg": "Gävleborg",
        "halland": "Halland",
        "jamtland": "Jämtland",
        "jonkoping": "Jönköping",
        "kalmar": "Kalmar",
        "kronoberg": "Kronoberg",
        "norrbotten": "Norrbotten",
        "skane": "Skåne",
        "stockholm": "Stockholm",
        "sodermanland": "Södermanland",
        "uppsala": "Uppsala",
        "varmland": "Värmland",
        "vasterbotten": "Västerbotten",
        "vasternorrland": "Västernorrland",
        "vastmanland": "Västmanland",
        "vastra_gotaland": "Västra Götaland",
        "orebro": "Örebro",
        "ostergotland": "Östergötland",
    }
    MISSING: ClassVar[set[tuple[str, str]]] = set()
    # Two rows outlived the population they were drawn from. Both were entered
    # while the text method still counted the template's black table header as
    # a redaction; with the header excluded on 1 September 2026 neither county
    # has a masked class A document left. The rows stay, because each one is an
    # authority's own covering sentence and both cite no provision at all,
    # which is exactly what a delivery without redaction looks like.
    # A third row joined them on 1 October 2026 for a different reason:
    # Gävleborg's one masked class B document was masked on the word "avmaskat"
    # and nothing else, and the word boundary took it away. The county's two
    # rows are the same covering sentence, which cites no provision either, so
    # the same reasoning holds for B as for A.
    UNMASKED_AFTER_THE_CORRECTION: ClassVar[set[tuple[str, str]]] = {
        ("Gävleborg", "A"),
        ("Gävleborg", "B"),
        ("Jämtland", "A"),
    }

    def population(self, masking) -> set[tuple[str, str]]:
        """Every county and class with at least one masked document."""
        found = set()
        for record in masking:
            if not record["masked"]:
                continue
            folder = record["path"].split("/")[0]
            county, _, klass = folder.rpartition("_")
            if klass in {"A", "B"} and county in self.COUNTIES:
                found.add((self.COUNTIES[county], klass))
        return found

    @staticmethod
    def traceable(provision: str, quote: str) -> bool:
        """Whether the provision can be read out of the quote it came from."""
        numbers = re.findall(r"\d+", provision)
        stem = provision.split()[0].casefold()[:5]
        if not numbers:
            return stem in quote.casefold()
        if len(numbers) < 2:
            return numbers[0] in quote and stem in quote.casefold()
        # Every occurrence, not only the first: a decision that cites two
        # provisions from the same chapter puts "2 kap." in the quote more
        # than once, and stopping at the first match would call the second
        # provision invented.
        for marker in re.finditer(
            rf"\b{numbers[0]}\s*(kap\.?|kapitel|:)", quote, re.IGNORECASE
        ):
            window = quote[marker.end() : marker.end() + 40]
            if re.search(rf"\b{numbers[1]}\b", window):
                return True
        return False

    def test_every_row_is_well_formed(self, grounds):
        for record in grounds:
            assert record["klass"] in {"A", "B"}
            # One covering e-mail cannot be located through the mailbox API, so
            # its row carries no message id. Its quote was pasted from the
            # mailbox by hand, which is why the flag allows a missing id and a
            # missing quote but never requires either.
            if not record["kalla_ej_atkomlig"]:
                assert record["meddelande_id"]
                assert record["citat"].strip()
            assert isinstance(record["bestammelser"], list)
            assert isinstance(record["citat_fullstandigt"], bool)
            assert isinstance(record["erbjudet_beslut"], bool)

    def test_no_provision_is_invented(self, grounds):
        # A provision recorded without its quote is the failure this catches;
        # one row carried 21 kap. 1 § from a paragraph that had not been stored.
        for record in grounds:
            for provision in record["bestammelser"]:
                assert self.traceable(provision, record["citat"]), (
                    f"{record['myndighet']} {record['klass']}: {provision}"
                )

    def test_no_row_without_a_masked_delivery(self, grounds, masking):
        covered = {(r["myndighet"], r["klass"]) for r in grounds}
        assert covered - self.population(masking) == self.UNMASKED_AFTER_THE_CORRECTION

    def test_the_register_is_closed(self, grounds, masking):
        covered = {(r["myndighet"], r["klass"]) for r in grounds}
        population = self.population(masking)
        # Both numbers moved by one on 28 September 2026, when a masked class
        # B delivery from Kalmar was found unlogged and unarchived: one masked
        # delivery joins the population and one hand-copied row joins the
        # register. The population lost one again on 1 October 2026, when
        # Gävleborg B left it with the word boundary, so the gap is three rows
        # rather than two. The register itself never shrinks: a row is an
        # authority's own sentence, and the sentence was said.
        assert len(population) == 24
        assert len(covered) == 27
        assert population - covered == self.MISSING


class TestTheRegisterExtractCountsKeeperRows:
    """A row in the request C extract is an animal keeper, not a control.

    The authority stated it on 24 August 2026: a control with two keepers becomes
    two rows. The extract carries four columns and no identifier, so nothing can
    collapse the rows onto controls, and every figure derived from it is a figure
    over keeper rows. The unit is easy to lose, because a column called
    kontroller reads as a count of controls to everyone who did not read the
    covering e-mail. These tests keep the name honest and the arithmetic sound.
    """

    def test_the_count_is_named_for_what_it_counts(self, deficiency):
        for record in deficiency:
            assert "rader" in record
            assert "kontroller" not in record

    def test_the_test_cells_carry_the_same_name(self, unannounced):
        for record in unannounced:
            assert "rader_brist" in record
            assert "kontroller_brist" not in record

    def test_no_cell_finds_more_faults_than_it_has_rows(self, deficiency):
        for record in deficiency:
            assert 0 <= record["med_brist"] <= record["rader"]
            assert record["andel_brist"] == round(
                record["med_brist"] / record["rader"], 3
            )

    def test_the_two_sides_of_the_test_stay_apart(self, unannounced):
        # The announced share counts controls and the deficiency share counts
        # keeper rows. They may not be summed, averaged or otherwise pooled, and
        # the row count must never stand in for the announced denominator.
        for record in unannounced:
            assert record["aviserade"] + record["oaviserade"] >= 0
            if record["andel_oanmalda"] is not None:
                total = record["aviserade"] + record["oaviserade"]
                share = round(record["oaviserade"] / total, 4)
                assert record["andel_oanmalda"] == share

    def test_the_limit_is_written_where_a_reader_meets_the_figures(self):
        readme = (ROOT / "README.md").read_text("utf-8")
        assert "counts animal keepers, not controls" in readme
        verified = (ROOT / "docs" / "VERIFIERAT.md").read_text("utf-8")
        assert "En rad är en djurhållare vid en kontroll, inte en kontroll" in verified


class TestTheAnnouncedReportsCarryAKnownFault:
    """One of the 336 reports holds another county's figure, and that is pinned.

    K_2024_oanmalda_gris.skv contains Länsbokstav W and is identical in content
    to W_2024_oanmalda_gris.skv, so Dalarna is counted twice and Blekinge's
    unannounced pig controls for 2024 never arrived. The delivery has the right
    number of files, so nothing about the count betrays it. Pinning the skew
    means a corrected delivery breaks this test and forces the note to be
    rewritten, rather than quietly changing a figure nobody re-derives.
    """

    def test_every_county_has_sixteen_reports_except_the_two(self, announced):
        by_letter = Counter(record["lansbokstav"] for record in announced)
        assert len(announced) == 336
        assert by_letter["K"] == 15
        assert by_letter["W"] == 17
        rest = {k: v for k, v in by_letter.items() if k not in {"K", "W"}}
        assert set(rest.values()) == {16}
        assert len(by_letter) == 21

    def test_the_duplicated_cell_is_the_one_named_in_the_note(self, announced):
        seen = Counter(
            (r["myndighet"], r["checklista"], r["år"], r["aviserad"]) for r in announced
        )
        assert [k for k, v in seen.items() if v > 1] == [
            ("Dalarna", "Gris", 2024, False)
        ]


class TestEveryRefusalDecisionIsInTheRegister:
    """P9 ranks appeals against each other, so the decisions need a register.

    The protocol allows five appeals for A and B together and orders them by
    criterion and then by falling deviation. Ranking needs every decision in one
    place, with the grounds it cites and the data type it names, both verbatim.
    The population is not a judgement call: it is every avslagsbeslut in the
    protocol log, so a decision cannot be received and then quietly left out.
    """

    def test_the_register_covers_every_logged_decision(self, decisions, protocol):
        logged = {
            (row["myndighet"], row["begaran"])
            for row in protocol
            if row["handelse"]
            in {"avslagsbeslut mottaget", "delvis avslagsbeslut mottaget"}
        }
        held = {(row["myndighet"], row["klass"]) for row in decisions}
        assert held == logged

    def test_every_decision_carries_its_own_words(self, decisions):
        for record in decisions:
            assert record["citat_bestammelser"].strip()
            assert record["citat_bedomning"].strip()
            assert record["bestammelser"]
            # Tillämpningsnot 6: criterion (b) may only be pursued where the
            # decision itself names the masked data type.
            if "b" in record["p9_kriterier"]:
                assert record["uppgiftstyp_namngiven"]
                assert record["citat_uppgiftstyp"].strip()

    def test_no_provision_is_invented(self, decisions):
        for record in decisions:
            for provision in record["bestammelser"]:
                assert TestTheGroundsRegisterKnowsItsOwnGaps.traceable(
                    provision, record["citat_bestammelser"]
                )

    def test_a_registered_case_carries_its_number(self, decisions, protocol):
        # The report reads the running court cases out of the register, so a
        # case number that stays in the log is a case nobody watches. On
        # 23 September 2026 Jordbruksverket's row lacked 3339-26, registered
        # thirteen days earlier, and the watch found three cases where there
        # were four.
        registered = {
            (row["myndighet"], row["begaran"])
            for row in protocol
            if row["handelse"] == "målregistrering i kammarrätten"
        }
        held = {
            (row["myndighet"], row["klass"]): row.get("malnummer") for row in decisions
        }
        for key in registered:
            assert key in held, f"{key} har en målregistrering utan beslutsrad"
            assert held[key], (
                f"{key} har en målregistrering i loggen men inget malnummer i "
                "registret, så bevakningen av målet räknar det inte"
            )

    def test_the_five_appeal_cap_is_not_exceeded(self, decisions):
        appealed = [r for r in decisions if r["overklagas"]]
        assert len(appealed) <= 5

    def test_the_appeal_forum_the_protocol_names(self, decisions):
        # P9 sends the appeal to kammarrätten. Where a decision says otherwise
        # the difference is recorded rather than reconciled, because which court
        # a decision points at is itself a measurement of the openness layer.
        for record in decisions:
            assert record["instans_enligt_p9"] == "kammarrätten"


class TestTheSwedishDatasetsShareOnePopulation:
    """Every derived Swedish dataset must cover the documents it claims to.

    Steps 18, 20, 21 and 26 read the same delivery folder at different times, and
    a delivery that lands between two runs leaves one of them behind. That is not
    hypothetical: on 26 August 2026 an audit found `djurslag.jsonl` one document
    short of `maskning.jsonl`, a Södermanland report delivered on 17 August after
    step 20 had last run. Nothing in the repository noticed for nine days. The
    figures did not move, but nothing guaranteed that.

    Step 18 is the spine, because it reads the folder itself and judges every
    file. The others are checked against it.
    """

    def paths(self, records) -> set[str]:
        return {record["path"] for record in records}

    def test_the_species_step_covers_every_delivered_document(self, masking, species):
        assert self.paths(species) == self.paths(masking), (
            "step 20 and step 18 disagree about which documents exist; re-run "
            "the later one rather than editing either file"
        )

    def test_the_hidden_text_measure_covers_the_born_digital_documents(
        self, masking, hidden_text
    ):
        # Step 26 compares a text layer to the rendered page, so a scan has
        # nothing to compare. Its population is exactly the born-digital set.
        born_digital = {r["path"] for r in masking if r["method"] == "text"}
        assert self.paths(hidden_text) == born_digital

    def test_the_contrast_counts_every_document_it_can_place(
        self, masking, species, contrast
    ):
        # A document reaches the contrast only if it is in a request class and
        # the rule named a species for it. Both conditions are derivable, so the
        # total is not a number anyone has to remember.
        dominant = {r["path"]: r["dominant"] for r in species}
        placeable = sum(
            1
            for record in masking
            if record["path"].split("/")[0].rpartition("_")[2] in {"A", "B"}
            # .get, so a missing document fails the population test above
            # with a useful message instead of crashing here.
            and dominant.get(record["path"]) is not None
        )
        assert sum(cell["dokument"] for cell in contrast) == placeable

    def test_the_hand_read_sample_still_points_at_documents_that_exist(
        self, species, species_sample
    ):
        # The sample is never redrawn, so it must keep resolving. A document
        # vanishing from step 20 would silently shrink the check.
        assert self.paths(species_sample) <= self.paths(species)


class TestTheDenominatorRegisterKeepsEachCountysOwnReading:
    """P11's answers are not one quantity, so each reading is recorded.

    Tillämpningsnot 9 of 29 September 2026 settled what to do when an authority
    asks whether hobby flocks belong in the count: the question's own words are
    repeated, no reading is prescribed, and the reading each authority used is
    recorded instead. The register is hand-copied from the log's verbatim
    quotes, like the grounds register, which is legitimate only while its
    population is pinned and its arithmetic is nobody's but the authority's.

    The rule that matters most here is the one a future run could quietly
    break: **nothing in this file is summed.** Västra Götaland reported 18
    controls of flocks above 350 laying hens and 425 below; adding them would
    invent a figure the county never wrote and would merge two readings the
    note keeps apart. Kalmar reported 48 förelägganden and 16 with a penalty,
    and the same applies.
    """

    READINGS: ClassVar[set[str]] = {
        "utan storleksgräns",
        "över 350 värphöns",
        "okänd",
        "kan inte tas fram",
    }

    def test_every_answer_in_the_log_has_a_row(self, denominators):
        from open_items import load

        answered = {
            row["myndighet"].removeprefix("Länsstyrelsen i ")
            for row in load()
            if row["handelse"] == "svar på nämnarfrågan"
        }
        assert {r["myndighet"] for r in denominators} == answered

    def test_every_row_is_well_formed(self, denominators):
        for record in denominators:
            assert record["lasning_fjaderfa"] in self.READINGS
            assert record["meddelande_id"]
            assert record["citat"].strip()
            assert isinstance(record["kontroller"], dict)
            assert isinstance(record["forelagganden"], dict)
            if record["kan_inte_tas_fram"]:
                assert not record["kontroller"]
                assert not record["forelagganden"]

    def test_no_figure_is_a_sum_of_two_readings(self, denominators):
        # Västra Götaland is the only county that reported both size
        # categories, and the two must stay apart. A key holding their sum, or
        # a plain fjäderfä key beside them, would be arithmetic the county
        # never did.
        west = next(r for r in denominators if r["myndighet"] == "Västra Götaland")
        above = west["kontroller"]["värphöns fler än 350 st"]
        below = west["kontroller"]["värphöns färre än 350 st"]
        assert (above, below) == (18, 425)
        assert above + below not in west["kontroller"].values()
        assert not any(key.strip() == "fjäderfä" for key in west["kontroller"])

    def test_the_two_counties_that_cannot_answer_are_named(self, denominators):
        missing = {
            r["myndighet"]
            for r in denominators
            if r["lasning_fjaderfa"] == "kan inte tas fram"
        }
        assert missing == {"Skåne", "Norrbotten"}


class TestTheRulesWrittenOnDay41AreStillWhereTheyWereWritten:
    """Two rules were written before they were applied, so they are pinned.

    Both were written on 29 September 2026: tillämpningsnot 9 on the
    denominator's size reading, and the addition to note 7 saying that a
    delivery after day 40 does not reopen the response-time measure. A rule
    that lives only in a commit message is a rule that quietly stops applying,
    and the second one is carried out by code, which makes the pair worth
    guarding together.
    """

    def test_note_nine_is_in_the_protocol(self):
        text = (ROOT / "docs" / "BEGARANMALL.md").read_text("utf-8")
        assert "Tillämpningsnot 9, 2026-09-29" in text
        assert "Läsningen registreras per län" in text
        assert "Bara lika jämförs med lika" in text

    def test_the_addition_to_note_seven_is_in_the_protocol(self):
        text = (ROOT / "docs" / "BEGARANMALL.md").read_text("utf-8")
        assert "Tillägg 2026-09-29: en leverans som kommer efter dag 40" in text
        assert "öppnar inte det stängda måttet" in text

    def test_the_packet_builder_carries_the_censoring(self):
        source = (ROOT / "pipeline" / "36_build_p12_packets.py").read_text("utf-8")
        assert "MEASURE_CLOSES = 40" in source
        assert "censurerad" in source

    def test_the_packet_builder_takes_slutstatus_from_the_measure(self):
        # The builder kept its own list of what ends a request, and it drifted
        # from the measure's: on 1 October 2026 it lacked "avgiftsbeslut
        # mottaget" and "leverans fullgjord", so three packets told their own
        # authority the request was not concluded although Skåne's and Örebro's
        # fee decisions had arrived and Västmanland's delivery was logged as
        # complete. Built from the measure's sets, the two cannot drift apart
        # again without this test failing.
        source = (ROOT / "pipeline" / "36_build_p12_packets.py").read_text("utf-8")
        assert "set(DELIVERY_COMPLETED)" in source
        assert "set(DECISION_CLOSERS)" in source

    def test_the_contrast_keeps_its_decimal(self):
        # Printed as a whole number the contrast overstated two counties' own
        # figure in a letter about them: Södermanland's 4,5 points read as 5
        # and Uppsala's 55,9 as 56.
        source = (ROOT / "pipeline" / "36_build_p12_packets.py").read_text("utf-8")
        assert "def points(value: float)" in source
        assert "points((share_a - share_b) * 100)" in source


class TestTheHandReadingOfTheDisagreeingDocumentsStands:
    """Eight documents were read by hand, and the verdict is pinned to them.

    ADR-0023 rejected the image-method trigger and said the disagreement it
    exposed would be settled by hand. It was, on 29 September 2026, against a
    criterion written to the protocol log first: three verdicts were available,
    maskning, fotografi or osäker, and all eight came back fotografi. The
    verdict is what holds class A at 109 of 170, so it is pinned here: a later
    run that quietly turns one of these documents into a redaction has to break
    this test and rewrite the facit rather than move a published figure.
    """

    VERDICTS: ClassVar[set[str]] = {"maskning", "fotografi", "osäker"}

    def test_every_hand_read_document_is_judged(self, image_reading):
        # Eight came from the threshold trial. The ninth, Västerbotten's
        # 11096-2025, came from the screen over all 35 false alarms the image
        # method produces on born-digital documents: it is the only one outside
        # the trial's selection with a bar that lies outside every picture on
        # its page, so it was read by hand on the same criterion.
        assert len(image_reading) == 9
        assert {r["path"].split("/")[0] for r in image_reading} == {
            "jamtland_A",
            "norrbotten_A",
            "vasterbotten_A",
        }
        for record in image_reading:
            assert record["dom"] in self.VERDICTS
            assert record["sidor_sedda"]
            assert record["notering"].strip()

    def test_not_one_bar_was_a_redaction(self, image_reading):
        assert {r["dom"] for r in image_reading} == {"fotografi"}

    def test_the_second_reading_covers_every_bar(self, image_reading):
        # 496 of 503 bars sit inside a raster image; the seven that do not run
        # across the seam between two adjacent pictures and were checked one by
        # one. Both figures are pinned, because the gap between them is the
        # part that needed a human.
        assert sum(r["balkar"] for r in image_reading) == 503
        assert sum(r["balkar_inuti_bild"] for r in image_reading) == 496

    def test_the_documents_are_the_ones_the_text_method_calls_clean(
        self, image_reading, masking
    ):
        judged = {r["path"] for r in image_reading}
        for record in masking:
            stem = record["path"].rsplit("/", 1)
            folder = stem[0]
            for path in judged:
                start = path.split("/")[1]
                if folder == path.split("/")[0] and stem[1].startswith(start):
                    assert record["masked"] is False


class TestTheDenominatorQuestionStaysOffTheRequestTracks:
    """P11 is not one of the 43 requests, so its events may not sit on them.

    Tillämpningsnot 7 says it in as many words: the denominator question is a
    follow-up, P2 and P3 do not apply to it, and it carries no deadline. Logged
    under begaran "A+B" its events landed on the request tracks anyway, where
    they reopened requests delivered weeks earlier and produced a P4 deadline
    the note denies. That corrupts the one reading that decides when the
    collection is closed, so the separation is guarded here.
    """

    def test_no_denominator_event_reaches_a_request(self):
        from open_items import by_request, is_p11, load

        rows = load()
        for events in by_request(rows).values():
            assert not [event for event in events if is_p11(event)]

    def test_every_county_asked_is_on_the_denominator_track(self):
        from open_items import denominator_track, load

        track = denominator_track(load())
        asked = {
            authority
            for authority, events in track.items()
            if any(event["handelse"] == "nämnarfråga" for event in events)
        }
        assert len(asked) == 21

    def test_the_rows_written_before_the_names_existed_are_named(self):
        # The log is append-only, so these three carry the old wording for ever
        # and the reader holds the exception. Naming them keeps the exception
        # from quietly growing into a rule that swallows P4 questions about the
        # requests themselves. Halland's answer to its own question joined the
        # set on 2 October 2026: it was written under the old name too, and
        # without it the P12 packet could not tell an answered question from an
        # open one.
        from open_items import P11_SUPERSEDED

        assert P11_SUPERSEDED == frozenset(
            {
                ("Länsstyrelsen i Halland", "2026-09-29", "09:59"),
                ("Länsstyrelsen i Halland", "2026-09-29", "16:22:13"),
                ("Länsstyrelsen i Västerbotten", "2026-09-30", "10:42"),
            }
        )
