# Experimento 5 — prototipo emergente (llenado entrópico)

El autoencoder debe construir su propia abstracción: se registran las 50
instancias reales por clase (round-robin label×freq → z_real) en
lugar del promedio artificial. Misma masa de registros que stage5;
M_dom_L idéntico; solo cambia el lado derecho de M_dom_H y M_dom_R.

## Resultados

| hipótesis | métrica | viejo (promedio) | nuevo (instancias) |
|---|---|---|---|
| H1 variedad | recalls distintos /12 | 12.0 | 10.6 |
| H2 aceptación inversa (train) | media 8 clases | 100.0% | 93.1% |
| H2 aceptación inversa (test) | media 8 clases | 82.5% | 0.0% |
| H3 routing temprano | acc (rechazo) | 80.0% (1.2%) | 70.0% (1.2%) |
| H4 entropía M_dom_H | media 8 clases | 5.3616 | 4.4579 |

## Detalle variedad por clase

| clase | cue | distintos viejo | distintos nuevo | L1 viejo | L1 nuevo |
|---|---|---|---|---|---|
| apple | fruit | 12/12 | 12/12 | 2.511 | 1.898 |
| car | vehicle | 12/12 | 12/12 | 2.560 | 1.814 |
| cow | milk | 12/12 | 12/12 | 2.994 | 1.346 |
| cup | drink | 12/12 | 12/12 | 2.073 | 1.037 |
| dog | pet | 12/12 | 12/12 | 2.395 | 1.733 |
| horse | mane | 12/12 | 12/12 | 2.263 | 1.515 |
| pear | pome | 12/12 | 12/12 | 2.285 | 0.657 |
| tomato | vegetable | 12/12 | 1/12 | 2.396 | 0.000 |

## Archivos
- metrics.json · fig1_recall_variety_grid.png · fig2_reverse_acceptance.png

Nota: ningún artefacto previo modificado; el brazo nuevo vive solo
en memoria durante la corrida.