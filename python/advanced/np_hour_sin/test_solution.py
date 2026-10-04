import numpy as np
from solution import np_hour_sin

def test_hour():
    assert abs(np_hour_sin(np.array([0.0]))[0]) < 1e-9
    assert abs(np_hour_sin(np.array([6.0]))[0] - 1) < 1e-9
