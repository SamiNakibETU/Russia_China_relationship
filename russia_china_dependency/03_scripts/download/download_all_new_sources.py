"""
=============================================================================
TÉLÉCHARGEMENT AUTOMATISÉ DES SOURCES DE DONNÉES ADDITIONNELLES
Projet : Dépendance Économique Russie-Chine
=============================================================================

Sources téléchargées par ce script :
1. Harvard Atlas of Economic Complexity (Dataverse API)
   - Growth Projections & Complexity Rankings (ECI, PCI)
   - International Trade Data HS92
   - Classifications Data
2. IMF Direction of Trade Statistics (DOTS) via REST API
3. GDELT Event Database (fichiers journaliers sélectifs)
4. UNCTAD (bulk download)

Sources nécessitant une action manuelle :
- Global Sanctions Database : inscription email sur https://www.globalsanctionsdatabase.com/
- ACLED : inscription sur https://acleddata.com/
- SIPRI : export via https://armstransfers.sipri.org
"""

import os
import sys
import time
import zipfile
import io
import json
from pathlib import Path
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    print("Installation de requests...")
    os.system(f"{sys.executable} -m pip install requests")
    import requests

try:
    import pandas as pd
except ImportError:
    print("Installation de pandas...")
    os.system(f"{sys.executable} -m pip install pandas")
    import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DATA = PROJECT_ROOT / "01_raw_data"

# Répertoires cibles
DIRS = {
    "complexity": RAW_DATA / "complexity",
    "imf_dots": RAW_DATA / "imf_dots",
    "gdelt_full": RAW_DATA / "gdelt_full",
    "unctad": RAW_DATA / "unctad",
    "sanctions": RAW_DATA / "sanctions",
    "arms": RAW_DATA / "arms",
}

for d in DIRS.values():
    d.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Research Project - Russia-China Economic Analysis)"
}


def download_file(url, dest_path, description=""):
    """Télécharge un fichier avec barre de progression simple."""
    print(f"\n{'='*60}")
    print(f"Téléchargement : {description}")
    print(f"URL : {url}")
    print(f"Destination : {dest_path}")
    print(f"{'='*60}")

    try:
        response = requests.get(url, headers=HEADERS, stream=True, timeout=120)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    pct = (downloaded / total_size) * 100
                    print(f"\r  Progression : {pct:.1f}% ({downloaded/1e6:.1f} MB)", end="", flush=True)

        print(f"\n  [OK] Termine : {dest_path.name} ({os.path.getsize(dest_path)/1e6:.1f} MB)")
        return True

    except requests.exceptions.RequestException as e:
        print(f"\n  [ERREUR] : {e}")
        return False


# ============================================================
# 1. HARVARD ATLAS OF ECONOMIC COMPLEXITY (Dataverse API)
# ============================================================
def download_atlas_complexity():
    """
    Télécharge les données de complexité économique depuis Harvard Dataverse.
    
    Datasets :
    - Growth Projections & Complexity Rankings (ECI par pays)
    - International Trade Data HS92 (commerce bilateral + RCA)
    - Classifications Data (métadonnées HS/SITC)
    """
    print("\n" + "=" * 70)
    print("  1. HARVARD ATLAS OF ECONOMIC COMPLEXITY")
    print("=" * 70)

    datasets = {
        "complexity_rankings": {
            "doi": "doi:10.7910/DVN/XTAQMC",
            "description": "Growth Projections & Complexity Rankings (ECI)",
        },
        "trade_hs92": {
            "doi": "doi:10.7910/DVN/T4CHWJ",
            "description": "International Trade Data (HS 1992)",
        },
        "classifications": {
            "doi": "doi:10.7910/DVN/3BAL1O",
            "description": "Classifications Data (HS/SITC metadata)",
        },
        "product_space": {
            "doi": "doi:10.7910/DVN/FCDZBN",
            "description": "Product Space Networks (JSON)",
        },
    }

    for name, info in datasets.items():
        dest_zip = DIRS["complexity"] / f"atlas_{name}.zip"

        if dest_zip.exists():
            print(f"\n  [SKIP] Deja telecharge : {dest_zip.name}")
            continue

        # Harvard Dataverse API : télécharger tout le dataset en ZIP
        api_url = f"https://dataverse.harvard.edu/api/access/dataset/:persistentId?persistentId={info['doi']}"

        success = download_file(api_url, dest_zip, info["description"])

        if success:
            # Extraire le ZIP
            try:
                extract_dir = DIRS["complexity"] / name
                extract_dir.mkdir(exist_ok=True)
                with zipfile.ZipFile(dest_zip, "r") as zf:
                    zf.extractall(extract_dir)
                    print(f"  [OK] Extrait dans : {extract_dir}")
                    for f in zf.namelist():
                        print(f"    - {f}")
            except zipfile.BadZipFile:
                print(f"  [WARN] Fichier non-ZIP, probablement un fichier unique")
                # Renommer selon le type de contenu
                content_type = ""
                try:
                    with open(dest_zip, "r") as f:
                        first_line = f.readline()
                    if "," in first_line:
                        new_name = dest_zip.with_suffix(".csv")
                        dest_zip.rename(new_name)
                        print(f"  -> Renomme en : {new_name.name}")
                except:
                    pass

        time.sleep(2)  # Rate limiting


