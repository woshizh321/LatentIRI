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

## Data Sources

| Dataset | N | Source |
|---------|---|--------|
| NHANES 2017–2020 | 27,493 | [CDC NHANES](https://www.cdc.gov/nchs/nhanes/) (public) |
| National Death Index linkage | 5,101 | CDC/NCHS restricted data |
| Local health-check cohort 2021–2025 | 99,873 | Institutional (de-identified) |

---


## Contact

**Wenxi He** | hezhu0418@gmail.com
