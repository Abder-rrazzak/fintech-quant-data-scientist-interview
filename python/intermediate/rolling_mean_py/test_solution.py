from solution import rolling_mean_py

def test_roll():
    assert rolling_mean_py([1, 2, 3, 4], 2) == [None, 1.5, 2.5, 3.5]
