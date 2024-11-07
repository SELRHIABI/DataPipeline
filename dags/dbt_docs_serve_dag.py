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
    'dbt_docs_serve_dag',
    default_args=default_args,
    description='A DAG to serve dbt docs',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['dbt'],
) as dag:

    dbt_docs_serve = BashOperator(
        task_id='dbt_docs_serve',
        bash_command='cd /opt/dbt && nohup dbt docs serve --port 8001 --host 0.0.0.0 > /opt/dbt/dbt_docs.log 2>&1 &',
    )

    wait = BashOperator(
        task_id='wait',
        bash_command='sleep 3600',  # Wait for 1 hour
    )

    stop_dbt_docs_serve = BashOperator(
        task_id='stop_dbt_docs_serve',
        bash_command='pkill -f "dbt docs serve"',
    )
"""