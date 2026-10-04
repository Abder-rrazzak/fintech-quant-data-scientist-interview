from solution import online_mean_var

def test_welford():
    mean, var = online_mean_var([1.0, 2.0, 3.0])
    assert mean == 2.0
    assert abs(var - (2 / 3)) < 1e-12
