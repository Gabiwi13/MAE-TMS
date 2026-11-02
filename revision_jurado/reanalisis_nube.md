Hice los reanálisis con lo que está versionado y casi todo confirma el dictamen. Una cosa no estaba en él: en los raw de exp11, los seis trozos de una misma semilla no comparten los directorios del protocolo, aunque el código dice que sí (detalle en M1).

No toqué la tesis, no hice commit ni push y no creé ramas. El script quedó en la raíz, sin versionar, en `/home/user/MAE-TMS/reanalisis_jurado.py`. Lo corrí desde la raíz con un entorno aparte (numpy 2.5.4, pandas 3.1.0, scipy 1.18.1) y dos corridas dieron la misma salida.

---

## M1. Exp11: clase correcta sobre el total

**Denominador de la tesis.** En `run_experiment11_monolithic.py:597` la métrica se define como `("nn_ok", "nn_ok", "responde")`. La función `_rate` (líneas 578-582) se queda con las filas que tienen `responde` verdadero y descarta las que no traen `nn_ok`. Así que la tesis calcula la clase correcta sobre las consultas respondidas, promedia dentro de cada semilla y luego entre semillas.

**Tabla M1.1. Clase correcta por brazo y corte** (media de 10 semillas; cada una, 171 consultas × 3 réplicas)

| N | brazo | responde % | clase / respondidas % (tesis) | clase / total % | distancia al oráculo, total (pp) | distancia al oráculo, respondidas (pp) |
|---|---|---|---|---|---|---|
| 25 | EHAM única | 100.0 | 97.6 | 97.6 | 2.4 | 2.4 |
| 25 | Oráculo | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 |
| 25 | Protocolo | 98.4 | 96.9 | 95.3 | 4.7 | 3.1 |
| 50 | EHAM única | 100.0 | 97.5 | 97.5 | 2.5 | 2.5 |
| 50 | Oráculo | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 |
| 50 | Protocolo | 98.7 | 98.8 | 97.4 | 2.6 | 1.2 |
| 100 | EHAM única | 100.0 | 97.6 | 97.6 | 2.4 | 2.4 |
| 100 | Oráculo | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 |
| 100 | Protocolo | 98.7 | 98.8 | 97.4 | 2.6 | 1.2 |
| 200 | EHAM única | 100.0 | 96.9 | 96.9 | 3.1 | 3.1 |
| 200 | Oráculo | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 |
| 200 | Protocolo | 98.7 | 98.3 | 97.0 | 3.0 | 1.7 |

_Fuente: `results/experimento11/raw/s*_N*_c*.json`, campos `responde` y `nn_ok`._

**Tabla M1.2. Protocolo contra EHAM única, pareado por consulta**

| N | versión | consultas | Δ protocolo − EHAM (pp) | IC 95 % bootstrap por consulta | consultas P>M / P<M | p exacto (por consulta) | por sorteo: b mediana [mín, máx] | por sorteo: c mediana [mín, máx] | por sorteo: p mediana [mín, máx] | sorteos con p<0.05 |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | total | 171 | -2.28 | [-5.8, +1.1] | 7 / 16 | 0.0931 | 7 [4, 11] | 4 [3, 6] | 0.34 [0.118, 1.00] | 0/30 |
| 25 | respondidas | 170 | -0.706 | [-3.8, +2.4] | 7 / 12 | 0.359 | 5 [1, 8] | 4 [3, 6] | 0.74 [0.219, 1.00] | 0/30 |
| 50 | total | 171 | -0.078 | [-2.9, +2.7] | 9 / 7 | 0.804 | 4 [2, 6] | 4 [2, 7] | 1.00 [0.453, 1.00] | 0/30 |
| 50 | respondidas | 170 | 1.27 | [-1.0, +3.7] | 9 / 4 | 0.267 | 2 [1, 3] | 4 [2, 7] | 0.69 [0.180, 1.00] | 0/30 |
| 100 | total | 171 | -0.156 | [-3.0, +2.7] | 9 / 9 | 1 | 4 [3, 7] | 4 [2, 7] | 1.00 [0.180, 1.00] | 0/30 |
| 100 | respondidas | 170 | 1.2 | [-1.2, +3.7] | 9 / 5 | 0.424 | 2 [1, 4] | 4 [2, 7] | 0.69 [0.219, 1.00] | 0/30 |
| 200 | total | 171 | 0.0975 | [-2.9, +3.2] | 12 / 9 | 0.664 | 5 [3, 7] | 5 [3, 7] | 1.00 [0.344, 1.00] | 0/30 |
| 200 | respondidas | 170 | 1.39 | [-1.2, +4.2] | 12 / 5 | 0.143 | 3 [1, 4] | 5 [3, 7] | 0.71 [0.180, 1.00] | 0/30 |

_Fuente: `results/experimento11/raw/s*_N*_c*.json`._ Cómo se leen las columnas:
- **Por consulta:** cada consulta se resume en su tasa de acierto sobre los 30 sorteos (10 semillas × 3 réplicas), y se aplica McNemar exacto a las consultas cuya tasa difiere entre brazos.
- **Por sorteo:** un McNemar exacto por cada (semilla, réplica). La b cuenta las consultas que solo acierta la EHAM única y la c las que solo acierta el protocolo.
- **Respondidas:** solo los pares en que responden los dos brazos.

**Tabla M1.3. Variación entre semillas de la clase correcta sobre el total**

| N | brazo | media % | DE entre semillas (pp) | mín % | máx % | consultas con acierto distinto entre réplicas de una semilla (media) | consultas cuyo destino cambia entre semillas | … dentro de una semilla | consultas cuya respuesta (sí/no) cambia entre semillas |
|---|---|---|---|---|---|---|---|---|---|
| 25 | EHAM única | 97.60 | 0.34 | 97.27 | 98.25 | 2.10 | — | — | — |
| 25 | Oráculo | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 | — | — | — |
| 25 | Protocolo | 95.32 | 1.20 | 93.57 | 97.66 | 0.00 | 15 | 0 | 3 |
| 50 | EHAM única | 97.50 | 0.40 | 96.88 | 98.05 | 3.80 | — | — | — |
| 50 | Oráculo | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 | — | — | — |
| 50 | Protocolo | 97.43 | 0.56 | 96.49 | 98.25 | 0.00 | 7 | 0 | 2 |
| 100 | EHAM única | 97.58 | 0.36 | 97.08 | 98.05 | 2.90 | — | — | — |
| 100 | Oráculo | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 | — | — | — |
| 100 | Protocolo | 97.43 | 0.74 | 95.91 | 98.25 | 0.00 | 8 | 0 | 3 |
| 200 | EHAM única | 96.92 | 0.35 | 96.49 | 97.27 | 3.00 | — | — | — |
| 200 | Oráculo | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 | — | — | — |
| 200 | Protocolo | 97.02 | 0.64 | 95.91 | 97.66 | 0.00 | 10 | 0 | 3 |

_Fuente: `results/experimento11/raw/s*_N*_c*.json`._

**Tabla M1.4. Formación de directorios (protocolo) entre semillas**

| N | semillas | registradas mín | registradas máx | rechazadas mín | rechazadas máx | acierto temprano mín | acierto temprano máx |
|---|---|---|---|---|---|---|---|
| 25 | 10 | 233 | 233 | 7 | 7 | 0.8412 | 0.8412 |
| 50 | 10 | 233 | 233 | 7 | 7 | 0.8841 | 0.8841 |
| 100 | 10 | 233 | 233 | 7 | 7 | 0.8841 | 0.8841 |
| 200 | 10 | 233 | 233 | 7 | 7 | 0.8755 | 0.8755 |

_Fuente: `meta.formacion_texto` de `results/experimento11/raw/s*_N*_c*.json`._

**Tabla M1.5. Tamaño del círculo de la entrada por trozo, donde alguna vez es menor que 8**

| corte | semilla | entrada | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|---|
| 25 | 42 | cup | 7 | 7 | 7 | 7 | 7 | 7 |
| 25 | 43 | car | 7 | 7 | 7 | 7 | 8 | 7 |
| 25 | 43 | cow | 7 | 7 | 7 | 7 | 8 | 7 |
| 25 | 43 | cup | 7 | 7 | 7 | 7 | 7 | 7 |
| 50 | 43 | car | 7 | 7 | 7 | 7 | 8 | 8 |
| 50 | 43 | cow | 7 | 7 | 7 | 7 | 8 | 8 |
| 100 | 43 | car | 7 | 7 | 7 | 7 | 8 | 7 |
| 100 | 43 | cow | 7 | 7 | 7 | 7 | 8 | 7 |
| 200 | 43 | car | 7 | 7 | 7 | 7 | 7 | 7 |
| 200 | 43 | cow | 7 | 7 | 7 | 7 | 7 | 7 |

_Fuente: campos `consultados`, `entrada` y `saltos` de `results/experimento11/raw/s*_N*_c*.json`._ Dos datos para leerla:
- `saltos` vale 0 en todas las filas, así que `consultados` es el tamaño del círculo de la entrada.
- Dentro de un trozo, ese tamaño es constante para cada entrada. Hay 6 combinaciones (corte, semilla, entrada) en que cambia de un trozo a otro de la misma semilla.

**Lectura.**
- **Se confirma el dictamen.** Sobre las 171 consultas, el protocolo y la EHAM única empatan: con N=200 la diferencia es +0.1 [−2.9, +3.2], y ningún corte es significativo (ni por consulta ni en ninguno de los 30 sorteos). Incluso sobre las respondidas, la prueba pareada no separa a los brazos (p entre 0.14 y 0.42). Los intervalos que no se solapan en la tesis vienen del bootstrap de 10 medias por semilla, que no cuenta la variación entre consultas.
- **Qué varía entre semillas.** Aquí corrijo en parte al jurado: en el protocolo no varía el muestreo del recuerdo, porque su acierto nunca cambia entre réplicas de una semilla. Su variación (DE de 0.56 a 1.20 pp) sale de 7 a 15 consultas que cambian de destino con el módulo de entrada. En la EHAM única la DE (0.34 a 0.40 pp) sí sale solo del recuerdo.
- **Hallazgo nuevo.** `run_job` forma los directorios (línea 389) sobre especialistas que cada proceso carga una sola vez (líneas 352-356) y no los reinicia entre trabajos. La tabla M1.5 muestra que los trozos de la semilla 43 no tienen los mismos directorios. Con los raw no se distingue si el estado se arrastró de un trabajo a otro o si esos trozos salen de otra corrida.
- **Qué cambiar en la tesis.**
  - Reportar las dos versiones de la clase correcta junto con la cobertura, y agregar McNemar.
  - Quitar «clasifica algo mejor» y «desde 50 los intervalos se separan».
  - Describir lo que varía entre semillas como la entrada y el recuerdo, no como la formación.
  - Reiniciar los directorios en cada trabajo y volver a correr el brazo del protocolo antes de dar intervalos por semilla. No lo corrí.

