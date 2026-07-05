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
- Baseline ι=0 κ=0 (exp. 1): early 76.2%, diag 90.9%
- Referencia ÷mem.mean (ι=0 κ=0): early 76.2%
- Mejor condición nativa: ι=0.0 κ=0.0 → early 76.2% (rechazo 5.0%), diag 90.9%

## Tabla del grid (brazo GATED, sin normalizar)

| ι \ κ | 0.0 | 0.5 | 1.0 | 1.5 |
|---|---|---|---|---|
| **0.0** | 76% (rej 5%) | 76% (rej 5%) | 76% (rej 5%) | 76% (rej 5%) |
| **0.25** | 76% (rej 5%) | 76% (rej 5%) | 76% (rej 5%) | 76% (rej 5%) |
| **0.5** | 69% (rej 11%) | 69% (rej 11%) | 69% (rej 11%) | 69% (rej 11%) |
| **1.0** | 6% (rej 76%) | 6% (rej 76%) | 6% (rej 76%) | 6% (rej 76%) |

## Downstream (¿sigue haciendo falta B1?)

| condición | early | mature RAW | mature B1 | counts M_dir |
|---|---|---|---|---|
| baseline ι=0 κ=0 (exp. 1) | 76.2% | 66.2% | 77.5% | [72, 16, 37, 25, 30, 21, 3, 23] |
| mejor nativa ι=0.0 κ=0.0 | 76.2% | 66.2% | 77.5% | [72, 16, 37, 25, 30, 21, 3, 23] |
| ÷mem.mean con ι=0 κ=0 | 76.2% | 63.7% | 77.5% | [72, 16, 40, 25, 34, 14, 3, 23] |

## Archivos
- results_grid.csv · results_downstream.csv
- heatmap_early_acc_gated.png · heatmap_early_rejection.png
- heatmap_early_acc_norm.png · heatmap_diag_gated.png