# Propuesta del experimento 27 — RAD-DINO ajustado a los hallazgos de tórax, a 224 px

**Estado:** propuesta; nada corrido ni descargado.

## Pregunta
Exp26 mostró que RAD-DINO congelado mejora tórax (31.5 % balanceado con prototipos, contra 21–24 % del ResNet ajustado) aun con imágenes de 128 px reescaladas, y que un modelo de fundación congelado no alcanza a uno ajustado a la especialidad. ¿Qué pasa si se combinan las dos cosas, conocimiento médico previo **y** ajuste con las etiquetas de tórax, con la resolución adecuada? ¿Y cómo queda la MAE cuando los rasgos están ajustados a la tarea?

## Descarga que hay que aprobar
| archivo | origen | tamaño | licencia | verificación |
|---|---|---|---|---|
| `chestmnist_224.npz` | Zenodo 10.5281/zenodo.10519652 (MedMNIST+ v3.0, el mismo registro de antes) | **3.89 GB** | CC BY 4.0 (de NIH ChestX-ray14) | md5 `45bd33e6f06c3e8cdb481c74a89152aa` |

Va a `data/medmnist/` (fuera de git). Descomprimido ocupa ≈ 5.6 GB, así que se extrae una vez a `.npy` y se lee con mapeo de memoria, para no cargar todo en los 16 GB de RAM. Disco libre: 776 GB.

## Diseño
Mismos 14 dominios de tórax del demo (sin hallazgo más los 13 hallazgos con ≥ 200 casos únicos), mismo registro balanceado (N = 328 por agente, 60 % llenado y 40 % fase A, 16 variantes) y mismo test oficial. Cuatro percepciones, todas a 224 px nativos:

| percepción | qué es |
|---|---|
| A. ResNet18 ajustado (224 px) | la contraparte justa del demo, ahora a 224 |
| B. RAD-DINO congelado (224 px) | aísla el efecto de la resolución frente a exp26 |
| C. **RAD-DINO ajustado** | todo el ViT-B con una capa de 64 y una cabeza de 14; entropía cruzada con muestreo balanceado por clase; AdamW, tasa 1e-5 en el backbone y 1e-3 en la cabeza; 5 épocas de 20 mil imágenes; precisión mixta; semilla 42 |
| D. RAD-DINO con solo la cabeza entrenada (linear probe) | separa cuánto aporta ajustar el backbone |

Validación solo con el split de validación oficial (para Mondrian y para elegir la época, nunca el test). Sobre la capa de 64 de cada percepción se comparan: MAE (`Level`, protocolo oficial), prototipos, kNN, la cabeza entrenada, listas MAE contra Mondrian, y la cobertura de placas con varios hallazgos (exp23).

Como referencia publicada, se reporta también el AUROC por hallazgo de la cabeza sobre el test multi-etiqueta completo, la métrica estándar de ChestX-ray14.

## Predicciones
1. RAD-DINO ajustado (C) es la mejor percepción: balanceado de la cabeza ≥ 40 % en los 14 dominios, por encima de B y de A.
2. La resolución sola (B contra el 31.5 % de exp26) suma pocos puntos; lo que más suma es el ajuste.
3. Con rasgos ajustados la brecha entre MAE y prototipos se achica, como en órganos (exp24: 93 contra 97), pero la MAE sigue por debajo.
4. Mondrian sigue igualando o superando la peor clase de la lista de la MAE.

## Costo
Descarga ≈ 3.9 GB (Zenodo bajó a ≈ 0.6–0.8 MB/s la vez pasada: ≈ 1.5 h). Ajuste fino de RAD-DINO ≈ 1–1.5 h en la GPU de 8 GB; ResNet ≈ 20 min. Rasgos con variantes y evaluación ≈ 40 min. Total ≈ 3–4 h, casi todo en segundo plano.
