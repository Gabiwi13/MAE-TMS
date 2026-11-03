# Experimento 11 — MAE monolítica contra sistema transactivo

Semillas: [42, 43, 44, 45, 46, 47, 48, 49, 50, 51]. Cortes N (imágenes por clase, ×16 variantes): [25, 50, 100, 200]. Intervalos: bootstrap del 95% sobre las medias por semilla. Banco: las consultas reservadas (no usadas para formar directorios), para los tres brazos. Diseño y criterio de refutación en `propuesta_fase5_mae_monolitica.md`.

Control del llenado en N=200: 4/8 clases idénticas a los `agent_*.pkl` oficiales; distintas: car 600 celdas, cow 600 celdas, dog 1200 celdas, horse 600 celdas (de 9,830,400 celdas por clase). Este script recalcula los latentes en GPU; una diferencia de redondeo puede mover una coordenada de un registro al nivel vecino.

## N = 25 (400 registros por clase; monolítica 3200)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | — | — | — | — | — | — | — | — | — | — | — |
| T-oraculo | — | — | — | — | — | — | — | — | — | — | — |
| T-protocolo | 100.0 [100.0, 100.0] | 98.4 [97.7, 98.9] | 94.7 [93.4, 96.0] | 94.7 [93.4, 96.0] | 94.7 [93.4, 96.0] | 19.54 [19.19, 19.90] | 1.00 [1.00, 1.00] | 94.7 [93.4, 96.0] | 6.72 [6.70, 6.73] | 93.2 [91.9, 94.6] | 2.37 [2.16, 2.59] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | — | — | — |
| T-oraculo | — | — | — |
| T-protocolo | 5.8 [5.1, 6.3] | 53.7 [47.1, 62.7] | 1.00 [1.00, 1.00] |

Fuera de dominio (12 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | — | — |
| T-oraculo | — | — |
| T-protocolo | 16.7 [16.7, 16.7] | 16.7 [16.7, 16.7] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 84.1 [84.1, 84.1].

## N = 50 (800 registros por clase; monolítica 6400)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | — | — | — | — | — | — | — | — | — | — | — |
| T-oraculo | — | — | — | — | — | — | — | — | — | — | — |
| T-protocolo | 100.0 [100.0, 100.0] | 98.7 [98.1, 99.2] | 98.1 [97.7, 98.5] | 98.1 [97.7, 98.5] | 98.1 [97.7, 98.5] | 20.81 [20.72, 20.92] | 1.00 [1.00, 1.00] | 98.1 [97.7, 98.5] | 8.49 [8.48, 8.51] | 96.8 [96.3, 97.4] | 1.64 [1.54, 1.75] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | — | — | — |
| T-oraculo | — | — | — |
| T-protocolo | 4.1 [4.1, 4.2] | 70.0 [58.6, 80.0] | 1.00 [1.00, 1.00] |

Fuera de dominio (12 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | — | — |
| T-oraculo | — | — |
| T-protocolo | 16.7 [16.7, 16.7] | 16.7 [16.7, 16.7] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 88.4 [88.4, 88.4].

## N = 100 (1600 registros por clase; monolítica 12800)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | — | — | — | — | — | — | — | — | — | — | — |
| T-oraculo | — | — | — | — | — | — | — | — | — | — | — |
| T-protocolo | 100.0 [100.0, 100.0] | 98.7 [98.1, 99.2] | 98.1 [97.7, 98.5] | 98.1 [97.7, 98.5] | 98.1 [97.7, 98.5] | 23.75 [23.59, 23.93] | 1.00 [1.00, 1.00] | 98.1 [97.7, 98.5] | 9.62 [9.60, 9.63] | 96.8 [96.3, 97.4] | 1.42 [1.34, 1.49] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | — | — | — |
| T-oraculo | — | — | — |
| T-protocolo | 4.1 [4.1, 4.2] | 70.0 [58.6, 80.0] | 1.00 [1.00, 1.00] |

Fuera de dominio (12 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | — | — |
| T-oraculo | — | — |
| T-protocolo | 16.7 [16.7, 16.7] | 16.7 [16.7, 16.7] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 88.4 [88.4, 88.4].

## N = 200 (3200 registros por clase; monolítica 25600)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | — | — | — | — | — | — | — | — | — | — | — |
| T-oraculo | — | — | — | — | — | — | — | — | — | — | — |
| T-protocolo | 100.0 [100.0, 100.0] | 98.7 [98.1, 99.1] | 98.2 [97.9, 98.5] | 98.2 [97.9, 98.5] | 98.2 [97.9, 98.5] | 27.18 [27.06, 27.32] | 1.00 [1.00, 1.00] | 98.2 [97.9, 98.5] | 10.54 [10.52, 10.56] | 96.8 [96.3, 97.4] | 1.30 [1.26, 1.35] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | — | — | — |
| T-oraculo | — | — | — |
| T-protocolo | 4.1 [4.1, 4.2] | 71.4 [61.4, 80.0] | 1.00 [1.00, 1.00] |

Fuera de dominio (12 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | — | — |
| T-oraculo | — | — |
| T-protocolo | 16.7 [16.7, 16.7] | 16.7 [16.7, 16.7] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 87.6 [87.6, 87.6].

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