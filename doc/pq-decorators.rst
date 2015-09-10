
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

    <ipython-input-50-bd6d8cb9b6d5> in <module>()
    ----> 1 power(1,1)
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.4-py3.4.egg/PhysicalQuantities/decorator.py in wrapper(wrapped, instance, args, kwargs)
         42     def wrapper(wrapped, instance, args, kwargs):
         43         for i, arg in enumerate(args):
    ---> 44             checkbaseunit(arg, units[i])
         45         for i, kwarg in enumerate(kwargs):
         46             checkbaseunit(kwarg, units[i])


    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.4-py3.4.egg/PhysicalQuantities/decorator.py in checkbaseunit(arg, unit)
         12     """
         13     if not isinstance(arg, PhysicalQuantity):
    ---> 14         raise UnitError('%s is not a PhysicalQuantitiy' % arg)
         15     try:
         16         arg.unit.conversion_tuple_to(unit_table[unit])


    UnitError: 1 is not a PhysicalQuantitiy


.. code:: python

    power(1V, 1A)




.. math::

    1.0 $\text{W}



.. code:: python

    power(1A, 1A)


::


    ---------------------------------------------------------------------------

    UnitError                                 Traceback (most recent call last)

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.4-py3.4.egg/PhysicalQuantities/decorator.py in checkbaseunit(arg, unit)
         15     try:
    ---> 16         arg.unit.conversion_tuple_to(unit_table[unit])
         17     except UnitError:


    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.4-py3.4.egg/PhysicalQuantities/Unit.py in conversion_tuple_to(self, other)
        323         if self.powers != other.powers:
    --> 324             raise UnitError('Incompatible units')
        325 


    UnitError: Incompatible units

    
    During handling of the above exception, another exception occurred:


    UnitError                                 Traceback (most recent call last)

    <ipython-input-52-5e21cfcad74a> in <module>()
    ----> 1 power(PhysicalQuantity(1,'A'), PhysicalQuantity(1,'A'))
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.4-py3.4.egg/PhysicalQuantities/decorator.py in wrapper(wrapped, instance, args, kwargs)
         42     def wrapper(wrapped, instance, args, kwargs):
         43         for i, arg in enumerate(args):
    ---> 44             checkbaseunit(arg, units[i])
         45         for i, kwarg in enumerate(kwargs):
         46             checkbaseunit(kwarg, units[i])


    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.4-py3.4.egg/PhysicalQuantities/decorator.py in checkbaseunit(arg, unit)
         16         arg.unit.conversion_tuple_to(unit_table[unit])
         17     except UnitError:
    ---> 18         raise UnitError('%s is not of unit %s' % (arg, unit))
         19 
         20 


    UnitError: 1 A is not of unit V


.. code:: python

    @require_units(u='V', i='A')
    def powerkw(u=u, i=i):
        return (u*i).W


::


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-53-b5e9fe7f7953> in <module>()
    ----> 1 @require_units(u='V', i='A')
          2 def powerkw(u=u, i=i):
          3     return (u*i).W


    TypeError: require_units() got an unexpected keyword argument 'u'


Optional units in function call
===============================

.. code:: python

    @optional_units('V', 'A', return_unit='W')
    def powero(u, i):
        return u*i

.. code:: python

    powero(1, 1)




.. math::

    1 $\text{W}



.. code:: python

    powero(1V, 1A)




.. math::

    1.0 $\text{W}



.. code:: python

    powero(1V, 1m)


::


    ---------------------------------------------------------------------------

    UnitError                                 Traceback (most recent call last)

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.4-py3.4.egg/PhysicalQuantities/decorator.py in dropunit(arg, unit)
         29     try:
    ---> 30         arg.unit.conversion_tuple_to(unit_table[unit])
         31         return arg.base.value


    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.4-py3.4.egg/PhysicalQuantities/Unit.py in conversion_tuple_to(self, other)
        323         if self.powers != other.powers:
    --> 324             raise UnitError('Incompatible units')
        325 


    UnitError: Incompatible units

    
    During handling of the above exception, another exception occurred:


    UnitError                                 Traceback (most recent call last)

    <ipython-input-57-4a19eba42854> in <module>()
    ----> 1 powero(PhysicalQuantity(1,'V'), PhysicalQuantity(1,'m'))
    

    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.4-py3.4.egg/PhysicalQuantities/decorator.py in wrapper(wrapped, instance, args, kwargs)
         58         newargs = []
         59         for i, arg in enumerate(args):
    ---> 60             newargs.append(dropunit(arg, units[i]))
         61         newkwargs = {}
         62         for i, key in enumerate(kwargs):


    /Users/juhasch/anaconda/lib/python3.4/site-packages/PhysicalQuantities-0.4-py3.4.egg/PhysicalQuantities/decorator.py in dropunit(arg, unit)
         31         return arg.base.value
         32     except UnitError:
    ---> 33         raise UnitError('%s is not of unit %s' % (arg, unit))
         34 
         35 


    UnitError: 1 m is not of unit A


.. code:: python

    @optional_units(u='V', i='A')
    def powerokw(u=u, i=i):
        return (u*i).W


::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-59-96f916b63d22> in <module>()
          1 @optional_units(u='V', i='A')
    ----> 2 def powerokw(u=u, i=i):
          3     return (u*i).W


    NameError: name 'u' is not defined


