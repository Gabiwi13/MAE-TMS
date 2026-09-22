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
| exp2_iota_kappa | 4.72 | 283.1 | ✓ |
| exp3_routing | 0.35 | 20.8 | ✓ |
| exp4_formation | 4.50 | 270.1 | ✓ |
| exp5_entropic | 9.83 | 589.7 | ✓ |
| exp6_capacity | 16.19 | 971.7 | ✓ |
| ablation | 23.36 | 1401.3 | ✓ |
| rejection_probe | 0.17 | 10.3 | ✓ |
| paper_figures | 11.35 | 681.0 | ✓ |

**Pipeline (etapas 1–8): 0.0 min**  ·  **Total (con batería de análisis): 70.5 min**

El entrenamiento del encoder (stage2, 50 épocas sobre 2624 imágenes) domina el costo; el resto del sistema —memorias asociativas, routing, directorios— es de bajo costo porque son operaciones matriciales sobre vectores cuantizados, no entrenamiento por gradiente.