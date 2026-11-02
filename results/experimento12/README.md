# Experimento 12 — la ventaja de partir contra el solapamiento entre dominios

28 pares de clases. Para cada par, una EHAM única con las dos clases (M2, N=200, mismo llenado que exp11) responde a las consultas reservadas de esas clases; semillas [42, 43, 44, 45, 46], 3 sorteos. Referencia: el especialista (T-oráculo de exp11) y la EHAM de ocho clases (M8 de exp11) sobre las mismas consultas y semillas. Solapamiento: Jaccard medio por coordenada de los soportes de las dos clases, en el lado de las etiquetas (homo L, 300×16) y en el latente (homo R, 64×32).

## Predicción pre-registrada

La brecha de fidelidad de M2 respecto del especialista crece con el solapamiento (Spearman ρ > 0, p < 0.05); con pares disjuntos la brecha es cercana a cero.

## Resultado

| estadístico | ρ | p |
|---|---|---|
| brecha vs solap izquierda | 0.01 | 0.9515 |
| brecha vs solap latente | 0.21 | 0.2895 |
| error clase vs solap izquierda | 0.49 | 0.0079 |
| brecha vs etiquetas compartidas | 0.21 | 0.2799 |

| par | solap. etiquetas | solap. latente | etiq. compartidas | consultas | d M2 | d oráculo | d M8 | brecha M2 | brecha M8 | clase M2 | compat con la otra clase |
|---|---|---|---|---|---|---|---|---|---|---|---|
| car-pear | 0.574 | 0.406 | 0 | 44 | 28.9 | 27.2 | 32.4 | +1.7 | +5.1 | 100.0 | 0.58 |
| cow-pear | 0.583 | 0.439 | 0 | 44 | 26.7 | 22.7 | 30.7 | +4.0 | +8.0 | 100.0 | 0.62 |
| dog-tomato | 0.586 | 0.452 | 0 | 42 | 28.9 | 27.2 | 33.6 | +1.7 | +6.4 | 100.0 | 0.67 |
| car-tomato | 0.588 | 0.356 | 0 | 44 | 29.2 | 27.9 | 32.8 | +1.3 | +4.9 | 100.0 | 0.54 |
| cow-tomato | 0.595 | 0.422 | 0 | 44 | 26.2 | 23.4 | 31.2 | +2.8 | +7.8 | 100.0 | 0.61 |
| cup-pear | 0.595 | 0.472 | 0 | 44 | 29.4 | 25.4 | 32.9 | +3.9 | +7.5 | 100.0 | 0.65 |
| cow-cup | 0.598 | 0.424 | 0 | 42 | 29.1 | 24.3 | 30.9 | +4.8 | +6.5 | 100.0 | 0.63 |
| dog-pear | 0.598 | 0.500 | 0 | 42 | 31.5 | 26.5 | 33.0 | +5.1 | +6.6 | 100.0 | 0.71 |
| horse-pear | 0.598 | 0.449 | 0 | 44 | 26.6 | 25.4 | 30.1 | +1.2 | +4.7 | 100.0 | 0.59 |
| car-cow | 0.601 | 0.397 | 0 | 42 | 28.8 | 26.2 | 30.3 | +2.5 | +4.0 | 100.0 | 0.61 |
| cup-tomato | 0.601 | 0.362 | 0 | 44 | 27.0 | 26.1 | 33.4 | +0.9 | +7.3 | 100.0 | 0.53 |
| horse-tomato | 0.602 | 0.453 | 0 | 44 | 26.2 | 26.0 | 30.5 | +0.2 | +4.5 | 100.0 | 0.61 |
| car-cup | 0.603 | 0.471 | 0 | 42 | 31.1 | 29.1 | 32.6 | +2.0 | +3.6 | 100.0 | 0.70 |
| cup-horse | 0.609 | 0.465 | 0 | 42 | 27.7 | 27.1 | 30.2 | +0.6 | +3.1 | 100.0 | 0.64 |
| apple-cow | 0.612 | 0.437 | 0 | 43 | 30.2 | 25.6 | 33.8 | +4.7 | +8.2 | 100.0 | 0.65 |
| car-dog | 0.613 | 0.441 | 0 | 40 | 33.5 | 30.4 | 32.7 | +3.2 | +2.4 | 100.0 | 0.67 |
| car-horse | 0.615 | 0.478 | 0 | 42 | 30.1 | 29.0 | 29.6 | +1.1 | +0.6 | 100.0 | 0.67 |
| apple-car | 0.617 | 0.442 | 0 | 43 | 32.8 | 30.2 | 35.5 | +2.6 | +5.3 | 100.0 | 0.67 |
| cup-dog | 0.621 | 0.458 | 1 | 40 | 32.1 | 28.3 | 33.4 | +3.8 | +5.0 | 100.0 | 0.67 |
| apple-horse | 0.625 | 0.431 | 0 | 43 | 28.4 | 28.2 | 33.1 | +0.2 | +4.9 | 100.0 | 0.62 |
| cow-dog | 0.628 | 0.467 | 2 | 40 | 30.1 | 25.4 | 30.9 | +4.7 | +5.5 | 100.0 | 0.70 |
| apple-cup | 0.631 | 0.446 | 0 | 43 | 30.1 | 28.3 | 36.1 | +1.8 | +7.8 | 100.0 | 0.67 |
| apple-dog | 0.632 | 0.454 | 0 | 41 | 33.0 | 29.5 | 36.4 | +3.5 | +6.8 | 100.0 | 0.69 |
| dog-horse | 0.638 | 0.458 | 2 | 40 | 28.1 | 28.3 | 30.2 | -0.2 | +1.9 | 100.0 | 0.69 |
| cow-horse | 0.639 | 0.458 | 2 | 42 | 27.5 | 24.3 | 27.9 | +3.2 | +3.6 | 97.6 | 0.63 |
| apple-tomato | 0.640 | 0.348 | 2 | 45 | 31.1 | 27.2 | 36.1 | +3.8 | +8.9 | 93.9 | 0.53 |
| apple-pear | 0.647 | 0.497 | 2 | 45 | 31.4 | 26.6 | 35.7 | +4.8 | +9.1 | 99.0 | 0.69 |
| pear-tomato | 0.652 | 0.386 | 1 | 46 | 25.8 | 24.5 | 33.1 | +1.3 | +8.6 | 100.0 | 0.53 |

## Archivos
- `raw/<par>.json`: filas por consulta, semilla y sorteo
- `solapamiento.json`: solapamientos por par
- `resumen.json`: tabla y estadísticos
- `fig1_brecha_vs_solapamiento.png`