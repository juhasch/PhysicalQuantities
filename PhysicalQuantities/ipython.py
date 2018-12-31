""" IPython extension for physical quantity input"""

import io
import tokenize
from tokenize import NAME, NUMBER, OP, TokenError

import PhysicalQuantities
from PhysicalQuantities import q
from IPython.core.inputtransformer import StatelessInputTransformer
from IPython import __version__

# Flag for multiline comments
within_comment = False


def add_pq_prefix(token: str, prefix: str=' pq.') -> str:
    """Add prefix 'pq.' if valid unit was found

    Parameters
    ----------
    token
        Token representing potenitial unit name
    prefix
        Prefix to add, default is ' pq.'

    Returns
    -------
        Token with 'pq.' prefix added
    """
    if token in q.table.keys():
        return prefix + token
    return token


# Retain legacy input transformer
if __version__ < '7.2.0':
    global __transformer

    @StatelessInputTransformer.wrap
    def transform_legacy(line=''):
        print(line)
        global within_comment
        if line.count('"""') % 2 or line.count("'''") % 2:
            within_comment = not within_comment
            return

        if within_comment:
            return

        string_io = io.StringIO(line)
        g = tokenize.generate_tokens(string_io.readline)

        tokenlist = []
        result = []
        token_type = []

        try:
            for t in g:
                tokenlist.append(t)
                token_type.append(t[0])
        except TokenError:
            pass

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
                result.append((tokenlist[i][0], '(' + tokenlist[i + 0][1]))
                newtokval = add_pq_prefix(tokenlist[i + 1][1], '*pq.')
                result.append((tokenlist[i + 1][0], newtokval + ')'))
                i += 2
            else:
                result.append(tokenlist[i])
                i += 1
        line = tokenize.untokenize(result)
        return line

    __transformer = transform_legacy()


def transform_line(line=''):
    """Transform a single line by replacing inline physical units with 'pq.<unit>',
       i.e. '1m' -> '1* pq.m'
    """
    string_io = io.StringIO(line)
    g = tokenize.generate_tokens(string_io.readline)
    tokenlist = []
    result = []
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
            result.append((tokenlist[i][0], '('+tokenlist[i+0][1]))
            newtokval = add_pq_prefix(tokenlist[i+1][1], '*pq.')
            result.append((tokenlist[i+1][0], newtokval + ')'))
            result.append((tokenlist[i+2][0], tokenlist[i+2][1]))
            newtokval = add_pq_prefix(tokenlist[i+3][1])
            result.append((tokenlist[i+3][0], newtokval))
            i += 4
        elif token_type[sh] == [NUMBER, NAME]:
            result.append((tokenlist[i][0], '('+tokenlist[i+0][1]))
            newtokval = add_pq_prefix(tokenlist[i+1][1], '*pq.')
            result.append((tokenlist[i+1][0], newtokval + ')'))
            i += 2
        else:
            result.append(tokenlist[i])
            i += 1
    line = tokenize.untokenize(result)
    return line


def transform(lines):
    result = []
    for line in lines:
        global within_comment
        if line.count('"""') % 2 or line.count("'''") % 2:
            within_comment = not within_comment

        if within_comment:
            return
        transformed_line = transform_line(line)
        if transformed_line:
            result.append(transformed_line)
    return result


def load_ipython_extension(ip):  # pragma: no cover
    global within_comment
    within_comment = False
    if __version__ < '7.2.0':
        global __transformer
        ip.input_transformer_manager.logical_line_transforms.insert(0, __transformer)
    else:
        ip.input_transformers_cleanup.append(transform)
    ip.user_ns['pq'] = PhysicalQuantities.q


def unload_ipython_extension(ip):  # pragma: no cover
    if __version__ < '7.2.0':
        global __transformer
        if type(__transformer) is StatelessInputTransformer:
            ip.input_transformer_manager.logical_line_transforms.remove(__transformer)
    else:
        ip.input_transformers_cleanup.remove(transform)
    ip.user_ns.pop('pq')
