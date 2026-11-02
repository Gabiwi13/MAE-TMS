# Reanálisis pedidos por el jurado (solo datos versionados)


## M1. Exp11: clase correcta (1-NN) sobre el total y sobre las respondidas

Datos: 61560 filas de texto; semillas 42–51 (10); cortes [25, 50, 100, 200]; consultas reservadas por (semilla, corte): [171]; réplicas del recuerdo por consulta y brazo: [3].

Denominador de la tesis: `run_experiment11_monolithic.py:597` define `("nn_ok", "nn_ok", "responde")`; `_rate` (líneas 578-582) filtra las filas con `responde` verdadero y además descarta las que no tienen `nn_ok` (las no respondidas no lo traen, línea 420). La clase correcta de la tesis es, por tanto, sobre las consultas respondidas, promediada por semilla y luego entre semillas.

**Tabla M1.1. Clase correcta por brazo y corte (media de 10 semillas; cada semilla, 171 consultas × 3 réplicas)**

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

_Fuente: results/experimento11/raw/s*_N*_c*.json, campos `responde` y `nn_ok`_

**Tabla M1.2. Protocolo contra EHAM única, pareado por consulta**

| N | versión | consultas | Δ protocolo − EHAM (pp) | IC 95 % bootstrap por consulta | consultas P>M / P<M | p exacto (por consulta) | por sorteo: b (solo M acierta) mediana [mín, máx] | por sorteo: c (solo P acierta) mediana [mín, máx] | por sorteo: p mediana [mín, máx] | sorteos con p<0.05 |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | total | 171 | -2.28 | [-5.8, +1.1] | 7 / 16 | 0.0931 | 7 [4, 11] | 4 [3, 6] | 0.34 [0.118, 1.00] | 0/30 |
| 25 | respondidas | 170 | -0.706 | [-3.8, +2.4] | 7 / 12 | 0.359 | 5 [1, 8] | 4 [3, 6] | 0.74 [0.219, 1.00] | 0/30 |
| 50 | total | 171 | -0.078 | [-2.9, +2.7] | 9 / 7 | 0.804 | 4 [2, 6] | 4 [2, 7] | 1.00 [0.453, 1.00] | 0/30 |
| 50 | respondidas | 170 | 1.27 | [-1.0, +3.7] | 9 / 4 | 0.267 | 2 [1, 3] | 4 [2, 7] | 0.69 [0.180, 1.00] | 0/30 |
| 100 | total | 171 | -0.156 | [-3.0, +2.7] | 9 / 9 | 1 | 4 [3, 7] | 4 [2, 7] | 1.00 [0.180, 1.00] | 0/30 |
| 100 | respondidas | 170 | 1.2 | [-1.2, +3.7] | 9 / 5 | 0.424 | 2 [1, 4] | 4 [2, 7] | 0.69 [0.219, 1.00] | 0/30 |
| 200 | total | 171 | 0.0975 | [-2.9, +3.2] | 12 / 9 | 0.664 | 5 [3, 7] | 5 [3, 7] | 1.00 [0.344, 1.00] | 0/30 |
| 200 | respondidas | 170 | 1.39 | [-1.2, +4.2] | 12 / 5 | 0.143 | 3 [1, 4] | 5 [3, 7] | 0.71 [0.180, 1.00] | 0/30 |

_Fuente: results/experimento11/raw/s*_N*_c*.json_

_«Por consulta»: cada consulta se resume en su tasa de acierto sobre los 30 sorteos (10 semillas × 3 réplicas); la prueba es McNemar exacto sobre las consultas cuya tasa difiere entre brazos (generalización a varias réplicas de McNemar; con un solo sorteo coincide con él). «Por sorteo»: McNemar exacto clásico sobre las 171 consultas de cada (semilla, réplica). «Respondidas»: solo los pares en que ambos brazos responden._

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

_Fuente: results/experimento11/raw/s*_N*_c*.json_

