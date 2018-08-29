.. image:: https://readthedocs.org/projects/physicalquantities/badge/?version=latest
   :target: http://physicalquantities.readthedocs.io/en/latest/
   :alt: Documentation Status

.. image:: https://codecov.io/gh/juhasch/PhysicalQuantities/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/juhasch/PhysicalQuantities

.. image:: https://badge.fury.io/py/physicalquantities.svg
    :target: https://badge.fury.io/py/physicalquantities

.. image:: https://travis-ci.org/juhasch/PhysicalQuantities.svg
    :target: https://travis-ci.org/juhasch/PhysicalQuantities


=====================================================
 PhysicalQuantites - Calculation in Python with Units
=====================================================

Overview
========

PhysicalQuantities is a module for Python 3.6 that allows calculations to be aware 
of physical units with a focus on engineering applications. 
Built-in unit conversion ensures that calculations will result in the correct aggregate 
unit.

The module also contains an extension for IPython. This allows greatly simplified use by typing in physical quantities
directly as number and unit.

Examples
--------

::

    In [1]: %load_ext PhysicalQuantities.ipython
    In [2]: a = 100mm
    In [3]: a
    Out[3]: 100 mm

    In [4]: a.cm
    Out[5]: 10.0 cm

    In [5]: a = 10_000_000 nm
    In [6]: a.autoscale
    Out[6]: 1.0 cm

    In [7]: a = 10 m/s
    In [8]: 5s * a
    Out[8]: 50 m


dB calculations are supported, too:

::

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

Additional units, e.g. imperial units:

::

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

Using PhysicalQuantities in plain Python:

::

    >>> from PhysicalQuantities import q
    >>> 1 * q.mm
    1 mm
    >>> 1 * q.dBm
    1 dBm
    >>>


Installation
------------
This module requires Python 3.6 or above. This is due to the use of new features like `f` strings
or supporting underscores in numeric literals.

To install, simply do a

    pip install PhysicalQuantities

There also is a conda receive, so you can do

    conda build

to generate a conda package. I will upload a receipe to conda-forge at a later time.

Note
----
This module is originally based on the IPython extension by Georg Brandl at
https://bitbucket.org/birkenfeld/ipython-physics.

