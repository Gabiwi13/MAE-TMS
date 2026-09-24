# Revisión de prosa al adoptar el llenado con 16 variantes (23 de septiembre de 2026)

Aprobada en el chat. Cifras del pipeline oficial re-corrido en CPU (etapas 5–8, `pipeline_v16_*.log`): fase A 1024 percepciones, acierto 99.9 %, rechazo 0.8 %, una rechazada por energía, registro completo del TME [2048, 2016, 2016, 2016, 2016, 2032, 2048, 2048] (16 registros por percepción), entropía 3.000; fase B 631/656 = 96.2 % de ruteo, 23 rechazos (3.5 %, cuatro por energía), 2 falsos (0.3 %, `horse7-000-000` y `horse7-035-135` → `dog`, que `dog` contiene con score 448 y 303); evocación top-3 113/116 = 97.4 %; etapa 8 16/16; stats de cuantización, umbral, escala de etiquetas y directorios de texto intactos.

## A. `.tex8/secciones/05_resultados.tex`

- Fase A (294–301). Viejo: «precisión del agente visual fue del 100 %, con una tasa de rechazo de solo el 4.2 % (la augmentación del llenado redujo el rechazo de fase A desde el ≈50 % de la versión de tres agentes). Los conteos del directorio visual al final de la fase A fueron [128, 121, 123, 120, 121, 121, 122, 125] con entropía de 3.000 bits». Nuevo: «precisión del 99.9 %, con un rechazo del 0.8 % (4.2 % con el llenado de 4 variantes; ≈50 % en la versión de tres agentes) y una percepción rechazada antes de la memoria por el umbral de energía. Cada percepción aceptada registra sus 16 variantes: el registro completo del TME quedó en [2048, 2016, 2016, 2016, 2016, 2032, 2048, 2048] con entropía de 3.000 bits».
- Fase B (303–310). Viejo: «con lectura B1 y tolerancia ξ = 2 […] 492/656 = 75.0 % […] rechazo del 25.0 % y cero falsos enrutamientos: sobre las imágenes aceptadas, la precisión es del 100 %. El directorio visual nunca se equivoca; cuando no sabe, rechaza.» Nuevo: «con lectura B1 estricta (ξ = 0, directorios perspectivales) […] 631/656 = 96.2 % […] rechazo del 3.5 % (23 imágenes, cuatro de ellas antes de la memoria por el umbral de energía) y dos falsos enrutamientos (0.3 %): sobre las aceptadas, la precisión es del 99.7 %. Los dos falsos son dos vistas del mismo objeto (`horse7`, frontal y 035-135) enviadas a `dog`, que las contiene. Con el llenado de 4 variantes de la versión anterior el ruteo era del 73.6 % (75.0 % con ξ = 2), con un rechazo del 26.4 % y cero falsos: el directorio no se equivocaba porque rechazaba una de cada cuatro imágenes.»
- Justificación de ξ (321–324). Viejo: «El experimento 13 lo confirma: […] el ruteo de test sube del 73.6 % del protocolo perspectival al 97.1 % y la cobertura de punta a punta de 66.5 a 94.5 %, con un falso ruteo de 656». Nuevo: «El experimento 13 lo midió y esta versión lo adopta: con 16 variantes por imagen en el contenido y por percepción en el directorio, el ruteo de test sube del 73.6 % al 96.2 % y la evocación del 85.3 al 97.4 %, con dos falsos de 656».
- Evocación (329). «81/95 = 85.3 %» → «113/116 = 97.4 % (85.3 % con el llenado de 4 variantes)».
- Pie de figura (374–375). «coherentes con el 85.3 % agregado; los fallos se concentran en car, dog y pear» → «coherentes con el 97.4 % agregado».

## B. `.tex8/secciones/06_discusion.tex`

- 13: «con cero falsos enrutamientos» → «con dos falsos enrutamientos en 656, ambos del mismo objeto».
- 130: «cero falsos enrutamientos visuales» → «dos falsos enrutamientos visuales de 656, del mismo objeto hacia la clase vecina».
- Limitación (b), párrafo de exp13 (181–184): «El precio no es cero: un ruteo equivocado de 656 (una vista frontal de horse a dog, en las cinco semillas) y cinco imágenes aceptadas por un especialista ajeno, siempre el par animal que ya confunde al texto.» → «Esta versión adopta las 16 variantes: el ruteo de test queda en 96.2 %, la evocación en 97.4 % y el rechazo en 3.5 %. El precio no es cero: dos ruteos equivocados de 656 (dos vistas de `horse7` a `dog`, que las contiene, así que la doble compuerta no las detiene) y, en el experimento, cinco imágenes aceptadas por un especialista ajeno, siempre el par animal que ya confunde al texto.»
- 208: «sin cambiar el ruteo (73.6 %)» → «sin cambiar el ruteo (medido con el llenado de 4 variantes; con el de 16 rechaza las mismas cuatro)».
- 231: «(75.0 % de enrutamiento, evocación top-3)» → «(96.2 % de enrutamiento, evocación top-3)».

