# Auditoría integral de sanidad y fidelidad — MAE_Experiment

Fecha: 2 de agosto de 2026 · Rama: `v5-multimodal` · Modalidad: solo lectura (ningún archivo modificado durante la auditoría).

Cinco auditores independientes en paralelo: núcleo asociativo (Opus), fidelidad del pipeline (Opus), apps interactivas (Sonnet), reportes vs. fuentes (Sonnet), scripts y results/ (Sonnet). Este informe consolida y deduplica sus hallazgos; los verificados por más de un auditor se indican.

---

## Veredicto global

**El principio central del proyecto se sostiene**: todas las decisiones (registro, reconocimiento, recuperación, enrutamiento, rechazo) salen de operaciones de memoria asociativa; no hay clasificadores auxiliares, umbrales supervisados ni vectores sintéticos en ningún camino oficial de decisión. El código vendorizado de Pineda & Morales es **byte-idéntico al upstream** (diff contra el clon git real, remote `eam-experiments/hetero`) salvo el guard documentado `fold is not None`, que solo evita cargar clasificadores TF y no toca ninguna operación de memoria.

Cero hallazgos CRITICAL en código. Los dos CRITICAL son documentales (una frase de reporte contradicha por su propia tabla; un report.md muerto en results/). Los MAJOR son de honestidad metodológica —cosas que los reportes deben *declarar*, no resultados que haya que retirar— más dos desajustes documentación-código.

---

## CRITICAL (documentales)

**C1 — "Jerarquía estricta" contradicha por la propia tabla.**
`.SMTex/secciones/05_resultados.tex` y `07_conclusiones.tex` afirman "SS < ST < RS < prototipo de forma estricta en las cuatro pistas", pero en la pista `green` ST y SS empatan exactamente en 0.000 ± 0.000 (la fuente `results/missing_cue/characterization.json` lo confirma, y el propio texto lo admite dos frases después). Corrección: "SS ≤ ST < RS < prototipo, con desigualdad estricta SS < ST en las pistas difíciles".

**C2 — `results/rejection_probe/report.md` está muerto y contradice los datos vigentes de su propia carpeta.**
El `.md` (22 jun, era de 3 clases: "5 rechazadas, 7 falsos routings") convive con `summary.json` y `results_per_query.json` (6 jul, 8 clases: 10 rechazadas, 2 falsos routings). El `run_rejection_probe.py` actual ya no genera ese `.md`. Riesgo alto de citar cifras muertas. Corrección: borrar el `.md` o reescribirlo con advertencia + cifras del JSON.

## MAJOR

**M1 — El rescate por `_label_vocab` vale +23.8 puntos y no está declarado en los reportes.**
`stage6_interaction.py:105-113`. Verificado que "nunca censura" es literalmente cierto (0 desacuerdos en las 411 queries del banco; solo admite). Pero la regla de *quién vota* deriva del vocabulario que llenó las memorias: sobre las 42 queries afectadas, con rescate 41/42 correctas, sin rescate 31/42, y las 10 que cambian de ganador se mueven todas hacia el ground truth (`bark`, `moo`, `saddle`, `wheel`, `brake`...). No es una violación de fidelidad (la EAM sigue decidiendo el ganador), pero es parte del protocolo con efecto medible y debe reportarse con ese delta.

**M2 — El encoder se selecciona con el split de test.**
`stage2_encoder.py:234-249`: no existe split de validación; el checkpoint ganador es el de menor RMSE sobre test, y ese encoder llena las memorias y produce el latente con que después se evalúa. Sesgo acotado (~5 checkpoints) pero es selección de modelo sobre test: declararlo o introducir split de validación.

**M3 — `XI_VISUAL = 2` se calibró sobre el test que después se reporta.**
`stage7_bidirectional.py:39-44` (el propio comentario lo documenta). ξ es mecanismo nativo de la EHAM — el problema es el protocolo de selección, no la operación. Declararlo.

**M4 — El split de ETH-80 es por imagen, no por objeto: solape de instancias del 100%.**
`stage1_dataset.py:118-124` + verificación sobre `splits.json`: ninguna instancia de objeto es exclusiva de test en ninguna de las 8 clases. Las cifras visuales (75.0% de ruteo, evocación, realtime_lab) miden generalización a *vista nueva de objeto conocido*, no a objeto nuevo. Cambio de alcance de la afirmación, no bug. El protocolo estándar es leave-one-object-out (ya listado como trabajo futuro en .tex8 y .SMTex; los reportes deberían acotar el alcance donde citan las cifras).

**M5 — Cadena latente de contaminación: `_stream_lookup(..., allow_fallback=True)` por default.**
`stage4_fasttext.py:30`, contradice su propio docstring. Hoy los 5 call-sites pasan `False` explícito y el cache persistido está limpio (auditado numéricamente: 0/246 vectores con firma sintética), pero una corrida futura con el default se llevaría vectores sintéticos al cache oficial (`models/token_vectors.json`) de forma permanente y silenciosa, porque `get_fasttext_vector` consulta el cache antes que fastText. Corrección: invertir el default a `False`.

