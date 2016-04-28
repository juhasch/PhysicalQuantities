Back to `Index <Index.html>`__

Introduction
============

PhysicalQuantities is a python module that allows calculations to be
aware of physical units. Built-in unit conversion ensures that
calculations will result in the correct unit.

The module also contains an extension for IPython. This allows much
simplified usage by typing in physical quantities as number and unit:

.. code:: python

    a = 1m ; b = 1s
    print("a=", a, ", b=",b,", a/b=", a/b)


.. parsed-literal::

    a= 1 m , b= 1 s , a/b= 1.0 m/s


The Github repository for this module can be found here:
https://github.com/juhasch/PhysicalQuantities

This module is based on the IPython extension by Georg Brandl:
https://bitbucket.org/birkenfeld/ipython-physics. It was converted into
a standalone Python module and extended heavily to be as flexible as
possible.

Example Notebooks
-----------------

-  `Basics and Installation <pq-basics.ipynb>`__
-  `Using Physical Quantities in IPython <pq-ipython.ipynb>`__
-  `Output Formatting <pq-formatting.ipynb>`__
-  `Doing dB Calculations <pq-dbquantity.ipynb>`__
-  `Using Numpy Arrays <pq-numpy.ipynb>`__
-  `Autoscaling <pq-autoscale.ipynb>`__
-  `SymPy <pq-sympy.ipynb>`__
-  `Uncertainties <pq-uncertainties.ipynb>`__
-  `Practical Example - Calculate a RC Circuit <pq-example.ipynb>`__

