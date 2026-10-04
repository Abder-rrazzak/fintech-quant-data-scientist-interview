from solution import cost_at_threshold

def test_cost():
    assert cost_at_threshold([1, 0], [0.2, 0.9], 0.5, 5, 500) == 505
