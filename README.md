[![Documentation Status](https://readthedocs.org/projects/physicalquantities/badge/?version=latest)](http://physicalquantities.readthedocs.io/en/latest/?badge=latest)

PhysicalQuantities is a python module that allows calculations to be aware 
of physical units with a focus on engineering applications. 
Built-in unit conversion ensures that calculations will result in the correct aggregate unit.

The module also contains an extension for IPython. This allows greatly simplified use by typing in physical quantities
directly as number and associated unit.

There are a number of implementations to allow using physical units in Python. This one
focuses on the ease of use, especially for interactive work in IPython and the Jupyter notebook.

```
In [1]: %load_ext PhysicalQuantities.ipython

In [2]: a = 100mm

In [3]: a
Out[3]: 100 mm

In [4]: a.cm
Out[4]: 10.0 cm

In [5]: a = 10_000_000 nm

In [6]: a.autoscale
Out[6]: 1.0 cm

In [7]: g = 9.81 m/s

In [8]: g
Out[8]: 9.81 m/s
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

In [2]: import PhysicalQuantities.imperial

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

For a discussion on the difficulties and pitfalls of implementing phyiscial units support
in Python, the talk from SciPy 2017 'MetPy’s Choice of Unit Support: A Descent into Madness'
by Ryan May and John Leeman is quite instructive.
