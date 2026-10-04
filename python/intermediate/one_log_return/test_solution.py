import math
from solution import one_log_return

def test_ret():
    assert abs(one_log_return(100, 110) - math.log(1.1)) < 1e-12
