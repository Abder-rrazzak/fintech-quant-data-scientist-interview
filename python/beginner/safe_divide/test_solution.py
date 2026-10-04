from solution import safe_divide

def test_div():
    assert safe_divide(10, 4) == 2.5
    assert safe_divide(10, 0) == 0.0
    assert safe_divide(10, 0, default=-1) == -1
