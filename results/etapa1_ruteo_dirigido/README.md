# Etapa 1: ruteo dirigido, lectura tolerante y respaldo por contenido

El piloto mostró que la flota aprende qué módulo lo hace mejor (79 % al mejor), pero consultaba 19 de 24 módulos y se abstenía en el 8.9 % de lo conocido. Aquí se intenta bajar el costo y la abstención **solo con propiedades de la memoria**: leer primero el directorio propio, preguntar a los conocidos en el orden de los conteos, tolerar ξ coordenadas sin soporte y recurrir al reconocimiento del contenido si nadie sabe. Diseño, predicciones y criterio fijados antes de correr en [`propuesta_etapa1_ruteo_dirigido.md`](../../propuesta_etapa1_ruteo_dirigido.md). Script: [`run_etapa1_ruteo_dirigido.py`](../../run_etapa1_ruteo_dirigido.py).

**Resultado en una línea:** el ruteo dirigido baja la abstención (8.9 → 3.0 %) y el costo (19.2 → 11.6 lecturas; mediana 7), y sube el acierto (80.8 → 83.4 %). Pero **pierde la preferencia por el mejor módulo** (79.0 → 54.7 %, casi azar) y queda 4.9 puntos bajo el router central. **No cumple el criterio.** La preferencia por calidad necesita juntar la evidencia de varios directorios; leer uno solo es más barato, pero no alcanza para distinguir calidad.

## Verificación

El piloto se reconstruyó con la misma semilla y dio exactamente las mismas cifras (790 transacciones; acierto de R2 80.80 %). R3 se evaluó sobre las mismas consultas y con la misma entrada que R2 y los rivales.

## Resultados (823 consultas conocidas, 756 desconocidas)

| método | acierto | abstención conocidas | acierto de lo respondido | abstención desconocidas | costo medio | respaldo por contenido | al mejor módulo |
|---|---|---|---|---|---|---|---|
| R2 del piloto (suma el círculo) | 80.8 | 8.9 | 88.7 | 100.0 | 19.2 | — | **79.0** |
| **R3, ξ = 0** | 83.6 | 3.4 | 86.5 | 100.0 | 12.6 | 17.0 % | 56.3 |
| **R3, ξ = 1** | 83.4 | **3.0** | 86.0 | 100.0 | **11.6** | 14.2 % | 54.7 |
| R3, ξ = 2 y 3 | 83.4 | 3.0 | 86.0 | 100.0 | 11.5 | 14.0 % | 54.8 |
| router central kNN | **88.3** | 1.2 | 89.4 | 100.0 | (central) | — | 71.6 |
| compuerta aprendida | 87.8 | 2.2 | 89.8 | 100.0 | (central) | — | 85.7 |
| cota «todos» con la pieza verdadera (no es rival) | 86.3 | 4.7 | 90.6 | 100.0 | 24 | — | 76.2 |

«Todos» conoce la pieza verdadera: entre los módulos que contienen la consulta, solo considera los de esa pieza (ver las notas del piloto). Es una cota, no un rival.

Directorios leídos por R3 en consultas conocidas: mediana 7, percentil 90 de 17–18 y máximo 22. El costo medio sube por el respaldo por contenido, que pregunta a los 24 módulos en el 14–17 % de las consultas. Pasar de ξ = 1 a ξ = 3 no cambia casi nada.

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| PE1 | 2 a 4 directorios en promedio; respaldo en < 10 % | **No se cumple**: mediana 7, media 11.6 contando el respaldo, que se usa en el 14 % |
| PE2 | con ξ = 1 o 2, abstención en lo conocido < 3 %, desconocidas ≥ 95 % | **En el borde**: 3.0 % y 100 % |
| PE3 | la preferencia por el mejor baja algo pero queda ≥ 70 % | **No se cumple**: cae a 54.7 % |

**Criterio** (para algún ξ: ≤ 3 puntos del central, costo ≤ 6, ≥ 70 % al mejor, desconocidas ≥ 95 %): **no sostenido** con ningún ξ. Fallan las tres primeras condiciones: diferencia de 4.7–5.0 puntos, costo de 11.5–12.6 y 54.7–56.3 % al mejor.

## Lectura

1. **Hay una tensión entre costo y calidad, y es una propiedad del sistema, no un detalle del código.** La tasa de éxito local se estima con las transacciones registradas. Como las entradas se sortean entre 24 módulos, cada directorio guarda unas 65 transacciones repartidas en 12 dominios: muy poca evidencia por dominio para distinguir dos módulos que difieren en 10 o 15 puntos. R2 junta la evidencia de unos 19 directorios y distingue calidad; R3 lee uno y no.
2. **Lo que sí funcionó:** pedirle primero al propio directorio y a los conocidos en orden de conteos baja la abstención y sube el acierto, porque casi siempre alguien sabe del dominio. La lectura tolerante aporta poco más allá de ξ = 1.
3. **El respaldo por contenido es caro** (pregunta a todos) y se necesita en el 14 % de los casos: los directorios no cubren todas las zonas del espacio.
4. **Lo que implica para el diseño:** con entradas al azar, la evidencia de cada módulo es escasa y está dispersa. Las salidas que siguen siendo propiedades de la memoria son:
   - **juntar evidencia a lo largo del recorrido** hasta que la decisión deje de ser ambigua, con el criterio de ambigüedad sacado de las propias proyecciones (como los tres estados del exp23);
   - **concentrar las transacciones**: que una consulta entre por el módulo cuyo contenido la reconoce, así cada directorio acumula experiencia de su zona. Eso cambia cómo llegan las consultas, no la memoria, y habría que justificarlo para una planta.

## Notas

- R3 y sus reglas de recorrido (orden por conteos, respaldo por contenido, desempate por peso de reconocimiento) se definieron para esta etapa. No están en el código oficial y solo leen proyecciones, soportes y conteos de las memorias.
- Para guardar la entrada de cada consulta se agregó un campo al registro de `run_piloto_modulos.evaluate`. No cambia ningún resultado del piloto.
- Una sola semilla.
