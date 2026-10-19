# Experimento 29: la demencia semántica como pérdida de conteos

Diseño, predicciones, criterio y decisiones del paso 0 en `propuesta_exp29_demencia_semantica.md` (el anexo se fijó antes de correr). Es la oportunidad C1 de `MAE-TMS/reports/Memorias asociativas en salud.md`.

- **Ambiente:** el de Rogers et al. 2004 (DOI 10.1037/0033-295X.111.1.205), con los prototipos de su Figura 3. Hay 48 ítems en 6 categorías y se agregó un factor de frecuencia: 4 ítems de cada categoría se registran 4 veces y 4 una sola vez. La especificación extraída está en `research_notes/.../rogers2004_especificacion.md`.
- **Modelos:**
  - la MAE (`HeteroAssociativeMemory` oficial, verbal ↔ visual), dañada adelgazando sus conteos;
  - un PDP recurrente como el de Rogers, dañado quitando pesos;
  - MINERVA 2 y un vecino más cercano, dañados borrando rasgos.
- **Tareas:** denominación (visual → nombre) de los 28 ítems con nombre propio, sin frutas, y dibujo (nombre → visual).
- **Corrida:** 10 semillas de ambiente, 24 niveles de daño y 10 lesiones por nivel.
- **Script:** `run_experiment29_demencia_semantica.py`; el informe lo genera `exp29_reporte.py`. Hubo 4 procesos en paralelo durante unas 3.5 h. El detalle completo está en `resumen.txt` y `resultados.json`. Las filas por ensayo (`filas_s*.json`) quedan fuera de git.

## Desviaciones de la propuesta (todas antes de ver resultados con daño)

- **10 lesiones por nivel y 2 ensayos por ítem en la MAE**, en lugar de 50 y 10. Cada recall cuesta 292 ms; con lo propuesto, la corrida habría durado unas 200 h.
- **Rejilla de daño:** a la de la propuesta (0 a 0.9 de 0.05 en 0.05) se le agregaron 0.01, 0.02, 0.03, 0.04 y 0.075, porque la MAE pierde el nombre con muy poco daño.
- **MINERVA 2:** los nombres se codificaron como +1 o 0 en lugar de ±1. Con −1 en los 39 nombres ausentes de cada trazo, el eco empujaba todos los nombres hacia abajo y el dibujo salía al revés (0 % de denominación y 17.7 % de rasgos sin daño).
- **Verificación sin daño** (≥ 95 % en denominación, ≥ 90 % en dibujo):
  - **Pasan:** la MAE con la lectura principal por recall (98.6 % en las 10 semillas; 100 % en la verificación con semilla 0) y el vecino más cercano (100 %).
  - **El PDP pasa en 8 de 10 semillas** (96.4–100 %). En las semillas 1 y 5 llegó al tope de 2000 épocas sin cumplir el criterio y nombra el 82.1 y el 78.6 % sin daño. Sus curvas se incluyen igual (media 94.3 %). Como la comparación con pacientes se hace a igual exactitud, esto pesa poco, pero hay que declararlo.
  - **No pasan:** MINERVA 2 (49.3 %), porque con similitud al cubo y ítems muy parecidos dentro de su categoría los vecinos frecuentes le ganan al propio ítem; y la lectura de la MAE por proyección (≈ 4 %).
  - Los dos que no pasan se reportan, pero quedan fuera del criterio.

## Resultado principal: denominación a la exactitud de cada cuartil de pacientes

Proporción de respuestas (%), modelo / pacientes de Rogers 2004 (Figura 6). Cada modelo se evalúa en el daño en que su exactitud iguala la del cuartil.

