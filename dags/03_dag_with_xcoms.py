from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'KVBA',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

def get_name(ti):
    ti.xcom_push(key="first_name", value="Kavyajeet")
    ti.xcom_push(key='last_name', value="Bora")

def get_pincode():
    return 122011

def greet(ti):
    first_name = ti.xcom_pull(task_ids = "return_to_xcoms", key="first_name")
    last_name = ti.xcom_pull(task_ids = "return_to_xcoms", key="last_name")
    pincode = ti.xcom_pull(task_ids='get_pincode')

    print(f"Hello {first_name} {last_name}. Address: {pincode}")

with DAG(
    dag_id = "dag_with_xcoms_v3",
    default_args=default_args,
    start_date=datetime(2023,10,31),
    schedule_interval = "0 0 * * *"
) as dag:
    task1 = PythonOperator(
        task_id = 'return_to_xcoms',
        python_callable= get_name
    )

    task3 = PythonOperator(
        task_id = "get_pincode",
        python_callable = get_pincode
    )


    task2 = PythonOperator(
        task_id = "greet",
        python_callable=greet
    )

    [task1, task3] >> task2

