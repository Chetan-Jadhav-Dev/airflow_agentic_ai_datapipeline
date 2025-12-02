from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def failing_task():
    raise Exception("This is a simulated failure for testing the AI Troubleshooter.")

with DAG(
    'example_failing_dag',
    default_args=default_args,
    description='A DAG that always fails',
    schedule_interval=timedelta(days=1),
) as dag:

    t1 = PythonOperator(
        task_id='failing_task',
        python_callable=failing_task,
    )
