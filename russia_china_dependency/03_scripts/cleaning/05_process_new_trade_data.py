import pandas as pd
import os
from pathlib import Path
import glob
import csv

# === CONFIGURATION ===
NEW_DIR = Path("new")
UNZIPPED_DIR = NEW_DIR / "unzipped"
OUTPUT_DIR = Path("russia_china_dependency/01_raw_data/trade")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_comtrade_files():
    """Traitement des fichiers TradeData (UN Comtrade)"""
    print("=== TRAITEMENT DES FICHIERS COMTRADE ===")
    files = list(NEW_DIR.glob("TradeData_*.csv"))
    print(f"Fichiers trouves : {len(files)}")
    
    all_data = []
    for f in files:
        try:
            # Les fichiers ont une colonne vide a la fin (trailing comma)
            # On lit d'abord le header pour avoir les vrais noms de colonnes
            with open(f, 'r', encoding='latin-1') as file:
                header = file.readline().strip().split(',')
            
            # Lecture du fichier en ignorant la derniere colonne vide
            df = pd.read_csv(f, encoding='latin-1', usecols=range(len(header)))
            all_data.append(df)
            print(f"  - {f.name}: {len(df)} lignes")
        except Exception as e:
            print(f"  ERREUR {f.name}: {e}")
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined = combined.drop_duplicates()
        output_file = OUTPUT_DIR / "comtrade_detailed_2013_2024.csv"
        combined.to_csv(output_file, index=False)
        print(f"[OK] Comtrade consolide : {len(combined)} lignes -> {output_file}")
        
        # Verification
        years = combined['refYear'].unique()
        print(f"    Annees: {sorted(years)}")
        print(f"    Reporters: {combined['reporterDesc'].unique()}")
        return combined
    return pd.DataFrame()

def process_exports_by_product():
    """Traitement des fichiers exports par produit HS4"""
    print("\n=== TRAITEMENT EXPORTS PAR PRODUIT HS4 ===")
    files = list(UNZIPPED_DIR.glob("exports-by-product-at-hs4-*.csv"))
    print(f"Fichiers trouves : {len(files)}")
    
    all_data = []
    for f in files:
        try:
            df = pd.read_csv(f)
            all_data.append(df)
            print(f"  - {f.name}: {len(df)} lignes")
        except Exception as e:
            print(f"  ERREUR {f.name}: {e}")
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined = combined.drop_duplicates()
        output_file = OUTPUT_DIR / "exports_bilateral_hs4_2018_2023.csv"
        combined.to_csv(output_file, index=False)
        print(f"[OK] Exports bilateraux HS4 : {len(combined)} lignes -> {output_file}")
        return combined
    return pd.DataFrame()

def process_russia_exports():
    """Traitement des fichiers exports Russie vers Chine"""
    print("\n=== TRAITEMENT EXPORTS RUSSIE -> CHINE ===")
    files = list(UNZIPPED_DIR.glob("exports-from-russia-to-china-*.csv"))
    print(f"Fichiers trouves : {len(files)}")
    
    all_data = []
    for f in files:
        try:
            df = pd.read_csv(f)
            all_data.append(df)
            print(f"  - {f.name}: {len(df)} lignes")
        except Exception as e:
            print(f"  ERREUR {f.name}: {e}")
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined = combined.drop_duplicates()
        output_file = OUTPUT_DIR / "exports_russia_to_china_2018_2023.csv"
        combined.to_csv(output_file, index=False)
        print(f"[OK] Exports RUS->CHN : {len(combined)} lignes -> {output_file}")
        return combined
    return pd.DataFrame()

def process_tariffs():
    """Traitement des fichiers tarifs douaniers"""
    print("\n=== TRAITEMENT TARIFS DOUANIERS ===")
    files = list(UNZIPPED_DIR.glob("russias-tariffs-*.csv"))
    print(f"Fichiers trouves : {len(files)}")
    
    all_data = []
    for f in files:
        try:
            df = pd.read_csv(f)
            year = f.name.split("-in-")[1].split("-")[0]
            df['Year'] = int(year)
            all_data.append(df)
            print(f"  - {f.name}: {len(df)} lignes (annee {year})")
        except Exception as e:
            print(f"  ERREUR {f.name}: {e}")
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined = combined.drop_duplicates()
        output_file = OUTPUT_DIR / "tariffs_russia_from_china_2019_2023.csv"
        combined.to_csv(output_file, index=False)
        print(f"[OK] Tarifs RUS<-CHN : {len(combined)} lignes -> {output_file}")
        return combined
    return pd.DataFrame()

def generate_summary(df_comtrade, df_bilateral, df_rus_exp, df_tariffs):
    """Generation du resume des donnees"""
    print("\n" + "="*60)
    print("RESUME DES DONNEES TRAITEES")
    print("="*60)
    
    summaries = []
    
    if not df_comtrade.empty:
        years = sorted(df_comtrade['refYear'].unique())
        summaries.append({
            'Source': 'UN Comtrade (TradeData)',
            'Fichier': 'comtrade_detailed_2013_2024.csv',
            'Lignes': len(df_comtrade),
            'Annees': f"{min(years)}-{max(years)}",
            'Colonnes_cles': 'refYear, cmdCode, primaryValue, flowDesc',
            'Description': 'Donnees commerciales detaillees par produit (HS4)'
        })
    
    if not df_bilateral.empty:
        years = sorted(df_bilateral['Year'].unique())
        summaries.append({
            'Source': 'Exports bilateraux HS4',
            'Fichier': 'exports_bilateral_hs4_2018_2023.csv',
            'Lignes': len(df_bilateral),
            'Annees': f"{min(years)}-{max(years)}",
            'Colonnes_cles': "Year, HS4, Russia's Exports, China's Exports",
            'Description': 'Comparaison des exports par produit'
        })
    
    if not df_rus_exp.empty:
        years = sorted(df_rus_exp['Year'].unique())
        summaries.append({
            'Source': 'Exports Russie -> Chine',
            'Fichier': 'exports_russia_to_china_2018_2023.csv',
            'Lignes': len(df_rus_exp),
            'Annees': f"{min(years)}-{max(years)}",
            'Description': 'Exports russes vers Chine par produit'
        })
    
    if not df_tariffs.empty:
        years = sorted(df_tariffs['Year'].unique())
        summaries.append({
            'Source': 'Tarifs douaniers Russie',
            'Fichier': 'tariffs_russia_from_china_2019_2023.csv',
            'Lignes': len(df_tariffs),
            'Annees': f"{min(years)}-{max(years)}",
            'Description': 'Tarifs russes sur imports chinois'
        })
    
    for s in summaries:
        print(f"\n{s['Source']}")
        print(f"  Fichier: {s['Fichier']}")
        print(f"  Lignes: {s['Lignes']}")
        print(f"  Annees: {s['Annees']}")
        print(f"  Description: {s['Description']}")
    
    return summaries

if __name__ == "__main__":
    df1 = process_comtrade_files()
    df2 = process_exports_by_product()
    df3 = process_russia_exports()
    df4 = process_tariffs()
    generate_summary(df1, df2, df3, df4)
