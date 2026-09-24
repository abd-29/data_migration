from src.data import generate_customers, get_customer_ids, get_products


class FakeCursor:
    def __init__(self, fetchall_result=None):
        self.fetchall_result = fetchall_result or []
        self.executed_query = None
        self.executed_params = None
        self.executemany_query = None
        self.executemany_params = None

    def execute(self, query, params=None):
        self.executed_query = query
        self.executed_params = params

    def executemany(self, query, params):
        self.executemany_query = query
        self.executemany_params = params

    def fetchall(self):
        return self.fetchall_result

def test_get_customer_ids():
    cursor = FakeCursor([(1,), (2,), (3,)])

    result = get_customer_ids(cursor)

    assert result == [1, 2, 3]
    assert "SELECT customer_id FROM customers" in cursor.executed_query


def test_get_products():
    cursor = FakeCursor([(1, 10.50), (2, 20.00)])

    result = get_products(cursor)

    assert result == [(1, 10.50), (2, 20.00)]
    assert "FROM products" in cursor.executed_query
    assert "stock_quantity > 0" in cursor.executed_query

def test_generate_customers():
    cursor = FakeCursor()

    generate_customers(cursor)

    assert cursor.executemany_query is not None
    assert "INSERT INTO customers" in cursor.executemany_query
    assert len(cursor.executemany_params) >= 5
    assert len(cursor.executemany_params) <= 20