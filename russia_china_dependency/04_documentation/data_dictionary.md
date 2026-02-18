# Dictionnaire de Données - Projet Dépendance Russie-Chine

Ce document décrit les variables contenues dans le fichier final `02_processed_data/master_dataset.csv`.

## 1. Identifiants
*   **Year** : Année de l'observation (1960 - 2024).

## 2. Commerce (Trade - Source BACI/Comtrade)
*   **Trade_RUS_Exp_to_CHN** : Valeur totale des exportations de la Russie vers la Chine (en milliers de USD).
*   **Trade_CHN_Exp_to_RUS** : Valeur totale des exportations de la Chine vers la Russie (en milliers de USD).
*   **RUS_Export_Dependency_to_CHN_pct** : Part des exportations vers la Chine dans le PIB Russe (en %).

## 3. Macroéconomie (Source Banque Mondiale)
*   **CHN_GDP_current_USD** : PIB de la Chine en dollars courants.
*   **RUS_GDP_current_USD** : PIB de la Russie en dollars courants.
*   **CHN_GDP_growth_annual_percent** : Taux de croissance annuel du PIB (Chine).
*   **RUS_GDP_growth_annual_percent** : Taux de croissance annuel du PIB (Russie).
*   **CHN_Inflation_consumer_prices_percent** : Taux d'inflation (Chine).
*   **RUS_Inflation_consumer_prices_percent** : Taux d'inflation (Russie).

## 4. Diplomatie (Source UN Voting Data)
*   **Diplomatic_Agreement_Score** : Score d'accord dans les votes à l'Assemblée Générale de l'ONU entre la Russie et la Chine (0 à 1).

## 5. Énergie (Source Statistical Review of World Energy)
*   **Oil_Cons_CHN_EJ** : Consommation de pétrole en Chine (Exajoules).
*   **Oil_Cons_RUS_EJ** : Consommation de pétrole en Russie/URSS (Exajoules).
