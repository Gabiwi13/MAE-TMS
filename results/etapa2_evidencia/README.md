# Etapa 2: acumular evidencia y entradas por receptor

Después de la etapa 1 quedaban dos alternativas para conciliar costo y calidad, ambas con propiedades de la memoria:
- **R4:** leer directorios uno por uno y parar cuando la memoria ya distingue al mejor (intervalo de Wilson sobre cuentas efectivas leídas de las proyecciones).
- **Entrada por receptor:** la consulta llega a un módulo cuyo contenido la reconoce, en vez de a uno al azar.

Diseño, predicciones y criterio fijados antes de correr en [`propuesta_etapa2_evidencia.md`](../../propuesta_etapa2_evidencia.md). Script: [`run_etapa2_evidencia.py`](../../run_etapa2_evidencia.py).

**Resultado en una línea:** con **entrada por receptor**, el ruteo dirigido (R3) **cumple por primera vez el criterio completo**: 85.7 % de acierto (2.5 puntos del router central), 2.5 lecturas por consulta (mediana 1), 73.4 % al mejor módulo y 100 % de abstención ante lo desconocido. **R4 no aporta nada**: para siempre en el mismo punto que R3, porque la memoria toma la ausencia de evidencia sobre el otro módulo como si la decisión fuera clara.

## Verificación

Con entrada al azar, la flota se reconstruyó igual que en el piloto (790 transacciones; R2 80.80 %; R3 igual que en la etapa 1). Con entrada por receptor se reaprendió desde cero, con las mismas consultas y la misma semilla (790 transacciones).

## Resultados (823 consultas conocidas, 756 desconocidas)

**Entrada al azar:**

| lectura | acierto | abst. conocidas | acierto de lo respondido | abst. desconocidas | costo medio (mediana) | respaldo por contenido | al mejor |
|---|---|---|---|---|---|---|---|
| R2 (suma el círculo) | 80.8 | 8.9 | 88.7 | 100 | 19.2 (19) | — | **79.0** |
| R3 (dirigido) | 83.4 | 3.0 | 86.0 | 100 | 11.6 (7) | 14.2 % | 54.7 |
| R4, z = 1.0 | 83.4 | 3.0 | 86.0 | 100 | 11.7 (7) | 14.2 % | 54.7 |
| R4, z = 1.96 | 83.4 | 3.0 | 86.0 | 100 | 11.7 (7) | 14.2 % | 54.7 |
| router central | 88.3 | 1.2 | 89.4 | 100 | central | — | 71.6 |

**Entrada por receptor:**

| lectura | acierto | abst. conocidas | acierto de lo respondido | abst. desconocidas | costo medio (mediana) | respaldo por contenido | al mejor |
|---|---|---|---|---|---|---|---|
| R2 (suma el círculo) | 80.9 | 10.6 | 90.5 | 100 | **2.0** (2) | — | **80.4** |
| **R3 (dirigido)** | **85.7** | 4.5 | 89.7 | 100 | **2.5** (1) | 5.8 % | **73.4** |
| R4, z = 1.0 | 85.5 | 4.5 | 89.6 | 100 | 3.1 (2) | 5.8 % | 73.4 |
| R4, z = 1.96 | 85.5 | 4.5 | 89.6 | 100 | 3.1 (2) | 5.8 % | 73.4 |
| router central | 88.2 | 1.2 | 89.3 | 100 | central | — | 63.6 |
| compuerta aprendida | 88.7 | 2.2 | 90.7 | 100 | central | — | 100 |
| cota «todos» con la pieza verdadera (no es rival) | 86.3 | 4.7 | 90.6 | 100 | 24 | — | 76.2 |

