import subprocess
from src.databases import get_mysql_connection


def database_is_empty():
    connection = get_mysql_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        return count == 0
    finally:
        cursor.close()
        connection.close()


def main():
    if database_is_empty():
        print("Empty database detected. Initializing data...")
        subprocess.run(["python", "/opt/airflow/src/seed_data.py"], check=True)
        print("Initial data created")
    else:
        print("Database already initialized. Skipping seed data.")


if __name__ == "__main__":
    main()