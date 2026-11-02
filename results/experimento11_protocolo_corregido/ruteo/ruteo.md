# exp11, solo ruteo de T-protocolo con directorios corregidos

Semillas [42, 43, 44, 45, 46, 47, 48, 49, 50, 51], cortes [25, 50, 100, 200]. Media entre semillas e IC 95 % bootstrap sobre semillas. «Viejo» y M salen de los raw oficiales de exp11.

## Reproducción de los trabajos oficiales limpios

| conjunto | iguales / total |
|---|---|
| texto_limpio | 1144 / 1144 |
| imagen_limpio | 320 / 320 |
| ood | 1600 / 1600 |
| texto_resto | 4047 / 5696 |
| imagen_resto | 2880 / 2880 |

Texto compara entrada, destino, círculo, saltos y aceptación; imagen, destino y aceptación; fuera de dominio, aceptación con y sin compuerta y destino. «resto» son los trabajos que en la corrida oficial heredaron directorios: ahí las diferencias son el efecto del error.

## Identidades comprobadas en los raw oficiales

| identidad | iguales / filas |
|---|---|
| texto_clase_igual_responde_y_ruteo_limpios | 3432 / 3432 |
| texto_clase_igual_responde_y_ruteo_todos | 20520 / 20520 |
| texto_clase_igual_ruteo_limpios | 3432 / 3432 |
| imagen_hit_igual_responde_y_ruteo_limpios | 320 / 320 |
| imagen_hit_igual_responde_y_ruteo_todos | 3200 / 3200 |
| texto_responde_compuerta_igual_oficial | 19869 / 19869 |
| imagen_responde_compuerta_igual_oficial | 3200 / 3200 |

## Texto (171 reservadas por semilla)

| N | brazo | acepta | ruteo ok | responde | clase correcta sobre el total |
|---|---|---|---|---|---|
| 25 | protocolo viejo | 100.0 [100.0, 100.0] | 95.3 [94.6, 96.1] | 98.4 [98.2, 98.7] | 95.3 [94.6, 96.1] |
| 25 | protocolo corregido | 100.0 [100.0, 100.0] | 93.2 [91.9, 94.6] | 98.4 [97.7, 98.9] | 93.2 [91.9, 94.6] |
| 25 | EHAM única | 100.0 [100.0, 100.0] | — | 100.0 [100.0, 100.0] | 97.6 [97.4, 97.8] |
| 50 | protocolo viejo | 100.0 [100.0, 100.0] | 97.4 [97.1, 97.8] | 98.7 [98.4, 98.9] | 97.4 [97.1, 97.8] |
| 50 | protocolo corregido | 100.0 [100.0, 100.0] | 96.8 [96.3, 97.4] | 98.7 [98.1, 99.2] | 96.8 [96.3, 97.4] |
| 50 | EHAM única | 100.0 [100.0, 100.0] | — | 100.0 [100.0, 100.0] | 97.5 [97.3, 97.7] |
| 100 | protocolo viejo | 100.0 [100.0, 100.0] | 97.4 [97.0, 97.8] | 98.7 [98.4, 98.9] | 97.4 [97.0, 97.8] |
| 100 | protocolo corregido | 100.0 [100.0, 100.0] | 96.8 [96.3, 97.4] | 98.7 [98.1, 99.2] | 96.8 [96.3, 97.4] |
| 100 | EHAM única | 100.0 [100.0, 100.0] | — | 100.0 [100.0, 100.0] | 97.6 [97.4, 97.8] |
| 200 | protocolo viejo | 100.0 [100.0, 100.0] | 97.0 [96.6, 97.4] | 98.7 [98.5, 98.9] | 97.0 [96.6, 97.4] |
| 200 | protocolo corregido | 100.0 [100.0, 100.0] | 96.8 [96.3, 97.4] | 98.7 [98.1, 99.1] | 96.8 [96.3, 97.4] |
| 200 | EHAM única | 100.0 [100.0, 100.0] | — | 100.0 [100.0, 100.0] | 96.9 [96.7, 97.1] |

## Imagen (80 por semilla)

Clase: en M y en el protocolo viejo es el hit laxo (una de las 3 etiquetas evocadas es del vocabulario de la clase); en el corregido, responde en el especialista correcto (igual al hit laxo en los raw oficiales, ver identidades).

