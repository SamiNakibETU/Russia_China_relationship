import pandas as pd
from pathlib import Path
import os

# Consolidation des fichiers USD/RUB
files = [
    "new/new_2/new_3/USD_RUB Historical Data.csv",
    "new/new_2/new_3/USD_RUB Historical Data (1).csv",
    "new/new_2/new_3/USD_RUB Historical Data (2).csv"
]

all_data = []
for f in files:
    df = pd.read_csv(f)
    all_data.append(df)
    print(f"{f}: {len(df)} lignes, {df['Date'].iloc[0]} - {df['Date'].iloc[-1]}")

# Fusion et deduplication
combined = pd.concat(all_data, ignore_index=True)
combined = combined.drop_duplicates(subset=['Date'])
combined = combined.sort_values('Date', ascending=False)

# Sauvegarde
output = Path("russia_china_dependency/01_raw_data/macro/usd_rub_investing.csv")
combined.to_csv(output, index=False)
print(f"\nConsolide: {len(combined)} lignes -> {output}")



