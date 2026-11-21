# Framework por etapas para modelos de predicción clínica — versión 1.0

Versión 1.0. El framework por etapas que sigue este modelo desde la definición del desenlace hasta el reporte. Versión en inglés: [`framework.md`](framework.md).

> **Nomenclatura.** Los archivos en español usan las etapas E1 a E11 y las puertas P1 a P4. Los archivos en inglés usan S1 a S11 y G1 a G4 para las mismas etapas y puertas.

![Framework por etapas: once etapas en cuatro bloques, cuatro puertas, retornos R1 a R4 y la reducción por tamaño de muestra](docs/framework_figure.png)

*Figura. El framework por etapas (en inglés: S = etapa, G = puerta). Un punto marca las etapas que usan la ficha del desenlace y un cuadrado las que usan el adaptador de datos; las etapas sin marca se reutilizan sin cambios.*

## 1. Qué responde el framework

Un modelo con buena discriminación puede predecir eventos que aún no ocurren o solo reconocer eventos que ya están en curso cuando se hace la predicción. El framework lleva cualquier desenlace adverso desde la definición hasta el reporte y termina clasificando el modelo ajustado como **predictor**, **identificador temprano** o **ninguno**.

## 2. Tres capas

| Capa | Contiene | Cambia cuando |
|---|---|---|
| **Núcleo** | Etapas, puertas, validación, métricas, regla de clasificación, reporte | Nunca entre desenlaces |
| **Ficha del desenlace** | Peldaño en la escalera de desenlaces, población, definición y momento del evento, punto de predicción, predictores propios, conjunto reducido de predictores, modelo principal, set de sensibilidad, conteos esperados | Un desenlace nuevo necesita una ficha nueva |
| **Adaptador de datos** | Código que convierte una fuente de datos en la tabla contrato | Una fuente nueva necesita un adaptador nuevo |

El núcleo solo lee la **tabla contrato**: una fila por unidad de análisis con `unit_id`, `group_id` (nunca se divide entre entrenamiento y prueba), `t0` (tiempo cero), `t_pred` (punto de predicción), la etiqueta principal y las de sensibilidad como columnas, cada predictor con un indicador de si se midió, y `period` (período calendario o era de codificación). En este modelo la tabla contrato es `data/contract/perinatal_nchs_v1.parquet`, construida por el adaptador de datos (`libraries/nchs_reader.py`) a partir de los archivos públicos de NCHS.

## 3. Etapas y puertas

| Bloque | Etapa o puerta | Pregunta | Ficha | Adaptador |
|---|---|---|---|---|
| Definir y auditar | **E1** Gobierno y configuración | ¿Qué se fija antes de correr nada? | • | |
| | **E2** Universo y población | ¿Qué unidades se pueden estudiar? | • | ■ |
| | **E3** Definición del desenlace | ¿Qué cuenta como evento, de qué fuentes y cuándo ocurrió? | • | ■ |
| | **E4** Auditoría de conteos | ¿Cuántos eventos, dónde, cuándo y con qué solapamiento? | • | ■ |
| | **P1** Puerta de definición | ¿Están fijos la población, la unidad y la definición, y se reproducen los conteos de referencia? | | |
| Fijar el punto de predicción | **E5** Unidad de análisis y solapamiento | ¿Qué es un registro y qué debe quedar en un solo lado de una partición? | | ■ |
| | **E6** Punto de predicción y ventana | ¿Cuándo se predice y qué información puede usarse? | • | ■ |
| | **P2** Puerta de fuga | ¿No entra nada posterior al punto de predicción y las particiones están agrupadas por paciente? | | |
| Construir | **E7** Predictores | ¿Qué variables, con qué cobertura y límites? | • | ■ |
| | **P3** Puerta de tamaño de muestra | ¿Hay eventos suficientes para los parámetros candidatos (Riley et al.)? | | |
| | **E8** Modelado, validación y métricas | ¿Qué tan bien funciona y con qué incertidumbre? | | |
| Verificar y actuar | **E9** Sensibilidad y robustez | ¿Resiste otras decisiones razonables, incluidos los criterios C1 a C4? | • | ■ |
| | **P4** Puerta de clasificación | ¿Predictor, identificador temprano o ninguno? | | |
| | **E10** De la clasificación a la acción | ¿Qué uso corresponde a la clase y es justo entre subgrupos? | • | ■ |
| | **E11** Reporte (TRIPOD+AI) | ¿Qué se entrega? | • | |

No se ajusta ningún modelo antes de P3. Cada decisión va al **libro de decisiones** con su fecha, las opciones consideradas, la opción elegida, la razón, el tipo de razón (clínica, metodológica o técnica) y quién la validó.

## 4. Las puertas en detalle

**P1, definición.** La población, la unidad y la definición del evento están fijas y los conteos de referencia se reproducen (una verificación `EXPECTED` detiene cualquier corrida cuya población no sea la auditada).

**P2, fuga.** No entra información posterior al punto de predicción (ni diagnósticos, procedimientos, códigos DRG o tratamientos de la misma admisión) y toda partición está agrupada por paciente. La imputación, el escalado, el ajuste, el apilamiento y la recalibración se ajustan dentro de la parte de entrenamiento.

