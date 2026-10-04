from solution import flatten_batches

def test_flat():
    assert flatten_batches([[1, 2], [], [3]]) == [1, 2, 3]
