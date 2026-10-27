# Memoria única contra partición en el demo industrial (VisA)

¿Una sola memoria asociativa entrópica (MAE) con las 12 piezas haría lo mismo que la arquitectura transactiva (12 especialistas + directorios), con el mismo contenido? Diseño, predicciones y criterio fijados antes de correr en [`propuesta_industrial_monolitica.md`](../../propuesta_industrial_monolitica.md). Script: [`run_industrial_monolitica.py`](../../run_industrial_monolitica.py). Detalle por pieza en `resumen.txt`; filas crudas en `resultados.json`. Base: el demo industrial ([`results/industrial/README.md`](../industrial/README.md)), con sus mismas cachés, semilla y corte (270 normales × 16 variantes de llenado y 180 de calibración por pieza; test completo: 962 normales y 1200 fallas).

**Resultado en una línea:** en ruteo, la memoria única empata con la partición. En detección, nunca rechaza una imagen que el especialista de su pieza acepte. Con vectores globales rechaza exactamente lo mismo que el especialista (las 4322 imágenes coinciden). Con parches detecta menos (14.6 contra 39.3 % de las fallas). Las dos predicciones se cumplen. Juntar las piezas no le quita nada al ruteo y le quita detección a la memoria, que ya era el punto débil.

## Qué es M

Una memoria hetero etiqueta ↔ latente (300 × 16 ↔ 64 × 32) y una homo de todo el llenado para los pesos, como en exp21. La etiqueta de cada pieza es el vector fastText de un término (media de sus palabras), cuantizado a 16 niveles: candle, capsules, cashew, chewing gum, snack wheel (fryum), macaroni one, macaroni two, pcb one … pcb four, snack pipe (pipe_fryum). Las 12 etiquetas cuantizadas son distintas. M decide por el soporte de cada etiqueta en la proyección y rechaza si la proyección tiene una fila vacía o si la imagen queda bajo el umbral de energía del nivel 1.

La percepción es la del nivel 1: ResNet18 + PCA a 64 de todo el train, cuantización del nivel 1. Es la única percepción global que una memoria única puede compartir. La G2 del demo usa una PCA distinta por pieza.

**Verificaciones del código**, hechas antes de usar los resultados:
- La relación de M se construye sumando los conteos de cada pieza bajo el nivel de su etiqueta (el contador satura en 2¹⁶ − 1). Sobre 192 inscripciones (1 imagen × 16 variantes por pieza) coincide celda por celda con `register` oficial, en la hetero y en la homo.
- En parches, con 2.5 millones de parches, no hay tiempo para proyectar cada uno con el código oficial. La aceptación se calcula con una regla equivalente (en la fila i, algún nivel a tiene, en las 64 coordenadas, alguna pieza con ese nivel que contenga el valor). En 2400 parches de test de las 12 piezas, 317 de ellos rechazados, el número de filas vacías coincide exactamente con el de `project` oficial. La homo única (U) también coincide con `recog_weights` oficial.

## Ruteo por pieza (todo el test)

| | normales: acierto / rechazo / a otra pieza | fallas: acierto / rechazo / a otra pieza |
|---|---|---|
| **M (memoria única)** | **99.1** / 0.9 / 0.0 | **90.1** / 9.9 / 0.0 |
| T-protocolo (directorios, `route_transactive`) | 98.4 / 1.6 / 0.0 | 87.5 / 12.5 / 0.0 |
| T-especialistas (sin directorio) | 99.1 / 0.9 / 0.0 | 90.1 / 9.9 / 0.0 |
| kNN (k = 5) | 100.0 / 0.0 / 0.0 | 99.9 / 0.0 / 0.1 |

M no manda ninguna imagen a otra pieza, ni entre macaroni one y two ni entre los cuatro pcb, aunque sus términos comparten palabra. Queda 0.7 puntos por encima del protocolo transactivo en normales porque no pasa por los directorios: la envolvente de los directorios sale de las 180 percepciones de fase A y es más estrecha que la de los especialistas, así que rechaza más (también en fallas: 12.5 contra 9.9). M decide igual que los especialistas sin directorio en todas las piezas.

## Detección de fallas, percepción global

**Inclusión:** de 4322 imágenes (test y calibración), ninguna es rechazada por M y aceptada por el especialista G1 de su pieza. Tampoco hay imágenes en el otro sentido: M y G1 aceptan y rechazan exactamente las mismas 4322 (155 rechazadas por ambos). Con estos latentes, la unión de piezas que comparten nivel de etiqueta nunca cubre lo que no cubre la pieza propia.

