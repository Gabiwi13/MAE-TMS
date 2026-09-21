# Experimento 8 — recuperación desde el directorio

## Método
- El directorio es una `HeteroAssociativeMemory4D` entre la pista y la identidad del agente (`n × m` a la izquierda, `n_agents × 2` a la derecha). El protocolo solo lo lee en un sentido —pista → agente, vía `predict`, que además toma una sola columna, `proj[:, 1]`—. Acá se lee en el sentido inverso: `recall_from_right(one-hot del agente)` devuelve una pista en el dominio de ese agente. No se agrega ninguna memoria ni se toca `hetero_lib`.
- Dos directorios por agente, con el mismo lado derecho y distinto lado izquierdo: `mem_dir` (texto, 300×16) y `mem_dir_R` (visión, 64×32). Las reconstrucciones de objeto salen del visual, que es el que tiene masa: 981 registros contra 52.
- Las memorias son las de la corrida oficial de 8 clases (`models/agent_*.pkl`, etapas 6 y 7). El juez de todas las reconstrucciones es el mismo clasificador latente del sistema (`models/classifier.pt`, 64D → 8 clases), así que las tres condiciones son comparables.
- La pista del lado derecho es un vector de índices de nivel, no de pesos: `1` lee la columna «ganó» de ese agente, `0` la de «no ganó», `nan` deja la coordenada fuera de la pregunta (`validate` la manda a `undefined`, `project` la saltea).
- El barrido de fracción presenciada reconstruye directorios desde cero sobre el pool visual de la etapa 7 (128 imágenes por clase, caché de exp7), con ground truth como maestro de registro: el objeto de estudio es el directorio, no la selección del ganador. La curva de capacidad usa el pool de llenado (`instance_latents_*.json`, 800 latentes por clase) para poder variar el número de registros.

## Resultados

### Las tres condiciones no se distinguen

| condición | operación | acierto |
|---|---|---|
| vivido | `mem_dom_H.recall_from_left(etiqueta propia)` | 80/80 |
| directorio · dominio propio | `mem_dir_R.recall_from_right(one-hot propio)` | 80/80 |
| directorio · dominio ajeno presenciado | `mem_dir_R.recall_from_right(one-hot ajeno)` | 112/112 |

La matriz 8×8 completa —cada agente contra cada dominio— sale con las ocho filas idénticas, y lo son literalmente: `np.array_equal` da True entre los ocho `mem_dir_R`. En el protocolo actual todos los agentes registran todos los broadcasts, así que es la misma relación ocho veces.

Controles que descartan que el 100% sea el juez siendo permisivo:

| control | resultado |
|---|---|
| clasificador ante latentes al azar | disperso: `dog` 139/500, `tomato` 15/500 |
| vecino más cercano entre las 6400 instancias reales | cae en la clase pedida 100% de las veces |
| centroide más cercano | el de la clase pedida siempre, rank 1/8 |

### Lo recuperado no es una copia

| clase | d(recuperado, instancia real más cercana) | d típica entre instancias vecinas | radio de la clase | dispersión entre sorteos | media de 20 semillas: d · dispersión |
|---|---|---|---|---|---|
| apple | 20.7 | 4.4 | 19.5 | 28.8 | 20.9 ± 0.6 · 30.1 |
| car | 22.2 | 5.5 | 22.7 | 30.5 | 23.1 ± 0.7 · 31.9 |
| cow | 16.9 | 5.1 | 16.2 | 24.4 | 16.5 ± 0.5 · 24.0 |
| cup | 22.4 | 4.8 | 19.2 | 31.1 | 22.9 ± 0.7 · 31.9 |
| dog | 19.3 | 6.6 | 22.3 | 28.1 | 20.1 ± 0.5 · 28.7 |
| horse | 16.9 | 5.7 | 16.4 | 24.6 | 16.7 ± 0.5 · 23.5 |
| pear | 18.1 | 5.9 | 17.4 | 25.9 | 17.5 ± 0.4 · 24.7 |
| tomato | 15.9 | 2.9 | 14.5 | 22.9 | 17.1 ± 0.4 · 24.7 |

Está entre 2.9 (dog) y 5.5 (tomato) veces más lejos de cualquier instancia real de lo que las instancias están entre sí, y en siete de ocho clases por encima del radio propio de la clase (en dog queda por debajo: 19.3 contra 22.3). La dispersión entre sorteos supera al radio en todas: cada recall cae en un sitio distinto, más lejos entre sí que dos ejemplares reales cualesquiera. Las cifras son de la pista de identidad con nan en los no ganadores y semilla fija (ver Notas); con ceros explícitos salían 3.6 a 7.1 veces, porque la cara «no ganó» de los otros siete agentes entraba en la columna de muestreo.

