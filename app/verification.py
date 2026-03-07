"""EC5 cross-section verification using eurocodepy."""

from __future__ import annotations

import numpy as np
from eurocodepy.ec5 import (
    LoadDuration,
    ServiceClass,
)
from eurocodepy.ec5 import (
    TimberClass as ec5_timber_class,
)
from eurocodepy.ec5.uls.bending import check_bending_with_normal
from eurocodepy.utils import RectangularCrossSection

from app.models import BeamCase, BeamResults, VerificationReport, VerificationResult


def verify_ec5(case: BeamCase, results: BeamResults) -> VerificationReport:
    """Run EC5 cross-section checks (bending, shear, deflection)."""

    sec = case.section
    mat = case.material
    L = case.length
    combos = case.combos

    ec_section = RectangularCrossSection(sec.b_m, sec.h_m)
    timber = ec5_timber_class(mat.grade)

    sc_map = {1: ServiceClass.SC1, 2: ServiceClass.SC2, 3: ServiceClass.SC3}  # pyright: ignore[reportAttributeAccessIssue]
    service_class = sc_map[mat.service_class]

    ld_map = {
        "Permanent": LoadDuration.Permanent,  # pyright: ignore[reportAttributeAccessIssue]
        "LongDuration": LoadDuration.LongDuration,  # pyright: ignore[reportAttributeAccessIssue]
        "MediumDuration": LoadDuration.MediumDuration,  # pyright: ignore[reportAttributeAccessIssue]
        "ShortDuration": LoadDuration.ShortDuration,  # pyright: ignore[reportAttributeAccessIssue]
        "Instantaneous": LoadDuration.Instantaneous,  # pyright: ignore[reportAttributeAccessIssue]
    }

    report = VerificationReport()

    # ELU checks
    elu_names = [
        n for n, t in zip(results.combo_names, results.combo_types) if t == "ELU"
    ]

    for combo_name in elu_names:
        has_q = "Q" in combo_name or "1.5Q" in combo_name
        load_dur = ld_map[mat.load_duration_Q if has_q else mat.load_duration_G]

        M_arr = results.M[combo_name]
        V_arr = results.V[combo_name]
        N_arr = results.N[combo_name]

        # Bending check at max |M| location
        idx_M = np.argmax(np.abs(M_arr))
        M_ed = M_arr[idx_M]
        N_ed = N_arr[idx_M]

        bending_result = check_bending_with_normal(
            n_ed=N_ed,
            m_ed_y=abs(M_ed),
            m_ed_z=0.0,
            section=ec_section,
            timber=timber,
            l_0y=L,
            l_0z=L,
            l_0m=L,
            service_class=service_class,
            load_duration=load_dur,
        )

        report_text = bending_result["report"]
        ratios = []
        for line in report_text.split("\n"):
            if "Check" in line and "<= 1.0" in line:
                try:
                    val = float(line.split(":")[1].strip().split(" ")[0])
                    ratios.append(val)
                except (ValueError, IndexError):
                    pass
        max_ratio_bending = max(ratios) if ratios else 0.0

        report.checks.append(
            VerificationResult(
                name=f"Bending — {combo_name}",
                is_ok=bending_result["is_ok"],
                ratio=round(max_ratio_bending, 3),
                details=report_text,
            )
        )

        # Shear check at max |V| location
        idx_V = np.argmax(np.abs(V_arr))
        V_ed = abs(V_arr[idx_V])

        timber.design_values(service_class=service_class, load_duration=load_dur)
        tau_d = 1.5 * V_ed / (ec_section.area * 1e3)
        fvd = timber.fvd
        shear_ratio = tau_d / fvd if fvd > 0 else float("inf")
        shear_ok = shear_ratio <= 1.0

        report.checks.append(
            VerificationResult(
                name=f"Shear — {combo_name}",
                is_ok=shear_ok,
                ratio=round(shear_ratio, 3),
                details=(
                    f"Shear check (EC5 §6.1.7):\n"
                    f"  V_Ed = {V_ed:.2f} kN\n"
                    f"  A = {ec_section.area:.4f} m²\n"
                    f"  tau_d = 1.5*V_Ed/A = {tau_d:.2f} MPa\n"
                    f"  kmod = {timber.kmod:.2f}, gamma_M = {timber.safety:.2f}\n"
                    f"  f_v,d = {fvd:.2f} MPa\n"
                    f"  Ratio: {shear_ratio:.3f} <= 1.0 -> "
                    f"{'OK' if shear_ok else 'NOT OK'}\n"
                ),
            )
        )

    # ELS checks
    els_names = [
        n for n, t in zip(results.combo_names, results.combo_types) if t == "ELS"
    ]

    for combo_name in els_names:
        D_arr = results.delta[combo_name]
        max_defl = np.max(np.abs(D_arr))
        max_defl_mm = max_defl * 1000.0

        if "car" in combo_name:
            limit_ratio = combos.wnet_limit_ratio
        elif "qp" in combo_name:
            limit_ratio = combos.wfin_limit_ratio
        else:
            limit_ratio = combos.wnet_limit_ratio

        limit_label = f"L/{limit_ratio:.0f}"
        limit_mm = L * 1000.0 / limit_ratio
        ratio_defl = max_defl_mm / limit_mm if limit_mm > 0 else 0.0

        report.checks.append(
            VerificationResult(
                name=f"Deflection — {combo_name}",
                is_ok=max_defl_mm <= limit_mm,
                ratio=round(ratio_defl, 3),
                details=(
                    f"  Max deflection: {max_defl_mm:.2f} mm\n"
                    f"  Limit ({limit_label}): {limit_mm:.2f} mm\n"
                    f"  Ratio: {ratio_defl:.3f}\n"
                ),
            )
        )

    report.all_ok = all(c.is_ok for c in report.checks)

    lines = ["=" * 60, "  EC5 VERIFICATION SUMMARY", "=" * 60]
    for c in report.checks:
        status = "OK" if c.is_ok else "FAIL"
        lines.append(f"  {status}  {c.name}  (ratio: {c.ratio:.3f})")
    lines.append("=" * 60)
    global_status = "ALL CHECKS PASS" if report.all_ok else "SOME CHECKS FAIL"
    lines.append(f"  {global_status}")
    lines.append("=" * 60)
    report.summary = "\n".join(lines)

    return report
