from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from config import Config as cfg


default_args = {
    'owner': 'Derek Herincx',
    'depends_on_past': False,
    'start_date': datetime.today(),
    'email': ['derek663@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


dag = DAG(
    dag_id='healthcare_api_dag',
    default_args=default_args,
    schedule_interval='0 * * * *',
    description="Healthcare API in Airflow"
)
