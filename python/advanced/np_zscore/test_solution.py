import numpy as np
from solution import np_zscore

def test_z():
    out = np_zscore(np.array([1.0, 2.0, 3.0]))
    assert abs(out.sum()) < 1e-9
