# Experimento 3 — protocolo completo con routing corregido

## Configuración
- Scoring oficial: recognize_gated (gate de containment, activación media de celdas no nulas), sin ÷mem.mean
- Sin filtro léxico: tokens representables por fastText entran como pista; el rechazo lo decide la EAM (score 0) o la frontera del encoder
- Aprendizaje: solo los directorios de labels registran (TME + un directorio por agente), token → ganador. mem_dir_R NO se actualiza con recalls (solo percepciones reales de imágenes en stage7)
- Fase madura: TME apagado, entrada aleatoria (seed 42), M_dir con B1
- Arquitectura 4-AMR completa con DirectoryMemory (EHAM real)
- ι=κ=ξ=0, σ=0.1 · M_dom de stage5 sin modificar

## Resultados (banco de 80 queries, 10 por clase)

| métrica | exp. 1 (crudo, v3 · 3 clases) | exp. 3 (corregido, 8 clases) |
|---|---|---|
| early accuracy | ~34% | **71.2%** |
| early rechazo | — | 8.8% |
| mature accuracy B1 | 98.8% (ablation B1, v3) | **75.0%** |
| mature accuracy RAW | 33.8% | 65.0% |
| fidelidad | 100% (sobre routing sesgado) | **90.0%** (sobre routing correcto) |
| M_dir counts | [81, 52, 31] estilo-crudo (v3) | [72, 14, 36, 21, 20, 21, 3, 23] |
| M_dir entropía | — | 2.651 bits (máx 3.000) |

## Réplica de las 16 TEST_QUERIES del pipeline oficial (2 por dominio)

- counts exp. 1 (v3, 10 queries de 3 clases): [7, 4, 2] (apple capturó vehicle, engine, red…)
- counts exp. 3: [24, 6, 5, 6, 2, 4, 0, 0]

| query | winner exp. 3 |
|---|---|
| a crunchy red fruit with a core | apple |
| fast vehicle with wheels | car |
| farm animal that gives milk | cow |
| a mug for drinking coffee | cup |
| a barking domestic pet | dog |
| animal with a mane | horse |
| sweet green fruit with a narrow neck | apple |
| red juicy fruit used in salads | apple |
| sweet fruit from an orchard tree | apple |
| machine for transportation with an engine | car |
| bovine beast that moos | cow |
| small container for a hot drink | cup |
| canine with a wagging tail | None |
| riding animal with hooves | horse |
| teardrop shaped orchard fruit | apple |
| round red fruit growing on a vine | apple |

## Archivos
- summary.json · results_per_query.csv · exp3_mdir_state.pkl
- fig1_exp1_vs_exp3.png · fig2_mdir_counts.png