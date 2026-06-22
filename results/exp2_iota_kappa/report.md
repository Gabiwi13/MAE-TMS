# Experimento 2 — iota y kappa como defensas contra el sesgo de densidad

## Hipótesis
Las defensas nativas del framework (ι: poda de la relación; κ: umbral
relativo a la media de cada memoria) eliminan el sesgo de masa que en el
experimento 1 obligó a introducir la normalización B1 / ÷mem.mean.

## Setup
- Grid: ι ∈ [0.0, 0.25, 0.5, 1.0] × κ ∈ [0.0, 0.5, 1.0, 1.5] (mutación en-memoria, setters originales)
- Banco: 80 queries del ablation con ground truth (27/27/26)
- Score: activación media de project() con pesos de M_dom_L,
  gateada por containment-ι y por κ·mem.mean (adaptación unilateral
  del criterio original de recognize()).

## Resultados clave
- Baseline ι=0 κ=0 (exp. 1): early 97.5%, diag 100.0%
- Referencia ÷mem.mean (ι=0 κ=0): early 97.5%
- Mejor condición nativa: ι=0.0 κ=0.0 → early 97.5% (rechazo 1.2%), diag 100.0%

## Tabla del grid (brazo GATED, sin normalizar)

| ι \ κ | 0.0 | 0.5 | 1.0 | 1.5 |
|---|---|---|---|---|
| **0.0** | 98% (rej 1%) | 98% (rej 1%) | 98% (rej 1%) | 98% (rej 1%) |
| **0.25** | 78% (rej 21%) | 78% (rej 21%) | 78% (rej 21%) | 78% (rej 21%) |
| **0.5** | 54% (rej 45%) | 54% (rej 45%) | 54% (rej 45%) | 54% (rej 45%) |
| **1.0** | 0% (rej 100%) | 0% (rej 100%) | 0% (rej 100%) | 0% (rej 100%) |

## Downstream (¿sigue haciendo falta B1?)

| condición | early | mature RAW | mature B1 | counts M_dir |
|---|---|---|---|---|
| baseline ι=0 κ=0 (exp. 1) | 97.5% | 85.0% | 98.8% | [71, 58, 46] |
| mejor nativa ι=0.0 κ=0.0 | 97.5% | 85.0% | 98.8% | [71, 58, 46] |
| ÷mem.mean con ι=0 κ=0 | 97.5% | 85.0% | 98.8% | [71, 58, 46] |

## Archivos
- results_grid.csv · results_downstream.csv
- heatmap_early_acc_gated.png · heatmap_early_rejection.png
- heatmap_early_acc_norm.png · heatmap_diag_gated.png