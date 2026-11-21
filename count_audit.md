# Count audit — perinatal mortality (NCHS)

Run on 2026-11-21 with `notebooks/02_count_audit.ipynb` on the population built by the data adapter (`notebooks/01_build_cohorts.ipynb`). Full output: [`data/outputs_02_count_audit.txt`](data/outputs_02_count_audit.txt). Spanish version: [`count_audit_es.md`](count_audit_es.md).

**Framework stage:** S4 (count audit) and gate G1. Its results fix the predictors (S7) and prepare the leakage gate (G2).

All figures are aggregate counts; counts from 1 to 9 are shown as "<10". Predictor frequencies are computed in the **whole population**, never split by outcome, so that no predictor is chosen by its association with death. The only comparison by component (Q-C7) is a leakage check.

## 1. Population and events

### Q-C1. Population flow

| Step (sum 2016–2023) | Live births | Fetal deaths |
|---|---|---|
| Records in the files | 29,950,846 | 358,175 |
| Mothers not resident in the US | 68,505 | 930 |
| Unknown gestational age | 21,917 | 11,837 |
| Under 22 weeks | 30,557 | 211,999 |
| **Population (22 to 47 weeks, residents)** | **29,829,867** | **133,409** |

**What it means.** Almost every live birth enters. In the fetal file, by contrast, most records are losses under 22 weeks, which some states report although they are not required; they are excluded because the perinatal period starts at 22 weeks.

### Q-C2. Events by year

| Year | Products | Events | Fetal | Neonatal 0–6 days | Per 1,000 | % fetal | Events ≥28 wk |
|---|---|---|---|---|---|---|---|
| 2016 | 3,956,689 | 27,006 | 18,401 | 8,605 | 6.83 | 68.1 | 15,364 |
| 2017 | 3,866,265 | 25,929 | 17,707 | 8,222 | 6.71 | 68.3 | 14,877 |
| 2018 | 3,802,569 | 25,324 | 17,326 | 7,998 | 6.66 | 68.4 | 14,501 |
| 2019 | 3,757,755 | 24,173 | 16,568 | 7,605 | 6.43 | 68.5 | 13,983 |
| 2020 | 3,623,630 | 23,261 | 16,151 | 7,110 | 6.42 | 69.4 | 13,601 |
| 2021 | 3,674,138 | 23,364 | 16,376 | 6,988 | 6.36 | 70.1 | 13,771 |
| 2022 | 3,677,156 | 22,780 | 15,632 | 7,148 | 6.20 | 68.6 | 13,657 |
| 2023 | 3,605,074 | 22,337 | 15,248 | 7,089 | 6.20 | 68.3 | 13,282 |

**What it means.** There are 194,174 events in 29.96 million products (6.5 per 1,000). Seven in ten events are fetal deaths. The rate declines gently over the years (from 6.83 to 6.20), which matters for calibration over time (C4).

**For the model.** Sample size is not a constraint: gate G3 will pass comfortably. Development with 2016–2021 (149,057 events) and temporal test with 2022–2023 (45,117 events).

### Q-C3. Timing of fetal death (population, 2016–2023)

| Estimated timing | Fetal deaths | % |
|---|---|---|
| Before labor (N) | 64,616 | 48.4 |
| During labor (L or A) | 17,704 | 13.3 |
| Unknown (U) or blank | 51,089 | 38.3 |

**What it means.** At least half of fetal deaths occur before labor. This confirms decision D2: a model at birth or at admission could not predict them.

**For the model.** It is not a predictor (it describes the outcome). It is used to describe the fetal component and as a sensitivity analysis (antepartum only or intrapartum only).

### Gate G1. Definition

The counts of products and events of the 8 years reproduce exactly those of the data adapter. The notebook stops if they do not match. **G1: passes.**

## 2. Candidate predictors (whole population)

### Q-C4. Categorical variables (percentage of the 29.96 million products)

| Variable | Distribution |
|---|---|
| Race and Hispanic origin | Non-Hispanic White 51.1; non-Hispanic Black 14.3; Hispanic 24.2; non-Hispanic Asian 6.2; more than one race 2.3; American Indian 0.7; Pacific Islander 0.3; unknown 0.9 |
| Mother's education | 8th grade or less 3.2; 9th–12th without diploma 8.9; high school 25.7; some college 19.0; associate 8.3; bachelor's 20.9; master's 9.8; doctorate 2.9; unknown 1.5 |
| Born in the US | Yes 77.2; no 22.6; unknown 0.2 |
| WIC | Yes 33.6; no 65.2; unknown 1.2 |
| Smoked during pregnancy | Yes 5.4; no 94.1; unknown 0.5 |
| Pre-existing diabetes | 1.0 |
| Gestational diabetes | 7.3 |
| Pre-existing hypertension | 2.4 |
| Gestational hypertension | 8.0 |
| Eclampsia | 0.3 |
| Infertility treatment | 2.1 |
| Earlier cesarean | 15.4 |
| Plurality | Single 96.7; twin 3.2; triplet or more 0.1 |

### Q-C5. Numeric variables

