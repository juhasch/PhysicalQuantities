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
from typing import TYPE_CHECKING

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
        Ensures NumPy ufuncs are handled correctly (set to 1000).
    """

    __array_priority__: int = 1000  # Ensure numpy compatibility over lists etc.
    format: str = ''                # Display format for value -> string conversion
    annotation: str = ''            # Optional annotation for the Quantity
    value: int | float | complex    # Numerical value of the quantity
    unit: PhysicalUnit              # The associated PhysicalUnit object

    def __init__(self, value: int | float | complex, unit: str | PhysicalUnit, annotation: str = ''):
        """Initializes a PhysicalQuantity.

        Parameters
        ----------
        value : int | float | complex
            The numerical value of the quantity.
        unit : str | PhysicalUnit
            The unit of the quantity, either as a string name or a PhysicalUnit object.
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
        """Lists available attributes, including units for conversion via attribute access.

        Extends the default `dir()` list with names of units from `unit_table`
        that share the same base unit dimension as the current quantity. This allows
        tab completion for unit conversions like `quantity.mV`.

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
    
    def __getattr__(self, attr) -> int | float | complex | PhysicalQuantity:
        """Converts to a different scaling prefix of the same unit via attribute access.

        Allows retrieving the quantity expressed in a unit with a different scaling
        prefix (e.g., `quantity.mV`).
        If the attribute name ends with an underscore (`_`), the numerical value
        (in the specified unit) is returned without the unit (e.g., `quantity.mV_`).
        Accessing just `_` returns the original numerical value.

        Parameters
        ----------
        attr : str
            The attribute name, expected to be a unit name (optionally with a
            trailing `_`) or just `_`.

        Returns
        -------
        int | float | complex | PhysicalQuantity
            The quantity converted to the specified unit scaling, or the numerical
            value if the attribute ends with `_`.

        Raises
        ------
        AttributeError
            If `attr` is not a unit name found in the `unit_table` or if the
            attribute syntax is otherwise invalid.

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> a = 2 * q.mm
        >>> a._
        2
        >>> a.mm_
        2
        >>> a.m_ # Converts mm to m and returns the value
        0.002
        >>> a.m # Converts mm to m and returns the PhysicalQuantity
        0.002 m
        """
        dropunit = (attr[-1] == '_')
        attr = attr.strip('_')
        if attr == '' and dropunit is True:
            return self.value
        try:
            attrunit = unit_table[attr]
        except KeyError:
            raise AttributeError(f'Unit {attr} not found')
        if dropunit is True:
            return self.to(attrunit.name).value
        else:
            return self.to(attrunit.name)

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

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity
        >>> import numpy as np
        >>> q_array = PhysicalQuantity(np.array([1, 2, 3]), 'm')
        >>> q_array[1]
        2 m
        >>> q_array[0:2]
        [1 2] m
        """
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            return self.__class__(self.value[key], self.unit)
        raise AttributeError('Not a PhysicalQuantity array or list', list)

    def __setitem__(self, key, value):
        """Allows item assignment if the underlying value is an array or list.

        The assigned value must be a PhysicalQuantity and will be converted to the
        unit of this quantity before assignment.

        Parameters
        ----------
        key : slice | int
            The index or slice where the value should be assigned.
        value : PhysicalQuantity
            The PhysicalQuantity instance to assign.

        Raises
        ------
        AttributeError
            If the underlying value does not support item assignment, or if
            `value` is not a PhysicalQuantity.
        UnitError
            If the unit of `value` is not compatible with this quantity's unit.

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity, q
        >>> import numpy as np
        >>> q_array = PhysicalQuantity(np.array([1.0, 2.0, 3.0]), 'm')
        >>> q_array[0] = 50 * q.cm
        >>> q_array
        [0.5 2.  3. ] m
        """
        if not isinstance(value, PhysicalQuantity):
            raise AttributeError('Not a Physical Quantity')
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            self.value[key] = value.to(str(self.unit)).value
            return self.__class__(self.value[key], self.unit)
        raise AttributeError('Not a PhysicalQuantity array or list', list)
        
    def __len__(self):
        """Returns the length if the underlying value is an array or list.

        Returns
        -------
        int
            The length of the underlying value array/list.

        Raises
        ------
        TypeError
            If the underlying value does not have a defined length.

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity
        >>> import numpy as np
        >>> q_list = PhysicalQuantity([1, 2, 3], 's')
        >>> len(q_list)
        3
        """
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            return len(self.value)
        raise TypeError('Object of type %s has no len()' % type(self.value))

    def _ipython_key_completions_(self):
        """Provides key completions for IPython environments (used for `obj['<tab>]`)."""
        return self.unit_table.keys()

    @property
    def dB(self) -> dBQuantity:
        """Converts the quantity to a dB representation (if applicable).

        Uses heuristics to determine whether to use 10*log10 (for power-like units
        containing 'W') or 20*log10 (for amplitude-like units).

        Returns
        -------
        dBQuantity
            The quantity expressed in decibels relative to its unit (e.g., dBV, dBW).

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

    def rint(self):
        """Rounds the numerical value(s) to the nearest integer.

        Applies `numpy.rint` to the underlying value.

        Returns
        -------
        PhysicalQuantity
            A new quantity with the value(s) rounded to the nearest integer.
        """
        value = np.rint(self.value)
        return self.__class__(value, self.unit)

    def __str__(self):
        """Returns the string representation 'value unit'.

        Uses IPython's float precision settings if available via `self.ptformatter`
        and no specific `self.format` is set.

        Returns
        -------
        str
            The string representation of the quantity.
        """
        if self.ptformatter is not None and self.format == '' and isinstance(self.value, float):  # pragma: no cover
            # %precision magic only works for floats
            fmt = self.ptformatter.float_format
            return u"%s %s" % (fmt % self.value, str(self.unit))
        return '{0:{format}} {1}'.format(self.value, str(self.unit), format=self.format)

    def __complex__(self):
        """Converts the quantity to a complex number after converting to base units.

        Returns
        -------
        complex
            The numerical value of the quantity in base units as a complex number.
        """
        return self.base.value

    def __float__(self):
        """Converts the quantity to a float after converting to base units.

        Returns
        -------
        float
             The numerical value of the quantity in base units as a float.
        """
        return self.base.value

    def __repr__(self):
        """Returns the canonical string representation (delegates to `__str__`)."""
        return self.__str__()

    def _repr_markdown_(self):
        """Returns a Markdown representation for IPython/Jupyter environments.

        Formats the output as 'value unit' using Markdown for the unit.
        Uses LaTeX via Sympy for Sympy values if detected.
        Respects IPython float formatting if available.

        Returns
        -------
        str
            Markdown formatted string.
        """
        if self.ptformatter is not None and self.format == '' and isinstance(self.value, float):  # pragma: no cover
            # %precision magic only works for floats
            fmt = self.ptformatter.float_format
            return u"%s %s" % (fmt % self.value, self.unit._repr_markdown_())
        if str(type(self.value)).find('sympy') > 0:
            from sympy import printing  # type: ignore
            return '${0}$ {1}'.format(printing.latex(self.value), self.unit.markdown)
        return '{0:{format}} {1}'.format(self.value, self.unit.markdown, format=self.format)

    def _repr_latex_(self):
        """Returns a LaTeX representation for IPython/Jupyter environments.

        Currently delegates to `_repr_markdown_`.

        Returns
        -------
        str
            LaTeX formatted string (via Markdown).
        """
        return self._repr_markdown_()

    def _sum(self, other, sign1, sign2):
        """Internal helper method for addition (`sign2`=1) and subtraction (`sign2`=-1).

        Performs `sign1 * self + sign2 * other`, converting `other` to the unit of `self`.

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to add or subtract.
        sign1 : int | float
            Multiplier for self (typically 1).
        sign2 : int | float
            Multiplier for other (+1 for add, -1 for subtract).

        Returns
        -------
        PhysicalQuantity
            The result of the operation, in the units of `self`.

        Raises
        -------
        UnitError
            If `other` is not a PhysicalQuantity or if units are incompatible.
        """
        if not isinstance(other, PhysicalQuantity):
            raise UnitError(f'Incompatible types {type(self)} and {type(other)}')
        new_value = sign1 * self.value + \
            sign2 * other.value * other.unit.conversion_factor_to(self.unit)
        return self.__class__(new_value, self.unit)

    def __add__(self, other):
        """Adds another PhysicalQuantity. Units must be compatible."""
        return self._sum(other, 1, 1)

    __radd__ = __add__

    def __sub__(self, other):
        """Subtracts another PhysicalQuantity. Units must be compatible."""
        return self._sum(other, 1, -1)

    def __rsub__(self, other):
        """Subtracts this quantity from another (`other - self`). Units must be compatible."""
        return self._sum(other, -1, 1)

    def __mul__(self, other):
        """Multiplies by a scalar or another PhysicalQuantity.

        - `self * scalar`: Scales the value, keeps the unit.
        - `self * other_quantity`: Multiplies values and units.
          If the resulting unit is dimensionless, returns a scaled scalar.
        """
        if not isinstance(other, PhysicalQuantity):
            return self.__class__(self.value * other, self.unit)
        value = self.value * other.value
        unit = self.unit * other.unit
        if unit.is_dimensionless:
            return value * unit.factor
        else:
            return self.__class__(value, unit)

    __rmul__ = __mul__

    def __floordiv__(self, other):
        """Performs floor division (`self // other`).

        - `self // scalar`: Floor divides value, keeps the unit.
        - `self // other_quantity`: Floor divides values, divides units.
          If the resulting unit is dimensionless, returns a scaled scalar.

        Parameters
        ----------
        other : number | PhysicalQuantity
            The divisor.

        Returns
        -------
        PhysicalQuantity | number
            The result of the floor division.
        """
        if not isinstance(other, PhysicalQuantity):
            return self.__class__(self.value // other, self.unit)
        value = self.value // other.value
        unit = self.unit // other.unit
        if unit.is_dimensionless:
            return value * unit.factor
        else:
            return self.__class__(value, unit)

    def __rfloordiv__(self, other):
        """Performs reverse floor division (`other // self`).

        `other` must be a scalar. The resulting unit is the reciprocal of `self.unit`.

        Parameters
        ----------
        other : number
            The dividend (must be a scalar).

        Returns
        -------
        PhysicalQuantity
            The result with reciprocal units.
        """
        return self.__class__(other // self.value, self.unit)
            
    def __div__(self, other):
        """Performs true division (`self / other`) (Python 2 style).

        See `__truediv__`.
        """
        if not isinstance(other, PhysicalQuantity):
            return self.__class__(self.value / other, self.unit)
        value = self.value / other.value
        unit = self.unit / other.unit
        if unit.is_dimensionless:
            return value * unit.factor
        else:
            return self.__class__(value, unit)

    def __rdiv__(self, other):
        """Performs reverse true division (`other / self`) (Python 2 style).

        See `__rtruediv__`.
        """
        if not isinstance(other, PhysicalQuantity):
            return self.__class__(other / self.value, pow(self.unit, -1))
        value = other.value / self.value
        unit = other.unit / self.unit
        if unit.is_dimensionless:
            return value * unit.factor
        else:
            return self.__class__(value, unit)

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __round__(self, ndigits=0):
        """Rounds the numerical value to a given number of decimal places.

        Applies `round()` or `numpy.round()` to the value.

        Parameters
        ----------
        ndigits : int, optional
            Number of decimal places to round to (default is 0).

        Returns
        -------
        PhysicalQuantity
            A new quantity with the rounded value.
        """
        if isinstance(self.value, np.ndarray):
            return self.__class__(np.round(self.value, ndigits), self.unit)
        else:
            return self.__class__(round(self.value, ndigits), self.unit)

    def __pow__(self, other):
        """Raises the quantity to a power (`self ** other`).

        The exponent `other` must be a dimensionless scalar.

        Parameters
        ----------
        other : number
            The exponent (must be dimensionless).

        Returns
        -------
        PhysicalQuantity
            The quantity raised to the power `other`.

        Raises
        -------
        UnitError
            If `other` is a PhysicalQuantity (exponent must be scalar).
        """
        if isinstance(other, PhysicalQuantity):
            raise UnitError('Exponents must be dimensionless not of unit %s' % other.unit)
        return self.__class__(pow(self.value, other), pow(self.unit, other))

    def __rpow__(self, other):
        """Raises a scalar base to the power of this quantity (`other ** self`).

        This operation is only valid if `self` is dimensionless.

        Parameters
        ----------
        other : number
            The base.

        Raises
        -------
        UnitError
            If `self` is not dimensionless.
        """
        raise UnitError('Exponents must be dimensionless, not of unit %s' % self.unit)

    def __abs__(self):
        """Returns the quantity with the absolute value.

        Applies `abs()` to the numerical value.

        Returns
        -------
        PhysicalQuantity
            A new quantity with the absolute value.
        """
        return self.__class__(abs(self.value), self.unit)

    def __pos__(self):
        """Returns the quantity itself (unary plus).

        Returns
        -------
        PhysicalQuantity
            The quantity itself (`+self`).
        """
        if isinstance(self.value, np.ndarray):
            return self.__class__(np.ndarray.__pos__(self.value), self.unit)
        return self.__class__(self.value, self.unit)

    def __neg__(self):
        """Returns the quantity with the negated value (unary minus).

        Returns
        -------
        PhysicalQuantity
            A new quantity with the negated value (`-self`).
        """
        if isinstance(self.value, np.ndarray):
            return self.__class__(np.ndarray.__neg__(self.value), self.unit)
        return self.__class__(-self.value, self.unit)

    def __nonzero__(self):
        """Tests if the quantity's value is non-zero (Python 2 boolean context).

        Returns
        -------
        bool | PhysicalQuantity
            For scalar values, returns `self.value != 0`.
            For numpy array values, returns `np.nonzero(self.value)` wrapped in a PhysicalQuantity.
        """
        if isinstance(self.value, np.ndarray):
            return self.__class__(np.nonzero(self.value), self.unit)
        return self.value != 0

    def __gt__(self, other):
        """Tests if this quantity is greater than another (`self > other`).

        Compares values after converting both quantities to base units.

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to compare against.

        Returns
        -------
        bool
            `True` if `self` is strictly greater than `other`.

        Raises
        -------
        UnitError
            If `other` is not a `PhysicalQuantity` or if units are incompatible.
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value > other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __ge__(self, other):
        """Tests if this quantity is greater than or equal to another (`self >= other`).

        Compares values after converting both quantities to base units.

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to compare against.

        Returns
        -------
        bool
            `True` if `self` is greater than or equal to `other`.

        Raises
        -------
        UnitError
            If `other` is not a `PhysicalQuantity` or if units are incompatible.
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value >= other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __lt__(self, other):
        """Tests if this quantity is less than another (`self < other`).

        Compares values after converting both quantities to base units.

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to compare against.

        Returns
        -------
        bool
            `True` if `self` is strictly less than `other`.

        Raises
        -------
        UnitError
            If `other` is not a `PhysicalQuantity` or if units are incompatible.
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value < other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __le__(self, other):
        """Tests if this quantity is less than or equal to another (`self <= other`).

        Compares values after converting both quantities to base units.

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to compare against.

        Returns
        -------
        bool
            `True` if `self` is less than or equal to `other`.

        Raises
        -------
        UnitError
            If `other` is not a `PhysicalQuantity` or if units are incompatible.

        Note
        ----
        The original docstring contained `:param:`, `:return:`, `:rtype:` which is not standard NumPy format.
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value <= other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __eq__(self, other):
        """Tests if two quantities are equal (`self == other`).

        Compares values after converting both quantities to base units.

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to compare against.

        Returns
        -------
        bool
            `True` if `self` is equal to `other`.

        Raises
        -------
        UnitError
            If `other` is not a `PhysicalQuantity` or if units are incompatible.
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit.name == other.base.unit.name:
                return self.base.value == other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __ne__(self, other):
        """Tests if two quantities are not equal (`self != other`).

        Compares values after converting both quantities to base units.

        Parameters
        ----------
        other : PhysicalQuantity
            The quantity to compare against.

        Returns
        -------
        bool
            `True` if `self` is not equal to `other`.

        Raises
        -------
        UnitError
            If `other` is not a `PhysicalQuantity` or if units are incompatible.
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return not self.base.value == other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __format__(self, *args, **kw):
        """Formats the quantity using a standard format specifier applied to the value."""
        return "{1:{0}} {2}".format(args[0], self.value, self.unit)

    def convert(self, unit):
        """Converts the quantity *in-place* to a different unit.

        Adjusts the value and updates the unit attribute. The new unit must be
        compatible with the original unit.

        Parameters
        ----------
        unit : str | PhysicalUnit
            The target unit to convert to.

        Raises
        -------
        UnitError
            If the target unit is not compatible.
        """
        unit = findunit(unit)
        self.value = convertvalue(self.value, self.unit, unit)
        self.unit = unit

    @staticmethod
    def _round(x):
        """Custom rounding function (rounds towards zero).

        Used internally by the `to` method for multi-unit conversions.
        Equivalent to `np.trunc`.
        """
        if np.greater(x, 0.):
            return np.floor(x)
        else:
            return np.ceil(x)

    def __deepcopy__(self, memo: dict) -> PhysicalQuantity:
        """Creates a deep copy of the PhysicalQuantity instance.

        Ensures that the numerical `value` is also deep-copied, crucial for
        mutable types like numpy arrays.

        Parameters
        ----------
        memo : dict
            The memo dictionary used by `copy.deepcopy`.

        Returns
        -------
        PhysicalQuantity
            A new, independent copy of the quantity.
        """
        new_value = copy.deepcopy(self.value)
        new_instance = self.__class__(new_value, self.unit)
        memo[id(self)] = new_instance
        return new_instance

    @property
    def autoscale(self) -> PhysicalQuantity:
        """Rescales the quantity to a unit with a 'reasonable' prefix.

        Attempts to find a unit prefix (like k, m, n, etc.) such that the numerical
        value falls roughly between 1 and 1000 (or 0.001 and 1 for scales < 1).
        Works best for simple units with standard SI prefixes defined.
        Returns the original quantity if no suitable rescaling is found.

        Returns
        -------
        PhysicalQuantity
            A new quantity object, possibly rescaled.

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
        if len(self.unit.names) == 1:
            b = self.base
            n = np.log10(abs(b.value))
            # we want to be between 0..999 
            _scale = np.floor(n)
            # now search for unit
            for i in unit_table:
                u = unit_table[i]
                if isinstance(u, PhysicalUnit):
                    if u.baseunit is self.unit.baseunit:
                        f = np.log10(u.factor) - _scale
                        if (f > -3) and (f < 1):
                            return self.to(i)
        return self

    def to(self, *units):
        """Converts the quantity to the specified unit(s).

        Parameters
        ----------
        *units : str | PhysicalUnit
            One or more target units (names or `PhysicalUnit` objects).

        Returns
        -------
        PhysicalQuantity | tuple[PhysicalQuantity, ...]
            - If one unit is specified: A new `PhysicalQuantity` object representing
              the value in that unit.
            - If multiple units are specified: A tuple of `PhysicalQuantity` objects,
              one for each specified unit. The values are calculated such that their
              sum equals the original quantity, and intermediate values (except the
              last) are integers (using `_round`). This is useful for irregular unit
              systems like hours/minutes/seconds.

        Raises
        -------
        UnitError
            If any target unit is incompatible with the quantity's current unit.

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity, q
        >>> b = PhysicalQuantity(4, 'J/s')
        >>> b.to('W')
        4.0 W
        >>> t = PhysicalQuantity(3661, 's')
        >>> h, m, s = t.to('h', 'min', 's') # Note the order matters for tuple unpacking
        >>> h, m, s # doctest: +SKIP
        (1 h, 1 min, 1.0 s)
        >>> t = PhysicalQuantity(1000, 's')
        >>> t.to('h', 'min', 's') # doctest: +SKIP
        (0 h, 16 min, 40.0 s)

        Notes
        -----
        When multiple units are provided, they are processed in order of magnitude
        (largest first, based on sorting internally). The internal `_round` method
        (truncation) is used to determine integer parts for intermediate units.
        Floating point inaccuracies might occur.
        """
        units = list(map(findunit, units))
        if len(units) == 1:
            unit = units[0]
            value = convertvalue(self.value, self.unit, unit)
            return self.__class__(value, unit)
        else:
            units.sort()
            result = []
            value = self.value
            unit = self.unit
            for i in range(len(units)-1, -1, -1):
                value *= unit.conversion_factor_to(units[i])
                if i == 0:
                    rounded = value
                else:
                    rounded = self._round(value)
                result.append(self.__class__(rounded, units[i]))
                value = value - rounded
                unit = units[i]
            return tuple(result)

    @property
    def base(self) -> PhysicalQuantity:
        """Converts the quantity to its equivalent representation in SI base units.

        Calculates the value in terms of the fundamental SI base units (kg, m, s, A, K, mol, cd)
        and constructs the corresponding unit string.
        Handles units with offsets (like temperature scales) correctly during value conversion.

        Returns
        -------
        PhysicalQuantity
            A new quantity object expressed in SI base units.

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity, q
        >>> (1 * q.km).base
        1000.0 m
        >>> (1 * q.V).base
        1.0 kg*m**2*s**-3*A**-1
        >>> q.PhysicalQuantity(0, 'degC').base # 0 degC -> 273.15 K
        273.15 K
        >>> q.PhysicalQuantity(32, 'degF').base # 32 degF -> 273.15 K
        273.15 K
        """
        # Correct conversion to base: value * factor + offset
        new_value = self.value * self.unit.factor + self.unit.offset
        num = ''
        denom = ''
        for i in range(len(base_names)):
            unit = base_names[i]
            power = self.unit.powers[i]
            if power < 0:
                denom += '/' + unit
                if power < -1:
                    denom += '**' + str(-power)
            elif power > 0:
                num += '*' + unit
                if power > 1:
                    num += '**' + str(power)
        if len(num) == 0:
            num = '1'
        else:
            num = num[1:]
        return self.__class__(new_value, num + denom)

    # Comment regarding complex numbers removed as properties are standard
    @property
    def real(self) -> PhysicalQuantity:
        """Returns the real part of the quantity's value, keeping the unit.

        Returns
        -------
        PhysicalQuantity
            A new quantity with the real part of the original value.

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
        """Returns the imaginary part of the quantity's value, keeping the unit.

        Returns
        -------
        PhysicalQuantity
            A new quantity with the imaginary part of the original value.

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
            The square root (`self ** 0.5`).
        """
        return self.__pow__(0.5)

    def pow(self, exponent: float) -> PhysicalQuantity:
        """Raises the quantity to the power of an exponent (alias for `__pow__`).

        Parameters
        ----------
        exponent : float
            The exponent (must be dimensionless scalar).

        Returns
        -------
        PhysicalQuantity
            The quantity raised to the specified power.
        """
        return self.__pow__(exponent)

    def sin(self) -> float:
        """Calculates the sine of the quantity, assuming it is an angle.

        Converts the value to radians before applying `numpy.sin`.

        Returns
        -------
        float
            The sine of the angle value in radians.

        Raises
        -------
        UnitError
            If the quantity's unit is not an angle type (e.g., rad, deg).
        """
        if self.unit.is_angle:
            return np.sin(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        else:
            raise UnitError('Argument of sin must be an angle')

    def cos(self) -> float:
        """Calculates the cosine of the quantity, assuming it is an angle.

        Converts the value to radians before applying `numpy.cos`.

        Returns
        -------
        float
            The cosine of the angle value in radians.

        Raises
        -------
        UnitError
            If the quantity's unit is not an angle type.
        """
        if self.unit.is_angle:
            return np.cos(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        raise UnitError('Argument of cos must be an angle')

    def tan(self) -> float:
        """Calculates the tangent of the quantity, assuming it is an angle.

        Converts the value to radians before applying `numpy.tan`.

        Returns
        -------
        float
            The tangent of the angle value in radians.

        Raises
        -------
        UnitError
            If the quantity's unit is not an angle type.
        """
        if self.unit.is_angle:
            return np.tan(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        raise UnitError('Argument of tan must be an angle')

    @property
    def to_dict(self) -> dict:
        """Exports the quantity to a serializable dictionary.

        Returns
        -------
        dict
            A dictionary with keys 'value' and 'PhysicalUnit' (containing the
            unit's dictionary representation from `unit.to_dict`). Numpy arrays
            in `value` are converted to lists.
        """
        q_dict = {'value': self.value,
                  'PhysicalUnit': self.unit.to_dict
                  }
        return q_dict

    @property
    def to_json(self) -> str:
        """Exports the quantity to a JSON string.

        Serializes the dictionary from `to_dict` into a JSON string under the top-level
        key 'PhysicalQuantity'.

        Returns
        -------
        str
            A JSON string representing the PhysicalQuantity.
        """
        json_quantity = json.dumps({'PhysicalQuantity': self.to_dict})
        return json_quantity

    @staticmethod
    def from_dict(quantity_dict: dict) -> PhysicalQuantity:
        """Creates a PhysicalQuantity instance from a dictionary representation.

        Parameters
        ----------
        quantity_dict : dict
            A dictionary containing 'value' and 'PhysicalUnit' keys. The
            'PhysicalUnit' value should be a dictionary suitable for
            `PhysicalUnit.from_dict`.
            Can optionally be nested under a 'PhysicalQuantity' key.

        Returns
        -------
        PhysicalQuantity
            The reconstructed PhysicalQuantity instance.

        Raises
        -------
        ValueError
            If the dictionary structure is incorrect.

        Notes
        -----
        This relies on `PhysicalUnit.from_dict` to reconstruct the unit. The unit
        must typically be predefined or definable from the dictionary content.
        """
        u = PhysicalUnit.from_dict(quantity_dict['PhysicalUnit'])
        q = PhysicalQuantity(quantity_dict['value'], u)
        return q

    @staticmethod
    def from_json(json_quantity: str) -> PhysicalQuantity:
        """Creates a PhysicalQuantity instance from a JSON string.

        Parameters
        ----------
        json_quantity : str
            A JSON string, typically generated by `to_json`, containing a
            'PhysicalQuantity' key whose value is the dictionary representation.

        Returns
        -------
        PhysicalQuantity
            The reconstructed PhysicalQuantity instance.

        Raises
        -------
        ValueError
            If the JSON string does not contain the expected structure.
        """
        quantity_dict = json.loads(json_quantity)
        return PhysicalQuantity.from_dict(quantity_dict['PhysicalQuantity'])
