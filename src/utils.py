from src.databases import get_mysql_connection, get_postgres_connection
from logs.logger import get_logger


logger = get_logger("migration")

INCREMENTAL_COLUMNS = {
    "customers": "updated_at",
    "products": "updated_at",
    "orders": "updated_at",
    "order_items": "updated_at"
}


def migrate_table(table_name, select_query, insert_query, batch_size=1000):
    mysql_conn = get_mysql_connection()
    postgres_conn = get_postgres_connection()

    mysql_cursor = mysql_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    total = 0

    try:
        logger.info(f"{table_name}: migration started")

        last_sync = get_last_sync(postgres_cursor, table_name)

        if last_sync is None:
            mode = "full"
            resume_value = get_checkpoint(postgres_cursor, table_name)
            logger.info(f"{table_name}: full migration starting after checkpoint {resume_value}")
        else:
            mode = "incremental"
            resume_value = last_sync
            logger.info(f"{table_name}: incremental migration starting after {resume_value}")

        while True:
            if mode == "full":
                mysql_cursor.execute(select_query, (resume_value, batch_size))
                rows = mysql_cursor.fetchall()

                if not rows:
                    last_sync = get_source_last_sync(mysql_cursor, table_name)

                    if last_sync is not None:
                        save_last_sync(postgres_cursor, table_name, last_sync)
                        postgres_conn.commit()

                    break

                postgres_cursor.executemany(insert_query, rows)

                resume_value = rows[-1][0]
                save_checkpoint(postgres_cursor, table_name, resume_value)

                postgres_conn.commit()
                total += len(rows)

                logger.info(
                    f"{table_name}: {len(rows)} rows migrated "
                    f"| total={total} | checkpoint={resume_value}"
                )

            else:
                rows = get_incremental_rows(
                    mysql_cursor,
                    table_name,
                    resume_value,
                    batch_size
                )

                if not rows:
                    logger.info(f"{table_name}: no new or updated rows found")
                    break

                postgres_cursor.executemany(insert_query, rows)

                resume_value = max(row[-1] for row in rows)
                save_last_sync(postgres_cursor, table_name, resume_value)

                postgres_conn.commit()
                total += len(rows)

                logger.info(
                    f"{table_name}: {len(rows)} rows synchronized "
                    f"| total={total} | last_sync={resume_value}"
                )

        logger.info(f"{table_name}: migration completed ({total} rows processed)")

    except Exception:
        postgres_conn.rollback()
        logger.exception(f"{table_name}: migration failed")
        raise

    finally:
        mysql_cursor.close()
        postgres_cursor.close()
        mysql_conn.close()
        postgres_conn.close()


def get_incremental_rows(mysql_cursor, table_name, last_sync, batch_size):
    updated_column = INCREMENTAL_COLUMNS.get(table_name)

    if updated_column is None:
        logger.info(f"{table_name}: incremental migration is not available")
        return []

    query = f"""
        SELECT *
        FROM {table_name}
        WHERE {updated_column} > %s
        ORDER BY {updated_column}
        LIMIT %s
    """

    mysql_cursor.execute(query, (last_sync, batch_size))
    return mysql_cursor.fetchall()


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
    return 0 if result is None else result[0]


def save_checkpoint(postgres_cursor, table_name, last_processed_id):
    postgres_cursor.execute(
        """
        INSERT INTO migration_checkpoints (table_name, last_processed_id, updated_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (table_name)
        DO UPDATE SET
            last_processed_id = EXCLUDED.last_processed_id,
            updated_at = CURRENT_TIMESTAMP
        """,
        (table_name, last_processed_id)
    )


def get_last_sync(postgres_cursor, table_name):
    postgres_cursor.execute(
        """
        SELECT last_sync
        FROM migration_sync_state
        WHERE table_name = %s
        """,
        (table_name,)
    )

    result = postgres_cursor.fetchone()
    return None if result is None else result[0]


def save_last_sync(postgres_cursor, table_name, last_sync):
    postgres_cursor.execute(
        """
        INSERT INTO migration_sync_state (table_name, last_sync)
        VALUES (%s, %s)
        ON CONFLICT (table_name)
        DO UPDATE SET last_sync = EXCLUDED.last_sync
        """,
        (table_name, last_sync)
    )


def get_source_last_sync(mysql_cursor, table_name):
    mysql_cursor.execute(f"SELECT MAX(updated_at) FROM {table_name}")
    result = mysql_cursor.fetchone()
    return result[0]