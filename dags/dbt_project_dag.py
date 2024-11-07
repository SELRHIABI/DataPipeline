from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=5),
}

# Define the DAG
with DAG(
    'dbt_project_dag',
    default_args=default_args,
    description='A DAG to orchestrate dbt project tasks with Great Expectations validations',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
    tags=['dbt', 'great_expectations'],
    max_active_runs=1,
    concurrency=1,
) as dag:

    # Task to run dbt deps
    dbt_deps = BashOperator(
        task_id='dbt_deps',
        bash_command='cd /opt/dbt && dbt deps',
    )

    # Task to run dbt seed
    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command='cd /opt/dbt && dbt seed',
    )

    # Task to run dbt run
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/dbt && dbt run',
    )

    # Task to run dbt test
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/dbt && dbt test',
    )

    # Task to generate dbt docs
    dbt_docs_generate = BashOperator(
        task_id='dbt_docs_generate',
        bash_command='cd /opt/dbt && dbt docs generate',
    )

    # Great Expectations validation task for the obt_sales table
    ge_validate_obt_sales = BashOperator(
        task_id='ge_validate_obt_sales',
        bash_command='cd /opt/dbt && great_expectations checkpoint run obt_sales_checkpoint',
    )

    # Define task dependencies with GE validation after dbt_run
    dbt_deps >> dbt_seed >> dbt_run >> dbt_test >> ge_validate_obt_sales >> dbt_docs_generate
