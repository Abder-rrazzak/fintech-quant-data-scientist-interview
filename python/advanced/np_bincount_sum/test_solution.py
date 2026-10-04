import numpy as np
from solution import np_bincount_sum

def test_bin():
    out = np_bincount_sum(np.array([0, 1, 0]), np.array([2.0, 3.0, 4.0]))
    assert out.tolist() == [6.0, 3.0]
