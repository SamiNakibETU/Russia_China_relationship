"""
08_process_wits_hhi.py
Traitement des données WITS et calcul du HHI (Herfindahl-Hirschman Index)
"""
import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
RAW_DIR = PROJECT_ROOT / "01_raw_data"
OUTPUT_DIR = PROJECT_ROOT / "02_processed_data"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_wits():
    """Charge les données WITS"""
    wits_path = RAW_DIR / "trade" / "wits_russia_china_hs6_2007_2021.csv"
    if not wits_path.exists():
        print(f"Fichier non trouve: {wits_path}")
        return pd.DataFrame()
    
    df = pd.read_csv(wits_path, encoding='latin-1', low_memory=False)
    print(f"WITS charge: {len(df):,} lignes")
    return df

def calculate_hhi_hs2(df):
    """
    Calcule le HHI (Herfindahl-Hirschman Index) au niveau HS2
    
    HHI = Σ(s_i)² où s_i est la part du produit i dans le total des exports
    
    Interprétation:
    - HHI < 0.15 : Marché non concentré
    - 0.15 < HHI < 0.25 : Marché modérément concentré
    - HHI > 0.25 : Marché très concentré
    """
    print("\n=== CALCUL HHI (Concentration des Exports) ===")
    
    # Extraire le code HS2 (2 premiers chiffres)
    df['HS2'] = df['ProductCode'].astype(str).str[:2]
    
    # Filtrer pour les exports uniquement
    exports = df[df['TradeFlowName'] == 'Export'].copy()
    
    # Agrégation par année et HS2
    exports_by_hs2 = exports.groupby(['Year', 'HS2'])['TradeValue in 1000 USD'].sum().reset_index()
    exports_by_hs2.columns = ['Year', 'HS2', 'Value']
    
    # Total exports par année
    total_by_year = exports_by_hs2.groupby('Year')['Value'].sum().reset_index()
    total_by_year.columns = ['Year', 'TotalValue']
    
    # Merge pour calculer les parts
    merged = pd.merge(exports_by_hs2, total_by_year, on='Year')
    merged['Share'] = merged['Value'] / merged['TotalValue']
    merged['ShareSquared'] = merged['Share'] ** 2
    
    # HHI par année
    hhi_by_year = merged.groupby('Year')['ShareSquared'].sum().reset_index()
    hhi_by_year.columns = ['Year', 'HHI_RUS_Exports_to_CHN']
    
    print("HHI des exports russes vers Chine par annee:")
    print(hhi_by_year.to_string(index=False))
    
    # Analyse des top secteurs
    print("\n=== TOP 10 SECTEURS EXPORTS RUS->CHN (moyenne 2019-2021) ===")
    recent = merged[merged['Year'] >= 2019].groupby('HS2').agg({
        'Value': 'mean',
        'Share': 'mean'
    }).sort_values('Share', ascending=False).head(10)
    
    # Ajouter descriptions HS2
    hs2_desc = {
        '27': 'Combustibles mineraux (petrole, gaz)',
        '44': 'Bois et ouvrages en bois',
        '26': 'Minerais, scories, cendres',
        '03': 'Poissons et crustaces',
        '31': 'Engrais',
        '28': 'Produits chimiques inorganiques',
        '71': 'Pierres et metaux precieux',
        '74': 'Cuivre et ouvrages en cuivre',
        '76': 'Aluminium et ouvrages',
        '72': 'Fonte, fer et acier'
    }
    
    recent['Description'] = recent.index.map(lambda x: hs2_desc.get(x, 'Autre'))
    recent['Value_Mrd_USD'] = recent['Value'] / 1e6
    recent['Share_pct'] = recent['Share'] * 100
    
    print(recent[['Description', 'Value_Mrd_USD', 'Share_pct']].to_string())
    
    return hhi_by_year, merged

def calculate_ecr(df):
    """
    Calcule l'Export Concentration Ratio (ECR)
    Part des X premiers produits dans le total
    """
    print("\n=== ECR (Export Concentration Ratio) ===")
    
    # HS2 level
    df['HS2'] = df['ProductCode'].astype(str).str[:2]
    exports = df[df['TradeFlowName'] == 'Export'].copy()
    
    results = []
    
    for year in sorted(exports['Year'].unique()):
        year_data = exports[exports['Year'] == year]
        by_hs2 = year_data.groupby('HS2')['TradeValue in 1000 USD'].sum().sort_values(ascending=False)
        total = by_hs2.sum()
        
        # Top 1, 3, 5 ratios
        top1 = by_hs2.head(1).sum() / total * 100
        top3 = by_hs2.head(3).sum() / total * 100
        top5 = by_hs2.head(5).sum() / total * 100
        
        results.append({
            'Year': year,
            'ECR_Top1': top1,
            'ECR_Top3': top3,
            'ECR_Top5': top5
        })
    
    ecr_df = pd.DataFrame(results)
    print(ecr_df.to_string(index=False))
    
    return ecr_df

def calculate_trade_balance(df):
    """Calcule la balance commerciale Russie-Chine"""
    print("\n=== BALANCE COMMERCIALE RUS-CHN ===")
    
    exports = df[df['TradeFlowName'] == 'Export'].groupby('Year')['TradeValue in 1000 USD'].sum()
    imports = df[df['TradeFlowName'] == 'Import'].groupby('Year')['TradeValue in 1000 USD'].sum()
    
    balance = pd.DataFrame({
        'Year': exports.index,
        'WITS_RUS_Exports_to_CHN': exports.values / 1e6,  # Milliards USD
        'WITS_RUS_Imports_from_CHN': imports.values / 1e6,
    })
    balance['Trade_Balance_RUS_CHN'] = balance['WITS_RUS_Exports_to_CHN'] - balance['WITS_RUS_Imports_from_CHN']
    balance['Trade_Balance_Ratio'] = balance['WITS_RUS_Exports_to_CHN'] / balance['WITS_RUS_Imports_from_CHN']
    
    print("(en milliards USD)")
    print(balance.to_string(index=False))
    
    return balance

def main():
    print("=" * 70)
    print("TRAITEMENT WITS - CALCUL HHI ET INDICATEURS DE CONCENTRATION")
    print("=" * 70)
    
    df = load_wits()
    if df.empty:
        return
    
    # 1. HHI
    hhi_df, exports_by_hs2 = calculate_hhi_hs2(df)
    
    # 2. ECR
    ecr_df = calculate_ecr(df)
    
    # 3. Trade Balance
    balance_df = calculate_trade_balance(df)
    
    # 4. Merge tous les indicateurs
    wits_indicators = pd.merge(hhi_df, ecr_df, on='Year')
    wits_indicators = pd.merge(wits_indicators, balance_df, on='Year')
    
    # 5. Sauvegarder
    wits_indicators.to_csv(OUTPUT_DIR / "wits_concentration_indicators.csv", index=False)
    exports_by_hs2.to_csv(OUTPUT_DIR / "wits_exports_by_hs2.csv", index=False)
    
    print("\n" + "=" * 70)
    print("FICHIERS SAUVEGARDES:")
    print(f"  - wits_concentration_indicators.csv")
    print(f"  - wits_exports_by_hs2.csv")
    print("=" * 70)
    
    return wits_indicators

if __name__ == "__main__":
    main()



