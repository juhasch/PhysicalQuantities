# Define additional units
from .prefixes import addprefixed
from .unit import *

add_composite_unit('Bq', '1/s', 'Becquerel')
add_composite_unit('Gy', 'J/kg', 'Gray')
add_composite_unit('Sv', 'J/kg', 'Sievert')
add_composite_unit('kat', 'mol/s', 'Katal')

add_composite_unit('abA', '10*A', 'Abampere')

# Time units
add_composite_unit('d', '24*h', 'day')
add_composite_unit('wk', '7*d', 'week')
add_composite_unit('yr', '365.25*d', 'year')
add_composite_unit('fortnight', '1209600*s', '14 days')

# Length units
add_composite_unit('Ang', '1.e-10*m', 'Angstrom')
add_composite_unit('AA', '1.e-10*m', 'Angstrom')

add_composite_unit('c0', '299792458*m/s','speed of light')
add_composite_unit('lyr', 'c0*yr', 'light year')

add_composite_unit('eps0', '28.854188e-12*F/m', 'vacuum permittivity')
add_composite_unit('Bohr', '4*pi*eps0*hbar**2/me/e0**2', 'Bohr radius')
add_composite_unit('furlong', '201.168*m', 'furlongs')
add_composite_unit('au', '149597870691*m', 'astronomical unit')

# Area units
add_composite_unit('ha', '10000*m**2', 'hectare')
add_composite_unit('acres', 'mi**2/640', 'acre')
add_composite_unit('b', '1.e-28*m', 'barn')

# Volume units
add_composite_unit('tsp', '4.92892159375*cm**3', 'teaspoon')
add_composite_unit('tbsp', '3*tsp', 'tablespoon')

# Mass units
add_composite_unit('t', '1000*kg', 'Metric ton')
add_composite_unit('amu', '1.660538921e-27*kg', 'atomic mass units')
add_composite_unit('Da', '1*amu', 'Dalton')

# Force units
add_composite_unit('dyn', '1.e-5*N', 'dyne (cgs unit)')

# Energy units
add_composite_unit('erg', '1.e-7*J', 'erg (cgs unit)')
addprefixed(add_composite_unit('eV', 'e0*V', 'electron volt'), range='engineering')
add_composite_unit('Hartree', 'me*e0**4/16/pi**2/eps0**2/hbar**2', 'Wavenumbers/inverse cm')
add_composite_unit('Ken', 'kb*K', 'Kelvin as energy unit')
add_composite_unit('cal', '4.184*J', 'thermochemical calorie')
add_composite_unit('kcal', '1000*cal', 'thermochemical kilocalorie')
add_composite_unit('cali', '4.1868*J', 'international calorie')
add_composite_unit('kcali', '1000*cali', 'international kilocalorie')


# Electromagnetic units
addprefixed(add_composite_unit('G', '1e-4*T', 'Gauss'), range='engineering')
addprefixed(add_composite_unit('Oe', '79.5774715*A/m', 'Oersted'), range='engineering')

# Power units
add_composite_unit('hp', '745.7*W', 'horsepower')

# Pressure units
add_composite_unit('bar', '1.e5*Pa', 'bar (cgs unit)')
add_composite_unit('mbar', '1.e2*Pa', 'millibar')
add_composite_unit('kbar', '1.e8*Pa', 'kilobar')
add_composite_unit('atm', '101325.*Pa', 'standard atmosphere')
add_composite_unit('torr', 'atm/760', 'torr = mm of mercury')

# Temperature units
add_composite_unit('degR', '(5./9.)*K', 'degrees Rankine')
add_composite_unit('degC', PhysicalUnit('K',   1.,    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], offset=273.15),
        url='https://en.wikipedia.org/wiki/Celsius', verbosename='degrees Celsius')

# Radiation-related units
addprefixed(add_composite_unit('Ci', '3.7e10*Bq', 'Curie'), range='engineering')
addprefixed(add_composite_unit('rem', '0.01*Sv', 'Rem'), range='engineering')

# Astronomical units
add_composite_unit('Msol', '1.98892e30*kg', 'solar mass')
add_composite_unit('Lsol', '3.839e26*W', 'solar luminosity')
addprefixed(add_composite_unit('pc', '3.08568025e16*m'), range='engineering')
