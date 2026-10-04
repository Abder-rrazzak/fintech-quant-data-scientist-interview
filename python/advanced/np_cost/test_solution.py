import numpy as np
from solution import np_cost

def test_cost():
    assert np_cost(np.array([1, 0]), np.array([0.2, 0.9]), 0.5, 5, 500) == 505