### Cuánta indeterminación resuelve el recall

| directorio | niveles vivos por coordenada | coordenadas | patrones admitidos |
|---|---|---|---|
| texto 300×16 | 3.28 – 5.86 de 16 | 300 | 10^152 – 10^228 |
| visión 64×32 | 7.78 – 10.70 de 32 | 64 | 10^56 – 10^65 |

La memoria no contiene la figura: contiene el conjunto de las compatibles, y el recall devuelve una. Lo estable son las marginales por coordenada — tanto que el argmax determinista, sin muestreo ni prueba de aceptación, ya clasifica en el dominio correcto en los ocho casos.

### Las dos caras del directorio

Cada registro escribe un 1 en el ganador y siete 0s en el resto, así que la masa es 7:1 exacta:

| directorio | registros | masa «ganó» | masa «no ganó» | razón | celdas con soporte |
|---|---|---|---|---|---|
| texto 300×16 | 52 | 15 600 | 109 200 | 7.00 | 26.5% / 61.3% |
| visión 64×32 | 981 | 62 784 | 439 488 | 7.00 | 29.2% / 76.6% |

Cuatro lecturas de la misma memoria:

| pista | coordenadas leídas | niveles vivos por coordenada |
|---|---|---|
| `[nan..1..nan]` cara «sí» de un agente | 1 de 8 | 9.91 |
| `[0..1..0]` one-hot | 8 de 8 | 9.91 |
| `[nan..0..nan]` cara «no» de un agente | 1 de 8 | 24.11 |
| `[0,0,…,0]` cara «no» de los ocho | 8 de 8 | 18.14 |

El one-hot y la cara positiva sola tienen el mismo soporte: las siete coordenadas en `0` no recortan un solo nivel. Pero sí cambian la masa de la columna que se muestrea: con ceros la columna es 6·N_all + 2·N_k (la cara «no ganó» de cada otro agente aporta toda la masa ajena), con nan es exactamente N_k (`sonda_pista_identidad.json`: TVD contra la distribución propia 0.235 en visión con ceros, 0 con nan; con ceros el 70% de la masa muestreada viene de otros agentes). Por eso todas las cifras de fidelidad, dispersión y capacidad de este README se miden con nan (`DirectoryMemory._identity_cue`, commit 65a7829). La cara negativa no restringe niveles cuando acompaña a un positivo; sí desplaza el sorteo.

Leída sola sí devuelve contenido, pero de otra naturaleza. `compat` mide qué fracción de las 64 coordenadas del patrón recuperado explica el soporte de cada agente (línea de base al azar: 0.292):

| cara | compat máx | agentes que explican >90% | separación entre centroides |
|---|---|---|---|
| «sí ganó» | 1.000 | 1 de 8 | 0.31 – 0.45 |
| «no ganó» | 0.595 – 0.645 | 0 de 8 | 0.94 – 0.97 |

En la cara positiva las 64 coordenadas salen del soporte de un solo agente. En la negativa ninguno pasa del 63%: el patrón está cosido de dominios distintos. La condición «no es de este agente» no ata las coordenadas entre sí. El dominio propio aparece 4 de 160 sorteos (2.5%) con la semilla fija; otras semillas dan entre 1 y 5 de 160, siempre por debajo del 12.5% del azar.

### Identidades imposibles: rechazo

| pista | niveles vivos | coordenadas vacías | responde |
|---|---|---|---|
| todo ceros | 18.14 | 0 / 64 | 10/10 |
| todo unos | 0.03 | 63 / 64 | 0/10 |
| dos-hot apple+car | 4.42 | 13 / 64 | 0/10 |
| dos-hot apple+dog | 4.16 | 9 / 64 | 0/10 |
| bits al azar (3 muestras) | 0.34 – 4.16 | 9 – 52 / 64 | 0/10 |

La proyección conjuntiva actúa como filtro: una sola coordenada sin nivel vivo basta para que el recall no conteste. Solo responde a identidades que pudieron haber ocurrido. La excepción es `todo ceros` —la lectura más laxa, 18.14 niveles—, que devuelve un punto sin dueño: separación 0.95, equidistante de todo.

### Fracción presenciada

