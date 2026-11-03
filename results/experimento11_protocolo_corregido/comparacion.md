# exp11, T-protocolo corregido: comparación

Pares (semilla, corte) completos en el raw nuevo: 40 de 40 (s42 N=25, s42 N=50, s42 N=100, s42 N=200, s43 N=25, s43 N=50, s43 N=100, s43 N=200, s44 N=25, s44 N=50, s44 N=100, s44 N=200, s45 N=25, s45 N=50, s45 N=100, s45 N=200, s46 N=25, s46 N=50, s46 N=100, s46 N=200, s47 N=25, s47 N=50, s47 N=100, s47 N=200, s48 N=25, s48 N=50, s48 N=100, s48 N=200, s49 N=25, s49 N=50, s49 N=100, s49 N=200, s50 N=25, s50 N=50, s50 N=100, s50 N=200, s51 N=25, s51 N=50, s51 N=100, s51 N=200). Las tablas lado a lado usan solo esos pares; la estadística pareada usa todas las (semilla, consulta, sorteo) con raw nuevo. Tablas con los tres brazos: `tablas_viejas/README.md` (todo lo oficial; debe coincidir con el README de exp11), `tablas_viejas_mismos_pares/README.md` y `tablas_nuevas/README.md`.

## T-protocolo: viejo contra corregido

Media entre semillas e IC 95 % bootstrap. «sobre respondidas» es la métrica del README de exp11; M y T-oráculo no cambian (mismas filas).

### N = 25

| medida | viejo | corregido |
|---|---|---|
| acepta | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| responde | 98.4 [98.2, 98.7] | 98.4 [97.7, 98.9] |
| ruteo ok | 95.3 [94.6, 96.1] | 93.2 [91.9, 94.6] |
| clase 1-NN (sobre respondidas) | 96.9 [96.3, 97.6] | 94.7 [93.4, 96.0] |
| centroide | 96.9 [96.3, 97.6] | 94.7 [93.4, 96.0] |
| clasificador | 96.9 [96.3, 97.6] | 94.7 [93.4, 96.0] |
| d_nn | 18.97 [18.80, 19.13] | 19.54 [19.19, 19.90] |
| compat máx | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| compat ok | 96.9 [96.3, 97.6] | 94.7 [93.4, 96.0] |
| niveles vivos | 6.73 [6.72, 6.73] | 6.72 [6.70, 6.73] |
| fracción pista compartida | 4.5 [4.2, 4.9] | 5.8 [5.1, 6.3] |
| clase 1-NN con pista compartida | 80.3 [72.5, 85.7] | 53.7 [47.1, 62.7] |
| F | 2.02 [1.83, 2.19] | 2.37 [2.16, 2.59] |
| fuera de dominio, acepta | 10.0 [10.0, 10.0] | — |
| fuera de dominio, con compuerta | 5.0 [5.0, 5.0] | — |
| formación: registradas / rechazadas / acierto temprano | 233.00 [233.00, 233.00] / 7.00 [7.00, 7.00] / 84.1 [84.1, 84.1] | 233.00 [233.00, 233.00] / 7.00 [7.00, 7.00] / 84.1 [84.1, 84.1] |
| imagen: acepta | 63.7 [63.7, 63.7] | 63.7 [63.7, 63.7] |
| imagen: responde | 41.2 [41.2, 41.2] | 41.2 [41.2, 41.2] |
| imagen: hit laxo | 41.2 [41.2, 41.2] | 41.2 [41.2, 41.2] |
| imagen: hit estricto | 41.1 [40.9, 41.2] | 41.2 [41.2, 41.2] |
| imagen: dominio ok | 41.0 [40.6, 41.2] | 41.1 [40.9, 41.2] |
| imagen: otro dominio | 0.2 [0.0, 0.6] | 0.1 [0.0, 0.4] |
| imagen: ruteo ok | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |

### N = 50

