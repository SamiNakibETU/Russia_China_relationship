# Russia-China Economic Dependency Analysis

Quantitative analysis of the Russia-China trade relationship through the lens of Western sanctions. Combines econometrics, causal inference, and network analysis to answer:

> **Have Western sanctions caused an irreversible structural dependency of Russia on China, and does this asymmetry constitute a strategic lever for Beijing?**

## Notebooks

| # | Notebook | Methods | Key Finding |
|---|----------|---------|-------------|
| 01 | [Structural Analysis](notebooks/01_structural_analysis.ipynb) | HHI, ECR, Grubel-Lloyd, Gravity (PPML) | HHI = 0.40 (extreme concentration), HS27 = 59% of exports |
| 02 | [Time Series Econometrics](notebooks/02_time_series_econometrics.ipynb) | VAR, Granger Causality, IRF, FEVD | Brent Granger-causes trade (p<0.001), explains 17% of trade variance |
| 03 | [Causal Inference](notebooks/03_causal_inference.ipynb) | DiD, CausalImpact (BSTS), Event Study | Post-2022 sanctions increased RUS-CHN trade by +54% vs counterfactual |
| 04 | [Network Analysis](notebooks/04_network_analysis.ipynb) | Centrality, Louvain communities, HITS | Russia migrated from European to Asian trade bloc (2017 vs 2023) |

## Selected Results

### Trade reorientation
- China's share in Russian trade: **5% (1995) → 39% (2023)**
- Europe's share: **59% (1995) → 16% (2023)**
- Russia's community membership (Louvain): **European bloc (2017) → Asian bloc (2023)**

### Causal evidence
- DiD: sanctions created significant excess trade growth vs control pairs (RUS-IND, RUS-TUR)
- Event Study: +81% trade increase in months [+3, +6] after Feb 2022 (p<0.001)
- Russian trade surplus tripled post-sanctions (0.68 → 2.02 Mrd USD/month)

### Econometric dynamics
- Oil prices Granger-cause bilateral trade, but not the reverse
- FEVD: Brent explains 17% of trade variance at 12-month horizon
- Structural break confirmed for Brent, USD/RUB, and trade equations (Chow test, p<0.05)

## Data Sources

| Source | Period | Description |
|--------|--------|-------------|
| [UN Comtrade](https://comtradeplus.un.org/) | 2017-2024 | Monthly bilateral trade (CHN/RUS reporter) |
| [Harvard Atlas HS92](https://dataverse.harvard.edu/dataverse/atlas) | 1988-2024 | Bilateral trade, 200+ countries |
| [FRED](https://fred.stlouisfed.org/) | 1992-2025 | Brent, USD/RUB, USD/CNY |
| [BACI (CEPII)](http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37) | 2017-2023 | Reconciled bilateral trade HS6 |
| [WITS](https://wits.worldbank.org/) | 2007-2021 | Product-level HS6 exports |
| [SIPRI](https://www.sipri.org/databases/armstransfers) | 1990-2024 | Arms transfers |
| [GDELT](https://www.gdeltproject.org/) | 2013-2025 | Geopolitical events |

Raw data is not included in the repo (multi-GB). Processed datasets are in `russia_china_dependency/02_processed_data/`.

## Project Structure

```
├── notebooks/
│   ├── 01_structural_analysis.ipynb
│   ├── 02_time_series_econometrics.ipynb
│   ├── 03_causal_inference.ipynb
│   └── 04_network_analysis.ipynb
├── reports/figures/              # Generated figures
├── russia_china_dependency/
│   ├── 01_raw_data/              # Raw data (gitignored, see above)
│   │   ├── trade/
│   │   ├── prices/
│   │   ├── macro/
│   │   ├── complexity/
│   │   ├── gdelt_full/
│   │   ├── diplomatic/
│   │   ├── energy/
│   │   └── arms/
│   └── 02_processed_data/        # Cleaned datasets (included)
├── config.py
└── README.md
```

## Setup

```bash
pip install pandas numpy matplotlib seaborn statsmodels scipy scikit-learn networkx python-louvain causalimpact
```

Notebooks auto-detect paths whether run from `notebooks/` or project root.

## Methodological Notes

- N=96 monthly observations (2017-2024) is a small sample for VAR. Results are exploratory.
- Post-2022 Russian trade data has reduced reliability (publication restrictions).
- DiD SUTVA assumption is partially violated (sanctions affect control countries indirectly).
- Atlas/BACI data is reconciled, so mirror statistics require raw Comtrade declarations.
- Louvain community detection is sensitive to edge weighting choices.

## License

Academic use. Data sources retain their original licenses.
