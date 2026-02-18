"""
Configuration centralisee du projet Chine-Russie.
Chemins et constantes pour tous les notebooks et scripts.
"""
from pathlib import Path

# Racine du projet (dossier Chine-russie)
_candidates = [Path(__file__).resolve().parent, Path.cwd(), Path.cwd().parent]
for c in _candidates:
    _proj = c / "russia_china_dependency"
    if _proj.exists() and (_proj / "01_raw_data").exists():
        PROJECT_ROOT = c
        break
else:
    PROJECT_ROOT = Path.cwd()

# Chemins principaux
PROJECT = PROJECT_ROOT / "russia_china_dependency"
RAW_DATA = PROJECT / "01_raw_data"
PROCESSED_DATA = PROJECT / "02_processed_data"
REPORTS = PROJECT_ROOT / "reports"
FIGURES = REPORTS / "figures"

# Sous-dossiers raw
TRADE = RAW_DATA / "trade"
PRICES = RAW_DATA / "prices"
MACRO = RAW_DATA / "macro"
ENERGY = RAW_DATA / "energy"
DIPLOMATIC = RAW_DATA / "diplomatic"
GRAVITY = RAW_DATA / "gravity"
COMPLEXITY = RAW_DATA / "complexity"
ARMS = RAW_DATA / "arms"
GDELT = RAW_DATA / "gdelt_full"

# Creer les dossiers de sortie si necessaire
FIGURES.mkdir(parents=True, exist_ok=True)
