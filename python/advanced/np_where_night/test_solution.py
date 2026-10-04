import numpy as np
from solution import np_where_night

def test_night():
    assert np_where_night(np.array([1, 12, 5])).tolist() == [1, 0, 1]
