"""Load case enum and load type models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, field_validator


class LoadCase(StrEnum):
    """Load case label for Pynite."""

    G = "G"
    Q = "Q"


class PointLoad(BaseModel):
    """Point load applied to the beam."""

    P: float
    """Load magnitude in kN (negative = downward)"""
    x: float
    """Distance from left end in m"""
    case: LoadCase = LoadCase.G

    @field_validator("x")
    @classmethod
    def x_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Position x must be >= 0")
        return v


class UniformLoad(BaseModel):
    """Uniform distributed load over part or all of the beam."""

    w: float
    """Load intensity in kN/m (negative = downward)"""
    x1: float | None = None
    """Start position in m (None = 0)"""
    x2: float | None = None
    """End position in m (None = L)"""
    case: LoadCase = LoadCase.G


class TrapezoidalLoad(BaseModel):
    """Linearly varying distributed load (trapezoidal)."""

    w1: float
    """Intensity at start in kN/m (negative = downward)"""
    w2: float
    """Intensity at end in kN/m (negative = downward)"""
    x1: float | None = None
    """Start position in m (None = 0)"""
    x2: float | None = None
    """End position in m (None = L)"""
    case: LoadCase = LoadCase.G
