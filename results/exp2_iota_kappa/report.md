# Experimento 2 — iota y kappa como defensas contra el sesgo de densidad

## Hipótesis
Las defensas nativas del framework (ι: poda de la relación; κ: umbral
relativo a la media de cada memoria) eliminan el sesgo de masa que en el
experimento 1 obligó a introducir la normalización B1 / ÷mem.mean.

## Setup
- Grid: ι ∈ [0.0, 0.25, 0.5, 1.0] × κ ∈ [0.0, 1.755, 1.801, 1.844, 1.937, 2.056, 2.107] (mutación en-memoria, setters originales). κ no se elige a mano: es 0 más los cuantiles 10%, 25%, 50%, 75%, 90%, 100% de la razón que compara la compuerta (activación por celda / mem.mean), medida con ι=0 sobre los 260 pares token-agente contenidos del banco (mín 1.523, mediana 1.844, máx 2.107). Con el cuantil q, κ deja pasar como mucho la fracción 1−q de esos pares.
- Banco: primeras 80 queries del banco de 8 clases con ground truth (10 por clase)
- **Dentro de muestra:** el downstream llena M_dir con los tokens de esas 80 queries y evalúa la fase madura sobre las mismas. Mide si el directorio reproduce lo que registró, no si generaliza.
- Score: activación media de project() con pesos de M_dom_L,
  gateada por containment-ι y por κ·mem.mean (adaptación unilateral
  del criterio original de recognize()).

## Resultados clave
- Baseline ι=0 κ=0 (la condición que usó exp. 1; número FRESCO de 8 clases, no la cifra histórica): early 81.2%, diag 81.8%
- Referencia ÷mem.mean (ι=0 κ=0): early 76.2%
- Mejor condición nativa: ι=0.25 κ=0.0 → early 82.5% (rechazo 5.0%), diag 81.8%
- κ con ι=0: la mejor columna con κ>0 da early 77.5% contra 81.2% sin κ; el rechazo va de 6.2% a 100.0%.

## Tabla del grid (brazo GATED, sin normalizar)

| ι \ κ | 0.0 | 1.755 | 1.801 | 1.844 | 1.937 | 2.056 | 2.107 |
|---|---|---|---|---|---|---|---|
| **0.0** | 81% (rej 5%) | 78% (rej 6%) | 65% (rej 10%) | 57% (rej 19%) | 35% (rej 45%) | 19% (rej 64%) | 0% (rej 100%) |
| **0.25** | 82% (rej 5%) | 82% (rej 5%) | 82% (rej 5%) | 82% (rej 5%) | 82% (rej 5%) | 82% (rej 5%) | 82% (rej 5%) |
| **0.5** | 75% (rej 11%) | 75% (rej 11%) | 75% (rej 11%) | 75% (rej 11%) | 75% (rej 11%) | 75% (rej 11%) | 75% (rej 11%) |
| **1.0** | 9% (rej 86%) | 9% (rej 86%) | 9% (rej 86%) | 9% (rej 86%) | 9% (rej 86%) | 9% (rej 86%) | 9% (rej 86%) |

### ¿Qué compara κ en cada ι?

La razón (activación por celda / mem.mean) de los pares token-agente contenidos. La rejilla de κ sale de la fila ι=0. Con poda, la activación se concentra en las celdas que sobreviven y mem.mean no cambia, así que la razón sube; si su mínimo supera el κ máximo (2.107), κ no rechaza nada en esa fila.

| ι | pares | mín | mediana | máx | ¿κ máx rechaza algo? |
|---|---|---|---|---|---|
| 0.0 | 260 | 1.523 | 1.844 | 2.107 | sí |
| 0.25 | 252 | 2.330 | 2.894 | 3.399 | no |
| 0.5 | 222 | 2.785 | 3.465 | 3.923 | no |
| 1.0 | 11 | 3.960 | 4.410 | 4.410 | no |

## Downstream (¿sigue haciendo falta B1?)

| condición | early | mature RAW | mature B1 | counts M_dir |
|---|---|---|---|---|
| baseline ι=0 κ=0 (exp. 1) | 81.2% | 72.5% | 81.2% | [46, 16, 40, 25, 30, 18, 21, 31] |
| mejor nativa ι=0.25 κ=0.0 | 82.5% | 80.0% | 83.8% | [38, 16, 40, 25, 30, 18, 29, 31] |
| ÷mem.mean con ι=0 κ=0 | 76.2% | 63.7% | 77.5% | [74, 16, 40, 25, 34, 14, 3, 21] |

## Archivos
- results_grid.csv · results_downstream.csv
- heatmap_early_acc_gated.png · heatmap_early_rejection.png
- heatmap_early_acc_norm.png · heatmap_diag_gated.png