# Experimento 14 — criterio de energía mínima del latente

Calibración: mínimo sobre los 1600 originales del llenado con margen 10% (niveles: mínimo menos uno). Banco degenerado generado como declara `propuesta_exp14_energia_latente.md` §4. Memoria oficial: agentes v5 (contenido y directorio, entrada `apple`); V16: contenido de exp13 con 16 variantes. Diseño y criterio en la propuesta.

## Umbrales y costo sobre imágenes reales

| estadístico | τ | mínimo llenado | rechaza llenado (1600) | rechaza fase A (1024) | rechaza test (656) |
|---|---|---|---|---|---|
| norma | 16.607 | 18.453 | 0 | 1 | 4 |
| desv_latente | 2.076 | 2.306 | 0 | 1 | 5 |
| desv_pixeles | 13.864 | 15.404 | 0 | 0 | 0 |
| niveles | 12.000 | 13.000 | 0 | 3 | 1 |

Imágenes de test rechazadas por la norma:

- `cow3-035-135.png` (cow): norma 13.95; contenido propio acepta; directorio → cow
- `cow3-068-090.png` (cow): norma 16.56; contenido propio acepta; directorio → cow
- `cow3-066-117.png` (cow): norma 10.78; contenido propio acepta; directorio → cow
- `cow6-035-045.png` (cow): norma 15.11; contenido propio acepta; directorio → cow

## Fuga: entradas degeneradas que la memoria acepta y el criterio deja pasar

Banco: 231 entradas. «Acepta»: algún especialista da soporte o el directorio rutea.

| estadístico | acepta la memoria oficial | pasan el criterio | acepta el contenido V16 | pasan el criterio |
|---|---|---|---|---|
| norma | 180 | 33 | 179 | 33 |
| desv_latente | 180 | 31 | 179 | 31 |
| desv_pixeles | 180 | 92 | 179 | 92 |
| niveles | 180 | 180 | 179 | 179 |

## Por familia (norma)

| familia | n | acepta oficial | rutea el directorio | acepta V16 | fuga oficial tras τ | fuga V16 tras τ |
|---|---|---|---|---|---|---|
| gris | 33 | 10 | 6 | 10 | 1 | 1 |
| color | 12 | 2 | 1 | 2 | 2 | 2 |
| desenfoque | 128 | 121 | 114 | 121 | 16 | 16 |
| contraste | 48 | 41 | 38 | 40 | 13 | 13 |
| gris con ruido | 6 | 4 | 4 | 4 | 1 | 1 |
| estructura | 4 | 2 | 1 | 2 | 0 | 0 |

## Entradas degeneradas aceptadas por la memoria oficial

