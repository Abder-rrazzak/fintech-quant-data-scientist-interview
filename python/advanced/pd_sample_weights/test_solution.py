import pandas as pd
from solution import pd_sample_weights

def test_w():
    frame = pd.DataFrame({'is_fraud': [0, 0, 1]})
    weights = pd_sample_weights(frame)
    assert abs(weights[frame['is_fraud'] == 0].sum() - weights[frame['is_fraud'] == 1].sum()) < 1e-9
