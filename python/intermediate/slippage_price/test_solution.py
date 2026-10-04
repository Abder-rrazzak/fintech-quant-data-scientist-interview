from solution import slippage_price

def test_slip():
    assert slippage_price(100, 'buy', 10) == 100.1
    assert abs(slippage_price(100, 'sell', 10) - 99.9) < 1e-9
