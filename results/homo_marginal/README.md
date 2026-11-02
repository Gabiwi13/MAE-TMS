# Memorias homo como marginal de la hetero (29 oct 2026)

**Pregunta:** ¿las memorias homo de cada agente guardan algo que su hetero no tenga? Con el llenado oficial, cada homo recibe los mismos registros que un lado de la hetero, así que debería ser su marginal.

**Método** (`run_homo_marginal.py`, solo lee `models/`; criterio declarado antes de correr en `plan_cierre_pesos_homo.md`, 29 oct):
- Se reemplaza cada homo por la marginal de la hetero de su agente: la latente suma la relación sobre los niveles de etiqueta; la de etiquetas, sobre los niveles latentes.
- Se repiten las lecturas oficiales, decisión por decisión, en 427 consultas de texto (411 del banco y 16 de la etapa 6) y 656 imágenes de test (652 pasan τ).
- Control: la corrida oficial repetida, con las mismas semillas.

## Las marginales

| Agente | Latente | Etiquetas: soporte | Factor |
|---|---|---|---|
| apple | idéntica | igual | 32–33 |
| car | idéntica | igual | 22–23 |
| cow | idéntica | igual | 30–31 |
| cup | idéntica | igual | 37–38 |
| dog | idéntica | igual | 21–22 |
| horse | idéntica | igual | 22–23 |
| pear | idéntica | igual | 94–95 |
| tomato | idéntica | igual | 82–82.4 |

La homo de etiquetas registra cada palabra una vez; la hetero empareja cada palabra con muchos latentes. Por eso la marginal es la homo multiplicada por un factor que no es el mismo en todas las celdas.

## Oficial contra marginal

| Lectura | Comparadas | Distintas | Control |
|---|---|---|---|
| Contención de texto (pista × agente) | 10 008 | 0 | 0 |
| Puntaje de texto, diferencia relativa máxima | 10 008 | 0.29 % | 0 |
| Ganador temprano | 427 | 0 | 0 |
| Destino del ruteo transactivo | 427 | 0 | 0 |
| Compuerta de contenido | 427 | 0 | 0 |
| Recuerdo texto → latente | 420 | 66 | 0 |
| Contención de imagen (imagen × agente) | 652 × 8 | 0 | 0 |
| Puntaje de imagen | 652 × 8 | 0 | 0 |
| Destino de imagen | 652 | 0 | 0 |
| Evocación top-3 | 652 | 0 | 0 |

Predicciones: (1) contención igual, se cumple; (2) imagen idéntica, se cumple; (3) en texto cambian los puntajes y las decisiones solo en empates, se cumple: ninguna decisión cambia.

**El recuerdo texto → latente** no estaba en la predicción. Usa los pesos de la homo de etiquetas para ponderar el muestreo; como el factor varía entre celdas, con la misma semilla el muestreo toma otro camino. En los 66 que difieren cambia en promedio el 14 % de las coordenadas (de 1.6 a 92 %), con diferencia máxima de 1 a 11 niveles de 32.

**Referencia agregada después de ver el resultado** (`run_homo_marginal_semilla.py`, `semilla.json`): con las homo oficiales, cambiar solo la semilla altera los 420 recuerdos (0 idénticos), con 3.09 niveles de diferencia media por coordenada. La marginal deja 354 idénticos, con 0.066. Su efecto sobre el recuerdo es unas 47 veces menor que el del azar del muestreo.

## ¿Cuándo agregan algo las homo? (criterio en el plan, 29 oct)

### A. Pesos y calidad del recuerdo (`run_pesos_recuerdo.py`, `pesos_recuerdo.json`)

Modelos oficiales. En las 404 consultas con ganador temprano se recuerda texto→latente con tres pesos y dos semillas. El latente recordado se compara por vecino más cercano (L1 por coordenada, en niveles de 32) con los 25 600 latentes de llenado. La corrida se hizo en dos invocaciones: las tres primeras pasadas vienen de una corrida detenida por falta de memoria, con el mismo código y las mismas semillas.

| Pesos | Acierto, clase verdadera | Vecino en la clase del agente | Distancia L1, semilla 0 | Distancia L1, semilla 100 000 |
|---|---|---|---|---|
| uniformes | 91.8 % | 100 % | 2.116 | 2.119 |
| homo | 91.8 % | 100 % | 2.150 | 2.178 |
| marginal | 91.8 % | 100 % | 2.150 | 2.177 |