# ============================================================
# 2. IMF DIRECTION OF TRADE STATISTICS (DOTS)
# ============================================================
def download_imf_dots():
    """
    Télécharge les données IMF DOTS via l'API REST SDMX.
    
    Focus : Commerce bilatéral Russie-Chine + comparaisons clés
    (Russie-Inde, Russie-Turquie, Russie-UE pour le DiD)
    
    Fréquence mensuelle (M) et annuelle (A)
    """
    print("\n" + "=" * 70)
    print("  2. IMF DIRECTION OF TRADE STATISTICS (DOTS)")
    print("=" * 70)

    base_url = "http://dataservices.imf.org/REST/SDMX_JSON.svc"

    # Codes pays IMF : RU=Russia, CN=China, IN=India, TR=Turkey, 
    # W00=World, U2=EU
    countries = {
        "RU": "Russia",
        "CN": "China",
        "IN": "India",
        "TR": "Turkey",
        "KZ": "Kazakhstan",
        "AE": "UAE",
        "DE": "Germany",
        "US": "United States",
    }

    # Indicateurs : TXG_FOB_USD = Exports FOB, TMG_CIF_USD = Imports CIF
    indicators = ["TXG_FOB_USD", "TMG_CIF_USD"]

    all_data = []

    # Pour chaque pays reporter (focus sur Russie et Chine)
    reporters = ["RU", "CN"]

    for reporter in reporters:
        for partner_code, partner_name in countries.items():
            if reporter == partner_code:
                continue

            for indicator in indicators:
                # Mensuel (M) depuis 2000
                key = f"M.{reporter}.{partner_code}.{indicator}"
                url = f"{base_url}/CompactData/DOT/{key}?startPeriod=2000&endPeriod=2025"

                print(f"\n  Requete : {reporter} -> {partner_code} ({indicator})...", end=" ")

                try:
                    resp = requests.get(url, headers=HEADERS, timeout=60)
                    resp.raise_for_status()
                    data = resp.json()

                    # Parser la réponse SDMX
                    series = data.get("CompactData", {}).get("DataSet", {}).get("Series", {})
                    if isinstance(series, dict):
                        series = [series]

                    for s in series:
                        obs = s.get("Obs", [])
                        if isinstance(obs, dict):
                            obs = [obs]
                        for o in obs:
                            all_data.append({
                                "reporter": reporter,
                                "partner": partner_code,
                                "indicator": indicator,
                                "period": o.get("@TIME_PERIOD", ""),
                                "value": float(o.get("@OBS_VALUE", 0)),
                            })

                    n_obs = sum(len(s.get("Obs", [])) if isinstance(s.get("Obs", []), list) else 1 for s in series)
                    print(f"[OK] {n_obs} observations")

                except requests.exceptions.RequestException as e:
                    print(f"[ERR] Erreur : {e}")
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"[ERR] Erreur parsing : {e}")

                time.sleep(1.5)  # Rate limiting IMF API

    if all_data:
        df = pd.DataFrame(all_data)
        output_path = DIRS["imf_dots"] / "imf_dots_bilateral_monthly.csv"
        df.to_csv(output_path, index=False)
        print(f"\n  [OK] Sauvegarde : {output_path}")
        print(f"    {len(df)} observations, {df['period'].nunique()} périodes")
        print(f"    Paires : {df.groupby(['reporter','partner']).ngroups}")
    else:
        print("\n  [WARN] Aucune donnee IMF DOTS recuperee")


