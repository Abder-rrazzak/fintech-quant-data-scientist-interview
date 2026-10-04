from solution import count_calls

def test_calls():
    @count_calls
    def add(a, b):
        return a + b
    add(1, 2)
    add(0, 0)
    assert add.calls == 2
