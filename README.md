# Beambo

2D beam analysis with Eurocode verification.

Built on [PyNiteFEA](https://github.com/JWock82/PyNite) for finite element analysis and [eurocodepy](https://github.com/pcachim/eurocodepy) for Eurocode 5 timber design checks. Uses [Streamlit](https://streamlit.io/) for the UI.

## What it does

1. **Define a beam** — span, section, material, loads
2. **Run FEA** — PyNite computes internal forces (N, V, M) and deflections
3. **Verify** — cross-section checks per Eurocode 5 (bending, shear, deflection)
4. **Plot** — N/V/M diagrams and load combination envelopes
5. **Report** — HTML report with results and plots

## Quick start

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
# Clone and install
git clone https://github.com/ZYME-dev/beambo.git
cd beambo
just install

# Run a beam case
just beam simply_supported_c24
```

This runs the full pipeline and opens an HTML report in your browser.

## Defining a beam case

Each case is a Python file in `app/cases/` that exports a `CASE: BeamCase`:

```python
from app.models import (
    BeamCase, LoadCase, PointLoad, RectangularSection,
    TimberGrade, TimberMaterial, UniformLoad,
)

CASE = BeamCase(
    length=5.0,  # m
    section=RectangularSection(b=100, h=300),  # mm
    material=TimberMaterial(
        grade=TimberGrade.C24,
        service_class=1,
        load_duration_G="Permanent",
        load_duration_Q="MediumDuration",
    ),
    uniform_loads=[
        UniformLoad(w=-2.0, case=LoadCase.G),   # kN/m
        UniformLoad(w=-3.5, case=LoadCase.Q),
    ],
    point_loads=[
        PointLoad(P=-5.0, x=2.5, case=LoadCase.Q),  # kN at midspan
    ],
)
```

Then run it:

```bash
just beam my_case_name
```

## Available commands

| Command | Description |
|---------|-------------|
| `just install` | First-time setup (dependencies + pre-commit hooks) |
| `just run` | Launch the Streamlit app |
| `just beam <case>` | Full beam workflow (analysis + verification + plots) |
| `just sync` | Sync dependencies |
| `just validate` | Lint + format + typecheck + test |
| `just test` | Run tests |
| `just precommit` | Run pre-commit hooks on all files |

## Units

| Quantity | Unit |
|----------|------|
| Length | m |
| Section dimensions | mm |
| Force / Point load | kN |
| Distributed load | kN/m |
| Moment | kNm |
| Stress | MPa |

## Project structure

```
app/
  models/         Pydantic data models (sections, materials, loads, results)
  cases/          Beam case definitions (1 file = 1 case)
  analysis.py     FEA computation (PyNite)
  verification.py EC5 cross-section checks (eurocodepy)
  plotting.py     N/V/M diagrams and envelopes
  formulas/       Analytical beam formulas (used for testing)
  run_beam.py     CLI runner
test/             Tests (pytest)
```
