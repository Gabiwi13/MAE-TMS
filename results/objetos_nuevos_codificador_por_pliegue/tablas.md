# Tablas (pliegues [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

## Punta a punta y etapas, codificador por pliegue (formato de exp16)

| banco | contenido acepta | responde | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | hit estricto | otro dominio |
|---|---|---|---|---|---|---|---|---|
| objeto conocido | 98.8 [98.4, 99.1] | 95.7 [94.8, 96.6] | 97.1 [96.6, 97.6] | 99.8 [99.7, 100.0] | 0.2 [0.0, 0.3] | 94.8 [93.8, 95.9] | — | — |
| objeto nuevo | 93.0 [90.8, 95.3] | 88.8 [85.5, 92.3] | 94.5 [92.2, 96.8] | 95.6 [94.3, 96.8] | 4.1 [3.0, 5.4] | 87.6 [84.3, 91.0] | 99.0 [97.5, 100.0] | 1.5 [0.0, 3.0] |

Brecha (conocido − nuevo, puntos, por pliegue):

| medida | brecha |
|---|---|
| contenido_acepta | 5.8 [3.5, 7.9] |
| responde | 6.9 [3.7, 10.3] |
| dir_acepta | 2.6 [0.5, 4.7] |
| e2e | 7.2 [4.1, 10.4] |

Razón e2e nuevo / conocido por pliegue: 0.92 [0.89, 0.96].

## Contra exp16 oficial (mismos pliegues; % de 328 por pliegue, media y bootstrap 95 %)

| medida | exp16 oficial | codificador por pliegue | diferencia (pliegue − oficial) |
|---|---|---|---|
| e2e objeto conocido | 95.5 [95.1, 95.9] | 94.8 [93.8, 95.9] | -0.6 [-1.6, 0.3] |
| e2e objeto nuevo | 89.2 [85.1, 93.2] | 87.6 [84.3, 91.0] | -1.6 [-5.7, 3.2] |
| brecha conocido − nuevo | 6.3 [2.5, 10.4] | 7.2 [4.1, 10.4] | |
| falsos ruteos, objeto nuevo (de 3280) | 2 | 136 | |
| falsos ruteos, objeto conocido (de 3280) | 3 | 5 | |

## Pliegue por pliegue

| pliegue | codificador RMSE / acc test | τ | e2e conocido: oficial → pliegue | e2e nuevo: oficial → pliegue | falsos nuevo: oficial / pliegue | fase A registradas: oficial / pliegue | min entrenar / lógica |
|---|---|---|---|---|---|---|---|
| 1 | 0.1054 / 99.7 | 17.05 | 95.7 → 94.2 | 94.2 → 89.6 | 0 / 5 | 1012 / 1013 | 5.5 / 59.6 |
| 2 | 0.1107 / 99.5 | 10.10 | 94.5 → 91.8 | 89.0 → 87.2 | 0 / 22 | 1015 / 1009 | 5.7 / 58.3 |
| 3 | 0.1118 / 99.5 | 15.48 | 96.0 → 94.2 | 79.3 → 91.2 | 1 / 6 | 1015 / 1018 | 4.8 / 41.5 |
| 4 | 0.1124 / 98.7 | 11.38 | 96.0 → 97.3 | 98.8 → 95.4 | 0 / 9 | 1013 / 1015 | 4.5 / 38.7 |
| 5 | 0.1082 / 99.2 | 12.16 | 95.7 → 95.7 | 91.8 → 84.5 | 0 / 26 | 1008 / 1010 | 4.5 / 38.9 |
| 6 | 0.1095 / 99.1 | 11.76 | 95.1 → 93.9 | 89.0 → 80.2 | 0 / 17 | 1015 / 1010 | 4.5 / 39.0 |
| 7 | 0.1181 / 98.3 | 8.38 | 96.6 → 94.5 | 93.9 → 92.7 | 1 / 15 | 1017 / 1013 | 4.5 / 95.1 |
| 8 | 0.1091 / 99.7 | 14.16 | 95.1 → 96.3 | 94.5 → 82.9 | 0 / 12 | 1012 / 1013 | 4.7 / 35.7 |
| 9 | 0.1175 / 99.3 | 11.09 | 94.8 → 96.6 | 82.6 → 93.0 | 0 / 14 | 1015 / 1018 | 4.6 / 36.4 |
| 10 | 0.1135 / 99.3 | 15.18 | 95.1 → 93.9 | 78.7 → 79.6 | 0 / 10 | 1015 / 1015 | 4.6 / 36.4 |

