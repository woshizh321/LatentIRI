# Latent_IRI: A PCA-Derived Immune Resilience Index

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![NHANES 2017-2020](https://img.shields.io/badge/data-NHANES%202017--2020-orange.svg)](https://www.cdc.gov/nchs/nhanes/)

> **Latent Immune Resilience Index (Latent_IRI)** — a composite biomarker derived from routine CBC and laboratory values that outperforms traditional inflammatory indices (SII, NLR, PLR) in all-cause mortality prediction and chronic disease protection.

---

## Overview

This repository contains the analysis pipeline and publication-quality figure scripts for a multi-cohort study that:

1. **Derives** Latent_IRI from NHANES 2017–2020 via locked PCA loadings
2. **Validates** it against the National Death Index (N = 5,101; Cox HR = 0.866, p < .001)
3. **Characterizes** its age/sex trajectory in a local health-check cohort (N = 99,873)
4. **Benchmarks** it head-to-head against 7 traditional immune-inflammatory indices
5. **Demonstrates** its protective association with arthritis and COPD

---

## Key Results

| Analysis | Result |
|----------|--------|
| NHANES-NDI mortality (Cox) | HR = 0.866 \[0.807–0.928\], p < .001, C-index = 0.828 |
| Sex × Age interaction (local cohort) | β = −0.0035 AU/year, p < .001 |
| vs SII (C-index difference) | +0.40 percentage points |
| Immune senescence decoupling (age > 60) | −18.5% vs SII −9.7% |
| COPD protection (OR per 1-SD) | 0.784 \[0.706–0.871\], p < .001 |
| Arthritis protection (OR per 1-SD) | 0.882 \[0.815–0.955\], p = .002 |

---

## Six Core Figures

| Figure | Description | Script |
|--------|-------------|--------|
| **Fig 1** | Cohort characteristics & study design | `src/14_Fig1_CohortCharacteristics.py` |
| **Fig 2** | Latent_IRI construction (PCA loadings & validation) | `src/15_Fig2_LatentIRI_Construction.py` |
| **Fig 3** | Local cohort 3-dimensional analysis (trajectory / inflammation / survival) | `src/16_Fig3_LocalCohort.py` |
| **Fig 4** | Head-to-head benchmarking tournament | `src/17_Fig4_Benchmarking.py` |
| **Fig 5** | Immune senescence decoupling trajectories | `src/18_Fig5_ImmuneDecoupling.py` |
| **Fig 6** | Chronic disease protection forest plot | `src/19_Fig6_DiseaseProtection.py` |

---

## Model Specification

Two model variants are provided depending on data availability:

### Latent_IRI_Full (5 features — NHANES cohort)

```python
LOADINGS = [-0.5658, -0.2352, -0.4414, -0.5196, +0.3996]   # NEU LYM PLT CRP ALB
MEANS    = [ 4.1482,  2.1531, 252.1044,  3.4345,   4.1242]
STDS     = [ 1.6040,  2.5572,  64.2584,  7.0060,   0.3430]

Latent_IRI_Full = sum(loading_i * (x_i - mean_i) / std_i  for each feature)
```

### Latent_IRI_CBC (3 features — local health-check cohort, 100% coverage)

```python
LOADINGS = [-0.5658, -0.2352, -0.4414]   # NEU LYM PLT
MEANS    = [ 4.1482,  2.1531, 252.1044]
STDS     = [ 1.6040,  2.5572,  64.2584]
```

Units: NEU / LYM in 10⁹/L; PLT in 10⁹/L; CRP in mg/L; ALB in **g/dL**.

Locked parameters: `00_project_meta/LockedModelSpec_v2.0.json`

---

## Repository Structure

```
.
├── src/                          # Numbered canonical scripts
│   ├── 01–13_Analysis_*.py       # Data extraction, Aims 3–7 analysis
│   └── 14–19_Fig*.py             # Publication figure generators (Figures 1–6)
├── scripts/                      # Original runnable scripts (use from project root)
│   └── generate_figure1-6_grant.py
├── results/main/                 # Final publication figures (PDF + PNG)
├── aim3/data/                    # Local cohort (N = 99,873)
├── aim4/data/                    # NHANES locked dataset (N = 15,378)
├── aim5–7/                       # Intermediate results, tables, sub-figures
├── 00_project_meta/              # Locked model spec (immutable PCA parameters)
├── archive/                      # Legacy R scripts, debug/test code
└── docs/                         # Technical documentation
```

---

## Quick Start

```bash
git clone https://github.com/woshizh321/LatentIRI.git
cd LatentIRI

# Install dependencies (Python 3.10+)
conda create -n latentiri python=3.10
conda activate latentiri
pip install pandas numpy scipy matplotlib seaborn lifelines statsmodels

# Reproduce a publication figure (requires data files — see Data Availability)
cd <project_root>
python src/17_Fig4_Benchmarking.py
```

> **Note**: Raw data files (NHANES XPT, local health-check XLSX) are not included due to
> privacy constraints. Contact the corresponding author for data access.

---

## Data Sources

| Dataset | N | Source |
|---------|---|--------|
| NHANES 2017–2020 | 27,493 | [CDC NHANES](https://www.cdc.gov/nchs/nhanes/) (public) |
| National Death Index linkage | 5,101 | CDC/NCHS restricted data |
| Local health-check cohort 2021–2025 | 99,873 | Institutional (de-identified) |

---

## Dependencies

```
pandas >= 1.5
numpy >= 1.23
scipy >= 1.9
matplotlib >= 3.6
seaborn >= 0.12
lifelines >= 0.27
statsmodels >= 0.13
```

---

## Citation

> He W, et al. *Latent Immune Resilience Index: A PCA-derived composite biomarker
> outperforms traditional inflammatory indices in mortality prediction and chronic
> disease protection.* (Manuscript in preparation, 2026)

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Contact

**Wenxi He** | hezhu0418@gmail.com
