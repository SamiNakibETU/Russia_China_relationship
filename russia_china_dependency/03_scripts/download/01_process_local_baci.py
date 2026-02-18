import pandas as pd
import os
from pathlib import Path

# === CONFIGURATION ===
# Utilisation de chemins relatifs à la RACINE du projet pour plus de sécurité
PROJECT_ROOT = Path(__file__).parent.parent.parent
SOURCE_DIR = PROJECT_ROOT.parent / "BACI_HS17_V202501" 
OUTPUT_DIR = PROJECT_ROOT / "01_raw_data/trade"
OUTPUT_FILE = OUTPUT_DIR / "baci_russia_china_processed_2017_2023.csv"

# Codes pays BACI/Comtrade
RUSSIA_CODE = 643
CHINA_CODE = 156

def process_baci_files():
    print(f"=== DÉBUT DU TRAITEMENT BACI ===")
    print(f"Root: {PROJECT_ROOT}")
    print(f"Source: {SOURCE_DIR}")
    
    if not SOURCE_DIR.exists():
        print(f"ERREUR: Le dossier source {SOURCE_DIR} n'existe pas.")
        return
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = list(SOURCE_DIR.glob("BACI_HS17_Y*.csv"))
    if not files:
        print(f"Aucun fichier BACI trouvé dans {SOURCE_DIR}.")
        return

    print(f"Fichiers trouvés : {len(files)}")
    all_data = []

    for file_path in files:
        year = file_path.name.split('_')[2].replace('Y', '')
        print(f"Traitement de l'année {year}...")
        
        chunk_size = 1000000
        try:
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                mask = (
                    ((chunk['i'] == RUSSIA_CODE) & (chunk['j'] == CHINA_CODE)) |
                    ((chunk['i'] == CHINA_CODE) & (chunk['j'] == RUSSIA_CODE))
                )
                filtered_chunk = chunk[mask].copy()
                if not filtered_chunk.empty:
                    all_data.append(filtered_chunk)
        except Exception as e:
            print(f"  ERREUR sur {file_path.name}: {e}")

    if all_data:
        final_df = pd.concat(all_data)
        final_df.to_csv(OUTPUT_FILE, index=False)
        print(f"SUCCÈS : {len(final_df)} lignes sauvegardées dans {OUTPUT_FILE}")
    else:
        print("Aucune donnée extraite.")

if __name__ == "__main__":
    process_baci_files()






