import numpy as np
from solution import np_log_returns

def test_ret():
    out = np_log_returns(np.array([100.0, 110.0]))
    assert abs(out[0] - np.log(1.1)) < 1e-12