| N | brazo | acepta | ruteo ok | responde | clase |
|---|---|---|---|---|---|
| 25 | protocolo viejo | 63.7 [63.7, 63.7] | 100.0 [100.0, 100.0] | 41.2 [41.2, 41.2] | 41.2 [41.2, 41.2] |
| 25 | protocolo corregido | 63.7 [63.7, 63.7] | 100.0 [100.0, 100.0] | 41.2 [41.2, 41.2] | 41.2 [41.2, 41.2] |
| 25 | EHAM única | 97.5 [97.5, 97.5] | — | 78.7 [78.7, 78.7] | 78.0 [77.5, 78.5] |
| 50 | protocolo viejo | 77.5 [77.5, 77.5] | 100.0 [100.0, 100.0] | 67.5 [67.5, 67.5] | 67.5 [67.5, 67.5] |
| 50 | protocolo corregido | 77.5 [77.5, 77.5] | 100.0 [100.0, 100.0] | 67.5 [67.5, 67.5] | 67.5 [67.5, 67.5] |
| 50 | EHAM única | 100.0 [100.0, 100.0] | — | 95.0 [95.0, 95.0] | 93.9 [93.1, 94.5] |
| 100 | protocolo viejo | 80.0 [80.0, 80.0] | 100.0 [100.0, 100.0] | 78.7 [78.7, 78.7] | 78.7 [78.7, 78.7] |
| 100 | protocolo corregido | 80.0 [80.0, 80.0] | 100.0 [100.0, 100.0] | 78.7 [78.7, 78.7] | 78.7 [78.7, 78.7] |
| 100 | EHAM única | 100.0 [100.0, 100.0] | — | 98.8 [98.8, 98.8] | 96.7 [95.7, 97.8] |
| 200 | protocolo viejo | 81.2 [81.2, 81.2] | 100.0 [100.0, 100.0] | 81.2 [81.2, 81.2] | 81.2 [81.2, 81.2] |
| 200 | protocolo corregido | 81.2 [81.2, 81.2] | 100.0 [100.0, 100.0] | 81.2 [81.2, 81.2] | 81.2 [81.2, 81.2] |
| 200 | EHAM única | 100.0 [100.0, 100.0] | — | 100.0 [100.0, 100.0] | 97.5 [96.5, 98.4] |

## Fuera de dominio (40 consultas)

| N | brazo | acepta | acepta con compuerta |
|---|---|---|---|
| 25 | protocolo viejo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |
| 25 | protocolo corregido | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |
| 25 | EHAM única | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| 50 | protocolo viejo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |
| 50 | protocolo corregido | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |
| 50 | EHAM única | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| 100 | protocolo viejo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |
| 100 | protocolo corregido | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |
| 100 | EHAM única | 12.5 [12.5, 12.5] | 12.5 [12.5, 12.5] |
| 200 | protocolo viejo | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |
| 200 | protocolo corregido | 10.0 [10.0, 10.0] | 5.0 [5.0, 5.0] |
| 200 | EHAM única | 20.0 [20.0, 20.0] | 20.0 [20.0, 20.0] |

## Protocolo contra EHAM única

McNemar exacto sobre los pares; bootstrap de la diferencia P − M remuestreando consultas (o imágenes), con cada una promediada entre semillas y sorteos. En texto los pares son (semilla, consulta, sorteo de M): el protocolo corregido es determinista por (semilla, consulta), así que el p de McNemar es optimista; el bootstrap por consulta es la prueba conservadora.

