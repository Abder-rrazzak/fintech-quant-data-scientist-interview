from solution import weighted_mean

def test_wmean():
    assert weighted_mean([10.0, 20.0], [1.0, 1.0]) == 15.0
    assert weighted_mean([10.0, 20.0], [3.0, 1.0]) == 12.5
