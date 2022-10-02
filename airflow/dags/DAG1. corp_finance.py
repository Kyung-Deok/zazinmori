# 에어플로우
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.dummy import DummyOperator
from pendulum import yesterday
from func import _get_fin
from datetime import datetime

tdy = datetime.today()

dag = DAG(
    dag_id='finance',
    schedule_interval='@yearly',
    start_date=yesterday('Asia/Seoul')
)

# task 지정
start_task=DummyOperator(
    task_id='start_task',
    dag=dag
)

get_fin_task=PythonOperator(
    task_id='get_fin_task',
    python_callable=_get_fin,
    dag=dag
)

put_hdfs_task=BashOperator(
    task_id='put_hdfs_task',
    bash_command=f'hdfs dfs -put update/corp_findata{tdy}.csv update/',
    dag=dag
)

spark_submit_task=SparkSubmitOperator(
    task_id='spark_submit_task',
    application='pyspark/corpfin_update.py',
    conn_id='spark_default',
    dag=dag
)

end_task=DummyOperator(
    task_id='end_task',
    dag=dag
)

# 디펜던시
start_task >> get_fin_task >> put_hdfs_task >> spark_submit_task >> end_task