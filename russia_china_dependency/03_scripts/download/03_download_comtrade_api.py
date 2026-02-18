import requests
import pandas as pd
import os
from pathlib import Path

# === CONFIGURATION ===
PROJECT_ROOT = Path(__file__).parent.parent.parent
KEY_FILE_PATH = PROJECT_ROOT.parent / "api_com_trade.txt"
OUTPUT_DIR = PROJECT_ROOT / "01_raw_data/trade"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_api_key():
    try:
        with open(KEY_FILE_PATH, 'r') as f:
            lines = f.readlines()
            # On cherche une ligne qui ressemble à une clé (32 chars hex)
            for line in lines:
                parts = line.strip().split('|')
                for p in parts:
                    if len(p) == 32: return p
        return None
    except: return None

def download_comtrade_recent():
    api_key = get_api_key()
    if not api_key:
        print("Clé API non trouvée.")
        return

    base_url = "https://comtradeplus.un.org/api/v1/getData"
    params = {
        'subscription-key': api_key,
        'reporterCode': '643',
        'partnerCode': '156',
        'period': '2023,2024',
        'flowCode': 'M,X',
        'cmdCode': 'TOTAL',
        'frequency': 'A',
    }
    
    try:
        r = requests.get(base_url, params=params, timeout=30)
        if r.status_code == 200:
            data = r.json()
            records = data.get('data') or data.get('dataset') or (data if isinstance(data, list) else [])
            if records:
                df = pd.DataFrame(records)
                out_file = OUTPUT_DIR / "comtrade_api_recent_total.csv"
                df.to_csv(out_file, index=False)
                print(f"SUCCÈS : {len(df)} lignes dans {out_file}")
            else:
                print("Pas de données trouvées.")
        else:
            print(f"Erreur API : {r.status_code}")
    except Exception as e:
        print(f"Exception : {e}")

if __name__ == "__main__":
    download_comtrade_recent()






