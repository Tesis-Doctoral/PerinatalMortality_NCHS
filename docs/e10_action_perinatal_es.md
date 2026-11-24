# Etapa E10 — de la clasificación a la acción: mortalidad perinatal NCHS (M5)

Versión en inglés: [`e10_action_perinatal.md`](e10_action_perinatal.md). Fuentes: `data/outputs_09_model_v2b.txt` (versión 2b) y `data/outputs_10_p2_imputation_check.txt` (verificación de la puerta P2 sobre la imputación), cohortes de desarrollo 2016–2021: 22,7 millones de productos y 149.057 eventos (6,6 por 1.000).

## 1. Clase y uso

El modelo quedó como **señal insuficiente**: con la información prenatal que comparten el certificado de nacimiento y el reporte de muerte fetal, el AUROC limpio es 0,723, por debajo del umbral de 0,75. Su calibración es buena (pendiente temporal 0,98), pero discrimina poco.

**No se recomienda su uso para decisiones individuales** (a qué gestante intensificar el control prenatal). Con el mejor umbral posible, la sensibilidad y la especificidad no pasan de 0,66 a la vez: se marcaría como de alto riesgo a un tercio de los embarazos sin evento y aun así se perdería un tercio de los eventos.

Lo que sí deja el modelo son tres aportes para las entidades de salud: un hallazgo sobre la calidad de los datos, la descripción de los factores de riesgo prenatales y la especificación de qué información haría falta para predecir.

## 2. Hallazgo principal: la calidad del reporte de muerte fetal

- El 47% de los reportes de muerte fetal tiene al menos un dato prenatal desconocido, frente al 14% de los certificados de nacimiento.
- Esa diferencia hace que un modelo "aprenda" el tipo de formulario y no el riesgo: con imputación por la mediana el AUROC sube a 0,7455, y con indicadores de desconocido a 0,770, sin que haya más información clínica. En los registros completos, las cuatro estrategias dan lo mismo (0,689–0,691).
- La puerta P2 del framework lo detectó dos veces: con el modelo de verificación M6 (muerte fetal, 0,680 con la fuga controlada) y con la prueba de la imputación (0,7455 → 0,723).

**Recomendación:** mejorar el diligenciamiento del reporte de muerte fetal, en especial de los antecedentes y datos del control prenatal, con los mismos campos y la misma calidad que el certificado de nacimiento. Sin esa mejora, cualquier modelo de mortalidad perinatal construido con estadísticas vitales corre el riesgo de inflar su desempeño.

## 3. Factores de riesgo prenatales (descriptivo, en la población)

Aunque el modelo no sirva para predecir caso a caso, sí describe qué grupos concentran el riesgo: el 10% de mayor riesgo agrupa el 42% de los eventos (4,2 veces lo esperado por azar). Algunas asociaciones ajustadas (regresión logística, todos los productos):

| Factor | Razón de odds ajustada |
|---|---|
| Tabaquismo en el embarazo | 1,23 (1,25 desde las 28 semanas) |
| Eclampsia | 1,16 |
| Medicamentos de fertilidad / reproducción asistida | 1,07 / 1,06 |
| Producto masculino | 1,06 |
| Talla materna (por pulgada) | 0,93 |

Este tipo de resultado sirve para la **planeación poblacional** (dónde enfocar programas de cesación del tabaquismo, control prenatal de embarazos con tratamiento de fertilidad), no para clasificar a cada gestante.

## 4. Qué haría falta para llegar a predecir

1. **Datos clínicos prenatales que las estadísticas vitales no tienen:** ecografía (crecimiento fetal, restricción del crecimiento, Doppler), resultados de laboratorio, número y contenido de los controles prenatales, antecedentes obstétricos detallados.
2. **Registro igual para todos los desenlaces:** que la información de los embarazos que terminan en muerte fetal se recoja con la misma completitud que la de los nacidos vivos, preferiblemente desde la historia clínica prenatal y no desde el certificado posterior al evento.
3. **Otro punto de predicción:** al ingreso para el parto (opción B, declarada como retorno R3 y no usada porque el modelo ya había agotado sus dos retornos), con información del trabajo de parto. Sería un modelo distinto, con otra utilidad.

## 5. Limitaciones

- Estadísticas vitales de EE. UU.; no hay geografía en los archivos públicos.
- Las asociaciones son descriptivas, no causales.
- El AUROC limpio (0,723) se estimó con una sola repetición de validación cruzada de 5 particiones; la versión 2b con la mediana usó 3 repeticiones.
