from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator


with DAG(
    dag_id="empty_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["hw23"],
):
    start = EmptyOperator(task_id="start")


with DAG(
    dag_id="single_task_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["hw23"],
):
    single = EmptyOperator(task_id="only_task")


with DAG(
    dag_id="dependent_tasks_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["hw23"],
):
    first = EmptyOperator(task_id="first_task")
    second = EmptyOperator(task_id="second_task")
    third = EmptyOperator(task_id="third_task")

    first >> second >> third

