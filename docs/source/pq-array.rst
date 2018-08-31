
PhysicalQuantitiesArray
=======================

.. code:: ipython3

    from PhysicalQuantities import q, QA
    import numpy as np

.. code:: ipython3

    a = QA(np.random.rand(10), 'm')
    b = QA(np.random.rand(10), 's')

.. code:: ipython3

    a




.. parsed-literal::

    PhysicalQuantityArray([0.38290499 0.0446361  0.69727907 0.73542758 0.32310051 0.08882622
     0.54634225 0.1663809  0.44703685 0.58633038], unit=m)



.. code:: ipython3

    a+a




.. parsed-literal::

    PhysicalQuantityArray([0.76580998 0.08927219 1.39455814 1.47085516 0.64620102 0.17765243
     1.09268451 0.3327618  0.8940737  1.17266076], unit=m)



.. code:: ipython3

    a+b


::


    ---------------------------------------------------------------------------

    UnitError                                 Traceback (most recent call last)

    <ipython-input-5-ca730b97bf8a> in <module>()
    ----> 1 a+b
    

    ~/git/PhysicalQuantities/PhysicalQuantities/quantityarray.py in __array_ufunc__(self, ufunc, method, *inputs, **kwargs)
         37             par1, par2 = inputs
         38             if isinstance(par2, PhysicalQuantityArray):
    ---> 39                 if par2.unit != self.unit:
         40                     raise ValueError('Incompatible units.')
         41                 args.append(par2.view(np.ndarray))


    ~/git/PhysicalQuantities/PhysicalQuantities/unit.py in __eq__(self, other)
        430         if isphysicalunit(other) and self.powers == other.powers:
        431             return self.factor == other.factor
    --> 432         raise UnitError('Cannot compare different dimensions %s and %s' % (self, other))
        433 
        434     def __mul__(self, other):


    UnitError: Cannot compare different dimensions s and m


.. code:: ipython3

    a/b




.. parsed-literal::

    PhysicalQuantityArray([ 0.41969088  0.05174994  1.31479216  0.74886358  5.32995917  0.12869864
     12.99434469  0.7032714   0.53587343  1.39371093], unit=m/s)



.. code:: ipython3

    a*b




.. parsed-literal::

    PhysicalQuantityArray([0.34934338 0.03850016 0.36979084 0.72223264 0.01958625 0.06130676
     0.02297075 0.03936262 0.37292751 0.24666759], unit=m*s)



.. code:: ipython3

    a.mm




.. parsed-literal::

    PhysicalQuantityArray([382.90499068  44.63609551 697.27906957 735.42757919 323.10050788
      88.82621671 546.34225407 166.38090045 447.03685138 586.33038064], unit=mm)



.. code:: ipython3

    a.km_




.. parsed-literal::

    array([3.82904991e-04, 4.46360955e-05, 6.97279070e-04, 7.35427579e-04,
           3.23100508e-04, 8.88262167e-05, 5.46342254e-04, 1.66380900e-04,
           4.47036851e-04, 5.86330381e-04])


