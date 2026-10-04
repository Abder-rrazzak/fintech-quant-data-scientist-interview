import numpy as np
from solution import np_corr

def test_corr():
    assert abs(np_corr(np.array([1.0, 2.0, 3.0]), np.array([2.0, 4.0, 6.0])) - 1) < 1e-9
