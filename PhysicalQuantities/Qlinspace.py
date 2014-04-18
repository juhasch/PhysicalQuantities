# -*- coding: utf-8 -*-
"""
Numpy helper functions for PyPUnits

"""


# numpy linspace wrapper for units
def Qlinspace(start, stop, num = 50,  endpoint=True, retstep=False):
    if not isinstance(start,PhysicalQuantity) and not isinstance(stop,PhysicalQuantity):
        return np.linspace(start, stop, num,  endpoint, retstep)

    if isinstance(start,PhysicalQuantity) and isinstance(stop,PhysicalQuantity):
        if start.base.unit != stop.base.unit:
            print start.base.unit, stop.base.unit
            raise UnitError("Cannot match units")
    
    if isinstance(start,PhysicalQuantity):
        start_value = start.value
        unit = start.unit
    else:
        start_value = start

    if isinstance(stop,PhysicalQuantity):
        stop_value = stop.value
        unit = stop.unit
    else:
        stop_value = stop

    array = np.linspace(start_value, stop_value, num,  endpoint, retstep)

    if retstep:
        return PhysicalQuantity(array[0], unit), PhysicalQuantity(array[1], unit)
    else:
        return array * PhysicalQuantity(1, unit)
