# -*- coding: utf-8 -*-
""" Class for dB calculations 

Example:
    >>> from PhysicalQuantities.dBQuantity import dBQuantity
    >>> a = dBQuantity(1,'dBm')
    >>> print(a)
    1 dBm

"""

import numpy as np
import copy
from IPython import get_ipython
from . import PhysicalQuantity, unit_table, UnitError, PhysicalUnit

__all__ = ['dB10', 'dB20', 'dBQuantity', 'dB_unit_table']

dB_unit_table = {}


class dBUnit:
    def __init__(self, name, unit, offset=0):
        self.name = name
        self.unit = unit
        self.offset = offset
        dB_unit_table[name] = self

    @property
    def __name__(self):
        return self.name


def add_dB_units(name, unit, offset=0):
    dB_unit_table[name] = dBUnit(name, unit, offset)

add_dB_units('dB', None)
add_dB_units('dBm', unit_table['mW'])
add_dB_units('dBW', unit_table['W'])
add_dB_units('dBnV', unit_table['nV'])
add_dB_units('dBuV', unit_table['uV'])
add_dB_units('dBmV', unit_table['mV'])
add_dB_units('dBV', unit_table['V'])
add_dB_units('dBnA', unit_table['nA'])
add_dB_units('dBuA', unit_table['uA'])
add_dB_units('dBmA', unit_table['mA'])
add_dB_units('dBA', unit_table['A'])
add_dB_units('dBsm', PhysicalQuantity(1,'m**2').unit)
add_dB_units('dBi', None, offset=2.15)
add_dB_units('dBc', None)


def PhysicalQuantity_to_dBQuantity(x, dBunit):
    """ Conversion from a PhysicalQuantity to correct dB<x> value

    :param x: convert a linear physical quanitiy into a dB quantitiy
    :type x: PhysicalQuantity
    :param dBunit: desired unit of dB value (i.e. dBm or dBW for Watt)
    :return: converted dB quantity
    :rtype: dBQuantity
    """
    """
    :param x:
    :return:
    """
    if isinstance(x, PhysicalQuantity):
        dbbase = None
        value = None
        if dBunit is not None and dB_unit_table[dBunit] is not None:
            if dB_unit_table[dBunit].unit.baseunit.name == x.unit.baseunit.name:
                    dbbase = dBunit
                    value = x.to(dB_unit_table[dBunit].unit.name).value
                    _unit = dB_unit_table[dBunit].unit
        else:
            for key in dB_unit_table:
                if dB_unit_table[key].unit is not None and dB_unit_table[key].unit.name == x.unit.name:
                    dbbase = key
                    value = x.value
                    break
                elif dB_unit_table[key].unit is not None and dB_unit_table[key].unit.baseunit.name == x.unit.baseunit.name:
                    dbbase = key
                    value = x.base.value
            _unit = x.unit
        if dbbase is None:
            raise UnitError('Cannot handle unit %s' % x.unit)
        factor = 20 - 10 * _unit.is_power
        dbvalue = factor * np.log10(value)
        return dBQuantity(dbvalue, dbbase ,islog=True, factor=factor)
    raise UnitError('Cannot handle unitless quantity %s' % x)

def dB10(x):
    """ Convert linear value to 10*log10() dB value

    :param x: linear value
    :return: 10*log10(x)
    """
    if isinstance(x, PhysicalQuantity):
        val = x.base.value
    else:
        val = x
    return dBQuantity(10*np.log10(val), 'dB', islog=True, factor=10)


def dB20(x):
    """ Convert linear value to 20*log10() dB value

    :param x: linear value
    :return: 20*log10(x)
    """
    if isinstance(x, PhysicalQuantity):
        val = x.base.value
    else:
        val = x
    return dBQuantity(20*np.log10(val), 'dB', islog=True, factor=20)


