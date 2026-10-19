# Etapa 1: ruteo dirigido, lectura tolerante y respaldo por contenido

**Fecha:** 19 de octubre de 2026
**Estado:** fijada antes de correr. Lo que cambie después se declara en el informe como desviación.

## 1. Pregunta

El piloto mostró que el directorio de intentos y éxitos aprende qué módulo lo hace mejor (79 % al mejor), pero consulta 19 de 24 módulos y se abstiene en el 8.9 % de lo conocido. ¿Se pueden bajar las consultas y la abstención **solo con propiedades de la memoria**, sin reglas fijas, sin perder la preferencia por calidad ni la abstención ante lo desconocido?

## 2. Restricción de diseño

Todas las decisiones salen de las memorias: de la proyección y el soporte de los directorios, de sus conteos, del parámetro ξ de la MAE y del reconocimiento del contenido. No hay reglas por pieza, tablas fijas ni umbrales ajustados al resultado. Las entradas se siguen sorteando entre los 24 módulos (el caso difícil).

## 3. Diseño

Misma flota, mismas consultas, mismo reparto aprendizaje/evaluación, misma semilla y misma fase de aprendizaje que el piloto (se reconstruye igual).

**R3, ruteo dirigido** (Wegner: preguntarle primero a quien uno sabe que sabe):
1. El módulo de entrada lee **solo su propio directorio**. Hay soporte si a lo más ξ coordenadas de la pista no tienen soporte; esas coordenadas se marcan como indefinidas y se proyecta el resto, como en `predict_tolerant`. Si hay soporte, decide con la lectura de calidad (proyección en éxitos / proyección en intentos) y consulta a ese módulo.
2. Si no hay soporte, pregunta a sus conocidos **uno por uno**, en el orden de su propio directorio (los módulos con más transacciones compartidas primero), y se detiene en el primero cuyo directorio tiene soporte. Ahí decide con la lectura de calidad de ese directorio.
3. Si ningún conocido tiene soporte, recurre al **contenido**: pregunta qué módulos contienen la pista (contención estricta, como en la fase de aprendizaje). Entre ellos, elige al de mejor tasa éxitos/intentos según los conteos de los directorios ya consultados. Si ninguno tiene conteos, elige al de mayor peso medio de reconocimiento. Si ninguno la contiene, se abstiene.

**Barrido de ξ ∈ {0, 1, 2, 3}**, reportado completo. ξ es el parámetro de tolerancia propio de la MAE.

**Costo de una consulta:** directorios leídos, más 24 si se usó el respaldo por contenido (se le pregunta a todos).

**Comparación:** R2 del piloto, router central kNN, compuerta aprendida y preguntarle a todos, sobre las mismas consultas y con la misma entrada.

## 4. Predicciones

- **PE1.** R3 consulta en promedio 2 a 4 directorios. El respaldo por contenido se usa en menos del 10 % de las consultas conocidas.
- **PE2.** Con ξ = 1 o 2, la abstención en lo conocido baja a menos del 3 %, y la abstención ante lo desconocido sigue ≥ 95 %.
- **PE3.** La preferencia por el mejor módulo baja algo respecto de R2 (79 %), porque se lee un solo directorio y hay menos evidencia, pero queda ≥ 70 %.

## 5. Criterio (el mismo del piloto)

Para algún ξ, R3 queda **sostenido** si cumple las tres condiciones:
- acierto a ≤ 3 puntos del router central;
- costo medio ≤ 6 consultas por consulta conocida;
- ≥ 70 % al mejor módulo (dominios con diferencia de ≥ 5 puntos), con abstención ante lo desconocido ≥ 95 %.

Si ningún ξ cumple, se reporta qué condición falla y por cuánto.

## 6. Entregables

`run_etapa1_ruteo_dirigido.py` y `results/etapa1_ruteo_dirigido/{README.md, resumen.txt, resultados.json}`.
