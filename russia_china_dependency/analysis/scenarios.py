"""
Scenario modeling: Russia-China dependency 2025-2030.

References:
  Carnegie 2024: dual-use ~300 M$/mo, 89% China (Politika)
  AEI 2024: semiconductor markup ~2x for Russia
  CEPR DP 18934: Urals discount, oil-trade elasticity
  Head & Mayer 2014: gravity GDP elasticity ~0.9
  SIPRI/Reuters: defense 140 B$ (2024), 175 B$ (2025)
"""
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "02_processed_data"
OUT_FILE = DATA_DIR / "scenario_projections_2025_2030.csv"

# Baseline 2024 (Carnegie, Comtrade, SIPRI)
DUAL_USE_MONTHLY = 300e6
OIL_REVENUE_CHN = 60e9
DEFENSE_2024 = 140e9
DEFENSE_2025 = 175e9
TRADE_VOLUME = 245e9
YUAN_SHARE = 0.30
CHN_SHARE_DUALUSE = 0.89

# Elasticities (literature)
ELAS_OIL_TRADE = 0.65  # oil revenue to trade (CEPR 18934, Kiel IfW)
ELAS_GDP_TRADE = 0.90  # gravity (Head & Mayer 2014)
DEFENSE_GROWTH_BASE = 0.05


def _mdi_composite(ccd: float, wfd: float, sri: float) -> dict:
    """MDI 0-100. CCD=dual-use share, WFD=oil/defense, SRI=yuan*trade."""
    weights = (0.40, 0.40, 0.20)
    mdi = weights[0] * ccd + weights[1] * wfd + weights[2] * sri
    if mdi < 30:
        cat = "low"
    elif mdi < 60:
        cat = "moderate"
    elif mdi < 80:
        cat = "high"
    else:
        cat = "critical"
    return {"mdi": round(mdi, 2), "category": cat}


def project_scenario(
    name: str,
    dual_use_path: list[float],
    oil_path: list[float],
    defense_path: list[float],
    trade_path: list[float],
    yuan_path: list[float],
) -> pd.DataFrame:
    """
    Project MDI over 2025-2030 with year-by-year paths.

    Paths are annual multipliers or levels (indexed to baseline).
    """
    years = list(range(2025, 2031))
    n = len(years)
    results = []
    for i in range(n):
        du = DUAL_USE_MONTHLY * dual_use_path[i]
        oil = OIL_REVENUE_CHN * oil_path[i]
        def_ = defense_path[i]
        trade = TRADE_VOLUME * trade_path[i]
        yuan = yuan_path[i]
        ccd = (du / (du + 50e6)) * CHN_SHARE_DUALUSE * 100 if du > 0 else 0
        wfd = (oil / def_) * 100 if def_ > 0 else 0
        sri = yuan * min(trade / 100e9, 1) * 100
        m = _mdi_composite(ccd, wfd, sri)
        results.append({
            "year": years[i],
            "scenario": name,
            "mdi": m["mdi"],
            "dual_use_bn": du * 12 / 1e9,
            "oil_revenue_bn": oil / 1e9,
            "defense_bn": def_ / 1e9,
            "trade_bn": trade / 1e9,
            "category": m["category"],
        })
    return pd.DataFrame(results)


# Scenario definitions: annual paths (index or level)
# S1: China stops dual-use (secondary sanctions, AEI/Carnegie)
#     dual-use -> 0 over 2yr, trade -15% (substitution lag)
SCENARIO_PATHS = {
    "S1_China_Stops": {
        "dual_use": [0.7, 0.3, 0.1, 0.05, 0.02, 0],
        "oil": [1.0, 0.98, 0.96, 0.94, 0.92, 0.90],
        "defense": [175e9, 160e9, 145e9, 135e9, 130e9, 125e9],
        "trade": [0.92, 0.85, 0.80, 0.78, 0.77, 0.76],
        "yuan": [0.28, 0.25, 0.22, 0.20, 0.18, 0.17],
    },
    # S2: Oil crash (Brent -40%, Urals discount widens, CEPR)
    "S2_Oil_Crash": {
        "dual_use": [1.0] * 6,
        "oil": [0.55, 0.50, 0.55, 0.60, 0.62, 0.65],
        "defense": [165e9, 155e9, 150e9, 148e9, 146e9, 145e9],
        "trade": [0.80, 0.75, 0.78, 0.82, 0.85, 0.87],
        "yuan": [0.32, 0.34, 0.33, 0.32, 0.31, 0.30],
    },
    # S3: War ends (2026), defense down, dual-use subsides
    "S3_War_Ends": {
        "dual_use": [0.9, 0.5, 0.25, 0.20, 0.18, 0.17],
        "oil": [1.0, 0.90, 0.82, 0.80, 0.79, 0.78],
        "defense": [170e9, 120e9, 95e9, 90e9, 88e9, 86e9],
        "trade": [1.0, 0.95, 0.92, 0.90, 0.89, 0.88],
        "yuan": [0.28, 0.26, 0.24, 0.23, 0.22, 0.21],
    },
    # S4: Integration deepens (Belt & Road, yuan clearing)
    "S4_Integration": {
        "dual_use": [1.1, 1.25, 1.4, 1.5, 1.55, 1.6],
        "oil": [1.05, 1.12, 1.15, 1.18, 1.20, 1.22],
        "defense": [180e9, 185e9, 188e9, 190e9, 192e9, 195e9],
        "trade": [1.05, 1.12, 1.18, 1.24, 1.30, 1.35],
        "yuan": [0.35, 0.42, 0.48, 0.52, 0.55, 0.58],
    },
}


def main() -> str:
    """Generate scenario_projections_2025_2030.csv."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    all_dfs = []
    for name, paths in SCENARIO_PATHS.items():
        df = project_scenario(
            name,
            paths["dual_use"],
            paths["oil"],
            paths["defense"],
            paths["trade"],
            paths["yuan"],
        )
        all_dfs.append(df)
    combined = pd.concat(all_dfs, ignore_index=True)
    combined.to_csv(OUT_FILE, index=False)
    return str(OUT_FILE)


if __name__ == "__main__":
    out = main()
    print(f"Saved: {out}")
