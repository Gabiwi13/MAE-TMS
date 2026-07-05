# Experimento 6 — curva de capacidad del llenado por instancias

| N | train propio | test propio | falsos (otras clases) | variedad L1 | routing | entropía |
|---|---|---|---|---|---|---|
| 25 | 100% | 0% | 0% | 1.85 | 65.0% | 3.649 |
| 50 | 100% | 0% | 0% | 1.90 | 70.0% | 4.388 |
| 100 | 100% | 0% | 0% | 1.82 | 73.8% | 4.992 |
| 200 | 100% | 9% | 0% | 2.00 | 75.0% | 5.248 |
| 328 | 100% | 47% | 0% | 2.24 | 76.2% | 5.360 |

Protocolo image-major: registros por clase = N (masas igualadas).
Aceptación = containment inverso unilateral con ξ=0.

## Archivos
- results_capacity.csv · fig1_capacity_curve.png
- fig2_variety_routing_entropy.png · fig3_apple_strips.png