| Variable | % unknown | P5 | P25 | Median | P75 | P95 |
|---|---|---|---|---|---|---|
| Mother's age | 0.0 | 20 | 25 | 29 | 33 | 39 |
| Pre-pregnancy BMI | 2.3 | 19.1 | 22.4 | 25.8 | 31.0 | 40.7 |
| Month prenatal care began | 2.3 | 1 | 2 | 3 | 3 | 6 |
| Earlier live births now living | 0.2 | 0 | 0 | 1 | 2 | 4 |
| Earlier live births now dead | 0.3 | 0 | 0 | 0 | 0 | 0 |
| Months since the last live birth | 3.2 | 13 | 24 | 37 | 63 | 128 |
| Number of earlier cesareans | 0.2 | 0 | 0 | 0 | 0 | 1 |
| Cigarettes per day before pregnancy (added by D4) | 0.5 | 0 | 0 | 0 | 0 | 6 |

For "months since the last live birth", 38.1% do not apply because it is the first child. Smoking before pregnancy fell from 9.4% of products in 2016 to 3.8% in 2023, a change that matters for calibration over time (C4).

### Q-C6. Missingness by year

In the whole population, every variable has less than 4% unknown in every year, with no jump between 2016–2017 and 2018 onward. The late adoption of the revised fetal report in some states is not visible in the whole population.

## 3. Leakage and definition checks

### Q-C7. Unknowns depend on the type of certificate

| Variable | % unknown, live births | % unknown, fetal deaths |
|---|---|---|
| WIC | 1.1 | 18.7 |
| Education | 1.4 | 13.1 |
| BMI | 2.2 | 12.9 |
| Months since the last live birth | 3.2 | 12.8 |
| Month prenatal care began | 2.3 | 12.5 |
| Smoked during pregnancy | 0.4 | 8.3 |
| Smoked before pregnancy | 0.4 | 8.3 |
| Number of earlier cesareans | 0.1 | 6.3 |
| Born in the US | 0.2 | 6.1 |
| Risk factors (diabetes, hypertension, eclampsia, infertility, cesarean) | 0.1 | 5.9 |
| Earlier births now dead | 0.3 | 4.8 |
| Race and Hispanic origin | 0.9 | 4.4 |
| Earlier births now living | 0.2 | 3.4 |
| Age, plurality | 0.0 | 0.0 |

**What it means.** The report of fetal death is completed with much less information than the birth certificate. Because every fetal death is an event, "unknown" is strongly associated with the outcome because of how the form is filled, not because of biology. A model that used unknown as information would learn to recognize the type of form: this is **leakage** (gate G2).

### Q-C8. Gestational age of the fetal component

Among fetal deaths with both estimates, the obstetric estimate (the one used) and the combined gestation agree on the same week in 62–64% and within one week in 79–80%. With the combined gestation, about 800 to 900 more fetal deaths per year would enter.

**What it means.** The gestational age of a fetal death is uncertain (the fetus may die days before delivery). The main population uses the obstetric estimate, the one NCHS uses for tabulation.

**For the model.** Sensitivity: population defined with the combined gestation.

## 4. Decisions from the audit (approved 2026-11-21, recorded in the outcome card)

**D3. Handling of unknowns (from Q-C7).** Proposal:
- The "unknown" code is treated as missing and is **never** used as a category or with a missingness indicator.
- Missing values are imputed inside the training part of each split, with an imputation model that does **not** use the type of certificate.
- Sensitivity 1: only products with every predictor complete.
- Sensitivity 2 (leakage check): a model with only the number of unknown fields per record; if it discriminates, it is reported as evidence of the form bias.

**D4. Predictors that depend on the length of pregnancy.** Option A already excluded the number of visits and weight gain. The audit shows others with the same problem:
- **Gestational diabetes:** screening is done at weeks 24 to 28; a pregnancy ending at week 22–24 can hardly have it recorded.
- **Gestational hypertension and eclampsia:** they appear from week 20 and are more likely the longer the pregnancy lasts.
- **Smoked during pregnancy:** includes the third trimester, which a short pregnancy does not have.
- **Month prenatal care began:** a pregnancy ending at week 22 cannot start care in month 6 or later.

Proposal: exclude gestational diabetes, gestational hypertension and eclampsia; replace "smoked during pregnancy" with **"smoked before pregnancy"** (field `CIG_0`, present in both files; it must be added to the adapter); and use the month prenatal care began grouped as "first trimester / later / no care". As sensitivity, the model with all variables and the population of 28 weeks or more.

**D5. Gestational age of the fetal component.** Edited obstetric estimate in the main population; combined gestation as sensitivity (Q-C8).

## 5. Predictor list (with D3 and D4)

| Block | Predictors |
|---|---|
| Mother | Age; race and Hispanic origin (White, Black, Hispanic, Asian, other); education (high school or less, associate or some college, bachelor's or more); born outside the US; WIC |
| Obstetric history | Earlier births now living (0, 1, 2 or more); any earlier birth now dead; months since the last live birth (first child, under 18, 18 to 59, 60 or more); earlier cesarean |
| Current pregnancy | Pre-pregnancy BMI; smoked before pregnancy; start of prenatal care (first trimester, later, no care); pre-existing diabetes; pre-existing hypertension; infertility treatment; plurality (single, multiple) |

About 20 parameters. Against about 150,000 development events, there are more than 20 events per parameter: by the framework rule, the primary learner is chosen in a preliminary run among the base learners.

*Confidential: internal use of the research project.*
