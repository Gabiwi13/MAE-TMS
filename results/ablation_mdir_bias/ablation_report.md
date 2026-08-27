# Ablation Report — Sesgo de M_dir en EAM-TMS
**Arquitectura:** HeteroAssociativeMemory (n=300, m=16, p=64, q=32) + ConceptNet 5.7.0
**Dominios:** apple / car / cow / cup / dog / horse / pear / tomato (ETH-80, 8 clases)

> **Nota:** los NÚMEROS de este reporte salen de la corrida actual de 8 clases
> (N=400, 5 seeds). La NARRATIVA cualitativa de P1–P7 abajo es el
> diagnóstico histórico de la era v2 (3 clases, cuantización `sign(v)`,
> polisemia de Apple Inc.); la cuantización actual es por MAGNITUD y el
> análisis vigente vive en el paper (.tex) y en generate_paper_figures.py.

---

## Resumen ejecutivo

El baseline (A) muestra sesgo estructural donde apple domina la fase madura con
24.00% de victorias vs 6.75% (horse)
y 12.00% (car) en N=400.

La mejor condición encontrada es **B1** (B1 Norm/count):
mejora mature accuracy de 80.00% a 93.25%
(Δ = +13.25%).

---

## Tabla de resultados (promedio sobre 5 seeds)

| Condicion              | N   | EarlyAcc | Fidelidad | MatureAcc |
|------------------------|-----|----------|-----------|----------|
| A Baseline             |  50 | 78.00%   | 84.00%    | 62.00%    |
| A Baseline             | 100 | 81.00%   | 78.00%    | 67.00%    |
| A Baseline             | 200 | 80.50%   | 81.00%    | 69.00%    |
| A Baseline             | 400 | 88.00%   | 87.25%    | 80.00%    |
| B1 Norm/count          |  50 | 78.00%   | 98.00%    | 80.00%    |
| B1 Norm/count          | 100 | 81.00%   | 90.00%    | 86.00%    |
| B1 Norm/count          | 200 | 80.50%   | 90.00%    | 86.00%    |
| B1 Norm/count          | 400 | 88.00%   | 93.50%    | 93.25%    |
| B2 Norm/sqrt           |  50 | 78.00%   | 98.00%    | 76.00%    |
| B2 Norm/sqrt           | 100 | 81.00%   | 87.00%    | 75.00%    |
| B2 Norm/sqrt           | 200 | 80.50%   | 87.50%    | 76.50%    |
| B2 Norm/sqrt           | 400 | 88.00%   | 95.00%    | 89.00%    |
| C Balanced M_dir       |  50 | 78.00%   | 94.00%    | 72.00%    |
| C Balanced M_dir       | 100 | 81.00%   | 87.00%    | 77.00%    |
| C Balanced M_dir       | 200 | 80.50%   | 82.50%    | 75.50%    |
| C Balanced M_dir       | 400 | 88.00%   | 91.50%    | 86.50%    |
| D Balanced queries     |  50 | 89.58%   | 96.67%    | 87.50%    |
| D Balanced queries     | 100 | 85.83%   | 93.12%    | 82.92%    |
| D Balanced queries     | 200 | 87.90%   | 91.90%    | 83.90%    |
| D Balanced queries     | 400 | 88.57%   | 89.57%    | 82.76%    |
| E32 m=32 binary        |  50 | 78.00%   | 84.00%    | 62.00%    |
| E32 m=32 binary        | 100 | 81.00%   | 78.00%    | 67.00%    |
| E32 m=32 binary        | 200 | 80.50%   | 83.00%    | 71.00%    |
| E32 m=32 binary        | 400 | 88.00%   | 91.25%    | 84.75%    |
| E64 m=64 binary        |  50 | 78.00%   | 86.00%    | 64.00%    |
| E64 m=64 binary        | 100 | 81.00%   | 79.00%    | 68.00%    |
| E64 m=64 binary        | 200 | 80.50%   | 81.50%    | 72.50%    |
| E64 m=64 binary        | 400 | 88.00%   | 92.00%    | 86.50%    |
| F Curated ConceptNet   |  50 | 78.00%   | 84.00%    | 62.00%    |
| F Curated ConceptNet   | 100 | 81.00%   | 78.00%    | 67.00%    |
| F Curated ConceptNet   | 200 | 80.50%   | 81.00%    | 69.00%    |
| F Curated ConceptNet   | 400 | 88.00%   | 87.25%    | 80.00%    |
| G Best (D+B1+F)        |  50 | 89.58%   | 99.17%    | 90.00%    |
| G Best (D+B1+F)        | 100 | 85.83%   | 97.09%    | 87.71%    |
| G Best (D+B1+F)        | 200 | 87.90%   | 94.40%    | 91.40%    |
| G Best (D+B1+F)        | 400 | 88.57%   | 93.63%    | 92.93%    |

