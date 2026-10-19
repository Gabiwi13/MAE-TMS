# Experimento de cierre: la MAE como detector con la mejor percepción

¿La MAE detecta fallas como los detectores estándar si se le da la percepción de referencia de PatchCore (WideResNet50-2) o una red especializada en buenas contra malas? ¿Se abstiene ante un tipo de falla nunca visto mejor que la red? Diseño, predicciones y criterio de cierre fijados antes de correr en [`propuesta_cierre_mae.md`](../../propuesta_cierre_mae.md). Script: [`run_cierre_mae.py`](../../run_cierre_mae.py). Detalle por pieza en `resumen.txt`; filas en `resultados.json`.

**Resultado en una línea:** como detector por sí sola, la MAE queda cerrada. Con WideResNet50 congelada detecta 5.8 % (global) y 26.8 % (parches), contra 29.9 % de Mahalanobis y 70.6 % de PatchCore, por debajo en 11 y 12 de 12 piezas. Sobre los latentes de una red especializada en buenas contra malas, en cambio, **queda cerca de la cabeza de la red** (90.5 contra 93.0 % de detección, por debajo en solo 6 de 12 piezas). Pero no aporta nada que la red no dé, y ante un tipo de falla nuevo se abstiene menos que la confianza de la red (2.6 contra 6.0 %). **No hay nicho.**

## Montaje

- **Percepción:** `wide_resnet50_2-95faca4d.pth` (ImageNet, torchvision; 138 223 492 bytes; sha256 `95faca4d11227dddf8633dbb5ff6c8a9003c1aa5b8945c73834b8007b10950b8`).
- **Datos:** VisA, 224 × 224, con el registro del demo industrial (270 normales × 16 variantes de llenado y 180 de calibración por pieza).
- **Parte 2:** WideResNet50 ajustada por pieza (capas 3 y 4; capas 1 y 2 congeladas por los 8 GB de la GPU), latente de 64 y cabeza de 2 clases. 12 épocas de 256 muestras balanceadas; la pérdida baja de alrededor de 0.5 a alrededor de 0.01. Se entrena con 270 normales y el 60 % de las fallas de los tipos no excluidos (de 29 a 60 por pieza).
- **Parte 3:** el tipo primario más frecuente de cada pieza se excluye del entrenamiento y del registro. capsules tiene un solo tipo y no tiene parte 3.

## Parte 1 · una clase, WideResNet50 congelada

Media de 12 piezas. Detección / falsa alarma en test (%), cada detector a la aceptación de calibración de la memoria, y AUROC:

| | memoria | lectura graduada | kNN (mismos 64) | Mahalanobis (mismos 64) | PatchCore 1536 (referencia) | memoria por debajo |
|---|---|---|---|---|---|---|
| global (WRN50) | 5.8 / 0.7 | (0.526) | 20.6 / 1.8 (0.788) | **29.9** / 1.2 (**0.811**) | — | 11/12 |
| parches (WRN50) | 26.8 / 10.2 | (0.583) | 62.8 / 10.8 (0.842) | 15.6 / 10.9 (0.550) | **70.6** / 9.0 (**0.886**) | 12/12 |
| *demo, ResNet18, global* | *5.8 / 0.2* | *(0.528)* | *(0.799)* | *29.1 / 1.9 (0.817)* | — | *12/12* |
| *demo, ResNet18, parches* | *45.6 / 14.8* | *(0.665)* | *73.9 / 17.1 (0.864)* | *39.5 / 18.5 (0.651)* | — | *12/12* |

- WideResNet50 no mejora la lectura global (Mahalanobis 0.811 contra 0.817).
- Por parches, PatchCore de 1536 sube a 0.886, pero la **memoria empeora** (26.8 contra 45.6 %). Al comprimir 1536 canales a 64, cada coordenada mezcla más variación y la envolvente cubre más.
- PatchCore de 1536 queda por debajo del alrededor de 0.95 de la literatura en VisA. Va de 0.613 (macaroni2) a 0.993 (pipe_fryum). Aquí las imágenes se aplastan a 224 sin el recorte central y sin el tamaño de entrada del protocolo original.

## Parte 2 · red especializada, fallas de tipos conocidos

Media de 12 piezas. Detección / falsa alarma en test (%):

| método | detección / falsa alarma |
|---|---|
| memoria, solo buenas (no cabe en las buenas → mala) | 69.4 / 0.2 |
| memoria, solo malas (cabe en las malas → mala) | 92.5 / 2.9 |
| **memoria, ambas** (decide el que la contiene; si ninguno, abstención) | **90.5 / 1.8** |
| cabeza de la red (argmax) | **93.0** / 3.4 (AUROC 0.994) |
| kNN de dos clases (5 vecinos) | 87.1 / 1.1 |
| Mahalanobis de una clase (normales) | AUROC 0.979 |

La memoria sobre el latente especializado da un salto respecto de todas las versiones anteriores: de 5.8 % a 90.5 %. La red separa buenas y malas en el latente (la cabeza tiene AUROC 0.994), y ahí la contención por coordenada sí ve la falla. Pero el trabajo lo hace la red: la memoria no supera a la cabeza en ninguna pieza. La iguala en capsules, macaroni1, pcb2, pcb3, pcb4 y pipe_fryum, y queda de 3 a 11 puntos por debajo en las otras 6.

## Parte 3 · tipo de falla nunca visto (11 piezas)