**P3, tamaño de muestra.** Los criterios de Riley et al. (encogimiento esperado de 0,9 o más, optimismo en la variación explicada de 0,05 o menos, riesgo global preciso) dan el mínimo de unidades y eventos para los parámetros candidatos, con el R² de Cox-Snell observado de una regresión logística con validación cruzada (o un valor supuesto cuando no se puede ajustar ningún modelo). Si los datos no alcanzan, el desenlace se reporta como análisis de factibilidad y el retorno R1 pasa al siguiente peldaño de la escalera de desenlaces.

**Reducción por tamaño de muestra.** Cuando un modelo cumple todos los criterios aplicables de P4 pero no pasa P3, puede reajustarse **una vez** con un conjunto reducido de predictores que no supere los parámetros que soportan los datos. El conjunto reducido se fija en la ficha con reglas (colapsar categorías, conservar las variables clínicas centrales), nunca por la asociación de un predictor con el desenlace. El modelo reducido debe pasar P3 y se clasifica de nuevo en P4 con los mismos umbrales. No es un retorno.

**P4, clasificación.** Cuatro criterios, cada uno probado con un análisis de sensibilidad preespecificado:

| Criterio | Pregunta | Se cumple si |
|---|---|---|
| C1, eventos ya presentes | ¿Cuánto cae el desempeño al retirar los eventos presentes en el punto de predicción (población landmark)? | La AUROC cae 0,05 o menos y se conservan al menos dos tercios de la ganancia de AUPRC sobre la prevalencia |
| C2, desenlace con tiempo | ¿Se mantiene el desempeño para eventos fechados después del punto de predicción? | AUROC de 0,75 o más, con límite inferior del IC 95% de 0,70 o más |
| C3, sesgo de detección | ¿Se mantiene entre las pacientes examinadas, cuando el desenlace depende de un examen? | La AUROC cae 0,05 o menos |
| C4, estabilidad en el tiempo | ¿Discrimina y calibra en un período posterior? | AUROC temporal de 0,70 o más, y calibración corregible solo con el intercepto |

- **Predictor:** AUROC de 0,75 o más en la población landmark o en un desenlace con tiempo, y cumple C1 a C4. Pasa a una estrategia de prevención.
- **Identificador temprano:** AUROC de 0,75 o más con la etiqueta completa y el 10% de mayor riesgo concentra al menos el doble de los eventos esperados por azar, pero falla C1, C3 o C4. Sirve para vigilancia y priorización de la revisión, no para prevención.
- **Ninguno:** en otro caso, o con AUROC temporal menor de 0,65.

Un criterio que no puede aplicarse a un desenlace (por ejemplo C3 cuando el desenlace no depende de un examen) se marca *no aplica* en la ficha, con la razón, antes de ajustar cualquier modelo.

## 5. Retornos y escalera de desenlaces

| Retorno | Desde | Hacia | Qué cambia |
|---|---|---|---|
| R1 | P3 | E3 | Siguiente peldaño de la escalera de desenlaces |
| R2 | P4 | E3 | Un desenlace fechado después del punto de predicción |
| R3 | P4 | E6 | Otro punto de predicción |
| R4 | P4 | E7 | Más predictores o predictores distintos |

Como máximo dos retornos por desenlace; cada retorno se reporta y el modelo se clasifica de nuevo después de cada uno. Sin retornos disponibles y sin uso, o sin peldaño disponible en P3, el resultado va a E11 como resultado negativo o de factibilidad.

**Escalera de desenlaces** (tres peldaños): el desenlace ideal; un sustituto más frecuente en la misma ruta clínica; un desenlace fechado después del punto de predicción.

## 6. Reglas de modelado (E8)

- Validación cruzada anidada agrupada por paciente (5 pliegues externos × 3 repeticiones, pliegues internos agrupados), recalibración de Platt dentro del entrenamiento, intervalos por bootstrap de pacientes.
- Métricas: AUROC, AUPRC frente a la prevalencia, puntaje de Brier, pendiente e intercepto de calibración, razón observados/esperados, error de calibración esperado, proporción de eventos en el 5% y el 10% de mayor riesgo, curva de decisión.
- Modelos base: regresión logística penalizada, bosque aleatorio, árboles extra, XGBoost; ensamble apilado con meta-aprendiz logístico como comparación. El ensamble se adopta solo si supera de forma consistente al mejor modelo base.
- **Modelo principal según eventos por parámetro (pendiente de validación del director).** Se fija en la ficha antes de cualquier modelo: con menos de 20 eventos por parámetro candidato, la regresión logística penalizada es el modelo principal y los demás son comparaciones; con 20 o más, el mejor modelo base de una corrida preliminar.
- Sin remuestreo en el análisis principal (las correcciones del desbalance dañan la calibración); pesos de clase y remuestreo solo como sensibilidad.

## 7. Principios que no cambian

1. Auditar antes de modelar.
2. Las reglas se miden primero como columnas y después se aplican como filtros, cada una con su análisis de sensibilidad.
3. La etiqueta es un proxy documentado: catálogo verificado de códigos (título, nivel, fuente, fecha) y una tabla de etiqueta con las definiciones de sensibilidad como columnas.
4. El punto de predicción y la ventana se fijan antes que los predictores.
5. Cada decisión es una decisión numerada en el libro.
6. Solo salidas agregadas; celdas pequeñas suprimidas; ningún identificador en archivos publicados.
7. Notebooks y documentos en pares EN/ES con código idéntico, configuración fija, reporte TRIPOD+AI.

*Confidencial: uso interno del proyecto de investigación.*
