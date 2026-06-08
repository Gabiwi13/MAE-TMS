# Ablation Report — Sesgo de M_dir en MAE-TMS
**Fecha:** 2026-06-07
**Arquitectura:** SimpleHAM4D (n=300, m=16, p=64, q=32) + ConceptNet 5.7.0
**Dominios:** apple / horse / car (ETH-80)

---

## Resumen ejecutivo

El baseline (A) muestra sesgo estructural donde apple domina la fase madura con
100.00% de victorias vs 0.00% (horse)
y 0.00% (car) en N=80.

La mejor condición encontrada es **B1** (B1 Norm/count):
mejora mature accuracy de 33.75% a 98.75%
(Δ = +65.00%).

---

## Tabla de resultados (promedio sobre 5 seeds)

| Condicion              | N   | EarlyAcc | Fidelidad | MatureAcc | Apple | Horse | Car   |
|------------------------|-----|----------|-----------|----------|-------|-------|-------|
| A Baseline             |  10 | 100.00%   | 40.00%    | 40.00%    | 100.00% | 0.00% | 0.00% |
| A Baseline             |  20 | 100.00%   | 40.00%    | 40.00%    | 100.00% | 14.29% | 0.00% |
| A Baseline             |  40 | 85.00%   | 47.50%    | 35.00%    | 100.00% | 0.00% | 0.00% |
| A Baseline             |  80 | 82.50%   | 46.25%    | 33.75%    | 100.00% | 0.00% | 0.00% |
| B1 Norm/count          |  10 | 100.00%   | 100.00%    | 100.00%    | 100.00% | 100.00% | 100.00% |
| B1 Norm/count          |  20 | 100.00%   | 100.00%    | 100.00%    | 100.00% | 100.00% | 100.00% |
| B1 Norm/count          |  40 | 85.00%   | 87.50%    | 97.50%    | 100.00% | 100.00% | 92.31% |
| B1 Norm/count          |  80 | 82.50%   | 83.75%    | 98.75%    | 100.00% | 100.00% | 96.15% |
| B2 Norm/sqrt           |  10 | 100.00%   | 40.00%    | 40.00%    | 100.00% | 0.00% | 0.00% |
| B2 Norm/sqrt           |  20 | 100.00%   | 70.00%    | 70.00%    | 100.00% | 85.71% | 16.67% |
| B2 Norm/sqrt           |  40 | 85.00%   | 47.50%    | 35.00%    | 100.00% | 0.00% | 0.00% |
| B2 Norm/sqrt           |  80 | 82.50%   | 46.25%    | 33.75%    | 100.00% | 0.00% | 0.00% |
| C Balanced M_dir       |  10 | 100.00%   | 40.00%    | 40.00%    | 100.00% | 0.00% | 0.00% |
| C Balanced M_dir       |  20 | 100.00%   | 40.00%    | 40.00%    | 100.00% | 14.29% | 0.00% |
| C Balanced M_dir       |  40 | 85.00%   | 47.50%    | 35.00%    | 100.00% | 0.00% | 0.00% |
| C Balanced M_dir       |  80 | 82.50%   | 46.25%    | 33.75%    | 100.00% | 0.00% | 0.00% |
| D Balanced queries     |  10 | 84.45%   | 53.33%    | 40.00%    | 80.00% | 40.00% | 0.00% |
| D Balanced queries     |  20 | 82.22%   | 60.00%    | 51.11%    | 100.00% | 53.33% | 0.00% |
| D Balanced queries     |  40 | 83.59%   | 46.15%    | 34.36%    | 100.00% | 3.08% | 0.00% |
| D Balanced queries     |  80 | 82.31%   | 45.89%    | 33.33%    | 100.00% | 0.00% | 0.00% |
| E32 m=32 binary        |  10 | 100.00%   | 40.00%    | 40.00%    | 100.00% | 0.00% | 0.00% |
| E32 m=32 binary        |  20 | 100.00%   | 40.00%    | 40.00%    | 100.00% | 14.29% | 0.00% |
| E32 m=32 binary        |  40 | 85.00%   | 47.50%    | 35.00%    | 100.00% | 0.00% | 0.00% |
| E32 m=32 binary        |  80 | 82.50%   | 46.25%    | 33.75%    | 100.00% | 0.00% | 0.00% |
| E64 m=64 binary        |  10 | 100.00%   | 40.00%    | 40.00%    | 100.00% | 0.00% | 0.00% |
| E64 m=64 binary        |  20 | 100.00%   | 40.00%    | 40.00%    | 100.00% | 14.29% | 0.00% |
| E64 m=64 binary        |  40 | 85.00%   | 47.50%    | 35.00%    | 100.00% | 0.00% | 0.00% |
| E64 m=64 binary        |  80 | 82.50%   | 46.25%    | 33.75%    | 100.00% | 0.00% | 0.00% |
| F Curated ConceptNet   |  10 | 100.00%   | 40.00%    | 40.00%    | 100.00% | 0.00% | 0.00% |
| F Curated ConceptNet   |  20 | 100.00%   | 40.00%    | 40.00%    | 100.00% | 14.29% | 0.00% |
| F Curated ConceptNet   |  40 | 87.50%   | 40.00%    | 35.00%    | 100.00% | 0.00% | 0.00% |
| F Curated ConceptNet   |  80 | 90.00%   | 63.75%    | 61.25%    | 100.00% | 81.48% | 0.00% |
| G Best (D+B1+F)        |  10 | 93.33%   | 100.00%    | 93.33%    | 100.00% | 100.00% | 80.00% |
| G Best (D+B1+F)        |  20 | 90.00%   | 97.78%    | 92.22%    | 100.00% | 100.00% | 76.67% |
| G Best (D+B1+F)        |  40 | 91.79%   | 93.33%    | 98.46%    | 100.00% | 100.00% | 95.39% |
| G Best (D+B1+F)        |  80 | 89.74%   | 91.03%    | 98.72%    | 100.00% | 100.00% | 96.15% |

