import pandas as pd
import os

files = [
    "russia_china_dependency/01_raw_data/finance/2025 Country Transition Tracker Data.xlsx",
    "russia_china_dependency/01_raw_data/energy/EI-Stats-Review-ALL-data.xlsx"
]

for f in files:
    if os.path.exists(f):
        try:
            xl = pd.ExcelFile(f)
            print(f"\nFichier : {f}")
            print(f"Feuilles : {xl.sheet_names[:10]}... (Total: {len(xl.sheet_names)})")
        except Exception as e:
            print(f"Erreur sur {f}: {e}")
    else:
        print(f"Fichier non trouvé : {f}")





