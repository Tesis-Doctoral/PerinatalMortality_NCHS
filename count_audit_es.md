# Auditoría de conteos — mortalidad perinatal (NCHS)

Ejecutada el 21/11/2026 con `notebooks/02_count_audit_es.ipynb` sobre la población que construye el adaptador de datos (`notebooks/01_build_cohorts_es.ipynb`). Salida completa: [`data/outputs_02_count_audit.txt`](data/outputs_02_count_audit.txt). Versión en inglés: [`count_audit.md`](count_audit.md).

**Etapa del framework:** E4 (auditoría de conteos) y puerta P1. Sus resultados fijan los predictores (E7) y preparan la puerta de fuga (P2).

Todas las cifras son conteos agregados; los conteos de 1 a 9 se muestran como "<10". Las frecuencias de los predictores se calculan en **toda la población**, nunca separadas por desenlace, para que ningún predictor se elija por su asociación con la muerte. La única comparación por componente (Q-C7) es una verificación de fuga.

## 1. Población y eventos

### Q-C1. Flujo de la población

| Paso (suma 2016–2023) | Nacidos vivos | Muertes fetales |
|---|---|---|
| Registros en los archivos | 29.950.846 | 358.175 |
| Madres no residentes en EE. UU. | 68.505 | 930 |
| Edad gestacional desconocida | 21.917 | 11.837 |
| Menos de 22 semanas | 30.557 | 211.999 |
| **Población (22 a 47 semanas, residentes)** | **29.829.867** | **133.409** |

**Qué significa.** Casi todos los nacidos vivos entran. En el archivo fetal, en cambio, la mayoría de los registros son pérdidas de menos de 22 semanas, que algunos estados reportan aunque no sean obligatorias; quedan fuera porque el período perinatal empieza en 22 semanas.

### Q-C2. Eventos por año

| Año | Productos | Eventos | Fetales | Neonatales 0–6 días | Por 1.000 | % fetales | Eventos ≥28 sem. |
|---|---|---|---|---|---|---|---|
| 2016 | 3.956.689 | 27.006 | 18.401 | 8.605 | 6,83 | 68,1 | 15.364 |
| 2017 | 3.866.265 | 25.929 | 17.707 | 8.222 | 6,71 | 68,3 | 14.877 |
| 2018 | 3.802.569 | 25.324 | 17.326 | 7.998 | 6,66 | 68,4 | 14.501 |
| 2019 | 3.757.755 | 24.173 | 16.568 | 7.605 | 6,43 | 68,5 | 13.983 |
| 2020 | 3.623.630 | 23.261 | 16.151 | 7.110 | 6,42 | 69,4 | 13.601 |
| 2021 | 3.674.138 | 23.364 | 16.376 | 6.988 | 6,36 | 70,1 | 13.771 |
| 2022 | 3.677.156 | 22.780 | 15.632 | 7.148 | 6,20 | 68,6 | 13.657 |
| 2023 | 3.605.074 | 22.337 | 15.248 | 7.089 | 6,20 | 68,3 | 13.282 |

**Qué significa.** Hay 194.174 eventos en 29,96 millones de productos (6,5 por 1.000). Siete de cada diez eventos son muertes fetales. La tasa baja de forma suave con los años (de 6,83 a 6,20), lo que importa para la calibración en el tiempo (C4).

**Para el modelo.** El tamaño de muestra no es una restricción: la puerta P3 se pasará con holgura. Desarrollo con 2016–2021 (149.057 eventos) y prueba temporal con 2022–2023 (45.117 eventos).

### Q-C3. Momento de la muerte fetal (población, 2016–2023)

| Momento estimado | Muertes fetales | % |
|---|---|---|
| Antes del trabajo de parto (N) | 64.616 | 48,4 |
| Durante el trabajo de parto (L o A) | 17.704 | 13,3 |
| Desconocido (U) o sin dato | 51.089 | 38,3 |

**Qué significa.** Al menos la mitad de las muertes fetales ocurre antes del trabajo de parto. Confirma la decisión D2: un modelo al nacer o al ingreso no podría predecirlas.

