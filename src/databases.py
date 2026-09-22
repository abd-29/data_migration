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