**Tabla M1.4. Formación de directorios (T-protocolo) entre semillas**

| N | semillas | registradas mín | registradas máx | rechazadas mín | rechazadas máx | acierto temprano mín | acierto temprano máx |
|---|---|---|---|---|---|---|---|
| 25 | 10 | 233 | 233 | 7 | 7 | 0.8412 | 0.8412 |
| 50 | 10 | 233 | 233 | 7 | 7 | 0.8841 | 0.8841 |
| 100 | 10 | 233 | 233 | 7 | 7 | 0.8841 | 0.8841 |
| 200 | 10 | 233 | 233 | 7 | 7 | 0.8755 | 0.8755 |

_Fuente: campo `meta.formacion_texto` de results/experimento11/raw/s*_N*_c*.json_

En T-protocolo, `saltos` vale [0.0] en todas las filas, así que `consultados` es el tamaño del círculo del módulo de entrada (él más los que conoce por su directorio). Dentro de un mismo trozo ese tamaño es constante para cada módulo de entrada. Según el código, la formación es determinista por semilla (`rng = np.random.RandomState(seed)`, línea 372; docstring de `run_job`, líneas 360-363), así que los seis trozos de una semilla deberían tener los mismos directorios. Pero `run_job` forma los directorios (línea 389) sobre `CTX["cached"]["specialists"]`, que cada proceso carga una sola vez (`init_worker`, líneas 352-356) y reutiliza entre trabajos sin reiniciar `mem_dir`.

**Tabla M1.5. Tamaño del círculo de la entrada por trozo, en las combinaciones donde alguna vez es menor que 8**

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

_Fuente: campos `consultados`, `entrada`, `saltos` de results/experimento11/raw/s*_N*_c*.json_

_Combinaciones (corte, semilla, entrada) cuyo círculo cambia entre trozos de la misma semilla: 6. En las combinaciones (corte, semilla) que no aparecen aquí, el círculo es 8 para toda entrada en todos los trozos. Con los raw no se distingue si esos trozos heredaron directorios de trabajos anteriores del mismo proceso o salen de otra corrida; en cualquier caso, no comparten la formación que el código declara._


## M2. Calibración: temprana, madura y composición del conjunto evaluado

Control: en 180 de 180 filas la temprana es k/n para un k entero, con n el tamaño reconstruido (primeras N del banco, o el sorteo balanceado de D y G, que puede dar menos de N), así que ese tamaño coincide con el que se evaluó.

**Tabla M2.1. Temprana y madura por condición y N, sobre las mismas consultas (media de 5 semillas)**

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

_Fuente: results/ablation_mdir_bias/ablation_metrics.csv, columnas `early_accuracy` y `mature_accuracy`_

_En run_ablation.py ambas fases se miden sobre la misma lista de consultas (líneas 446-458): la diferencia es pareada por construcción._

**Tabla M2.2. Variación entre las 5 semillas, por condición (máximo sobre los 4 N)**

| cond. | DE máx. de la madura entre semillas (pp) | DE máx. de la temprana (pp) | columnas del CSV que varían entre semillas | de |
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

_Fuente: results/ablation_mdir_bias/ablation_metrics.csv_

_Condiciones con las 108 columnas idénticas en las 5 semillas: 7 de 9. En run_ablation.py la semilla solo entra en el sorteo balanceado (D y G, línea 244) y en el módulo de entrada de la fase madura (línea 325); como cada transacción se registra en los directorios de los ocho módulos (líneas 312-313), los ocho directorios son iguales y la entrada no cambia nada._

Equivalencias en el CSV: F idéntica a A en las 108 columnas: True. G y D con la misma fase temprana y los mismos registros del directorio (18 columnas): True; solo cambia la lectura madura (G = D + B1).

**Tabla M2.3. Precisión temprana por tramos del banco (condiciones estándar: A, B1, B2, C, E32, E64, F)**

