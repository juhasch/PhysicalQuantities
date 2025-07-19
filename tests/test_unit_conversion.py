import pytest
from PhysicalQuantities.unit import PhysicalUnit, convertvalue, unit_table, add_composite_unit, UnitError
from PhysicalQuantities import q # Import the main registry

# Retrieve units from the registry
K = q.K.unit
degC = q.degC.unit
m = q.m.unit
km = q.km.unit


def test_kelvin_to_celsius_conversion():
    """Test conversion from Kelvin to Celsius."""
    assert convertvalue(273.15, K, degC) == pytest.approx(0.0)
    assert convertvalue(373.15, K, degC) == pytest.approx(100.0)
    assert convertvalue(0, K, degC) == pytest.approx(-273.15)
    assert convertvalue(300, K, degC) == pytest.approx(26.85)

def test_celsius_to_kelvin_conversion():
    """Test conversion from Celsius to Kelvin."""
    assert convertvalue(0, degC, K) == pytest.approx(273.15)
    assert convertvalue(100, degC, K) == pytest.approx(373.15)
    assert convertvalue(-273.15, degC, K) == pytest.approx(0.0)
    assert convertvalue(26.85, degC, K) == pytest.approx(300)

def test_no_offset_conversion():
    """Test conversion between units without offsets (regression check)."""
    assert convertvalue(1000, m, km) == pytest.approx(1.0)
    assert convertvalue(1, km, m) == pytest.approx(1000.0)
    assert convertvalue(5, m, m) == pytest.approx(5.0)

def test_incompatible_units_conversion():
    """Test conversion attempt between incompatible units."""
    with pytest.raises(UnitError, match='Incompatible unit'):
        convertvalue(10, K, m)
    with pytest.raises(UnitError, match='Incompatible unit'):
        convertvalue(5, degC, m)

def test_conversion_tuple_kelvin_celsius():
    """Test the internal conversion_tuple_to directly for K/degC."""
    # K to degC: y = x * F + O => degC = K * 1.0 + (-273.15)
    factor, offset = K.conversion_tuple_to(degC)
    assert factor == pytest.approx(1.0)
    assert offset == pytest.approx(-273.15)

    # degC to K: y = x * F + O => K = degC * 1.0 + 273.15
    factor, offset = degC.conversion_tuple_to(K)
    assert factor == pytest.approx(1.0)
    assert offset == pytest.approx(273.15)

def test_conversion_tuple_no_offset():
    """Test the internal conversion_tuple_to directly for non-offset units."""
    # m to km: km = m * 0.001 + 0
    factor, offset = m.conversion_tuple_to(km)
    assert factor == pytest.approx(0.001)
    assert offset == pytest.approx(0.0)

    # km to m: m = km * 1000 + 0
    factor, offset = km.conversion_tuple_to(m)
    assert factor == pytest.approx(1000.0)
    assert offset == pytest.approx(0.0) 