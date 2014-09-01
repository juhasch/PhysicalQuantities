# -*- coding: utf-8 -*-
# Define additional units
from .Unit import *
from .constants import *

addUnit('Bq', '1/s', 'Becquerel')
addUnit('Gy', 'J/kg', 'Gray')
addUnit('Sv', 'J/kg', 'Sievert')
addUnit('kat', 'mol/s', 'Katal')

addUnit('abA', '10*A', 'Abampere')

# Time units
addUnit('d', '24*h', 'day')
addUnit('wk', '7*d', 'week')
addUnit('yr', '365.25*d', 'year')
addUnit('fortnight', '1209600*s', '14 days')

# Length units
addUnit('Ang', '1.e-10*m', 'Angstrom')
addUnit('AA', '1.e-10*m', 'Angstrom')

addUnit('c0','299792458*m/s','speed of light')
addUnit('lyr', 'c0*yr', 'light year')

addUnit('eps0','28.854188e-12*F/m','vacuum permittivity')
addUnit('Bohr', '4*pi*eps0*hbar**2/me/e0**2', 'Bohr radius')
addUnit('furlong', '201.168*m', 'furlongs')
addUnit('au', '149597870691*m', 'astronomical unit')

# Area units
addUnit('ha', '10000*m**2', 'hectare')
addUnit('acres', 'mi**2/640', 'acre')
addUnit('b', '1.e-28*m', 'barn')

# Volume units
addUnit('tsp', '4.92892159375*cm**3', 'teaspoon')
addUnit('tbsp', '3*tsp', 'tablespoon')

# Mass units
addUnit('t', '1000*kg', 'Metric ton')
addUnit('amu', '1.660538921e-27*kg', 'atomic mass units')
addUnit('Da', '1*amu', 'Dalton')

# Force units
addUnit('dyn', '1.e-5*N', 'dyne (cgs unit)')

# Energy units
addUnit('erg', '1.e-7*J', 'erg (cgs unit)')
addPrefixed(addUnit('eV', 'e0*V', 'electron volt'),range='engineering')
addUnit('Hartree', 'me*e0**4/16/pi**2/eps0**2/hbar**2', 'Wavenumbers/inverse cm')
addUnit('Ken', 'kb*K', 'Kelvin as energy unit')
addUnit('cal', '4.184*J', 'thermochemical calorie')
addUnit('kcal', '1000*cal', 'thermochemical kilocalorie')
addUnit('cali', '4.1868*J', 'international calorie')
addUnit('kcali', '1000*cali', 'international kilocalorie')


# Electromagnetic units
addPrefixed(addUnit('G', '1e-4*T', 'Gauss'),range='engineering')
addPrefixed(addUnit('Oe', '79.5774715*A/m', 'Oersted'),range='engineering')

# Power units
addUnit('hp', '745.7*W', 'horsepower')

# Pressure units
addUnit('bar', '1.e5*Pa', 'bar (cgs unit)')
addUnit('mbar', '1.e2*Pa', 'millibar')
addUnit('kbar', '1.e8*Pa', 'kilobar')
addUnit('atm', '101325.*Pa', 'standard atmosphere')
addUnit('torr', 'atm/760', 'torr = mm of mercury')

# Temperature units -- can't use the 'eval' trick that _addUnit provides
# for degC and degF because you can't add units
addUnit('degR', '(5./9.)*K', 'degrees Rankine')
addUnit('degC', PhysicalUnit(None, 1.0, kelvin.powers, 273.15),
         'degrees Celcius')

# Radiation-related units
addPrefixed(addUnit('Ci', '3.7e10*Bq', 'Curie'),range='engineering')
addPrefixed(addUnit('rem', '0.01*Sv', 'Rem'),range='engineering')

# Astronomical units
addUnit('Msol', '1.98892e30*kg', 'solar mass')
addUnit('Lsol', '3.839e26*W', 'solar luminosity')
addPrefixed(addUnit('pc', '3.08568025e16*m'),range='engineering')
