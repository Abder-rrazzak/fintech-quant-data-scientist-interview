import math
from solution import squared_log_amounts

def test_sq():
    assert squared_log_amounts([0.0]) == [0.0]
    assert squared_log_amounts([math.e - 1]) == [1.0]
