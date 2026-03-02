# Russia-China Economic Dependency Analysis

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Data](https://img.shields.io/badge/data-2017--2024-informational.svg)
![Methods](https://img.shields.io/badge/methods-VAR%20|%20Event%20Study%20|%20Network-orange.svg)
![License](https://img.shields.io/badge/license-Academic-yellow.svg)

**Core finding**: HHI=0.40 (extreme concentration). RUS 67.5% exports → CHN, asymmetry 7.2x. Event Study post-2022: +53.6% trade (p<0.001). Russia migrated from European to Asian trade bloc (2017→2023).

> Have Western sanctions caused irreversible structural dependency of Russia on China?

[View Analysis (HTML)](reports/01_structural_analysis.html) · [Dashboard](reports/dashboard.html) · [Executive Summary](reports/EXECUTIVE_SUMMARY.md) · [Notebooks](notebooks/)

---

## Visual Evidence

| Figure                        | Caption                                                      |
| ----------------------------- | ------------------------------------------------------------ |
| china_share_timeline          | China: 5.3% (1995) → 39.4% (2023). Europe: 59.4% → 15.6%.    |
| hhi_timeline                  | HHI: 0.24 (2007) → 0.40 (2021). Threshold 0.25.              |
| did_treatment_effect          | Event Study [+3,+6]: +81.5%. Mean post: +53.6%. R²=0.90.     |
| network_communities_2017_2023 | RUS 2017: European bloc. RUS 2023: Asian bloc (incl. CHN).   |
| mdi_timeline                  | MDI: 2.67%–7.98% (mean 3.89%). Carnegie ~300 M$/mo dual-use. |
| crink_network_graph           | CHN→RUS 245 Bn. Total CRINK: 300 Bn.                         |

---

## Analysis

| Notebook | Method           | N            | Result               | Test                     |
| -------- | ---------------- | ------------ | -------------------- | ------------------------ |
| 01       | HHI, Gravity OLS | 15 yr        | HHI=0.404, R²=0.937  | Chow p=0.007             |
| 02       | VAR(2), Granger  | 96 mo        | Brent→Trade p=0.0000 | FEVD h=12: 17.2%         |
| 03       | Event Study      | 96 mo        | +53.6% post-2022     | [+3,+6]: +81.5%, p<0.001 |
| 04       | Louvain          | 50 countries | RUS: Euro→Asian bloc | CHN share 39.4%          |
| 05       | MDI              | 32 mo        | 2.67–7.98%           | Carnegie categories      |
| 06       | Asymmetry        | 7 dyads      | CHN→RUS 245 Bn       | IRN-RUS 4.38             |

---

## Data Sources

| Source             | Period    | Description               |
| ------------------ | --------- | ------------------------- |
| UN Comtrade        | 2017-2024 | Monthly bilateral         |
| Harvard Atlas HS92 | 1988-2024 | Bilateral, 200+ countries |
| FRED               | 1992-2025 | Brent, USD/RUB, USD/CNY   |
| BACI (CEPII)       | 2017-2023 | Reconciled HS6            |
| WITS               | 2007-2021 | HS6 exports               |
| SIPRI              | 1990-2024 | Arms                      |
| Carnegie           | 2024      | Dual-use estimates        |

Processed: `russia_china_dependency/02_processed_data/`.

---

## Methodology

- VAR(2) en dlog. Ordering: Brent → USD/RUB → USD/CNY → Exp RUS→CHN.
- Event Study: phase dummies, ref baseline <−6 mo. OLS, Brent+USD/RUB controls.
- Louvain: edge weight = trade value. Modularity by year.

---

## Limitations

- N=96 monthly obs. VAR: 80% power at d≈0.5. Below N=150 for stable IRF (Lütkepohl 2005).
- Post-2022 RUS data: mirror gap CHN-RUS up to −15% (2020).
- DiD SUTVA: sanctions spill to control (IND, TUR).
- Louvain: modularity varies with edge weights.

---

## Setup

```bash
pip install -r requirements.txt
```

Notebooks run from project root or `notebooks/`.

## License

- Code: MIT
- Reports/figures: CC BY 4.0
- Data sources: original licenses (see `russia_china_dependency/01_raw_data/` if SOURCES.md present)
