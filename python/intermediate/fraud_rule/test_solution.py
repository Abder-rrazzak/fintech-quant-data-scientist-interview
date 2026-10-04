from solution import fraud_rule

def test_rule():
    assert fraud_rule(3.2, 1, 0, 0) is True
    assert fraud_rule(0.1, 1, 1, 0) is False
    assert fraud_rule(0.1, 1, 1, 1) is True
