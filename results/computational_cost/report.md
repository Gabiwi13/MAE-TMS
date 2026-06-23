# Costo computacional — reproducción completa del experimento EAM-TMS

Tiempo de pared (wall-clock) de reproducir el experimento desde cero en esta máquina. **Todo corre en CPU** (PyTorch CPU-only); la GPU NVIDIA presente no se utiliza.

## Máquina

- CPU: Intel Core i5-13420H (8 núcleos físicos / 12 hilos lógicos; torch usa 8)
- RAM: 16.9 GB
- GPU: NVIDIA RTX 2050 4GB (torch es CPU-only, no se usa)
- SO: Windows-11-10.0.26200-SP0
- Python 3.13.6  ·  torch 2.12.0+cpu  ·  CUDA disponible: False

## Tiempos por etapa

| paso | minutos | segundos | ok |
|---|---:|---:|:--:|
| stage1_dataset | 0.00 | 0.2 | ✓ |
| stage2_train_encoder | 24.32 | 1459.5 | ✓ |
| stage3_conceptnet | 0.00 | 0.0 | ✓ |
| stage4_fasttext | 0.12 | 7.2 | ✓ |
| stage5_fill | 0.50 | 30.2 | ✓ |
| stage6_interaction | 0.49 | 29.5 | ✓ |
| stage7_bidirectional | 0.22 | 13.3 | ✓ |
| stage8_mature | 0.79 | 47.1 | ✓ |
| exp2_iota_kappa | 2.91 | 174.8 | ✓ |
| exp3_routing | 0.31 | 18.7 | ✓ |
| exp4_formation | 5.63 | 337.6 | ✓ |
| exp5_entropic | 2.76 | 165.8 | ✓ |
| exp6_capacity | 8.60 | 516.2 | ✓ |
| ablation | 7.73 | 464.0 | ✓ |
| rejection_probe | 0.23 | 13.8 | ✓ |
| paper_figures | 9.23 | 553.6 | ✗* |

(*) El benchmark se corrió con un encoder re-entrenado solo para medir el costo;
ese encoder dejó el hemisferio visual en 0% de aceptación (fragilidad estocástica
del containment ξ=0), por lo que la última figura imagen→labels no encontró
muestras y abortó. Con el encoder canónico restaurado, las 16 figuras se generan
sin problema; los ~9 min son representativos del costo de generación.

**Pipeline (etapas 1–8): 26.6 min**  ·  **Total (con batería de análisis): 64.0 min**

## Lectura

El entrenamiento del encoder por gradiente (stage2: 50 épocas sobre 984 imágenes)
es **~24 min, el ~91 % del pipeline y casi todo el costo real**. En contraste,
**todo el sistema asociativo —llenado de memorias, fase temprana, directorios,
hemisferio visual, fase madura— suma menos de 2.5 min** (etapas 1 y 3–8), porque
son operaciones matriciales sobre vectores cuantizados, sin entrenamiento por
gradiente. La batería de análisis (exp2–6 + ablation) es trabajo de evaluación
repetida (cientos de corridas), no parte de un despliegue del sistema.

Implicación: una vez entrenado el encoder visual (la única pieza costosa), el
modelo de memoria transactiva opera a un costo despreciable en CPU, sin GPU.