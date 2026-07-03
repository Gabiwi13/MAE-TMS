# Experimento 6 — curva de capacidad del llenado por instancias

| N | train propio | test propio | falsos (otras clases) | variedad L1 | routing | entropía |
|---|---|---|---|---|---|---|
| 25 | 100% | 0% | 0% | 1.61 | 62.5% | 3.681 |
| 50 | 100% | 0% | 0% | 1.82 | 71.2% | 4.464 |
| 100 | 100% | 3% | 0% | 2.00 | 78.8% | 4.930 |
| 200 | 100% | 21% | 0% | 2.12 | 78.8% | 5.170 |
| 328 | 100% | 52% | 0% | 2.19 | 77.5% | 5.279 |

Protocolo image-major: registros por clase = N (masas igualadas).
Aceptación = containment inverso unilateral con ξ=0.

## Archivos
- results_capacity.csv · fig1_capacity_curve.png
- fig2_variety_routing_entropy.png · fig3_apple_strips.png