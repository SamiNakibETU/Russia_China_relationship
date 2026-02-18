"""Download IMF Direction of Trade Statistics (DOTS) via REST API."""
import requests
import json
import time
import pandas as pd
from pathlib import Path

DEST = Path(r"d:\Users\Proprietaire\Desktop\Projet_perso\Chine-russie\russia_china_dependency\01_raw_data\imf_dots")
DEST.mkdir(parents=True, exist_ok=True)

OUTPUT = DEST / "imf_dots_bilateral_monthly.csv"

if OUTPUT.exists() and OUTPUT.stat().st_size > 10000:
    print(f"[SKIP] Deja telecharge: {OUTPUT} ({OUTPUT.stat().st_size/1e6:.1f} MB)")
    exit(0)

BASE_URL = "https://dataservices.imf.org/REST/SDMX_JSON.svc"

reporters = ["RU", "CN"]
partners = {
    "RU": "Russia",
    "CN": "China",
    "IN": "India",
    "TR": "Turkey",
    "KZ": "Kazakhstan",
    "AE": "UAE",
    "DE": "Germany",
    "US": "United States",
}
indicators = ["TXG_FOB_USD", "TMG_CIF_USD"]

all_data = []

for reporter in reporters:
    for pcode, pname in partners.items():
        if reporter == pcode:
            continue
        for ind in indicators:
            key = f"M.{reporter}.{pcode}.{ind}"
            url = f"{BASE_URL}/CompactData/DOT/{key}?startPeriod=2000&endPeriod=2025"

            try:
                r = requests.get(url, timeout=30)
                if r.status_code == 200:
                    data = r.json()
                    series = data.get("CompactData", {}).get("DataSet", {}).get("Series", {})
                    if isinstance(series, dict):
                        series = [series]

                    count = 0
                    for s in series:
                        obs = s.get("Obs", [])
                        if isinstance(obs, dict):
                            obs = [obs]
                        for o in obs:
                            all_data.append({
                                "reporter": reporter,
                                "partner": pcode,
                                "indicator": ind,
                                "period": o.get("@TIME_PERIOD", ""),
                                "value": float(o.get("@OBS_VALUE", 0)),
                            })
                            count += 1

                    ind_label = "Exports" if "TXG" in ind else "Imports"
                    print(f"  {reporter} -> {pcode} ({ind_label}): {count} obs")
                elif r.status_code == 429:
                    print(f"  {reporter} -> {pcode}: Rate limited, waiting 5s...")
                    time.sleep(5)
                else:
                    print(f"  {reporter} -> {pcode}: HTTP {r.status_code}")
            except Exception as e:
                print(f"  {reporter} -> {pcode}: ERR {e}")

            time.sleep(1.5)  # Rate limiting

if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT, index=False)
    
    n_pairs = len(df.groupby(["reporter", "partner"]))
    period_min = df["period"].min()
    period_max = df["period"].max()
    
    print(f"\n[OK] Sauvegarde: {OUTPUT}")
    print(f"  {len(df)} observations")
    print(f"  {n_pairs} paires bilaterales")
    print(f"  Periode: {period_min} -> {period_max}")
    
    # Stats par paire
    print("\nResume par paire:")
    for (rep, par), grp in df.groupby(["reporter", "partner"]):
        print(f"  {rep} -> {par}: {len(grp)} obs, {grp['period'].min()} - {grp['period'].max()}")
else:
    print("[WARN] Aucune donnee recuperee")
