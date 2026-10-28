# Experimento 11 — MAE monolítica contra sistema transactivo

Semillas: [42, 43, 44, 45, 46, 47, 48, 49, 50, 51]. Cortes N (imágenes por clase, ×4 variantes): [25, 50, 100, 200]. Intervalos: bootstrap del 95% sobre las medias por semilla. Banco: las consultas reservadas (no usadas para formar directorios), para los tres brazos. Diseño y criterio de refutación en `propuesta_fase5_mae_monolitica.md`.

Control del llenado en N=200: especialistas reconstruidos DISTINTOS a los `agent_*.pkl` oficiales (4/8 clases).

## N = 25 (400 registros por clase; monolítica 3200)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.7 [97.5, 97.8] | 97.4 [97.1, 97.6] | 97.7 [97.4, 97.9] | 22.82 [22.77, 22.88] | 0.98 [0.98, 0.98] | 97.9 [97.8, 98.0] | 7.03 [7.03, 7.03] | — | 1.82 [1.79, 1.84] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 18.18 [18.14, 18.22] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 6.76 [6.76, 6.76] | 100.0 [100.0, 100.0] | 1.21 [1.19, 1.23] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.0 [97.7, 98.2] | 95.6 [95.0, 96.1] | 95.6 [95.0, 96.1] | 95.6 [95.0, 96.1] | 19.29 [19.13, 19.47] | 1.00 [1.00, 1.00] | 95.6 [95.0, 96.1] | 6.73 [6.72, 6.73] | 93.6 [93.2, 94.1] | 2.38 [2.28, 2.49] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 50.0 [44.4, 55.0] | 0.76 [0.76, 0.77] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 4.7 [4.2, 5.4] | 79.5 [70.1, 85.7] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 83.3 [83.3, 83.3].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 97.5 [97.5, 97.5] | 78.7 [78.7, 78.7] | 78.0 [77.5, 78.5] | 76.4 [75.5, 77.2] | 73.2 [71.8, 74.5] | 5.5 [4.2, 7.0] | — |
| T-oraculo | 86.2 [86.2, 86.2] | 43.8 [43.8, 43.8] | 43.8 [43.8, 43.8] | 43.8 [43.8, 43.8] | 43.6 [43.4, 43.8] | 0.1 [0.0, 0.4] | — |
| T-protocolo | 63.7 [63.7, 63.7] | 41.2 [41.2, 41.2] | 41.2 [41.2, 41.2] | 41.1 [40.9, 41.2] | 41.0 [40.6, 41.2] | 0.2 [0.0, 0.6] | 100.0 [100.0, 100.0] |

## N = 50 (800 registros por clase; monolítica 6400)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.6 [97.3, 98.0] | 97.4 [97.1, 97.8] | 97.3 [97.0, 97.7] | 26.50 [26.45, 26.55] | 0.98 [0.98, 0.98] | 97.7 [97.5, 97.8] | 8.81 [8.81, 8.81] | — | 1.49 [1.47, 1.52] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 20.40 [20.35, 20.44] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 8.50 [8.50, 8.50] | 100.0 [100.0, 100.0] | 1.11 [1.10, 1.12] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.8 [98.6, 99.1] | 98.5 [98.2, 98.8] | 98.5 [98.2, 98.8] | 98.5 [98.2, 98.8] | 20.80 [20.69, 20.91] | 1.00 [1.00, 1.00] | 98.5 [98.2, 98.8] | 8.49 [8.48, 8.49] | 97.3 [97.0, 97.7] | 1.50 [1.43, 1.57] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 52.2 [45.6, 60.0] | 0.74 [0.73, 0.75] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 4.1 [4.1, 4.2] | 85.7 [85.7, 85.7] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 88.4 [88.4, 88.4].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 95.0 [95.0, 95.0] | 93.9 [93.1, 94.5] | 92.0 [91.0, 92.9] | 87.3 [85.6, 88.9] | 7.5 [5.9, 9.2] | — |
| T-oraculo | 98.8 [98.8, 98.8] | 75.0 [75.0, 75.0] | 75.0 [75.0, 75.0] | 74.1 [73.5, 74.8] | 73.1 [72.5, 73.8] | 1.9 [1.2, 2.5] | — |
| T-protocolo | 77.5 [77.5, 77.5] | 67.5 [67.5, 67.5] | 67.5 [67.5, 67.5] | 67.4 [67.1, 67.5] | 65.8 [65.0, 66.4] | 1.8 [1.1, 2.5] | 100.0 [100.0, 100.0] |

