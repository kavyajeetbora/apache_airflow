from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': "KVBA",
    'retries': 5,   
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_with_cron_expression_v3',
    default_args= default_args,
    description="This is my first DAG in airflow. DAG - Directed Acyclic Graph",
    start_date = datetime(2023,10,20),
    schedule_interval="0 3 * * Tue,Fri"
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo hello world, this is our first task with cron expression"
    )

    task1
