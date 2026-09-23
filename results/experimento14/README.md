# Experimento 14 — criterio de energía mínima del latente

Calibración: mínimo sobre los 1600 originales del llenado con margen 10% (niveles: mínimo menos uno). Banco degenerado generado como declara `propuesta_exp14_energia_latente.md` §4. Memoria oficial: agentes v5 (contenido y directorio, entrada `apple`); V16: contenido de exp13 con 16 variantes. Diseño y criterio en la propuesta.

## Umbrales y costo sobre imágenes reales

| estadístico | τ | mínimo llenado | rechaza llenado (1600) | rechaza fase A (1024) | rechaza test (656) |
|---|---|---|---|---|---|
| norma | 16.607 | 18.453 | 0 | 1 | 4 |
| desv_latente | 2.076 | 2.306 | 0 | 1 | 5 |
| desv_pixeles | 13.864 | 15.404 | 0 | 0 | 0 |
| niveles | 12.000 | 13.000 | 0 | 0 | 1 |

Imágenes de test rechazadas por la norma:

- `cow3-035-135.png` (cow): norma 13.95; contenido propio acepta; directorio → rechazo
- `cow3-068-090.png` (cow): norma 16.56; contenido propio rechaza; directorio → rechazo
- `cow3-066-117.png` (cow): norma 10.78; contenido propio acepta; directorio → rechazo
- `cow6-035-045.png` (cow): norma 15.11; contenido propio acepta; directorio → rechazo

## Fuga: entradas degeneradas que la memoria acepta y el criterio deja pasar

Banco: 231 entradas. «Acepta»: algún especialista da soporte o el directorio rutea.

| estadístico | acepta la memoria oficial | pasan el criterio | acepta el contenido V16 | pasan el criterio |
|---|---|---|---|---|
| norma | 103 | 18 | 179 | 33 |
| desv_latente | 103 | 17 | 179 | 31 |
| desv_pixeles | 103 | 50 | 179 | 92 |
| niveles | 103 | 103 | 179 | 179 |

## Por familia (norma)

| familia | n | acepta oficial | rutea el directorio | acepta V16 | fuga oficial tras τ | fuga V16 tras τ |
|---|---|---|---|---|---|---|
| gris | 33 | 3 | 0 | 10 | 0 | 1 |
| color | 12 | 1 | 0 | 2 | 1 | 2 |
| desenfoque | 128 | 66 | 2 | 121 | 6 | 16 |
| contraste | 48 | 31 | 5 | 40 | 11 | 13 |
| gris con ruido | 6 | 2 | 0 | 4 | 0 | 1 |
| estructura | 4 | 0 | 0 | 2 | 0 | 0 |

## Entradas degeneradas aceptadas por la memoria oficial