- **El acierto no distingue los pesos.** El vecino más cercano siempre cae en la clase del agente que recordó (404 de 404). El acierto es igual al del ganador temprano en las seis pasadas.
- **Homo contra marginal:** la diferencia (0.00004 y 0.001) es mucho menor que la de cambiar la semilla (0.027).
- **Pesos contra uniformes:** con pesos, el recuerdo queda más lejos del llenado en las dos semillas: 0.034 y 0.059 niveles. Esa diferencia es mayor que la de las semillas.
- Predicción: se cumple en el acierto y entre homo y marginal. No se cumple «sin dirección clara»: con pesos el recuerdo queda un poco más lejos que con uniformes. La diferencia es pequeña (0.03–0.06 de 32 niveles) y no favorece a los pesos.

### B. Datos sin pareja (`run_homo_sin_pareja.py`, `sin_pareja.json`)

La hetero de cada agente se llena solo con las primeras 50 o 100 de sus 200 imágenes de llenado (con sus 16 variantes y el emparejamiento oficial). La homo latente se queda con las 200. Reconocimiento visual en las 652 imágenes de test con energía:

| Homo latente | Acepta su clase | Aceptaciones de otra clase | Rechazadas por todos |
|---|---|---|---|
| oficial (200 imágenes) | 98.6 % | 3 | 8 |
| marginal de la hetero con 100 | 97.1 % | 2 | 18 |
| marginal de la hetero con 50 | 92.8 % | 2 | 46 |

- La homo reconoce 10 vistas más (con 100) y 38 más (con 50) que la marginal. A cambio acepta 1 de otra clase más.
- **Ninguna de esas vistas extra se puede nombrar:** el recuerdo imagen→texto de la hetero reducida no reconoce ninguna (10 de 10 y 38 de 38). Esto es por construcción, no un hallazgo empírico. La proyección es un AND entre coordenadas: si un valor latente nunca se registró en la hetero, su rebanada es cero y anula toda la proyección.
- Predicción: se cumple. La homo acepta más vistas de su clase y algo más de otras, y las vistas extra son justo las que la hetero no puede nombrar.

Con datos sin pareja, la homo sí agrega algo: reconoce **«esto ya lo vi»** en vistas que el agente no puede nombrar. Las lecturas actuales de la hetero no pueden representar ese estado, porque para ellas lo que no se puede recordar no está contenido. La hetero sí podría guardarlo (D).

### C. Emparejamiento desigual (`run_emparejamiento_desigual.py`, `emparejamiento_desigual.json`)

La homo de etiquetas se queda como la oficial (cada palabra × su frecuencia). La hetero se vuelve a llenar con los mismos latentes y otro reparto de palabras:
- C1: todas las palabras, en proporción a 1/rango;
- C2: solo la primera mitad de las palabras.

Se corre el sistema con los pesos de la homo oficial y con los de la marginal de la nueva hetero, en las 411 consultas del banco (9 592 pares pista × agente).

| | C1 homo | C1 marginal | C2 homo | C2 marginal |
|---|---|---|---|---|
| Pares que la homo de etiquetas contiene | 1 025 | 1 025 | 1 025 | 703 |
| Pares que pasa la compuerta de la hetero | 1 025 | 1 025 | 703 | 703 |
| Ganador temprano correcto | 89.5 % | 91.0 % | 55.5 % | 55.2 % |
| Consultas rechazadas al inicio | 7 | 7 | 128 | 128 |

Homo contra marginal, decisión por decisión:

| | C1 | C2 |
|---|---|---|
| Contención de la homo distinta | 0 | 322 |
| Compuerta de la hetero distinta | 0 | 0 |
| Ganador temprano distinto | 8 de 411 | 5 de 411 |
| Destino del ruteo transactivo distinto | 0 | 0 |
| Compuerta del ruteo distinta | 0 | 0 |

- **C1:** el soporte es el mismo. Los pesos cambian de forma y mueven 8 ganadores tempranos (1.9 %). Neto, la marginal acierta 6 más (con el llenado oficial son 371 de 411). El ruteo transactivo no cambia en ninguna consulta.
- **C2:** la homo contiene 322 pares pista × agente que la hetero rechaza. En esos pares el agente conoce la palabra pero no puede evocar una imagen. La caída a 55 % viene de dejar sin pareja la mitad del vocabulario y es igual con los dos pesos.
- **Recuerdo:** como en A, el acierto es igual con los dos pesos y la distancia homo contra marginal queda dentro de la diferencia entre semillas:
  - C1: homo 1.759 y 1.757, marginal 1.746 y 1.761;
  - C2: homo 2.062 y 2.033, marginal 2.053 y 2.051.