## N = 100 (1600 registros por clase; monolítica 12800)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.3 [97.1, 97.5] | 97.1 [96.8, 97.4] | 97.2 [96.9, 97.6] | 29.49 [29.43, 29.55] | 0.98 [0.98, 0.98] | 97.3 [97.2, 97.5] | 10.01 [10.01, 10.01] | — | 1.32 [1.30, 1.34] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 23.44 [23.36, 23.52] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 9.63 [9.63, 9.63] | 100.0 [100.0, 100.0] | 1.05 [1.04, 1.07] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.7 [98.5, 98.9] | 98.5 [98.2, 98.8] | 98.5 [98.2, 98.8] | 98.5 [98.2, 98.8] | 23.76 [23.64, 23.87] | 1.00 [1.00, 1.00] | 98.5 [98.2, 98.8] | 9.63 [9.62, 9.63] | 97.2 [96.8, 97.7] | 1.31 [1.26, 1.36] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 44.4 [40.6, 50.0] | 0.76 [0.75, 0.77] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 4.1 [4.1, 4.2] | 85.7 [85.7, 85.7] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 12.5 [12.5, 12.5] | 12.5 [12.5, 12.5] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 88.4 [88.4, 88.4].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 98.8 [98.8, 98.8] | 96.7 [95.7, 97.8] | 93.6 [91.9, 95.2] | 88.2 [86.2, 90.2] | 10.5 [8.5, 12.5] | — |
| T-oraculo | 98.8 [98.8, 98.8] | 92.5 [92.5, 92.5] | 92.5 [92.5, 92.5] | 91.1 [90.5, 91.8] | 89.8 [88.8, 90.8] | 2.6 [1.7, 3.5] | — |
| T-protocolo | 80.0 [80.0, 80.0] | 78.7 [78.7, 78.7] | 78.7 [78.7, 78.7] | 77.5 [76.8, 78.2] | 76.5 [75.6, 77.4] | 2.2 [1.4, 3.1] | 100.0 [100.0, 100.0] |

## N = 200 (3200 registros por clase; monolítica 25600)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 96.8 [96.6, 97.0] | 96.6 [96.4, 96.8] | 96.6 [96.4, 96.8] | 32.43 [32.32, 32.53] | 0.98 [0.98, 0.98] | 96.7 [96.5, 96.9] | 10.94 [10.94, 10.94] | — | 1.29 [1.27, 1.31] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 26.75 [26.66, 26.87] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 10.55 [10.55, 10.55] | 100.0 [100.0, 100.0] | 1.03 [1.02, 1.05] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.5 [98.2, 98.8] | 98.5 [98.2, 98.9] | 98.5 [98.2, 98.9] | 98.5 [98.2, 98.9] | 27.08 [26.91, 27.28] | 1.00 [1.00, 1.00] | 98.5 [98.2, 98.9] | 10.54 [10.54, 10.55] | 97.0 [96.5, 97.5] | 1.24 [1.19, 1.28] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 48.9 [43.9, 55.0] | 0.76 [0.76, 0.76] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 4.2 [4.1, 4.2] | 85.7 [85.7, 85.7] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 20.0 [20.0, 20.0] | 20.0 [20.0, 20.0] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 87.6 [87.6, 87.6].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.5 [96.5, 98.4] | 93.6 [91.5, 95.6] | 89.1 [87.2, 91.2] | 10.9 [8.8, 12.8] | — |
| T-oraculo | 98.8 [98.8, 98.8] | 97.5 [97.5, 97.5] | 97.5 [97.5, 97.5] | 95.7 [95.0, 96.5] | 93.4 [92.0, 94.8] | 4.1 [2.8, 5.5] | — |
| T-protocolo | 81.2 [81.2, 81.2] | 81.2 [81.2, 81.2] | 81.2 [81.2, 81.2] | 79.8 [78.9, 80.6] | 78.1 [77.0, 79.2] | 3.0 [1.9, 4.0] | 100.0 [100.0, 100.0] |

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