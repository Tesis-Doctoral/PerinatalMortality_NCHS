# Perinatal mortality with NCHS data

> **Framework.** This repository applies the thesis's staged framework for clinical prediction models. The framework (stages, gates, criteria and literature) and the catalogue of models with their status are in [StagedFramework_ClinicalPrediction](https://github.com/Tesis-Doctoral/StagedFramework_ClinicalPrediction).

Can pregnancies at high risk of ending in a perinatal death (fetal death at 22 weeks or more, or neonatal death in the first 7 days) be identified? This model uses the public-use files of the National Center for Health Statistics (NCHS, CDC) and follows the staged framework for clinical prediction models.

> **Status (2026-11-21): outcome card written and decisions D1 and D2 resolved.** Fetal component data: public-use fetal death files 2016–2023. Prediction point: antenatal (option A). Next: adapter for the fetal component. The adapter for the early neonatal component is ready.

[Versión en español](README_es.md)

## Scope

- **Outcome:** perinatal death, with its fetal and early neonatal components.
- **Framework:** [`framework.md`](framework.md) (Spanish: [`framework_es.md`](framework_es.md)), version 1.0. Outcome card: [`docs/outcome_card_perinatal_nchs.md`](docs/outcome_card_perinatal_nchs.md).

## Data

The NCHS files are kept **outside the repository**, in the sibling folder `../NCHS_data/raw/` (another location is set with the environment variable `NCHS_RAW_DIR`). They are public but are not redistributed: only the code is published. Their use is subject to the NCHS data use agreement: statistical analysis only, no attempt to identify persons and no linkage with identifiable data. Reports show no cell with fewer than 10 cases.

## Run order

| Order | Notebook | Creates | Framework stage |
|---|---|---|---|
| 1 | `notebooks/01_build_cohorts.ipynb` | `data/interim/cohort_<year>.parquet` (live births and early neonatal death) | S2 (data adapter) |

*Confidential: internal use of the research project.*