## M2. Calibración

**Tabla M2.1. Temprana y madura sobre las mismas consultas** (media de 5 semillas). En el CSV, la temprana de las 180 filas cuadra exactamente con el tamaño del conjunto evaluado que reconstruí.

| cond. | N | consultas evaluadas | temprana % | madura % | madura − temprana (pp) | DE temprana (pp) | DE madura (pp) |
|---|---|---|---|---|---|---|---|
| A | 50 | 50 | 78.00 | 66.00 | -12.00 | 0.00 | 0.00 |
| A | 100 | 100 | 83.00 | 70.00 | -13.00 | 0.00 | 0.00 |
| A | 200 | 200 | 82.50 | 69.50 | -13.00 | 0.00 | 0.00 |
| A | 400 | 400 | 90.00 | 85.25 | -4.75 | 0.00 | 0.00 |
| B1 | 50 | 50 | 78.00 | 78.00 | 0.00 | 0.00 | 0.00 |
| B1 | 100 | 100 | 83.00 | 87.00 | 4.00 | 0.00 | 0.00 |
| B1 | 200 | 200 | 82.50 | 88.00 | 5.50 | 0.00 | 0.00 |
| B1 | 400 | 400 | 90.00 | 93.00 | 3.00 | 0.00 | 0.00 |
| B2 | 50 | 50 | 78.00 | 76.00 | -2.00 | 0.00 | 0.00 |
| B2 | 100 | 100 | 83.00 | 82.00 | -1.00 | 0.00 | 0.00 |
| B2 | 200 | 200 | 82.50 | 82.00 | -0.50 | 0.00 | 0.00 |
| B2 | 400 | 400 | 90.00 | 91.75 | 1.75 | 0.00 | 0.00 |
| C | 50 | 50 | 78.00 | 74.00 | -4.00 | 0.00 | 0.00 |
| C | 100 | 100 | 83.00 | 77.00 | -6.00 | 0.00 | 0.00 |
| C | 200 | 200 | 82.50 | 74.50 | -8.00 | 0.00 | 0.00 |
| C | 400 | 400 | 90.00 | 88.00 | -2.00 | 0.00 | 0.00 |
| D | 50 | 48 | 91.25 | 90.00 | -1.25 | 4.75 | 5.39 |
| D | 100 | 96 | 88.75 | 86.46 | -2.29 | 3.24 | 3.83 |
| D | 200 | 200 | 90.50 | 89.20 | -1.30 | 1.80 | 3.03 |
| D | 400 | 399 | 90.48 | 87.32 | -3.16 | 0.36 | 1.76 |
| E32 | 50 | 50 | 78.00 | 68.00 | -10.00 | 0.00 | 0.00 |
| E32 | 100 | 100 | 83.00 | 70.00 | -13.00 | 0.00 | 0.00 |
| E32 | 200 | 200 | 82.50 | 72.00 | -10.50 | 0.00 | 0.00 |
| E32 | 400 | 400 | 90.00 | 88.50 | -1.50 | 0.00 | 0.00 |
| E64 | 50 | 50 | 78.00 | 68.00 | -10.00 | 0.00 | 0.00 |
| E64 | 100 | 100 | 83.00 | 71.00 | -12.00 | 0.00 | 0.00 |
| E64 | 200 | 200 | 82.50 | 73.50 | -9.00 | 0.00 | 0.00 |
| E64 | 400 | 400 | 90.00 | 89.75 | -0.25 | 0.00 | 0.00 |
| F | 50 | 50 | 78.00 | 66.00 | -12.00 | 0.00 | 0.00 |
| F | 100 | 100 | 83.00 | 70.00 | -13.00 | 0.00 | 0.00 |
| F | 200 | 200 | 82.50 | 69.50 | -13.00 | 0.00 | 0.00 |
| F | 400 | 400 | 90.00 | 85.25 | -4.75 | 0.00 | 0.00 |
| G | 50 | 48 | 91.25 | 91.67 | 0.42 | 4.75 | 4.17 |
| G | 100 | 96 | 88.75 | 90.00 | 1.25 | 3.24 | 3.73 |
| G | 200 | 200 | 90.50 | 93.20 | 2.70 | 1.80 | 0.57 |
| G | 400 | 399 | 90.48 | 93.53 | 3.05 | 0.36 | 0.33 |

_Fuente: `results/ablation_mdir_bias/ablation_metrics.csv`, columnas `early_accuracy` y `mature_accuracy`. Las dos fases se miden sobre la misma lista (`run_ablation.py:446-458`)._

**Tabla M2.2. Variación entre las 5 semillas** (máximo sobre los 4 N)

| cond. | DE máx. de la madura (pp) | DE máx. de la temprana (pp) | columnas del CSV que varían entre semillas | de |
|---|---|---|---|---|
| A | 0.00 | 0.00 | 0 | 108 |
| B1 | 0.00 | 0.00 | 0 | 108 |
| B2 | 0.00 | 0.00 | 0 | 108 |
| C | 0.00 | 0.00 | 0 | 108 |
| D | 5.39 | 4.75 | 54 | 108 |
| E32 | 0.00 | 0.00 | 0 | 108 |
| E64 | 0.00 | 0.00 | 0 | 108 |
| F | 0.00 | 0.00 | 0 | 108 |
| G | 4.17 | 4.75 | 53 | 108 |

_Fuente: el mismo CSV._
- En 7 de 9 condiciones las 108 columnas son idénticas en las cinco semillas.
- La semilla solo entra en el sorteo de D y G (`run_ablation.py:244`) y en el módulo de entrada de la fase madura (línea 325). Como cada transacción se registra en los ocho directorios (líneas 312-313), la entrada no cambia nada.
- F es idéntica a A en las 108 columnas. G y D comparten la fase temprana y los registros del directorio.

**Tabla M2.3. Precisión temprana por tramos del banco** (condiciones A, B1, B2, C, E32, E64 y F)

| tramo del banco | consultas | aciertos tempranos | temprana del tramo % | con nombre de la clase % | con palabra exclusiva % |
|---|---|---|---|---|---|
| 1–50 | 50 | 39/50 | 78.0 | 10.0 | 76.0 |
| 51–100 | 50 | 44/50 | 88.0 | 20.0 | 82.0 |
| 101–200 | 100 | 82/100 | 82.0 | 15.0 | 78.0 |
| 201–400 | 200 | 195/200 | 97.5 | 84.5 | 99.5 |

_Fuente: `early_accuracy × N` del CSV; composición con `src/eval_bank.py` y `labels_<clase>.json`. Restar los aciertos de cortes consecutivos es válido porque el ganador temprano lo decide M_dom, que es el mismo para todo N._

**Tabla M2.4. Composición de las primeras N consultas**

| conjunto | n | nombre de la clase (exacto) | nombre (con plural) | palabra del vocabulario (exacto) | vocabulario (con plural) | palabra exclusiva (exacto) | exclusiva (con plural) |
|---|---|---|---|---|---|---|---|
| primeras 50 | 50 | 5 (10.0 %) | 5 (10.0 %) | 47 (94.0 %) | 47 (94.0 %) | 38 (76.0 %) | 38 (76.0 %) |
| primeras 100 | 100 | 15 (15.0 %) | 15 (15.0 %) | 94 (94.0 %) | 94 (94.0 %) | 79 (79.0 %) | 79 (79.0 %) |
| primeras 200 | 200 | 30 (15.0 %) | 30 (15.0 %) | 191 (95.5 %) | 191 (95.5 %) | 155 (77.5 %) | 157 (78.5 %) |
| primeras 400 | 400 | 194 (48.5 %) | 199 (49.8 %) | 388 (97.0 %) | 391 (97.8 %) | 351 (87.8 %) | 356 (89.0 %) |
| banco completo | 411 | 203 (49.4 %) | 208 (50.6 %) | 399 (97.1 %) | 402 (97.8 %) | 362 (88.1 %) | 367 (89.3 %) |

_Fuente: `src/eval_bank.py`; `labels_<clase>.json`._

**Tabla M2.5. Sorteo balanceado de D y G** (5 semillas; reproduje `run_ablation.balanced_queries`)

| N | consultas | con nombre de la clase, media % | mín % | máx % |
|---|---|---|---|---|
| 50 | 48 | 51.7 | 41.7 | 64.6 |
| 100 | 96 | 50.0 | 44.8 | 61.5 |
| 200 | 200 | 50.1 | 48.0 | 55.0 |
| 400 | 399 | 50.7 | 49.6 | 51.4 |

**Lectura.**
- **Se confirma todo.** La temprana sube de 82.5 a 90.0 % porque las consultas 201–400 dan 195/200 (97.5 %) y el 84.5 % trae el nombre de la clase. En las primeras 200 ese nombre aparece en el 15 %.
- **El directorio aporta poco y no crece con N.** Medida sobre las mismas consultas, la diferencia madura menos temprana de B1 es 0, +4.0, +5.5 y +3.0 puntos. El ascenso de la madura con N (78 → 93 %) es sobre todo el de la temprana (78 → 90 %), es decir, la composición del banco.
- **D y G** sortean de un banco donde ~50 % trae el nombre de la clase.
- **Qué cambiar en la tesis.**
  - Reportar la diferencia madura menos temprana.
  - Retirar «hace falta el banco completo».
  - Reinterpretar D y G como consultas más fáciles.
  - Decir que en 7 condiciones las semillas no replican nada.

