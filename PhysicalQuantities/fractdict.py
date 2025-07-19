from __future__ import annotations
from typing import Union
from fractions import Fraction


class FractionalDict(dict):
    """Dictionary storing fractional values.

    An instance of this class acts like an array of number with generalized
    (non-integer) indices. A value of zero is assumed for undefined
    entries. NumberDict instances support addition, and subtraction with other
    NumberDict instances, and multiplication and division by scalars.

    Args:
        *args: Positional arguments passed to the dict constructor.
        **kwargs: Keyword arguments passed to the dict constructor.
    """

    def __getitem__(self, item: Union[int, str]) -> Fraction:
        """Return the value of the item, or 0 if it is not defined.

        Args:
            item: The key to retrieve the value for.

        Returns:
            The fractional value associated with the key, or Fraction(0) if the
            key is not found.
        """
        return self.get(item, Fraction(0)) # Ensure return type is Fraction

    def __add__(self, other: FractionalDict) -> FractionalDict:
        """Return the sum of self and other.

        Args:
            other: The FractionalDict to add to self.

        Returns:
            A new FractionalDict representing the element-wise sum.
        """
        sum_dict = FractionalDict()
        for key in self.keys() | other.keys():
            sum_dict[key] = self[key] + other[key]
        return sum_dict

    def __sub__(self, other: FractionalDict) -> FractionalDict:
        """Return the difference of self and other.

        Args:
            other: The FractionalDict to subtract from self.

        Returns:
            A new FractionalDict representing the element-wise difference.
        """
        sub_dict = FractionalDict()
        for key in self.keys() | other.keys():
            sub_dict[key] = self[key] - other[key]
        return sub_dict

    def __mul__(self, other: Fraction) -> FractionalDict:
        """Return the product of self and a scalar.

        Args:
            other: The scalar (Fraction) to multiply self by.

        Returns:
            A new FractionalDict with each value multiplied by the scalar.
        """
        new = FractionalDict()
        for key in self.keys():
            new[key] = other*self[key]
        return new

    def __truediv__(self, other: Fraction) -> FractionalDict:
        """Return the true division of self by a scalar.

        Args:
            other: The scalar (Fraction) to divide self by.

        Returns:
            A new FractionalDict with each value divided by the scalar.
        """
        new = FractionalDict()
        for key in self.keys():
            new[key] = self[key]/other
        return new

    def __floordiv__(self, other: Fraction) -> FractionalDict:
        """Return the floor division of self by a scalar.

        Args:
            other: The scalar (Fraction) to floor-divide self by.

        Returns:
            A new FractionalDict with each value floor-divided by the scalar.
        """
        new = FractionalDict()
        for key in self.keys():
            new[key] = self[key] // other # Corrected to floor division
        return new

    # __rdiv__ is deprecated in Python 3, use __rtruediv__ instead.
    # def __rdiv__(self, other: Fraction) -> FractionalDict:
    #     """Return the quotient of other and self."""
    #     new = FractionalDict()
    #     for key in self.keys():
    #         new[key] = other/self[key]
    #     return new

    def __rmul__(self, other: Fraction) -> FractionalDict:
        """Return the product of a scalar and self.

        Args:
            other: The scalar (Fraction) to multiply self by.

        Returns:
            A new FractionalDict with each value multiplied by the scalar.
        """
        new = FractionalDict()
        for key in self.keys():
            new[key] = other*self[key]
        return new
 
    def __rfloordiv__(self, other: Fraction) -> FractionalDict:
        """Return the floor division of a scalar by self.

        Args:
            other: The scalar (Fraction) to be floor-divided by self's values.

        Returns:
            A new FractionalDict representing the element-wise floor division.
        """
        new = FractionalDict()
        for key in self.keys():
            new[key] = other // self[key] # Corrected to floor division
        return new

    def __rtruediv__(self, other: Fraction) -> FractionalDict:
        """Return the true division of a scalar by self.

        Args:
            other: The scalar (Fraction) to be divided by self's values.

        Returns:
            A new FractionalDict representing the element-wise true division.
        """
        new = FractionalDict()
        for key in self.keys():
            new[key] = other/self[key]
        return new

    def __repr__(self) -> str:
        """Return a string representation of the FractionalDict."""
        # Filter out zero values for a cleaner representation
        items = {k: v for k, v in self.items() if v != 0}
        return f"{self.__class__.__name__}({items})"

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        # Filter out zero values and format Fractions nicely
        items = []
        for k, v in self.items():
            if v != 0:
                # Simplify fraction representation if possible
                if v.denominator == 1:
                    val_str = str(v.numerator)
                else:
                    val_str = str(v)
                items.append(f"{repr(k)}: {val_str}")
        return '{' + ', '.join(items) + '}'

    def __eq__(self, other):
        """Check equality with another FractionalDict."""
        if not isinstance(other, FractionalDict):
            return NotImplemented
        # Consider dictionaries equal if they have the same non-zero items
        keys = self.keys() | other.keys()
        for key in keys:
            if self[key] != other[key]:
                return False
        return True

    def __ne__(self, other):
        """Check inequality with another FractionalDict."""
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal

    def copy(self) -> FractionalDict:
        """Return a shallow copy of the FractionalDict."""
        return FractionalDict(self)
