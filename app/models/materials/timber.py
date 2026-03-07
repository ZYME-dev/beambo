"""Timber material model and grade enum (EC5)."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel


class TimberGrade(StrEnum):
    """Available timber grades from eurocodepy database."""

    C16 = "C16"
    C18 = "C18"
    C24 = "C24"
    C30 = "C30"
    D24 = "D24"
    D30 = "D30"
    D40 = "D40"
    D50 = "D50"
    D60 = "D60"
    D70 = "D70"
    GL20h = "GL20h"
    GL22h = "GL22h"
    GL24h = "GL24h"
    GL26h = "GL26h"
    GL28h = "GL28h"
    GL30h = "GL30h"
    GL32h = "GL32h"
    GL20c = "GL20c"
    GL22c = "GL22c"
    GL24c = "GL24c"
    GL26c = "GL26c"
    GL28c = "GL28c"
    GL30c = "GL30c"
    GL32c = "GL32c"


class TimberMaterial(BaseModel):
    """Timber material definition per EC5."""

    grade: TimberGrade = TimberGrade.C24
    """Timber grade"""
    service_class: Literal[1, 2, 3] = 1
    """Service class (1, 2, or 3)"""
    load_duration_G: Literal[
        "Permanent",
        "LongDuration",
        "MediumDuration",
        "ShortDuration",
        "Instantaneous",
    ] = "Permanent"
    """Load duration class for permanent loads (G)"""
    load_duration_Q: Literal[
        "Permanent",
        "LongDuration",
        "MediumDuration",
        "ShortDuration",
        "Instantaneous",
    ] = "MediumDuration"
    """Load duration class for variable loads (Q)"""
