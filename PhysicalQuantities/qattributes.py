from .quantity import PhysicalQuantity
from .prefixes import *
from PhysicalQuantities.dBQuantity import dBQuantity, dB_unit_table


class QuantityAttributes:
    """Class to provide attributes for all known units including prefixes

    Examples
    --------
    >>> from PhysicalQuantities import  QuantityAttributes
    >>> q = QuantityAttributes()
    >>> q['m']
    1 m
    >>> q.m
    1 m
    >>>  type(q['m'])
    PhysicalQuantities.quantity.PhysicalQuantity

    Notes
    -----
    When adding more units, the class has to be reinitialized using `update()`for the new units to be listed.
    """
    table = dict()  # Lookup table from string to Quantity: 'V': 1 V

    def __init__(self):
        self.update()

    def update(self):
        """Update table with all """
        for key in dB_unit_table:
            self.table[key] = dBQuantity(1, key)
        for key in unit_table:
            self.table[key] = PhysicalQuantity(1, unit_table[key])

    def __dir__(self):
        return self.table.keys()

    def __getitem__(self, key):
        if type(key) is str:
            return self.table[key]
        else:
            return self.table[key.name]
        raise TypeError(f"'QuantityAttribute' object has no element '{key}'")

    def __getattr__(self, attr):
        if attr in self.table:
            return self.table[attr]
        raise AttributeError  # (f'Unknown attribute {attr}')

    def _ipython_key_completions_(self):
        return list(self.table.keys())
