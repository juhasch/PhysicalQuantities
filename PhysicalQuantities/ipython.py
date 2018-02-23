""" IPython extension for physical quantity input"""

import io
import tokenize
from tokenize import NAME, NUMBER, OP

from IPython.core.inputtransformer import StatelessInputTransformer

import PhysicalQuantities


@StatelessInputTransformer.wrap
def _transform(line):

    g = tokenize.tokenize(io.BytesIO(line.encode('utf-8')).readline)
    val = []
    num = []
    for toknum, tokval, _, _, _ in g:
        val.append(tokval)
        num.append(toknum)

    result = []
    i = 0
    while i < len(num):
        lo = slice(i, i + 4)
        sh = slice(i, i + 2)
        if num[lo] == [NUMBER, NAME, OP, NAME]:
            result.append((num[i], val[i]))
            newtokval = '* pq.' + val[i+1]
            result.append((num[i+1], newtokval))
            result.append((num[i+2], val[i+2]))
            newtokval = ' pq.' + val[i+3]
            result.append((num[i+3], newtokval))
            i += 4
        elif num[sh] == [NUMBER, NAME]:
            result.append((num[i], val[i]))
            newtokval = '* pq.' + val[i+1]
            result.append((num[i+1], newtokval))
            i += 2
        else:
            result.append((num[i], val[i]))
            i += 1

    line = tokenize.untokenize(result).decode('utf-8')
    return line


__transformer = _transform()


def load_ipython_extension(ip):  # pragma: no cover
    global __transformer
    ip.input_transformer_manager.logical_line_transforms.insert(0, __transformer)
    ip.user_ns['pq'] = PhysicalQuantities.q

def unload_ipython_extension(ip):  # pragma: no cover
    global __transformer
    if type(__transformer) is StatelessInputTransformer:
        ip.input_transformer_manager.logical_line_transforms.remove(__transformer)
        ip.user_ns.pop('pq')
