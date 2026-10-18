# Experimento 19 — el sistema completo con una percepción que conserva el detalle

Corre en la copia `MAE-TMS-exp18`. Pregunta: si el encoder conserva lo que varía dentro de la clase (manchas, pelo, color), ¿qué gana el especialista y qué pierde el índice?

## Dos encoders probados

1. **Sin pérdida de clase** (`CLS_WEIGHT=0` en `src/stage2_encoder.py`; la cabeza se entrena sobre el latente desacoplado, como sonda). Misma receta que el oficial: 50 épocas, semilla 42. RMSE 0.082 (oficial 0.110); sonda lineal de clase 94.2 % (cabeza oficial 99.7 %). Respaldo en `models/encoder_sin_clase/`.
   La sonda de atributos (kNN, leave-object-out, balanceada) **refuta** que la pérdida de clase sea lo que borra el detalle. Mejora el color de apple (36.6 → 72.2), pero no las manchas de cow (63.7 → 53.7) ni el pelo de dog (35.0 → 23.3). Lo que las borra es comprimir a 64 dimensiones con reconstrucción MSE. No se corrió el pipeline con este encoder.
2. **Congelado: ResNet18 de ImageNet + PCA a 64** (`build_encoder_resnet_in_pca.py`). Cabe en la clase `Encoder` sin cambiarla: `features` con los pesos de ImageNet y `fc` = PCA ajustada **solo con train** (2624 imágenes, 87.1 % de varianza). Es el que se corrió completo (`run_experiment19_pipeline.sh`, reanudado con `run_experiment19_resume.sh`): etapas 5–8, exp16 (10 pliegues) y exp18 (14 casos, con la lectura tolerante de exp18).

## El índice pierde

| medida | encoder oficial | congelado |
|---|---|---|
| etapa 7, ruteo visual de test (656) | 96.2 % | **80.5 %** |
| rechazo | 3.5 % | 6.9 % |
| falsos ruteos | 0.3 % (2) | **≈12.6 % (83)** |
| fase A (acierto al formar directorios) | 99.9 % | 90.2 % |
| evocación top-3 de dominio | 97.4 % | 83.5 % |
| etapa 8, fidelidad temprana ↔ madura | 16/16 | 16/16 |
| exp16, punta a punta, objeto conocido | 95.5 [95.1, 95.9] | **76.3** [74.7, 77.7] |
| exp16, punta a punta, objeto nuevo | 89.2 [85.1, 93.2] | **60.8** [58.3, 63.1] |
| exp16, falso ruteo, objeto nuevo | 0.1 [0.0, 0.2] | **14.4** [12.3, 16.9] |

Los falsos ruteos de exp16 se concentran entre animales: dog → cow 118, dog → horse 114, horse → cow 104, cow → horse 75; tomato → apple 22. Detalle en `exp16/README.md`.

## El especialista gana poco

exp18 sobre el agente de la clase verdadera; objetos nuevos (leave-object-out completo); acierto balanceado con soporte normalizado. «Propio» es exp18 con el encoder oficial. Fuera de la tabla, porque al sacar un objeto solo queda un valor posible: color de cow, pear y tomato, y patrón de dog.

| caso | azar | propio | congelado r=0 | congelado r=1 | congelado r=2 | conocidos, congelado |
|---|---|---|---|---|---|---|
| color · apple | 50 | 39.6 | 54.3 | **75.6** | 83.6 | 100.0 |
| pelo · dog | 50 | 48.6 | **68.2** | 66.8 | 67.2 | 96.3 |
| patrón · cow | 50 | 55.9 | 55.8 | 61.0 | 64.4 | 86.9 |
| patrón · cup | 50 | 37.4 | 46.5 | 50.3 | 52.5 | 84.6 |
| color · horse | 33 | 39.6 | 36.6 | 40.6 | 45.1 | 63.1 |
| patrón · horse | 50 | 50.0 | 46.0 | 44.9 | 45.6 | 81.2 |
| techo · car | 50 | 42.5 | 33.7 | 33.1 | 39.0 | 68.4 |
| color · cup | 50 | — | 100.0 | 98.1 | 95.5 | 100.0 |
| color · car | 33 | — | 30.9 | 34.6 | 41.2 | 85.8 |
| color · dog | 50 | — | 25.0 | 27.5 | 29.8 | 59.4 |

Promedio de los 7 casos con columna propia: propio 44.8, congelado r = 0 48.7, r = 1 53.2, con azar medio de 47.6. Las ganancias se concentran en el color de apple y el pelo de dog. Los demás quedan en el azar. En objetos conocidos la memoria con el encoder congelado sí acierta (63–100 %).

## Lectura

- **Hay una tensión entre el índice y el especialista.** Los rasgos que conservan color, textura y pelo son justamente los que comparten especies distintas: una vaca café se parece a un caballo café. Con esa percepción, los dominios se tocan y el directorio rutea mal (2 → 83 falsos en test; 0.1 → 14.4 % en objetos nuevos). Lo que necesita el índice (invariancia dentro de la clase) y lo que necesita el especialista (sensibilidad dentro de la clase) se oponen en una sola percepción compartida.
- **A cambio, el especialista gana poco en objetos nuevos.** Unos 5 puntos sobre el azar en promedio con r = 1, y casi todo viene de dos casos. El segundo cuello de botella de exp18 sigue: la lectura por soporte no generaliza como un vecino más cercano aunque el latente traiga la característica.
- **No conviene cambiar el encoder del sistema oficial.** El precio en ruteo es grande y lo que se gana en atributos es poco.
- Para la teoría TMS, lo que sugiere es **dos percepciones**: una invariante para el índice (quién) y otra sensible al detalle para el especialista (cómo es). Esa combinación no se midió. Como la exp18 de esta copia se evalúa sobre el agente correcto, rutear con el encoder oficial y responder el atributo con el congelado daría, en principio, el ruteo oficial con los aciertos de atributo de la tabla de arriba. Queda como hipótesis por probar.

## Archivos

- `build_encoder_resnet_in_pca.py`, `run_experiment19_pipeline.sh`, `run_experiment19_resume.sh`; `src/stage2_encoder.py` con `CLS_WEIGHT`
- `stage*.log`, `exp16.log`, `exp18.log`, `tiempos.txt` (fuera de git los `.log`)
- `exp16/`: README, resumen, figura y filas por pliegue (`latentes.npy` fuera de git)
- `filas_exp18.json`, `resumen_exp18.txt`
- `models/encoder_oficial/`, `models/encoder_sin_clase/`: respaldos de la copia, fuera de git. En la copia, `models/` quedó con el encoder congelado; los archivos versionados de `models/` (estadísticas, umbral, latentes de instancia) no se commitean y en la rama siguen los oficiales.