| medida | viejo | corregido |
|---|---|---|
| acepta | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| responde | 98.7 [98.4, 98.9] | 98.7 [98.1, 99.2] |
| ruteo ok | 97.4 [97.1, 97.8] | 96.8 [96.3, 97.4] |
| clase 1-NN (sobre respondidas) | 98.8 [98.6, 98.9] | 98.1 [97.7, 98.5] |
| centroide | 98.8 [98.6, 98.9] | 98.1 [97.7, 98.5] |
| clasificador | 98.8 [98.6, 98.9] | 98.1 [97.7, 98.5] |
| d_nn | 20.67 [20.59, 20.76] | 20.81 [20.72, 20.92] |
| compat máx | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| compat ok | 98.8 [98.6, 98.9] | 98.1 [97.7, 98.5] |
| niveles vivos | 8.49 [8.48, 8.49] | 8.49 [8.48, 8.51] |
| fracción pista compartida | 4.1 [4.1, 4.2] | 4.1 [4.1, 4.2] |
| clase 1-NN con pista compartida | 82.9 [78.6, 85.7] | 70.0 [58.6, 80.0] |
| F | 1.42 [1.36, 1.48] | 1.64 [1.54, 1.75] |
| fuera de dominio, acepta | 10.0 [10.0, 10.0] | — |
| fuera de dominio, con compuerta | 5.0 [5.0, 5.0] | — |
| formación: registradas / rechazadas / acierto temprano | 233.00 [233.00, 233.00] / 7.00 [7.00, 7.00] / 88.4 [88.4, 88.4] | 233.00 [233.00, 233.00] / 7.00 [7.00, 7.00] / 88.4 [88.4, 88.4] |
| imagen: acepta | 77.5 [77.5, 77.5] | 77.5 [77.5, 77.5] |
| imagen: responde | 67.5 [67.5, 67.5] | 67.5 [67.5, 67.5] |
| imagen: hit laxo | 67.5 [67.5, 67.5] | 67.5 [67.5, 67.5] |
| imagen: hit estricto | 67.4 [67.1, 67.5] | 66.6 [66.0, 67.2] |
| imagen: dominio ok | 65.8 [65.0, 66.4] | 66.0 [65.0, 66.9] |
| imagen: otro dominio | 1.8 [1.1, 2.5] | 1.5 [0.6, 2.5] |
| imagen: ruteo ok | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |

### N = 100

| medida | viejo | corregido |
|---|---|---|
| acepta | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| responde | 98.7 [98.4, 98.9] | 98.7 [98.1, 99.2] |
| ruteo ok | 97.4 [97.0, 97.8] | 96.8 [96.3, 97.4] |
| clase 1-NN (sobre respondidas) | 98.8 [98.4, 99.1] | 98.1 [97.7, 98.5] |
| centroide | 98.8 [98.4, 99.1] | 98.1 [97.7, 98.5] |
| clasificador | 98.8 [98.4, 99.1] | 98.1 [97.7, 98.5] |
| d_nn | 23.78 [23.66, 23.88] | 23.75 [23.59, 23.93] |
| compat máx | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| compat ok | 98.8 [98.4, 99.1] | 98.1 [97.7, 98.5] |
| niveles vivos | 9.63 [9.62, 9.63] | 9.62 [9.60, 9.63] |
| fracción pista compartida | 4.1 [4.1, 4.2] | 4.1 [4.1, 4.2] |
| clase 1-NN con pista compartida | 84.3 [81.4, 85.7] | 70.0 [58.6, 80.0] |
| F | 1.28 [1.21, 1.34] | 1.42 [1.34, 1.49] |
| fuera de dominio, acepta | 10.0 [10.0, 10.0] | — |
| fuera de dominio, con compuerta | 5.0 [5.0, 5.0] | — |
| formación: registradas / rechazadas / acierto temprano | 233.00 [233.00, 233.00] / 7.00 [7.00, 7.00] / 88.4 [88.4, 88.4] | 233.00 [233.00, 233.00] / 7.00 [7.00, 7.00] / 88.4 [88.4, 88.4] |
| imagen: acepta | 80.0 [80.0, 80.0] | 80.0 [80.0, 80.0] |
| imagen: responde | 78.7 [78.7, 78.7] | 78.7 [78.7, 78.7] |
| imagen: hit laxo | 78.7 [78.7, 78.7] | 78.7 [78.7, 78.7] |
| imagen: hit estricto | 77.5 [76.8, 78.2] | 77.1 [76.5, 77.8] |
| imagen: dominio ok | 76.5 [75.6, 77.4] | 75.5 [74.6, 76.2] |
| imagen: otro dominio | 2.2 [1.4, 3.1] | 3.1 [2.4, 4.0] |
| imagen: ruteo ok | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |

### N = 200

| medida | viejo | corregido |
|---|---|---|
| acepta | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| responde | 98.7 [98.5, 98.9] | 98.7 [98.1, 99.1] |
| ruteo ok | 97.0 [96.6, 97.4] | 96.8 [96.3, 97.4] |
| clase 1-NN (sobre respondidas) | 98.3 [97.9, 98.6] | 98.2 [97.9, 98.5] |
| centroide | 98.3 [97.9, 98.6] | 98.2 [97.9, 98.5] |
| clasificador | 98.3 [97.9, 98.6] | 98.2 [97.9, 98.5] |
| d_nn | 26.98 [26.86, 27.09] | 27.18 [27.06, 27.32] |
| compat máx | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| compat ok | 98.3 [97.9, 98.6] | 98.2 [97.9, 98.5] |
| niveles vivos | 10.54 [10.53, 10.55] | 10.54 [10.52, 10.56] |
| fracción pista compartida | 4.1 [4.1, 4.2] | 4.1 [4.1, 4.2] |
| clase 1-NN con pista compartida | 78.6 [68.6, 85.7] | 71.4 [61.4, 80.0] |
| F | 1.25 [1.21, 1.30] | 1.30 [1.26, 1.35] |
| fuera de dominio, acepta | 10.0 [10.0, 10.0] | — |
| fuera de dominio, con compuerta | 5.0 [5.0, 5.0] | — |
| formación: registradas / rechazadas / acierto temprano | 233.00 [233.00, 233.00] / 7.00 [7.00, 7.00] / 87.6 [87.6, 87.6] | 233.00 [233.00, 233.00] / 7.00 [7.00, 7.00] / 87.6 [87.6, 87.6] |
| imagen: acepta | 81.2 [81.2, 81.2] | 81.2 [81.2, 81.2] |
| imagen: responde | 81.2 [81.2, 81.2] | 81.2 [81.2, 81.2] |
| imagen: hit laxo | 81.2 [81.2, 81.2] | 81.2 [81.2, 81.2] |
| imagen: hit estricto | 79.8 [78.9, 80.6] | 79.2 [78.6, 79.9] |
| imagen: dominio ok | 78.1 [77.0, 79.2] | 78.0 [76.8, 79.1] |
| imagen: otro dominio | 3.0 [1.9, 4.0] | 3.1 [2.1, 4.3] |
| imagen: ruteo ok | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |

## Clase correcta sobre el total (no respuesta = fallo)

Consultas reservadas × 3 sorteos por semilla (las mismas en todos los brazos); media entre semillas e IC 95 % bootstrap.

