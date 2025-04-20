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
    """ Physical quantity with units.

        PhysicalQuantity instances allow addition, subtraction, multiplication, and
        division with each other as well as multiplication, division, and
        exponentiation with numbers.  Addition and subtraction check that the units
        of the two operands are compatible and return the result in the units of the
        first operand. A limited set of mathematical functions (from numpy) is
        applicable as well.
    """

    __array_priority__: int = 1000  # make sure numpy arrays do not get iterated
    format: str = ''                # display format for number to string conversion
    annotation: str = ''            # optional annotation of Quantity
    value: int | float | complex    # value of the quantity
    unit: PhysicalUnit

    def __init__(self, value: int | float | complex, unit: str | PhysicalUnit, annotation: str = ''):
        """There are two constructor calling patterns

        Parameters
        ----------
        value: any
            value of the quantity
        
        unit: string or PhysicalUnit class
            unit of the quantity

        Examples
        --------
        >>> from PhysicalQuantities import PhysicalQuantity
        >>> PhysicalQuantity(1, 'V')
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
        """List available attributes including conversion to other scaling prefixes

        Returns
        -------
        list of units for tab completion
        """
        ulist = list(super().__dir__())
        u = unit_table.values()
        for _u in u:
            if isphysicalunit(_u):
                if str(_u.baseunit) is str(self.unit.baseunit):
                    ulist.append(_u.name)
        return ulist
    
    def __getattr__(self, attr) -> int | float | complex | PhysicalQuantity:
        """ Convert to different scaling in the same unit.
            If a '_' is appended, drop unit (possibly after rescaling) and return value only.

        Parameters
        ----------
        attr : string
            attribute name
            
        Raises
        ------
        AttributeError
            If unit is not a valid attribute

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
        """ Allow indexing if quantities if underlying object is array or list
            e.g. obj[0] or obj[0:4]

        """
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            return self.__class__(self.value[key], self.unit)
        raise AttributeError('Not a PhysicalQuantity array or list', list)

    def __setitem__(self, key, value):
        """ Set quantities if underlying object is array or list
            e.g. obj[0] = 1m

        """
        if not isinstance(value, PhysicalQuantity):
            raise AttributeError('Not a Physical Quantity')
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            self.value[key] = value.to(str(self.unit)).value
            return self.__class__(self.value[key], self.unit)
        raise AttributeError('Not a PhysicalQuantity array or list', list)
        
    def __len__(self):
        """ Return length of quantity if underlying object is array or list
            e.g. len(obj)
        """
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            return len(self.value)
        raise TypeError('Object of type %s has no len()' % type(self.value))

    def _ipython_key_completions_(self):
        return self.unit_table.keys()

    @property
    def dB(self) -> dBQuantity:
        """ Convert to dB scaled unit, if possible. Guess if it is a power unit to select 10*log10 or 20*log10

        Returns
        -------
        dBQuantity
            dB quantity converted from PhysicalQuantity
        

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> (10 q.V).dB
        20.0 dBV
        >>> (10 q.W).dB
        10.0 dBW
        """
        from .dBQuantity import PhysicalQuantity_to_dBQuantity
        return PhysicalQuantity_to_dBQuantity(self)

    def rint(self):
        """ Round elements to the nearest integer

        Returns
        -------
        any
            rounded elements
        """
        value = np.rint(self.value)
        return self.__class__(value, self.unit)

    def __str__(self):
        """ Return string representation as 'value unit'
            e.g. str(obj)
            
        Returns
        -------
        string
            string representation of PhysicalQuantity            
        """
        if self.ptformatter is not None and self.format == '' and isinstance(self.value, float):  # pragma: no cover
            # %precision magic only works for floats
            fmt = self.ptformatter.float_format
            return u"%s %s" % (fmt % self.value, str(self.unit))
        return '{0:{format}} {1}'.format(self.value, str(self.unit), format=self.format)

    def __complex__(self):
        """ Return complex number without units converted to base units 
        """
        return self.base.value

    def __float__(self):
        """ Return float number without units converted to base units 
        """
        return self.base.value

    def __repr__(self):
        """ Return string representation
        """
        return self.__str__()

    def _repr_markdown_(self):
        """ Return markdown representation for IPython notebook
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
        """ Return latex representation for IPython notebook
        """
        return self._repr_markdown_()

    def _sum(self, other, sign1, sign2):
        """ Add two quantities

        Parameters
        ----------
        other: PhysicalQuantity
            Quantity to add
        
        sign1: float
            factor +1 or -1 with sign for self

        sign2: float
            factor +1 or -1 with sign for other


        Returns
        -------
        PhysicalQuantity
            sum of the two quantities
        """
        if not isinstance(other, PhysicalQuantity):
            raise UnitError(f'Incompatible types {type(self)} and {type(other)}')
        new_value = sign1 * self.value + \
            sign2 * other.value * other.unit.conversion_factor_to(self.unit)
        return self.__class__(new_value, self.unit)

    def __add__(self, other):
        return self._sum(other, 1, 1)

    __radd__ = __add__

    def __sub__(self, other):
        return self._sum(other, 1, -1)

    def __rsub__(self, other):
        return self._sum(other, -1, 1)

    def __mul__(self, other):
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
        """ Implement integer division: self // other
        
        Parameters
        ----------
        other: PhysicalQuantity
            Quantity to divide by
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
        """ Implement integer division: other // self
        
        Parameters
        ----------
        other
        """
        return self.__class__(other // self.value, self.unit)
            
    def __div__(self, other):
        if not isinstance(other, PhysicalQuantity):
            return self.__class__(self.value / other, self.unit)
        value = self.value / other.value
        unit = self.unit / other.unit
        if unit.is_dimensionless:
            return value * unit.factor
        else:
            return self.__class__(value, unit)

    def __rdiv__(self, other):
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
        """ Return rounded values
        
        Parameters
        ----------
        ndigits: int
            number of digits to round to
        
        Returns
        -------
        PhysicalQuantity
            rounded quantity
        """
        if isinstance(self.value, np.ndarray):
            return self.__class__(np.round(self.value, ndigits), self.unit)
        else:
            return self.__class__(round(self.value, ndigits), self.unit)

    def __pow__(self, other):
        """ Return power of other for quantity

        Parameters
        ----------
        other
            exponent

        Returns
        -------
        PhysicalQuantity
            power of other for quantity
        """
        if isinstance(other, PhysicalQuantity):
            raise UnitError('Exponents must be dimensionless not of unit %s' % other.unit)
        return self.__class__(pow(self.value, other), pow(self.unit, other))

    def __rpow__(self, other):
        raise UnitError('Exponents must be dimensionless, not of unit %s' % self.unit)

    def __abs__(self):
        """ Return quantity with absolute value

        Returns
        -------
        PhysicalQuantity
            Absolute value of quantity
        """
        return self.__class__(abs(self.value), self.unit)

    def __pos__(self):
        """ Return quantity with positive sign

        Returns
        -------
        PhysicalQuantity
            positive value of quantity
        """
        if isinstance(self.value, np.ndarray):
            return self.__class__(np.ndarray.__pos__(self.value), self.unit)
        return self.__class__(self.value, self.unit)

    def __neg__(self):
        """ Return quantity with negative sign

        Returns
        -------
        PhysicalQuantity
            negative value of quantity
        """
        if isinstance(self.value, np.ndarray):
            return self.__class__(np.ndarray.__neg__(self.value), self.unit)
        return self.__class__(-self.value, self.unit)

    def __nonzero__(self):
        """ Test if quantity is not zero

        Returns
        -------
        bool
            true if quantity is not zero
        """
        if isinstance(self.value, np.ndarray):
            return self.__class__(np.nonzero(self.value), self.unit)
        return self.value != 0

    def __gt__(self, other):
        """ Test if quantity is greater than other

        Parameters
        ----------
        other: PhysicalQuantity
        

        Returns
        -------
        bool
            true if quantity is greater than other
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value > other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __ge__(self, other):
        """ Test if quantity is greater or equal than other

        Parameters
        ----------
        other: PhysicalQuantity
            Quantity to compare against

        Returns
        -------
        bool
            True if quantity is greater or equal than other
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value >= other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __lt__(self, other):
        """ Test if quantity is less than other

        Parameters
        ----------
        other: PhysicalQuantity
            Quantity to compare against

        Returns
        -------
        bool
            True if quantity is less than other
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value < other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __le__(self, other):
        """ Test if quantity is less or equal than other

        Parameters
        ----------
        other: PhysicalQuantity
            Quantity to compare against

        Returns
        -------
        bool
            :param other: other PhysicalQuantity
            :return: true if quantity is less or equal than other
            :rtype: bool
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value <= other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __eq__(self, other):
        """ Test if two quantities are equal

        Parameters
        ----------
        other: PhysicalQuantity
            Quantity to compare against

        Returns
        -------
        bool
            True if quantities are equal
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit.name == other.base.unit.name:
                return self.base.value == other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __ne__(self, other):
        """Test if two quantities are not equal

        Parameters
        ----------
        other: PhysicalQuantity
            Quantity to compare against

        Returns
        -------
        bool
            True if quantities are not equal
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return not self.base.value == other.base.value
            else:
                raise UnitError(f'Cannot compare unit {self.unit} with unit {other.unit}')
        else:
            raise UnitError(f'Cannot compare PhysicalQuantity with type {type(other)}')

    def __format__(self, *args, **kw):
        return "{1:{0}} {2}".format(args[0], self.value, self.unit)

    def convert(self, unit):
        """ Change the unit and adjust the value such that the combination is
            equivalent to the original one. The new unit must be compatible with the
            previous unit of the object.

        Parameters
        ----------
        unit: PhysicalUnit
            Unit to convert to
        """
        unit = findunit(unit)
        self.value = convertvalue(self.value, self.unit, unit)
        self.unit = unit

    @staticmethod
    def _round(x):
        if np.greater(x, 0.):
            return np.floor(x)
        else:
            return np.ceil(x)

    def __deepcopy__(self, memo: dict) -> PhysicalQuantity:
        """ Return a copy of the PhysicalQuantity including the value.
            Needs deepcopy to copy the value
        """
        new_value = copy.deepcopy(self.value)
        new_instance = self.__class__(new_value, self.unit)
        memo[id(self)] = new_instance
        return new_instance

    @property
    def autoscale(self) -> PhysicalQuantity:
        """ Autoscale to a reasonable unit, if possible

        Examples
        --------
        >>> b = PhysicalQuantity(4e-9, 'F')
        >>> b.autoscale
        4 nF
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
        """ Express the quantity in different units.

        Parameters
        ----------
        units: str
            Name of the unit

        Examples
        --------
            >>> b = PhysicalQuantity(4, 'J/s')
            >>> b.to('W')
            4.0 W
            >>> b = PhysicalQuantity(1000, 's')
            >>> b.to('h', 'min, ''s')
            (0.0 h, 16.0 min, 40.000000000000071 s)

        Notes
        -----
            If one unit is specified, a new PhysicalQuantity object is returned that expresses the quantity in
            that unit. If several units are specified, the return value is a tuple of PhysicalObject instances with
            one element per unit such that the sum of all quantities in the tuple equals the original quantity and
            all the values except for the last one are integers. This is used to convert to irregular unit systems like
            hour/minute/second.
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
        """ Returns the same quantity converted to SI base units

        Returns
        -------
        any
            values in base unit

        >>> a = PhysicalQuantity(1, 'V')
        >>> a.base
        1.0 m^2*kg/s^3/A
        >>> from PhysicalQuantities import q # Import q for other examples
        >>> q.PhysicalQuantity(0, 'degC').base # 0 degC should be 273.15 K
        273.15 K
        >>> q.PhysicalQuantity(0, 'degF').base # 0 degF should be 255.37... K
        255.37222222222223 K
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

    # make it easier using complex numbers
    @property
    def real(self) -> PhysicalQuantity:
        """ Return real part of a complex PhysicalQuantity

        Returns
        -------
        PhysicalQuantity
            real part

        Examples
        --------
        >>> b = PhysicalQuantity(2 + 1j, 'V')
        >>> b.real
        2.0 V
        """
        return self.__class__(self.value.real, self.unit)

    @property
    def imag(self) -> PhysicalQuantity:
        """ Return imaginary part of a complex PhysicalQuantity

        Returns
        -------
        PhysicalQuantity
            imaginary part

        Examples
        --------
        >>> b = PhysicalQuantity(2 + 1j, 'V')
        >>> b.imag
        1.0 V
        """
        return self.__class__(self.value.imag, self.unit)

    def sqrt(self) -> PhysicalQuantity:
        """ Return the positive square-root

        Returns
        -------
        PhysicalQuantity
            Positive square-root
        """
        return self.__pow__(0.5)

    def pow(self, exponent: float) -> PhysicalQuantity:
        """ Return PhysicalQuantity raised to power of exponent

        Parameters
        ----------
        exponent: float
            Power to be raised

        Returns
        -------
        PhysicalQuantity
            Raised to power of exponent
        """
        return self.__pow__(exponent)

    def sin(self) -> float:
        """ Return sine of given PhysicalQuantity with angle unit

        Returns
        -------
            Sine values

        Raises
        ------
        UnitError
            If quantity is not of unit angle
        """
        if self.unit.is_angle:
            return np.sin(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        else:
            raise UnitError('Argument of sin must be an angle')

    def cos(self) -> float:
        """ Return cosine of given PhysicalQuantity with angle unit

        Returns
        -------
            Cosine values

        Raises
        ------
        UnitError
            If quantity is not of unit angle
        """
        if self.unit.is_angle:
            return np.cos(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        raise UnitError('Argument of cos must be an angle')

    def tan(self) -> float:
        """ Return tangens of given PhysicalQuantity with angle unit

        Returns
        -------
            Tangens values

        Raises
        ------
        UnitError
            If quantity is not of unit angle
        """
        if self.unit.is_angle:
            return np.tan(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        raise UnitError('Argument of tan must be an angle')

    @property
    def to_dict(self) -> dict:
        """Export as dict

        Returns
        -------
        dict
            Dict describing PhysicalQuantity
        """
        q_dict = {'value': self.value,
                  'PhysicalUnit': self.unit.to_dict
                  }
        return q_dict

    @property
    def to_json(self) -> str:
        """Export as JSON

        Returns
        -------
        str
            JSON string describing PhysicalQuantity

        """
        json_quantity = json.dumps({'PhysicalQuantity': self.to_dict})
        return json_quantity

    @staticmethod
    def from_dict(quantity_dict: dict) -> PhysicalQuantity:
        """Retrieve PhysicalUnit from dict description

        Parameters
        ----------
        quantity_dict
            PhysicalQuantity stored as dict

        Returns
        -------
        PhysicalQuantity
            Retrieved PhysicalQuantity

        Notes
        -----
        Current implementation: throw exception if unit has not already been defined
        """
        u = PhysicalUnit.from_dict(quantity_dict['PhysicalUnit'])
        q = PhysicalQuantity(quantity_dict['value'], u)
        return q

    @staticmethod
    def from_json(json_quantity: str) -> PhysicalQuantity:
        """Retrieve PhysicaQuantity from JSON string description

        Parameters
        ----------
        json_quantity
            PhysicalQuantity encoded as JSON string

        Returns
        -------
        PhysicalQuantity
            New PhysicalQuantity
        """
        quantity_dict = json.loads(json_quantity)
        return PhysicalQuantity.from_dict(quantity_dict['PhysicalQuantity'])
