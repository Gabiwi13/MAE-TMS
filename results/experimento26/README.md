# Experimento 26 — el sistema médico con modelos de fundación

Diseño y predicciones en `propuesta_exp26_fundacion.md` (fijados antes de correr). Misma selección de imágenes que la corrida balanceada; cambia la percepción. BiomedCLIP (torre visual, 512) para la modalidad, los órganos, la piel y la mama; RAD-DINO (CLS, 768) para tórax, y también BiomedCLIP en tórax para comparar. Los modelos se usan **congelados**, con PCA a 64 por nivel. MedMNIST viene a 128 px y se reescala a 224 y 518. Script `run_experiment26_fundacion.py`, 111 min; detalle en `resumen.txt` y `resultados.json`.

**Diferencia clave con la corrida balanceada:** allá el nivel 1 usaba ResNet18 de ImageNet congelado y **los encoders del nivel 2 eran ResNet18 ajustados con las etiquetas de cada especialidad**. Aquí todo está congelado.

## Balanceado por nivel (%)

| nivel | MAE | prototipos (64) | kNN | logística | ResNet ajustado, corrida balanceada (MAE / cabeza) |
|---|---|---|---|---|---|
| modalidad (4) | 94.2 (rechazo 6.8) | **100.0** | 100.0 | 100.0 | 92.3 / — (ResNet congelado) |
| tórax (14), RAD-DINO | 12.2 | **31.5** | 19.6 | 30.9 | 21.1 / 20.6 |
| tórax (14), BiomedCLIP | 8.0 | 21.3 | 15.6 | 22.8 | — |
| órganos (11) | 43.2 | 61.9 | 81.2 | 83.7 | **92.9 / 96.5** |
| piel (7) | 17.7 (acierto 63.4: casi todo «nevo») | 50.8 | 57.4 | 62.4 | 62.6 / **74.1** |
| mama (2) | 46.9 | 75.1 | 78.6 | 78.1 | 81.1 / **84.9** |

**Punta a punta** (nivel 1 y nivel 2 correctos, acierto): tórax MAE 10.5 contra prototipos **26.6**; órganos 40.0 contra **65.3**; piel 61.3 contra 49.7 (el acierto de la MAE viene de responder casi siempre la clase mayoritaria; su balanceado es 17.7 contra 50.8); mama 67.9 contra **72.4**.

**Listas a igual cobertura total** (tamaño / peor clase), MAE contra Mondrian: órganos 6.17 / **96.7** contra 6.19 / 88.5; tórax con RAD-DINO 11.15 / 72.9 contra **7.70 / 71.2**; piel 5.58 / 69.0 contra 5.40 / **92.4**; mama 1.77 / 83.3 contra 1.88 / **99.1**.

**Fondo de ojo**, a igual aceptación de lo propio (93.2 %): MAE rechaza 99.9 % y prototipos 100 %. Con BiomedCLIP lo ajeno queda lejos y ambos lo separan.

## Predicciones

1. *Tórax mejora con RAD-DINO en todos los métodos.* **Se cumple solo para los métodos por distancia:** prototipos 31.5 y logística 30.9 contra ≈ 21 antes (+10 puntos). La MAE empeora (12.2 contra 21.1). La mejora existe, pero no es «muy por encima».
2. *De punta a punta, prototipos supera a la MAE.* **Se cumple** en tórax, órganos y mama. En piel la MAE tiene más acierto bruto solo porque colapsa a la clase mayoritaria.
3. *La brecha MAE–prototipos se achica con mejores rasgos.* **Se refuta:** se agranda (órganos 43 contra 62; tórax 12 contra 32). Con rasgos genéricos congelados, las envolventes por coordenada se solapan y la contención decide mal, como en exp24.
4. *Mondrian sigue cubriendo mejor la peor clase.* **Mixto:** gana en piel y mama, empata en tórax con listas más cortas, y pierde en órganos (88.5 contra 96.7 a igual tamaño).

## Lectura

- **Un modelo de fundación congelado no reemplaza a un encoder ajustado a la especialidad:** en órganos, piel y mama, el ResNet ajustado de la corrida balanceada gana (órganos 96.5 contra 83.7 con la mejor cabeza). La excepción es tórax, donde RAD-DINO congelado ya supera al ResNet ajustado (31 contra 21).
- **La MAE es la más sensible a la calidad de los rasgos:** con rasgos genéricos cae mucho más que los métodos por distancia. Es lo mismo que exp24.
- **Para medicina** lo que sigue es **ajustar** los modelos de fundación por especialidad (por ejemplo, RAD-DINO con las etiquetas de tórax) y usar más resolución (MedMNIST a 224 px). Con estos rasgos de 128 px reescalados el techo de tórax sigue bajo para todos.
