"""Download Harvard Atlas of Economic Complexity datasets."""
import requests
import zipfile
import os
from pathlib import Path

DEST = Path(r"d:\Users\Proprietaire\Desktop\Projet_perso\Chine-russie\russia_china_dependency\01_raw_data\complexity")
DEST.mkdir(parents=True, exist_ok=True)

datasets = {
    "complexity_rankings": "doi:10.7910/DVN/XTAQMC",
    "trade_hs92": "doi:10.7910/DVN/T4CHWJ",
    "classifications": "doi:10.7910/DVN/3BAL1O",
    "product_space": "doi:10.7910/DVN/FCDZBN",
}

for name, doi in datasets.items():
    dest_zip = DEST / f"atlas_{name}.zip"
    if dest_zip.exists() and dest_zip.stat().st_size > 1000:
        print(f"[SKIP] {name} deja telecharge ({dest_zip.stat().st_size/1e6:.1f} MB)")
        continue

    url = f"https://dataverse.harvard.edu/api/access/dataset/:persistentId?persistentId={doi}"
    print(f"\nTelechargement {name}...")
    print(f"  URL: {url}")

    try:
        r = requests.get(url, timeout=120, stream=True)
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        print(f"  Status: {r.status_code}, Size: {total/1e6:.1f} MB")

        dl = 0
        with open(dest_zip, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
                dl += len(chunk)
                if total > 0 and dl % (1024*1024) == 0:
                    print(f"  {dl/1e6:.0f}/{total/1e6:.0f} MB", end="\r")

        print(f"  [OK] Telecharge: {dl/1e6:.1f} MB")

        # Extract
        try:
            extract_dir = DEST / name
            extract_dir.mkdir(exist_ok=True)
            with zipfile.ZipFile(dest_zip, "r") as zf:
                zf.extractall(extract_dir)
                print(f"  [OK] Extrait dans {extract_dir}")
                for fn in zf.namelist()[:10]:
                    print(f"    - {fn}")
                if len(zf.namelist()) > 10:
                    print(f"    ... et {len(zf.namelist())-10} autres fichiers")
        except zipfile.BadZipFile:
            print("  [INFO] Pas un ZIP, fichier unique")

    except Exception as e:
        print(f"  [ERR] {e}")

print("\n=== Atlas download complete ===")
