from solution import running_balance

def test_balance():
    assert running_balance(100.0, [-20.0, 5.0]) == [80.0, 85.0]
    assert running_balance(10.0, []) == []