| N | juez | M | T-oráculo | P viejo | P corregido |
|---|---|---|---|---|---|
| 25 | nn_ok | 97.6 [97.4, 97.8] | 100.0 [100.0, 100.0] | 95.3 [94.6, 96.1] | 93.2 [91.9, 94.6] |
| 25 | centroide_ok | 97.4 [97.3, 97.6] | 100.0 [100.0, 100.0] | 95.3 [94.6, 96.1] | 93.2 [91.9, 94.6] |
| 25 | clf_ok | 97.7 [97.4, 97.9] | 100.0 [100.0, 100.0] | 95.3 [94.6, 96.1] | 93.2 [91.9, 94.6] |
| 50 | nn_ok | 97.5 [97.3, 97.7] | 100.0 [100.0, 100.0] | 97.4 [97.1, 97.8] | 96.8 [96.3, 97.4] |
| 50 | centroide_ok | 97.2 [96.9, 97.5] | 100.0 [100.0, 100.0] | 97.4 [97.1, 97.8] | 96.8 [96.3, 97.4] |
| 50 | clf_ok | 97.2 [96.9, 97.5] | 100.0 [100.0, 100.0] | 97.4 [97.1, 97.8] | 96.8 [96.3, 97.4] |
| 100 | nn_ok | 97.6 [97.4, 97.8] | 100.0 [100.0, 100.0] | 97.4 [97.0, 97.8] | 96.8 [96.3, 97.4] |
| 100 | centroide_ok | 97.1 [96.9, 97.2] | 100.0 [100.0, 100.0] | 97.4 [97.0, 97.8] | 96.8 [96.3, 97.4] |
| 100 | clf_ok | 97.2 [97.0, 97.4] | 100.0 [100.0, 100.0] | 97.4 [97.0, 97.8] | 96.8 [96.3, 97.4] |
| 200 | nn_ok | 96.9 [96.7, 97.1] | 100.0 [100.0, 100.0] | 97.0 [96.6, 97.4] | 96.8 [96.3, 97.4] |
| 200 | centroide_ok | 96.9 [96.7, 97.1] | 100.0 [100.0, 100.0] | 97.0 [96.6, 97.4] | 96.8 [96.3, 97.4] |
| 200 | clf_ok | 96.9 [96.7, 97.2] | 100.0 [100.0, 100.0] | 97.0 [96.6, 97.4] | 96.8 [96.3, 97.4] |

## McNemar exacto, T-protocolo contra M (clase correcta sobre el total)

Pares (semilla, consulta, sorteo). b: M acierta y P no; c: P acierta y M no. Los sorteos de una misma consulta no son independientes, así que este p es optimista; el bootstrap por consulta (cada consulta con la media de sus pares entre semillas y sorteos) es la prueba conservadora.

