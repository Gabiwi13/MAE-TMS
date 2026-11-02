# Costo computacional — reproducción completa del experimento EAM-TMS

Tiempo de pared (wall-clock) de reproducir el experimento desde cero en esta máquina.

## Máquina

- CPU: Intel(R) Core(TM) Ultra 7 265HX  ·  20 hilos lógicos  (torch usa 20)
- RAM: 16.6 GB
- GPU: no usada (torch sin CUDA o CUDA_VISIBLE_DEVICES vacío)
- SO: Windows-11-10.0.26100-SP0
- Python 3.13.15  ·  torch 2.12.0+cu130  ·  CUDA disponible: False

## Tiempos por etapa

| paso | minutos | segundos | ok |
|---|---:|---:|:--:|
| stage1_dataset | 0.00 | 0.0 | ✓ |
| stage2_train_encoder | 21.48 | 1288.6 | ✓ |
| stage3_conceptnet | 0.30 | 17.8 | ✓ |
| stage4_fasttext | 0.28 | 16.6 | ✓ |
| stage5_fill | 37.42 | 2245.0 | ✓ |
| stage6_interaction | 0.94 | 56.2 | ✓ |
| stage7_bidirectional | 40.03 | 2401.7 | ✓ |
| stage8_mature | 2.42 | 144.9 | ✓ |

**Pipeline (etapas 1–8): 102.9 min**  ·  **Total (con batería de análisis): 102.9 min**

El entrenamiento del encoder (stage2, 50 épocas sobre 2624 imágenes) domina el costo; el resto del sistema —memorias asociativas, routing, directorios— es de bajo costo porque son operaciones matriciales sobre vectores cuantizados, no entrenamiento por gradiente.