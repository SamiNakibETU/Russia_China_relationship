"""Download GDELT Event Database - selective key periods for Russia-China analysis."""
import requests
import os
import time
from pathlib import Path

DEST = Path(r"d:\Users\Proprietaire\Desktop\Projet_perso\Chine-russie\russia_china_dependency\01_raw_data\gdelt_full")
DEST.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://data.gdeltproject.org/events/"

# Strategy: download 1st and 15th of each month for key years
# This gives ~24 files/year, enough for monthly aggregation
dates = []

# Key years: 2013-2025 (bi-monthly samples)
for year in range(2013, 2026):
    for month in range(1, 13):
        for day in [1, 15]:
            dates.append(f"{year}{month:02d}{day:02d}")

# 2026 (jan-feb)
for month in range(1, 3):
    for day in [1, 15]:
        dates.append(f"2026{month:02d}{day:02d}")

files = [f"{d}.export.CSV.zip" for d in dates]
downloaded = 0
skipped = 0
failed = 0

print(f"=== GDELT Download: {len(files)} fichiers a verifier ===\n")

for i, fname in enumerate(files):
    dest = DEST / fname
    
    if dest.exists() and dest.stat().st_size > 100:
        skipped += 1
        continue
    
    url = BASE_URL + fname
    try:
        r = requests.get(url, timeout=20, stream=True)
        if r.status_code == 200:
            with open(dest, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            size = dest.stat().st_size / 1e6
            downloaded += 1
            if downloaded % 10 == 0:
                print(f"  [{downloaded} telecharges] dernier: {fname} ({size:.1f} MB)")
        else:
            failed += 1
    except Exception:
        failed += 1
    
    time.sleep(0.3)
    
    # Progress every 50 files
    if (i + 1) % 50 == 0:
        print(f"  Progress: {i+1}/{len(files)} (dl:{downloaded}, skip:{skipped}, fail:{failed})")

print(f"\n=== GDELT Resume ===")
print(f"  Telecharges: {downloaded}")
print(f"  Deja existants: {skipped}")
print(f"  Echoues/indisponibles: {failed}")

# Count total files
total_files = len(list(DEST.glob("*.zip")))
total_size = sum(f.stat().st_size for f in DEST.glob("*.zip")) / 1e6
print(f"  Total dans dossier: {total_files} fichiers ({total_size:.0f} MB)")
