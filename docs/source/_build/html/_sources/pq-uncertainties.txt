
Working with Uncertainties
==========================

This is still work in progress.

.. code:: python

    from uncertainties import ufloat


::


    ---------------------------------------------------------------------------

    ImportError                               Traceback (most recent call last)

    <ipython-input-1-caf4a16ea7e8> in <module>()
    ----> 1 from uncertainties import ufloat
    

    ImportError: No module named 'uncertainties'


.. code:: python

    x = ufloat(2, 0.25) * 1 m
    x




.. math::

    2.00+/-0.25 $m



.. code:: python

    square = x**2  # Transparent calculations
    square




.. math::

    4.0+/-1.0 $m^2



.. code:: python

    square - x*x




.. math::

    0.0+/-0 $m^2



.. code:: python

    from uncertainties.umath import *  # sin(), etc.
    x = ufloat(2, 0.25) * 35 deg
    #x = 35 deg
    #sin(x)
    #x

.. code:: python

    x = ufloat(2, 0.25) * 1 m
    #d = (2*x).derivatives[x]  # Automatic calculation of derivatives
    #print(d)

.. code:: python

    from uncertainties import unumpy  # Array manipulation
    random_vars = unumpy.uarray([1, 2], [0.1, 0.2]) * 1 s
    print(random_vars)


.. parsed-literal::

    [1.0+/-0.1 2.0+/-0.2] s


.. code:: python

    print(random_vars.s_.mean())


.. parsed-literal::

    1.50+/-0.11


