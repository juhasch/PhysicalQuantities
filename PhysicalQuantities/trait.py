""" PhysicalTrait class definition

"""

from traitlets import TraitError, TraitType

__all__ = ['PhysicalTrait']


class PhysicalTrait(TraitType):
    """ Physical Trait - Object with physical traits like unit, etc.

    """

    def __init__(self):
        """There are two constructor calling patterns

        Parameters
        ----------
        value: any
            value of the quantity

        unit: string or PhysicalUnit class
            unit of the quantity

        >>> PhysicalQuantity(1, 'V')
        """
        ip = get_ipython()
        if ip is not None:
            self.ptformatter = ip.display_formatter.formatters['text/plain']
        else:
            self.ptformatter = None
        self.format = ''  # display format for number to string conversion
        self.value = value
        self.unit = findunit(unit)

    def to_xarray(self):


    def to_json(self):
        """"""
        return

    def from_json(self):
        """"""
        return
