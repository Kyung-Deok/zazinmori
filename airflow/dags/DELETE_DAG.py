from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from pendulum import yesterday

dag=DAG(
    dag_id='DELETE',
    schedule_interval='@monthly',
    start_date= yesterday('Asia/Seoul')
)

# task 1
start=DummyOperator(
    task_id='start',
    dag=dag
)

# task 2
local_clear=BashOperator(
    task_id='local_clear',
    bash_command='rm -r update/*',
    dag=dag
)

# task3
hdfs_clear=BashOperator(
    task_id='hdfs_clear',
    bash_command='hdfs dfs -rm -r update/*',
    dag=dag
)

# task 4
end=DummyOperator(
    task_id='end',
    dag=dag
)

# 디펜던시
start >> local_clear >> hdfs_clear >> end