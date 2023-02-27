from currency import Money, Bank, Sum, Expression

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

def test_sum():
    five = Money("USD", 5).dollar()
    sum = five + five
    bank = Bank()
    reduced = bank.reduce("USD", source=sum)
    assert Money("USD", 10).dollar() == reduced

def test_plus_returns_sum():
    five = Money("USD", 5).dollar()
    result = five + five
    sum = result
    assert sum.augend == five
    assert sum.addend == five

def test_reduce_sum():
    sum = Sum(Money("USD", 3), Money("USD", 4))
    bank = Bank()
    result = bank.reduce("USD", source=sum)
    assert Money("USD", 7) == result

def test_reduce_money():
    bank = Bank()
    result = bank.reduce("USD", source=Money("USD", 1).dollar())
    assert result == Money("USD", 1).dollar()

def test_reduce_different_currency():
    bank = Bank()
    bank.add_rate("RUB", "USD", 70)
    result = bank.reduce("USD", source=Money("RUB", 70).ruble())
    assert result == Money("USD", 1).dollar()

def test_reduce_identity_rate():
    assert 1 == Bank().rate("USD", "USD")

def test_mixed_addition():
    bucks: Expression = Money("USD", 5).dollar()
    rubles: Expression = Money("RUB", 140).ruble()
    bank = Bank()
    bank.add_rate("RUB", "USD", 70)
    result = bank.reduce("USD", source=(bucks + rubles))
    assert result == Money("USD", 7).dollar()

def test_sum_plus_money():
    bucks = Money("USD", 4).dollar()
    rubles = Money("RUB", 210).ruble()
    bank = Bank()
    bank.add_rate("RUB", "USD", 70)
    sum = Sum(bucks, rubles) + bucks
    result = bank.reduce("USD", source=sum)
    assert Money("USD", 11) == result

def test_sum_times():
    bucks = Money("USD", 4).dollar()
    rubles = Money("RUB", 210).ruble()
    bank = Bank()
    bank.add_rate("RUB", "USD", 70)
    sum = Sum(bucks, rubles).times(2)
    result = bank.reduce("USD", source=sum)
    assert Money("USD", 14) == result