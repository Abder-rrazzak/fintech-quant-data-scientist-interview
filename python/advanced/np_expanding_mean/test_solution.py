import numpy as np
from solution import np_expanding_mean

def test_exp():
    assert np_expanding_mean(np.array([2.0, 4.0, 6.0])).tolist() == [2.0, 3.0, 4.0]
