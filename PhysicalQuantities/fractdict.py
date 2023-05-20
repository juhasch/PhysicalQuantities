from __future__ import annotations
from typing import Union
from fractions import Fraction


class FractionalDict(dict):
    """Dictionary storing fractional values.

    An instance of this class acts like an array of number with generalized
    (non-integer) indices. A value of zero is assumed for undefined
    entries. NumberDict instances support addition, and subtraction with other
    NumberDict instances, and multiplication and division by scalars.
    """

    def __getitem__(self, item: Union[int, str]) -> Fraction:
        """Return the value of the item, or 0 if it is not defined."""
        return self.get(item, 0)

    def __add__(self, other: FractionalDict) -> FractionalDict:
        """Return the sum of self and other."""
        sum_dict = FractionalDict()
        for key in self.keys() | other.keys():
            sum_dict[key] = self[key] + other[key]
        return sum_dict

    def __sub__(self, other: FractionalDict) -> FractionalDict:
        """Return the difference of self and other."""
        sub_dict = FractionalDict()
        for key in self.keys() | other.keys():
            sub_dict[key] = self[key] - other[key]
        return sub_dict

    def __mul__(self, other: Fraction) -> FractionalDict:
        """Return the product of self and other."""
        new = FractionalDict()
        for key in self.keys():
            new[key] = other*self[key]
        return new

    def __truediv__(self, other: Fraction) -> FractionalDict:
        """Return the quotient of self and other."""
        new = FractionalDict()
        for key in self.keys():
            new[key] = self[key]/other
        return new

    def __floordiv__(self, other: Fraction) -> FractionalDict:
        """Return the floored quotient of self and other."""
        new = FractionalDict()
        for key in self.keys():
            new[key] = self[key] / other
        return new

    def __rdiv__(self, other):
        """Return the quotient of other and self."""
        new = FractionalDict()
        for key in self.keys():
            new[key] = other/self[key]
        return new

    def __rmul__(self, other: Fraction) -> FractionalDict:
        """Return the product of self and other."""
        new = FractionalDict()
        for key in self.keys():
            new[key] = other*self[key]
        return new

    __rtruediv__ = __rdiv__

    def __rfloordiv__(self, other):
        """Return the floored quotient of other and self."""
        new = FractionalDict()
        for key in self.keys():
            new[key] = other / self[key]
        return new
