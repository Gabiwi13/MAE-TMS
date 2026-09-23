# Experimento 13 — augmentación del llenado visual

656 imágenes de test (82 por clase). Intervalos: bootstrap del 95 % sobre las medias por semilla. Contenido: `recognize_gated_right` del especialista propio. Responde: `recall_from_right` del especialista propio reconoce (proyección sin filas vacías, el criterio de `recall_from_right`). Hit estricto y otro dominio: sobre las respuestas de las primeras 5 imágenes de test por clase, con la evocación completa. Directorio: `route_transactive` desde una entrada no especialista, ξ = 0. e2e: rutea a la clase correcta y el destino responde. Falso contenido: algún especialista ajeno acepta. Diseño en `propuesta_exp13_augmentacion_visual.md`.

Control: Vc=4, N=200 igual a los `agent_*.pkl` oficiales en 8/8 clases.
Encoder en GPU contra los latentes oficiales (variantes 0-3 de train[:200], cuantizados): 148 niveles distintos de 409600 (0.036 %); se usan los oficiales.

## A0: oficial (Vc=4, Vd=1)

| V | contenido acepta | responde | hit estricto | otro dominio | falso contenido | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | densidad R | densidad dir |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 93.6 [93.6, 93.6] | 76.2 [76.2, 76.2] | 98.8 [97.6, 100.0] | 1.8 [0.0, 4.2] | 0.2 [0.2, 0.2] | 73.6 [73.6, 73.6] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 66.5 [66.5, 66.5] | 35.4 % | 69.1 % |

## A1: solo directorio (Vc=4, Vd=V)

| V | contenido acepta | responde | hit estricto | otro dominio | falso contenido | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | densidad R | densidad dir |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 93.6 [93.6, 93.6] | 76.2 [76.2, 76.2] | 98.8 [97.6, 100.0] | 1.2 [0.0, 2.4] | 0.2 [0.2, 0.2] | 87.7 [87.7, 87.7] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 74.8 [74.8, 74.8] | 35.4 % | 74.1 % |
| 8 | 93.6 [93.6, 93.6] | 76.2 [76.2, 76.2] | 98.2 [95.8, 100.0] | 3.0 [0.6, 5.5] | 0.2 [0.2, 0.2] | 92.4 [92.4, 92.4] | 99.8 [99.8, 99.8] | 0.2 [0.2, 0.2] | 75.3 [75.3, 75.3] | 35.4 % | 76.1 % |
| 12 | 93.6 [93.6, 93.6] | 76.2 [76.2, 76.2] | 98.2 [97.0, 99.4] | 1.8 [0.6, 3.0] | 0.2 [0.2, 0.2] | 95.0 [95.0, 95.0] | 99.8 [99.8, 99.8] | 0.2 [0.2, 0.2] | 75.6 [75.6, 75.6] | 35.4 % | 79.0 % |
| 16 | 93.6 [93.6, 93.6] | 76.2 [76.2, 76.2] | 99.4 [98.2, 100.0] | 2.4 [0.6, 4.2] | 0.2 [0.2, 0.2] | 96.2 [96.2, 96.2] | 99.8 [99.8, 99.8] | 0.2 [0.2, 0.2] | 75.8 [75.8, 75.8] | 35.4 % | 80.0 % |

## A2: solo contenido (Vc=V, Vd=1)

| V | contenido acepta | responde | hit estricto | otro dominio | falso contenido | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | densidad R | densidad dir |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 82.9 [82.9, 82.9] | 19.1 [19.1, 19.1] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 63.7 [63.7, 63.7] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 18.4 [18.4, 18.4] | 31.5 % | 66.9 % |
| 4 | 93.6 [93.6, 93.6] | 76.2 [76.2, 76.2] | 98.8 [97.6, 100.0] | 1.8 [0.0, 4.2] | 0.2 [0.2, 0.2] | 73.6 [73.6, 73.6] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 66.5 [66.5, 66.5] | 35.4 % | 69.1 % |
| 8 | 96.3 [96.3, 96.3] | 86.4 [86.4, 86.4] | 96.7 [95.6, 97.2] | 5.6 [3.9, 7.2] | 0.6 [0.6, 0.6] | 75.0 [75.0, 75.0] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 72.3 [72.3, 72.3] | 37.5 % | 69.2 % |
| 12 | 97.7 [97.7, 97.7] | 93.3 [93.3, 93.3] | 98.4 [96.3, 100.0] | 2.6 [0.5, 4.7] | 0.6 [0.6, 0.6] | 76.7 [76.7, 76.7] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 76.4 [76.4, 76.4] | 39.3 % | 69.8 % |
| 16 | 98.6 [98.6, 98.6] | 96.2 [96.2, 96.2] | 97.9 [97.4, 99.0] | 5.1 [3.6, 6.7] | 0.8 [0.8, 0.8] | 77.0 [77.0, 77.0] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 76.8 [76.8, 76.8] | 40.0 % | 70.0 % |

## A3: ambos (Vc=Vd=V)

