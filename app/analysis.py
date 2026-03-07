"""2D beam FEA computation using Pynite."""

from __future__ import annotations

import numpy as np
from eurocodepy.ec5 import TimberClass as ec5_timber_class
from Pynite import FEModel3D

from app.models import BeamCase, BeamResults, LoadCase
from app.models.supports import support_dofs


def compute_beam(case: BeamCase) -> BeamResults:
    """Build Pynite model, apply loads & combos, analyze, extract diagrams."""

    L = case.length
    sec = case.section
    mat = case.material
    combos = case.combos

    # Timber properties from eurocodepy
    timber = ec5_timber_class(mat.grade)

    # Pynite units: m, kN -> E in kN/m², rho in kN/m³
    E = timber.E0mean * 1e3  # MPa -> kN/m²
    G = timber.Gmean * 1e3  # MPa -> kN/m²
    nu = E / (2 * G) - 1
    rho = timber.rhom / 1000.0

    # Build model
    model = FEModel3D()
    model.add_node("N1", 0, 0, 0)
    model.add_node("N2", L, 0, 0)

    model.add_material("Timber", E, G, nu, rho)
    model.add_section("Sec", sec.A, sec.Iy, sec.Iz, sec.J)
    model.add_member("M1", "N1", "N2", "Timber", "Sec")

    # Supports
    model.def_support("N1", *support_dofs(case.support_left).as_tuple())
    model.def_support("N2", *support_dofs(case.support_right).as_tuple())

    # Apply loads
    for pl in case.point_loads:
        model.add_member_pt_load("M1", "Fy", pl.P, pl.x, case=pl.case.value)

    for ul in case.uniform_loads:
        x1 = ul.x1 if ul.x1 is not None else 0.0
        x2 = ul.x2 if ul.x2 is not None else L
        model.add_member_dist_load("M1", "Fy", ul.w, ul.w, x1, x2, case=ul.case.value)

    for tl in case.trapezoidal_loads:
        x1 = tl.x1 if tl.x1 is not None else 0.0
        x2 = tl.x2 if tl.x2 is not None else L
        model.add_member_dist_load("M1", "Fy", tl.w1, tl.w2, x1, x2, case=tl.case.value)

    # Determine which load cases are present
    all_loads = [
        *((pl.case for pl in case.point_loads)),
        *((ul.case for ul in case.uniform_loads)),
        *((tl.case for tl in case.trapezoidal_loads)),
    ]
    has_G = LoadCase.G in all_loads
    has_Q = LoadCase.Q in all_loads

    # Load combinations
    combo_definitions: list[tuple[str, str, dict[str, float]]] = []

    # ELU combinations (EN 1990 §6.4.3.2 — STR/GEO)
    if has_G and has_Q:
        combo_definitions.extend(
            [
                (
                    "ELU_1: 1.35G+1.5Q",
                    "ELU",
                    {
                        "G": combos.gamma_G_unfav,
                        "Q": combos.gamma_Q,
                    },
                ),
                (
                    "ELU_2: 1.0G+1.5Q",
                    "ELU",
                    {
                        "G": combos.gamma_G_fav,
                        "Q": combos.gamma_Q,
                    },
                ),
                (
                    "ELU_3: 1.35G",
                    "ELU",
                    {
                        "G": combos.gamma_G_unfav,
                    },
                ),
            ]
        )
    elif has_G:
        combo_definitions.append(("ELU_1: 1.35G", "ELU", {"G": combos.gamma_G_unfav}))
    elif has_Q:
        combo_definitions.append(("ELU_1: 1.5Q", "ELU", {"Q": combos.gamma_Q}))

    # ELS combinations
    if has_G and has_Q:
        combo_definitions.extend(
            [
                (
                    "ELS_car: 1.0G+1.0Q",
                    "ELS",
                    {
                        "G": 1.0,
                        "Q": 1.0,
                    },
                ),
                (
                    "ELS_freq: 1.0G+psi1Q",
                    "ELS",
                    {
                        "G": 1.0,
                        "Q": combos.psi_1_Q,
                    },
                ),
                (
                    "ELS_qp: 1.0G+psi2Q",
                    "ELS",
                    {
                        "G": 1.0,
                        "Q": combos.psi_2_Q,
                    },
                ),
            ]
        )
    elif has_G:
        combo_definitions.append(("ELS_car: 1.0G", "ELS", {"G": 1.0}))
    elif has_Q:
        combo_definitions.append(("ELS_car: 1.0Q", "ELS", {"Q": 1.0}))

    for name, _, factors in combo_definitions:
        model.add_load_combo(name, factors)

    # Analyze
    model.analyze(check_statics=False)

    # Extract results
    member = model.members["M1"]
    n_pts = case.n_points

    combo_names = [c[0] for c in combo_definitions]
    combo_types = [c[1] for c in combo_definitions]

    result_array = member.moment_array("Mz", n_points=n_pts, combo_name=combo_names[0])
    x = result_array[0]

    N_dict: dict[str, np.ndarray] = {}
    V_dict: dict[str, np.ndarray] = {}
    M_dict: dict[str, np.ndarray] = {}
    D_dict: dict[str, np.ndarray] = {}

    for cname in combo_names:
        N_dict[cname] = member.axial_array(
            n_points=n_pts,
            combo_name=cname,
            x_array=x,
        )[1]
        V_dict[cname] = member.shear_array(
            "Fy",
            n_points=n_pts,
            combo_name=cname,
            x_array=x,
        )[1]
        M_dict[cname] = member.moment_array(
            "Mz",
            n_points=n_pts,
            combo_name=cname,
            x_array=x,
        )[1]
        D_dict[cname] = member.deflection_array(
            "dy",
            n_points=n_pts,
            combo_name=cname,
            x_array=x,
        )[1]

    # Envelopes over ELU combos
    elu_names = [n for n, t in zip(combo_names, combo_types) if t == "ELU"]
    if elu_names:
        N_stack = np.array([N_dict[n] for n in elu_names])
        V_stack = np.array([V_dict[n] for n in elu_names])
        M_stack = np.array([M_dict[n] for n in elu_names])
        D_stack = np.array([D_dict[n] for n in elu_names])
    else:
        N_stack = V_stack = M_stack = D_stack = np.zeros((1, len(x)))

    return BeamResults(
        combo_names=combo_names,
        combo_types=combo_types,
        x=x,
        N=N_dict,
        V=V_dict,
        M=M_dict,
        delta=D_dict,
        N_max=N_stack.max(axis=0),
        N_min=N_stack.min(axis=0),
        V_max=V_stack.max(axis=0),
        V_min=V_stack.min(axis=0),
        M_max=M_stack.max(axis=0),
        M_min=M_stack.min(axis=0),
        delta_max=D_stack.max(axis=0),
        delta_min=D_stack.min(axis=0),
    )
