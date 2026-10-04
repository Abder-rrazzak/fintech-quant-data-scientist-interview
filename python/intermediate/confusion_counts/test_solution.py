from solution import confusion_counts

def test_cm():
    assert confusion_counts([1, 0, 1, 0], [1, 1, 0, 0]) == {'tp': 1, 'fp': 1, 'tn': 1, 'fn': 1}
