# Stage S10 — from classification to action: NCHS perinatal mortality (M5)

Spanish version: [`e10_action_perinatal_es.md`](e10_action_perinatal_es.md). Sources: `data/outputs_09_model_v2b.txt` (version 2b) and `data/outputs_10_p2_imputation_check.txt` (gate G2 check of the imputation), development cohorts 2016–2021: 22.7 million products and 149,057 events (6.6 per 1,000).

## 1. Class and use

The model was classified as **insufficient signal**: with the antenatal information shared by the birth certificate and the fetal death report, the clean AUROC is 0.723, below the 0.75 threshold. Its calibration is good (temporal slope 0.98), but it discriminates poorly.

**Its use for individual decisions is not recommended** (which pregnant woman should get more intensive prenatal care). At the best possible threshold, sensitivity and specificity do not exceed 0.66 at the same time: a third of the pregnancies without an event would be flagged as high risk, and a third of the events would still be missed.

What the model does leave are three contributions for health entities: a finding on data quality, a description of antenatal risk factors and a specification of which information would be needed to predict.

## 2. Main finding: the quality of the fetal death report

- 47% of fetal death reports have at least one unknown antenatal item, against 14% of birth certificates.
- That difference makes a model "learn" the type of form rather than the risk: with median imputation the AUROC rises to 0.7455, and with unknown indicators to 0.770, with no additional clinical information. In complete records, all four strategies give the same result (0.689–0.691).
- Gate G2 of the framework detected it twice: with the verification model M6 (fetal death, 0.680 with the leakage controlled) and with the imputation test (0.7455 → 0.723).

**Recommendation:** improve the completion of the fetal death report, especially the history and prenatal-care items, with the same fields and quality as the birth certificate. Without that improvement, any perinatal mortality model built from vital statistics risks inflating its performance.

## 3. Antenatal risk factors (descriptive, at population level)

Although the model is not useful to predict case by case, it does describe which groups concentrate the risk: the top 10% of risk holds 42% of the events (4.2 times chance). Some adjusted associations (logistic regression, all products):

| Factor | Adjusted odds ratio |
|---|---|
| Smoking during pregnancy | 1.23 (1.25 from 28 weeks) |
| Eclampsia | 1.16 |
| Fertility drugs / assisted reproduction | 1.07 / 1.06 |
| Male product | 1.06 |
| Mother's height (per inch) | 0.93 |

This kind of result serves **population planning** (where to focus smoking-cessation programs, prenatal follow-up of pregnancies after fertility treatment), not classifying each pregnant woman.

## 4. What would be needed to predict

1. **Antenatal clinical data that vital statistics lack:** ultrasound (fetal growth, growth restriction, Doppler), laboratory results, number and content of prenatal visits, detailed obstetric history.
2. **The same recording for every outcome:** information on pregnancies that end in fetal death collected as completely as for live births, preferably from the antenatal clinical record rather than from the certificate filed after the event.
3. **Another prediction point:** at admission for delivery (option B, declared as return R3 and not used because the model had already used its two returns), with labor information. It would be a different model, with a different use.

## 5. Limitations

- US vital statistics; no geography in the public-use files.
- The associations are descriptive, not causal.
- The clean AUROC (0.723) was estimated with a single repeat of 5-fold cross-validation; version 2b with median imputation used 3 repeats.
