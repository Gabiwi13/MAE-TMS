# Caracterizacion distribucional — pista faltante (RS/ST/SS)

30 corridas por metodo y pista, semillas 1000..1029 (random + np.random). Metrica: distancia de retro-proyeccion (backward_distance_from_left), la misma de la tabla del reporte .SMTex. Prototipo = argmax por columna (determinista, 1 valor).

| Pista | Agente | Prototipo | RS (media±σ) | ST (media±σ) | SS (media±σ) | RS d=0 | ST d=0 | SS d=0 |
|---|---|---|---|---|---|---|---|---|
| pear | pear | 6.389 | 6.017 ± 0.734 | 1.875 ± 2.070 | 0.353 ± 0.878 | 0/30 | 16/30 | 25/30 |
| car | car | 6.587 | 5.772 ± 0.556 | 1.942 ± 1.329 | 0.789 ± 0.817 | 0/30 | 7/30 | 7/30 |
| green | apple | 6.722 | 5.801 ± 0.846 | 2.640 ± 1.122 | 0.469 ± 0.477 | 0/30 | 1/30 | 3/30 |
| animal | horse | 5.915 | 5.378 ± 0.826 | 1.926 ± 0.962 | 0.366 ± 0.452 | 0/30 | 3/30 | 8/30 |

Tiempos medios por corrida: random 0.01s, sample_test 0.45s, sample_search 3.96s.