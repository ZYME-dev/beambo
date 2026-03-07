"""Render HTML report with Jinja2 template and Plotly.js charts."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

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

    template = _ENV.get_template("template.html.j2")
    html = template.render(ctx)

    out_path = out_dir / "report.html"
    out_path.write_text(html)
    return out_path