| cuartil (exactitud) | modelo | omisión | semántico | superordinado | entre dominios | dentro de ±10 |
|---|---|---|---|---|---|---|
| Q1 (79.6) | **MAE** | 19.7 / 10.4 | **0.0** / 8.9 | 0.7 / 1.0 | 0.0 / 0.1 | sí |
| | PDP | 7.1 / 10.4 | 9.1 / 8.9 | 3.6 / 1.0 | 0.6 / 0.1 | sí |
| | vecino | 20.3 / 10.4 | 0.0 / 8.9 | 0.1 / 1.0 | 0.0 / 0.1 | sí |
| Q2 (38.1) | **MAE** | **61.1** / 31.2 | **0.0** / 24.1 | 0.8 / 6.3 | 0.0 / 0.5 | no |
| | PDP | 24.5 / 31.2 | 27.4 / 24.1 | 7.5 / 6.3 | 2.6 / 0.5 | sí |
| | vecino | 55.6 / 31.2 | 4.1 / 24.1 | 1.2 / 6.3 | 1.0 / 0.5 | no |
| Q3 (12.9) | **MAE** | **86.7** / 56.0 | **0.0** / 17.0 | 0.4 / 14.1 | 0.0 / 0.2 | no |
| | PDP | 43.5 / 56.0 | 30.5 / 17.0 | 7.2 / 14.1 | 5.9 / 0.2 | no |
| | vecino | 77.9 / 56.0 | 6.3 / 17.0 | 1.3 / 14.1 | 1.7 / 0.2 | no |
| Q4 (4.5) | **MAE** | 95.2 / 82.2 | **0.0** / 7.0 | 0.3 / 5.9 | 0.0 / 0.6 | no |
| | PDP | 60.5 / 82.2 | 24.0 / 7.0 | 4.4 / 5.9 | 6.6 / 0.6 | no |
| | vecino | 91.4 / 82.2 | 2.8 / 7.0 | 0.5 / 5.9 | 0.8 / 0.6 | sí |

**Curva de la MAE.**
- En ninguno de los 24 niveles da un error semántico ni entre dominios, y las respuestas superordinadas nunca pasan de 1.3 %.
- La exactitud baja en dos escalones, uno por frecuencia:
  - los ítems vistos una vez pierden el nombre entre d = 0.01 y 0.05, y la exactitud queda en ~50 % hasta d ≈ 0.2;
  - los ítems vistos 4 veces aguantan hasta d ≈ 0.3–0.45;
  - desde d = 0.55 todo es omisión.

## Predicciones

| | predicción para la MAE | MAE | PDP | vecino |
|---|---|---|---|---|
| P1 | las omisiones crecen con el daño | **se cumple** (10/10 semillas) | se cumple | se cumple |
| P2 | superordinados < omisiones en Q4 | se cumple (0.3 contra 95.2) | se cumple | se cumple |
| P3 | errores semánticos en U invertida | **no se cumple: no hay ninguno** | se cumple (máximo 31.9 % en d = 0.3) | se cumple, débil (máximo 6.9 %) |
| P4 | entre dominios < 5 % | se cumple (0 %) | no (hasta 11.1 %) | se cumple |
| P5 | errores más típicos que el blanco y crecientes | **no se puede: no hay errores semánticos** | no (diferencia −0.003) | se cumple apenas (+0.004) |
| P6 | los frecuentes resisten más y los intrusos son frecuentes, cada vez más | **no se cumple.** Resisten mucho más (+72.2 puntos en promedio; +36.9 en los cuartiles), pero no hay intrusos y el efecto no crece (pendiente −1.46) | se cumple (+19.9; intrusos frecuentes 59 %) | no (+0.3) |
| P7 | al dibujar se pierden antes los distintivos y crecen las intrusiones compartidas | **no se cumple.** Pierde por igual distintivos (73.2 %) y compartidos (74.0 %) y no agrega intrusiones: dibuja el ítem completo o nada | no, a medias: omite más distintivos (63.2 contra 48.7 %), pero las intrusiones no crecen | no |
| P8 | crecen con el daño las respuestas al nombre frecuente o más típico de la categoría | **no se cumple** (siempre 0) | no | se cumple apenas |
| P9 | los rivales reproducen P1–P4, pero MINERVA y el vecino no dan la U invertida y el PDP no produce P6 sin frecuencia | el PDP reproduce P1–P3, no P4; el vecino sí da una U débil; el PDP sí produce P6 con frecuencia de entrenamiento. MINERVA no pasó la verificación (con semánticos de 20 a 55 % y sin omisiones) | | |

