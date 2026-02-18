# COMPTE RENDU - Inventaire Complet des Donnees

## Projet : Modelisation de la Dependance Russie-Chine

**Date de mise a jour :** 6 Janvier 2026

---

## 1. DONNEES COMMERCIALES (`01_raw_data/trade/`)

### 1.1 BACI (CEPII) - Donnees reconciliees

| Attribut     | Valeur                                                                                                                    |
| ------------ | ------------------------------------------------------------------------------------------------------------------------- |
| **Fichier**  | `baci_russia_china_processed_2017_2023.csv`                                                                               |
| **Source**   | CEPII - BACI HS17 V202501                                                                                                 |
| **Lignes**   | 43,494                                                                                                                    |
| **Periode**  | 2017-2023                                                                                                                 |
| **Format**   | CSV                                                                                                                       |
| **Colonnes** | `t` (annee), `i` (exportateur), `j` (importateur), `k` (code HS6), `v` (valeur en milliers USD), `q` (quantite en tonnes) |
| **Avantage** | Donnees reconciliees (asymetries corrigees entre declarants)                                                              |

### 1.2 UN Comtrade - Donnees detaillees

| Attribut          | Valeur                                                                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Fichier**       | `comtrade_detailed_2013_2024.csv`                                                                                                     |
| **Source**        | UN Comtrade Plus (telechargement manuel)                                                                                              |
| **Lignes**        | 477,068                                                                                                                               |
| **Periode**       | 2013-2024                                                                                                                             |
| **Format**        | CSV (47 colonnes)                                                                                                                     |
| **Colonnes cles** | `refYear`, `reporterDesc`, `partnerDesc`, `flowDesc` (Export/Import), `cmdCode` (HS4), `cmdDesc`, `primaryValue` (USD), `netWgt` (kg) |
| **Reporters**     | China, Russian Federation                                                                                                             |
| **Avantage**      | Donnees les plus recentes (jusqu'a 2024), detail mensuel disponible                                                                   |

### 1.3 Exports Bilateraux HS4

| Attribut     | Valeur                                                                                         |
| ------------ | ---------------------------------------------------------------------------------------------- |
| **Fichier**  | `exports_bilateral_hs4_2018_2023.csv`                                                          |
| **Source**   | Observatory of Economic Complexity (OEC)                                                       |
| **Lignes**   | 4,560                                                                                          |
| **Periode**  | 2018-2023                                                                                      |
| **Colonnes** | `Section ID`, `Section`, `HS4 ID`, `HS4`, `Year`, `Russia's Exports`, `China's Exports`, `PCI` |
| **Avantage** | Comparaison directe des exports par produit entre les deux pays                                |

### 1.4 Exports Russie vers Chine

| Attribut     | Valeur                                                                                        |
| ------------ | --------------------------------------------------------------------------------------------- |
| **Fichier**  | `exports_russia_to_china_2018_2023.csv`                                                       |
| **Source**   | Observatory of Economic Complexity (OEC)                                                      |
| **Lignes**   | 4,965                                                                                         |
| **Periode**  | 2018-2023                                                                                     |
| **Colonnes** | `Section ID`, `Section`, `HS4 ID`, `HS4`, `Year`, `Exports from Russia to China (USD)`, `PCI` |
| **Avantage** | Focus sur les exportations russes avec indice de complexite (PCI)                             |

### 1.5 Tarifs Douaniers Russie

| Attribut     | Valeur                                                                             |
| ------------ | ---------------------------------------------------------------------------------- |
| **Fichier**  | `tariffs_russia_from_china_2019_2023.csv`                                          |
| **Source**   | Observatory of Economic Complexity (OEC)                                           |
| **Lignes**   | 4,689                                                                              |
| **Periode**  | 2019, 2020, 2021, 2023                                                             |
| **Colonnes** | `Section ID`, `Section`, `HS4 ID`, `HS4`, `Tariff`, `Imports (USD)`, `PCI`, `Year` |
| **Avantage** | Donnees tarifaires pour analyser les barrieres commerciales                        |

### 1.6 Douanes Chinoises (Detail)

| Attribut          | Valeur                                                                                                           |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Fichier**       | `china_customs_detailed.csv`                                                                                     |
| **Source**        | General Administration of Customs of China                                                                       |
| **Lignes**        | 10,000                                                                                                           |
| **Partenaires**   | 189 pays                                                                                                         |
| **Lignes Russie** | 301 (valeur: $417M)                                                                                              |
| **Colonnes**      | `Commodity code`, `Commodity`, `Trading partner`, `Customs Regime`, `Locations`, `Quantity`, `Unit`, `US dollar` |
| **Avantage**      | Detail par province chinoise, regime douanier, quantites physiques                                               |

---

## 2. DONNEES MACROECONOMIQUES (`01_raw_data/macro/`)

### 2.1 Banque Mondiale (World Development Indicators)

| Attribut        | Valeur                                            |
| --------------- | ------------------------------------------------- |
| **Fichier**     | `worldbank_russia_china_raw.csv`                  |
| **Source**      | API World Bank via `wbdata`                       |
| **Periode**     | 1960-2024                                         |
| **Pays**        | Russia (RUS), China (CHN)                         |
| **Indicateurs** |                                                   |
|                 | - `GDP_current_USD` : PIB en dollars courants     |
|                 | - `GDP_growth_annual_percent` : Croissance du PIB |
|                 | - `Inflation_consumer_prices_percent` : Inflation |
|                 | - `Exports_percent_GDP` : Exports en % du PIB     |
|                 | - `Imports_percent_GDP` : Imports en % du PIB     |
|                 | - `FDI_net_inflows_USD` : IDE entrants            |
|                 | - `Exchange_rate_LCU_per_USD` : Taux de change    |

### 2.2 Taux de Change USD/CNY (FRED)

| Attribut    | Valeur                               |
| ----------- | ------------------------------------ |
| **Fichier** | `usd_cny_daily.csv`                  |
| **Source**  | Federal Reserve (FRED - DEXCHUS)     |
| **Lignes**  | 9,394                                |
| **Periode** | 1990-01-02 - 2026-01-02              |
| **Format**  | Quotidien                            |
| **Usage**   | Analyse des fluctuations Yuan/Dollar |

### 2.3 PIB Reel Russie (FRED)

| Attribut    | Valeur                                    |
| ----------- | ----------------------------------------- |
| **Fichier** | `russia_real_gdp_annual.csv`              |
| **Source**  | Federal Reserve (FRED - RGDPNARUA666NRUG) |
| **Lignes**  | 30                                        |
| **Periode** | 1990-2019                                 |
| **Unite**   | Millions USD 2017 (prix constants)        |
| **Usage**   | Analyse de la croissance reelle russe     |

### 2.4 Indicateur Credit Russie (FRED)

| Attribut    | Valeur                                      |
| ----------- | ------------------------------------------- |
| **Fichier** | `russia_credit_indicator.csv`               |
| **Source**  | Federal Reserve (FRED - CCUSMA02RUM618N)    |
| **Lignes**  | 402                                         |
| **Periode** | 1992-06-01 - 2025-11-01                     |
| **Format**  | Mensuel                                     |
| **Usage**   | Indicateur de credit/conditions financieres |

### 2.5 PIB Reel Mondial (Penn World Table)

| Attribut    | Valeur                                |
| ----------- | ------------------------------------- |
| **Fichier** | `real_gdp_all_nations.csv`            |
| **Source**  | Penn World Table / FRED               |
| **Lignes**  | 167 pays                              |
| **Periode** | 1990-2019                             |
| **Unite**   | Millions USD 2017 (prix constants)    |
| **Usage**   | Comparaisons internationales PIB reel |

---

## 3. PRIX DES COMMODITES (`01_raw_data/prices/`)

### 3.1 Prix Petrole Brent (FRED)

| Attribut    | Valeur                                            |
| ----------- | ------------------------------------------------- |
| **Fichier** | `brent_oil_daily.csv`                             |
| **Source**  | Federal Reserve (FRED - DCOILBRENTEU)             |
| **Lignes**  | 9,390                                             |
| **Periode** | 1990-01-02 - 2025-12-29                           |
| **Format**  | Quotidien                                         |
| **Unite**   | USD par baril                                     |
| **Usage**   | Variable cle pour les exports energetiques russes |

### 3.2 Prix Cuivre (FRED)

| Attribut    | Valeur                             |
| ----------- | ---------------------------------- |
| **Fichier** | `copper_monthly.csv`               |
| **Source**  | Federal Reserve (FRED - PCOPPUSDM) |
| **Lignes**  | 426                                |
| **Periode** | 1990-01-01 - 2025-06-01            |
| **Format**  | Mensuel                            |
| **Unite**   | USD par tonne metrique             |

### 3.3 Prix Charbon (FRED)

| Attribut    | Valeur                               |
| ----------- | ------------------------------------ |
| **Fichier** | `coal_monthly.csv`                   |
| **Source**  | Federal Reserve (FRED - PCOALAUUSDM) |
| **Lignes**  | 426                                  |
| **Periode** | 1990-01-01 - 2025-06-01              |
| **Format**  | Mensuel                              |
| **Unite**   | USD par tonne metrique               |

### 3.4 Prix Aluminium (FRED)

| Attribut    | Valeur                             |
| ----------- | ---------------------------------- |
| **Fichier** | `aluminum_monthly.csv`             |
| **Source**  | Federal Reserve (FRED - PALUMUSDM) |
| **Lignes**  | 426                                |
| **Periode** | 1990-01-01 - 2025-06-01            |
| **Format**  | Mensuel                            |
| **Unite**   | USD par tonne metrique             |

---

## 4. DONNEES ENERGETIQUES (`01_raw_data/energy/`)

### 4.1 Statistical Review of World Energy

| Attribut            | Valeur                                                                                         |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| **Fichier**         | `Statistical Review of World Energy Narrow File.csv`                                           |
| **Source**          | Energy Institute (ex-BP)                                                                       |
| **Periode**         | 1965-2024                                                                                      |
| **Format**          | Format "narrow" (une ligne par observation)                                                    |
| **Colonnes**        | `Country`, `Year`, `ISO3166_alpha3`, `Region`, `Var`, `Value`                                  |
| **Variables (Var)** | `oilcons_ej`, `gascons_ej`, `coalcons_ej`, `nuclear_ej`, `hydro_ej`, `co2_combust_mtco2`, etc. |

### 4.2 EI Stats Review (Complet)

| Attribut    | Valeur                                                                                        |
| ----------- | --------------------------------------------------------------------------------------------- |
| **Fichier** | `EI-Stats-Review-ALL-data.xlsx`                                                               |
| **Source**  | Energy Institute                                                                              |
| **Format**  | Excel multi-feuilles (100 onglets)                                                            |
| **Contenu** | Production, consommation, reserves, prix pour petrole, gaz, charbon, nucleaire, renouvelables |

---

## 5. DONNEES DIPLOMATIQUES (`01_raw_data/diplomatic/`)

### 5.1 UN Voting Agreement Scores

| Attribut       | Valeur                                                                                             |
| -------------- | -------------------------------------------------------------------------------------------------- |
| **Fichier**    | `AgreementScoresAll_Jun2024.csv`                                                                   |
| **Source**     | Harvard Dataverse (Erik Voeten)                                                                    |
| **Periode**    | 1946-2023                                                                                          |
| **Colonnes**   | `ccode1`, `ccode2` (codes COW), `agree` (score 0-1), `year`, `IdealPointAll`, `IdealPointDistance` |
| **Codes pays** | Russie = 365, Chine = 710                                                                          |
| **Usage**      | Mesure de l'alignement diplomatique via les votes a l'ONU                                          |

---

## 6. DONNEES FINANCIERES (`01_raw_data/finance/`)

### 6.1 Country Tracker

| Attribut      | Valeur                                                                 |
| ------------- | ---------------------------------------------------------------------- |
| **Fichier**   | `2025 Country Tracker CSV.csv`                                         |
| **Source**    | Energy Institute - Climate Tracker                                     |
| **Colonnes**  | `Country`, `Year`, `Variable`, `Unit`, `Value`                         |
| **Variables** | Emissions GES, Consommation fossiles, Renouvelables, Intensite carbone |

### 6.2 Transition Tracker

| Attribut    | Valeur                                         |
| ----------- | ---------------------------------------------- |
| **Fichier** | `2025 Country Transition Tracker Data.xlsx`    |
| **Format**  | Excel multi-feuilles                           |
| **Contenu** | Indicateurs de transition energetique par pays |

---

## 7. DONNEES EVENEMENTIELLES (`01_raw_data/events/`)

### 7.1 GDELT Events

| Attribut          | Valeur                                                                                                         |
| ----------------- | -------------------------------------------------------------------------------------------------------------- |
| **Fichier**       | `gdelt_russia_china_latest.csv`                                                                                |
| **Source**        | GDELT Project                                                                                                  |
| **Periode**       | Dec 2025 - Jan 2026 (3 derniers jours)                                                                         |
| **Lignes**        | 215 evenements                                                                                                 |
| **Colonnes cles** | `GLOBALEVENTID`, `SQLDATE`, `Actor1CountryCode`, `Actor2CountryCode`, `EventCode`, `GoldsteinScale`, `AvgTone` |
| **Usage**         | Analyse des evenements mediatiques bilateraux                                                                  |

---

## 8. FICHIER MASTER CONSOLIDE (`02_processed_data/`)

### master_dataset.csv

| Attribut     | Valeur                                                                             |
| ------------ | ---------------------------------------------------------------------------------- |
| **Fichier**  | `master_dataset.csv`                                                               |
| **Periode**  | 1960-2024                                                                          |
| **Colonnes** |                                                                                    |
|              | - `Year`                                                                           |
|              | - `Trade_RUS_Exp_to_CHN` (milliers USD)                                            |
|              | - `Trade_CHN_Exp_to_RUS` (milliers USD)                                            |
|              | - `CHN_GDP_current_USD`, `RUS_GDP_current_USD`                                     |
|              | - `CHN_GDP_growth_annual_percent`, `RUS_GDP_growth_annual_percent`                 |
|              | - `CHN_Inflation_consumer_prices_percent`, `RUS_Inflation_consumer_prices_percent` |
|              | - `Diplomatic_Agreement_Score` (0-1)                                               |
|              | - `Oil_Cons_CHN_EJ`, `Oil_Cons_RUS_EJ`                                             |
|              | - `RUS_Export_Dependency_to_CHN_pct` (indicateur calcule)                          |

---

## 9. DONNEES GRAVITY MODEL (`01_raw_data/gravity/`)

### 9.1 CEPII GeoDist (Distances Bilaterales)

| Attribut     | Valeur                                                                          |
| ------------ | ------------------------------------------------------------------------------- |
| **Fichier**  | `dist_cepii.xls`                                                                |
| **Source**   | CEPII - GeoDist Database                                                        |
| **Lignes**   | 50,176 paires de pays                                                           |
| **Colonnes** | `iso_o`, `iso_d`, `contig`, `comlang_off`, `colony`, `dist`, `distcap`, `distw` |
| **Usage**    | Modele de gravite (PPML) - distance, contiguite, langue commune, lien colonial  |

**Paire Russie-Chine :**

- Distance : 5,795 km (population-weighted)
- Contiguïté : 1 (frontiere commune)
- Langue commune officielle : 0

### 9.2 CEPII Geo (Donnees Geographiques)

| Attribut     | Valeur                                                             |
| ------------ | ------------------------------------------------------------------ |
| **Fichier**  | `geo_cepii.xls`                                                    |
| **Source**   | CEPII                                                              |
| **Lignes**   | 238 pays                                                           |
| **Colonnes** | `iso3`, `country`, `area`, `landlocked`, `continent`, `lat`, `lon` |

---

## 10. DONNEES CMO WORLD BANK (`01_raw_data/prices/`)

### 10.1 CMO Historical Data (Annual)

| Attribut     | Valeur                                                               |
| ------------ | -------------------------------------------------------------------- |
| **Fichier**  | `CMO-Historical-Data-Annual.xlsx`                                    |
| **Source**   | World Bank - Commodity Markets ("Pink Sheet")                        |
| **Periode**  | 1960-2024                                                            |
| **Feuilles** | Annual Prices (Nominal), Annual Prices (Real), Annual Indices        |
| **Usage**    | Prix commodites, calcul MUV (Manufactures Unit Value Index) pour ToT |

### 10.2 CMO Historical Data (Monthly)

| Attribut    | Valeur                             |
| ----------- | ---------------------------------- |
| **Fichier** | `CMO-Historical-Data-Monthly.xlsx` |
| **Source**  | World Bank - Commodity Markets     |
| **Periode** | 1960-2024 (mensuel)                |
| **Usage**   | Analyse haute frequence des prix   |

### 10.3 MUV Index (Calcule)

| Attribut     | Valeur                                                                  |
| ------------ | ----------------------------------------------------------------------- |
| **Fichier**  | `02_processed_data/muv_tot_indices.csv`                                 |
| **Colonnes** | `Year`, `MUV_Index`, `Energy_Index_Nominal`, `ToT_Russia_Approx`        |
| **Periode**  | 1960-2024                                                               |
| **Usage**    | Proxy pour les termes de l'echange (corrige la critique sur ToT faible) |

---

## 11. SCRIPTS DISPONIBLES (`03_scripts/`)

### Download

- `01_process_local_baci.py` : Extraction des donnees BACI locales
- `02_download_macro_events.py` : Telechargement World Bank + GDELT
- `03_download_comtrade_api.py` : API UN Comtrade

### Cleaning

- `04_merge_all_sources.py` : Fusion des sources en master_dataset
- `05_process_new_trade_data.py` : Traitement des nouvelles donnees commerciales
- `06_process_usd_rub.py` : Consolidation taux de change USD/RUB
- `07_process_cepii_cmo.py` : Traitement CEPII GeoDist + CMO World Bank

### Analysis

- `analyze_new_gravity_data.py` : Inspection des donnees gravity
- `show_dependency.py` : Affichage des metriques de dependance

---

## 12. MASTER DATASET FINAL

**Fichier :** `02_processed_data/master_dataset.csv`
**Periode :** 1960-2024 (65 observations annuelles)

### Colonnes disponibles :

| Categorie  | Variables                                                                                             |
| ---------- | ----------------------------------------------------------------------------------------------------- |
| Commerce   | `Trade_RUS_Exp_to_CHN`, `Trade_CHN_Exp_to_RUS`                                                        |
| PIB        | `CHN_GDP_current_USD`, `RUS_GDP_current_USD`, `Russia_Real_GDP_2017_USD`                              |
| Croissance | `CHN_GDP_growth_annual_percent`, `RUS_GDP_growth_annual_percent`                                      |
| Inflation  | `CHN_Inflation_consumer_prices_percent`, `RUS_Inflation_consumer_prices_percent`                      |
| Energie    | `Oil_Cons_CHN_EJ`, `Gas_Cons_CHN_EJ`, `Oil_Cons_RUS_EJ`, `Gas_Cons_RUS_EJ`                            |
| Diplomatie | `Diplomatic_Agreement_Score`                                                                          |
| Change     | `USD_RUB_Exchange_Rate`                                                                               |
| Prix (CMO) | `Crude oil, Brent`, `Natural gas, Europe`, `Coal, Australian`, `Aluminum`, `Copper`, `Nickel`, `Gold` |
| ToT        | `MUV_Index`, `ToT_Russia_Approx`                                                                      |
| Dependance | `RUS_Export_Dependency_to_CHN_pct`, `CHN_Export_Dependency_to_RUS_pct`                                |

---

## 13. CORRECTIONS METHODOLOGIQUES APPLIQUEES

Suite aux critiques de l'evaluateur, les corrections suivantes ont ete integrees :

| Critique                      | Correction                                         | Fichier                    |
| ----------------------------- | -------------------------------------------------- | -------------------------- |
| ToT proxy faible (cuivre/alu) | MUV Index (World Bank) + indices energie/metaux    | `muv_tot_indices.csv`      |
| Gravity sans distances        | CEPII GeoDist (dist, contig, comlang)              | `cepii_geodist_full.csv`   |
| Prix commodites incomplets    | CMO Pink Sheet (petrole, gaz, charbon, metaux, or) | `cmo_commodity_prices.csv` |

---

## 14. DONNEES MANQUANTES (ACTION UTILISATEUR)

### WITS Quarterly Trade Data

- **URL :** https://wits.worldbank.org/
- **Action requise :** Inscription gratuite + telechargement manuel
- **Selection :** Russia, China, Quarterly, 2000-2024
- **Utilite :** Augmenter le nombre d'observations pour Bai-Perron (N>30)

### Alternative : UN Comtrade Monthly via API

- L'API clé est disponible dans `api_com_trade.txt`
- Possibilité de récupérer les données mensuelles et agréger en trimestres
