# Reanálisis pedido por la lectura de jurado

`reanalisis_jurado.py` lee solo datos versionados (`results/experimento11/raw`, `results/ablation_mdir_bias/ablation_metrics.csv`, `results/experimento14/banco_degenerado.json`, `src/eval_bank.py` y `labels_<clase>.json`) y produce `salida.md`. Se corre desde la raíz con `PYTHONIOENCODING=utf-8 python results/reanalisis_jurado/reanalisis_jurado.py`. Responde a `revision_jurado/jurado_metodologia.md` (M1, M2, M3, M5 y menores) y a M6 de `jurado_wegner.md`; la lectura de cada tabla está en `revision_jurado/reanalisis_nube.md`.

Se escribió en una sesión en la nube y se volvió a correr en esta máquina (numpy 2.4.6, pandas 3.0.3, scipy 1.17.1): las 204 filas de tablas coinciden con las de la nube, salvo el texto de dos encabezados.

Hallazgo que no estaba en el dictamen: en exp11, los directorios perspectivales del protocolo no se reinician entre trabajos de un mismo proceso (ver `results/experimento11_protocolo_corregido/`).
