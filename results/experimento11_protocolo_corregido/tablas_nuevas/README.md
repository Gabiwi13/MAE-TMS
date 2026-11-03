# Experimento 11 — MAE monolítica contra sistema transactivo

Semillas: [42, 43, 44, 45, 46, 47, 48, 49, 50, 51]. Cortes N (imágenes por clase, ×16 variantes): [25, 50, 100, 200]. Intervalos: bootstrap del 95% sobre las medias por semilla. Banco: las consultas reservadas (no usadas para formar directorios), para los tres brazos. Diseño y criterio de refutación en `propuesta_fase5_mae_monolitica.md`.

Control del llenado en N=200: 4/8 clases idénticas a los `agent_*.pkl` oficiales; distintas: car 600 celdas, cow 600 celdas, dog 1200 celdas, horse 600 celdas (de 9,830,400 celdas por clase). Este script recalcula los latentes en GPU; una diferencia de redondeo puede mover una coordenada de un registro al nivel vecino.

## N = 25 (400 registros por clase; monolítica 3200)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.6 [97.4, 97.8] | 97.4 [97.3, 97.6] | 97.7 [97.4, 97.9] | 22.86 [22.80, 22.92] | 0.98 [0.98, 0.98] | 97.7 [97.6, 97.9] | 7.03 [7.03, 7.03] | — | 1.81 [1.78, 1.85] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 18.22 [18.20, 18.24] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 6.76 [6.76, 6.76] | 100.0 [100.0, 100.0] | 1.22 [1.21, 1.23] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.4 [97.7, 98.9] | 94.7 [93.4, 96.0] | 94.7 [93.4, 96.0] | 94.7 [93.4, 96.0] | 19.54 [19.19, 19.90] | 1.00 [1.00, 1.00] | 94.7 [93.4, 96.0] | 6.72 [6.70, 6.73] | 93.2 [91.9, 94.6] | 2.37 [2.16, 2.59] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 48.3 [42.8, 54.4] | 0.76 [0.75, 0.76] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 5.8 [5.1, 6.3] | 53.7 [47.1, 62.7] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | — | — |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 84.1 [84.1, 84.1].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 97.5 [97.5, 97.5] | 78.7 [78.7, 78.7] | 78.0 [77.5, 78.5] | 76.4 [75.5, 77.2] | 73.2 [71.8, 74.5] | 5.5 [4.2, 7.0] | — |
| T-oraculo | 86.2 [86.2, 86.2] | 43.8 [43.8, 43.8] | 43.8 [43.8, 43.8] | 43.8 [43.8, 43.8] | 43.6 [43.4, 43.8] | 0.1 [0.0, 0.4] | — |
| T-protocolo | 63.7 [63.7, 63.7] | 41.2 [41.2, 41.2] | 41.2 [41.2, 41.2] | 41.2 [41.2, 41.2] | 41.1 [40.9, 41.2] | 0.1 [0.0, 0.4] | 100.0 [100.0, 100.0] |

## N = 50 (800 registros por clase; monolítica 6400)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.5 [97.3, 97.7] | 97.2 [96.9, 97.5] | 97.2 [96.9, 97.5] | 26.57 [26.52, 26.61] | 0.98 [0.98, 0.98] | 97.5 [97.3, 97.7] | 8.81 [8.81, 8.81] | — | 1.48 [1.46, 1.51] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 20.38 [20.31, 20.45] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 8.50 [8.50, 8.50] | 100.0 [100.0, 100.0] | 1.10 [1.08, 1.11] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.7 [98.1, 99.2] | 98.1 [97.7, 98.5] | 98.1 [97.7, 98.5] | 98.1 [97.7, 98.5] | 20.81 [20.72, 20.92] | 1.00 [1.00, 1.00] | 98.1 [97.7, 98.5] | 8.49 [8.48, 8.51] | 96.8 [96.3, 97.4] | 1.64 [1.54, 1.75] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 47.8 [42.2, 53.3] | 0.74 [0.74, 0.75] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 4.1 [4.1, 4.2] | 70.0 [58.6, 80.0] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | — | — |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 88.4 [88.4, 88.4].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 95.0 [95.0, 95.0] | 93.9 [93.1, 94.5] | 92.0 [91.0, 92.9] | 87.3 [85.6, 88.9] | 7.5 [5.9, 9.2] | — |
| T-oraculo | 98.8 [98.8, 98.8] | 75.0 [75.0, 75.0] | 75.0 [75.0, 75.0] | 74.1 [73.5, 74.8] | 73.1 [72.5, 73.8] | 1.9 [1.2, 2.5] | — |
| T-protocolo | 77.5 [77.5, 77.5] | 67.5 [67.5, 67.5] | 67.5 [67.5, 67.5] | 66.6 [66.0, 67.2] | 66.0 [65.0, 66.9] | 1.5 [0.6, 2.5] | 100.0 [100.0, 100.0] |

