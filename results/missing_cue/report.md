# Caracterizacion distribucional — pista faltante (RS/ST/SS)

30 corridas por metodo y pista, semillas 1000..1029 (random + np.random). Metrica: distancia de retro-proyeccion (backward_distance_from_left), la misma de la tabla del reporte .SMTex. Prototipo = argmax por columna (determinista, 1 valor).

| Pista | Agente | Prototipo | RS (media±σ) | ST (media±σ) | SS (media±σ) | RS d=0 | ST d=0 | SS d=0 |
|---|---|---|---|---|---|---|---|---|
| pear | pear | 9.015 | 7.821 ± 1.672 | 0.356 ± 1.118 | 0.063 ± 0.323 | 1/30 | 27/30 | 28/30 |
| car | car | 7.972 | 4.370 ± 1.446 | 0.029 ± 0.158 | 0.006 ± 0.031 | 0/30 | 29/30 | 29/30 |
| green | apple | 7.000 | 3.999 ± 1.254 | 0.000 ± 0.000 | 0.000 ± 0.000 | 1/30 | 30/30 | 30/30 |
| animal | horse | 7.008 | 5.018 ± 1.016 | 1.170 ± 1.078 | 0.185 ± 0.228 | 0/30 | 13/30 | 13/30 |

Tiempos medios por corrida: random 0.01s, sample_test 1.14s, sample_search 3.34s.