""" PhysicalUnit class definition

Original author: Georg Brandl <georg@python.org>, https://bitbucket.org/birkenfeld/ipython-physics
"""

import copy
import json
from functools import reduce

import numpy as np

from .NDict import *


class UnitError(ValueError):
    pass


# Helper functions
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

    Examples
    --------
    >>> findunit('mm')
     <PhysicalUnit mm>
    """
    if isinstance(unitname, str):
        if unitname == '':
            raise UnitError('Empty unit name is not valid')
        name = str(unitname).strip().replace('^', '**')
        if name[0:2] == '1/':
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
    """
    (factor, offset) = src_unit.conversion_tuple_to(target_unit)
    if isinstance(value, list):
        raise UnitError('Cannot convert units for a list')
    return (value + offset) * factor


def isphysicalunit(x):
    """ Return true if valid PhysicalUnit class

    Parameters
    ----------
    x: PhysicalUnit
        Unit
    """
    return isinstance(x, PhysicalUnit)


class PhysicalUnit:
    """Physical unit.

    A physical unit is defined by a name (possibly composite), a scaling factor, and the exponentials of each of
    the SI base units that enter into it. Units can be multiplied, divided, and raised to integer powers.

    Attributes
    ----------
    prefixed: bool
        If instance is a scaled version of a unit
    baseunit: PhysicalUnit
        Base unit if prefixed, otherwise self
    names: NumberDict
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
        (see http://www.unece.org/fileadmin/DAM/cefact/recommendations/rec20/rec20_Rev9e_2014.xls)

    """

    def __init__(self, names, factor, powers, offset=0, url=None, verbosename=None, unece_code=None):
        """ Initialize object

        Parameters
        ----------
        names: NumberDict|str
            A dictionary mapping each name component to its associated integer power (e.g. C{{'m': 1, 's': -1}})
            for M{m/s}). As a shorthand, a string may be passed which is assigned an implicit power 1.
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
            (see http://www.unece.org/fileadmin/DAM/cefact/recommendations/rec20/rec20_Rev9e_2014.xls)

        """
        self.prefixed = False
        self.baseunit = self
        self.verbosename = verbosename
        self.url = url
        if isinstance(names, str):
            self.names = NumberDict()
            self.names[names] = 1
        else:
            self.names = NumberDict()
            for _name in names:
                self.names[_name] = names[_name]
        self.factor = factor
        self.offset = offset
        if len(base_names) != len(powers):
            raise ValueError('Invalid number of powers given for existing base_names')
        self.powers = powers
        self.unece_code = unece_code

    def set_name(self, name):
        """Set unit name as NumberDict

        Parameters
        ----------
        name: str
            Unit name
        """
        self.names = NumberDict()
        self.names[name] = 1

    @property
    def name(self):
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
    def _markdown_name(self):
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
                if denom is '':
                    denom = '\\text{' + unit + '}'
                else:
                    denom = denom + '\\cdot \\text{' + unit + '}'
                if power < -1:
                    denom = denom + '^' + str(-power)
            elif power > 0:
                if num is '':
                    num = '\\text{' + unit + '}'
                else:
                    num = num + '\\cdot \\text{' + unit + '}'
                if power > 1:
                    num = num + '^{' + str(power) + '}'
        if num is '':
            num = '1'
        if denom is not '':
            name = '\\frac{' + num + '}{' + denom + '}'
        else:
            name = num
        name = name.replace('u', u'µ').replace('\\text{deg}', '\\,^{\\circ}').replace(' pi', ' \\pi ')
        return name

    @property
    def is_power(self):
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
    def is_dimensionless(self):
        """ Check if no dimension is given

        Returns
        -------
        bool
            True if dimensionless
        """
        return not reduce(lambda a, b: a or b, self.powers)

    @property
    def is_angle(self):
        """ Check if unit is an angle

        Returns
        -------
        bool
            True if unit is an angle
        """
        return self.powers[7] == 1 and reduce(lambda a, b: a + b, self.powers) == 1

    def __str__(self):
        """ Return string text representation of unit

        Returns
        -------
        str
            Text representation of unit
        """
        name = self.name.strip().replace('**', u'^')
        return name

    def __repr__(self):
        return '<PhysicalUnit ' + self.name + '>'

    def _repr_markdown_(self):
        """ Return markdown representation for IPython notebook

        Returns
        -------
        str
            Unit as LaTeX string
        """
        unit = self._markdown_name
        s = '$%s$' % unit
        return s

    def _repr_latex_(self):
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
    def markdown(self):
        """ Return unit as a markdown formatted string

        Returns
        -------
        str
            Unit as LaTeX string
        """
        return self._repr_markdown_()

    @property
    def latex(self):
        """ Return unit as a LaTeX formatted string

        Returns
        -------
        str
            Unit as LaTeX string
        """
        return self._repr_latex_()

    def __gt__(self, other):
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

    def __ge__(self, other):
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

    def __lt__(self, other):
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

    def __le__(self, other):
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

    def __eq__(self, other):
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
        # TODO: add test
            return PhysicalUnit(self.names + NumberDict({str(other): 1}),
                                self.factor * other.factor, self.powers, self.offset)
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
        if self.offset != 0 or (isphysicalunit(other) and other.offset != 0):
            raise UnitError(f'Cannot divide units {self} and {other} with non-zero offset')
        if isphysicalunit(other):
            return PhysicalUnit(self.names - other.names,
                                self.factor / other.factor,
                                list(map(lambda a, b: a - b, self.powers, other.powers)))
        else:
            # TODO: add test
            return PhysicalUnit(self.names + NumberDict({str(other): -1}),
                                self.factor/other.factor, self.powers)

    def __rdiv__(self, other):
        if self.offset != 0 or (isphysicalunit(other) and other.offset != 0):
            raise UnitError('Cannot divide units %s and %s with non-zero offset' % (self, other))
        if isphysicalunit(other):
            return PhysicalUnit(other.names - self.names,
                                other.factor / self.factor,
                                list(map(lambda a, b: a - b, other.powers, self.powers)))
        else:
            return PhysicalUnit(NumberDict({str(other): 1}) - self.names,
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
            return PhysicalUnit(self.names + NumberDict({str(other): -1}),
                                self.factor//other.factor, self.powers)

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __pow__(self, exponent):
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
            p = list(map(lambda x, _p=exponent: x * _p, self.powers))
            f = pow(self.factor, exponent)
            names = NumberDict((k, self.names[k] * exponent) for k in self.names)
            return PhysicalUnit(names, f, p)
        if isinstance(exponent, float):
            inv_exp = 1. / exponent
            rounded = int(np.floor(inv_exp + 0.5))
            if abs(inv_exp - rounded) < 1.e-10:
                if reduce(lambda a, b: a and b,
                          list(map(lambda x, e=rounded: x % e == 0, self.powers))):
                    f = pow(self.factor, exponent)
                    p = list(map(lambda x, _p=rounded: x / _p, self.powers))
                    p = [int(x) for x in p]
                    if reduce(lambda a, b: a and b,
                              list(map(lambda x, e=rounded: x % e == 0,
                                       self.names.values()))):
                        names = NumberDict((k, self.names[k] / rounded) for k in self.names)
                    else:
                        names = NumberDict()
                        if f != 1.:
                            names[str(f)] = 1
                        for i in range(len(p)):
                            names[base_names[i]] = p[i]
                    return PhysicalUnit(names, f, p)
                else:
                    raise UnitError('Illegal exponent %f' % exponent)
        raise UnitError('Only integer and inverse integer exponents allowed')

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
        """Return conversion factor and offset to another unit

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
        """
        if self.powers != other.powers:
            raise UnitError(f'Incompatible unit for conversion from {self} to {other}')

        # let (s1,d1) be the conversion tuple from 'self' to base units
        #   (ie. (x+d1)*s1 converts a value x from 'self' to base units,
        #   and (x/s1)-d1 converts x from base to 'self' units)
        # and (s2,d2) be the conversion tuple from 'other' to base units
        # then we want to compute the conversion tuple (S,D) from
        #   'self' to 'other' such that (x+D)*S converts x from 'self'
        #   units to 'other' units
        # the formula to convert x from 'self' to 'other' units via the
        #   base units is (by definition of the conversion tuples):
        #     ( ((x+d1)*s1) / s2 ) - d2
        #   = ( (x+d1) * s1/s2) - d2
        #   = ( (x+d1) * s1/s2 ) - (d2*s2/s1) * s1/s2
        #   = ( (x+d1) - (d1*s2/s1) ) * s1/s2
        #   = (x + d1 - d2*s2/s1) * s1/s2
        # thus, D = d1 - d2*s2/s1 and S = s1/s2
        factor = self.factor / other.factor
        offset = self.offset - (other.offset * other.factor / self.factor)
        return factor, offset

    @property
    def to_dict(self):
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
        for i,exponent in enumerate(p):
            base_dict[base_names[i]] = exponent
        unit_dict['base_exponents'] = base_dict
        return unit_dict

    @property
    def to_json(self):
        """Export unit as JSON


        Notes
        -----
        Give unit and iterate over base units

        """

        json_unit = json.dumps({'PhysicalUnit': self.to_dict})
        return json_unit

    @staticmethod
    def from_dict(unit_dict):
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
        Current implementation: throw exception of unit has not already been defined
        """
        u = findunit(unit_dict['name'])
        if u.to_dict != unit_dict:
            raise UnitError(f'Unit {str(u)} does not correspond to given dict')
        return u

    @staticmethod
    def from_json(json_unit):
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


unit_table = {}
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
        unece_code=None))
addunit(PhysicalUnit('currency', 1., [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        url='https://en.wikipedia.org/wiki/Currency', verbosename='Currency',
        unece_code=None))



def add_composite_unit(name, factor, units, offset=0, verbosename='', prefixed=False, baseunit=None, url=''):
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
    baseunit : PhysicalUnit
        Base unit
    url: str
        A URL linking to more information about the unit

    Returns
    -------
    str
        Name of new unit

    Raises
    ------
    KeyError
        If unit already exists

    """
    if name in unit_table:
        raise KeyError(f'Unit {name} already defined')
    baseunit = eval(units, unit_table)
    for cruft in ['__builtins__', '__args__']:
        try:
            del unit_table[cruft]
        except KeyError:
            pass
    newunit = copy.deepcopy(baseunit)
    newunit.set_name(name)
    newunit.verbosename = verbosename
    if prefixed is True:
        newunit.baseunit = baseunit
    else:
        newunit.baseunit = newunit
    newunit.prefixed = prefixed
    newunit.url = url
    newunit.factor = newunit.factor * factor
    newunit.offset = newunit.offset + offset
    unit_table[name] = newunit
    return name
