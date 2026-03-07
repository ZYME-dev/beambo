"""Shared fixtures for formula tests."""

from __future__ import annotations

from app.models import RectangularSection

SECTION = RectangularSection(b=200, h=400)
L = 6.0
N_POINTS = 200
_GRADE = "C24"


def get_EI() -> tuple[float, float]:
    """Return (E in kN/m², I in m⁴) for the test section and grade."""
    from eurocodepy.ec5 import TimberClass as ec5_timber_class

    timber = ec5_timber_class(_GRADE)
    E = timber.E0mean * 1e3  # MPa -> kN/m²
    I = SECTION.Iz  # strong axis (resists Fy bending)
    return E, I


def els_combo(results):
    """Return the first ELS combo name from results."""
    for name, typ in zip(results.combo_names, results.combo_types):
        if typ == "ELS":
            return name
    raise ValueError("No ELS combo found")
