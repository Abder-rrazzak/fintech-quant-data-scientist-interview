from solution import dedupe_rows

def test_rows():
    rows = [{'transaction_id': 1, 'amount': 5}, {'transaction_id': 1, 'amount': 9}]
    assert dedupe_rows(rows) == [{'transaction_id': 1, 'amount': 5}]
