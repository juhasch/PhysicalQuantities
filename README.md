[![Documentation Status](https://readthedocs.org/projects/physicalquantities/badge/?version=latest)](http://physicalquantities.readthedocs.io/en/latest/?badge=latest)

PhysicalQuantities is a python module that allows calculations to be aware 
of physical units with a focus on engineering applications. 
Built-in unit conversion ensures that calculations will result in the correct aggregate unit.

The module also contains an extension for IPython. This allows greatly simplified use by typing in physical quantities
directly as number and unit.

```
In [1]: a = 100mm

In [2]: a
Out[2]: 100 mm

In [3]: a.cm
Out[3]: 10.0 cm

In [4]: a = 10_000_000 nm

In [5]: a.autoscale
Out[5]: 1.0 cm

In [6]: g = 9.81 m/s

In [7]: g
Out[7]: 9.81 m/s
```

dB calculations are supported, too:

```
In [1]: u = 10V

In [2]: u.dB
Out[2]: 20.0 dBV

In [3]: p = 10 dBm

In [4]: p
Out[4]: 10 dBm

In [5]: p.W
Out[5]: 0.01 W

In [6]: p.mW
Out[6]: 10.0 mW
```

Additional units, e.g. imperial units:

```
In [1]: %precision 2
Out[1]: '%.2f'

In [2]: import  PhysicalQuantities.imperial

In [3]: a = 2 inch

In [4]: a
Out[4]: 2 inch

In [5]: a.mil
Out[5]: 2000.00 mil

In [6]: a.mm
Out[6]: 50.80 mm
```


This module is originally based on the IPython extension by Georg Brandl 
(<https://bitbucket.org/birkenfeld/ipython-physics>). It was heavily extended to improve the
ease of use.

