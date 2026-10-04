import pandas as pd
from solution import pd_boolean_fraud_rule

def test_rule():
    frame = pd.DataFrame({'amount_zscore': [0.2, 3.4], 'txn_count_1h': [1, 1]})
    assert pd_boolean_fraud_rule(frame).tolist() == [False, True]
