"""Build template context from analysis inputs and results."""

from __future__ import annotations

import json
import re
from typing import Any

import numpy as np
from eurocodepy.ec5 import LoadDuration, ServiceClass
from eurocodepy.ec5 import TimberClass as ec5_timber_class

from app.models import BeamCase, BeamResults, VerificationReport, VerificationResult


def build_context(
    case: BeamCase,
    results: BeamResults,
    report: VerificationReport,
) -> dict[str, Any]:
    """Build a flat dict of all values needed by the Jinja2 template."""
    sec = case.section
    mat = case.material

    crit = _critical_values(results)
    m_val, m_combo = crit.get("M_max", (0.0, ""))
    v_val, v_combo = crit.get("V_max", (0.0, ""))
    d_val, d_combo = crit.get("delta_max", (0.0, ""))
    worst_ratio = max((c.ratio for c in report.checks), default=0.0)

    return {
        # Beam definition
        "length": case.length,
        "support_left": case.support_left.value,
        "support_right": case.support_right.value,
        # Cross section
        "b": sec.b,
        "h": sec.h,
        "A_cm2": sec.A * 1e4,
        "Iz_cm4": sec.Iz * 1e8,
        "Iy_cm4": sec.Iy * 1e8,
        "Wel_z_cm3": sec.Iz / (sec.h_m / 2) * 1e6,
        # Material & design values
        "grade": str(mat.grade),
        "service_class": mat.service_class,
        **_material_design_values(mat),
        # Loads
        "loads": _load_rows(case),
        # KPI
        "m_max": abs(m_val),
        "m_combo": m_combo,
        "v_max": abs(v_val),
        "v_combo": v_combo,
        "d_max": d_val,
        "d_combo": d_combo,
        "worst_ratio": worst_ratio,
        "all_ok": report.all_ok,
        # Verification tables (split by type)
        **_pivot_checks(report),
        # Chart data (JSON for Plotly)
        "chart_data_json": _build_chart_data_json(case, results),
    }


def _critical_values(results: BeamResults) -> dict[str, tuple[float, str]]:
    """Extract critical M, V, delta across all combos."""
    crit: dict[str, tuple[float, str]] = {}

    for cname in results.combo_names:
        if cname not in results.M:
            continue
        M_abs_max = float(np.max(np.abs(results.M[cname])))
        if "M_max" not in crit or M_abs_max > abs(crit["M_max"][0]):
            idx = int(np.argmax(np.abs(results.M[cname])))
            crit["M_max"] = (float(results.M[cname][idx]), cname)

        V_abs_max = float(np.max(np.abs(results.V[cname])))
        if "V_max" not in crit or V_abs_max > abs(crit["V_max"][0]):
            idx = int(np.argmax(np.abs(results.V[cname])))
            crit["V_max"] = (float(results.V[cname][idx]), cname)

    for cname in results.combo_names:
        if cname not in results.delta:
            continue
        d_max = float(np.max(np.abs(results.delta[cname]))) * 1000
        if "delta_max" not in crit or d_max > abs(crit["delta_max"][0]):
            crit["delta_max"] = (d_max, cname)

    return crit


def _material_design_values(
    mat: Any,
) -> dict[str, Any]:
    """Compute EC5 design values for the material card."""
    from app.models.materials.timber import TimberMaterial

    assert isinstance(mat, TimberMaterial)

    sc_map = {1: ServiceClass.SC1, 2: ServiceClass.SC2, 3: ServiceClass.SC3}  # pyright: ignore[reportAttributeAccessIssue]
    ld_map = {
        "Permanent": LoadDuration.Permanent,  # pyright: ignore[reportAttributeAccessIssue]
        "LongDuration": LoadDuration.LongDuration,  # pyright: ignore[reportAttributeAccessIssue]
        "MediumDuration": LoadDuration.MediumDuration,  # pyright: ignore[reportAttributeAccessIssue]
        "ShortDuration": LoadDuration.ShortDuration,  # pyright: ignore[reportAttributeAccessIssue]
        "Instantaneous": LoadDuration.Instantaneous,  # pyright: ignore[reportAttributeAccessIssue]
    }

    timber = ec5_timber_class(mat.grade)
    sc = sc_map[mat.service_class]

    # Design values for G-only and G+Q
    timber.design_values(service_class=sc, load_duration=ld_map[mat.load_duration_G])
    kmod_g = timber.kmod
    gamma_m = timber.safety

    timber.design_values(service_class=sc, load_duration=ld_map[mat.load_duration_Q])
    kmod_q = timber.kmod
    fmd_q = timber.fmd
    fvd_q = timber.fvd

    return {
        "load_duration_G": mat.load_duration_G,
        "load_duration_Q": mat.load_duration_Q,
        "gamma_M": gamma_m,
        "kmod_G": kmod_g,
        "kmod_Q": kmod_q,
        "fmk": timber.fmk,
        "fvk": timber.fvk,
        "fmd_Q": fmd_q,
        "fvd_Q": fvd_q,
        "E0mean": timber.E0mean,
    }


