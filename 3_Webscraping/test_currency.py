from currency import Dollar, Ruble

def test_equals_dollar():
    assert Dollar(5) == Dollar(5)
    assert Dollar(5) != Dollar(6)

def test_equals_ruble():
    assert Ruble(5) == Ruble(5)
    assert Ruble(5) != Ruble(6)

def test_multiplication():
    five = Dollar(5)
    assert Dollar(15) == five.times(3)
    assert Dollar(20) == five.times(4)