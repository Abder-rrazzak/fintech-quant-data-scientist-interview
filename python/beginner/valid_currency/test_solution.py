from solution import valid_currency

def test_ccy():
    assert valid_currency('USD') is True
    assert valid_currency('JPY') is False