**M6 — El reporte .SMTex y el README del lab afirman "VAD Silero"; el código lo desactiva.**
`stt.py:42-44` pasa `vad_filter=False`; la segmentación real la hace un VAD por energía con piso de ruido adaptativo (`audio_worker.py`, cuyo docstring sí lo dice bien). Corrección: `.SMTex` (intro, marco 2.2, arquitectura) y `realtime_lab/README.md` deben describir el VAD por energía; la mención a Silero solo como capacidad de faster-whisper no utilizada.

**M7 — Cifra retractada (47.1%) viva en `realtime_lab/README.md:113`.**
Es un número pre-auditoría-v4 no citable; el vigente es 75.0% (que .SMTex sí usa). Corregir el README para que no contamine informes futuros.

**M8 — Punteros de "fuente canónica" rotos.**
`README.md:94` y `results/experimento1/informe.md:13` citan `results/exp3_corrected_routing/summary.json` como fuente de las cifras v3/3-clases (97.5, 98.75, ...), pero ese archivo fue sobrescrito por la re-corrida de 8 clases y ya no contiene ninguno de esos valores. El disclaimer v3/v4 del README sí existe; solo el enlace está roto.

**M9 — "≈2.1 s" de evocación en la tabla de latencias del .SMTex sin fuente escrita.**
Proviene de una medición real (2089 ms, corrida del 30 jul) pero no está documentada en el repo y el resto del documento dice "~2 s". Alinear a "≈2 s" (o documentar la medición).

**M10 — Documentación de teclas del lab desactualizada.**
`realtime_lab/README.md` y el docstring de `main.py` listan 2 de 6 teclas e incluyen una tecla `espacio` que no existe. El overlay en pantalla sí las lista todas.

## MINOR (selección; detalle completo en los informes de cada auditor)

- **N1** `backward_distance_from_left`: un sentinel (32) se recorta a 31 en silencio por `validate()` y produciría d=0.0 — *el mejor valor posible* — para un no-resultado. Hoy inalcanzable (los 3 callers filtran por `recognized`; 0/40 pistas reales reconocidas con sentinel), pero la protección vive fuera de la función y el modo de falla es silencioso y favorable. Fix barato: mapear sentinel→NaN antes de `validate`.
- **N2** `_norm_weights` convierte pesos todo-cero en unos (opinaría donde debería rechazar). Hoy inocuo por una propiedad *accidental* del llenado (verificado: 0/8725 coordenadas problema) — no un invariante custodiado.
- **N3** `ExperimentSettings` del vendorizado muta una lista global compartida (bug upstream). Benigno hoy porque todos los constructores pasan los 4 parámetros; peligroso si alguien construye una memoria con parámetros parciales tras un barrido ι×κ.
- **N4** `evoke()` en hilo sin try/except: una excepción deja el overlay en "recalling..." para siempre.
- **N5** Margen de ~3 px entre el panel evocado y la sección VISION en cámaras 480p (medido con `cv2.getTextSize`); técnicamente sin traslape, sin margen de diseño.
- **N6** `quantize_binary` cae a escala 0.5 con un `print` si falta `label_quant_scale.json` (incompatible con las memorias llenadas con S=0.18809); debería `raise`.
- **N7** `.SMTex/referencias.bib` tiene 3 entradas sin citar (herencia del .bib de .tex8); los artefactos compilados viejos de `.tex/` aún contienen la clave prohibida `pineda2024hetero` (el fuente está limpio — recompilar antes de entregar ese PDF).
- **N8** Empates de ruteo se resuelven por índice menor (favorece a `apple`) sin registro; `mode` cae a `sqrt` ante cualquier typo distinto de `"linear"`.
- **N9** Carpetas huérfanas pre-v2 en `results/` (`label_recall/`, 3 CSV `semantic_*` en `ablation_mdir_bias/`); comentarios obsoletos en `generate_paper_figures.py`; import muerto en `stage8_mature.py`; `ACCEPTED_POS` duplicado en display de `app_tme.py`.

## Verificado y limpio (declaración explícita)

