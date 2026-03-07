# Beambo

Streamlit app for computing 2D beams using PyNite and pyEurocodes.

## Stack

- Python 3.13+, managed with uv
- Streamlit (UI)
- Pydantic (data models)
- pydantic-ai (LLM integration)
- eurocodepy (Eurocode 5 implementation)
- PyNiteFEA (FEA engine)
- matplotlib (plotting)
- numpy (numerical calculations)

## Project structure

- `app/` - Application modules
  - `models/` - Pydantic data models
    - `supports.py` - SupportType enum, support_dofs()
    - `loads/` - Load and combination models
      - `cases.py` - LoadCase, PointLoad, UniformLoad, TrapezoidalLoad
      - `combinations.py` - LoadCombinations (EN 1990)
    - `sections/` - Cross-section models
      - `rectangular.py` - RectangularSection, HollowRectangularSection
      - `circular.py` - CircularSection, HollowCircularSection
    - `materials/` - Material models
      - `timber.py` - TimberGrade enum, TimberMaterial (EC5)
      - `steel.py` - SteelGrade enum, SteelMaterial (EC3)
    - `case.py` - BeamCase (top-level input)
    - `results.py` - BeamResults, VerificationResult, VerificationReport
  - `analysis.py` - FEA computation with Pynite
  - `verification.py` - EC5 cross-section verification with eurocodepy
  - `plotting.py` - N/V/M diagram and envelope plots
  - `formulas/` - Analytical beam formulas (for testing against FEA)
    - `simply_supported.py` - Pinned-roller beam (uniform, point load)
    - `cantilever.py` - Fixed-free beam (uniform, tip, arbitrary point load)
  - `cases/` - Beam case definitions (1 file = 1 case, exports `CASE: BeamCase`)
  - `run_beam.py` - CLI runner: case -> analysis -> verification -> plotting
- `llm/` - LLM-related modules
  - `context/` - **Local package documentation** (see below)
- `test/` - Tests (pytest)
- `tmp/` - Temporary files (not tracked)

## Local documentation (`llm/context/`)

Package docs are downloaded locally into `llm/context/`. **Always consult these
docs instead of relying on training data** when working with:

- `llm/context/streamlit/` - Streamlit API reference and guides
- `llm/context/pynite/` - PyNiteFEA documentation
- `llm/context/eurocodepy/` - eurocodepy (Eurocode 5) documentation

Read the relevant files in these directories before using or modifying code
that depends on these packages.

## Commands

- `just run` - Run the Streamlit app
- `just sync` - Sync everything (dependencies, etc.)
- `just validate` (or `just v`) - Lint + format + typecheck + test (all-in-one)
- `just lint` - Ruff lint with auto-fix
- `just format` - Ruff format
- `just check` - Pyright typecheck
- `just test` - Run pytest
- `just beam <case>` - Full beam workflow (e.g. `just beam simply_supported_c24`), outputs to `tmp/<timestamp>/`
- `just llm-upgrade` - Download/refresh local package docs
- `uv run pytest test/test_foo.py::test_name` - Run a single test

## Python best practices

- StrEnum not (str, Enum)
- Pydantic v2 field style:
  - No `Field(...)` if there are no constraints — just use the type annotation
  - Use docstring-style field descriptions (inline `"""..."""` below the field), not `Field(description="...")`
  - Only use `Field()` when you need `gt`, `ge`, `default_factory`, `alias`, etc.

## Units

Length: m | Force: kN | Moment: kNm | Stress: MPa
Section dimensions: mm | Distributed loads: kN/m | Point loads: kN