from solution import clamp_score

def test_clamp():
    assert clamp_score(1.4) == 1.0
    assert clamp_score(-0.2) == 0.0
    assert clamp_score(0.3) == 0.3