| tramo del banco | consultas | aciertos tempranos | temprana del tramo % | con nombre de la clase % | con palabra exclusiva % |
|---|---|---|---|---|---|
| 1–50 | 50 | 39/50 | 78.0 | 10.0 | 76.0 |
| 51–100 | 50 | 44/50 | 88.0 | 20.0 | 82.0 |
| 101–200 | 100 | 82/100 | 82.0 | 15.0 | 78.0 |
| 201–400 | 200 | 195/200 | 97.5 | 84.5 | 99.5 |

_Fuente: early_accuracy × N de results/ablation_mdir_bias/ablation_metrics.csv; composición con src/eval_bank.py y labels_<clase>.json_

_Los aciertos de un tramo se obtienen restando los de N consecutivos. Es válido porque el ganador temprano de cada consulta lo decide M_dom (run_ablation.py:270-317), que es el mismo para todo N; el directorio no interviene._

**Tabla M2.4. Composición de las primeras N consultas (las que evalúan A, B1, B2, C, E32, E64 y F)**

| conjunto | n | nombre de la clase (exacto) | nombre (con plural) | palabra del vocabulario (exacto) | vocabulario (con plural) | palabra exclusiva (exacto) | exclusiva (con plural) |
|---|---|---|---|---|---|---|---|
| primeras 50 | 50 | 5 (10.0 %) | 5 (10.0 %) | 47 (94.0 %) | 47 (94.0 %) | 38 (76.0 %) | 38 (76.0 %) |
| primeras 100 | 100 | 15 (15.0 %) | 15 (15.0 %) | 94 (94.0 %) | 94 (94.0 %) | 79 (79.0 %) | 79 (79.0 %) |
| primeras 200 | 200 | 30 (15.0 %) | 30 (15.0 %) | 191 (95.5 %) | 191 (95.5 %) | 155 (77.5 %) | 157 (78.5 %) |
| primeras 400 | 400 | 194 (48.5 %) | 199 (49.8 %) | 388 (97.0 %) | 391 (97.8 %) | 351 (87.8 %) | 356 (89.0 %) |
| banco completo | 411 | 203 (49.4 %) | 208 (50.6 %) | 399 (97.1 %) | 402 (97.8 %) | 362 (88.1 %) | 367 (89.3 %) |

_Fuente: src/eval_bank.py (ALL_QUERIES, GROUND_TRUTH); labels_<clase>.json_

**Tabla M2.5. Composición del sorteo balanceado de D y G (5 semillas)**

| N | consultas | con nombre de la clase, media % | mín % | máx % |
|---|---|---|---|---|
| 50 | 48 | 51.7 | 41.7 | 64.6 |
| 100 | 96 | 50.0 | 44.8 | 61.5 |
| 200 | 200 | 50.1 | 48.0 | 55.0 |
| 400 | 399 | 50.7 | 49.6 | 51.4 |

_Fuente: run_ablation.balanced_queries reproducida; src/eval_bank.py_


## M3. Composición de las particiones del banco de texto

Las 171 reservadas se toman de los raw de exp11 (las consultas que de verdad se evaluaron). Formación por clase: {'apple': 30, 'car': 30, 'cow': 30, 'cup': 30, 'dog': 30, 'horse': 30, 'pear': 30, 'tomato': 30}. ¿Las reservadas son exactamente la cola de cada lista de clase de src/eval_bank.py? True.

**Tabla M3.1. Consultas que traen el nombre de su clase o una palabra de su vocabulario**

