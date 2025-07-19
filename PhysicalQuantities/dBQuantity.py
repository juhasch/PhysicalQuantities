""" Class for dB calculations

Examples
--------
>>> from PhysicalQuantities.dBQuantity import dBQuantity
>>> dBQuantity(1, 'dBm')
1 dBm


TODO:
 * Allow 1 dBm + 1 dBW
 * (1,2) * dBQuantity(3, 'dBV') gives strange result:  (1, 2, 1, 2, 1, 2) dBV

"""
from __future__ import annotations
import copy
import numpy as np
#
from .quantity import PhysicalQuantity
from .unit import PhysicalUnit, UnitError, unit_table

__all__ = ['dB10', 'dB20', 'PhysicalQuantity_to_dBQuantity', 'dBQuantity', 'dB_unit_table']

# Dynamically generated list of all dB units
dB_unit_table = {}


class dBUnit:
    """Class for handling dB units

    Attributes
    ----------
    name
        Name of dB unit
    physicalunit
        Physical representation of the dB value
    offset: float
        Offset, used e.g. for dBd vs. dBi
    factor:
        Factur for dB <-> linear conversion
    """
    name: str
    physicalunit: PhysicalUnit
    offset: float
    factor: float
    z0: PhysicalQuantity

    def __init__(self, name: str, physicalunit: PhysicalUnit, offset: float = 0, factor: int = 0,
                 z0=PhysicalQuantity(50, 'Ohm')):
        """

        Parameters
        ----------
        name
            Name of dB unit
        physicalunit: PhysicalUnit
            Physical representation of the dB value
        offset
            Specify offset used e.g. for dBd vs. dBi

        """
        self.name = name
        self.physicalunit = physicalunit
        self.offset = offset
        self.z0 = z0
        try:
            self.factor = 10 if self.physicalunit.is_power else 20
        except AttributeError:
            self.factor = factor
        dB_unit_table[name] = self

    @property
    def is_power(self) -> bool:
        return self.physicalunit.is_power

    @property
    def __name__(self) -> str:
        return self.name


def _add_dB_units(name, unit,  offset: float = 0, factor: int = 0):
    dB_unit_table[name] = dBUnit(name, unit, offset, factor)


# Predefined dB units
_add_dB_units('dB', unit=None)
_add_dB_units('dBm', unit=unit_table['mW'])
_add_dB_units('dBW', unit=unit_table['W'])
_add_dB_units('dBnV', unit=unit_table['nV'])
_add_dB_units('dBuV', unit=unit_table['uV'])
_add_dB_units('dBmV', unit=unit_table['mV'])
_add_dB_units('dBV', unit=unit_table['V'])
_add_dB_units('dBnA', unit=unit_table['nA'])
_add_dB_units('dBuA', unit=unit_table['uA'])
_add_dB_units('dBmA', unit=unit_table['mA'])
_add_dB_units('dBA', unit=unit_table['A'])
_add_dB_units('dBsm', unit=PhysicalQuantity(1, 'm**2').unit)
_add_dB_units('dBd', unit=None, factor=10, offset=2.15)
_add_dB_units('dBi', unit=None, factor=10)
_add_dB_units('dBc', unit=None, factor=10)


def PhysicalQuantity_to_dBQuantity(x: PhysicalQuantity, dBunitname: str | None = None):
    """ Conversion from a PhysicalQuantity to correct dB<x> value

    Parameters
    ----------
    x:
        Linear physical quantiy to be converted into a dB quantitiy
    dBunitname:
        Desired unit of dB value (i.e. dBm or dBW for Watt)

    Returns
    -------
    dBQuantity
        Converted dB quantity

    """
    if isinstance(x, PhysicalQuantity):
        dbbase = None

        if dBunitname is not None and dB_unit_table[dBunitname] is not None:
            if dB_unit_table[dBunitname].physicalunit.baseunit.name == x.unit.baseunit.name:
                dbbase = dBunitname
                value = x.to(dB_unit_table[dBunitname].physicalunit.name).value
                _unit = dB_unit_table[dBunitname].physicalunit  # FIXME
        else:
            for key in dB_unit_table:
                if dB_unit_table[key].physicalunit is not None and dB_unit_table[key].physicalunit.name == x.unit.name:
                    dbbase = key
                    value = x.value
                    break
                elif dB_unit_table[key].physicalunit is not None and dB_unit_table[key].physicalunit.baseunit.name == \
                        x.unit.baseunit.name:
                    dbbase = key
                    value = x.base.value
        _unit = x.unit
        if dbbase is None:
            raise UnitError(f'Cannot handle unit {x.unit}')
        factor = 20 - 10 * int(_unit.is_power)
        dbvalue = factor * np.log10(value)
        return dBQuantity(dbvalue, dbbase, islog=True)
    raise UnitError('Cannot handle unitless quantity %s' % x)


