"""
 Adapted from ScientificPython:
 Written by Konrad Hinsen <hinsen@cnrs-orleans.fr>
 with contributions from Greg Ward
 last revision: 2007-5-25
"""


class NumberDict(dict):
    """Dictionary storing numerical values.

    An instance of this class acts like an array of number with generalized
    (non-integer) indices. A value of zero is assumed for undefined
    entries. NumberDict instances support addition, and subtraction with other
    NumberDict instances, and multiplication and division by scalars.
    """

    def __getitem__(self, item):
        """Return the value of the item, or 0 if it is not defined."""
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            return 0

    def __add__(self, other):
        """Return the sum of self and other."""
        sum_dict: NumberDict = NumberDict()
        for key in self.keys():
            sum_dict[key] = self[key]
        for key in other.keys():
            sum_dict[key] = sum_dict[key] + other[key]
        return sum_dict
    __radd__ = __add__

    def __sub__(self, other):
        """Return the difference of self and other."""
        sum_dict = NumberDict()
        for key in self.keys():
            sum_dict[key] = self[key]
        for key in other.keys():
            sum_dict[key] = sum_dict[key] - other[key]
        return sum_dict
    __rsub__ = __sub__

    def __mul__(self, other):
        """Return the product of self and other."""
        new = NumberDict()
        for key in self.keys():
            new[key] = other*self[key]
        return new

    __rmul__ = __mul__

    def __div__(self, other):
        """Return the quotient of self and other."""
        new = NumberDict()
        for key in self.keys():
            new[key] = self[key]/other
        return new

    def __rdiv__(self, other):
        """Return the quotient of other and self."""
        new = NumberDict()
        for key in self.keys():
            new[key] = other/self[key]
        return new

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __floordiv__(self, other):
        """Return the floored quotient of self and other."""
        new = NumberDict()
        for key in self.keys():
            new[key] = self[key] // other
        return new

    def __rfloordiv__(self, other):
        """Return the floored quotient of other and self."""
        new = NumberDict()
        for key in self.keys():
            new[key] = other // self[key]
        return new
