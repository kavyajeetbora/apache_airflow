# Airflow

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

![](https://miro.medium.com/v2/resize:fit:786/format:webp/1*8foi9cV4CLUixQO7M7hrrw.png)

## Airflow Scheduler with Cron Expression

A cron expression is a string of fields separated by spaces, representing a schedule in time. Each field represents a unit of time, and the special character '\*' is used to mean "any". In the context of Apache Airflow, the cron expression is used in the schedule_interval parameter when defining a DAG

**Why use cron expression in scheduling task ?**

While datetime and timedelta can be used for scheduling tasks in Airflow, they are better suited for situations where you have relatively simple and fixed scheduling requirements. For more complex and recurring scheduling needs, cron expressions offer a more efficient and maintainable approach. Airflow natively supports cron-style scheduling in its ScheduleInterval parameter, making it a convenient choice for defining task schedules.

You can create cron expression using this web tool: [Cronitor](https://crontab.guru/)

![](https://miro.medium.com/v2/resize:fit:1358/1*3KXqWXyDBN7QUwURIBbfYg.gif)

## Airflow connection to Postgres
