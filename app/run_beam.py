"""Run the full beam workflow: case -> analysis -> verification -> plotting."""

from __future__ import annotations

import importlib
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from app.analysis import compute_beam
from app.models import BeamCase
from app.plotting import plot_diagrams, plot_envelope
from app.report import generate_report
from app.verification import verify_ec5


def load_case(name: str) -> BeamCase:
    """Import CASE from app.cases.<name>."""
    module = importlib.import_module(f"app.cases.{name}")
    case = getattr(module, "CASE", None)
    if not isinstance(case, BeamCase):
        raise ValueError(f"app/cases/{name}.py must export a CASE: BeamCase")
    return case


def run(name: str) -> None:
    print(f"Loading case: {name}")
    case = load_case(name)

    # Create timestamped output directory
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = Path("tmp") / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    # Analysis
    print("Running FEA...")
    results = compute_beam(case)
    print(f"  {len(results.combo_names)} combos computed")

    # Verification
    print("Running EC5 verification...")
    report = verify_ec5(case, results)
    print(report.summary)

    verification_path = out_dir / "verification.txt"
    verification_path.write_text(report.summary)

    # Plotting
    print("Generating plots...")
    plot_diagrams(case, results, save_path=str(out_dir / "diagrams.png"))
    plot_envelope(case, results, save_path=str(out_dir / "envelope.png"))

    # HTML report
    print("Generating HTML report...")
    report_path = generate_report(case, results, report, out_dir=out_dir)
    print(f"  -> Report saved to {report_path}")

    print(f"\nOutput: {out_dir}/")

    # Open report in browser
    subprocess.Popen(["open", str(report_path)])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.run_beam <case_name>")
        print("Example: python -m app.run_beam simply_supported_c24")
        sys.exit(1)
    run(sys.argv[1])
