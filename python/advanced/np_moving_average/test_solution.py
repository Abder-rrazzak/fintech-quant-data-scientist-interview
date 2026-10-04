import numpy as np
from solution import np_moving_average

def test_ma():
    assert np_moving_average(np.array([1.0, 2.0, 3.0, 4.0]), 2).tolist() == [1.5, 2.5, 3.5]
