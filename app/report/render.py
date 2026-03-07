"""Render HTML report: diagram images + Jinja2 template."""

from __future__ import annotations

import base64
import io
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from matplotlib.figure import Figure

from app.models import BeamCase, BeamResults, VerificationReport
from app.report.context import build_context

_TEMPLATE_DIR = Path(__file__).parent
_ENV = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=False,
)


def generate_report(
    case: BeamCase,
    results: BeamResults,
    report: VerificationReport,
    out_dir: Path | None = None,
) -> Path:
    """Generate an HTML report and write it to out_dir/report.html."""
    if out_dir is None:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_dir = Path("tmp") / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    ctx = build_context(case, results, report)
    ctx["now"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    ctx["diagrams_img"] = _render_diagrams(case, results)
    ctx["envelope_img"] = _render_envelope(results)

    template = _ENV.get_template("template.html.j2")
    html = template.render(ctx)

    out_path = out_dir / "report.html"
    out_path.write_text(html)
    return out_path


# ---------------------------------------------------------------------------
# Matplotlib rendering
# ---------------------------------------------------------------------------


def _fig_to_base64(fig: Figure) -> str:
    """Render a matplotlib figure to a base64-encoded PNG data URI."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{b64}"


def _render_diagrams(case: BeamCase, results: BeamResults) -> str:
    """Render N/V/M/delta diagrams, return base64 data URI."""
    x = results.x
    elu_names = [
        n for n, t in zip(results.combo_names, results.combo_types) if t == "ELU"
    ]
    els_names = [
        n for n, t in zip(results.combo_names, results.combo_types) if t == "ELS"
    ]

    sec = case.section
    fig, axes = plt.subplots(4, 1, figsize=(12, 14), sharex=True)
    fig.suptitle(
        f"L={case.length}m, {sec.b:.0f}\u00d7{sec.h:.0f}mm, {case.material.grade}",
        fontsize=12,
        fontweight="bold",
    )

    configs = [
        (axes[0], "N", "kN", results.N, results.N_min, results.N_max, "blue", False),
        (axes[1], "V", "kN", results.V, results.V_min, results.V_max, "red", False),
        (
            axes[2],
            "M",
            "kN\u00b7m",
            results.M,
            results.M_min,
            results.M_max,
            "green",
            True,
        ),
    ]
    for ax, label, unit, data, env_min, env_max, color, invert in configs:
        for cname in elu_names:
            ax.plot(x, data[cname], label=cname, linewidth=0.8)
        ax.fill_between(
            x,
            env_min,
            env_max,
            alpha=0.15,
            color=color,
            label="Envelope",
        )
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_ylabel(f"{label} ({unit})")
        ax.set_title(f"{label}")
        ax.legend(fontsize=7, loc="best")
        ax.grid(True, alpha=0.3)
        if invert:
            ax.invert_yaxis()

    # Deflection
    ax = axes[3]
    for cname in els_names:
        ax.plot(x, results.delta[cname] * 1000, label=cname, linewidth=0.8)
    limit_char = case.length * 1000 / case.combos.wnet_limit_ratio
    limit_label = f"L/{case.combos.wnet_limit_ratio:.0f}"
    ax.axhline(
        -limit_char,
        color="red",
        linestyle="--",
        linewidth=0.7,
        label=limit_label,
    )
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_ylabel("\u03b4 (mm)")
    ax.set_xlabel("Position along beam (m)")
    ax.set_title("Deflection (ELS)")
    ax.legend(fontsize=7, loc="best")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return _fig_to_base64(fig)


def _render_envelope(results: BeamResults) -> str:
    """Render ELU envelope diagrams, return base64 data URI."""
    x = results.x

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    fig.suptitle("ELU Envelope", fontsize=12, fontweight="bold")

    for ax, label, ymax, ymin, unit, color in [
        (axes[0], "N", results.N_max, results.N_min, "kN", "steelblue"),
        (axes[1], "V", results.V_max, results.V_min, "kN", "indianred"),
        (axes[2], "M", results.M_max, results.M_min, "kN\u00b7m", "seagreen"),
    ]:
        ax.fill_between(x, ymin, ymax, alpha=0.3, color=color)
        ax.plot(x, ymax, color=color, linewidth=1.2, label="Max")
        ax.plot(x, ymin, color=color, linewidth=1.2, linestyle="--", label="Min")
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_ylabel(f"{label} ({unit})")
        ax.set_title(f"{label} \u2014 ELU Envelope")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    axes[2].invert_yaxis()
    axes[2].set_xlabel("Position along beam (m)")
    plt.tight_layout()
    return _fig_to_base64(fig)