## M3. Composición de las particiones

Tomé las 171 reservadas de los raw de exp11 y son exactamente la cola de cada lista de clase: 30 de formación por clase.

**Tabla M3.1. Consultas con el nombre de su clase o con palabras de su vocabulario**

| conjunto | n | nombre de la clase (exacto) | nombre (con plural) | palabra del vocabulario (exacto) | vocabulario (con plural) | palabra exclusiva (exacto) | exclusiva (con plural) |
|---|---|---|---|---|---|---|---|
| banco completo | 411 | 203 (49.4 %) | 208 (50.6 %) | 399 (97.1 %) | 402 (97.8 %) | 362 (88.1 %) | 367 (89.3 %) |
| las 400 (ablación, N=400) | 400 | 194 (48.5 %) | 199 (49.8 %) | 388 (97.0 %) | 391 (97.8 %) | 351 (87.8 %) | 356 (89.0 %) |
| las 80 (exp2, exp4-6: ALL_QUERIES[:80]) | 80 | 11 (13.8 %) | 11 (13.8 %) | 75 (93.8 %) | 75 (93.8 %) | 63 (78.8 %) | 63 (78.8 %) |
| formación de exp11 (240) | 240 | 58 (24.2 %) | 58 (24.2 %) | 231 (96.2 %) | 231 (96.2 %) | 195 (81.2 %) | 197 (82.1 %) |
| reservadas de exp11 (171) | 171 | 145 (84.8 %) | 150 (87.7 %) | 168 (98.2 %) | 171 (100.0 %) | 167 (97.7 %) | 170 (99.4 %) |

_Fuente: `src/eval_bank.py`, `labels_<clase>.json` y los raw de exp11._ Cómo cuento:
- Los tokens son secuencias de letras en minúsculas.
- «Con plural» acepta además ±s o ±es.
- El sistema real tokeniza con spaCy (`src/stage6_interaction.py:88`), que no está en el entorno. Mi regla es una aproximación declarada.

**Tabla M3.2. Vocabulario por clase**

| clase | palabras | exclusivas | ¿el nombre está en su vocabulario? |
|---|---|---|---|
| apple | 21 | 18 | sí |
| car | 21 | 21 | sí |
| cow | 21 | 19 | sí |
| cup | 21 | 20 | sí |
| dog | 21 | 18 | sí |
| horse | 21 | 19 | sí |
| pear | 21 | 19 | sí |
| tomato | 21 | 19 | sí |

_Fuente: `labels_<clase>.json`._

**Lectura.**
- **Se confirman las cifras del jurado:** 208 de 411 consultas traen el nombre de su clase y 150 de 171 reservadas. Además, 399 tienen una palabra del vocabulario de su clase y 362 una exclusiva.
- Las reservadas traen el nombre en el 87.7 %, contra el 24.2 % de las de formación y el 13.8 % de las 80. Eso explica que el 97.0 % fuera de muestra supere al 93.0 % dentro de muestra.
- **Qué cambiar en la tesis:** declarar en 04 que se reserva la cola de cada lista y rehacer la partición con un sorteo estratificado. No calculé la línea base léxica porque no estaba en el encargo.

## M6 (Wegner). Información mutua del directorio

`mdir_entropy` es exactamente la entropía de los conteos `mdir_reg_<clase>`, con diferencia de 0.0000 bits.

**Tabla M6.1. H_dir frente a I(dominio; ganador)** (bits; media de 5 semillas)

| cond. | N | n (sin rechazos) | H_dir (mdir_entropy) | H(ganador) | I(dominio; ganador) | H(ganador dado el dominio) | IM normalizada = I / H(dominio) | sesgo esperado de I bajo independencia |
|---|---|---|---|---|---|---|---|---|
| A | 50 | 47.0 | 2.832 | 2.501 | 2.198 | 0.304 | 0.734 | 0.645 |
| A | 100 | 99.0 | 2.916 | 2.566 | 2.176 | 0.390 | 0.726 | 0.357 |
| A | 200 | 200.0 | 2.923 | 2.578 | 2.109 | 0.469 | 0.703 | 0.151 |
| A | 400 | 400.0 | 2.974 | 2.906 | 2.438 | 0.467 | 0.813 | 0.088 |
| B1 | 50 | 47.0 | 2.832 | 2.845 | 2.458 | 0.386 | 0.822 | 0.752 |
| B1 | 100 | 99.0 | 2.916 | 2.960 | 2.497 | 0.462 | 0.833 | 0.357 |
| B1 | 200 | 200.0 | 2.923 | 2.980 | 2.495 | 0.484 | 0.832 | 0.177 |
| B1 | 400 | 400.0 | 2.974 | 2.991 | 2.649 | 0.342 | 0.883 | 0.088 |
| B2 | 50 | 47.0 | 2.832 | 2.779 | 2.427 | 0.352 | 0.811 | 0.752 |
| B2 | 100 | 99.0 | 2.916 | 2.905 | 2.358 | 0.547 | 0.787 | 0.357 |
| B2 | 200 | 200.0 | 2.923 | 2.850 | 2.377 | 0.474 | 0.792 | 0.177 |
| B2 | 400 | 400.0 | 2.974 | 2.969 | 2.634 | 0.335 | 0.878 | 0.088 |
| C | 50 | 47.0 | 2.921 | 2.696 | 2.344 | 0.352 | 0.783 | 0.645 |
| C | 100 | 99.0 | 2.953 | 2.817 | 2.275 | 0.542 | 0.759 | 0.357 |
| C | 200 | 200.0 | 2.939 | 2.683 | 2.256 | 0.427 | 0.752 | 0.177 |
| C | 400 | 400.0 | 2.979 | 2.938 | 2.527 | 0.411 | 0.842 | 0.088 |
| D | 50 | 48.0 | 2.952 | 2.925 | 2.654 | 0.271 | 0.885 | 0.736 |
| D | 100 | 95.6 | 2.957 | 2.928 | 2.502 | 0.426 | 0.834 | 0.370 |
| D | 200 | 199.8 | 2.972 | 2.939 | 2.571 | 0.368 | 0.857 | 0.177 |
| D | 400 | 399.0 | 2.977 | 2.934 | 2.495 | 0.439 | 0.832 | 0.089 |
| E32 | 50 | 47.0 | 2.832 | 2.529 | 2.225 | 0.304 | 0.744 | 0.645 |
| E32 | 100 | 99.0 | 2.916 | 2.566 | 2.176 | 0.390 | 0.726 | 0.357 |
| E32 | 200 | 200.0 | 2.923 | 2.622 | 2.164 | 0.457 | 0.721 | 0.151 |
| E32 | 400 | 400.0 | 2.974 | 2.945 | 2.527 | 0.418 | 0.842 | 0.088 |
| E64 | 50 | 47.0 | 2.832 | 2.529 | 2.225 | 0.304 | 0.744 | 0.645 |
| E64 | 100 | 99.0 | 2.916 | 2.610 | 2.191 | 0.418 | 0.731 | 0.357 |
| E64 | 200 | 200.0 | 2.923 | 2.637 | 2.212 | 0.424 | 0.737 | 0.151 |
| E64 | 400 | 400.0 | 2.974 | 2.955 | 2.580 | 0.374 | 0.860 | 0.088 |
| F | 50 | 47.0 | 2.832 | 2.501 | 2.198 | 0.304 | 0.734 | 0.645 |
| F | 100 | 99.0 | 2.916 | 2.566 | 2.176 | 0.390 | 0.726 | 0.357 |
| F | 200 | 200.0 | 2.923 | 2.578 | 2.109 | 0.469 | 0.703 | 0.151 |
| F | 400 | 400.0 | 2.974 | 2.906 | 2.438 | 0.467 | 0.813 | 0.088 |
| G | 50 | 48.0 | 2.952 | 2.970 | 2.681 | 0.289 | 0.894 | 0.736 |
| G | 100 | 95.6 | 2.957 | 2.975 | 2.595 | 0.380 | 0.865 | 0.370 |
| G | 200 | 199.8 | 2.972 | 2.986 | 2.676 | 0.310 | 0.892 | 0.177 |
| G | 400 | 399.0 | 2.977 | 2.993 | 2.668 | 0.325 | 0.889 | 0.089 |

_Fuente: columnas `cm_<verdad>_<ganador>` (fase madura) y `mdir_entropy` del CSV._ Para leerla:
- El estimador es plug-in y H(dominio) va de 2.992 a 3.000 bits.
- El sesgo bajo independencia es (filas−1)(columnas−1)/(2 n ln 2).
- La matriz excluye los rechazos y es dentro de muestra.
- La fase temprana no tiene matriz en el CSV.

**Lectura.**
- **Se confirma M6.** H_dir es idéntica en A, B1, B2, E32, E64 y F para cada N, porque solo cuenta registros de la fase temprana. En cambio, I(dominio; ganador) va de 2.11 a 2.68 bits.
- Por ejemplo, con N=400, A y B1 comparten 2.974 bits de H_dir, pero su I es 2.438 frente a 2.649 (normalizada, 0.81 frente a 0.88). Los 186 frente a 112 registros siguen dando 2.974 bits.
- **Qué cambiar en la tesis:** reportar la I normalizada, con la advertencia de sesgo (0.65 a 0.75 bits con N=50) y la de que es dentro de muestra. Dejar H_dir solo como balance de registros.

## M5. Fuera de dominio

**Tabla M5.1. Aceptación de las 40 consultas fuera de dominio**

| N | semillas con la misma tabla | EHAM acepta | protocolo (doble compuerta) acepta | ambos | solo EHAM | solo protocolo | p McNemar exacto (doble compuerta) | protocolo sin 2.ª compuerta acepta | p McNemar exacto (sin 2.ª compuerta) |
|---|---|---|---|---|---|---|---|---|---|
| 25 | 10/10 | 2 | 2 | 2 | 0 | 0 | 1.000 | 4 | 0.500 |
| 50 | 10/10 | 2 | 2 | 2 | 0 | 0 | 1.000 | 4 | 0.500 |
| 100 | 10/10 | 5 | 2 | 2 | 3 | 0 | 0.250 | 4 | 1.000 |
| 200 | 10/10 | 8 | 2 | 2 | 6 | 0 | 0.031 | 4 | 0.219 |

