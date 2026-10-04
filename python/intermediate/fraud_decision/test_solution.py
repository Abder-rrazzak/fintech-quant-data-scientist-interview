from solution import fraud_decision

def test_decision():
    assert fraud_decision(0.1, 0.4, 0.8) == 'approve'
    assert fraud_decision(0.5, 0.4, 0.8) == 'review'
    assert fraud_decision(0.9, 0.4, 0.8) == 'block'
