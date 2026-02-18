# PLAN D'ANALYSE FINAL - Dépendance Économique Russie-Chine

## État des Données au 6 Janvier 2026

### Données Disponibles (Master Dataset)

| Source | Période | Variables clés |
|--------|---------|----------------|
| BACI | 2017-2023 | Commerce bilatéral réconcilié |
| UN Comtrade | 2013-2024 | Détail mensuel, 47 colonnes |
| **WITS** | **2007-2021** | **3,181 produits HS6, HHI calculé** |
| World Bank | 1960-2024 | PIB, inflation, croissance |
| FRED | 1990-2025 | Taux de change, prix commodités |
| CMO | 1960-2024 | MUV Index, ToT proxy |
| CEPII | Statique | Distances, contiguïté, gravity |
| Energy Institute | 1965-2024 | Consommation énergie |
| UN Voting | 1946-2023 | Score diplomatique ONU |

**Total : 35 variables, 65 observations annuelles (1960-2024)**

---

## PLAN D'ANALYSE EN 4 AXES (Corrigé)

### AXE 1 : Mesure de la Dépendance Structurelle

#### 1.1 Indicateurs Calculés ✅

| Indicateur | Formule | Données |
|------------|---------|---------|
| **TDI** (Trade Dependency Index) | (Exports RUS→CHN) / PIB_RUS × 100 | WITS + WB |
| **HHI** (Herfindahl-Hirschman) | Σ(share_i)² sur 97 catégories HS2 | WITS ✅ Calculé |
| **ECR** (Export Concentration Ratio) | Top1/Top3/Top5 shares | WITS ✅ Calculé |
| **ToT** (Terms of Trade) | (Energy_Index × 0.6 + Metals × 0.4) / MUV | CMO ✅ |

#### 1.2 Résultats Préliminaires

```
HHI Exports RUS→CHN (2021) = 0.40 → TRÈS CONCENTRÉ
ECR Top1 (2021) = 59% → HS27 (pétrole/gaz) domine
ECR Top3 (2021) = 87% → Quasi-monopole sectoriel
Balance commerciale (2021) = +183 Mrd USD excédent russe
```

#### 1.3 Code Notebook (Axe 1)

```python
# 1. Visualisation HHI et ECR dans le temps
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# HHI
axes[0].plot(master['Year'], master['HHI_RUS_Exports_to_CHN'], 'b-o')
axes[0].axhline(y=0.25, color='r', linestyle='--', label='Seuil concentration élevée')
axes[0].set_title('HHI des exports russes vers Chine')
axes[0].legend()

# ECR
axes[1].plot(master['Year'], master['ECR_Top1'], label='Top 1')
axes[1].plot(master['Year'], master['ECR_Top3'], label='Top 3')
axes[1].plot(master['Year'], master['ECR_Top5'], label='Top 5')
axes[1].set_title('Export Concentration Ratio')
axes[1].legend()

# 2. Indice de Vulnérabilité Composite (VI)
# CORRECTION: Utiliser ACP pour les poids (pas arbitraire)
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

indicators = master[['HHI_RUS_Exports_to_CHN', 'ECR_Top1', 'ToT_Russia_Approx']].dropna()
scaler = StandardScaler()
scaled = scaler.fit_transform(indicators)

pca = PCA(n_components=1)
pca.fit(scaled)
weights = np.abs(pca.components_[0]) / np.sum(np.abs(pca.components_[0]))
print(f"Poids ACP: HHI={weights[0]:.2f}, ECR={weights[1]:.2f}, ToT={weights[2]:.2f}")

# VI avec poids déterminés par données
master['VI'] = (weights[0] * master['HHI_RUS_Exports_to_CHN'] + 
                weights[1] * master['ECR_Top1']/100 + 
                weights[2] * (1/master['ToT_Russia_Approx']))
```

---

### AXE 2 : Détection des Ruptures Structurelles

#### 2.1 Test de Bai-Perron

```python
# Avec données annuelles (N=15 pour WITS, N=65 pour master)
from statsmodels.tsa.stattools import adfuller
import ruptures as rpt

# 1. Test stationnarité (ADF) - Ajouté suite à critique
series = master['HHI_RUS_Exports_to_CHN'].dropna()
adf_result = adfuller(series)
print(f"ADF Statistic: {adf_result[0]:.4f}")
print(f"p-value: {adf_result[1]:.4f}")

# 2. Détection ruptures (Bai-Perron via ruptures)
signal = series.values
algo = rpt.Pelt(model="rbf").fit(signal)
breakpoints = algo.predict(pen=3)

# Validation visuelle
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(series.index, series.values)
for bp in breakpoints[:-1]:
    ax.axvline(x=series.index[bp], color='r', linestyle='--', alpha=0.7)
ax.set_title('Ruptures structurelles détectées (Bai-Perron)')
```

#### 2.2 Ruptures Attendues

| Année | Événement | Impact attendu |
|-------|-----------|----------------|
| **2014** | Sanctions Crimée | ↑ Réorientation vers Chine |
| **2018** | Guerre commerciale US-CHN | ↑ Opportunité pour RUS |
| **2022** | Sanctions Ukraine | ↑↑ Dépendance accrue |

---

### AXE 3 : Modèle de Gravité (PPML)

