# Aprendizaje en línea con deriva: el olvido exacto como mecanismo de adaptación

En una flota real, un módulo que era el mejor puede degradarse. ¿El sistema transactivo, aprendiendo en línea, lo nota y pasa al otro? ¿El **olvido exacto** de las transacciones viejas (ventana deslizante restando conteos) es lo que se lo permite? Diseño, predicciones y criterio fijados antes de correr en [`propuesta_deriva_olvido.md`](../../propuesta_deriva_olvido.md). Script: [`run_deriva_olvido.py`](../../run_deriva_olvido.py). Detalle en `resumen.txt` y `resultados.json`.

**Resultado en una línea:** el olvido exacto **sí es lo que permite adaptarse**. Sin olvido, la memoria nunca vuelve a preferir al módulo bueno tras la deriva (queda alrededor del 50 %). Con una ventana de 1200 transacciones se recupera a los 1250 pasos (≥ 70 % al nuevo mejor). Pero en acierto final queda **6.2 puntos bajo el bandido central** con la misma ventana (74.3 contra 80.5 %), por encima del límite de 5 que se fijó. Toda esa diferencia viene del 6.5 % de consultas que ningún contenido reconoce. Sobre lo que sí responde, la diferencia es de 1 punto (análisis hecho después de ver los resultados).

## Montaje

- 24 módulos (12 piezas × 2), entrada por receptor y recorrido R3.
- **Exploración por muestreo de Thompson** con los éxitos e intentos efectivos leídos del directorio: sale de la memoria, sin tasa fija.
- **Corriente en línea de 6000 consultas** sorteadas con reposición, usando una variante al azar como pista.
- **Deriva en t = 3000:** en 7 dominios (candle, capsules, chewinggum, pcb1, pcb2, pcb3, pipe_fryum), el mejor módulo invierte su respuesta con probabilidad 0.5. La misma secuencia de inversiones se usa para todos los métodos.
- **Olvido:** al entrar una transacción, se resta exactamente la más vieja (la operación verificada en `olvido_privacidad`).
- **Rival:** bandido central de Thompson por dominio, que conoce el dominio verdadero de cada consulta (una ventaja que la memoria no tiene), sin ventana y con ventana.

## Resultados

**Acierto en línea por tramo (%):**

| método | antes (2000–3000) | justo después (3000–3500) | recuperación (3500–4500) | final (5000–6000) |
|---|---|---|---|---|
| memoria sin olvido (F0) | 85.9 | 62.2 | 70.9 | 69.9 |
| memoria, ventana 300 | 83.7 | 65.4 | 73.6 | 70.6 |
| memoria, ventana 600 | 84.1 | 61.2 | 74.6 | 72.3 |
| **memoria, ventana 1200** | 85.2 | 62.8 | 73.0 | **74.3** |
| bandido central sin ventana | 91.8 | 63.8 | 72.9 | 75.4 |
| bandido central, ventana 300 | 90.4 | 70.2 | 78.9 | 78.9 |
| bandido central, ventana 600 | 90.7 | 66.4 | 79.9 | 79.4 |
| **bandido central, ventana 1200** | 91.5 | 65.8 | 80.1 | **80.5** |
| oráculo | 92.1 | 78.6 | 83.1 | 81.2 |

La memoria lee 1.04–1.27 directorios por consulta. 317 de las 6000 consultas (5.3 %; 65 de las 1000 finales, 6.5 %) no tienen ningún módulo cuyo contenido las contenga; cuentan como fallo.

**Fracción al mejor módulo vigente en los dominios con deriva** (tramos de 250; la deriva está entre el 4.º y el 5.º):

| método | antes de la deriva | primer tramo después | recupera ≥ 70 % a los |
|---|---|---|---|
| memoria F0 | 80–82 % | 27.6 % | **nunca** (termina en 54 %) |
| memoria, ventana 300 | 56–66 % | 42.8 % | nunca (ruido alrededor del 60 %) |
| memoria, ventana 600 | 68–75 % | 31.0 % | 1750 pasos |
| **memoria, ventana 1200** | 72–75 % | 29.7 % | **1250 pasos** (termina en 71–78 %) |
| bandido sin ventana | 98–99 % | 5.2 % | nunca |
| bandido, ventana 300 / 600 / 1200 | 73–99 % | 17–33 % | 250 / 750 / 1000 pasos |