def _load_rows(case: BeamCase) -> list[dict[str, str]]:
    """Build a list of load description dicts for the template."""
    rows: list[dict[str, str]] = []
    L = case.length
    # Count loads per case type for subscript numbering
    case_counters: dict[str, int] = {}

    def _next_label(case_value: str) -> str:
        case_counters[case_value] = case_counters.get(case_value, 0) + 1
        return f"{case_value}_{{{case_counters[case_value]}}}"

    for ul in case.uniform_loads:
        x1 = ul.x1 if ul.x1 is not None else 0.0
        x2 = ul.x2 if ul.x2 is not None else L
        rows.append(
            {
                "type": "Uniform",
                "magnitude": f"{ul.w:.2f} kN/m",
                "position": f"{x1:.2f} \u2013 {x2:.2f} m",
                "case": _next_label(ul.case.value),
            }
        )
    for pl in case.point_loads:
        rows.append(
            {
                "type": "Point",
                "magnitude": f"{pl.P:.2f} kN",
                "position": f"x = {pl.x:.2f} m",
                "case": _next_label(pl.case.value),
            }
        )
    for tl in case.trapezoidal_loads:
        x1 = tl.x1 if tl.x1 is not None else 0.0
        x2 = tl.x2 if tl.x2 is not None else L
        rows.append(
            {
                "type": "Trapezoidal",
                "magnitude": f"{tl.w1:.2f} \u2192 {tl.w2:.2f} kN/m",
                "position": f"{x1:.2f} \u2013 {x2:.2f} m",
                "case": _next_label(tl.case.value),
            }
        )
    return rows


def _pivot_checks(
    report: VerificationReport,
) -> dict[str, Any]:
    """Pivot flat check list into ELU and ELS combo dicts.

    Returns {"elu_combos": [...], "els_combos": [...]}.

    ELU entries have: name, bending, shear (each {ratio_pct, is_ok, details}).
    ELS entries have: name, deflection ({ratio_pct, is_ok, details, defl_mm, limit_mm}).
    """
    ordered: dict[str, dict[str, VerificationResult]] = {}
    for c in report.checks:
        parts = c.name.split(" \u2014 ", 1)
        check_type = parts[0].strip()
        combo_name = parts[1].strip() if len(parts) > 1 else c.name
        if combo_name not in ordered:
            ordered[combo_name] = {}
        ordered[combo_name][check_type] = c

    elu: list[dict[str, Any]] = []
    els: list[dict[str, Any]] = []

    for combo_name, checks in ordered.items():
        is_elu = combo_name.startswith("ELU")

        short = _strip_prefix(combo_name)
        latex = _combo_to_latex(short)
        label = _extract_label(combo_name)

        if is_elu:
            combo: dict[str, Any] = {
                "name": short,
                "label": label,
                "latex": latex,
            }
            for key in ("Bending", "Shear"):
                chk = checks.get(key)
                if chk is None:
                    combo[key.lower()] = None
                else:
                    combo[key.lower()] = {
                        "ratio_pct": chk.ratio * 100,
                        "is_ok": chk.is_ok,
                        "details": chk.details,
                    }
            elu.append(combo)
        else:
            chk = checks.get("Deflection")
            if chk is None:
                continue
            defl_mm, limit_mm = _parse_deflection(chk.details)
            els.append(
                {
                    "name": short,
                    "label": label,
                    "latex": latex,
                    "deflection": {
                        "ratio_pct": chk.ratio * 100,
                        "is_ok": chk.is_ok,
                        "details": chk.details,
                        "defl_mm": defl_mm,
                        "limit_mm": limit_mm,
                    },
                }
            )

    return {"elu_combos": elu, "els_combos": els}


