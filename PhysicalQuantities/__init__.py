# -*- coding: utf-8 -*-
"""
Physical Quantities for Python and IPython

Usage in Python:
================

    import PhysicalQuantities as pq
    a = pq.PhysicalQuanty(1.0, 'm')
or simply    
    a = pq.Q(1.0, 'm')

The value of a physical quantity can by any number, list or numpy array.
The units are derived from SI base units and can be any combination,
including prefixes:
    a = pq.Q(1.0, 'm**2/s**3')
    
Lists or arrays can also be used and indexed:
    b = [1,2,3]
    c = a*b
    print c[0]    

Usage in IPython:
===============

    %load_ext PyPUnits.ipython
Then you can type directly:
    a = 1 mm
without explicitly calling a function constructor

"""
from __future__ import absolute_import
from .Quantity import *

Q=PhysicalQuantity
U=PhysicalUnit

# Add additional units (SI units are predefined)
addPrefixed(addUnit('Hz', '1/s', 'Hertz', url='https://en.wikipedia.org/wiki/Hertz'),range='engineering')
addPrefixed(addUnit('N', 'm*kg/s**2', 'Newton', url='https://en.wikipedia.org/wiki/Newton_(unit)'),range='engineering')
addPrefixed(addUnit('Pa', 'N/m**2', 'Pascal', url='https://en.wikipedia.org/wiki/Pascal_(unit)'),range='engineering')
addPrefixed(addUnit('J', 'N*m', 'Joule', url='https://en.wikipedia.org/wiki/Joule'),range='engineering')
addPrefixed(addUnit('W', 'J/s', 'Watt', url='https://en.wikipedia.org/wiki/Watt'),range='engineering')
addPrefixed(addUnit('C', 's*A', 'Coulomb', url='https://en.wikipedia.org/wiki/Coulomb'),range='engineering')
addPrefixed(addUnit('V', 'W/A', 'Volt', url='https://en.wikipedia.org/wiki/Volt'),range='engineering')
addPrefixed(addUnit('F', 'C/V', 'Farad', url='https://en.wikipedia.org/wiki/Farad'),range='engineering')
addPrefixed(addUnit('Ohm', 'V/A', 'Ohm', url='https://en.wikipedia.org/wiki/Ohm_(unit)'),range='engineering')
addPrefixed(addUnit('S', 'A/V', 'Siemens', url='https://en.wikipedia.org/wiki/Siemens_(unit)'),range='engineering')
addPrefixed(addUnit('Wb', 'V*s', 'Weber', url='https://en.wikipedia.org/wiki/Weber_(unit)'),range='engineering')
addPrefixed(addUnit('T', 'Wb/m**2', 'Tesla', url='https://en.wikipedia.org/wiki/Tesla_(unit)'),range='engineering')
addPrefixed(addUnit('H', 'Wb/A', 'Henry', url='https://en.wikipedia.org/wiki/Henry_(unit)'),range='engineering')
addPrefixed(addUnit('lm', 'cd*sr', 'Lumen', url='https://en.wikipedia.org/wiki/Lumen_(unit)'),range='engineering')
addPrefixed(addUnit('lx', 'lm/m**2', 'Lux', url='https://en.wikipedia.org/wiki/Lux'),range='engineering')

# Angle units
unit_table['pi'] = pi #np.pi
addUnit('deg', 'pi*rad/180', 'Degree', url='http://en.wikipedia.org/wiki/Degree_%28angle%29')
addUnit('arcmin', 'pi*rad/180/60', 'minutes of arc')
addUnit('arcsec', 'pi*rad/180/3600', 'seconds of arc')

# Time
addUnit('minutes', '60*s', 'Minute', url='https://en.wikipedia.org/wiki/Hour')
addUnit('hours', '60*60*s', 'Hour', url='https://en.wikipedia.org/wiki/Hour')

# numpy linspace wrapper for units
def linspace(start, stop, num = 50,  endpoint=True, retstep=False):
    """ numpy.linespace with units
    
    """
    if not isinstance(start,PhysicalQuantity) and not isinstance(stop,PhysicalQuantity):
        return np.linspace(start, stop, num,  endpoint, retstep)

    if isinstance(start,PhysicalQuantity) and isinstance(stop,PhysicalQuantity):
        if start.base.unit != stop.base.unit:
            raise UnitError("Cannot match units")
    
    if isinstance(start,PhysicalQuantity):
        start_value = start.value
        unit = start.unit
    else:
        start_value = start

    if isinstance(stop,PhysicalQuantity):
        stop_value = stop.value
        unit = stop.unit
    else:
        stop_value = stop

    array = np.linspace(start_value, stop_value, num,  endpoint, retstep)

    if retstep:
        return PhysicalQuantity(array[0], unit), PhysicalQuantity(array[1], unit)
    else:
        return array * PhysicalQuantity(1, unit)
