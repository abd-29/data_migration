from databases import  get_mysql_connection, get_postgres_connection


def migrate_orders():
    mysql_conn = get_mysql_connection()
    postgres_conn = get_postgres_connection()

    mysql_cursor = mysql_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    try:
        mysql_cursor.execute("""
        SELECT 
            order_id,
            customer_id,
            order_status,
            total_amount,
            order_date,
            updated_at
        FROM orders
        ORDER BY order_id
        """)

        orders = mysql_cursor.fetchall()
        print(f"len(orders) = {len(orders)} orders found in MySQL")
        insert_query = """
        INSERT INTO orders (
            order_id,
            customer_id,
            order_status,
            total_amount,
            order_date,
            updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        postgres_cursor.executemany(insert_query, orders)
        postgres_conn.commit()

        print(f"{len(orders)} orders TO PostgreSQL")

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
    migrate_orders()