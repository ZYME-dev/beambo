"""Analytical formulas for propped cantilever (fixed at x=0, roller at x=L).

Sign convention (matches Pynite):
  - w, P: negative = downward (Fy direction)
  - V: positive = upward shear on left face
  - M: positive = hogging (Pynite Mz convention)
  - delta: positive = upward displacement

Derived by superposition on the primary cantilever structure.
"""

from __future__ import annotations

import numpy as np

# -- Uniform load over full span ----------------------------------------


def uniform_load_shear(w: float, L: float, x: np.ndarray) -> np.ndarray:
    """V(x) for uniform load w over full span."""
    return w * (x - 5 * L / 8)


def uniform_load_moment(w: float, L: float, x: np.ndarray) -> np.ndarray:
    """M(x) for uniform load w over full span."""
    return w * (L - x) * (4 * x - L) / 8


def uniform_load_deflection(
    w: float, L: float, E: float, I: float, x: np.ndarray
) -> np.ndarray:
    """delta(x) for uniform load w over full span."""
    return w * x**2 * (3 * L - 2 * x) * (L - x) / (48 * E * I)


# -- Point load at arbitrary position a from fixed end ------------------


def _roller_reaction(P: float, a: float, L: float) -> float:
    """Roller reaction R_B from compatibility on the cantilever."""
    return -P * a**2 * (3 * L - a) / (2 * L**3)


def point_load_shear(P: float, a: float, L: float, x: np.ndarray) -> np.ndarray:
    """V(x) for point load P at distance a from fixed end."""
    R_B = _roller_reaction(P, a, L)
    R_A = -P - R_B
    return np.where(x < a, R_A, R_A + P)


def point_load_moment(P: float, a: float, L: float, x: np.ndarray) -> np.ndarray:
    """M(x) for point load P at distance a from fixed end."""
    R_B = _roller_reaction(P, a, L)
    left = -P * (a - x) - R_B * (L - x)
    right = -R_B * (L - x)
    return np.where(x <= a, left, right)


def point_load_deflection(
    P: float, a: float, L: float, E: float, I: float, x: np.ndarray
) -> np.ndarray:
    """delta(x) for point load P at distance a from fixed end."""
    R_B = _roller_reaction(P, a, L)
    coeff = 1 / (6 * E * I)
    # Cantilever deflection due to P at a
    left_P = P * x**2 * (3 * a - x) * coeff
    right_P = P * a**2 * (3 * x - a) * coeff
    # Cantilever deflection due to R_B at tip
    tip_d = R_B * x**2 * (3 * L - x) * coeff
    return np.where(x <= a, left_P + tip_d, right_P + tip_d)
