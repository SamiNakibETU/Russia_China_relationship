import wbdata
import pandas as pd
from gdelt import gdelt
import datetime
from pathlib import Path
import os

# === CONFIGURATION ===
PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR_MACRO = PROJECT_ROOT / "01_raw_data/macro"
OUTPUT_DIR_EVENTS = PROJECT_ROOT / "01_raw_data/events"

os.makedirs(OUTPUT_DIR_MACRO, exist_ok=True)
os.makedirs(OUTPUT_DIR_EVENTS, exist_ok=True)

def download_worldbank_data():
    print("=== TÉLÉCHARGEMENT WORLD BANK ===")
    countries = ['RUS', 'CHN']
    indicators = {
        'NY.GDP.MKTP.CD': 'GDP_current_USD',
        'NY.GDP.MKTP.KD.ZG': 'GDP_growth_annual_percent',
        'FP.CPI.TOTL.ZG': 'Inflation_consumer_prices_percent',
        'NE.EXP.GNFS.ZS': 'Exports_percent_GDP',
        'NE.IMP.GNFS.ZS': 'Imports_percent_GDP',
        'BX.KLT.DINV.CD.WD': 'FDI_net_inflows_USD',
        'PA.NUS.FCRF': 'Exchange_rate_LCU_per_USD'
    }
    try:
        # On essaie sans paramètre de date pour voir si wbdata récupère tout par défaut
        print("Interrogation de l'API WorldBank (toutes dates disponibles)...")
        df = wbdata.get_dataframe(indicators, country=countries)
        
        df = df.reset_index()
        output_file = OUTPUT_DIR_MACRO / "worldbank_russia_china_raw.csv"
        df.to_csv(output_file, index=False)
        print(f"SUCCÈS : Sauvegardé dans {output_file}")
    except Exception as e:
        print(f"ERREUR WorldBank: {e}")

def download_gdelt_data():
    print("\n=== TÉLÉCHARGEMENT GDELT (PRUDENT) ===")
    gd = gdelt(version=2)
    try:
        # On réduit à une période très courte pour éviter le crash (ex: les 3 derniers jours)
        # GDELT télécharge TOUT le fichier mondial avant de filtrer.
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=3)
        
        date_range = [start_date.strftime('%Y %b %d'), end_date.strftime('%Y %b %d')]
        print(f"Recherche GDELT du {date_range[0]} au {date_range[1]}...")
        
        results = gd.Search(date_range, table='events', coverage=True)
        
        if results is not None and not results.empty:
            print("Filtrage des événements Russie-Chine...")
            mask = (
                ((results['Actor1CountryCode'] == 'RUS') & (results['Actor2CountryCode'] == 'CHN')) |
                ((results['Actor1CountryCode'] == 'CHN') & (results['Actor2CountryCode'] == 'RUS'))
            )
            filtered = results[mask].copy()
            output_file = OUTPUT_DIR_EVENTS / "gdelt_russia_china_latest.csv"
            filtered.to_csv(output_file, index=False)
            print(f"SUCCÈS : {len(filtered)} événements sauvegardés dans {output_file}")
        else:
            print("Aucun résultat GDELT sur cette courte période.")
    except Exception as e:
        print(f"ERREUR GDELT: {e}")
        print("Note: GDELT peut saturer la RAM. Si cela échoue, nous passerons par un téléchargement manuel.")

if __name__ == "__main__":
    download_worldbank_data()
    download_gdelt_data()


