from solution import precision_recall

def test_pr():
    assert precision_recall(2, 2, 0) == (0.5, 1.0)
