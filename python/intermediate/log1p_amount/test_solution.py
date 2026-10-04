from solution import log1p_amount

def test_log():
    assert log1p_amount(0) == 0.0
    assert log1p_amount(-5) == 0.0