| conjunto | n | nombre de la clase (exacto) | nombre (con plural) | palabra del vocabulario (exacto) | vocabulario (con plural) | palabra exclusiva (exacto) | exclusiva (con plural) |
|---|---|---|---|---|---|---|---|
| banco completo | 411 | 203 (49.4 %) | 208 (50.6 %) | 399 (97.1 %) | 402 (97.8 %) | 362 (88.1 %) | 367 (89.3 %) |
| las 400 (ablación, N=400) | 400 | 194 (48.5 %) | 199 (49.8 %) | 388 (97.0 %) | 391 (97.8 %) | 351 (87.8 %) | 356 (89.0 %) |
| las 80 (exp2, exp4-6: ALL_QUERIES[:80]) | 80 | 11 (13.8 %) | 11 (13.8 %) | 75 (93.8 %) | 75 (93.8 %) | 63 (78.8 %) | 63 (78.8 %) |
| formación de exp11 (240) | 240 | 58 (24.2 %) | 58 (24.2 %) | 231 (96.2 %) | 231 (96.2 %) | 195 (81.2 %) | 197 (82.1 %) |
| reservadas de exp11 (171) | 171 | 145 (84.8 %) | 150 (87.7 %) | 168 (98.2 %) | 171 (100.0 %) | 167 (97.7 %) | 170 (99.4 %) |

_Fuente: src/eval_bank.py; labels_<clase>.json; reservadas: results/experimento11/raw/s*_N*_c*.json_

_Regla: tokens = secuencias de letras en minúsculas. «Exacto»: el token es igual a la palabra. «Con plural»: además ±s o ±es (tomato/tomatoes, cup/cups). «Exclusiva»: palabra que está en labels_<clase>.json de una sola clase. El sistema tokeniza con spaCy (lemas NOUN/ADJ/PROPN, src/stage6_interaction.py:88), que no está versionado; la regla de aquí es una aproximación declarada._

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

_Fuente: labels_<clase>.json_


## M6 (Wegner). Información mutua entre dominio y ganador maduro

Control: la entropía de los conteos `mdir_reg_<clase>` reproduce `mdir_entropy` con una diferencia máxima de 0.0000 bits. H_dir es la entropía de los registros del directorio por módulo, no de la relación pista → módulo.

**Tabla M6.1. Entropía del directorio frente a información mutua (bits; media de 5 semillas)**

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

_Fuente: results/ablation_mdir_bias/ablation_metrics.csv, columnas `cm_<verdad>_<ganador>` (fase madura) y `mdir_entropy`_

_Estimador plug-in; H(dominio) vale entre 2.992 y 3.000 bits en todas las filas. «Sesgo esperado bajo independencia» = (filas−1)(columnas−1)/(2 n ln 2), lo que el plug-in daría en promedio si el ganador no dependiera del dominio; con N=50 no es despreciable. La matriz `cm` excluye las consultas rechazadas (REJ) y es dentro de muestra: las mismas consultas formaron el directorio. La fase temprana no tiene matriz en el CSV._

Referencia para leer H_dir: en A con N=400 los registros por módulo son {'apple': 186, 'car': 115, 'cow': 181, 'cup': 137, 'dog': 135, 'horse': 112, 'pear': 120, 'tomato': 164} y dan 2.974 bits. Un enrutamiento que ignore el dominio con esos mismos registros tendría la misma H_dir e I(dominio; ganador) = 0.


## M5. Fuera de dominio: protocolo con doble compuerta contra EHAM única

Archivos: 40 (results/experimento11/raw/s*_N*_o0.json); consultas por (semilla, corte): [40].

**Tabla M5.1. Aceptación de las 40 consultas fuera de dominio**

| N | semillas con la misma tabla | EHAM acepta | protocolo (doble compuerta) acepta | ambos | solo EHAM | solo protocolo | p McNemar exacto (doble compuerta) | protocolo sin 2.ª compuerta acepta | p McNemar exacto (sin 2.ª compuerta) |
|---|---|---|---|---|---|---|---|---|---|
| 25 | 10/10 | 2 | 2 | 2 | 0 | 0 | 1.000 | 4 | 0.500 |
| 50 | 10/10 | 2 | 2 | 2 | 0 | 0 | 1.000 | 4 | 0.500 |
| 100 | 10/10 | 5 | 2 | 2 | 3 | 0 | 0.250 | 4 | 1.000 |
| 200 | 10/10 | 8 | 2 | 2 | 6 | 0 | 0.031 | 4 | 0.219 |

