"""Currencies

BEWARE:
  * Currency exchange rates are initially taken from the Internet, and never updated
  * Currency calculations are done using standard float, not decimal

"""
import PhysicalQuantities
from .unit import add_composite_unit
from typing import TYPE_CHECKING


try:
    if TYPE_CHECKING:
        raise ImportError
    else:
        from forex_python.converter import CurrencyRates
        from forex_python.bitcoin import BtcConverter
except ImportError:
    def CurrencyRates():
        return None

    def BtcConverter():
        return None


def get_currency_rate(reference: str, target: str):
    """
    Parameters
    ----------
    reference
        Reference currency to convert from
    target
        Currenty to convert to
    """

    c = CurrencyRates()
    return c.get_rate(reference, target)


add_composite_unit('EUR', 1.0000000001, 'currency', verbosename='Euro',
                   url='https://en.wikipedia.org/wiki/Euro')

if CurrencyRates() is not None:
    add_composite_unit('USD', get_currency_rate('USD', 'EUR'), 'currency', verbosename='US Dollar',
                       url='https://en.wikipedia.org/wiki/USD')

    add_composite_unit('GBP', get_currency_rate('GBP', 'EUR'), 'currency', verbosename='British Pound',
                       url='https://en.wikipedia.org/wiki/GPB')

    add_composite_unit('BTC', BtcConverter().get_latest_price('EUR'), 'currency', verbosename='British Pound',
                       url='https://en.wikipedia.org/wiki/GPB')


PhysicalQuantities.q.update()
