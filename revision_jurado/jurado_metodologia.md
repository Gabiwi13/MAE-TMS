# Dictamen de jurado: metodología y validez (sesión en la nube, 2 nov 2026)

Copia del último mensaje de la sesión «Jurado: metodología y validez de la tesis», sobre `una-hetero` en el commit 62995a8.

## 1. Veredicto
Aprobar con correcciones mayores. El sistema está bien construido y documentado, y declara limitaciones con franqueza, pero tres resultados centrales dependen del diseño de la evaluación: la ventaja en clase sobre la EHAM única, el crecimiento de la precisión madura con N y la generalización a objetos nuevos. Además, las conclusiones atribuyen al mecanismo un mérito que exp19 asigna en buena parte al codificador supervisado. Casi todo se resuelve reanalizando `results/`; unas pocas cosas necesitan corridas de horas.

## 2. Fortalezas
- Hay diseño preregistrado: exp11 §8, exp16 §6 y la lesión (`results/homo_marginal/README.md`), y los cambios posteriores al piloto están declarados.
- Hay controles internos: en exp16, objeto nuevo contra conocido; en exp11, tres brazos con un juez 1-NN.
- Se reportan resultados negativos: κ, la división entre mem.mean, el árbitro y el margen de exp15, y el costo de τ.
- Se declaran las limitaciones que buscaría un jurado: dentro de muestra, partición por imagen (f), selección sobre el conjunto de prueba (g) y rescate con el vocabulario propio (h).
- Unas 40 cifras cotejadas contra `results/` coinciden.

## 3. Observaciones mayores

### M1. En exp11, la clase correcta del protocolo se calcula solo sobre las consultas que responde
- **Dónde:** 05:497-499 y 522-530; 06:189-193; 07:60-63 («clasifica algo mejor, 1.4 puntos con 200»).
- **Evidencia:**
  - `run_experiment11_monolithic.py:597` usa como denominador las consultas respondidas. El protocolo responde el 98.4–98.7 % y la EHAM única el 100 %.
  - Recalculado sobre las 171 consultas, con no respuesta contada como fallo: EHAM única 97.6 / 97.5 / 97.6 / 96.9; protocolo 95.3 / 97.4 / 97.4 / 97.0.
  - Con N=200 la diferencia es +0.1 [−2.9, +3.1] (bootstrap pareado por consulta), y con N=25 la EHAM única queda arriba.
  - La distancia al oráculo pasa a 4.7, 2.6, 2.6 y 3.0 puntos.
  - Los intervalos salen de 10 semillas que solo cambian el muestreo del recuerdo; la formación es determinista.
  - Así se cumple la condición 1 del criterio preregistrado (§8). La tesis no queda refutada, porque d_nn sí separa los brazos, pero en clase hay empate.
- **Qué cambiar:** reportar la clase correcta sobre el total, o las dos versiones junto con la cobertura; usar McNemar; quitar «clasifica algo mejor». Lo defendible es la fidelidad (d_nn), el dominio ajeno y el fuera de dominio.

### M2. En la calibración, N cambia a la vez la formación del directorio y la dificultad del conjunto evaluado
- **Dónde:** 05:19-23, 72-90, 147-150 y 256-260; 06:86-90; 07:49-51; main:85-89.
- **Evidencia:**
  - La fase madura se evalúa sobre las primeras N consultas (`run_ablation.py:264-268`), y la proporción que trae el nombre de la clase es de 10/15/15/50 % para N = 50/100/200/400.
  - La precisión temprana, que no depende del directorio, sube de 82.5 a 90.0 % entre N=200 y N=400. Eso implica 195/200 aciertos en las consultas 201–400, frente a 165/200 en las primeras 200.
  - D y G sortean del banco completo, donde el 51 % trae el nombre de la clase, así que su ventaja refleja consultas más fáciles.
  - En 7 de las 9 condiciones la desviación estándar es 0: las cinco semillas no replican nada.
