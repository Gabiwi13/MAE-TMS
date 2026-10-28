# Experimento 15 — árbitro por contenido y abstención por margen

Políticas sobre la misma salida de `route_transactive`: argmax (oficial); árbitro (entre los 3 mejores del directorio decide el contenido); margen (abstención si (s1 − s2)/s1 < δ, δ = 0.2 pre-registrado); ambas; contenido (los ocho por contenido, diagnóstico). Intervalos: bootstrap del 95 % sobre semillas. Diseño en `propuesta_exp15_arbitro_margen.md`.

## Texto (N = 200, 10 semillas)

171 reservadas: acierto / error / rechazo (% de las consultas). Fuera de dominio (40): aceptadas.

| política | acierto | error | rechazo | OOD aceptadas |
|---|---|---|---|---|
| argmax | 96.8 [96.3, 97.4] | 3.2 [2.6, 3.7] | 0.0 [0.0, 0.0] | 10.0 [10.0, 10.0] |
| arbitro | 93.6 [93.6, 93.6] | 5.8 [5.8, 5.8] | 0.6 [0.6, 0.6] | 5.0 [5.0, 5.0] |
| margen | 91.9 [90.5, 93.5] | 1.5 [1.2, 1.8] | 6.6 [5.1, 8.0] | 10.0 [10.0, 10.0] |
| ambas | 88.9 [87.5, 90.3] | 3.9 [3.4, 4.3] | 7.2 [5.7, 8.6] | 5.0 [5.0, 5.0] |
| contenido | 93.6 [93.6, 93.6] | 6.4 [6.4, 6.4] | 0.0 [0.0, 0.0] | 5.0 [5.0, 5.0] |

Transiciones respecto del argmax (media de consultas por semilla, reservadas):

| política | acierto→error | acierto→rechazo | error→acierto | error→rechazo | rechazo→acierto |
|---|---|---|---|---|---|
| arbitro | 8.0 | 0.0 | 2.4 | 1.0 | 0.0 |
| ambas | 5.7 | 8.4 | 0.6 | 3.9 | 0.0 |
| contenido | 9.0 | 0.0 | 3.4 | 0.0 | 0.0 |

Curva de δ (reservadas): margen solo / ambas.

| δ | acierto | error | rechazo | acierto (ambas) | error (ambas) | rechazo (ambas) |
|---|---|---|---|---|---|---|
| 0.00 | 96.8 | 3.2 | 0.0 | 93.6 | 5.8 | 0.6 |
| 0.05 | 95.6 | 2.2 | 2.2 | 91.8 | 5.4 | 2.8 |
| 0.10 | 94.3 | 1.9 | 3.8 | 90.5 | 5.1 | 4.4 |
| 0.15 | 93.2 | 1.6 | 5.1 | 89.8 | 4.5 | 5.7 |
| 0.20 | 91.9 | 1.5 | 6.6 | 88.9 | 3.9 | 7.2 |
| 0.25 | 89.9 | 1.3 | 8.8 | 87.9 | 2.7 | 9.4 |
| 0.30 | 88.0 | 1.2 | 10.8 | 86.5 | 2.0 | 11.4 |
| 0.35 | 84.9 | 0.8 | 14.3 | 84.0 | 1.2 | 14.9 |
| 0.40 | 80.2 | 0.8 | 19.0 | 80.1 | 0.3 | 19.6 |
| 0.45 | 78.2 | 0.7 | 21.1 | 78.3 | 0.1 | 21.6 |
| 0.50 | 75.9 | 0.6 | 23.5 | 76.0 | 0.0 | 24.0 |

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
| margen | 95.4 [95.4, 95.4] | 0.2 [0.2, 0.2] | 4.4 [4.4, 4.4] | 75.8 [75.8, 75.8] |
| ambas | 91.3 [91.3, 91.3] | 0.0 [0.0, 0.0] | 8.7 [8.7, 8.7] | 75.8 [75.8, 75.8] |
| contenido | 93.1 [93.1, 93.1] | 0.0 [0.0, 0.0] | 6.9 [6.9, 6.9] | 76.2 [76.2, 76.2] |

Transiciones respecto del argmax (media por semilla):

| política | acierto→error | acierto→rechazo | error→acierto | error→rechazo | rechazo→acierto |
|---|---|---|---|---|---|
| arbitro | 0.0 | 27.0 | 0.0 | 1.0 | 0.0 |
| ambas | 0.0 | 27.0 | 0.0 | 1.0 | 0.0 |
| contenido | 0.0 | 27.0 | 0.0 | 1.0 | 12.0 |

## El caso `horse7-000-000`

| directorios | semilla | argmax | directorio (>0) | contenido (>0) | árbitro | ambas |
|---|---|---|---|---|---|---|
| Vd1 | s42 | None | {} | {} | None | None |
| Vd1 | s43 | None | {} | {} | None | None |
| Vd1 | s44 | None | {} | {} | None | None |
| Vd1 | s45 | None | {} | {} | None | None |
| Vd1 | s46 | None | {} | {} | None | None |
| Vd16 | s42 | dog | {'dog': 41.2669} | {} | None | None |
| Vd16 | s43 | dog | {'dog': 50.0746} | {} | None | None |
| Vd16 | s44 | dog | {'dog': 69.0582} | {} | None | None |
| Vd16 | s45 | dog | {'dog': 29.4429} | {} | None | None |
| Vd16 | s46 | dog | {'dog': 51.1571} | {} | None | None |

## Archivos
- `raw/texto_s<semilla>.json`, `raw/imagen_Vd<Vd>_s<semilla>.json`: por consulta, vector del directorio y scores de contenido de los ocho agentes
- `resumen.json`, `fig1_curva_margen.png`
