# Experimento 11 — MAE monolítica contra sistema transactivo

Semillas: [42, 43, 44, 45, 46, 47, 48, 49, 50, 51]. Cortes N (imágenes por clase, ×4 variantes): [25, 50, 100, 200]. Intervalos: bootstrap del 95% sobre las medias por semilla. Banco: las consultas reservadas (no usadas para formar directorios), para los tres brazos. Diseño y criterio de refutación en `propuesta_fase5_mae_monolitica.md`.

Control del llenado en N=200: especialistas reconstruidos idénticos a los `agent_*.pkl` oficiales (8/8 clases).

## N = 25 (100 registros por clase; monolítica 800)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 81.3 [81.3, 81.3] | 81.3 [81.3, 81.3] | 95.9 [95.7, 96.1] | 95.8 [95.6, 96.0] | 96.2 [96.1, 96.4] | 17.26 [17.21, 17.32] | 0.99 [0.99, 0.99] | 96.1 [95.9, 96.3] | 4.04 [4.04, 4.04] | — | 3.37 [3.29, 3.45] |
| T-oraculo | 81.3 [81.3, 81.3] | 80.1 [80.1, 80.1] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 15.25 [15.21, 15.30] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 3.88 [3.88, 3.88] | 100.0 [100.0, 100.0] | 1.83 [1.79, 1.87] |
| T-protocolo | 100.0 [100.0, 100.0] | 78.9 [78.5, 79.3] | 98.5 [97.8, 99.1] | 98.5 [97.8, 99.1] | 98.5 [97.8, 99.1] | 15.72 [15.51, 15.98] | 1.00 [1.00, 1.00] | 98.5 [97.8, 99.1] | 3.88 [3.87, 3.88] | 95.4 [94.6, 96.3] | 2.95 [2.46, 3.55] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 4.3 [4.3, 4.3] | 37.2 [33.3, 42.2] | 0.71 [0.71, 0.72] |
| T-oraculo | 4.4 [4.4, 4.4] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 5.2 [5.2, 5.2] | 78.6 [68.5, 85.7] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | 7.5 [7.5, 7.5] | 5.0 [5.0, 5.0] |

Formación de directorios (T-protocolo): registradas 221.00 [221.00, 221.00], rechazadas 19.00 [19.00, 19.00], acierto temprano 82.8 [82.8, 82.8].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 86.2 [86.2, 86.2] | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] | 0.0 [0.0, 0.0] | — |
| T-oraculo | 57.5 [57.5, 57.5] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | — |
| T-protocolo | 41.2 [41.2, 41.2] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 100.0 [100.0, 100.0] |

## N = 50 (200 registros por clase; monolítica 1600)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.1 [96.9, 97.3] | 97.0 [96.8, 97.2] | 97.5 [97.3, 97.8] | 21.29 [21.26, 21.33] | 0.99 [0.99, 0.99] | 97.3 [97.2, 97.5] | 5.68 [5.68, 5.68] | — | 1.83 [1.80, 1.86] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 18.85 [18.78, 18.91] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 5.48 [5.48, 5.48] | 100.0 [100.0, 100.0] | 1.26 [1.25, 1.27] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.5 [98.0, 98.9] | 97.9 [97.5, 98.3] | 97.9 [97.5, 98.3] | 97.9 [97.5, 98.3] | 19.60 [19.44, 19.78] | 1.00 [1.00, 1.00] | 97.9 [97.5, 98.3] | 5.47 [5.47, 5.48] | 96.4 [96.0, 96.8] | 2.15 [1.96, 2.36] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 33.9 [29.4, 38.9] | 0.72 [0.72, 0.73] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 4.2 [4.1, 4.2] | 65.7 [55.7, 77.1] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 84.5 [84.5, 84.5].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 98.8 [98.8, 98.8] | 53.7 [53.7, 53.7] | 53.4 [53.0, 53.7] | 52.8 [52.1, 53.4] | 51.1 [50.4, 51.8] | 2.6 [2.0, 3.4] | — |
| T-oraculo | 85.0 [85.0, 85.0] | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] | 0.0 [0.0, 0.0] | — |
| T-protocolo | 66.2 [66.2, 66.2] | 3.7 [3.7, 3.7] | 3.7 [3.7, 3.7] | 3.7 [3.7, 3.7] | 3.7 [3.7, 3.7] | 0.0 [0.0, 0.0] | 100.0 [100.0, 100.0] |