_Fuente: results/experimento11/raw/s*_N*_o0.json, campos `acepta` y `acepta_compuerta`_

Con N=200: EHAM única acepta ['a candle burning on a windowsill', 'a kitchen appliance that heats food', 'a laptop computer with a keyboard', 'a lighthouse on a rocky coast', 'a piece of furniture for sitting', 'a screwdriver for tightening screws', 'a thunderstorm with heavy rain', 'a wooden table and chairs']; protocolo con doble compuerta acepta ['a kitchen appliance that heats food', 'a wooden table and chairs']; sin la segunda compuerta, ['a kitchen appliance that heats food', 'a piano with black and white keys', 'a thunderstorm with heavy rain', 'a wooden table and chairs'].


## Menor: evocación estricta y nivel de azar


**Tabla E.1. Niveles de azar de la evocación top-3 (unión de vocabularios: 159 palabras)**

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

_Fuente: label_vectors_<clase>.json (mismas claves que labels_<clase>.json)_

_Laxo: alguna de las 3 palabras está en el vocabulario de la clase real (definición de 04_metodologia:258 y de src/stage7_bidirectional.py:246). Estricto: alguna es exclusiva de esa clase. El decodificador elige las 3 por coseno sobre la unión (stage7:128-147). La última columna supone que el módulo destino es el correcto y que las 3 palabras salen de su propio vocabulario: el criterio laxo da entonces 100 % por construcción._

Etapa 7 (cifra de la tesis): `Evocacion top-3 domain-hit: 113/116 = 97.4%`. El log solo imprime 0 de esas evocaciones ( por clase); las demás no están en results/. En esas 0: enrutadas a su clase 0; laxo 0/0; estricto 0/0. La versión estricta sobre las 116 no se puede calcular con lo versionado.

**Tabla E.2. Evocación imagen → palabras en exp11, laxa y estricta**

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

_Fuente: results/experimento11/raw/s*_N*_i*.json, campos `labels`, `hit`, `responde`, `ruteo_ok`_


## Menor: entradas degeneradas de exp14 que siguen aceptadas después de τ


**Tabla X.1. Fuga de exp14 (memoria oficial)**

| estadístico | banco | aceptadas por la memoria | siguen aceptadas tras τ | de ellas, con soporte de una clase ajena | solo de su propia clase | aceptadas por clase ajena | ajenas que τ rechaza |
|---|---|---|---|---|---|---|---|
| norma | 231 | 180 | 33 | 15 | 18 | 152 | 137 |
| desv_latente | 231 | 180 | 31 | 13 | 18 | 152 | 139 |
| desv_pixeles | 231 | 180 | 92 | 72 | 20 | 152 | 80 |
| niveles | 231 | 180 | 180 | 152 | 28 | 152 | 0 |

_Fuente: results/experimento14/banco_degenerado.json, campos `acepta`, `contenido`, `nombre`, `pasa_<estadístico>`_

_«Clase ajena»: algún especialista distinto de la clase de origen da soporte (para grises, colores y estructuras, que no tienen clase, cualquiera). Es la cuenta que reproduce el 137 de 152 de 06_discusion:254._

**Tabla X.2. Por familia (norma)**

| familia | n | aceptadas | aceptadas tras τ |
|---|---|---|---|
| gris | 33 | 10 | 1 |
| color | 12 | 2 | 2 |
| desenfoque | 128 | 121 | 16 |
| contraste | 48 | 41 | 13 |
| gris con ruido | 6 | 4 | 1 |
| estructura | 4 | 2 | 0 |

_Fuente: results/experimento14/banco_degenerado.json_
