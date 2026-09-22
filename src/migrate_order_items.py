from databases import  get_mysql_connection, get_postgres_connection


def migrate_order_items():
    mysql_conn = get_mysql_connection()
    postgres_conn = get_postgres_connection()

    mysql_cursor = mysql_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    try:
        mysql_cursor.execute("""
        SELECT 
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price
        FROM order_items
        ORDER BY order_item_id
        """)

        order_items = mysql_cursor.fetchall()
        print(f"len(order_items) : {len(order_items)} order_items found in MySQL")
        insert_query = """
        INSERT INTO order_items (
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price)
        VALUES (%s, %s, %s, %s, %s)
        """

        postgres_cursor.executemany(insert_query, order_items)
        postgres_conn.commit()

        print(f"{len(order_items)} order_items TO PostgreSQL")

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
    migrate_order_items()