# Tabla de predictores y puertas P2 y P3 — mortalidad perinatal (NCHS)

Ejecutada el 21/11/2026 con `notebooks/03_predictors_g2_g3_es.ipynb`. Salida completa: [`data/outputs_03_predictors_g2_g3.txt`](data/outputs_03_predictors_g2_g3.txt). Versión en inglés: [`predictor_table.md`](predictor_table.md).

**Etapas del framework:** E7 (predictores), P2 (fuga) y P3 (tamaño de muestra). La tabla contrato queda en `data/contract/perinatal_nchs_v1/` (un archivo por año, no se versiona).

## 1. La tabla contrato (E7)

29.963.276 productos de 22 semanas o más (2016–2023), una fila por producto, con 24 parámetros. Decisiones aplicadas: D3 (el código desconocido es faltante, sin categoría ni indicador) y D4 (sin variables que dependen de la duración del embarazo).

| Bloque | Parámetros | Referencia | % faltante |
|---|---|---|---|
| Edad de la madre (continua) | 1 | — | 0,00 |
| Raza y origen hispano: negra, hispana, asiática, otra | 4 | Blanca no hispana | 0,92 |
| Educación: técnica o universidad sin título; profesional o más | 2 | Bachiller o menos | 1,49 |
| Nacida fuera de EE. UU. | 1 | — | 0,23 |
| WIC | 1 | — | 1,19 |
| Hijos que viven: 1; 2 o más | 2 | Ninguno | 0,17 |
| Algún hijo nacido vivo ya fallecido | 1 | — | 0,28 |
| Meses desde el último nacido vivo: menos de 18; 18 a 59; 60 o más | 3 | Primer hijo | 4,50 |
| Cesárea anterior | 1 | — | 0,13 |
| IMC antes del embarazo (continuo) | 1 | — | 2,28 |
| Fumaba antes del embarazo | 1 | — | 0,48 |
| Control prenatal: inició después del primer trimestre; sin control | 2 | Primer trimestre | 2,31 |
| Diabetes previa; hipertensión previa; tratamiento de infertilidad | 3 | — | 0,13 |
| Embarazo múltiple | 1 | Único | 0,00 |
| **Total** | **24** | | |

En "meses desde el último nacido vivo", los códigos 000–003 (registro de un parto múltiple, no un intervalo) se tratan como faltantes; por eso su faltante (4,5%) supera al desconocido de la auditoría (3,2%).

## 2. Puerta P2: fuga

| Verificación | Resultado |
|---|---|
| Ningún predictor es del parto, del producto o del desenlace, ni una variable excluida por D4 | Cumple |
| Ningún indicador de faltante entre los predictores | Cumple |
| Unidad: el producto; el grupo es la propia unidad (los archivos no identifican a la madre) | Cumple |

**Prueba de fuga de la decisión D3.** El número de campos desconocidos de cada registro, **por sí solo**, separa los eventos con una **AUROC de 0,639** en los años de desarrollo. El 89,1% de los productos no tiene ningún desconocido.

**Qué significa.** La diferencia en cómo se llenan los dos formularios lleva información del desenlace: un modelo que usara los desconocidos como dato obtendría una AUROC cercana a 0,64 sin saber nada del embarazo. Por eso D3 prohíbe los indicadores de faltante. El modelo final se evaluará además con solo registros completos (sensibilidad de D3): si el desempeño cae mucho, una parte venía del formulario.

**P2: pasa**, con la sensibilidad de registros completos como control obligatorio en E9.

## 3. Puerta P3: tamaño de muestra

| Medida | Valor |
|---|---|
| Productos de desarrollo (2016–2021) | 22.681.046 |
| Eventos de desarrollo | 149.057 (prevalencia 0,657%) |
| Parámetros candidatos | 24 (6.211 eventos por parámetro) |
| R² de Cox-Snell observado (validación cruzada) | 0,0058 (7,6% del máximo de 0,0761) |
| Productos requeridos (criterio de encogimiento, el mayor) | 37.147 |
| Eventos requeridos | 245 |
| Parámetros que soportan los datos | 14.654 |

**Cómo se calculó.** Regresión logística con validación cruzada de 5 particiones sobre todos los eventos y el 3% de los no eventos, con pesos inversos a la probabilidad de muestreo para que la verosimilitud represente a todos los datos. La imputación (mediana) y el escalado se ajustan dentro de cada partición.

**P3: pasa** con amplio margen: los datos superan en más de 600 veces el tamaño requerido.

**Modelo principal (E8).** Con 6.211 eventos por parámetro, la regla del framework (20 o más) indica elegir el mejor modelo base en una corrida preliminar.

**Lectura del R².** Un R² de Cox-Snell del 7,6% de su máximo indica una señal moderada. Como referencia aproximada, a esta prevalencia corresponde a una discriminación del orden de 0,73 a 0,76 de AUROC, cerca del umbral de 0,75 del framework. Es coherente con la expectativa escrita en la ficha antes de los resultados (0,65 a 0,75). No es la AUROC del modelo: esa se estima en E8.

*Confidencial: uso interno del proyecto de investigación.*
