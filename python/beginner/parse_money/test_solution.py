from solution import parse_money

def test_money():
    assert parse_money('$1,200.50') == 1200.50
    assert parse_money('15') == 15.0
