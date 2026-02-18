# Feuille de Route : Modélisation Dépendance Russie-Chine

Cette feuille de route détaille les étapes pour construire votre base de données.

## Phase 1 : Collecte Automatisée (Scripts Python) - TERMINÉE ✅

Ces données sont récupérées via les scripts dans `russia_china_dependency/03_scripts/download/`.

1.  **Données Commerciales Historiques (BACI)** ✅

    - **Source :** Vos fichiers locaux dans `BACI_HS17_V202501`.
    - **Résultat :** `01_raw_data/trade/baci_russia_china_processed_2017_2023.csv` (~43k lignes).

2.  **Données Macroéconomiques (Banque Mondiale)** ✅

    - **Source :** API Banque Mondiale via `wbdata`.
    - **Résultat :** `01_raw_data/macro/worldbank_russia_china_raw.csv`.

3.  **Événements Géopolitiques (GDELT)** ✅

    - **Source :** Projet GDELT.
    - **Résultat :** `01_raw_data/events/gdelt_russia_china_latest.csv`.

4.  **Données Commerciales Récentes (UN Comtrade)** ✅
    - **Source :** API UN Comtrade.
    - **Résultat :** `01_raw_data/trade/comtrade_api_recent_total.csv`.

---

## Phase 2 : Collecte Manuelle - TERMINÉE ✅

Vous avez récupéré les fichiers suivants qui ont été classés :

### 1. Énergie (Energy Institute) ✅

- `russia_china_dependency/01_raw_data/energy/EI-Stats-Review-ALL-data.xlsx`
- `russia_china_dependency/01_raw_data/energy/Statistical Review of World Energy Narrow File.csv`

### 2. Investissements et Transition ✅

- `russia_china_dependency/01_raw_data/finance/2025 Country Tracker CSV.csv`
- `russia_china_dependency/01_raw_data/finance/2025 Country Transition Tracker Data.xlsx`
- `russia_china_dependency/01_raw_data/finance/Panel format CSV.csv`

### 3. Diplomatie (Votes ONU / Scores d'accord) ✅

- `russia_china_dependency/01_raw_data/diplomatic/AgreementScores.csv`
- `russia_china_dependency/01_raw_data/diplomatic/AgreementScoresAll_Jun2024.csv`

---

## Phase 3 : Nettoyage et Fusion (Master Dataset) - EN COURS 🔄

Prochaines étapes :

1.  **Analyse des formats** : Vérifier les colonnes de chaque nouveau fichier pour identifier les clés de fusion (Année, Pays).
2.  **Script de Fusion** : Créer `03_scripts/cleaning/04_merge_all_sources.py`.
3.  **Génération** : Créer `02_processed_data/master_dataset.csv`.
