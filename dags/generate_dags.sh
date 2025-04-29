#!/bin/bash
mkdir -p ~/crdp-net/airflow/dags
for region in jakarta nyc london sydney saopaulo; do
  cat << EOF > ~/crdp-net/airflow/dags/${region}_pipeline.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    '${region}_pipeline',
    default_args=default_args,
    description='Pipeline for ${region} region',
    schedule_interval=timedelta(minutes=5),
    start_date=datetime(2025, 4, 29),
    catchup=False,
) as dag:

    check_data = BashOperator(
        task_id='check_data_${region}',
        bash_command='echo "Checking data for ${region}"',
    )

    check_data
EOF
done
