
Using Decorators to wrap functions
==================================

.. code:: python

    from PhysicalQuantities.decorator import *

Require units in function call
------------------------------

.. code:: python

    @require_units('V', 'A')
    def power(u, i):
        return (u*i).W

.. code:: python

    power(1,1)


::


    ---------------------------------------------------------------------------

    UnitError                                 Traceback (most recent call last)

    <ipython-input-3-bd6d8cb9b6d5> in <module>()
    ----> 1 power(1,1)
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.6.1-py3.4.egg/PhysicalQuantities/decorator.py in wrapper(wrapped, instance, args, kwargs)
         53     def wrapper(wrapped, instance, args, kwargs):
         54         for i, arg in enumerate(args):
    ---> 55             checkbaseunit(arg, units[i])
         56         for i, kwarg in enumerate(kwargs):
         57             checkbaseunit(kwarg, units[i])
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.6.1-py3.4.egg/PhysicalQuantities/decorator.py in checkbaseunit(arg, unit)
         12     """
         13     if not isinstance(arg, PhysicalQuantity):
    ---> 14         raise UnitError('%s is not a PhysicalQuantitiy' % arg)
         15     try:
         16         arg.unit.conversion_tuple_to(unit_table[unit])
    

    UnitError: 1 is not a PhysicalQuantitiy


.. code:: python

    power(1V, 1A)




1.0 :math:`\text{W}`



.. code:: python

    power(1A, 1A)


::


    ---------------------------------------------------------------------------

    UnitError                                 Traceback (most recent call last)

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.6.1-py3.4.egg/PhysicalQuantities/decorator.py in checkbaseunit(arg, unit)
         15     try:
    ---> 16         arg.unit.conversion_tuple_to(unit_table[unit])
         17         return True
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.6.1-py3.4.egg/PhysicalQuantities/Unit.py in conversion_tuple_to(self, other)
        336         if self.powers != other.powers:
    --> 337             raise UnitError('Incompatible units')
        338 
    

    UnitError: Incompatible units

    
    During handling of the above exception, another exception occurred:
    

    UnitError                                 Traceback (most recent call last)

    <ipython-input-5-5e21cfcad74a> in <module>()
    ----> 1 power(PhysicalQuantity(1,'A'), PhysicalQuantity(1,'A'))
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.6.1-py3.4.egg/PhysicalQuantities/decorator.py in wrapper(wrapped, instance, args, kwargs)
         53     def wrapper(wrapped, instance, args, kwargs):
         54         for i, arg in enumerate(args):
    ---> 55             checkbaseunit(arg, units[i])
         56         for i, kwarg in enumerate(kwargs):
         57             checkbaseunit(kwarg, units[i])
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.6.1-py3.4.egg/PhysicalQuantities/decorator.py in checkbaseunit(arg, unit)
         17         return True
         18     except UnitError:
    ---> 19         raise UnitError('%s is not of unit %s' % (arg, unit))
         20 
         21 
    

    UnitError: 1 A is not of unit V


.. code:: python

    @require_units(u='V', i='A')
    def powerkw(u=0V, i=0A):
        return (u*i).W

.. code:: python

    powerkw(u=1V, i=1A)


::


    ---------------------------------------------------------------------------

    IndexError                                Traceback (most recent call last)

    <ipython-input-20-20a0a3217087> in <module>()
    ----> 1 powerkw(u=PhysicalQuantity(1,'V'), i=PhysicalQuantity(1,'A'))
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.6.1-py3.4.egg/PhysicalQuantities/decorator.py in wrapper(wrapped, instance, args, kwargs)
         55             checkbaseunit(arg, units[i])
         56         for i, kwarg in enumerate(kwargs):
    ---> 57             checkbaseunit(kwarg, units[i])
         58         ret = wrapped(*args, **kwargs)
         59         return ret
    

    IndexError: tuple index out of range


Optional units in function call
===============================

.. code:: python

    @optional_units('V', 'A', return_unit='W')
    def powero(u, i):
        return u*i

.. code:: python

    powero(1, 1)




1 :math:`\text{W}`



.. code:: python

    powero(1V, 1A)




1.0 :math:`\text{W}`



.. code:: python

    powero(1V, 1m)


::


    ---------------------------------------------------------------------------

    UnitError                                 Traceback (most recent call last)

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.6.1-py3.4.egg/PhysicalQuantities/decorator.py in dropunit(arg, unit)
         30     try:
    ---> 31         arg.unit.conversion_tuple_to(unit_table[unit])
         32         return arg.base.value
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.6.1-py3.4.egg/PhysicalQuantities/Unit.py in conversion_tuple_to(self, other)
        336         if self.powers != other.powers:
    --> 337             raise UnitError('Incompatible units')
        338 
    

    UnitError: Incompatible units

    
    During handling of the above exception, another exception occurred:
    

    UnitError                                 Traceback (most recent call last)

    <ipython-input-11-4a19eba42854> in <module>()
    ----> 1 powero(PhysicalQuantity(1,'V'), PhysicalQuantity(1,'m'))
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.6.1-py3.4.egg/PhysicalQuantities/decorator.py in wrapper(wrapped, instance, args, kwargs)
         78         newargs = []
         79         for i, arg in enumerate(args):
    ---> 80             newargs.append(dropunit(arg, units[i]))
         81         newkwargs = {}
         82         for i, key in enumerate(kwargs):
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.6.1-py3.4.egg/PhysicalQuantities/decorator.py in dropunit(arg, unit)
         32         return arg.base.value
         33     except UnitError:
    ---> 34         raise UnitError('%s is not of unit %s' % (arg, unit))
         35 
         36 
    

    UnitError: 1 m is not of unit A


.. code:: python

    @optional_units(u='V', i='A')
    def powerokw(u=0, i=0):
        return (u*i).W

.. code:: python

    def a(u=1):
        return b

