# Experimento 11 — MAE monolítica contra sistema transactivo

Semillas: [43]. Cortes N (imágenes por clase, ×16 variantes): [25]. Intervalos: bootstrap del 95% sobre las medias por semilla. Banco: las consultas reservadas (no usadas para formar directorios), para los tres brazos. Diseño y criterio de refutación en `propuesta_fase5_mae_monolitica.md`.

## N = 25 (400 registros por clase; monolítica 3200)

| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 98.2 [98.2, 98.2] | 97.7 [97.7, 97.7] | 98.2 [98.2, 98.2] | 22.76 [22.76, 22.76] | 0.98 [0.98, 0.98] | 98.1 [98.1, 98.1] | 7.03 [7.03, 7.03] | — | 1.76 [1.76, 1.76] |
| T-oraculo | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 18.23 [18.23, 18.23] | 1.00 [1.00, 1.00] | 100.0 [100.0, 100.0] | 6.76 [6.76, 6.76] | 100.0 [100.0, 100.0] | 1.21 [1.21, 1.21] |
| T-protocolo | 100.0 [100.0, 100.0] | 98.8 [98.8, 98.8] | 97.0 [97.0, 97.0] | 97.0 [97.0, 97.0] | 97.0 [97.0, 97.0] | 18.94 [18.94, 18.94] | 1.00 [1.00, 1.00] | 97.0 [97.0, 97.0] | 6.71 [6.71, 6.71] | 95.9 [95.9, 95.9] | 2.01 [2.01, 2.01] |

Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:

| brazo | fracción de respuestas | clase 1-NN | compat máx |
|---|---|---|---|
| M | 3.5 [3.5, 3.5] | 66.7 [66.7, 66.7] | 0.76 [0.76, 0.76] |
| T-oraculo | 3.5 [3.5, 3.5] | 100.0 [100.0, 100.0] | 1.00 [1.00, 1.00] |
| T-protocolo | 4.7 [4.7, 4.7] | 62.5 [62.5, 62.5] | 1.00 [1.00, 1.00] |

Fuera de dominio (40 consultas): tasa de aceptación. «Con compuerta»: el agente destino además debe contener la pista (en M y oráculo coincide con la aceptación).

| brazo | acepta | acepta con compuerta |
|---|---|---|
| M | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-oraculo | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| T-protocolo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 84.1 [84.1, 84.1].

Imagen → texto. Laxo: alguna de las 3 etiquetas evocadas está en el vocabulario del dominio (etapa 7). Estricto: alguna es exclusiva de la clase. Dominio: mayoría de etiquetas exclusivas; 'otro dominio' cuenta las respuestas cuyo dominio es otra clase. Todo sobre el total de imágenes.

| brazo | acepta | responde | hit laxo | hit estricto | dominio ok | otro dominio | ruteo ok |
|---|---|---|---|---|---|---|---|
| M | 97.5 [97.5, 97.5] | 78.8 [78.8, 78.8] | 78.8 [78.8, 78.8] | 75.0 [75.0, 75.0] | 72.5 [72.5, 72.5] | 6.2 [6.2, 6.2] | — |
| T-oraculo | 86.2 [86.2, 86.2] | 43.8 [43.8, 43.8] | 43.8 [43.8, 43.8] | 43.8 [43.8, 43.8] | 43.8 [43.8, 43.8] | 0.0 [0.0, 0.0] | — |
| T-protocolo | 63.7 [63.7, 63.7] | 41.2 [41.2, 41.2] | 41.2 [41.2, 41.2] | 40.0 [40.0, 40.0] | 40.0 [40.0, 40.0] | 1.2 [1.2, 1.2] | 100.0 [100.0, 100.0] |

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