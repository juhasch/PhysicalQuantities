Changelog
=========

All notable changes to this project should be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres (at least as of 0.3.0!) to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).


1.3.0
-----

- Introduce fractdict to handle fractions in units.
- Refactor arithmetic operations (`*`, `/`, `//`) in `PhysicalUnit` and `PhysicalQuantity` for type consistency and Python 3 compatibility.
- Resolve circular imports between `unit.py` and `quantity.py` via local imports.
- Correct logic in `PhysicalUnit.is_power` and `dBQuantity` comparison methods for proper dimensional handling.
- Fix `PhysicalUnit.__hash__` to enable unit/quantity hashing and restore `@lru_cache` on `findunit`.
- Improve error handling and type checks in `findunit` and `add_composite_unit`.
- Correct unit handling and type checking in `numpywrapper.linspace`.
- Update tests to match corrected behavior and expected exceptions.
- Improve code readability (f-strings, type checks).



1.1.1
-----

- Cleanup
- Add more units
  [#133](https://github.com/juhasch/PhysicalQuantities/pull/133)
  [@juhasch](https://github.com/juhasch)
- Add currencies and retrieve exchange rates from `forex-python` 
  [#134](https://github.com/juhasch/PhysicalQuantities/pull/134)
  [@juhasch](https://github.com/juhasch)
- Fix ReadTheDocs build

1.1.0
-----

- Added CHANGELOG.md
   [#100](https://github.com/juhasch/PhysicalQuantities/pull/100)
   [@juhasch](https://github.com/juhasch)
- Move from regular expression to tokenize in IPython extension 
   [#98](https://github.com/juhasch/PhysicalQuantities/pull/98)
   [@juhasch](https://github.com/juhasch)
