import numpy as np
from solution import np_lag_matrix

def test_lags():
    x, y = np_lag_matrix(np.array([1.0, 2.0, 3.0, 4.0]), 2)
    assert x.shape == (2, 2)
    assert y.tolist() == [3.0, 4.0]
    assert x[0].tolist() == [2.0, 1.0]
