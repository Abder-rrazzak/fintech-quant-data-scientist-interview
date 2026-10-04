import numpy as np
from solution import np_cumsum_reset

def test_csum():
    assert np_cumsum_reset(np.array([1.0, 2.0, 3.0])).tolist() == [1.0, 3.0, 6.0]
