from solution import brier_score

def test_brier():
    assert brier_score([1, 0], [1.0, 0.0]) == 0.0
