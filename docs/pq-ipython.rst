
Back to `Index <Index.ipynb>`__

Using PhysicalQuantities in IPython
===================================

The IPython extension makes using physical quantities easier. To load
the extension use:

.. code:: python

    %load_ext PhysicalQuantities.ipython


.. parsed-literal::

    The PhysicalQuantities.ipython extension is already loaded. To reload it, use:
      %reload_ext PhysicalQuantities.ipython


Now entering a physical quantities gets very easy:

.. code:: python

    d = 2.3 s**3
    t = 3 A
    v = 2.3e3 * d / t

.. code:: python

    print("d = %s" %d)
    print("t = %s" %t)
    print("v = %s" %v)


.. parsed-literal::

    d = 2.3 s^3
    t = 3 A
    v = 1763.3333333333333 s^3/A


Unit conversion
---------------

The easiest way to scale a unit is to use prefix attributes:

.. code:: python

    u = 1 V
    print(u)
    print(u.mV)
    print(u.uV)


.. parsed-literal::

    1 V
    1000.0 mV
    1000000.0 uV


To convert between different representations of a unit, ``to()`` can be
used:

.. code:: python

    a = 1 N * 1 m
    print(a)
    print(a.to('J'))


.. parsed-literal::

    1 N*m
    1.0 J


Using other value types
-----------------------

The ``PhysicalQuantity`` class tries to be a wrapper around the value of
a given quantity, i.e. not only single numbers can be used. For examples
using Numpy arrays, take a look at the `Using Numpy
Arrays <pq-numpy.ipynb>`__ notebook.

.. code:: python

    u = (1 + 1j) * 1V
    print("u = %s" %u)
    u = [1,2,3] * 1V
    print("u = %s" %u)


.. parsed-literal::

    u = (1+1j) V
    u = [1, 2, 3] V


There is limited support for the ``uncertainties`` module. This should
improve in the future.

.. code:: python

    from uncertainties import ufloat


::


    ---------------------------------------------------------------------------

    ImportError                               Traceback (most recent call last)

    <ipython-input-7-caf4a16ea7e8> in <module>()
    ----> 1 from uncertainties import ufloat
    

    ImportError: No module named 'uncertainties'


.. code:: python

    x = ufloat(2, 0.25) * 1 m
    x

.. code:: python

    square = x**2  # Transparent calculations
    square

.. code:: python

    square - x*x

List of all defined Units:
--------------------------

All predefined units can be listed using the ``list()`` or
``html_list()`` function of a unit:

**BUG:** Links for base units are missing

.. code:: python

    import PhysicalQuantities as pq
    pq.units_html_list()