Las imágenes del tipo excluido, distribuidas en abstención, «mala» y «buena» (falla silenciosa), en %. Los rivales se fijan a la abstención de la memoria en lo conocido (0.7 % de media):

| método | abstención | mala | buena (silenciosa) |
|---|---|---|---|
| memoria, ambas | 2.6 | 63.2 | **34.2** |
| MSP de la cabeza | 6.0 | 69.9 | 24.1 |
| energía de la cabeza | 6.0 | 69.9 | 24.1 |
| distancia kNN | 4.8 | 56.2 | 39.1 |
| *memoria, solo buenas: rechaza* | — | *51.5* | — |
| *cabeza a la aceptación de «solo buenas»* | — | *66.8* | — |

- La memoria casi no se abstiene: en el latente especializado sus envolventes son anchas. Las fallas nuevas caen dentro de la envolvente de las malas o de las buenas.
- Deja pasar en silencio más fallas nuevas que la cabeza (34.2 contra 24.1 %).
- Por pieza, la falla nueva es fácil donde se parece a las conocidas (cashew: 100 % detectada por todos). Es casi invisible donde se parece a las sanas (macaroni1 y 2: de 80 a 88 % pasa como buena con todos los métodos). Y en pcb1 la memoria deja pasar el 92.5 % del tipo «melt», mientras la cabeza deja pasar el 15.1 %.

## Predicciones y criterio de cierre

| | predicción | resultado |
|---|---|---|
| P1 | PatchCore 1536 ≥ 0.90; la memoria por parches mejora sobre 45.6 % pero queda por debajo en ≥ 8/12; global < 15 % | **En parte.** PatchCore 0.886 (por debajo de 0.90). La memoria por parches **empeora** (26.8 %). Por debajo en 12/12; global 5.8 % |
| P2 | cabeza AUROC ≥ 0.90; «ambas» y kNN cerca sin superarla; «solo malas», el peor esquema | **Se cumple** lo de la cabeza (0.994) y lo de «ambas» y kNN. **No se cumple** lo de «solo malas»: es el mejor esquema (92.5 %); el peor es «solo buenas» (69.4 %) |
| P3 | la memoria se abstiene ante el tipo nuevo más que MSP y la energía | **No se cumple**: 2.6 contra 6.0 % |

**Criterio de cierre** (fijado antes de correr):

| condición | resultado |
|---|---|
| parte 1, global: memoria por debajo en ≥ 8/12 | **11/12, se cumple** |
| parte 1, parches: memoria por debajo en ≥ 8/12 | **12/12, se cumple** |
| parte 2: memoria por debajo en ≥ 8/12 | **6/12, no se cumple** |
| nicho: la memoria se abstiene ≥ 10 puntos más que MSP y la energía ante el tipo nuevo | **−3.4 puntos, no hay nicho** |

Por la letra del criterio, la línea «solo MAE» **se cierra con percepción genérica** (partes 1 global y por parches) y **no se cierra con percepción especializada** (parte 2). Pero en la parte 2 la memoria no es un detector por sí sola: lee lo que separó la red, y la red sola rinde igual o mejor.

## Veredicto

1. **La MAE como detector propio, sobre una percepción genérica, queda descartada.** Con la mejor percepción congelada disponible (WideResNet50) pierde en 11 y 12 de 12 piezas. Con parches, incluso detecta menos que con ResNet18. No hay más vueltas que darle por el lado de la percepción genérica.
2. **Con una red especializada, la MAE funciona, pero como capa sobre la red.** Llega a 90.5 % porque la red ya separó buenas y malas. No agrega detección ni abstención ante lo nuevo. Esto ya es la arquitectura mixta: la red decide y la MAE, encima, conserva lo que sabe hacer (caja blanca, olvido exacto, sin ejemplares, ruteo).
3. **No hay nicho en fallas nuevas.** El precedente del órgano nunca visto (exp20: 96.3 contra 75.0 de MSP) no se repite aquí. Ahí el latente distinguía órganos, y el órgano ausente caía fuera de todas las envolventes. Aquí la red solo aprendió «buena contra mala», y la falla nueva cae dentro de alguna de las dos.
4. **Se vuelve a la arquitectura mixta**, con el detector como parte neuronal: PatchCore de 1536 (AUROC 0.886) si solo hay piezas sanas, o una red especializada (AUROC 0.994) si hay fallas etiquetadas. La MAE va delante como enrutador con abstención y registro auditable. Hay que tener presente que con la red especializada todos los métodos dejan pasar en silencio entre el 24 y el 39 % de un tipo de falla nunca visto.

## Desviaciones y notas

- **PatchCore de 1536 en float16.** La primera corrida de la parte 1 se detuvo porque la GPU (8 GB, compartida con otro proceso del equipo) desbordaba a la memoria del sistema. El banco de parches se pasó a float16 y cada pieza se guarda al terminar. En candle, el único resultado que alcanzó a dar la primera corrida, el AUROC de PatchCore coincide (0.948).
- La memoria de la parte 2 usa una cuantización común a buenas y malas (el rango de lo registrado con margen del 10 %) y no usa el umbral de energía.
- En la parte 2, cada esquema de memoria tiene su propia aceptación de calibración (de 75 a 100 %), y los detectores se fijan a la de cada esquema.
- Una sola semilla y un solo reparto de fallas. Con 18 a 40 fallas de test por pieza, cada punto porcentual por pieza son menos de una imagen.