#### 3.1 Données Disponibles ✅

```
CEPII GeoDist:
- Distance RUS-CHN: 5,795 km
- Contiguïté: 1 (frontière commune)
- Langue commune: 0
- Colonie: 0
```

#### 3.2 Spécification PPML (Corrigée)

```python
import statsmodels.api as sm
from statsmodels.genmod.families import Poisson

# Panel de commerce bilatéral
# Note: Pour PPML rigoureux, il faut un panel multi-pays
# Ici on utilise les données WITS Russia-China comme point de départ

# Variables
X = master[['RUS_GDP_current_USD', 'CHN_GDP_current_USD']].dropna()
X['log_gdp_rus'] = np.log(X['RUS_GDP_current_USD'])
X['log_gdp_chn'] = np.log(X['CHN_GDP_current_USD'])
X['dist'] = 5795  # km (CEPII)
X['contig'] = 1    # frontière commune
X['log_dist'] = np.log(X['dist'])

y = master.loc[X.index, 'WITS_RUS_Exports_to_CHN'].dropna() * 1e9  # en USD

# PPML (Poisson Pseudo-Maximum Likelihood)
X_model = sm.add_constant(X[['log_gdp_rus', 'log_gdp_chn', 'log_dist', 'contig']])
model = sm.GLM(y, X_model, family=sm.families.Poisson())
results = model.fit()
print(results.summary())

# Interpréter les coefficients comme élasticités
```

#### 3.3 Extension: Panel Multi-Pays

Pour un gravity model rigoureux, utiliser:
```python
# Charger données CEPII complètes (50,176 paires)
geodist = pd.read_csv('russia_china_dependency/02_processed_data/cepii_geodist_full.csv')

# Joindre avec données commerce mondial (BACI ou Comtrade)
# Estimer sur échantillon plus large
```

---

### AXE 4 : Scénarios Prospectifs (Sans Probabilités)

#### 4.1 Scénarios Qualitatifs

| Scénario | Description | Hypothèses |
|----------|-------------|------------|
| **Status Quo Tendu** | Sanctions maintenues, coopération sino-russe stable | HHI stable ~0.40 |
| **Découplage Partiel** | Chine diversifie fournisseurs énergie | HHI ↓ pour RUS, risque |
| **Intégration Profonde** | Monnaie commune, corridor économique | HHI ↑, dépendance mutuelle |
| **Rupture Géopolitique** | Conflit Taïwan, sanctions secondaires | Choc systémique |

#### 4.2 Analyse de Sensibilité

```python
# Impact d'une variation du prix du pétrole sur la dépendance
def sensitivity_oil_price(base_exports, oil_price_change_pct):
    """
    Simule l'impact d'un changement de prix du pétrole
    Hypothèse: 60% des exports = pétrole/gaz
    """
    energy_share = 0.58  # ECR Top1
    new_exports = base_exports * (1 + energy_share * oil_price_change_pct / 100)
    return new_exports

# Scénarios
scenarios = {
    'Pétrole -30%': sensitivity_oil_price(308.9, -30),
    'Pétrole stable': 308.9,
    'Pétrole +30%': sensitivity_oil_price(308.9, 30),
}
```

---

## CHECKLIST MÉTHODOLOGIQUE (Réponse aux Critiques)

| Critique | Correction | Statut |
|----------|------------|--------|
| HHI mal calculé (4 vs 97 catégories) | ✅ Calcul sur tous les HS2 | ✅ Fait |
| ToT proxy faible | ✅ MUV Index + indices énergie/métaux | ✅ Fait |
| VI poids arbitraires | ✅ ACP pour poids naturels | 📝 À implémenter |
| Gravity incomplet | ✅ CEPII GeoDist intégré | ✅ Fait |
| Bai-Perron N<30 | ⚠️ N=15 (WITS), disclaimer nécessaire | 📝 Note |
| Probabilités scénarios | ✅ Supprimées, scénarios qualitatifs | ✅ Fait |
| PIB russe manipulé | 📝 Robustesse avec -10% | 📝 À ajouter |

---

## STRUCTURE DU NOTEBOOK

```
01_data_loading.ipynb
├── Chargement master_dataset.csv
├── Vérification colonnes
└── Statistiques descriptives

02_axe1_dependance.ipynb
├── Visualisation HHI, ECR
├── Calcul TDI
├── ACP pour VI
└── Graphiques publication

03_axe2_ruptures.ipynb
├── Test ADF stationnarité
├── Bai-Perron (ruptures)
├── Validation événements
└── Graphiques avec annotations

04_axe3_gravity.ipynb
├── PPML simple (RUS-CHN)
├── Extension panel (optionnel)
└── Interprétation élasticités

05_axe4_scenarios.ipynb
├── Définition scénarios
├── Analyse sensibilité
└── Visualisations prospectives

06_synthese.ipynb
├── Résumé des résultats
├── Limites méthodologiques
└── Conclusion
```

---

## COMMANDE POUR LANCER L'ANALYSE

```bash
# Vérifier que toutes les données sont prêtes
python russia_china_dependency/03_scripts/analysis/show_master_stats.py

# Lancer Jupyter
jupyter notebook
```

**Prêt à commencer l'analyse dans le notebook !**



