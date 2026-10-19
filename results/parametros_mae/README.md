# Los parámetros nativos de la MAE (ι y κ) como lectura para detectar fallas

En todos los experimentos de detección anteriores se usó la contención estricta (sí/no) sobre la relación sin podar, y nunca la poda ι ni el peso medio κ. El [modelo formal](../revision_cientifica/modelo_formal.md) sugería que la MAE no perdía por mirar coordenada por coordenada (sobre latentes de PCA, Mahalanobis también es una suma por coordenada), sino por leer en sí/no. Diseño, predicciones y criterio fijados antes de correr en [`propuesta_parametros_mae.md`](../../propuesta_parametros_mae.md). Script: [`run_parametros_mae.py`](../../run_parametros_mae.py).

**Resultado en una línea:** leyendo **la misma relación** en grado (suma de log-frecuencias, H), la MAE pasa de AUROC 0.547 a **0.789** en las 6 piezas de confirmación, **a 0.011 de Mahalanobis (0.800) y por encima de kNN (0.784)**. Con detección al 95 % de aceptación de 47.2 % contra 49.2 %. **Criterio sostenido.** Se repite con WideResNet50 (0.756 contra 0.768). En parches supera a Mahalanobis, pero queda muy por debajo de PatchCore (0.695 contra 0.830). La poda ι no sirve: dispara las falsas alarmas.

## Método

- **Lecturas de la relación R (64 × 32):**
  - C(ι): contención con poda ι ∈ {0, 0.25, 0.5, 1};
  - K: peso medio, el que compara κ;
  - H: Σᵢ log(R[i, qᵢ] + 1).
  En parches, el puntaje de la imagen es el del peor parche.
- **Verificación contra la API oficial:** relación, pesos y bandera de reconocimiento con cada ι, sobre 80 pistas: **0 discrepancias** en los cuatro valores de ι.
- **Diseño y confirmación:** 6 piezas de diseño (candle, cashew, macaroni1, pcb2, pcb3, pcb4) eligieron, sin ver las otras, la lectura graduada (H) y el ι de la contención (ι = 0, porque todo ι > 0 subía la falsa alarma más de 5 puntos). Se midió **una sola vez** en las 6 de confirmación (capsules, chewinggum, fryum, macaroni2, pcb1, pipe_fryum).
- Graduados al **95 % de aceptación de las normales de calibración**; C(ι) en su punto de operación.

## Resultados en confirmación (media de 6 piezas; detección / falsa alarma, AUROC)

| lectura | G2 ResNet18 | G2 WideResNet50 | parches ResNet18 |
|---|---|---|---|
| C(0), contención estricta (la de siempre) | 9.7 / 0.3 (0.547) | 8.0 / 1.0 (0.535) | 47.8 / 15.2 (0.675) |
| C(0.25) | 86.7 / **66.6** (0.741); acepta 30.7 % de la calibración | 85.8 / 64.9 (0.726) | 100 / 100 (0.688) |
| C(0.5) y C(1) | ≈ 99 / ≈ 95–100 | ≈ 99 / ≈ 95–100 | 100 / 100 |
| **K, peso medio (κ)** | 42.7 / 3.9 (0.772) | 35.3 / 5.2 (0.744) | 24.5 / 6.1 (0.684) |
| **H, log-frecuencias** | **47.2 / 4.1 (0.789)** | **39.3 / 4.2 (0.756)** | 28.2 / 6.1 (0.695) |
| Mahalanobis | 49.2 / 5.7 (0.800) | 40.8 / 4.3 (0.768) | 25.3 / 7.4 (0.637) |
| kNN euclídeo / PatchCore | 45.2 / 5.6 (0.784) | 34.3 / 5.5 (0.746) | **58.7 / 7.9 (0.830)** |

En las piezas de diseño el orden es el mismo (G2 ResNet18: H 0.787, Mahalanobis 0.834, kNN 0.813).

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| PM1 | K y H se acercan a Mahalanobis en los globales (a ≤ 0.05), H más que K | **Se cumple**: H a 0.011 (ResNet18) y 0.012 (WRN50); K a 0.028 y 0.024 |
| PM2 | la poda ι sube la detección y la falsa alarma; queda por debajo de K y H a igual aceptación | **Se cumple**: ι = 0.25 detecta 86.7 % con 66.6 % de falsa alarma |
| PM3 | en parches, H y K mejoran sobre la contención en AUROC pero quedan por debajo de PatchCore | **Se cumple en lo esencial**: H 0.695 contra 0.675 de la contención y 0.830 de PatchCore. A igual aceptación, H detecta menos que la contención (28 contra 48 %), que opera con mucha más falsa alarma (15 %) |

**Criterio «los parámetros nativos arreglan la lectura de la MAE»** (en confirmación, G2 ResNet18: AUROC ≥ Mahalanobis − 0.03 y detección ≥ Mahalanobis − 3 puntos): **sostenido** (0.789 contra 0.800; 47.2 contra 49.2).

**Criterio «la poda ι sirve en la contención»:** **no sostenido**. Ningún ι > 0 pasó la condición de falsa alarma en el diseño.

## Lectura

1. **La derrota de la MAE como detector no era del mecanismo de memoria, sino de la lectura.** La relación de conteos ya contiene la información que usa Mahalanobis sobre latentes de PCA: frecuencias por coordenada. Leída en sí/no (contención) se pierde casi todo; leída en grado, se recupera casi todo.
2. **Es una suma de términos por coordenada, igual que Mahalanobis en la base de la PCA**, y por eso rinde casi igual. Es la predicción del modelo formal, confirmada en piezas que no se usaron para elegir.
3. **El techo sigue siendo la percepción global.** Con vectores globales, el mejor método detecta solo el 47–49 % de las fallas a 95 % de aceptación. La MAE iguala a los estándar en ese techo, pero no lo rompe.
4. **Con parches, la MAE no compite con PatchCore**, que mide distancias conjuntas entre parches (0.695 contra 0.830). La lectura por coordenada pierde lo conjunto, como dice el modelo formal (Prop. 1, C1.2). Aun así, supera a una gaussiana común de parches.
5. **La poda ι no sirve para detectar:** quita niveles enteros por coordenada, y una normal con un valor poco frecuente en cualquiera de las 64 coordenadas queda fuera. Es demasiado brusca.

## Qué cambia en el registro de afirmaciones

- La afirmación «la MAE no es competitiva como detector» se **precisa**: con la contención estricta no lo es. Con la lectura graduada de sus propios conteos, **iguala a Mahalanobis y supera a kNN sobre latentes globales**, y **no** alcanza a PatchCore con parches.
- La afirmación «la contención no ve desviaciones conjuntas» se mantiene, y ahora queda claro qué parte de la derrota era eso (parches) y qué parte era la lectura en sí/no (globales).

## Notas

- H es una lectura de los mismos conteos que K, en escala logarítmica; se declaró antes de correr como variante de lectura. K es la lectura nativa exacta del peso que usa κ.
- Las cifras de Mahalanobis y kNN de este experimento difieren algo de las del demo industrial porque aquí todos los puntajes se fijan al 95 % de aceptación de calibración, y allá a la aceptación de la memoria.
- Una sola partición diseño/confirmación (semilla 42), elegida antes de correr.
