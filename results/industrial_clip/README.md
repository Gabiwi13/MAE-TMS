# Demo industrial con texto: CLIP como percepción compartida (VisA)

El sistema es heteroasociativo, así que la pista podría ser una oración. Con CLIP, que pone texto e imagen en el mismo espacio, se probaron dos preguntas. ¿Una oración llega al especialista de la pieza como llegaría una imagen? ¿Las descripciones de cómo se ve una falla le dan a la memoria la detección que no tiene registrando solo normales? Diseño, predicciones y criterio fijados antes de correr en [`propuesta_industrial_clip.md`](../../propuesta_industrial_clip.md). Script: [`run_industrial_clip.py`](../../run_industrial_clip.py). Detalle por pieza en `resumen.txt`; filas crudas en `resultados.json`.

**Resultado en una línea:** no, en ninguno de los dos casos. Ninguna de las 1232 oraciones llega a una pieza: el 100 % se rechaza, cruda o con la brecha de modalidad corregida. Una memoria llena solo de oraciones no contiene ninguna imagen. Y el agente de texto anómalo agrega 0.2 puntos de detección. CLIP sin ningún ejemplo de falla sí detecta algo (AUROC 0.667), pero leyendo por similitud, no por contención.

## Montaje

- **Percepción:** CLIP ViT-B/16 de OpenAI, congelado. El peso es `open_clip_model.safetensors` de `timm/vit_base_patch16_clip_224.openai`, 598 516 980 bytes, sha256 `4b8699299b1e8997753c64b052ba32031449d5d853f55a039148560ee02b820f` verificado. Licencia MIT, aunque la tarjeta del modelo de OpenAI desaconseja desplegarlo sin pruebas en el dominio. Está fuera de git en `C:\Users\aq99l\Datasets\CLIP_ViT-B-16_openai`. Se instaló `open_clip_torch` 3.3.0 con `--no-deps`.
- **Datos:** las imágenes, el registro y la calibración del demo industrial (270 normales × 16 variantes y 180 de calibración por pieza; test de 962 normales y 1200 fallas).
- **Oraciones:** los 7 estados normales, los 4 anómalos y las 22 plantillas de la ensamble de prompts de WinCLIP (CPE), con los nombres de pieza de WinCLIP. Eso da 154 oraciones normales y 88 anómalas por nombre. La variante «vocabulario» suma «… {pieza} with {tipo}» con los nombres de tipo de falla de cada pieza.
- **Corrección de la brecha de modalidad:** restar la media del texto y sumar la de las normales registradas.

## T · ¿una oración llega a su pieza?

Es el nivel 1 con el protocolo `Level` sobre la PCA a 64 de los CLS de imagen. Como control, las imágenes de test llegan a su pieza en el 97.2 % de las normales (rechazo 2.8) y en el 81.3 % de las fallas (rechazo 18.7). Con ResNet18 eran 98.4 y 87.5.

| oraciones (154 por cada uno de los 8 nombres) | a su nombre | rechazo | motivo |
|---|---|---|---|
| crudas | 0.0 | **100.0** | contención: mediana de 8 coordenadas fuera del rango de las imágenes |
| brecha corregida | 0.0 | **100.0** | 1218 bajo el umbral de energía, 14 por contención |
| brecha corregida, sin umbral de energía (post hoc) | 0.0 | **100.0** | ningún directorio las contiene |
| *coseno de CLIP contra el prototipo de cada pieza, sin abstención* | *57.7* | — | candle 149/154, cashew y pcb 154/154; fryum 0, macaroni 11, capsule 29 |

Al corregir la brecha, la oración queda cerca de la media de las imágenes. En un espacio centrado en esa media, eso da una norma baja (0.26 de media, contra un umbral de 0.35), y por eso el umbral de energía la frena. Sin el umbral tampoco pasa: los directorios se forman con percepciones de imagen, y la parte de la oración que no explica la media de las imágenes cae fuera de sus envolventes en alguna coordenada.

Ni siquiera el coseno de CLIP, la lectura para la que CLIP fue entrenado, llega a su pieza de forma confiable: 57.7 %.

## Z · detección solo con texto (cero imágenes de falla)

Por pieza hay dos agentes llenos de oraciones (uno normal y otro anómalo). Una imagen es falla si el agente anómalo gana, y es rechazo (alarma) si ninguno la contiene. Media de 12 piezas:

| | memoria | lectura graduada de la memoria (AUROC) | CLIP cero ejemplos, CPE solo con CLS (AUROC) |
|---|---|---|---|
| crudo | ningún agente contiene ninguna imagen (100 % de calibración y de test) | 0.492 | **0.667** |
| brecha corregida | igual: 100 % sin contener | 0.503 | 0.667 |

La memoria no tiene un punto de operación: lo rechaza todo, así que la comparación a igual aceptación no aplica. CPE va de 0.365 (pcb1) a 0.951 (chewinggum). Como referencia de la literatura, WinCLIP con ventanas reporta un AUROC de imagen de 78.1 en VisA sin ejemplos (Jeong et al., CVPR 2023, con otro backbone, ViT-B/16+). No se midió aquí.

## N · normales registradas + agente de texto anómalo

