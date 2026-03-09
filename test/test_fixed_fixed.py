"""Test fixed-fixed beam (encastré) against analytical formulas."""

from __future__ import annotations

import pytest

from app.analysis import compute_beam
from app.formulas import fixed_fixed
from app.models import (
    BeamCase,
    LoadCase,
    PointLoad,
    SupportType,
    UniformLoad,
)
from test.conftest import N_POINTS, SECTION, L, els_combo, get_EI
from test.helpers import assert_allclose

# -- Uniform load ----------------------------------------------------------


class TestUniformLight:
    """Light uniform load: w = -1 kN/m."""

    W = -1.0

    @pytest.fixture(autouse=True)
    def setup(self):
        case = BeamCase(
            length=L,
            support_left=SupportType.FIXED,
            support_right=SupportType.FIXED,
            section=SECTION,
            uniform_loads=[UniformLoad(w=self.W, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = fixed_fixed.uniform_load_shear(self.W, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = fixed_fixed.uniform_load_moment(self.W, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = fixed_fixed.uniform_load_deflection(
            self.W, L, self.E, self.I, self.x
        )
        assert_allclose(
            self.results.delta[self.combo], expected, rtol=0.02, name="delta"
        )


class TestUniformMedium:
    """Medium uniform load: w = -5 kN/m."""

    W = -5.0

    @pytest.fixture(autouse=True)
    def setup(self):
        case = BeamCase(
            length=L,
            support_left=SupportType.FIXED,
            support_right=SupportType.FIXED,
            section=SECTION,
            uniform_loads=[UniformLoad(w=self.W, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = fixed_fixed.uniform_load_shear(self.W, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = fixed_fixed.uniform_load_moment(self.W, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = fixed_fixed.uniform_load_deflection(
            self.W, L, self.E, self.I, self.x
        )
        assert_allclose(
            self.results.delta[self.combo], expected, rtol=0.02, name="delta"
        )


class TestUniformHeavy:
    """Heavy uniform load: w = -15 kN/m."""

    W = -15.0

    @pytest.fixture(autouse=True)
    def setup(self):
        case = BeamCase(
            length=L,
            support_left=SupportType.FIXED,
            support_right=SupportType.FIXED,
            section=SECTION,
            uniform_loads=[UniformLoad(w=self.W, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = fixed_fixed.uniform_load_shear(self.W, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = fixed_fixed.uniform_load_moment(self.W, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = fixed_fixed.uniform_load_deflection(
            self.W, L, self.E, self.I, self.x
        )
        assert_allclose(
            self.results.delta[self.combo], expected, rtol=0.02, name="delta"
        )


# -- Point load at midspan ------------------------------------------------


class TestPointLoadMidspan:
    """Midspan point load: P = -10 kN."""

    P = -10.0
    A = L / 2

    @pytest.fixture(autouse=True)
    def setup(self):
        case = BeamCase(
            length=L,
            support_left=SupportType.FIXED,
            support_right=SupportType.FIXED,
            section=SECTION,
            point_loads=[PointLoad(P=self.P, x=self.A, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = fixed_fixed.point_load_shear(self.P, self.A, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = fixed_fixed.point_load_moment(self.P, self.A, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = fixed_fixed.point_load_deflection(
            self.P, self.A, L, self.E, self.I, self.x
        )
        assert_allclose(
            self.results.delta[self.combo], expected, rtol=0.02, name="delta"
        )


# -- Point load at quarter span -------------------------------------------


class TestPointLoadQuarterSpan:
    """Quarter-span point load: P = -8 kN at L/4."""

    P = -8.0
    A = L / 4

    @pytest.fixture(autouse=True)
    def setup(self):
        case = BeamCase(
            length=L,
            support_left=SupportType.FIXED,
            support_right=SupportType.FIXED,
            section=SECTION,
            point_loads=[PointLoad(P=self.P, x=self.A, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = fixed_fixed.point_load_shear(self.P, self.A, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = fixed_fixed.point_load_moment(self.P, self.A, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = fixed_fixed.point_load_deflection(
            self.P, self.A, L, self.E, self.I, self.x
        )
        assert_allclose(
            self.results.delta[self.combo], expected, rtol=0.02, name="delta"
        )


# -- Point load at third span ---------------------------------------------


class TestPointLoadThirdSpan:
    """Third-span point load: P = -12 kN at L/3."""

    P = -12.0
    A = L / 3

    @pytest.fixture(autouse=True)
    def setup(self):
        case = BeamCase(
            length=L,
            support_left=SupportType.FIXED,
            support_right=SupportType.FIXED,
            section=SECTION,
            point_loads=[PointLoad(P=self.P, x=self.A, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = fixed_fixed.point_load_shear(self.P, self.A, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = fixed_fixed.point_load_moment(self.P, self.A, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = fixed_fixed.point_load_deflection(
            self.P, self.A, L, self.E, self.I, self.x
        )
        assert_allclose(
            self.results.delta[self.combo], expected, rtol=0.02, name="delta"
        )


# -- Heavy point load at midspan ------------------------------------------


class TestPointLoadHeavy:
    """Heavy point load: P = -25 kN at midspan."""

    P = -25.0
    A = L / 2

    @pytest.fixture(autouse=True)
    def setup(self):
        case = BeamCase(
            length=L,
            support_left=SupportType.FIXED,
            support_right=SupportType.FIXED,
            section=SECTION,
            point_loads=[PointLoad(P=self.P, x=self.A, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = fixed_fixed.point_load_shear(self.P, self.A, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = fixed_fixed.point_load_moment(self.P, self.A, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = fixed_fixed.point_load_deflection(
            self.P, self.A, L, self.E, self.I, self.x
        )
        assert_allclose(
            self.results.delta[self.combo], expected, rtol=0.02, name="delta"
        )
