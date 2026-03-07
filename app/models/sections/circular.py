"""Circular cross-sections (solid and hollow)."""

from __future__ import annotations

import math

from pydantic import BaseModel, field_validator, model_validator


class CircularSection(BaseModel):
    """Solid circular cross-section (dimensions in mm)."""

    d: float
    """Diameter in mm"""

    @field_validator("d")
    @classmethod
    def positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Diameter must be > 0")
        return v

    @property
    def d_m(self) -> float:
        """Diameter in meters."""
        return self.d / 1000.0

    @property
    def r_m(self) -> float:
        """Radius in meters."""
        return self.d_m / 2.0

    @property
    def A(self) -> float:
        """Area in m²."""
        return math.pi * self.r_m**2

    @property
    def Iy(self) -> float:
        """Second moment of area about y-axis in m⁴."""
        return math.pi * self.d_m**4 / 64.0

    @property
    def Iz(self) -> float:
        """Second moment of area about z-axis in m⁴."""
        return self.Iy

    @property
    def J(self) -> float:
        """Torsional constant (polar moment) in m⁴."""
        return math.pi * self.d_m**4 / 32.0


class HollowCircularSection(BaseModel):
    """Hollow circular cross-section (dimensions in mm)."""

    d: float
    """Outer diameter in mm"""
    t: float
    """Wall thickness in mm"""

    @field_validator("d", "t")
    @classmethod
    def positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Section dimensions must be > 0")
        return v

    @model_validator(mode="after")
    def thickness_fits(self) -> HollowCircularSection:
        """Ensure wall thickness is less than half the diameter."""
        if self.t >= self.d / 2:
            raise ValueError("Wall thickness must be < half the diameter")
        return self

    @property
    def d_m(self) -> float:
        """Outer diameter in meters."""
        return self.d / 1000.0

    @property
    def d_inner(self) -> float:
        """Inner diameter in meters."""
        return self.d_m - 2 * self.t / 1000.0

    @property
    def A(self) -> float:
        """Area in m²."""
        return math.pi * (self.d_m**2 - self.d_inner**2) / 4.0

    @property
    def Iy(self) -> float:
        """Second moment of area about y-axis in m⁴."""
        return math.pi * (self.d_m**4 - self.d_inner**4) / 64.0

    @property
    def Iz(self) -> float:
        """Second moment of area about z-axis in m⁴."""
        return self.Iy

    @property
    def J(self) -> float:
        """Torsional constant (polar moment) in m⁴."""
        return math.pi * (self.d_m**4 - self.d_inner**4) / 32.0
