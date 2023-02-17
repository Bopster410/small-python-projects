from currency import Dollar, Ruble, Money

def test_equals_dollar():
    assert Money(5).dollar() == Money(5).dollar()
    assert Money(5).dollar() != Money(6).dollar()
    assert Money(5).ruble() == Money(5).ruble()
    assert Money(5).ruble() != Money(6).ruble()
    assert Money(5).ruble() != Money(5).dollar()

def test_multiplication():
    five = Money(5).dollar()
    assert Money(15).dollar() == five.times(3)
    assert Money(20).dollar() == five.times(4)