- Predicción: se cumple en los dos casos.

### D. Lo sin pareja dentro de la hetero (`run_homo_borde.py`, `borde.json`)

La hetero reserva un valor indefinido por dominio, con su borde fijado en 1 («funciones parciales»). Todas sus lecturas usan solo el interior `[:m, :q]`. Se repite B, pero las imágenes de llenado que quedan sin pareja se registran con la palabra indefinida (NaN) en vez de omitirse. Se compara con la hetero de B, que solo recibe las emparejadas.

| | 100 de 200 emparejadas | 50 de 200 emparejadas |
|---|---|---|
| Registros en el borde, por agente | 1 600 | 2 400 |
| Agentes con interior, relación ι, medias y entropías iguales a B | 8 de 8 | 8 de 8 |
| Proyección desde las imágenes de test idéntica a B | 652 de 652 | 652 de 652 |
| Vistas extra de la homo sin recuerdo imagen→texto | 10 de 10 | 38 de 38 |
| Recuerdo idéntico a B en esas vistas | 10 de 10 | 38 de 38 |
| Agentes donde el borde es la misma tabla en cada coordenada de palabra | 8 de 8 | 8 de 8 |
| Agentes donde borde + marginal del interior = homo latente oficial, celda por celda | 8 de 8 | 8 de 8 |
| Reconocimiento con la marginal del interior | 97.1 %, 2 de otra clase, 18 rechazadas | 92.8 %, 2, 46 |
| Reconocimiento con borde + marginal | 98.6 %, 3, 8 | 98.6 %, 3, 8 |
| Decisiones distintas de borde + marginal contra la homo oficial | 0 de 652 × 8 | 0 de 652 × 8 |

- **La hetero sí guarda lo que llega sin pareja,** en su borde de valor indefinido. Ninguna lectura del sistema lo ve: todo lo que lee la hetero queda igual que en B.
- **El borde es una homo latente dentro de la hetero.** Sumado a la marginal de lo emparejado, reproduce exacta la homo oficial, y reconocer con esa tabla da las mismas decisiones que la homo oficial.
- Predicción: se cumple en los tres puntos.

### E. ¿Qué hace una homo que la hetero con borde no? (`run_homo_lesion.py`, `lesion.json`)

**Pregunta** (1 nov). Si las homo hacen algo que una sola hetero con borde no puede reproducir, se quedan. Si no, se reemplazan por lecturas de la hetero.

**Montaje.** Los 8 agentes. De las 200 imágenes de llenado, las primeras 100 (con sus 16 variantes) se emparejan como en el llenado oficial y las otras 100 llegan sin palabra.
- **B:** la hetero recibe las emparejadas; la homo latente, todas (es la oficial).
- **A:** una sola hetero; las sin pareja van a su borde. La homo latente se lee de ella (borde + marginal).

Solo se mide el lado de la imagen. Cada imagen va al agente de su clase: no interviene el ruteo.

**Consultas por agente:** la variante original de las 100 emparejadas y de las 100 sin pareja, y las imágenes de test de su clase con energía. Las de test de otras clases sirven solo para contar falsas alarmas.

**Lecturas:**
- **familiar:** la homo (o la lectura) contiene la imagen, con contención estricta como en el ruteo visual;
- **nombra:** el recuerdo imagen → texto de la hetero se reconoce, con los pesos de la homo (o de la lectura);
- **nombra bien:** además, alguna de las 3 palabras evocadas es del vocabulario de su clase.

**Parte 1, sin lesión.**
- Respuesta a cada imagen en A y en B: nombra, reconoce sin nombrar o rechaza.
- Completar: a cada imagen sin pareja se le deja indefinida la mitad de las coordenadas, se recupera desde la homo (o la lectura) y se mide el error en las coordenadas ocultas, contra la imagen original y contra otra imagen sin pareja del mismo agente.

**Parte 2, lesión.** Se destruye una fracción f ∈ {0.25, 0.5, 0.75, 1} de las celdas de la hetero, con la misma máscara en todas las condiciones:
- **B focal:** la hetero pierde las celdas y la homo queda intacta;
- **A al azar:** la única hetero pierde las celdas, del interior y del borde (el borde vuelve a su 1 fijo);
- **A desasociar:** el conteo de cada celda del interior elegida pasa a los dos bordes (imagen sin palabra y palabra sin imagen), y la celda queda en cero;
- **B global:** como B focal, y la homo pierde además la misma fracción de sus celdas.