## N = 100 (400 registros por clase; monolítica 3200)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.7 [97.4, 97.9] | 97.3 [97.1, 97.5] | 97.9 [97.7, 98.1] | 23.88 [23.82, 23.94] | 0.98 [0.98, 0.98] | 97.5 [97.3, 97.7] | 7.51 [7.51, 7.51] | — | 1.59 [1.56, 1.61] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 19.66 [19.60, 19.71] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 7.23 [7.23, 7.23] | 100.0 [100.0, 100.0] | 1.15 [1.14, 1.17] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.6 [98.1, 99.1] | 97.3 [96.7, 97.9] | 97.3 [96.7, 97.9] | 97.3 [96.7, 97.9] | 20.42 [20.22, 20.65] | 1.00 [1.00, 1.00] | 97.3 [96.7, 97.9] | 7.20 [7.19, 7.21] | 96.0 [95.2, 96.7] | 1.98 [1.80, 2.18] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 50.6 [43.9, 57.2] | 0.74 [0.74, 0.75] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 4.4 [4.1, 4.7] | 62.5 [52.7, 73.8] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 7.5 [7.5, 7.5] | 7.5 [7.5, 7.5] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 84.5 [84.5, 84.5].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 98.8 [98.8, 98.8] | 81.2 [81.2, 81.2] | 80.8 [80.1, 81.1] | 79.1 [78.2, 79.9] | 76.2 [74.8, 77.9] | 4.9 [3.4, 6.2] | — |
| T-oraculo | 93.8 [93.8, 93.8] | 45.0 [45.0, 45.0] | 45.0 [45.0, 45.0] | 44.8 [44.4, 45.0] | 44.6 [44.0, 45.0] | 0.4 [0.0, 1.0] | — |
| T-protocolo | 75.0 [75.0, 75.0] | 42.5 [42.5, 42.5] | 42.5 [42.5, 42.5] | 42.4 [42.1, 42.5] | 42.0 [41.2, 42.5] | 0.5 [0.0, 1.2] | 100.0 [100.0, 100.0] |

## N = 200 (800 registros por clase; monolítica 6400)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.4 [97.3, 97.7] | 97.3 [97.1, 97.5] | 97.7 [97.4, 98.0] | 26.69 [26.64, 26.75] | 0.98 [0.98, 0.98] | 97.5 [97.2, 97.8] | 9.03 [9.03, 9.03] | — | 1.36 [1.34, 1.38] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 22.20 [22.15, 22.26] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 8.69 [8.69, 8.69] | 100.0 [100.0, 100.0] | 1.08 [1.07, 1.10] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.6 [98.2, 99.0] | 97.5 [97.1, 97.9] | 97.5 [97.1, 97.9] | 97.5 [97.1, 97.9] | 22.75 [22.59, 22.88] | 1.00 [1.00, 1.00] | 97.5 [97.1, 97.9] | 8.66 [8.65, 8.67] | 96.1 [95.7, 96.6] | 1.75 [1.61, 1.88] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 44.4 [38.9, 50.6] | 0.73 [0.73, 0.74] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 4.2 [4.1, 4.2] | 65.7 [57.1, 75.7] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 7.5 [7.5, 7.5] | 7.5 [7.5, 7.5] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 85.4 [85.4, 85.4].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 96.2 [96.2, 96.2] | 95.2 [94.8, 95.7] | 92.8 [91.9, 93.6] | 87.4 [85.8, 89.0] | 8.9 [7.3, 10.5] | — |
| T-oraculo | 97.5 [97.5, 97.5] | 78.7 [78.7, 78.7] | 78.7 [78.7, 78.7] | 78.0 [77.4, 78.6] | 77.5 [76.6, 78.4] | 1.2 [0.4, 2.1] | — |
| T-protocolo | 81.2 [81.2, 81.2] | 72.5 [72.5, 72.5] | 72.5 [72.5, 72.5] | 71.5 [70.9, 72.1] | 70.9 [70.4, 71.4] | 1.6 [1.1, 2.1] | 100.0 [100.0, 100.0] |

## Qué operaciones de la MAE usa cada brazo

Ningún brazo tiene reglas propias: todos pasan por las mismas operaciones de la memoria.

| paso | M | T-oráculo | T-protocolo | dónde |
|---|---|---|---|---|
| llenado | `register` de una hetero y dos homo con las 8 clases | `register` por clase | igual que T-oráculo | `stage5_fill.fill_agent`, `run_experiment11_monolithic.build_*` |
| aceptación | `Agent.recognize_gated` (containment de la homo + proyección de la hetero) | máximo de `recognize_gated` sobre los 8 | `route_transactive` sobre directorios | `stage6_interaction.py` |
| quién responde | la única memoria | el especialista de la verdad de terreno | el destino del directorio (agregado + encadenado) | `stage6_interaction.route_transactive` |
| respuesta | `mem_dom_H.recall_from_left` con la primera pista reconocida | igual | igual | `run_experiment9_member_loss.recall_lived` |
| directorios | no se usan | no se usan | `register_transaction` en la formación | `stage6_interaction.register_transaction` |
| jueces | 1-NN y centroide sobre las 6400 instancias reales, clasificador latente, `d_nn`; `compat` con `mem_dom_R.recog_weights` de cada clase | igual | igual | `run_experiment9_member_loss.Judge`, `run_experiment11_monolithic.compat` |

F es la razón de exp9 (Bessel), calculada dentro de cada clase y promediada entre clases.

## Archivos
- `raw/s<semilla>_N<corte>_c<trozo>.json`: filas por consulta, sorteo y brazo
- `resumen.json`: medias e intervalos
- `fig1_clase_vs_N.png`, `fig2_dnn_vs_N.png`, `fig3_compat.png`, `fig4_ood.png`