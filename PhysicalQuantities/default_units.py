"""

"""
from .unit import *
from .prefixes import addprefixed
from math import pi

addunit('g', 0.001, 'kg', 'Gramm', url='https://en.wikipedia.org/wiki/Kilogram')

addunit('deg', pi/180, 'rad', 'Degrees', url='http://en.wikipedia.org/wiki/Degree_%28angle%29')
addunit('arcmin', pi/180/60 ,'rad', 'minutes of arc')
addunit('arcsec', pi/180/3600 ,'rad', 'seconds of arc')
addunit('min', 60,'s', 'Minute', url='https://en.wikipedia.org/wiki/Minute')
addunit('h', 60*60, 's', 'Hour', url='https://en.wikipedia.org/wiki/Hour')

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

addprefixed(addunit('Hz', 1, '1/s', 'Hertz', url='https://en.wikipedia.org/wiki/Hertz'), 'engineering')
addprefixed(addunit('N', 1, 'm*kg/s**2', 'Newton', url='https://en.wikipedia.org/wiki/Newton_(unit)'), prefixrange='engineering')
addprefixed(addunit('Pa', 1, 'N/m**2', 'Pascal', url='https://en.wikipedia.org/wiki/Pascal_(unit)'), prefixrange='engineering')
addprefixed(addunit('J', 1, 'N*m', 'Joule', url='https://en.wikipedia.org/wiki/Joule'), prefixrange='engineering')
addprefixed(addunit('W', 1, 'J/s', 'Watt', url='https://en.wikipedia.org/wiki/Watt'), prefixrange='engineering')
addprefixed(addunit('C', 1, 's*A', 'Coulomb', url='https://en.wikipedia.org/wiki/Coulomb'), prefixrange='engineering')
addprefixed(addunit('V', 1, 'W/A', 'Volt', url='https://en.wikipedia.org/wiki/Volt'), prefixrange='engineering')
addprefixed(addunit('F', 1, 'C/V', 'Farad', url='https://en.wikipedia.org/wiki/Farad'), prefixrange='engineering')
addprefixed(addunit('Ohm', 1, 'V/A', 'Ohm', url='https://en.wikipedia.org/wiki/Ohm_(unit)'), prefixrange='engineering')
addprefixed(addunit('S', 1, 'A/V', 'Siemens', url='https://en.wikipedia.org/wiki/Siemens_(unit)'), prefixrange='engineering')
addprefixed(addunit('Wb', 1, 'V*s', 'Weber', url='https://en.wikipedia.org/wiki/Weber_(unit)'), prefixrange='engineering')
addprefixed(addunit('T', 1, 'Wb/m**2', 'Tesla', url='https://en.wikipedia.org/wiki/Tesla_(unit)'), prefixrange='engineering')
addprefixed(addunit('H', 1, 'Wb/A', 'Henry', url='https://en.wikipedia.org/wiki/Henry_(unit)'), prefixrange='engineering')
addprefixed(addunit('lm', 1, 'cd*sr', 'Lumen', url='https://en.wikipedia.org/wiki/Lumen_(unit)'), prefixrange='engineering')
addprefixed(addunit('lx', 1, 'lm/m**2', 'Lux', url='https://en.wikipedia.org/wiki/Lux'), prefixrange='engineering')
