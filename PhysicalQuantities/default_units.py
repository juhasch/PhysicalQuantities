"""

"""
from math import pi

from .prefixes import addprefixed
from .unit import add_composite_unit

add_composite_unit('g', 0.001, 'kg', verbosename='Gramm', url='https://en.wikipedia.org/wiki/Kilogram')

add_composite_unit('deg', pi/180, 'rad', verbosename='Degrees', url='http://en.wikipedia.org/wiki/Degree_%28angle%29')
add_composite_unit('arcmin', pi/180/60,'rad', verbosename='minutes of arc')
add_composite_unit('arcsec', pi/180/3600, 'rad', verbosename='seconds of arc')
add_composite_unit('min', 60,'s', verbosename='Minute', url='https://en.wikipedia.org/wiki/Minute')
add_composite_unit('h', 60*60, 's', verbosename='Hour', url='https://en.wikipedia.org/wiki/Hour')

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

addprefixed(add_composite_unit('Hz', 1, '1/s', verbosename='Hertz',
                               url='https://en.wikipedia.org/wiki/Hertz'), 'engineering')
addprefixed(add_composite_unit('N', 1, 'm*kg/s**2', verbosename='Newton',
                               url='https://en.wikipedia.org/wiki/Newton_(unit)'), prefixrange='engineering')
addprefixed(add_composite_unit('Pa', 1, 'N/m**2', verbosename='Pascal',
                               url='https://en.wikipedia.org/wiki/Pascal_(unit)'), prefixrange='engineering')
addprefixed(add_composite_unit('J', 1, 'N*m', verbosename='Joule',
                               url='https://en.wikipedia.org/wiki/Joule'), prefixrange='engineering')
addprefixed(add_composite_unit('W', 1, 'J/s', verbosename='Watt',
                               url='https://en.wikipedia.org/wiki/Watt'), prefixrange='engineering')
addprefixed(add_composite_unit('C', 1, 's*A', verbosename='Coulomb',
                               url='https://en.wikipedia.org/wiki/Coulomb'), prefixrange='engineering')
addprefixed(add_composite_unit('V', 1, 'W/A', verbosename='Volt',
                               url='https://en.wikipedia.org/wiki/Volt'), prefixrange='engineering')
addprefixed(add_composite_unit('F', 1, 'C/V', verbosename='Farad',
                               url='https://en.wikipedia.org/wiki/Farad'), prefixrange='engineering')
addprefixed(add_composite_unit('Ohm', 1, 'V/A', verbosename='Ohm',
                               url='https://en.wikipedia.org/wiki/Ohm_(unit)'), prefixrange='engineering')
addprefixed(add_composite_unit('S', 1, 'A/V', verbosename='Siemens',
                               url='https://en.wikipedia.org/wiki/Siemens_(unit)'), prefixrange='engineering')
addprefixed(add_composite_unit('Wb', 1, 'V*s', verbosename='Weber',
                               url='https://en.wikipedia.org/wiki/Weber_(unit)'), prefixrange='engineering')
addprefixed(add_composite_unit('T', 1, 'Wb/m**2', verbosename='Tesla',
                               url='https://en.wikipedia.org/wiki/Tesla_(unit)'), prefixrange='engineering')
addprefixed(add_composite_unit('H', 1, 'Wb/A', verbosename='Henry',
                               url='https://en.wikipedia.org/wiki/Henry_(unit)'), prefixrange='engineering')
addprefixed(add_composite_unit('lm', 1, 'cd*sr', verbosename='Lumen',
                               url='https://en.wikipedia.org/wiki/Lumen_(unit)'), prefixrange='engineering')
addprefixed(add_composite_unit('lx', 1, 'lm/m**2', verbosename='Lux',
                               url='https://en.wikipedia.org/wiki/Lux'), prefixrange='engineering')
