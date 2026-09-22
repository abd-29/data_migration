from faker import Faker
import random
import mysql.connector
from datetime import datetime

fake = Faker("fr_FR")

DB_CONFIG = {
    "host": "localhost",
    "port": 3307,
    "user": "user",
    "password": "password",
    "database": "mysqldb"
}

NB_CUSTOMERS = 5_000
NB_PRODUCTS = 500
NB_ORDERS = 20_000


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def insert_customers(cursor):
    customers = []

    for _ in range(NB_CUSTOMERS):
        email = fake.email()

        # insertion d'anomalies
        if random.random() < 0.01:
            email = None

        customers.append(
            (
                fake.first_name(),
                fake.last_name(),
                email,
                fake.country(),
                fake.date_time_between(start_date="-3y", end_date="now")
            )
        )

    query = """
        INSERT INTO customers
        (
            first_name,
            last_name,
            email,
            country,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.executemany(query, customers)

    print(f"{len(customers)} clients insérés")


def insert_products(cursor):
    products = []

    categories = [
        "informatique",
        "telephone",
        "audio",
        "maison",
        "sport",
        "livres",
        "accessoires"
    ]

    for i in range(NB_PRODUCTS):
        products.append(
            (
                f"SKU-{i + 1:05d}",
                fake.catch_phrase(),
                random.choice(categories),
                round(random.uniform(5, 1500), 2),
                random.randint(0, 500)
            )
        )

    query = """
        INSERT INTO products
        (
            sku,
            product_name,
            category,
            price,
            stock_quantity
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.executemany(query, products)

    print(f"{len(products)} produits insérés")


def insert_orders(cursor):
    statuses = [
        "pending",
        "paid",
        "shipped",
        "delivered",
        "cancelled"
    ]

    orders = []

    for _ in range(NB_ORDERS):
        customer_id = random.randint(1, NB_CUSTOMERS)

        total_amount = round(
            random.uniform(10, 3000),
            2
        )

        order_date = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )

        orders.append(
            (
                customer_id,
                random.choice(statuses),
                total_amount,
                order_date,
                order_date
            )
        )

    query = """
        INSERT INTO orders
        (
            customer_id,
            order_status,
            total_amount,
            order_date,
            updated_at
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.executemany(query, orders)

    print(f"{len(orders)} commandes insérées")


def insert_order_items(cursor):
    order_items = []

    for order_id in range(1, NB_ORDERS + 1):

        nb_items = random.randint(1, 5)

        for _ in range(nb_items):
            product_id = random.randint(1, NB_PRODUCTS)

            quantity = random.randint(1, 4)

            unit_price = round(
                random.uniform(5, 1500),
                2
            )

            order_items.append(
                (
                    order_id,
                    product_id,
                    quantity,
                    unit_price
                )
            )

    query = """
        INSERT INTO order_items
        (
            order_id,
            product_id,
            quantity,
            unit_price
        )
        VALUES (%s, %s, %s, %s)
    """

    cursor.executemany(query, order_items)

    print(f"{len(order_items)} lignes de commande insérées")


def main():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        print("Début du chargement...")

        insert_customers(cursor)
        insert_products(cursor)
        insert_orders(cursor)
        insert_order_items(cursor)

        connection.commit()

        print("Chargement terminé avec succès.")

    except Exception as e:
        connection.rollback()

        print("Erreur pendant le chargement :")
        print(e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()