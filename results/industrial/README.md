# Demo industrial — detección de fallas en una línea con varias piezas (VisA)

El sistema EAM-TMS en una línea donde pasan 12 piezas distintas: el nivel 1 rutea cada imagen al especialista de su pieza; el especialista, que solo registró piezas sanas, debe rechazar las piezas con falla. El diseño, las predicciones y el criterio se fijaron antes de correr en [`propuesta_demo_industrial.md`](../../propuesta_demo_industrial.md). Script: [`run_industrial_demo.py`](../../run_industrial_demo.py). Detalle por pieza en `resumen.txt`; filas crudas en `resultados.json`.

**Resultado en una línea:** el ruteo por pieza funciona (98.4 % de las normales a su pieza, ningún ruteo falso). La detección de fallas por rechazo no funciona con vectores globales: el especialista acepta el 99 % de las normales y deja pasar el 94 % de las fallas. Con parches detecta algo (45.6 % de fallas contra 14.8 % de falsas alarmas), pero a igual aceptación de normales el kNN por parches estilo PatchCore detecta 73.9 %. La memoria queda por debajo del mejor detector estándar en las 12 piezas, con vectores globales y con parches. Se cumple lo que predijo exp20.

## Datos

VisA (Zou et al., ECCV 2022), Amazon, **CC BY 4.0** (el `LICENSE-DATASET` del tar lo confirma). `VisA_20220922.tar` (1 929 840 640 bytes) se descargó de `amazon-visual-anomaly.s3.us-west-2.amazonaws.com` con aprobación del usuario y se verificó contra el ETag multiparte de S3 (`05c830591a1172938cb714895c9e0cfb-113`, partes de 17 179 870 bytes; VisA no publica checksum). SHA-256: `2eb8690c803ab37de0324772964100169ec8ba1fa3f7e94291c9ca673f40f362`. El tar se extrajo fuera de git en `C:\Users\aq99l\Datasets\VisA`. Partición oficial `split_csv/1cls.csv` (es idéntica a la de GitHub `amazon-science/spot-diff`). Para restaurar: descargar el tar, extraerlo y correr `python run_industrial_demo.py --visa <carpeta>` (las cachés se regeneran en `results/industrial/cache/`, unos 10 min con GPU).

| | por pieza |
|---|---|
| train (solo normales) | 450 a 905 |
| test normales | 50 a 101 (962 en total) |
| test fallas | 100 (1200 en total), con tipo de falla en `image_anno.csv` |

## Diseño (resumen de la propuesta)

- **Registro balanceado.** N = máx(328, pieza más chica) = 450 normales de train por pieza (semilla 42): 270 de llenado (60 %, 16 variantes cada una) y 180 de fase A (40 %). Las 180 de fase A son las **normales de calibración**: el especialista no las registró, porque la fase A solo escribe en los directorios.
- **Nivel 1.** ResNet18 de ImageNet congelado + PCA a 64 ajustada sobre todo el train. Protocolo de `run_medico_demo.Level` sin cambios (Q = 32, umbral de energía, ξ = 0, directorios perspectivales, `route_transactive` desde un no especialista).
- **Nivel 2, falla = rechazo del especialista** (alguna coordenada sin soporte o la imagen bajo el umbral de energía). Tres percepciones: **G1** (los latentes del nivel 1; es el mismo especialista), **G2** (principal: PCA a 64 ajustada sobre el llenado de la pieza) y **P** (parches estilo PatchCore: capas 2 y 3, 784 parches por imagen, PCA a 64 por pieza; una memoria por pieza con los 211 680 parches del llenado; falla = algún parche no contenido).
- **Detectores sobre los mismos latentes**: kNN (similitud coseno media a 5 vecinos; en P, distancia al parche más cercano y máximo sobre la imagen, PatchCore sin coreset) y Mahalanobis estilo PaDiM global (covarianza + 0.01 I).
- **Comparación justa**: cada detector se fija para aceptar la misma fracción de normales de calibración que la memoria, y se mide en test cuánto rechaza de fallas (detección) y de normales (falsa alarma). Se da el AUROC de test de cada detector y de una lectura graduada de la memoria: el número de coordenadas sin soporte (en P, el máximo sobre los parches).

## Nivel 1 — ruteo por pieza

Fase A: 2133 percepciones registradas (todas al agente correcto) y 27 rechazadas.

| test | n | a su pieza | rechazo | a otra pieza | kNN |
|---|---|---|---|---|---|
| normales | 962 | **98.4** | 1.6 | 0.0 | 100.0 |
| fallas | 1200 | 87.5 | 12.5 | 0.0 | 99.9 |

Ninguna imagen se rutea a otra pieza, ni siquiera entre pcb1–pcb4 o entre macaroni1 y macaroni2. El directorio rechaza más fallas que normales (12.5 contra 1.6 %), sobre todo en pipe_fryum (45 de 150 imágenes de test) y chewinggum (32 de 150). Esto pasa porque la envolvente de los directorios sale de las 180 percepciones de fase A y es más estrecha que la del especialista (270 de llenado).

