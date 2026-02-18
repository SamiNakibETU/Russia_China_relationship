import pandas as pd
import numpy as np
import os
from pathlib import Path

# === CONFIGURATION ===
PROJECT_ROOT = Path(__file__).parent.parent.parent
RAW_DIR = PROJECT_ROOT / "01_raw_data"
OUTPUT_DIR = PROJECT_ROOT / "02_processed_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Codes Pays
RUS_BACI = 643
CHN_BACI = 156
RUS_COW = 365
CHN_COW = 710

def load_trade():
    print("Chargement Trade...")
    
    # Priorite au fichier Comtrade (plus recent et plus complet)
    comtrade_path = RAW_DIR / "trade" / "comtrade_detailed_2013_2024.csv"
    baci_path = RAW_DIR / "trade" / "baci_russia_china_processed_2017_2023.csv"
    
    if comtrade_path.exists():
        df = pd.read_csv(comtrade_path)
        # Agregation par annee et sens du flux
        # flowDesc = 'Export' ou 'Import'
        # reporterDesc = 'China' ou 'Russian Federation'
        
        # Exports de Russie vers Chine = Reporter=Russia, Flow=Export, Partner=China
        rus_exp = df[(df['reporterDesc'] == 'Russian Federation') & (df['flowDesc'] == 'Export')]
        rus_exp_annual = rus_exp.groupby('refYear')['primaryValue'].sum().reset_index()
        rus_exp_annual.columns = ['Year', 'Trade_RUS_Exp_to_CHN']
        
        # Exports de Chine vers Russie = Reporter=China, Flow=Export, Partner=Russia
        chn_exp = df[(df['reporterDesc'] == 'China') & (df['flowDesc'] == 'Export')]
        chn_exp_annual = chn_exp.groupby('refYear')['primaryValue'].sum().reset_index()
        chn_exp_annual.columns = ['Year', 'Trade_CHN_Exp_to_RUS']
        
        trade_annual = pd.merge(rus_exp_annual, chn_exp_annual, on='Year', how='outer')
        print(f"  Comtrade: {len(trade_annual)} annees (2013-2024)")
        return trade_annual
    
    elif baci_path.exists():
        df = pd.read_csv(baci_path)
        df['flow'] = np.where((df['i'] == RUS_BACI) & (df['j'] == CHN_BACI), 'RUS_to_CHN', 'CHN_to_RUS')
        trade_annual = df.groupby(['t', 'flow'])['v'].sum().unstack().reset_index()
        trade_annual.columns = ['Year', 'Trade_RUS_Exp_to_CHN', 'Trade_CHN_Exp_to_RUS']
        # BACI est en milliers USD, on convertit en USD pour cohérence avec Comtrade
        trade_annual['Trade_RUS_Exp_to_CHN'] = trade_annual['Trade_RUS_Exp_to_CHN'] * 1000
        trade_annual['Trade_CHN_Exp_to_RUS'] = trade_annual['Trade_CHN_Exp_to_RUS'] * 1000
        print(f"  BACI: {len(trade_annual)} annees")
        return trade_annual
    
    return pd.DataFrame()

def load_macro():
    print("Chargement Macro...")
    wb_path = RAW_DIR / "macro" / "worldbank_russia_china_raw.csv"
    if wb_path.exists():
        df = pd.read_csv(wb_path)
        # Normalisation
        df['country'] = df['country'].replace('Russian Federation', 'RUS')
        df['country'] = df['country'].replace('China', 'CHN')
        df_pivot = df.pivot(index='date', columns='country', values=['GDP_current_USD', 'GDP_growth_annual_percent', 'Inflation_consumer_prices_percent'])
        df_pivot.columns = [f"{col[1]}_{col[0]}" for col in df_pivot.columns]
        df_pivot = df_pivot.reset_index().rename(columns={'date': 'Year'})
        df_pivot['Year'] = df_pivot['Year'].astype(int)
        return df_pivot
    return pd.DataFrame()

def load_diplomatic():
    print("Chargement Diplomatique...")
    dip_path = RAW_DIR / "diplomatic" / "AgreementScoresAll_Jun2024.csv"
    if dip_path.exists():
        df = pd.read_csv(dip_path)
        mask = (
            ((df['ccode1'] == RUS_COW) & (df['ccode2'] == CHN_COW)) |
            ((df['ccode1'] == CHN_COW) & (df['ccode2'] == RUS_COW))
        )
        res = df[mask][['year', 'agree']].groupby('year').mean().reset_index()
        res.columns = ['Year', 'Diplomatic_Agreement_Score']
        return res
    return pd.DataFrame()

def load_energy():
    print("Chargement Énergie...")
    energy_path = RAW_DIR / "energy" / "Statistical Review of World Energy Narrow File.csv"
    if energy_path.exists():
        df = pd.read_csv(energy_path)
        # On utilise la consommation de pétrole (oilcons_ej)
        target_countries = ['Russian Federation', 'USSR', 'China']
        df_filtered = df[df['Country'].isin(target_countries) & (df['Var'] == 'oilcons_ej')].copy()
        df_filtered.loc[:, 'Country'] = df_filtered['Country'].replace({'USSR': 'RUS', 'Russian Federation': 'RUS', 'China': 'CHN'})
        df_pivot = df_filtered.pivot_table(index='Year', columns='Country', values='Value', aggfunc='sum')
        return df_pivot.reset_index().rename(columns={'CHN': 'Oil_Cons_CHN_EJ', 'RUS': 'Oil_Cons_RUS_EJ'})
    return pd.DataFrame()

def main():
    df_trade = load_trade()
    df_macro = load_macro()
    df_dip = load_diplomatic()
    df_energy = load_energy()

    master = df_trade
    for df in [df_macro, df_dip, df_energy]:
        if not df.empty:
            if master.empty: master = df
            else: master = pd.merge(master, df, on='Year', how='outer')

    master = master.sort_values('Year')
    
    if 'Trade_RUS_Exp_to_CHN' in master.columns and 'RUS_GDP_current_USD' in master.columns:
        # Trade data est deja en USD (Comtrade) ou converti en USD (BACI)
        master['RUS_Export_Dependency_to_CHN_pct'] = master['Trade_RUS_Exp_to_CHN'] / master['RUS_GDP_current_USD'] * 100
        master['CHN_Export_Dependency_to_RUS_pct'] = master['Trade_CHN_Exp_to_RUS'] / master['CHN_GDP_current_USD'] * 100

    output_file = OUTPUT_DIR / "master_dataset.csv"
    master.to_csv(output_file, index=False)
    print(f"\n[OK] MASTER DATASET CREE : {output_file}")
    print(f"Période couverte : {master.Year.min()} - {master.Year.max()}")
    print(f"Colonnes : {list(master.columns)}")

if __name__ == "__main__":
    main()
