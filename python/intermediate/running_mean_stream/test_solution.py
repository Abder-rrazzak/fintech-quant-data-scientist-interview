from solution import running_mean_stream

def test_stream():
    assert list(running_mean_stream([2.0, 4.0, 6.0])) == [2.0, 3.0, 4.0]
