# -*- coding: utf-8 -*-
""" Load custom inputtransformer for PhysicalQuantities

    Useful when converting to IPython:

    >>> jupyter nbconvert --to python mynotebook.ipynb

    Will make sure that quantities will be converted to valid Python code

"""

from nbconvert.preprocessors import Preprocessor
from IPython.core.interactiveshell import InteractiveShell
from PhysicalQuantities.ipython import _transform

shell = InteractiveShell.instance()
shell.input_transformer_manager.logical_line_transforms.insert(0, _transform())


class InputTransformerPreprocessor(Preprocessor):
    def preprocess_cell(self, cell, resources, index):
        return cell, resources