_Fuente: `results/experimento11/raw/s*_N*_o0.json`, campos `acepta` y `acepta_compuerta`._ Con N=200, el protocolo con doble compuerta acepta «a kitchen appliance that heats food» y «a wooden table and chairs».

**Lectura.**
- **Se confirma el p ≈ 0.03 del jurado, pero solo con N=200** (6 contra 0 pares discordantes). Con N=100 da p = 0.25, y con 25 y 50, p = 1.
- **La significancia depende de la segunda compuerta, que se agregó después de ver estas 40 consultas.** Sin ella, el protocolo acepta 4 y el p con N=200 es 0.22.
- **Qué cambiar en la tesis:** dar el p por corte, declarar que la compuerta se decidió después de ver los datos y no generalizar el rechazo hasta confirmarlo con un banco nuevo.

## Menores

**Tabla E.1. Niveles de azar de la evocación top-3** (unión de vocabularios: 159 palabras)

| clase | vocabulario | exclusivas | azar laxo (3 de la unión) % | azar estricto (3 de la unión) % | azar estricto dado el módulo correcto (3 de su vocabulario) % |
|---|---|---|---|---|---|
| apple | 21.0 | 18.0 | 34.8 | 30.4 | 99.9 |
| car | 21.0 | 21.0 | 34.8 | 34.8 | 100.0 |
| cow | 21.0 | 19.0 | 34.8 | 31.9 | 100.0 |
| cup | 21.0 | 20.0 | 34.8 | 33.4 | 100.0 |
| dog | 21.0 | 18.0 | 34.8 | 30.4 | 99.9 |
| horse | 21.0 | 19.0 | 34.8 | 31.9 | 100.0 |
| pear | 21.0 | 19.0 | 34.8 | 31.9 | 100.0 |
| tomato | 21.0 | 19.0 | 34.8 | 31.9 | 100.0 |
| media | 21.0 | 19.1 | 34.8 | 32.1 | 100.0 |

_Fuente: `label_vectors_<clase>.json`, que tiene las mismas claves que `labels_<clase>.json`._

**Tabla E.2. Evocación imagen → palabras en exp11**

| N | brazo | imágenes por semilla | responde % | laxo / total % | estricto / total % | laxo / respondidas % | estricto / respondidas % | laxo / respondidas con ruteo correcto % |
|---|---|---|---|---|---|---|---|---|
| 25 | EHAM única | 80 | 78.7 | 78.0 | 76.4 | 99.0 | 97.0 | — |
| 25 | Oráculo | 80 | 43.8 | 43.8 | 43.8 | 100.0 | 100.0 | — |
| 25 | Protocolo | 80 | 41.2 | 41.2 | 41.1 | 100.0 | 99.7 | 100.0 |
| 50 | EHAM única | 80 | 95.0 | 93.9 | 92.0 | 98.8 | 96.8 | — |
| 50 | Oráculo | 80 | 75.0 | 75.0 | 74.1 | 100.0 | 98.8 | — |
| 50 | Protocolo | 80 | 67.5 | 67.5 | 67.4 | 100.0 | 99.8 | 100.0 |
| 100 | EHAM única | 80 | 98.8 | 96.7 | 93.6 | 98.0 | 94.8 | — |
| 100 | Oráculo | 80 | 92.5 | 92.5 | 91.1 | 100.0 | 98.5 | — |
| 100 | Protocolo | 80 | 78.7 | 78.7 | 77.5 | 100.0 | 98.4 | 100.0 |
| 200 | EHAM única | 80 | 100.0 | 97.5 | 93.6 | 97.5 | 93.6 | — |
| 200 | Oráculo | 80 | 97.5 | 97.5 | 95.7 | 100.0 | 98.2 | — |
| 200 | Protocolo | 80 | 81.2 | 81.2 | 79.8 | 100.0 | 98.2 | 100.0 |

_Fuente: `results/experimento11/raw/s*_N*_i*.json`._

**Dato que falta.** El 113/116 de la tesis está en `results/hemisferio_visual/stage7_bidirectional.log`, pero el log solo imprime 24 evocaciones (3 por clase): laxo 23/24 y estricto 23/24. La versión estricta sobre las 116 no se puede calcular con lo versionado, y no la estimé.

**Lectura (evocación).**
- **Se confirma que la métrica casi queda implicada por el enrutamiento.** En exp11, entre las respuestas con ruteo correcto, la laxa da 100 % y la estricta, de 98 a 100 %, frente a un azar de 34.8 % (laxa) y 32.1 % (estricta).
- **Qué cambiar en la tesis:** reportar la versión estricta y el nivel de azar, y presentar la evocación como algo condicionado al enrutamiento, no como una medida independiente. La estricta sobre las 116 pide volver a correr la etapa 7 y guardar las etiquetas evocadas por imagen.

**Tabla X.1. Fuga de exp14 (memoria oficial)**

| estadístico | banco | aceptadas por la memoria | siguen aceptadas tras τ | de ellas, con soporte de una clase ajena | solo de su propia clase | aceptadas por clase ajena | ajenas que τ rechaza |
|---|---|---|---|---|---|---|---|
| norma | 231 | 180 | 33 | 15 | 18 | 152 | 137 |
| desv_latente | 231 | 180 | 31 | 13 | 18 | 152 | 139 |
| desv_pixeles | 231 | 180 | 92 | 72 | 20 | 152 | 80 |
| niveles | 231 | 180 | 180 | 152 | 28 | 152 | 0 |

**Tabla X.2. Por familia (norma)**

| familia | n | aceptadas | aceptadas tras τ |
|---|---|---|---|
| gris | 33 | 10 | 1 |
| color | 12 | 2 | 2 |
| desenfoque | 128 | 121 | 16 |
| contraste | 48 | 41 | 13 |
| gris con ruido | 6 | 4 | 1 |
| estructura | 4 | 2 | 0 |

_Fuente: `results/experimento14/banco_degenerado.json`._

**Lectura (exp14).**
- **Se confirma el 33.** De las 231 entradas degeneradas, 33 siguen aceptadas después de τ: 15 con soporte de una clase ajena y 18 solo de la suya. Reproduzco también el 137 de 152 de 06:254.
- **Qué cambiar en la tesis:** junto a «cierra el 90 %», agregar el total: 33 de 231 entradas (33 de las 180 aceptadas) siguen pasando.

---

## Script completo (`reanalisis_jurado.py`, en la raíz del repositorio)

