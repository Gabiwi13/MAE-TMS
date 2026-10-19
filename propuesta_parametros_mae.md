# Los parámetros nativos de la MAE (ι y κ) como lectura para detectar fallas

**Fecha:** 19 de octubre de 2026
**Estado:** fijada antes de correr. Es la última prueba de la MAE como detector. Lo que cambie después se declara en el informe como desviación.

## 1. Pregunta

En todos los experimentos de detección se usó la contención estricta sobre la relación sin podar (ι = 0) y nunca el peso medio (κ). El modelo formal sugiere que la derrota contra Mahalanobis no se debe a que la MAE mire coordenada por coordenada: sobre latentes de PCA, Mahalanobis también es una suma de términos por coordenada (Σ zᵢ²/λᵢ). Se debería a que la MAE lee en **sí/no**. ¿Las lecturas que ya ofrecen sus parámetros (poda ι y peso medio κ) la hacen competitiva?

## 2. Lecturas (todas salen de la relación R ∈ ℕ^{64×32} de la memoria)

- **C(ι):** contención con la relación podada por ι (en cada coordenada se anulan las celdas con conteo < ι × el conteo medio de las celdas no nulas, como `_update_iota_relation`). ι ∈ {0, 0.25, 0.5, 1.0}. Punto de operación propio (sí/no) y puntaje graduado: menos el número de coordenadas fuera.
- **K (κ como puntaje):** peso medio w(z) = (1/64) Σᵢ R[i, qᵢ(z)], el que compara κ con la media de la memoria. Puntaje continuo.
- **H (frecuencias en logaritmo):** Σᵢ log(R[i, qᵢ(z)] + 1). Es la misma información que K, sumada en escala logarítmica, como el detector por histogramas HBOS (Goldstein y Dengel, 2012). Se declara como una variante de lectura de los mismos conteos.
- En **parches**, el puntaje de la imagen es el del peor parche (mínimo de K o de H; contención: algún parche fuera).

**Verificación previa:** la poda y las lecturas se calculan con numpy sobre la relación. Se comparan con la API oficial (memoria construida con `iota = ι` y su `recog_weights`) en una muestra, y deben coincidir exactamente.

## 3. Percepciones y comparaciones (cachés existentes)

- **G2 ResNet18:** global, PCA a 64 por pieza (como el demo industrial).
- **G2 WideResNet50:** global, PCA a 64 por pieza (como la parte 1 del cierre).
- **Parches ResNet18:** 784 parches, PCA a 64 por pieza (como el demo industrial).
- **Rivales sobre los mismos latentes:** Mahalanobis (gaussiana + 0.01 I; en parches, el peor parche), kNN euclídeo (5 vecinos; en parches, PatchCore).

**Registro:** 270 normales de llenado (16 variantes en global; sin variantes en parches). **Calibración:** 180 normales. **Test:** normales y fallas.

**Medidas:** AUROC en test, y detección y falsa alarma a una aceptación común del **95 % de las normales de calibración** para todos los puntajes graduados. La contención C(ι) se reporta en su propio punto de operación.

## 4. Diseño y confirmación (contra el jardín de caminos)

Las 12 piezas se reparten al azar (semilla 42) en **6 de diseño y 6 de confirmación**. Con las de diseño, y solo con ellas, se elige:
- el ι de la contención (la mayor detección con un aumento de falsa alarma ≤ 5 puntos respecto de ι = 0);
- la mejor lectura graduada entre K y H (mayor AUROC medio en G2 ResNet18).

Esa elección se congela y se mide **una sola vez** en las 6 piezas de confirmación.

## 5. Predicciones

- **PM1.** K y H mejoran mucho el AUROC frente a la contención (alrededor de 0.53) y se acercan a Mahalanobis en los latentes globales de PCA (H más que K, por la escala logarítmica): a ≤ 0.05 de Mahalanobis.
- **PM2.** La poda ι sube la detección de la contención, pero también la falsa alarma. A igual aceptación, queda por debajo de K y H.
- **PM3.** En parches, H y K mejoran sobre la contención, pero quedan por debajo de PatchCore, que mide distancias conjuntas entre parches.

## 6. Criterio (sobre las 6 piezas de confirmación)

- **«Los parámetros nativos arreglan la lectura de la MAE»:** sostenido si la lectura graduada elegida alcanza en G2 ResNet18 un AUROC medio ≥ el de Mahalanobis − 0.03, **y** una detección al 95 % de aceptación ≥ la de Mahalanobis − 3 puntos. Refutado si el AUROC queda > 0.10 por debajo de Mahalanobis.
- **«La poda ι sirve en la contención»:** sostenido si el ι elegido sube la detección ≥ 10 puntos con ≤ 5 puntos más de falsa alarma respecto de ι = 0.

## 7. Entregables

`run_parametros_mae.py` (cachés en `results/parametros_mae/cache/`, fuera de git) y `results/parametros_mae/{README.md, resumen.txt, resultados.json}`.
