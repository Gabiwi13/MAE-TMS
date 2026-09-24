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
19.50% de victorias vs 9.25% (horse)
y 12.00% (car) en N=400.

La mejor condición encontrada es **G** (G Best (D+B1+F)):
mejora mature accuracy de 87.00% a 94.03%
(Δ = +7.03%).

---

## Tabla de resultados (promedio sobre 5 seeds)

| Condicion              | N   | EarlyAcc | Fidelidad | MatureAcc |
|------------------------|-----|----------|-----------|----------|
| A Baseline             |  50 | 78.00%   | 86.00%    | 64.00%    |
| A Baseline             | 100 | 83.00%   | 79.00%    | 70.00%    |
| A Baseline             | 200 | 82.50%   | 79.50%    | 69.50%    |
| A Baseline             | 400 | 90.00%   | 92.00%    | 87.00%    |
| B1 Norm/count          |  50 | 78.00%   | 98.00%    | 80.00%    |
| B1 Norm/count          | 100 | 83.00%   | 94.00%    | 88.00%    |
| B1 Norm/count          | 200 | 82.50%   | 90.50%    | 87.50%    |
| B1 Norm/count          | 400 | 90.00%   | 95.25%    | 93.50%    |
| B2 Norm/sqrt           |  50 | 78.00%   | 98.00%    | 76.00%    |
| B2 Norm/sqrt           | 100 | 83.00%   | 94.00%    | 82.00%    |
| B2 Norm/sqrt           | 200 | 82.50%   | 91.00%    | 83.00%    |
| B2 Norm/sqrt           | 400 | 90.00%   | 95.25%    | 93.25%    |
| C Balanced M_dir       |  50 | 78.00%   | 96.00%    | 74.00%    |
| C Balanced M_dir       | 100 | 83.00%   | 88.00%    | 76.00%    |
| C Balanced M_dir       | 200 | 82.50%   | 80.50%    | 74.50%    |
| C Balanced M_dir       | 400 | 90.00%   | 92.50%    | 89.50%    |
| D Balanced queries     |  50 | 91.25%   | 97.92%    | 90.42%    |
| D Balanced queries     | 100 | 88.75%   | 93.96%    | 86.67%    |
| D Balanced queries     | 200 | 90.50%   | 94.20%    | 89.90%    |
| D Balanced queries     | 400 | 90.48%   | 92.53%    | 89.02%    |
| E32 m=32 binary        |  50 | 78.00%   | 90.00%    | 68.00%    |
| E32 m=32 binary        | 100 | 83.00%   | 79.00%    | 70.00%    |
| E32 m=32 binary        | 200 | 82.50%   | 81.50%    | 72.50%    |
| E32 m=32 binary        | 400 | 90.00%   | 93.50%    | 90.50%    |
| E64 m=64 binary        |  50 | 78.00%   | 92.00%    | 70.00%    |
| E64 m=64 binary        | 100 | 83.00%   | 79.00%    | 70.00%    |
| E64 m=64 binary        | 200 | 82.50%   | 82.50%    | 75.50%    |
| E64 m=64 binary        | 400 | 90.00%   | 93.25%    | 92.25%    |
| F Curated ConceptNet   |  50 | 78.00%   | 86.00%    | 64.00%    |
| F Curated ConceptNet   | 100 | 83.00%   | 79.00%    | 70.00%    |
| F Curated ConceptNet   | 200 | 82.50%   | 79.50%    | 69.50%    |
| F Curated ConceptNet   | 400 | 90.00%   | 92.00%    | 87.00%    |
| G Best (D+B1+F)        |  50 | 91.25%   | 99.17%    | 91.67%    |
| G Best (D+B1+F)        | 100 | 88.75%   | 97.50%    | 90.21%    |
| G Best (D+B1+F)        | 200 | 90.50%   | 95.20%    | 93.80%    |
| G Best (D+B1+F)        | 400 | 90.48%   | 95.34%    | 94.03%    |

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

Baseline N=400: winner_apple=19.50%,
winner_horse=9.25%, winner_car=12.00%.

### P2 — ¿Normalización B1/B2 reduce el sesgo?

B1 (÷count): mature_acc N=400 = 93.50% vs baseline 87.00%
B2 (÷√count): mature_acc N=400 = 93.25%

La normalización penaliza al agente con más registros (apple). B1 divide directamente
por el número de veces que el agente fue registrado, equilibrando los scores.
El efecto es parcial si el sesgo también viene de M_dom (reconocimiento).

Horse N=400: A=72.00% → B1=88.00%
Car  N=400: A=96.00% → B1=98.00%

### P3 — ¿El balanceo de queries (D) mejora el early phase?

D early_acc N=400 = 90.48% vs A = 90.00%
D mature_acc N=400 = 89.02%

Con floor(N/3) queries exactas por dominio e interleaved, los registros en M_dir
deberían ser más balanceados. Sin embargo, si M_dom tiene sesgos propios (reconoce
mejor apple), el efecto es limitado.

### P4 — ¿El registro balanceado (C) es efectivo?

C mature_acc N=400 = 89.50%
C winner_apple = 17.50% vs A = 19.50%

El cap (max_ratio=3.0) previene que un agente acumule >3× los registros del mínimo.
Esto ayuda si el sesgo es de registro; si el sesgo viene de M_dom (reconocimiento en
early phase), C no puede compensarlo completamente.

### P5 — ¿Aumentar m (E32, E64) mejora discriminación?

E32 mature_acc N=400 = 90.50%
E64 mature_acc N=400 = 92.25%

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
F mature_acc N=400 = 87.00%

Remover {computer, mac, macintosh, eden} del M_dom de apple hace que tokens como
"engine", "machine", "motor" tengan menos afinidad con apple en early phase.
El agente car gana más queries con tokens mecanicos → M_dir aprende correctamente.

### P7 — ¿Cuál es la mejor combinación?

Mejor condicion: G (G Best (D+B1+F))
N=400: mature_acc=94.03% (baseline: 87.00%, mejora: +7.03%)

Entropía M_dir (A): 2.974 bits
Entropía M_dir (G): 2.977 bits
(máximo posible: 3.000 bits para 8 agentes)

Registros M_dir (A): apple=186,
  horse=112, car=115
Registros M_dir (G): apple=180,
  horse=113, car=114

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
