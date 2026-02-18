import pandas as pd

print("=== ANALYSE DES NOUVELLES DONNEES ===\n")

# 1. Douanes chinoises
print("1. DOUANES CHINOISES")
try:
    df = pd.read_csv('russia_china_dependency/01_raw_data/trade/china_customs_detailed.csv', encoding='latin-1')
    print(f"   Lignes: {len(df)}")
    print(f"   Partenaires: {df['Trading partner'].nunique()}")
    russia = df[df['Trading partner'].str.contains('Russia', case=False, na=False)]
    print(f"   Lignes avec Russie: {len(russia)}")
    if len(russia) > 0:
        vals = russia['US dollar'].str.replace(',','').astype(float)
        print(f"   Valeur totale (USD): ${vals.sum():,.0f}")
except Exception as e:
    print(f"   Erreur: {e}")

# 2. Prix Brent
print("\n2. PRIX PETROLE BRENT")
brent = pd.read_csv('russia_china_dependency/01_raw_data/prices/brent_oil_daily.csv')
print(f"   Lignes: {len(brent)}")
print(f"   Periode: {brent['observation_date'].min()} - {brent['observation_date'].max()}")

# 3. Taux de change USD/CNY
print("\n3. TAUX DE CHANGE USD/CNY")
fx = pd.read_csv('russia_china_dependency/01_raw_data/macro/usd_cny_daily.csv')
print(f"   Lignes: {len(fx)}")
print(f"   Periode: {fx['observation_date'].min()} - {fx['observation_date'].max()}")

# 4. Prix Cuivre
print("\n4. PRIX CUIVRE")
copper = pd.read_csv('russia_china_dependency/01_raw_data/prices/copper_monthly.csv')
print(f"   Lignes: {len(copper)}")
print(f"   Periode: {copper['observation_date'].min()} - {copper['observation_date'].max()}")

# 5. Prix Charbon
print("\n5. PRIX CHARBON")
coal = pd.read_csv('russia_china_dependency/01_raw_data/prices/coal_monthly.csv')
print(f"   Lignes: {len(coal)}")
print(f"   Periode: {coal['observation_date'].min()} - {coal['observation_date'].max()}")

# 6. Prix Aluminium
print("\n6. PRIX ALUMINIUM")
alu = pd.read_csv('russia_china_dependency/01_raw_data/prices/aluminum_monthly.csv')
print(f"   Lignes: {len(alu)}")
print(f"   Periode: {alu['observation_date'].min()} - {alu['observation_date'].max()}")

# 7. PIB Reel Russie
print("\n7. PIB REEL RUSSIE (FRED)")
gdp_rus = pd.read_csv('russia_china_dependency/01_raw_data/macro/russia_real_gdp_annual.csv')
print(f"   Lignes: {len(gdp_rus)}")
print(f"   Periode: {gdp_rus['observation_date'].min()} - {gdp_rus['observation_date'].max()}")

# 8. Indicateur Credit Russie
print("\n8. INDICATEUR CREDIT RUSSIE")
credit = pd.read_csv('russia_china_dependency/01_raw_data/macro/russia_credit_indicator.csv')
print(f"   Lignes: {len(credit)}")
print(f"   Periode: {credit['observation_date'].min()} - {credit['observation_date'].max()}")

# 9. PIB Reel Mondial
print("\n9. PIB REEL MONDIAL")
gdp_world = pd.read_csv('russia_china_dependency/01_raw_data/macro/real_gdp_all_nations.csv')
print(f"   Lignes: {len(gdp_world)}")
print(f"   Colonnes: {gdp_world.columns.tolist()[:5]}...")

