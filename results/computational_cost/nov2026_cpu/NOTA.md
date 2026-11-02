# Condiciones de la medición del 1 nov 2026

- Corrida con `run_cost_benchmark.py` en una copia aparte del repositorio (`MAE-TMS-costo`), desde cero: etapas 1 a 8, de 18:53 a 20:37.
- Solo CPU: Intel Core Ultra 7 265HX, 20 hilos lógicos (torch usa 20), 16.6 GB de RAM. La laptop tiene una GPU NVIDIA, oculta con `CUDA_VISIBLE_DEVICES=-1` (en Windows una variable vacía no la oculta: una primera corrida así entrenó en la GPU y se descartó).
- Llenado con 16 variantes por imagen (`FILL_VARIANTS = 16`): 3200 registros por módulo. La medición del 22 sep (50.6 min) fue con 4 variantes; por eso el llenado pasa de 10.3 a 37.4 min.
- Durante las etapas 5 y 7 corrían en la misma máquina procesos ligeros (lectura de archivos y búsquedas). El llenado tardó entre 4:05 y 4:37 min por módulo en siete de los ocho; `car` tardó 5:18, al arrancar esos procesos.
- Al partir de cero, la corrida recalculó `models/latent_global_stats.json` con las 16 variantes; los modelos oficiales usan el archivo del 5 de julio, calculado con 4. No afecta los tiempos.
- La última frase de `report.md` («El entrenamiento del encoder … domina el costo») es un texto fijo del script y no vale para esta medición: el llenado (37.4 min) y el hemisferio visual (40.0 min) tardan más que el encoder (21.5 min).
