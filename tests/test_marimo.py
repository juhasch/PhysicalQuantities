import sys
import pytest

pytestmark = pytest.mark.skipif(
    pytest.importorskip('marimo', reason='marimo not installed') is None,
    reason='marimo not installed'
)

def test_marimo_physics_magic_enables(monkeypatch):
    # Importing should set up the environment and enable magic
    import importlib
    import PhysicalQuantities.marimo
    from PhysicalQuantities.marimo import _physics_transformer

    # Test a simple transformation
    code = 'a = 5 m + 10 cm'
    transformed = _physics_transformer.transform_code(code)
    assert 'pq' in transformed
    assert '5' in transformed and 'm' in transformed
    assert '10' in transformed and 'cm' in transformed 