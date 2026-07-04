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
- Baseline ι=0 κ=0 (exp. 1): early 71.2%, diag 90.9%
- Referencia ÷mem.mean (ι=0 κ=0): early 71.2%
- Mejor condición nativa: ι=0.0 κ=0.0 → early 71.2% (rechazo 8.8%), diag 90.9%

## Tabla del grid (brazo GATED, sin normalizar)

| ι \ κ | 0.0 | 0.5 | 1.0 | 1.5 |
|---|---|---|---|---|
| **0.0** | 71% (rej 9%) | 71% (rej 9%) | 71% (rej 9%) | 71% (rej 9%) |
| **0.25** | 71% (rej 9%) | 71% (rej 9%) | 71% (rej 9%) | 71% (rej 9%) |
| **0.5** | 64% (rej 15%) | 64% (rej 15%) | 64% (rej 15%) | 64% (rej 15%) |
| **1.0** | 6% (rej 76%) | 6% (rej 76%) | 6% (rej 76%) | 6% (rej 76%) |

## Downstream (¿sigue haciendo falta B1?)

| condición | early | mature RAW | mature B1 | counts M_dir |
|---|---|---|---|---|
| baseline ι=0 κ=0 (exp. 1) | 71.2% | 65.0% | 75.0% | [72, 14, 36, 21, 20, 21, 3, 23] |
| mejor nativa ι=0.0 κ=0.0 | 71.2% | 65.0% | 75.0% | [72, 14, 36, 21, 20, 21, 3, 23] |
| ÷mem.mean con ι=0 κ=0 | 71.2% | 58.8% | 75.0% | [72, 14, 41, 21, 24, 12, 3, 23] |

## Archivos
- results_grid.csv · results_downstream.csv
- heatmap_early_acc_gated.png · heatmap_early_rejection.png
- heatmap_early_acc_norm.png · heatmap_diag_gated.png