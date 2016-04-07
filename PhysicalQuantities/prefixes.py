# -*- coding: utf-8 -*-
from .Quantity import unit_table
from .Unit import addunit

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
            addunit(prefixedname, prefix[1] * unit, prefixed=True, baseunit=unit, verbosename=unit.verbosename,
                    url=unit.url)


# Add additional units (base SI units are predefined)
addprefixed('m', prefixrange='engineering')
addprefixed('g', prefixrange='engineering')
addprefixed('s', prefixrange='engineering')
addprefixed('A', prefixrange='engineering')
addprefixed('K', prefixrange='engineering')
addprefixed('mol', prefixrange='engineering')
addprefixed('cd', prefixrange='engineering')
addprefixed('rad', prefixrange='engineering')
addprefixed('sr', 'prefixrange=engineering')

addprefixed(addunit('Hz', '1/s', 'Hertz', url='https://en.wikipedia.org/wiki/Hertz'), 'engineering')
addprefixed(addunit('N', 'm*kg/s**2', 'Newton', url='https://en.wikipedia.org/wiki/Newton_(unit)'), prefixrange='engineering')
addprefixed(addunit('Pa', 'N/m**2', 'Pascal', url='https://en.wikipedia.org/wiki/Pascal_(unit)'), prefixrange='engineering')
addprefixed(addunit('J', 'N*m', 'Joule', url='https://en.wikipedia.org/wiki/Joule'), prefixrange='engineering')
addprefixed(addunit('W', 'J/s', 'Watt', url='https://en.wikipedia.org/wiki/Watt'), prefixrange='engineering')
addprefixed(addunit('C', 's*A', 'Coulomb', url='https://en.wikipedia.org/wiki/Coulomb'), prefixrange='engineering')
addprefixed(addunit('V', 'W/A', 'Volt', url='https://en.wikipedia.org/wiki/Volt'), prefixrange='engineering')
addprefixed(addunit('F', 'C/V', 'Farad', url='https://en.wikipedia.org/wiki/Farad'), prefixrange='engineering')
addprefixed(addunit('Ohm', 'V/A', 'Ohm', url='https://en.wikipedia.org/wiki/Ohm_(unit)'), prefixrange='engineering')
addprefixed(addunit('S', 'A/V', 'Siemens', url='https://en.wikipedia.org/wiki/Siemens_(unit)'), prefixrange='engineering')
addprefixed(addunit('Wb', 'V*s', 'Weber', url='https://en.wikipedia.org/wiki/Weber_(unit)'), prefixrange='engineering')
addprefixed(addunit('T', 'Wb/m**2', 'Tesla', url='https://en.wikipedia.org/wiki/Tesla_(unit)'), prefixrange='engineering')
addprefixed(addunit('H', 'Wb/A', 'Henry', url='https://en.wikipedia.org/wiki/Henry_(unit)'), prefixrange='engineering')
addprefixed(addunit('lm', 'cd*sr', 'Lumen', url='https://en.wikipedia.org/wiki/Lumen_(unit)'), prefixrange='engineering')
addprefixed(addunit('lx', 'lm/m**2', 'Lux', url='https://en.wikipedia.org/wiki/Lux'), prefixrange='engineering')
