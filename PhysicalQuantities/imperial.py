# -*- coding: utf-8 -*-
""" Define additional units
"""
from .Unit import addunit
from .constants import *

# Length units
addunit('inch', '2.54*cm', 'inch')
addunit('ft', '12*inch', 'foot')
addunit('yd', '3*ft', 'yard')
addunit('mi', '5280.*ft', '(British) mile')
addunit('nmi', '1852.*m', 'Nautical mile')
addunit('furlong', '201.168*m', 'furlongs')

# Area units
addunit('acres', 'mi**2/640', 'acre')
addunit('b', '1.e-28*m', 'barn')

# Volume units
addunit('tsp', '4.92892159375*cm**3', 'teaspoon')
addunit('tbsp', '3*tsp', 'tablespoon')
addunit('floz', '2*tbsp', 'fluid ounce')
addunit('cup', '8*floz', 'cup')
addunit('pt', '16*floz', 'pint')
addunit('qt', '2*pt', 'quart')
addunit('galUS', '4*qt', 'US gallon')
addunit('galUK', '4.54609*1000*cm**3', 'British gallon')

# Mass units
addunit('oz', '28.349523125*g', 'ounce')
addunit('lb', '16*oz', 'pound')
addunit('ton', '2000*lb', 'US ton')


# Energy units
addunit('Btu', '1055.05585262*J', 'British thermal unit')

# Power units
addunit('hp', '745.7*W', 'horsepower')

# Pressure units
addunit('psi', '6894.75729317*Pa', 'pounds per square inch')

addunit('degF', PhysicalUnit(None,   5./9,    [0, 0, 0, 0, 1, 0, 0, 0, 0], offset=459.67), comment='degree Fahrenheit')
