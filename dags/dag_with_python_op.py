from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'KVBA',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(age, ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key="last_name")
    print(f"Hello World!! My name is {first_name} {last_name}, my age is {age}")

def get_name(ti):
    ti.xcom_push(key="first_name", value="Kabeer")
    ti.xcom_push(key='last_name', value="Bora")

with DAG(
    default_args= default_args,
    dag_id = "python_operator_v5",
    description= "First Dag with python operator",
    start_date=datetime(2023,10,27),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'age': 31}
    )

    task2 = PythonOperator(
        task_id = 'get_name',
        python_callable=get_name
    )

    task2 >> task1