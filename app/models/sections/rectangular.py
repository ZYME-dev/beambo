"""Rectangular cross-sections (solid and hollow)."""

from __future__ import annotations

from pydantic import BaseModel, field_validator, model_validator


class RectangularSection(BaseModel):
    """Solid rectangular cross-section (dimensions in mm)."""

    b: float
    """Width in mm"""
    h: float
    """Height (depth) in mm"""

    @field_validator("b", "h")
    @classmethod
    def positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Section dimensions must be > 0")
        return v

    @property
    def b_m(self) -> float:
        """Width in meters."""
        return self.b / 1000.0

    @property
    def h_m(self) -> float:
        """Height in meters."""
        return self.h / 1000.0

    @property
    def A(self) -> float:
        """Area in m²."""
        return self.b_m * self.h_m

    @property
    def Iy(self) -> float:
        """Second moment of area about y-axis in m⁴ (weak axis)."""
        return self.h_m * self.b_m**3 / 12.0

    @property
    def Iz(self) -> float:
        """Second moment of area about z-axis in m⁴ (strong axis)."""
        return self.b_m * self.h_m**3 / 12.0

    @property
    def J(self) -> float:
        """Torsional constant (Saint-Venant) in m⁴."""
        a = max(self.b_m, self.h_m) / 2.0
        b = min(self.b_m, self.h_m) / 2.0
        return a * b**3 * (16.0 / 3.0 - 3.36 * b / a * (1 - b**4 / (12 * a**4)))


class HollowRectangularSection(BaseModel):
    """Hollow rectangular cross-section (dimensions in mm)."""

    b: float
    """Outer width in mm"""
    h: float
    """Outer height (depth) in mm"""
    t: float
    """Wall thickness in mm"""

    @field_validator("b", "h", "t")
    @classmethod
    def positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Section dimensions must be > 0")
        return v

    @model_validator(mode="after")
    def thickness_fits(self) -> HollowRectangularSection:
        """Ensure wall thickness is less than half the smallest dimension."""
        if self.t >= min(self.b, self.h) / 2:
            raise ValueError("Wall thickness must be < half the smallest dimension")
        return self

    @property
    def b_m(self) -> float:
        """Outer width in meters."""
        return self.b / 1000.0

    @property
    def h_m(self) -> float:
        """Outer height in meters."""
        return self.h / 1000.0

    @property
    def t_m(self) -> float:
        """Wall thickness in meters."""
        return self.t / 1000.0

    @property
    def b_inner(self) -> float:
        """Inner width in meters."""
        return self.b_m - 2 * self.t_m

    @property
    def h_inner(self) -> float:
        """Inner height in meters."""
        return self.h_m - 2 * self.t_m

    @property
    def A(self) -> float:
        """Area in m²."""
        return self.b_m * self.h_m - self.b_inner * self.h_inner

    @property
    def Iy(self) -> float:
        """Second moment of area about y-axis in m⁴ (weak axis)."""
        return (self.h_m * self.b_m**3 - self.h_inner * self.b_inner**3) / 12.0

    @property
    def Iz(self) -> float:
        """Second moment of area about z-axis in m⁴ (strong axis)."""
        return (self.b_m * self.h_m**3 - self.b_inner * self.h_inner**3) / 12.0

    @property
    def J(self) -> float:
        """Torsional constant for thin-walled hollow rectangle in m⁴."""
        b_mid = self.b_m - self.t_m
        h_mid = self.h_m - self.t_m
        Am = b_mid * h_mid
        perimeter = 2 * (b_mid + h_mid)
        return 4 * Am**2 * self.t_m / perimeter
