# Demo industrial con texto: percepción compartida (CLIP)

**Fecha:** 18 de octubre de 2026
**Estado:** fijada antes de correr. Lo que cambie después se declara en el informe como desviación.

## 1. Pregunta

El sistema es heteroasociativo: la pista puede ser una oración. Con una percepción en la que texto e imagen comparten espacio (CLIP), ¿una oración llega al especialista de la pieza como llegaría una imagen? ¿Y las descripciones de cómo se ve una falla le dan a la memoria la detección que no tiene con solo registrar normales?

## 2. Percepción y datos

CLIP ViT-B/16 de OpenAI (`open_clip_model.safetensors`, MIT, sha256 `4b8699…820f`), congelado. El embedding de imagen es el CLS proyectado (512), y el de texto, el EOT proyectado (512). Los dos se normalizan a norma 1, como en CLIP. Las imágenes son las del demo industrial (VisA 1cls, 224 × 224 sin recorte, en caché), normalizadas con la media y la desviación de CLIP. Mismo registro que el demo: por pieza, 270 normales de llenado × 16 variantes y 180 de fase A, que son la calibración. Test completo: 962 normales y 1200 fallas.

**Oraciones.** Estados y plantillas de la ensamble de prompts de WinCLIP (CPE), en mi transcripción:
- 7 estados normales: «{}», «flawless {}», «perfect {}», «unblemished {}», «{} without flaw», «{} without defect», «{} without damage».
- 4 estados anómalos: «damaged {}», «{} with flaw», «{} with defect», «{} with damage».
- 22 plantillas: «a cropped photo of the {}.», «a photo of a {} for visual inspection.», etc.

Eso da 154 oraciones normales y 88 anómalas por nombre. Los nombres siguen la práctica de WinCLIP: candle, capsule, cashew, chewing gum, fryum, macaroni (macaroni1 y 2), printed circuit board (pcb1–4) y pipe fryum. Variante **con vocabulario de fallas**: además, «a photo of a {pieza} with {tipo}» con los nombres de tipo de `image_anno.csv` de esa pieza. Usa solo el vocabulario, ninguna imagen de falla.

**Brecha de modalidad.** En CLIP, los embeddings de texto y los de imagen ocupan regiones distintas (Liang et al. 2022). La corrección declarada es restar la media de su modalidad y sumar la de la otra: al texto se le resta la media de las oraciones y se le suma la media de las normales registradas. Usa normales sin etiqueta de falla, así que deja de ser cero ejemplos: es el mismo régimen de solo normales del demo.

## 3. Diseño

**T · Oración → pieza.** Nivel 1 con el protocolo de `run_medico_demo.Level`, sobre PCA a 64 de los CLS de las 5400 imágenes de registro de las 12 piezas. Cada una de las 154 oraciones normales de cada nombre se manda como pista latente por `route_transactive`, en dos versiones: cruda y con la brecha corregida. Es correcta si llega a una pieza con ese nombre (pcb1–4 cuentan como una, igual que macaroni1–2). Comparación: coseno de CLIP contra el prototipo (media) de cada pieza, sin abstención.

**Z · Detección con cero imágenes de falla, solo texto.** Por pieza, dos agentes llenados con oraciones: uno con las normales y otro con las anómalas. PCA a 64 y rango de cuantización ajustados sobre las oraciones de las 12 piezas. Una imagen se lee con `recognize_gated_right` en los dos agentes de su pieza: es falla si el agente anómalo gana. Si ninguno la contiene es rechazo, y cuenta como alarma. Se corre crudo y con la brecha corregida. Comparación: CLIP cero ejemplos con CPE solo con CLS, p(anómalo) = softmax(100 · [cos(x, t̄ₙ), cos(x, t̄ₐ)]). No reimplemento las ventanas de WinCLIP. Como referencia de la literatura queda el AUROC de imagen de WinCLIP en VisA, que se cita y no se mide.

**N · Normales registradas + texto.** Igual que G2 del demo, pero con CLIP: PCA a 64 de la pieza sobre su llenado y especialista con 270 × 16. Más un **agente de texto anómalo** con las oraciones anómalas de la pieza, con la brecha corregida y proyectadas al mismo espacio y rango. Regla declarada: falla = el especialista normal rechaza o el agente anómalo acepta. Variantes: sin agente de texto, con CPE y con CPE + vocabulario de fallas. Detectores sobre los mismos latentes: kNN euclídeo (5 vecinos), Mahalanobis (+0.01 I) y CPE + kNN (media de p(anómalo) y (1 − cos máximo a las referencias)/2, imitando WinCLIP+ solo a nivel imagen). Mismo protocolo que el demo: cada detector se fija a la aceptación de calibración de la memoria. Se reportan la detección y la falsa alarma en test, y el AUROC.

## 4. Predicciones

- **PT.** Oraciones crudas: el nivel 1 rechaza casi todas (≥ 90 %), porque por la brecha el texto cae fuera de las envolventes de imagen. Con la brecha corregida, una parte llega a su pieza, pero por debajo del coseno de CLIP (que espero ≥ 90 % al nivel del nombre).
- **PZ.** Con solo texto, la memoria rechaza casi todas las imágenes, crudas o corregidas, porque una envolvente de 154 u 88 oraciones no contiene imágenes. No hay señal (AUROC graduado cerca de 0.5). CLIP cero ejemplos con CPE y solo CLS: AUROC medio de 0.65 a 0.75, por debajo de lo que reporta WinCLIP con ventanas.
- **PN.** El especialista con CLIP global detecta poco, como G2 con ResNet. kNN y Mahalanobis con CLIP: AUROC de 0.75 a 0.85. El agente de texto anómalo agrega menos de 2 puntos de detección, porque su envolvente es estrecha y casi no contiene imágenes. CPE + kNN ≥ kNN.

## 5. Criterio

- «Una oración llega al especialista como una imagen» (la hipótesis del usuario) queda **sostenida** si, con la brecha corregida, ≥ 90 % de lo respondido va a su nombre y el rechazo es ≤ 20 %. Queda **refutada** si el rechazo supera 50 % o el acierto de lo respondido baja de 70 %.
- «El texto le da detección a la memoria» queda **sostenida** si el agente de texto anómalo sube la detección media en ≥ 5 puntos con ≤ 2 puntos más de rechazo de calibración. Queda **refutada** si la sube menos de 1 punto.

## 6. Entregables

`run_industrial_clip.py` (caché en `results/industrial_clip/cache/`, fuera de git; `--report-only`) y `results/industrial_clip/{README.md, resumen.txt, resultados.json}`.
