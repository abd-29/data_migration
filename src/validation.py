from databases import get_mysql_connection, get_postgres_connection
from logs.logger import get_logger


logger = get_logger("validation")


TABLES = [
    "customers",
    "products",
    "orders",
    "order_items"
]


def get_row_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]


def validate_row_counts():
    mysql_conn = get_mysql_connection()
    postgres_conn = get_postgres_connection()

    mysql_cursor = mysql_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    try:
        for table_name in TABLES:
            mysql_count = get_row_count(mysql_cursor, table_name)
            postgres_count = get_row_count(postgres_cursor, table_name)

            if mysql_count == postgres_count:
                logger.info(
                    f"{table_name}: validation passed "
                    f"| MySQL={mysql_count} | PostgreSQL={postgres_count}"
                )
            else:
                logger.error(
                    f"{table_name}: validation failed "
                    f"| MySQL={mysql_count} | PostgreSQL={postgres_count}"
                )

    finally:
        mysql_cursor.close()
        postgres_cursor.close()
        mysql_conn.close()
        postgres_conn.close()


if __name__ == "__main__":
    validate_row_counts()