```python
"""
Reanálisis pedidos por el jurado (revision_jurado/jurado_metodologia.md, M1, M2,
M3, M5 y menores; revision_jurado/jurado_wegner.md, M6) usando solo lo
versionado: results/, src/eval_bank.py, labels_<clase>.json,
label_vectors_<clase>.json y el código de los run_*.py como referencia.

No corre ningún modelo ni necesita los datos de imagen. No escribe nada en el
repositorio: imprime las tablas en Markdown por la salida estándar.

Uso (desde la raíz del repositorio):
    python reanalisis_jurado.py > reanalisis_jurado_salida.md
Dependencias: numpy, pandas, scipy.

Convenciones:
  - «Total»: denominador = todas las consultas evaluadas; la no respuesta cuenta
    como fallo. «Respondidas»: denominador = filas con responde=True (lo que hace
    run_experiment11_monolithic.py:597 a través de _rate, línea 578-582).
  - Pruebas exactas: McNemar exacto = binomial bilateral sobre los pares
    discordantes (scipy.stats.binomtest).
  - Bootstrap: remuestreo de consultas con reemplazo, 10 000 réplicas,
    generador numpy default_rng(0). La semilla solo fija la reproducibilidad del
    intervalo; no interviene en ninguna cifra puntual.
"""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parent
if not (ROOT / "results").is_dir():
    ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "src"))
from eval_bank import ALL_QUERIES, GROUND_TRUTH, DOMAIN_QUERIES, CLASSES  # noqa: E402

RES = ROOT / "results"
EXP11 = RES / "experimento11" / "raw"
ABL = RES / "ablation_mdir_bias" / "ablation_metrics.csv"
EXP14 = RES / "experimento14" / "banco_degenerado.json"
STAGE7_LOG = RES / "hemisferio_visual" / "stage7_bidirectional.log"
N_BOOT = 10_000
BOOT_SEED = 0
ARMS = ("M", "T-oraculo", "T-protocolo")
ARM_NAME = {"M": "EHAM única", "T-oraculo": "Oráculo", "T-protocolo": "Protocolo"}


# ---------------------------------------------------------------- utilidades

def md(df, floatfmt="{:.1f}"):
    """DataFrame -> tabla Markdown (sin depender de tabulate)."""
    cols = [str(c) for c in df.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for row in df.itertuples(index=False):        # itertuples no convierte int en float
        cells = []
        for v in row:
            if isinstance(v, (bool, np.bool_)):
                cells.append("sí" if v else "no")
            elif isinstance(v, (int, np.integer)):
                cells.append(str(int(v)))
            elif isinstance(v, (float, np.floating)):
                cells.append("—" if np.isnan(v) else floatfmt.format(v))
            else:
                cells.append(str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def section(title):
    print(f"\n\n## {title}\n")


def table(title, df, source, floatfmt="{:.1f}", note=None):
    print(f"\n**{title}**\n")
    print(md(df, floatfmt))
    print(f"\n_Fuente: {source}_")
    if note:
        print(f"\n_{note}_")


def mcnemar_exact(b, c):
    """b, c: pares discordantes. Devuelve p bilateral exacto."""
    n = b + c
    return 1.0 if n == 0 else float(binomtest(min(b, c), n, 0.5).pvalue)


def boot_mean_ci(x, rng):
    x = np.asarray(x, dtype=float)
    idx = rng.integers(0, len(x), size=(N_BOOT, len(x)))
    means = x[idx].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def plural_match(tok, w):
    """Coincidencia exacta o por plural regular (±s, ±es), en ambos sentidos."""
    return tok in (w, w + "s", w + "es") or w in (tok + "s", tok + "es")


def load_vocab():
    vocab = {}
    for c in CLASSES:
        lab = json.loads((ROOT / f"labels_{c}.json").read_text())
        vec = json.loads((ROOT / f"label_vectors_{c}.json").read_text())
        assert set(lab) == set(vec), f"labels_{c} y label_vectors_{c} difieren"
        vocab[c] = set(lab)
    owner = defaultdict(set)
    for c in CLASSES:
        for w in vocab[c]:
            owner[w].add(c)
    excl = {c: {w for w in vocab[c] if len(owner[w]) == 1} for c in CLASSES}
    return vocab, excl


VOCAB, EXCL = load_vocab()


def query_features(q, cls):
    toks = words(q)
    return {
        "nombre_exacto": cls in toks,
        "nombre_plural": any(plural_match(t, cls) for t in toks),
        "vocab_exacto": any(t in VOCAB[cls] for t in toks),
        "vocab_plural": any(plural_match(t, w) for t in toks for w in VOCAB[cls]),
        "excl_exacto": any(t in EXCL[cls] for t in toks),
        "excl_plural": any(plural_match(t, w) for t in toks for w in EXCL[cls]),
    }


def composition(pairs):
    feats = [query_features(q, c) for q, c in pairs]
    n = len(pairs)
    out = {"n": n}
    for k in ("nombre_exacto", "nombre_plural", "vocab_exacto", "vocab_plural",
              "excl_exacto", "excl_plural"):
        out[k] = sum(f[k] for f in feats)
    return out


def comp_row(label, pairs):
    c = composition(pairs)
    n = c["n"]
    pct = lambda k: f"{c[k]} ({100 * c[k] / n:.1f} %)" if n else "—"
    return {"conjunto": label, "n": n,
            "nombre de la clase (exacto)": pct("nombre_exacto"),
            "nombre (con plural)": pct("nombre_plural"),
            "palabra del vocabulario (exacto)": pct("vocab_exacto"),
            "vocabulario (con plural)": pct("vocab_plural"),
            "palabra exclusiva (exacto)": pct("excl_exacto"),
            "exclusiva (con plural)": pct("excl_plural")}


# ---------------------------------------------------------------- exp11: carga

def load_exp11_text():
    rows, metas = [], []
    for f in sorted(EXP11.glob("s*_N*_c*.json")):
        d = json.loads(f.read_text())
        metas.append(dict(d["meta"], archivo=f.name))
        for r in d["texto"]:
            r = {k: v for k, v in r.items() if k != "z"}
            r["trozo"] = d["meta"]["trozo"]
            rows.append(r)
    df = pd.DataFrame(rows)
    df["ok_resp"] = df["nn_ok"].astype("boolean")          # NaN si no respondió
    df["ok_total"] = df["responde"] & df["nn_ok"].fillna(False).astype(bool)
    return df, metas


def load_exp11_files(kind):
    out = []
    for f in sorted(EXP11.glob(f"s*_N*_{kind}*.json")):
        out.append(json.loads(f.read_text()))
    return out


# ---------------------------------------------------------------- M1

def m1(df, metas):
    section("M1. Exp11: clase correcta (1-NN) sobre el total y sobre las respondidas")
    seeds = sorted(df.semilla.unique())
    cuts = sorted(df.corte.unique())
    nq = df.groupby(["corte", "semilla"]).query.nunique()
    nrep = df.groupby(["corte", "semilla", "brazo", "query"]).size()
    print(f"Datos: {len(df)} filas de texto; semillas {seeds[0]}–{seeds[-1]} ({len(seeds)}); "
          f"cortes {[int(c) for c in cuts]}; consultas reservadas por (semilla, corte): "
          f"{sorted(int(v) for v in set(nq.values))}; réplicas del recuerdo por consulta y brazo: "
          f"{sorted(int(v) for v in set(nrep.values))}.")
    print("\nDenominador de la tesis: `run_experiment11_monolithic.py:597` define "
          "`(\"nn_ok\", \"nn_ok\", \"responde\")`; `_rate` (líneas 578-582) filtra las filas "
          "con `responde` verdadero y además descarta las que no tienen `nn_ok` (las no "
          "respondidas no lo traen, línea 420). La clase correcta de la tesis es, por tanto, "
          "sobre las consultas respondidas, promediada por semilla y luego entre semillas.")

    # --- tabla principal
    rec = []
    for N in cuts:
        for arm in ARMS:
            s = df[(df.corte == N) & (df.brazo == arm)]
            per_seed_resp = s.groupby("semilla").ok_resp.mean()     # NaN excluidos
            per_seed_tot = s.groupby("semilla").ok_total.mean()
            per_seed_r = s.groupby("semilla").responde.mean()
            rec.append({"N": N, "brazo": ARM_NAME[arm],
                        "responde %": 100 * per_seed_r.mean(),
                        "clase / respondidas % (tesis)": 100 * per_seed_resp.mean(),
                        "clase / total %": 100 * per_seed_tot.mean()})
    t = pd.DataFrame(rec)
    orc = t[t.brazo == "Oráculo"].set_index("N")
    t["distancia al oráculo, total (pp)"] = [
        orc.loc[r["N"], "clase / total %"] - r["clase / total %"] for _, r in t.iterrows()]
    t["distancia al oráculo, respondidas (pp)"] = [
        orc.loc[r["N"], "clase / respondidas % (tesis)"] - r["clase / respondidas % (tesis)"]
        for _, r in t.iterrows()]
    n_q, n_r = int(nq.iloc[0]), int(nrep.iloc[0])
    table(f"Tabla M1.1. Clase correcta por brazo y corte (media de {len(seeds)} semillas; cada semilla, "
          f"{n_q} consultas × {n_r} réplicas)",
          t, "results/experimento11/raw/s*_N*_c*.json, campos `responde` y `nn_ok`")

    # --- comparación pareada protocolo contra EHAM única
    rng = np.random.default_rng(BOOT_SEED)
    rec = []
    for N in cuts:
        s = df[(df.corte == N) & (df.brazo.isin(["M", "T-protocolo"]))]
        piv_tot = s.pivot_table(index=["semilla", "rep", "query"], columns="brazo",
                                values="ok_total", aggfunc="first")
        piv_res = s.pivot_table(index=["semilla", "rep", "query"], columns="brazo",
                                values="responde", aggfunc="first")
        piv_ok = s.assign(ok=s.ok_resp.astype(float)).pivot_table(
            index=["semilla", "rep", "query"], columns="brazo", values="ok", aggfunc="first")
        for version in ("total", "respondidas"):
            if version == "total":
                A = piv_tot.astype(float)
            else:
                both = piv_res["M"].astype(bool) & piv_res["T-protocolo"].astype(bool)
                A = piv_ok[both]
            # por consulta: media sobre los 30 sorteos (10 semillas × 3 réplicas)
            pq = A.groupby(level="query").mean()
            d = (pq["T-protocolo"] - pq["M"]).to_numpy()
            lo, hi = boot_mean_ci(100 * d, rng)
            n_plus, n_minus = int((d > 0).sum()), int((d < 0).sum())
            p_q = mcnemar_exact(n_plus, n_minus)
            # por sorteo: un McNemar exacto por (semilla, réplica)
            ps, bs, cs = [], [], []
            for (_sd, _rp), g in A.groupby(level=["semilla", "rep"]):
                b = int(((g["M"] == 1) & (g["T-protocolo"] == 0)).sum())
                c = int(((g["M"] == 0) & (g["T-protocolo"] == 1)).sum())
                bs.append(b); cs.append(c); ps.append(mcnemar_exact(b, c))
            rec.append({"N": N, "versión": version, "consultas": len(pq),
                        "Δ protocolo − EHAM (pp)": 100 * d.mean(),
                        "IC 95 % bootstrap por consulta": f"[{lo:+.1f}, {hi:+.1f}]",
                        "consultas P>M / P<M": f"{n_plus} / {n_minus}",
                        "p exacto (por consulta)": p_q,
                        "por sorteo: b (solo M acierta) mediana [mín, máx]": f"{int(np.median(bs))} [{min(bs)}, {max(bs)}]",
                        "por sorteo: c (solo P acierta) mediana [mín, máx]": f"{int(np.median(cs))} [{min(cs)}, {max(cs)}]",
                        "por sorteo: p mediana [mín, máx]": f"{np.median(ps):.2f} [{min(ps):.3f}, {max(ps):.2f}]",
                        "sorteos con p<0.05": f"{sum(p < 0.05 for p in ps)}/{len(ps)}"})
    table("Tabla M1.2. Protocolo contra EHAM única, pareado por consulta",
          pd.DataFrame(rec), "results/experimento11/raw/s*_N*_c*.json",
          floatfmt="{:.3g}",
          note=(f"«Por consulta»: cada consulta se resume en su tasa de acierto sobre los {len(seeds) * n_r} "
                f"sorteos ({len(seeds)} semillas × {n_r} réplicas); la prueba es McNemar exacto sobre las "
                "consultas cuya tasa difiere entre brazos (generalización a varias réplicas de McNemar; con "
                f"un solo sorteo coincide con él). «Por sorteo»: McNemar exacto clásico sobre las {n_q} "
                "consultas de cada (semilla, réplica). «Respondidas»: solo los pares en que ambos brazos "
                "responden."))

    # --- variación entre semillas
    rec = []
    for N in cuts:
        for arm in ARMS:
            s = df[(df.corte == N) & (df.brazo == arm)]
            ps_ = 100 * s.groupby("semilla").ok_total.mean()
            # variación dentro de una semilla (solo réplicas del recuerdo)
            within = s.groupby(["semilla", "query"]).ok_total.nunique()
            n_within = (within > 1).groupby(level="semilla").sum().mean()
            # variación del destino y de la respuesta entre semillas
            if arm == "T-protocolo":
                dest = s.groupby("query").destino.apply(lambda x: x.fillna("—").nunique())
                resp = s.groupby("query").responde.nunique()
                dest_w = s.groupby(["semilla", "query"]).destino.apply(lambda x: x.fillna("—").nunique())
                n_dest, n_resp, n_dest_w = int((dest > 1).sum()), int((resp > 1).sum()), int((dest_w > 1).sum())
            else:
                n_dest = n_resp = n_dest_w = "—"
            rec.append({"N": N, "brazo": ARM_NAME[arm],
                        "media %": ps_.mean(), "DE entre semillas (pp)": ps_.std(ddof=1),
                        "mín %": ps_.min(), "máx %": ps_.max(),
                        "consultas con acierto distinto entre réplicas de una semilla (media)": round(float(n_within), 1),
                        "consultas cuyo destino cambia entre semillas": n_dest,
                        "… dentro de una semilla": n_dest_w,
                        "consultas cuya respuesta (sí/no) cambia entre semillas": n_resp})
    table("Tabla M1.3. Variación entre semillas de la clase correcta sobre el total",
          pd.DataFrame(rec), "results/experimento11/raw/s*_N*_c*.json", floatfmt="{:.2f}")

    form = pd.DataFrame([{"N": m["corte"], "semilla": m["semilla"],
                          **m["formacion_texto"]} for m in metas]).drop_duplicates()
    fsum = form.groupby("N").agg(**{"semillas": ("semilla", "nunique"),
                                    "registradas mín": ("registradas", "min"),
                                    "registradas máx": ("registradas", "max"),
                                    "rechazadas mín": ("rechazadas", "min"),
                                    "rechazadas máx": ("rechazadas", "max"),
                                    "acierto temprano mín": ("acierto_temprano", "min"),
                                    "acierto temprano máx": ("acierto_temprano", "max")}).reset_index()
    table("Tabla M1.4. Formación de directorios (T-protocolo) entre semillas",
          fsum, "campo `meta.formacion_texto` de results/experimento11/raw/s*_N*_c*.json",
          floatfmt="{:.4f}")

    # --- estado de los directorios entre trozos de una misma semilla
    p = df[(df.brazo == "T-protocolo") & (df.rep == 0)]
    hops = sorted(float(h) for h in p.saltos.unique())
    circ = p.groupby(["corte", "semilla", "entrada", "trozo"]).consultados.agg(["min", "max"])
    assert (circ["min"] == circ["max"]).all()          # constante dentro de un trozo
    circ = circ["min"].unstack("trozo")
    varying = circ[circ.apply(lambda r: r.dropna().nunique() > 1, axis=1)]
    small = circ[(circ < len(CLASSES)).any(axis=1)]
    print(f"\nEn T-protocolo, `saltos` vale {hops} en todas las filas, así que `consultados` es el "
          "tamaño del círculo del módulo de entrada (él más los que conoce por su directorio). Dentro "
          "de un mismo trozo ese tamaño es constante para cada módulo de entrada. Según el código, "
          "la formación es determinista por semilla (`rng = np.random.RandomState(seed)`, línea 372; "
          "docstring de `run_job`, líneas 360-363), así que los seis trozos de una semilla deberían "
          "tener los mismos directorios. Pero `run_job` forma los directorios (línea 389) sobre "
          "`CTX[\"cached\"][\"specialists\"]`, que cada proceso carga una sola vez (`init_worker`, "
          "líneas 352-356) y reutiliza entre trabajos sin reiniciar `mem_dir`.")
    v = small.reset_index()
    v.columns = [str(c) for c in v.columns]
    table(f"Tabla M1.5. Tamaño del círculo de la entrada por trozo, en las combinaciones donde alguna vez "
          f"es menor que {len(CLASSES)}",
          v, "campos `consultados`, `entrada`, `saltos` de results/experimento11/raw/s*_N*_c*.json",
          floatfmt="{:.0f}",
          note=(f"Combinaciones (corte, semilla, entrada) cuyo círculo cambia entre trozos de la misma "
                f"semilla: {len(varying)}. En las combinaciones (corte, semilla) que no aparecen aquí, el "
                f"círculo es {len(CLASSES)} para toda entrada en todos los trozos. Con los raw no se "
                "distingue si esos trozos heredaron directorios de trabajos anteriores del mismo proceso "
                "o salen de otra corrida; en cualquier caso, no comparten la formación que el código "
                "declara."))


