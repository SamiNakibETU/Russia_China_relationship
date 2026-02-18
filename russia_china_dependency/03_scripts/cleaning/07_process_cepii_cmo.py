"""
07_process_cepii_cmo.py
Traitement des données CEPII (gravity) et CMO (MUV) pour le modèle de gravité
"""
import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
RAW_DIR = PROJECT_ROOT / "01_raw_data"
OUTPUT_DIR = PROJECT_ROOT / "02_processed_data"
OUTPUT_DIR.mkdir(exist_ok=True)

def process_cepii_geodist():
    """Traite les données CEPII GeoDist pour le modèle de gravité"""
    print("=== CEPII GeoDist ===")
    
    dist_path = RAW_DIR / "gravity" / "dist_cepii.xls"
    if not dist_path.exists():
        print(f"  Fichier non trouvé: {dist_path}")
        return pd.DataFrame()
    
    df = pd.read_excel(dist_path)
    
    # Variables disponibles:
    # iso_o, iso_d : codes ISO pays origine/destination
    # contig : frontière commune (1/0)
    # comlang_off : langue officielle commune (1/0)
    # comlang_ethno : langue ethnique commune (1/0)
    # colony : relation coloniale (1/0)
    # dist : distance en km (population weighted)
    # distcap : distance entre capitales
    
    # Extraire la paire Russie-Chine
    rus_chn = df[
        ((df['iso_o'] == 'RUS') & (df['iso_d'] == 'CHN')) |
        ((df['iso_o'] == 'CHN') & (df['iso_d'] == 'RUS'))
    ].copy()
    
    print(f"  Paire RUS-CHN trouvée: {len(rus_chn)} entrées")
    print(f"  Distance: {rus_chn['dist'].values[0]:.0f} km")
    print(f"  Contiguïté: {rus_chn['contig'].values[0]}")
    print(f"  Langue commune: {rus_chn['comlang_off'].values[0]}")
    
    # Sauvegarder les données brutes complètes (pour PPML sur panel multi-pays)
    df.to_csv(OUTPUT_DIR / "cepii_geodist_full.csv", index=False)
    rus_chn.to_csv(OUTPUT_DIR / "cepii_geodist_rus_chn.csv", index=False)
    
    print(f"  Sauvegardé: cepii_geodist_full.csv ({len(df)} paires)")
    print(f"  Sauvegardé: cepii_geodist_rus_chn.csv")
    
    return df

def process_cepii_geo():
    """Traite les données géographiques CEPII"""
    print("\n=== CEPII Geo ===")
    
    geo_path = RAW_DIR / "gravity" / "geo_cepii.xls"
    if not geo_path.exists():
        print(f"  Fichier non trouvé: {geo_path}")
        return pd.DataFrame()
    
    df = pd.read_excel(geo_path)
    
    # Extraire Russie et Chine
    rus_chn = df[df['iso3'].isin(['RUS', 'CHN'])][
        ['iso3', 'country', 'area', 'landlocked', 'continent', 'lat', 'lon']
    ]
    
    print(f"  Pays: {rus_chn['country'].tolist()}")
    print(f"  Continents: {rus_chn['continent'].tolist()}")
    
    df.to_csv(OUTPUT_DIR / "cepii_geo_full.csv", index=False)
    rus_chn.to_csv(OUTPUT_DIR / "cepii_geo_rus_chn.csv", index=False)
    
    print(f"  Sauvegardé: cepii_geo_full.csv ({len(df)} pays)")
    
    return df

