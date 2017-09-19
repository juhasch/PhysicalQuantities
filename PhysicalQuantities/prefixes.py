# -*- coding: utf-8 -*-
from .quantity import unit_table
from .unit import add_composite_unit

# add scaling prefixes
_full_prefixes = [
    ('Y', 1.e24), ('Z', 1.e21), ('E', 1.e18), ('P', 1.e15), ('T', 1.e12),
    ('G', 1.e9), ('M', 1.e6), ('k', 1.e3), ('h', 1.e2), ('da', 1.e1),
    ('d', 1.e-1), ('c', 1.e-2), ('m', 1.e-3), ('u', 1.e-6), ('n', 1.e-9),
    ('p', 1.e-12), ('f', 1.e-15), ('a', 1.e-18), ('z', 1.e-21),
    ('y', 1.e-24),
]

# educed set of scaling prefixes for engineering purposes:
_engineering_prefixes = [
    ('T', 1.e12),
    ('G', 1.e9), ('M', 1.e6), ('k', 1.e3),
    ('c', 1.e-2), ('m', 1.e-3), ('u', 1.e-6), ('n', 1.e-9),
    ('p', 1.e-12), ('f', 1.e-15), ('a', 1.e-18),
]


def addprefixed(unitname, prefixrange='full'):
    """ Add prefixes to already defined unit

    Parameters
    ----------
    unitname: str
        Name of unit to be prefixed, e.k. 'm' -> 'mm','cm','dm','km'
    prefixrange: str
        Range: 'engineering' -> 1e-18 to 1e12 or 'full' -> 1e-24 to 1e24

    """
    if prefixrange == 'engineering':
        _prefixes = _engineering_prefixes
    else:
        _prefixes = _full_prefixes
    unit = unit_table[unitname]
    for prefix in _prefixes:
        prefixedname = prefix[0] + unitname
        if prefixedname not in unit_table:
            add_composite_unit(prefixedname, prefix[1], unitname, prefixed=True, baseunit=unit, verbosename=unit.verbosename,
                    url=unit.url)
