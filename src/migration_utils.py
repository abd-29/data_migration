from databases import get_mysql_connection, get_postgres_connection


def migrate_table(table_name, select_query, insert_query, batch_size=1000):
    mysql_conn = get_mysql_connection()
    postgres_conn = get_postgres_connection()

    mysql_cursor = mysql_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    total = 0

    try:
        mysql_cursor.execute(select_query)

        while True:
            rows = mysql_cursor.fetchmany(batch_size)

            if not rows:
                break

            postgres_cursor.executemany(insert_query, rows)
            postgres_conn.commit()

            total += len(rows)

            print(
                f"{table_name}: "
                f"{len(rows)} rows migrated "
                f"| total={total}"
            )

        print(
            f"{table_name}: migration completed "
            f"({total} rows processed)"
        )

    except Exception:
        postgres_conn.rollback()
        raise

    finally:
        mysql_cursor.close()
        postgres_cursor.close()

        mysql_conn.close()
        postgres_conn.close()