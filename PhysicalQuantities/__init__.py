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
import collections

from .quantity import PhysicalQuantity
from .unit import unit_table, addunit, isphysicalunit, PhysicalUnit
from .prefixes import *
from .default_units import *
from .dBQuantity import dBQuantity, dB_unit_table
from .quantityarray import PhysicalQuantityArray
import numpy as np

__version__: str = '1.1.1'

Q = PhysicalQuantity
U = PhysicalUnit
QA = PhysicalQuantityArray


def np_add_unit(array: np.ndarray, unit: str = '') -> np.ndarray:
    """Add unit metadata to array

    Parameters
    ----------
     array: Input numpy array
     unit:  PhysicalUnit to assign to array
    """
    if len(unit) > 0:
        metadata = dict(unit=unit)
        dtype = np.dtype(str(array.dtype), metadata=metadata)
        return array.astype(dtype)
    return array


class _Quantity:
    """Class to provide attributes for all known units include prefixes

    Examples
    --------
    >>> from PhysicalQuantities import q
    >>> q['m']
    1 m
    >>> q.m
    1 m
    >>>  type(q['m'])
    PhysicalQuantities.quantity.PhysicalQuantity

    Notes
    -----
    When adding more units, the class has to be reinitialized using `update()`for the new units to be listed.
    """
    def __init__(self):
        self.table = {}
        self.update()

    def update(self):
        """ Update the table of known units"""
        for key in dB_unit_table:
            self.table[key] = dBQuantity(1, key)
        for key in unit_table:
            self.table[key] = PhysicalQuantity(1, unit_table[key])

    def __dir__(self):
        return self.table.keys()

    def __getitem__(self, key):
        try:
            if isinstance(key, str):
                _Q = self.table[key]
            else:
                _Q = self.table[key.name]
        except KeyError as exc:
            raise KeyError(f'Unit {key} not found') from exc
        return _Q

    def __getattr__(self, attr):
        try:
            _Q = self.table[attr]
        except KeyError as exc:
            raise KeyError(f'Unit {attr} not found') from exc
        return _Q
    
    def _ipython_key_completions_(self):
        return list(self.table.keys())


q: _Quantity = _Quantity()


def isphysicalquantity(x) -> bool:
    """ Test if parameter is a PhysicalQuantity or dBQuantity object

    Parameters
    ----------
    x:  PhysicalQuantity or dBQuantity
        parameter to test

    Returns
    -------
        True if x is a PhysicalQuantity

    Examples
    --------
    >>> isphysicalquantity( PhysicalQuantity(1, 'V'))
    True
    """
    return isinstance(x, (PhysicalQuantity, dBQuantity))


def units_html_list():
    """ List all defined units in a HTML table

    Returns
    -------
    str
        HTML formatted list of all defined units
    """
    from IPython.display import HTML  # type: ignore
    table = "<table>"
    table += "<tr><th>Name</th><th>Base Unit</th><th>Quantity</th></tr>"
    for name in unit_table:
        _unit = unit_table[name]
        if isinstance(_unit, PhysicalUnit):
            if _unit.prefixed is False:
                a = PhysicalQuantity(1, name)
                baseunit = a.base._repr_latex_()
                table += f'<tr><td>{name}</td><td>{baseunit}' + \
                         f'</td><td><a href="{_unit.url}" target="_blank">{_unit.verbosename}</a></td></tr>'
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
