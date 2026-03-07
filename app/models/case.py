"""Beam case definition — the single input for the entire analysis."""

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from app.models.loads import LoadCombinations, PointLoad, TrapezoidalLoad, UniformLoad
from app.models.materials import TimberMaterial
from app.models.sections import RectangularSection
from app.models.supports import SupportType


class BeamCase(BaseModel):
    """Complete beam case definition — single input for the entire analysis."""

    length: float = Field(gt=0)
    """Beam span in m"""
    support_left: SupportType = SupportType.PINNED
    """Left end support"""
    support_right: SupportType = SupportType.ROLLER_X
    """Right end support"""
    section: RectangularSection
    material: TimberMaterial = Field(default_factory=TimberMaterial)
    point_loads: list[PointLoad] = Field(default_factory=list)
    uniform_loads: list[UniformLoad] = Field(default_factory=list)
    trapezoidal_loads: list[TrapezoidalLoad] = Field(default_factory=list)
    combos: LoadCombinations = Field(default_factory=LoadCombinations)
    n_points: int = Field(default=200, ge=20)
    """Number of points for diagram output"""

    @model_validator(mode="after")
    def check_load_positions(self) -> BeamCase:
        """Ensure all load positions are within the beam span."""
        L = self.length
        for pl in self.point_loads:
            if pl.x > L:
                raise ValueError(f"Point load at x={pl.x} exceeds beam length L={L}")
        for ul in self.uniform_loads:
            x1 = ul.x1 if ul.x1 is not None else 0.0
            x2 = ul.x2 if ul.x2 is not None else L
            if x1 > L or x2 > L:
                raise ValueError(
                    f"Uniform load range [{x1}, {x2}] exceeds beam length L={L}"
                )
        for tl in self.trapezoidal_loads:
            x1 = tl.x1 if tl.x1 is not None else 0.0
            x2 = tl.x2 if tl.x2 is not None else L
            if x1 > L or x2 > L:
                raise ValueError(
                    f"Trapezoidal load range [{x1}, {x2}] exceeds beam length L={L}"
                )
        return self
