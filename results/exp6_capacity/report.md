# Experimento 6 — curva de capacidad del llenado por instancias

| N | train propio | test propio | falsos (otras clases) | variedad L1 | routing | entropía |
|---|---|---|---|---|---|---|
| 25 | 100% | 0% | 0% | 1.91 | 61.3% | 3.648 |
| 50 | 100% | 0% | 0% | 1.87 | 71.2% | 4.369 |
| 100 | 100% | 2% | 0% | 1.74 | 78.8% | 4.950 |
| 200 | 100% | 20% | 0% | 1.94 | 81.2% | 5.204 |
| 328 | 100% | 56% | 0% | 2.18 | 81.2% | 5.318 |

Protocolo image-major: registros por clase = N (masas igualadas).
Aceptación = containment inverso unilateral con ξ=0.

## Archivos
- results_capacity.csv · fig1_capacity_curve.png
- fig2_variety_routing_entropy.png · fig3_apple_strips.png