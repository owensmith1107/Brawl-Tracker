from dagster import Definitions, ScheduleDefinition, define_asset_job, AssetSelection
from dagster_dbt import DbtCliResource
from pathlib import Path
from orchestration.assets import raw_battles, brawl_dbt_assets

DBT_PROJECT_DIR = Path(__file__).parent.parent / "brawl_dbt"

# Job that runs everything end to end
full_pipeline_job = define_asset_job(
    name="full_pipeline",
    selection=AssetSelection.all(),
    description="Fetch new battles then run dbt transformations"
)

# Run every 3 hours
pipeline_schedule = ScheduleDefinition(
    job=full_pipeline_job,
    cron_schedule="0 * * * *",
    name="every_3_hours"
)

defs = Definitions(
    assets=[raw_battles, brawl_dbt_assets],
    schedules=[pipeline_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=str(DBT_PROJECT_DIR))
    }
)