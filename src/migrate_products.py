from databases import get_postgres_connection, get_mysql_connection


def migrate_products():
    mysql_conn = get_mysql_connection()
    postgres_conn = get_postgres_connection()

    mysql_cursor = mysql_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    try:
        mysql_cursor.execute("""
        SELECT 
            product_id,
            sku,
            product_name,
            category,
            price,
            stock_quantity,
            created_at,
            updated_at
        FROM products
        ORDER BY product_id
        """)

        products = mysql_cursor.fetchall()
        print(f"len(products) = {len(products)} products found in MySQL")

        insert_query = """
        INSERT INTO products (
            product_id,
            sku,
            product_name,
            category,
            price,
            stock_quantity,
            created_at,
            updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        postgres_cursor.executemany(insert_query, products)
        postgres_conn.commit()

        print(f"{len(products)} products TO PostgreSQL")

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
    migrate_products()