**Análisis hecho después de ver los resultados:** acierto en el tramo final **sobre lo respondido**: memoria con ventana de 1200, 79.5 %; bandido con ventana de 1200, 80.5 %; memoria sin olvido, 74.8 %.

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| PD1 | antes de la deriva todas prefieren al mejor (≥ 70 %) | **En parte**: F0 80 %, ventanas de 600 y 1200 de 68 a 75 %, **ventana de 300 de 56 a 66 %** (con 300 transacciones hay poca evidencia) |
| PD2 | sin olvido no se recupera, o tarda > 1500 | **Se cumple**: nunca |
| PD3 | con ventana se recupera en ≤ 1000 pasos, más rápido con W chica | **No se cumple tal cual**: 1250 (W = 1200) y 1750 (W = 600); W = 300 nunca, porque no llega a preferir con claridad |
| PD4 | la memoria con ventana a ≤ 3 puntos del bandido con la misma ventana | **No se cumple**: 6.2 puntos (sobre lo respondido, 1.0) |

**Criterio:**
- Primera parte («con ventana se recupera en ≤ 1500 pasos y sin olvido no»): **se cumple** con W = 1200 (1250 pasos contra nunca).
- Segunda parte («a ≤ 3 puntos del bandido con ventana en el tramo final»): **no se cumple**, y por la letra queda dentro de la cláusula de refutación (más de 5 puntos: 6.2).

**Veredicto por la letra:** el olvido exacto **es** el mecanismo que permite adaptarse (sostenido). Pero el sistema completo **no** iguala al bandido central (refutado por 1.2 puntos sobre el límite de 5). La causa está identificada: consultas sin candidato por cobertura del contenido, no el mecanismo de adaptación.

## Lectura

1. **Sin olvido, la memoria queda presa de su historia.** Igual que el bandido sin ventana: la evidencia vieja del módulo que era bueno pesa más que la nueva. Con olvido exacto, la evidencia que decide es la reciente, y el sistema vuelve a preferir al módulo que ahora es mejor. Es la primera vez que el olvido exacto, demostrado como operación en `olvido_privacidad`, funciona como **mecanismo** del sistema.
2. **La ventana tiene un compromiso claro.** Con W = 300 hay poca evidencia y la preferencia es ruidosa antes y después. Con W = 1200 la preferencia es estable y la recuperación tarda más. Es el mismo compromiso que tiene el bandido con ventana, y en la memoria se ve más fuerte, porque la evidencia se reparte entre directorios.
3. **El bandido central se adapta más rápido** (250–1000 pasos), porque conoce el dominio verdadero y junta toda la evidencia de un dominio en un solo lugar. La memoria no conoce el dominio: la evidencia está distribuida y se lee del primer directorio con soporte.
4. **El 6.5 % de consultas sin candidato es el límite principal**, y es de la percepción. El contenido de cada módulo son normales de su pieza, y algunas imágenes con falla no caen en ninguna envolvente. Sobre lo respondido, la memoria con ventana queda a 1 punto del bandido central.

## Lo que esto aporta a la línea

Con esta etapa, el sistema transactivo de memorias asociativas tiene demostradas, en la misma flota:
- ruteo con 1–3 consultas y aprendizaje de calidad mejor que un router central (etapa 2);
- abstención ante lo desconocido (100 %);
- adopción de módulos nuevos y tolerancia a bajas (piloto);
- **adaptación a la deriva por olvido exacto** (aquí).

Lo que falta para igualar a un rival central es **cobertura**. Las consultas que ningún contenido reconoce se pierden. Mejorarlo es una pregunta de percepción (que el contenido cubra también las piezas con falla) y de lectura (un respaldo tolerante en el contenido), no del mecanismo transactivo.

## Notas

- La ventana se mide en transacciones globales (cada una registra 16 variantes en 2 a 4 directorios). Se olvida restando exactamente lo que se sumó.
- El bandido central recibe el dominio verdadero de cada consulta. Es el rival estándar con información privilegiada; la memoria tiene que reconocer el dominio con su contenido.
- Una sola semilla para la corriente y para la deriva. Las fracciones por tramo en los dominios con deriva salen de unas 140–150 consultas por tramo.
