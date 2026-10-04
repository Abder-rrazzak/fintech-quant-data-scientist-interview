from solution import velocity_count

def test_velocity():
    assert velocity_count([0, 10, 50], 20) == [1, 2, 1]
