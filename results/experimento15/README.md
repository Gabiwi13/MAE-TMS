# Experimento 15 — árbitro por contenido y abstención por margen

Políticas sobre la misma salida de `route_transactive`: argmax (oficial); árbitro (entre los 3 mejores del directorio decide el contenido); margen (abstención si (s1 − s2)/s1 < δ, δ = 0.2 pre-registrado); ambas; contenido (los ocho por contenido, diagnóstico). Intervalos: bootstrap del 95 % sobre semillas. Diseño en `propuesta_exp15_arbitro_margen.md`.

## Texto (N = 200, 10 semillas)

171 reservadas: acierto / error / rechazo (% de las consultas). Fuera de dominio (40): aceptadas.

| política | acierto | error | rechazo | OOD aceptadas |
|---|---|---|---|---|
| argmax | 96.1 [95.7, 96.6] | 3.9 [3.4, 4.3] | 0.0 [0.0, 0.0] | 10.0 [10.0, 10.0] |
| arbitro | 90.6 [90.6, 90.6] | 8.8 [8.8, 8.8] | 0.6 [0.6, 0.6] | 5.0 [5.0, 5.0] |
| margen | 91.8 [90.6, 92.7] | 1.9 [1.5, 2.3] | 6.4 [5.4, 7.6] | 10.0 [10.0, 10.0] |
| ambas | 88.4 [87.4, 89.3] | 5.0 [4.5, 5.6] | 6.5 [5.6, 7.7] | 5.0 [5.0, 5.0] |
| contenido | 90.6 [90.6, 90.6] | 9.4 [9.4, 9.4] | 0.0 [0.0, 0.0] | 5.0 [5.0, 5.0] |

Transiciones respecto del argmax (media de consultas por semilla, reservadas):

| política | acierto→error | acierto→rechazo | error→acierto | error→rechazo | rechazo→acierto |
|---|---|---|---|---|---|
| arbitro | 11.4 | 0.0 | 2.0 | 1.0 | 0.0 |
| ambas | 6.7 | 7.5 | 1.0 | 3.7 | 0.0 |
| contenido | 12.4 | 0.0 | 3.0 | 0.0 | 0.0 |

Curva de δ (reservadas): margen solo / ambas.

| δ | acierto | error | rechazo | acierto (ambas) | error (ambas) | rechazo (ambas) |
|---|---|---|---|---|---|---|
| 0.00 | 96.1 | 3.9 | 0.0 | 90.6 | 8.8 | 0.6 |
| 0.05 | 95.6 | 3.3 | 1.2 | 90.3 | 8.0 | 1.7 |
| 0.10 | 94.3 | 2.9 | 2.8 | 89.8 | 7.0 | 3.2 |
| 0.15 | 92.9 | 2.2 | 4.9 | 88.9 | 5.8 | 5.3 |
| 0.20 | 91.8 | 1.9 | 6.4 | 88.4 | 5.0 | 6.5 |
| 0.25 | 89.7 | 1.5 | 8.8 | 86.8 | 4.2 | 8.9 |
| 0.30 | 88.3 | 1.3 | 10.4 | 86.0 | 3.5 | 10.5 |
| 0.35 | 85.6 | 1.1 | 13.3 | 84.4 | 2.1 | 13.5 |
| 0.40 | 82.9 | 0.7 | 16.4 | 82.8 | 0.6 | 16.6 |
| 0.45 | 79.3 | 0.5 | 20.2 | 79.4 | 0.3 | 20.4 |
| 0.50 | 76.0 | 0.1 | 24.0 | 75.9 | 0.1 | 24.0 |

## Imagen (Vc = 4, Vd = 1, 5 semillas)

656 de test (4 rechazadas antes por energía): acierto / error / rechazo / punta a punta.

