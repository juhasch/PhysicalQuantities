[![Documentation Status](https://readthedocs.org/projects/physicalquantities/badge/?version=latest)](http://physicalquantities.readthedocs.io/en/latest/?badge=latest)

PhysicalQuantities is a python module that allows calculations to be aware of physical units. 
Built-in unit conversion ensures that calculations will result in the correct aggregate unit.

The module also contains an extension for IPython. This allows greatly simplified use by typing in physical quantities
directly as number and unit.

```
>>> a = 10m ; b = 2s
>>> print("a=", a, ", b=",b,", a/b=", a//b)
a= 10 m , b= 2 s , a/b= 5 m/s
```

dB calculations are supported, too:

```
>>> p = 200mW
>>> p.dB
23.010299956639813 dBm
```

This module is originally based on the IPython extension by Georg Brandl 
(<https://bitbucket.org/birkenfeld/ipython-physics>). It was heavily extended to improve the
ease of use.

