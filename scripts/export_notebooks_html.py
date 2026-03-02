"""
Export notebooks to HTML for reports/ (Phase 1.4).
Usage: python scripts/export_notebooks_html.py
"""
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
REPORTS_DIR = PROJECT_ROOT / "reports"

NOTEBOOKS = [
    "01_structural_analysis.ipynb",
    "02_time_series_econometrics.ipynb",
    "03_causal_inference.ipynb",
    "04_network_analysis.ipynb",
    "05_war_dependency.ipynb",
    "06_crink_network.ipynb",
]


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    for nb in NOTEBOOKS:
        nb_path = NOTEBOOKS_DIR / nb
        if not nb_path.exists():
            print(f"Skip: {nb} not found")
            continue
        out_name = nb.replace(".ipynb", ".html")
        cmd = [
            sys.executable, "-m", "nbconvert",
            "--to", "html",
            "--output", out_name,
            "--output-dir", str(REPORTS_DIR),
            str(nb_path),
        ]
        try:
            subprocess.run(cmd, check=True, cwd=PROJECT_ROOT)
            print(f"OK: {nb} -> reports/{out_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {nb} -- {e}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
