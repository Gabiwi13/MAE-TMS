# Tablas (pliegues [1, 2, 3])

## Punta a punta y etapas, codificador por pliegue (formato de exp16)

| banco | contenido acepta | responde | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | hit estricto | otro dominio |
|---|---|---|---|---|---|---|---|---|
| objeto conocido | 98.6 [97.9, 99.4] | 94.3 [92.7, 95.4] | 97.0 [96.6, 97.3] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 93.4 [91.8, 94.2] | — | — |
| objeto nuevo | 92.8 [90.5, 93.9] | 90.5 [88.1, 92.7] | 94.6 [93.6, 95.7] | 96.5 [93.0, 98.4] | 3.4 [1.5, 6.7] | 89.3 [87.2, 91.2] | 98.5 [95.5, 100.0] | 1.5 [0.0, 4.5] |

Brecha (conocido − nuevo, puntos, por pliegue):

| medida | brecha |
|---|---|
| contenido_acepta | 5.8 [4.6, 7.3] |
| responde | 3.8 [2.1, 4.6] |
| dir_acepta | 2.3 [0.9, 3.7] |
| e2e | 4.1 [3.0, 4.6] |

Razón e2e nuevo / conocido por pliegue: 0.96 [0.95, 0.97].

## Contra exp16 oficial (mismos pliegues; % de 328 por pliegue, media y bootstrap 95 %)

| medida | exp16 oficial | codificador por pliegue | diferencia (pliegue − oficial) |
|---|---|---|---|
| e2e objeto conocido | 95.4 [94.5, 96.0] | 93.4 [91.8, 94.2] | -2.0 [-2.7, -1.5] |
| e2e objeto nuevo | 87.5 [79.3, 94.2] | 89.3 [87.2, 91.2] | 1.8 [-4.6, 11.9] |
| brecha conocido − nuevo | 7.9 [1.5, 16.8] | 4.1 [3.0, 4.6] | |
| falsos ruteos, objeto nuevo (de 984) | 1 | 33 | |
| falsos ruteos, objeto conocido (de 984) | 1 | 0 | |

## Pliegue por pliegue

| pliegue | codificador RMSE / acc test | τ | e2e conocido: oficial → pliegue | e2e nuevo: oficial → pliegue | falsos nuevo: oficial / pliegue | fase A registradas: oficial / pliegue | min entrenar / lógica |
|---|---|---|---|---|---|---|---|
| 1 | 0.1054 / 99.7 | 17.05 | 95.7 → 94.2 | 94.2 → 89.6 | 0 / 5 | 1012 / 1013 | 5.5 / 59.6 |
| 2 | 0.1107 / 99.5 | 10.10 | 94.5 → 91.8 | 89.0 → 87.2 | 0 / 22 | 1015 / 1009 | 5.7 / 58.3 |
| 3 | 0.1118 / 99.5 | 15.48 | 96.0 → 94.2 | 79.3 → 91.2 | 1 / 6 | 1015 / 1018 | 4.8 / 41.5 |

Diagnóstico (no lo usa el sistema): acierto de la cabeza clasificadora del codificador del pliegue.

| pliegue | objeto nuevo | objeto conocido |
|---|---|---|
| 1 | 97.3 | 100.0 |
| 2 | 92.1 | 99.7 |
| 3 | 97.0 | 100.0 |

## Por clase (media de pliegues, %)

| clase | contenido acepta: conocido / nuevo | responde | directorio acepta | e2e | falso ruteo (nuevo) |
|---|---|---|---|---|---|
| apple | 98.4 / 100.0 | 97.6 / 98.4 | 99.2 / 99.2 | 97.6 / 98.4 | 0.0 |
| car | 99.2 / 97.6 | 91.9 / 92.7 | 93.5 / 91.9 | 88.6 / 89.4 | 0.0 |
| cow | 95.9 / 89.4 | 91.1 / 87.0 | 98.4 / 94.3 | 91.1 / 87.0 | 2.4 |
| cup | 98.4 / 100.0 | 94.3 / 100.0 | 95.9 / 100.0 | 93.5 / 100.0 | 0.0 |
| dog | 97.6 / 85.4 | 91.9 / 81.3 | 95.9 / 84.6 | 91.9 / 78.0 | 3.3 |
| horse | 99.2 / 72.4 | 92.7 / 68.3 | 94.3 / 87.8 | 90.2 / 65.0 | 21.1 |
| pear | 100.0 / 98.4 | 97.6 / 97.6 | 100.0 / 100.0 | 97.6 / 97.6 | 0.0 |
| tomato | 100.0 / 99.2 | 97.6 / 99.2 | 98.4 / 99.2 | 96.7 / 99.2 | 0.0 |

## Falsos ruteos (todos los pliegues corridos)

| banco: par | imágenes |
|---|---|
| nuevo: horse → cow | 17 |
| nuevo: horse → dog | 9 |
| nuevo: dog → horse | 3 |
| nuevo: cow → horse | 2 |
| nuevo: dog → cow | 1 |
| nuevo: cow → dog | 1 |

Fase A (media por pliegue): registradas 1013, rechazadas 10.3, sin energía 0.3, acierto 1012 de las registradas.

## Por objeto reservado (e2e sobre sus 41 vistas, %)

Objetos con e2e ≥ 70 %: oficial 21 de 24, codificador por pliegue 22 de 24. Los que quedan debajo en alguno:

| objeto | pliegue | oficial | codificador por pliegue | falsos (oficial / pliegue) |
|---|---|---|---|---|
| horse2 | 2 | 80 | 27 | 0 / 22 |
| dog3 | 3 | 66 | 54 | 0 / 1 |
| cow2 | 2 | 68 | 88 | 0 / 0 |
| apple3 | 3 | 0 | 100 | 0 / 0 |

Tabla completa en `por_objeto.csv`; por pliegue en `por_pliegue.csv`.
