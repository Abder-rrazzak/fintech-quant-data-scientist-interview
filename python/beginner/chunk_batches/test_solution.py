from solution import chunk_batches

def test_chunk():
    assert chunk_batches([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
