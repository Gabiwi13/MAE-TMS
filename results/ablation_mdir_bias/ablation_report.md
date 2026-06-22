# Ablation Report — Sesgo de M_dir en EAM-TMS
**Fecha:** 2026-06-07
**Arquitectura:** HeteroAssociativeMemory (n=300, m=16, p=64, q=32) + ConceptNet 5.7.0
**Dominios:** apple / horse / car (ETH-80)

---

## Resumen ejecutivo

El baseline (A) muestra sesgo estructural donde apple domina la fase madura con
82.50% de victorias vs 15.00% (horse)
y 1.25% (car) en N=80.

La mejor condición encontrada es **G** (G Best (D+B1+F)):
mejora mature accuracy de 50.00% a 93.33%
(Δ = +43.33%).

---

## Tabla de resultados (promedio sobre 5 seeds)

| Condicion              | N   | EarlyAcc | Fidelidad | MatureAcc | Apple | Horse | Car   |
|------------------------|-----|----------|-----------|----------|-------|-------|-------|
| A Baseline             |  10 | 100.00%   | 100.00%    | 100.00%    | 100.00% | 100.00% | 100.00% |
| A Baseline             |  20 | 85.00%   | 85.00%    | 80.00%    | 100.00% | 100.00% | 33.33% |
| A Baseline             |  40 | 70.00%   | 60.00%    | 52.50%    | 100.00% | 53.85% | 0.00% |
| A Baseline             |  80 | 71.25%   | 56.25%    | 50.00%    | 100.00% | 44.44% | 3.85% |
| B1 Norm/count          |  10 | 100.00%   | 100.00%    | 100.00%    | 100.00% | 100.00% | 100.00% |
| B1 Norm/count          |  20 | 85.00%   | 100.00%    | 85.00%    | 85.71% | 100.00% | 66.67% |
| B1 Norm/count          |  40 | 70.00%   | 85.00%    | 85.00%    | 85.71% | 100.00% | 69.23% |
| B1 Norm/count          |  80 | 71.25%   | 78.75%    | 91.25%    | 92.59% | 100.00% | 80.77% |
| B2 Norm/sqrt           |  10 | 100.00%   | 100.00%    | 100.00%    | 100.00% | 100.00% | 100.00% |
| B2 Norm/sqrt           |  20 | 85.00%   | 90.00%    | 75.00%    | 85.71% | 100.00% | 33.33% |
| B2 Norm/sqrt           |  40 | 70.00%   | 67.50%    | 55.00%    | 92.86% | 61.54% | 7.69% |
| B2 Norm/sqrt           |  80 | 71.25%   | 62.50%    | 53.75%    | 92.59% | 59.26% | 7.69% |
| C Balanced M_dir       |  10 | 100.00%   | 100.00%    | 100.00%    | 100.00% | 100.00% | 100.00% |
| C Balanced M_dir       |  20 | 85.00%   | 85.00%    | 80.00%    | 100.00% | 100.00% | 33.33% |
| C Balanced M_dir       |  40 | 70.00%   | 60.00%    | 52.50%    | 100.00% | 53.85% | 0.00% |
| C Balanced M_dir       |  80 | 71.25%   | 56.25%    | 50.00%    | 100.00% | 44.44% | 3.85% |
| D Balanced queries     |  10 | 68.89%   | 97.78%    | 66.67%    | 66.67% | 86.67% | 46.67% |
| D Balanced queries     |  20 | 68.89%   | 88.89%    | 70.00%    | 80.00% | 96.67% | 33.33% |
| D Balanced queries     |  40 | 73.33%   | 72.82%    | 61.03%    | 93.85% | 78.46% | 10.77% |
| D Balanced queries     |  80 | 71.28%   | 55.90%    | 49.23%    | 100.00% | 43.85% | 3.85% |
| E32 m=32 binary        |  10 | 100.00%   | 100.00%    | 100.00%    | 100.00% | 100.00% | 100.00% |
| E32 m=32 binary        |  20 | 85.00%   | 85.00%    | 80.00%    | 100.00% | 100.00% | 33.33% |
| E32 m=32 binary        |  40 | 70.00%   | 60.00%    | 52.50%    | 100.00% | 53.85% | 0.00% |
| E32 m=32 binary        |  80 | 71.25%   | 56.25%    | 50.00%    | 100.00% | 44.44% | 3.85% |
| E64 m=64 binary        |  10 | 100.00%   | 100.00%    | 100.00%    | 100.00% | 100.00% | 100.00% |
| E64 m=64 binary        |  20 | 85.00%   | 85.00%    | 80.00%    | 100.00% | 100.00% | 33.33% |
| E64 m=64 binary        |  40 | 70.00%   | 60.00%    | 52.50%    | 100.00% | 53.85% | 0.00% |
| E64 m=64 binary        |  80 | 71.25%   | 56.25%    | 50.00%    | 100.00% | 44.44% | 3.85% |
| F Curated ConceptNet   |  10 | 100.00%   | 100.00%    | 100.00%    | 100.00% | 100.00% | 100.00% |
| F Curated ConceptNet   |  20 | 85.00%   | 85.00%    | 80.00%    | 100.00% | 100.00% | 33.33% |
| F Curated ConceptNet   |  40 | 75.00%   | 85.00%    | 75.00%    | 92.86% | 100.00% | 30.77% |
| F Curated ConceptNet   |  80 | 73.75%   | 77.50%    | 68.75%    | 96.30% | 100.00% | 7.69% |
| G Best (D+B1+F)        |  10 | 73.34%   | 97.78%    | 75.56%    | 73.33% | 100.00% | 53.33% |
| G Best (D+B1+F)        |  20 | 72.22%   | 96.67%    | 73.33%    | 73.33% | 100.00% | 46.67% |
| G Best (D+B1+F)        |  40 | 76.92%   | 87.69%    | 88.20%    | 89.23% | 100.00% | 75.38% |
| G Best (D+B1+F)        |  80 | 73.85%   | 79.49%    | 93.33%    | 89.23% | 100.00% | 90.77% |

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

