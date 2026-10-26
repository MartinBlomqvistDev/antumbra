"""Structural checks on the dbt project.

dbt itself needs a warehouse and an account to run, so CI cannot execute the
models. What CI can do is hold the project to the things that would otherwise
break silently: that every model references something that exists, that the
sources match the tables the pipeline actually writes, and that the promises
made in the schema files are about columns the models select.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DBT = ROOT / "dbt"

REF = re.compile(r"\{\{\s*ref\(\s*'([^']+)'\s*\)\s*\}\}")
SOURCE = re.compile(r"\{\{\s*source\(\s*'([^']+)'\s*,\s*'([^']+)'\s*\)\s*\}\}")


BUILD_DIRS = {"dbt_packages", "target", "logs"}


def sql_files() -> list[Path]:
    """Every model and singular test in the project itself.

    Running dbt materialises installed packages and compiled output under
    dbt/; those are build artefacts, outside the project under test.
    """
    return sorted(
        path
        for path in DBT.rglob("*.sql")
        if BUILD_DIRS.isdisjoint(part.lower() for part in path.parts)
    )


def model_names() -> set[str]:
    """The models the project defines."""
    return {path.stem for path in (DBT / "models").rglob("*.sql")}


def warehouse_tables() -> set[str]:
    """The tables the local pipeline writes, from its committed manifest."""
    import json

    manifest = json.loads(
        (ROOT / "data" / "dgsante_warehouse_manifest.json").read_text("utf-8")
    )
    return {table["table"] for table in manifest["tables"]}


class TestTheProjectHangsTogether:
    def test_every_ref_points_at_a_model(self):
        known = model_names()
        for path in sql_files():
            for name in REF.findall(path.read_text("utf-8")):
                assert name in known, f"{path.name} refs unknown model {name}"

    def test_every_source_is_a_table_the_pipeline_writes(self):
        known = warehouse_tables()
        for path in sql_files():
            for _, table in SOURCE.findall(path.read_text("utf-8")):
                assert table in known, f"{path.name} reads unknown source {table}"

    def test_the_sources_file_covers_the_whole_warehouse(self):
        declared = set(
            re.findall(
                r"^\s*-\s*name:\s*(\w+)\s*$",
                (DBT / "models" / "staging" / "sources.yml").read_text("utf-8"),
                re.M,
            )
        )
        missing = warehouse_tables() - declared
        assert not missing, f"warehouse tables not declared as sources: {missing}"


class TestTheModelsKeepTheProjectsRules:
    @pytest.mark.parametrize(
        "model", ["mart_chain", "mart_country_year", "stg_citations"]
    )
    def test_a_mart_exists_for_each_promised_grain(self, model):
        assert next((DBT / "models").rglob(f"{model}.sql"), None) is not None, (
            f"{model} is documented but missing"
        )

    def test_the_chain_is_built_outwards_with_left_joins(self):
        """An inner join here would hide every recommendation that cites nothing.

        The count of what does not close is the result, so the mart must keep
        those rows rather than restricting itself to the part that does.
        """
        sql = (DBT / "models" / "marts" / "mart_chain.sql").read_text("utf-8")
        assert sql.count("left join") >= 2
        assert "chain_closes" in sql

    def test_shares_keep_their_numerator_and_denominator(self):
        """A ratio without its counts cannot be judged for thinness."""
        sql = (DBT / "models" / "marts" / "mart_country_year.sql").read_text("utf-8")
        for column in ("recommendations", "answered", "stating_their_basis"):
            assert column in sql
        assert "share_answered" in sql

    def test_the_singular_tests_guard_the_headline_claim(self):
        names = {path.stem for path in (DBT / "tests").glob("*.sql")}
        assert "a_closed_chain_has_its_parts" in names
        assert "citations_stay_within_their_audit" in names


class TestNoCredentialsAreCommitted:
    def test_the_profile_is_an_example_with_nothing_filled_in(self):
        text = (DBT / "profiles.example.yml").read_text("utf-8")
        assert "CHANGE-ME" in text
        assert "private_key" not in text

    def test_no_service_account_key_is_tracked(self):
        """The invariant guards the repository, and the local build is outside it.

        Running dbt writes lockfiles and manifests under dbt/ on disk, so the
        check asks git what is tracked rather than sweeping the filesystem.
        """
        import subprocess

        tracked = subprocess.run(
            ["git", "ls-files", "dbt"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        ).stdout.splitlines()
        keys = [path for path in tracked if path.endswith(".json")]
        assert not keys, f"a key file must never be committed: {keys}"
