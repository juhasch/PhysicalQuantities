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


def isphysicalquantity(x):
    """
    :return: true if x is a PhysicalQuantity
    """
    return hasattr(x, 'value') and hasattr(x, 'unit')


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
        """There are two constructor calling patterns:
        :param value: numerical value
        :param unit: unit as string or PhysicalUnit class
        """
        ip = get_ipython()
        if ip is not None:
            self.ptformatter = ip.display_formatter.formatters['text/plain']
        else:
            self.ptformatter = None
        self.format = ''  # display format for number to string conversion
        if unit is not None:
            self.value = value
            self.unit = findunit(unit)
        else:
            raise UnitError('No unit given in %s' % unit)
            
    def __dir__(self):
        """
        :return: list of units for tab completion
        """
        ulist = []
        u = unit_table.values()
        for _u in u:
            if isphysicalunit(_u):
                if str(_u.baseunit) is str(self.unit.baseunit):
                    ulist.append(_u.name)
        ulist.append('value')
        ulist.append('unit')
        return ulist
    
    def __getattr__(self, attr):
        """ Convert to different scaling in the same unit.
            If a '_' is appended, drop unit after rescaling and return value only.
            :param:
            :return:
        """
        dropunit = (attr[-1] is '_')
        attr = attr.strip('_')
        try:
            attrunit = unit_table[attr]
        except:
            raise AttributeError
        if isphysicalunit(attrunit):
            if dropunit is True:
                return self.to(attrunit.name).value
            else:
                return self.to(attrunit.name)
        raise AttributeError
        
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

    def __array__(self):
        """ Return array without units converted to base units
        """
        return np.array(self.base.value)

    def __repr__(self):
        """ Simply return string representation
        """
        return self.__str__()

    def _repr_latex_(self):
        """ Return Latex representation for IPython notebook
        """
        if self.ptformatter is not None and self.format is '' and isinstance(self.value, float):
            # %precision magic only works for floats
            fmt = self.ptformatter.float_format
            return u"%s %s" % (fmt % self.value, self.unit._repr_latex_())
        if str(type(self.value)).find('sympy') > 0:
            # sympy
            return '${0}$ {1}'.format(printing.latex(self.value), self.unit.latex)
        return '{0:{format}} {1}'.format(self.value, self.unit.latex,format=self.format)

    def _sum(self, other, sign1, sign2):
        if not isphysicalquantity(other):
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
        if not isphysicalquantity(other):
            return self.__class__(self.value * other, self.unit)
        value = self.value * other.value
        unit = self.unit * other.unit
        if unit.is_dimensionless:
            return value * unit.factor
        else:
            return self.__class__(value, unit)

    __rmul__ = __mul__

    def __div__(self, other):
        if not isphysicalquantity(other):
            return self.__class__(self.value / other, self.unit)
        value = self.value / other.value
        unit = self.unit / other.unit
        if unit.is_dimensionless:
            return value * unit.factor
        else:
            return self.__class__(value, unit)

    def __rdiv__(self, other):
        if not isphysicalquantity(other):
            return self.__class__(other / self.value, pow(self.unit, -1))
        value = other.value / self.value
        unit = other.unit / self.unit
        if unit.is_dimensionless:
            return value * unit.factor
        else:
            return self.__class__(value, unit)

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __pow__(self, other):
        if isphysicalquantity(other):
            raise UnitError('Exponents must be dimensionless')
        return self.__class__(pow(self.value, other), pow(self.unit, other))

    def __rpow__(self, other):
        raise UnitError('Exponents must be dimensionless')

    def __abs__(self):
        return self.__class__(abs(self.value), self.unit)

    def __pos__(self):
        return self

    def __neg__(self):
        return self.__class__(-self.value, self.unit)

    def __nonzero__(self):
        return self.value != 0

    def __gt__(self, other):
        if isphysicalquantity(other):
            if self.base.unit is other.base.unit:
                return self.base.value > other.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare PhysicalQuantity with type %s' % type(other))

    def __ge__(self, other):
        if isphysicalquantity(other):
            if self.base.unit is other.base.unit:
                return self.base.value >= other.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare PhysicalQuantity with type %s' % type(other))

    def __lt__(self, other):
        print("less")
        if isphysicalquantity(other):
            if self.base.unit is other.base.unit:
                return self.base.value < other.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare PhysicalQuantity with type %s' % type(other))

    def __le__(self, other):
        if isphysicalquantity(other):
            if self.base.unit is other.base.unit:
                return self.base.value <= other.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare PhysicalQuantity with type %s' % type(other))

    def __eq__(self, other):
        if isphysicalquantity(other):
            if self.base.unit is other.base.unit:
                return self.base.value == other.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare PhysicalQuantity with type %s' % type(other))

    def __ne__(self, other):
        if isphysicalquantity(other):
            if self.base.unit is other.base.unit:
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
        """ autoscale if it has a simple unit """
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

    @staticmethod
    def any_to(qty, unit):
        if not isphysicalquantity(qty):
            qty = PhysicalQuantity(qty, 'rad')
        return qty.to(unit)

    @property
    def base(self):
        """ Returns the same quantity converted to base units."""
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
        return self.__class__(self.value.real, self.unit)

    @property
    def imag(self):
        return self.__class__(self.value.imag, self.unit)

    def sin(self):
        if self.unit.is_angle:
            return np.sin(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        else:
            raise UnitError('Argument of sin must be an angle')

    def cos(self):
        if self.unit.is_angle:
            return np.cos(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        else:
            raise UnitError('Argument of cos must be an angle')

    def tan(self):
        if self.unit.is_angle:
            return np.tan(self.value * self.unit.conversion_factor_to(unit_table['rad']))
        else:
            raise UnitError('Argument of tan must be an angle')
