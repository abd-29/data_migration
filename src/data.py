import random
from faker import Faker

from src.databases import get_mysql_connection


fake = Faker("fr_FR")

MIN_NEW_CUSTOMERS = 5
MAX_NEW_CUSTOMERS = 20

MIN_NEW_ORDERS = 50
MAX_NEW_ORDERS = 150

MIN_ITEMS_PER_ORDER = 1
MAX_ITEMS_PER_ORDER = 5

MIN_STATUS_UPDATES = 5
MAX_STATUS_UPDATES = 20


def generate_customers(cursor):
    number_of_customers = random.randint(MIN_NEW_CUSTOMERS, MAX_NEW_CUSTOMERS)

    customers = []

    for _ in range(number_of_customers):
        customers.append(
            (
                fake.first_name(),
                fake.last_name(),
                fake.email(),
                fake.country()
            )
        )

    query = """
    INSERT INTO customers (
        first_name,
        last_name,
        email,
        country
    )
    VALUES (%s, %s, %s, %s)
    """

    cursor.executemany(query, customers)

    print(f"{number_of_customers} new customers created")


def get_customer_ids(cursor):
    cursor.execute("SELECT customer_id FROM customers")
    return [row[0] for row in cursor.fetchall()]


def get_products(cursor):
    cursor.execute("""
        SELECT product_id, price
        FROM products
        WHERE stock_quantity > 0
    """)

    return cursor.fetchall()


def generate_orders(cursor):
    customer_ids = get_customer_ids(cursor)
    products = get_products(cursor)

    number_of_orders = random.randint(MIN_NEW_ORDERS, MAX_NEW_ORDERS)

    for _ in range(number_of_orders):
        customer_id = random.choice(customer_ids)

        cursor.execute(
            """
            INSERT INTO orders (
                customer_id,
                order_status,
                total_amount
            )
            VALUES (%s, %s, %s)
            """,
            (
                customer_id,
                "pending",
                0
            )
        )

        order_id = cursor.lastrowid

        number_of_items = random.randint(
            MIN_ITEMS_PER_ORDER,
            MAX_ITEMS_PER_ORDER
        )

        selected_products = random.sample(
            products,
            number_of_items
        )

        total_amount = 0

        for product_id, unit_price in selected_products:
            quantity = random.randint(1, 4)

            cursor.execute(
                """
                INSERT INTO order_items (
                    order_id,
                    product_id,
                    quantity,
                    unit_price
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    order_id,
                    product_id,
                    quantity,
                    unit_price
                )
            )

            total_amount += quantity * unit_price

        cursor.execute(
            """
            UPDATE orders
            SET total_amount = %s
            WHERE order_id = %s
            """,
            (
                total_amount,
                order_id
            )
        )

    print(f"{number_of_orders} new orders created")


def update_order_statuses(cursor):
    number_of_updates = random.randint(
        MIN_STATUS_UPDATES,
        MAX_STATUS_UPDATES
    )

    cursor.execute("""
        SELECT order_id, order_status
        FROM orders
        WHERE order_status != 'delivered'
          AND order_status != 'cancelled'
        ORDER BY RAND()
        LIMIT %s
    """, (number_of_updates,))

    orders = cursor.fetchall()

    status_transitions = {
        "pending": "paid",
        "paid": "shipped",
        "shipped": "delivered"
    }

    updated = 0

    for order_id, current_status in orders:
        new_status = status_transitions.get(current_status)

        if new_status is None:
            continue

        cursor.execute(
            """
            UPDATE orders
            SET order_status = %s
            WHERE order_id = %s
            """,
            (
                new_status,
                order_id
            )
        )

        updated += 1

    print(f"{updated} existing orders updated")


def main():
    connection = get_mysql_connection()
    cursor = connection.cursor()

    try:
        print("Starting daily data generation...")

        generate_customers(cursor)
        generate_orders(cursor)
        update_order_statuses(cursor)

        connection.commit()

        print("Daily data generation completed")

    except Exception as e:
        connection.rollback()

        print("ERROR DURING DATA GENERATION")
        print(e)

        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()