| broadcasts ajenos presenciados (de 128) | registros del directorio | propio: responde / acierta | ajeno: responde / acierta |
|---|---|---|---|
| 0 | 128 | 1.00 / 1.00 | 0.00 / — |
| 1 | 133 | 1.00 / 1.00 | 0.59 / 1.00 |
| 2 | 141 | 1.00 / 1.00 | 0.89 / 1.00 |
| 4 | 154 | 1.00 / 1.00 | 0.98 / 1.00 |
| 8 | 184 | 1.00 / 1.00 | 1.00 / 1.00 |
| 16 · 32 · 64 · 128 | 243 – 1024 | 1.00 / 1.00 | 1.00 / 1.00 |

La transición está entera en si responde; la precisión es 1.00 desde el primer registro. Es todo-o-nada por containment: o la pista está contenida y la respuesta es correcta, o no está y no contesta. Presenciar el 6% de lo ajeno alcanza para reconstruirlo al 100%.

La transición es la probabilidad de haber presenciado al menos uno de los 128 broadcasts del agente: 1 − (1 − f)^128 da 0.63, 0.87, 0.98 y 1.00 para 1, 2, 4 y 8 broadcasts esperados; lo medido es 0.59, 0.89, 0.98 y 1.00. La curva de «responde» no mide nada de la memoria, mide el sorteo de qué se presenció. Lo que sí es de la memoria es que la precisión sea 1.00 desde el primer registro.

### Capacidad: más registros empeoran la figura

| registros por agente | niveles vivos | dispersión entre sorteos | d a instancia real | d, media de 20 semillas | acierto (20 semillas) |
|---|---|---|---|---|---|
| 1 | 1.00 | 0.0 | 3.3 | 3.3 ± 0.00 | 80/80 en todas |
| 2 | 1.58 | 8.3 | 7.3 | 7.3 ± 0.06 | 80/80 |
| 4 | 2.61 | 15.4 | 12.1 | 12.1 ± 0.09 | 80/80 |
| 8 | 4.09 | 22.4 | 16.1 | 16.0 ± 0.12 | 80/80 |
| 16 | 6.02 | 26.1 | 18.5 | 18.4 ± 0.17 | 80/80 |
| 32 | 7.53 | 27.7 | 19.0 | 18.9 ± 0.23 | 80/80 |
| 64 | 8.64 | 28.2 | 19.6 | 19.3 ± 0.13 | 80/80 |
| 128 | 9.63 | 29.1 | 19.8 | 19.9 ± 0.17 | 80/80 |
| 256 | 10.43 | 29.2 | 20.1 | 20.2 ± 0.25 | 80/80 |
| 512 | 11.04 | 29.1 | 20.2 | 20.2 ± 0.24 | 80/80 |
| 800 | 11.34 | 29.5 | 20.5 | 20.0 ± 0.18 | 80/80 |

Con un registro por agente la reconstrucción cae a 3.3 de una instancia real, con dispersión 0: hay un solo valor admisible por coordenada y no queda nada que sortear. Con 800, los que tiene la memoria de contenido de cada especialista, cae a 20.5. La fidelidad se pierde entre 1 y 16 registros (3.3 → 18.5) y después se estabiliza: de 16 a 800 cambia 2 unidades. El acierto de clase es 80/80 en los once tamaños y en las 20 semillas; el 79/80 en N=800 de la corrida original con ceros no reapareció en 40 corridas (20 con nan, 20 con ceros; con ceros hubo un solo 79/80, en N=256 de una semilla).

## Hallazgos
1. El directorio admite una operación que el protocolo nunca usa: leído por identidad reconstruye el dominio del agente, y lo hace igual de bien para el dominio propio que para uno ajeno presenciado. El privilegio del especialista no está en el directorio.
2. Lo reconstruido no es un ejemplar sino la envolvente coordenada a coordenada del dominio: correctamente ubicado (1-NN y centroide dan la clase pedida siempre) y a la vez fuera de la nube de instancias reales: de 2.9 a 5.5 veces la distancia típica entre instancias, por encima del radio de clase en siete de ocho. La coherencia no viene de que la memoria guarde el objeto, viene de que la condición «este agente ganó esto» restringe todas las coordenadas al mismo soporte.
3. La cara del «no ganó» acumula siete veces más masa que la del «sí» y no restringe nada: el one-hot completo y la cara positiva sola dan proyecciones idénticas. `predict` siempre leyó solo la cara positiva, así que el ruteo oficial nunca dependió de la negativa.
4. Leída sola, esa cara sí guarda el complemento del agente, pero sin identidad: ningún agente explica más del 63% de las coordenadas del patrón recuperado, contra el 100% de la cara positiva. Es una quimera cosida de varios dominios. El directorio guarda, por agente, lo que ganó con identidad y lo que no ganó sin ella.
5. La proyección conjuntiva rechaza identidades que no pudieron ocurrir —dos agentes ganando la misma pista, combinaciones al azar—: entre 9 y 63 coordenadas de 64 quedan sin soporte y el recall no contesta. No se puede fabricar contenido preguntando cualquier cosa.
6. Un solo broadcast ajeno presenciado ya deja reconstruir el dominio el 59% de las veces, y ocho lo dejan al 100%. La precisión nunca degrada: el fallo es siempre no contestar, nunca contestar mal.
7. Cobertura y especificidad tiran para lados opuestos: más registros hacen que conteste siempre pero ensanchan la envolvente. De 8 a 800 registros la reconstrucción pierde 4 unidades de fidelidad (16.1 → 20.5) sin ganar nada en cobertura, y la clase no falla en ninguna semilla. El óptimo de fidelidad está en 4 a 8 percepciones ajenas presenciadas, pero es un óptimo de reconstrucción, no de ruteo: con esos mismos 4 a 8 registros el directorio no rutea las consultas de ese agente. Exp10 lo mide con ruteo directo (sin encadenar) según los broadcasts presenciados de cada otro agente:

