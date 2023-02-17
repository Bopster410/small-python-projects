from currency import Dollar, Ruble

def test_equals_dollar():
    assert Dollar(5) == Dollar(5)
    assert Dollar(5) != Dollar(6)
    assert Ruble(5) == Ruble(5)
    assert Ruble(5) != Ruble(6)
    assert Ruble(5) != Dollar(5)

def test_multiplication():
    five = Dollar(5)
    assert Dollar(15) == five.times(3)
    assert Dollar(20) == five.times(4)