class dBQuantity:
    """ dB scaled physical quantity with units.

        dBquantity instances allow addition, subtraction, comparison and conversion.
    """

    __array_priority__ = 1000  # make sure numpy arrays do not get iterated

    def __init__(self, value, unit, **kwargs):
        """ Initialize and convert to logarithm if islog=False

        :param value: value
        :param unit: unit
        """
        self.z0 = PhysicalQuantity(50, 'Ohm')
        islog = True

        try:
            self.sourceunit = dB_unit_table[unit].unit
        except KeyError:
            self.sourceunit = None

        if self.sourceunit is None:
            self.factor = 0
        else:
            self.factor = 20 - 10 * self.sourceunit.is_power
        ip = get_ipython()
        if ip is not None:
            self.ptformatter = ip.display_formatter.formatters['text/plain']
        else:
            self.ptformatter = None
        self.format = '' # display format for number to string conversion

        for key, val in list(kwargs.items()):
            if key is 'islog':
                islog = val    # convert to log at initialization
            if key is 'z0':
                self.z0 = val
            if key is 'factor':
                self.factor = val
        if dB_unit_table[unit]:
            self.unit = unit
            if islog is True:
                self.value = value
            else:
                self.value = self.factor * np.log10(value) - dB_unit_table[self.unit].offset
        else:
            raise UnitError('Unknown unit %s' % unit)

    def __dir__(self):
        """ return list for tab completion
            Include conversions to linear and ther dB units
        """
        x = super().__dir__()
        if self.sourceunit is not None:
            base = self.sourceunit.baseunit
            # add PhysicalUnits
            if isinstance(base, PhysicalUnit):
                for key in unit_table:
                    if unit_table[key].baseunit is base:
                        x.append(key)
                for key in dB_unit_table:
                    unit = dB_unit_table[key]
                    if isinstance(unit, PhysicalUnit):
                        if unit.baseunit is base:
                            x.append(key)
        return filter(None, [str(_x) for _x in x])
    
    def __getattr__(self, attr):
        """ Convert to different scaling in the same unit.
            If a '_' is appended, drop unit after rescaling and return value only.
        """
        dropunit = (attr[-1] == '_')
        unit = attr.strip('_')

        isdbunit = unit in dB_unit_table.keys()

        if not isdbunit:
            if dropunit is False:
                return self.lin.to(unit)
            else:
                return self.lin.to(unit).value
        
        # convert to different scaling
        if self.unit is unit:
            return self
        elif unit in dB_unit_table.keys():
            # convert to same base unit, only scaling
            scaling = self.factor * np.log10( dB_unit_table[self.unit].unit.factor / dB_unit_table[unit].unit.factor)
            value = self.value + scaling
            if dropunit is False:
                return self.__class__(value, unit, islog=True)
            else:
                return value
        else:
            raise UnitError('No conversion between units %s and %s' % (self.unit, unit))

    def __len__(self):
        """ Return length of quantity if underlying object is array or list
            e.g. len(obj)
        """
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            return len(self.value)
#        return 1
        raise TypeError('Not a list or array: %s', self)

    def to(self, unit):
        """ Convert to differently scaled dB units
        :param unit:
        :return:
        """
        if unit in dB_unit_table.keys():
            # convert to same base unit, only scaling
            scaling = self.factor * np.log10( dB_unit_table[self.unit].unit.factor / dB_unit_table[unit].unit.factor)
            value = self.value + scaling
            return self.__class__(value, unit, islog=True)

    def copy(self):
        """Return a copy of the dBQuantity including the value.
        Needs deepcopy to copy the value
        """
        return copy.deepcopy(self)

    def __getitem__(self, key):
        """ Allow indexing if quantities if underlying object is array or list
            e.g. obj[0] or obj[0:4]
        """
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            return self.__class__(self.value[key], self.unit)
        raise AttributeError('Not a list or array: %s' % self)        

    def __setitem__(self, key, value):
        """ Set quantities if underlying object is array or list

            >>> from PhysicalQuantities import q
            >>> obj = np.linspace(0,10,10) * 1 q.dBm
            >>> obj[0] = 0 q.dBm
        """
        if not isinstance(value, dBQuantity):
            raise AttributeError('Not a dBQuantity')
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            self.value[key] = value.to(self.unit).value
            return self.__class__(self.value[key], self.unit)
        raise AttributeError('Not a dBQuantity array or list')

    @property
    def dB(self):
        """ return dB value without unit """
        return dBQuantity(self.value, 'dB', islog=True)

    @property
    def lin(self):
        """
        :return: linear value or unit
        """
        if self.sourceunit is not None:
            return PhysicalQuantity(self.__float__(), self.sourceunit)
        if self.factor == 0:
            raise UnitError('Cannot convert dB unit with unknown factor to linear')
        val = self.value / self.factor

        return pow(10, val)

    def __add__(self, other):
        if (self.unit is 'dB') or (other.unit is 'dB'):
            # easy unitless adding
            value = self.value + other.value
            unit = other.unit if self.unit is 'dB' else self.unit
            return self.__class__(value, unit, islog=True)
        elif dB_unit_table[self.unit] is dB_unit_table[other.unit]:
            # same unit adding
            val1 = float(self)
            val2 = float(other)
            return self.__class__(val1+val2, self.unit, islog=False)
        else:
            raise UnitError('Cannot add unequal units %s and %s' % (self.unit, other.unit))

    __radd__ = __add__

    def __sub__(self, other):
        if self.unit is 'dB' or other.unit is 'dB':
            # easy unitless adding
            value = self.value - other.value
            return self.__class__(value, self.unit, islog=True)
        elif dB_unit_table[self.unit] is dB_unit_table[other.unit]:
            # same unit subtraction
            val1 = float(self)
            val2 = float(other)
            return self.__class__(val1-val2, self.unit, islog=False)
        else:
            raise UnitError('Cannot add unequal units %s and %s' % (self.unit, other.unit))

    __rsub__ = __sub__
    
    def __mul__(self, other):
        if  not hasattr(other,'unit'):
            # dB values will be multiplied with a factor to enable "a = 2 * q.dBm"
            value = self.value * other
            return self.__class__(value, self.unit, islog=True)

    __rmul__ = __mul__

    def __div__(self, other):
        if self.unit is 'dB' and not hasattr(other,'unit'):
            # dB without physical dimension can be divided by a factor
            value = self.value / other
            return self.__class__(value, self.unit, islog=True)

    __rdiv__ = __div__

    def __neg__(self):
        return self.__class__(-self.value, self.unit, islog=True)
    
    def __float__(self):
        # return linear value in base unit
        dbw = self.value + dB_unit_table[self.unit].offset
        return 10**(dbw/self.factor)

    def __str__(self):
        if self.ptformatter is not None and self.format is '' and isinstance(self.value,float):
            # %precision magic only works for floats
            format = self.ptformatter.float_format
            return "%s %s" % (format%self.value, str(self.unit))
        return '{0:{format}} {1}'.format(self.value, str(self.unit), format=self.format)

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        if isinstance(other, dBQuantity):
            # dB values without scaling
            if self.unit == other.unit:
                return self.value > other.value
            elif self.lin.base.unit is other.linbase.unit:
                return self.lin.base.value > other.lin.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __ge__(self, other):
        if isinstance(other, dBQuantity):
            if self.unit is other.unit:
                return self.value >= other.value
            elif self.lin.base.unit is other.linbase.unit:
                return self.lin.base.value >= other.lin.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __lt__(self, other):
        if isinstance(other, dBQuantity):
            if self.unit == other.unit:
                return self.value < other.value
            elif self.lin.base.unit is other.linbase.unit:
                return self.lin.base.value < other.lin.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __le__(self, other):
        if isinstance(other, dBQuantity):
            if self.unit <= other.unit:
                return self.value <= other.value
            elif self.lin.base.unit is other.linbase.unit:
                return self.lin.base.value <= other.lin.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __eq__(self, other):
        if isinstance(other, dBQuantity):
            if self.unit == other.unit:
                return self.value == other.value
            elif self.lin.base.unit is other.linbase.unit:
                return self.lin.base.value == other.lin.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __ne__(self, other):
        if isinstance(other, dBQuantity):
            if self.unit == other.unit:
                return self.value != other.value
            elif self.lin.base.unit is other.linbase.unit:
                return self.lin.base.value != other.lin.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))
