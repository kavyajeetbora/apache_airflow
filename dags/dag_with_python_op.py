from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'KVBA',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(name,age):
    print(f"Hello World!! My name is {name} and my age is {age}")

with DAG(
    default_args= default_args,
    dag_id = "python_operator_v2",
    description= "First Dag with python operator",
    start_date=datetime(2023,10,27),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'name': 'Kavyajeet Bora', 'age': 31}
    )

    task1