Baseline N=80: winner_apple=82.50%,
winner_horse=15.00%, winner_car=1.25%.

### P2 — ¿Normalización B1/B2 reduce el sesgo?

B1 (÷count): mature_acc N=80 = 91.25% vs baseline 50.00%
B2 (÷√count): mature_acc N=80 = 53.75%

La normalización penaliza al agente con más registros (apple). B1 divide directamente
por el número de veces que el agente fue registrado, equilibrando los scores.
El efecto es parcial si el sesgo también viene de M_dom (reconocimiento).

Horse N=80: A=44.44% → B1=100.00%
Car  N=80: A=3.85% → B1=80.77%

### P3 — ¿El balanceo de queries (D) mejora el early phase?

D early_acc N=80 = 71.28% vs A = 71.25%
D mature_acc N=80 = 49.23%

Con floor(N/3) queries exactas por dominio e interleaved, los registros en M_dir
deberían ser más balanceados. Sin embargo, si M_dom tiene sesgos propios (reconoce
mejor apple), el efecto es limitado.

### P4 — ¿El registro balanceado (C) es efectivo?

C mature_acc N=80 = 50.00%
C winner_apple = 82.50% vs A = 82.50%

El cap (max_ratio=3.0) previene que un agente acumule >3× los registros del mínimo.
Esto ayuda si el sesgo es de registro; si el sesgo viene de M_dom (reconocimiento en
early phase), C no puede compensarlo completamente.

### P5 — ¿Aumentar m (E32, E64) mejora discriminación?

E32 mature_acc N=80 = 50.00%
E64 mature_acc N=80 = 50.00%

**Resultado esperado y confirmado**: cambiar m NO mejora discriminación para vectores
binarios. `quantize_binary` mapea sign(v)∈{-1,+1} a {0, m-1}, usando solo 2 de m bins.
Con m=32: usa posiciones 0 y 31. Con m=64: posiciones 0 y 63. El patrón de bits es
idéntico, cambian solo los índices absolutos.

**Recomendación**: usar vectores fastText continuos (no sign(v)) para M_dir con
normalización global min/max permitiría aprovechar la resolución de m>2.

### P6 — ¿La curación de ConceptNet (F) reduce engine→apple?

F mature_acc_car N=80 = 7.69% vs A = 3.85%
F mature_acc N=80 = 68.75%

Remover {computer, mac, macintosh, eden} del M_dom de apple hace que tokens como
"engine", "machine", "motor" tengan menos afinidad con apple en early phase.
El agente car gana más queries con tokens mecanicos → M_dir aprende correctamente.

### P7 — ¿Cuál es la mejor combinación?

Mejor condicion: G (G Best (D+B1+F))
N=80: mature_acc=93.33% (baseline: 50.00%, mejora: +43.33%)

Entropía M_dir (A): 1.534 bits
Entropía M_dir (G): 1.547 bits
(máximo posible: 1.585 bits para 3 agentes)

Registros M_dir (A): apple=84,
  horse=69, car=43
Registros M_dir (G): apple=74,
  horse=73, car=44

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
