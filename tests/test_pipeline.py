from app.validator import validate_sql

def test_blocks_drop():
    valid, msg = validate_sql("DROP TABLE customers")
    assert valid is False

def test_blocks_delete():
    valid, msg = validate_sql("DELETE FROM orders")
    assert valid is False

def test_allows_select():
    valid, msg = validate_sql("SELECT * FROM customers")
    assert valid is True

def test_catches_bad_syntax():
    valid, msg = validate_sql("SELEKT * FORM customers")
    assert valid is False