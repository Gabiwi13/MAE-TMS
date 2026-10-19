# Cascada de módulos: malas → buenas partidas → revisión humana

La idea: un módulo de **malas** mira la pieza. Si no la reconoce, pasa al módulo de **buenas**. Si tampoco, va a **revisión humana**. En el experimento de cierre, esa cascada casi nunca mandaba nada a revisión, porque el módulo de buenas reconocía las fallas nuevas. Aquí se parte el módulo de buenas en k especialistas más estrechos, para ver si las fallas nuevas dejan de esconderse en él. Diseño, predicciones y criterio fijados antes de correr en [`propuesta_cascada_modulos.md`](../../propuesta_cascada_modulos.md). Script: [`run_cascada_modulos.py`](../../run_cascada_modulos.py). Detalle en `resumen.txt` y `resultados.json`.

**Resultado en una línea:** partir el módulo de buenas no cambia ninguna decisión. Con k = 1, 2, 4 y 8, las cifras son idénticas, imagen por imagen, en las 12 piezas. La cascada deja pasar en silencio el 31.8 % de las fallas de tipo nuevo, contra 24.1 % de la confianza de la red a igual revisión humana. **Criterio refutado.** La razón no está en la memoria: la red aplasta las piezas buenas sobre casi una línea, y pone sobre esa línea las fallas que no aprendió.

## Montaje

Misma red especializada del cierre (WideResNet50, capas 3 y 4 ajustadas con buenas y malas, tipo primario más frecuente excluido, semilla 42). La reproducción es exacta: la pérdida por época de candle coincide con la del cierre. Módulos sobre el latente de 64 con cuantización común y 16 variantes:
- malas: un especialista;
- buenas: k-means (semilla 42) en k ∈ {1, 2, 4, 8} grupos, un especialista por grupo.

## Resultados (media de 12 piezas; tipo nuevo, 11 piezas)

| k | conocido: detección / falsa alarma | revisión: normales / fallas | tipo nuevo: revisión / mala / **pasa en silencio** |
|---|---|---|---|
| 1, 2, 4 y 8 (idénticos) | 92.5 / 2.9 | 0.0 / 1.9 | 2.6 / 65.6 / **31.8** |
| *cabeza de la red, sin revisión* | *93.0 / 3.4* | — | *— / 73.3 / 26.7* |

**Rivales a la misma revisión humana en lo conocido (1.9 % de las fallas, 0 % de las normales):**

| rival | conocido: detección / falsa alarma | tipo nuevo: pasa en silencio |
|---|---|---|
| MSP de la cabeza | 92.2 / 3.2 | **24.1** |
| energía de la cabeza | 92.2 / 3.1 | **24.1** |
| distancia kNN (dos clases) | 85.4 / 1.1 | 39.1 |

Por pieza, la cascada deja pasar más que MSP en candle (29.2 contra 12.5), pcb1 (92.5 contra 15.1) y pcb3 (47.6 contra 35.7). Deja pasar menos en chewinggum (4.3 contra 8.5), pcb2 (7.7 contra 11.5), pcb4 (3.4 contra 17.2) y pipe_fryum (4.8 contra 0.0 de MSP, pero mandando 19 % a revisión). En macaroni1 y 2, todos dejan pasar de 76 a 80 %.

## Por qué partir no cambia nada (diagnóstico hecho al ver cifras idénticas)

| pieza | niveles por coordenada: buenas completo → subgrupo (k = 8) | fallas nuevas contenidas: buenas completo / algún subgrupo | varianza de las buenas en 3 direcciones |
|---|---|---|---|
| candle | 18.1 → 11.9 | 11 / 11 de 24 | 98.8 % |
| pcb1 | 22.0 → 11.1 | 51 / 51 de 53 | 99.9 % |
| macaroni1 | 18.1 → 11.0 | 23 / 23 de 25 | 98.7 % |

- Partir **sí estrecha** las envolventes, casi a la mitad.
- Pero la red entrenada para «buena contra mala» **colapsa** las piezas buenas: casi toda su variación vive en 1 a 3 direcciones del latente de 64. Los subgrupos de k-means son tramos de esa línea, y su unión cubre lo mismo que el módulo completo.
- La red pone la falla nueva **sobre la misma línea** que las buenas, porque no aprendió nada que las distinga. Siempre cae en algún tramo.
- Así, ninguna imagen cambia de destino entre k = 1 y k = 8, ni en el test conocido ni en el tipo nuevo, ni en la calibración.

El cuello de botella no es el ancho de la envolvente: es lo que la red dejó en el latente. Lo que la red borró, ninguna partición de la memoria lo recupera. Es lo mismo que mostró el experimento 19 en otro contexto: comprimir para clasificar borra el detalle.

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| PC1 | al subir k sube la revisión de fallas nuevas y baja la falla silenciosa | **No se cumple**: nada cambia con k |
| PC2 | con k = 1, parecido a «ambas» del cierre (abstención de alrededor del 3 %) | **Se cumple**: 2.6 % de revisión en lo nuevo. Pasa en silencio 31.8 % (en «ambas», 34.2 %: cuando los dos módulos contienen, la cascada decide «mala») |
| PC3 | con k = 8, cerca de MSP sin ganarle por 10 puntos | **Peor**: 31.8 contra 24.1, la cascada pierde |

**Criterio** («partir los módulos de buenas hace útil la cascada»): **refutado**. Para ningún k la falla silenciosa de la cascada baja de la de MSP.

## Lectura

1. **La lógica de la cascada es correcta, pero depende de la percepción.** «No lo reconozco → al siguiente → si nadie, revisión humana» solo funciona si la percepción conserva lo que distingue a lo desconocido. Una red entrenada para buenas contra malas no lo conserva: borra todo lo que no sirve para separar esas dos clases.
2. **La partición de la memoria estrecha envolventes, pero no crea información.** En el experimento de la memoria única, partir ayudó porque el latente sí guardaba diferencias entre piezas. Aquí el latente no guarda diferencias entre una pieza buena y una falla nueva.
3. **Para detectar lo nunca visto, la memoria tendría que ir sobre una percepción que no colapse:** por ejemplo, los rasgos congelados de WideResNet50 por parches, donde la variación se conserva. Pero ahí la memoria ya perdió como detector (parte 1 del cierre: 26.8 % contra 70.6 % de PatchCore). Las dos percepciones fallan por razones opuestas: la genérica conserva el detalle pero la memoria no lo separa; la especializada separa lo conocido pero borra lo nuevo.

## Notas

- Las cifras idénticas entre k se verificaron directamente (diagnóstico de la tabla anterior); no son un error de código.
- El módulo de malas no se partió (decisión de diseño).
- Una sola semilla. Con 20 a 53 fallas nuevas por pieza, cada punto porcentual por pieza son menos de una imagen.