Diagnóstico (no lo usa el sistema): acierto de la cabeza clasificadora del codificador del pliegue.

| pliegue | objeto nuevo | objeto conocido |
|---|---|---|
| 1 | 97.3 | 100.0 |
| 2 | 92.1 | 99.7 |
| 3 | 97.0 | 100.0 |
| 4 | 95.7 | 100.0 |
| 5 | 92.4 | 100.0 |
| 6 | 94.2 | 100.0 |
| 7 | 93.9 | 98.2 |
| 8 | 90.9 | 99.7 |
| 9 | 96.0 | 99.7 |
| 10 | 95.4 | 100.0 |

## Por clase (media de pliegues, %)

| clase | contenido acepta: conocido / nuevo | responde | directorio acepta | e2e | falso ruteo (nuevo) |
|---|---|---|---|---|---|
| apple | 99.3 / 92.2 | 98.5 / 89.0 | 98.8 / 91.0 | 98.0 / 88.5 | 0.0 |
| car | 98.3 / 97.6 | 91.7 / 94.6 | 93.4 / 95.4 | 90.0 / 93.7 | 0.0 |
| cow | 98.0 / 85.1 | 95.4 / 79.8 | 98.0 / 93.9 | 94.6 / 78.3 | 12.2 |
| cup | 98.8 / 98.0 | 95.9 / 96.1 | 96.8 / 95.6 | 94.6 / 94.4 | 0.0 |
| dog | 97.3 / 89.5 | 92.7 / 82.7 | 95.1 / 90.2 | 92.2 / 80.2 | 4.4 |
| horse | 98.5 / 85.4 | 94.4 / 74.9 | 95.6 / 93.9 | 92.9 / 72.9 | 16.6 |
| pear | 100.0 / 98.5 | 98.8 / 97.6 | 100.0 / 99.0 | 98.8 / 97.1 | 0.0 |
| tomato | 100.0 / 97.6 | 98.5 / 95.9 | 98.8 / 97.1 | 97.6 / 95.9 | 0.0 |

## Falsos ruteos (todos los pliegues corridos)

| banco: par | imágenes |
|---|---|
| nuevo: horse → cow | 35 |
| nuevo: horse → dog | 33 |
| nuevo: cow → dog | 23 |
| nuevo: cow → car | 20 |
| nuevo: dog → horse | 12 |
| nuevo: cow → horse | 7 |
| nuevo: dog → cow | 5 |
| conocido: cow → horse | 3 |
| nuevo: dog → car | 1 |
| conocido: horse → cow | 1 |
| conocido: cow → dog | 1 |

Fase A (media por pliegue): registradas 1013, rechazadas 10.0, sin energía 0.6, acierto 1012 de las registradas.

## Por objeto reservado (e2e sobre sus 41 vistas, %)

Objetos con e2e ≥ 70 %: oficial 71 de 80, codificador por pliegue 68 de 80. Los que quedan debajo en alguno:

| objeto | pliegue | oficial | codificador por pliegue | falsos (oficial / pliegue) |
|---|---|---|---|---|
| horse2 | 2 | 80 | 27 | 0 / 22 |
| cow5 | 5 | 100 | 29 | 0 / 23 |
| cow6 | 6 | 95 | 37 | 0 / 12 |
| apple6 | 6 | 100 | 46 | 0 / 0 |
| apple10 | 10 | 32 | 51 | 0 / 0 |
| dog3 | 3 | 66 | 54 | 0 / 1 |
| cup8 | 8 | 93 | 63 | 0 / 0 |
| dog8 | 8 | 98 | 63 | 0 / 2 |
| horse8 | 8 | 100 | 63 | 0 / 9 |
| horse10 | 10 | 100 | 63 | 0 / 6 |
| horse7 | 7 | 95 | 66 | 1 / 14 |
| dog10 | 10 | 49 | 68 | 0 / 1 |
| cow2 | 2 | 68 | 88 | 0 / 0 |
| car6 | 5 | 63 | 88 | 0 / 0 |
| pear6 | 6 | 59 | 90 | 0 / 0 |
| cup10 | 10 | 61 | 90 | 0 / 0 |
| apple3 | 3 | 0 | 100 | 0 / 0 |
| pear9 | 9 | 10 | 100 | 0 / 0 |

Tabla completa en `por_objeto.csv`; por pliegue en `por_pliegue.csv`.
