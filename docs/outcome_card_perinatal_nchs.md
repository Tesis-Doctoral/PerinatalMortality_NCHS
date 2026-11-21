# Outcome card — perinatal mortality, NCHS

Outcome card following the staged framework ([`../framework.md`](../framework.md)), version 1, 2026-11-20. Fields marked **pending** are fixed, and recorded in the decision log, before the gate that needs them. Spanish version: [`outcome_card_perinatal_nchs_es.md`](outcome_card_perinatal_nchs_es.md).

## 1. The question

**Can pregnancies at high risk of ending in a perinatal death be identified?**

Perinatal mortality covers, per WHO and ICD-10, the period from 22 completed weeks of gestation to 7 completed days after birth. It has two components:

- **Fetal:** fetal death at 22 weeks or more (stillbirth).
- **Early neonatal:** death of a live-born infant between day 0 and day 6.

## 2. Identity

| Field | Value |
|---|---|
| Outcome | Perinatal death: fetal death at 22 weeks or more, or early neonatal death (0 to 6 days) |
| Rung | First rung of the outcome ladder |
| Data source | NCHS (CDC): public-use *Linked Birth/Infant Death* files, cohort version, for live births and their early neonatal death; public-use fetal death file for the fetal component (**pending**, decision D1) |
| Unit and group | Delivery of a product of 22 weeks or more (live birth or fetal death). No mother identifier: the group is the unit itself |
| Population | US-resident mothers, 22 weeks or more (`COMBGEST` 22–47 in live births; the equivalent field in the fetal file is **pending**) |
| Main label | Fetal death at 22 weeks or more, or death between day 0 and day 6 |
| Sensitivity labels | Only 28 weeks or more (WHO international-comparison definition); each component separately |
| Counts | **Pending** the audit. Early neonatal component already available: about 7,000 to 8,600 events per cohort among live births of 22 weeks or more |

## 3. Decisions pending before the audit

**D1. Data for the fetal component.** The early neonatal component can already be built from the linked files (the adapter `libraries/nchs_reader.py` is ready). The fetal component needs the NCHS public-use fetal death file. The download page must be checked for which years are published, in what format and with which variables, and whether they use the same 2003 revised certificate as the births.

**D2. Prediction point.** This is the central decision for this outcome. Most fetal deaths occur before labor, so **they cannot be predicted at birth**: by then they have already happened. The options are:

| Option | Allowed information | Consequence under the framework |
|---|---|---|
| A. Antenatal | Only what is known about the pregnancy before delivery: maternal characteristics, obstetric history, prenatal care, smoking, risk factors and infections | The event occurs after the information (C1 and C2 are met). Without gestational age at delivery, birthweight or Apgar, the expected discrimination is moderate |
| B. At admission for delivery | Option A plus gestational age at admission | Many fetal deaths have already happened at admission: for that component the model identifies rather than predicts (criterion C1), as an early identifier |

**Decided on 2026-11-20: option A (antenatal)**, before any count by outcome. It is the only option in which the whole perinatal outcome, including the fetal component, occurs after the information. Option B is declared now as a possible return R3 (another prediction point) if model A is classified as *neither*; in that case it is reported as an early identifier for the fetal component.

## 4. Predictors (S7)

The final list is fixed with the count audit. With option A:

| Field | Value |
|---|---|
| Prediction point | Before delivery: what is known about the pregnancy without the delivery or product information |
| Allowed | Maternal characteristics (age, race and Hispanic origin, education, marital status, born in the US or abroad, payment source, WIC); obstetric history (earlier births now living and now dead, other terminations, interval since the last pregnancy, earlier cesareans, earlier preterm birth); month prenatal care began; smoking; pre-pregnancy BMI; pre-existing and gestational diabetes and hypertension, eclampsia; infertility treatment; infections; plurality |
| Excluded because it depends on the length of the pregnancy | Number of prenatal visits and weight gain: fewer weeks mean fewer visits and less weight gained, so they would leak gestational age at delivery |
| Excluded as delivery or product information | Gestational age and birthweight, labor and delivery, presentation and route, Apgar, sex, congenital anomalies, everything after birth |
| Plurality | Allowed: a multiple pregnancy is usually known at prenatal visits |
| Expectation, stated before the results | Fetal death models with pregnancy information only usually reach an AUROC of 0.65 to 0.75. The model may be classified as *neither*; the 0.75 threshold is not changed |

## 5. Sample size and learner (G3, S8)

| Field | Value |
|---|---|
| Events | Thousands per cohort; gate G3 is checked with the Riley et al. criteria |
| Primary learner | Fixed in S8 with the framework rule on events per parameter |

## 6. Classification criteria (G4)

| Criterion | Status |
|---|---|
| C1, events already present | Applicable: with option A the event occurs after the information |
| C2, outcome with time | Applicable |
| C3, detection bias | Not applicable: the outcome comes from certificates, not from a test |
| C4, stability over time | Applicable: development with cohorts 2016–2021 and temporal test with 2022–2023 |

## 7. Data and conditions of use

- The NCHS files are kept outside the repository, in the shared folder `../NCHS_data/raw/`; they are not redistributed.
- NCHS data use agreement: statistical analysis only; no attempt to identify any person; no linkage with identifiable data. Reports show no cell with fewer than 10 cases.

## 8. Next tasks

1. D1: confirm and download the fetal death file.
2. ~~D2: prediction point~~ (option A, antenatal, 2026-11-20).
3. Adapter for the fetal component and join with the early neonatal component.
4. Count audit; predictors; gate G3; model and classification.

*Confidential: internal use of the research project.*
