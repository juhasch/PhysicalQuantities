# -*- coding: utf-8 -*-
# Define additional units
from .Unit import *
from .constants import *

# Length units
addUnit('inch', '2.54*cm', 'inch')
addUnit('ft', '12*inch', 'foot')
addUnit('yd', '3*ft', 'yard')
addUnit('mi', '5280.*ft', '(British) mile')
addUnit('nmi', '1852.*m', 'Nautical mile')
addUnit('furlong', '201.168*m', 'furlongs')

# Area units
addUnit('acres', 'mi**2/640', 'acre')
addUnit('b', '1.e-28*m', 'barn')

# Volume units
addUnit('tsp', '4.92892159375*cm**3', 'teaspoon')
addUnit('tbsp', '3*tsp', 'tablespoon')
addUnit('floz', '2*tbsp', 'fluid ounce')
addUnit('cup', '8*floz', 'cup')
addUnit('pt', '16*floz', 'pint')
addUnit('qt', '2*pt', 'quart')
addUnit('galUS', '4*qt', 'US gallon')
addUnit('galUK', '4.54609*1000*cm**3', 'British gallon')

# Mass units
addUnit('oz', '28.349523125*g', 'ounce')
addUnit('lb', '16*oz', 'pound')
addUnit('ton', '2000*lb', 'US ton')


# Energy units
addUnit('Btu', '1055.05585262*J', 'British thermal unit')

# Power units
addUnit('hp', '745.7*W', 'horsepower')

# Pressure units
addUnit('psi', '6894.75729317*Pa', 'pounds per square inch')

addUnit('degF', PhysicalUnit(None,   5./9,    [0, 0, 0, 0, 1, 0, 0, 0, 0], offset=459.67), comment='degree Fahrenheit')

#addUnit('degF', PhysicalUnit(None, 5./9., kelvin.powers, 459.67),
#         'degree Fahrenheit')
