# Russia-China Dependency: Executive Summary

**Question**: Have Western sanctions caused irreversible structural dependency of Russia on China?

**Answer**: Yes. HHI 0.40, asymmetry 7.2x. Event Study +53.6% post-2022 (p<0.001). Russia in Asian bloc 2023.

**Period**: 2017-01–2024-12. N=96 monthly obs.

---

## Metrics

| Indicator | Value | Source |
|-----------|-------|--------|
| HHI (2021) | 0.404 | Nb01 |
| HS27 share | 58.1% | Nb01 |
| Asymmetry ratio | 7.2x | Nb01 |
| Granger Brent→Trade | p=0.0000 | Nb02 |
| FEVD Brent h=12 | 17.2% | Nb02 |
| Event Study mean | +53.6% | Nb03 |
| Event Study [+3,+6] | +81.5% | Nb03 |
| Trade surplus pre/post | 0.68 → 2.02 Mrd/mo | Nb03 |
| CHN share 2023 | 39.4% | Nb04 |
| Europe share 2023 | 15.6% | Nb04 |
| MDI range | 2.67–7.98% | Nb05 |
| CRINK total | 300 Bn USD | Nb06 |

---

## Methods

| Notebook | Method | N | Result | Test |
|----------|--------|---|--------|------|
| 01 | PPML Gravity | 15 | β_GDP_CHN=0.895 | R²=0.937 |
| 02 | VAR(2) | 96 | Granger p=0.0000 | FEVD 17.2% |
| 03 | Event Study | 96 | +53.6% | 95% CI, p<0.001 |
| 04 | Louvain | 50 nodes | RUS Euro→Asian | Q by year |
| 05 | MDI | 32 mo | 3.89% mean | Carnegie |
| 06 | Asymmetry | 7 dyads | CHN-RUS 0.10 | IRN-RUS 4.38 |

---

## Implications

- **Economic**: Surplus russe x3 (0.68 → 2.02 Mrd/mo). CHN 39.4% du commerce russe.
- **Strategic**: Asymétrie 7.2x. RUS dans bloc asiatique 2023.
- **Method**: 3 approches (DiD, Event Study, Network) donnent le meme sens.

---

## Data

| Source | Coverage | Used in |
|--------|----------|---------|
| Panel VAR | 96 mo | Nb02, Nb03 |
| Atlas HS92 | 1988-2024 | Nb03, Nb04 |
| WITS | 2007-2021 | Nb01 |
| Carnegie | 2022-03–2024-10 | Nb05 |
| CRINK | 2024 | Nb06 |

---

## Limitations

- N=96: VAR power limitée.
- Données RUS post-2022: fiabilité réduite.
- DiD SUTVA: spill-over vers contrôles.
- Louvain: stabilité des communautés.
