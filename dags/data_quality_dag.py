"""
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'data_quality_dag',
    default_args=default_args,
    description='A DAG to run data quality checks with Great Expectations',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
    tags=['data_quality'],
    max_active_runs=1,  # Ensure only one run is active at a time
    concurrency=1, 
) as dag:

    run_great_expectations = BashOperator(
        task_id='run_great_expectations',
        bash_command='cd /opt/dbt && great_expectations checkpoint run GX-person_checkpoint',
    )
"""