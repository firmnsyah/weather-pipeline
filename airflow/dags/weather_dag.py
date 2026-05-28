from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data-engineer",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="weather_pipeline",
    description="Ingest cuaca -> load Postgres -> transform dbt",
    schedule="0 6 * * *",          # tiap hari jam 06:00
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["weather", "portfolio"],
) as dag:

    ingest = BashOperator(
        task_id="ingest",
        bash_command="cd /opt/project && python -m ingestion.fetch_weather",
    )
    load = BashOperator(
        task_id="load",
        bash_command="cd /opt/project && python -m load.load_to_postgres",
    )
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/project/dbt/weather_dbt && dbt run",
    )
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/project/dbt/weather_dbt && dbt test",
    )

    ingest >> load >> dbt_run >> dbt_test