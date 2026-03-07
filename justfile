# First-time repo setup (dependencies + hooks)
install:
    uv sync
    uv run pre-commit install

# Run the streamlit app
run:
    uv run streamlit run main.py

# Sync dependencies
sync:
    uv sync

# Add a dependency
add *args:
    uv add {{args}}

# Download/update LLM context docs
llm-upgrade:
    uv run python llm/context/context.py

# Run pre-commit on all files
precommit:
    uv run pre-commit run --all-files

# Lint (ruff check + fix)
lint:
    uv run ruff check --fix .

# Format (ruff format)
format:
    uv run ruff format .

# Typecheck (pyright)
check:
    uv run pyright

# Run tests
test:
    uv run pytest

# Validate: lint + format + typecheck + test
validate: lint format check test

alias v := validate

# Run full beam workflow: case -> analysis -> verification -> plotting
beam case_name="simply_supported_c24":
    uv run python -m app.run_beam {{case_name}}