def process_muv_index():
    """Traite l'indice MUV (Manufactures Unit Value) de la Banque Mondiale"""
    print("\n=== MUV Index (World Bank CMO) ===")
    
    cmo_annual_path = RAW_DIR / "prices" / "CMO-Historical-Data-Annual.xlsx"
    if not cmo_annual_path.exists():
        print(f"  Fichier non trouvé: {cmo_annual_path}")
        return pd.DataFrame()
    
    cmo = pd.ExcelFile(cmo_annual_path)
    
    # Lire les indices nominaux et réels
    nominal = pd.read_excel(cmo, sheet_name='Annual Indices (Nominal)', header=9)
    real = pd.read_excel(cmo, sheet_name='Annual Indices (Real)', header=9)
    
    nominal = nominal.rename(columns={'Unnamed: 0': 'Year'})
    real = real.rename(columns={'Unnamed: 0': 'Year'})
    
    # MUV = Nominal / Real (le déflateur utilisé)
    merged = pd.merge(
        nominal[['Year', 'iOVERALL', 'iENERGY', 'iNONFUEL', 'iMETMIN']],
        real[['Year', 'KiOVERALL', 'KiENERGY', 'KiNONFUEL', 'KiMETMIN']],
        on='Year'
    )
    
    # Calculer le MUV (indice des prix manufacturés)
    merged['MUV_Index'] = (merged['iOVERALL'] / merged['KiOVERALL']) * 100
    
    # Créer indices pour calcul ToT (Terms of Trade)
    # ToT Russie = Prix exports Russie / Prix imports Russie
    # Russie exporte: énergie, métaux -> iENERGY, iMETMIN
    # Russie importe: manufacturés -> on utilise MUV
    
    merged['Energy_Index_Nominal'] = merged['iENERGY']
    merged['Metals_Index_Nominal'] = merged['iMETMIN']
    
    # ToT approximatif Russie = (Energy + Metals) / MUV
    merged['ToT_Russia_Approx'] = (merged['iENERGY'] * 0.6 + merged['iMETMIN'] * 0.4) / merged['MUV_Index'] * 100
    
    result = merged[['Year', 'MUV_Index', 'Energy_Index_Nominal', 'Metals_Index_Nominal', 'ToT_Russia_Approx']]
    result = result.dropna()
    
    result.to_csv(OUTPUT_DIR / "muv_tot_indices.csv", index=False)
    
    print(f"  Période: {result['Year'].min()} - {result['Year'].max()}")
    print(f"  MUV 2023: {result[result['Year']==2023]['MUV_Index'].values[0]:.1f}")
    print(f"  ToT Russie 2023: {result[result['Year']==2023]['ToT_Russia_Approx'].values[0]:.1f}")
    print(f"  Sauvegardé: muv_tot_indices.csv")
    
    return result

def process_cmo_prices():
    """Extrait les prix des commodités du CMO"""
    print("\n=== CMO Commodity Prices ===")
    
    cmo_annual_path = RAW_DIR / "prices" / "CMO-Historical-Data-Annual.xlsx"
    if not cmo_annual_path.exists():
        return pd.DataFrame()
    
    cmo = pd.ExcelFile(cmo_annual_path)
    
    # Lecture des prix nominaux
    prices = pd.read_excel(cmo, sheet_name='Annual Prices (Nominal)', header=4)
    
    # Les colonnes importantes:
    # CRUDE_BRENT, CRUDE_WTI : pétrole
    # NGAS_EUR, NGAS_US, NGAS_JP : gaz naturel
    # COAL_AUS : charbon
    # ALUMINUM, COPPER, IRON_ORE, NICKEL : métaux
    
    # Première colonne = Year
    prices = prices.rename(columns={prices.columns[0]: 'Year'})
    prices = prices.dropna(subset=['Year'])
    prices['Year'] = pd.to_numeric(prices['Year'], errors='coerce')
    prices = prices.dropna(subset=['Year'])
    prices['Year'] = prices['Year'].astype(int)
    
    # Sélectionner les colonnes clés pour Russie-Chine
    key_cols = ['Year']
    for col in prices.columns:
        if any(x in col.upper() for x in ['CRUDE', 'NGAS', 'COAL', 'ALUM', 'COPPER', 'IRON', 'NICKEL', 'GOLD']):
            key_cols.append(col)
    
    result = prices[key_cols].copy()
    result.to_csv(OUTPUT_DIR / "cmo_commodity_prices.csv", index=False)
    
    print(f"  Colonnes extraites: {len(key_cols)-1}")
    print(f"  Période: {result['Year'].min()} - {result['Year'].max()}")
    print(f"  Sauvegardé: cmo_commodity_prices.csv")
    
    return result

def main():
    print("=" * 60)
    print("TRAITEMENT CEPII & CMO (World Bank)")
    print("=" * 60)
    
    process_cepii_geodist()
    process_cepii_geo()
    process_muv_index()
    process_cmo_prices()
    
    print("\n" + "=" * 60)
    print("TRAITEMENT TERMINÉ")
    print("=" * 60)

if __name__ == "__main__":
    main()



