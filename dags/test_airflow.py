from airflow.sdk import dag, task
from datetime import datetime

@dag(
    dag_id = "test_airflow",
    start_date=datetime(2026, 9, 25),
    schedule=None,
    catchup=False
)

def test_airflow():
    @task
    def hello():
        print("Airflow work")
    hello()

test_airflow()