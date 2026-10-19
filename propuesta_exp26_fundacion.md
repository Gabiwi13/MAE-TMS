# Propuesta del experimento 26 — el sistema médico con modelos de fundación

**Estado:** fijada antes de correr.

## Pregunta
En todos los experimentos médicos el límite de tórax (≈ 21 % balanceado con 14 dominios, para todos los métodos) fue la percepción. ¿Qué cambia si cada nivel percibe con un modelo entrenado en imágenes médicas? ¿El sistema todo con prototipos supera de punta a punta al sistema con MAE?

## Percepción (pesos MIT, Hugging Face)
- **BiomedCLIP** (`microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224`), solo la torre visual: ViT-B/16 a 224 px con su proyección, vector de 512. Se usa para el índice de modalidad y para los especialistas de órganos, piel y mama.
- **RAD-DINO** (`microsoft/rad-dino`): ViT-B/14 a 518 px, token CLS de 768. Se usa para el especialista de tórax. En tórax también se corre BiomedCLIP, para comparar.
- MedMNIST viene a 128 px y se reescala a la entrada de cada modelo (limitación declarada).
- Cada nivel reduce con PCA a 64, ajustada con las originales del llenado de ese nivel.

## Protocolo (igual que la corrida balanceada)
N = máx(328, clase más chica) por agente, 60 % llenado y 40 % fase A, 16 variantes. Test oficial completo. La calibración de Mondrian usa el split de validación.

## Sistemas
- **MAE:** especialistas y directorios MAE (clase `Level`, protocolo oficial, `route_transactive`).
- **Prototipos:** un prototipo medio por agente sobre los mismos 64 rasgos (equivale al directorio de prototipos de exp25 con visibilidad completa, que rutea igual).
- **Referencias:** kNN (k = 5) y regresión logística sobre los mismos 64 rasgos; prototipos sobre el vector completo.
- **Listas:** el conjunto S de la MAE (exp23) contra Mondrian sobre la regresión logística, a igual cobertura total.
- **Lo ajeno:** fondo de ojo en el nivel 1, a igual aceptación de lo propio (MAE, prototipos con coseno, Mahalanobis y MSP).
- **Punta a punta:** nivel 1 correcto y nivel 2 correcto, sobre las mismas imágenes de test.

## Predicciones
1. Tórax mejora con RAD-DINO en todos los métodos (balanceado ≫ 21 %).
2. De punta a punta, el sistema de prototipos supera al de la MAE.
3. La brecha MAE–prototipos se achica con mejores rasgos, pero no desaparece.
4. Mondrian sigue cubriendo mejor la peor clase que la lista de la MAE.

## Comparación contra la percepción anterior
Las mismas métricas de la corrida balanceada (ResNet18 de ImageNet + ajuste por nivel) están en `results/medico_balanceado`, `results/experimento23` y `results/experimento24`.
