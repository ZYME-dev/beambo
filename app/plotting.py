"""Beam analysis plotting functions."""

from __future__ import annotations

import matplotlib.pyplot as plt

from app.models import BeamCase, BeamResults

ENV_LABEL = "ELU envelope"


def _combo_names_by_type(results: BeamResults, typ: str) -> list[str]:
    return [n for n, t in zip(results.combo_names, results.combo_types) if t == typ]


def plot_diagrams(
    case: BeamCase,
    results: BeamResults,
    save_path: str | None = None,
):
    """Plot N, V, M diagrams for all combos + ELU envelope."""

    x = results.x
    elu_names = _combo_names_by_type(results, "ELU")
    els_names = _combo_names_by_type(results, "ELS")

    sec = case.section
    fig, axes = plt.subplots(4, 1, figsize=(14, 16), sharex=True)
    title = (
        f"Beam Analysis — L={case.length}m, "
        f"{sec.b:.0f}x{sec.h:.0f}mm, {case.material.grade}"
    )
    fig.suptitle(title, fontsize=14, fontweight="bold")

    # Axial force N
    ax = axes[0]
    for cname in elu_names:
        ax.plot(x, results.N[cname], label=cname, linewidth=0.8)
    ax.fill_between(
        x,
        results.N_min,
        results.N_max,
        alpha=0.15,
        color="blue",
        label=ENV_LABEL,
    )
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_ylabel("N (kN)")
    ax.set_title("Axial Force (N)")
    ax.legend(fontsize=7, loc="best")
    ax.grid(True, alpha=0.3)

    # Shear V
    ax = axes[1]
    for cname in elu_names:
        ax.plot(x, results.V[cname], label=cname, linewidth=0.8)
    ax.fill_between(
        x,
        results.V_min,
        results.V_max,
        alpha=0.15,
        color="red",
        label=ENV_LABEL,
    )
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_ylabel("V (kN)")
    ax.set_title("Shear Force (V)")
    ax.legend(fontsize=7, loc="best")
    ax.grid(True, alpha=0.3)

    # Bending Moment M
    ax = axes[2]
    for cname in elu_names:
        ax.plot(x, results.M[cname], label=cname, linewidth=0.8)
    ax.fill_between(
        x,
        results.M_min,
        results.M_max,
        alpha=0.15,
        color="green",
        label=ENV_LABEL,
    )
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_ylabel("M (kN*m)")
    ax.set_title("Bending Moment (M)")
    ax.legend(fontsize=7, loc="best")
    ax.grid(True, alpha=0.3)
    ax.invert_yaxis()

    # Deflection
    ax = axes[3]
    for cname in els_names:
        ax.plot(
            x,
            results.delta[cname] * 1000,
            label=cname,
            linewidth=0.8,
        )
    L = case.length
    limit_char = L * 1000 / case.combos.wnet_limit_ratio
    limit_label = f"L/{case.combos.wnet_limit_ratio:.0f}"
    ax.axhline(
        -limit_char,
        color="red",
        linestyle="--",
        linewidth=0.7,
        label=limit_label,
    )
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_ylabel("delta (mm)")
    ax.set_xlabel("Position along beam (m)")
    ax.set_title("Deflection (ELS)")
    ax.legend(fontsize=7, loc="best")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  -> Diagrams saved to {save_path}")
    else:
        plt.show()


def plot_envelope(
    case: BeamCase,
    results: BeamResults,
    save_path: str | None = None,
):
    """Plot ELU envelope diagrams only (N, V, M)."""

    x = results.x
    sec = case.section

    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
    title = (
        f"ELU Envelope — L={case.length}m, "
        f"{sec.b:.0f}x{sec.h:.0f}mm, {case.material.grade}"
    )
    fig.suptitle(title, fontsize=14, fontweight="bold")

    for ax, label, ymax, ymin, unit, color in [
        (axes[0], "N", results.N_max, results.N_min, "kN", "steelblue"),
        (axes[1], "V", results.V_max, results.V_min, "kN", "indianred"),
        (axes[2], "M", results.M_max, results.M_min, "kN*m", "seagreen"),
    ]:
        ax.fill_between(x, ymin, ymax, alpha=0.3, color=color)
        ax.plot(x, ymax, color=color, linewidth=1.2, label="Max")
        ax.plot(
            x,
            ymin,
            color=color,
            linewidth=1.2,
            linestyle="--",
            label="Min",
        )
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_ylabel(f"{label} ({unit})")
        ax.set_title(f"{label} — ELU Envelope")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    axes[2].invert_yaxis()
    axes[2].set_xlabel("Position along beam (m)")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  -> Envelope saved to {save_path}")
    else:
        plt.show()
