# Experimento 6 — curva de capacidad del llenado por instancias

| N | train propio | test propio | falsos (otras clases) | variedad L1 | routing | entropía |
|---|---|---|---|---|---|---|
| 25 | 100% | 0% | 0% | 0.00 | 60.0% | 3.306 |
| 50 | 100% | 0% | 0% | 2.25 | 93.8% | 3.722 |
| 100 | 100% | 12% | 0% | 2.53 | 98.8% | 3.931 |
| 200 | 100% | 57% | 0% | 2.75 | 97.5% | 4.002 |
| 328 | 100% | 78% | 0% | 3.09 | 85.0% | 4.039 |

Protocolo image-major: registros por clase = N (masas igualadas).
Aceptación = containment inverso unilateral con ξ=0.

## Archivos
- results_capacity.csv · fig1_capacity_curve.png
- fig2_variety_routing_entropy.png · fig3_apple_strips.png