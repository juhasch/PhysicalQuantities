
PhysicalQuantities and Numpy
============================

Units can be mixed with numpy arrays:

.. code:: python

    t = np.arange(10) * 1 s
    print(t)


.. parsed-literal::

    [0 1 2 3 4 5 6 7 8 9] s


Array indexing and slicing is supported:

.. code:: python

    print(t[1:4])
    a = np.random.rand(3,4) * 1 m
    print(a)
    print(a[2][3])


.. parsed-literal::

    [1 2 3] s
    [[ 0.00651857  0.26930867  0.58597492  0.93524793]
     [ 0.05795865  0.99960178  0.82773778  0.52771415]
     [ 0.52239363  0.23701236  0.67595263  0.30514639]] m
    0.30514638981968711 m


Assignment of array elements is supported:

.. code:: python

    a = np.linspace(0,10,10) * 1m
    a[0] = 3 m
    print(a)


.. parsed-literal::

    [  3.     1.11   2.22   3.33   4.44   5.56   6.67   7.78   8.89  10.  ] m


Pretty printing Numpy arrays can be achieved using ``set_printoptions``

.. code:: python

    np.set_printoptions(precision=2)
    print(a)


.. parsed-literal::

    [[ 0.01  0.27  0.59  0.94]
     [ 0.06  1.    0.83  0.53]
     [ 0.52  0.24  0.68  0.31]] m


Prefixing units is also possible like for single values:

.. code:: python

    print(t.ms)
    print(t.ms_)


.. parsed-literal::

    [    0.  1000.  2000.  3000.  4000.  5000.  6000.  7000.  8000.  9000.] ms
    [    0.  1000.  2000.  3000.  4000.  5000.  6000.  7000.  8000.  9000.]


A more practical example:

.. code:: python

    t = linspace(0,10, 10) * 1 ms
    f = 100 Hz
    u = np.sin(2*np.pi*f*t) * 1 V
    t,u




.. parsed-literal::

    ([  0.     1.11   2.22   3.33   4.44   5.56   6.67   7.78   8.89  10.  ] ms,
     [  0.00e+00   6.43e-01   9.85e-01   8.66e-01   3.42e-01  -3.42e-01
       -8.66e-01  -9.85e-01  -6.43e-01   6.43e-16] V)



.. code:: python

    plt.plot(t.ms_,u.V_);



.. image:: pq-numpy_files/pq-numpy_13_0.png


A helper function ``PhysicalQuantities.linspace`` simplifies specifying
ranges:

.. code:: python

    t = pq.linspace(0, 10ms, 11)
    print(t)


.. parsed-literal::

    [  0.   1.   2.   3.   4.   5.   6.   7.   8.   9.  10.] ms


.. code:: python

    plot(t.ms_)




.. parsed-literal::

    [<matplotlib.lines.Line2D at 0x7e2bc50>]




.. image:: pq-numpy_files/pq-numpy_16_1.png


