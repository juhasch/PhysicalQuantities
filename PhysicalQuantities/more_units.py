# Define additional units
import PhysicalQuantities
from .prefixes import addprefixed
from .unit import add_composite_unit

#add_composite_unit('Bq', 1., '1/s', verbosename='Becquerel', url='https://en.wikipedia.org/wiki/Becquerel')
#add_composite_unit('Gy', 1., 'm**2/s**2', verbosename='Gray', url='https://en.wikipedia.org/wiki/Gray_(unit)')
#add_composite_unit('Sv', 1., 'J/kg', verbosename='Sievert', url='https://en.wikipedia.org/wiki/Sievert')
#add_composite_unit('kat', 1., 'mol/s', verbosename='Katal', url='https://en.wikipedia.org/wiki/Katal')
#add_composite_unit('abA', 1., '10*A', verbosename='Abampere', url='https://en.wikipedia.org/wiki/Abampere')

# Time units
add_composite_unit('d', 24, 'h', verbosename='day')
add_composite_unit('wk',7, 'd', verbosename='week')
add_composite_unit('yr', 365.25, 'd', verbosename='year')
add_composite_unit('fortnight', 1209600, 's', verbosename='14 days')

# Length units
#add_composite_unit('Ang', 1.e-10, 'm', verbosename='Angstrom')
#add_composite_unit('AA', 1.e-10, 'm', verbosename='Angstrom')

#add_composite_unit('lyr', 'c0*yr', verbosename='light year')

#add_composite_unit('Bohr', 4*pi, 'eps0*hbar**2/me/e0**2', verbosename='Bohr radius')
#add_composite_unit('furlong', 201.168, 'm', verbosename='furlongs')
#add_composite_unit('au', 149597870691, 'm', verbosename='astronomical unit')

# Area units
#add_composite_unit('ha', 10000, 'm**2', verbosename='hectare')
#add_composite_unit('acres', 1/640., 'mi**2', verbosename='acre')
#add_composite_unit('b', 1.e-28, 'm', verbosename='barn')

# Volume units
#add_composite_unit('tsp', 4.92892159375, 'cm**3', verbosename='teaspoon')
#add_composite_unit('tbsp', 3, 'tsp', verbosename='tablespoon')

# Mass units
#add_composite_unit('t', 1000, 'kg', verbosename='Metric ton')
#add_composite_unit('amu', 1.660538921e-27, 'kg', verbosename='atomic mass units')
#add_composite_unit('Da', 1., 'amu', verbosename='Dalton')

# Force units
#add_composite_unit('dyn', 1.e-5, 'N', verbosename='dyne (cgs unit)')

# Energy units
#add_composite_unit('erg', 1.e-7, 'J', verbosename='erg (cgs unit)')
#addprefixed(add_composite_unit('eV', 'e0*V', verbosename='electron volt'), prefixrange='engineering')
#add_composite_unit('Hartree', 1., 'me*e0**4/16/pi**2/eps0**2/hbar**2', verbosename='Wavenumbers/inverse cm')
#add_composite_unit('Ken', 1., 'kb*K', verbosename='Kelvin as energy unit')
add_composite_unit('cal', 4.184, 'J', verbosename='thermochemical calorie')
add_composite_unit('kcal', 1000, 'cal', verbosename='thermochemical kilocalorie')
add_composite_unit('cali', 4.1868,'J', verbosename='international calorie')
add_composite_unit('kcali', 1000, 'cali', verbosename='international kilocalorie')

# Electromagnetic units
#addprefixed(add_composite_unit('G', 1e-4, 'T', verbosename='Gauss'), prefixrange='engineering')
#addprefixed(add_composite_unit('Oe', 79.5774715, 'A/m', verbosename='Oersted'), prefixrange='engineering')

# Power units
#add_composite_unit('hp', 745.7, 'W', verbosename='horsepower')

# Pressure units
#add_composite_unit('bar', 1.e5, 'Pa', verbosename='bar (cgs unit)')
#add_composite_unit('mbar', 1.e2, 'Pa', verbosename='millibar')
#add_composite_unit('kbar', 1.e8, 'Pa', verbosename='kilobar')
#add_composite_unit('atm', 101325, 'Pa', verbosename='standard atmosphere')
#add_composite_unit('torr', 1/760., 'atm', verbosename='torr = mm of mercury')

# Temperature units
#add_composite_unit('degR', 5./9., 'K', verbosename='degrees Rankine')
#add_composite_unit('degC', 1, offset=273.15, url='https://en.wikipedia.org/wiki/Celsius', verbosename='degrees Celsius')
# Radiation-related units
#addprefixed(add_composite_unit('Ci', 3.7e10, 'Bq', verbosename='Curie'), prefixrange='engineering')
#addprefixed(add_composite_unit('rem', 0.01, 'Sv', verbosename='Rem'), prefixrange='engineering')

# Astronomical units
#add_composite_unit('Msol', 1.98892e30, 'kg', verbosename='solar mass')
#add_composite_unit('Lsol', 3.839e26, 'W', verbosename='solar luminosity')

#addprefixed(add_composite_unit('pc', 3.08568025e16, 'm'), prefixrange='engineering')

PhysicalQuantities.q.update()
