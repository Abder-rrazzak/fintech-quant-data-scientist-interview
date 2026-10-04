from solution import prior_mean_list

def test_prior():
    assert prior_mean_list([10.0, 30.0, 50.0]) == [None, 10.0, 20.0]
