class Dollar():
    def __init__(self, amount):
        self.amount = amount
    
    def __eq__(self, __o: object) -> bool:
        return __o.amount == self.amount

    def times(self, multiplier) -> object:
        return Dollar(self.amount * multiplier)