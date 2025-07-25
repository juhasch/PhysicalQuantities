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

        This method is called only if standard attribute lookup fails.

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
            If `attr` is not a unit name found in `unit_table`, if the found unit
            is incompatible with the quantity's unit, or if the attribute syntax
            is otherwise invalid.

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
        >>> a.base # Accesses the .base property, does not go through __getattr__
        0.002 m
        >>> a.kg # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        AttributeError: Unit 'kg' is not compatible with unit 'mm'
        """
        # Check if it's the special case for accessing the value directly
        if attr == '_':
            return self.value

        dropunit = (attr[-1] == '_')
        attr_unit_name = attr.strip('_')

        # Optimization: check unit_table *first*. If not there, it's not a unit attr.
        if attr_unit_name not in unit_table:
            # If it wasn't found in unit_table, raise standard AttributeError
            # This allows access to normal methods/properties like .base, .value etc.
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")

        # If it IS in unit_table, proceed with unit conversion logic
        try:
            attrunit = unit_table[attr_unit_name]
            # Check for dimensional compatibility BEFORE conversion using the 'powers' array
            if self.unit.powers != attrunit.powers:
                raise AttributeError(f"Unit '{attr_unit_name}' is not compatible with unit '{self.unit.name}' (dimension mismatch)")

            # If compatible, perform the conversion
            converted_quantity = self.to(attrunit.name)
            if dropunit:
                return converted_quantity.value
            else:
                return converted_quantity

        except KeyError:
            raise AttributeError(f'Unit {attr} not found')

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
    def np(self) -> np.ndarray:
        """ Return a numpy array with the unit as metadata attribute

         Returns
         -------
         np.ndarray
            dtype.metadata = dict(unit=PhysicalUnit)
         """
        if isinstance(self.value, np.ndarray):
            array = self.value
            metadata = dict(unit=str(self.unit))
            dtype = np.dtype(str(array.dtype), metadata=metadata)
            return array.astype(dtype)
        array = np.array(self.value)
        metadata = dict(unit=str(self.unit))
        dtype = np.dtype(dtype=array.dtype, metadata=metadata)
        array = array.astype(dtype)
        return array

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
        if isinstance(other, np.ndarray):
            metadata = other.dtype.metadata
            if metadata and 'unit' in metadata:
                other = PhysicalQuantity(other, metadata['unit'])
        return self._sum(other, 1, 1)

    __radd__ = __add__

    def __sub__(self, other):
        """Subtracts another PhysicalQuantity. Units must be compatible."""
        return self._sum(other, 1, -1)

    def __rsub__(self, other):
        """Subtracts this quantity from another (`other - self`). Units must be compatible."""
        # Check if other is a PhysicalQuantity
        if isinstance(other, PhysicalQuantity):
            # Delegate to other's subtraction method
            return other._sum(self, 1, -1) # other + (-1)*self
        else:
            # Subtraction of PhysicalQuantity from a scalar is ambiguous
            raise TypeError(f"Unsupported operand type(s) for -: '{type(other).__name__}' and '{type(self).__name__}'")

    def __mul__(self, other):
        """Multiplies by a scalar or another PhysicalQuantity.

        - `self * scalar`: Scales the value, keeps the unit.
        - `self * other_quantity`: Multiplies values and units.
          If the resulting unit is dimensionless, returns a scaled scalar.
        """
        if not isinstance(other, PhysicalQuantity):
            # Handle quantity * scalar or quantity * unit
            if isphysicalunit(other):
                # quantity * unit
                value = self.value  # Value remains the same
                unit = self.unit * other  # Multiply units
                if unit.is_dimensionless:
                    # If result is dimensionless, return scaled scalar value
                    return value * unit.factor
                else:
                    # Return new quantity with combined unit
                    return self.__class__(value, unit)
            else:
                # Assume quantity * scalar (or list, array, complex, etc.)
                # Revert to simpler multiplication, relying on self.value's behavior
                # This handles numeric types, lists, arrays via duck typing / NumPy overload
                return self.__class__(self.value * other, self.unit)
        else:
            # Handle quantity * quantity
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
        
        Raises
        ------
        TypeError
            If `other` is a PhysicalQuantity.
        """
        if isinstance(other, PhysicalQuantity):
            # Floor division between two quantities is handled by __floordiv__
            # Reverse floor division is not defined between two quantities in this way.
            raise TypeError(f"Unsupported operand type(s) for //: '{type(other).__name__}' and '{type(self).__name__}'")
        else:
            # Handle scalar // quantity
            value = other // self.value
            reciprocal_unit = 1 / self.unit
            return self.__class__(value, reciprocal_unit)
            
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
        # This method primarily handles scalar / quantity
        if isinstance(other, PhysicalQuantity):
            # Division between two quantities is handled by __div__ / __truediv__.
            # Reverse division is not defined between two quantities in this way.
             raise TypeError(f"Unsupported operand type(s) for /: '{type(other).__name__}' and '{type(self).__name__}'")
        else:
            # Handle scalar / quantity
            value = other / self.value
            reciprocal_unit = 1 / self.unit
            return self.__class__(value, reciprocal_unit)

    __truediv__ = __div__
    __rtruediv__ = __rdiv__ # Alias __rtruediv__ to the corrected __rdiv__

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

    # __nonzero__ is Python 2. Use __bool__ in Python 3.
    def __bool__(self) -> bool:
        """Tests if the quantity's value is non-zero (Python 3 boolean context).

        This method provides the standard boolean interpretation used in contexts like `if quantity:`.

        Returns
        -------
        bool
            `True` if the value is non-zero, `False` otherwise.
            For array values, tests if *any* element is non-zero using `numpy.any()`.
        """
        if isinstance(self.value, np.ndarray):
            # Correct Python 3 boolean context: check if *any* element is non-zero
            # Explicitly cast numpy.bool_ to standard Python bool
            return bool(np.any(self.value))
        # Standard boolean conversion for scalars
        return bool(self.value)

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
        TypeError
            If `other` is not a `PhysicalQuantity`.
        UnitError
            If units are incompatible.
        """
        if not isinstance(other, PhysicalQuantity):
            # Raise TypeError for comparison with incompatible types
            raise TypeError(f"\'>' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        # Check dimensional compatibility first
        if self.unit.powers != other.unit.powers:
            raise UnitError(f'Cannot compare quantities with incompatible units: {self.unit} and {other.unit}')
        # Compare values in base units
        return self.base.value > other.base.value

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
        TypeError
            If `other` is not a `PhysicalQuantity`.
        UnitError
            If units are incompatible.
        """
        if not isinstance(other, PhysicalQuantity):
            raise TypeError(f"\'>=' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        if self.unit.powers != other.unit.powers:
            raise UnitError(f'Cannot compare quantities with incompatible units: {self.unit} and {other.unit}')
        return self.base.value >= other.base.value

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
        TypeError
            If `other` is not a `PhysicalQuantity`.
        UnitError
            If units are incompatible.
        """
        if not isinstance(other, PhysicalQuantity):
            raise TypeError(f"\'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        if self.unit.powers != other.unit.powers:
            raise UnitError(f'Cannot compare quantities with incompatible units: {self.unit} and {other.unit}')
        return self.base.value < other.base.value

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
        TypeError
            If `other` is not a `PhysicalQuantity`.
        UnitError
            If units are incompatible.
        """
        if not isinstance(other, PhysicalQuantity):
            raise TypeError(f"\'<=' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        if self.unit.powers != other.unit.powers:
            raise UnitError(f'Cannot compare quantities with incompatible units: {self.unit} and {other.unit}')
        return self.base.value <= other.base.value

    def __eq__(self, other):
        """Tests if two quantities are equal (`self == other`).

        Compares values after converting both quantities to base units.
        Returns `False` if `other` is not a `PhysicalQuantity` or if units
        are dimensionally incompatible.

        Parameters
        ----------
        other : object
            The object to compare against.

        Returns
        -------
        bool
            `True` if `self` is equal to `other`.
        """
        if not isinstance(other, PhysicalQuantity):
            # According to Python data model, __eq__ should return False for different types
            return False
        # Check dimensional compatibility
        if self.unit.powers != other.unit.powers:
            # Dimensionally incompatible objects cannot be equal
            return False
        # Compare values in base units (consider np.isclose for floats if needed)
        return self.base.value == other.base.value

    def __ne__(self, other):
        """Tests if two quantities are not equal (`self != other`).

        Parameters
        ----------
        other : object
            The object to compare against.

        Returns
        -------
        bool
            `True` if `self` is not equal to `other`.
        """
        # Delegate to __eq__
        return not self.__eq__(other)

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

    # NumPy interoperability
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """Implements NumPy Universal Function (ufunc) support."""
        # Ensure the method is a standard call
        if method != '__call__':
            return NotImplemented

        # --- Prepare inputs ---
        # Convert inputs to values and units
        processed_inputs = []
        input_units = []
        for x in inputs:
            if isinstance(x, PhysicalQuantity):
                processed_inputs.append(x.value)
                input_units.append(x.unit)
            elif isinstance(x, (int, float, complex, list, np.ndarray)):
                processed_inputs.append(x)
                input_units.append(None) # Mark non-quantity inputs
            else:
                # Cannot handle other types
                return NotImplemented

        # --- Handle specific ufuncs ---

        # Division (np.true_divide)
        if ufunc is np.true_divide:
            if len(processed_inputs) != 2:
                return NotImplemented # Requires 2 arguments

            val1, val2 = processed_inputs
            unit1, unit2 = input_units

            # Calculate result value
            # Check for output argument and handle if necessary (ignoring for now)
            if 'out' in kwargs:
                # For simplicity, we don't support 'out' for now with unit changes
                return NotImplemented
            
            result_value = ufunc(val1, val2, **kwargs)

            # Determine result unit
            if unit1 is not None and unit2 is not None: # quantity / quantity
                result_unit = unit1 / unit2
            elif unit1 is not None and unit2 is None: # quantity / scalar_or_array
                result_unit = unit1
            elif unit1 is None and unit2 is not None: # scalar_or_array / quantity
                result_unit = 1 / unit2
            else: # scalar_or_array / scalar_or_array (should not happen via PhysicalQuantity)
                 return NotImplemented

            # Return result
            # Add assertion to check type before accessing property
            assert isphysicalunit(result_unit), f"result_unit should be PhysicalUnit, got {type(result_unit)}"
            if result_unit.is_dimensionless:
                return result_value * result_unit.factor
            else:
                return self.__class__(result_value, result_unit)

        # Add / Subtract (requires compatible units)
        elif ufunc in (np.add, np.subtract):
             if len(processed_inputs) != 2:
                return NotImplemented
             val1, val2 = processed_inputs
             unit1, unit2 = input_units

             if unit1 is None or unit2 is None:
                 # Cannot add/subtract scalar and quantity directly via ufunc
                 return NotImplemented
            
             # Ensure units are compatible
             if unit1.powers != unit2.powers:
                  raise UnitError(f"Cannot {ufunc.__name__} quantities with incompatible units: {unit1} and {unit2}")

             # Convert second value to units of the first
             val2_converted = val2 * unit2.conversion_factor_to(unit1)
             result_value = ufunc(val1, val2_converted, **kwargs)
             # Result is in the unit of the first operand
             return self.__class__(result_value, unit1)

        # Multiply
        elif ufunc is np.multiply:
            if len(processed_inputs) != 2:
                return NotImplemented
            val1, val2 = processed_inputs
            unit1, unit2 = input_units

            result_value = ufunc(val1, val2, **kwargs)

            # Determine result unit
            if unit1 is not None and unit2 is not None: # quantity * quantity
                result_unit = unit1 * unit2
            elif unit1 is not None and unit2 is None: # quantity * scalar_or_array
                result_unit = unit1
            elif unit1 is None and unit2 is not None: # scalar_or_array * quantity
                result_unit = unit2
            else: # scalar_or_array * scalar_or_array
                 return NotImplemented

            # Return result
            if result_unit.is_dimensionless:
                return result_value * result_unit.factor
            else:
                return self.__class__(result_value, result_unit)

        # Trig functions (sin, cos, tan)
        elif ufunc in (np.sin, np.cos, np.tan):
            if len(processed_inputs) != 1:
                 return NotImplemented # Requires 1 argument
            val = processed_inputs[0]
            unit = input_units[0]

            if unit is None:
                 # Applying trig func to scalar/array without unit
                 return NotImplemented # Or should we allow np.sin(5)? Let NumPy handle.
            
            if not unit.is_angle:
                 raise UnitError(f"Argument of {ufunc.__name__} must be an angle, not {unit}")

            # Convert to radians
            value_rad = val * unit.conversion_factor_to(unit_table['rad'])
            # Apply ufunc to value in radians
            result_value = ufunc(value_rad, **kwargs)
            # Result is dimensionless scalar/array
            return result_value

        # --- Default: Ufunc not handled ---
        return NotImplemented
