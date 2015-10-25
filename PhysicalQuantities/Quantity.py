# -*- coding: utf-8 -*-
""" PhysicalQuantity class definition

    Original author: Georg Brandl <georg@python.org>.
    https://bitbucket.org/birkenfeld/ipython-physics
"""

from __future__ import division

try:
    from sympy import printing
except ImportError:
    pass

from .Unit import *
import copy
from IPython import get_ipython

__all__ = ['PhysicalQuantity']


class PhysicalQuantity:
    """ Physical quantity with units.

        PhysicalQuantity instances allow addition, subtraction, multiplication, and
        division with each other as well as multiplication, division, and
        exponentiation with numbers.  Addition and subtraction check that the units
        of the two operands are compatible and return the result in the units of the
        first operand. A limited set of mathematical functions (from numpy) is
        applicable as well.
    """

    __array_priority__ = 1000  # make sure numpy arrays do not get iterated

    def __init__(self, value, unit=None,  **kwargs):
        """There are two constructor calling patterns

        :param value: value
        :type value: any
        :param unit: unit
        :type unit: string or PhysicalUnit class

        >>> PhysicalQuantity(1, 'V')
        """
        ip = get_ipython()
        if ip is not None:
            self.ptformatter = ip.display_formatter.formatters['text/plain']
        else:
            self.ptformatter = None
        self.format = ''  # display format for number to string conversion
        self.value = value
        self.unit = findunit(unit)

    def __dir__(self):
        """ List attributes

        :return: list of units for tab completion
        """
        ulist = super().__dir__()
        u = unit_table.values()
        for _u in u:
            if isphysicalunit(_u):
                if str(_u.baseunit) is str(self.unit.baseunit):
                    ulist.append(_u.name)
        return ulist
    
    def __getattr__(self, attr):
        """ Convert to different scaling in the same unit.
            If a '_' is appended, drop unit after rescaling and return value only.

            :param: attribute
            :raises AttributeError: If unit is not a valid attribute
        """
        dropunit = (attr[-1] is '_')
        attr = attr.strip('_')
        try:
            attrunit = unit_table[attr]
        except:
            raise AttributeError('Unit %s not found' % attr)
        if isphysicalunit(attrunit):
            if dropunit is True:
                return self.to(attrunit.name).value
            else:
                return self.to(attrunit.name)
        raise AttributeError('Unknown attribute %s' % attr)
        
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
            self.value[key] = value.to(self.unit).value
            return self.__class__(self.value[key], self.unit)
        raise AttributeError('Not a PhysicalQuantity array or list', list)
        
    def __len__(self):
        """ Return length of quantity if underlying object is array or list
            e.g. len(obj)
        """
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            return len(self.value)
        raise TypeError

    def rint(self):
        """ Round elements to the nearest integer

        :return: rounded elements
        """
        value = np.rint(self.value)
        return self.__class__(value, self.unit)

    def __str__(self):
        """ Return string representation as 'value unit'
            e.g. str(obj)
        """
        if self.ptformatter is not None and self.format is '' and isinstance(self.value, float):
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

    #def __array__(self):
        #""" Return array with units converted to base units
        #"""
        #return np.array(self.base.value)

    def __repr__(self):
        """ Return string representation
        """
        return self.__str__()

    def _repr_markdown_(self):
        """ Return markdown representation for IPython notebook
        """
        if self.ptformatter is not None and self.format is '' and isinstance(self.value, float):
            # %precision magic only works for floats
            fmt = self.ptformatter.float_format
            return u"%s %s" % (fmt % self.value, self.unit._repr_markdown_())
        if str(type(self.value)).find('sympy') > 0:
            # sympy
            return '${0}$ {1}'.format(printing.latex(self.value), self.unit.markdown)
        return '{0:{format}} {1}'.format(self.value, self.unit.markdown,format=self.format)

    def _repr_latex_(self):
        """ Return latex representation for IPython notebook
        """
        return self._repr_markdown_()

    def _sum(self, other, sign1, sign2):
        """ Add two quantities

        :param other: quantity to add
        :type other: PhysicalQuantity
        :param sign1: factor +1 or -1 with sign for self
        :type sign1: float
        :param sign2: factor +1 or -1 with sign for other
        :type sign2: float
        :return: sum of the two quantities
        :rtype: PhysicalQuantity
        """
        if not isinstance(other, PhysicalQuantity):
            raise UnitError('Incompatible types %s' % type(other))
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
        """ self // other
        :param other:
        :return:
        """
        if not isinstance(other, PhysicalQuantity):
            return self.__class__(self.value / other, self.unit)
        value = self.value // other.value
        unit = self.unit / other.unit
        if unit.is_dimensionless:
            return value * unit.factor
        else:
            return self.__class__(value, unit)

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

        :param ndigits: number of digits to round to
        :type ndigits:  int
        :return: rounded quantity
        :rtype: PhysicalQuantity
        """
        if isinstance(self.value, np.ndarray):
            return self.__class__(np.round(self.value, ndigits), self.unit)
        else:
            return self.__class__(round(self.value, ndigits), self.unit)

    def __pow__(self, other):
        """ Return power of other for quantity

        :param other: exponent
        :return: power of other for quantity
        :rtype: PhysicalQuantity
        """
        if isinstance(other, PhysicalQuantity):
            raise UnitError('Exponents must be dimensionless not of unit %s' % other.unit)
        return self.__class__(pow(self.value, other), pow(self.unit, other))

    def __rpow__(self, other):
        raise UnitError('Exponents must be dimensionless not of unit %s' % other.unit)

    def __abs__(self):
        """ Return quantity with absolute value

        :return: absolute value of quantity
        :rtype: PhysicalQuantity
        """
        return self.__class__(abs(self.value), self.unit)

    def __pos__(self):
        """ Return quantity with positive sign

        :return: positive value of quantity
        :rtype: PhysicalQuantity
        """
        if isinstance(self.value, np.array):
            return self.__class__(np.ndarray.__pos__(self.value), self.unit)
        return self.__class__(self.value, self.unit)

    def __neg__(self):
        """ Return quantity with negative sign

        :return: negative value of quantity
        :rtype: PhysicalQuantity
        """
        if isinstance(self.value, np.ndarray):
            return self.__class__(np.ndarray.__neg__(self.value), self.unit)
        return self.__class__(-self.value, self.unit)

    def __nonzero__(self):
        """ Test if quantity is not zero

            :return: true if quantity is not zero
            :rtype: bool
        """
        if isinstance(self.value, np.array):
            return self.__class__(np.ndarray.__neg__(self.value), self.unit)
        return self.value != 0

    def __gt__(self, other):
        """ Test if quantity is greater than other

            :param other: other PhysicalQuantity
            :return: true if quantity is greater than other
            :rtype: bool
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value > other.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare PhysicalQuantity with type %s' % type(other))

    def __ge__(self, other):
        """ Test if quantity is greater or equal than other

        :param other: other PhysicalQuantity
        :return: true if quantity is greater or equal than other
        :rtype: bool
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value >= other.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare PhysicalQuantity with type %s' % type(other))

    def __lt__(self, other):
        """ Test if quantity is less than other

            :param other: other PhysicalQuantity
            :return: true if quantity is less than other
            :rtype: bool
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value < other.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare PhysicalQuantity with type %s' % type(other))

    def __le__(self, other):
        """ Test if quantity is less or equal than other

            :param other: other PhysicalQuantity
            :return: true if quantity is less or equal than other
            :rtype: bool
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return self.base.value <= other.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare PhysicalQuantity with type %s' % type(other))

    def __eq__(self, other):
        """ Test if two quantities are equal

            :param other: quantity to test with
            :return: true if quantities are equal
            :rtype: bool
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit.name == other.base.unit.name:
                return self.base.value == other.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare PhysicalQuantity with type %s' % type(other))

    def __ne__(self, other):
        """ Test if two quantities are not equal

            :param other: quantity to test with
            :return: true if quantities are not equal
            :rtype: bool
        """
        if isinstance(other, PhysicalQuantity):
            if self.base.unit == other.base.unit:
                return not self.base.value == other.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare PhysicalQuantity with type %s' % type(other))

    def __format__(self, *args, **kw):
        return "{1:{0}} {2}".format(args[0], self.value, self.unit)

    def convert(self, unit):
        """ Change the unit and adjust the value such that the combination is
            equivalent to the original one. The new unit must be compatible with the
            previous unit of the object.

            :param unit: Unit to convert to
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

    def copy(self):
        """ Return a copy of the PhysicalQuantity including the value.
            Needs deepcopy to copy the value
        """
        return copy.deepcopy(self)

    @property
    def autoscale(self):
        """ Autoscale to a reasonable unit, if possible

        >>> b = PhysicalQuantity(4e-9, 'F')
        >>> b.autoscale
        4 nF
        """
        if len(self.unit.names) is 1:
            b = self.base
            n = np.log10(b.value)
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
        """ Express the quantity in different units. If one unit is specified, a
            new PhysicalQuantity object is returned that expresses the quantity in
            that unit. If several units are specified, the return value is a tuple
            of PhysicalObject instances with with one element per unit such that the
            sum of all quantities in the tuple equals the the original quantity and
            all the values except for the last one are integers. This is used to
            convert to irregular unit systems like hour/minute/second.

            >>> b = PhysicalQuantity(4, 'J/s')
            >>> b.to('W')
        """
        units = list(map(findunit, units))
        if len(units) is 1:
            unit = units[0]
            value = convertvalue(self.value, self.unit, unit)
            return self.__class__(value, unit)
        else:
            units.sort()
            result = []
            value = self.value
            unit = self.unit
            for i in range(len(units)-1, -1, -1):
                value = value*unit.conversion_factor_to(units[i])
                if i is 0:
                    rounded = value
                else:
                    rounded = self._round(value)
                result.append(self.__class__(rounded, units[i]))
                value = value - rounded
                unit = units[i]
            return tuple(result)

    @property
    def base(self):
        """ Returns the same quantity converted to SI base units

        :return: value in base unit

        >>> a = PhysicalQuantity(1, 'V')
        >>> a.base
        1.0 m^2*kg/s^3
        """
        new_value = self.value * self.unit.factor
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
        if len(num) is 0:
            num = '1'
        else:
            num = num[1:]
        return self.__class__(new_value, num + denom)

    # make it easier using complex numbers
    @property
    def real(self):
        """ Return real part of a complex PhysicalQuantity
        :return: real part
        :rtype: PhysicalQuantity

        >>> b = PhysicalQuantity(2 + 1j, 'V')
        >>> b.real
        2.0 V
        """
        return self.__class__(self.value.real, self.unit)

    @property
    def imag(self):
        """ Return imaginary part of a complex PhysicalQuantity

        :return: imaginary part
        :rtype: PhysicalQuantity

        >>> b = PhysicalQuantity(2 + 1j, 'V')
        >>> b.imag
        1.0 V
        """
        return self.__class__(self.value.imag, self.unit)

    def sqrt(self):
        """ Return the positive square-root

        :return: positive square-root
        :rtype: PhysicalQuantity
        """
        return self.__pow__(0.5)

    def pow(self, exponent):
        """ Return PhysicalQuantity raised to power of exponent

        :param exponent: power to be raised
        :type exponent: real number
        :return:
        :rtype: PhysicalQuantity
        """
        return self.__pow__(exponent)

    def sin(self):
        """ Return sine of given PhysicalQuantity with angle unit

        :return: sine values
        """
        if self.unit.is_angle:
            return np.sin(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        else:
            raise UnitError('Argument of sin must be an angle')

    def cos(self):
        """ Return cosine of given PhysicalQuantity with angle unit

        :return: cosine values
        """
        if self.unit.is_angle:
            return np.cos(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        else:
            raise UnitError('Argument of cos must be an angle')

    def tan(self):
        """ Return tangens of given PhysicalQuantity with angle unit

        :return: tangens values
        """
        if self.unit.is_angle:
            return np.tan(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        else:
            raise UnitError('Argument of tan must be an angle')
