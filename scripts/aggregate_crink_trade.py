"""
Aggregate CRINK bilateral trade flows into crink_bilateral_2024.csv.
Data from Brief_finalisation and CSIS research.
"""
from pathlib import Path

import pandas as pd

# Output path (russia_china_dependency/02_processed_data)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUT_PATH = PROJECT_ROOT / "russia_china_dependency" / "02_processed_data" / "crink_bilateral_2024.csv"


def build_crink_df() -> pd.DataFrame:
    """Build CRINK bilateral 2024 DataFrame from curated sources."""
    rows = [
        ("CHN", "RUS", 245, "trade", "comtrade_2024"),
        ("CHN", "IRN", 42, "trade+oil", "csis_2024"),
        ("CHN", "PRK", 1, "trade", "tass_2024"),
        ("RUS", "IRN", 5, "arms", "sipri_estimate"),
        ("RUS", "PRK", 1, "munitions", "us_estimate"),
        ("IRN", "RUS", 3, "drones", "oryx_2024"),
        ("PRK", "RUS", 2.5, "munitions", "pentagon_estimate"),
    ]
    return pd.DataFrame(
        rows,
        columns=["exporter", "importer", "value_bn", "category", "source"],
    )


def main() -> None:
    df = build_crink_df()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Wrote {len(df)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
