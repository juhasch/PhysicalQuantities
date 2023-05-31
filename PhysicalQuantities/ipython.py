""" IPython extension for physical quantity input"""

import io
import tokenize
from tokenize import NAME, NUMBER, OP, COMMENT, TokenError

from IPython import __version__
from IPython.core.inputtransformer import StatelessInputTransformer

import PhysicalQuantities
from .transform import transform_line, add_pq_prefix

# Flag for multiline comments
WITHIN_COMMENT = False


# Retain legacy input transformer
if __version__ < '7.0.0':
    global __transformer

    @StatelessInputTransformer.wrap
    def transform_legacy(line: str = ''):
        global WITHIN_COMMENT
        if line.count('"""') % 2 or line.count("'''") % 2:
            WITHIN_COMMENT = not WITHIN_COMMENT
            return

        if WITHIN_COMMENT:
            return

        string_io = io.StringIO(line)
        g = tokenize.generate_tokens(string_io.readline)

        tokenlist = []
        result: list = []
        token_type = []

        try:
            for t in g:
                tokenlist.append(t)
                token_type.append(t[0])
        except TokenError:
            pass

        i = 0
        while i < len(tokenlist):
            lo = slice(i, i + 4)
            sh = slice(i, i + 2)
            if token_type[lo] == [NUMBER, NAME, OP, NAME]:
                result.append((tokenlist[i][0], '(' + tokenlist[i + 0][1]))
                newtokval = add_pq_prefix(tokenlist[i + 1][1], '*pq.')
                result.append((tokenlist[i + 1][0], newtokval + ')'))
                result.append((tokenlist[i + 2][0], tokenlist[i + 2][1]))
                newtokval = add_pq_prefix(tokenlist[i + 3][1])
                result.append((tokenlist[i + 3][0], newtokval))
                i += 4
            elif token_type[sh] == [NUMBER, NAME]:
                if tokenlist[i + 2].string in ['**']:
                    # apply exponent only unit not number
                    result.append((tokenlist[i][0], 'PhysicalQuantity(' + tokenlist[i + 0][1]))
                    newtokval = add_pq_prefix(tokenlist[i + 1][1], ',"')
                    result.append(
                        (tokenlist[i + 1][0], newtokval + tokenlist[i + 2].string + tokenlist[i + 3].string + '")'))
                    i += 4
                else:
                    result.append((tokenlist[i][0], '(' + tokenlist[i + 0][1]))
                    newtokval = add_pq_prefix(tokenlist[i + 1][1], '*pq.')
                    result.append((tokenlist[i + 1][0], newtokval + ')'))
                    i += 2
            else:
                result.append(tokenlist[i])
                i += 1
        if token_type[0] != COMMENT:
            line = tokenize.untokenize(result)
        return line

    __transformer = transform_legacy()


def transform(lines: str):
    """
    Parameters
    ----------
    lines
        Lines where units should be replaced with valid Python code
    """
    global WITHIN_COMMENT
    result = []
    WITHIN_COMMENT = False
    for line in lines:

        if line.count('"""') % 2 or line.count("'''") % 2:
            WITHIN_COMMENT = not WITHIN_COMMENT

        if WITHIN_COMMENT:
            return lines

        transformed_line = transform_line(line)
        if transformed_line:
            result.append(transformed_line)
    return result


def load_ipython_extension(ip):  # pragma: no cover
    global WITHIN_COMMENT
    WITHIN_COMMENT = False
    if __version__ < '7.0.0':
        global __transformer
        ip.input_transformer_manager.logical_line_transforms.insert(0, __transformer)
    else:
        ip.input_transformers_cleanup.append(transform)
    ip.user_ns['pq'] = PhysicalQuantities.q


def unload_ipython_extension(ip):  # pragma: no cover
    if __version__ < '7.0.0':
        global __transformer
        if type(__transformer) is StatelessInputTransformer:
            ip.input_transformer_manager.logical_line_transforms.remove(__transformer)
    else:
        ip.input_transformers_cleanup.remove(transform)
    ip.user_ns.pop('pq')