Es el especialista G2 del demo con CLIP (PCA a 64 de la pieza, 270 × 16), más un agente con las oraciones anómalas de la pieza, con la brecha corregida y en la misma cuantización. Falla = el especialista rechaza o el agente de texto acepta. Media de 12 piezas, detección / falsa alarma en test (%); detectores a la aceptación de calibración de cada variante; AUROC entre paréntesis:

| variante | acepta calibración | memoria | el texto acepta (fallas / normales) | kNN euclídeo | Mahalanobis | CPE | CPE + kNN |
|---|---|---|---|---|---|---|---|
| sin texto | 98.4 | 8.6 / 1.6 | — | 26.1 / 1.8 (0.789) | 19.8 / 2.2 (0.755) | 19.8 / 3.0 (0.667) | 20.4 / 3.0 (0.676) |
| + texto CPE | 98.2 | 8.8 / 1.6 | 0.2 / 0.0 | 29.2 / 2.1 | 20.6 / 2.5 | 20.6 / 3.3 | 21.3 / 3.2 |
| + texto CPE y vocabulario de fallas | 92.4 | 10.8 / 9.1 | 2.2 / **7.8** | 48.0 / 9.4 | 38.4 / 9.2 | 33.4 / 9.5 | 34.3 / 9.1 |

La envolvente de 88 oraciones casi no contiene imágenes: el texto CPE suma 0.2 puntos. Con el vocabulario de fallas («candle with chunk of wax missing», …) la envolvente crece, pero contiene más normales (7.8 %) que fallas (2.2 %): las oraciones de falla, ya corregidas, caen donde están las piezas sanas, no donde están las fallas.

Comparado con ResNet18 (G2 del demo), CLIP global no mejora: memoria 8.6 contra 5.8, kNN euclídeo 0.789 contra 0.799, Mahalanobis 0.755 contra 0.817.

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| PT | crudas: ≥ 90 % rechazadas. Corregidas: una parte llega a su pieza. El coseno de CLIP, ≥ 90 % | **Crudas, se cumple** (100 %). **Corregidas, no se cumple**: ninguna llega, y ninguna llega tampoco sin el umbral de energía. **El coseno no llega** (57.7 %) |
| PZ | la memoria solo con texto rechaza casi todo y no hay señal; CPE con AUROC de 0.65 a 0.75, por debajo de WinCLIP | **Se cumple**: 100 % sin contener, graduada 0.49–0.50; CPE 0.667 |
| PN | el especialista detecta poco; kNN y Mahalanobis de 0.75 a 0.85; el texto agrega < 2 puntos; CPE + kNN ≥ kNN | **Se cumple** lo del especialista (8.6), lo de kNN (0.789) y Mahalanobis (0.755) y lo del texto (+0.2). **No se cumple que CPE + kNN ≥ kNN** (0.676 contra 0.789): en mi combinación, el término de referencia ((1 − cos máx)/2) tiene una escala mucho menor que p(anómalo) y el resultado queda dominado por CPE |

**Criterio 1** («una oración llega al especialista como una imagen»): **refutado**, con 100 % de rechazo (el umbral era 50 %).

**Criterio 2** («el texto le da detección a la memoria»): **refutado**. Con CPE sube 0.2 puntos (el umbral era 1). Con vocabulario sube 2.2 puntos, pero con 6 puntos más de rechazo de calibración y 7.5 más de falsas alarmas en test.

## Lectura

1. **La heteroasociación necesita pares, y la contención necesita que la pista caiga dentro de la envolvente.** Una oración nunca registrada junto a imágenes no cae dentro de envolventes hechas con imágenes, aunque CLIP las ponga en el mismo espacio. La brecha de modalidad lo garantiza para el texto crudo. Corregirla con una traslación no basta: lo que queda de la oración después de quitar la media es justo lo que la distingue de una imagen.
2. **Para que una oración rutee, el sistema tiene que registrar oraciones**, como en ETH-80, donde el directorio de etiquetas se formaba con transacciones de texto. Eso funciona como búsqueda por nombre, pero no aporta nada que un índice de texto no haga.
3. **CLIP sin ningún ejemplo de falla detecta algo** (AUROC 0.667, y hasta 0.95 en chewinggum), y lo hace por similitud con descripciones. Es una capacidad real del texto, pero la memoria no puede aprovecharla con su lectura por contención.
4. **La conclusión del demo industrial no cambia:** el sistema sirve como enrutador de piezas con abstención, y la detección de fallas queda para un detector estándar. Con texto, la mejor opción de este experimento es la CPE de CLIP, o WinCLIP completo, sin la memoria.

## Desviaciones y notas

- **Post hoc:** el conteo de motivos de rechazo y el ruteo de las oraciones corregidas sin umbral de energía se agregaron después de ver que el umbral frenaba 1218 de 1232. Al agregarlos, todos los números declarados se reprodujeron exactamente.
- No se reimplementaron las ventanas de WinCLIP. CPE usa solo el CLS. El 78.1 de WinCLIP es la cifra del artículo con otro backbone, no una medición propia.
- Las imágenes se usan a 224 × 224 sin recorte (aspecto deformado), igual que en el demo, sin el recorte central del preprocesamiento de CLIP.
- La lista de estados y plantillas de CPE es mi transcripción de WinCLIP.
- Una sola semilla. Cada punto porcentual por pieza son 1 o 2 imágenes.
