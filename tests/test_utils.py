from src.utils import get_checkpoint, get_last_sync, save_checkpoint, save_last_sync, get_source_last_sync, \
    get_incremental_rows


class FakeCursor:
    def __init__(self, result=None, results=None):
        self.result = result
        self.results = results or []

        self.executed_query = None
        self.executed_params = None

    def execute(self, query, params=None):
        self.executed_query = query
        self.executed_params = params

    def fetchone(self):
        return self.result

    def fetchall(self):
        return self.results


def test_get_checkpoint_existing():
    cursor = FakeCursor((5000,))

    result = get_checkpoint(cursor, "customers")

    assert result == 5000


def test_get_checkpoint_missing():
    cursor = FakeCursor(None)

    result = get_checkpoint(cursor, "customers")

    assert result == 0

def test_get_last_sync_existing():
    cursor = FakeCursor(("2026-09-24 14:00:00",))

    result = get_last_sync(cursor, "orders")

    assert result == "2026-09-24 14:00:00"


def test_get_last_sync_missing():
    cursor = FakeCursor(None)

    result = get_last_sync(cursor, "orders")

    assert result is None


def test_save_checkpoint():
    cursor = FakeCursor()

    save_checkpoint(cursor,"orders",20070)

    assert cursor.executed_params == ("orders", 20070)

    assert "migration_checkpoints" in cursor.executed_query

def test_save_last_sync():
    cursor = FakeCursor()

    save_last_sync(
        cursor,
        "orders",
        "2026-09-24 14:00:00"
    )

    assert cursor.executed_params == ("orders", "2026-09-24 14:00:00")

    assert "migration_sync_state" in cursor.executed_query

def test_get_source_last_sync():
    cursor = FakeCursor(("2026-09-24 15:00:00",))

    result = get_source_last_sync(cursor,"orders")

    assert result == "2026-09-24 15:00:00"
    assert "MAX(updated_at)" in cursor.executed_query
    assert "orders" in cursor.executed_query


def test_get_incremental_rows():
    rows = [
        (20071, 12, "paid", 45.50, "2026-09-24", "2026-09-24 16:00:00"),
        (20072, 18, "pending", 72.00, "2026-09-24", "2026-09-24 16:01:00")
    ]

    cursor = FakeCursor(results=rows)

    result = get_incremental_rows(
        cursor,
        "orders",
        "2026-09-24 15:00:00",
        1000
    )

    assert result == rows

    assert cursor.executed_params == ("2026-09-24 15:00:00", 1000)

    assert "updated_at > %s" in cursor.executed_query
    assert "FROM orders" in cursor.executed_query

def test_get_incremental_rows_not_available():
    cursor = FakeCursor()

    result = get_incremental_rows(
        cursor,
        "unknown_table",
        "2026-09-24 15:00:00",
        1000
    )

    assert result == []
    assert cursor.executed_query is None