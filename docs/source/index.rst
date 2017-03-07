.. PhysicalQuantities documentation master file, created by

PhysicalQuantities Documentation
================================

*PhysicalQuantities* is a Python module that allows calculations to be aware of physical units. Built-in unit
conversion ensures that calculations will result in the correct unit.

The module also contains an extension for IPython. This allows much simplified usage by typing in physical quantities
as number and unit:

.. code::

    >>> a = 1m ; b = 1s
    >>> print("a=", a, ", b=",b,", a/b=", a/b)
    a= 1 m , b= 1 s , a/b= 1.0 m/s

The Github repository for this module can be found here:

    https://github.com/juhasch/PhysicalQuantities

This module is based on the IPython extension by Georg Brandl. It was converted into a standalone Python module and
extended heavily to be as flexible as possible. The original extension can be found here:

    https://bitbucket.org/birkenfeld/ipython-physics

User Guide
----------

.. toctree::
    :maxdepth: 1

    pq-basics
    pq-q-units
    pq-ipython
    pq-autoscale
    pq-dbquantity
    pq-formatting
    pq-numpy
    pq-sympy
    pq-uncertainties
    pq-imperial
    pq-decorators
    pq-example

Reference
---------

.. toctree::
    :maxdepth: 1

    Quantity
    Unit
    constants
    pq-numpywrapper

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

