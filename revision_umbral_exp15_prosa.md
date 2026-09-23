# Revisión de prosa tras instalar el umbral de energía y tras el experimento 15 (23 de septiembre de 2026)

Formato viejo / nuevo, aprobada en el chat antes de aplicarse.

## A. `.tex8/secciones/07_conclusiones.tex`, trabajo futuro, ítem 1

**Viejo:** «Ambos están medidos y ninguno instalado; instalarlos exige rehacer la etapa 5, la fase A y las verificaciones.»

**Nuevo:** «El umbral ya está instalado en la codificación de la percepción (etapa 7 y aplicación), sin cambio en las cifras de ruteo; las 16 variantes siguen medidas y no instaladas, porque exigen rehacer la etapa 5, la fase A y las verificaciones.»

## B. `.tex8/secciones/06_discusion.tex`, limitación (b), tras «...no entradas degeneradas.»

**Añadir:** «El umbral está instalado en la codificación de la percepción; en la etapa 7 rechaza una percepción de 1024 en la fase A y cuatro imágenes de 656 en test, sin cambiar el ruteo (73.6\,\%).»

## C. `.tex8/secciones/06_discusion.tex`, limitación (a), al final del párrafo

**Añadir:** «Un árbitro más amplio (que el contenido decida entre los tres mejores candidatos del directorio) empeora el ruteo de texto (96.1 → 90.6\,\% de acierto, experimento 15): el índice calibrado compara mejor que la activación del contenido, y la abstención por margen de score quita un acierto por cada error a cualquier umbral. La doble compuerta se queda como está.»

## D. `CONTEXTO_SEP2026.md`

§7, línea de `models/`, viejo: «- `models/` contiene desde el 21 de septiembre los agentes y TME del protocolo **v5** (directorios perspectivales, re-corrido del 14 de septiembre); […] `models_v5_perspectival/` conserva la copia de los v5. Ambos directorios están excluidos vía `.git/info/exclude`.»

Nuevo: «- `models/` contiene desde el 23 de septiembre los agentes y TME del protocolo **v5 con umbral de energía** (etapa 7 re-corrida en esta laptop con `latent_energy_threshold.json`, versionado): las memorias de contenido son bit a bit las de v4; el registro completo del TME es el v5 salvo un registro (la percepción `cow4-066-027`, rechazada antes de la memoria); los directorios perspectivales cambian porque saltar una percepción desplaza el sorteo del agente de entrada; ruteo de test 73.6 %, evocación 85.3 %, etapa 8 16/16. `models_v5_perspectival/` conserva el v5 sin umbral y `models_backup_pre_perspectival/` el v4; ambos excluidos vía `.git/info/exclude`.»

§9, viñetas nuevas antes de «Experimento 12»:

«- Umbral de energía instalado (23 de septiembre, commit cc37d2e): `latent_energy_threshold()` y `latent_has_energy()` en `stage7_bidirectional.py`, aplicados en la fase A, la fase B y la pestaña de imagen de la app (que muestra ‖z‖ y τ y ofrece una sonda gris). La etapa 7 ahora parte de directorios visuales vacíos: re-correrla sola duplicaba los registros (128 → 256) porque los pickles ya traían la fase A. Verificado: fase A 1 rechazada antes de la memoria, fase B 4 de 656, ruteo 73.6 %, evocación 85.3 %, etapa 8 16/16, app con gris rechazado (‖z‖ 10.7) y apple ruteada (34.2).
- Experimento 15 (23 de septiembre, `run_experiment15_arbiter.py`, `results/experimento15/`, diseño en `propuesta_exp15_arbitro_margen.md`): árbitro por contenido y abstención por margen, evaluados fuera de línea sobre las decisiones de `route_transactive`, refutados. Texto: el árbitro entre los tres mejores del directorio convierte 11.4 aciertos por semilla en errores y corrige 2 (96.1 → 90.6), igual que el contenido solo: el índice compara mejor que el contenido; el margen quita un acierto por cada error a cualquier δ. Fuera de dominio el árbitro iguala a la doble compuerta. Imagen: con Vd=1 nada cambia; con Vd=16 quita el falso de `horse7` y 27 aciertos sin recall, punta a punta igual. El contenido solo rutearía el 93.1 % de las imágenes con cero errores contra 73.6 % del directorio. Nada instalado. De paso se verificó que las 171 × 10 decisiones de T-protocolo de exp11 se reproducen con directorios vacíos por semilla (`form_text_directories` acumula si se reutilizan los agentes).»

§8 Pendiente: quitar «Instalar el criterio de energía mínima…».

## E. `INICIO_NUEVA_SESION.md`

§4, línea de `models/`: misma sustitución que D §7, en corto: «- `models/` tiene desde el 23 de septiembre los 9 pickles del protocolo **v5 con umbral de energía** (etapa 7 re-corrida; contenido bit a bit v4; TME igual al v5 salvo un registro; directorios perspectivales con otro sorteo de entradas; ruteo 73.6 %, etapa 8 16/16). `models/latent_energy_threshold.json` está versionado.»

§5, filas nuevas: `| umbral | energía mínima del latente instalada en etapa 7 y app; cifras sin cambio | stage7_bidirectional.py, app_tme.py |` y `| exp15 | árbitro por contenido y margen, refutados: el índice compara mejor que el contenido | run_experiment15_arbiter.py, results/experimento15/ |`

§6, bloque nuevo tras Exp14: «**Exp15:** un árbitro por contenido entre los tres mejores del directorio empeora el texto (96.1 → 90.6) y el margen quita un acierto por error; en imagen es la doble compuerta. Nada instalado; el índice compara mejor que el contenido.»

§7, comando: `python run_experiment15_arbiter.py   # minutos; --report-only`

§8, trampas: «- **La etapa 7 parte de directorios visuales vacíos** (desde el 23 de septiembre); antes, re-correrla sola duplicaba los registros. `form_text_directories` de exp11 acumula si se reutilizan los agentes entre semillas: vaciar `mem_dir` por semilla (exp15 lo hace).»

§9: quitar «Instalar el criterio de energía mínima…».
