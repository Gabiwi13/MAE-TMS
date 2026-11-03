# exp11, T-protocolo corregido: comparación

Pares (semilla, corte) completos en el raw nuevo: 1 de 40 (s43 N=25). Las tablas lado a lado usan solo esos pares; la estadística pareada usa todas las (semilla, consulta, sorteo) con raw nuevo. Tablas con los tres brazos: `tablas_viejas/README.md` (todo lo oficial; debe coincidir con el README de exp11), `tablas_viejas_mismos_pares/README.md` y `tablas_nuevas/README.md`.

## T-protocolo: viejo contra corregido

Media entre semillas e IC 95 % bootstrap. «sobre respondidas» es la métrica del README de exp11; M y T-oráculo no cambian (mismas filas).

### N = 25

| medida | viejo | corregido |
|---|---|---|
| acepta | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| responde | 98.8 [98.8, 98.8] | 99.4 [99.4, 99.4] |
| ruteo ok | 95.9 [95.9, 95.9] | 97.1 [97.1, 97.1] |
| clase 1-NN (sobre respondidas) | 97.0 [97.0, 97.0] | 97.6 [97.6, 97.6] |
| centroide | 97.0 [97.0, 97.0] | 97.6 [97.6, 97.6] |
| clasificador | 97.0 [97.0, 97.0] | 97.6 [97.6, 97.6] |
| d_nn | 18.94 [18.94, 18.94] | 18.72 [18.72, 18.72] |
| compat máx | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| compat ok | 97.0 [97.0, 97.0] | 97.6 [97.6, 97.6] |
| niveles vivos | 6.71 [6.71, 6.71] | 6.71 [6.71, 6.71] |
| fracción pista compartida | 4.7 [4.7, 4.7] | 4.7 [4.7, 4.7] |
| clase 1-NN con pista compartida | 62.5 [62.5, 62.5] | 50.0 [50.0, 50.0] |
| F | 2.01 [2.01, 2.01] | 1.81 [1.81, 1.81] |
| fuera de dominio, acepta | 10.0 [10.0, 10.0] | — |
| fuera de dominio, con compuerta | 5.0 [5.0, 5.0] | — |
| formación: registradas / rechazadas / acierto temprano | 233.00 [233.00, 233.00] / 7.00 [7.00, 7.00] / 84.1 [84.1, 84.1] | 233.00 [233.00, 233.00] / 7.00 [7.00, 7.00] / 84.1 [84.1, 84.1] |
| imagen: acepta | 63.7 [63.7, 63.7] | 63.7 [63.7, 63.7] |
| imagen: responde | 41.2 [41.2, 41.2] | 41.2 [41.2, 41.2] |
| imagen: hit laxo | 41.2 [41.2, 41.2] | 41.2 [41.2, 41.2] |
| imagen: hit estricto | 40.0 [40.0, 40.0] | 41.2 [41.2, 41.2] |
| imagen: dominio ok | 40.0 [40.0, 40.0] | 41.2 [41.2, 41.2] |
| imagen: otro dominio | 1.2 [1.2, 1.2] | 0.0 [0.0, 0.0] |
| imagen: ruteo ok | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |

## Clase correcta sobre el total (no respuesta = fallo)

Consultas reservadas × 3 sorteos por semilla (las mismas en todos los brazos); media entre semillas e IC 95 % bootstrap.

| N | juez | M | T-oráculo | P viejo | P corregido |
|---|---|---|---|---|---|
| 25 | nn_ok | 98.2 [98.2, 98.2] | 100.0 [100.0, 100.0] | 95.9 [95.9, 95.9] | 97.1 [97.1, 97.1] |
| 25 | centroide_ok | 97.7 [97.7, 97.7] | 100.0 [100.0, 100.0] | 95.9 [95.9, 95.9] | 97.1 [97.1, 97.1] |
| 25 | clf_ok | 98.2 [98.2, 98.2] | 100.0 [100.0, 100.0] | 95.9 [95.9, 95.9] | 97.1 [97.1, 97.1] |
| 200 | nn_ok | 97.7 [97.7, 97.7] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| 200 | centroide_ok | 97.1 [97.1, 97.1] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |
| 200 | clf_ok | 96.6 [96.6, 96.6] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] |

## McNemar exacto, T-protocolo contra M (clase correcta sobre el total)

