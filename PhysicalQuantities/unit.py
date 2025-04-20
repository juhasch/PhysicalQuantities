""" PhysicalUnit class definition

Original author: Georg Brandl <georg@python.org>, https://bitbucket.org/birkenfeld/ipython-physics
"""
from __future__ import annotations
from __future__ import annotations
import copy
import json
from functools import reduce, lru_cache
from typing import Dict
from fractions import Fraction

import numpy as np

from .fractdict import FractionalDict


class UnitError(ValueError):
    pass


class PhysicalUnit:
    prefixed: bool = False
    """Physical unit.

    A physical unit is defined by a name (possibly composite), a scaling factor, and the exponentials of each of
    the SI base units that enter into it. Units can be multiplied, divided, and raised to integer powers.

    Attributes
    ----------
    prefixed: bool
        If instance is a scaled version of a unit
    baseunit: PhysicalUnit
        Base unit if prefixed, otherwise self
    names: FractionalDict
        A dictionary mapping each name component to its associated integer power (e.g. C{{'m': 1, 's': -1}})
        for M{m/s})
    factor: float
        A scaling factor from base units
    powers: list
        The integer powers for each of the nine base units:
        ['m', 'kg', 's', 'A', 'K', 'mol', 'cd', 'rad', 'sr']
    offset: float
        An additive offset to the unit (used only for temperatures)
    url: str
        URL describing the unit
    verbosename: str
        The verbose name of the unit (e.g. Coulomb)
    unece_code: str
        Official unit code
        (see https://www.unece.org/fileadmin/DAM/cefact/recommendations/rec20/rec20_Rev9e_2014.xls)

    """

    def __init__(self, names, factor: float, powers: list[int], offset: float = 0, url: str = '', verbosename: str = '',
                 unece_code: str = ''):
        """ Initialize object

        Parameters
        ----------
        names: FractionalDict|str
            A dictionary mapping each name component to its associated integer power (e.g. C{{'m': 1, 's': -1}})
            for M{m/s}). As a shorthand, a string may be passed which is assigned an implicit power 1.
        factor:
            A scaling factor from base units
        powers:
            The integer powers for each of the nine base units:
            ['m', 'kg', 's', 'A', 'K', 'mol', 'cd', 'rad', 'sr']
        offset:
            An additive offset to the unit (used only for temperatures)
        url:
            URL describing the unit
        verbosename:
            The verbose name of the unit (e.g. Coulomb)
        unece_code:
            Official unit code
            (see https://www.unece.org/fileadmin/DAM/cefact/recommendations/rec20/rec20_Rev9e_2014.xls)

        """
        self.baseunit = self
        self.verbosename = verbosename
        self.url = url
        if isinstance(names, str):
            self.names = FractionalDict()
            self.names[names] = 1
        else:
            self.names = FractionalDict()
            for _name in names:
                self.names[_name] = names[_name]
        self.factor = factor
        self.offset = offset
        if len(base_names) != len(powers):
            raise ValueError('Invalid number of powers given for existing base_names')
        self.powers = powers
        self.unece_code = unece_code

    def set_name(self, name):
        """Set unit name as FractionalDict

        Parameters
        ----------
        name: str
            Unit name
        """
        self.names = FractionalDict()
        self.names[name] = 1

    @property
    def name(self) -> str:
        """ Return name of unit

        Returns
        -------
        str
            Name of unit

        """
        num = ''
        denom = ''
        for unit in self.names.keys():
            power = self.names[unit]
            if power < 0:
                denom = denom + '/' + unit
                if power < -1:
                    denom = denom + '**' + str(-power)
            elif power > 0:
                num = num + '*' + unit
                if power > 1:
                    num = num + '**' + str(power)
        if len(num) == 0:
            num = '1'
        else:
            num = num[1:]
        return num + denom

    @property
    def _markdown_name(self) -> str:
        """ Return name of unit as markdown string

        Returns
        -------
        str
            Name of unit as markdown string

        """
        num = ''
        denom = ''
        for unit in self.names.keys():
            power = self.names[unit]
            if power < 0:
                if denom == '':
                    denom = '\\text{' + unit + '}'
                else:
                    denom = denom + '\\cdot \\text{' + unit + '}'
                if power < -1:
                    denom = denom + '^' + str(-power)
            elif power > 0:
                if num == '':
                    num = '\\text{' + unit + '}'
                else:
                    num = num + '\\cdot \\text{' + unit + '}'
                if power > 1:
                    num = num + '^{' + str(power) + '}'
        if num == '':
            num = '1'
        if denom != '':
            name = '\\frac{' + num + '}{' + denom + '}'
        else:
            name = num
        name = name.replace('\\text{deg}', '\\,^{\\circ}').replace(' pi', ' \\pi ')
        return name

    @property
    def is_power(self) -> bool:
        """ Test if unit is a power unit. Used of dB conversion
        TODO: basically very dumb right now

        Returns
        -------
        bool
            True if it is a power unit, i.e. W, J or anything like it
        """
        p = self.powers
        if p == [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
            return True  # for m^ -> dBsm
        if p[0] == 2 and p[1] == 1 and p[3] > -1:
            return True
        return False

    @property
    def is_dimensionless(self) -> bool:
        """ Check if no dimension is given

        Returns
        -------
        bool
            True if dimensionless
        """
        return not reduce(lambda a, b: a or b, self.powers)

    @property
    def is_angle(self) -> bool:
        """ Check if unit is an angle

        Returns
        -------
        bool
            True if unit is an angle
        """
        return self.powers[7] == 1 and reduce(lambda a, b: a + b, self.powers) == 1

    def __str__(self) -> str:
        """ Return string text representation of unit

        Returns
        -------
        str
            Text representation of unit
        """
        name = self.name.strip().replace('**', u'^')
        return name

    def __repr__(self) -> str:
        return '<PhysicalUnit ' + self.name + '>'

    def _repr_markdown_(self) -> str:
        """ Return markdown representation for IPython notebook

        Returns
        -------
        str
            Unit as LaTeX string
        """
        unit = self._markdown_name
        s = '$%s$' % unit
        return s

    def _repr_latex_(self) -> str:
        """ Return LaTeX representation for IPython notebook

        Returns
        -------
        str
            Unit as LaTeX string
        """
        unit = self._markdown_name
        s = '%s' % unit
        return s

    @property
    def markdown(self) -> str:
        """ Return unit as a markdown formatted string

        Returns
        -------
        str
            Unit as LaTeX string
        """
        return self._repr_markdown_()

    @property
    def latex(self) -> str:
        """ Return unit as a LaTeX formatted string

        Returns
        -------
        str
            Unit as LaTeX string
        """
        return self._repr_latex_()

    def __gt__(self, other) -> bool:
        """ Test if unit is greater than other unit

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to compare with

        Returns
        -------
        bool
            True, if unit is greater than other unit
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor > other.factor
        raise UnitError('Cannot compare different dimensions %s and %s' % (self, other))

    def __ge__(self, other) -> bool:
        """ Test if unit is greater or equal than other unit

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to compare with

        Returns
        -------
        bool
            True, if unit is greater or equal than other unit
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor >= other.factor
        raise UnitError('Cannot compare different dimensions %s and %s' % (self, other))

    def __lt__(self, other) -> bool:
        """ Test if unit is less than other unit

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to compare with

        Returns
        -------
        bool
            True, if unit is less than other unit
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor < other.factor
        raise UnitError('Cannot compare different dimensions %s and %s' % (self, other))

    def __le__(self, other) -> bool:
        """ Test if unit is less or equal than other unit

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to compare with

        Returns
        -------
        bool
            True, if unit is less or equal than other unit
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor <= other.factor
        raise UnitError('Cannot compare different dimensions %s and %s' % (self, other))

    def __eq__(self, other) -> bool:
        """ Test if unit is equal than other unit

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to compare with

        Returns
        -------
        bool
            True, if unit is equal than other unit
        """
        if isphysicalunit(other) and self.powers == other.powers:
            return self.factor == other.factor
        raise UnitError('Cannot compare different dimensions %s and %s' % (self, other))

    def __mul__(self, other):
        """ Multiply units with other value

        Parameters
        ----------
        other:
            Value or unit to multiply with

        Returns
        -------
        PhysicalUnit or PhysicalQuantity
            Multiplied unit

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.m.unit * q.s.unit
        m*s
        """
        from .quantity import PhysicalQuantity
        if self.offset != 0 or (isphysicalunit(other) and other.offset != 0):
            raise UnitError(f'Cannot multiply units {self} and {other} with non-zero offset')
        if isphysicalunit(other):
            return PhysicalUnit(self.names + other.names,
                                self.factor * other.factor,
                                list(map(lambda a, b: a + b, self.powers, other.powers)))
        elif isinstance(other, PhysicalQuantity):
            other = other.unit
            newpowers = [a + b for a, b in zip(other.powers, self.powers)]
            return PhysicalUnit(self.names + FractionalDict({str(other): 1}),
                                self.factor * other.factor, newpowers, self.offset)
        else:
            return PhysicalQuantity(other, self)

    __rmul__ = __mul__

    def __div__(self, other):
        """ Divide two units

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to divide

        Returns
        -------
        PhysicalUnit
            Divided unit

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.m.unit / q.s.unit
        m/s
        """
        from .quantity import PhysicalQuantity
        if self.offset != 0 or (isphysicalunit(other) and other.offset != 0):
            raise UnitError(f'Cannot divide units {self} and {other} with non-zero offset')
        if isphysicalunit(other):
            return PhysicalUnit(self.names - other.names,
                                self.factor / other.factor,
                                list(map(lambda a, b: a - b, self.powers, other.powers)))
        elif isinstance(other, PhysicalQuantity):
            other = other.unit
            newpowers = [a - b for a, b in zip(other.powers, self.powers)]
            return PhysicalUnit(self.names + FractionalDict({str(other): 1}),
                                self.factor / other.factor, newpowers)
        else:
            return PhysicalUnit(self.names + FractionalDict({str(other): -1}),
                                self.factor/other.factor, self.powers)

    def __rdiv__(self, other):
        if self.offset != 0 or (isphysicalunit(other) and other.offset != 0):
            raise UnitError('Cannot divide units %s and %s with non-zero offset' % (self, other))
        if isphysicalunit(other):
            return PhysicalUnit(other.names - self.names,
                                other.factor / self.factor,
                                list(map(lambda a, b: a - b, other.powers, self.powers)))
        else:
            return PhysicalUnit(FractionalDict({str(other): 1}) - self.names,
                                other / self.factor,
                                list(map(lambda x: -x, self.powers)))

    def __floordiv__(self, other):
        """ Divide two units

        Parameters
        ----------
        other: PhysicalUnit
            Other unit to divide

        Returns
        -------
        PhysicalUnit
            Divided unit

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.m.unit / q.s.unit
        m/s
        """
        if self.offset != 0 or (isphysicalunit(other) and other.offset != 0):
            raise UnitError(f'Cannot divide units {self} and {other} with non-zero offset')
        if isphysicalunit(other):
            return PhysicalUnit(self.names - other.names,
                                self.factor // other.factor,
                                list(map(lambda a, b: a - b, self.powers, other.powers)))
        else:
            # TODO: add test
            return PhysicalUnit(self.names + FractionalDict({str(other): -1}),
                                self.factor//other.factor, self.powers)

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __pow__(self, exponent: PhysicalUnit | int):
        """ Power of a unit

        Parameters
        ----------
        exponent: PhysicalUnit
            Power exponent

        Returns
        -------
        PhysicalUnit
            Unit to the power of exponent

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.m.unit ** 2
        m^2
        """
        if self.offset != 0:
            raise UnitError('Cannot exponentiate units %s and %s with non-zero offset' % (self, exponent))
        if isinstance(exponent, int):
            y = lambda x, _p=exponent: x * _p
            p = list(map(y, self.powers))
            f = pow(self.factor, exponent)
            names = FractionalDict((k, self.names[k] * Fraction(exponent, 1)) for k in self.names)
            return PhysicalUnit(names, f, p)
        elif isinstance(exponent, float):
            inv_exp = 1. / exponent
            rounded = int(np.floor(inv_exp + 0.5))
            if abs(inv_exp - rounded) < 1.e-10:
                if all(x % rounded == 0 for x in self.powers):
                    f = pow(self.factor, exponent)
                    p = [int(x / rounded) for x in self.powers]
                    if all(x % rounded == 0 for x in self.names.values()):
                        names = FractionalDict((k, v / rounded) for k, v in self.names.items())
                    else:
                        names = FractionalDict({str(f): 1} if f != 1. else {})
                        names.update({base_names[i]: p_i for i, p_i in enumerate(p)})
                    return PhysicalUnit(names, f, p)
                else:
                    raise UnitError('Illegal exponent %f' % exponent)
        raise UnitError('Only integer and inverse integer exponents allowed')

    def __hash__(self):
        """Custom hash function"""
        return hash((self.factor, self.offset, str(self.powers)))

    def conversion_factor_to(self, other):
        """Return conversion factor to another unit

        Parameters
        ----------
        other: PhysicalUnit
            Unit to compute conversion factor for

        Returns
        -------
        float
            Conversion factor

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.km.unit.conversion_factor_to(q.m.unit)
        1000.0
        """
        if self.powers != other.powers:
            raise UnitError('Incompatible units')
        if self.offset != other.offset and self.factor != other.factor:
            raise UnitError(('Unit conversion (%s to %s) cannot be expressed ' +
                             'as a simple multiplicative factor') %
                            (self.name, other.name))
        return self.factor / other.factor

    def conversion_tuple_to(self, other):
        """Return conversion factor and offset to another unit.

        The conversion is defined such that ``value_in_other = value_in_self * factor + offset``.

        Parameters
        ----------
        other: PhysicalUnit
            Unit to compute conversion factor and offset for

        Returns
        -------
        float tuple
            Tuple (factor, offset)

        Examples
        --------
        >>> from PhysicalQuantities import q
        >>> q.km.unit.conversion_tuple_to(q.m.unit)
        (1000.0, 0.0)
        >>> q.degC = add_composite_unit('degC', 1.0, 'K', offset=273.15) # Define Celsius relative to Kelvin
        >>> q.K.unit.conversion_tuple_to(q.degC.unit) # K to degC
        (1.0, -273.15)
        >>> q.degC.unit.conversion_tuple_to(q.K.unit) # degC to K
        (1.0, 273.15)
        """
        if self.powers != other.powers:
            raise UnitError(f'Incompatible unit for conversion from {self} to {other}')

        # Based on the definition: base = value * factor + offset
        # Let (f1, o1) be the conversion from 'self' (x) to base: base = x * f1 + o1
        # Let (f2, o2) be the conversion from 'other' (y) to base: base = y * f2 + o2
        # We want (F, O) such that y = x * F + O.
        # x * f1 + o1 = (x * F + O) * f2 + o2
        # x * f1 + o1 = x * F * f2 + O * f2 + o2
        # Equating coefficients:
        # f1 = F * f2  => F = f1 / f2
        # o1 = O * f2 + o2 => O = (o1 - o2) / f2
        # Note: Division by zero is possible if other.factor is 0, but this shouldn't
        # happen for physically meaningful units.

        f1, o1 = self.factor, self.offset
        f2, o2 = other.factor, other.offset

        factor = f1 / f2
        offset = (o1 - o2) / f2
        return factor, offset

    @property
    def to_dict(self) -> dict:
        """Export unit as dict

        Returns
        -------
        dict
            Dict containing unit description

        Notes
        -----
        Give unit and iterate over base units

        """
        unit_dict = {'name': self.name,
                     'verbosename': self.verbosename,
                     'offset': self.offset,
                     'factor': self.factor
                     }
        b = self.baseunit
        p = b.powers
        base_dict = {}
        for i, exponent in enumerate(p):
            base_dict[base_names[i]] = exponent
        unit_dict['base_exponents'] = base_dict
        return unit_dict

    @property
    def to_json(self) -> str:
        """Export unit as JSON


        Notes
        -----
        Give unit and iterate over base units

        """

        json_unit = json.dumps({'PhysicalUnit': self.to_dict})
        return json_unit

    @staticmethod
    def from_dict(unit_dict) -> PhysicalUnit:
        """Retrieve PhysicalUnit from dict description

        Parameters
        ----------
        unit_dict: dict
            PhysicalUnit stored as dict

        Returns
        -------
        PhysicalUnit
            Retrieved PhysicalUnit

        Notes
        -----
        Current implementation: throw exception if unit has not already been defined
        """
        u = findunit(unit_dict['name'])
        if u.to_dict != unit_dict:
            raise UnitError(f'Unit {str(u)} does not correspond to given dict')
        return u

    @staticmethod
    def from_json(json_unit) -> PhysicalUnit:
        """Retrieve PhysicalUnit from JSON string description

        Parameters
        ----------
        json_unit: str
            PhysicalUnit encoded as JSON string

        Returns
        -------
        PhysicalUnit
            New PhysicalUnit
        """
        unit_dict = json.loads(json_unit)
        return PhysicalUnit.from_dict(unit_dict['PhysicalUnit'])


def addunit(unit):
    """ Add new PhysicalUnit entry to the unit_table

    Parameters
    -----------
    unit: Physicalunit
        PhysicalUnit object

    Raises
    ------
    KeyError
        If unit already exists

    """
    if unit.name in unit_table:
        raise KeyError(f'Unit {unit.name} already defined')
    unit_table[unit.name] = unit


unit_table: Dict[str, PhysicalUnit] = {}
# These are predefined base units 
base_names = ['m', 'kg', 's', 'A', 'K', 'mol', 'cd', 'rad', 'sr', 'Bit', 'currency']

addunit(PhysicalUnit('m', 1., [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Metre', verbosename='Metre',
        unece_code='MTR'))
addunit(PhysicalUnit('kg', 1, [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Kilogram', verbosename='Kilogram',
        unece_code='KGM'))
addunit(PhysicalUnit('s', 1., [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Second', verbosename='Second',
        unece_code='SEC'))
addunit(PhysicalUnit('A', 1., [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Ampere', verbosename='Ampere',
        unece_code='AMP'))
addunit(PhysicalUnit('K', 1., [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Kelvin', verbosename='Kelvin',
        unece_code='KEL'))
addunit(PhysicalUnit('mol', 1., [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Mole_(unit)', verbosename='Mol',
        unece_code='C34'))
addunit(PhysicalUnit('cd', 1., [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Candela', verbosename='Candela',
        unece_code='CDL'))
addunit(PhysicalUnit('rad', 1., [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        url='https://en.wikipedia.org/wiki/Radian', verbosename='Radian',
        unece_code='C81'))
addunit(PhysicalUnit('sr', 1., [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        url='https://en.wikipedia.org/wiki/Steradian', verbosename='Steradian',
        unece_code='D27'))
addunit(PhysicalUnit('Bit', 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        url='https://en.wikipedia.org/wiki/Bit', verbosename='Bit',
        unece_code=''))
addunit(PhysicalUnit('currency', 1., [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        url='https://en.wikipedia.org/wiki/Currency', verbosename='Currency',
        unece_code=''))


def add_composite_unit(name, factor, units, offset=0, verbosename='', prefixed=False, url=''):
    """ Add new unit to the unit_table

    Parameters
    -----------
    name: str
        Name of the unit
    factor: float
        scaling factor
    units: str
        Composed units of new unit
    offset: float
        Offset factor
    verbosename: str
        A more verbose name for the unit
    prefixed: bool
        This is a prefixed unit
    url: str
        A URL linking to more information about the unit

    Returns
    -------
    str
        Name of new unit

    Raises
    ------
    KeyError
        If unit already exists or if units string is invalid
    ValueError
        If factor or offset is not numeric
    """
    if name in unit_table:
        raise KeyError(f'Unit {name} already defined')
    # Parse composed units string
    try:
        baseunit = eval(units, unit_table)
    except (SyntaxError, ValueError):
        raise KeyError(f'Invalid units string: {units}')

    # Validate factor and offset values
    for value in (factor, offset):
        if not isinstance(value, (int, float)):
            raise ValueError('Factor and offset values have to be numeric')

    # Remove unwanted keys from unit_table
    for key in ['__builtins__', '__args__']:
        unit_table.pop(key, None)

    newunit = copy.deepcopy(baseunit)
    newunit.set_name(name)
    newunit.verbosename = verbosename
    newunit.baseunit = baseunit if prefixed else newunit
    newunit.prefixed = prefixed
    newunit.url = url
    newunit.factor *= factor
    newunit.offset += offset
    unit_table[name] = newunit

    return name


# Helper functions
@lru_cache(maxsize=None)
def findunit(unitname):
    """ Return PhysicalUnit class if given parameter is a valid unit

    Parameters
    ----------
    unitname: str or PhysicalUnit
        Unit to check if valid

    Returns
    -------
    PhysicalUnit
        Unit

    Raises
    ------
    UnitError
        If the input is invalid.

    Examples
    --------
    >>> findunit('mm')
     <PhysicalUnit mm>
    """
    if isinstance(unitname, str):
        if unitname == '':
            raise UnitError('Empty unit name is not valid')
        name = unitname.strip().replace('^', '**')
        if name.startswith('1/'):
            name = '(' + name[2:] + ')**-1'
        try:
            unit = eval(name, unit_table)
        except NameError:
            raise UnitError('Invalid or unknown unit %s' % name)
        for cruft in ['__builtins__', '__args__']:
            try:
                del unit_table[cruft]
            except KeyError:
                pass
    else:
        unit = unitname
    if not isphysicalunit(unit):
        raise UnitError(f'{str(unit)} is not a unit')
    return unit


def convertvalue(value, src_unit, target_unit):
    """ Convert between units, if possible

    Parameters
    ----------
    value:
        Value in source units
    src_unit: PhysicalUnit
        Source unit
    target_unit: PhysicalUnit
        Target unit

    Returns
    -------
    any
        Value scaled to target unit

    Examples
    --------
    >>> from PhysicalQuantities import q
    >>> convertvalue(1, q.mm.unit, q.km.unit)
    1e-06
    >>> convertvalue(0, q.degC.unit, q.K.unit) # 0 degC to K
    273.15
    >>> convertvalue(273.15, q.K.unit, q.degC.unit) # 273.15 K to degC
    0.0
    """
    (factor, offset) = src_unit.conversion_tuple_to(target_unit)
    if isinstance(value, list):
        raise UnitError('Cannot convert units for a list')
    # Apply conversion: value_in_other = value_in_self * factor + offset
    return value * factor + offset


def isphysicalunit(x):
    """ Return true if valid PhysicalUnit class

    Parameters
    ----------
    x: PhysicalUnit
        Unit
    """
    return isinstance(x, PhysicalUnit)
