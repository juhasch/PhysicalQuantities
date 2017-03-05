"""
IPython extension for binary units

Author: Juergen Hasch <python@elbonia.de>
Distributed under the terms of the BSD License.  The full license is in
the file COPYING, distributed as part of this software.
"""

import re
from IPython.core.inputtransformer import StatelessInputTransformer

_units = {'Ki': 2 ** 10,
          'Mi': 2 ** 20,
          'Gi': 2 ** 30,
          'Ti': 2 ** 40,
          'Pi': 2 ** 50,
          'Ei': 2 ** 60,
          'Zi': 2 ** 70,
          'Yi': 2 ** 80,
          }

# RegEx: number + space + unit
# valid: 1Ki, 1 Ki, 1. Ki
# invalid: 1.Ki, "1 Ki"
_unit_list = '('
for x in _units.keys()[0:-1]:
    _unit_list += x + '|'
_unit_list += _units.keys()[-1] + ')'

# regex for finding units and quoted strings
number = r'-?[\d0-9.]+'
stringmatch = r'(["\'])(?:(?=(\\?))\2.)*?\1'
match = stringmatch + '|' + number + r'(\s*)' + _unit_list
line_match = re.compile(match)

# regex to match unit after it has been found using line_match
number = r'(-?[\d0-9-]+)'
match = number + r'(.\s|\s*)' + _unit_list
unit_match = re.compile(match)


def replace_inline(ml):
    """Replace an inline unit expression by valid Python code
    """
    if ml.group()[0][0] in '"\'':
        return ml.group()

    def replace_unit(mo):
        try:
            return mo.group(1) + "*" + str(_units[mo.group(3)])
        except KeyError:
            return mo.group()

    return unit_match.sub(replace_unit, ml.group())


@StatelessInputTransformer.wrap
def transform(line):
    line = line_match.sub(replace_inline, line)
    return line


__transformer = transform()


def load_ipython_extension(ip):
    global __transformer
    ip.input_transformer_manager.logical_line_transforms.insert(0, __transformer)
    print("Binary units extension activated.")


def unload_ipython_extension(ip):
    global __transformer
    if type(__transformer) is StatelessInputTransformer:
        ip.input_transformer_manager.logical_line_transforms.remove(__transformer)
    print("Binary units extension deactivated.")
