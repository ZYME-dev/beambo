"""Test propped cantilever (fixed-roller) against analytical formulas."""

from __future__ import annotations

import pytest

from app.analysis import compute_beam
from app.formulas import propped_cantilever
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
            support_right=SupportType.ROLLER_X,
            section=SECTION,
            uniform_loads=[UniformLoad(w=self.W, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = propped_cantilever.uniform_load_shear(self.W, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = propped_cantilever.uniform_load_moment(self.W, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = propped_cantilever.uniform_load_deflection(
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
            support_right=SupportType.ROLLER_X,
            section=SECTION,
            uniform_loads=[UniformLoad(w=self.W, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = propped_cantilever.uniform_load_shear(self.W, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = propped_cantilever.uniform_load_moment(self.W, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = propped_cantilever.uniform_load_deflection(
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
            support_right=SupportType.ROLLER_X,
            section=SECTION,
            uniform_loads=[UniformLoad(w=self.W, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = propped_cantilever.uniform_load_shear(self.W, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = propped_cantilever.uniform_load_moment(self.W, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = propped_cantilever.uniform_load_deflection(
            self.W, L, self.E, self.I, self.x
        )
        assert_allclose(
            self.results.delta[self.combo], expected, rtol=0.02, name="delta"
        )


# -- Point load at midspan ------------------------------------------------


class TestPointLoadMidspan:
    """Midspan point load: P = -10 kN at L/2."""

    P = -10.0
    A = L / 2

    @pytest.fixture(autouse=True)
    def setup(self):
        case = BeamCase(
            length=L,
            support_left=SupportType.FIXED,
            support_right=SupportType.ROLLER_X,
            section=SECTION,
            point_loads=[PointLoad(P=self.P, x=self.A, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = propped_cantilever.point_load_shear(self.P, self.A, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = propped_cantilever.point_load_moment(self.P, self.A, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = propped_cantilever.point_load_deflection(
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
            support_right=SupportType.ROLLER_X,
            section=SECTION,
            point_loads=[PointLoad(P=self.P, x=self.A, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = propped_cantilever.point_load_shear(self.P, self.A, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = propped_cantilever.point_load_moment(self.P, self.A, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = propped_cantilever.point_load_deflection(
            self.P, self.A, L, self.E, self.I, self.x
        )
        assert_allclose(
            self.results.delta[self.combo], expected, rtol=0.02, name="delta"
        )


# -- Point load at three-quarter span -------------------------------------


class TestPointLoadThreeQuarterSpan:
    """Point load near roller: P = -6 kN at 3L/4."""

    P = -6.0
    A = 3 * L / 4

    @pytest.fixture(autouse=True)
    def setup(self):
        case = BeamCase(
            length=L,
            support_left=SupportType.FIXED,
            support_right=SupportType.ROLLER_X,
            section=SECTION,
            point_loads=[PointLoad(P=self.P, x=self.A, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = propped_cantilever.point_load_shear(self.P, self.A, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = propped_cantilever.point_load_moment(self.P, self.A, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = propped_cantilever.point_load_deflection(
            self.P, self.A, L, self.E, self.I, self.x
        )
        assert_allclose(
            self.results.delta[self.combo], expected, rtol=0.02, name="delta"
        )


# -- Heavy point load at midspan ------------------------------------------


class TestPointLoadHeavy:
    """Heavy point load: P = -20 kN at midspan."""

    P = -20.0
    A = L / 2

    @pytest.fixture(autouse=True)
    def setup(self):
        case = BeamCase(
            length=L,
            support_left=SupportType.FIXED,
            support_right=SupportType.ROLLER_X,
            section=SECTION,
            point_loads=[PointLoad(P=self.P, x=self.A, case=LoadCase.G)],
            n_points=N_POINTS,
        )
        self.results = compute_beam(case)
        self.x = self.results.x
        self.combo = els_combo(self.results)
        self.E, self.I = get_EI()

    def test_shear(self):
        expected = propped_cantilever.point_load_shear(self.P, self.A, L, self.x)
        assert_allclose(self.results.V[self.combo], expected, rtol=0.02, name="V")

    def test_moment(self):
        expected = propped_cantilever.point_load_moment(self.P, self.A, L, self.x)
        assert_allclose(self.results.M[self.combo], expected, rtol=0.02, name="M")

    def test_deflection(self):
        expected = propped_cantilever.point_load_deflection(
            self.P, self.A, L, self.E, self.I, self.x
        )
        assert_allclose(
            self.results.delta[self.combo], expected, rtol=0.02, name="delta"
        )
