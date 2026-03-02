"""
Military / Dual-use Dependency Index (MDI).

Combines Carnegie dual-use exports (China → Russia) with bilateral trade
to compute the share of dual-use in China's exports to Russia.
Output: mdi_monthly_2022_2024.csv for dashboard and 05_war_dependency notebook.

Based on Carnegie Endowment (May 2024): ~$300M/month dual-use.
"""
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "02_processed_data"
OUT_FILE = DATA_DIR / "mdi_monthly_2022_2024.csv"


def load_carnegie_dualuse() -> pd.DataFrame:
    """Load Carnegie dual-use monthly, aggregate by date (sum over categories)."""
    path = DATA_DIR / "carnegie_dualuse_monthly.csv"
    if not path.exists():
        raise FileNotFoundError(f"Run scripts/fetch_carnegie_dualuse.py first: {path}")
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"] + "-01")
    agg = df.groupby("date")["value_usd"].sum().reset_index()
    agg.columns = ["date", "dual_use_usd"]
    return agg


def load_china_exports_to_russia() -> pd.DataFrame:
    """Load China exports to Russia (bn USD) from panel_monthly_var."""
    path = DATA_DIR / "panel_monthly_var.csv"
    if not path.exists():
        raise FileNotFoundError(f"Panel not found: {path}")
    df = pd.read_csv(path, parse_dates=["date"])
    df = df[["date", "CHN_exp_to_RUS_bn"]].dropna()
    df["chn_exp_usd"] = df["CHN_exp_to_RUS_bn"] * 1e9
    return df[["date", "chn_exp_usd", "CHN_exp_to_RUS_bn"]]


def compute_mdi(
    carnegie: pd.DataFrame,
    trade: pd.DataFrame,
) -> pd.DataFrame:
    """
    MDI = dual_use_usd / chn_exp_usd (share of China→Russia exports that are dual-use).
    """
    trade = trade.copy()
    trade["date"] = trade["date"].dt.to_period("M").dt.to_timestamp()
    merged = trade.merge(carnegie, on="date", how="inner")
    merged["mdi_pct"] = 100 * merged["dual_use_usd"] / merged["chn_exp_usd"]
    merged["dual_use_bn"] = merged["dual_use_usd"] / 1e9
    return merged[
        [
            "date",
            "dual_use_usd",
            "dual_use_bn",
            "CHN_exp_to_RUS_bn",
            "mdi_pct",
        ]
    ]


def build_mdi_monthly() -> pd.DataFrame:
    """Build MDI monthly series (2022-03 onward, when Carnegie data starts)."""
    carnegie = load_carnegie_dualuse()
    trade = load_china_exports_to_russia()
    mdi = compute_mdi(carnegie, trade)
    return mdi.sort_values("date").reset_index(drop=True)


def main() -> str:
    """Compute and save mdi_monthly_2022_2024.csv."""
    mdi = build_mdi_monthly()
    mdi.to_csv(OUT_FILE, index=False)
    return str(OUT_FILE)


if __name__ == "__main__":
    out = main()
    df = pd.read_csv(out)
    print(f"Saved: {out}")
    print(f"Rows: {len(df)}, Range: {df['date'].min()} to {df['date'].max()}")
    print(f"MDI pct: min={df['mdi_pct'].min():.2f}%, max={df['mdi_pct'].max():.2f}%")
