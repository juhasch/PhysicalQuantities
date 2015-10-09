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
from PhysicalQuantities import PhysicalQuantity, PhysicalUnit, unit_table

__all__ = ['dB', 'dB10', 'dB20', 'dBQuantity', 'dB_units']


_m2unit = PhysicalQuantity(1,'m**2').unit

# list of tuples: (base unit, correction factor to linear unit, conversion factor to linear)
dB_units = {'dB' : (None, 0, 0),
            'dBm':  (unit_table['mW'], 0, 10),  # Power in Watt
            'dBW':  (unit_table['W'], 0, 10),
            'dBnV': (unit_table['nV'], 0, 20),  # Voltage
            'dBuV': (unit_table['uV'], 0, 20),
            'dBmV': (unit_table['mV'], 0, 20),
            'dBV':  (unit_table['V'], 0, 20),
            'dBnA': (unit_table['nA'], 0, 20),  # Ampere
            'dBuA': (unit_table['uA'], 20, 20),
            'dBmA': (unit_table['mA'], 0, 20),
            'dBA':  (unit_table['A'], 0, 20),
            'dBsm': (_m2unit, 0, 10),  # dB square meters
            'dBi':  (None, 0, 10),       # Antenna gain
            'dBd':  (None, 2.15, 10)}    # Antenna gain


def dB(x):
    """ Conversion from a PhysicalQuantity to correct dB<x> value

    :param x: convert a linear physical quanitiy into a dB quantitiy
    :type x: PhysicalQuantity
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
        for key in dB_units:
            if dB_units[key][0] is not None and dB_units[key][0].name == x.unit.baseunit.name:
                dbbase = key
                value = x.base.value
        for key in dB_units:
            if dB_units[key][0] is not None and dB_units[key][0].name == x.unit.name:
                dbbase = key
                value = x.value
        if dbbase is None:
            raise UnitError('Cannot handle unit %s' % x.unit)
        try:
            factor = dB_units[dbbase][2]
            dbvalue = factor * np.log10(value)
        except:
            raise UnitError('Cannot handle unit %s' % x.unit)
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
    return dBQuantity(10*np.log10(val),'dB',islog=True, factor=10)


def dB20(x):
    """ Convert linear value to 20*log10() dB value

    :param x: linear value
    :return: 20*log10(x)
    """
    if isinstance(x, PhysicalQuantity):
        val = x.base.value
    else:
        val = x
    return dBQuantity(20*np.log10(val),'dB',islog=True, factor=20)


def isdbquantity(q):
    """ Test if quantity is a dBQuantity class

    :param q: test quantity
    :return: True if dBQuantity class
    """
    return isinstance( q, dBQuantity)


class UnitError(ValueError):
    pass


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
        self.factor = 0
        islog = True

        try:
            self.sourceunit = dB_units[unit][0]
            self.factor = dB_units[unit][2]
        except KeyError:
            self.sourceunit = None
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
        if dB_units[unit]:
            self.unit = unit
            if islog is True:
                self.value = value
            else:
                self.value = dB_units[self.unit][2] * np.log10(value) - dB_units[self.unit][1]
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
                for key in dB_units:
                    unit = dB_units[key][0]
                    if isinstance(unit, PhysicalUnit):
                        if unit.baseunit is base:
                            x.append(key)
        return filter(None,[str(_x) for _x in x])
    
    def __getattr__(self,attr):
        """ Convert to different scaling in the same unit.
            If a '_' is appended, drop unit after rescaling and return value only.
        """
        dropunit = (attr[-1] == '_')
        unit = attr.strip('_')

        isdbunit = unit in dB_units.keys()

        if not isdbunit:
            if dropunit is False:
                return self.lin.to(unit)
            else:
                return self.lin.to(unit).value
        
        # convert to different scaling
        if self.unit is unit:
            return self
        elif unit in dB_units.keys():
            # convert to same base unit, only scaling
            scaling = self.factor * np.log10( dB_units[self.unit][0].factor / dB_units[unit][0].factor)
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
        raise TypeError

    def to(self, unit):
        """ Convert to differently scaled dB unit
        :param unit:
        :return:
        """
        if unit in dB_units.keys():
            # convert to same base unit, only scaling
            scaling = self.factor * np.log10( dB_units[self.unit][0].factor / dB_units[unit][0].factor)
            value = self.value + scaling
            return self.__class__(value, unit, islog=True)

    def copy(self):
        """Return a copy of the PhysicalQuantity including the value.
        Needs deepcopy to copy the value
        """
        return copy.deepcopy(self)

    def __getitem__(self, key):
        """ Allow indexing if quantities if underlying object is array or list
            e.g. obj[0] or obj[0:4]
        """
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            return self.__class__(self.value[key], self.unit)
        raise AttributeError        

    def __setitem__(self, key, value):
        """ Set quantities if underlying object is array or list

            >>> obj = np.linspace(0,10,10) * 1 dBm
            >>> obj[0] = 0 dBm
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
        linunit = dB_units[self.unit][0]
        if isinstance(linunit, PhysicalUnit):
            return PhysicalQuantity(self.__float__(),linunit.name)
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
        elif dB_units[self.unit][0] is dB_units[other.unit][0]:
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
        elif dB_units[self.unit][0] is dB_units[other.unit][0]:
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
        dbw = self.value + dB_units[self.unit][1]
        return 10**(dbw/(dB_units[self.unit][2]))

    def __str__(self):
        if self.ptformatter is not None and self.format is '' and isinstance(self.value,float):
            # %precision magic only works for floats
            format = self.ptformatter.float_format
            return "%s %s" % (format%self.value, str(self.unit))
        return '{0:{format}} {1}'.format(self.value, str(self.unit),format=self.format)

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        if isdbquantity(other):
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
        if isdbquantity(other):
            if self.unit is other.unit:
                return self.value >= other.value
            elif self.lin.base.unit is other.linbase.unit:
                return self.lin.base.value >= other.lin.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __lt__(self, other):
        if isdbquantity(other):
            if self.unit == other.unit:
                return self.value < other.value
            elif self.lin.base.unit is other.linbase.unit:
                return self.lin.base.value < other.lin.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __le__(self, other):
        if isdbquantity(other):
            if self.unit <= other.unit:
                return self.value <= other.value
            elif self.lin.base.unit is other.linbase.unit:
                return self.lin.base.value <= other.lin.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __eq__(self, other):
        if isdbquantity(other):
            if self.unit == other.unit:
                return self.value == other.value
            elif self.lin.base.unit is other.linbase.unit:
                return self.lin.base.value == other.lin.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __ne__(self, other):
        if isdbquantity(other):
            if self.unit == other.unit:
                return self.value != other.value
            elif self.lin.base.unit is other.linbase.unit:
                return self.lin.base.value != other.lin.base.value
            else:
                raise UnitError('Cannot compare unit %s with unit %s' % (self.unit, other.unit))
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))
