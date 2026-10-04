from solution import clip_amounts

def test_clip():
    assert clip_amounts([-5, 10, 80], 0, 50) == [0, 10, 50]
