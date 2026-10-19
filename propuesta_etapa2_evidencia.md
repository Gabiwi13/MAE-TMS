# Etapa 2: acumular evidencia hasta que la decisión sea clara, y entradas por receptor

**Fecha:** 19 de octubre de 2026
**Estado:** fijada antes de correr. Lo que cambie después se declara en el informe como desviación.

## 1. Pregunta

En la etapa 1, leer un solo directorio bajó el costo pero perdió la preferencia por calidad (55 % al mejor), y sumar todo el círculo (R2) la conserva (79 %) a un costo de 19 lecturas. ¿Hay un punto medio que salga de la propia memoria? Se prueban dos alternativas y su combinación:
- **R4, acumular evidencia:** leer directorios uno por uno y parar cuando la memoria ya distingue al mejor.
- **Entrada por receptor:** la consulta llega a un módulo cuyo contenido la reconoce, en vez de a uno al azar. Así cada directorio acumula experiencia de su propia zona.

## 2. Cantidades de la memoria

La proyección de un directorio suma conteos sobre las coordenadas definidas de la pista. Para cada módulo i:

> cuenta efectiva nᵢ = proyección en intentos / (coordenadas definidas × 16 variantes)
> éxitos efectivos sᵢ = proyección en éxitos / (coordenadas definidas × 16 variantes)

Son las transacciones registradas cerca de la pista, leídas de la memoria. Lo que se acumula a lo largo del recorrido son estas cuentas.

## 3. R4: acumular hasta que sea claro

Recorrido de la etapa 1: el directorio propio y luego los conocidos uno por uno en el orden de sus conteos, con lectura tolerante ξ = 1. Tras cada directorio con soporte, se suman sᵢ y nᵢ y se calcula para cada módulo con nᵢ > 0 el intervalo de Wilson de su tasa de éxito.

**Para** cuando:
- el líder (tasa máxima) tiene un límite inferior mayor que el límite superior de todos los demás con nᵢ > 0, o
- un solo módulo tiene soporte.

Si se acaban los conocidos, decide el líder con lo acumulado. Si nadie tiene soporte, se usa el respaldo por contenido de la etapa 1.

Nivel de confianza: z ∈ {1.0, 1.96}, barrido declarado; no se elige al ver el resultado.

## 4. Entradas por receptor

En aprendizaje y en evaluación, la consulta entra por un módulo **cuyo contenido la contiene**, al azar entre ellos; si ninguno la contiene, por uno al azar. Modela que en una planta la pieza llega a una estación que reconoce su tipo. Encontrar el receptor no se cuenta en el costo (es dónde llega la consulta), y se declara. Con este modo se reaprende la flota desde cero.

## 5. Combinaciones evaluadas

| entrada | lecturas |
|---|---|
| al azar (la del piloto, reconstruida) | R2 (suma el círculo), R3 (etapa 1, ξ = 1), R4 (z = 1.0 y 1.96) |
| por receptor | R2, R3, R4 (z = 1.0 y 1.96) |

Rivales con las transacciones de cada modo: router central kNN, compuerta aprendida y preguntarle a todos. Mismas consultas, reparto y semilla que el piloto.

## 6. Predicciones

- **PE4.** Con entrada al azar, R4 queda entre R3 y R2: preferencia de 65–75 % al mejor, con 5–10 lecturas.
- **PE5.** Con entrada por receptor, el costo baja mucho (el círculo de cada módulo se concentra en su dominio) y la preferencia por calidad se conserva, porque cada directorio tiene evidencia de su zona. R4 con receptor es la mejor combinación.
- **PE6.** La abstención ante lo desconocido sigue ≥ 95 % en todos los casos.

## 7. Criterio (el de las etapas anteriores)

Alguna combinación queda **sostenida** si cumple a la vez:
- acierto a ≤ 3 puntos del router central de su mismo modo;
- costo medio ≤ 6 lecturas por consulta conocida;
- ≥ 70 % al mejor módulo (dominios con diferencia de ≥ 5 puntos);
- abstención ante lo desconocido ≥ 95 %.

Si ninguna cumple, se reporta qué condición falla en cada una y se da por agotado el diseño con estas cantidades de la memoria.

## 8. Entregables

`run_etapa2_evidencia.py` y `results/etapa2_evidencia/{README.md, resumen.txt, resultados.json}`.