def dB10(x) -> dBQuantity:
    """ Convert linear value to 10*log10() dB value

    Parameters
    ----------
    x: array_like
        linear value

    Returns
    -------
    array_like
        10*log10(x)
    """
    if isinstance(x, PhysicalQuantity):
        val = x.base.value
    else:
        val = x
    return dBQuantity(10*np.log10(val), 'dB', islog=True)


def dB20(x) -> dBQuantity:
    """ Convert linear value to 20*log10() dB value

    Parameters
    ----------
    x: array_like
        linear value

    Returns
    -------
    array_like
        20*log10(x)
    """
    if isinstance(x, PhysicalQuantity):
        val = x.base.value
    else:
        val = x
    return dBQuantity(20*np.log10(val), 'dB', islog=True)


class dBQuantity:
    """ dB scaled physical quantity with units.

        dBquantity instances allow addition, subtraction, comparison and conversion.
    """

    __array_priority__ = 1000  # make sure numpy arrays do not get iterated

    def __init__(self, value, unitname, islog=True):
        """ Initialize and convert to logarithm if islog=False

        Parameters
        ----------
        unitname: str
            Name of the dB unit
        value: any
            Value of dB unit
        islog: bool
            True: value is already dB scaled
            False:  value needs to be converted to dB (n*log10(value))
                    where n is determined by PhysicalQuantity.is_power()

        Raises
        ------
        UnitError
            Unknown dB unit given in unitname

        """
        try:
            self.unit = dB_unit_table[unitname]
        except KeyError:
            raise UnitError(f'Unknown unit {unitname}')

        try:
            ip = get_ipython()
            self.ptformatter = ip.display_formatter.formatters['text/plain']
        except NameError:
            self.ptformatter = None
        self.format = ''  # display format for number to string conversion

        if islog is True:
            self.value = value
        else:
            self.value = self.unit.factor * np.log10(value) - self.unit.offset

    def __dir__(self):
        """ return list for tab completion
            Include conversions to linear and their dB units
        """
        x = list(super().__dir__())
        # This is required, as strange things happen with IPython...
        for cruft in ['__builtins__', '__args__']:
            try:
                del unit_table[cruft]
            except KeyError:
                pass

        # add PhysicalUnits and dBUnits that can be converted into
        if self.unit.physicalunit is not None:
            base = self.unit.physicalunit.baseunit
            if isinstance(base, PhysicalUnit):
                for key in unit_table:
                    if unit_table[key].baseunit is base:
                        x.append(key)
                for key in dB_unit_table:
                    unit = dB_unit_table[key]
                    if unit.physicalunit is not None:
                        if unit.physicalunit.baseunit is base:
                            x.append(str(key))
        return x
    
    def __getattr__(self, attr):
        """ Convert to different scaling in the same unit.
            If a '_' is appended, drop unit (possibly after rescaling) and return value only.

        Parameters
        ----------
        attr : string
            attribute name
            
        Raises
        ------
        UnitError
            If no conversion between units is possible

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> a = 2 * q.dBm
        >>> a
        2 dBm
        >>> a._
        2
        """
        dropunit = (attr[-1] == '_')
        unitname = attr.strip('_')
        if unitname == '' and dropunit is True:
            return self.value

        isdbunit = unitname in dB_unit_table.keys()
        if not isdbunit:
            if dropunit is False:
                return self.lin.to(unitname)
            else:
                return self.lin.to(unitname).value
        
        # convert to different scaling
        if self.unit.name is unitname:
            return self
        else:
            # convert to same base unit, only scaling
            if self.unit.physicalunit is not None:
                scaling = self.unit.factor * np.log10(self.unit.physicalunit.factor /
                                                      dB_unit_table[unitname].physicalunit.factor)
            else:
                scaling = self.unit.offset
            value = self.value + scaling
            if dropunit is False:
                return self.__class__(value, unitname, islog=True)
            else:
                return value

    def __len__(self):
        """ Return length of quantity if underlying object is array or list
            e.g. len(obj)
        """
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            return len(self.value)
        raise TypeError('Not a list or array: %s', self)

    def to(self, unitname: str) -> dBQuantity:
        """ Convert to differently scaled dB units

        Parameters
        ----------
        unitname: str
            Name of new dB unit

        """
        if unitname in dB_unit_table.keys():
            # convert to same base unit, only scaling
            scaling = self.unit.factor * np.log10(self.unit.physicalunit.factor /
                                                  dB_unit_table[unitname].physicalunit.factor)
            value = self.value + scaling
            return self.__class__(value, unitname, islog=True)

        raise UnitError('Cannot convert to unit %s' % unitname)

    def __deepcopy__(self, memo: dict):
        """ Return a copy of the PhysicalQuantity including the value.
            Needs deepcopy to copy the value
        """
        new_value = copy.deepcopy(self.value)
        new_instance = self.__class__(new_value, self.unit.name, islog=True)
        memo[id(self)] = new_instance
        return new_instance

    def __getitem__(self, key):
        """ Allow indexing if quantities if underlying object is array or list
            e.g. obj[0] or obj[0:4]
        """
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            return self.__class__(self.value[key], self.unit.name)
        raise AttributeError('Not a list or array: %s' % self)        

    def __setitem__(self, key, value):
        """ Set quantities if underlying object is array or list

            >>> from PhysicalQuantities import q
            >>> obj = np.linspace(0,10,10) * q.dBm
            >>> obj[0] = 0 q.dBm

        """
        if not isinstance(value, dBQuantity):
            raise AttributeError('Not a dBQuantity')
        if isinstance(self.value, np.ndarray) or isinstance(self.value, list):
            self.value[key] = value.to(self.unit.name).value
            return self.__class__(self.value[key], self.unit.name)
        raise AttributeError('Not a dBQuantity array or list')

    @property
    def dB(self) -> dBQuantity:
        """ return dB value without unit """
        return dBQuantity(self.value, 'dB', islog=True)

    @property
    def lin(self) -> PhysicalQuantity:
        """Return linear value of dBQuantity

        Returns
        -------
            Linear value

        Examples
        --------
        >>> a = 0 dBm
        >>> a.lin
        1 mW
        >>> a = dB10(8)
        18.06 dB
        >>> a.lin
        8.00
        """
        if self.unit.physicalunit is not None:
            return PhysicalQuantity(self.__float__(), self.unit.physicalunit)
        return self.__float__()

    @property
    def lin10(self) -> PhysicalQuantity | float:
        """Return linear value of dBQuantity and with 10^(value/10)

        Returns
        -------
            Linear value

        Examples
        --------
        >>> a = 6 dB
        >>> a.lin10
        3.98
        >>> a = 0 dBm
        >>> a.lin10
        1 mW

        Raises
        ------
        ValueError
            If a non-power quantity is converted
        """
        val = pow(10, self.value / 10)
        if self.unit.physicalunit is not None:
            if self.unit.is_power is True:
                return PhysicalQuantity(val, self.unit.physicalunit)
            else:
                raise ValueError('Invalid 10^(x/10) conversion of a non-power quantity')
        else:
            return val

    @property
    def lin20(self) -> PhysicalQuantity | float:
        """Return linear value of dBQuantity and with 10^(value/20)

        Returns
        -------
            Linear value

        Examples
        --------
        >>> a = 6 dB
        >>> a.lin20
        2.00

        Raises
        ------
        ValueError
            If a power quantity is converted
        """
        val = pow(10, self.value / 20)
        if self.unit.physicalunit is not None:
            # This property is for amplitude-like units (is_power is False)
            if self.unit.is_power is False:
                return PhysicalQuantity(val, self.unit.physicalunit)
            else:
                # Raise error if called on a power unit
                raise ValueError('Invalid 10^(x/20) conversion of a power quantity')
        else:
            # No physical unit, return raw value (e.g., for plain dB)
            return val

    def __add__(self, other):
        """ Add two dBQuantity values
        Values without physical units are simply added
        For physical units, the linear values are added and converted back to dB.
        
        :parm other: Value to be added
        
        >>> 1 dB + 2 dB
        3 dB
        >>> 1 dBm + 2 dB
        3 dBm
        >>> 1 dBm + 1 dBm
        4.01 dBm
        """
        
        if (self.unit.name == 'dB') or (other.unit.name == 'dB'):
            # easy unitless adding
            value = self.value + other.value
            unit = other.unit.name if self.unit.name == 'dB' else self.unit.name
            return self.__class__(value, unit, islog=True)
        elif dB_unit_table[self.unit.name] is dB_unit_table[other.unit.name]:
            # same unit adding
            val1 = float(self)
            val2 = float(other)
            return self.__class__(val1+val2, self.unit.name, islog=False)
        else:
            raise UnitError('Cannot add unequal units %s and %s' % (self.unit.name, other.unit.name))

    __radd__ = __add__

    def __sub__(self, other):
        """ Subtract a dBQuantity from another

        Parameters
        ----------
        other: dBQuantity
            dBQuantity to subtract from self.

        Examples
        --------
        >>> 0 dBm + 1 dB
        1 dBm
        >>> 0 dBm + 1 dBW
        xx dBm
        """
        if self.unit.name == 'dB' or other.unit.name == 'dB':
            # easy unitless adding
            value = self.value - other.value
            return self.__class__(value, self.unit.name, islog=True)
        elif self.unit.physicalunit is other.unit.physicalunit:
            # same unit subtraction
            val1 = float(self)
            val2 = float(other)
            return self.__class__(val1-val2, self.unit.name, islog=False)
        else:
            raise UnitError('Cannot add unequal units %s and %s' % (self.unit.name, other.unit.name))

    __rsub__ = __sub__
    
    def __mul__(self, other):
        if not hasattr(other, 'unit'):
            # dB values will be multiplied with a factor to enable "a = 2 * q.dBm"
            value = self.value * other
            return self.__class__(value, self.unit.name, islog=True)

    __rmul__ = __mul__

    def __div__(self, other):
        """ Divide a dB value by another factor
        Only valid if the dB value is not associated whith a physical quantity

        Parameters
        ----------
        other: dBQuantity

        Returns
        -------
        dBQuantity
            divided dBQuantity
        
        >>> 3 dB / 4
        """
        if self.unit.name == 'dB' and not hasattr(other, 'unit'):
            # dB without physical dimension can be divided by a factor
            value = self.value / other
            return self.__class__(value, self.unit.name, islog=True)
        raise UnitError('Cannot divide dB units')

    __truediv__ = __div__

    def __floordiv__(self, other):
        """ Divide a dB value by another factor
        Only valid if the dB value is not associated whith a physical quantity

        Parameters
        ----------
        other: dBQuantity

        Returns
        -------
        dBQuantity
            divided dBQuantity
        
        >>> 3 dB / 4
        """
        if self.unit.name == 'dB' and not hasattr(other, 'unit'):
            # dB without physical dimension can be divided by a factor
            value = self.value // other
            return self.__class__(value, self.unit.name, islog=True)
        raise UnitError('Cannot divide dB units')
            
    def __rfloordiv__(self, other):
        """ Divide a dB value by another factor
        Only valid if the dB value is not associated whith a physical quantity

        Parameters
        ----------
        other: dBQuantity
            Divisor

        Returns
        -------
        dBQuantity
            divided dBQuantity
        
        >>> 3 dB / 4
        """
        if self.unit.name == 'dB' and not hasattr(other, 'unit'):
            # dB without physical dimension can be divided by a factor
            value = other // self.value
            return self.__class__(value, self.unit.name, islog=True)
        
    def __neg__(self):
        """ Return negative value """
        return self.__class__(-self.value, self.unit.name, islog=True)
    
    def __float__(self):
        # return linear value in base unit
        if self.unit.factor == 0:
            raise UnitError('Cannot convert dB unit with unknown factor to linear')

        val = self.value / self.unit.factor
        return pow(10, val)
    
    def __str__(self):
        if self.ptformatter is not None and self.format == '' and isinstance(self.value, float):  # pragma: no cover
            # %precision magic only works for floats
            fmt = self.ptformatter.float_format
            return "%s %s" % (fmt % self.value, str(self.unit.name))
        return '{0:{format}} {1}'.format(self.value, str(self.unit.name), format=self.format)

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        """ Test if quantity is greater than other

        Parameters
        ----------
        other: dBQuantity
            Quantity to compare with

        Returns
        -------
        bool
            True if quantity is greater than other

        Raises
        ------
        UnitError
            If different dBunit or type are compared, or if underlying
            physical units are dimensionally incompatible.

        """
        if isinstance(other, dBQuantity):
            # dB values without scaling
            if self.unit.name == other.unit.name:
                return self.value > other.value
            # If dB units differ, check underlying physical units
            elif self.lin.base.unit.powers == other.lin.base.unit.powers:
                # If dimensions match, compare linear values in base units
                return self.lin.base.value > other.lin.base.value
            else:
                # If dimensions differ, raise error
                raise UnitError(f'Cannot compare dB quantities with incompatible underlying units: {self.unit.physicalunit.name} and {other.unit.physicalunit.name}')
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __ge__(self, other):
        """ Test if quantity is greater or equal than other

        Parameters
        ----------
        other: dBQuantity
            Quantity to compare with

        Returns
        -------
        bool
            True if quantity is greater or equal than other

        Raises
        ------
        UnitError
            If different dBunit or type are compared, or if underlying
            physical units are dimensionally incompatible.

        """
        if isinstance(other, dBQuantity):
            if self.unit.name == other.unit.name:
                return self.value >= other.value
            elif self.lin.base.unit.powers == other.lin.base.unit.powers:
                return self.lin.base.value >= other.lin.base.value
            else:
                raise UnitError(f'Cannot compare dB quantities with incompatible underlying units: {self.unit.physicalunit.name} and {other.unit.physicalunit.name}')
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __lt__(self, other):
        """ Test if quantity is less than other

        Parameters
        ----------
        other: dBQuantity
            Quantity to compare with

        Returns
        -------
        bool
            True if quantity is less than other

        Raises
        ------
        UnitError
            If different dBunit or type are compared, or if underlying
            physical units are dimensionally incompatible.

        """
        if isinstance(other, dBQuantity):
            if self.unit.name == other.unit.name:
                return self.value < other.value
            elif self.lin.base.unit.powers == other.lin.base.unit.powers:
                return self.lin.base.value < other.lin.base.value
            else:
                raise UnitError(f'Cannot compare dB quantities with incompatible underlying units: {self.unit.physicalunit.name} and {other.unit.physicalunit.name}')
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __le__(self, other):
        """ Test if quantity is less or equal than other

        Parameters
        ----------
        other: dBQuantity
            Quantity to compare with

        Returns
        -------
        bool
            True if quantity is less or equal than other

        Raises
        ------
        UnitError
            If different dBUnit or type are compared, or if underlying
            physical units are dimensionally incompatible.

        """
        if isinstance(other, dBQuantity):
            if self.unit.name == other.unit.name:
                return self.value <= other.value
            elif self.lin.base.unit.powers == other.lin.base.unit.powers:
                return self.lin.base.value <= other.lin.base.value
            else:
                 raise UnitError(f'Cannot compare dB quantities with incompatible underlying units: {self.unit.physicalunit.name} and {other.unit.physicalunit.name}')
        else:
            raise UnitError('Cannot compare dBQuantity with type %s' % type(other))

    def __eq__(self, other):
        """ Test if two quantities are equal

        Parameters
        ----------
        other: dBQuantity
            Quantity to compare with

        Returns
        -------
        bool
            True if quantities are equal

        Raises
        ------
        UnitError
            If different dBunit or type are compared, or if underlying
            physical units are dimensionally incompatible.

        """
        if isinstance(other, dBQuantity):
            if self.unit.name == other.unit.name:
                return self.value == other.value
            elif self.lin.base.unit.powers == other.lin.base.unit.powers:
                return self.lin.base.value == other.lin.base.value
            else:
                 raise UnitError(f'Cannot compare dB quantities with incompatible underlying units: {self.unit.physicalunit.name} and {other.unit.physicalunit.name}')
        else:
            # Return False for comparison with non-dBQuantity types
            return False

    def __ne__(self, other):
        """ Test if two quantities are not equal

        Parameters
        ----------
        other: dBQuantity
            Quantity to compare with

        Returns
        -------
        bool
            True if quantities are not equal

        Raises
        ------
        UnitError
            If different dBUnit or type are compared, or if underlying
            physical units are dimensionally incompatible.

        """
        if isinstance(other, dBQuantity):
            if self.unit.name == other.unit.name:
                return self.value != other.value
            elif self.lin.base.unit.powers == other.lin.base.unit.powers:
                return self.lin.base.value != other.lin.base.value
            else:
                raise UnitError(f'Cannot compare dB quantities with incompatible underlying units: {self.unit.physicalunit.name} and {other.unit.physicalunit.name}')
        else:
            # Return True for comparison with non-dBQuantity types
            return True
