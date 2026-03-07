"""Eurocode load combination factors."""

from __future__ import annotations

from pydantic import BaseModel


class LoadCombinations(BaseModel):
    """Eurocode load combination factors (EN 1990 — French NA defaults)."""

    gamma_G_unfav: float = 1.35
    """gamma_G unfavorable"""
    gamma_G_fav: float = 1.0
    """gamma_G favorable"""
    gamma_Q: float = 1.5
    """gamma_Q"""
    psi_0_Q: float = 0.7
    """psi_0 for variable loads (habitation)"""
    psi_1_Q: float = 0.5
    """psi_1 for variable loads"""
    psi_2_Q: float = 0.3
    """psi_2 for variable loads"""
    wnet_limit_ratio: float = 250.0
    """L/xxx limit for net deflection (ELS char.)"""
    wfin_limit_ratio: float = 200.0
    """L/xxx limit for final deflection (ELS QP)"""
