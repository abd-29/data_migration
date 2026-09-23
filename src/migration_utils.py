from databases import get_mysql_connection, get_postgres_connection


def migrate_table(table_name, select_query, insert_query, batch_size=1000, crash=None):
    mysql_conn = get_mysql_connection()
    postgres_conn = get_postgres_connection()

    mysql_cursor = mysql_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    total, batch = 0, 0

    try:
        checkpoint = get_checkpoint(postgres_cursor, table_name)

        print(f"{table_name}: starting after checkpoint {checkpoint}")

        while True:
            mysql_cursor.execute(select_query, (checkpoint, batch_size))
            rows = mysql_cursor.fetchall()

            if not rows:
                break

            postgres_cursor.executemany(insert_query, rows)

            last_processed_id = rows[-1][0]

            save_checkpoint(postgres_cursor, table_name, last_processed_id)
            postgres_conn.commit()

            checkpoint = last_processed_id

            total += len(rows)
            batch += 1

            print(
                f"{table_name}: "
                f"{len(rows)} rows migrated "
                f"| total={total} "
                f"| checkpoint={checkpoint}"
            )

            if crash is not None and batch >= crash:
                raise RuntimeError(f"SIMULATED CRASH after {batch} batches")

        print(
            f"{table_name}: migration completed "
            f"({total} rows processed)"
        )

    except Exception:
        postgres_conn.rollback()
        print(f"{table_name}: ERROR DURING MIGRATION")
        raise

    finally:
        mysql_cursor.close()
        postgres_cursor.close()

        mysql_conn.close()
        postgres_conn.close()


def get_checkpoint(postgres_cursor, table_name):
    postgres_cursor.execute(
        """
        SELECT last_processed_id
        FROM migration_checkpoints
        WHERE table_name = %s
        """,
        (table_name,)
    )

    result = postgres_cursor.fetchone()

    if result is None:
        return 0

    return result[0]


def save_checkpoint(postgres_cursor, table_name, last_processed_id):
    postgres_cursor.execute(
        """
        INSERT INTO migration_checkpoints (
            table_name,
            last_processed_id,
            updated_at
        )
        VALUES (%s, %s, CURRENT_TIMESTAMP)

        ON CONFLICT (table_name)
        DO UPDATE SET
            last_processed_id = EXCLUDED.last_processed_id,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            table_name,
            last_processed_id
        )
    )