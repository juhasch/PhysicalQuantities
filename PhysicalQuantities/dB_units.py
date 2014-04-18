""" IPython extension for dB calculations """

#-----------------------------------------------------------------------------
#  Copyright (C) 2013  The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

import re
import numpy as np

import PhysicalQuantities as pq

from IPython.core.inputtransformer import StatelessInputTransformer

# list of tuples: (base unit, correction factor to base unit, conversion factor to linear)
_dB_units = {'dB':  ('', 0, 1),
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
        self.stddev = 0
        self.z0 = 50
        for key, val in kwargs.iteritems():
            if key is 'islog':
                islog = val    # convert to log at initialization
            if key is 'stddev':
                self.stddev = val
        if _dB_units[unit]:
            self.unit = unit
            if islog is True:
                self.value = value
            else:
                self.value = _dB_units[self.unit][2] * np.log10(value) - _dB_units[self.unit][1]
        else:
            raise UnitError('Unknown unit %s' % unit)

        for key, val in kwargs.iteritems():
            # add attributes, e.g. varname.dBm
            if key is 'attr':
                base = _dB_units[self.unit][0]
                for attr in _dB_units.keys():
                    if _dB_units[attr][0] == base:
                        setattr(self,attr, self.to(attr))

    def __dir__(self):
        """ return list of dB units for tab completion """
        try:
            base = _dB_units[self.unit][0]
        except:
            raise AttributeError
        if base == '':
            return

        x = []
        for _u in _dB_units:
            if _dB_units[_u][0] == base:
                x.append(_u)
        x.append(base)
        return filter(None,[str(_x) for _x in x])
    
    def __getattr__(self,attr):
        """ Convert to different scaling in the same unit.
            If a '_' is appended, drop unit after rescaling and return value only.
        """
        dropunit = (attr[-1] == '_')
        unit = attr.strip('_')
        isdBunit = unit in _dB_units.keys()
        islinunit = unit in  _dB_units[self.unit][0]

        if islinunit:
            if dropunit is False:
                return pu.Q(self.__float__(),_dB_units[self.unit][0] )
            else:
                return self.__float__()
        
        # convert to different scaling
        if self.unit is unit:
            return self
        elif _dB_units[unit][0] is _dB_units[self.unit][0]:
            # convert to same base unit, only scaling
            value = self.value + _dB_units[self.unit][1] - _dB_units[unit][1]
            if dropunit is False:
                return self.__class__(value, unit, islog=True)
            else:
                return value
        else:
            raise UnitError('No conversion between units %s and %s' % (self.unit, unit))
            
    @property
    def dB(self):
        # return dB value without unit
        return dBUnit(self.value, 'dB', islog=True)

    def __add__(self, other):
        if (self.unit is 'dB') or (other.unit is 'dB'):
            # easy unitless adding
            value = self.value + other.value
            return self.__class__(value, self.unit, islog=True)
        elif _dB_units[self.unit][0] is _dB_units[other.unit][0]:
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
        elif _dB_units[self.unit][0] is _dB_units[other.unit][0]:
            # same unit substraction
            val1 = float(self)
            val2 = float(other)
            return self.__class__(val1-val2, self.unit, islog=False)
        else:
            raise UnitError('Cannot add unequal units %s and %s' % (self.unit, other.unit))

    __rsub__ = __sub__

    def __float__(self):
        # return linear value in base unit
        dbw = self.value + _dB_units[self.unit][1]
        return 10**(dbw/(_dB_units[self.unit][2]))

    def __str__(self):
        return "%.1f %s" % (self.value, self.unit)

    def __repr__(self):
        return '<dBUnit ' + str(self.value) + ' ' + self.unit + '>'

# regex: number + space + dB-unit
# valid: 0dBm, 0 dBm, 0. dBm
# invalid: 0.dBm
number = r'(-?[\d0-9-.]+)'
_unit_list = '('
for x in _dB_units.keys()[0:-1]:
    _unit_list += x + '|'
_unit_list += _dB_units.keys()[-1] + ')'
match = number + r'(\s*)' + _unit_list

# regex for finding units and quoted strings
number = r'-?[\d0-9.]+'  # problem: 1dBm-0dB
stringmatch = r'(["\'])(?:(?=(\\?))\2.)*?\1'
match = stringmatch + '|' + number + r'(\s*)' + _unit_list
line_match = re.compile(match)

# regex to match unit after it has been found using line_match
number = r'(-?[\d0-9-]+' +r'-?[\d0-9.eE-]*)'
match = number + r'(.\s|\s*)' + _unit_list
unit_match = re.compile(match)


def replace_inline(ml):
    """Replace an inline unit expression by valid Python code
    """
    if ml.group()[0][0] in '"\'':
        return ml.group()

    def replace_unit(mo):
        try:
            return "dBUnit(" + mo.group(1) + ", '" + mo.group(3) + "', islog=True)"
        except KeyError:
            return mo.group()

    return unit_match.sub(replace_unit, ml.group())


@StatelessInputTransformer.wrap
def dBUnit_transform(line):
    line = line_match.sub(replace_inline, line)
    return line

__transformer = dBUnit_transform()


def load_ipython_extension(ip):
    global __transformer
    ip.input_transformer_manager.logical_line_transforms.insert(0, __transformer)
    ip.user_ns['dBUnit'] = dBUnit


def unload_ipython_extension(ip):
    global __transformer
    if type(__transformer) is StatelessInputTransformer:
        ip.input_transformer_manager.logical_line_transforms.remove(__transformer)
        ip.user_ns.pop('dBUnit')
