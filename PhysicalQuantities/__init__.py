# -*- coding: utf-8 -*-
"""
Physical Quantities for Python and IPython

Usage in Python:
================

    import PhysicalQuantities as pq
    a = pq.PhysicalQuantity(1.0, 'm')
or simply    
    a = pq.Q(1.0, 'm')

The value of a physical quantity can by any number, list or numpy array.
The units are derived from SI base units and can be any combination,
including prefixes:
    a = pq.Q(1.0, 'm**2/s**3')
    
Lists or arrays can also be used and indexed:
    b = [1,2,3]
    c = a*b
    print c[0]    

Usage in IPython:
===============

    %load_ext PyPUnits.ipython
Then you can type directly:
    a = 1 mm
without explicitly calling a function constructor

"""
from __future__ import absolute_import
from .Quantity import unit_table, PhysicalQuantity
from .Unit import addunit, isphysicalunit, PhysicalUnit
from .prefixes import *
from PhysicalQuantities.dBQuantity import dBQuantity, dB_unit_table
from math import pi
import collections

import pkg_resources
__version__ = '0.6.7'

Q = PhysicalQuantity
U = PhysicalUnit

unit_table['pi'] = pi
addunit('deg', 'pi*rad/180', 'Degree', url='http://en.wikipedia.org/wiki/Degree_%28angle%29')
addunit('arcmin', 'pi*rad/180/60', 'minutes of arc')
addunit('arcsec', 'pi*rad/180/3600', 'seconds of arc')
del unit_table['pi']
addunit('min', '60*s', 'Minute', url='https://en.wikipedia.org/wiki/Hour')
addunit('h', '60*60*s', 'Hour', url='https://en.wikipedia.org/wiki/Hour')


class _Quantity:
    def __init__(self):
        self.table = {}
        for key in dB_unit_table:
            self.table[key] = dBQuantity(1, key)
        for key in unit_table:
            self.table[key] = PhysicalQuantity(1, unit_table[key])

    def __dir__(self):
        return self.table.keys()

    def __getitem__(self, key):
        try:
            if type(key) is str:
                _Q = self.table[key]
            else:
                _Q = self.table[key.name]
        except KeyError:
            raise KeyError('Unit %s not found' % key)
        return _Q

    def __getattr__(self, attr):
        try:
            _Q = self.table[attr]
        except:
            raise AttributeError('Unit %s not found' % attr)
        return _Q
    
    def _ipython_key_completions_(self):
        return list(self.table.keys())

q = _Quantity()


def isphysicalquantity(x):
    """ Test if parameter is a PhysicalQuantity or dBQuantity object

    :param x: parameter to test
    :return: true if x is a PhysicalQuantity
    :rtype: bool

    >>> isphysicalquantity( PhysicalQuantity(1, 'V'))
    True
    """
    return isinstance(x, PhysicalQuantity) or isinstance(x, dBQuantity)


def units_html_list():
    """ List all defined units in a HTML table

    Returns
    -------
    str
        HTML formatted list of all defined units
    """
    from IPython.display import HTML
    table = "<table>"
    table += "<tr><th>Name</th><th>Base Unit</th><th>Quantity</th></tr>"
    for name in unit_table:
        unit = unit_table[name]
        if isinstance(unit, PhysicalUnit):
            if unit.prefixed is False:
                a = PhysicalQuantity(1, name)
                baseunit = a.base._repr_latex_()
                table += "<tr><td>" + name + '</td><td>' + baseunit + \
                         '</td><td><a href="' + unit.url + '" target="_blank">' + unit.verbosename + \
                         '</a></td></tr>'
    table += "</table>"
    return HTML(table)


def units_list():
    """ List all defined units

    Returns
    -------
    str
        List of all defined units
    """
    units = []
    baseunits = []
    ut = collections.OrderedDict(sorted(unit_table.items()))
    for name in ut:
        unit = unit_table[name]
        if isinstance(unit, PhysicalUnit) and unit.prefixed is False:
            units.append(unit.name)
            a = PhysicalQuantity(1, name)
            baseunits.append(str(a.base))
    return units, baseunits
