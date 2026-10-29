# Experimento 12 — la ventaja de partir contra el solapamiento entre dominios

28 pares de clases. Para cada par, una EHAM única con las dos clases (M2, N=200, mismo llenado que exp11) responde a las consultas reservadas de esas clases; semillas [42, 43, 44, 45, 46], 3 sorteos. Referencia: el especialista (T-oráculo de exp11) y la EHAM de ocho clases (M8 de exp11) sobre las mismas consultas y semillas. Solapamiento: Jaccard medio por coordenada de los soportes de las dos clases, en el lado de las etiquetas (homo L, 300×16) y en el latente (homo R, 64×32).

## Predicción pre-registrada

La brecha de fidelidad de M2 respecto del especialista crece con el solapamiento (Spearman ρ > 0, p < 0.05); con pares disjuntos la brecha es cercana a cero.

## Resultado

| estadístico | ρ | p |
|---|---|---|
| brecha vs solap izquierda | 0.06 | 0.7503 |
| brecha vs solap latente | 0.23 | 0.2427 |
| error clase vs solap izquierda | 0.49 | 0.0079 |
| brecha vs etiquetas compartidas | 0.19 | 0.3351 |

| par | solap. etiquetas | solap. latente | etiq. compartidas | consultas | d M2 | d oráculo | d M8 | brecha M2 | brecha M8 | clase M2 | compat con la otra clase |
|---|---|---|---|---|---|---|---|---|---|---|---|
| car-pear | 0.574 | 0.406 | 0 | 44 | 28.5 | 27.5 | 32.9 | +1.1 | +5.4 | 100.0 | 0.57 |
| cow-pear | 0.583 | 0.439 | 0 | 44 | 25.6 | 23.0 | 31.4 | +2.5 | +8.3 | 100.0 | 0.61 |
| dog-tomato | 0.586 | 0.452 | 0 | 42 | 27.9 | 26.6 | 33.5 | +1.2 | +6.8 | 100.0 | 0.66 |
| car-tomato | 0.588 | 0.356 | 0 | 44 | 28.8 | 27.9 | 32.9 | +0.9 | +4.9 | 100.0 | 0.51 |
| cow-tomato | 0.595 | 0.422 | 0 | 44 | 25.0 | 23.5 | 31.3 | +1.5 | +7.8 | 100.0 | 0.60 |
| cup-pear | 0.595 | 0.472 | 0 | 44 | 28.2 | 25.4 | 33.4 | +2.7 | +8.0 | 100.0 | 0.64 |
| cow-cup | 0.598 | 0.424 | 0 | 42 | 28.4 | 24.5 | 31.0 | +3.9 | +6.6 | 100.0 | 0.62 |
| dog-pear | 0.598 | 0.500 | 0 | 42 | 31.0 | 26.2 | 33.6 | +4.8 | +7.4 | 100.0 | 0.71 |
| horse-pear | 0.598 | 0.449 | 0 | 44 | 25.5 | 25.5 | 30.1 | +0.1 | +4.7 | 100.0 | 0.57 |
| car-cow | 0.601 | 0.397 | 0 | 42 | 27.9 | 26.6 | 30.5 | +1.3 | +3.9 | 100.0 | 0.60 |
| cup-tomato | 0.601 | 0.362 | 0 | 44 | 26.4 | 25.9 | 33.3 | +0.5 | +7.4 | 100.0 | 0.51 |
| horse-tomato | 0.602 | 0.453 | 0 | 44 | 25.6 | 25.9 | 30.1 | -0.3 | +4.2 | 100.0 | 0.59 |
| car-cup | 0.603 | 0.471 | 0 | 42 | 30.5 | 29.1 | 32.7 | +1.4 | +3.5 | 100.0 | 0.69 |
| cup-horse | 0.609 | 0.465 | 0 | 42 | 27.5 | 27.0 | 29.7 | +0.5 | +2.7 | 100.0 | 0.62 |
| apple-cow | 0.612 | 0.437 | 0 | 43 | 28.9 | 25.3 | 33.8 | +3.5 | +8.4 | 100.0 | 0.65 |
| car-dog | 0.613 | 0.441 | 0 | 40 | 32.7 | 30.1 | 32.8 | +2.7 | +2.7 | 100.0 | 0.66 |
| car-horse | 0.615 | 0.478 | 0 | 42 | 29.8 | 29.2 | 29.3 | +0.6 | +0.1 | 100.0 | 0.65 |
| apple-car | 0.617 | 0.442 | 0 | 43 | 32.1 | 29.9 | 35.4 | +2.2 | +5.5 | 100.0 | 0.65 |
| cup-dog | 0.621 | 0.458 | 1 | 40 | 30.5 | 27.8 | 33.3 | +2.7 | +5.5 | 100.0 | 0.67 |
| apple-horse | 0.625 | 0.431 | 0 | 43 | 27.1 | 27.8 | 32.5 | -0.7 | +4.7 | 100.0 | 0.61 |
| cow-dog | 0.628 | 0.467 | 2 | 40 | 29.1 | 25.2 | 31.1 | +4.0 | +5.9 | 100.0 | 0.69 |
| apple-cup | 0.631 | 0.446 | 0 | 43 | 29.7 | 27.8 | 35.8 | +1.9 | +8.1 | 100.0 | 0.66 |
| apple-dog | 0.632 | 0.454 | 0 | 41 | 31.3 | 28.6 | 36.1 | +2.7 | +7.5 | 100.0 | 0.68 |
| dog-horse | 0.638 | 0.458 | 2 | 40 | 27.4 | 27.9 | 29.7 | -0.4 | +1.9 | 100.0 | 0.68 |
| cow-horse | 0.639 | 0.458 | 2 | 42 | 26.4 | 24.5 | 27.6 | +1.9 | +3.1 | 97.6 | 0.61 |
| apple-tomato | 0.640 | 0.348 | 2 | 45 | 30.4 | 26.7 | 35.9 | +3.7 | +9.2 | 93.0 | 0.52 |
| apple-pear | 0.647 | 0.497 | 2 | 45 | 29.9 | 26.2 | 35.9 | +3.7 | +9.7 | 98.8 | 0.69 |
| pear-tomato | 0.652 | 0.386 | 1 | 46 | 24.9 | 24.5 | 33.5 | +0.4 | +9.1 | 100.0 | 0.51 |

## Archivos
- `raw/<par>.json`: filas por consulta, semilla y sorteo
- `solapamiento.json`: solapamientos por par
- `resumen.json`: tabla y estadísticos
- `fig1_brecha_vs_solapamiento.png`