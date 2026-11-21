# Ficha del desenlace — mortalidad perinatal, NCHS

Ficha del desenlace según el framework por etapas ([`../framework_es.md`](../framework_es.md)), versión 1, 20/11/2026. Los campos marcados **pendiente** se fijan, y se registran en el libro de decisiones, antes de la puerta que los necesita. Versión en inglés: [`outcome_card_perinatal_nchs.md`](outcome_card_perinatal_nchs.md).

## 1. La pregunta

**¿Se puede identificar a los embarazos con riesgo alto de terminar en una muerte perinatal?**

La mortalidad perinatal comprende, según la OMS y la CIE-10, el período que va desde las 22 semanas completas de gestación hasta los 7 días completos después del nacimiento. Tiene dos componentes:

- **Fetal:** muerte fetal de 22 semanas o más (mortinato).
- **Neonatal precoz:** muerte de un nacido vivo entre el día 0 y el día 6.

## 2. Identidad

| Campo | Valor |
|---|---|
| Desenlace | Muerte perinatal: muerte fetal de 22 semanas o más, o muerte neonatal precoz (0 a 6 días) |
| Peldaño | Primer peldaño de la escalera de desenlaces |
| Fuente de datos | NCHS (CDC): archivos públicos *Linked Birth/Infant Death*, versión cohorte, para los nacidos vivos y su muerte neonatal precoz; archivo público de muertes fetales para el componente fetal (**pendiente**, decisión D1) |
| Unidad y grupo | Parto con producto de 22 semanas o más (nacido vivo o muerte fetal). Sin identificador de la madre: el grupo es la propia unidad |
| Población | Madres residentes en EE. UU., 22 semanas o más (`COMBGEST` 22–47 en nacidos vivos; el campo equivalente en el archivo fetal, **pendiente**) |
| Etiqueta principal | Muerte fetal de 22 semanas o más, o muerte entre el día 0 y el día 6 |
| Etiquetas de sensibilidad | Solo 28 semanas o más (definición de comparación internacional de la OMS); cada componente por separado |
| Conteos | **Pendiente** de la auditoría. Componente neonatal precoz ya disponible: unos 7.000 a 8.600 eventos por cohorte en nacidos vivos de 22 semanas o más |

## 3. Decisiones pendientes antes de la auditoría

**D1. Datos del componente fetal (resuelta el 21/11/2026).** Se usan los archivos públicos de muertes fetales de NCHS con causa de muerte (`Fetal<año>US_COD.zip`, 2016–2023), guardados en `../NCHS_data/raw/fetal/` con sus guías de usuario. Lo que mostró la revisión:

| Aspecto | Hallazgo |
|---|---|
| Registros | Una fila por muerte fetal: 39.574 a 51.391 por año; incluyen muertes de menos de 20 semanas que algunos estados reportan |
| Muertes fetales de 22 semanas o más, madres residentes en EE. UU. | 15.248 (2023) a 18.401 (2016) por año; de 28 semanas o más, 9.514 a 11.336 |
| Edad gestacional | Estimación obstétrica editada (`OEGest_Comb`, posiciones 340–341), la que NCHS usa para tabular; desconocida en 1.120 a 1.805 registros por año |
| Momento de la muerte (`ESTOFD`) | En las de 22 semanas o más: cerca del 50% antes del trabajo de parto, cerca del 15% durante el trabajo de parto y cerca del 38% desconocido; algunos estados no lo reportan |
| Certificado | El modelo revisado de 2003 se implantó por etapas y lo usan todos los estados desde 2018; en 2016 y 2017 algunos ítems revisados faltan en algunos estados |
| Diseño de registro | 3.052 caracteres por registro en 2016–2017 y 2.653 desde 2018; las posiciones de los campos prenatales son iguales en ambos diseños, pero distintas a las del archivo de nacimientos |
| Variables prenatales comunes con el archivo de nacimientos | Edad, raza y origen hispano, educación, nacida en EE. UU. o fuera, WIC, hijos vivos y muertos anteriores, intervalo desde el último nacido vivo, mes de inicio del control prenatal, tabaquismo, IMC antes del embarazo, diabetes e hipertensión previas y gestacionales, eclampsia, infertilidad, cesáreas anteriores, pluralidad |
| Variables que **no** trae el archivo fetal | Estado civil, fuente de pago, otras terminaciones anteriores, parto pretérmino anterior, infecciones, intervalo desde el último embarazo. No pueden entrar al modelo, porque faltarían en todo el componente fetal |

**Consecuencia:** la población perinatal se arma con el mismo año de parto: nacidos vivos de 22 semanas o más con su muerte de 0 a 6 días (archivos vinculados) más muertes fetales de 22 semanas o más (archivos fetales), una fila por producto. La edad gestacional del componente fetal sale de `OEGest_Comb`; la del componente de nacidos vivos, de `COMBGEST`. Su comparabilidad se revisa en la auditoría de conteos.

**D2. Punto de predicción.** Es la decisión central de este desenlace. La mayoría de las muertes fetales ocurre antes del trabajo de parto, así que **no se pueden predecir al nacer**: a esa hora ya ocurrieron. Las opciones son:

