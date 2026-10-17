# Experimento 17 — de la imagen a una palabra específica

Pregunta: la evocación imagen → palabra se reporta como top-3 con acierto de dominio (97.4 %). ¿Devuelve una palabra específica?

Por construcción, no podía: en el llenado oficial cada imagen se registra con la siguiente palabra de la lista de la clase (`label_seq[i % L]`). La pareja no dice nada de la imagen, y la memoria aprende «imágenes de la clase ↔ conjunto de palabras de la clase». El recuerdo es una mezcla por coordenada que luego se interpreta por coseno. El experimento mide qué tan lejos llega la palabra en tres condiciones: la palabra de siempre (A), una palabra arbitraria por objeto (B) y una palabra con significado visual, el color (C).

Lecturas usadas:
- **oficial**: `recall_from_right` (muestreo, ~17 s por imagen) y vecino por coseno en el diccionario.
- **prototipo**: argmax por coordenada de la misma proyección, después coseno.
- **soporte**: probabilidad media, coordenada por coordenada, que la proyección da a los valores de cada palabra candidata. Es determinista y rápida.
- **soporte normalizado**: soporte con la imagen ÷ soporte en la marginal de la propia memoria (la relación sumada sobre todo el lado latente). Es el análogo de B1. Se fijó de antemano como única variante.

## A — modelos oficiales, top-1 en vez de top-3

Las mismas 118 imágenes de test que dan el 97.4 % (15 por clase; 2 sin energía, 116 ruteadas, todas al destino correcto); 3 recuerdos por imagen con semilla fija.

| medida (oficial, diccionario crudo) | % |
|---|---|
| top-3 en el vocabulario de la clase (métrica oficial) | 97.4 |
| top-1 en el vocabulario de la clase | 96.0 |
| top-1 con palabra exclusiva de la clase | 85.9 |
| top-1 = nombre de la clase | 48.0 |
| mismo top-1 en los 3 recuerdos | 38.9 |

El dominio sale en top-1. La palabra no: cambia de un recuerdo a otro y el margen entre la primera y la segunda es mínimo (coseno, mediana 0.025). El nombre de la clase depende de la clase: dog 40/42, horse 42/45, car 33/39, pero apple 0/45 (gana «fruit»), cup 3/45 (gana «drink»), pear 9/42. El prototipo da casi lo mismo (nombre 52.6 %, dominio 97.4 %).

## B — una palabra arbitraria por objeto

El objeto k de cada clase recibe la k-ésima palabra exclusiva de su vocabulario y todas sus vistas se registran con ella (200 imágenes × 16 variantes por clase, latentes de exp16). Se evalúa en el agente de la clase verdadera; el azar es 10 %.

| lectura | vistas nuevas de objetos conocidos, top-1 / top-3 | vistas del llenado, top-1 / top-3 |
|---|---|---|
| soporte | **40.8 / 73.7** | 51.2 / 84.8 |
| oficial, palabras del agente | 35.4 / 65.8 | — |
| prototipo | 29.7 / 55.4 | 37.5 / 63.1 |

La memoria distingue objetos dentro de la clase (4 veces el azar), pero ni las vistas que memorizó devuelve bien (51 %). Los objetos de una clase se pisan en la envolvente por coordenada.

## Sonda: ¿el latente lleva el color?

80 objetos etiquetados a mano con un color dominante (`colores_borrador.json`, aprobado tal cual); 59 tienen color claro y 21 quedan fuera por dudosos. Paleta: red, green, yellow, orange, brown, white, black, gray. Leave-object-out con k = 5 vecinos; azar balanceado 12.5 %.

| representación | intra-clase, balanceada | global sin tomato, balanceada |
|---|---|---|
| latente continuo | 41.1 | 41.1 |
| latente cuantizado (memoria) | 41.2 | 41.0 |
| píxeles 16×16 | 40.6 | 43.7 |
| color medio del objeto (medida directa) | 47.0 | 47.6 |

El latente lleva casi todo el color que da medirlo directamente, y cuantizarlo no pierde nada. El techo lo pone el conjunto de datos: 9 de los 49 objetos (sin tomato) son los únicos de su color en su clase, y orange tiene un solo objeto.

## C — el color como palabra

Solo objetos con color claro; vectores fastText de las 8 palabras (en fastText se parecen: white–black coseno 0.93, red–yellow 0.88). Agente de la clase verdadera. Los porcentajes son sobre clases con más de un color (tomato, siempre rojo, queda fuera).

**Objetos conocidos** (41 vistas no usadas por clase):

| lectura | top-1 | balanceada |
|---|---|---|
| soporte | 66.9 | 49.3 |
| soporte normalizado | **74.4** | **67.1** |
| prototipo | 66.9 | 50.5 |
| base: el color más registrado del agente | 55.5 | — |

Sin normalizar, el error va hacia el color dominante del agente (black→brown 13, gray→brown 13). La normalización corrige ese sesgo. Con los 8 colores como candidatos nunca gana uno que el agente no haya visto.

**Objetos nuevos** (leave-object-out; pliegues 1–3 = los tres primeros objetos claros de cada clase, fijados antes de correr; 24 objetos, 984 vistas):

| lectura | top-1 | solo casos posibles (608) | vistas del llenado |
|---|---|---|---|
| soporte | **57.8** | 73.2 | 69.2 |
| soporte normalizado | 48.6 | 61.5 | 82.5 |
| base | 49.5 | — | 54.2 |

«Posible» quiere decir que el color del objeto nuevo existe en el agente. En 4 objetos no existe (car3 orange, pear3 brown, pear5 yellow, dog4 black) y ninguno acierta.

Por objeto (soporte, de 41 vistas): aciertan los que tienen el color mayoritario de su agente (cup1–3 white 116/116, cow4 40, cow6 39, horse4 41, pear2 39, dog2 36, apple2 32). Fallan los minoritarios: apple4 green → red 41/41, car2 green → black, horse5 black → brown 41/41; apple3 green no se reconoce (0/41). La única excepción parcial es car1 yellow (12/41). La normalización sube algo los minoritarios (horse5 0 → 8, car1 12 → 16) pero rompe los mayoritarios (cow6 39 → 7): en objetos nuevos empeora.

## Lectura

- La evocación da el **dominio** con fiabilidad (96 % en top-1). Una **palabra específica** sale a medias: 41 % con palabras arbitrarias por objeto y 74 % con color en objetos conocidos.
- En objetos nuevos el color **no generaliza más allá de la mayoría del agente**. El fallo es confusión sin rechazo: un color raro en un objeto nuevo se responde con el color común. Es lo contrario de exp16, donde el fallo era rechazar.
- Causas medidas: dentro de una clase el latente separa objetos sobre todo por forma y pose (sonda: 41 % contra 47 % de la medida directa), y cada agente ve 1–3 objetos por color. El color está encerrado en cada agente: «red» de manzanas y tomates no llega al auto.
- Pendiente: el color en un dominio compartido entre agentes, para que los objetos de todas las clases alimenten la misma palabra.

## Archivos

- `run_experiment17_specific_word.py` (`--parte a|b|c`, `--folds`), `run_experiment17_color_probe.py`
- `parte_a_*`, `parte_b_*`, `parte_c_*`: filas por imagen, resúmenes y logs; `sonda_color_*`
- `colores_borrador.json` (etiquetas aprobadas), `color_vectors.json` (fastText crudo)
- `modelos_b/`, `modelos_c/`, `modelos_c_lo*/`: memorias, fuera de git (~170 MB cada una; se regeneran con el script)
- Los latentes vienen de `results/experimento16/latentes.npy`
