# Inventario de experimentos

Una fila por script. **Versión actual del sistema:**
- llenado oficial con 16 variantes (23 sep);
- directorios perspectivales (14 sep, a423950);
- pesos homo en todas las lecturas (26 oct, 763c902).

Un resultado medido con otra versión está **desactualizado**. Se actualiza la fila con cada corrida, en el mismo commit que sus resultados.

Columnas:
- **Lee memorias:** «directo» si el script llama a la proyección; «vía X» si lo hace a través de otro script.
- **Último commit:** el de sus resultados en esta rama.

## Sistema principal (ETH-80)

| Script | Resultados | Lee memorias | Último commit | Estado |
|---|---|---|---|---|
| `src/stage5_fill.py` | `models/` | llena (no lee) | 23 sep | al día: el llenado no usa pesos, se verificó byte a byte |
| `src/stage6_interaction.py` | `models/` | directo | 28 oct (d0df16c) | al día |
| `src/stage7_bidirectional.py` | `models/` | directo | 28 oct (d0df16c) | al día |
| `src/stage8_mature.py` | log | directo | 28 oct (d0df16c) | al día |
| `generate_paper_figures.py` | `papers_images/` | directo | 28 oct (d0df16c) | al día |
| `run_ablation.py` | `ablation_mdir_bias` | directo | 28 oct (d0df16c) | al día |
| `run_experiment2_iota_kappa.py` | `exp2_iota_kappa` | directo | 28 oct (abf1735) | al día: κ por cuantiles de la razón medida |
| `run_experiment3.py` | `exp3_corrected_routing` | directo | 28 oct (d0df16c) | al día |
| `run_experiment4.py` | `exp4_directory_formation` | directo | 28 oct (d0df16c) | al día |
| `run_experiment5.py` | `exp5_entropic_prototype` | directo | 28 oct (d0df16c) | al día |
| `run_experiment6.py` | `exp6_capacity` | directo | 28 oct (d0df16c) | al día |
| `run_experiment7_unified_dir.py` | `experimento7` | directo | 28 oct (224f7cd) | al día |
| `run_experiment8_directory_recall.py` | `experimento8` | directo | 28 oct (d0df16c) | al día: sus sondas de texto describen el directorio oficial tal como está (52 registros en car); la tabla de ruteo directo viene de exp10, y la curva de formación de texto está en exp9 |
| `run_experiment8_identity_cue_probe.py` | `experimento8` | directo | 28 oct (d0df16c) | al día |
| `run_sampling_distributions.py` | `experimento8`, `experimento9` | directo | 28 oct (d0df16c) | al día |
| `run_experiment9_member_loss.py` | `experimento9`, `experimento9/formacion_texto` | directo | 28 oct (este commit) | al día; la curva de formación (16 a 240 interacciones de texto) y la mitad texto con 240 están en `formacion_texto` |
| `run_experiment9_probe_phase2.py` | `experimento9` | directo | 28 oct (d0df16c) | al día |
| `run_experiment9_probe_recognition.py` | `experimento9` | directo | 28 oct (d0df16c) | al día |
| `run_experiment10_perspectival_routing.py` | `experimento10` | directo | 28 oct (d0df16c) | al día |
| `run_experiment11_monolithic.py`, `_gate_cost.py`, `_probes.py` | `experimento11` | directo | 28 oct (d0df16c; reporte 224f7cd) | al día |
| `run_experiment12_overlap.py` | `experimento12` | directo | 28 oct (d0df16c) | **control con pesos uniformes corriendo** (`results/controles_uniformes/experimento12`) |
| `run_experiment13_augmentation.py` | `experimento13` | directo | 28 oct (d0df16c) | al día |
| `run_experiment14_latent_energy.py` | `experimento14` | directo | 28 oct (224f7cd) | al día; los rechazos de fase A por «niveles» varían 0–3 de 1024 entre corridas por redondeo de la GPU |
| `run_experiment15_arbiter.py` | `experimento15` | directo | 28 oct (d0df16c) | al día |
| `run_experiment16_leave_object_out.py` | `experimento16` | directo | 28 oct (d0df16c) | al día |
| `run_experiment17_specific_word.py` parte a | `experimento17` | directo | 28 oct (d0df16c) | al día |
| `run_experiment17_specific_word.py` partes b y c | `experimento17` | directo | 17 oct | al día: sus proyecciones reciben los pesos homo explícitos (`recog_weights`), así que ya eran homo |
| `run_experiment17_color_probe.py` | `experimento17` | no (latentes) | 17 oct | al día |
| `run_experiment18_attributes.py` | `experimento18` | directo | 18 oct | al día: igual que exp17 b y c, pesos homo explícitos |
| `run_experiment18_feature_probe.py` | `experimento18` | no (latentes) | 18 oct | al día |
| `run_missing_cue.py` | `missing_cue` | directo | 28 oct (d0df16c; control aa283f6) | al día; el control dice que el cambio viene de las 16 variantes |
| `run_rejection_probe.py` | `rejection_probe` | directo | 23 sep | al día: re-corrido el 28 oct con pesos homo, idéntico byte a byte (10 rechazadas, 2 ruteos falsos de 12) |
| exp19 (checkout `MAE-TMS-exp18`) | `experimento19` | directo | 18 oct | **desactualizado** (pesos): falta decidir si se porta el código (~2.2 h de cómputo) |
| `run_experiment22_size_eth80.py` (traído de exp7-directorio-unificado, 4c9cf01) | `experimento22` | directo | 28 oct (este commit) | al día: con pesos homo, filas idénticas byte a byte |
| `run_cost_benchmark.py` | `computational_cost` | no (tiempos) | 22 sep | no depende de los pesos |
| `run_experiment.py` | — | no | 26 ago | lanzador viejo |