| política | acierto | error | rechazo | e2e |
|---|---|---|---|---|
| argmax | 73.6 [73.6, 73.6] | 0.0 [0.0, 0.0] | 26.4 [26.4, 26.4] | 66.5 [66.5, 66.5] |
| arbitro | 73.6 [73.6, 73.6] | 0.0 [0.0, 0.0] | 26.4 [26.4, 26.4] | 66.5 [66.5, 66.5] |
| margen | 73.6 [73.6, 73.6] | 0.0 [0.0, 0.0] | 26.4 [26.4, 26.4] | 66.5 [66.5, 66.5] |
| ambas | 73.6 [73.6, 73.6] | 0.0 [0.0, 0.0] | 26.4 [26.4, 26.4] | 66.5 [66.5, 66.5] |
| contenido | 93.1 [93.1, 93.1] | 0.0 [0.0, 0.0] | 6.9 [6.9, 6.9] | 76.2 [76.2, 76.2] |

Transiciones respecto del argmax (media por semilla):

| política | acierto→error | acierto→rechazo | error→acierto | error→rechazo | rechazo→acierto |
|---|---|---|---|---|---|
| arbitro | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| ambas | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| contenido | 0.0 | 0.0 | 0.0 | 0.0 | 128.0 |

## Imagen (Vc = 4, Vd = 16, 5 semillas)

656 de test (4 rechazadas antes por energía): acierto / error / rechazo / punta a punta.

| política | acierto | error | rechazo | e2e |
|---|---|---|---|---|
| argmax | 95.4 [95.4, 95.4] | 0.2 [0.2, 0.2] | 4.4 [4.4, 4.4] | 75.8 [75.8, 75.8] |
| arbitro | 91.3 [91.3, 91.3] | 0.0 [0.0, 0.0] | 8.7 [8.7, 8.7] | 75.8 [75.8, 75.8] |
| margen | 95.4 [95.3, 95.4] | 0.2 [0.2, 0.2] | 4.5 [4.4, 4.5] | 75.8 [75.8, 75.8] |
| ambas | 91.2 [91.2, 91.3] | 0.0 [0.0, 0.0] | 8.8 [8.7, 8.8] | 75.8 [75.8, 75.8] |
| contenido | 93.1 [93.1, 93.1] | 0.0 [0.0, 0.0] | 6.9 [6.9, 6.9] | 76.2 [76.2, 76.2] |

Transiciones respecto del argmax (media por semilla):

| política | acierto→error | acierto→rechazo | error→acierto | error→rechazo | rechazo→acierto |
|---|---|---|---|---|---|
| arbitro | 0.0 | 27.0 | 0.0 | 1.0 | 0.0 |
| ambas | 0.0 | 27.4 | 0.0 | 1.0 | 0.0 |
| contenido | 0.0 | 27.0 | 0.0 | 1.0 | 12.0 |

## El caso `horse7-000-000`

| directorios | semilla | argmax | directorio (>0) | contenido (>0) | árbitro | ambas |
|---|---|---|---|---|---|---|
| Vd1 | s42 | None | {} | {} | None | None |
| Vd1 | s43 | None | {} | {} | None | None |
| Vd1 | s44 | None | {} | {} | None | None |
| Vd1 | s45 | None | {} | {} | None | None |
| Vd1 | s46 | None | {} | {} | None | None |
| Vd16 | s42 | dog | {'dog': 37.0529} | {} | None | None |
| Vd16 | s43 | dog | {'dog': 46.067} | {} | None | None |
| Vd16 | s44 | dog | {'dog': 64.2552} | {} | None | None |
| Vd16 | s45 | dog | {'dog': 27.337} | {} | None | None |
| Vd16 | s46 | dog | {'dog': 47.05} | {} | None | None |

## Archivos
- `raw/texto_s<semilla>.json`, `raw/imagen_Vd<Vd>_s<semilla>.json`: por consulta, vector del directorio y scores de contenido de los ocho agentes
- `resumen.json`, `fig1_curva_margen.png`
