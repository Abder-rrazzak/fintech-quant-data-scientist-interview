from solution import batch_stream

def test_batches():
    assert list(batch_stream([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
