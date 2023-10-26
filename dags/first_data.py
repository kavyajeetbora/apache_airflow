from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': "KVBA",
    'retries': 5,   
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='first_dag_v2',
    default_args= default_args,
    description="This is my first DAG in airflow. DAG - Directed Acyclic Graph",
    start_date = datetime(2023,10,26, 17,0,0),
    schedule_interval="@daily"
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo hello world, this is our first task"
    )

    task2 = BashOperator(
        task_id="second_task",
        bash_command="echo hello world, this is our second task and it will run after task1"
    )

    task1.set_downstream(task2)