**Predicciones** (escritas antes de correr):
1. **Sin lesión, A = B** en familiaridad, decisión por decisión, y en nombrar: el interior es el mismo y el borde no entra a la proyección. Las imágenes sin pareja quedan en «reconoce sin nombrar», por construcción.
2. **Completar no recupera esa imagen, ni en A ni en B.** El error contra la original es igual al error contra otra imagen del mismo agente. Una homo cuenta cada coordenada por separado y, al completar, sortea cada coordenada oculta de su columna: no tiene con qué distinguir esa imagen de otra.
3. **Lesión.** Nombrar cae con f en las cuatro condiciones.
   - B focal: la familiaridad no cambia con f (por construcción) y crece «reconoce sin nombrar».
   - A desasociar: igual, por construcción.
   - A al azar: la familiaridad cae con f. No sé cuánto: una celda de la lectura suma hasta 17 celdas de la hetero, así que puede caer más despacio que nombrar.
   - B global: la familiaridad cae más rápido que en A al azar, porque cada celda de la homo es una sola celda.

**Regla de decisión** (escrita antes de correr):
- Si en alguna lectura B logra algo que A no reproduce con ninguna de sus dos operaciones, se quedan las homo.
- Si A lo reproduce todo, se reemplazan. Que B focal conserve la familiaridad sin una operación específica se reporta como una elección de modelado, no como una razón de los datos.

**Cambios después de la prueba con un agente** (apple, 10 consultas por conjunto, f = 0.5), antes de la corrida completa:
- **Nombrar se lee de la proyección.** El recuerdo oficial con muestreo tarda ~22 s por imagen; la corrida completa habría tomado ~20 h por agente. El recuerdo oficial se reconoce si y solo si ninguna columna de la proyección queda vacía (el muestreo no rechaza después), así que «nombra» es el mismo criterio. Las palabras de «nombra bien» se evocan del prototipo de la proyección (el valor más probable por coordenada), no del muestreo.
- **Se agregan f = 0.01, 0.05 y 0.1.** Con f = 0.5, nombrar ya era 0 en las cuatro condiciones; las fracciones declaradas se mantienen.
- La prueba ya contradice la predicción 1 en un punto: 9 de 10 imágenes sin pareja se nombran. No es por construcción: la hetero las nombra igual que a las de test, porque se parecen a las emparejadas.

**Resultados** (8 agentes, ~7 min cada uno). En los 8, el interior de A es igual al de B y la lectura de A es la homo oficial celda por celda.

*Parte 1, sin lesión* (A y B dan lo mismo):

| Consultas | Familiar | Nombra | Reconoce sin nombrar | Rechaza |
|---|---|---|---|---|
| Emparejadas (800) | 800 | 800 | 0 | 0 |
| Sin pareja (800) | 800 | 722 | 78 | 0 |
| Test de su clase (652) | 643 | 590 | 53 | 9 |
| Test de otra clase (4 564) | 3 aceptadas | — | — | — |

- **A contra B, consulta por consulta:** 0 diferencias en familiaridad, en nombrar y en el prototipo, en las 2 252 consultas.
- **Sin pareja:** 78 de 800 quedan en «reconoce sin nombrar», de 3 (horse) a 23 (car) por agente. El resto lo nombra la hetero por parecido, igual que a las de test.
- «Nombra bien» coincide con «nombra» en todas las condiciones: cuando la proyección se reconoce, alguna de las 3 palabras del prototipo es de su clase. No agrega información y no va en las tablas.
- **Completar** (mitad oculta, las 800 sin pareja): error medio de 2.228 niveles contra la original y de 2.240 contra otra imagen del mismo agente. Más cerca de la original en 383, de la otra en 406. Igual en A y en B.
- Predicción 1: se cumple A = B. No se cumple que lo sin pareja quede sin nombre: 90 % se nombra.
- Predicción 2: se cumple. Ni la homo ni la lectura recuperan esa imagen; recuperan el promedio del agente.

*Parte 2, lesión.* Nombrar es igual en las cuatro condiciones, consulta por consulta.

