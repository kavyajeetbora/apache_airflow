from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import sklearn
import matplotlib
from airflow.decorators import dag, task

default_args = {
    'owner': 'KVBA',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    dag_id = "dag_with_py_ext_lib_v2",
    default_args = default_args,
    start_date  = datetime(2023,10,31),
    schedule = "0 12 * * Mon"
)
def sklearn_etl():

    @task()
    def sklearn_version():
        print(sklearn.__version__)

    @task()
    def get_matplotlib():
        print(matplotlib.__version__)
    
    sklearn_version()
    get_matplotlib()

sklearn_dag = sklearn_etl()
