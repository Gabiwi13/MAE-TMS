# Caracterizacion distribucional — pista faltante (RS/ST/SS)

30 corridas por metodo y pista, semillas 1000..1029 (random + np.random). Metrica: distancia de retro-proyeccion (backward_distance_from_left), la misma de la tabla del reporte .SMTex. Prototipo = argmax por columna (determinista, 1 valor).

| Pista | Agente | Prototipo | RS (media±σ) | ST (media±σ) | SS (media±σ) | RS d=0 | ST d=0 | SS d=0 |
|---|---|---|---|---|---|---|---|---|
| pear | pear | 9.210 | 8.649 ± 1.671 | 2.472 ± 3.129 | 0.545 ± 1.182 | 1/30 | 18/30 | 24/30 |
| car | car | 8.085 | 7.221 ± 0.665 | 2.176 ± 1.701 | 0.674 ± 0.727 | 0/30 | 9/30 | 9/30 |
| green | apple | 7.826 | 6.833 ± 0.892 | 3.335 ± 1.426 | 0.415 ± 0.353 | 0/30 | 1/30 | 6/30 |
| animal | horse | 7.153 | 6.581 ± 0.889 | 2.556 ± 1.313 | 0.455 ± 0.557 | 0/30 | 4/30 | 7/30 |

Tiempos medios por corrida: random 0.01s, sample_test 0.53s, sample_search 4.22s.