| V | contenido acepta | responde | hit estricto | otro dominio | falso contenido | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | densidad R | densidad dir |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 82.9 [82.9, 82.9] | 19.1 [19.1, 19.1] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 63.7 [63.7, 63.7] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 18.4 [18.4, 18.4] | 31.5 % | 66.9 % |
| 4 | 93.6 [93.6, 93.6] | 76.2 [76.2, 76.2] | 98.8 [97.6, 100.0] | 1.2 [0.0, 2.4] | 0.2 [0.2, 0.2] | 87.7 [87.7, 87.7] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 74.8 [74.8, 74.8] | 35.4 % | 74.1 % |
| 8 | 96.3 [96.3, 96.3] | 86.4 [86.4, 86.4] | 98.3 [95.0, 100.0] | 3.9 [0.0, 9.4] | 0.6 [0.6, 0.6] | 93.0 [93.0, 93.0] | 99.7 [99.7, 99.7] | 0.3 [0.3, 0.3] | 85.4 [85.4, 85.4] | 37.5 % | 76.1 % |
| 12 | 97.7 [97.7, 97.7] | 93.3 [93.3, 93.3] | 97.4 [95.3, 99.5] | 5.3 [3.2, 7.4] | 0.6 [0.6, 0.6] | 95.6 [95.6, 95.6] | 99.6 [99.6, 99.7] | 0.4 [0.3, 0.4] | 91.7 [91.6, 91.8] | 39.3 % | 79.8 % |
| 16 | 98.6 [98.6, 98.6] | 96.2 [96.2, 96.2] | 100.0 [100.0, 100.0] | 2.1 [0.0, 5.1] | 0.8 [0.8, 0.8] | 97.1 [97.1, 97.1] | 99.8 [99.7, 99.8] | 0.2 [0.2, 0.2] | 94.5 [94.4, 94.5] | 40.0 % | 80.7 % |

## N328: 328 imágenes reales, Vc=4, Vd=1

| V | contenido acepta | responde | hit estricto | otro dominio | falso contenido | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | densidad R | densidad dir |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 95.4 [95.4, 95.4] | 87.3 [87.3, 87.3] | 95.7 [93.5, 97.8] | 5.9 [4.3, 7.6] | 0.2 [0.2, 0.2] | 77.4 [77.4, 77.4] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 75.6 [75.6, 75.6] | 36.3 % | 70.6 % |

## Sondas sintéticas

Especialistas que aceptan (de 8, media por semilla) y fracción de semillas en que el directorio rutea.

| combinación | ruido | color sólido | píxeles barajados |
|---|---|---|---|
| Vc1|N200|Vd1 | 0.0 / 0 % | 0.0 / 0 % | 0.0 / 0 % |
| Vc4|N200|Vd1 | 0.0 / 0 % | 1.0 / 0 % | 0.0 / 0 % |
| Vc4|N200|Vd4 | 0.0 / 0 % | 1.0 / 0 % | 0.0 / 0 % |
| Vc4|N200|Vd8 | 0.0 / 0 % | 1.0 / 0 % | 0.0 / 0 % |
| Vc4|N200|Vd12 | 0.0 / 0 % | 1.0 / 0 % | 0.0 / 0 % |
| Vc4|N200|Vd16 | 0.0 / 0 % | 1.0 / 100 % | 0.0 / 0 % |
| Vc4|N328|Vd1 | 0.0 / 0 % | 2.0 / 0 % | 0.0 / 0 % |
| Vc8|N200|Vd1 | 0.0 / 0 % | 2.0 / 0 % | 0.0 / 0 % |
| Vc8|N200|Vd8 | 0.0 / 0 % | 2.0 / 100 % | 0.0 / 0 % |
| Vc12|N200|Vd1 | 0.0 / 0 % | 3.0 / 0 % | 0.0 / 0 % |
| Vc12|N200|Vd12 | 0.0 / 0 % | 3.0 / 100 % | 0.0 / 0 % |
| Vc16|N200|Vd1 | 0.0 / 0 % | 3.0 / 0 % | 0.0 / 0 % |
| Vc16|N200|Vd16 | 0.0 / 0 % | 3.0 / 100 % | 0.0 / 0 % |

## Formación de directorios (fase A, media por semilla)

| combinación | registradas | rechazadas | acierto temprano |
|---|---|---|---|
| Vc1|N200|Vd1 | 876 | 148 | 100.0 |
| Vc4|N200|Vd1 | 981 | 43 | 100.0 |
| Vc4|N200|Vd4 | 981 | 43 | 100.0 |
| Vc4|N200|Vd8 | 981 | 43 | 100.0 |
| Vc4|N200|Vd12 | 981 | 43 | 100.0 |
| Vc4|N200|Vd16 | 981 | 43 | 100.0 |
| Vc4|N328|Vd1 | 1024 | 0 | 100.0 |
| Vc8|N200|Vd1 | 995 | 29 | 99.9 |
| Vc8|N200|Vd8 | 995 | 29 | 99.9 |
| Vc12|N200|Vd1 | 1013 | 11 | 99.9 |
| Vc12|N200|Vd12 | 1013 | 11 | 99.9 |
| Vc16|N200|Vd1 | 1016 | 8 | 99.9 |
| Vc16|N200|Vd16 | 1016 | 8 | 99.9 |

## Archivos
- `raw/Vc<Vc>_N<N>_Vd<Vd>_s<semilla>.json`: filas por imagen de test, sondas y formación
- `resumen.json`, `fig1_cobertura_vs_V.png`, `fig2_falsos_vs_V.png`
- `latentes_llenado.json`, `latentes_test.json`, `latentes_sondas.json`: latentes continuos del encoder
