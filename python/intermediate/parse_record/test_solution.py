from solution import parse_record

def test_parse():
    assert parse_record({'customer_id': '7', 'amount': '3.5'}) == (7, 3.5)
