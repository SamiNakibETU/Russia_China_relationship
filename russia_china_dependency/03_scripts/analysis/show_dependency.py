import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

df = pd.read_csv('russia_china_dependency/02_processed_data/master_dataset.csv')

# Affichage des donnees commerciales
trade_cols = ['Year', 'Trade_RUS_Exp_to_CHN', 'Trade_CHN_Exp_to_RUS', 
              'RUS_Export_Dependency_to_CHN_pct', 'CHN_Export_Dependency_to_RUS_pct']

print("=== DONNEES COMMERCIALES (2013-2024) ===\n")
result = df[trade_cols].dropna()
result['Trade_RUS_Exp_to_CHN'] = result['Trade_RUS_Exp_to_CHN'] / 1e9  # En milliards
result['Trade_CHN_Exp_to_RUS'] = result['Trade_CHN_Exp_to_RUS'] / 1e9
result.columns = ['Annee', 'Export RUS->CHN (Mrd$)', 'Export CHN->RUS (Mrd$)', 
                  'Dependance RUS (%PIB)', 'Dependance CHN (%PIB)']
print(result.to_string(index=False))

print("\n=== EVOLUTION DE LA DEPENDANCE ===")
print(f"Dependance RUS vers CHN: {result['Dependance RUS (%PIB)'].iloc[0]:.2f}% (2013) -> {result['Dependance RUS (%PIB)'].iloc[-1]:.2f}% (2021)")
print(f"Dependance CHN vers RUS: {result['Dependance CHN (%PIB)'].iloc[0]:.2f}% (2013) -> {result['Dependance CHN (%PIB)'].iloc[-1]:.2f}% (2021)")



