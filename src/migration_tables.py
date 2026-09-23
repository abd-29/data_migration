from migration_utils import migrate_table

# CUSTOMERS ------------------------------------------------
SELECT_CUSTOMERS = """
            SELECT
                customer_id,
                first_name,
                last_name,
                email,
                country,
                created_at,
                updated_at
            FROM customers            
            WHERE customer_id > %s
            ORDER BY customer_id
            LIMIT %s
        """

UPSERT_CUSTOMERS = """
            INSERT INTO customers (
                customer_id,
                first_name,
                last_name,
                email,
                country,
                created_at,
                updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)

            ON CONFLICT (customer_id)
            DO UPDATE SET
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                email = EXCLUDED.email,
                country = EXCLUDED.country,
                created_at = EXCLUDED.created_at,
                updated_at = EXCLUDED.updated_at
        """

# PRODUCTS -----------------------------------------------------------------
SELECT_PRODUCTS = """
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
        WHERE product_id > %s
        ORDER BY product_id
        LIMIT %s
        """

UPSERT_PRODUCTS = """
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

        ON CONFLICT (product_id) 
        DO UPDATE SET 
        sku = EXCLUDED.sku,
        product_name = EXCLUDED.product_name,
        category = EXCLUDED.category,
        price = EXCLUDED.price,
        stock_quantity = EXCLUDED.stock_quantity,
        created_at = EXCLUDED.created_at,
        updated_at = EXCLUDED.updated_at
        """

# ORDERS ---------------------------------------------------------
SELECT_ORDERS = """
        SELECT 
            order_id,
            customer_id,
            order_status,
            total_amount,
            order_date,
            updated_at
        FROM orders
        WHERE order_id > %s
        ORDER BY order_id
        LIMIT %s
        """

UPSERT_ORDERS = """
        INSERT INTO orders (
            order_id,
            customer_id,
            order_status,
            total_amount,
            order_date,
            updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)

        ON CONFLICT (order_id) 
        DO UPDATE SET 
            customer_id = EXCLUDED.customer_id,
            order_status = EXCLUDED.order_status,
            total_amount = EXCLUDED.total_amount,
            order_date = EXCLUDED.order_date,
            updated_at = EXCLUDED.updated_at
        """

# ORDER_ITEMS -----------------------------------------------------------
SELECT_ORDER_ITEMS = """
        SELECT 
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price
        FROM order_items
        WHERE order_item_id > %s
        ORDER BY order_item_id
        LIMIT %s
        """

UPSERT_ORDER_ITEMS = """
        INSERT INTO order_items (
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price)
        VALUES (%s, %s, %s, %s, %s)

        ON CONFLICT (order_item_id)
        DO UPDATE SET
            order_id = excluded.order_id,
            product_id = excluded.product_id,
            quantity = excluded.quantity,
            unit_price = excluded.unit_price
        """

TABLES = [
    ("customers", SELECT_CUSTOMERS, UPSERT_CUSTOMERS),
    ("products", SELECT_PRODUCTS, UPSERT_PRODUCTS),
    ("orders", SELECT_ORDERS, UPSERT_ORDERS),
    ("order_items", SELECT_ORDER_ITEMS, UPSERT_ORDER_ITEMS),
]

if __name__ == '__main__':
    for table_name, select_query, upsert_query in TABLES:
            migrate_table(
                table_name,
                select_query,
                upsert_query
            )