| f | Nombra (emparejadas) | Familiar, emparejadas: B focal · A desasociar · A al azar · B global | Familiar, test: B focal · A desasociar · A al azar · B global |
|---|---|---|---|
| 0 | 800 | 800 · 800 · 800 · 800 | 643 · 643 · 643 · 643 |
| 0.01 | 64 | 800 · 800 · 800 · 416 | 643 · 643 · 642 · 341 |
| 0.05 | 0 | 800 · 800 · 800 · 32 | 643 · 643 · 643 · 29 |
| 0.1 | 0 | 800 · 800 · 799 · 0 | 643 · 643 · 640 · 1 |
| 0.25 | 0 | 800 · 800 · 795 · 0 | 643 · 643 · 638 · 0 |
| 0.5 | 0 | 800 · 800 · 675 · 0 | 643 · 643 · 533 · 0 |
| 0.75 | 0 | 800 · 800 · 15 · 0 | 643 · 643 · 12 · 0 |
| 1 | 0 | 800 · 800 · 0 · 0 | 643 · 643 · 0 · 0 |

- Con f = 0.01 también se nombran 61 de 800 sin pareja y 44 de 652 de test; con 0.05, ninguna.
- Aceptaciones de otra clase: 3 en B focal y A desasociar en todo f; en A al azar bajan a 2 con f = 0.25 y a 0 desde 0.5; en B global, 1 con f = 0.01 y 0 después.
- **Nombrar es lo más frágil:** con 1 % de las celdas destruidas se pierde el 92 %, y con 5 %, todo. La proyección es un AND: cada una de las 64 coordenadas de la imagen tiene que dejar apoyo en cada una de las 300 de la palabra.
- **La familiaridad leída de la hetero aguanta mucho más.** Con daño al azar en la única memoria (A al azar), entre f = 0.05 y 0.25 no se nombra nada y se reconocen 795 a 800 de 800 emparejadas. La disociación «pierdo la asociación, conservo la familiaridad» le sale sola a A, sin una operación específica. La familiaridad de A empieza a caer recién con f = 0.5.
- **La homo es la más frágil ante el mismo daño** (B global): 416 de 800 con f = 0.01, 0 con 0.1. Una celda de la homo es un punto único. Una celda de la lectura suma las de los 17 valores de palabra en esa coordenada.
- Predicción 3: se cumple en las cuatro condiciones. La distancia entre nombrar y la familiaridad de A es mucho mayor de lo que esperaba.

**Decisión según la regla.** A reproduce todo lo que hace B:
- sin lesión, consulta por consulta;
- con lesión focal, «desasociar» lo reproduce exacto en todo f;
- y el daño al azar lo reproduce sin operación específica hasta f = 0.25, cuando nombrar ya es 0 desde f = 0.05.

B focal solo se separa de A al azar desde f = 0.5, donde ya no queda nada que nombrar. **Las homo se reemplazan por lecturas de la hetero.** Con el mismo daño en todas las memorias, las homo son además lo primero que se pierde.

**No se midió:** el lado de las palabras; el recuerdo con muestreo (se usó el prototipo); lesiones que restan conteos en lugar de destruir celdas; una lectura que promedie las 300 coordenadas de palabra en vez de leer solo la primera.

## Lectura

Con el llenado oficial, las dos homo de cada agente se pueden calcular de su hetero sin cambiar ninguna decisión del sistema. Solo cambian los recuerdos muestreados, por la escala de los pesos. Los pesos tampoco mejoran el recuerdo: con pesos uniformes queda un poco más cerca del llenado (A).

Las homo agregan algo solo si reciben registros que la hetero no recibe:
- imágenes sin palabra: «lo vi pero no lo puedo nombrar» (B);
- palabras sin imagen: «conozco la palabra pero no puedo evocar la imagen» (C2).

Si solo cambia la proporción del emparejamiento (C1), el soporte es el mismo. Los pesos mueven 2 % de los ganadores tempranos y ninguna decisión del ruteo.

Ni siquiera eso exige una memoria aparte (D). La hetero guarda lo que llega sin pareja en su borde de valor indefinido, y ese borde más la marginal de lo emparejado es exactamente la homo oficial. Lo que falta en el sistema actual no es información, sino una lectura de reconocimiento que use el borde. Con esa lectura, una sola hetero por agente daría las mismas decisiones que la hetero más sus dos homo. Esto se midió del lado latente; el lado de etiquetas (C2) es simétrico por construcción, pero no se midió.

Interpretación, no medida: todo lo del agente puede vivir en una sola memoria conjunta, incluido lo que llega sin pareja, como sugiere la idea de un mismo espacio latente. Las homo son una forma de leer esa memoria, no un contenido que ella no pueda guardar.