**Para el modelo.** No es un predictor (describe el desenlace). Se usa para describir el componente fetal y como análisis de sensibilidad (solo muertes anteparto o solo intraparto).

### Puerta P1. Definición

Los conteos de productos y eventos de los 8 años reproducen exactamente los del adaptador de datos. El notebook se detiene si no coinciden. **P1: pasa.**

## 2. Predictores candidatos (toda la población)

### Q-C4. Variables categóricas (porcentaje de los 29,96 millones de productos)

| Variable | Distribución |
|---|---|
| Raza y origen hispano | Blanca no hispana 51,1; negra no hispana 14,3; hispana 24,2; asiática no hispana 6,2; más de una raza 2,3; indígena americana 0,7; isleña del Pacífico 0,3; desconocida 0,9 |
| Educación de la madre | Hasta 8.° grado 3,2; 9.° a 12.° sin diploma 8,9; bachiller 25,7; universidad sin título 19,0; técnico 8,3; profesional 20,9; maestría 9,8; doctorado 2,9; desconocida 1,5 |
| Nacida en EE. UU. | Sí 77,2; no 22,6; desconocido 0,2 |
| WIC | Sí 33,6; no 65,2; desconocido 1,2 |
| Fumó durante el embarazo | Sí 5,4; no 94,1; desconocido 0,5 |
| Diabetes previa | 1,0 |
| Diabetes gestacional | 7,3 |
| Hipertensión previa | 2,4 |
| Hipertensión gestacional | 8,0 |
| Eclampsia | 0,3 |
| Tratamiento de infertilidad | 2,1 |
| Cesárea anterior | 15,4 |
| Pluralidad | Único 96,7; gemelar 3,2; triple o más 0,1 |

### Q-C5. Variables numéricas

| Variable | % desconocido | P5 | P25 | Mediana | P75 | P95 |
|---|---|---|---|---|---|---|
| Edad de la madre | 0,0 | 20 | 25 | 29 | 33 | 39 |
| IMC antes del embarazo | 2,3 | 19,1 | 22,4 | 25,8 | 31,0 | 40,7 |
| Mes de inicio del control prenatal | 2,3 | 1 | 2 | 3 | 3 | 6 |
| Hijos nacidos vivos que viven | 0,2 | 0 | 0 | 1 | 2 | 4 |
| Hijos nacidos vivos ya fallecidos | 0,3 | 0 | 0 | 0 | 0 | 0 |
| Meses desde el último nacido vivo | 3,2 | 13 | 24 | 37 | 63 | 128 |
| Número de cesáreas anteriores | 0,2 | 0 | 0 | 0 | 0 | 1 |
| Cigarrillos al día antes del embarazo (agregado por D4) | 0,5 | 0 | 0 | 0 | 0 | 6 |

En "meses desde el último nacido vivo", el 38,1% no aplica porque es el primer hijo. Fumar antes del embarazo bajó de 9,4% de los productos en 2016 a 3,8% en 2023, un cambio que importa para la calibración en el tiempo (C4).

### Q-C6. Faltantes por año

En toda la población, cada variable tiene menos de 4% de desconocidos en todos los años, sin saltos entre 2016–2017 y 2018 en adelante. La implantación tardía del reporte fetal revisado en algunos estados no se nota en la población completa.

## 3. Verificaciones de fuga y de definición

### Q-C7. Los desconocidos dependen del tipo de certificado

| Variable | % desconocido en nacidos vivos | % desconocido en muertes fetales |
|---|---|---|
| WIC | 1,1 | 18,7 |
| Educación | 1,4 | 13,1 |
| IMC | 2,2 | 12,9 |
| Meses desde el último nacido vivo | 3,2 | 12,8 |
| Mes de inicio del control prenatal | 2,3 | 12,5 |
| Fumó durante el embarazo | 0,4 | 8,3 |
| Fumaba antes del embarazo | 0,4 | 8,3 |
| Número de cesáreas anteriores | 0,1 | 6,3 |
| Nacida en EE. UU. | 0,2 | 6,1 |
| Factores de riesgo (diabetes, hipertensión, eclampsia, infertilidad, cesárea) | 0,1 | 5,9 |
| Hijos ya fallecidos | 0,3 | 4,8 |
| Raza y origen hispano | 0,9 | 4,4 |
| Hijos que viven | 0,2 | 3,4 |
| Edad, pluralidad | 0,0 | 0,0 |

