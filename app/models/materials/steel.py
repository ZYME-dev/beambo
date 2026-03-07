"""Steel material model and grade enum (EC3)."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class SteelGrade(StrEnum):
    """Structural steel grades per EC3."""

    S235 = "S235"
    S275 = "S275"
    S355 = "S355"
    S450 = "S450"


class SteelMaterial(BaseModel):
    """Steel material definition per EC3."""

    grade: SteelGrade = SteelGrade.S355
    """Steel grade"""