| prueba | N | lado | pares | M sí, P no | P sí, M no | P − M | p | bootstrap por consulta |
|---|---|---|---|---|---|---|---|---|
| texto | 25 | nuevo | 5130 | 347 | 119 | -4.44 | 6.48e-27 | -8.09, -0.92 |
| texto | 25 | viejo | 5130 | 240 | 123 | -2.28 | 8.21e-10 | -5.75, +1.09 |
| imagen | 25 | nuevo | 800 | 297 | 3 | -36.75 | 4.42e-84 | -47.75, -26.12 |
| imagen | 25 | viejo | 800 | 297 | 3 | -36.75 | 4.42e-84 | -47.75, -26.12 |
| ood | 25 | acepta | 400 | 0 | 20 | +5.00 | 1.91e-06 | +0.00, +12.50 |
| ood | 25 | acepta_compuerta | 400 | 0 | 0 | +0.00 | 1 | +0.00, +0.00 |
| texto | 50 | nuevo | 5130 | 145 | 111 | -0.66 | 0.039 | -3.29, +1.97 |
| texto | 50 | viejo | 5130 | 129 | 125 | -0.08 | 0.851 | -2.96, +2.79 |
| imagen | 50 | nuevo | 800 | 213 | 2 | -26.38 | 8.82e-61 | -36.00, -17.25 |
| imagen | 50 | viejo | 800 | 213 | 2 | -26.38 | 8.82e-61 | -36.00, -17.25 |
| ood | 50 | acepta | 400 | 0 | 20 | +5.00 | 1.91e-06 | +0.00, +12.50 |
| ood | 50 | acepta_compuerta | 400 | 0 | 0 | +0.00 | 1 | +0.00, +0.00 |
| texto | 100 | nuevo | 5130 | 146 | 108 | -0.74 | 0.0201 | -3.39, +1.95 |
| texto | 100 | viejo | 5130 | 132 | 124 | -0.16 | 0.662 | -3.06, +2.71 |
| imagen | 100 | nuevo | 800 | 154 | 10 | -18.00 | 2.68e-34 | -26.88, -9.87 |
| imagen | 100 | viejo | 800 | 154 | 10 | -18.00 | 2.68e-34 | -26.88, -9.87 |
| ood | 100 | acepta | 400 | 30 | 20 | -2.50 | 0.203 | -12.50, +7.50 |
| ood | 100 | acepta_compuerta | 400 | 30 | 0 | -7.50 | 1.86e-09 | -17.50, +0.00 |
| texto | 200 | nuevo | 5130 | 151 | 147 | -0.08 | 0.862 | -2.88, +2.88 |
| texto | 200 | viejo | 5130 | 146 | 151 | +0.10 | 0.817 | -2.90, +3.16 |
| imagen | 200 | nuevo | 800 | 139 | 9 | -16.25 | 4.39e-31 | -24.75, -8.50 |
| imagen | 200 | viejo | 800 | 139 | 9 | -16.25 | 4.39e-31 | -24.75, -8.50 |
| ood | 200 | acepta | 400 | 50 | 10 | -10.00 | 1.62e-07 | -22.50, +0.00 |
| ood | 200 | acepta_compuerta | 400 | 60 | 0 | -15.00 | 1.73e-18 | -27.50, -5.00 |

En fuera de dominio, «acepta» y «acepta_compuerta» comparan la aceptación del protocolo (sin y con la segunda compuerta) con la de M; ahí aceptar es fallar.

## Fuera de dominio aceptadas por el protocolo corregido

- N = 25: «a kitchen appliance that heats food» 10 semillas, 10 con compuerta → ['apple']; «a wooden table and chairs» 10 semillas, 10 con compuerta → ['cup']; «a piano with black and white keys» 10 semillas, 0 con compuerta → ['dog']; «a thunderstorm with heavy rain» 10 semillas, 0 con compuerta → ['car']
- N = 50: «a kitchen appliance that heats food» 10 semillas, 10 con compuerta → ['apple']; «a wooden table and chairs» 10 semillas, 10 con compuerta → ['cup']; «a piano with black and white keys» 10 semillas, 0 con compuerta → ['dog']; «a thunderstorm with heavy rain» 10 semillas, 0 con compuerta → ['car']
- N = 100: «a kitchen appliance that heats food» 10 semillas, 10 con compuerta → ['apple']; «a wooden table and chairs» 10 semillas, 10 con compuerta → ['cup']; «a piano with black and white keys» 10 semillas, 0 con compuerta → ['dog']; «a thunderstorm with heavy rain» 10 semillas, 0 con compuerta → ['car']
- N = 200: «a kitchen appliance that heats food» 10 semillas, 10 con compuerta → ['apple']; «a wooden table and chairs» 10 semillas, 10 con compuerta → ['cup']; «a piano with black and white keys» 10 semillas, 0 con compuerta → ['dog']; «a thunderstorm with heavy rain» 10 semillas, 0 con compuerta → ['car']

## Tiempo

| corte | semillas | s por semilla (texto + fuera de dominio + imagen) |
|---|---|---|
| 25 | 10 | 27 |
| 50 | 10 | 28 |
| 100 | 10 | 29 |
| 200 | 10 | 28 |
