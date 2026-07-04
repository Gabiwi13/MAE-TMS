# Experimento 6 — curva de capacidad del llenado por instancias

| N | train propio | test propio | falsos (otras clases) | variedad L1 | routing | entropía |
|---|---|---|---|---|---|---|
| 25 | 100% | 0% | 0% | 1.89 | 58.8% | 3.649 |
| 50 | 100% | 0% | 0% | 1.88 | 65.0% | 4.388 |
| 100 | 100% | 0% | 0% | 1.82 | 67.5% | 4.992 |
| 200 | 100% | 9% | 0% | 1.99 | 70.0% | 5.248 |
| 328 | 100% | 47% | 0% | 2.30 | 71.2% | 5.360 |

Protocolo image-major: registros por clase = N (masas igualadas).
Aceptación = containment inverso unilateral con ξ=0.

## Archivos
- results_capacity.csv · fig1_capacity_curve.png
- fig2_variety_routing_entropy.png · fig3_apple_strips.png