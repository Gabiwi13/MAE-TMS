# Costo computacional — reproducción completa del experimento EAM-TMS

Tiempo de pared (wall-clock) de reproducir el experimento desde cero en esta máquina. **Todo corre en CPU** (PyTorch CPU-only); la GPU NVIDIA presente no se utiliza.

## Máquina

- CPU: Intel64 Family 6 Model 186 Stepping 2, GenuineIntel  ·  12 hilos lógicos  (torch usa 8)
- RAM: 16.9 GB
- GPU: NVIDIA RTX 2050 4GB (torch es CPU-only, no se usa)
- SO: Windows-11-10.0.26200-SP0
- Python 3.13.6  ·  torch 2.12.0+cpu  ·  CUDA disponible: False

## Tiempos por etapa

| paso | minutos | segundos | ok |
|---|---:|---:|:--:|
| stage1_dataset | 0.01 | 0.3 | ✓ |
| stage2_train_encoder | 79.91 | 4794.3 | ✓ |
| stage3_conceptnet | 0.46 | 27.4 | ✓ |
| stage4_fasttext | 0.43 | 25.6 | ✓ |
| stage5_fill | 15.73 | 943.6 | ✓ |
| stage6_interaction | 1.00 | 60.2 | ✓ |
| stage7_bidirectional | 33.99 | 2039.1 | ✓ |
| stage8_mature | 1.86 | 111.9 | ✓ |
| exp2_iota_kappa | 8.24 | 494.6 | ✓ |
| exp3_routing | 0.59 | 35.2 | ✓ |
| exp4_formation | 8.44 | 506.6 | ✓ |
| exp5_entropic | 17.38 | 1042.6 | ✓ |
| exp6_capacity | 27.12 | 1627.4 | ✓ |
| ablation | 39.20 | 2351.7 | ✗ |
| rejection_probe | 0.26 | 15.4 | ✓ |
| paper_figures | 58.64 | 3518.4 | ✓ |

**Pipeline (etapas 1–8): 133.5 min**  ·  **Total (con batería de análisis): 293.4 min**

El entrenamiento del encoder (stage2, 50 épocas sobre 984 imágenes) domina el costo; el resto del sistema —memorias asociativas, routing, directorios— es de bajo costo porque son operaciones matriciales sobre vectores cuantizados, no entrenamiento por gradiente.