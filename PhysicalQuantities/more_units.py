# -*- coding: utf-8 -*-
# Define additional units
from .Unit import *
from .prefixes import addprefixed

addunit('Bq', '1/s', 'Becquerel')
addunit('Gy', 'J/kg', 'Gray')
addunit('Sv', 'J/kg', 'Sievert')
addunit('kat', 'mol/s', 'Katal')

addunit('abA', '10*A', 'Abampere')

# Time units
addunit('d', '24*h', 'day')
addunit('wk', '7*d', 'week')
addunit('yr', '365.25*d', 'year')
addunit('fortnight', '1209600*s', '14 days')

# Length units
addunit('Ang', '1.e-10*m', 'Angstrom')
addunit('AA', '1.e-10*m', 'Angstrom')

addunit('c0', '299792458*m/s','speed of light')
addunit('lyr', 'c0*yr', 'light year')

addunit('eps0', '28.854188e-12*F/m', 'vacuum permittivity')
addunit('Bohr', '4*pi*eps0*hbar**2/me/e0**2', 'Bohr radius')
addunit('furlong', '201.168*m', 'furlongs')
addunit('au', '149597870691*m', 'astronomical unit')

# Area units
addunit('ha', '10000*m**2', 'hectare')
addunit('acres', 'mi**2/640', 'acre')
addunit('b', '1.e-28*m', 'barn')

# Volume units
addunit('tsp', '4.92892159375*cm**3', 'teaspoon')
addunit('tbsp', '3*tsp', 'tablespoon')

# Mass units
addunit('t', '1000*kg', 'Metric ton')
addunit('amu', '1.660538921e-27*kg', 'atomic mass units')
addunit('Da', '1*amu', 'Dalton')

# Force units
addunit('dyn', '1.e-5*N', 'dyne (cgs unit)')

# Energy units
addunit('erg', '1.e-7*J', 'erg (cgs unit)')
addprefixed(addunit('eV', 'e0*V', 'electron volt'), range='engineering')
addunit('Hartree', 'me*e0**4/16/pi**2/eps0**2/hbar**2', 'Wavenumbers/inverse cm')
addunit('Ken', 'kb*K', 'Kelvin as energy unit')
addunit('cal', '4.184*J', 'thermochemical calorie')
addunit('kcal', '1000*cal', 'thermochemical kilocalorie')
addunit('cali', '4.1868*J', 'international calorie')
addunit('kcali', '1000*cali', 'international kilocalorie')


# Electromagnetic units
addprefixed(addunit('G', '1e-4*T', 'Gauss'), range='engineering')
addprefixed(addunit('Oe', '79.5774715*A/m', 'Oersted'), range='engineering')

# Power units
addunit('hp', '745.7*W', 'horsepower')

# Pressure units
addunit('bar', '1.e5*Pa', 'bar (cgs unit)')
addunit('mbar', '1.e2*Pa', 'millibar')
addunit('kbar', '1.e8*Pa', 'kilobar')
addunit('atm', '101325.*Pa', 'standard atmosphere')
addunit('torr', 'atm/760', 'torr = mm of mercury')

# Temperature units
addunit('degR', '(5./9.)*K', 'degrees Rankine')
addunit('degC', PhysicalUnit('K',   1.,    [0, 0, 0, 0, 1, 0, 0, 0, 0], offset=273.15),
        url='https://en.wikipedia.org/wiki/Celsius', verbosename='degrees Celsius')

# Radiation-related units
addprefixed(addunit('Ci', '3.7e10*Bq', 'Curie'), range='engineering')
addprefixed(addunit('rem', '0.01*Sv', 'Rem'), range='engineering')

# Astronomical units
addunit('Msol', '1.98892e30*kg', 'solar mass')
addunit('Lsol', '3.839e26*W', 'solar luminosity')
addprefixed(addunit('pc', '3.08568025e16*m'), range='engineering')