«Todos» conoce la pieza verdadera: entre los módulos que contienen la consulta, solo considera los de esa pieza (ver las notas del piloto). Es una cota, no un rival, y es la misma con ambos modos de entrada.

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| PE4 | con entrada al azar, R4 entre R3 y R2 (65–75 % al mejor, 5–10 lecturas) | **No se cumple**: R4 = R3 (54.7 %, 11.7) |
| PE5 | con receptor, el costo baja mucho, se conserva la calidad y R4 es la mejor combinación | **Se cumple en costo y calidad** (2–3 lecturas, 73–80 % al mejor). **R4 no es mejor que R3**: son iguales |
| PE6 | abstención ante lo desconocido ≥ 95 % | **Se cumple**: 100 % en todos los casos |

**Criterio** (≤ 3 puntos del central de su modo, costo ≤ 6, ≥ 70 % al mejor, desconocidas ≥ 95 %):

| combinación | diferencia con el central | costo | al mejor | ¿sostenido? |
|---|---|---|---|---|
| azar · R2 / R3 / R4 | 7.5 / 5.0 / 5.0 | 19.2 / 11.6 / 11.7 | 79.0 / 54.7 / 54.7 | no |
| receptor · R2 | 7.3 | 2.0 | 80.4 | no (acierto) |
| **receptor · R3** | **2.5** | **2.5** | **73.4** | **sí** |
| receptor · R4 (z = 1.0 y 1.96) | 2.7 | 3.1 | 73.4 | sí (igual que R3) |

## Lectura

1. **Dónde entra la consulta decide si la descentralización funciona.** Con entradas al azar, cada directorio guarda unas 65 transacciones repartidas en 12 dominios, y cada módulo «conoce» a casi todos. Con entrada por receptor, cada directorio guarda experiencia de **su zona**: el círculo se reduce a los módulos del dominio, el costo baja de 12–19 a 2–3 lecturas, y la evidencia de calidad queda concentrada donde se necesita. Es la idea de Wegner en su forma natural: le pregunta primero quien recibe el problema y sabe de él, y ese consulta a quien sabe que lo hace bien.
2. **La preferencia por calidad sobrevive con lecturas baratas** cuando la evidencia está concentrada (R3: 73.4 % al mejor con 1 lectura de mediana), y supera al router central con las mismas transacciones (63.6 %).
3. **El acierto queda a 2.5 puntos del central.** Casi toda la diferencia es abstención en lo conocido (4.5 contra 1.2 %): lo que responde, lo responde igual (89.7 contra 89.3 %).
4. **R4 falla por una razón de fondo.** Para cuando un solo módulo tiene soporte en lo leído, y con evidencia escasa eso pasa casi siempre al primer directorio. La memoria no distingue «no hay evidencia del otro módulo» de «el otro módulo es peor». Para separar esos dos casos haría falta registrar también los fracasos como evidencia negativa, y eso hoy no tiene forma en la memoria de directorio.
5. **Lo que hay que declarar siempre:** encontrar el receptor no se contó en el costo. En una planta es dónde llega la pieza (la estación de su línea). Si el sistema tuviera que encontrarlo preguntándole al contenido de todos, costaría 24 consultas de contenido.

## Estado de la línea

Con esta etapa, el sistema transactivo de memorias asociativas cumple el criterio que se fijó para considerarlo un organizador viable de una flota de módulos:
- rutea con un costo de 2–3 consultas;
- aprende qué módulo lo hace mejor, mejor que un router central con las mismas transacciones;
- se abstiene ante el 100 % de lo desconocido;
- adopta módulos nuevos y tolera bajas (piloto).

Queda por delante lo que lo haría un aporte completo: aprender en línea con deriva usando el olvido exacto (etapa 2 del plan), la escala a más de 100 módulos y heterogéneos, y la evidencia negativa para que «sin evidencia» no se lea como «claro».

## Notas

- Una sola semilla. Las cifras de preferencia salen de 7 dominios con diferencia de ≥ 5 puntos.
- R3 y R4 usan solo proyecciones, soportes y conteos de las memorias. El intervalo de Wilson se aplica sobre las cuentas efectivas leídas de las proyecciones; z se fijó antes (1.0 y 1.96).
- La compuerta aprendida llega a 100 % al mejor con entrada por receptor porque sus tasas globales por dominio ordenan bien a los módulos en esta corrida. Es central y no tiene abstención por zona.
