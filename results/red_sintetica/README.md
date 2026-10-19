# Red con fallas sintéticas y término anti-colapso

La red especializada (buenas contra malas) colapsa las piezas buenas en 1 a 3 direcciones, y ahí pone las fallas que no vio. Por eso ni ella ni la cascada de la MAE detectan bien un tipo de falla nuevo. Se probaron dos remedios: entrenar con **fallas sintéticas**, para que aprenda «cualquier desviación», y con un **término anti-colapso** (varianza y covarianza del latente, estilo VICReg). Diseño, predicciones y criterio fijados antes de correr en [`propuesta_red_sintetica.md`](../../propuesta_red_sintetica.md). Script: [`run_red_sintetica.py`](../../run_red_sintetica.py). Detalle en `resumen.txt` y `resultados.json`.

**Resultado en una línea:** las fallas sintéticas **empeoraron** a la red ante lo nuevo (de 26.7 a 36.8 % de fallas nuevas que pasan como buenas). El anti-colapso descolapsó el latente solo en parte (de 1 a entre 3 y 5 direcciones para el 95 % de la varianza). Con él, la cascada de la MAE **le ganó por primera vez a la confianza de la red** a igual revisión (26.8 contra 33.7 %), pero por 7 puntos, no por los 10 del criterio. El mejor sistema sigue siendo la red base con MSP (24.1 %).

## Montaje

- **Red:** la del cierre (WideResNet50, capas 3 y 4 ajustadas, latente de 64, cabeza de 2 clases), mismos repartos y semilla 42.
- **Variantes:**
  - A: base (latentes de la cascada);
  - B: + sintéticas;
  - C: + sintéticas + anti-colapso;
  - D: + anti-colapso.
- **Entrenamiento de B, C y D:** 16 épocas de 288 muestras, lotes de 24. La base usó 12 de 256 con lotes de 16 (declarado).
- **Fallas sintéticas (implementación propia):** CutPaste (rectángulo de la misma imagen, con brillo y contraste alterados), cicatriz (franja rotada) y mancha (elipse de color con borde suave). Se revisaron a ojo sobre pcb1, candle y cashew antes de correr. Algunas caen sobre el fondo, como en CutPaste original.

## Resultados (media de 12 piezas; tipo nuevo, 11 piezas)

| variante | varianza de las buenas en 3 direcciones · direcciones para el 95 % | red: conocido detección / falsa alarma | red: nuevo pasa en silencio |
|---|---|---|---|
| A base | 0.988 · 1.0 | 93.0 / 3.4 | **26.7** |
| B + sintéticas | 0.954 · 4.8 | 87.9 / 7.7 | 36.8 |
| C + sintéticas + anti-colapso | 0.944 · 3.3 | 91.1 / 5.8 | 30.0 |
| D + anti-colapso | 0.951 · 3.2 | 81.6 / 0.7 | 38.1 |

**Cascada de la MAE** (malas → buenas partidas en k → revisión) y **MSP de la misma red a igual revisión**:

| variante | cascada k = 8: conocido detección / falsa alarma | nuevo: revisión / pasa en silencio | MSP a igual revisión: pasa en silencio | diferencia (MSP − cascada) |
|---|---|---|---|---|
| A | 92.5 / 2.9 | 2.6 / 31.8 | **24.1** | −7.7 |
| B | 89.4 / 8.2 | 0.9 / 31.1 | 36.3 | +5.2 |
| C | 88.8 / 6.7 | 5.1 / 31.8 | 27.1 | −4.7 |
| D | 85.0 / 1.8 | 5.2 / **26.8** | 33.7 | **+6.9** |

Con k = 1 las cifras son casi las mismas. Con el anti-colapso (C y D), partir el módulo de buenas ya cambia algunas decisiones: la revisión de fallas nuevas sube de 3.8 a 5.1 % en C y de 3.1 a 5.2 % en D.

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| PS1 | las sintéticas bajan la falla silenciosa de la red ≥ 10 puntos | **Refutada: la suben** (B 36.8, C 30.0, contra A 26.7), y suben la falsa alarma (de 3.4 a 7.7 y 5.8) |
| PS2 | el anti-colapso baja la varianza en 3 direcciones por debajo de 0.90 | **No se cumple**: 0.944–0.951. Descolapso parcial: de 1 a 3–5 direcciones para el 95 % |
| PS3 | con C, la cascada manda a revisión > 10 % de lo nuevo, y k = 8 cambia decisiones | **En parte**: k = 8 cambia algunas decisiones, pero la revisión queda en 5.1 % |
| PS4 | a igual revisión, la cascada no le gana a MSP por 10 puntos | **Se cumple**: le gana por 5.2 (B) y 6.9 (D); pierde en A y C |

**Criterio 1** («las sintéticas resuelven lo nuevo para la red»): **refutado**.
**Criterio 2** («la MAE aprovecha una red no colapsada», ≥ 10 puntos menos que MSP con falsa alarma ≤ la de la red + 2): **no sostenido**. En D la ventaja es de 6.9 puntos (falsa alarma 1.8, contra 0.7 de la red, dentro del margen). Según lo fijado, se pasa a la arquitectura mixta.

## Lectura

1. **Las fallas sintéticas, así implementadas, no generalizan a las fallas reales de VisA.** Las fallas reales son chicas y sutiles (una mancha de color parecido, un borde astillado). Las sintéticas son más gruesas, y la red aprende a detectar esas, no «cualquier desviación». En la literatura CutPaste funciona por parches y sin fallas reales; aquí se mezcló con fallas reales y a nivel de imagen. No se exploraron otras versiones.
2. **El anti-colapso va en la dirección correcta para la MAE.** Es la primera vez en todo el proyecto que la memoria, a igual revisión, deja pasar menos fallas nuevas que la confianza de la red de su mismo latente (D: 26.8 contra 33.7). Pero lo logra empeorando a la red (detección 81.6 %), no mejorando sobre el mejor sistema.
3. **En términos absolutos, el mejor sistema sigue siendo la red base con MSP** (24.1 % de fallas nuevas en silencio, 92 % de detección). Ninguna variante lo mejoró.
4. **Decisión:** se pasa a la arquitectura mixta, con la red base (A) como detector para piezas con fallas etiquetadas, o PatchCore si solo hay piezas sanas, y la MAE como capa de ruteo, registro y olvido. Queda abierto, como línea de investigación y no como solución, el hallazgo de que un latente menos colapsado favorece a la memoria frente a la confianza de la red.

## Notas

- Corrección hecha al escribir este informe: en el informe de la cascada, la fila «cabeza de la red, sin revisión» decía 24.1 % de falla silenciosa. Es 26.7 % (24.1 es MSP a igual revisión). Ya está corregida.
- Una sola semilla por variante. Con 20 a 53 fallas nuevas por pieza, cada punto porcentual por pieza son menos de una imagen. Las diferencias de 5 a 7 puntos en la media están dentro de lo que puede mover otra semilla.
