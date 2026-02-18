import pandas as pd

# 1. Analyse CMO (Commodity Markets Outlook - World Bank)
print("=== CMO WORLD BANK ===")
cmo = pd.ExcelFile("russia_china_dependency/01_raw_data/prices/CMO-Historical-Data-Monthly.xlsx")
print(f"Feuilles disponibles: {cmo.sheet_names}")

# Lecture de la feuille principale
df_prices = pd.read_excel(cmo, sheet_name="Monthly Prices")
print(f"\nColonnes prix: {df_prices.columns.tolist()[:15]}...")

# Cherche Manufactures Unit Value Index
muv_cols = [c for c in df_prices.columns if 'MUV' in str(c).upper() or 'MANUFACT' in str(c).upper()]
print(f"\nColonnes Manufactures trouvees: {muv_cols}")

# 2. Analyse CEPII GeoDist
print("\n=== CEPII GEODIST ===")
cepii = pd.read_excel("russia_china_dependency/01_raw_data/gravity/dist_cepii.xls")
print(f"Colonnes: {cepii.columns.tolist()}")
print(f"Lignes: {len(cepii)}")

# Cherche la paire Russie-Chine
rus_chn = cepii[
    ((cepii['iso_o'] == 'RUS') & (cepii['iso_d'] == 'CHN')) |
    ((cepii['iso_o'] == 'CHN') & (cepii['iso_d'] == 'RUS'))
]
print(f"\nPaire Russie-Chine:")
print(rus_chn)

# 3. Analyse geo_cepii (coordonnées géographiques)
print("\n=== CEPII GEO ===")
geo = pd.read_excel("russia_china_dependency/01_raw_data/gravity/geo_cepii.xls")
print(f"Colonnes: {geo.columns.tolist()}")
print(f"Pays: {len(geo)}")



