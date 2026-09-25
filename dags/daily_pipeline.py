from airflow.sdk import dag, task
from datetime import datetime
import subprocess


@dag(
    dag_id="daily_data_pipeline",
    start_date=datetime(2026, 9, 25),
    schedule="0 6 * * *",
    catchup=False
)
def daily_data_pipeline():

    @task
    def generate_data():
        subprocess.run(["python", "/opt/airflow/src/data.py"], check=True)

    @task
    def migrate_data():
        subprocess.run(["python", "/opt/airflow/src/migration_tables.py"], check=True)

    @task
    def validation_data():
        subprocess.run(["python", "/opt/airflow/src/validation.py"], check=True)

    generate = generate_data()
    migrate = migrate_data()
    validate = validation_data()

    generate >> migrate >> validate


daily_data_pipeline()