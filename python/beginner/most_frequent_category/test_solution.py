from solution import most_frequent_category

def test_mode():
    assert most_frequent_category(['fuel', 'grocery', 'fuel']) == 'fuel'
    assert most_frequent_category(['b', 'a']) == 'a'
