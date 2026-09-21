# Experimento 11 — MAE monolítica contra sistema transactivo

Semillas: [42, 43, 44, 45, 46, 47, 48, 49, 50, 51]. Cortes N (imágenes por clase, ×4 variantes): [200]. Intervalos: bootstrap del 95% sobre las medias por semilla. Banco: las consultas reservadas (no usadas para formar directorios), para los tres brazos. Diseño y criterio de refutación en `propuesta_fase5_mae_monolitica.md`.

Control del llenado en N=200: especialistas reconstruidos idénticos a los `agent_*.pkl` oficiales (8/8 clases).

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

Fuera de dominio (12 consultas de `run_rejection_probe`): tasa de aceptación.

| brazo | acepta |
|---|---|
| M | 25.0 [25.0, 25.0] |
| T-oraculo | 16.7 [16.7, 16.7] |
| T-protocolo | 16.7 [16.7, 16.7] |

Formación de directorios (T-protocolo): registradas 233.00 [233.00, 233.00], rechazadas 7.00 [7.00, 7.00], acierto temprano 85.4 [85.4, 85.4].

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