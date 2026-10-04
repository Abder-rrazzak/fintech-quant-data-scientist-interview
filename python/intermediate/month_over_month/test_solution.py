from solution import month_over_month

def test_mom():
    assert month_over_month(100.0, 150.0) == 0.5
    assert month_over_month(None, 10.0) is None
