# Experimento 3 — protocolo completo con routing corregido

## Configuración
- Scoring oficial: recognize_gated (gate de containment, activación media de celdas no nulas), sin ÷mem.mean
- Sin filtro léxico: tokens representables por fastText entran como pista; el rechazo lo decide la EAM (score 0) o la frontera del encoder
- Aprendizaje: solo los directorios de labels registran (TME + 3 agentes), token → ganador. mem_dir_R NO se actualiza con recalls (solo percepciones reales de imágenes en stage7)
- Fase madura: TME apagado, entrada aleatoria (seed 42), M_dir con B1
- Arquitectura 4-AMR completa con DirectoryMemory (EHAM real)
- ι=κ=ξ=0, σ=0.1 · M_dom de stage5 sin modificar

## Resultados (banco de 80 queries, GT 27/27/26)

| métrica | exp. 1 (crudo) | exp. 3 (corregido) |
|---|---|---|
| early accuracy | ~34% | **97.5%** |
| early rechazo | — | 1.2% |
| mature accuracy B1 | 98.8% (ablation B1) | **98.8%** |
| mature accuracy RAW | 33.8% | 53.8% |
| fidelidad | 100% (sobre routing sesgado) | **97.5%** (sobre routing correcto) |
| M_dir counts | [81, 52, 31] estilo-crudo | [78, 65, 53] |
| M_dir entropía | — | 1.567 bits (máx 1.585) |

## Réplica de las 10 TEST_QUERIES del exp. 1

- counts exp. 1: [7, 4, 2] (apple capturó vehicle, engine, red…)
- counts exp. 3: [6, 7, 6]

| query | winner exp. 3 |
|---|---|
| a round red fruit | apple |
| fast vehicle with wheels | car |
| animal with a mane | horse |
| sweet edible thing | None |
| large powerful mammal | horse |
| machine for transportation | car |
| grows on trees | apple |
| has four legs and hooves | horse |
| has an engine | car |
| fruit with seeds inside | apple |

## Archivos
- summary.json · results_per_query.csv · exp3_mdir_state.pkl
- fig1_exp1_vs_exp3.png · fig2_mdir_counts.png