| N | juez | lado | pares | b | c | P − M | p | bootstrap por consulta | semillas con p < 0.05 (P arriba / M arriba) |
|---|---|---|---|---|---|---|---|---|---|
| 25 | nn_ok | viejo | 5130 | 240 | 123 | -2.28 | 8.21e-10 | -2.28 [-5.87, +1.13] | 0 / 5 de 10 |
| 25 | nn_ok | corregido | 5130 | 347 | 119 | -4.44 | 6.48e-27 | -4.44 [-8.17, -0.94] | 0 / 7 de 10 |
| 25 | centroide_ok | viejo | 5130 | 237 | 128 | -2.12 | 1.24e-08 | -2.12 [-5.65, +1.23] | 0 / 3 de 10 |
| 25 | centroide_ok | corregido | 5130 | 340 | 120 | -4.29 | 2.02e-25 | -4.29 [-7.93, -0.86] | 0 / 7 de 10 |
| 25 | clf_ok | viejo | 5130 | 237 | 116 | -2.36 | 1.12e-10 | -2.36 [-5.85, +0.92] | 0 / 6 de 10 |
| 25 | clf_ok | corregido | 5130 | 343 | 111 | -4.52 | 1.28e-28 | -4.52 [-8.09, -1.15] | 0 / 7 de 10 |
| 50 | nn_ok | viejo | 5130 | 129 | 125 | -0.08 | 0.851 | -0.08 [-2.98, +2.77] | 0 / 0 de 10 |
| 50 | nn_ok | corregido | 5130 | 145 | 111 | -0.66 | 0.039 | -0.66 [-3.29, +1.97] | 0 / 1 de 10 |
| 50 | centroide_ok | viejo | 5130 | 127 | 139 | +0.23 | 0.5 | +0.23 [-2.71, +3.06] | 0 / 0 de 10 |
| 50 | centroide_ok | corregido | 5130 | 138 | 120 | -0.35 | 0.29 | -0.35 [-2.88, +2.11] | 0 / 0 de 10 |
| 50 | clf_ok | viejo | 5130 | 129 | 139 | +0.19 | 0.583 | +0.19 [-2.71, +2.96] | 0 / 0 de 10 |
| 50 | clf_ok | corregido | 5130 | 143 | 123 | -0.39 | 0.244 | -0.39 [-2.94, +2.07] | 0 / 0 de 10 |
| 100 | nn_ok | viejo | 5130 | 132 | 124 | -0.16 | 0.662 | -0.16 [-3.10, +2.71] | 0 / 0 de 10 |
| 100 | nn_ok | corregido | 5130 | 146 | 108 | -0.74 | 0.0201 | -0.74 [-3.45, +1.95] | 0 / 1 de 10 |
| 100 | centroide_ok | viejo | 5130 | 131 | 150 | +0.37 | 0.283 | +0.37 [-2.59, +3.20] | 0 / 0 de 10 |
| 100 | centroide_ok | corregido | 5130 | 139 | 128 | -0.21 | 0.541 | -0.21 [-2.83, +2.34] | 0 / 1 de 10 |
| 100 | clf_ok | viejo | 5130 | 132 | 144 | +0.23 | 0.508 | +0.23 [-2.67, +2.98] | 0 / 0 de 10 |
| 100 | clf_ok | corregido | 5130 | 144 | 126 | -0.35 | 0.301 | -0.35 [-2.98, +2.16] | 0 / 1 de 10 |
| 200 | nn_ok | viejo | 5130 | 146 | 151 | +0.10 | 0.817 | +0.10 [-2.90, +3.14] | 0 / 0 de 10 |
| 200 | nn_ok | corregido | 5130 | 151 | 147 | -0.08 | 0.862 | -0.08 [-2.94, +2.83] | 0 / 0 de 10 |
| 200 | centroide_ok | viejo | 5130 | 145 | 151 | +0.12 | 0.771 | +0.12 [-2.83, +3.02] | 0 / 0 de 10 |
| 200 | centroide_ok | corregido | 5130 | 147 | 144 | -0.06 | 0.907 | -0.06 [-2.81, +2.69] | 0 / 1 de 10 |
| 200 | clf_ok | viejo | 5130 | 146 | 150 | +0.08 | 0.862 | +0.08 [-2.88, +3.02] | 0 / 0 de 10 |
| 200 | clf_ok | corregido | 5130 | 148 | 143 | -0.10 | 0.815 | -0.10 [-2.85, +2.69] | 0 / 1 de 10 |

## d_nn contra la EHAM única, pareado por consulta

Por consulta: media de d_nn de cada brazo sobre sus respuestas (semillas × sorteos); diferencia brazo − M y bootstrap remuestreando consultas. Negativo: el brazo recuerda más cerca de una instancia real de la clase.

| N | brazo | consultas | brazo − M [IC 95 %] |
|---|---|---|---|
| 25 | P viejo | 170 | -3.91 [-4.83, -3.02] |
| 25 | P corregido | 170 | -3.37 [-4.33, -2.43] |
| 25 | T-oráculo | 171 | -4.64 [-5.40, -3.94] |
| 50 | P viejo | 170 | -5.93 [-6.78, -5.14] |
| 50 | P corregido | 170 | -5.79 [-6.59, -5.01] |
| 50 | T-oráculo | 171 | -6.18 [-6.96, -5.45] |
| 100 | P viejo | 170 | -5.69 [-6.52, -4.90] |
| 100 | P corregido | 170 | -5.68 [-6.47, -4.92] |
| 100 | T-oráculo | 171 | -6.06 [-6.82, -5.30] |
| 200 | P viejo | 170 | -5.63 [-6.56, -4.71] |
| 200 | P corregido | 170 | -5.39 [-6.30, -4.49] |
| 200 | T-oráculo | 171 | -5.75 [-6.64, -4.86] |

