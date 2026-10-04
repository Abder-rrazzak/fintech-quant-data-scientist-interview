from solution import sum_amounts

def test_sum():
    assert sum_amounts([10.0, 2.5, 0.5]) == 13.0
    assert sum_amounts([]) == 0.0
