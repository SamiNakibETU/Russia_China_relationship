"""
Generate plausible monthly Carnegie dual-use export series (China → Russia).

Based on Carnegie Endowment report (May 2024):
- ~$300M/month dual-use exports
- Categories: semiconductors (largest), telecom equipment, machine tools
- Machine tools share: 60% (2022) → 90% (2023)
- share_china from brief: semiconductors ~0.89, machine_tools ~0.60, telecom ~0.75

No exact monthly breakdown in the article; series is synthetic/plausible.
"""
import pandas as pd
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "russia_china_dependency" / "02_processed_data"
OUTPUT_FILE = OUTPUT_DIR / "carnegie_dualuse_monthly.csv"

TOTAL_MONTHLY_USD = 300e6  # ~$300M/month
SOURCE_LABEL = "carnegie_2024_may"

# share_china by category (from brief)
SHARE_CHINA = {
    "semiconductors": 0.89,
    "machine_tools": 0.60,
    "telecom": 0.75,
}


def _machine_tools_share(month_idx: int, total_months: int) -> float:
    """Linear: 40% at start → 60% (2022) → 90% by end of 2023, then plateau."""
    # 2022-03: 40%; reach 60% by mid-2022 (month 3); reach 90% by 2023-12 (month 21)
    if month_idx <= 3:
        return 0.40 + (0.20 * month_idx / 3)  # 40% → 60% over first 4 months
    if month_idx >= 21:
        return 0.90
    return 0.60 + (0.30 * (month_idx - 3) / 18)  # 60% → 90% from month 4 to 21


def _category_shares(month_idx: int, total_months: int) -> dict[str, float]:
    """Get shares for semiconductors, machine_tools, telecom. Initially 40/40/20, machine_tools grows to 90%."""
    mt_share = _machine_tools_share(month_idx, total_months)
    remainder = 1.0 - mt_share
    # Semiconductors largest of remainder; use ~67% of remainder for semi, 33% telecom
    semi_share = remainder * (2 / 3)
    telecom_share = remainder * (1 / 3)
    return {
        "semiconductors": semi_share,
        "machine_tools": mt_share,
        "telecom": telecom_share,
    }


def generate_series() -> pd.DataFrame:
    """Generate month × category rows for 2022-03 to 2024-10."""
    dates = pd.date_range("2022-03", "2024-10", freq="MS")
    rows = []

    for month_idx, dt in enumerate(dates):
        shares = _category_shares(month_idx, len(dates))
        for category, share in shares.items():
            value_usd = int(round(TOTAL_MONTHLY_USD * share, 0))
            rows.append({
                "date": dt.strftime("%Y-%m"),
                "category": category,
                "value_usd": value_usd,
                "share_china": SHARE_CHINA[category],
                "source": SOURCE_LABEL,
            })

    return pd.DataFrame(rows)


def main() -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = generate_series()
    df.to_csv(OUTPUT_FILE, index=False)
    return str(OUTPUT_FILE)


if __name__ == "__main__":
    out_path = main()
    df = pd.read_csv(out_path)
    print(f"Saved: {out_path}")
    print(f"Rows: {len(df)}, Columns: {list(df.columns)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
