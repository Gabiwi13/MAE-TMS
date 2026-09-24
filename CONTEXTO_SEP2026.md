# Contexto completo: directorio, TME y revisión (13 a 20 de septiembre de 2026)

Rama `exp7-directorio-unificado`. Este documento recoge, en orden, todo lo hecho en el repositorio entre el 13 y el 20 de septiembre: la discusión teórica sobre el directorio, los experimentos 9 y 10, el cambio del protocolo oficial a directorios perspectivales, y las fases 0 a 2 de la revisión adversarial con sus correcciones y cifras antes/después. Al final, el estado de los modelos, los archivos y lo pendiente.

---

## 1. Punto de partida (13 de septiembre)

Pregunta: "memoria directorio" suena ambiguo porque un directorio de memoria es una memoria por sí mismo; y la idea de que el TME tenga dominio y se incorpore al grupo en la fase madura.

Lo que se encontró en el código antes de tocar nada:

1. El directorio contiene contenido. Leído por identidad reconstruye el dominio del agente al 100% (exp8).
2. Hay nueve copias de la misma relación: cada agente registra todos los broadcasts y el TME también; los ocho `mem_dir_R` son iguales bit a bit (exp8).
3. El TME como entidad no está en Wegner; en el código es un pizarrón de fase temprana con dos directorios.

Se descartó el "TME generalista" (noveno agente lleno con las ocho clases): no prueba ninguna tesis y su resultado se deduce de exp6.

## 2. Marco teórico

Documento: `discusion_marco_teorico_directorio.md`. Bibliografía verificada con enlaces: `bibliografia_marco_teorico.bib` (14 entradas; acceso abierto marcado).

