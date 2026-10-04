from solution import count_categories

def test_counts():
    assert count_categories(['grocery', 'grocery', 'fuel']) == {'grocery': 2, 'fuel': 1}
