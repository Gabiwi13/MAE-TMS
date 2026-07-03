# Experimento 2 — iota y kappa como defensas contra el sesgo de densidad

## Hipótesis
Las defensas nativas del framework (ι: poda de la relación; κ: umbral
relativo a la media de cada memoria) eliminan el sesgo de masa que en el
experimento 1 obligó a introducir la normalización B1 / ÷mem.mean.

## Setup
- Grid: ι ∈ [0.0, 0.25, 0.5, 1.0] × κ ∈ [0.0, 0.5, 1.0, 1.5] (mutación en-memoria, setters originales)
- Banco: primeras 80 queries del banco de 8 clases con ground truth (10 por clase)
- Score: activación media de project() con pesos de M_dom_L,
  gateada por containment-ι y por κ·mem.mean (adaptación unilateral
  del criterio original de recognize()).

## Resultados clave
- Baseline ι=0 κ=0 (exp. 1): early 80.0%, diag 100.0%
- Referencia ÷mem.mean (ι=0 κ=0): early 78.8%
- Mejor condición nativa: ι=0.25 κ=0.0 → early 83.8% (rechazo 1.2%), diag 81.8%

## Tabla del grid (brazo GATED, sin normalizar)

| ι \ κ | 0.0 | 0.5 | 1.0 | 1.5 |
|---|---|---|---|---|
| **0.0** | 80% (rej 1%) | 80% (rej 1%) | 80% (rej 1%) | 80% (rej 1%) |
| **0.25** | 84% (rej 1%) | 84% (rej 1%) | 84% (rej 1%) | 84% (rej 1%) |
| **0.5** | 64% (rej 16%) | 64% (rej 16%) | 64% (rej 16%) | 64% (rej 16%) |
| **1.0** | 22% (rej 55%) | 22% (rej 55%) | 22% (rej 55%) | 22% (rej 55%) |

## Downstream (¿sigue haciendo falta B1?)

| condición | early | mature RAW | mature B1 | counts M_dir |
|---|---|---|---|---|
| baseline ι=0 κ=0 (exp. 1) | 80.0% | 68.8% | 82.5% | [64, 19, 25, 22, 27, 32, 13, 21] |
| mejor nativa ι=0.25 κ=0.0 | 83.8% | 76.2% | 82.5% | [46, 19, 25, 22, 28, 31, 31, 21] |
| ÷mem.mean con ι=0 κ=0 | 78.8% | 68.8% | 80.0% | [74, 19, 25, 22, 27, 32, 3, 21] |

## Archivos
- results_grid.csv · results_downstream.csv
- heatmap_early_acc_gated.png · heatmap_early_rejection.png
- heatmap_early_acc_norm.png · heatmap_diag_gated.png