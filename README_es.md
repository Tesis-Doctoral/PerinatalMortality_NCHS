# Mortalidad perinatal con datos NCHS

> **Framework.** Este repositorio aplica el framework por etapas para modelos de predicción clínica de la tesis. El framework (etapas, puertas, criterios y literatura) y el catálogo de modelos con su estado están en [StagedFramework_ClinicalPrediction](https://github.com/Tesis-Doctoral/StagedFramework_ClinicalPrediction).

¿Se puede identificar a los embarazos con riesgo alto de terminar en una muerte perinatal (muerte fetal de 22 semanas o más, o muerte neonatal en los primeros 7 días)? Este modelo usa los archivos públicos del National Center for Health Statistics (NCHS, CDC) y sigue el framework por etapas para modelos de predicción clínica.

> **Estado (21/11/2026): ficha del desenlace escrita y decisiones D1 y D2 resueltas.** Datos del componente fetal: archivos públicos de muertes fetales 2016–2023. Punto de predicción: prenatal (opción A). Adaptador de datos hecho: 8 años (2016–2023), de 22.337 a 27.006 eventos perinatales por año ([`data/outputs_01_build_perinatal.txt`](data/outputs_01_build_perinatal.txt)). Auditoría de conteos hecha ([`count_audit_es.md`](count_audit_es.md)): P1 pasa. Decisiones D3 a D5 aprobadas. Tabla de predictores (24 parámetros) y puertas P2 y P3 pasadas ([`predictor_table_es.md`](predictor_table_es.md)). Siguiente: modelado (E8).

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

Lectores: `libraries/nchs_reader.py` (nacimientos vinculados con defunciones) y `libraries/perinatal_builder.py` (muertes fetales y unión de los dos componentes). Leen los ZIP directamente, sin descomprimirlos.

*Confidencial: uso interno del proyecto de investigación.*
