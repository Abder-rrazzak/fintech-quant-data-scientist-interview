import pandas as pd
from solution import pd_vector_zscore

def test_z():
    frame = pd.DataFrame({'amount': [1.0, 2.0, 3.0]})
    out = pd_vector_zscore(frame)
    assert abs(out.sum()) < 1e-9
