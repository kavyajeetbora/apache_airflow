from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    'owner': 'KVBA',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    dag_id="dag_with_taskflow_api_v2",
    default_args=default_args,
    start_date=datetime(2023,10,27),
    schedule='@daily'
)
def hello_world_etl():
    

    @task(multiple_outputs=True)
    def get_name():
        return {
            "first_name": "Arpita",
            "last_name": "Das"
        }
    
    @task()
    def get_age():
        return 61
    
    @task()
    def greet(first_name, last_name,  age):
        print(f"Hello my name is {first_name} {last_name} and I am {age} years old.") 

    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], last_name=name_dict['last_name'], age=age)

## Create an instance of the DAG to initiate
greet_dag = hello_world_etl()