## Nivel 2 — detección de fallas

Media de las 12 piezas. Detección / falsa alarma en test (%) y AUROC de test entre paréntesis. Cada detector está fijado a la aceptación de calibración de la memoria.

| percepción | memoria acepta calibración | memoria (punto de operación) | memoria graduada | kNN | Mahalanobis | kNN euclídeo (post hoc) |
|---|---|---|---|---|---|---|
| G1 · latentes del nivel 1 | 98.8 | 9.9 / 1.0 | (0.545) | 26.2 / 2.1 (0.780) | **32.4** / 1.5 (**0.821**) | 25.8 / 1.4 (0.789) |
| G2 · PCA por pieza | 99.2 | 5.8 / 0.2 | (0.528) | 3.9 / 1.1 (0.569) | **29.1** / 1.9 (**0.817**) | 25.7 / 1.9 (0.799) |
| P · parches | 84.4 | 45.6 / 14.8 | (0.665) | **73.9** / 17.1 (**0.864**) | 39.5 / 18.5 (0.651) | — |

Por pieza, G2 (detección de la memoria / del mejor detector declarado, AUROC de Mahalanobis): candle 0 / 41 (0.875), capsules 4 / 7 (0.641), cashew 6 / 43 (0.857), chewinggum 16 / 65 (0.969), fryum 2 / 43 (0.850), macaroni1 0 / 4 (0.725), macaroni2 1 / 10 (0.550), pcb1 5 / 30 (0.891), pcb2 1 / 22 (0.821), pcb3 2 / 34 (0.790), pcb4 2 / 16 (0.939), pipe_fryum 30 / 43 (0.899).

Por pieza, P (detección de la memoria / de PatchCore, AUROC de PatchCore): candle 55 / 76 (0.914), capsules 28 / 46 (0.642), cashew 58 / 72 (0.927), chewinggum 79 / 95 (0.966), fryum 51 / 70 (0.867), macaroni1 31 / 78 (0.855), macaroni2 16 / 28 (0.660), pcb1 50 / 74 (0.863), pcb2 35 / 83 (0.881), pcb3 35 / 68 (0.832), pcb4 46 / 98 (0.981), pipe_fryum 63 / 99 (0.980).

**Punta a punta** (nivel 1 y después el especialista G2 de la pieza a la que se ruteó): de las normales, 98.3 % pasan como normales y 1.7 % dan alarma. De las fallas, 12.5 % dan alarma en el nivel 1, 2.2 % en el nivel 2 y **85.2 % pasan como normales**.

### Por qué el especialista global no rechaza

Con 270 normales × 16 variantes, cada coordenada de la envolvente cubre casi todo el rango que toman las piezas sanas. Una falla local (una mancha, una grieta, un componente que falta) mueve poco el vector global, y ninguna de sus 64 coordenadas sale de la envolvente. Por eso la lectura graduada casi no cambia nada: el número de coordenadas sin soporte es 0 en casi todas las imágenes, sanas o con falla, y su AUROC queda en 0.53–0.55. Mahalanobis sí detecta lo mismo en los mismos 64 números (AUROC 0.82), porque mide combinaciones de coordenadas y distancias dentro del rango, y la contención por coordenada no ve ninguna de las dos cosas.

Con parches, la regla «algún parche fuera» se vuelve sensible a lo local. Pero la envolvente de cada coordenada cubre en promedio 27.8 de los 32 niveles, y la memoria pierde contra el vecino más cercano por la misma razón: el vecino más cercano mide distancia en el espacio conjunto y la memoria mide pertenencia coordenada por coordenada.

## Tipos de falla como dominios (análisis secundario, n chico)

Por pieza, cada tipo de falla con etiqueta única y al menos 10 imágenes es un dominio. 60 % de llenado (16 variantes, percepción G2) y 40 % de test, asignación por `recognize_gated_right` máximo, sin directorio. capsules tiene un solo tipo y queda fuera. Acierto balanceado (%):

| pieza | tipos (azar) | test | memoria balanceado | memoria rechazo | kNN balanceado |
|---|---|---|---|---|---|
| candle | 5 (20.0) | 25 | 2.9 | 60.0 | 36.4 |
| cashew | 5 (20.0) | 27 | 5.0 | 74.1 | 44.3 |
| chewinggum | 3 (33.3) | 18 | 27.6 | 50.0 | 70.8 |
| fryum | 4 (25.0) | 24 | 9.4 | 41.7 | 38.6 |
| macaroni1 | 5 (20.0) | 30 | 14.2 | 56.7 | 40.0 |
| macaroni2 | 4 (25.0) | 26 | 9.1 | 53.8 | 43.5 |
| pcb1 | 4 (25.0) | 34 | 31.9 | 26.5 | 57.5 |
| pcb2 | 4 (25.0) | 34 | 27.9 | 26.5 | 40.4 |
| pcb3 | 4 (25.0) | 36 | 30.7 | 11.1 | 36.1 |
| pcb4 | 2 (50.0) | 11 | 14.3 | 63.6 | 87.5 |
| pipe_fryum | 6 (16.7) | 35 | 9.7 | 65.7 | 46.7 |