---

## Respuestas a las 7 preguntas de investigación

> **[HISTÓRICO v2/3-clases]** P1–P7 describen el diagnóstico de la era de
> `sign(v)` + Apple Inc.; NO aplican a la cuantización por magnitud vigente
> (ver disclaimer arriba). Los NÚMEROS de la tabla sí son de la corrida actual.

### P1 — ¿El sesgo hacia apple es estructural o aleatorio?

**[HISTÓRICO]** **Estructural.** Tres mecanismos se combinan:
1. **Cuantización binaria** *(ya no vigente: hoy es por magnitud)*:
   `quantize_binary(sign(v), m=16)` mapeaba exactamente 2 valores
   (0 y 15). Apple acumula más registros cuando sus labels ganan el early phase.
2. **Acumulación asimétrica**: si apple gana N_a queries y el resto gana menos, M_dir
   acumula N_a × n_tokens registros para apple vs. menos para los demás.
3. **Polisemia de ConceptNet**: labels de Apple Inc. (computer, mac, macintosh) permiten
   que tokens de car/horse activen el agente apple en early phase.

Baseline N=400: winner_apple=24.00%,
winner_horse=6.75%, winner_car=12.00%.

### P2 — ¿Normalización B1/B2 reduce el sesgo?

B1 (÷count): mature_acc N=400 = 93.25% vs baseline 80.00%
B2 (÷√count): mature_acc N=400 = 89.00%

La normalización penaliza al agente con más registros (apple). B1 divide directamente
por el número de veces que el agente fue registrado, equilibrando los scores.
El efecto es parcial si el sesgo también viene de M_dom (reconocimiento).

Horse N=400: A=54.00% → B1=82.00%
Car  N=400: A=96.00% → B1=98.00%

### P3 — ¿El balanceo de queries (D) mejora el early phase?

D early_acc N=400 = 88.57% vs A = 88.00%
D mature_acc N=400 = 82.76%

Con floor(N/3) queries exactas por dominio e interleaved, los registros en M_dir
deberían ser más balanceados. Sin embargo, si M_dom tiene sesgos propios (reconoce
mejor apple), el efecto es limitado.

### P4 — ¿El registro balanceado (C) es efectivo?

C mature_acc N=400 = 86.50%
C winner_apple = 20.75% vs A = 24.00%

El cap (max_ratio=3.0) previene que un agente acumule >3× los registros del mínimo.
Esto ayuda si el sesgo es de registro; si el sesgo viene de M_dom (reconocimiento en
early phase), C no puede compensarlo completamente.

### P5 — ¿Aumentar m (E32, E64) mejora discriminación?

E32 mature_acc N=400 = 84.75%
E64 mature_acc N=400 = 86.50%

**[HISTÓRICO — sign(v), ya no vigente]** Cuando la cuantización era binaria,
cambiar m NO mejoraba discriminación: `quantize_binary` mapeaba sign(v)∈{-1,+1}
a {0, m-1}, usando solo 2 de m bins. HOY la cuantización es por MAGNITUD y usa
todos los m niveles, así que E32/E64 ya no prueban lo que su nombre sugiere;
la recomendación de "usar vectores continuos" YA se aplicó (fastText crudo).

### P6 — ¿La curación de ConceptNet (F) reduce engine→apple?

**[NO-OP en v4]** Los labels de Apple Inc. (computer/mac/macintosh/eden) ya no
están en labels_apple.json (vocabulario por masa asociativa), así que F no
remueve nada y F ≡ A; los números F/A abajo deben coincidir.

F mature_acc_car N=400 = 96.00% vs A = 96.00%
F mature_acc N=400 = 80.00%

Remover {computer, mac, macintosh, eden} del M_dom de apple hace que tokens como
"engine", "machine", "motor" tengan menos afinidad con apple en early phase.
El agente car gana más queries con tokens mecanicos → M_dir aprende correctamente.

### P7 — ¿Cuál es la mejor combinación?

Mejor condicion: B1 (B1 Norm/count)
N=400: mature_acc=93.25% (baseline: 80.00%, mejora: +13.25%)

Entropía M_dir (A): 2.955 bits
Entropía M_dir (G): 2.961 bits
(máximo posible: 3.000 bits para 8 agentes)

Registros M_dir (A): apple=206,
  horse=100, car=115
Registros M_dir (G): apple=199,
  horse=101, car=114

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
| `domain_accuracy_ablation.png` | Accuracy por dominio por condicion (N=400) |
| `winner_distribution.png` | Distribucion de ganadores en fase madura |
| `confusion_matrix_baseline.png` | Matriz de confusion baseline A |
| `confusion_matrix_best_condition.png` | Matriz de confusion mejor condicion |
| `mdir_registration_counts.png` | Registros en M_dir por agente |