| entrada | norma | desv. latente | desv. píxeles | niveles | especialistas | directorio | d al vecino real (mediana intraclase) |
|---|---|---|---|---|---|---|---|
| gris 104 | 15.86 | 1.950 | 0.00 | 14 | dog | dog | 29.5 (6.7, dog) |
| gris 112 | 12.85 | 1.581 | 0.00 | 15 | dog,horse | horse | 29.6 (6.7, dog) |
| gris 120 | 11.21 | 1.384 | 0.00 | 13 | cow,dog,horse | horse | 13.9 (5.7, cow) |
| gris 128 | 10.69 | 1.323 | 0.00 | 12 | cow,dog,horse | horse | 14.2 (5.7, cow) |
| gris 136 | 10.73 | 1.331 | 0.00 | 12 | cow,dog,horse | dog | 14.6 (5.7, cow) |
| gris 144 | 11.23 | 1.393 | 0.00 | 14 | cow,dog,horse | dog | 15.0 (5.7, cow) |
| gris 152 | 11.95 | 1.482 | 0.00 | 14 | cow,dog,horse | — | 15.6 (5.7, cow) |
| gris 160 | 13.04 | 1.618 | 0.00 | 13 | cow,dog,horse | — | 16.5 (5.7, cow) |
| gris 168 | 14.78 | 1.836 | 0.00 | 13 | cow,dog | — | 17.9 (5.7, cow) |
| gris 176 | 17.34 | 2.156 | 0.00 | 14 | cow | — | 19.9 (5.7, cow) |
| color (255, 0, 255) | 27.56 | 3.444 | 0.00 | 16 | apple | apple | 11.5 (4.9, apple) |
| color (63, 77, 150) | 18.80 | 2.300 | 0.00 | 14 | dog | — | 27.7 (6.7, dog) |
| apple desenfoque r=2 | 14.55 | 1.819 | 31.67 | 14 | apple | apple | 19.7 (4.9, apple) |
| apple desenfoque r=4 | 10.91 | 1.363 | 29.56 | 14 | apple | apple | 18.6 (4.9, apple) |
| apple desenfoque r=6 | 7.21 | 0.897 | 27.57 | 14 | apple | dog | 23.1 (4.9, apple) |
| apple desenfoque r=8 | 8.11 | 0.996 | 25.61 | 14 | dog,horse | horse | 28.5 (6.7, dog) |
| apple desenfoque r=10 | 9.89 | 1.211 | 23.69 | 14 | dog,horse | dog | 28.2 (6.7, dog) |
| apple desenfoque r=12 | 10.76 | 1.317 | 21.83 | 14 | dog,horse | horse | 28.1 (6.7, dog) |
| apple desenfoque r=14 | 11.13 | 1.362 | 20.07 | 14 | dog,horse | horse | 28.1 (6.7, dog) |
| apple desenfoque r=16 | 11.30 | 1.382 | 18.42 | 14 | dog,horse | horse | 28.1 (6.7, dog) |
| apple desenfoque r=18 | 11.36 | 1.390 | 16.89 | 14 | cow,dog,horse | horse | 15.6 (5.7, cow) |
| apple desenfoque r=20 | 11.35 | 1.390 | 15.45 | 14 | cow,dog,horse | horse | 15.6 (5.7, cow) |
| apple desenfoque r=22 | 11.34 | 1.390 | 14.10 | 14 | cow,dog,horse | horse | 15.5 (5.7, cow) |
| apple desenfoque r=24 | 11.30 | 1.386 | 12.83 | 14 | cow,dog,horse | horse | 15.5 (5.7, cow) |
| apple desenfoque r=26 | 11.27 | 1.382 | 11.61 | 14 | cow,dog,horse | horse | 15.5 (5.7, cow) |
| apple desenfoque r=28 | 11.24 | 1.379 | 10.46 | 14 | cow,dog,horse | horse | 15.5 (5.7, cow) |
| apple desenfoque r=30 | 11.20 | 1.376 | 9.38 | 14 | cow,dog,horse | horse | 15.5 (5.7, cow) |
| apple desenfoque r=32 | 11.18 | 1.374 | 8.37 | 14 | cow,dog,horse | horse | 15.5 (5.7, cow) |
| apple contraste 0.5 | 24.72 | 3.085 | 16.85 | 15 | apple | apple | 7.9 (4.9, apple) |
| apple contraste 0.4 | 20.18 | 2.517 | 13.50 | 14 | apple | apple | 10.7 (4.9, apple) |
| apple contraste 0.3 | 14.32 | 1.788 | 10.12 | 14 | apple | apple | 17.0 (4.9, apple) |
| apple contraste 0.1 | 10.56 | 1.308 | 3.42 | 13 | cow,dog,horse | horse | 14.2 (5.7, cow) |
| apple contraste 0.05 | 10.73 | 1.327 | 1.76 | 13 | cow,dog,horse | horse | 14.1 (5.7, cow) |
| car desenfoque r=2 | 33.34 | 4.167 | 34.49 | 16 | car | car | 15.7 (6.7, car) |
| car desenfoque r=6 | 21.00 | 2.603 | 28.18 | 16 | horse | — | 9.9 (5.8, horse) |
| car desenfoque r=8 | 18.50 | 2.290 | 25.46 | 14 | cow,dog,horse | dog | 18.3 (5.7, cow) |
| car desenfoque r=10 | 16.97 | 2.100 | 22.99 | 14 | cow,dog,horse | dog | 16.7 (5.7, cow) |
| car desenfoque r=12 | 16.31 | 2.018 | 20.86 | 13 | cow,dog,horse | dog | 16.1 (5.7, cow) |
| car desenfoque r=14 | 15.95 | 1.975 | 19.06 | 13 | cow,dog,horse | dog | 15.8 (5.7, cow) |
| car desenfoque r=16 | 15.65 | 1.938 | 17.56 | 13 | cow,dog,horse | dog | 15.7 (5.7, cow) |
| car desenfoque r=18 | 15.44 | 1.911 | 16.28 | 13 | cow,dog,horse | dog | 15.6 (5.7, cow) |
| car desenfoque r=20 | 15.26 | 1.889 | 15.22 | 13 | cow,dog,horse | dog | 15.5 (5.7, cow) |
| car desenfoque r=22 | 15.07 | 1.865 | 14.29 | 12 | cow,dog,horse | dog | 15.5 (5.7, cow) |
| car desenfoque r=24 | 14.90 | 1.844 | 13.44 | 12 | cow,dog,horse | dog | 15.4 (5.7, cow) |
| car desenfoque r=26 | 14.73 | 1.823 | 12.70 | 12 | cow,dog,horse | dog | 15.4 (5.7, cow) |
| car desenfoque r=28 | 14.58 | 1.804 | 11.99 | 12 | cow,dog,horse | dog | 15.3 (5.7, cow) |
| car desenfoque r=30 | 14.48 | 1.792 | 11.37 | 13 | cow,dog,horse | dog | 15.3 (5.7, cow) |
| car desenfoque r=32 | 14.38 | 1.778 | 10.81 | 13 | cow,dog,horse | dog | 15.3 (5.7, cow) |
| car contraste 0.5 | 37.64 | 4.701 | 19.44 | 17 | car | car | 10.9 (6.7, car) |
| car contraste 0.4 | 30.56 | 3.815 | 15.54 | 15 | car | car | 16.8 (6.7, car) |
| car contraste 0.3 | 22.40 | 2.793 | 11.68 | 14 | car | car | 22.2 (6.7, car) |
| car contraste 0.2 | 13.82 | 1.719 | 7.73 | 12 | car | — | 30.6 (6.7, car) |
| car contraste 0.05 | 10.97 | 1.363 | 2.09 | 12 | dog,horse | dog | 31.2 (6.7, dog) |
| cow desenfoque r=2 | 28.25 | 3.523 | 32.20 | 17 | cow | cow | 8.7 (5.7, cow) |
| cow desenfoque r=4 | 15.27 | 1.905 | 28.04 | 14 | cow | — | 13.7 (5.7, cow) |
| cow desenfoque r=6 | 10.92 | 1.364 | 24.67 | 13 | cow,dog | dog | 12.1 (5.7, cow) |
| cow desenfoque r=8 | 10.99 | 1.365 | 21.83 | 14 | cow,dog,horse | dog | 12.0 (5.7, cow) |
| cow desenfoque r=10 | 11.37 | 1.408 | 19.41 | 14 | cow,dog,horse | dog | 12.0 (5.7, cow) |
| cow desenfoque r=12 | 11.52 | 1.426 | 17.34 | 14 | cow,dog,horse | dog | 12.2 (5.7, cow) |
| cow desenfoque r=14 | 11.57 | 1.432 | 15.56 | 14 | cow,dog,horse | dog | 12.3 (5.7, cow) |
| cow desenfoque r=16 | 11.58 | 1.432 | 14.05 | 14 | cow,dog,horse | dog | 12.4 (5.7, cow) |
| cow desenfoque r=18 | 11.62 | 1.436 | 12.74 | 14 | cow,dog,horse | dog | 12.5 (5.7, cow) |
| cow desenfoque r=20 | 11.68 | 1.443 | 11.63 | 15 | cow,dog,horse | dog | 12.6 (5.7, cow) |
| cow desenfoque r=22 | 11.74 | 1.450 | 10.71 | 14 | cow,dog,horse | dog | 12.7 (5.7, cow) |
| cow desenfoque r=24 | 11.81 | 1.459 | 9.96 | 14 | cow,dog,horse | horse | 12.8 (5.7, cow) |
| cow desenfoque r=26 | 11.89 | 1.468 | 9.35 | 14 | cow,dog,horse | horse | 12.9 (5.7, cow) |
| cow desenfoque r=28 | 11.99 | 1.480 | 8.84 | 14 | cow,dog,horse | horse | 12.9 (5.7, cow) |
| cow desenfoque r=30 | 12.08 | 1.490 | 8.42 | 14 | cow,dog,horse | horse | 12.9 (5.7, cow) |
| cow desenfoque r=32 | 12.17 | 1.500 | 8.02 | 14 | cow,dog,horse | horse | 12.9 (5.7, cow) |
| cow contraste 0.5 | 38.16 | 4.764 | 18.23 | 18 | cow | cow | 4.0 (5.7, cow) |
| cow contraste 0.4 | 34.17 | 4.267 | 14.56 | 17 | cow | cow | 6.6 (5.7, cow) |
| cow contraste 0.3 | 25.79 | 3.222 | 10.95 | 15 | cow | cow | 7.6 (5.7, cow) |
| cow contraste 0.2 | 15.02 | 1.878 | 7.25 | 14 | cow | dog | 11.3 (5.7, cow) |
| cow contraste 0.1 | 11.36 | 1.404 | 3.68 | 13 | cow,dog,horse | horse | 13.7 (5.7, cow) |
| cow contraste 0.05 | 12.28 | 1.513 | 1.91 | 14 | dog,horse | horse | 29.8 (6.7, dog) |
| cup desenfoque r=6 | 20.37 | 2.544 | 55.86 | 12 | apple | — | 22.3 (4.9, apple) |
| cup desenfoque r=8 | 17.37 | 2.171 | 52.10 | 12 | apple | — | 23.8 (4.9, apple) |
| cup desenfoque r=10 | 15.12 | 1.890 | 48.19 | 13 | horse | — | 17.3 (5.8, horse) |
| cup desenfoque r=12 | 13.48 | 1.683 | 44.24 | 13 | dog,horse | dog | 30.4 (6.7, dog) |
| cup desenfoque r=14 | 12.24 | 1.525 | 40.32 | 14 | dog,horse | horse | 29.7 (6.7, dog) |
| cup desenfoque r=16 | 11.45 | 1.424 | 36.51 | 14 | dog,horse | horse | 29.3 (6.7, dog) |
| cup desenfoque r=18 | 10.96 | 1.360 | 32.85 | 14 | dog,horse | horse | 29.0 (6.7, dog) |
| cup desenfoque r=20 | 10.82 | 1.340 | 29.40 | 14 | dog,horse | horse | 28.9 (6.7, dog) |
| cup desenfoque r=22 | 10.81 | 1.337 | 26.19 | 13 | dog,horse | horse | 28.9 (6.7, dog) |
| cup desenfoque r=24 | 10.88 | 1.345 | 23.20 | 14 | dog,horse | horse | 28.8 (6.7, dog) |
| cup desenfoque r=26 | 11.00 | 1.358 | 20.44 | 14 | dog,horse | horse | 28.8 (6.7, dog) |
| cup desenfoque r=28 | 11.13 | 1.373 | 17.90 | 14 | dog,horse | horse | 28.8 (6.7, dog) |
| cup desenfoque r=30 | 11.26 | 1.389 | 15.61 | 15 | dog,horse | horse | 28.8 (6.7, dog) |
| cup desenfoque r=32 | 11.40 | 1.405 | 13.58 | 15 | cow,dog,horse | horse | 14.1 (5.7, cow) |
| cup contraste 0.5 | 21.60 | 2.661 | 32.77 | 14 | cup | cup | 11.9 (4.8, cup) |
| cup contraste 0.4 | 15.28 | 1.881 | 26.23 | 14 | cup | cup | 14.9 (4.8, cup) |
| cup contraste 0.2 | 8.85 | 1.106 | 13.14 | 14 | — | dog | — |
| cup contraste 0.1 | 10.88 | 1.350 | 6.65 | 13 | dog,horse | horse | 31.2 (6.7, dog) |
| cup contraste 0.05 | 12.32 | 1.518 | 3.43 | 14 | dog,horse | horse | 29.9 (6.7, dog) |
| dog desenfoque r=2 | 19.82 | 2.456 | 25.99 | 14 | cow | cow | 12.2 (5.7, cow) |
| dog desenfoque r=4 | 17.24 | 2.123 | 24.31 | 13 | cow,dog,horse | dog | 15.5 (5.7, cow) |
| dog desenfoque r=6 | 16.80 | 2.060 | 22.93 | 14 | cow,dog,horse | horse | 16.6 (5.7, cow) |
| dog desenfoque r=8 | 16.48 | 2.020 | 21.71 | 15 | cow,dog,horse | horse | 16.7 (5.7, cow) |
| dog desenfoque r=10 | 16.11 | 1.974 | 20.53 | 14 | cow,dog,horse | horse | 16.4 (5.7, cow) |
| dog desenfoque r=12 | 15.76 | 1.933 | 19.37 | 12 | cow,dog,horse | horse | 16.1 (5.7, cow) |
| dog desenfoque r=14 | 15.49 | 1.900 | 18.21 | 12 | cow,dog,horse | horse | 15.8 (5.7, cow) |
| dog desenfoque r=16 | 15.20 | 1.866 | 17.09 | 12 | cow,dog,horse | horse | 15.6 (5.7, cow) |
| dog desenfoque r=18 | 14.93 | 1.834 | 16.00 | 12 | cow,dog,horse | horse | 15.3 (5.7, cow) |
| dog desenfoque r=20 | 14.68 | 1.804 | 14.96 | 13 | cow,dog,horse | horse | 15.2 (5.7, cow) |
| dog desenfoque r=22 | 14.43 | 1.773 | 13.95 | 13 | cow,dog,horse | horse | 15.0 (5.7, cow) |
| dog desenfoque r=24 | 14.18 | 1.744 | 12.99 | 13 | cow,dog,horse | horse | 14.9 (5.7, cow) |
| dog desenfoque r=26 | 13.99 | 1.720 | 12.11 | 13 | cow,dog,horse | horse | 14.8 (5.7, cow) |
| dog desenfoque r=28 | 13.83 | 1.701 | 11.33 | 13 | cow,dog,horse | horse | 14.7 (5.7, cow) |
| dog desenfoque r=30 | 13.68 | 1.682 | 10.56 | 13 | cow,dog,horse | horse | 14.7 (5.7, cow) |
| dog desenfoque r=32 | 13.54 | 1.666 | 9.86 | 13 | cow,dog,horse | horse | 14.7 (5.7, cow) |
| dog contraste 0.5 | 13.56 | 1.641 | 14.14 | 13 | dog | dog | 22.2 (6.7, dog) |
| dog contraste 0.4 | 12.33 | 1.500 | 11.32 | 12 | cow,dog | dog | 16.8 (5.7, cow) |
| dog contraste 0.3 | 11.91 | 1.463 | 8.49 | 12 | cow,dog | dog | 15.4 (5.7, cow) |
| dog contraste 0.2 | 11.69 | 1.444 | 5.67 | 13 | dog,horse | horse | 29.4 (6.7, dog) |
| dog contraste 0.1 | 11.17 | 1.380 | 2.85 | 12 | cow,dog,horse | horse | 14.5 (5.7, cow) |
| dog contraste 0.05 | 11.27 | 1.391 | 1.47 | 13 | cow,dog,horse | horse | 13.9 (5.7, cow) |
| horse desenfoque r=2 | 32.48 | 4.002 | 25.55 | 17 | horse | horse | 7.2 (5.8, horse) |
| horse desenfoque r=4 | 26.78 | 3.294 | 22.52 | 16 | horse | horse | 5.8 (5.8, horse) |
| horse desenfoque r=6 | 21.22 | 2.607 | 20.07 | 15 | horse | horse | 6.4 (5.8, horse) |
| horse desenfoque r=8 | 16.89 | 2.073 | 17.99 | 14 | cow,dog,horse | horse | 18.4 (5.7, cow) |
| horse desenfoque r=10 | 15.49 | 1.903 | 16.29 | 12 | cow,dog,horse | horse | 17.0 (5.7, cow) |
| horse desenfoque r=12 | 14.98 | 1.841 | 14.75 | 12 | cow,dog,horse | dog | 16.6 (5.7, cow) |
| horse desenfoque r=14 | 14.67 | 1.803 | 13.36 | 12 | cow,dog,horse | dog | 16.3 (5.7, cow) |
| horse desenfoque r=16 | 14.40 | 1.770 | 12.11 | 13 | cow,dog,horse | dog | 16.2 (5.7, cow) |
| horse desenfoque r=18 | 14.18 | 1.744 | 10.98 | 13 | cow,dog,horse | dog | 16.0 (5.7, cow) |
| horse desenfoque r=20 | 14.00 | 1.723 | 9.90 | 13 | cow,dog,horse | dog | 15.9 (5.7, cow) |
| horse desenfoque r=22 | 13.82 | 1.700 | 8.94 | 13 | cow,dog,horse | dog | 15.8 (5.7, cow) |
| horse desenfoque r=24 | 13.67 | 1.682 | 8.05 | 13 | cow,dog,horse | dog | 15.7 (5.7, cow) |
| horse desenfoque r=26 | 13.54 | 1.666 | 7.24 | 13 | cow,dog,horse | dog | 15.6 (5.7, cow) |
| horse desenfoque r=28 | 13.43 | 1.653 | 6.47 | 13 | cow,dog,horse | dog | 15.5 (5.7, cow) |
| horse desenfoque r=30 | 13.36 | 1.644 | 5.82 | 13 | cow,dog,horse | dog | 15.5 (5.7, cow) |
| horse desenfoque r=32 | 13.28 | 1.635 | 5.26 | 13 | cow,dog,horse | dog | 15.5 (5.7, cow) |
| horse contraste 0.5 | 25.21 | 3.092 | 14.48 | 17 | horse | horse | 7.2 (5.8, horse) |
| horse contraste 0.4 | 20.76 | 2.550 | 11.59 | 17 | horse | horse | 7.9 (5.8, horse) |
| horse contraste 0.3 | 15.66 | 1.930 | 8.72 | 15 | cow,dog,horse | horse | 17.0 (5.7, cow) |
| horse contraste 0.2 | 12.56 | 1.556 | 5.84 | 12 | dog,horse | horse | 31.4 (6.7, dog) |
| horse contraste 0.1 | 11.29 | 1.402 | 2.96 | 12 | dog,horse | horse | 31.0 (6.7, dog) |
| horse contraste 0.05 | 10.78 | 1.335 | 1.51 | 12 | cow,dog,horse | horse | 14.6 (5.7, cow) |
| pear desenfoque r=2 | 25.51 | 3.179 | 31.75 | 15 | pear | — | 13.9 (5.5, pear) |
| pear desenfoque r=4 | 15.00 | 1.869 | 30.34 | 14 | cow | — | 16.9 (5.7, cow) |
| pear desenfoque r=10 | 10.56 | 1.312 | 25.21 | 12 | dog,horse | horse | 30.3 (6.7, dog) |
| pear desenfoque r=12 | 10.37 | 1.284 | 23.31 | 12 | cow,dog,horse | horse | 15.1 (5.7, cow) |
| pear desenfoque r=14 | 10.35 | 1.279 | 21.40 | 12 | cow,dog,horse | horse | 14.9 (5.7, cow) |
| pear desenfoque r=16 | 10.38 | 1.280 | 19.51 | 15 | cow,dog,horse | horse | 14.7 (5.7, cow) |
| pear desenfoque r=18 | 10.44 | 1.287 | 17.68 | 14 | cow,dog,horse | horse | 14.5 (5.7, cow) |
| pear desenfoque r=20 | 10.51 | 1.295 | 15.92 | 14 | cow,dog,horse | horse | 14.3 (5.7, cow) |
| pear desenfoque r=22 | 10.59 | 1.305 | 14.26 | 14 | cow,dog,horse | horse | 14.2 (5.7, cow) |
| pear desenfoque r=24 | 10.67 | 1.315 | 12.72 | 14 | cow,dog,horse | horse | 14.1 (5.7, cow) |
| pear desenfoque r=26 | 10.75 | 1.325 | 11.29 | 14 | cow,dog,horse | horse | 14.0 (5.7, cow) |
| pear desenfoque r=28 | 10.85 | 1.336 | 10.01 | 14 | cow,dog,horse | horse | 14.0 (5.7, cow) |
| pear desenfoque r=30 | 10.95 | 1.348 | 8.86 | 14 | cow,dog,horse | horse | 14.0 (5.7, cow) |
| pear desenfoque r=32 | 11.06 | 1.362 | 7.85 | 14 | cow,dog,horse | horse | 13.9 (5.7, cow) |
| pear contraste 0.4 | 25.06 | 3.130 | 13.20 | 16 | cow | cow | 10.7 (5.7, cow) |
| pear contraste 0.3 | 24.04 | 3.004 | 9.92 | 14 | cow | — | 9.2 (5.7, cow) |
| pear contraste 0.2 | 15.17 | 1.896 | 6.57 | 14 | cow | — | 12.1 (5.7, cow) |
| pear contraste 0.1 | 11.12 | 1.376 | 3.36 | 12 | cow,dog,horse | horse | 14.0 (5.7, cow) |
| pear contraste 0.05 | 11.29 | 1.394 | 1.76 | 13 | cow,dog,horse | horse | 13.9 (5.7, cow) |
| tomato desenfoque r=2 | 28.84 | 3.597 | 42.16 | 18 | tomato | tomato | 2.5 (3.4, tomato) |
| tomato desenfoque r=8 | 9.49 | 1.175 | 36.53 | 14 | dog | dog | 29.1 (6.7, dog) |
| tomato desenfoque r=10 | 11.72 | 1.448 | 34.30 | 14 | dog | dog | 29.1 (6.7, dog) |
| tomato desenfoque r=12 | 13.14 | 1.622 | 32.05 | 14 | dog | dog | 29.2 (6.7, dog) |
| tomato desenfoque r=14 | 13.87 | 1.711 | 29.85 | 14 | dog | dog | 29.2 (6.7, dog) |
| tomato desenfoque r=16 | 14.32 | 1.766 | 27.69 | 14 | dog | dog | 29.2 (6.7, dog) |
| tomato desenfoque r=18 | 14.66 | 1.805 | 25.61 | 15 | dog | dog | 29.2 (6.7, dog) |
| tomato desenfoque r=20 | 14.90 | 1.835 | 23.59 | 15 | dog | dog | 29.1 (6.7, dog) |
| tomato desenfoque r=22 | 15.02 | 1.849 | 21.62 | 15 | cow,dog | dog | 13.8 (5.7, cow) |
| tomato desenfoque r=24 | 15.11 | 1.859 | 19.71 | 15 | cow,dog | dog | 13.7 (5.7, cow) |
| tomato desenfoque r=26 | 15.18 | 1.867 | 17.84 | 15 | cow,dog,horse | horse | 13.7 (5.7, cow) |
| tomato desenfoque r=28 | 15.16 | 1.864 | 16.08 | 15 | cow,dog,horse | horse | 13.7 (5.7, cow) |
| tomato desenfoque r=30 | 15.13 | 1.861 | 14.42 | 15 | cow,dog,horse | horse | 13.6 (5.7, cow) |
| tomato desenfoque r=32 | 15.09 | 1.855 | 12.85 | 15 | cow,dog,horse | horse | 13.6 (5.7, cow) |
| tomato contraste 0.2 | 9.42 | 1.167 | 8.65 | 13 | dog | dog | 30.2 (6.7, dog) |
| tomato contraste 0.1 | 10.89 | 1.346 | 4.39 | 14 | cow,dog,horse | horse | 13.9 (5.7, cow) |
| tomato contraste 0.05 | 10.89 | 1.346 | 2.27 | 14 | cow,dog,horse | horse | 13.9 (5.7, cow) |
| gris 127 + ruido sigma=1 | 10.70 | 1.327 | 0.74 | 12 | cow,dog,horse | horse | 14.3 (5.7, cow) |
| gris 127 + ruido sigma=2 | 10.76 | 1.336 | 1.37 | 12 | dog,horse | horse | 31.1 (6.7, dog) |
| gris 127 + ruido sigma=4 | 11.20 | 1.392 | 2.68 | 12 | dog,horse | dog | 31.4 (6.7, dog) |
| gris 127 + ruido sigma=8 | 22.64 | 2.828 | 5.33 | 13 | apple | apple | 16.4 (4.9, apple) |
| gradiente horizontal | 12.99 | 1.622 | 73.91 | 13 | dog | dog | 30.8 (6.7, dog) |
| gradiente radial | 15.41 | 1.925 | 51.55 | 13 | apple | — | 23.6 (4.9, apple) |

## Curva de τ (norma)

| τ | test rechazadas | fase A rechazadas | fuga oficial | fuga V16 |
|---|---|---|---|---|
| 6.0 | 0 | 0 | 180 | 179 |
| 8.0 | 0 | 0 | 179 | 178 |
| 10.0 | 0 | 0 | 174 | 174 |
| 12.0 | 1 | 0 | 105 | 105 |
| 14.0 | 2 | 0 | 80 | 80 |
| 16.0 | 3 | 1 | 36 | 36 |
| 18.0 | 5 | 1 | 27 | 27 |
| 20.0 | 7 | 1 | 24 | 24 |
| 22.0 | 9 | 2 | 18 | 18 |
| 24.0 | 16 | 3 | 16 | 16 |
| 26.0 | 19 | 5 | 10 | 10 |
| 28.0 | 20 | 7 | 8 | 8 |
| 30.0 | 28 | 16 | 6 | 6 |
| 32.0 | 43 | 31 | 5 | 5 |

## Archivos
- `resumen.json`, `banco_degenerado.json` (fila por entrada), `reales.json` (estadísticos de llenado, fase A y test)
- `fig1_norma_vs_aceptacion.png`