**Qué significa.** El reporte de muerte fetal se llena con mucha menos información que el certificado de nacimiento. Como todas las muertes fetales son eventos, "dato desconocido" está fuertemente asociado al desenlace por cómo se llena el formulario, no por la biología. Un modelo que use el desconocido como información aprendería a reconocer el tipo de formulario: es **fuga de información** (puerta P2).

### Q-C8. Edad gestacional del componente fetal

En las muertes fetales con las dos estimaciones, la estimación obstétrica (la usada) y la gestación combinada coinciden en la misma semana en el 62–64% y con una semana de diferencia en el 79–80%. Con la gestación combinada entrarían unas 800 a 900 muertes fetales más por año.

**Qué significa.** La edad gestacional de una muerte fetal es incierta (el feto puede morir días antes del parto). La población principal usa la estimación obstétrica, que es la que NCHS usa para tabular.

**Para el modelo.** Sensibilidad: población definida con la gestación combinada.

## 4. Decisiones que deja la auditoría (aprobadas el 21/11/2026, registradas en la ficha del desenlace)

**D3. Tratamiento de los desconocidos (por Q-C7).** Propuesta:
- El código "desconocido" se trata como faltante y **nunca** se usa como categoría ni con indicador de faltante.
- Los faltantes se imputan dentro del entrenamiento de cada partición, con un modelo de imputación que **no** use el tipo de certificado.
- Sensibilidad 1: solo productos con todos los predictores completos.
- Sensibilidad 2 (verificación de fuga): un modelo con solo el número de campos desconocidos por registro; si discrimina, se reporta como evidencia del sesgo del formulario.

**D4. Predictores que dependen de la duración del embarazo.** Con la opción A ya se excluyeron el número de controles y la ganancia de peso. La auditoría muestra otros con el mismo problema:
- **Diabetes gestacional:** el tamizaje se hace entre las semanas 24 y 28; un embarazo que termina en la semana 22–24 casi no puede tenerla registrada.
- **Hipertensión gestacional y eclampsia:** aparecen desde la semana 20 y son más probables cuanto más dura el embarazo.
- **Fumó durante el embarazo:** incluye el tercer trimestre, que un embarazo corto no tiene.
- **Mes de inicio del control prenatal:** un embarazo que termina en la semana 22 no puede empezar el control en el mes 6 o después.

Propuesta: excluir la diabetes gestacional, la hipertensión gestacional y la eclampsia; reemplazar "fumó durante el embarazo" por **"fumaba antes del embarazo"** (campo `CIG_0`, presente en los dos archivos; hay que agregarlo al adaptador); y usar el mes de inicio del control prenatal agrupado en "primer trimestre / después / sin control". Como sensibilidad, el modelo con todas las variables y la población de 28 semanas o más.

**D5. Edad gestacional del componente fetal.** Estimación obstétrica editada en la población principal; gestación combinada como sensibilidad (Q-C8).

## 5. Lista de predictores (con D3 y D4)

| Bloque | Predictores |
|---|---|
| Madre | Edad; raza y origen hispano (blanca, negra, hispana, asiática, otra); educación (hasta bachiller, técnica o universidad sin título, profesional o más); nacida fuera de EE. UU.; WIC |
| Historia obstétrica | Hijos que viven (0, 1, 2 o más); algún hijo ya fallecido; meses desde el último nacido vivo (primer hijo, menos de 18, 18 a 59, 60 o más); cesárea anterior |
| Embarazo actual | IMC antes del embarazo; fumaba antes del embarazo; inicio del control prenatal (primer trimestre, después, sin control); diabetes previa; hipertensión previa; tratamiento de infertilidad; pluralidad (único, múltiple) |

Unos 20 parámetros. Frente a unos 150.000 eventos de desarrollo, hay más de 20 eventos por parámetro: según la regla del framework, el modelo principal se elige en una corrida preliminar entre los modelos base.

*Confidencial: uso interno del proyecto de investigación.*
