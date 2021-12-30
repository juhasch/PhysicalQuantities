"""Physical Quantities for Python and IPython"""
import sys

from .quantity import PhysicalQuantity
from .unit import unit_table, addunit, isphysicalunit, PhysicalUnit
from .prefixes import *
from .default_units import *
from PhysicalQuantities.dBQuantity import dBQuantity, dB_unit_table
from PhysicalQuantities.quantityarray import PhysicalQuantityArray
from .qattributes import QuantityAttributes

if sys.version_info < (3, 8):
    sys.exit('Sorry, Python < 3.8 is not supported')

__version__ = '1.1.0'

QA = PhysicalQuantityArray
Q = PhysicalQuantity
U = PhysicalUnit

q = QuantityAttributes()


def isphysicalquantity(x) -> bool:
    """ Test if parameter is a PhysicalQuantity or dBQuantity object

    Parameters
    ----------
    x
        parameter to test

    Returns
    -------
        True if x is a PhysicalQuantity

    Examples
    --------
    >>> isphysicalquantity( PhysicalQuantity(1, 'V'))
    True
    """
    return isinstance(x, PhysicalQuantity) or isinstance(x, dBQuantity)


def units_html_list() -> str:
    """ List all defined units in a HTML table

    Returns
    -------
        HTML formatted list of all defined units
    """
    from IPython.display import HTML
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


def units_list() -> list:
    """ List all defined units without prefixes

    Returns
    -------
        List of all defined units without prefixes
    """
    units = list()
    for key in unit_table:
        if not unit_table[key].prefixed:
            units.append(key)
    return sorted(units)
