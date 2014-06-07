# -*- coding: utf-8 -*-
""" Class for dB calculations 

Example:
    from PhysicalQuantities.dBunits import dBUnit
    a = dBUnit(0.1,'dBm', islog=True)
    print(a)

"""

# TODO:
# Conversion from a PhysicalQuantity to correct dB<x> value

def dB(x):
    """ Convert value to 10*log10 """
    return dBUnit(10*np.log10(x),'dB',islog=True)

import numpy as np
import copy

import re
import PhysicalQuantities as pq

# list of tuples: (base unit, correction factor to base unit, conversion factor to linear)
dB_units = {'dB':  ('', 0, 10),
            'dBm':  ('W', -30, 10),  # Power in Watt
            'dBW':  ('W', 0, 10),
            'dBnV': ('V', -90, 20),  # Voltage
            'dBuV': ('V', -60, 20),
            'dBmV': ('V', -30, 20),
            'dBV':  ('V', 0, 20),
            'dBnA': ('A', -90, 20),  # Ampere
            'dBuA': ('A', -60, 20),
            'dBmA': ('A', -30, 20),
            'dBA':  ('A', 0, 20),
            'dBi':  ('', 0, 10),    # Antenna gain G
            'dBd':  ('', 2.15, 10)}

           
class UnitError(ValueError):
    pass


class dBUnit(object):
    """ dB unit calculations """

    def __init__(self, value, unit, **kwargs):
        # initialize and convert to logarithm if islog=False
        islog = False
        self.z0 = 50.
        try:
            ip = get_ipython()
            self.ptformatter = ip.display_formatter.formatters['text/plain']
        except:
            self.ptformatter = None
        self.format = '' # display format for number to string conversion
        for key, val in list(kwargs.items()):
            if key is 'islog':
                islog = val    # convert to log at initialization
        if dB_units[unit]:
            self.unit = unit
            if islog is True:
                self.value = value
            else:
                self.value = dB_units[self.unit][2] * np.log10(value) - dB_units[self.unit][1]
        else:
            raise UnitError('Unknown unit %s' % unit)

        for key, val in list(kwargs.items()):
            # add attributes, e.g. varname.dBm
            if key is 'attr':
                base = dB_units[self.unit][0]
                for attr in dB_units.keys():
                    if dB_units[attr][0] == base:
                        setattr(self,attr, self.to(attr))

    def __dir__(self):
        """ return list of dB units for tab completion """
        try:
            base = dB_units[self.unit][0]
        except:
            raise AttributeError
        if base == '':
            return

        x = []
        for _u in dB_units:
            if dB_units[_u][0] == base:
                x.append(_u)
        x.append(base)
        return filter(None,[str(_x) for _x in x])
    
    def __getattr__(self,attr):
        """ Convert to different scaling in the same unit.
            If a '_' is appended, drop unit after rescaling and return value only.
        """
        dropunit = (attr[-1] == '_')
        unit = attr.strip('_')
        isdBunit = unit in dB_units.keys()
        islinunit = unit in  dB_units[self.unit][0]

        if islinunit:
            if dropunit is False:
                return pq.Q(self.__float__(),dB_units[self.unit][0] )
            else:
                return self.__float__()
        
        # convert to different scaling
        if self.unit is unit:
            return self
        elif dB_units[unit][0] is dB_units[self.unit][0]:
            # convert to same base unit, only scaling
            value = self.value + dB_units[self.unit][1] - dB_units[unit][1]
            if dropunit is False:
                return self.__class__(value, unit, islog=True)
            else:
                return value
        else:
            raise UnitError('No conversion between units %s and %s' % (self.unit, unit))

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
		
    @property
    def dB(self):
        # return dB value without unit
        return dBUnit(self.value, 'dB', islog=True)

    def __add__(self, other):
        if (self.unit is 'dB') or (other.unit is 'dB'):
            # easy unitless adding
            value = self.value + other.value
            return self.__class__(value, self.unit, islog=True)
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
        if self.unit is 'dB' and not hasattr(other,'unit'):
            # dB without physical dimension can be multiplied with a factor
            print self,self.value,other,value
            return self.__class__(value, self.unit, islog=True)

    __rmul__ = __mul__

    def __div__(self, other):
        if self.unit is 'dB' and not hasattr(other,'unit'):
            # dB without physical dimension can be divided by a factor
            value = self.value / other
            return self.__class__(value, self.unit, islog=True)

    __rdiv__ = __div__

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
        return '<dBUnit ' + str(self) + '>'
