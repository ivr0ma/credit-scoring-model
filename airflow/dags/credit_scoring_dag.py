from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_data():
    print("Loading credit scoring data...")
    return "data_loaded"

def preprocess_data(**context):
    print("Preprocessing data...")
    return "data_preprocessed"

def train_model(**context):
    print("Training credit scoring model...")
    return "model_trained"

def evaluate_model(**context):
    print("Evaluating model...")
    return "model_evaluated"

with DAG(
    'credit_scoring_pipeline',
    default_args=default_args,
    description='Credit scoring ML pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['ml', 'credit-scoring'],
) as dag:

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    preprocess_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
    )

    train_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
    )

    evaluate_task = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model,
    )

    load_task >> preprocess_task >> train_task >> evaluate_task