## Criterio

- **«La MAE es un modelo viable de la demencia semántica»: refutado.**
  - Cumple P1, P2 y P4.
  - No cumple P3, que la propuesta ponía como condición de refutación.
  - Queda dentro de ±10 puntos de los pacientes en 1 de 4 cuartiles (se pedían 3).
  - No cumple P8: su sesgo a lo típico no aparece con el daño.
- **«La MAE aporta algo que el modelo canónico no»: refutado.** No cumple P5 ni P6. El PDP, con la misma frecuencia de entrenamiento, sí cumple P6.

## Lectura

1. **La MAE dañada solo sabe callarse.** Su recuperación es una conjunción sobre las 64 columnas de la pista. El nombre específico de un ítem solo tiene soporte si cada rasgo visual de la pista coexistió con ese nombre. Al quitar conteos, basta con perder una celda para que el nombre se quede sin soporte, y la recuperación entera se rechaza. Nunca cae en el nombre de un vecino: para eso el vecino tendría que coincidir con el ítem en todos los rasgos. Es la misma propiedad que la hace rechazar en lugar de confundir en los experimentos 14, 16 y 20, vista aquí como síntoma. Los pacientes con demencia semántica sí confunden, y mucho (24 % de errores semánticos en Q2).
2. **La frecuencia sí está, pero como umbral, no como sesgo.** Un nombre registrado 4 veces necesita perder las 4 copias de una celda para caer, así que resiste mucho más. Eso da un efecto de frecuencia grande, pero no las intrusiones de nombres frecuentes ni los errores típicos que describen Woollams et al. (2008) y Hodges et al. (1995). En la MAE, la frecuencia decide cuándo se pierde un nombre, no qué nombre se dice en su lugar.
3. **El sesgo «hacia lo típico» de los experimentos anteriores no se trasladó aquí.** Allí aparecía porque el latente continuo, cuantizado, hacía que muchos objetos compartieran celdas y la pista cayera dentro de varias envolventes. Con rasgos binarios y sin variantes, cada nombre tiene una envolvente estrecha y no hay mezcla.
4. **El PDP de Rogers sigue siendo el mejor modelo de los cuatro**, aun simplificado: reproduce Q1 y Q2, la U invertida y el efecto de frecuencia. Sus fallas (demasiados errores semánticos y entre dominios con daño alto) no las corrige ninguno de los otros modelos.
5. **Para el camino cognitivo de la MAE en salud**, este resultado debilita la línea de la demencia semántica, como preveía el informe de literatura si la MAE fallaba aquí.
   - **No cubre:** la variante con ruido en lugar de quitar conteos (prevista como C2), ni una MAE con variantes en el registro (envolventes más anchas, como en los experimentos 13–16), que podría producir confusiones.
   - **Una advertencia sobre esa variante:** ensanchar las envolventes para que aparezcan confusiones sería elegir el ambiente para obtener el resultado esperado. Solo valdría con una razón independiente (por ejemplo, que la percepción humana no es exacta) y con predicciones fijadas antes.

## Notas

- Una sola red PDP por semilla, lesionada 10 veces por nivel; Rogers usó 100 lesiones de una red.
- La clasificación de errores es la de la propuesta. El superordinado de un ave puede ser «bird» o «animal»; los objetos domésticos y las frutas no tienen nombre general.
- Las cifras de pacientes salen de una lectura de la Figura 6 de Rogers 2004 calibrada por píxel (±0.005), no de una tabla.
- Los ítems de prueba son los del ambiente aprendido, como en Rogers: la denominación mide recuperación de lo conocido, no generalización.
