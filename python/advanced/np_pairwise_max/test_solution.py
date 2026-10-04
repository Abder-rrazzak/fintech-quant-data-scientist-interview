import numpy as np
from solution import np_pairwise_max

def test_max():
    assert np_pairwise_max(np.array([1.0, 5.0]), np.array([2.0, 3.0])).tolist() == [2.0, 5.0]
