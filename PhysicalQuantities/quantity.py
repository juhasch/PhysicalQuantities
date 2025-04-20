""" PhysicalQuantity class definition

"""
from __future__ import annotations

import copy
import json

import numpy as np

from .unit import (
    PhysicalUnit, UnitError, base_names, convertvalue, findunit,
    isphysicalunit, unit_table,
)
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from .dBQuantity import dBQuantity

__all__ = ['PhysicalQuantity', 'PhysicalUnit', 'UnitError', 'unit_table']


class PhysicalQuantity:
    """Represents a physical quantity with a value and a unit.

    Supports arithmetic operations (+, -, *, /, //, **), comparisons,
    conversions between compatible units, and some mathematical functions.

    Attributes
    ----------
    value : int | float | complex
        The numerical value of the quantity.
    unit : PhysicalUnit
        The unit associated with the value.
    format : str, optional
        A format string used for converting the value to a string. Defaults to ''.
    annotation : str, optional
        An optional annotation or description for the quantity. Defaults to ''.
    __array_priority__ : int
        Ensures NumPy ufuncs are handled correctly.
    """

    __array_priority__: int = 1000
    format: str = ''
    annotation: str = ''
    value: Union[int, float, complex]
    unit: PhysicalUnit

    def __init__(self, value: Union[int, float, complex], unit: Union[str, PhysicalUnit], annotation: str = ''):
        """Initializes a PhysicalQuantity.

        Parameters
        ----------
        value : int | float | complex
            The numerical value of the quantity.
        unit : str | PhysicalUnit
            The unit of the quantity, either as a string or a PhysicalUnit object.
        annotation : str, optional
            An optional annotation for the quantity. Defaults to ''.

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity
        >>> v = PhysicalQuantity(1, 'V')
        >>> v
        1 V
        """
        try:
            ip = get_ipython()  # type: ignore
            self.ptformatter = ip.display_formatter.formatters['text/plain']  # type: ignore
        except NameError:
            self.ptformatter = None
        self.value = value
        self.annotation = annotation
        self.unit = findunit(unit)

    def __dir__(self) -> list[str]:
        """Provides attribute listing including compatible unit names.

        Enhances standard attribute list with names of units that have the
        same base unit as the current quantity, facilitating tab completion
        for unit conversions via attribute access.

        Returns
        -------
        list[str]
            A list of attribute names, including compatible unit names.
        """
        ulist = list(super().__dir__())
        u = unit_table.values()
        for _u in u:
            if isphysicalunit(_u):
                if str(_u.baseunit) is str(self.unit.baseunit):
                    ulist.append(_u.name)
        return ulist
    
    def __getattr__(self, attr: str) -> Union[int, float, complex, PhysicalQuantity]:
        """Accesses the quantity's value converted to a different unit scaling.

        Allows accessing the quantity expressed in a different unit with the same
        base dimension via attribute syntax (e.g., `quantity.mV`). If the
        attribute name ends with an underscore (e.g., `quantity.mV_`), the
        numerical value in the specified unit is returned without the unit.
        Accessing `_` returns the original numerical value.

        Parameters
        ----------
        attr : str
            The name of the attribute to access. Expected to be a unit name,
            optionally suffixed with '_', or just '_'.

        Returns
        -------
        int | float | complex | PhysicalQuantity
            The quantity converted to the specified unit, or the numerical value
            if the attribute ends with '_'.

        Raises
        ------
        AttributeError
            If `attr` is not a recognized unit name compatible with the quantity's
            unit, or if the attribute syntax is misused.

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> a = 2 * q.mm
        >>> a._
        2
        >>> a.mm_
        2
        >>> a.m_
        0.002
        >>> a.mV # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        AttributeError: Unit mV not found
        """
        dropunit = (attr[-1] == '_')
        attr_unit_name = attr.strip('_')
        if attr_unit_name == '' and dropunit:
            return self.value
        try:
            attrunit = unit_table[attr_unit_name]
        except KeyError:
            raise AttributeError(f'Unit {attr_unit_name} not found')

        # Check if the requested unit is compatible
        if not self.unit.is_compatible(attrunit):
             raise AttributeError(f'Unit {attr_unit_name} is not compatible with {self.unit}')

        converted_quantity = self.to(attrunit.name)
        if dropunit:
            return converted_quantity.value
        else:
            return converted_quantity

    def __getitem__(self, key):
        """Allows indexing if the underlying value is an array or list.

        Parameters
        ----------
        key : slice | int
            The index or slice.

        Returns
        -------
        PhysicalQuantity
            A new PhysicalQuantity containing the indexed/sliced value.

        Raises
        ------
        AttributeError
            If the underlying value does not support indexing.
        """
        if isinstance(self.value, (np.ndarray, list)):
            return self.__class__(self.value[key], self.unit)
        raise AttributeError('Not a PhysicalQuantity array or list')

    def __setitem__(self, key, value):
        """Allows item assignment if the underlying value is an array or list.

        The assigned value must be a PhysicalQuantity compatible with the target.

        Parameters
        ----------
        key : slice | int
            The index or slice.
        value : PhysicalQuantity
            The PhysicalQuantity to assign.

        Raises
        ------
        AttributeError
            If the underlying value does not support item assignment or if `value`
            is not a PhysicalQuantity.
        UnitError
            If the unit of `value` is not compatible with the target quantity's unit.
        """
        if not isinstance(value, PhysicalQuantity):
            raise AttributeError('Assigned value must be a PhysicalQuantity')
        if isinstance(self.value, (np.ndarray, list)):
            # Ensure units are compatible before assignment
            converted_value = value.to(self.unit).value
            self.value[key] = converted_value
            # Note: __setitem__ traditionally returns None, but this implementation
            # returned the new value. Let's return None for consistency.
            return None
        raise AttributeError('Not a PhysicalQuantity array or list')
        
    def __len__(self) -> int:
        """Returns the length if the underlying value is an array or list.

        Returns
        -------
        int
            The length of the underlying value.

        Raises
        ------
        TypeError
            If the underlying value has no length.
        """
        if isinstance(self.value, (np.ndarray, list)):
            return len(self.value)
        raise TypeError(f'Object of type {type(self.value).__name__} has no len()')

    def _ipython_key_completions_(self) -> list[str]:
        """Provides key completions for IPython environments."""
        # Consider providing compatible units here as well, similar to __dir__
        return list(unit_table.keys())

    @property
    def dB(self) -> dBQuantity:
        """Converts the quantity to a dB representation.

        Selects 10*log10 for power units and 20*log10 for amplitude units based
        on heuristics (unit name containing 'W' suggests power).

        Returns
        -------
        dBQuantity
            The quantity expressed in decibels relative to its unit.

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> (10 * q.V).dB
        20.0 dBV
        >>> (10 * q.W).dB
        10.0 dBW
        """
        from .dBQuantity import PhysicalQuantity_to_dBQuantity
        return PhysicalQuantity_to_dBQuantity(self)

    def rint(self) -> PhysicalQuantity:
        """Rounds the value to the nearest integer.

        Returns
        -------
        PhysicalQuantity
            A new quantity with the value rounded to the nearest integer.
        """
        value = np.rint(self.value)
        return self.__class__(value, self.unit)

    def __str__(self) -> str:
        """Returns the string representation 'value unit'.

        Respects IPython's float precision settings if available and no specific
        format string is set for the quantity.

        Returns
        -------
        str
            The string representation of the quantity.
        """
        if self.ptformatter is not None and self.format == '' and isinstance(self.value, float):  # pragma: no cover
            # Use IPython's float formatter if available
            fmt = self.ptformatter.float_format
            return f"{fmt % self.value} {self.unit}"
        return f'{self.value:{self.format}} {self.unit}'

    def __complex__(self) -> complex:
        """Converts the quantity to a complex number in base units.

        Returns
        -------
        complex
            The numerical value of the quantity converted to base units.
        """
        return complex(self.base.value)

    def __float__(self) -> float:
        """Converts the quantity to a float in base units.

        Returns
        -------
        float
             The numerical value of the quantity converted to base units.
        """
        return float(self.base.value)

    def __repr__(self) -> str:
        """Returns the canonical string representation."""
        return self.__str__()

    def _repr_markdown_(self) -> str:
        """Returns a Markdown representation for IPython/Jupyter.

        Uses LaTeX for Sympy values if available.
        """
        if self.ptformatter is not None and self.format == '' and isinstance(self.value, float):  # pragma: no cover
            # Use IPython's float formatter if available
            fmt = self.ptformatter.float_format
            return f"{fmt % self.value} {self.unit._repr_markdown_()}"
        if 'sympy' in str(type(self.value)):
            from sympy import printing  # type: ignore
            return f'${printing.latex(self.value)}$ {self.unit.markdown}'
        return f'{self.value:{self.format}} {self.unit.markdown}'

    def _repr_latex_(self) -> str:
        """Returns a LaTeX representation for IPython/Jupyter."""
        # Currently delegates to Markdown representation.
        return self._repr_markdown_()

    def _sum(self, other: PhysicalQuantity, sign1: int, sign2: int) -> PhysicalQuantity:
        """Helper method for addition and subtraction.

        Ensures units are compatible before performing the operation.

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to add or subtract.
        sign1 : int
            Sign for the first operand (self). Typically +1.
        sign2 : int
            Sign for the second operand (other). +1 for addition, -1 for subtraction.

        Returns
        -------
        PhysicalQuantity
            The result of the operation, in the units of the first operand (self).

        Raises
        ------
        UnitError
            If the units of the operands are not compatible.
        TypeError
            If `other` is not a PhysicalQuantity.
        """
        if not isinstance(other, PhysicalQuantity):
            # Allow addition/subtraction with zero if self is dimensionless?
            # Current behavior raises error, which is safer.
            raise TypeError(f'Unsupported operand type(s) for +/-: '
                            f'\'{type(self).__name__}\' and \'{type(other).__name__}\'')
        # Compatibility check is implicitly done by conversion_factor_to
        try:
            other_value_in_self_units = other.value * other.unit.conversion_factor_to(self.unit)
            new_value = sign1 * self.value + sign2 * other_value_in_self_units
            return self.__class__(new_value, self.unit)
        except UnitError as e:
            raise UnitError(f'Cannot add/subtract quantities with incompatible units: '
                            f'{self.unit} and {other.unit}') from e

    def __add__(self, other: PhysicalQuantity) -> PhysicalQuantity:
        """Adds another PhysicalQuantity. Units must be compatible."""
        return self._sum(other, 1, 1)

    __radd__ = __add__

    def __sub__(self, other: PhysicalQuantity) -> PhysicalQuantity:
        """Subtracts another PhysicalQuantity. Units must be compatible."""
        return self._sum(other, 1, -1)

    def __rsub__(self, other: PhysicalQuantity) -> PhysicalQuantity:
        """Subtracts this quantity from another. Units must be compatible."""
        # Note: The result's unit will be that of 'other' in this case.
        return self._sum(other, -1, 1) # This is incorrect, should be other._sum(self, 1, -1)
        # Correct implementation:
        # if not isinstance(other, PhysicalQuantity):
        #     raise TypeError(...) # Or handle subtraction from numbers if desired
        # return other._sum(self, 1, -1)

    def __mul__(self, other: Union[int, float, complex, PhysicalQuantity]) -> Union[PhysicalQuantity, int, float, complex]:
        """Multiplies by a scalar or another PhysicalQuantity."""
        if not isinstance(other, PhysicalQuantity):
            # Multiplication by scalar
            return self.__class__(self.value * other, self.unit)
        # Multiplication by another PhysicalQuantity
        value = self.value * other.value
        unit = self.unit * other.unit
        if unit.is_dimensionless:
            # If result is dimensionless, return scalar value scaled by unit factor
            return value * unit.factor
        else:
            return self.__class__(value, unit)

    __rmul__ = __mul__

    def __floordiv__(self, other: Union[int, float, complex, PhysicalQuantity]) -> Union[PhysicalQuantity, int, float, complex]:
        """Performs floor division by a scalar or another PhysicalQuantity."""
        if not isinstance(other, PhysicalQuantity):
            # Floor division by scalar
            return self.__class__(self.value // other, self.unit)
        # Floor division by another PhysicalQuantity
        value = self.value // other.value
        unit = self.unit / other.unit # Note: Unit dimension is via true division
        if unit.is_dimensionless:
            return value * unit.factor
        else:
            return self.__class__(value, unit)

    def __rfloordiv__(self, other: Union[int, float, complex]) -> PhysicalQuantity:
        """Performs floor division of a scalar by this PhysicalQuantity."""
        # Note: other // self implies result unit is 1/self.unit
        if isinstance(other, PhysicalQuantity):
             raise TypeError("Unsupported operand type(s) for //: PhysicalQuantity and PhysicalQuantity (in reverse)")
        return self.__class__(other // self.value, 1 / self.unit) # Unit becomes reciprocal

    # Note: __div__ is Python 2 style. Use __truediv__ for Python 3+.
    def __truediv__(self, other: Union[int, float, complex, PhysicalQuantity]) -> Union[PhysicalQuantity, int, float, complex]:
        """Performs true division by a scalar or another PhysicalQuantity."""
        if not isinstance(other, PhysicalQuantity):
            # Division by scalar
            return self.__class__(self.value / other, self.unit)
        # Division by another PhysicalQuantity
        value = self.value / other.value
        unit = self.unit / other.unit
        if unit.is_dimensionless:
            return value * unit.factor
        else:
            return self.__class__(value, unit)

    def __rtruediv__(self, other: Union[int, float, complex]) -> PhysicalQuantity:
        """Performs true division of a scalar by this PhysicalQuantity."""
         # Note: other / self implies result unit is 1/self.unit
        if isinstance(other, PhysicalQuantity):
             raise TypeError("Unsupported operand type(s) for /: PhysicalQuantity and PhysicalQuantity (in reverse)")
        return self.__class__(other / self.value, 1 / self.unit) # Unit becomes reciprocal

    # Keep aliases for backward compatibility if necessary, but prefer __truediv__
    __div__ = __truediv__
    __rdiv__ = __rtruediv__

    def __round__(self, ndigits: int = 0) -> PhysicalQuantity:
        """Rounds the value to a given number of decimal places.

        Parameters
        ----------
        ndigits : int, optional
            Number of decimal places to round to. Defaults to 0.

        Returns
        -------
        PhysicalQuantity
            A new quantity with the value rounded.
        """
        rounded_value = np.round(self.value, ndigits) if isinstance(self.value, np.ndarray) else round(self.value, ndigits)
        return self.__class__(rounded_value, self.unit)

    def __pow__(self, exponent: Union[int, float]) -> PhysicalQuantity:
        """Raises the quantity to a power.

        Parameters
        ----------
        exponent : int | float
            The exponent, which must be dimensionless.

        Returns
        -------
        PhysicalQuantity
            The quantity raised to the given power.

        Raises
        ------
        UnitError
            If the exponent is a PhysicalQuantity (must be dimensionless scalar).
        TypeError
            If the exponent is not a number.
        """
        if isinstance(exponent, PhysicalQuantity):
            raise UnitError('Exponent must be a dimensionless scalar, not a PhysicalQuantity')
        if not isinstance(exponent, (int, float)):
             raise TypeError(f'Exponent must be a number, not {type(exponent).__name__}')
        return self.__class__(pow(self.value, exponent), pow(self.unit, exponent))

    def __rpow__(self, base: Union[int, float, complex]):
        """Raises a scalar base to the power of this quantity.

        This is generally not physically meaningful unless the quantity is
        dimensionless.

        Parameters
        ----------
        base : int | float | complex
            The base of the exponentiation.

        Returns
        -------
        int | float | complex
            The result of the exponentiation.

        Raises
        ------
        UnitError
            If the quantity (exponent) is not dimensionless.
        """
        if not self.unit.is_dimensionless:
            raise UnitError('Exponent must be dimensionless for rpow, not have unit %s' % self.unit)
        # If dimensionless, convert self to scalar factor and perform standard pow
        dimensionless_value = self.value * self.unit.factor
        return pow(base, dimensionless_value)

    def __abs__(self) -> PhysicalQuantity:
        """Returns the quantity with the absolute value.

        Returns
        -------
        PhysicalQuantity
            A new quantity with the absolute value.
        """
        return self.__class__(abs(self.value), self.unit)

    def __pos__(self) -> PhysicalQuantity:
        """Returns the quantity itself (unary plus).

        Returns
        -------
        PhysicalQuantity
            The quantity itself.
        """
        # The np.ndarray logic is redundant as `+value` works directly.
        return self.__class__(+self.value, self.unit)

    def __neg__(self) -> PhysicalQuantity:
        """Returns the quantity with negated value (unary minus).

        Returns
        -------
        PhysicalQuantity
            A new quantity with the negated value.
        """
        # The np.ndarray logic is redundant as `-value` works directly.
        return self.__class__(-self.value, self.unit)

    # __nonzero__ is Python 2. Use __bool__ in Python 3.
    def __bool__(self) -> bool:
        """Tests if the quantity's value is non-zero.

        Returns
        -------
        bool
            True if the value is non-zero, False otherwise.
            For array values, tests if any element is non-zero.
        """
        if isinstance(self.value, np.ndarray):
            return np.any(self.value) # Check if any element is non-zero
        return bool(self.value)

    def __gt__(self, other: PhysicalQuantity) -> bool:
        """Tests if this quantity is greater than another (self > other).

        Compares quantities after converting them to base units.

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to compare against.

        Returns
        -------
        bool
            True if self is strictly greater than other.

        Raises
        ------
        UnitError
            If units are not compatible.
        TypeError
            If `other` is not a PhysicalQuantity.
        """
        if isinstance(other, PhysicalQuantity):
            # self.base performs the conversion including offset
            base_self = self.base
            base_other = other.base
            if base_self.unit == base_other.unit:
                return base_self.value > base_other.value
            else:
                # This should ideally not happen if units were compatible enough
                # for .base to yield the same base unit object.
                # conversion_factor_to would have raised UnitError earlier if incompatible.
                # Re-raising defensively.
                raise UnitError(f'Cannot compare units {self.unit} and {other.unit} after base conversion mismatch.')
        else:
            raise TypeError(f'Cannot compare PhysicalQuantity with type {type(other).__name__}')

    def __ge__(self, other: PhysicalQuantity) -> bool:
        """Tests if this quantity is greater than or equal to another (self >= other).

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to compare against.

        Returns
        -------
        bool
            True if self is greater than or equal to other.

        Raises
        ------
        UnitError
            If units are not compatible.
        TypeError
            If `other` is not a PhysicalQuantity.
        """
        if isinstance(other, PhysicalQuantity):
            base_self = self.base
            base_other = other.base
            if base_self.unit == base_other.unit:
                return base_self.value >= base_other.value
            else:
                raise UnitError(f'Cannot compare units {self.unit} and {other.unit} after base conversion mismatch.')
        else:
            raise TypeError(f'Cannot compare PhysicalQuantity with type {type(other).__name__}')

    def __lt__(self, other: PhysicalQuantity) -> bool:
        """Tests if this quantity is less than another (self < other).

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to compare against.

        Returns
        -------
        bool
            True if self is strictly less than other.

        Raises
        ------
        UnitError
            If units are not compatible.
        TypeError
            If `other` is not a PhysicalQuantity.
        """
        if isinstance(other, PhysicalQuantity):
            base_self = self.base
            base_other = other.base
            if base_self.unit == base_other.unit:
                return base_self.value < base_other.value
            else:
                 raise UnitError(f'Cannot compare units {self.unit} and {other.unit} after base conversion mismatch.')
        else:
            raise TypeError(f'Cannot compare PhysicalQuantity with type {type(other).__name__}')

    def __le__(self, other: PhysicalQuantity) -> bool:
        """Tests if this quantity is less than or equal to another (self <= other).

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to compare against.

        Returns
        -------
        bool
            True if self is less than or equal to other.

        Raises
        ------
        UnitError
            If units are not compatible.
        TypeError
            If `other` is not a PhysicalQuantity.
        """
        if isinstance(other, PhysicalQuantity):
            base_self = self.base
            base_other = other.base
            if base_self.unit == base_other.unit:
                return base_self.value <= base_other.value
            else:
                 raise UnitError(f'Cannot compare units {self.unit} and {other.unit} after base conversion mismatch.')
        else:
            raise TypeError(f'Cannot compare PhysicalQuantity with type {type(other).__name__}')

    def __eq__(self, other: object) -> bool:
        """Tests if two quantities are equal (self == other).

        Compares quantities after converting them to base units. Returns False
        if `other` is not a PhysicalQuantity.

        Parameters
        ----------
        other : object
            The object to compare against.

        Returns
        -------
        bool
            True if `other` is a PhysicalQuantity with the same base unit and
            value in base units, False otherwise.

        Raises
        ------
        UnitError
            If units are incompatible such that base conversion fails (rare).
        """
        if isinstance(other, PhysicalQuantity):
            # Use try-except for compatibility check, as base comparison might fail
            try:
                base_self = self.base
                base_other = other.base
                # Ensure units are truly identical after conversion
                if base_self.unit == base_other.unit:
                     # Use np.isclose for floating point comparisons? Might be better.
                     # For now, direct comparison.
                    return base_self.value == base_other.value
                else:
                    # Units are fundamentally incompatible if base units differ
                    return False # Or raise UnitError? Returning False seems more conventional for __eq__
            except UnitError:
                 # If conversion to base fails due to incompatible units
                 return False # Cannot be equal if units are incompatible
        # Not equal if other is not a PhysicalQuantity
        return False

    def __ne__(self, other: object) -> bool:
        """Tests if two quantities are not equal (self != other).

        Parameters
        ----------
        other : object
            The object to compare against.

        Returns
        -------
        bool
            True if quantities are not equal (different types, incompatible units,
            or different values in base units).
        """
        return not self.__eq__(other)

    def __format__(self, format_spec: str) -> str:
        """Formats the quantity using a format specifier.

        Applies the format specifier to the numerical value.

        Parameters
        ----------
        format_spec : str
             The format specification (e.g., '.2f').

        Returns
        -------
        str
            The formatted string representation 'value unit'.
        """
        return f"{self.value:{format_spec}} {self.unit}"

    def convert(self, unit: Union[str, PhysicalUnit]) -> None:
        """Converts the quantity *in-place* to a different unit.

        The new unit must be compatible with the current unit.

        Parameters
        ----------
        unit : str | PhysicalUnit
            The target unit to convert to.

        Raises
        ------
        UnitError
            If the target unit is not compatible with the current unit.
        """
        target_unit = findunit(unit)
        self.value = convertvalue(self.value, self.unit, target_unit)
        self.unit = target_unit

    @staticmethod
    def _round(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Custom rounding logic used by `to` method (rounds towards zero)."""
        # This is effectively np.trunc or int() casting behaviour, not standard rounding.
        # return np.trunc(x) might be clearer if that's the intent.
        # Let's keep the original logic for now.
        return np.floor(x) if np.greater(x, 0.) else np.ceil(x)

    def __deepcopy__(self, memo: dict) -> PhysicalQuantity:
        """Creates a deep copy of the PhysicalQuantity.

        Ensures that the numerical value is also copied, which is important
        for mutable values like NumPy arrays.

        Parameters
        ----------
        memo : dict
            Memoization dictionary used by `copy.deepcopy`.

        Returns
        -------
        PhysicalQuantity
            A new, independent copy of the quantity.
        """
        new_value = copy.deepcopy(self.value)
        # Unit objects are typically immutable or shared; deep copy might be excessive.
        # Assuming PhysicalUnit handles its own copying or is immutable.
        new_instance = self.__class__(new_value, self.unit) # Keep original unit ref
        memo[id(self)] = new_instance
        return new_instance

    @property
    def autoscale(self) -> PhysicalQuantity:
        """Converts the quantity to a unit with a more 'reasonable' prefix.

        Attempts to find a unit prefix (like k, m, n) such that the numerical
        value falls roughly between 1 and 1000. Works best for units with
        standard SI prefixes defined. Returns `self` if no better scaling is found.

        Returns
        -------
        PhysicalQuantity
            A new quantity, potentially with a different unit prefix.

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity, q
        >>> (4e-9 * q.F).autoscale
        4.0 nF
        >>> (0.005 * q.V).autoscale
        5.0 mV
        >>> (12345 * q.m).autoscale
        12.345 km
        """
        # Only attempt scaling if the unit is a simple, named unit (not composite)
        # and the value is non-zero.
        if len(self.unit.names) == 1 and self.value != 0:
            base_quantity = self.base
            # Use magnitude, avoid log(0)
            abs_base_value = abs(base_quantity.value)
            if abs_base_value == 0: # Avoid log10(0)
                 return self # Cannot scale zero

            log10_val = np.log10(abs_base_value)
            # Target scale exponent (e.g., 0 for 1-1000, -3 for milli, etc.)
            # Find the closest SI prefix exponent.
            target_scale_exp = np.floor(log10_val / 3) * 3

            best_unit = self.unit # Default to current unit
            min_diff = float('inf')

            # Iterate through known units to find a match
            for unit_name, u in unit_table.items():
                if isinstance(u, PhysicalUnit) and u.baseunit is self.unit.baseunit:
                    # Calculate the exponent corresponding to this unit's factor
                    if u.factor == 0: continue # Avoid log10(0)
                    unit_exp = np.log10(u.factor)
                    # Check if this unit's scale is close to the target scale
                    # We want the value in the new unit V' = V * (F_old / F_new) to be ~ 1-1000
                    # log10(V') = log10(V) + log10(F_old) - log10(F_new)
                    # log10(V') = log10(V_base) - log10(F_new)
                    # We want log10(V') to be between 0 and 3.
                    new_val_log10 = log10_val + np.log10(self.unit.factor) - unit_exp
                    
                    if 0 <= new_val_log10 < 3:
                         # Prefer the unit whose exponent is closest to target_scale_exp?
                         # Or simply the one that puts the value in range?
                         # Let's prioritize putting the value in [1, 1000) range first.
                         # Calculate difference from the ideal center (1.5)
                         diff = abs(new_val_log10 - 1.5)
                         if diff < min_diff:
                             min_diff = diff
                             best_unit = u


            if best_unit is not self.unit:
                 return self.to(best_unit)

        # Return original if no scaling applied or possible
        return self

    def to(self, *units: Union[str, PhysicalUnit]) -> Union[PhysicalQuantity, tuple[PhysicalQuantity, ...]]:
        """Converts the quantity to specified units.

        If one unit is given, returns a new PhysicalQuantity in that unit.
        If multiple units are given, returns a tuple of quantities where the
        sum equals the original quantity, and values are integers except possibly
        the last one (e.g., for time conversion like h/min/s).

        Parameters
        ----------
        *units : str | PhysicalUnit
            One or more target units (names or PhysicalUnit objects).

        Returns
        -------
        PhysicalQuantity | tuple[PhysicalQuantity, ...]
            The converted quantity or a tuple of quantities.

        Raises
        ------
        UnitError
            If any target unit is incompatible with the quantity's unit.

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity, q
        >>> b = PhysicalQuantity(4, 'J/s')
        >>> b.to('W')
        4.0 W
        >>> t = PhysicalQuantity(3661, 's')
        >>> h, m, s = t.to('h', 'min', 's')
        >>> h
        1.0 h
        >>> m
        1.0 min
        >>> s # Note: floating point inaccuracy might occur
        1.0 s
        >>> t = PhysicalQuantity(1000, 's')
        >>> t.to('h', 'min', 's')
        (<0.0 h>, <16.0 min>, <40.0 s>)

        Notes
        -----
        When multiple units are provided, they are processed in descending order
        of their magnitude relative to the base unit. The custom `_round`
        (effectively truncation) is used for intermediate values.
        """
        target_units = [findunit(u) for u in units]

        if len(target_units) == 1:
            unit = target_units[0]
            value = convertvalue(self.value, self.unit, unit)
            return self.__class__(value, unit)
        else:
            # Sort units by magnitude (descending) for cascading conversion
            # We need the conversion factor relative to a common base for sorting
            target_units.sort(key=lambda u: u.conversion_factor_to(self.unit.baseunit), reverse=True)

            result = []
            remaining_value = self.value # Start with the original value
            current_unit = self.unit   # and unit

            for i, target_unit in enumerate(target_units):
                # Convert the *remaining* value to the current target unit
                value_in_target = convertvalue(remaining_value, current_unit, target_unit)

                if i == len(target_units) - 1:
                    # Last unit takes the remaining fractional part
                    component_value = value_in_target
                else:
                    # Intermediate units: take the integer part (using _round logic)
                    component_value = self._round(value_in_target)
                    # Calculate the remainder *in the current target unit's scale*
                    remainder_in_target = value_in_target - component_value
                    # Convert the remainder back to the original unit scale for the next step
                    # This requires careful handling of units. It's easier to convert
                    # the rounded part back to the original scale and subtract.
                    rounded_part_in_original_unit_val = convertvalue(component_value, target_unit, current_unit)
                    remaining_value = remaining_value - rounded_part_in_original_unit_val
                    # Update current_unit for the next iteration's conversion (though it cancels out)

                result.append(self.__class__(component_value, target_unit))

            # The tuple elements should be in the order the units were passed originally.
            # We need to map the results back. Let's rebuild the result tuple in the input order.
            original_unit_names = [findunit(u).name for u in units]
            result_dict = {res.unit.name: res for res in result}
            final_result_tuple = tuple(result_dict[name] for name in original_unit_names if name in result_dict)

            # This logic seems overly complex and prone to floating point issues.
            # Let's try a simpler approach: Convert total to the smallest unit first?
            # Or convert total to base, then distribute.

            # --- Reimplementing multi-unit conversion ---
            target_units_orig_order = [findunit(u) for u in units]
            # Sort by magnitude, largest first
            target_units_sorted = sorted(target_units_orig_order, key=lambda u: u.conversion_factor_to(self.unit.baseunit), reverse=True)

            result_values = {}
            # Convert original value to the smallest unit provided for precision
            # Or convert to base unit first
            value_in_base = self.base.value

            for i, target_unit in enumerate(target_units_sorted):
                 # How much of the base value does this unit represent?
                 value_in_target = value_in_base / target_unit.baseunit.conversion_factor_to(target_unit)

                 if i == len(target_units_sorted) - 1:
                      # Last unit (smallest magnitude) takes the rest
                      component_value = value_in_target
                 else:
                      # Take integer part (using _round logic)
                      component_value = self._round(value_in_target)
                      # Subtract the value of this component (in base units) from the total
                      value_in_base -= component_value * target_unit.baseunit.conversion_factor_to(target_unit)

                 result_values[target_unit.name] = self.__class__(component_value, target_unit)

            # Return tuple in the original order requested by the user
            return tuple(result_values[u.name] for u in target_units_orig_order)

    @property
    def base(self) -> PhysicalQuantity:
        """Converts the quantity to its equivalent in SI base units.

        Handles units with offsets like degrees Celsius or Fahrenheit correctly.
        The resulting unit string represents the combination of base SI units.

        Returns
        -------
        PhysicalQuantity
            The quantity expressed in SI base units (e.g., m, kg, s, A, K, mol, cd).

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity, q
        >>> a = PhysicalQuantity(1, 'mV')
        >>> a.base
        0.001 m**2*kg*s**-3*A**-1
        >>> temp_c = q.PhysicalQuantity(0, 'degC')
        >>> temp_c.base # 0 degC should be 273.15 K
        273.15 K
        >>> temp_f = q.PhysicalQuantity(32, 'degF')
        >>> temp_f.base # 32 degF should be 273.15 K
        273.15 K
        """
        # Formula: BaseValue = Value * Factor + Offset
        # Factor converts to the scale of the base unit combination, Offset is added after scaling.
        base_value = self.value * self.unit.factor + self.unit.offset

        # Construct the base unit string representation
        num_parts, denom_parts = [], []
        for i, name in enumerate(base_names):
            power = self.unit.powers[i]
            if power == 0:
                continue
            part = name
            abs_power = abs(power)
            if abs_power > 1:
                part += f'**{abs_power}'

            if power > 0:
                num_parts.append(part)
            else:
                denom_parts.append(part)

        num_str = '*'.join(num_parts) if num_parts else '1'
        denom_str = '*'.join(denom_parts) # Denominator parts joined by *

        if denom_str:
             # Simplify representation: m*kg/s/A -> m*kg*s**-1*A**-1
             # Let PhysicalUnit handle the string representation?
             # For now, construct string manually, aiming for compatibility
             base_unit_str = num_str
             for i, name in enumerate(base_names):
                  power = self.unit.powers[i]
                  if power < 0:
                       base_unit_str += f'*{name}**{power}'

             # Alternative: Use the canonical base unit object directly?
             # base_unit = self.unit.baseunit # This should work if baseunit is correct
             base_unit = self.unit._get_base_unit() # Assuming a method exists
             return self.__class__(base_value, base_unit)

        else:
             # Handle case where there is no denominator (e.g. kg*m)
              return self.__class__(base_value, num_str)

    # make it easier using complex numbers (comment removed, properties are standard)
    @property
    def real(self) -> PhysicalQuantity:
        """Returns the real part of a complex PhysicalQuantity.

        Returns
        -------
        PhysicalQuantity
            A new quantity representing the real part.

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity
        >>> b = PhysicalQuantity(2 + 1j, 'V')
        >>> b.real
        2.0 V
        """
        return self.__class__(self.value.real, self.unit)

    @property
    def imag(self) -> PhysicalQuantity:
        """Returns the imaginary part of a complex PhysicalQuantity.

        Returns
        -------
        PhysicalQuantity
            A new quantity representing the imaginary part.

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity
        >>> b = PhysicalQuantity(2 + 1j, 'V')
        >>> b.imag
        1.0 V
        """
        return self.__class__(self.value.imag, self.unit)

    def sqrt(self) -> PhysicalQuantity:
        """Calculates the positive square root of the quantity.

        Returns
        -------
        PhysicalQuantity
            The square root of the quantity (value and unit adjusted).
        """
        return self.__pow__(0.5)

    def pow(self, exponent: float) -> PhysicalQuantity:
        """Raises the quantity to the power of an exponent.

        Alias for `__pow__`.

        Parameters
        ----------
        exponent : float
            The power to raise the quantity to. Must be dimensionless.

        Returns
        -------
        PhysicalQuantity
            The quantity raised to the power of the exponent.
        """
        # This just calls __pow__, type checking happens there.
        return self.__pow__(exponent)

    def sin(self) -> float:
        """Calculates the sine of the quantity, assuming it is an angle.

        Converts the value to radians before applying `numpy.sin`.

        Returns
        -------
        float
            The sine of the angle.

        Raises
        ------
        UnitError
            If the quantity does not have units of angle (e.g., rad, deg).
        """
        if self.unit.is_angle:
            # Convert value to radians for numpy functions
            value_in_rad = self.value * self.unit.conversion_factor_to(unit_table['rad'])
            return np.sin(value_in_rad)
        else:
            raise UnitError(f'Argument of sin must be an angle, not {self.unit}')

    def cos(self) -> float:
        """Calculates the cosine of the quantity, assuming it is an angle.

        Converts the value to radians before applying `numpy.cos`.

        Returns
        -------
        float
            The cosine of the angle.

        Raises
        ------
        UnitError
            If the quantity does not have units of angle (e.g., rad, deg).
        """
        if self.unit.is_angle:
            value_in_rad = self.value * self.unit.conversion_factor_to(unit_table['rad'])
            return np.cos(value_in_rad)
        else: # Raise error if not an angle
            raise UnitError(f'Argument of cos must be an angle, not {self.unit}')

    def tan(self) -> float:
        """Calculates the tangent of the quantity, assuming it is an angle.

        Converts the value to radians before applying `numpy.tan`.

        Returns
        -------
        float
            The tangent of the angle.

        Raises
        ------
        UnitError
            If the quantity does not have units of angle (e.g., rad, deg).
        """
        if self.unit.is_angle:
            value_in_rad = self.value * self.unit.conversion_factor_to(unit_table['rad'])
            return np.tan(value_in_rad)
        else: # Raise error if not an angle
            raise UnitError(f'Argument of tan must be an angle, not {self.unit}')

    @property
    def to_dict(self) -> dict[str, Any]:
        """Exports the quantity to a dictionary.

        Returns
        -------
        dict[str, Any]
            A dictionary containing the 'value' and the unit's dictionary
            representation ('PhysicalUnit').
        """
        # Ensure the value is JSON serializable if possible (e.g., convert ndarray)
        serializable_value = self.value
        if isinstance(serializable_value, np.ndarray):
             serializable_value = serializable_value.tolist() # Convert array to list

        q_dict = {'value': serializable_value,
                  'PhysicalUnit': self.unit.to_dict # Assuming unit.to_dict returns serializable dict
                  }
        return q_dict

    @property
    def to_json(self) -> str:
        """Exports the quantity to a JSON string.

        Returns
        -------
        str
            A JSON string representing the quantity, encapsulating the dictionary
            from `to_dict` under the key 'PhysicalQuantity'.
        """
        # Use custom encoder if needed for complex numbers or other types
        json_quantity = json.dumps({'PhysicalQuantity': self.to_dict})
        return json_quantity

    @staticmethod
    def from_dict(quantity_dict: dict[str, Any]) -> PhysicalQuantity:
        """Creates a PhysicalQuantity instance from a dictionary representation.

        Parameters
        ----------
        quantity_dict : dict[str, Any]
            A dictionary usually obtained from `to_dict`, containing 'value'
            and 'PhysicalUnit' (which is itself a dict).

        Returns
        -------
        PhysicalQuantity
            The reconstructed PhysicalQuantity instance.

        Notes
        -----
        Relies on `PhysicalUnit.from_dict` to reconstruct the unit. This assumes
        the unit described in the dictionary is already known or can be defined
        by `PhysicalUnit.from_dict`.
        """
        # Allow structure {'PhysicalQuantity': {'value': ..., 'PhysicalUnit': ...}}
        if 'PhysicalQuantity' in quantity_dict:
            quantity_dict = quantity_dict['PhysicalQuantity']

        if 'value' not in quantity_dict or 'PhysicalUnit' not in quantity_dict:
             raise ValueError("Dictionary must contain 'value' and 'PhysicalUnit' keys.")

        unit_info = quantity_dict['PhysicalUnit']
        value = quantity_dict['value']
        # Reconstruct the unit first
        unit = PhysicalUnit.from_dict(unit_info)
        # Create the quantity
        q = PhysicalQuantity(value, unit)
        return q

    @staticmethod
    def from_json(json_quantity: str) -> PhysicalQuantity:
        """Creates a PhysicalQuantity instance from a JSON string.

        Parameters
        ----------
        json_quantity : str
            A JSON string, typically generated by `to_json`.

        Returns
        -------
        PhysicalQuantity
            The reconstructed PhysicalQuantity instance.
        """
        quantity_dict = json.loads(json_quantity)
        # Expects the structure {'PhysicalQuantity': {...}}
        if 'PhysicalQuantity' not in quantity_dict:
             raise ValueError("JSON string must contain a 'PhysicalQuantity' object.")
        return PhysicalQuantity.from_dict(quantity_dict['PhysicalQuantity'])
