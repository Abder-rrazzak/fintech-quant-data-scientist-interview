from solution import fraud_ids

def test_fraud_ids():
    assert fraud_ids([10, 11, 12], [0, 1, 0]) == [11]