def _parse_deflection(details: str) -> tuple[float, float]:
    """Extract deflection and limit values from check details text."""
    defl_mm = 0.0
    limit_mm = 0.0
    for line in details.splitlines():
        if "Max deflection:" in line:
            defl_mm = float(line.split(":")[1].strip().split()[0])
        elif "Limit" in line:
            limit_mm = float(line.split(":")[1].strip().split()[0])
    return defl_mm, limit_mm


def _strip_prefix(combo_name: str) -> str:
    """Strip 'ELU_1: ' or 'ELS_car: ' prefix, keep only the expression."""
    if ": " in combo_name:
        return combo_name.split(": ", 1)[1]
    return combo_name


def _extract_label(combo_name: str) -> str:
    """Extract the short label from a combo name.

    "ELU_1: 1.35G+1.5Q" -> "1"
    "ELS_car: 1.0G+1.0Q" -> "car"
    "ELS_freq: 1.0G+psi1Q" -> "freq"
    """
    prefix = combo_name.split(": ", 1)[0] if ": " in combo_name else combo_name
    # Strip ELU_ or ELS_ prefix
    for p in ("ELU_", "ELS_"):
        if prefix.startswith(p):
            return prefix[len(p) :]
    return prefix


def _combo_to_latex(expr: str) -> str:
    r"""Convert a combo expression to KaTeX-compatible LaTeX.

    Examples:
        "1.35G+1.5Q"   -> "1.35\,G + 1.5\,Q"
        "1.0G+psi1Q"   -> "1.0\,G + \psi_1\,Q"
        "1.0G+psi2Q"   -> "1.0\,G + \psi_2\,Q"
        "1.35G"         -> "1.35\,G"
    """
    # Replace psiN with \psi_N before splitting
    expr = re.sub(r"psi(\d)", r"\\psi_\1", expr)
    # Split on + keeping terms
    terms = expr.split("+")
    latex_terms: list[str] = []
    for term in terms:
        term = term.strip()
        # coeff + optional \psi_N + load letter: "1.35G" or "1.0\psi_1Q"
        m = re.match(r"^([\d.]+)(\\psi_\d)?([A-Z])$", term)
        if m:
            coeff, psi, load = m.group(1), m.group(2), m.group(3)
            if psi:
                latex_terms.append(f"{coeff}\\,{psi}\\,{load}")
            else:
                latex_terms.append(f"{coeff}\\,{load}")
            continue
        # \psi_N + load letter without coefficient: "psi1Q" -> "\psi_1Q"
        m = re.match(r"^(\\psi_\d)([A-Z])$", term)
        if m:
            psi, load = m.group(1), m.group(2)
            latex_terms.append(f"{psi}\\,{load}")
        else:
            latex_terms.append(term)
    return " + ".join(latex_terms)


def _build_chart_data_json(case: BeamCase, results: BeamResults) -> str:
    """Build JSON string with all data needed for Plotly charts."""
    x = results.x.tolist()

    elu_names = [
        n for n, t in zip(results.combo_names, results.combo_types) if t == "ELU"
    ]
    els_names = [
        n for n, t in zip(results.combo_names, results.combo_types) if t == "ELS"
    ]

    def _arr(a: np.ndarray | None) -> list[float]:
        return a.tolist() if a is not None else []

    elu_series: dict[str, dict[str, list[float]]] = {}
    for cname in elu_names:
        elu_series[cname] = {
            "N": results.N[cname].tolist() if cname in results.N else [],
            "V": results.V[cname].tolist() if cname in results.V else [],
            "M": results.M[cname].tolist() if cname in results.M else [],
        }

    els_series: dict[str, dict[str, list[float]]] = {}
    for cname in els_names:
        if cname in results.delta:
            els_series[cname] = {
                "delta_mm": (results.delta[cname] * 1000).tolist(),
            }

    limit_mm = case.length * 1000 / case.combos.wnet_limit_ratio
    limit_label = f"L/{case.combos.wnet_limit_ratio:.0f}"

    data = {
        "x": x,
        "elu": elu_series,
        "els": els_series,
        "envelopes": {
            "N_max": _arr(results.N_max),
            "N_min": _arr(results.N_min),
            "V_max": _arr(results.V_max),
            "V_min": _arr(results.V_min),
            "M_max": _arr(results.M_max),
            "M_min": _arr(results.M_min),
        },
        "deflection_limit_mm": limit_mm,
        "deflection_limit_label": limit_label,
        "title": (
            f"L={case.length}m, "
            f"{case.section.b:.0f}\u00d7{case.section.h:.0f}mm, "
            f"{case.material.grade}"
        ),
    }
    return json.dumps(data)
