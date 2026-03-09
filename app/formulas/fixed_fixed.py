"""Analytical formulas for fixed-fixed beam (encastré, both ends fixed).

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
    return -w * (L**2 - 6 * L * x + 6 * x**2) / 12


def uniform_load_deflection(
    w: float, L: float, E: float, I: float, x: np.ndarray
) -> np.ndarray:
    """delta(x) for uniform load w over full span."""
    return w * x**2 * (L - x) ** 2 / (24 * E * I)


# -- Point load at arbitrary position a from left end -------------------


def point_load_shear(P: float, a: float, L: float, x: np.ndarray) -> np.ndarray:
    """V(x) for point load P at distance a from left."""
    b = L - a
    R_A = -P * b**2 * (3 * a + b) / L**3
    return np.where(x < a, R_A, R_A + P)


def point_load_moment(P: float, a: float, L: float, x: np.ndarray) -> np.ndarray:
    """M(x) for point load P at distance a from left."""
    b = L - a
    M_A = P * a * b**2 / L**2
    R_A = -P * b**2 * (3 * a + b) / L**3
    left = -(M_A + R_A * x)
    right = -(M_A + R_A * x + P * (x - a))
    return np.where(x <= a, left, right)


def point_load_deflection(
    P: float, a: float, L: float, E: float, I: float, x: np.ndarray
) -> np.ndarray:
    """delta(x) for point load P at distance a from left."""
    b = L - a
    coeff = P / (6 * E * I * L**3)
    left = coeff * b**2 * x**2 * (3 * a * L - x * (3 * a + b))
    right = coeff * a**2 * (L - x) ** 2 * (3 * b * L - (L - x) * (3 * b + a))
    return np.where(x <= a, left, right)
