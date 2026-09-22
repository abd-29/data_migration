import mysql.connector
import psycopg2

MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3307,
    "user": "user",
    "password": "password",
    "database": "mysqldb",
}

POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "user": "user",
    "password": "password",
    "database": "postgresdb",
}


def get_mysql_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

def get_postgres_connection():
    return psycopg2.connect(**POSTGRES_CONFIG)


def migrate_customers():
    mysql_conn = get_mysql_connection()
    postgres_conn = get_postgres_connection()

    mysql_cursor = mysql_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    try:
        mysql_cursor.execute("""
        SELECT 
            customer_id,
            first_name,
            last_name,
            email,
            country,
            created_at,
            updated_at
        FROM customers
        ORDER BY customer_id
        """)

        customers = mysql_cursor.fetchall()
        print(f"len(customers) = {len(customers)} clients found in MySQL")

        insert_query = """
        INSERT INTO customers (
            customer_id,
            first_name, 
            last_name, 
            email, 
            country, 
            created_at, 
            updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        postgres_cursor.executemany(insert_query, customers)
        postgres_conn.commit()

        print(f"{len(customers)} clients TO PostgreSQL")

    except Exception as e:
        postgres_conn.rollback()

        print("ERROR DURING MIGRATION")
        print(e)

    finally:
        mysql_cursor.close()
        postgres_cursor.close()

        mysql_conn.close()
        postgres_conn.close()


if __name__ == "__main__":
    migrate_customers()