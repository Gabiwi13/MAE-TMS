# Experimento 16 — leave-one-object-out

10 pliegues (objeto reservado [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), una semilla. Por pliegue: contenido con 200 imágenes de los 9 objetos restantes (16 variantes), fase A con 128 (16 variantes), umbral de energía. Bancos por pliegue: «nuevo» = 41 vistas del objeto reservado por clase (328); «conocido» = 41 vistas no usadas de los objetos que sí contribuyeron (328). Intervalos: bootstrap del 95 % sobre pliegues. Diseño en `propuesta_exp16_leave_object_out.md`.

| banco | contenido acepta | responde | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | hit estricto | otro dominio |
|---|---|---|---|---|---|---|---|---|
| objeto conocido | 95.2 [94.3, 96.1] | 87.0 [85.9, 88.2] | 92.5 [91.2, 93.5] | 88.1 [86.8, 89.4] | 11.0 [9.8, 12.2] | 76.3 [74.7, 77.7] | — | — |
| objeto nuevo | 85.6 [82.7, 88.7] | 73.4 [70.4, 76.4] | 83.1 [79.9, 86.1] | 82.7 [80.1, 85.1] | 14.4 [12.3, 16.9] | 60.8 [58.3, 63.1] | 99.2 [97.7, 100.0] | 2.7 [0.7, 4.9] |

Brecha de memorización (conocido − nuevo, puntos, por pliegue):

| medida | brecha |
|---|---|
| contenido_acepta | 9.5 [5.9, 13.0] |
| responde | 13.7 [10.1, 17.3] |
| dir_acepta | 9.4 [5.9, 13.0] |
| e2e | 15.5 [12.1, 18.8] |

Razón e2e nuevo / conocido por pliegue: 0.80 [0.76, 0.84] (criterio §6: sostenida si ≥ 0.75, refutada si < 0.5).

## Por clase (media de pliegues, %)

| clase | contenido acepta: conocido / nuevo | responde | directorio acepta | e2e | falso ruteo (nuevo) |
|---|---|---|---|---|---|
| apple | 97.8 / 76.1 | 94.6 / 69.5 | 95.9 / 78.5 | 93.2 / 69.3 | 1.7 |
| car | 94.9 / 90.2 | 85.4 / 72.7 | 90.0 / 76.1 | 81.7 / 67.3 | 0.0 |
| cow | 94.4 / 84.4 | 85.4 / 72.0 | 94.9 / 88.0 | 73.4 / 56.8 | 20.5 |
| cup | 95.1 / 81.2 | 86.6 / 69.3 | 89.5 / 69.8 | 83.7 / 62.0 | 0.0 |
| dog | 91.2 / 83.7 | 75.9 / 61.7 | 87.3 / 80.7 | 33.7 / 18.8 | 56.6 |
| horse | 94.9 / 86.6 | 81.5 / 68.8 | 93.9 / 94.1 | 63.7 / 50.7 | 30.0 |
| pear | 96.8 / 91.2 | 93.4 / 86.3 | 94.1 / 88.0 | 91.7 / 81.5 | 1.2 |
| tomato | 96.1 / 91.5 | 93.7 / 86.8 | 94.1 / 89.5 | 89.5 / 80.0 | 5.4 |

## Falsos ruteos sobre objetos nuevos (todos los pliegues)

| par | imágenes |
|---|---|
| dog → cow | 118 |
| dog → horse | 114 |
| horse → cow | 104 |
| cow → horse | 75 |
| tomato → apple | 22 |
| horse → dog | 19 |
| cow → dog | 9 |
| apple → pear | 7 |
| pear → apple | 5 |

Fase A (media por pliegue): registradas 987, rechazadas 37.2, sin energía 0.0, acierto 905 de las registradas.

## Archivos
- `raw/pliegue_<k>.json`: filas por imagen y banco
- `resumen.json`, `fig1_nuevo_vs_conocido.png`
- `latentes.npy`, `latentes_indice.json`: latentes de las 410 × 16 por clase (fuera de git; se regeneran)
