# Experimento 5 — prototipo emergente: delta vs instancias

Ablación del protocolo de llenado con ambos brazos EN MEMORIA sobre
las mismas 50 imágenes/clase y la misma masa de registros. DELTA:
label×freq → el mismo latente promediado (abstracción fuera de la
memoria, protocolo v1). INSTANCIAS: label×freq → latente real
round-robin (la relación acumula la distribución, protocolo v2+).
M_dom_L compartido; solo cambia el lado derecho de M_dom_H y M_dom_R.

## Resultados

| hipótesis | métrica | delta (promedio) | instancias |
|---|---|---|---|
| H1 variedad | recalls distintos /12 | 1.0 | 12.0 |
| H2 aceptación inversa (train) | media 8 clases | 0.0% | 100.0% |
| H2 aceptación inversa (test) | media 8 clases | 0.0% | 0.0% |
| H3 routing temprano | acc (rechazo) | 65.0% (8.8%) | 67.5% (8.8%) |
| H4 entropía M_dom_H | media 8 clases | 2.6364 | 4.9030 |

## Detalle variedad por clase

| clase | cue | distintos delta | distintos inst | L1 delta | L1 inst |
|---|---|---|---|---|---|
| apple | fruit | 1/12 | 12/12 | 0.000 | 1.629 |
| car | vehicle | 1/12 | 12/12 | 0.000 | 2.321 |
| cow | milk | 1/12 | 12/12 | 0.000 | 1.314 |
| cup | drink | 1/12 | 12/12 | 0.000 | 1.815 |
| dog | pet | 1/12 | 12/12 | 0.000 | 1.915 |
| horse | mane | 1/12 | 12/12 | 0.000 | 1.036 |
| pear | pome | 1/12 | 12/12 | 0.000 | 1.495 |
| tomato | vegetable | 1/12 | 12/12 | 0.000 | 1.883 |

## Archivos
- metrics.json · fig1_recall_variety_grid.png · fig2_reverse_acceptance.png

Nota: ningún artefacto previo modificado; ambos brazos viven solo
en memoria durante la corrida.