# Experimento 27 — RAD-DINO ajustado a los hallazgos de tórax, a 224 px

Diseño y predicciones en `propuesta_exp27_raddino_ajustado.md` (fijados antes de correr). ChestMNIST a 224 px (Zenodo, CC BY 4.0, md5 verificado; las etiquetas coinciden con la versión de 128 px). Mismos 14 dominios y misma selección de imágenes que la corrida balanceada. Cada percepción entrega un latente de 64. Para las tres entrenadas, la época se eligió por el balanceado en validación. Script `run_experiment27_raddino_ajustado.py`, 70 min; detalle en `resumen.txt` y `resultados.json`.

## Balanceado en test, 14 dominios (%)

| percepción | MAE | prototipos | kNN | logística (64) | AUROC medio de la cabeza (multi-etiqueta) |
|---|---|---|---|---|---|
| A. ResNet18 ajustado, 224 px | 25.4 | 28.0 | 23.0 | 28.5 | 0.698 |
| B. RAD-DINO congelado, 224 px | 12.4 | 30.5 | 20.2 | 30.5 | — |
| **C. RAD-DINO ajustado** | **30.1** | **34.8** | 26.8 | 33.0 | **0.753** |
| D. RAD-DINO + capa de 64 y cabeza entrenadas | 26.6 | 33.6 | 25.0 | 31.4 | 0.732 |
| referencia: ResNet ajustado a 128 px (corrida balanceada) | 21.1 | — | 20.6 (cabeza) | — | — |
| referencia: RAD-DINO congelado reescalado desde 128 px (exp26) | 12.2 | 31.5 | 19.6 | 30.9 | — |

AUROC por hallazgo de C: enfisema 0.91, cardiomegalia 0.86, edema 0.85, neumotórax 0.85, derrame 0.82, masa 0.79, fibrosis 0.76, consolidación 0.72, atelectasia 0.71, engrosamiento pleural 0.70, nódulo 0.66, neumonía 0.60, infiltración 0.54. Como referencia publicada, MedMNIST v2 reporta para ChestMNIST un AUC de 0.773 con ResNet-18 a 224 px, entrenado multi-etiqueta con los 14 hallazgos. El nuestro (0.753) usa una cabeza de 14 dominios de hallazgo único: no es la misma tarea, pero está en el mismo rango.

Validación por época de C: 35.1, 32.9, 32.5, 31.6, 30.5. **El mejor punto es la primera época**: con una tasa de 1e-5 en el backbone, más épocas sobreajustan. D se mantiene estable (33.2–33.4).

**Listas a igual cobertura total** (tamaño / peor clase), MAE contra Mondrian: A 11.47 / 69.5 contra 10.68 / **87.2**; C 9.71 / 50.8 contra 8.41 / **85.5**; D 9.90 / 67.8 contra 8.12 / **83.1**; B 11.45 / **79.6** contra 7.86 / 61.0.

## Predicciones

1. *RAD-DINO ajustado es la mejor percepción, ≥ 40 % balanceado.* **Es la mejor (34.8 con prototipos, AUROC 0.753), pero no llega a 40 %.**
2. *La resolución sola suma poco; lo que más suma es el ajuste.* **La resolución sola no suma nada:** RAD-DINO congelado da 30.5 a 224 px nativos y 31.5 reescalado desde 128. **El ajuste suma poco:** +4.3 sobre el congelado. Casi todo lo aporta ya la cabeza entrenada sobre RAD-DINO congelado (D, 33.6); ajustar el backbone agrega 1.2 más.
3. *Con rasgos ajustados la brecha MAE–prototipos se achica, pero no desaparece.* **Se cumple:** 18.1 puntos con RAD-DINO congelado, 4.7 ajustado, 2.6 con ResNet ajustado. La MAE sigue por debajo.
4. *Mondrian iguala o supera la peor clase de la lista de la MAE.* **Se cumple con los tres rasgos entrenados**, con listas más cortas. Con RAD-DINO congelado la MAE gana la peor clase (79.6 contra 61.0), pero con listas de 11.5 contra 7.9 candidatos.

## Lectura

- **El techo de tórax con estos datos está en ≈ 35 % balanceado sobre 14 dominios (AUROC ≈ 0.75)**, y lo alcanzan todas las percepciones médicas, con diferencias de pocos puntos. Más resolución no ayuda; un modelo radiológico ayuda algo, y ajustarlo, un poco más. El límite parece estar en los datos (ChestMNIST 224 viene de imágenes reducidas desde 1024 px, con etiquetas extraídas de informes) más que en el modelo.
- **La MAE mejora mucho con rasgos ajustados** (12 → 30) y queda cerca de los prototipos (30.1 contra 34.8). Lo que más necesita la MAE es que los rasgos estén ajustados a la tarea; más que eso, nada la acerca.
- Para un sistema médico, la combinación que dan los datos es **RAD-DINO con cabeza entrenada (o ajustado una época) + prototipos + Mondrian**: 34.8 % balanceado, AUROC 0.75 y listas con peor clase del 85 %.