Pares (semilla, consulta, sorteo). b: M acierta y P no; c: P acierta y M no. Los sorteos de una misma consulta no son independientes, así que este p es optimista; el bootstrap por consulta (cada consulta con la media de sus pares entre semillas y sorteos) es la prueba conservadora.

| N | juez | lado | pares | b | c | P − M | p | bootstrap por consulta | semillas con p < 0.05 (P arriba / M arriba) |
|---|---|---|---|---|---|---|---|---|---|
| 25 | nn_ok | viejo | 513 | 21 | 9 | -2.34 | 0.0428 | -2.34 [-5.85, +0.97] | 0 / 1 de 1 |
| 25 | nn_ok | corregido | 513 | 15 | 9 | -1.17 | 0.307 | -1.17 [-4.29, +1.95] | 0 / 0 de 1 |
| 25 | centroide_ok | viejo | 513 | 18 | 9 | -1.75 | 0.122 | -1.75 [-5.26, +1.75] | 0 / 0 de 1 |
| 25 | centroide_ok | corregido | 513 | 12 | 9 | -0.58 | 0.664 | -0.58 [-3.51, +2.34] | 0 / 0 de 1 |
| 25 | clf_ok | viejo | 513 | 18 | 6 | -2.34 | 0.0227 | -2.34 [-5.65, +0.58] | 0 / 1 de 1 |
| 25 | clf_ok | corregido | 513 | 12 | 6 | -1.17 | 0.238 | -1.17 [-3.90, +1.36] | 0 / 0 de 1 |
| 200 | nn_ok | viejo | 174 | 0 | 4 | +2.30 | 0.125 | +2.30 [+0.00, +6.32] | 0 / 0 de 1 |
| 200 | nn_ok | corregido | 174 | 0 | 4 | +2.30 | 0.125 | +2.30 [+0.00, +6.32] | 0 / 0 de 1 |
| 200 | centroide_ok | viejo | 174 | 0 | 5 | +2.87 | 0.0625 | +2.87 [+0.00, +6.90] | 0 / 0 de 1 |
| 200 | centroide_ok | corregido | 174 | 0 | 5 | +2.87 | 0.0625 | +2.87 [+0.00, +6.90] | 0 / 0 de 1 |
| 200 | clf_ok | viejo | 174 | 0 | 6 | +3.45 | 0.0312 | +3.45 [+0.00, +8.05] | 1 / 0 de 1 |
| 200 | clf_ok | corregido | 174 | 0 | 6 | +3.45 | 0.0312 | +3.45 [+0.00, +8.05] | 1 / 0 de 1 |

## d_nn contra la EHAM única, pareado por consulta

Por consulta: media de d_nn de cada brazo sobre sus respuestas (semillas × sorteos); diferencia brazo − M y bootstrap remuestreando consultas. Negativo: el brazo recuerda más cerca de una instancia real de la clase.

| N | brazo | consultas | brazo − M [IC 95 %] |
|---|---|---|---|
| 25 | P viejo | 169 | -3.84 [-4.71, -2.97] |
| 25 | P corregido | 170 | -4.04 [-4.81, -3.29] |
| 25 | T-oráculo | 171 | -4.53 [-5.27, -3.84] |
| 200 | P viejo | 58 | -5.52 [-7.26, -3.82] |
| 200 | P corregido | 58 | -5.71 [-7.62, -3.86] |
| 200 | T-oráculo | 58 | -6.62 [-8.43, -4.89] |

## Diagnóstico del arreglo

- Entradas con círculo variable entre trozos (consultas resueltas sin saltos): viejo en 3 de 40 pares (semilla, corte); corregido en 0 de 2.

Coincidencia del ruteo viejo con el corregido (texto: destino y tamaño del círculo, sorteo 0; imagen: destino; fuera de dominio: acepta, compuerta y destino):

| semilla | corte | texto distintas / consultas | trozos con diferencias | imagen distintas / n | fuera de dominio distintas / n |
|---|---|---|---|---|---|
| 43 | 25 | 9 / 171 | [4] | 0 / 80 | 0 / 12 |
| 43 | 200 | 0 / 58 | [] | 0 / 0 | 0 / 12 |

## Fuera de dominio aceptadas por T-protocolo (semillas que aceptan / con compuerta)


## Tiempo por trabajo (corrida corregida)

| tipo y corte | trabajos | media (s) | suma (h) |
|---|---|---|---|
| c|N=200 | 2 | 409 | 0.23 |
| c|N=25 | 6 | 149 | 0.25 |
| i|N=25 | 6 | 55 | 0.09 |
