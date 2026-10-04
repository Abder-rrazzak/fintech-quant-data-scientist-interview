import numpy as np
from solution import np_mae

def test_mae():
    assert np_mae(np.array([1.0, 2.0]), np.array([1.0, 4.0])) == 1.0
