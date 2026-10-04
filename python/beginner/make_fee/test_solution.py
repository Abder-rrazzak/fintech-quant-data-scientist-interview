from solution import make_fee

def test_fee():
    add = make_fee(1.5)
    assert add(10) == 11.5
