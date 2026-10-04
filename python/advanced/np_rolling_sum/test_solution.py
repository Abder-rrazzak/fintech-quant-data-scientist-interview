import numpy as np
from solution import np_rolling_sum

def test_roll():
    assert np_rolling_sum(np.array([1.0, 2.0, 3.0, 4.0]), 2).tolist() == [3.0, 5.0, 7.0]