## N = 100 (1600 registros por clase; monolítica 12800)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.6 [97.4, 97.8] | 97.1 [96.9, 97.2] | 97.2 [97.0, 97.4] | 29.40 [29.31, 29.50] | 0.98 [0.98, 0.98] | 97.5 [97.3, 97.7] | 10.01 [10.01, 10.01] | — | 1.32 [1.31, 1.34] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 23.35 [23.24, 23.46] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 9.63 [9.63, 9.63] | 100.0 [100.0, 100.0] | 1.06 [1.06, 1.07] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.7 [98.1, 99.2] | 98.1 [97.7, 98.5] | 98.1 [97.7, 98.5] | 98.1 [97.7, 98.5] | 23.75 [23.59, 23.93] | 1.00 [1.00, 1.00] | 98.1 [97.7, 98.5] | 9.62 [9.60, 9.63] | 96.8 [96.3, 97.4] | 1.42 [1.34, 1.49] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 52.2 [47.8, 57.2] | 0.77 [0.76, 0.77] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 4.1 [4.1, 4.2] | 70.0 [58.6, 80.0] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 12.5 [12.5, 12.5] | 12.5 [12.5, 12.5] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | — | — |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 88.4 [88.4, 88.4].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 98.8 [98.8, 98.8] | 96.7 [95.7, 97.8] | 93.6 [91.9, 95.2] | 88.2 [86.2, 90.2] | 10.5 [8.5, 12.5] | — |
| T-oraculo | 98.8 [98.8, 98.8] | 92.5 [92.5, 92.5] | 92.5 [92.5, 92.5] | 91.1 [90.5, 91.8] | 89.8 [88.8, 90.8] | 2.6 [1.7, 3.5] | — |
| T-protocolo | 80.0 [80.0, 80.0] | 78.7 [78.7, 78.7] | 78.7 [78.7, 78.7] | 77.1 [76.5, 77.8] | 75.5 [74.6, 76.2] | 3.1 [2.4, 4.0] | 100.0 [100.0, 100.0] |

## N = 200 (3200 registros por clase; monolítica 25600)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 96.9 [96.7, 97.1] | 96.9 [96.7, 97.1] | 96.9 [96.7, 97.2] | 32.53 [32.45, 32.60] | 0.98 [0.98, 0.98] | 96.9 [96.6, 97.1] | 10.94 [10.94, 10.94] | — | 1.28 [1.26, 1.29] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 26.78 [26.66, 26.91] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 10.55 [10.55, 10.55] | 100.0 [100.0, 100.0] | 1.04 [1.03, 1.05] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.7 [98.1, 99.1] | 98.2 [97.9, 98.5] | 98.2 [97.9, 98.5] | 98.2 [97.9, 98.5] | 27.18 [27.06, 27.32] | 1.00 [1.00, 1.00] | 98.2 [97.9, 98.5] | 10.54 [10.52, 10.56] | 96.8 [96.3, 97.4] | 1.30 [1.26, 1.35] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 51.1 [45.0, 56.7] | 0.75 [0.75, 0.76] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 4.1 [4.1, 4.2] | 71.4 [61.4, 80.0] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 20.0 [20.0, 20.0] | 20.0 [20.0, 20.0] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | — | — |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 87.6 [87.6, 87.6].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 97.5 [96.5, 98.4] | 93.6 [91.5, 95.6] | 89.1 [87.2, 91.2] | 10.9 [8.8, 12.8] | — |
| T-oraculo | 98.8 [98.8, 98.8] | 97.5 [97.5, 97.5] | 97.5 [97.5, 97.5] | 95.7 [95.0, 96.5] | 93.4 [92.0, 94.8] | 4.1 [2.8, 5.5] | — |
| T-protocolo | 81.2 [81.2, 81.2] | 81.2 [81.2, 81.2] | 81.2 [81.2, 81.2] | 79.2 [78.6, 79.9] | 78.0 [76.8, 79.1] | 3.1 [2.1, 4.3] | 100.0 [100.0, 100.0] |

## Qué operaciones de la MAE usa cada brazo

Ningún brazo tiene reglas propias: todos pasan por las mismas operaciones de la memoria.

| paso | M | T-oráculo | T-protocolo | dónde |
|---|---|---|---|---|
| llenado | `register` de una hetero con las 8 clases | `register` por clase | igual que T-oráculo | `stage5_fill.fill_agent`, `run_experiment11_monolithic.build_*` |
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