## C. `.tex8/secciones/07_conclusiones.tex`

- 18–21: «enrutó el 75.0 % de las 656 imágenes de prueba con cero falsos enrutamientos (100 % de precisión sobre las aceptadas) y una evocación de dominio del 85.3 %» → «enrutó el 96.2 % de las 656 imágenes de prueba con dos falsos enrutamientos (99.7 % de precisión sobre las aceptadas; ambos, vistas del mismo objeto hacia la clase vecina) y una evocación de dominio del 97.4 %».
- Trabajo futuro, ítem 1: se elimina (las dos mejoras están instaladas); queda en la limitación (b) y en resultados.

## D. `.tex8/secciones/03_arquitectura.tex`, 448–450

«la especificidad permanece intacta en todo el rango (cero falsos enrutamientos)» → «la especificidad permaneció intacta en todo el rango de aquel barrido, hecho con el llenado de 4 variantes».

## E. `README.md`

- Fila 126: «Visual routing with 16 augmentation variants… (exp13) | 97.1 % routing · 94.5 % end-to-end (from 73.6 / 66.5) | 1 false route of 656; not adopted as the official fill» → «Visual routing, official fill since 23 Sep (16 variants + energy threshold) | **96.2%** routing · 3.5% rejection | 2 false routes of 656 (0.3%), both views of `horse7` → `dog`; exp13 measured 97.1 / 1 with GPU-encoded variants».
- Fila 129: «85.3%» → «**97.4%** (85.3% with the 4-variant fill)».

## F. `CONTEXTO_SEP2026.md`

- §7, línea de `models/`: «v5 con umbral de energía (…)» → «v5 con umbral de energía y llenado de 16 variantes (etapas 5–8 re-corridas el 23 de septiembre en CPU: 3200 registros por agente, fase A con 16 registros por percepción; stats, umbral, escala y directorios de texto idénticos a los anteriores; ruteo 96.2 %, 2 falsos, evocación 97.4 %, etapa 8 16/16). `models_v5_umbral/` conserva el v5 con umbral y 4 variantes, `models_v5_perspectival/` el v5 sin umbral, `models_backup_pre_perspectival/` el v4».
- §9, viñeta nueva: «Llenado con 16 variantes adoptado (23 de septiembre): `FILL_VARIANTS = 16` y `augment_variants` en `stage5_fill.py` (familia de exp13; las cuatro primeras son las de antes), la fase A registra las variantes de cada percepción (`image_variants_to_latents`), la frescura del llenado comprueba el número de latentes, exp8/exp11/exp13/exp14 leen `FILL_VARIANTS` (la caché de exp11 pasa a `N<corte>_V<variantes>.pkl`). Pipeline 5–8 en CPU: 38 + 1 + 38 + 2 min. Resultado: ruteo 631/656 = 96.2 % (antes 73.6), rechazo 3.5 % (antes 26.4), 2 falsos (`horse7` frontal y 035-135 → dog; dog las contiene, la compuerta no las detiene), evocación 97.4 % (antes 85.3), fase A 99.9 % / 0.8 %, etapa 8 16/16. Exp13 había medido 97.1 % y 1 falso con las variantes nuevas codificadas en GPU; la diferencia es de cuantización (0.036 % de niveles) sobre una conjunción de 64 coordenadas. Los `instance_latents_*.json` (versionados) pasan de 800 a 3200 filas; los jueces 1-NN de exp8/exp9/exp11 que los usan como «instancias reales» verían 25 600 en vez de 6400 si se re-corrieran.»
- §8: quitar «Decidir si el llenado con 16 variantes…».

## G. `INICIO_NUEVA_SESION.md`

- §4: «v5 con umbral de energía (…)» → como F §7, en corto; y añadir «Los `instance_latents_*.json` tienen 3200 filas por clase (16 variantes)».
- §5: fila «v16 | llenado oficial con 16 variantes: ruteo 73.6 → 96.2 %, evocación 85.3 → 97.4 %, 2 falsos de 656 | stage5_fill.py, stage7_bidirectional.py».
- §6, Exp13: «No adoptado como llenado oficial.» → «Adoptado el 23 de septiembre: el pipeline real da 96.2 % y 2 falsos (las variantes en CPU).»
- §7: comando del pipeline: «python src\stage5_fill.py; python src\stage6_interaction.py; python src\stage7_bidirectional.py; python src\stage8_mature.py   # 5-8 en CPU: 38 + 1 + 38 + 2 min».
- §9: quitar «Decidir si el llenado con 16 variantes…».

## H. `discusion_marco_teorico_directorio.md`, tras la tabla (148)

Añadir: «Con el llenado de 16 variantes y el umbral de energía (23 de septiembre): ruteo 96.2 %, rechazo 3.5 %, 2 errores de 656; evocación 97.4 %; fidelidad 16/16.»
