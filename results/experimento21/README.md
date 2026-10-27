# Experimento 21 — memoria única contra partición, sobre MedMNIST+

Pregunta: ¿varias memorias guardan más que una? Con el mismo contenido (pozo de la muestra: 200 de llenado × 16 variantes por agente, fase A 128) y el mismo test (hasta 300 por dominio), por nivel:

- **M, memoria única:** una sola memoria hetero imagen ↔ etiqueta con todos los dominios del nivel. La etiqueta es el vector fastText del término del dominio (media de sus palabras, `medico_terminos.json`; «dermatofibroma» no está en fastText y se usó «skin fibroma»), como en exp11. Decide por el soporte de cada etiqueta en la proyección y rechaza si la proyección tiene una fila vacía.
- **T-especialistas:** una memoria por dominio; decide el especialista que reconoce con más fuerza, sin directorio.
- **T-protocolo:** el sistema con directorios perspectivales (el demo).

Script `run_experiment21_monolitica.py`, 75 min (5 niveles en paralelo; lo que tarda es llenar la memoria hetero de M). Detalle en `resumen.txt` y `filas.json`.

| nivel | M | T-especialistas | T-protocolo |
|---|---|---|---|
| modalidad (4): acierto / rechazo / balanceado | 93.0 / 5.7 / 93.4 | 93.1 / 5.7 / 93.5 | 85.7 / 13.6 / 86.0 |
| órganos (11) | 90.7 / 6.0 / 90.7 | 90.8 / 6.0 / 90.8 | 87.7 / 10.0 / 87.7 |
| piel (7) | 72.9 / 4.8 / 63.1 | 72.3 / 4.8 / 63.1 | 72.7 / 6.3 / 64.5 |
| mama (2) | 76.9 / 3.2 / 63.2 | 78.8 / 3.2 / 66.7 | **88.5 / 1.9 / 82.3** |
| **tórax (14)** | **14.1** / 0.6 / **13.1** | **24.8** / 0.6 / **24.4** | 22.4 / 1.1 / 23.0 |

Predicción fijada antes de correr: *M confunde más entre dominios cuyos términos comparten palabras*. **No se cumple:** fémur izquierdo → derecho, 11 en M y 11 en especialistas. Donde M sí falla es en tórax, y de otra forma: casi todo cae en «pleural thickening» (nódulo 240, masa 227, sin hallazgo 218, neumotórax 215). Una etiqueta se lleva el soporte de la mezcla.

## Lectura

- **Con dominios visualmente separables, una memoria única con etiquetas distribuidas iguala a la partición** (diferencias ≤ 0.6 puntos en modalidad, órganos y piel). Es lo mismo que exp11 en ETH-80: en clase, empatan.
- **Con 14 dominios muy superpuestos (radiografía de tórax), la partición casi duplica a la memoria única** (24.4 contra 13.1 balanceado; azar 7.1). En la memoria única, una etiqueta («pleural thickening») se lleva el soporte de casi todo. Es exp12 a escala: la ventaja de partir crece con el solapamiento de las pistas.
- **«Varias guardan más que una» se sostiene donde importa: cuando los contenidos se pisan.** No se sostiene como regla general de exactitud. Lo que la partición compra es no mezclar.
- **Los directorios** no suman exactitud sobre los especialistas en modalidad y órganos (rechazan más y aciertan un poco más de lo que responden). Sí suman en mama (88.5 contra 78.8): la fase A registra a quién ganó cada percepción, y eso corrige el sesgo de reconocimiento hacia benigno.
- M y los especialistas rechazan exactamente la misma fracción en todos los niveles.
- **Ninguno de los dos brazos recuerda** (nota del 26 oct 2026). M decide con `support_ranking`: normaliza la proyección por fila y elige, entre la lista cerrada de etiquetas de los dominios, la de mayor probabilidad media. Los especialistas eligen al de mayor reconocimiento entre los dominios. Las dos son lecturas de conjunto cerrado y en ningún caso se ejecuta `recall_from_right`. Por eso las cifras hablan de cuánto separa cada memoria los dominios, no de qué palabra devolvería un recuerdo (exp17 muestra que el recuerdo es menos estable que el soporte).
