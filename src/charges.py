from collections.abc import MutableMapping

class Charges(MutableMapping):
    """Classe stockant des charges"""

    def calcul_charge_totales(self):
        sum = 0.
        for value in self.values():
            sum += value
        return sum

    def __delitem__(self, key):
        self.__dict__.pop(key)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __setitem__(self, key, value):
        self.__dict__[key] = value





