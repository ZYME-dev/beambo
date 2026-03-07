"""Analytical formulas for simply supported beam (pinned-roller).

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
    return w * (x - L / 2)


def uniform_load_moment(w: float, L: float, x: np.ndarray) -> np.ndarray:
    """M(x) for uniform load w over full span."""
    return -w * x * (x - L) / 2


def uniform_load_deflection(
    w: float, L: float, E: float, I: float, x: np.ndarray
) -> np.ndarray:
    """delta(x) for uniform load w over full span."""
    return w * x * (x**3 - 2 * L * x**2 + L**3) / (24 * E * I)


# -- Point load ----------------------------------------------------------


def point_load_shear(P: float, a: float, L: float, x: np.ndarray) -> np.ndarray:
    """V(x) for point load P at distance a from left."""
    b = L - a
    R_A = -P * b / L
    return np.where(x < a, R_A, R_A + P)


def point_load_moment(P: float, a: float, L: float, x: np.ndarray) -> np.ndarray:
    """M(x) for point load P at distance a from left."""
    b = L - a
    R_A = -P * b / L
    return -np.where(x <= a, R_A * x, R_A * x + P * (x - a))


def point_load_deflection(
    P: float, a: float, L: float, E: float, I: float, x: np.ndarray
) -> np.ndarray:
    """delta(x) for point load P at distance a from left."""
    b = L - a
    coeff_l = -P * b / (6 * L * E * I)
    left = coeff_l * x * (x**2 - L**2 + b**2)

    coeff_r = -P * a / (6 * L * E * I)
    xr = L - x
    right = coeff_r * xr * (xr**2 - L**2 + a**2)

    return np.where(x <= a, left, right)
