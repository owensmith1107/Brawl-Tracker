import subprocess
import sys
from dagster import asset, AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

DBT_PROJECT_DIR = Path(__file__).parent.parent / "brawl_dbt"


@asset(group_name="ingestion", description="Fetch latest battles from Brawl Stars API and insert into PostgreSQL")
def raw_battles(context: AssetExecutionContext):
    result = subprocess.run(
        [sys.executable, "-m", "ingestion.poller"],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent.parent)
    )
    if result.returncode != 0:
        raise Exception(f"Poller failed:\n{result.stderr}")
    context.log.info(result.stdout.strip())
    return result.stdout.strip()


dbt_resource = DbtCliResource(project_dir=str(DBT_PROJECT_DIR))


@dbt_assets(manifest=DBT_PROJECT_DIR / "target" / "manifest.json")
def brawl_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run"], context=context).stream()