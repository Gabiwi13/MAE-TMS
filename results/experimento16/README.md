# Experimento 16 — leave-one-object-out

10 pliegues (objeto reservado [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), una semilla. Por pliegue: contenido con 200 imágenes de los 9 objetos restantes (16 variantes), fase A con 128 (16 variantes), umbral de energía. Bancos por pliegue: «nuevo» = 41 vistas del objeto reservado por clase (328); «conocido» = 41 vistas no usadas de los objetos que sí contribuyeron (328). Intervalos: bootstrap del 95 % sobre pliegues. Diseño en `propuesta_exp16_leave_object_out.md`.

| banco | contenido acepta | responde | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | hit estricto | otro dominio |
|---|---|---|---|---|---|---|---|---|
| objeto conocido | 99.1 [98.9, 99.4] | 96.2 [95.7, 96.7] | 98.0 [97.3, 98.6] | 99.9 [99.8, 100.0] | 0.1 [0.0, 0.2] | 95.5 [95.1, 95.9] | — | — |
| objeto nuevo | 95.2 [92.1, 97.7] | 91.0 [87.4, 94.5] | 92.2 [88.6, 95.4] | 99.9 [99.8, 100.0] | 0.1 [0.0, 0.2] | 89.2 [85.1, 93.2] | 99.1 [97.8, 100.0] | 1.8 [0.4, 3.2] |

Brecha de memorización (conocido − nuevo, puntos, por pliegue):

| medida | brecha |
|---|---|
| contenido_acepta | 3.9 [1.6, 6.9] |
| responde | 5.2 [1.7, 9.0] |
| dir_acepta | 5.8 [2.7, 9.1] |
| e2e | 6.3 [2.5, 10.4] |

Razón e2e nuevo / conocido por pliegue: 0.93 [0.89, 0.97] (criterio §6: sostenida si ≥ 0.75, refutada si < 0.5).

## Por clase (media de pliegues, %)

| clase | contenido acepta: conocido / nuevo | responde | directorio acepta | e2e | falso ruteo (nuevo) |
|---|---|---|---|---|---|
| apple | 99.8 / 86.3 | 99.0 / 83.4 | 99.8 / 82.7 | 99.0 / 82.4 | 0.0 |
| car | 98.3 / 95.6 | 90.7 / 89.5 | 95.1 / 93.4 | 89.3 / 88.8 | 0.0 |
| cow | 98.8 / 95.9 | 95.9 / 91.7 | 98.0 / 95.9 | 95.4 / 91.0 | 0.2 |
| cup | 99.8 / 96.6 | 97.1 / 91.0 | 98.0 / 93.9 | 95.6 / 89.8 | 0.0 |
| dog | 99.5 / 97.1 | 93.4 / 91.2 | 96.6 / 90.7 | 92.7 / 87.3 | 0.0 |
| horse | 98.3 / 98.0 | 96.6 / 95.1 | 98.3 / 95.9 | 96.1 / 94.4 | 0.2 |
| pear | 98.8 / 94.4 | 97.1 / 89.8 | 98.0 / 88.0 | 95.9 / 83.9 | 0.0 |
| tomato | 100.0 / 97.8 | 100.0 / 96.3 | 100.0 / 97.1 | 100.0 / 95.9 | 0.0 |

## Falsos ruteos sobre objetos nuevos (todos los pliegues)

| par | imágenes |
|---|---|
| cow → dog | 1 |
| horse → dog | 1 |

Fase A (media por pliegue): registradas 1014, rechazadas 8.2, sin energía 2.1, acierto 1013 de las registradas.

## Archivos
- `raw/pliegue_<k>.json`: filas por imagen y banco
- `resumen.json`, `fig1_nuevo_vs_conocido.png`
- `latentes.npy`, `latentes_indice.json`: latentes de las 410 × 16 por clase (fuera de git; se regeneran)