# ---------------------------------------------------------------- M2

def balanced_queries(N, seed):
    """Copia literal de run_ablation.balanced_queries (líneas 242-261)."""
    rng = np.random.RandomState(seed)
    n_per = N // len(CLASSES)
    pools = []
    for cls in CLASSES:
        pool = DOMAIN_QUERIES[cls][:]
        rng.shuffle(pool)
        pools.append(pool[:n_per])
    q, gt = [], []
    for i in range(n_per):
        for j, cls in enumerate(CLASSES):
            if i < len(pools[j]):
                q.append(pools[j][i]); gt.append(cls)
    return q, gt


def m2(ab):
    section("M2. Calibración: temprana, madura y composición del conjunto evaluado")
    conds = list(dict.fromkeys(ab.condition))
    Ns = sorted(ab.N.unique())
    seeds = sorted(ab.seed.unique())
    balanced = {"D", "G"}      # run_ablation.get_condition_config: use_balanced

    # tamaño del conjunto evaluado por fila y control de integridad
    def n_eval(cond, N, seed):
        return len(balanced_queries(N, seed)[0]) if cond in balanced else len(ALL_QUERIES[:N])
    ab = ab.copy()
    ab["n_eval"] = [n_eval(r.condition, r.N, r.seed) for r in ab.itertuples()]
    # el CSV redondea a 4 decimales: k/n debe quedar a ≤ 5e-5 de la temprana para algún k entero
    k = (ab.early_accuracy * ab.n_eval).round()
    ok = ((k / ab.n_eval - ab.early_accuracy).abs() <= 5e-5 + 1e-12)
    print(f"Control: en {int(ok.sum())} de {len(ab)} filas la temprana es k/n para un k entero, con n "
          "el tamaño reconstruido (primeras N del banco, o el sorteo balanceado de D y G, que "
          "puede dar menos de N), así que ese tamaño coincide con el que se evaluó.")

    rec = []
    for cond in conds:
        for N in Ns:
            s = ab[(ab.condition == cond) & (ab.N == N)]
            diff = s.mature_accuracy - s.early_accuracy
            rec.append({"cond.": cond, "N": N, "consultas evaluadas": "/".join(map(str, sorted(set(s.n_eval)))),
                        "temprana %": 100 * s.early_accuracy.mean(),
                        "madura %": 100 * s.mature_accuracy.mean(),
                        "madura − temprana (pp)": 100 * diff.mean(),
                        "DE temprana (pp)": 100 * s.early_accuracy.std(ddof=1),
                        "DE madura (pp)": 100 * s.mature_accuracy.std(ddof=1)})
    t = pd.DataFrame(rec)
    table(f"Tabla M2.1. Temprana y madura por condición y N, sobre las mismas consultas (media de {len(seeds)} semillas)",
          t, "results/ablation_mdir_bias/ablation_metrics.csv, columnas `early_accuracy` y `mature_accuracy`",
          floatfmt="{:.2f}",
          note=("En run_ablation.py ambas fases se miden sobre la misma lista de consultas "
                "(líneas 446-458): la diferencia es pareada por construcción."))

    # desviación entre semillas por condición
    metric_cols = [c for c in ab.columns if c not in ("condition", "N", "seed", "n_eval")]
    rec = []
    for cond in conds:
        s = ab[ab.condition == cond]
        sd = s.groupby("N")[metric_cols].std(ddof=1)
        rec.append({"cond.": cond,
                    "DE máx. de la madura entre semillas (pp)": 100 * sd["mature_accuracy"].max(),
                    "DE máx. de la temprana (pp)": 100 * sd["early_accuracy"].max(),
                    "columnas del CSV que varían entre semillas": int((sd.max() > 0).sum()),
                    "de": len(metric_cols)})
    t2 = pd.DataFrame(rec)
    n_zero = int((t2["columnas del CSV que varían entre semillas"] == 0).sum())
    table(f"Tabla M2.2. Variación entre las {len(seeds)} semillas, por condición (máximo sobre los {len(Ns)} N)",
          t2, "results/ablation_mdir_bias/ablation_metrics.csv", floatfmt="{:.2f}",
          note=(f"Condiciones con las {len(metric_cols)} columnas idénticas en las {len(seeds)} semillas: "
                f"{n_zero} de {len(conds)}. En run_ablation.py la semilla solo entra en el sorteo "
                "balanceado (D y G, línea 244) y en el módulo de entrada de la fase madura (línea "
                "325); como cada transacción se registra en los directorios de los ocho módulos "
                "(líneas 312-313), los ocho directorios son iguales y la entrada no cambia nada."))

    # equivalencias
    def same(a, b, cols):
        x = ab[ab.condition == a].sort_values(["N", "seed"])[cols].to_numpy()
        y = ab[ab.condition == b].sort_values(["N", "seed"])[cols].to_numpy()
        return bool(np.allclose(x, y))
    early_cols = [c for c in metric_cols if c.startswith(("early_acc", "mdir_reg_", "mdir_entropy"))]
    print(f"\nEquivalencias en el CSV: F idéntica a A en las {len(metric_cols)} columnas: "
          f"{same('F', 'A', metric_cols)}. G y D con la misma fase temprana y los mismos registros del "
          f"directorio ({len(early_cols)} columnas): {same('G', 'D', early_cols)}; solo cambia la lectura "
          "madura (G = D + B1).")

    # temprana por tramos (no depende del directorio: el ganador temprano sale de M_dom)
    std_conds = [c for c in conds if c not in balanced]
    early_hits = {}
    for N in Ns:
        vals = ab[(ab.N == N) & (ab.condition.isin(std_conds))].early_accuracy * N
        assert np.allclose(vals, vals.iloc[0]), "la temprana difiere entre condiciones estándar"
        early_hits[N] = int(round(vals.iloc[0]))
    rec = []
    prev = 0
    for N in Ns:
        lo, hi = prev, N
        pairs = list(zip(ALL_QUERIES[lo:hi], GROUND_TRUTH[lo:hi]))
        c = composition(pairs)
        hits = early_hits[N] - (early_hits[prev] if prev else 0)
        rec.append({"tramo del banco": f"{lo + 1}–{hi}", "consultas": hi - lo,
                    "aciertos tempranos": f"{hits}/{hi - lo}",
                    "temprana del tramo %": 100 * hits / (hi - lo),
                    "con nombre de la clase %": 100 * c["nombre_plural"] / c["n"],
                    "con palabra exclusiva %": 100 * c["excl_plural"] / c["n"]})
        prev = N
    table("Tabla M2.3. Precisión temprana por tramos del banco (condiciones estándar: " + ", ".join(std_conds) + ")",
          pd.DataFrame(rec),
          "early_accuracy × N de results/ablation_mdir_bias/ablation_metrics.csv; composición con src/eval_bank.py y labels_<clase>.json",
          floatfmt="{:.1f}",
          note=("Los aciertos de un tramo se obtienen restando los de N consecutivos. Es válido porque el "
                "ganador temprano de cada consulta lo decide M_dom (run_ablation.py:270-317), que es el "
                "mismo para todo N; el directorio no interviene."))

    # composición del conjunto evaluado
    rec = [comp_row(f"primeras {N}", list(zip(ALL_QUERIES[:N], GROUND_TRUTH[:N]))) for N in Ns]
    rec.append(comp_row(f"banco completo", list(zip(ALL_QUERIES, GROUND_TRUTH))))
    table("Tabla M2.4. Composición de las primeras N consultas (las que evalúan A, B1, B2, C, E32, E64 y F)",
          pd.DataFrame(rec), "src/eval_bank.py (ALL_QUERIES, GROUND_TRUTH); labels_<clase>.json")
    rec = []
    for N in Ns:
        fr = []
        for sd in seeds:
            q, gt = balanced_queries(N, sd)
            c = composition(list(zip(q, gt)))
            fr.append(100 * c["nombre_plural"] / c["n"])
        rec.append({"N": N, "consultas": len(balanced_queries(N, seeds[0])[0]),
                    "con nombre de la clase, media %": float(np.mean(fr)),
                    "mín %": min(fr), "máx %": max(fr)})
    table(f"Tabla M2.5. Composición del sorteo balanceado de D y G ({len(seeds)} semillas)",
          pd.DataFrame(rec), "run_ablation.balanced_queries reproducida; src/eval_bank.py")