# ============================================================
# 3. GDELT EVENT DATABASE (sélectif)
# ============================================================
def download_gdelt_selective():
    """
    Télécharge les fichiers GDELT 1.0 Event Database pour des périodes clés.
    
    Stratégie : télécharger les fichiers mensuels/annuels historiques
    et les fichiers journaliers pour les périodes d'intérêt.
    
    Périodes clés :
    - 2013-2014 : Baseline + Crimée
    - 2018 : Guerre commerciale
    - 2020 : COVID
    - 2022-2023 : Invasion Ukraine + sanctions
    - 2024-2025 : Période récente
    """
    print("\n" + "=" * 70)
    print("  3. GDELT EVENT DATABASE (fichiers sélectifs)")
    print("=" * 70)

    base_url = "http://data.gdeltproject.org/events/"

    # Fichiers annuels historiques (avant avril 2013)
    yearly_files = [
        "2013.export.CSV.zip",
    ]

    # Fichiers journaliers pour périodes clés
    # On prend le 1er et le 15 de chaque mois pour les périodes d'intérêt
    key_periods = []

    # 2014 : Crimée (fév-juin)
    for month in range(1, 13):
        for day in [1, 15]:
            key_periods.append(f"2014{month:02d}{day:02d}")

    # 2018 : Guerre commerciale (mars-dec)
    for month in range(3, 13):
        for day in [1, 15]:
            key_periods.append(f"2018{month:02d}{day:02d}")

    # 2022 : Invasion Ukraine (jan-dec)
    for month in range(1, 13):
        for day in [1, 15]:
            key_periods.append(f"2022{month:02d}{day:02d}")

    # 2023 complet
    for month in range(1, 13):
        for day in [1, 15]:
            key_periods.append(f"2023{month:02d}{day:02d}")

    # 2024 complet
    for month in range(1, 13):
        for day in [1, 15]:
            key_periods.append(f"2024{month:02d}{day:02d}")

    # 2025 (jan-dec)
    for month in range(1, 13):
        for day in [1, 15]:
            key_periods.append(f"2025{month:02d}{day:02d}")

    daily_files = [f"{d}.export.CSV.zip" for d in key_periods]

    all_files = yearly_files + daily_files
    downloaded = 0
    failed = 0

    for filename in all_files:
        dest = DIRS["gdelt_full"] / filename

        if dest.exists():
            continue

        url = base_url + filename
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30, stream=True)
            if resp.status_code == 200:
                with open(dest, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                downloaded += 1
                size = os.path.getsize(dest) / 1e6
                print(f"  [OK] {filename} ({size:.1f} MB)")
            else:
                failed += 1
                # Fichier inexistant (date invalide ou manquant)
        except:
            failed += 1

        time.sleep(0.3)  # Rate limiting

    print(f"\n  Résumé GDELT : {downloaded} téléchargés, {failed} échoués/indisponibles")


# ============================================================
# 4. UNCTAD - FDI et services
# ============================================================
def download_unctad():
    """
    Télécharge les données UNCTAD via leur API/bulk download.
    Focus : IDE (Investissements Directs Étrangers) bilatéraux
    """
    print("\n" + "=" * 70)
    print("  4. UNCTAD - IDE et Services")
    print("=" * 70)

    # UNCTAD a une API SDMX similaire à l'IMF
    # Indicateurs clés pour IDE
    indicators = {
        "US.FdiFlowsIn": "FDI Inflows (millions USD)",
        "US.FdiFlowsOut": "FDI Outflows (millions USD)",
        "US.FdiStockIn": "FDI Inward Stock",
        "US.FdiStockOut": "FDI Outward Stock",
    }

    # On cible Russie (643) et Chine (156) - codes UN
    # API UNCTAD : https://unctadstat.unctad.org/api/
    base_url = "https://unctadstat.unctad.org/api"

    # Essayer d'abord le bulk download des tableaux clés
    bulk_urls = {
        "fdi_inflows": "https://unctadstat.unctad.org/datacentre/dataviewer/US.FdiFlowsIn",
        "fdi_outflows": "https://unctadstat.unctad.org/datacentre/dataviewer/US.FdiFlowsOut",
    }

    # UNCTAD offre aussi des CSV via URL directe pour certains rapports
    # On essaie le World Investment Report data
    wir_url = "https://unctad.org/system/files/non-official-document/WIR2024_tab01.xlsx"
    
    dest = DIRS["unctad"] / "unctad_wir_fdi_2024.xlsx"
    if not dest.exists():
        success = download_file(wir_url, dest, "UNCTAD World Investment Report - FDI Tables")
        if not success:
            print("  [WARN] Telechargement UNCTAD WIR echoue - donnees disponibles manuellement")
            print("  -> Aller sur : https://unctadstat.unctad.org/datacentre/")
            print("  -> Chercher : 'Foreign direct investment: Inward and outward flows and stock'")
            print("  -> Filtrer pays : Russian Federation, China")
            print("  -> Exporter en CSV")


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 70)
    print("  TÉLÉCHARGEMENT DES SOURCES DE DONNÉES ADDITIONNELLES")
    print(f"  Projet Dépendance Russie-Chine — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    # 1. Atlas of Economic Complexity
    try:
        download_atlas_complexity()
    except Exception as e:
        print(f"\n  [ERR] Erreur Atlas : {e}")

    # 2. IMF DOTS
    try:
        download_imf_dots()
    except Exception as e:
        print(f"\n  [ERR] Erreur IMF DOTS : {e}")

    # 3. GDELT (sélectif)
    try:
        download_gdelt_selective()
    except Exception as e:
        print(f"\n  [ERR] Erreur GDELT : {e}")

    # 4. UNCTAD
    try:
        download_unctad()
    except Exception as e:
        print(f"\n  [ERR] Erreur UNCTAD : {e}")

    # ============================================================
    # RÉSUMÉ ET ACTIONS MANUELLES
    # ============================================================
    print("\n" + "=" * 70)
    print("  RÉSUMÉ")
    print("=" * 70)

    for name, path in DIRS.items():
        files = list(path.iterdir())
        total_size = sum(f.stat().st_size for f in files if f.is_file()) / 1e6
        print(f"  {name:20s} : {len(files):3d} fichiers ({total_size:.1f} MB)")

    print("\n" + "=" * 70)
    print("  ACTIONS MANUELLES REQUISES")
    print("=" * 70)
    print("""
  1. GLOBAL SANCTIONS DATABASE (GSDB)
     -> https://www.globalsanctionsdatabase.com/
     -> Remplir le formulaire (email, affiliation, usage)
     -> Dataset envoye par email
     -> Sauvegarder dans : 01_raw_data/sanctions/

  2. SIPRI ARMS TRANSFERS
     -> https://armstransfers.sipri.org
     -> Menu "Data" -> "Import/export values"
     -> Selectionner : Russia supplier, China recipient (et inverse)
     -> Periode : 1990-2024
     -> Export to CSV
     -> Sauvegarder dans : 01_raw_data/arms/

  3. ACLED (optionnel)
     -> https://acleddata.com/data-export-tool/
     -> Inscription gratuite requise
     -> Filtrer : Russia, China, 2010-2025
     -> Sauvegarder dans : 01_raw_data/acled/

  4. CEPII CHELEM (optionnel)
     -> http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=17
     -> Inscription CEPII requise (gratuite pour chercheurs)
     -> Sauvegarder dans : 01_raw_data/gravity/
    """)


if __name__ == "__main__":
    main()
