"""
CRINK asymmetry indices.

Computes asymmetry ratio between country pairs:
  asymmetry(A→B) = (exports_A_to_B / total_exports_A) / (imports_B_from_A / total_imports_B)
  Higher = A more dependent on B (A sends more of its exports to B than B receives from A as share of B's imports).
"""
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "02_processed_data"

# Approximate 2024 total trade (bn USD) from World Bank / OEC — for asymmetry denominator
TOTAL_TRADE_2024 = {
    "CHN": {"total_exports_bn": 3400, "total_imports_bn": 3000},
    "RUS": {"total_exports_bn": 500, "total_imports_bn": 350},
    "IRN": {"total_exports_bn": 80, "total_imports_bn": 70},
    "PRK": {"total_exports_bn": 3, "total_imports_bn": 4},
}


def compute_asymmetry(
    exports_A_to_B: float,
    total_exports_A: float,
    imports_B_from_A: float,
    total_imports_B: float,
) -> float:
    """
    Asymmetry ratio: Higher = A more dependent on B.
    share_A = exports_A_to_B / total_exports_A (share of A's exports going to B)
    share_B = imports_B_from_A / total_imports_B (share of B's imports coming from A)
    """
    if total_exports_A <= 0 or total_imports_B <= 0:
        return np.nan
    share_A = exports_A_to_B / total_exports_A
    share_B = imports_B_from_A / total_imports_B  # B imports from A = A exports to B
    return share_A / share_B if share_B > 0 else np.inf


def total_trade_from_bilateral(bilateral: pd.DataFrame) -> pd.DataFrame:
    """Derive total CRINK exports/imports from bilateral flows."""
    countries = sorted(set(bilateral["exporter"].tolist() + bilateral["importer"].tolist()))
    rows = []
    for c in countries:
        exp = bilateral[bilateral["exporter"] == c]["value_bn"].sum()
        imp = bilateral[bilateral["importer"] == c]["value_bn"].sum()
        rows.append({"country": c, "total_exports_bn": exp, "total_imports_bn": imp})
    return pd.DataFrame(rows)


def build_total_trade(crink_only: bool = False) -> pd.DataFrame:
    """Build total trade DataFrame. If crink_only, use CRINK-internal sums; else use global estimates."""
    bilateral = pd.read_csv(DATA_DIR / "crink_bilateral_2024.csv")
    if crink_only:
        return total_trade_from_bilateral(bilateral)
    countries = ["CHN", "RUS", "IRN", "PRK"]
    return pd.DataFrame([
        {
            "country": c,
            "total_exports_bn": TOTAL_TRADE_2024[c]["total_exports_bn"],
            "total_imports_bn": TOTAL_TRADE_2024[c]["total_imports_bn"],
        }
        for c in countries
    ])


def compute_asymmetry_matrix(
    bilateral_trade: pd.DataFrame,
    total_trade: pd.DataFrame,
) -> pd.DataFrame:
    """
    Args:
        bilateral_trade: [exporter, importer, value_bn]
        total_trade: [country, total_exports_bn, total_imports_bn]

    Returns:
        Asymmetry matrix (row=exporter, col=importer). matrix[A,B] = A's dependence on B.
    """
    countries = sorted(set(bilateral_trade["exporter"].tolist() + bilateral_trade["importer"].tolist()))
    matrix = pd.DataFrame(index=countries, columns=countries, dtype=float)

    for i, country_a in enumerate(countries):
        for j, country_b in enumerate(countries):
            if country_a == country_b:
                matrix.loc[country_a, country_b] = np.nan
                continue
            flow = bilateral_trade[
                (bilateral_trade["exporter"] == country_a) & (bilateral_trade["importer"] == country_b)
            ]
            exports_A_to_B = flow["value_bn"].sum() if len(flow) else 0
            imports_B_from_A = exports_A_to_B  # B imports from A = A exports to B

            tot_a = total_trade[total_trade["country"] == country_a]
            tot_b = total_trade[total_trade["country"] == country_b]
            if tot_a.empty or tot_b.empty:
                matrix.loc[country_a, country_b] = np.nan
                continue
            total_exports_A = tot_a["total_exports_bn"].values[0]
            total_imports_B = tot_b["total_imports_bn"].values[0]

            matrix.loc[country_a, country_b] = compute_asymmetry(
                exports_A_to_B, total_exports_A,
                imports_B_from_A, total_imports_B,
            )
    return matrix


def main() -> pd.DataFrame:
    """Compute asymmetry matrix from crink_bilateral_2024."""
    bilateral = pd.read_csv(DATA_DIR / "crink_bilateral_2024.csv")
    total = build_total_trade(crink_only=False)
    matrix = compute_asymmetry_matrix(bilateral, total)
    out = DATA_DIR / "crink_asymmetry_matrix.csv"
    matrix.to_csv(out)
    return matrix


if __name__ == "__main__":
    m = main()
    print("CRINK Asymmetry Matrix (row = exporter, col = importer; >1 = row more dependent on col)")
    print(m.round(2).to_string())
    print(f"\nSaved to {DATA_DIR / 'crink_asymmetry_matrix.csv'}")