| presenciados de 128 | ruteo directo, imagen (test) | ruteo directo, texto (reservadas) |
|---|---|---|
| 2 | 10.2% | 27.4% |
| 4 | 10.2% | 34.1% |
| 8 | 10.4% | 43.4% |
| 16 | 12.9% | 64.6% |
| 32 | 32.4% | 82.2% |
| 64 | 62.1% | 92.0% |
| 128 | 81.9% | 93.6% |

Para reconstruir bastan 4 a 8; para rutear directo hacen falta 64 a 128, o encadenar (`results/experimento10/results.csv`, protocolo directo, f × 128). El límite no son los datos: la pista de identidad no selecciona nada dentro del dominio, así que cada registro nuevo solo agrega varianza.

## Archivos
- `fig1_objeto_recuperado.png` — por dominio: imagen real, reconstrucción del especialista desde el contenido, del directorio propio, del directorio de un no-especialista, e instancia real más cercana a lo recuperado
- `fig2_witnessed_fraction.png` — curvas de la fracción presenciada, dominio propio contra ajeno
- `fig3_sorteos.png` — cuatro sorteos del mismo dominio ajeno más la lectura determinista por argmax
- `fig4_cara_negativa.png` — qué devuelve la cara del «no ganó» de cada agente
- `results_witnessed_fraction.csv` — 576 celdas del barrido (fracción × agente × dominio)
- `sondas.json` — todas las mediciones numéricas de arriba
- `figura_meta.json`, `sorteos_meta.json`, `cara_negativa_meta.json` — metadatos por figura

Los registros de corrida (`probes.log`, `sweep.log`) quedan locales: `*.log` está en el `.gitignore`.

## Notas
- `run_experiment8_directory_recall.py` no modifica etapas ni memorias existentes. `DirectoryMemory` se usa tal cual; la lectura por identidad se arma en el script sobre `_ham`, que es la misma `HeteroAssociativeMemory4D` que la clase envuelve.
- La curva de capacidad construye directorios nuevos desde el pool de llenado (train[:200] × 4 variantes), que son imágenes distintas de las que llenaron el directorio real (train[200:328]). Mismo encoder y misma cuantización; sirve para variar el número de registros, no para comparar contra los valores absolutos del directorio entrenado.
- Los recalls muestrean con `random` de Python, no con numpy (`hetero_lib/hetero_associative_4d.py:538`, `choose`). Las figuras y sondas siembran `random` y `numpy` juntos (semilla 42); antes solo se sembraba numpy y ningún sorteo era reproducible. Sin semilla cada corrida devuelve un sorteo distinto, que es justamente lo que muestra `fig3_sorteos.png`. El barrido de fracción presenciada no se regeneró: su métrica `reconocido` depende solo del soporte y no cambia con la pista ni con la semilla.
- La curva de capacidad reconstruye memorias desde `instance_latents_*.json`. La etapa 5 cuantizó esos latentes en float32; releerlos en float64 cambia un nivel en un latente de car, cow y dog (600 celdas de 9.8 millones por memoria). Para reproducir bit a bit las memorias oficiales hay que cuantizar en float32 (`run_experiment11_monolithic.load_pool`). El efecto sobre esta curva es una coordenada de un latente y no se re-corrió.
- El barrido tarda unos 50 minutos: con soporte escaso la búsqueda del recall itera mucho más que con el directorio lleno.
