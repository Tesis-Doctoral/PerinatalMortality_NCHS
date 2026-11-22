# Perinatal mortality with NCHS data

> **Framework.** This repository applies the thesis's staged framework for clinical prediction models. The framework (stages, gates, criteria and literature) and the catalogue of models with their status are in [StagedFramework_ClinicalPrediction](https://github.com/Tesis-Doctoral/StagedFramework_ClinicalPrediction).

Can pregnancies at high risk of ending in a perinatal death (fetal death at 22 weeks or more, or neonatal death in the first 7 days) be identified? This model uses the public-use files of the National Center for Health Statistics (NCHS, CDC) and follows the staged framework for clinical prediction models.

> **Status (2026-11-21): outcome card written and decisions D1 and D2 resolved.** Fetal component data: public-use fetal death files 2016–2023. Prediction point: antenatal (option A). Data adapter done: 8 years (2016–2023), 22,337 to 27,006 perinatal events per year ([`data/outputs_01_build_perinatal.txt`](data/outputs_01_build_perinatal.txt)). Count audit done ([`count_audit.md`](count_audit.md)): G1 passes. Decisions D3 to D5 approved. Predictor table (24 parameters) and gates G2 and G3 passed ([`predictor_table.md`](predictor_table.md)). Next: modeling (S8).

[Versión en español](README_es.md)

## Scope

- **Outcome:** perinatal death, with its fetal and early neonatal components.
- **Framework:** [`framework.md`](framework.md) (Spanish: [`framework_es.md`](framework_es.md)), version 1.0. Outcome card: [`docs/outcome_card_perinatal_nchs.md`](docs/outcome_card_perinatal_nchs.md).

## Data

How the files are produced, from the hospital to the download: [`docs/data_source_nchs.md`](docs/data_source_nchs.md).

The NCHS files are kept **outside the repository**, in the sibling folder `../NCHS_data/raw/` (another location is set with the environment variable `NCHS_RAW_DIR`). They are public but are not redistributed: only the code is published. Their use is subject to the NCHS data use agreement: statistical analysis only, no attempt to identify persons and no linkage with identifiable data. Reports show no cell with fewer than 10 cases.

## Run order

| Order | Notebook | Creates | Framework stage |
|---|---|---|---|
| 1 | `notebooks/01_build_cohorts.ipynb` | `data/interim/perinatal_<year>.parquet` (one row per product of 22 weeks or more: live births with their death at 0 to 6 days and fetal deaths) and `data/outputs_01_build_perinatal.txt` | S2 (data adapter) |
| 2 | `notebooks/02_count_audit.ipynb` | `data/outputs_02_count_audit.txt`; written up in [`count_audit.md`](count_audit.md) | S4, G1 |
| 3 | `notebooks/03_predictors_g2_g3.ipynb` | `data/contract/perinatal_nchs_v1/` (contract table) and `data/outputs_03_predictors_g2_g3.txt`; written up in [`predictor_table.md`](predictor_table.md) | S7, G2, G3 |
| 4 | `notebooks/04_preliminary_learners.ipynb` | `data/outputs_04_preliminary_learners.txt` (preliminary run: hyperparameter search and choice of the primary learner) | S8 |
| 5 | `notebooks/05_main_evaluation.ipynb` | `data/outputs_05_main_evaluation.txt` (recalibrated internal validation, temporal validation, sensitivities and classification) | S8, S9, G4 |
| 6 | `notebooks/06_return_r4.ipynb` | `data/contract/perinatal_nchs_r4/` and `data/outputs_06_return_r4.txt` (return R4: 28 weeks or more, complete records, finer predictors; G2, G3, preliminary run, evaluation and classification) | R4, S7–S9, G2–G4 |
| 7 | `notebooks/07_model_v2.ipynb` | `data/contract/perinatal_nchs_v2/` and `data/outputs_07_model_v2.txt` (version 2: version 1 population and predictors + gestational diabetes, gestational hypertension, eclampsia and smoking during pregnancy, by decision of the modeling team) | S7–S9, G2–G4 |

Readers: `libraries/nchs_reader.py` (linked births and infant deaths) and `libraries/perinatal_builder.py` (fetal deaths and the join of both components). They read the ZIP files directly, without extracting them.

*Confidential: internal use of the research project.*