# ---------------------------------------------------------------- M3

def m3(df, ab):
    section("M3. Composición de las particiones del banco de texto")
    n_abl = int(ab.N.max())                      # banco de la ablación con el N mayor
    src2 = (ROOT / "run_experiment2_iota_kappa.py").read_text()
    n_80 = int(re.search(r"ALL_QUERIES\[:(\d+)\]", src2).group(1))   # banco de exp2 (y exp4-6)
    held = df[["query", "truth"]].drop_duplicates()
    held_set = set(map(tuple, held.to_numpy()))
    bank = list(zip(ALL_QUERIES, GROUND_TRUTH))
    train = [p for p in bank if p not in held_set]
    # comprobación: las reservadas son la cola de cada lista de clase
    per_cls_train = Counter(c for _, c in train)
    tail_ok = all(set(DOMAIN_QUERIES[c][per_cls_train[c]:]) ==
                  {q for q, t in held_set if t == c} for c in CLASSES)
    print(f"Las {len(held_set)} reservadas se toman de los raw de exp11 (las consultas que de verdad se "
          f"evaluaron). Formación por clase: {dict(per_cls_train)}. ¿Las reservadas son exactamente la "
          f"cola de cada lista de clase de src/eval_bank.py? {tail_ok}.")
    rec = [comp_row("banco completo", bank),
           comp_row(f"las {n_abl} (ablación, N={n_abl})", bank[:n_abl]),
           comp_row(f"las {n_80} (exp2, exp4-6: ALL_QUERIES[:{n_80}])", bank[:n_80]),
           comp_row(f"formación de exp11 ({len(train)})", train),
           comp_row(f"reservadas de exp11 ({len(held_set)})", [p for p in bank if p in held_set])]
    table("Tabla M3.1. Consultas que traen el nombre de su clase o una palabra de su vocabulario",
          pd.DataFrame(rec),
          "src/eval_bank.py; labels_<clase>.json; reservadas: results/experimento11/raw/s*_N*_c*.json",
          note=("Regla: tokens = secuencias de letras en minúsculas. «Exacto»: el token es igual a la "
                "palabra. «Con plural»: además ±s o ±es (tomato/tomatoes, cup/cups). «Exclusiva»: palabra "
                "que está en labels_<clase>.json de una sola clase. El sistema tokeniza con spaCy "
                "(lemas NOUN/ADJ/PROPN, src/stage6_interaction.py:88), que no está versionado; la regla "
                "de aquí es una aproximación declarada."))
    rec = []
    for c in CLASSES:
        rec.append({"clase": c, "palabras": len(VOCAB[c]), "exclusivas": len(EXCL[c]),
                    "¿el nombre está en su vocabulario?": c in VOCAB[c]})
    table("Tabla M3.2. Vocabulario por clase", pd.DataFrame(rec), "labels_<clase>.json")


# ---------------------------------------------------------------- M6

def entropy_bits(p):
    p = np.asarray(p, dtype=float)
    p = p[p > 0]
    p = p / p.sum()
    return float(-(p * np.log2(p)).sum())


def mi_from_cm(cm):
    cm = np.asarray(cm, dtype=float)
    n = cm.sum()
    pj = cm / n
    pd_ = pj.sum(axis=1)
    pw = pj.sum(axis=0)
    hd, hw = entropy_bits(pd_), entropy_bits(pw)
    hj = entropy_bits(pj.ravel())
    I = hd + hw - hj
    r = int((cm.sum(axis=1) > 0).sum()); c = int((cm.sum(axis=0) > 0).sum())
    bias = (r - 1) * (c - 1) / (2 * n * math.log(2))
    return {"n": n, "H_D": hd, "H_W": hw, "I": I, "H_W|D": hw - I, "sesgo_indep": bias}


def m6(ab):
    section("M6 (Wegner). Información mutua entre dominio y ganador maduro")
    conds = list(dict.fromkeys(ab.condition))
    Ns = sorted(ab.N.unique())
    cm_cols = [[f"cm_{a}_{b}" for b in CLASSES] for a in CLASSES]
    reg_cols = [f"mdir_reg_{c}" for c in CLASSES]
    chk = [abs(entropy_bits(r[reg_cols].to_numpy(dtype=float)) - r.mdir_entropy) for _, r in ab.iterrows()]
    print(f"Control: la entropía de los conteos `mdir_reg_<clase>` reproduce `mdir_entropy` con una "
          f"diferencia máxima de {max(chk):.4f} bits. H_dir es la entropía de los registros del "
          "directorio por módulo, no de la relación pista → módulo.")
    rec = []
    for cond in conds:
        for N in Ns:
            s = ab[(ab.condition == cond) & (ab.N == N)]
            vals = []
            for _, r in s.iterrows():
                cm = np.array([[r[c] for c in row] for row in cm_cols])
                vals.append(mi_from_cm(cm))
            v = pd.DataFrame(vals).mean()
            rec.append({"cond.": cond, "N": N, "n (sin rechazos)": f"{v['n']:.1f}", "_H_D": v["H_D"],
                        "H_dir (mdir_entropy)": s.mdir_entropy.mean(),
                        "H(ganador)": v["H_W"],
                        "I(dominio; ganador)": v["I"], "H(ganador dado el dominio)": v["H_W|D"],
                        "IM normalizada = I / H(dominio)": v["I"] / v["H_D"],
                        "sesgo esperado de I bajo independencia": v["sesgo_indep"]})
    t = pd.DataFrame(rec)
    hd_lo, hd_hi = t["_H_D"].min(), t["_H_D"].max()
    table(f"Tabla M6.1. Entropía del directorio frente a información mutua (bits; media de "
          f"{ab.seed.nunique()} semillas)",
          t.drop(columns="_H_D"),
          "results/ablation_mdir_bias/ablation_metrics.csv, columnas `cm_<verdad>_<ganador>` (fase madura) y `mdir_entropy`",
          floatfmt="{:.3f}",
          note=(f"Estimador plug-in; H(dominio) vale entre {hd_lo:.3f} y {hd_hi:.3f} bits en todas las "
                "filas. «Sesgo esperado bajo independencia» = (filas−1)(columnas−1)/(2 n ln 2), "
                f"lo que el plug-in daría en promedio si el ganador no dependiera del dominio; con N={min(Ns)} "
                "no es despreciable. La matriz `cm` excluye las consultas rechazadas (REJ) y es dentro de muestra: "
                "las mismas consultas formaron el directorio. La fase temprana no tiene matriz en el CSV."))
    # referencia: un directorio que enruta al azar
    s = ab[(ab.condition == "A") & (ab.N == max(Ns))].iloc[0]
    regs = s[reg_cols].to_numpy(dtype=float)
    print(f"\nReferencia para leer H_dir: en A con N={max(Ns)} los registros por módulo son "
          f"{dict(zip(CLASSES, (int(x) for x in regs)))} y dan {entropy_bits(regs):.3f} bits. Un enrutamiento "
          "que ignore el dominio con esos mismos registros tendría la misma H_dir e I(dominio; ganador) = 0.")


# ---------------------------------------------------------------- M5