## Industrial (VisA)

| Script | Resultados | Lee memorias | Último commit | Estado |
|---|---|---|---|---|
| `run_industrial_demo.py` | `industrial` | directo | 28 oct (este commit) | al día: con pesos homo sale idéntico a la corrida uniforme |
| `run_enrutador_flota.py` | `enrutador_flota` | directo | 28 oct (este commit) | al día: con pesos homo sale idéntico a la corrida uniforme |
| `run_parametros_mae.py` | `parametros_mae` | directo | 28 oct (este commit) | al día: con pesos homo sale idéntico a la corrida uniforme |
| `run_industrial_clip.py` | `industrial_clip` | directo | 28 oct (este commit) | al día: con pesos homo sale idéntico a la corrida uniforme |
| `run_industrial_monolitica.py` | `industrial_monolitica` | directo | 28 oct (este commit) | al día: con pesos homo sale idéntico a la corrida uniforme |
| `run_cierre_mae.py` | `cierre_mae` | vía demo industrial | 19 oct | al día: re-corrido el 28 oct con pesos homo, idéntico byte a byte |
| `run_cascada_modulos.py` | `cascada_modulos` | vía cierre | 28 oct (este commit) | al día: con pesos homo sale idéntico a la corrida uniforme |
| `run_red_sintetica.py` | `red_sintetica` | vía cierre | 28 oct (este commit) | al día: con pesos homo sale idéntico a la corrida uniforme |
| `run_piloto_modulos.py` | `piloto_modulos` | directo | 28 oct (d0df16c) | al día |
| `run_etapa1_ruteo_dirigido.py` | `etapa1_ruteo_dirigido` | directo | 28 oct (d0df16c) | al día |
| `run_etapa2_evidencia.py` | `etapa2_evidencia` | directo | 28 oct (d0df16c) | al día |
| `run_replica_ablaciones.py` | `replica_ablaciones` | directo | 28 oct (d0df16c) | al día (usa la copia médica de medico-demo) |
| `run_deriva_olvido.py` | `deriva_olvido` | directo | 28 oct (d0df16c) | al día |
| `run_olvido_privacidad.py` | `olvido_privacidad` | directo | 28 oct (d0df16c) | al día |

Las lecturas industriales ya son homo. El ruteo lee los directorios con pesos homo: en el nivel 1, los 1239 puntajes con soporte cambian con el modo de pesos, pero en cada pista una sola pieza tiene soporte, así que el ganador no puede cambiar (0 de 2162 decisiones distintas). Los especialistas leen contención (no depende de pesos) o el puntaje medio de `recog_weights`, que son los pesos homo R[i, a_i]; la monolítica pasa esos mismos pesos de forma explícita.

## Médico (fuente: rama medico-demo)

En esta rama, los resultados médicos son copias viejas. La fuente es medico-demo (af52f80, 28 oct): medico, medico_balanceado, medico_completo y exp20, 21, 23, 25, 26, 27, 28 y 29, al día. Desactualizados: `run_experiment20_ood.py`, `run_experiment24_incremental.py` y `run_experiment24_mondrian.py`.
