"""Load the local star schema into BigQuery.

Step 12 of the pipeline; run 10_build_warehouse.py first. Uploads the Parquet
tables into the raw dataset that the dbt project reads from. The cloud copy is
a publication of the local model, never a second source of truth: this step
replaces the tables outright rather than merging into them, so a run can never
leave the two out of step.

Credentials are read from the environment, never from the repository:

    ANTUMBRA_GCP_PROJECT    the project id
    GOOGLE_APPLICATION_CREDENTIALS   path to the service account key file

Running without them prints what would be uploaded and exits without touching
anything, so the step can be checked before an account exists.

Usage:
    python pipeline/12_load_bigquery.py [--dataset dgsante_raw]
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAREHOUSE = ROOT / "data" / "warehouse"
DEFAULT_DATASET = "dgsante_raw"


def tables() -> list[Path]:
    """The Parquet tables written by step 10, in a stable order."""
    return sorted(WAREHOUSE.glob("*.parquet"))


def describe(paths: list[Path], dataset: str, project: str | None) -> None:
    """Print what a run would do."""
    where = f"{project}.{dataset}" if project else f"<project>.{dataset}"
    print(f"would replace {len(paths)} tables in {where}:")
    for path in paths:
        print(f"  {path.stem:22s} {path.stat().st_size // 1024:6d} KiB")


def load(paths: list[Path], dataset: str, project: str) -> int:
    """Replace each table in BigQuery with its local Parquet file."""
    from google.cloud import bigquery

    client = bigquery.Client(project=project)
    # The dbt profile declares location EU. Creating the dataset without a
    # location would default to US, and every downstream query would then
    # fail on the region mismatch.
    target_dataset = bigquery.Dataset(f"{project}.{dataset}")
    target_dataset.location = "EU"
    client.create_dataset(target_dataset, exists_ok=True)
    config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    for path in paths:
        target = f"{project}.{dataset}.{path.stem}"
        with path.open("rb") as handle:
            job = client.load_table_from_file(handle, target, job_config=config)
        job.result()
        print(f"{path.stem}: {client.get_table(target).num_rows} rows -> {target}")
    return 0


def main() -> int:
    """Upload the warehouse, or explain what is missing and stop."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the plan and exit without contacting BigQuery",
    )
    args = parser.parse_args()

    paths = tables()
    if not paths:
        print("no Parquet tables found; run pipeline/10_build_warehouse.py first")
        return 1

    project = os.environ.get("ANTUMBRA_GCP_PROJECT")
    key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if args.dry_run or not project or not key:
        describe(paths, args.dataset, project)
        if not args.dry_run:
            print()
            print("nothing was uploaded. set ANTUMBRA_GCP_PROJECT and")
            print("GOOGLE_APPLICATION_CREDENTIALS, then run again.")
        return 0
    return load(paths, args.dataset, project)


if __name__ == "__main__":
    sys.exit(main())
