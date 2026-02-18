import pandas as pd
import csv
from io import StringIO

# Lecture brute pour compter les colonnes
with open('new/TradeData_1_6_2026_11_0_56.csv', 'r', encoding='latin-1') as f:
    header = f.readline().strip()
    data1 = f.readline().strip()

header_cols = header.split(',')
data_cols = list(csv.reader(StringIO(data1)))[0]

print(f"Nombre colonnes header: {len(header_cols)}")
print(f"Nombre colonnes data: {len(data_cols)}")

# Les dernieres colonnes
print("\n--- Dernieres colonnes header ---")
for i, c in enumerate(header_cols[-5:]):
    print(f"  {len(header_cols)-5+i}: {c}")

print("\n--- Dernieres colonnes data ---")
for i, c in enumerate(data_cols[-5:]):
    print(f"  {len(data_cols)-5+i}: {c}")

# Solution : lire avec names= et skip la premiere ligne
print("\n--- TEST LECTURE CORRECTE ---")
df = pd.read_csv('new/TradeData_1_6_2026_11_0_56.csv', 
                 encoding='latin-1', 
                 header=0,
                 on_bad_lines='skip',
                 nrows=5)
print("refYear:", df['refYear'].tolist())
