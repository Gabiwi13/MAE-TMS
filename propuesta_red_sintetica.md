# Red con fallas sintéticas y término anti-colapso

**Fecha:** 19 de octubre de 2026
**Estado:** fijada antes de correr. Lo que cambie después se declara en el informe como desviación. Según el resultado se decide si se pasa a la arquitectura mixta.

## 1. Pregunta

La red entrenada con buenas contra malas colapsa las piezas buenas en 1 a 3 direcciones y pone ahí las fallas de un tipo que no vio. El 24.1 % pasa como buena con la red y el 31.8 % con la cascada de la MAE. ¿Entrenar con fallas sintéticas (aprender «cualquier desviación») y con un término que conserve la variación del latente (anti-colapso) baja esa falla silenciosa? ¿Le da a la MAE un latente donde la cascada sí manda lo nuevo a revisión?

## 2. Diseño

Mismo montaje que el cierre y la cascada: WideResNet50, capas 3 y 4 ajustadas, latente de 64, cabeza de 2 clases, mismos repartos de fallas (tipo primario más frecuente excluido), 270 normales de llenado, semilla 42.

**Fallas sintéticas** (sobre una pieza buena, generadas al vuelo; implementación propia, sin descargas):
- **CutPaste:** un rectángulo del 2 al 15 % del área y proporción de 0.3 a 3.3, recortado de la misma imagen, con brillo y contraste alterados en ±20 %, y pegado en otra posición.
- **Cicatriz:** una franja de 2 a 16 px de ancho y 10 a 25 px de largo, recortada de la misma imagen, rotada al azar y pegada.
- **Mancha:** una elipse de 4 a 24 px de semieje, con color aleatorio y borde suave, mezclada con opacidad de 0.5 a 1.

Cada falla sintética usa uno de los tres tipos con la misma probabilidad. Las sintéticas cuentan como «mala».

**Término anti-colapso** (estilo VICReg sobre el latente del lote): varianza = media de max(0, 1 − desviación de cada dimensión); covarianza = suma de los cuadrados de las covarianzas fuera de la diagonal, dividida por 64. Pérdida = entropía cruzada + 1.0 × varianza + 0.04 × covarianza.

**Variantes de red:**
- **A:** base (la del cierre, latentes en caché).
- **B:** + fallas sintéticas.
- **C:** + fallas sintéticas + anti-colapso.
- **D:** + anti-colapso, sin sintéticas.

Entrenamiento de B, C y D: 16 épocas de 288 muestras, lotes de 24, Adam con lr 1e-4 y precisión mixta. El muestreo es un tercio normales, un tercio fallas reales y un tercio sintéticas (en D: mitad normales, mitad fallas reales). A se entrenó con 12 épocas de 256 y lotes de 16; la diferencia de presupuesto se declara.

**Medidas por variante** (12 piezas; tipo nuevo en 11):
- **Colapso:** fracción de la varianza de las buenas en las 3 primeras direcciones, y número de direcciones para el 95 %.
- **Red:** detección y falsa alarma en lo conocido (argmax); falla silenciosa en el tipo nuevo (argmax).
- **Cascada de la MAE:** malas → buenas (k = 1 y k = 8) → revisión. Detección, falsa alarma y revisión en lo conocido; revisión, mala y falla silenciosa en lo nuevo.
- **MSP de la red** a igual revisión en lo conocido que la cascada: falla silenciosa en lo nuevo.

## 3. Predicciones

- **PS1.** Las sintéticas (B, C) bajan la falla silenciosa de la red en el tipo nuevo respecto de A (24.1 %), en al menos 10 puntos.
- **PS2.** El anti-colapso (C, D) baja la fracción de varianza en 3 direcciones por debajo de 0.90 (A: de 0.987 a 0.999).
- **PS3.** Con C, la cascada manda a revisión más fallas nuevas que con A (> 10 %), y partir el módulo de buenas (k = 8) ahora sí cambia decisiones.
- **PS4.** Aun así, a igual revisión, la cascada no le gana a MSP de la misma red por 10 puntos.

## 4. Criterio

- **«Las fallas sintéticas resuelven lo nuevo para la red»:** sostenido si en B o C la falla silenciosa de la red baja ≥ 10 puntos respecto de A, sin subir la falsa alarma en lo conocido más de 3 puntos.
- **«La MAE aprovecha una red no colapsada»:** sostenido si en C o D la falla silenciosa de la cascada (k = 1 u 8) es al menos 10 puntos menor que la de MSP a igual revisión, con falsa alarma ≤ la de la red + 2 puntos. Si no, la MAE queda como capa de ruteo y registro, y se pasa a la arquitectura mixta con la mejor red de este experimento como detector.

## 5. Entregables

`run_red_sintetica.py` (latentes en `results/red_sintetica/cache/`, fuera de git) y `results/red_sintetica/{README.md, resumen.txt, resultados.json}`.