| Opción | Información permitida | Consecuencia con el framework |
|---|---|---|
| A. Prenatal | Solo lo que se sabe del embarazo antes del parto: características de la madre, historia obstétrica, controles prenatales, tabaquismo, factores de riesgo e infecciones | El evento ocurre después de la información (C1 y C2 se cumplen). Sin edad gestacional al parto, peso ni Apgar, la discriminación esperada es moderada |
| B. Al ingreso para el parto | Lo de la opción A más la edad gestacional al ingreso | Muchas muertes fetales ya ocurrieron al ingreso: para ese componente el modelo identifica, no predice (criterio C1), como en un identificador temprano |

**Decidido el 20/11/2026: opción A (prenatal)**, antes de cualquier conteo por desenlace. Es la única opción en la que todo el desenlace perinatal, incluido el componente fetal, ocurre después de la información. La opción B queda declarada desde ahora como posible retorno R3 (otro punto de predicción) si el modelo A queda clasificado como *ninguno*; en ese caso se reporta como identificador temprano para el componente fetal.

## 3b. Decisiones de la auditoría de conteos (21/11/2026)

Tomadas después de la auditoría ([`../count_audit_es.md`](../count_audit_es.md)) y antes de cualquier modelo:

| Decisión | Elección | Razón |
|---|---|---|
| D3. Desconocidos | El código "desconocido" se trata como faltante, nunca como categoría ni con indicador de faltante; imputación dentro del entrenamiento de cada partición, sin usar el tipo de certificado. Sensibilidades: solo registros completos; modelo con solo el número de campos desconocidos (verificación de fuga) | El reporte de muerte fetal tiene de 5 a 18 veces más desconocidos que el certificado de nacimiento (Q-C7): usarlos sería fuga |
| D4. Variables que dependen de la duración del embarazo | Se excluyen diabetes gestacional, hipertensión gestacional y eclampsia; "fumó durante el embarazo" se reemplaza por "fumaba antes del embarazo" (`CIG_0`); el inicio del control prenatal se agrupa en primer trimestre, después o sin control. Sensibilidad: todas las variables en la población de 28 semanas o más | Un embarazo corto tiene menos tiempo para que se diagnostiquen o registren; filtrarían la edad gestacional al parto |
| D5. Edad gestacional del componente fetal | Estimación obstétrica editada (`OEGest_Comb`); gestación combinada como sensibilidad | Es la que NCHS usa para tabular; las dos coinciden en la misma semana solo en el 62–64% (Q-C8) |

## 4. Predictores (E7)

La lista definitiva se fija con la auditoría de conteos. Con la opción A:

| Campo | Valor |
|---|---|
| Punto de predicción | Antes del parto: lo que se sabe del embarazo sin la información del parto ni del producto |
| Permitida | Características de la madre (edad, raza y origen hispano, educación, estado civil, nacida en EE. UU. o fuera, fuente de pago, WIC); historia obstétrica (hijos vivos y muertos anteriores, otras terminaciones, intervalo desde el último embarazo, cesáreas anteriores, parto pretérmino anterior); mes de inicio del control prenatal; tabaquismo; IMC antes del embarazo; diabetes e hipertensión previas y gestacionales, eclampsia; tratamiento de infertilidad; infecciones; pluralidad |
| Excluida por depender de la duración del embarazo | Número de controles prenatales y ganancia de peso: menos semanas implican menos controles y menos peso ganado, así que filtrarían la edad gestacional al parto |
| Excluida por ser del parto o del producto | Edad gestacional y peso al nacer, trabajo de parto y parto, presentación y vía, Apgar, sexo, anomalías congénitas, todo lo posterior al nacimiento |
| Pluralidad | Se permite: un embarazo múltiple suele conocerse en los controles prenatales |
| Expectativa, dicha antes de los resultados | Los modelos de muerte fetal con solo información del embarazo suelen alcanzar una AUROC de 0,65 a 0,75. El modelo puede quedar como *ninguno*; el umbral de 0,75 no se cambia |

## 5. Tamaño de muestra y modelo (P3, E8)

| Campo | Valor |
|---|---|
| Eventos | Del orden de miles por cohorte; la puerta P3 se verifica con los criterios de Riley et al. |
| Modelo principal | Se fija en E8 con la regla del framework según los eventos por parámetro |

## 6. Criterios de clasificación (P4)

| Criterio | Estado |
|---|---|
| C1, eventos ya presentes | Aplica: con la opción A el evento ocurre después de la información |
| C2, desenlace con tiempo | Aplica |
| C3, sesgo de detección | No aplica: el desenlace sale de los certificados, no de un examen |
| C4, estabilidad en el tiempo | Aplica: desarrollo con las cohortes 2016–2021 y prueba temporal con 2022–2023 |

## 7. Datos y condiciones de uso

- Los archivos de NCHS se guardan fuera del repositorio, en la carpeta compartida `../NCHS_data/raw/`; no se redistribuyen.
- Acuerdo de uso de datos de NCHS: solo análisis estadístico; no intentar identificar a ninguna persona; no unir con datos identificables. En los reportes no se muestran celdas con menos de 10 casos.

## 8. Próximas tareas

1. ~~D1: archivo de muertes fetales~~ (2016–2023 descargados y revisados, 21/11/2026).
2. ~~D2: punto de predicción~~ (opción A, prenatal, 20/11/2026).
3. Adaptador del componente fetal y unión con el componente neonatal precoz.
4. Auditoría de conteos; predictores; puerta P3; modelo y clasificación.

*Confidencial: uso interno del proyecto de investigación.*
