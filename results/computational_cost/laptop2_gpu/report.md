# Costo computacional — reproducción completa del experimento EAM-TMS

Tiempo de pared (wall-clock) de reproducir el experimento desde cero en esta máquina.

## Máquina

- CPU: Intel(R) Core(TM) Ultra 7 265HX  ·  20 hilos lógicos  (torch usa 20)
- RAM: 16.6 GB
- GPU: NVIDIA RTX PRO 1000 Blackwell Generation Laptop GPU (9 GB), usada por torch
- SO: Windows-11-10.0.26100-SP0
- Python 3.13.15  ·  torch 2.12.0+cu130  ·  CUDA disponible: True

## Tiempos por etapa

| paso | minutos | segundos | ok |
|---|---:|---:|:--:|
| stage1_dataset | 0.00 | 0.0 | ✓ |
| stage2_train_encoder | 5.05 | 303.2 | ✓ |
| stage3_conceptnet | 0.28 | 16.9 | ✓ |
| stage4_fasttext | 0.27 | 16.0 | ✓ |
| stage5_fill | 10.08 | 604.5 | ✓ |
| stage6_interaction | 0.65 | 38.7 | ✓ |
| stage7_bidirectional | 14.61 | 876.6 | ✓ |
| stage8_mature | 0.92 | 55.1 | ✓ |

**Pipeline (etapas 1–8): 31.9 min**  ·  **Total (con batería de análisis): 31.9 min**

El entrenamiento del encoder (stage2, 50 épocas sobre 2624 imágenes) domina el costo; el resto del sistema —memorias asociativas, routing, directorios— es de bajo costo porque son operaciones matriciales sobre vectores cuantizados, no entrenamiento por gradiente.