"""Add binary units, i.e. Bits

Example
-------

In [5]: 1 Bit
Out[5]: 1 Bit

In [6]: 1 KiBit
Out[6]: 1 KiBit

In [7]: 100 KiBit  + 1 MiBit
Out[7]: 1124.0 KiBit

"""
import PhysicalQuantities

from .unit import add_composite_unit

add_composite_unit('Byte', 8, 'Bit', verbosename='Byte', prefixed=True, baseunit=PhysicalQuantities.q.Bit,
                   url='https://en.wikipedia.org/wiki/Byte')
PhysicalQuantities.q.__init__()


_units = {'Ki': 2 ** 10,
          'Mi': 2 ** 20,
          'Gi': 2 ** 30,
          'Ti': 2 ** 40,
          'Pi': 2 ** 50,
          'Ei': 2 ** 60,
          'Zi': 2 ** 70,
          'Yi': 2 ** 80,
          }

for key in _units.keys():
    name = key + 'Bit'
    scale = _units[key]
    add_composite_unit(name, scale, 'Bit', verbosename=name, prefixed=True, baseunit=PhysicalQuantities.q.Bit,
                       url='https://en.wikipedia.org/wiki/Bit')

    name = key + 'Byte'
    scale = _units[key]
    add_composite_unit(name, scale, 'Byte', verbosename=name, prefixed=True, baseunit=PhysicalQuantities.q.Byte,
                       url='https://en.wikipedia.org/wiki/Byte')


PhysicalQuantities.q.__init__()