Con 6 a 29 imágenes de llenado por tipo, las envolventes son chicas y rechazan entre 11 y 74 % del test. La memoria queda por encima del azar solo en pcb1, pcb2 y pcb3, y por poco; kNN queda por encima del azar en las 11 piezas.

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| P1 | nivel 1 ≥ 95 % de lo respondido en normales; las fallas se rutean casi igual; confusiones entre pcb y entre macaroni | **Se cumple en normales** (100 % de lo respondido, 98.4 % de acierto). **En parte en fallas**: 87.5 % a su pieza, y el 12.5 % restante se rechaza, no se confunde. **Las confusiones no aparecen** (0 ruteos falsos) |
| P2 | en G1 y G2, kNN y Mahalanobis detectan igual o más que la memoria; G2 detecta más que G1; AUROC de 0.75 a 0.90; la lectura graduada, por debajo | **Se cumple** la comparación (la memoria queda por debajo en 9 de 12 piezas con G1 y en 12 de 12 con G2) y el rango de Mahalanobis (0.82). **No se cumple que G2 detecte más que G1** (5.8 contra 9.9). **El kNN coseno de G2 queda fuera del rango** (0.569), por diseño: ver desviaciones |
| P3 | PatchCore tiene el AUROC más alto (≥ 0.85); la memoria por parches satura y rechaza poco | **Se cumple lo de PatchCore** (0.864). **La saturación no se cumple tal cual**: la regla «algún parche fuera» rechaza 45.6 % de las fallas y 15.6 % de las normales de calibración. Aun así queda 28 puntos por debajo de PatchCore a igual aceptación |
| P4 | tipos de falla: la memoria por encima del azar en pcb, con mucho rechazo; empate o peor que kNN | **Peor que lo predicho**: apenas por encima del azar en pcb1–pcb3, por debajo en las demás piezas, y peor que kNN en las 11 |

**Criterio 1** («la memoria detecta como los detectores estándar», a igual aceptación de calibración, ±2 puntos en al menos 8 de 12 piezas): **refutado** con G2 (por debajo en 12/12) y con P (12/12); con G1, 9/12 por debajo.

**Criterio 2** («el rechazo por cobertura detecta algo», detección − falsa alarma de la memoria ≥ 20 puntos de media): **sostenido con parches** (30.8 puntos). **Con G2, 5.6 puntos**: entre el umbral de refutación (< 5) y el de sostén, así que queda sin decidir, en el borde bajo. Con G1, 8.9 puntos.

## Lectura

1. **El nivel transactivo hace su trabajo**: con registro balanceado y piezas visualmente distintas, el directorio rutea sin errores y rechaza poco. Es el caso fácil para la contención (dominios separables, exp21).
2. **La detección de fallas por rechazo es detección por cobertura**, y una falla local no saca de la cobertura a un vector global. Es el mismo resultado de exp20 (la memoria rechaza lo cercano solo cuando cae fuera de la envolvente de alguna coordenada), aquí en su versión más difícil: lo ajeno es casi idéntico a lo propio.
3. **Los parches ayudan a la memoria, pero no la vuelven competitiva**: la regla es binaria por coordenada, y el vecino más cercano y Mahalanobis aprovechan la estructura conjunta de las coordenadas. A igual aceptación, la distancia entre PatchCore y la memoria (28 puntos) es mayor que la que había con vectores globales entre Mahalanobis y la memoria (23 puntos).
4. Para un demo industrial, el sistema sirve como **enrutador de piezas con abstención**, no como detector de fallas. Un detector estándar por pieza detrás del ruteo (PatchCore, AUROC 0.86 con ResNet18 y sin coreset) es la combinación que estos números sostienen.

## Desviaciones y notas

- `src/stage5_fill._scaled` tenía el tamaño fijo en 128 px. Ahora usa el tamaño de la imagen; a 128 px da el mismo resultado. Las traslaciones de 6 px de `augment_variants` pesan menos a 224 px que a 128.
- **kNN euclídeo, post hoc.** En G2, la PCA está centrada en la media de la pieza, y sobre datos centrados el coseno mide la dirección desde la media, no la distancia (en pcb1 el AUROC queda en 0.33, por debajo del azar). Se agregó después de ver los resultados un kNN con distancia euclídea media a 5 vecinos (AUROC 0.799). El criterio usa solo los detectores declarados, y agregar el euclídeo no lo cambia (el mejor detector sigue por encima en 12/12). Frente al euclídeo solo, la memoria lo iguala o lo supera en capsules (4 contra 3) y macaroni2 (1 contra 1). Al agregarlo, la corrida reprodujo exactamente todos los números declarados.
- Las imágenes se llevan a 224 × 224 sin recorte, así que se deforma el aspecto (las originales van de 1274 × 1176 a 1562 × 960).
- Una sola semilla (42) y un solo corte de registro. El test tiene de 150 a 201 imágenes por pieza, así que cada punto porcentual por pieza equivale a 1 o 2 imágenes.