Media de 12 piezas. Detección / falsa alarma en test (%) y AUROC entre paréntesis. Detectores fijados a la aceptación de calibración de la memoria (98.8 %, igual para M y G1):

| | detección / falsa alarma |
|---|---|
| **M** (punto de operación) | 9.9 / 1.0 (graduada 0.545) |
| especialista G1 (partición) | 9.9 / 1.0 (graduada 0.545) |
| kNN coseno por pieza | 26.2 / 2.1 (0.780) |
| kNN euclídeo por pieza | 25.8 / 1.4 (0.789) |
| Mahalanobis por pieza | **32.4** / 1.5 (**0.821**) |
| kNN coseno, un solo banco | 26.2 / 2.1 (0.780) |
| kNN euclídeo, un solo banco | 25.8 / 1.4 (0.789) |
| Mahalanobis, una sola gaussiana | 14.1 / 1.9 (0.721) |

Por pieza, M queda por debajo del mejor detector en 10 de 12 piezas (en capsules por 1 punto, 3 contra 4); en macaroni1 empata (1 contra 1) y en macaroni2 lo supera (3 contra 1). Son los mismos números de G1 en el demo.

**Punta a punta** (alarma = rechazo en cualquier etapa):

| | normales: alarma / pasa | fallas: alarma / pasa |
|---|---|---|
| M | 0.9 / 99.1 | 9.9 / 90.1 |
| partición: directorios + especialista G1 | 1.8 / 98.2 | 13.9 / 86.1 |
| partición: directorios + especialista G2 (PCA por pieza) | 1.7 / 98.3 | 14.8 / 85.2 |

La partición da 4 a 5 puntos más de alarmas en fallas, pero el doble de falsas alarmas. Casi todo lo que agrega viene de que los directorios rechazan más, no de que detecten mejor: el especialista G2 suma 0.9 puntos sobre G1.

## Detección de fallas, parches

Mismos parches del demo (capas 2 y 3, 784 por imagen), con **una PCA y una cuantización comunes** a las 12 piezas, porque una memoria única necesita un solo espacio. S = especialista por pieza en ese espacio; M = hetero con etiquetas; U = una sola homo con todos los parches. Imagen aceptada si todos sus parches lo están. Media de 12 piezas; detectores en el mismo espacio, por pieza, fijados a la aceptación de calibración de cada brazo.

| brazo | acepta calibración | memoria: detección / falsa alarma (AUROC graduada) | PatchCore a esa aceptación | Mahalanobis a esa aceptación |
|---|---|---|---|---|
| S (partición) | 88.5 | **39.3** / 11.2 (0.645) | 73.6 / 12.9 (0.875) | 49.0 / 14.5 (0.756) |
| M (única con etiquetas) | 95.9 | 14.6 / 3.4 (0.556) | 57.0 / 5.1 | 34.9 / 5.4 |
| U (única sin etiquetas) | 99.9 | 2.1 / 0.4 (0.508) | 34.3 / 0.6 | 22.2 / 0.7 |
| *P del demo (PCA y rango por pieza)* | 84.4 | 45.6 / 14.8 (0.665) | 73.9 / 17.1 (0.864) | 39.5 / 18.5 (0.651) |

**Inclusión:** 0 imágenes rechazadas por M y aceptadas por S; 0 rechazadas por U y aceptadas por M. Rechazo de U ⊆ rechazo de M ⊆ rechazo de S, como se predijo.

Aquí juntar sí cuesta. La envolvente de U cubre en promedio 28.0 de 32 niveles por coordenada, contra 19.5 de cada especialista. Una pieza con falla casi siempre cae dentro de lo que alguna otra pieza sana ocupa. M recupera parte de la selectividad gracias a las etiquetas: una fila solo tiene soporte si un mismo nivel de etiqueta cubre las 64 coordenadas. Pero las piezas que comparten nivel en una fila de la etiqueta se suman. M detecta 14.6 % de las fallas, menos de la mitad que S. Por pieza, M queda por debajo de S en las 12 y por debajo de PatchCore a su misma aceptación en las 12 (detección − falsa alarma: M 11.2 puntos, S 28.1).