- Vendorizado byte-idéntico al upstream (3 archivos, diff contra blobs commiteados); sin monkeypatching en todo el proyecto.
- ST/RS/SS fieles: mismo `distance_recall`, misma proyección; `stats[1]` ≡ `backward_distance_from_left` (6/6 corridas); conteos de candidatos 1/127/128; números del reporte reproducidos con las semillas del script (prototipo pear 9.015 exacto).
- `run_missing_cue.py`: estadística recomputada desde las 360 distancias crudas — coincidencia exacta; sembrar `random` de Python es suficiente (único generador del camino estocástico); métrica uniforme entre métodos.
- Tabla 3 del .SMTex verificada dígito a dígito contra el JSON por dos auditores independientes.
- Cero vectores sintéticos en camino oficial (26 call-sites revisados + cache auditado numéricamente); cero binarización por signo viva; cuantización por magnitud consistente en todos los puntos de uso; escala S=0.18809 fresca respecto de las memorias.
- Lectura B1 derivable de la propia relación (counts ≡ suma de la relación, verificado en directorio real): no introduce información externa a la MAE. Lectura tolerante ξ usa el mecanismo nativo de funciones parciales.
- Rechazos bien separados (`no_representable_tokens` / `mae_no_support` / `directory_no_support`); `token_in_vocabulary` confinado a logging/display.
- App: suite missing-cue consistente cómputo↔render con casos borde cubiertos; sin keys duplicadas de Streamlit; paletas clara/oscura sin mezcla; contrato router↔main↔overlay coherente; sin carreras de hilos (más allá de N4).
- Reportes: cero citas rotas en los tres; regla de citación EHAM cumplida en los tres fuentes; números inter-reportes (98.75 / 88.0 / 93.2 / 75.0) coherentes; todos los números del lab citados en .SMTex trazan al README sin contradicciones internas (salvo M9).
- Los 12 `run_*.py` + 3 `test_*` del lab compilan; cero llamadas a nombres pre-refactor v3.

## Plan de corrección sugerido

**Lote A — baratos y sin riesgo (código/documentos):** C1 (frase "estricta"), C2 (report.md muerto), M5 (default `allow_fallback=False`), M6 (VAD en .SMTex + README), M7 (47.1%), M8 (punteros), M9 (2.1s→2s), M10 (teclas), N1 (sentinel→NaN), N4 (try/except en evoke), N6 (raise en quantizer), N7 (bib sin citar).

**Lote B — requieren decisión editorial (párrafos nuevos en reportes):** M1 (declarar el rescate con su delta en .tex8/.SMTex), M2+M3 (declarar selección sobre test en limitaciones), M4 (acotar "vista nueva de objeto conocido" donde se citan las cifras visuales).

**Lote C — higiene opcional:** N2, N3, N5, N8, N9.

---

## Estado de aplicación (2 ago 2026, misma fecha)

**Lote A: APLICADO** por tres agentes de corrección + verificación integral posterior:
- C1, M6, M9, N7 (.SMTex + recompilación de .tex): ambos PDF recompilan limpios (0 refs sin resolver); `pineda2024hetero` ausente de los artefactos regenerados; verificado además que los PDF antiguos "(1)" nunca contuvieron la entrada errónea.
- M5, N1, N4, N6 (código): default `allow_fallback=False`; sentinel→NaN en `backward_distance_from_left` con pesos 0 en coordenadas indefinidas y NaN para candidato totalmente indefinido (el fix descubrió y cerró una segunda vía del mismo bug: `project()` con suma de pesos cero + el fallback de columna cero de `calculate_distance` también fabricaban d=0); try/except + estado "error" en la evocación del lab; `raise` en `quantizer.label_scale()`.
- C2, M7, M8, M10 (docs): rejection_probe/report.md reescrito desde los JSON vigentes; 47.1%→75.0%/25%; punteros de fuente canónica corregidos (verificado que ningún destino prometido carece de los números); teclas y VAD del README alineados con el código.
- Verificación final: smoke test sobre memorias reales — prototipos idénticos pre/post fix (pear 9.0150, car 7.9715), RS/ST/SS funcionando; 18 archivos modificados en total.

**Lote B: APLICADO** (commit `faeb03f`): .tex8 declara en metodología el rescate con su delta (+23.8 pts), la selección del encoder por RMSE-sobre-test y el barrido de ξ sobre test, y el solape de instancias del 100% con su consecuencia de alcance; limitación (e) reforzada y nuevas (f)/(g); .SMTex hereda ambas salvedades en su limitación de herencia. Ambos reportes recompilados sin referencias sin resolver.

**Lote C: APLICADO** (commit `7d16899`): N2 (pesos todo-cero → rechazo, en `_norm_weights` y `recognize_gated/both`), N3 (avisos del bug de `ExperimentSettings` en los 3 constructores, vendorizado intacto), N5 (layout del overlay con márgenes reales en 480p), N8 (`mode` inválido falla ruidoso; desempate documentado), N9 (huérfanos pre-v2 → `archive/results_pre_v2/` con README; comentarios obsoletos de generate_paper_figures corregidos; import muerto fuera; `ACCEPTED_POS` sin duplicar). Verificado: py_compile ×7, smoke tests con prototipos idénticos y render del panel.

**La auditoría queda cerrada: los tres lotes aplicados.**
