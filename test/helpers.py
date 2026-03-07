"""Test assertion utilities."""

from __future__ import annotations

import numpy as np


def assert_allclose(
    actual: np.ndarray,
    expected: np.ndarray,
    rtol: float = 0.01,
    atol: float = 1e-6,
    name: str = "",
) -> None:
    """Assert arrays are close within relative tolerance.

    Uses relative tolerance where |expected| is significant,
    falls back to absolute tolerance near zero.
    """
    actual = np.asarray(actual)
    expected = np.asarray(expected)

    if actual.shape != expected.shape:
        raise AssertionError(
            f"{name}: shape mismatch: {actual.shape} vs {expected.shape}"
        )

    abs_diff = np.abs(actual - expected)
    abs_expected = np.abs(expected)

    # Use relative where expected is significant, absolute otherwise
    threshold = np.maximum(rtol * abs_expected, atol)
    failures = abs_diff > threshold

    if not np.any(failures):
        return

    # Build error message
    idx = np.argmax(abs_diff)
    max_abs = abs_diff.flat[idx]
    max_rel = (
        max_abs / abs_expected.flat[idx]
        if abs_expected.flat[idx] > atol
        else float("inf")
    )
    n_fail = int(np.sum(failures))
    label = f" [{name}]" if name else ""
    raise AssertionError(
        f"Arrays not close{label}: "
        f"{n_fail}/{actual.size} points exceed tolerance. "
        f"Max abs diff: {max_abs:.6g} at index {idx} "
        f"(actual={actual.flat[idx]:.6g}, expected={expected.flat[idx]:.6g}, "
        f"rel={max_rel:.4g}). rtol={rtol}, atol={atol}"
    )
