import pandas as pd

master = pd.read_csv('russia_china_dependency/02_processed_data/master_dataset.csv')
print('=== MASTER DATASET FINAL ===')
print(f'Periode: {int(master.Year.min())} - {int(master.Year.max())}')
print(f'Observations: {len(master)}')
print(f'Colonnes: {len(master.columns)}')
print()

# Liste des colonnes
print('=== COLONNES DISPONIBLES ===')
for i, col in enumerate(master.columns):
    print(f'  {i+1}. {col}')
print()

# Stats 2023
if 2023 in master.Year.values:
    row = master[master.Year == 2023].iloc[0]
    print('=== CHIFFRES CLES 2023 ===')
    
    if 'Crude oil, Brent' in master.columns:
        val = row['Crude oil, Brent']
        if pd.notna(val):
            print(f'  Brent Oil: {val:.2f} USD/bbl')
    
    if 'ToT_Russia_Approx' in master.columns:
        val = row['ToT_Russia_Approx']
        if pd.notna(val):
            print(f'  ToT Russia: {val:.1f}')
    
    if 'MUV_Index' in master.columns:
        val = row['MUV_Index']
        if pd.notna(val):
            print(f'  MUV Index: {val:.1f}')
    
    if 'Diplomatic_Agreement_Score' in master.columns:
        val = row['Diplomatic_Agreement_Score']
        if pd.notna(val):
            print(f'  Diplomatic Score: {val:.3f}')



