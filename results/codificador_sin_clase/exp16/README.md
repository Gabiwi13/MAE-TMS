# Experimento 16 — leave-one-object-out

10 pliegues (objeto reservado [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), una semilla. Por pliegue: contenido con 200 imágenes de los 9 objetos restantes (16 variantes), fase A con 128 (16 variantes), umbral de energía. Bancos por pliegue: «nuevo» = 41 vistas del objeto reservado por clase (328); «conocido» = 41 vistas no usadas de los objetos que sí contribuyeron (328). Intervalos: bootstrap del 95 % sobre pliegues. Diseño en `propuesta_exp16_leave_object_out.md`.

| banco | contenido acepta | responde | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | hit estricto | otro dominio |
|---|---|---|---|---|---|---|---|---|
| objeto conocido | 97.4 [96.7, 98.1] | 91.3 [90.1, 92.4] | 97.3 [96.7, 97.8] | 75.8 [73.7, 77.6] | 23.6 [21.8, 25.5] | 69.9 [68.0, 71.6] | — | — |
| objeto nuevo | 92.9 [90.9, 94.8] | 83.9 [80.8, 87.1] | 95.5 [94.2, 96.6] | 68.3 [65.3, 71.2] | 30.2 [27.4, 33.2] | 59.3 [55.5, 62.9] | 99.5 [98.6, 100.0] | 1.5 [0.0, 3.1] |

Brecha de memorización (conocido − nuevo, puntos, por pliegue):

| medida | brecha |
|---|---|
| contenido_acepta | 4.5 [2.9, 6.2] |
| responde | 7.3 [5.0, 9.7] |
| dir_acepta | 1.8 [0.7, 3.2] |
| e2e | 10.6 [6.8, 14.8] |

Razón e2e nuevo / conocido por pliegue: 0.85 [0.79, 0.90] (criterio §6: sostenida si ≥ 0.75, refutada si < 0.5).

## Por clase (media de pliegues, %)

| clase | contenido acepta: conocido / nuevo | responde | directorio acepta | e2e | falso ruteo (nuevo) |
|---|---|---|---|---|---|
| apple | 97.6 / 93.7 | 93.7 / 85.1 | 99.3 / 96.3 | 82.4 / 72.4 | 17.8 |
| car | 93.9 / 90.2 | 83.9 / 80.2 | 91.2 / 89.8 | 63.4 / 59.0 | 24.1 |
| cow | 96.3 / 91.2 | 89.8 / 81.7 | 98.8 / 97.6 | 48.3 / 37.6 | 54.1 |
| cup | 98.5 / 90.0 | 91.2 / 76.3 | 97.1 / 93.2 | 80.7 / 64.6 | 17.6 |
| dog | 98.5 / 93.2 | 89.3 / 78.8 | 96.8 / 98.3 | 62.4 / 45.1 | 44.1 |
| horse | 95.9 / 93.2 | 87.6 / 82.4 | 97.6 / 97.1 | 41.2 / 25.4 | 67.8 |
| pear | 99.3 / 93.4 | 96.6 / 91.0 | 98.8 / 94.9 | 90.7 / 85.1 | 7.1 |
| tomato | 99.3 / 98.3 | 98.0 / 95.6 | 98.5 / 96.6 | 90.0 / 85.1 | 9.3 |

## Falsos ruteos sobre objetos nuevos (todos los pliegues)

| par | imágenes |
|---|---|
| horse → dog | 161 |
| cow → dog | 114 |
| dog → horse | 93 |
| horse → cow | 76 |
| cow → horse | 64 |
| dog → cow | 56 |
| car → dog | 51 |
| apple → tomato | 45 |
| cow → car | 39 |
| cup → cow | 32 |
| tomato → apple | 29 |
| apple → cup | 23 |
| car → cow | 22 |
| cup → horse | 21 |
| horse → car | 20 |
| dog → car | 17 |
| car → horse | 15 |
| horse → cup | 15 |
| dog → cup | 14 |
| pear → dog | 12 |
| cup → dog | 11 |
| pear → cup | 9 |
| tomato → cup | 9 |
| car → cup | 6 |
| pear → cow | 5 |
| cow → cup | 5 |
| cup → apple | 5 |
| horse → pear | 4 |
| car → pear | 4 |
| pear → horse | 3 |
| cup → tomato | 3 |
| apple → pear | 3 |
| horse → apple | 2 |
| apple → horse | 2 |
| car → apple | 1 |
| dog → pear | 1 |

Fase A (media por pliegue): registradas 1013, rechazadas 11.3, sin energía 0.0, acierto 832 de las registradas.

## Archivos
- `raw/pliegue_<k>.json`: filas por imagen y banco
- `resumen.json`, `fig1_nuevo_vs_conocido.png`
- `latentes.npy`, `latentes_indice.json`: latentes de las 410 × 16 por clase (fuera de git; se regeneran)