La PCA común le cuesta poco a la partición: S detecta 39.3 / 11.2 contra 45.6 / 14.8 de P con PCA por pieza, a una aceptación algo mayor (88.5 contra 84.4).

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| (a) | ruteo: M dentro de ±2 puntos del protocolo transactivo en normales y ≤ 1 % de ruteos falsos; confusiones, si hay, entre macaroni y entre pcb | **Se cumple**: 99.1 contra 98.4 (+0.7), 0 ruteos falsos. **Las confusiones no aparecen** (como en exp21, la palabra compartida no confunde) |
| (b) | detección: rechazo de M ⊆ rechazo del especialista de la pieza con la misma cuantización; en parches U ⊆ M ⊆ S; M detecta menos y los detectores siguen por encima | **Se cumple sin excepciones**: 0 violaciones en 4322 imágenes (global) y en todas las de parches. En global la inclusión es igualdad (M = G1 en todas las imágenes, 9.9 % de detección). En parches M detecta 14.6 contra 39.3 de S y 2.1 de U |
| (c) | detectores únicos: el kNN con un solo banco ≈ kNN por pieza; la gaussiana única detecta menos | **Se cumple**: kNN idéntico en las 12 piezas (26.2 / 2.1); gaussiana única 14.1 contra 32.4 |

**Criterio (a)**: no refutada (diferencia +0.7 puntos, 0 % a otra pieza). **Criterio (b)**: no refutada. Una sola imagen rechazada por M y aceptada por el especialista la habría refutado, y no hubo ninguna.

## Lectura

1. **Para el ruteo da igual.** Con piezas separables, la memoria única hace lo mismo que los especialistas sin directorio, imagen por imagen. Es el resultado de exp21 con dominios separables. El protocolo transactivo rechaza un poco más porque el directorio tiene una envolvente más estrecha que la de los especialistas, no porque rutee mejor.
2. **Para la detección, la memoria única no puede ganar, y con parches pierde.** La inclusión es una propiedad de la construcción y se verificó en todas las imágenes. Con vectores globales no se nota, porque el especialista ya casi no rechazaba (9.9 %) y la unión de piezas no cubre nada nuevo. Con parches, donde el especialista sí detecta algo, la memoria única pierde casi dos tercios (39.3 → 14.6) y la homo sin etiquetas lo pierde casi todo (2.1).
3. **La partición tiene una ventaja en detección: estrecha la envolvente.** Lo que cuenta para rechazar es el contenido de cada especialista, no cómo se elige entre ellos. Un detector estándar no tiene ese problema en kNN (el vecino más cercano ya es de la misma pieza) y sí en Mahalanobis (una gaussiana para todo pierde 18 puntos). Aun así, la conclusión del demo no cambia: ni la partición ni la memoria única llegan a PatchCore o Mahalanobis por pieza.

## Desviaciones y notas

- La regla de parches de M y la construcción por conteos de M y U no son el `register`/`project` oficial. Son equivalentes, y se verificaron contra el código oficial en las muestras indicadas antes de leer los resultados.
- Los términos se fijaron en la propuesta. «fryum» no está en el vocabulario de fastText, así que se usó «snack wheel» y «snack pipe».
- Los detectores de parches usan el espacio común (PCA común), así que no son exactamente los del demo. PatchCore por pieza queda casi igual (AUROC 0.875 contra 0.864 en el demo).
- Una sola semilla (42) y un solo corte. El test tiene de 150 a 201 imágenes por pieza, así que cada punto porcentual por pieza son 1 o 2 imágenes.
- Las cachés del demo se leyeron del worktree `industrial-demo-4132e4` sin escribir en él. Las cachés propias (PCA de parches común y parches proyectados, 1.5 GB) están en `results/industrial_monolitica/cache/`, fuera de git. Se regeneran en unos 4 minutos con GPU.

- **Umbral de energía (nota del 26 oct 2026).** El umbral de norma del latente se aplica antes de las memorias, pero aquí no actúa: las 4322 consultas lo pasan (campo `energia` de `resultados.json`).
- **M no recuerda** (nota del 26 oct 2026). M rutea con `support_ranking` (de exp17): entre las 12 etiquetas de pieza, elige la de mayor probabilidad media en la proyección. Es una lectura de conjunto cerrado; no se ejecuta `recall_from_right`. Los especialistas también eligen entre las 12 piezas, así que la comparación es entre dos lecturas cerradas.
