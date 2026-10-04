from solution import get_nested

def test_nested():
    assert get_nested({'cust': {'limit': 20.0}}, 'cust', 'limit', 0.0) == 20.0
    assert get_nested({}, 'cust', 'limit', 0.0) == 0.0
