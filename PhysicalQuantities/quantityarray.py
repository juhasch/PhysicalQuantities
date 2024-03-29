"""Implement a Numpy array with physical units"""
from __future__ import annotations
import numpy as np
from numpy import ndarray
from typing import Any

from .unit import (
    UnitError, base_names, convertvalue, findunit,
    isphysicalunit, unit_table, PhysicalUnit
)



class PhysicalQuantityArray(ndarray):
    value: ndarray
    unit: PhysicalUnit

    def __new__(cls, input_array, unit=None):
        obj = np.asarray(input_array).view(cls)
        obj.unit = findunit(unit)
        return obj

    def __array_finalize__(self, obj, *args: Any, **kwargs: Any):
        if isinstance(obj, PhysicalQuantityArray):
            self.unit = obj.unit

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
                    raise UnitError('Incompatible units.')
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
                raise UnitError('Incompatible units.')
            else:
                args.append(par2)
                out_unit = out_unit ** par2
        elif op in ['bitwise_or', 'bitwise_and', 'bitwise_xir']:
            args = []
            for par in inputs:
                args.append(par.view(np.ndarray))
            kwargs = dict(out=self.view(np.ndarray))
        else:
            args = []
            for par2 in inputs:
                if isinstance(par2, PhysicalQuantityArray):
                    if par2.unit != self.unit:
                        raise UnitError('Incompatible units.')
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

    def __repr__(self) -> str:
        arrstr = super().__str__()
        return f'PhysicalQuantityArray({arrstr}, unit={self.unit})'

    def to(self, *units) -> PhysicalQuantityArray:
        """Convert to a different unit

        Parameters
        ----------
        units : str
            Units to convert to

        Returns
        -------
        PhysicalQuantityArray
            Array with converted units
        """
        _units = list(map(findunit, units))
        if len(_units) == 1:
            factor = convertvalue(1, self.unit, _units[0])
            return self.__class__(self * factor, _units[0])
        raise UnitError('More than one unit given to convert to')

    @property
    def base(self) -> PhysicalQuantityArray:
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
