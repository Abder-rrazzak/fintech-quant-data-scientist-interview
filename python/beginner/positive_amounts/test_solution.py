from solution import positive_amounts

def test_pos():
    assert positive_amounts([-1, 0, 2, 3]) == [2, 3]
