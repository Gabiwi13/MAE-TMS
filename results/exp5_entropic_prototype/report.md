# Experimento 5 — prototipo emergente (llenado entrópico)

La MAE debe construir su propia abstracción: se registran las 50
instancias reales por clase (round-robin label×freq → z_real) en
lugar del promedio artificial. Misma masa de registros que stage5;
M_dom_L idéntico; solo cambia el lado derecho de M_dom_H y M_dom_R.

## Resultados

| hipótesis | métrica | viejo (promedio) | nuevo (instancias) |
|---|---|---|---|
| H1 variedad | recalls distintos /12 | 1.0 | 12.0 |
| H2 aceptación inversa (train) | media 3 clases | 0.0% | 100.0% |
| H2 aceptación inversa (test) | media 3 clases | 0.0% | 0.0% |
| H3 routing temprano | acc (rechazo) | 97.5% (2.5%) | 97.5% (2.5%) |
| H4 entropía M_dom_H | media 3 clases | 0.7747 | 3.9333 |

## Detalle variedad por clase

| clase | cue | distintos viejo | distintos nuevo | L1 viejo | L1 nuevo |
|---|---|---|---|---|---|
| apple | fruit | 1/12 | 12/12 | 0.000 | 2.983 |
| horse | mane | 1/12 | 12/12 | 0.000 | 1.462 |
| car | vehicle | 1/12 | 12/12 | 0.000 | 3.487 |

## Archivos
- metrics.json · fig1_recall_variety_grid.png · fig2_reverse_acceptance.png

Nota: ningún artefacto previo modificado; el brazo nuevo vive solo
en memoria durante la corrida.