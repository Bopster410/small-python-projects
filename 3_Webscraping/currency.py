class Expression():
    def reduce(self, to: str, *, bank):
        pass
    
    def times(self, multiplier):
        pass

    def __add__(self, __o: object):
        pass

class Money(Expression):
    def __init__(self, currency, amount=0):
        self._amount = amount
        self._currency = currency

    def __eq__(self, __o: object) -> bool:
        return __o._amount == self._amount and self.currency() == __o.currency()
    
    def __add__(self, __o: object) -> Expression:
        return Sum(self, __o)
    
    def __str__(self) -> str:
        return f"{self._amount} {self._currency}"
    
    def __repr__(self) -> str:
        return self.__str__()

    def amount(self):
        return self._amount

    def currency(self):
        return self._currency

    def times(self, multiplier) -> Expression:
        return Money(self._currency, self._amount * multiplier)

    def reduce(self, to: str, *, bank):
        rate = bank.rate(self._currency, to)
        return Money(to, round(self._amount / rate, 2))
    
class Sum(Expression):
    def __init__(self, augend: Expression, addend: Expression):
        self.augend = augend
        self.addend = addend
    
    def __add__(self, __o: object) -> Expression:
        return Sum(self, __o)

    def times(self, multiplier):
        return Sum(self.augend.times(multiplier), self.addend.times(multiplier))

    def reduce(self, to: str, *, bank):
        amount = self.augend.reduce(to, bank=bank).amount()\
               + self.addend.reduce(to, bank=bank).amount()
        return Money(to, amount)


class Bank():
    def __init__(self) -> None:
        self.__rates = {}
    
    def add_rate(self, initial: str, to: str, rate):
        self.__rates[Pair(initial, to)] = rate

    def reduce(self, to: str, *, source: Expression):
        return source.reduce(to, bank=self)
    
    def rate(self, initial: str, to: str):
        if initial == to:
            return 1
        rate = self.__rates[Pair(initial, to)]
        return rate

class Pair():
    def __init__(self, initial: str, to: str) -> None:
        self.__initial = initial
        self.__to = to
    
    def __eq__(self, __o: object) -> bool:
        return self.__initial == __o.__initial and self.__to == __o.__to
    
    def __hash__(self) -> int:
        return 0