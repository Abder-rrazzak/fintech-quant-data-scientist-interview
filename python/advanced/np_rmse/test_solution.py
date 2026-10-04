import numpy as np
from solution import np_rmse

def test_rmse():
    assert abs(np_rmse(np.array([0.0, 0.0]), np.array([3.0, 4.0])) - (12.5 ** 0.5)) < 1e-9