- **Qué cambiar:** fijar un conjunto de evaluación reservado e independiente de N; sortear la formación con semillas que de verdad varíen; reportar la diferencia madura menos temprana sobre las mismas consultas; retirar «hace falta el banco completo»; reinterpretar D y G.

### M3. El banco de texto está alineado con el vocabulario de llenado, las reservadas no lo representan y faltan líneas base
- **Dónde:** 04:170-189; 05:28-29; 07:17-18.
- **Evidencia:**
  - El nombre de la clase aparece en 208 de 411 consultas, pero en 150 de las 171 reservadas (88 %), porque se reserva la cola de cada lista. Por eso el 97.0 % fuera de muestra supera al 93.0 % dentro de muestra.
  - 399 de 411 consultas tienen una palabra del vocabulario de su clase, y 362 una exclusiva de ella.
  - Una línea base de coincidencia exacta de tokens (cálculo del revisor) da 80.5 % en las 400, 72.5 % en las 80 y 91.2 % en las 171.
  - No hay líneas base ajenas a la EAM, ni una comparación del directorio contra una tabla de conteos. La revisión científica del repositorio, en sus afirmaciones 8 y 9, marca que en aplicaciones el directorio no le gana a contar.
- **Qué cambiar:** agregar líneas base léxica, coseno de fastText y tabla de conteos; rehacer la partición reservada con un sorteo estratificado; idealmente, un banco nuevo escrito por terceros.

### M4. En el hemisferio visual, el codificador es supervisado y vio todos los objetos, así que exp16 tiene fuga
- **Dónde:** 04:127-142; 05:374-381 y 433-453; 06:287-300; main:94-96; 07:106-110.
- **Evidencia:**
  - La pérdida es MSE + 0.1·CE sobre todo train, con los 10 objetos de cada clase (`src/stage2_encoder.py`).
  - Exp16 no reentrena el codificador por pliegue.
  - En exp19 (no citado), con ImageNet + PCA: enrutamiento 96.2 → 80.5 %, falsos 2 → 83, fase A 99.9 → 90.2 %, evocación 97.4 → 83.5 % y objetos nuevos 89.2 → 60.8 %, con 14.4 % de falsos.
  - El codificador con CLS_WEIGHT=0 nunca se corrió de punta a punta.
- **Qué cambiar:** reentrenar el codificador por pliegue en exp16 o entrenarlo solo con los objetos de llenado; reportar exp19; reformular «sin clasificadores supervisados».

### M5. Varias decisiones de diseño se tomaron mirando los conjuntos que luego se reportan
- **Dónde:** 06:208-220 y 302-313; main:97-100; 05:59-67, 323-324 y 548-551; 04:94-110.
- **Evidencia:**
  - La doble compuerta se agregó (ddddeff, 21 sep 22:03) después de ver dos fugas en esas mismas 40 consultas (4732739, 21 sep 18:16).
  - McNemar exacto para el fuera de dominio da p ≈ 0.03, con n = 40 y un banco escrito por quien sustenta.
  - El punto de control del codificador, las 16 variantes, B1, el rescate léxico y N=200 se eligieron con datos de evaluación.
- **Qué cambiar:** declarar las decisiones posteriores a ver resultados; hacer la partición de validación; confirmar al final con bancos nuevos e intactos.

### M6. Trazabilidad: la contribución 4 promete más de lo que el repositorio permite verificar
- **Dónde:** 01:98-104; 04:215-230; 05:641-668; 07:81-83.
- **Evidencia:**
  - `stage7_bidirectional.log` está ignorado por `.gitignore:64` (`*.log`), así que no está en el repositorio.
  - Los modelos no están versionados.
  - La corrida de costo midió tiempo, no resultados, y recalculó la escala con 16 variantes.
  - El README raíz contradice la tesis: 93.5 % para B1, 13.2 % para apple, «M 97.4 vs T 97.5» y que el codificador movió pear de 52 a 86 %.
