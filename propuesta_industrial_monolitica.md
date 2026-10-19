# Memoria única contra partición en el demo industrial (VisA): propuesta

**Fecha:** 18 de octubre de 2026
**Estado:** fijada antes de correr. Lo que cambie después se declara en el informe como desviación.

## 1. Pregunta

En el demo industrial ([`propuesta_demo_industrial.md`](propuesta_demo_industrial.md), [`results/industrial/README.md`](results/industrial/README.md)) el sistema transactivo (12 especialistas + directorios) rutea bien por pieza y detecta fallas mal. ¿Una sola memoria asociativa entrópica (MAE) con las 12 piezas haría lo mismo, mejor o peor, con el mismo contenido?

## 2. Diseño

Mismos datos, cachés y semilla que el demo: por pieza, 270 normales de llenado × 16 variantes y 180 de fase A (las normales de calibración); test completo (962 normales, 1200 fallas). Q = 32, ξ = 0, mismo umbral de energía del nivel 1.

**Percepción global (principal).** Los latentes del nivel 1 (ResNet18 + PCA a 64 sobre todo el train) con la cuantización del nivel 1 (rango de todo el llenado + 10 %). Es la única percepción global que una sola memoria puede compartir: la G2 del demo usa una PCA distinta por pieza.

- **M (memoria única)**, como exp21: una memoria hetero etiqueta ↔ latente (300 × 16 ↔ 64 × 32) más una homo de todo el llenado para los pesos. Etiqueta de cada pieza: el vector fastText (media de sus palabras) de un término, cuantizado con `quantize_binary(·, 16)`. Términos, fijados aquí: candle, capsules, cashew, chewing gum, snack wheel (fryum), macaroni one, macaroni two, pcb one, pcb two, pcb three, pcb four, snack pipe (pipe_fryum). «fryum» no está en el vocabulario de fastText. Decisión: la etiqueta con más soporte en la proyección (`support_ranking`); rechazo si la proyección tiene una fila vacía o la imagen queda bajo el umbral de energía.
- **Partición, misma percepción**: el protocolo transactivo del demo (`Level.route`), los especialistas sin directorio (`recognize_gated_right` máximo) y, para fallas, el especialista G1 de la pieza (el del nivel 1). También se reporta el especialista G2 (PCA por pieza) y el punta a punta del demo, como el mejor resultado de la partición.
- **Llenado de M.** Todas las inscripciones tienen la forma (etiqueta de la pieza, latente). Como el contador de la relación suma 1 por inscripción y satura en 2¹⁶ − 1, la relación es `min(Σ_{piezas con nivel a en la coordenada i de la etiqueta} conteo_pieza[j, b], 2¹⁶ − 1)`. Se construye así (son 51 840 inscripciones) y **se verifica antes** que coincide celda por celda con `register` oficial sobre un subconjunto. Proyección, pesos y decisión se hacen con el código oficial.

**Percepción por parches (si cabe).** Los mismos parches del demo (capas 2 y 3, 784 por imagen), pero con **una PCA a 64 común a las 12 piezas** (ajustada sobre una muestra de parches del llenado de todas) y una cuantización común (rango del llenado de todas + 10 %), porque una sola memoria necesita un solo espacio. Brazos, todos sin variantes ni umbral de energía (como P del demo), imagen aceptada si todos sus parches lo están:

- **S** especialista por pieza en ese espacio común (homo, solo sus parches);
- **M** hetero con las mismas etiquetas, mismo llenado compuesto que arriba; con 2.5 millones de parches la proyección oficial por parche no cabe en tiempo, así que la aceptación se calcula con una regla equivalente (una fila i tiene soporte si algún nivel a tiene, en las 64 coordenadas, alguna pieza con ese nivel que contenga el valor) y **se verifica** contra `project` oficial en una muestra de parches;
- **U** una sola homo con todos los parches (sin etiquetas).
- Referencia: P del demo (PCA y rango por pieza).

**Detectores a igual aceptación de calibración**, por pieza, sobre los mismos latentes de cada brazo: kNN (global: coseno a 5 vecinos y euclídeo; parches: PatchCore sin coreset) y Mahalanobis por pieza, fijados a la aceptación de calibración de M. Secundario, solo en la percepción global: las versiones «únicas» de los detectores (un banco kNN y una gaussiana con todas las piezas), para ver si juntar el contenido también cuesta a un detector estándar.

## 3. Predicciones

- **(a) Ruteo.** M empata con la partición: acierto en normales dentro de ±2 puntos del protocolo transactivo (98.4 %) y ruteos falsos ≤ 1 %, porque las piezas son separables (exp21: la memoria única iguala a los especialistas con dominios separables). Las fallas se rutean casi como las normales. Si hay confusiones, entre macaroni one/two y entre los pcb (sus términos comparten palabra; en exp21 esto no se cumplió).
- **(b) Detección.** M detecta a lo sumo lo que detecta el especialista de la pieza con la misma cuantización. Es una consecuencia de la construcción: si el especialista de la pieza contiene la imagen, las inscripciones (etiqueta de la pieza, latente) dan soporte en cada fila de la etiqueta de esa pieza, así que la proyección de M no tiene filas vacías. Imagen por imagen: rechazo de M ⊆ rechazo del especialista G1. En parches, además, rechazo de U ⊆ rechazo de M ⊆ rechazo de S. Se espera que M acepte más normales de calibración que el especialista y detecte menos fallas; a igual aceptación, kNN y Mahalanobis siguen por encima.
- **(c) Detectores únicos (secundario).** El kNN con un solo banco detecta casi lo mismo que el kNN por pieza (los vecinos son de la misma pieza); la gaussiana única detecta bastante menos que la gaussiana por pieza.

## 4. Criterio de refutación

- **(a)** refutada si el acierto de M en normales queda más de 5 puntos por debajo del protocolo transactivo o si M manda a otra pieza más del 2 % de las normales. Entre 2 y 5 puntos, empate no sostenido.
- **(b)** refutada si **alguna** imagen de test o de calibración es rechazada por M y aceptada por el especialista G1 de su pieza (o, en parches, rechazada por U y aceptada por M, o por M y aceptada por S), o si la detección media de M supera a la del especialista con la misma cuantización. Una sola imagen basta, porque la predicción es una inclusión, no una tendencia.

## 5. Entregables

`run_industrial_monolitica.py` (lee las cachés del demo sin escribir en ellas; cachés propias en `results/industrial_monolitica/cache/`, fuera de git), `results/industrial_monolitica/{README.md, resumen.txt, resultados.json}`.
