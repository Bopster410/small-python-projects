class Expression():
    def reduce(self, to: str, *, bank):
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
    
    def dollar(self):
        return Money("USD", self._amount)
    
    def ruble(self):
        return Money("RUB", self._amount)

    def times(self, multiplier):
        return Money(self._currency, self._amount * multiplier)

    def reduce(self, to: str, *, bank):
        rate = bank.rate(self._currency, to)
        return Money(to, self._amount / rate)

class Bank():
    def __init__(self) -> None:
        self.__rates = {}
    
    def add_rate(self, initial: str, to: str, rate: int):
        self.__rates[Pair(initial, to)] = rate

    def reduce(self, to: str, *, source: Expression):
        return source.reduce(to, bank=self)
    
    def rate(self, initial: str, to: str):
        if initial == to:
            return 1
        rate = self.__rates[Pair(initial, to)]
        return rate
    
class Sum(Expression):
    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend
    
    def reduce(self, to: str, *, bank):
        amount = self.augend.amount() + self.addend.amount()
        return Money(to, amount)

class Pair():
    def __init__(self, initial: str, to: str) -> None:
        self.__initial = initial
        self.__to = to
    
    def __eq__(self, __o: object) -> bool:
        return self.__initial == __o.__initial and self.__to == __o.__to
    
    def __hash__(self) -> int:
        return 0