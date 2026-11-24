# Mortalidad perinatal con datos NCHS

> **Framework.** Este repositorio aplica el framework por etapas para modelos de predicción clínica de la tesis. El framework (etapas, puertas, criterios y literatura) y el catálogo de modelos con su estado están en [StagedFramework_ClinicalPrediction](https://github.com/Tesis-Doctoral/StagedFramework_ClinicalPrediction).

¿Se puede identificar a los embarazos con riesgo alto de terminar en una muerte perinatal (muerte fetal de 22 semanas o más, o muerte neonatal en los primeros 7 días)? Este modelo usa los archivos públicos del National Center for Health Statistics (NCHS, CDC) y sigue el framework por etapas para modelos de predicción clínica.

> **Estado (24/11/2026): modelo cerrado como señal insuficiente.** XGBoost, AUROC limpio 0,723 (versión 2b con imputación por sorteo aleatorio; [`data/outputs_10_p2_imputation_check.txt`](data/outputs_10_p2_imputation_check.txt)). El 0,7455 de la versión 2b incluía la señal del tipo de formulario que traía la imputación por la mediana, detectada por la puerta P2. Modelo M5 del catálogo.

[English version](README.md)

## Alcance

- **Desenlace:** muerte perinatal, con sus componentes fetal y neonatal precoz.
- **Framework:** [`framework_es.md`](framework_es.md) (inglés: [`framework.md`](framework.md)), versión 1.0. Ficha del desenlace: [`docs/outcome_card_perinatal_nchs_es.md`](docs/outcome_card_perinatal_nchs_es.md).

## Datos

Cómo se producen los archivos, del hospital a la descarga: [`docs/data_source_nchs_es.md`](docs/data_source_nchs_es.md).

Los archivos de NCHS se guardan **fuera del repositorio**, en la carpeta hermana `../NCHS_data/raw/` (otra ubicación se indica con la variable de entorno `NCHS_RAW_DIR`). Son públicos, pero no se redistribuyen: solo se publica el código. Su uso está sujeto al acuerdo de uso de datos de NCHS: análisis estadístico únicamente, sin intentar identificar personas ni unir con datos identificables. Los reportes no muestran celdas con menos de 10 casos.

## Orden de ejecución

| Orden | Notebook | Crea | Etapa del framework |
|---|---|---|---|
| 1 | `notebooks/01_build_cohorts_es.ipynb` | `data/interim/perinatal_<año>.parquet` (una fila por producto de 22 semanas o más: nacidos vivos con su muerte de 0 a 6 días y muertes fetales) y `data/outputs_01_build_perinatal.txt` | E2 (adaptador de datos) |
| 2 | `notebooks/02_count_audit_es.ipynb` | `data/outputs_02_count_audit.txt`; documentado en [`count_audit_es.md`](count_audit_es.md) | E4, P1 |
| 3 | `notebooks/03_predictors_g2_g3_es.ipynb` | `data/contract/perinatal_nchs_v1/` (tabla contrato) y `data/outputs_03_predictors_g2_g3.txt`; documentado en [`predictor_table_es.md`](predictor_table_es.md) | E7, P2, P3 |
| 4 | `notebooks/04_preliminary_learners_es.ipynb` | `data/outputs_04_preliminary_learners.txt` (corrida preliminar: búsqueda de hiperparámetros y elección del modelo principal) | E8 |
| 5 | `notebooks/05_main_evaluation_es.ipynb` | `data/outputs_05_main_evaluation.txt` (validación interna recalibrada, validación temporal, sensibilidades y clasificación) | E8, E9, P4 |
| 6 | `notebooks/06_return_r4_es.ipynb` | `data/contract/perinatal_nchs_r4/` y `data/outputs_06_return_r4.txt` (retorno R4: 28 semanas o más, registros completos, predictores más finos; P2, P3, corrida preliminar, evaluación y clasificación) | R4, E7–E9, P2–P4 |
| 7 | `notebooks/07_model_v2_es.ipynb` | `data/contract/perinatal_nchs_v2/` y `data/outputs_07_model_v2.txt` (versión 2: población y predictores de la versión 1 + diabetes gestacional, hipertensión gestacional, eclampsia y tabaquismo en el embarazo, por decisión del equipo de modelado) | E7–E9, P2–P4 |
| 8 | `notebooks/08_new_learners_es.ipynb` | `data/outputs_08_new_learners.txt` (datos de la versión 2: regresión logística con *splines*, EBM, MLP y CatBoost por separado frente a XGBoost; requiere `catboost` e `interpret`) | E8 |
| 9 | `notebooks/09_model_v2b_es.ipynb` | `data/contract/perinatal_nchs_v2b/` y `data/outputs_09_model_v2b.txt` (versión 2 completa, segundo retorno: + talla de la madre, cigarrillos en el primer trimestre, medicamentos para la fertilidad y reproducción asistida, sexo del producto, mes de la última menstruación; edad del padre como sensibilidad). Requiere el notebook 01 reconstruido con `REBUILD = True` | E7–E9, P2–P4 |
| 10 | `notebooks/10_p2_imputation_check_es.ipynb` | `data/outputs_10_p2_imputation_check.txt` (verificación de P2 sobre la imputación por la mediana antes de la versión 3: mediana frente a sorteo aleatorio, indicadores explícitos y manejo nativo) | P2 |

Lectores: `libraries/nchs_reader.py` (nacimientos vinculados con defunciones) y `libraries/perinatal_builder.py` (muertes fetales y unión de los dos componentes). Leen los ZIP directamente, sin descomprimirlos.

*Confidencial: uso interno del proyecto de investigación.*
