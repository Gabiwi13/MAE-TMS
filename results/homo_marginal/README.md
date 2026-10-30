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

Con datos sin pareja, la homo sí agrega algo: reconoce **«esto ya lo vi»** en vistas que el agente no puede nombrar. Es un estado que la hetero sola no puede representar, porque para ella lo que no se puede recordar no está contenido.

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

## Lectura

Con el llenado oficial, las dos homo de cada agente se pueden calcular de su hetero sin cambiar ninguna decisión del sistema. Solo cambian los recuerdos muestreados, por la escala de los pesos. Los pesos tampoco mejoran el recuerdo: con pesos uniformes queda un poco más cerca del llenado (A).

Las homo agregan algo solo si reciben registros que la hetero no recibe:
- imágenes sin palabra: «lo vi pero no lo puedo nombrar» (B);
- palabras sin imagen: «conozco la palabra pero no puedo evocar la imagen» (C2).

Si solo cambia la proporción del emparejamiento (C1), el soporte es el mismo. Los pesos mueven 2 % de los ganadores tempranos y ninguna decisión del ruteo.

Interpretación, no medida: si todo lo que entra al agente llega emparejado, basta una sola memoria conjunta, y lo que guardan las homo ya está en ella. Esto coincide con la idea de que todo puede vivir en el mismo espacio latente. Las homo solo dejan de ser redundantes para lo que llega sin pareja.
