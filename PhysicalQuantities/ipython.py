""" IPython extension for physical quantity input"""

from typing import List
import PhysicalQuantities
from .transform import transform_line

# Flag for multiline comments
WITHIN_COMMENT = False


def transform(lines: List[str]) -> List[str]:
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
    ip.input_transformers_cleanup.append(transform)
    ip.user_ns['pq'] = PhysicalQuantities.q


def unload_ipython_extension(ip):  # pragma: no cover
    ip.input_transformers_cleanup.remove(transform)
    ip.user_ns.pop('pq')
