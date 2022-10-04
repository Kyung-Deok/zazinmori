# 에어플로우
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.dummy import DummyOperator
from pendulum import yesterday
from func import _get_news, _get_total
from datetime import datetime

tdy = datetime.today()

dag = DAG(
    dag_id='topic&corporation',
    schedule_interval='@weekly',
    start_date=yesterday('Asia/Seoul')
)

# task 지정
start_task=DummyOperator(
    task_id='start_task',
    dag=dag
)

get_news_task=PythonOperator(
    task_id='get_news_task',
    python_callable=_get_news,
    dag=dag
)

get_total_task=PythonOperator(
    task_id='get_total_task',
    python_callable=_get_total,
    dag=dag
)

put_hdfs_task1=BashOperator(
    task_id='put_hdfs_task',
    bash_command=f'hdfs dfs -put update/corp_news{tdy}.csv update/',
    dag=dag
)

put_hdfs_task2=BashOperator(
    task_id='put_hdfs_task',
    bash_command='hdfs dfs -put update/corp_total*.csv update/',
    dag=dag
)


spark_submit_task=SparkSubmitOperator(
    task_id='spark_submit_task',
    application='pyspark/topic&corp_update.py',
    conn_id='spark_default',
    dag=dag
)

end_task=DummyOperator(
    task_id='end_task',
    dag=dag
)

# 디펜던시
start_task >> [get_news_task, get_total_task]
get_news_task >> put_hdfs_task1
get_total_task >> put_hdfs_task2
[put_hdfs_task1, put_hdfs_task2] >> spark_submit_task >> end_task