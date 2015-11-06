.. PhysicalQuantities documentation master file, created by
   sphinx-quickstart on Thu Sep 10 21:52:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PhysicalQuantities's documentation!
==============================================

PhysicalQuantities is a Python module that allows calculations to be aware of physical units.
Built-in unit conversion ensures that calculations will result in the correct aggregate unit.

This package was developed to be used in engineering applications, providing easy handling of numbers with units.

The module also contains an extension for IPython. This allows greatly simplified use by typing in physical quantities
directly as number and unit.

The documentation is contained in IPython notebooks:
http://nbviewer.ipython.org/github/juhasch/PhysicalQuantities/blob/master/examples/Index.ipynb

This module is originally based on the IPython extension by Georg Brandl:
https://bitbucket.org/birkenfeld/ipython-physics.
It was converted into a standalone Python module and extended heavily.


User Guide:

.. toctree::
    :maxdepth: 2

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

Reference:

.. toctree::
    :maxdepth: 2

    constants
    Quantity
    Unit

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

