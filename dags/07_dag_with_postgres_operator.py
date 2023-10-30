from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': "KVBA",
    'retries': 5,   
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id = 'dag_with_postgres_operator_v3',
    default_args=default_args,
    start_date = datetime(2023,10,30),
    schedule_interval="0 0 * * *"
) as dag:
    task1 = PostgresOperator(
        task_id = 'create_postgres_table',
        postgres_conn_id = "BH_training_db",
        sql = '''
            create table if not exists public.airflow_dag_runs (
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )
        '''
    )

    task2 = PostgresOperator(
        task_id = 'insert_into_table',
        postgres_conn_id = 'BH_training_db',
        sql = '''
            insert into public.airflow_dag_runs (dt, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}');
        '''
    )

    task3 = PostgresOperator(
        task_id = "delete_from_table",
        postgres_conn_id = "BH_training_db",
        sql = '''
            delete from public.airflow_dag_runs where dt = '{{ ds }}' and dag_id = '{{ dag.dag_id }}';
        '''
    )
    
    ## Delete the entry if already there then insert the new record
    task1 >> task3 >> task2