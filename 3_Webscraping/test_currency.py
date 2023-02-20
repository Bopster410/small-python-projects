from currency import Money

def test_equals_dollar():
    assert Money("USD", 5).dollar() != Money("USD", 6).dollar()
    assert Money("USD", 5).dollar() == Money("USD", 5).dollar()
    assert Money("RUB", 5).ruble() != Money("USD", 5).dollar()

def test_multiplication():
    five = Money("USD", 5).dollar()
    assert Money("USD", 15).dollar() == five.times(3)
    assert Money("USD", 20).dollar() == five.times(4)

def test_currency():
    assert Money("USD", 1).dollar().currency() == "USD"
    assert Money("RUB", 1).ruble().currency() == "RUB"