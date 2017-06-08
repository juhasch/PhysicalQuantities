""" Define additional units
"""
from .Unit import PhysicalUnit, addunit
from PhysicalQuantities.ipython import load_ipython_extension, unload_ipython_extension

# Length units
addunit('inch', '2.54*cm', verbosename='inch', url='https://en.wikipedia.org/wiki/Inch')
addunit('mil', 'inch/1000', verbosename='foot', url='https://en.wikipedia.org/wiki/Thousandth_of_an_inch')
addunit('ft', '12*inch', verbosename='foot', url='https://en.wikipedia.org/wiki/Foot_(unit)')
addunit('yd', '3*ft', verbosename='yard', url='https://en.wikipedia.org/wiki/Yard')
addunit('mi', '5280.*ft', verbosename='(British) mile')
addunit('nmi', '1852.*m', verbosename='Nautical mile')
addunit('furlong', '201.168*m', verbosename='furlongs')

# Area units
addunit('acres', 'mi**2/640', verbosename='acre')
addunit('barn', '1.e-28*m', verbosename='barn')

# Volume units
addunit('tsp', '4.92892159375*cm**3', verbosename='teaspoon')
addunit('tbsp', '3*tsp', verbosename='tablespoon')
addunit('floz', '2*tbsp', verbosename='fluid ounce')
addunit('cup', '8*floz', verbosename='cup')
addunit('pt', '16*floz', verbosename='pint')
addunit('qt', '2*pt', verbosename='quart')
addunit('galUS', '4*qt', verbosename='US gallon')
addunit('galUK', '4.54609*1000*cm**3', verbosename='British gallon')

# Mass units
addunit('oz', '28.349523125*g', verbosename='ounce', url='https://en.wikipedia.org/wiki/Ounce')
addunit('lb', '16*oz', verbosename='pound')
addunit('ton', '2000*lb', verbosename='US ton')


# Energy units
addunit('Btu', '1055.05585262*J', verbosename='British thermal unit')

# Power units
addunit('hp', '745.7*W', verbosename='horsepower')

# Pressure units
addunit('psi', '6894.75729317*Pa', verbosename='pounds per square inch')

addunit('degF', PhysicalUnit('K', 5./9, [0, 0, 0, 0, 1, 0, 0, 0, 0], offset=459.67), verbosename='degree Fahrenheit',
        url='https://en.wikipedia.org/wiki/Fahrenheit')

# Reload transformer in IPython
try:
    ip = get_ipython()
    if 'PhysicalQuantity' in ip.user_ns:
        unload_ipython_extension(ip)
        load_ipython_extension(ip)
except:
    pass