def m5():
    section("M5. Fuera de dominio: protocolo con doble compuerta contra EHAM única")
    files = load_exp11_files("o")
    rows = [r for d in files for r in d["ood"]]
    df = pd.DataFrame(rows)
    nq = df.groupby(["corte", "semilla"]).query.nunique()
    print(f"Archivos: {len(files)} (results/experimento11/raw/s*_N*_o0.json); consultas por "
          f"(semilla, corte): {sorted(int(v) for v in set(nq.values))}.")
    rec = []
    for N in sorted(df.corte.unique()):
        tables, details = set(), None
        for sd, g in df[df.corte == N].groupby("semilla"):
            M = g[g.brazo == "M"].set_index("query").acepta.astype(bool)
            P = g[g.brazo == "T-protocolo"].set_index("query")
            Pg = P.acepta_compuerta.astype(bool).reindex(M.index)
            P1 = P.acepta.astype(bool).reindex(M.index)
            key = (int((M & Pg).sum()), int((M & ~Pg).sum()), int((~M & Pg).sum()), int((~M & ~Pg).sum()),
                   int((M & ~P1).sum()), int((~M & P1).sum()), int(P1.sum()))
            tables.add(key)
            details = (sorted(M[M].index), sorted(Pg[Pg].index), sorted(P1[P1].index))
        assert len(tables) == 1, "la tabla 2×2 cambia entre semillas"
        both, m_only, p_only, neither, m_only1, p_only1, p1 = tables.pop()
        rec.append({"N": N, "semillas con la misma tabla": f"{df[df.corte == N].semilla.nunique()}/{df[df.corte == N].semilla.nunique()}",
                    "EHAM acepta": both + m_only, "protocolo (doble compuerta) acepta": both + p_only,
                    "ambos": both, "solo EHAM": m_only, "solo protocolo": p_only,
                    "p McNemar exacto (doble compuerta)": mcnemar_exact(m_only, p_only),
                    "protocolo sin 2.ª compuerta acepta": p1,
                    "p McNemar exacto (sin 2.ª compuerta)": mcnemar_exact(m_only1, p_only1)})
        if N == max(df.corte.unique()):
            last = details
    table(f"Tabla M5.1. Aceptación de las {int(nq.iloc[0])} consultas fuera de dominio",
          pd.DataFrame(rec), "results/experimento11/raw/s*_N*_o0.json, campos `acepta` y `acepta_compuerta`",
          floatfmt="{:.3f}")
    print(f"\nCon N={max(df.corte.unique())}: EHAM única acepta {last[0]}; protocolo con doble compuerta "
          f"acepta {last[1]}; sin la segunda compuerta, {last[2]}.")


# ---------------------------------------------------------------- menores

def chance_at_least_one(K, H, k):
    """P(al menos una de k palabras distintas tomadas al azar de K esté entre H)."""
    if K - H < k:
        return 1.0
    return 1.0 - math.comb(K - H, k) / math.comb(K, k)


def minor_evocation():
    section("Menor: evocación estricta y nivel de azar")
    st7 = (ROOT / "src" / "stage7_bidirectional.py").read_text()
    top_k = int(re.search(r"def evoke_labels\([^)]*top_k: int = (\d+)", st7).group(1))
    union = set().union(*VOCAB.values())
    K = len(union)
    rec = []
    for c in CLASSES:
        rec.append({"clase": c, "vocabulario": len(VOCAB[c]), "exclusivas": len(EXCL[c]),
                    f"azar laxo ({top_k} de la unión) %": 100 * chance_at_least_one(K, len(VOCAB[c]), top_k),
                    f"azar estricto ({top_k} de la unión) %": 100 * chance_at_least_one(K, len(EXCL[c]), top_k),
                    f"azar estricto dado el módulo correcto ({top_k} de su vocabulario) %":
                        100 * chance_at_least_one(len(VOCAB[c]), len(EXCL[c]), top_k)})
    t = pd.DataFrame(rec).astype({"vocabulario": float, "exclusivas": float})
    t.loc[len(t)] = {"clase": "media", "vocabulario": t.vocabulario.mean(), "exclusivas": t.exclusivas.mean(),
                     **{k: t[k].mean() for k in t.columns[3:]}}
    table(f"Tabla E.1. Niveles de azar de la evocación top-{top_k} (unión de vocabularios: {K} palabras)",
          t, "label_vectors_<clase>.json (mismas claves que labels_<clase>.json)", floatfmt="{:.1f}",
          note=(f"Laxo: alguna de las {top_k} palabras está en el vocabulario de la clase real (definición "
                "de 04_metodologia:258 y de src/stage7_bidirectional.py:246). Estricto: alguna es exclusiva "
                f"de esa clase. El decodificador elige las {top_k} por coseno sobre la unión (stage7:128-147). "
                f"La última columna supone que el módulo destino es el correcto y que las {top_k} palabras "
                "salen de su propio vocabulario: el criterio laxo da entonces 100 % por construcción."))

    # etapa 7: solo las 24 muestras impresas en el log
    pat = re.compile(r"^\s+(OK|X)\s+(\w+)\s+->\s+(\w+)\s+·\s+\[(.*)\]\s*$")
    samples = []
    for line in STAGE7_LOG.read_text().splitlines():
        m = pat.match(line)
        if m:
            labels = re.findall(r"'([^']*)'", m.group(4))
            samples.append((m.group(1), m.group(2), m.group(3), labels))
    tot_line = next(l for l in STAGE7_LOG.read_text().splitlines() if "Evocacion" in l)
    lax = sum(any(w in VOCAB[c] for w in L) for _, c, _, L in samples)
    strict = sum(any(w in EXCL[c] for w in L) for _, c, _, L in samples)
    routed_ok = sum(c == d for _, c, d, _ in samples)
    n_tried = int(re.search(r"(\d+)/(\d+)", tot_line).group(2))
    per_cls = Counter(c for _, c, _, _ in samples)
    print(f"\nEtapa 7 (cifra de la tesis): `{tot_line.strip()}`. El log solo imprime {len(samples)} de "
          f"esas evocaciones ({'/'.join(map(str, sorted(set(per_cls.values()))))} por clase); las demás "
          "no están en results/. "
          f"En esas {len(samples)}: enrutadas a su clase {routed_ok}; laxo {lax}/{len(samples)}; estricto "
          f"{strict}/{len(samples)}. La versión estricta sobre las {n_tried} no se puede calcular con lo "
          "versionado.")

    # exp11: todas las imágenes de prueba tienen sus 3 etiquetas guardadas
    files = load_exp11_files("i")
    rows = [r for d in files for r in d["imagen"]]
    df = pd.DataFrame(rows)
    df["estricto"] = [any(w in EXCL[t] for w in (L or [])) for t, L in zip(df.truth, df.labels)]
    df["laxo"] = [any(w in VOCAB[t] for w in (L or [])) for t, L in zip(df.truth, df.labels)]
    assert (df.laxo == df.hit).all(), "el laxo recalculado no coincide con `hit`"
    assert df.labels.map(lambda L: len(L or [])).max() == top_k
    rec = []
    for N in sorted(df.corte.unique()):
        for arm in ARMS:
            s = df[(df.corte == N) & (df.brazo == arm)]
            per = s.groupby("semilla")
            r_ = s[s.responde]
            rec.append({"N": N, "brazo": ARM_NAME[arm], "imágenes por semilla": int(per.size().iloc[0]),
                        "responde %": 100 * per.responde.mean().mean(),
                        "laxo / total %": 100 * per.laxo.mean().mean(),
                        "estricto / total %": 100 * per.estricto.mean().mean(),
                        "laxo / respondidas %": 100 * r_.laxo.mean(),
                        "estricto / respondidas %": 100 * r_.estricto.mean(),
                        "laxo / respondidas con ruteo correcto %":
                            100 * r_[r_.ruteo_ok == True].laxo.mean() if arm == "T-protocolo" else float("nan")})
    table("Tabla E.2. Evocación imagen → palabras en exp11, laxa y estricta",
          pd.DataFrame(rec), "results/experimento11/raw/s*_N*_i*.json, campos `labels`, `hit`, `responde`, `ruteo_ok`",
          floatfmt="{:.1f}")


def minor_exp14():
    section("Menor: entradas degeneradas de exp14 que siguen aceptadas después de τ")
    d = json.loads(EXP14.read_text())
    stats = [k[len("pasa_"):] for k in d[0] if k.startswith("pasa_")]

    def src(x):
        w = x["nombre"].split()[0]
        return w if w in CLASSES else None

    def foreign(x):
        return src(x) is None or any(c != src(x) for c in x["contenido"])

    acc = [x for x in d if x["acepta"]]
    rec = []
    for st in stats:
        passed = [x for x in acc if x[f"pasa_{st}"]]
        fa = [x for x in acc if foreign(x)]
        rec.append({"estadístico": st, "banco": len(d), "aceptadas por la memoria": len(acc),
                    "siguen aceptadas tras τ": len(passed),
                    "de ellas, con soporte de una clase ajena": sum(foreign(x) for x in passed),
                    "solo de su propia clase": sum(not foreign(x) for x in passed),
                    "aceptadas por clase ajena": len(fa),
                    "ajenas que τ rechaza": sum(not x[f"pasa_{st}"] for x in fa)})
    table("Tabla X.1. Fuga de exp14 (memoria oficial)", pd.DataFrame(rec),
          "results/experimento14/banco_degenerado.json, campos `acepta`, `contenido`, `nombre`, `pasa_<estadístico>`",
          floatfmt="{:.0f}",
          note=("«Clase ajena»: algún especialista distinto de la clase de origen da soporte (para grises, "
                "colores y estructuras, que no tienen clase, cualquiera). Es la cuenta que reproduce el "
                "137 de 152 de 06_discusion:254."))
    fam = defaultdict(lambda: [0, 0, 0])
    for x in d:
        fam[x["familia"]][0] += 1
        fam[x["familia"]][1] += x["acepta"]
        fam[x["familia"]][2] += x["acepta"] and x["pasa_norma"]
    table("Tabla X.2. Por familia (norma)",
          pd.DataFrame([{"familia": k, "n": v[0], "aceptadas": v[1], "aceptadas tras τ": v[2]} for k, v in fam.items()]),
          "results/experimento14/banco_degenerado.json", floatfmt="{:.0f}")


# ---------------------------------------------------------------- main

def main():
    print("# Reanálisis pedidos por el jurado (solo datos versionados)")
    df, metas = load_exp11_text()
    m1(df, metas)
    ab = pd.read_csv(ABL)
    m2(ab)
    m3(df, ab)
    m6(ab)
    m5()
    minor_evocation()
    minor_exp14()


if __name__ == "__main__":
    main()
```