- **Qué cambiar:** versionar el log y publicar los modelos con sus hashes; hacer una réplica desde cero con tolerancias; actualizar el README.

### M7. Algunas conclusiones van más allá de la evidencia
- **Dónde:** main:101-103; 06:5-24; 07:9-10, 43-48 y 106-110; 01:89-96.
- **Evidencia:**
  - «Los límites están en la representación, no en el mecanismo» no se probó. El mecanismo tiene límites propios: la normalización externa, nombrar colapsa con un 1 % de daño y el contenido acepta 180 de 231 entradas degeneradas. Exp19 muestra que la representación fija tanto los límites como los aciertos.
  - En la fase B el primer círculo reúne los ocho directorios, lo que equivale a uno compartido; exp10 muestra que el perspectival como mucho iguala al compartido.
  - El «rechazo claro en ambas direcciones» descansa en 40 consultas propias y en sondas sintéticas, sin ninguna imagen real de otra categoría.
- **Qué cambiar:** reformular la conclusión, presentar el perspectival como algo que reproduce al compartido y acotar el rechazo a lo medido.

## 4. Observaciones menores
- **ι:** ι=0.25 da 82.5/83.8 % frente a 81.2/81.2 % con ι=0, y aun así se elige ι=0 (04:200-204). Además, 05:217-223 lee como efecto diferencias de 1 o 2 consultas de 80.
- **Orden de formación:** la invariancia ocurre por construcción, y D_raw es idéntico a la condición intercalada.
- **Condiciones:** F ≡ A y G = D + B1, así que son 7 condiciones efectivas, no 9.
- **Evocación:** la métrica es laxa (top-3, palabras compartidas) y casi queda implicada por el enrutamiento. Conviene la versión estricta y el nivel de azar.
- **05:579, «todas las cifras son de una sola memoria»:** exp15 y exp10 no se re-corrieron.
- **exp13:** la línea de control de su README dice «323364/8» y está mal. Su llenado difiere del oficial en 30–58 mil celdas por clase.
- **Lesión:** «el mismo daño» se aplica a memorias de tamaño distinto, la lectura usa solo la primera coordenada y las fracciones 0.01–0.1 se agregaron tras el piloto.
- **06:254, «cierra el 90 % de la fuga»:** conviene dar también el total, 33 de 231 entradas siguen aceptadas después de τ.
- **Imagen → texto en exp11:** los brazos tienen coberturas distintas y el directorio no lleva variantes.
- **Rescate léxico:** el costo corresponde a quitar sus dos vías a la vez.
- **Fidelidad:** cuenta como coincidencia un rechazo en las dos fases, y el «ideal 12.5 %» debería ser la proporción real.
- **Versiones que faltan:** el modelo de fastText (wiki-news-subwords-300), el de spaCy, la variante de ETH-80 (cropped-close128) y el commit de `hetero_lib`.
- **Resumen:** junto al 96.2 % debería decir «vistas nuevas de objetos conocidos».

## 5. Preguntas para la defensa
- ¿Qué queda de la ventaja en clase si se calcula sobre las 171 consultas?
- ¿Cómo separa la formación del directorio del cambio en la dificultad de las consultas?
- ¿Cuánto dan líneas base sin memoria?
- ¿Quién escribió el banco de consultas y con qué acceso al vocabulario?
- En exp16, ¿cuánto cae la cobertura si se reentrena el codificador sin ese objeto? ¿Por qué no aparece exp19?
- ¿Cómo sostiene «sin clasificadores supervisados»?
- ¿Qué decisiones se tomaron después de ver los datos de evaluación?
- ¿Qué aporta el directorio perspectival frente al compartido?
- ¿Qué experimento distingue representación de mecanismo?
- ¿Se puede reproducir 631/656 sin los modelos?
- ¿Por qué se quedó ι = 0?
- ¿Cómo responde el sistema a fotos reales de otras categorías?

