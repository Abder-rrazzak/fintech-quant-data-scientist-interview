from solution import causal_split_ok

def test_causal():
    assert causal_split_ok(10, 10) is True
    assert causal_split_ok(11, 10) is False
