"""Simply supported C24 timber beam — 5m span, uniform + point loads."""

from app.models import (
    BeamCase,
    LoadCase,
    PointLoad,
    RectangularSection,
    TimberGrade,
    TimberMaterial,
    UniformLoad,
)

CASE = BeamCase(
    length=5.0,
    section=RectangularSection(b=100, h=300),
    material=TimberMaterial(
        grade=TimberGrade.C24,
        service_class=1,
        load_duration_G="Permanent",
        load_duration_Q="MediumDuration",
    ),
    uniform_loads=[
        UniformLoad(w=-2.0, case=LoadCase.G),
        UniformLoad(w=-3.5, case=LoadCase.Q),
    ],
    point_loads=[
        PointLoad(P=-5.0, x=2.5, case=LoadCase.Q),
    ],
)