- Eje: división del trabajo epistémico (Putnam 1975; Wegner 1987, 1995). El sistema transactivo es memorias individuales más directorios más procesos; no hay entidad mediadora.
- Dos modos de conocer (Russell 1910): familiaridad (el especialista, que vivió las instancias) y descripción (los demás, que presenciaron y guardan una envolvente). Wegner: codificación profunda y superficial.
- Ícono e índice (Peirce, en Buchler 1955) y nombre como designador rígido (Kripke 1980): el contenido es icónico (métrica, la indeterminación es generalización), el directorio es indicial y su lado derecho es un nombre (sin métrica; la indeterminación es error). Correlato: índice hipocampal (Teyler y DiScenna 1986; Teyler y Rudy 2007) y sistemas complementarios (McClelland, McNaughton y O'Reilly 1995).
- Metamemoria (Nelson y Narens 1990): nivel objeto y nivel meta, monitoreo y control. "El directorio es una memoria per se" deja de ser objeción.
- Dinámica: TME como andamio (Wood, Bruner y Ross 1976) que se internaliza (Vygotsky 1978) contra artefacto compartido (Hutchins 1995; Clark y Chalmers 1998).
- Principio: la entropía vive en el ícono, la decisión en el índice.

Dos tesis con predicción y refutación:
- A (Russell): la descripción rutea pero no reemplaza a la familiaridad. Experimento 9.
- B (Vygotsky contra Hutchins): la internalización perspectival basta o hace falta el pizarrón. Experimento 10.

## 3. Experimento 9: pérdida de un miembro

Script `run_experiment9_member_loss.py`, resultados en `results/experimento9/`. Se quita el agente k; las consultas de su dominio entran por un sobreviviente. Políticas: rechazo, sustitución (mejor sobreviviente responde con su contenido), descripción (sobreviviente responde con `recall_domain(k)` de su directorio). Referencia: vivido (recall del especialista presente). Banco de 411 consultas; el directorio oficial de texto tiene 52 registros (las 16 consultas de fase temprana) y rutea 229 a k, 65 a otro, 117 rechazadas.

Resultados originales (14 de septiembre, pista de identidad con ceros, sin semilla):
- El índice sobrevive al miembro; el directorio rutea a k igual.
- Sustitución: responde 24.5%, clase 0% (confabula con la clase del sustituto) o calla.
- Descripción: responde 100%, clase 100%, d a instancia real 23.3 contra 21.9 del vivido.
- Ninguna respuesta depende de la pista (F cerca de 1 en vivido y descripción).
- Sonda de reconocimiento: el especialista reconoce el 98.3% de las consultas de su dominio, un no especialista el 16.1%, el directorio rutea el 55.7%. La familiaridad se ubicó en el reconocimiento, no en la reproducción.

Estos números cambiaron en la revisión (sección 6).

## 4. Experimento 10: directorios perspectivales

Script `run_experiment10_perspectival_routing.py`, resultados en `results/experimento10/`. Cada agente presencia solo parte de los broadcasts ajenos (al azar con probabilidad f, o solo los de vecinos en anillo de radio r). Protocolos: directo (sin soporte rechaza), encadenado (pregunta a los conocidos por familiaridad hasta que alguien tiene soporte), agregado (suma los scores de todos los conocidos), pizarrón (un directorio con todo). Formación con verdad de terreno; texto 240 consultas de formación y 171 reservadas; imagen 128 de formación y 20 de test por clase; xi=0 en imagen. Ruteo determinista; las semillas 42, 43 y 44 controlan solo el presenciado (verificado en fase 2).

- Imagen: el encadenado iguala al pizarrón (81.9%, cero errores) en toda condición con f>0 o r≥1, desde f=1/64, con 3.5 saltos; directorios que difieren en el 83% de sus celdas.
- Texto: el encadenado elimina el rechazo pero deja errores (33% con f=1/64, 6% con f=1/2); el agregado alcanza al pizarrón desde f=1/32 (91% reservadas contra 93.6). Con f=1/4 el agregado dio 94.3% contra 93.6%, pero la revisión señaló que son cuatro consultas en una de tres semillas: igualación, no superación (pendiente de corregir en prosa, fase 3).
- Alcance y comparación son operaciones distintas: el encadenado alcanza, el agregado compara; con anillo r=1 el agregado cae al 55%.
- La diferencia entre modalidades es de resolución del signo: 64×32 es índice absoluto (cabe o no cabe), 300×16 es relativo (quién cabe mejor).

## 5. Cambio del protocolo oficial (v5, commit f54d64f)

- `register_transaction` (stage 6 y 7): una transacción pista→ganador la registran el agente de entrada, el ganador y el TME. Antes registraban los ocho y el TME.
- `route_transactive` (stage 7 fase B, stage 8, rutas de fase madura e imagen de la app): el agente de entrada agrega su directorio y los de los agentes que conoce; sin soporte, la consulta pasa a los conocidos y cada uno agrega su círculo.
- `XI_VISUAL = 0`: la tolerancia xi define los huecos sobre el soporte de todos los agentes del directorio, así que con directorios perspectivales dependía de lo que presenciaron los demás.
- `process_query` acepta `entry`; stage 6 y 7 eligen la entrada con `RandomState(42)`.
- Re-corrido de etapas 6, 7 y 8: ruteo visual de test 73.6% (antes 75.0%, costo de xi=0), 0 errores; evocación 85.3% (igual); fidelidad temprana↔madura 16/16. Directorios visuales por agente: ~120 propios más 11 a 22 de cada otro (entropía ≈2.3 bits; registro completo 3.0). En texto, con 16 consultas de fase temprana, apple, car y horse quedan conociéndose solo a sí mismos.
- Pendiente declarado: la pestaña en vivo de la app entrena un directorio único de sesión y su animación muestra a todos registrando.
- Respaldo de los modelos v4 en `models_backup_pre_perspectival/`.

## 6. Revisión adversarial: fases 0 a 2 (14 a 15 de septiembre)

Lista de trabajo del usuario: dos defectos de código, cuatro sobreafirmaciones en README, una contradicción entre documentos, y el experimento central pendiente (comparación contra MAE monolítica). Reglas: por fases, números antes que conclusiones, un commit por arreglo, antes y después, split real.

### Fase 0: reconocimiento
- `data/eth80/splits.json` existía pero no estaba versionado (`data/` en `.gitignore`); lo genera `make_splits(seed=42)` con `sorted` más `random.shuffle`, 328/82 por clase. El "128 formación / 20 prueba" no es un split: es `train[200:328]` y `test[:20]` en `run_experiment7_unified_dir.py:148`.
- `_identity_cue` ponía ceros explícitos en los no ganadores. Exp8 no pasaba por ahí: tenía su propio `onehot()` con el mismo defecto.
- F en exp9 sin corrección de Bessel en `var_b` (÷G) y `var_w` (÷REPS).

### Fase 1: pista de identidad
- Diagnóstico confirmado en el split real (`results/experimento8/sonda_pista_identidad.json`): la columna de muestreo con one-hot coincide exactamente con 6·N_all + 2·N_k en las 8 clases; TVD contra la distribución propia 0.235 (visión) y 0.188 (texto); 70 y 74% de la masa viene de otros agentes; con nan la columna es N_k exacta, mismo soporte y mismos niveles vivos (9.34 y 4.24).
- Hallazgo mayor: `hetero_lib` muestrea con `random` de Python (`hetero_associative_4d.py:538`, `:552`, `:571`) y exp8/exp9 solo sembraban numpy. Ningún sorteo publicado era reproducible. La nota de los README que atribuía el muestreo al RNG de numpy es falsa. Se agregó `random.seed(SEED)` junto a `np.random.seed(SEED)` en exp8 y exp9.
- Commits: 565d70d (split versionado en `data/eth80/splits_relative.json`, `make_splits` lo restaura, README), 5532c93 (exp8 usa `DirectoryMemory.recall_domain` y `domain_projection`; deterministas idénticas byte a byte, muestreadas dentro del ruido), 82b6e16 (siembra, sonda, `run_sampling_distributions.py`, `summarize_sampling_distributions.py`), 65a7829 (`_identity_cue` con nan), 9c99157 (figuras y sondas de exp8 regeneradas con nan y semilla, sin el barrido de 50 minutos, que no cambia porque su métrica `reconocido` depende solo del soporte).
- Distribuciones con 20 semillas (`results/experimento8/muestreo_*.json`, `results/experimento9/muestreo_*.json`, resúmenes en `muestreo_resumen.json`), modelos v4:

| cantidad | ceros | nan |
|---|---|---|
| exp8 fidelidad, media de clases (d a instancia real) | 23.38 ± 0.17 | 19.35 ± 0.14 |
| exp8 dispersión entre sorteos, media | 32.6 ± 0.3 | 27.4 ± 0.2 |
| exp8 capacidad N=8 → N=800 | 15.9 → 25.6 | 16.0 → 20.0 |
| exp8 acierto de clase | 1.00 (una semilla 0.988 en N=256) | 1.00 en todo |
| exp9 descripción, media de clases | 23.34 ± 0.14 | 19.30 ± 0.13 |
| exp9 vivido (especialista, 10 semillas) | 22.03 ± 0.21 | igual (no depende de la pista) |

Con la pista corregida, la descripción supera al especialista en fidelidad en 7 de 8 clases y en la media. El 79/80 publicado en capacidad N=800 no reapareció en 40 corridas.

### Fase 2: F y tres preguntas extra
- Nulo simulado: F sin Bessel 1.444 (p5 1.409, p95 1.481), igual al analítico REPS/(REPS−1)·(G−1)/G; con Bessel 1.001 (p5 0.976, p95 1.027).
- Corrida única de exp9 con nan, semilla y Bessel (commit bbde155): F vivido 1.64 → 1.14 (por encima del nulo, dependencia débil), sustitución 2.89 → 2.08, descripción 1.46 → 1.00. Descripción d_nn 19.29 contra vivido 21.87; dispersión 27.7 contra 32.3. Imagen→texto: descripción acierta 100% (antes 98.5%).
- Colapso de primera pista: 198 de 229 consultas ruteadas (86%) comparten su primera pista reconocida con otra; 63 pistas distintas; en el banco completo 73 para 411.
- Razón envolvente / distancia intraclase con nan, 20 semillas: 2.9 a 5.9 veces (antes 3.6 a 7.1); en dog la envolvente queda por debajo del radio de clase.
- Por qué la descripción supera al especialista (`results/experimento9/sonda_fase2.json`): directorio inverso 9.34 niveles vivos / 2.78 bits; mem_dom_H condicionada por etiqueta 8.28 / 2.71; mem_dom_R con 800 instancias 11.34 / 2.87. Condicionar recorta niveles y aun así dispersa más (32.1 contra 27.4). `stage5_fill` registra `label_seq[i % L]` con `z_q[i]`: cada etiqueta quedó emparejada con 38 instancias distintas en promedio (16 a 105), sin correspondencia con la imagen; el directorio guarda ~122 imágenes reales sin aumentación.
- Fallos del especialista (car 3 consultas, horse 1): contención por coordenada; cada token tiene de 12 a 76 coordenadas de etiqueta cuyo valor cuantizado el agente nunca registró, y coincide exactamente con los ceros de la homo izquierda. La descripción no tiene esa puerta.
- Commit a936f0a: sonda de fase 2.
- Exp10 verificado determinista; las semillas controlan solo el presenciado.

### Prosa desactualizada (no reescrita; la reescribe el usuario en fase 3)
- README exp8 y exp9, Notas: "los recalls muestrean con el RNG global de numpy" (falso).
- README exp8: tabla de fidelidad y dispersión, "entre tres y siete veces", hallazgos 2 y 7 ("de 8 a 800 pierde 10 unidades", con nan pierde 4), 79/80 en N=800 y "aparece el primer fallo de clase", "el propio sale 1/160" (5/160 y 4/160 en otras corridas), compat 0.602–0.630 de un sorteo.
- README exp9: tabla texto→imagen, "23.3 contra 21.9 (+6%)", "+11%", "fidelidad apenas menor", "casi la del testigo" (cambian de dirección: 19.3 contra 22.0 a favor de la descripción), F 1.64/2.89/1.46 y "F ≈ 1", tabla imagen→texto (98.5% de una corrida), hallazgo 5 sigue pero hay que agregar la contención en la etiqueta.
- `discusion_marco_teorico_directorio.md` 2.2 ("3 a 7 veces"), 4.1 y 4.3 (números de exp9 y "fidelidad casi igual").
- README exp10: "el agregado supera al pizarrón" (igualación).
- README exp7: atribuir el 25.0% de la consulta emparejada al veto conjuntivo (hereda el rechazo de la imagen, 73.1%).
- Deck: "3.6 a 7.1 veces".

## 7. Estado de modelos y archivos

- `models/` contiene desde el 23 de septiembre los agentes y TME del protocolo **v5 con umbral de energía y llenado de 16 variantes** (etapas 5–8 re-corridas en CPU: 3200 registros por agente, fase A con 16 registros por percepción; stats de cuantización, umbral, escala de etiquetas y directorios de texto idénticos a los anteriores; ruteo de test 96.2 %, 2 falsos, evocación 97.4 %, etapa 8 16/16). `models_v5_umbral/` conserva el v5 con umbral y 4 variantes, `models_v5_perspectival/` el v5 sin umbral y `models_backup_pre_perspectival/` el v4 (directorios idénticos entre agentes, los que produjeron exp8, exp9 y las fases 1 y 2); los tres excluidos vía `.git/info/exclude`.
- Scripts nuevos en la raíz: `run_experiment9_member_loss.py`, `run_experiment9_probe_recognition.py`, `run_experiment9_probe_phase2.py`, `run_experiment10_perspectival_routing.py`, `run_experiment8_identity_cue_probe.py`, `run_sampling_distributions.py`, `summarize_sampling_distributions.py`.
- Cambios en `src/`: `associative_memory.py` (`recall_domain`, `domain_projection`, `_identity_cue` con nan), `stage6_interaction.py` (`register_transaction`, `route_transactive`, `entry` en `process_query`), `stage7_bidirectional.py` (entrada aleatoria, `route_transactive`, `XI_VISUAL=0`), `stage8_mature.py` (`route_transactive`), `stage1_dataset.py` (restauración desde `splits_relative.json`). `app_tme.py`: ruta de imagen con `route_transactive`.
- Resultados: `results/experimento9/`, `results/experimento10/` (con `v1_sin_agregado/`), `results/experimento8/` regenerado (sin el barrido), `sonda_*.json`, `muestreo_*.json`.
- Documentos: `discusion_marco_teorico_directorio.md`, `bibliografia_marco_teorico.bib`, este archivo.
- Logs locales (ignorados): `exp9_*.log`, `exp10*.log`, `muestreo_*.log`, `rerun_perspectival.log`, `exp8_*.log`.

Commits de este periodo, en orden: ddef014, 39e5cf3, 3a130a8, f54d64f, 565d70d, 5532c93, 82b6e16, 65a7829, 9c99157, bbde155, a936f0a.

## 9. Fases 4 y 5 (20 y 21 de septiembre)

- Fase 4: material en `revision_fase4_directorio_entropico_vs_metamemoria.md`. La contradicción es real y acotada: `recall_domain` sí llama a `recall` (`recall_from_right` → `sample_n_search_recall` → `choose`, `random.random()`), pero ningún camino del protocolo lo usa. σ sigue sin importar porque el muestreo por defecto no lo usa. Tres salidas; se aplicó la 5.1 el 21 de septiembre: las frases de `discusion_directorio_entropico.md` se restringen al ruteo y se añade el párrafo de los dos lados de la relación; el marco teórico no cambia.
- Fase 5: diseño en `propuesta_fase5_mae_monolitica.md`, implementación `run_experiment11_monolithic.py`, resultados y `veredicto.md` en `results/experimento11/`. Tres brazos (M, T-oráculo, T-protocolo), cortes {25, 50, 100, 200}, 10 semillas, 3 sorteos, 171 reservadas. Control: los especialistas reconstruidos en float32 son bit a bit los `agent_*.pkl`. No refutada por el criterio pre-registrado (clase empata en 0.1 puntos, fidelidad difiere en 3.9). La partición compra fidelidad (brecha 2.0 → 4.5 con N), coherencia con pista compartida (M 44% de clase, compat 0.73) y precisión en imagen→texto (dominio ajeno 8% contra 1%); cuesta cobertura (79% contra 96% en imagen), 2.5 puntos de directorio y 8× las celdas.
- Infraestructura: cache de memorias por corte (`cache/exp11/`, 1.5 GB cada uno; el registro de hetero_lib cuesta 80 ms), relaciones en memoria compartida entre procesos, trabajos por trozos, `--image-only`, `--ood-only`.
- Hallazgo de reproducibilidad: la etapa 5 cuantizó en float32; en float64 cambia un nivel en un latente de car, cow y dog.
- Fase 3 aplicada el 21 de septiembre (`revision_fase3_prosa.md`): READMEs de exp7, exp8, exp9 y exp10, cifras del marco teórico, README principal y este archivo.
- Fuera de dominio con 40 consultas (21 de septiembre, `results/experimento11/consultas_fuera_dominio.txt`): EHAM única 3/40, oráculo 2/40, protocolo 4/40; el directorio deja pasar dos consultas que el contenido rechaza (piano → dog, thunderstorm → car). Recalculado el 22 de septiembre con la doble compuerta de contenido: el protocolo baja a 2/40 en los cuatro cortes, el nivel del oráculo; la columna «acepta» quedó idéntica.
- Imagen→texto largo (22 de septiembre, 134 min con 6 procesos): cuatro cortes × diez semillas × 80 imágenes de prueba. La cobertura del especialista sube con N (responde 0, 5, 45, 79 %) y la de la EHAM única antes (5, 54, 81, 96 %); el dominio ajeno de la EHAM única sube con N (0 → 8.9 %), el de los especialistas queda en 1.2–1.6 %. En N=200 las cifras de 5 semillas apenas se mueven (dominio ajeno 8.0 → 8.9).
- Doble compuerta de contenido en la fase madura textual (22 de septiembre, commit 3538b4a): tras `route_transactive`, el agente destino debe dar `recognize_gated > 0` para alguna pista; si no, rechazo con motivo `content_no_support` conservando el destino señalado. En `stage8_mature.route_mature`, en los tres backends de la pestaña 4 de la app y en `ood_rows_for` de exp11 (campo `acepta_compuerta`, sin tocar `acepta`). Etapa 8: 16/16. En la app con los modelos oficiales v5 las 40 consultas fuera de dominio las rechaza el propio directorio. De paso: `route_mature` mandaba el latente a cuda y la app tiene el decodificador en CPU; ahora usa el dispositivo del decodificador.
- Costo de la compuerta sobre las reservadas (22 de septiembre, `run_experiment11_gate_cost.py`, `results/experimento11/compuerta_reservadas.md`): ninguna respuesta perdida; 1.4–1.5 % de rechazos en N ≥ 50, todos ruteos equivocados sin recall; 21.1 % en N = 25, sin recall.
- Costo computacional en la laptop 2 (22 de septiembre, `results/computational_cost/comparacion_laptops.md`): pipeline 133.5 → 50.6 min en CPU y 31.9 con GPU; la GPU solo acelera el encoder (22.3 → 5.1 min); batería 159.9 → 70.5 min. Medido en un worktree aislado (`../MAE-TMS-bench`), que sigue ahí con sus logs; se puede borrar con `git worktree remove ..\MAE-TMS-bench --force`.
- Experimento 13 (22–23 de septiembre, `run_experiment13_augmentation.py`, `results/experimento13/`, diseño en `propuesta_exp13_augmentacion_visual.md`): augmentación del llenado visual, 13 combinaciones × 5 semillas sobre las 656 de test. El 25 % de rechazo son dos compuertas: el directorio visual (formado sin augmentar) y el recall de la hetero (conjunción de `project`); cada una cede solo con su augmentación. Solo directorio: aceptación 73.6 → 96.2 % con la cobertura total estancada en 76 %; solo contenido: respuesta de la hetero 76 → 96 % con el directorio en 77 %; ambas con 16 variantes: punta a punta 66.5 → 94.5 %, 1 falso ruteo de 656 (`horse7` frontal → dog en las 5 semillas) y 5 aceptaciones por un ajeno; la sonda de color sólido pasa de 1 a 3 especialistas y el directorio la rutea. 128 imágenes reales más rinden como 4 variantes para la hetero y nada para el directorio. Los latentes van en GPU con las variantes 0–3 oficiales (control 8/8; el encoder en GPU cambia 148 de 409 600 niveles). `evoke_labels` cuesta 17 s por imagen (búsqueda por muestreo de `recall_from_right`): «responde» se decide con una proyección y la evocación completa va sobre 5 por clase. No adoptado como llenado oficial.
- Experimento 14 (23 de septiembre, `run_experiment14_latent_energy.py`, `results/experimento14/`, diseño en `propuesta_exp14_energia_latente.md`): criterio de energía mínima del latente. La fuga de «color sólido» es una región cerca del origen del latente (norma 10–17) donde el encoder colapsa las entradas sin estructura (grises 112–128, desenfoque de radio ≥ 8, contraste ≤ 0.2) y que la envolvente de `horse` contiene (79 de 83 aceptaciones por clase ajena; la instancia real más cercana está a 3 veces la distancia intraclase). τ = 16.6 (mínimo del llenado, margen 10 %) cierra el 94 % de esa fuga (88 % con 16 variantes, donde la comparten dog, horse y cow) y cuesta 5 imágenes reales de 3280, todas vacas oscuras que el directorio ya rechazaba (una de la fase A refuta la letra del criterio pre-registrado). Norma y desviación del latente equivalen; la desviación de píxeles deja pasar el desenfoque; los niveles vivos no separan. No instalado en el pipeline.
- Umbral de energía instalado (23 de septiembre, commit cc37d2e): `latent_energy_threshold()` y `latent_has_energy()` en `stage7_bidirectional.py`, aplicados en la fase A, la fase B y la pestaña de imagen de la app (que muestra ‖z‖ y τ y ofrece una sonda gris). La etapa 7 ahora parte de directorios visuales vacíos: re-correrla sola duplicaba los registros (128 → 256) porque los pickles ya traían la fase A. Verificado: fase A 1 rechazada antes de la memoria, fase B 4 de 656, ruteo 73.6 %, evocación 85.3 %, etapa 8 16/16, app con gris rechazado (‖z‖ 10.7) y apple ruteada (34.2).
- Experimento 15 (23 de septiembre, `run_experiment15_arbiter.py`, `results/experimento15/`, diseño en `propuesta_exp15_arbitro_margen.md`): árbitro por contenido y abstención por margen, evaluados fuera de línea sobre las decisiones de `route_transactive`, refutados. Texto: el árbitro entre los tres mejores del directorio convierte 11.4 aciertos por semilla en errores y corrige 2 (96.1 → 90.6), igual que el contenido solo: el índice compara mejor que el contenido; el margen quita un acierto por cada error a cualquier δ. Fuera de dominio el árbitro iguala a la doble compuerta. Imagen: con Vd=1 nada cambia; con Vd=16 quita el falso de `horse7` y 27 aciertos sin recall, punta a punta igual. El contenido solo rutearía el 93.1 % de las imágenes con cero errores contra 73.6 % del directorio. Nada instalado. De paso se verificó que las 171 × 10 decisiones de T-protocolo de exp11 se reproducen con directorios vacíos por semilla (`form_text_directories` acumula si se reutilizan los agentes).
- Llenado con 16 variantes adoptado (23 de septiembre): `FILL_VARIANTS = 16` y `augment_variants` en `stage5_fill.py` (familia de exp13; las cuatro primeras son las de antes), la fase A registra las variantes de cada percepción (`image_variants_to_latents`), la frescura del llenado comprueba el número de latentes, exp8/exp11/exp13/exp14 leen `FILL_VARIANTS` (la caché de exp11 pasa a `N<corte>_V<variantes>.pkl`). Pipeline 5–8 en CPU: 38 + 1 + 38 + 2 min. Resultado: ruteo 631/656 = 96.2 % (antes 73.6), rechazo 3.5 % (antes 26.4), 2 falsos (`horse7` frontal y 035-135 → dog; dog las contiene, la compuerta no las detiene), evocación 97.4 % (antes 85.3), fase A 99.9 % / 0.8 %, etapa 8 16/16. Exp13 había medido 97.1 % y 1 falso con las variantes nuevas codificadas en GPU; la diferencia es de cuantización (0.036 % de niveles) sobre una conjunción de 64 coordenadas. Los `instance_latents_*.json` (versionados) pasan de 800 a 3200 filas; los jueces 1-NN de exp8/exp9/exp11 que los usan como «instancias reales» verían 25 600 en vez de 6400 si se re-corrieran.
- Experimento 12 (21 de septiembre, `run_experiment12_overlap.py`, `results/experimento12/`): brecha de fidelidad de una EHAM de dos clases contra el solapamiento entre ellas, 28 pares, 5 semillas. La brecha crece con el solapamiento de soportes en etiquetas (ρ 0.45, p 0.017) y el error de clase también (ρ 0.49, p 0.008); no con el solapamiento del latente (ρ −0.07). Las 28 brechas son positivas (mínimo +0.5): no hay pares disjuntos en esta representación (Jaccard 0.57–0.65). Lectura en `veredicto.md`.
- App (21 de septiembre): la fase temprana en vivo usa el protocolo v5 (`SessionAgent` por agente, `TME` de sesión, `register_transaction` con agente de entrada elegido o al azar), la animación muestra solo a entrada y ganador registrando, la pestaña 3 muestra la matriz perspectival y la fase madura de sesión rutea con `route_transactive`. Verificado en el navegador: pear (entrada) → apple con score 568 tras tres consultas. Corregido de paso un import local de `route_transactive` dentro de `main()` que hacía sombra al de módulo.
- Deck mínimo: `hallazgos_exp7_a_exp11.pptx`.

## 8. Pendiente

- Deck externo de Drive (`exp7-10_literatura_corta (2).pptx`): lista viejo/nuevo entregada el 22 de septiembre (envolvente 2.9 a 5.5, descripción 19.3 contra 21.9 y familiaridad, 3.5 saltos); sin aplicar.
