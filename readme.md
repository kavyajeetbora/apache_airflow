<a href="https://airflow.apache.org/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/AirflowLogo.png/1200px-AirflowLogo.png" height=100></a>

## what is airflow ?

Airflow is an open-source platform for orchestrating and automating complex workflows and data pipelines, represented as directed acyclic graphs (DAGs). It enables users to define, schedule, and monitor the execution of tasks in a flexible and extensible manner.

## Installing airflow with Docker

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Sva8rDtlWi4/0.jpg)](https://www.youtube.com/watch?v=Sva8rDtlWi4)

## Airflow Core Concept

Workflow is sequence of task. Workflow is defined as DAG in airflow. DAG - Directed Acyclic Graph

![](https://miro.medium.com/v2/resize:fit:828/format:webp/1*a1WQzfZwrh8FQmfr2CHNJw.png)

## Airflow Task Life Cycle

The possible states for a Task Instance are:

- **None**: The Task has not yet been queued for execution (its dependencies are not yet met)
- **Scheduled**: The scheduler has determined the Task’s dependencies are met and it should run
- **Queued**: The task has been assigned to an Executor and is awaiting a worker
- **running**: The task is running on a worker (or on a local/synchronous executor)
- **success**: The task finished running without errors
- **restarting**: The task was externally requested to restart when it was running
- **failed**: The task had an error during execution and failed to run
- **skipped**: The task was skipped due to branching, LatestOnly, or similar.
- **upstream_failed**: An upstream task failed and the Trigger Rule says we needed it
- **up_for_retry**: The task failed, but has retry attempts left and will be rescheduled.
- **up_for_reschedule**: The task is a Sensor that is in reschedule mode
- **deferred**: The task has been deferred to a trigger
- **removed**: The task has vanished from the DAG since the run started

## BashOperators

Use the BashOperator to execute commands in a Bash shell.

Syntax:

```python
run_this = BashOperator(
    task_id="run_after_loop",
    bash_command="echo 1",
)
```

## PythonOperators

Use the @task decorator to execute Python callables.

Syntax:

```python
def function(args):
    return args

run_this = PythonOperator(
    task_id="run_after_loop",
    python_callable=function
)
```

## Data Sharing via Airflow XComs ?

Xcoms are used for sharing data between task. But the downside is that the maximum limit is 48KB only

- Pushing one return value from a task:

```python
def get_pincode():
    return 122011
```

- Pushing multiple values to xcoms from a task:

```python
def get_name(ti):
    ti.xcom_push(key="first_name", value="Kavyajeet")
    ti.xcom_push(key='last_name', value="Bora")
```

- To retrieve the values:

```python
first_name = ti.xcom_pull(task_ids = "return_to_xcoms", key="first_name")
last_name = ti.xcom_pull(task_ids = "return_to_xcoms", key="last_name")
pincode = ti.xcom_pull(task_ids='get_pincode')
```

## Airflow Taskflow API

The TaskFlow API was introduced in Airflow 2.0 and is a wonderful alternative to PythonOperator.

The TaskFlow API offers a number of benefits over the traditional PythonOperator. Some of the most obvious are:

- Reduced boilerplate code
- Intuitive data transfer between DAGs
- No unnecessary code for explicit dependency chain
- Simplified task instantiation
- No need to provide task id
- Elimination of xcoms

Here is an example showing how taskflow api simplifies the code:

<img src="https://miro.medium.com/v2/resize:fit:786/0*OsZaXXCxL5FlLlD5" height=500/>

[Reference](https://medium.com/apache-airflow/unleashing-the-power-of-taskflow-api-in-apache-airflow-371637089141)

**Summary**

If you are using Python to perform tasks in your workflows, TaskFlow methods make a great replacement for the PythonOperator. They reduce boilerplate code and simplify your DAGs, while still being able to interact with your other Operators.

## Airflow Catchup and Backfill

By default, Airflow will run any past scheduled intervals that have not been run.

<img src="https://miro.medium.com/v2/resize:fit:786/format:webp/1*8foi9cV4CLUixQO7M7hrrw.png" height=400/>

## Airflow Scheduler with Cron Expression

A cron expression is a string of fields separated by spaces, representing a schedule in time. Each field represents a unit of time, and the special character '\*' is used to mean "any". In the context of Apache Airflow, the cron expression is used in the schedule_interval parameter when defining a DAG

**Why use cron expression in scheduling task ?**

While datetime and timedelta can be used for scheduling tasks in Airflow, they are better suited for situations where you have relatively simple and fixed scheduling requirements. For more complex and recurring scheduling needs, cron expressions offer a more efficient and maintainable approach. Airflow natively supports cron-style scheduling in its ScheduleInterval parameter, making it a convenient choice for defining task schedules.

You can create cron expression using this web tool: [Cronitor](https://crontab.guru/)

<img src="https://miro.medium.com/v2/resize:fit:1358/1*3KXqWXyDBN7QUwURIBbfYg.gif" height=400/>

## Airflow connection to Postgres

The purpose of PostgresOperator is to define tasks involving interactions with a PostgreSQL database.

- First setup the postgres connection on airflow UI:

<img src="https://i.stack.imgur.com/VbRsL.png" height=400/>

- Use the connection id to pass it as an argument in the postgresoperator:

```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG(
    dag_id = 'dag_with_postgres_operator_v3',
    default_args=default_args,
    start_date = datetime(2023,10,30),
    schedule_interval="0 0 * * *"
) as dag:
    task1 = PostgresOperator(
        task_id = 'create_postgres_table',
        postgres_conn_id = "BH_training_db",  ## Enter the connection id from step 1
        ## Type SQL command to be executed:
        sql = '''
            create table if not exists public.airflow_dag_runs (
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )
        '''
        =
    )
```

[Here is a comprehensive guide on how to guide for PostgresOperator](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators/postgres_operator_howto_guide.html)

## Installing python packages in Airflow

There are two ways of installing python packages:

1. Docker Image Extending - This is the recommended way, it is fast and simple to execute

Follow the steps to install the python packages to the airflow docker image:

- first create a requirement.txt file in the parent directory where in all python external libraries are written with version as shown:
  <img src="https://miro.medium.com/v2/resize:fit:1116/1*jqwf3sUzzfpdVpYv3DwOxw.png" height=400/>

- Create a Docker file, extending the airflow docker image:

```Dockerfile
# Install python packages on top of airflow image
FROM apache/airflow:2.7.2
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt
```

To build this docker image in the Docker local hub, type the following in the terminal:

```git
docker build . --tag <<name of the docker image>>
```

This will build the docker image with the python packages installed in it

- Now initiate the airflow image from the official docker compose file

```
docker-compose up airflow-init
```

- Now start the image:

```
docker-compose up
```

2. Image Customizing
