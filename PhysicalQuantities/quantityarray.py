"""Implement a Numpy array with physical units"""
import numpy as np
from numpy import ndarray

from .unit import (
    PhysicalUnit, UnitError, base_names, convertvalue, findunit,
    isphysicalunit, unit_table,
)


class PhysicalQuantityArray(ndarray):

    def __new__(cls, input_array, unit=None):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj.unit = findunit(unit)
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self.unit = getattr(obj, 'unit', None)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        # add, substract
        # divide
        # square, power
        args = []
        op = ufunc.__name__
        out_unit = self.unit
        args.append(self.view(np.ndarray))

        if op in ['add', 'subtract']:
            par1, par2 = inputs
            if isinstance(par2, PhysicalQuantityArray):
                if par2.unit != self.unit:
                    raise ValueError('Incompatible units.')
                args.append(par2.view(np.ndarray))
            else:
                args.append(par2)
        elif op in ['multiply']:
            par1, par2 = inputs
            if isinstance(par2, PhysicalQuantityArray):
                args.append(par2.view(np.ndarray))
                out_unit *= par2.unit
            else:
                args.append(par2)
        elif op in ['true_divide']:
            par1, par2 = inputs
            if isinstance(par2, PhysicalQuantityArray):
                args.append(par2.view(np.ndarray))
                out_unit /= par2.unit
            else:
                args.append(par2)
        elif op in ['square']:
            out_unit = out_unit ** 2
        elif op in ['square', 'power']:
            par1, par2 = inputs
            if isinstance(par2, PhysicalQuantityArray):
                raise ValueError('Incompatible units.')
            else:
                args.append(par2)
                out_unit = out_unit ** par2
        else:
            args = []
            for par2 in inputs:
                if isinstance(par2, PhysicalQuantityArray):
                    if par2.unit != self.unit:
                        raise ValueError('Incompatible units.')
                    args.append(par2.view(np.ndarray))
                else:
                    args.append(par2)

        results = super().__array_ufunc__(ufunc, method, *args, **kwargs)
        return self.__class__(results, out_unit)

    def __dir__(self):
        ulist = super().__dir__()
        u = unit_table.values()
        for _u in u:
            if isphysicalunit(_u):
                if str(_u.baseunit) is str(self.unit.baseunit):
                    ulist.append(_u.name)
        return ulist

    def __getattr__(self, attr):
        dropunit = (attr[-1] == '_')
        attr = attr.strip('_')
        if attr == '' and dropunit is True:
            return self.view(ndarray)
        try:
            attrunit = unit_table[attr]
        except KeyError:
            raise AttributeError(f'Unit {attr} not found')
        if dropunit is True:
            return self.to(attrunit.name).view(ndarray)
        else:
            return self.to(attrunit.name)

    def __repr__(self):
        arrstr = super().__str__()
        return f'PhysicalQuantityArray({arrstr}, unit={self.unit})'

    def to(self, *units):
        units = list(map(findunit, units))
        if len(units) == 1:
            unit = units[0]
            factor = convertvalue(1, self.unit, unit)
            return self.__class__(self * factor, unit)
        raise ValueError('More than one unit given to convert to')

    @property
    def base(self):
        num = ''
        denom = ''
        for i in range(len(base_names)):
            unit = base_names[i]
            power = self.unit.powers[i]
            if power < 0:
                denom += '/' + unit
                if power < -1:
                    denom += '**' + str(-power)
            elif power > 0:
                num += '*' + unit
                if power > 1:
                    num += '**' + str(power)
        if len(num) == 0:
            num = '1'
        else:
            num = num[1:]
        return self.__class__((self + self.unit.offset) * self.unit.factor, num + denom)
