# Experimento de cierre: la MAE como detector con la mejor percepción

**Fecha:** 18 de octubre de 2026
**Estado:** fijada antes de correr, junto con el criterio de cierre aprobado en el chat. Lo que cambie después se declara en el informe como desviación.

## 1. Pregunta

Con la percepción de referencia de PatchCore (WideResNet50-2 de ImageNet) y con una red especializada en buenas contra malas, ¿la MAE detecta fallas como los detectores estándar? ¿Se abstiene ante un tipo de falla nunca visto mejor que la confianza de la red? Este experimento decide si se cierra la línea «solo MAE» y se vuelve a la arquitectura mixta.

## 2. Percepción y datos

- **Percepción:** `wide_resnet50_2-95faca4d.pth` (IMAGENET1K_V1, 138 223 492 bytes, sha256 `95faca4d…50b8` verificado).
- **Datos:** VisA 1cls, imágenes de 224 × 224 del demo industrial. Por pieza: 270 normales de llenado (16 variantes), 180 normales de calibración y test completo de normales.
- **Fallas:** las 100 de cada pieza tienen tipo de falla. Para las partes 2 y 3 se reparten por tipo primario (la primera etiqueta de `image_anno.csv`), con semilla 42.

## 3. Diseño

### Parte 1 · una clase, WideResNet50 congelada

- **Global:** pooling de 2048 → PCA a 64 de la pieza → especialista con 270 × 16 (como G2).
- **Parches:** capas 2 y 3 (la 3 interpolada a 28 × 28), promedio local 3 × 3, 1536 canales, 784 parches → PCA a 64 de la pieza → memoria con los 211 680 parches del llenado. Falla = algún parche no contenido.
- **Detectores:** kNN euclídeo (5 vecinos) y Mahalanobis sobre los mismos 64. En parches: PatchCore sobre los mismos 64 y **PatchCore de referencia sobre los 1536 canales** (sin coreset).
- **Comparación:** cada detector a la aceptación de calibración de la memoria; detección y falsa alarma en test, y AUROC.

### Parte 2 · red especializada (buenas contra malas)

- **Folds:** por pieza, el tipo de falla primario más frecuente queda **fuera** (es la parte 3). El resto de las fallas se reparte en 60 % para entrenar y registrar y 40 % para test, estratificado por tipo.
- **Red:** WideResNet50 de ImageNet con las capas 1 y 2 congeladas (por los 8 GB de la GPU); capas 3 y 4 ajustadas. La salida del pooling va a una capa de 64 (el latente) y a una cabeza de 2 clases. Muestreo balanceado por clase, volteo y rotación de 10°, Adam con lr 1e-4, 12 épocas de 256 muestras. Las normales de entrenamiento son las 270 de llenado.
- **Memoria sobre el latente de 64** (16 variantes por imagen registrada), con la cuantización del rango de lo registrado y margen del 10 %:
  - **solo buenas:** falla = el especialista de buenas no la contiene;
  - **solo malas:** falla = el especialista de malas la contiene;
  - **ambas:** dos especialistas. Si solo uno contiene, decide ese. Si ambos, decide el de mayor puntaje dividido por su número de registros (la calibración B1 de los directorios). Si ninguno, **desconocida** (abstención).
- **Comparaciones sobre el mismo latente:** la cabeza de la red (p(mala)), kNN de dos clases (5 vecinos), y kNN euclídeo y Mahalanobis de una clase (normales).
- **Test con fallas conocidas:** normales de test y el 40 % de las fallas de los tipos entrenados. Detectores y cabeza a la aceptación de calibración de «solo buenas».

### Parte 3 · tipo de falla nunca visto

- **Test:** todas las imágenes del tipo excluido de esa pieza. capsules tiene un solo tipo y no tiene parte 3; en capsules la parte 2 usa ese tipo con el reparto 60/40.
- **Para cada método:**
  - abstención (la memoria «ambas» no la contiene en ninguno);
  - detectada como mala;
  - pasa como buena (falla silenciosa).
- **Abstenedores rivales:** MSP de la cabeza, energía (log-sum-exp de los logits) y distancia kNN de dos clases. Sus umbrales se fijan para que se abstengan en la misma fracción del test conocido que la memoria «ambas».

## 4. Predicciones

- **P1.** Parte 1: PatchCore de 1536 tiene AUROC medio ≥ 0.90 (literatura: alrededor de 0.95). La memoria por parches detecta más que con ResNet18 (45.6 %), pero queda por debajo de PatchCore a igual aceptación en ≥ 8 de 12 piezas. Global: la memoria detecta poco (< 15 %).
- **P2.** Parte 2: la cabeza de la red detecta mucho mejor que en la parte 1 (AUROC ≥ 0.90 en fallas conocidas). La memoria «ambas» y kNN de dos clases quedan cerca de la cabeza, sin superarla. «Solo malas» es el peor esquema, porque deja pasar muchas fallas conocidas.
- **P3.** Parte 3: ante el tipo nuevo, la cabeza deja pasar una parte importante como buena. La memoria «ambas» se abstiene más que MSP y la energía a igual abstención en lo conocido (precedente: exp20, órgano nunca visto, 96.3 contra 75.0 de MSP). Con unas 60 fallas de entrenamiento, el riesgo es que la falla nueva caiga cerca de las buenas y nadie se abstenga.

## 5. Criterio de cierre (aprobado)

- **Se cierra la línea «solo MAE»** si, a igual aceptación de normales, la memoria queda por debajo del mejor detector en al menos 8 de 12 piezas en la parte 1 (global y parches) y en la parte 2. Por debajo significa más de 2 puntos de detección.
- **Queda un nicho** si, en la parte 3, la memoria «ambas» se abstiene ante el tipo nuevo al menos 10 puntos más que MSP y que la energía (media de las piezas), a igual abstención en lo conocido. Ese nicho entraría a la arquitectura mixta como «falla de un tipo nunca visto → revisión humana».

## 6. Entregables

`run_cierre_mae.py` (caché en `results/cierre_mae/cache/`, fuera de git) y `results/cierre_mae/{README.md, resumen.txt, resultados.json}`.
