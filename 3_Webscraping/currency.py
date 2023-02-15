class Dollar():
    def __init__(self, amount):
        self.__amount = amount
    
    def __eq__(self, __o: object) -> bool:
        return __o.__amount == self.__amount

    def times(self, multiplier) -> object:
        return Dollar(self.__amount * multiplier)

class Ruble():
    def __init__(self, amount):
        self.__amount = amount
    
    def __eq__(self, __o: object) -> bool:
        return __o.__amount == self.__amount

    def times(self, multiplier) -> object:
        return Dollar(self.__amount * multiplier)