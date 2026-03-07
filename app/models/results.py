"""FEA results and EC5 verification report models."""

from __future__ import annotations

import numpy as np
from pydantic import BaseModel, ConfigDict, Field


class BeamResults(BaseModel):
    """Results from the Pynite FEA analysis."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    combo_names: list[str]
    combo_types: list[str]
    """'ELU' or 'ELS'"""
    x: np.ndarray

    N: dict[str, np.ndarray] = Field(default_factory=dict)
    """Per-combo axial force arrays: combo_name → np.ndarray"""
    V: dict[str, np.ndarray] = Field(default_factory=dict)
    """Per-combo shear force arrays: combo_name → np.ndarray"""
    M: dict[str, np.ndarray] = Field(default_factory=dict)
    """Per-combo bending moment arrays: combo_name → np.ndarray"""
    delta: dict[str, np.ndarray] = Field(default_factory=dict)
    """Per-combo deflection arrays: combo_name → np.ndarray"""

    N_max: np.ndarray | None = None
    N_min: np.ndarray | None = None
    V_max: np.ndarray | None = None
    V_min: np.ndarray | None = None
    M_max: np.ndarray | None = None
    M_min: np.ndarray | None = None
    delta_max: np.ndarray | None = None
    delta_min: np.ndarray | None = None


class VerificationResult(BaseModel):
    """Result of a single EC5 verification check."""

    name: str
    is_ok: bool
    ratio: float
    """Utilization ratio (<=1.0 = OK)"""
    details: str = ""


class VerificationReport(BaseModel):
    """Complete EC5 verification report."""

    checks: list[VerificationResult] = Field(default_factory=list)
    all_ok: bool = True
    summary: str = ""
