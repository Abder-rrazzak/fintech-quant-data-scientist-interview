from solution import fraud_ratio_json

def test_ratio():
    assert fraud_ratio_json('[{"is_fraud": 1}, {"is_fraud": 0}]') == 0.5
    assert fraud_ratio_json('[]') == 0.0
