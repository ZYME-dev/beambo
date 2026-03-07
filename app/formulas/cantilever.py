"""Analytical formulas for cantilever beam (fixed at x=0, free at x=L).

Sign convention (matches Pynite):
  - w, P: negative = downward (Fy direction)
  - V: positive = upward shear on left face
  - M: positive = hogging (Pynite Mz convention)
  - delta: positive = upward displacement
"""

from __future__ import annotations

import numpy as np

# -- Uniform load over full span ----------------------------------------


def uniform_load_shear(w: float, L: float, x: np.ndarray) -> np.ndarray:
    """V(x) for uniform load w over full span."""
    return w * (x - L)


def uniform_load_moment(w: float, L: float, x: np.ndarray) -> np.ndarray:
    """M(x) for uniform load w over full span."""
    return -w * (L - x) ** 2 / 2


def uniform_load_deflection(
    w: float, L: float, E: float, I: float, x: np.ndarray
) -> np.ndarray:
    """delta(x) for uniform load w over full span."""
    return w * (x**4 - 4 * L * x**3 + 6 * L**2 * x**2) / (24 * E * I)


# -- Point load at free end (tip) ---------------------------------------


def tip_load_shear(P: float, L: float, x: np.ndarray) -> np.ndarray:
    """V(x) for point load P at free end."""
    return np.full_like(x, -P)


def tip_load_moment(P: float, L: float, x: np.ndarray) -> np.ndarray:
    """M(x) for point load P at free end."""
    return -P * (L - x)


def tip_load_deflection(
    P: float, L: float, E: float, I: float, x: np.ndarray
) -> np.ndarray:
    """delta(x) for point load P at free end."""
    return P * x**2 * (3 * L - x) / (6 * E * I)


# -- Point load at arbitrary position a from fixed end ------------------


def point_load_shear(P: float, a: float, L: float, x: np.ndarray) -> np.ndarray:
    """V(x) for point load P at distance a from fixed end."""
    return np.where(x < a, -P, 0.0)


def point_load_moment(P: float, a: float, L: float, x: np.ndarray) -> np.ndarray:
    """M(x) for point load P at distance a from fixed end."""
    return -np.where(x <= a, P * (a - x), 0.0)


def point_load_deflection(
    P: float, a: float, L: float, E: float, I: float, x: np.ndarray
) -> np.ndarray:
    """delta(x) for point load P at distance a from fixed end."""
    left = P * x**2 * (3 * a - x) / (6 * E * I)
    right = P * a**2 * (3 * x - a) / (6 * E * I)
    return np.where(x <= a, left, right)