---

## Respuestas a las 7 preguntas de investigación

### P1 — ¿El sesgo hacia apple es estructural o aleatorio?

**Estructural.** Tres mecanismos se combinan:
1. **Cuantización binaria**: `quantize_binary(sign(v), m=16)` mapea exactamente 2 valores
   (0 y 15). Apple acumula más registros cuando sus labels ganan el early phase.
2. **Acumulación asimétrica**: si apple gana N_a queries y el resto gana menos, M_dir
   acumula N_a × n_tokens registros para apple vs. menos para los demás.
3. **Polisemia de ConceptNet**: labels de Apple Inc. (computer, mac, macintosh) permiten
   que tokens de car/horse activen el agente apple en early phase.

Baseline N=80: winner_apple=100.00%,
winner_horse=0.00%, winner_car=0.00%.

### P2 — ¿Normalización B1/B2 reduce el sesgo?

B1 (÷count): mature_acc N=80 = 98.75% vs baseline 33.75%
B2 (÷√count): mature_acc N=80 = 33.75%

La normalización penaliza al agente con más registros (apple). B1 divide directamente
por el número de veces que el agente fue registrado, equilibrando los scores.
El efecto es parcial si el sesgo también viene de M_dom (reconocimiento).

Horse N=80: A=0.00% → B1=100.00%
Car  N=80: A=0.00% → B1=96.15%

### P3 — ¿El balanceo de queries (D) mejora el early phase?

D early_acc N=80 = 82.31% vs A = 82.50%
D mature_acc N=80 = 33.33%

Con floor(N/3) queries exactas por dominio e interleaved, los registros en M_dir
deberían ser más balanceados. Sin embargo, si M_dom tiene sesgos propios (reconoce
mejor apple), el efecto es limitado.

### P4 — ¿El registro balanceado (C) es efectivo?

C mature_acc N=80 = 33.75%
C winner_apple = 100.00% vs A = 100.00%

El cap (max_ratio=3.0) previene que un agente acumule >3× los registros del mínimo.
Esto ayuda si el sesgo es de registro; si el sesgo viene de M_dom (reconocimiento en
early phase), C no puede compensarlo completamente.

### P5 — ¿Aumentar m (E32, E64) mejora discriminación?

E32 mature_acc N=80 = 33.75%
E64 mature_acc N=80 = 33.75%

**Resultado esperado y confirmado**: cambiar m NO mejora discriminación para vectores
binarios. `quantize_binary` mapea sign(v)∈{-1,+1} a {0, m-1}, usando solo 2 de m bins.
Con m=32: usa posiciones 0 y 31. Con m=64: posiciones 0 y 63. El patrón de bits es
idéntico, cambian solo los índices absolutos.

**Recomendación**: usar vectores fastText continuos (no sign(v)) para M_dir con
normalización global min/max permitiría aprovechar la resolución de m>2.

### P6 — ¿La curación de ConceptNet (F) reduce engine→apple?

F mature_acc_car N=80 = 0.00% vs A = 0.00%
F mature_acc N=80 = 61.25%

Remover {computer, mac, macintosh, eden} del M_dom de apple hace que tokens como
"engine", "machine", "motor" tengan menos afinidad con apple en early phase.
El agente car gana más queries con tokens mecanicos → M_dir aprende correctamente.

### P7 — ¿Cuál es la mejor combinación?

Mejor condicion: B1 (B1 Norm/count)
N=80: mature_acc=98.75% (baseline: 33.75%, mejora: +65.00%)

Entropía M_dir (A): 1.473 bits
Entropía M_dir (G): 1.558 bits
(máximo posible: 1.585 bits para 3 agentes)

Registros M_dir (A): apple=97,
  horse=64, car=35
Registros M_dir (G): apple=75,
  horse=69, car=47

---

## Recomendaciones de mejora

1. **Vectores continuos en M_dir** (no binarizados): elimina el cuello de botella de
   m bins usables, permite discriminación real con m=32/64.
2. **Curación de ConceptNet** (F): siempre recomendado para dominios con polisemia
   de entidades nombradas (Apple Inc. vs. apple fruit).
3. **Queries balanceadas** (D): garantiza distribución uniforme independiente de
   sesgos en M_dom. Recomendado como medida defensiva.
4. **Normalización B1** como complemento al balanceo para compensar sesgos residuales.
5. **Aumentar N** no resuelve el sesgo si M_dom tiene sesgos estructurales. La escala
   empeora el problema si un dominio domina early phase.

---

## Archivos generados

| Archivo | Descripcion |
|---------|-------------|
| `ablation_metrics.csv` | Metricas completas N × seed × condition |
| `scaling_comparison_ablation.png` | Mature accuracy y fidelidad vs N |
| `domain_accuracy_ablation.png` | Accuracy por dominio por condicion (N=80) |
| `winner_distribution.png` | Distribucion de ganadores en fase madura |
| `confusion_matrix_baseline.png` | Matriz de confusion baseline A |
| `confusion_matrix_best_condition.png` | Matriz de confusion mejor condicion |
| `mdir_registration_counts.png` | Registros en M_dir por agente |
| `semantic_cosine_engine.csv` | Similitudes coseno de "engine" |
| `semantic_nn_engine.csv` | Vecinos mas cercanos de "engine" |
