# Experimento 12 — la ventaja de partir contra el solapamiento entre dominios

28 pares de clases. Para cada par, una EHAM única con las dos clases (M2, N=200, mismo llenado que exp11) responde a las consultas reservadas de esas clases; semillas [42, 43, 44, 45, 46], 3 sorteos. Referencia: el especialista (T-oráculo de exp11) y la EHAM de ocho clases (M8 de exp11) sobre las mismas consultas y semillas. Solapamiento: Jaccard medio por coordenada de los soportes de las dos clases, en el lado de las etiquetas (homo L, 300×16) y en el latente (homo R, 64×32).

## Predicción pre-registrada

La brecha de fidelidad de M2 respecto del especialista crece con el solapamiento (Spearman ρ > 0, p < 0.05); con pares disjuntos la brecha es cercana a cero.

## Resultado

| estadístico | ρ | p |
|---|---|---|
| brecha vs solap izquierda | 0.45 | 0.0170 |
| brecha vs solap latente | -0.07 | 0.7107 |
| error clase vs solap izquierda | 0.49 | 0.0079 |
| brecha vs etiquetas compartidas | 0.32 | 0.0981 |

| par | solap. etiquetas | solap. latente | etiq. compartidas | consultas | d M2 | d oráculo | d M8 | brecha M2 | brecha M8 | clase M2 | compat con la otra clase |
|---|---|---|---|---|---|---|---|---|---|---|---|
| car-pear | 0.574 | 0.358 | 0 | 44 | 23.1 | 22.1 | 25.3 | +1.0 | +3.2 | 100.0 | 0.56 |
| cow-pear | 0.583 | 0.383 | 0 | 44 | 23.3 | 22.5 | 23.9 | +0.8 | +1.4 | 100.0 | 0.55 |
| dog-tomato | 0.586 | 0.397 | 0 | 42 | 23.1 | 21.3 | 29.8 | +1.8 | +8.5 | 100.0 | 0.65 |
| car-tomato | 0.588 | 0.318 | 0 | 44 | 21.9 | 20.9 | 29.3 | +1.0 | +8.5 | 100.0 | 0.54 |
| cow-tomato | 0.595 | 0.393 | 0 | 44 | 22.1 | 21.3 | 28.0 | +0.8 | +6.7 | 100.0 | 0.54 |
| cup-pear | 0.595 | 0.422 | 0 | 44 | 23.6 | 22.7 | 24.6 | +0.9 | +1.9 | 100.0 | 0.60 |
| cow-cup | 0.598 | 0.368 | 0 | 42 | 26.2 | 25.6 | 25.6 | +0.6 | -0.0 | 100.0 | 0.57 |
| dog-pear | 0.598 | 0.454 | 0 | 42 | 23.9 | 22.5 | 25.5 | +1.4 | +3.0 | 100.0 | 0.70 |
| horse-pear | 0.598 | 0.412 | 0 | 44 | 20.5 | 19.7 | 23.0 | +0.7 | +3.2 | 100.0 | 0.56 |
| car-cow | 0.601 | 0.350 | 0 | 42 | 25.5 | 25.0 | 26.3 | +0.5 | +1.3 | 100.0 | 0.58 |
| cup-tomato | 0.601 | 0.330 | 0 | 44 | 23.6 | 21.4 | 28.7 | +2.2 | +7.2 | 100.0 | 0.49 |
| horse-tomato | 0.602 | 0.429 | 0 | 44 | 20.3 | 18.5 | 27.0 | +1.8 | +8.5 | 100.0 | 0.60 |
| car-cup | 0.603 | 0.423 | 0 | 42 | 26.2 | 25.2 | 27.1 | +0.9 | +1.8 | 100.0 | 0.69 |
| cup-horse | 0.609 | 0.425 | 0 | 42 | 24.8 | 22.8 | 24.6 | +2.0 | +1.8 | 100.0 | 0.59 |
| apple-cow | 0.612 | 0.357 | 0 | 43 | 24.6 | 22.8 | 27.1 | +1.8 | +4.3 | 100.0 | 0.53 |
| car-dog | 0.613 | 0.388 | 0 | 40 | 26.4 | 25.2 | 28.1 | +1.2 | +2.9 | 100.0 | 0.65 |
| car-horse | 0.615 | 0.444 | 0 | 42 | 22.8 | 22.2 | 25.3 | +0.7 | +3.2 | 100.0 | 0.69 |
| apple-car | 0.617 | 0.378 | 0 | 43 | 24.5 | 22.4 | 28.5 | +2.1 | +6.2 | 100.0 | 0.64 |
| cup-dog | 0.621 | 0.408 | 1 | 40 | 28.0 | 25.9 | 27.4 | +2.1 | +1.5 | 100.0 | 0.65 |
| apple-horse | 0.625 | 0.376 | 0 | 43 | 21.5 | 20.0 | 26.1 | +1.5 | +6.2 | 100.0 | 0.57 |
| cow-dog | 0.628 | 0.401 | 2 | 40 | 26.4 | 25.7 | 26.6 | +0.8 | +1.0 | 100.0 | 0.63 |
| apple-cup | 0.631 | 0.378 | 0 | 43 | 23.9 | 23.0 | 27.9 | +0.9 | +4.9 | 100.0 | 0.61 |
| apple-dog | 0.632 | 0.401 | 0 | 41 | 26.5 | 22.9 | 28.9 | +3.7 | +6.1 | 100.0 | 0.64 |
| dog-horse | 0.638 | 0.410 | 2 | 40 | 23.6 | 22.7 | 25.6 | +1.0 | +2.9 | 100.0 | 0.65 |
| cow-horse | 0.639 | 0.406 | 2 | 42 | 25.0 | 22.6 | 23.9 | +2.4 | +1.3 | 97.6 | 0.58 |
| apple-tomato | 0.640 | 0.294 | 2 | 45 | 23.4 | 18.8 | 30.0 | +4.6 | +11.2 | 94.5 | 0.48 |
| apple-pear | 0.647 | 0.419 | 2 | 45 | 22.9 | 20.0 | 26.1 | +2.9 | +6.1 | 98.4 | 0.60 |
| pear-tomato | 0.652 | 0.348 | 1 | 46 | 19.9 | 18.6 | 26.9 | +1.3 | +8.3 | 100.0 | 0.54 |

## Archivos
- `raw/<par>.json`: filas por consulta, semilla y sorteo
- `solapamiento.json`: solapamientos por par
- `resumen.json`: tabla y estadísticos
- `fig1_brecha_vs_solapamiento.png`