| entrada | norma | desv. latente | desv. píxeles | niveles | especialistas | directorio | d al vecino real (mediana intraclase) |
|---|---|---|---|---|---|---|---|
| gris 112 | 12.85 | 1.581 | 0.00 | 15 | horse | — | 15.7 (5.8, horse) |
| gris 120 | 11.21 | 1.384 | 0.00 | 13 | horse | — | 17.5 (5.8, horse) |
| gris 128 | 10.69 | 1.323 | 0.00 | 12 | horse | — | 18.2 (5.8, horse) |
| color (255, 0, 255) | 27.56 | 3.444 | 0.00 | 16 | apple | — | 11.5 (4.9, apple) |
| apple desenfoque r=10 | 9.89 | 1.211 | 23.69 | 14 | horse | — | 17.2 (5.8, horse) |
| apple desenfoque r=12 | 10.76 | 1.317 | 21.83 | 14 | horse | — | 16.4 (5.8, horse) |
| apple desenfoque r=14 | 11.13 | 1.362 | 20.07 | 14 | horse | — | 16.2 (5.8, horse) |
| apple desenfoque r=16 | 11.30 | 1.382 | 18.42 | 14 | horse | — | 16.1 (5.8, horse) |
| apple desenfoque r=18 | 11.36 | 1.390 | 16.89 | 14 | horse | — | 16.1 (5.8, horse) |
| apple desenfoque r=20 | 11.35 | 1.390 | 15.45 | 14 | horse | — | 16.1 (5.8, horse) |
| apple desenfoque r=22 | 11.34 | 1.390 | 14.10 | 14 | horse | — | 16.1 (5.8, horse) |
| apple desenfoque r=24 | 11.30 | 1.386 | 12.83 | 14 | horse | — | 16.2 (5.8, horse) |
| apple desenfoque r=26 | 11.27 | 1.382 | 11.61 | 14 | horse | — | 16.3 (5.8, horse) |
| apple desenfoque r=28 | 11.24 | 1.379 | 10.46 | 14 | horse | — | 16.3 (5.8, horse) |
| apple desenfoque r=30 | 11.20 | 1.376 | 9.38 | 14 | horse | — | 16.4 (5.8, horse) |
| apple desenfoque r=32 | 11.18 | 1.374 | 8.37 | 14 | horse | — | 16.4 (5.8, horse) |
| apple contraste 0.1 | 10.56 | 1.308 | 3.42 | 13 | horse | — | 18.2 (5.8, horse) |
| apple contraste 0.05 | 10.73 | 1.327 | 1.76 | 13 | horse | — | 18.0 (5.8, horse) |
| car contraste 0.5 | 37.64 | 4.701 | 19.44 | 17 | car | car | 10.9 (6.7, car) |
| car contraste 0.4 | 30.56 | 3.815 | 15.54 | 15 | car | car | 16.8 (6.7, car) |
| car contraste 0.3 | 22.40 | 2.793 | 11.68 | 14 | car | — | 22.2 (6.7, car) |
| cow desenfoque r=2 | 28.25 | 3.523 | 32.20 | 17 | cow | — | 8.7 (5.7, cow) |
| cow desenfoque r=8 | 10.99 | 1.365 | 21.83 | 14 | horse | — | 18.0 (5.8, horse) |
| cow desenfoque r=10 | 11.37 | 1.408 | 19.41 | 14 | horse | — | 17.3 (5.8, horse) |
| cow desenfoque r=12 | 11.52 | 1.426 | 17.34 | 14 | horse | — | 17.1 (5.8, horse) |
| cow desenfoque r=14 | 11.57 | 1.432 | 15.56 | 14 | horse | — | 17.0 (5.8, horse) |
| cow desenfoque r=16 | 11.58 | 1.432 | 14.05 | 14 | horse | — | 17.0 (5.8, horse) |
| cow desenfoque r=18 | 11.62 | 1.436 | 12.74 | 14 | horse | — | 16.9 (5.8, horse) |
| cow desenfoque r=20 | 11.68 | 1.443 | 11.63 | 15 | horse | — | 16.8 (5.8, horse) |
| cow desenfoque r=22 | 11.74 | 1.450 | 10.71 | 14 | horse | — | 16.7 (5.8, horse) |
| cow desenfoque r=24 | 11.81 | 1.459 | 9.96 | 14 | horse | — | 16.6 (5.8, horse) |
| cow desenfoque r=26 | 11.89 | 1.468 | 9.35 | 14 | horse | — | 16.5 (5.8, horse) |
| cow desenfoque r=28 | 11.99 | 1.480 | 8.84 | 14 | horse | — | 16.4 (5.8, horse) |
| cow desenfoque r=30 | 12.08 | 1.490 | 8.42 | 14 | horse | — | 16.3 (5.8, horse) |
| cow desenfoque r=32 | 12.17 | 1.500 | 8.02 | 14 | horse | — | 16.2 (5.8, horse) |
| cow contraste 0.5 | 38.16 | 4.764 | 18.23 | 18 | cow | cow | 4.0 (5.7, cow) |
| cow contraste 0.4 | 34.17 | 4.267 | 14.56 | 17 | cow | cow | 6.6 (5.7, cow) |
| cow contraste 0.3 | 25.79 | 3.222 | 10.95 | 15 | cow | — | 7.6 (5.7, cow) |
| cow contraste 0.2 | 15.02 | 1.878 | 7.25 | 14 | cow | — | 11.3 (5.7, cow) |
| cow contraste 0.1 | 11.36 | 1.404 | 3.68 | 13 | horse | — | 17.6 (5.8, horse) |
| cow contraste 0.05 | 12.28 | 1.513 | 1.91 | 14 | horse | — | 16.0 (5.8, horse) |
| cup desenfoque r=14 | 12.24 | 1.525 | 40.32 | 14 | horse | — | 15.6 (5.8, horse) |
| cup desenfoque r=16 | 11.45 | 1.424 | 36.51 | 14 | horse | — | 15.4 (5.8, horse) |
| cup desenfoque r=18 | 10.96 | 1.360 | 32.85 | 14 | horse | — | 15.3 (5.8, horse) |
| cup desenfoque r=20 | 10.82 | 1.340 | 29.40 | 14 | horse | — | 15.3 (5.8, horse) |
| cup desenfoque r=22 | 10.81 | 1.337 | 26.19 | 13 | horse | — | 15.3 (5.8, horse) |
| cup desenfoque r=24 | 10.88 | 1.345 | 23.20 | 14 | horse | — | 15.3 (5.8, horse) |
| cup desenfoque r=26 | 11.00 | 1.358 | 20.44 | 14 | horse | — | 15.3 (5.8, horse) |
| cup desenfoque r=28 | 11.13 | 1.373 | 17.90 | 14 | horse | — | 15.3 (5.8, horse) |
| cup desenfoque r=30 | 11.26 | 1.389 | 15.61 | 15 | horse | — | 15.3 (5.8, horse) |
| cup desenfoque r=32 | 11.40 | 1.405 | 13.58 | 15 | horse | — | 15.3 (5.8, horse) |
| cup contraste 0.5 | 21.60 | 2.661 | 32.77 | 14 | cup | — | 11.9 (4.8, cup) |
| cup contraste 0.4 | 15.28 | 1.881 | 26.23 | 14 | cup | — | 14.9 (4.8, cup) |
| cup contraste 0.1 | 10.88 | 1.350 | 6.65 | 13 | horse | — | 18.3 (5.8, horse) |
| cup contraste 0.05 | 12.32 | 1.518 | 3.43 | 14 | horse | — | 16.1 (5.8, horse) |
| dog desenfoque r=2 | 19.82 | 2.456 | 25.99 | 14 | cow | — | 12.2 (5.7, cow) |
| dog desenfoque r=6 | 16.80 | 2.060 | 22.93 | 14 | horse | — | 12.2 (5.8, horse) |
| dog desenfoque r=8 | 16.48 | 2.020 | 21.71 | 15 | horse | — | 12.2 (5.8, horse) |
| dog desenfoque r=10 | 16.11 | 1.974 | 20.53 | 14 | horse | — | 12.5 (5.8, horse) |
| dog desenfoque r=12 | 15.76 | 1.933 | 19.37 | 12 | horse | — | 12.9 (5.8, horse) |
| dog desenfoque r=14 | 15.49 | 1.900 | 18.21 | 12 | horse | — | 13.2 (5.8, horse) |
| dog desenfoque r=16 | 15.20 | 1.866 | 17.09 | 12 | horse | — | 13.4 (5.8, horse) |
| dog desenfoque r=18 | 14.93 | 1.834 | 16.00 | 12 | horse | — | 13.7 (5.8, horse) |
| dog desenfoque r=20 | 14.68 | 1.804 | 14.96 | 13 | horse | — | 13.9 (5.8, horse) |
| dog desenfoque r=22 | 14.43 | 1.773 | 13.95 | 13 | horse | — | 14.1 (5.8, horse) |
| dog desenfoque r=24 | 14.18 | 1.744 | 12.99 | 13 | horse | — | 14.3 (5.8, horse) |
| dog desenfoque r=26 | 13.99 | 1.720 | 12.11 | 13 | horse | — | 14.4 (5.8, horse) |
| dog desenfoque r=28 | 13.83 | 1.701 | 11.33 | 13 | horse | — | 14.5 (5.8, horse) |
| dog desenfoque r=30 | 13.68 | 1.682 | 10.56 | 13 | horse | — | 14.7 (5.8, horse) |
| dog desenfoque r=32 | 13.54 | 1.666 | 9.86 | 13 | horse | — | 14.8 (5.8, horse) |
| dog contraste 0.5 | 13.56 | 1.641 | 14.14 | 13 | dog | — | 22.2 (6.7, dog) |
| dog contraste 0.2 | 11.69 | 1.444 | 5.67 | 13 | horse | — | 18.3 (5.8, horse) |
| dog contraste 0.1 | 11.17 | 1.380 | 2.85 | 12 | horse | — | 17.5 (5.8, horse) |
| dog contraste 0.05 | 11.27 | 1.391 | 1.47 | 13 | horse | — | 17.2 (5.8, horse) |
| horse desenfoque r=2 | 32.48 | 4.002 | 25.55 | 17 | horse | horse | 7.2 (5.8, horse) |
| horse desenfoque r=4 | 26.78 | 3.294 | 22.52 | 16 | horse | — | 5.8 (5.8, horse) |
| horse contraste 0.5 | 25.21 | 3.092 | 14.48 | 17 | horse | — | 7.2 (5.8, horse) |
| horse contraste 0.4 | 20.76 | 2.550 | 11.59 | 17 | horse | — | 7.9 (5.8, horse) |
| horse contraste 0.3 | 15.66 | 1.930 | 8.72 | 15 | horse | — | 12.1 (5.8, horse) |
| horse contraste 0.2 | 12.56 | 1.556 | 5.84 | 12 | horse | — | 16.6 (5.8, horse) |
| horse contraste 0.1 | 11.29 | 1.402 | 2.96 | 12 | horse | — | 18.5 (5.8, horse) |
| horse contraste 0.05 | 10.78 | 1.335 | 1.51 | 12 | horse | — | 18.2 (5.8, horse) |
| pear desenfoque r=10 | 10.56 | 1.312 | 25.21 | 12 | horse | — | 19.1 (5.8, horse) |
| pear desenfoque r=12 | 10.37 | 1.284 | 23.31 | 12 | horse | — | 18.1 (5.8, horse) |
| pear desenfoque r=14 | 10.35 | 1.279 | 21.40 | 12 | horse | — | 17.6 (5.8, horse) |
| pear desenfoque r=16 | 10.38 | 1.280 | 19.51 | 15 | horse | — | 17.3 (5.8, horse) |
| pear desenfoque r=18 | 10.44 | 1.287 | 17.68 | 14 | horse | — | 17.2 (5.8, horse) |
| pear desenfoque r=20 | 10.51 | 1.295 | 15.92 | 14 | horse | — | 17.2 (5.8, horse) |
| pear desenfoque r=22 | 10.59 | 1.305 | 14.26 | 14 | horse | — | 17.1 (5.8, horse) |
| pear desenfoque r=24 | 10.67 | 1.315 | 12.72 | 14 | horse | — | 17.1 (5.8, horse) |
| pear desenfoque r=26 | 10.75 | 1.325 | 11.29 | 14 | horse | — | 17.0 (5.8, horse) |
| pear desenfoque r=28 | 10.85 | 1.336 | 10.01 | 14 | horse | — | 16.9 (5.8, horse) |
| pear desenfoque r=30 | 10.95 | 1.348 | 8.86 | 14 | horse | — | 16.9 (5.8, horse) |
| pear desenfoque r=32 | 11.06 | 1.362 | 7.85 | 14 | horse | — | 16.8 (5.8, horse) |
| pear contraste 0.4 | 25.06 | 3.130 | 13.20 | 16 | cow | cow | 10.7 (5.7, cow) |
| pear contraste 0.3 | 24.04 | 3.004 | 9.92 | 14 | cow | — | 9.2 (5.7, cow) |
| pear contraste 0.1 | 11.12 | 1.376 | 3.36 | 12 | horse | — | 18.0 (5.8, horse) |
| pear contraste 0.05 | 11.29 | 1.394 | 1.76 | 13 | horse | — | 17.3 (5.8, horse) |
| tomato desenfoque r=2 | 28.84 | 3.597 | 42.16 | 18 | tomato | tomato | 2.5 (3.4, tomato) |
| tomato contraste 0.1 | 10.89 | 1.346 | 4.39 | 14 | horse | — | 17.8 (5.8, horse) |
| tomato contraste 0.05 | 10.89 | 1.346 | 2.27 | 14 | horse | — | 17.9 (5.8, horse) |
| gris 127 + ruido sigma=1 | 10.70 | 1.327 | 0.74 | 12 | horse | — | 18.4 (5.8, horse) |
| gris 127 + ruido sigma=2 | 10.76 | 1.336 | 1.37 | 12 | horse | — | 18.8 (5.8, horse) |

## Curva de τ (norma)

| τ | test rechazadas | fase A rechazadas | fuga oficial | fuga V16 |
|---|---|---|---|---|
| 6.0 | 0 | 0 | 103 | 179 |
| 8.0 | 0 | 0 | 103 | 178 |
| 10.0 | 0 | 0 | 102 | 174 |
| 12.0 | 1 | 0 | 42 | 105 |
| 14.0 | 2 | 0 | 30 | 80 |
| 16.0 | 3 | 1 | 20 | 36 |
| 18.0 | 5 | 1 | 17 | 27 |
| 20.0 | 7 | 1 | 16 | 24 |
| 22.0 | 9 | 2 | 14 | 18 |
| 24.0 | 16 | 3 | 13 | 16 |
| 26.0 | 19 | 5 | 9 | 10 |
| 28.0 | 20 | 7 | 7 | 8 |
| 30.0 | 28 | 16 | 5 | 6 |
| 32.0 | 43 | 31 | 4 | 5 |

## Archivos
- `resumen.json`, `banco_degenerado.json` (fila por entrada), `reales.json` (estadísticos de llenado, fase A y test)
- `fig1_norma_vs_aceptacion.png`
