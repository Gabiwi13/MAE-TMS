# Costo computacional: laptop 1 (julio de 2026) contra laptop 2 (22 de septiembre de 2026)

Misma medición (`run_cost_benchmark.py`: tiempo de pared por etapa, entrenamiento del encoder forzado, batería de análisis en subprocesos), misma RAM nominal (16 GB). La laptop 2 se midió en un worktree aislado del repo (`../MAE-TMS-bench`), con los mismos datos y el mismo código, sin tocar los modelos oficiales. Archivos: `cost.json` y `report.md` (laptop 1), `laptop2_cpu/`, `laptop2_gpu/` y `laptop2_cpu_bateria/`.

| | laptop 1 | laptop 2 |
|---|---|---|
| CPU | Intel Core i5 de 13.ª generación, 12 hilos lógicos (torch usa 8) | Intel Core Ultra 7 265HX, 20 hilos lógicos (torch usa 20) |
| RAM | 16.9 GB | 16.6 GB |
| GPU | NVIDIA RTX 2050 4 GB, no usada (torch CPU-only) | NVIDIA RTX PRO 1000 8 GB, usada solo en la corrida «GPU» |
| torch | 2.12.0+cpu | 2.12.0+cu130 |
| Python | 3.13.6 | 3.13.15 |

## Pipeline (etapas 1–8)

| etapa | laptop 1, CPU | laptop 2, CPU | laptop 2, GPU | ganancia CPU | ganancia GPU |
|---|---:|---:|---:|---:|---:|
| 1 dataset (ya descargado) | 0.0 | 0.0 | 0.0 | — | — |
| 2 encoder ResNet18, 50 épocas, 2624 imágenes | 79.9 | 22.3 | 5.1 | 3.6× | 15.8× |
| 3 ConceptNet (caché) | 0.46 | 0.27 | 0.28 | 1.7× | 1.6× |
| 4 fastText | 0.43 | 0.26 | 0.27 | 1.7× | 1.6× |
| 5 llenado de memorias (8 agentes, instancias + augmentación) | 15.7 | 10.3 | 10.1 | 1.5× | 1.6× |
| 6 fase temprana | 1.00 | 0.61 | 0.65 | 1.6× | 1.5× |
| 7 hemisferio visual (1024 interacciones + test) | 34.0 | 15.8 | 14.6 | 2.2× | 2.3× |
| 8 fase madura | 1.86 | 1.05 | 0.92 | 1.8× | 2.0× |
| **pipeline** | **133.5** | **50.6** | **31.9** | **2.6×** | **4.2×** |

Minutos. «Ganancia» = tiempo de la laptop 1 entre el de la laptop 2.

## Batería de análisis (CPU en las dos)

| paso | laptop 1 | laptop 2 | ganancia |
|---|---:|---:|---:|
| exp2 iota/kappa | 8.24 | 4.72 | 1.7× |
| exp3 ruteo | 0.59 | 0.35 | 1.7× |
| exp4 formación | 8.44 | 4.50 | 1.9× |
| exp5 entrópico | 17.38 | 9.83 | 1.8× |
| exp6 capacidad | 27.12 | 16.19 | 1.7× |
| ablación | 39.20 (falló, rc=1) | 23.35 | 1.7× (no comparable del todo) |
| sonda de rechazo | 0.26 | 0.17 | 1.5× |
| figuras del reporte | 58.64 | 11.35 | 5.2× |
| **batería** | **159.9** | **70.5** | **2.3×** |
| **total (pipeline CPU + batería)** | **293.4** | **121.1** | **2.4×** |

Con el pipeline en GPU y la batería en CPU el total baja a 102.4 min (2.9×).

## Lectura

- **La GPU solo cuenta en el encoder.** Es la única parte con gradientes: 22.3 → 5.1 min. Las etapas de memoria (llenado, directorios, ruteo, hemisferio visual, fase madura) corren en numpy dentro de `hetero_lib` y no usan la GPU: sus tiempos en las corridas CPU y GPU de la laptop 2 coinciden dentro del ruido (10.3 / 10.1, 15.8 / 14.6). En el hemisferio visual el encoder solo codifica; la GPU le ahorra un minuto.
- **La ganancia de las memorias viene de la CPU sola, y es de 1.5 a 2.3×.** Es menor que la del encoder porque el registro de una hetero es secuencial (un `register` reconstruye la relación de 86 MB, ~80 ms) y no aprovecha los 20 hilos; la diferencia entre las dos máquinas es de núcleo, no de paralelismo.
- **Aun con el encoder 16× más rápido, el llenado y el hemisferio visual dominan el pipeline en la laptop 2** (25 de 32 min): la parte cara del sistema pasa a ser la memoria, no el entrenamiento. La frase del reporte «el entrenamiento del encoder concentra el costo» describe la laptop 1 y una configuración sin GPU.
- **Salvedades.** (1) La ablación falló en la laptop 1 (rc=1 a los 39 min), así que su tiempo es de una corrida incompleta. (2) Las figuras del reporte tardaron 58.6 min en la laptop 1 y 11.4 aquí; la diferencia (5.2×) es mayor que la de todo lo demás y no se explica solo por la CPU; no se investigó. (3) La batería con la GPU visible falla en `run_experiment5.py`, `run_experiment6.py` y `generate_paper_figures.py`: cargan el encoder en cuda y le pasan tensores de CPU (`Input type (torch.FloatTensor) and weight type (torch.cuda.FloatTensor)`); esos scripts solo se habían corrido sin GPU. Por eso la batería se midió con `CUDA_VISIBLE_DEVICES=-1`, igual que en la laptop 1. (4) torch usó 8 hilos en la laptop 1 y 20 en la 2; el encoder en CPU es la única etapa a la que eso le importa. (5) Los modelos que entrena el benchmark en el worktree no son los oficiales; solo se usan para medir tiempo.

## Cómo se corrió

```powershell
git worktree add --detach ..\MAE-TMS-bench HEAD          # copia aislada; copiar data/ a mano
cd ..\MAE-TMS-bench
python run_cost_benchmark.py --pipeline-only --tag laptop2_gpu
$env:CUDA_VISIBLE_DEVICES="-1"                            # "" en PowerShell borra la variable, no la vacía
python run_cost_benchmark.py --pipeline-only --tag laptop2_cpu
python run_cost_benchmark.py --battery-only  --tag laptop2_cpu_bateria
```
