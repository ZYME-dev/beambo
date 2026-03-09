"""Brice — Simply supported C18 timber beam, 5.2m span, entraxe 0.5m."""

from app.models import (
    BeamCase,
    LoadCase,
    RectangularSection,
    TimberGrade,
    TimberMaterial,
    UniformLoad,
)

CASE = BeamCase(
    length=5.2,
    section=RectangularSection(b=60, h=200),
    material=TimberMaterial(
        grade=TimberGrade.C18,
        service_class=1,
        load_duration_G="Permanent",
        load_duration_Q="MediumDuration",
    ),
    uniform_loads=[
        # G1: 50 kg/m² × 0.5m entraxe = 0.25 kN/m (full span)
        UniformLoad(w=-0.25, case=LoadCase.G),
        # G2: 100 kg/m² × 0.5m entraxe = 0.50 kN/m (x = 0 to 2.0m)
        UniformLoad(w=-0.50, x1=0.0, x2=2.0, case=LoadCase.G),
        # Q1: 150 kg/m² × 0.5m entraxe = 0.75 kN/m (x = 2.0m to L)
        UniformLoad(w=-0.75, x1=2.0, case=LoadCase.Q),
        # Q2: 400 kg/m² × 0.5m entraxe = 2.0 kN/m (x = 0 to 2.0m)
        UniformLoad(w=-2.0, x1=0.0, x2=2.0, case=LoadCase.Q),
    ],
)
