from solution import count_above

def test_count():
    assert count_above([10, 50, 51, 7], 50) == 1
    assert count_above([], 1) == 0
