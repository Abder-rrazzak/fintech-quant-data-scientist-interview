import pandas as pd
from solution import pd_fraud_rate

def test_rate():
    frame = pd.DataFrame({'customer_segment': ['a', 'a', 'b'], 'is_fraud': [1, 0, 0]})
    assert pd_fraud_rate(frame).loc['a'] == 0.5
