""" Define imperial units
"""
import PhysicalQuantities

from .unit import add_composite_unit

# Length units
add_composite_unit('inch', 2.54, 'cm', verbosename='inch',
                   url='https://en.wikipedia.org/wiki/Inch')
add_composite_unit('mil', 1 / 1000, 'inch', verbosename='foot',
                   url='https://en.wikipedia.org/wiki/Thousandth_of_an_inch')
add_composite_unit('ft', 12, 'inch', verbosename='foot',
                   url='https://en.wikipedia.org/wiki/Foot_(unit)')
add_composite_unit('yd', 3, 'ft', verbosename='yard',
                   url='https://en.wikipedia.org/wiki/Yard')
add_composite_unit('mi', 5280, 'ft', verbosename='(British) mile',
                   url='https://en.wikipedia.org/wiki/Mile#British_and_Irish_miles')
add_composite_unit('nmi', 1852, 'm', verbosename='Nautical mile',
                   url='https://en.wikipedia.org/wiki/Nautical_mile')
add_composite_unit('furlong', 201.168, 'm', verbosename='furlongs',
                   url='https://en.wikipedia.org/wiki/Furlong')

# Area units
add_composite_unit('acres', 4046.8564224, 'm**2', verbosename='acre',
                   url='https://en.wikipedia.org/wiki/Acre)')
add_composite_unit('barn', 1.e-28, 'm', verbosename='barn',
                   url='https://en.wikipedia.org/wiki/Barn_(unit)')

# Volume units
add_composite_unit('tsp', 4.92892159375, 'cm**3', verbosename='teaspoon',
                   url='https://en.wikipedia.org/wiki/Teaspoon')
add_composite_unit('tbsp', 3, 'tsp', verbosename='tablespoon',
                   url='https://en.wikipedia.org/wiki/Tablespoon')
add_composite_unit('floz', 2, 'tbsp', verbosename='fluid ounce',
                   url='https://en.wikipedia.org/wiki/Fluid_ounce')
add_composite_unit('cup', 8, 'floz', verbosename='cup',
                   url='https://en.wikipedia.org/wiki/Cup')
add_composite_unit('pt', 16, 'floz', verbosename='pint',
                   url='https://en.wikipedia.org/wiki/Pint')
add_composite_unit('qt', 2, 'pt', verbosename='quart',
                   url='https://en.wikipedia.org/wiki/Quart')
add_composite_unit('galUS', 4, 'qt', verbosename='US gallon',
                   url='https://en.wikipedia.org/wiki/Gallon')
add_composite_unit('galUK', 4.54609 * 1000, 'cm**3', verbosename='British gallon',
                   url='https://en.wikipedia.org/wiki/Gallon')

# Mass units
add_composite_unit('oz', 28.349523125, 'g', verbosename='ounce',
                   url='https://en.wikipedia.org/wiki/Ounce')
add_composite_unit('lb', 16, 'oz', verbosename='pound',
                   url='https://en.wikipedia.org/wiki/Pound_(mass)')
add_composite_unit('ton', 2000, 'lb', verbosename='US ton',
                   url='https://en.wikipedia.org/wiki/Pound_(mass)')

# Energy units
add_composite_unit('Btu', 1055.05585262, 'J', verbosename='British thermal unit')

# Power units
add_composite_unit('hp', 745.7, 'W', verbosename='horsepower',
                   url='https://en.wikipedia.org/wiki/Horsepower')

# Pressure units
add_composite_unit('psi', 6894.75729317, 'Pa', verbosename='pounds per square inch',
                   url='https://en.wikipedia.org/wiki/Pounds_per_square_inch')

add_composite_unit('degF', 5/9, 'K', offset=459.67,
                   verbosename='degree Fahrenheit',
                   url='https://en.wikipedia.org/wiki/Fahrenheit')

PhysicalQuantities.q.__init__()
