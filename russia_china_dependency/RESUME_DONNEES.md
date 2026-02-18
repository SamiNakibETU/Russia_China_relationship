# RÉSUMÉ DONNÉES - Projet Dépendance Russie-Chine

**Date : 6 Janvier 2026**

---

## MASTER DATASET FINAL

**Fichier :** `02_processed_data/master_dataset.csv`

| Attribut | Valeur |
|----------|--------|
| Période | 1960-2024 |
| Observations | 65 (annuelles) |
| Variables | 35 |

### Variables Disponibles

| Catégorie | Variables |
|-----------|-----------|
| **Commerce** | Trade_RUS_Exp_to_CHN, Trade_CHN_Exp_to_RUS |
| **WITS** | WITS_RUS_Exports_to_CHN, WITS_RUS_Imports_from_CHN (2007-2021) |
| **Concentration** | HHI_RUS_Exports_to_CHN, ECR_Top1/Top3/Top5 |
| **Balance** | Trade_Balance_RUS_CHN, Trade_Balance_Ratio |
| **PIB** | CHN_GDP_current_USD, RUS_GDP_current_USD |
| **Croissance** | CHN_GDP_growth_annual_percent, RUS_GDP_growth_annual_percent |
| **Inflation** | CHN_Inflation_consumer_prices_percent, RUS_Inflation_consumer_prices_percent |
| **Énergie** | Oil_Cons_CHN_EJ, Gas_Cons_CHN_EJ, Oil_Cons_RUS_EJ, Gas_Cons_RUS_EJ |
| **Diplomatie** | Diplomatic_Agreement_Score |
| **Prix** | Crude oil Brent, Natural gas Europe, Coal Australian, Aluminum, Copper, Nickel, Gold |
| **ToT** | MUV_Index, ToT_Russia_Approx |
| **Dépendance** | RUS_Export_Dependency_to_CHN_pct, CHN_Export_Dependency_to_RUS_pct |

---

## SOURCES DE DONNÉES

| Source | Fichier | Période | Lignes |
|--------|---------|---------|--------|
| BACI (CEPII) | baci_russia_china_processed_2017_2023.csv | 2017-2023 | 43,494 |
| UN Comtrade | comtrade_detailed_2013_2024.csv | 2013-2024 | 477,068 |
| **WITS** | wits_russia_china_hs6_2007_2021.csv | 2007-2021 | 100,000 |
| OEC | exports_bilateral_hs4_2018_2023.csv | 2018-2023 | 4,560 |
| World Bank | worldbank_russia_china_raw.csv | 1960-2024 | - |
| FRED | brent_oil_daily.csv, copper_monthly.csv, etc. | 1990-2025 | - |
| CMO | CMO-Historical-Data-Annual.xlsx | 1960-2024 | - |
| CEPII | dist_cepii.xls, geo_cepii.xls | Statique | 50,176 |
| Energy Institute | Statistical Review of World Energy.csv | 1965-2024 | - |
| UN Voting | AgreementScoresAll_Jun2024.csv | 1946-2023 | - |

---

## INDICATEURS CLÉS (2021)

| Indicateur | Valeur | Interprétation |
|------------|--------|----------------|
| **HHI Exports RUS→CHN** | 0.404 | 🔴 TRÈS CONCENTRÉ (>0.25) |
| **ECR Top 1** | 59.2% | Pétrole/gaz domine |
| **ECR Top 3** | 86.6% | 3 secteurs = quasi-totalité |
| **Exports RUS→CHN** | 308.9 Mrd USD | Record historique |
| **Balance commerciale** | +182.6 Mrd USD | Fort excédent russe |
| **Score diplomatique ONU** | 0.797 | Alignement élevé |
| **ToT Russia** | 92.7 | Index 2010=100 |

---

## FICHIERS GÉNÉRÉS

### Données Traitées (02_processed_data/)

| Fichier | Contenu |
|---------|---------|
| master_dataset.csv | Dataset consolidé (35 vars, 65 obs) |
| wits_concentration_indicators.csv | HHI, ECR, Balance (2007-2021) |
| wits_exports_by_hs2.csv | Exports par catégorie HS2 |
| muv_tot_indices.csv | MUV Index, ToT proxy |
| cmo_commodity_prices.csv | Prix commodités (pétrole, gaz, métaux) |
| cepii_geodist_full.csv | Distances bilatérales (50,176 paires) |
| cepii_geodist_rus_chn.csv | Paire Russie-Chine (distance=5795km) |

### Scripts (03_scripts/)

| Script | Fonction |
|--------|----------|
| 01_process_local_baci.py | Extraction BACI |
| 02_download_macro_events.py | World Bank + GDELT |
| 03_download_comtrade_api.py | API UN Comtrade |
| 04_merge_all_sources.py | Fusion master_dataset |
| 05_process_new_trade_data.py | OEC + Comtrade |
| 06_process_usd_rub.py | Taux de change |
| 07_process_cepii_cmo.py | CEPII + CMO |
| **08_process_wits_hhi.py** | **HHI, ECR, Balance** |

---

## CORRECTIONS MÉTHODOLOGIQUES

| Critique Initiale | Correction Appliquée |
|-------------------|---------------------|
| HHI sur 4 catégories seulement | ✅ Calcul sur 97 catégories HS2 (WITS) |
| ToT proxy faible (cuivre/alu) | ✅ MUV Index (World Bank CMO) |
| Gravity sans distances | ✅ CEPII GeoDist intégré |
| VI poids arbitraires | 📝 ACP à implémenter dans notebook |
| Probabilités scénarios | ✅ Supprimées, scénarios qualitatifs |

---

## PRÊT POUR L'ANALYSE

Tous les indicateurs sont calculés et disponibles dans `master_dataset.csv`.

**Prochaine étape :** Ouvrir le notebook et lancer l'analyse des 4 axes.

```bash
# Vérifier les données
python russia_china_dependency/03_scripts/analysis/show_master_stats.py

# Lancer Jupyter
jupyter notebook
```



