
Back to `Index <index.ipynb>`__

PhysicalQuantities - dBUnits
============================

The IPython extension for dB units is loaded using:

.. code:: python

    %reload_ext PhysicalQuantities.dBQuantity_ipython

It provides an easy way to do dB calculations:

.. code:: python

    p = 0 dBm
    print(p)
    print(p.dBW)
    print(p.W)


.. parsed-literal::

    0 dBm
    -30.0 dBW
    0.001 W


.. code:: python

    g = 3 dB
    print (p+g)


.. parsed-literal::

    3 dBm


.. code:: python

    print(p.dBW)
    print(p.dBW_)


.. parsed-literal::

    -30.0 dBW
    -30.0


.. code:: python

    from PhysicalQuantities.dBQuantity import dBQuantity

.. code:: python

    a = dBQuantity(0.1,'dBm', islog=True)
    print(a)


.. parsed-literal::

    0.1 dBm


.. code:: python

    a.value, a.unit




.. parsed-literal::

    (0.1, 'dBm')



.. code:: python

    a.W




0.0010232929922807542 :math:`\text{W}`



.. code:: python

    %precision 2
    a.mW




1.02 :math:`\text{mW}`



Helper function to generate dB values from a linear value:

.. code:: python

    from PhysicalQuantities.dBQuantity import dB, dB10, dB20
    dB(1 mW)




.. parsed-literal::

    0.00 dBm



.. code:: python

    dB10(10)




.. parsed-literal::

    10.00 dB



.. code:: python

    dB20(10)




.. parsed-literal::

    20.00 dB



