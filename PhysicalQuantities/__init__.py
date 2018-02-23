"""
Physical Quantities for Python and IPython

Usage in Python:
================

    from PhysicalQuantities import PhysiscalQuantity, q
    a = PhysicalQuantity(1.0, 'm')
or simply    
    a = 1.0 * q.mm

The value of a physical quantity can by any number, list or numpy array.
The units are derived from SI base units and can be any combination,
including prefixes:
    a = PhysicalQuantity(1.0, 'm**2/s**3')
    
Usage in IPython:
===============

    %load_ext PhysicalQuantities.ipython
Then you can type directly:
    a = 1 mm
without explicitly calling a function constructor

"""
from .quantity import unit_table, PhysicalQuantity
from .unit import addunit, isphysicalunit, PhysicalUnit
from .prefixes import *
import collections
from .default_units import *
from PhysicalQuantities.dBQuantity import dBQuantity, dB_unit_table
import sys

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported')

__version__ = '0.8.0'

Q = PhysicalQuantity
U = PhysicalUnit


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
            raise KeyError(f'Unit {key} not found')
        return _Q

    def __getattr__(self, attr):
        try:
            _Q = self.table[attr]
        except KeyError:
            raise KeyError(f'Unit {attr} not found')
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
                table += f'<tr><td>{name}</td><td>{baseunit}' + \
                         f'</td><td><a href="{unit.url}" target="_blank">{unit.verbosename}</a></td></tr>'
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
        _unit = unit_table[name]
        if isinstance(_unit, PhysicalUnit) and _unit.prefixed is False:
            units.append(_unit.name)
            a = PhysicalQuantity(1, name)
            baseunits.append(str(a.base))
    return units, baseunits
