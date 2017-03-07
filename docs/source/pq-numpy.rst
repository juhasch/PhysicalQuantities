
PhysicalQuantities and Numpy
============================

Units can be mixed with numpy arrays. There is a helper module for this
called ``numpywrapper``:

.. code:: python

    >>> import PhysicalQuantities.numpywrapper as nw
    >>> t = np.arange(10) * 1 s
    >>> print(t)
    [0 1 2 3 4 5 6 7 8 9] s

Array indexing and slicing is supported:

.. code:: python

    >>> print(t[1:4])
    [1 2 3] s
    >>> a = np.random.rand(3,4) * 1 m
    >>> print(a)
    [[ 0.59994977  0.65224855  0.7659288   0.72208264]
     [ 0.39490532  0.05471093  0.96338392  0.15117082]
     [ 0.67440078  0.02391973  0.0248514   0.45410086]] m
    >>> print(a[2][3])
    0.45410086453921439 m

Assignment of array elements is supported:

.. code:: python

    >>> a = nw.linspace(0, 10m, 10)
    >>> a[0] = 3 m
    >>> print(a)
    [  3.           1.11111111   2.22222222   3.33333333   4.44444444
       5.55555556   6.66666667   7.77777778   8.88888889  10.        ] m

Pretty printing Numpy arrays can be achieved using ``set_printoptions``

.. code:: python

    >>> np.set_printoptions(precision=2)
    >>> print(a)
    [  3.     1.11   2.22   3.33   4.44   5.56   6.67   7.78   8.89  10.  ] m

Prefixing units is also possible like for single values:

.. code:: python

    >>> print(t.ms)
    >>> print(t.ms_)
    [    0.  1000.  2000.  3000.  4000.  5000.  6000.  7000.  8000.  9000.] ms
    [    0.  1000.  2000.  3000.  4000.  5000.  6000.  7000.  8000.  9000.]

A more practical example:

.. code:: python

    >>> t = nw.linspace(0, 10ms, 10)
    >>> f = 100 Hz
    >>> u = np.sin(2*np.pi*f*t) * 1 V
    >>> t,u
    ([  0.     1.11   2.22   3.33   4.44   5.56   6.67   7.78   8.89  10.  ] ms,
     [  0.00e+00   6.43e-01   9.85e-01   8.66e-01   3.42e-01  -3.42e-01
       -8.66e-01  -9.85e-01  -6.43e-01   6.43e-16] V)


.. code:: python

    >>> plot(t.us_,u.V_);



Or simply using the current unit prefix:

.. code:: python

    >>> plot(t._,u._);




