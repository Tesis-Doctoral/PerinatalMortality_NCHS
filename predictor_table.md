# Predictor table and gates G2 and G3 — perinatal mortality (NCHS)

Run on 2026-11-21 with `notebooks/03_predictors_g2_g3.ipynb`. Full output: [`data/outputs_03_predictors_g2_g3.txt`](data/outputs_03_predictors_g2_g3.txt). Spanish version: [`predictor_table_es.md`](predictor_table_es.md).

**Framework stages:** S7 (predictors), G2 (leakage) and G3 (sample size). The contract table is in `data/contract/perinatal_nchs_v1/` (one file per year, not versioned).

## 1. The contract table (S7)

29,963,276 products of 22 weeks or more (2016–2023), one row per product, with 24 parameters. Decisions applied: D3 (the unknown code is missing, no category or indicator) and D4 (no variables that depend on the length of pregnancy).

| Block | Parameters | Reference | % missing |
|---|---|---|---|
| Mother's age (continuous) | 1 | — | 0.00 |
| Race and Hispanic origin: Black, Hispanic, Asian, other | 4 | Non-Hispanic White | 0.92 |
| Education: associate or some college; bachelor's or more | 2 | High school or less | 1.49 |
| Born outside the US | 1 | — | 0.23 |
| WIC | 1 | — | 1.19 |
| Earlier births now living: 1; 2 or more | 2 | None | 0.17 |
| Any earlier live birth now dead | 1 | — | 0.28 |
| Months since the last live birth: under 18; 18 to 59; 60 or more | 3 | First child | 4.50 |
| Earlier cesarean | 1 | — | 0.13 |
| Pre-pregnancy BMI (continuous) | 1 | — | 2.28 |
| Smoked before pregnancy | 1 | — | 0.48 |
| Prenatal care: started after the first trimester; no care | 2 | First trimester | 2.31 |
| Pre-existing diabetes; pre-existing hypertension; infertility treatment | 3 | — | 0.13 |
| Multiple pregnancy | 1 | Single | 0.00 |
| **Total** | **24** | | |

For "months since the last live birth", codes 000–003 (a record of a multiple delivery, not an interval) are treated as missing; that is why its missingness (4.5%) exceeds the unknown share of the audit (3.2%).

## 2. Gate G2: leakage

| Check | Result |
|---|---|
| No predictor comes from delivery, the product or the outcome, or is a variable excluded by D4 | Met |
| No missingness indicator among the predictors | Met |
| Unit: the product; the group is the unit itself (the files do not identify the mother) | Met |

**Leakage test of decision D3.** The number of unknown fields of each record, **on its own**, separates the events with an **AUROC of 0.639** in the development years. 89.1% of products have no unknown field.

**What it means.** The difference in how the two forms are completed carries information about the outcome: a model that used the unknowns as data would reach an AUROC near 0.64 without knowing anything about the pregnancy. That is why D3 forbids missingness indicators. The final model will also be evaluated on complete records only (D3 sensitivity): if performance falls a lot, part of it came from the form.

**G2: passes**, with the complete-records sensitivity as a mandatory control in S9.

## 3. Gate G3: sample size

| Measure | Value |
|---|---|
| Development products (2016–2021) | 22,681,046 |
| Development events | 149,057 (prevalence 0.657%) |
| Candidate parameters | 24 (6,211 events per parameter) |
| Observed Cox-Snell R² (cross-validated) | 0.0058 (7.6% of the maximum of 0.0761) |
| Products required (shrinkage criterion, the largest) | 37,147 |
| Events required | 245 |
| Parameters the data support | 14,654 |

**How it was computed.** Logistic regression with 5-fold cross-validation on all events and 3% of non-events, with weights inverse to the sampling probability so the likelihood represents the full data. Imputation (median) and scaling are fitted inside each fold.

**G3: passes** by a wide margin: the data exceed the required size more than 600 times.

**Primary learner (S8).** With 6,211 events per parameter, the framework rule (20 or more) says to choose the best base learner in a preliminary run.

**Reading the R².** A Cox-Snell R² of 7.6% of its maximum indicates a moderate signal. As a rough reference, at this prevalence it corresponds to discrimination of the order of 0.73 to 0.76 AUROC, close to the framework's 0.75 threshold. It is consistent with the expectation written in the card before the results (0.65 to 0.75). It is not the model's AUROC: that is estimated in S8.

*Confidential: internal use of the research project.*
