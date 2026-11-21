# Mortalidad perinatal con datos NCHS

> **Framework.** Este repositorio aplica el framework por etapas para modelos de predicción clínica de la tesis. El framework (etapas, puertas, criterios y literatura) y el catálogo de modelos con su estado están en [StagedFramework_ClinicalPrediction](https://github.com/khem777/StagedFramework_ClinicalPrediction).

¿Se puede identificar a los embarazos con riesgo alto de terminar en una muerte perinatal (muerte fetal de 22 semanas o más, o muerte neonatal en los primeros 7 días)? Este modelo usa los archivos públicos del National Center for Health Statistics (NCHS, CDC) y sigue el framework por etapas para modelos de predicción clínica.

> **Estado (20/11/2026): ficha del desenlace escrita, con una decisión pendiente** (datos del componente fetal). Punto de predicción: prenatal (opción A). El adaptador del componente neonatal precoz está listo.

[English version](README.md)

## Alcance

- **Desenlace:** muerte perinatal, con sus componentes fetal y neonatal precoz.
- **Framework:** [`framework_es.md`](framework_es.md) (inglés: [`framework.md`](framework.md)), versión 1.0. Ficha del desenlace: [`docs/outcome_card_perinatal_nchs_es.md`](docs/outcome_card_perinatal_nchs_es.md).

## Datos

Los archivos de NCHS se guardan **fuera del repositorio**, en la carpeta hermana `../NCHS_data/raw/` (otra ubicación se indica con la variable de entorno `NCHS_RAW_DIR`). Son públicos, pero no se redistribuyen: solo se publica el código. Su uso está sujeto al acuerdo de uso de datos de NCHS: análisis estadístico únicamente, sin intentar identificar personas ni unir con datos identificables. Los reportes no muestran celdas con menos de 10 casos.

## Orden de ejecución

| Orden | Notebook | Crea | Etapa del framework |
|---|---|---|---|
| 1 | `notebooks/01_build_cohorts_es.ipynb` | `data/interim/cohort_<año>.parquet` (nacidos vivos y muerte neonatal precoz) | E2 (adaptador de datos) |

*Confidencial: uso interno del proyecto de investigación.*