## Diagnóstico del arreglo

- Entradas con círculo variable entre trozos (consultas resueltas sin saltos): viejo en 3 de 40 pares (semilla, corte); corregido en 0 de 40.

Coincidencia del ruteo viejo con el corregido (texto: destino y tamaño del círculo, sorteo 0; imagen: destino; fuera de dominio: acepta, compuerta y destino):

| semilla | corte | texto distintas / consultas | trozos con diferencias | imagen distintas / n | fuera de dominio distintas / n |
|---|---|---|---|---|---|
| 42 | 25 | 0 / 171 | [] | 0 / 80 | 0 / 12 |
| 42 | 50 | 0 / 171 | [] | 0 / 80 | 0 / 12 |
| 42 | 100 | 0 / 171 | [] | 0 / 80 | 0 / 12 |
| 42 | 200 | 0 / 171 | [] | 0 / 80 | 0 / 12 |
| 43 | 25 | 9 / 171 | [4] | 0 / 80 | 0 / 12 |
| 43 | 50 | 13 / 171 | [4, 5] | 0 / 80 | 0 / 12 |
| 43 | 100 | 8 / 171 | [4] | 0 / 80 | 0 / 12 |
| 43 | 200 | 0 / 171 | [] | 0 / 80 | 0 / 12 |
| 44 | 25 | 105 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 44 | 50 | 80 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 44 | 100 | 81 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 44 | 200 | 80 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 45 | 25 | 72 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 45 | 50 | 4 / 171 | [3, 4, 5] | 0 / 80 | 0 / 12 |
| 45 | 100 | 3 / 171 | [3, 4] | 0 / 80 | 0 / 12 |
| 45 | 200 | 4 / 171 | [3, 4, 5] | 0 / 80 | 0 / 12 |
| 46 | 25 | 69 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 46 | 50 | 44 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 46 | 100 | 45 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 46 | 200 | 45 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 47 | 25 | 68 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 47 | 50 | 8 / 171 | [0, 2, 3, 4] | 0 / 80 | 0 / 12 |
| 47 | 100 | 7 / 171 | [0, 2, 3, 4] | 0 / 80 | 0 / 12 |
| 47 | 200 | 26 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 48 | 25 | 63 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 48 | 50 | 42 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 48 | 100 | 43 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 48 | 200 | 42 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 49 | 25 | 42 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 49 | 50 | 20 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 49 | 100 | 20 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 49 | 200 | 21 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 50 | 25 | 111 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 50 | 50 | 48 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 50 | 100 | 48 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 50 | 200 | 48 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 51 | 25 | 107 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 51 | 50 | 73 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 51 | 100 | 75 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |
| 51 | 200 | 75 / 171 | [0, 1, 2, 3, 4, 5] | 0 / 80 | 0 / 12 |

## Fuera de dominio aceptadas por T-protocolo (semillas que aceptan / con compuerta)


## Tiempo por trabajo (corrida corregida)

| tipo y corte | trabajos | media (s) | suma (h) |
|---|---|---|---|
| c|N=100 | 60 | 218 | 3.64 |
| c|N=200 | 60 | 308 | 5.14 |
| c|N=25 | 60 | 293 | 4.88 |
| c|N=50 | 60 | 151 | 2.51 |
| i|N=100 | 60 | 181 | 3.02 |
| i|N=200 | 60 | 222 | 3.70 |
| i|N=25 | 60 | 49 | 0.81 |
| i|N=50 | 60 | 115 | 1.92 |
