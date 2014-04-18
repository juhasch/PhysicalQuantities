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
addUnit('inch', '2.54*cm', 'inch')
addUnit('ft', '12*inch', 'foot')
addUnit('yd', '3*ft', 'yard')
addUnit('mi', '5280.*ft', '(British) mile')
addUnit('nmi', '1852.*m', 'Nautical mile')
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
addUnit('l', 'dm**3', 'liter')
addUnit('dl', '0.1*l', 'deci liter')
addUnit('cl', '0.01*l', 'centi liter')
addUnit('ml', '0.001*l', 'milli liter')
addUnit('mul', '0.000001*l', 'micro liter')
addUnit('tsp', '4.92892159375*ml', 'teaspoon')
addUnit('tbsp', '3*tsp', 'tablespoon')
addUnit('floz', '2*tbsp', 'fluid ounce')
addUnit('cup', '8*floz', 'cup')
addUnit('pt', '16*floz', 'pint')
addUnit('qt', '2*pt', 'quart')
addUnit('galUS', '4*qt', 'US gallon')
addUnit('galUK', '4.54609*l', 'British gallon')

# Mass units
addUnit('t', '1000*kg', 'Metric ton')
addUnit('amu', '1.660538921e-27*kg', 'atomic mass units')
addUnit('Da', '1*amu', 'Dalton')
addUnit('oz', '28.349523125*g', 'ounce')
addUnit('lb', '16*oz', 'pound')
addUnit('ton', '2000*lb', 'US ton')

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
addUnit('Btu', '1055.05585262*J', 'British thermal unit')


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
addUnit('psi', '6894.75729317*Pa', 'pounds per square inch')

# Angle units
addUnit('deg', 'pi*rad/180', 'degrees')
addUnit('arcmin', 'pi*rad/180/60', 'minutes of arc')
addUnit('arcsec', 'pi*rad/180/3600', 'seconds of arc')
#_unit_table['cycles'] = 2*np.pi

# Temperature units -- can't use the 'eval' trick that _addUnit provides
# for degC and degF because you can't add units
#kelvin = _findUnit('K')
addUnit('degR', '(5./9.)*K', 'degrees Rankine')
addUnit('degC', PhysicalUnit(None, 1.0, kelvin.powers, 273.15),
         'degrees Celcius')
addUnit('degF', PhysicalUnit(None, 5./9., kelvin.powers, 459.67),
         'degree Fahrenheit')
#del kelvin

# Radiation-related units
addPrefixed(addUnit('Ci', '3.7e10*Bq', 'Curie'),range='engineering')
addPrefixed(addUnit('rem', '0.01*Sv', 'Rem'),range='engineering')

# Astronomical units
addUnit('Msol', '1.98892e30*kg', 'solar mass')
addUnit('Lsol', '3.839e26*W', 'solar luminosity')
addPrefixed(addUnit('pc', '3.08568025e16*m'),range='engineering')
