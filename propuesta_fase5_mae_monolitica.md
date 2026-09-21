# Fase 5: propuesta de diseño para la comparación contra la MAE monolítica

**Fecha:** 20 de septiembre de 2026
**Estado:** propuesta. No hay código nuevo ni corridas. Cada decisión abierta está marcada como **[decisión]**.

---

## 1. Qué falta y por qué es el experimento central

La tesis sostiene que la maquinaria transactiva escala (`.tex8/secciones/07_conclusiones.tex:25-28`) y reporta 88.0% temprano, 93.2% maduro y 0 falsos ruteos visuales. Ninguna de esas cifras se compara con lo que haría una sola memoria asociativa con el mismo contenido. Sin esa línea base no se sabe si dividir el contenido en ocho especialistas coordinados por directorios aporta algo, o si es solo ocho veces más memoria más un ruteo que a veces falla.

La pregunta que este experimento responde: **dado el mismo contenido y el mismo sustrato MAE, ¿qué gana y qué pierde el sistema por partirlo en especialistas y rutear?**

## 2. Brazos

| brazo | memorias | cómo responde una consulta de texto |
|---|---|---|
| **M** (monolítica) | 1 `HeteroAssociativeMemory(300,16,64,32)` + 1 `HomoAssociativeMemory(300,16)` + 1 `HomoAssociativeMemory(64,32)`, llenadas con las 8 clases | `recognize_gated` en la única memoria; si hay soporte, `recall_from_left` con la primera pista reconocida, decodificar |
| **T-oráculo** | los 8 especialistas oficiales | el especialista lo elige la verdad de terreno; mismo recall |
| **T-protocolo** | los 8 especialistas + directorios perspectivales v5 | protocolo oficial: fase temprana (`process_query`) forma los directorios; fase madura `route_transactive` desde una entrada al azar; rechazo incluido |

M se construye con la clase `Agent` sin cambios: `Agent("todo", mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)`. `recognize_gated`, `recall` y `recognize_gated_right` funcionan igual sobre una memoria que contiene las ocho clases. Sus directorios quedan vacíos y no se consultan. No hace falta ninguna clase nueva.

T-oráculo existe para separar dos efectos que T-protocolo mezcla: lo que aporta la partición del contenido y lo que cuesta el ruteo. Sin él, si M iguala a T-protocolo no se sabe si es porque partir no sirve o porque el directorio pierde lo que la partición gana. **[decisión]** Incluirlo. Recomiendo que sí; cuesta una corrida más de recalls, no de llenado.

Para imagen los tres brazos son análogos: M puntúa con su homo latente (`recognize_gated_right`) y evoca etiquetas con `recall_from_right`; T-oráculo evoca desde el especialista verdadero; T-protocolo rutea con `route_transactive` en modalidad imagen.

## 3. Capacidad equivalente

Hay tres formas de igualar, y no son intercambiables. Propongo reportar las dos primeras y declarar por qué la tercera no aplica.

**3.1 Misma memoria, mismos datos.** Las dimensiones (300,16,64,32) las fija la cuantización, no el diseño. M recibe todos los registros de las ocho clases; cada especialista recibe los de la suya. M ve exactamente los mismos pares (etiqueta, latente) que la suma de los ocho. Es la comparación que responde "¿hace falta partir?". T usa ocho veces más celdas; eso se declara como costo, no se esconde.

**3.2 Barrido por registros.** Cortes N ∈ {25, 50, 100, 200} imágenes por clase, con las 4 variantes de aumentación (100 a 800 registros por clase; el corte 200 es el llenado oficial). En cada corte M tiene 8N imágenes y cada especialista N. Esto da la curva de cómo se degrada cada brazo al crecer el contenido, que es donde la teoría predice que M sufre: exp6 mostró que un especialista con 328 imágenes propias sigue en 0% de falsos aceptos, pero nunca se midió una memoria con 8×200.

**3.3 Mismas celdas.** No se puede sin cambiar m o q, y cambiar los niveles cambia la representación (exp1 y exp7 mostraron que la resolución del signo decide el comportamiento del ruteo). Una M con 8 veces más niveles no sería "la misma memoria más grande". Se deja fuera y se dice por qué.

## 4. Orden de alimentación

La relación de una MAE es aditiva: `abstract` suma cuentas. El estado final de M y de cada especialista no depende del orden en que entran los registros. El orden solo importa en dos lugares:

- La formación de los directorios en T-protocolo, que ya está fijada por el protocolo oficial (16 consultas de fase temprana intercaladas por clase, `TEST_QUERIES`; percepciones visuales intercaladas, etapa 7 fase A). No se toca.
- Las curvas por corte N. Para que los cortes sean comparables entre brazos, el llenado va intercalado por clase (la imagen i de cada clase, en el orden de `instance_latents_{cls}.json`, que ya es image-major con las variantes contiguas). El corte N usa los primeros 4N latentes de cada clase en los tres brazos.

No hay llenado por bloques. Un llenado por bloques daría la misma relación final y solo cambiaría cortes intermedios que no se van a medir.

## 5. Bancos

- **Texto:** las 411 consultas de `eval_bank`. Para T-protocolo, la partición de exp10 (`load_text`: 30 por clase de formación = 240, el resto reservado = 171). M y T-oráculo no forman nada, así que se evalúan en las 411; la comparación con T-protocolo se hace sobre las 171 reservadas, donde los tres brazos están en igualdad.
- **Imagen:** las 82 de test por clase (656). El caché de exp7 solo tiene 20 de test por clase; hay que codificar las 656 con el encoder (GPU, segundos).
- **Fuera de dominio:** las 12 consultas de `run_rejection_probe.PROBE_QUERIES`. Con los especialistas actuales: 10 rechazadas, 2 ruteadas en falso (a apple y a cup). **[decisión]** Ampliar el banco a 40 consultas con el mismo criterio (representables, fuera de los 8 dominios). Doce consultas dan intervalos demasiado anchos para separar brazos; recomiendo ampliar, y que las nuevas las escriba el autor para que no las sesgue quien diseña el experimento.

## 6. Métricas

Por consulta y por sorteo (R = 3 sorteos, como exp9), en texto→imagen:

1. **Responde**: el recall reconoce la pista (containment).
2. **Clase**: del latente decodificado, con tres jueces. Principal: vecino real más cercano entre las 6400 instancias del llenado (exp8 mostró que el clasificador es permisivo, 80/80 ante cualquier envolvente). Secundarios: centroide más cercano y `classifier.pt`. Se reportan los tres; decide el 1-NN.
3. **Fidelidad**: distancia del latente recuperado a la instancia real más cercana de la clase verdadera (`d_nn`, la misma de exp8 y exp9).
4. **Coherencia del patrón** (`compat`, exp8 parte C): para cada clase c, fracción de las 64 coordenadas cuyo valor recuperado tiene soporte en la homo latente de c. Se reporta el máximo sobre clases y si esa clase coincide con la verdadera. En T vale 1.0 por construcción (el patrón sale de una sola memoria). En M mide directamente la quimera: un patrón con `compat` máximo de 0.6 está cosido de varias clases.
5. **Niveles vivos por coordenada** de la proyección antes de muestrear. Es la causa de 3 y 4: cuanto más ancha la proyección, más lejos cae el sorteo.
6. **Dependencia de la pista**: razón F con corrección de Bessel (exp9, commit bbde155). Secundaria.
7. **Rechazo**: tasa de no respuesta en el banco propio y tasa de falsos aceptos en el banco fuera de dominio.

Imagen→texto: responde, y acierto top-3 de dominio (`evoke_labels`, etapa 7).

Para T-protocolo, además: acierto de ruteo, rechazo del directorio, y el desglose de cada error final en "ruteo equivocado" contra "contenido equivocado".

## 7. Predicciones, con el mecanismo que las produce

El mecanismo está en las etiquetas compartidas. De las 159 etiquetas con vector, 6 aparecen en más de una clase:

| etiqueta | clases | frecuencia de llenado |
|---|---|---|
| fruit | apple, pear, tomato | 8, 3, 5 |
| animal | cow, dog, horse | 8, 8, 8 |
| mammal | cow, dog, horse | 3, 8, 8 |
| red | apple, tomato | 8, 3 |
| pome | apple, pear | 2, 2 |
| table | cup, dog | 4, 6 |

En M, "fruit" queda registrada con latentes de apple, pear y tomato. La proyección de esa pista es la unión de los tres soportes, coordenada por coordenada, y `choose` sortea cada coordenada por separado: el patrón puede salir con coordenadas de apple y de pear a la vez. En T, la consulta primero se rutea (sumando `recognize_gated` sobre todos los tokens) y después se recuerda dentro de una sola clase. La diferencia entre brazos no es de capacidad sino de orden: decidir antes o después de recordar.

- **P1 (quimera).** En M, las consultas cuya primera pista reconocida es compartida producen patrones con `compat` máximo menor que 1 y clase 1-NN incorrecta en una fracción medible. En T-oráculo `compat` es 1 y la clase es 100% (exp9, vivido: 100% clasificador y vecino).
- **P2 (fidelidad).** `d_nn` de M es mayor que la de T-oráculo, y la diferencia crece con N, porque la proyección de M tiene más niveles vivos por coordenada. Referencia: T-oráculo a N=200 da 21.9 a 22.0 (exp9, `muestreo_vivido.json`).
- **P3 (especificidad).** M acepta más consultas fuera de dominio que T. La homo de M es la unión de ocho soportes; el containment se vuelve más fácil de satisfacer. Referencia T: 2 de 12.
- **P4 (cobertura).** M responde más consultas del banco propio que T-protocolo, porque no rechaza por directorio (T-protocolo rechaza el 28.5% del banco con el directorio de 52 registros, exp9) y porque una pista compartida siempre tiene soporte en M. Este es el punto a favor de M que hay que reportar sin atenuarlo.
- **P5 (costo del ruteo).** T-protocolo queda entre M y T-oráculo en clase y fidelidad. Cuánto pierde respecto de T-oráculo es el precio del directorio.

## 8. Criterio de refutación

Se fija antes de correr. Sobre las 171 consultas reservadas, 10 semillas, intervalos del 95% por bootstrap sobre semillas:

**La tesis queda refutada** si se cumplen las tres a la vez:
1. Clase 1-NN de M y de T-protocolo difieren en menos de 2 puntos y sus intervalos se solapan.
2. `d_nn` de M y de T-protocolo difieren en menos de 1 unidad (la desviación entre semillas observada en exp9 es de 0.13 a 0.21).
3. Falsos aceptos fuera de dominio de M no superan a los de T.

En ese caso partir el contenido no aporta nada medible y el sistema transactivo es solo costo: ocho veces la memoria y un ruteo que rechaza.

**La tesis se sostiene en forma fuerte** si M pierde en clase o en `compat` (P1) aunque gane en cobertura (P4): la decisión antes del contenido es lo que evita la quimera.

**Resultado intermedio** que también hay que poder decir: M iguala a T-oráculo pero T-protocolo es peor que ambos. Entonces la partición no aporta y el directorio cuesta; la tesis tendría que reformularse alrededor de la coordinación (exp10) y no de la especialización.

## 9. Semillas y reproducibilidad

- 10 semillas (42 a 51). En cada corrida se siembran `random` y `numpy` juntos (hallazgo de la fase 1: `hetero_lib` muestrea con `random`, `hetero_associative_4d.py:538`).
- Las memorias son deterministas dados los datos y el corte; la semilla afecta solo al muestreo del recall y a la entrada aleatoria de T-protocolo (`RandomState(seed)`).
- Los directorios de T-protocolo se forman una vez por semilla con el protocolo oficial sobre las memorias del corte N. No se reutilizan los `agent_*.pkl` oficiales salvo en el corte N=200, donde deben coincidir con ellos (control de que el llenado reproducido es el oficial: comparar `mem_dom_H.relation` con `np.array_equal`).

## 10. Código reutilizable y código nuevo

Reutilizable tal cual:

| qué | de dónde |
|---|---|
| latentes del pool de llenado, 800 por clase, ya codificados | `models/instance_latents_{cls}.json` |
| secuencia de etiquetas por clase | `stage5_fill.build_label_sequence` |
| cuantización del latente | `stage5_fill.quantize_latent_global`, `latent_global_stats.json` |
| patrón de construcción por corte N | `run_experiment6.build_agent_n` |
| puntuación y recall de texto | `Agent.recognize_gated`, `Agent.recall` (`stage6_interaction`) |
| tokenización y vectores | `tokenize_query`, `prevectorize`, `get_fasttext_vector`, `token_vectors.json` |
| formación de directorios y ruteo | `register_transaction`, `route_transactive`, `TEST_QUERIES` |
| partición 240/171 | `run_experiment10_perspectival_routing.load_text` |
| imagen: puntuación y evocación | `stage7_bidirectional.recognize_gated_right`, `evoke_labels` |
| jueces | `run_experiment8_directory_recall`: `load_classifier`, `decode_image`, `dequantize_latent`, distancia a instancias; parte C para `compat` |
| F con Bessel y dispersiones | `run_experiment9_member_loss` |
| banco fuera de dominio | `run_rejection_probe.PROBE_QUERIES` |

Nuevo (un script, `run_experiment11_monolithic.py`):

- `build_arm(N, arm)`: construye M o los 8 especialistas desde los latentes del pool, intercalando por clase.
- `answer_text(agent_or_agents, item, arm)`: aplica la regla de respuesta de cada brazo y devuelve el latente, la proyección y los diagnósticos.
- `judge(z, truth)`: 1-NN, centroide, clasificador, `d_nn`, `compat`, niveles vivos.
- Bucle de semillas con `multiprocessing` por semilla (20 núcleos; cada proceso carga sus memorias, ~80 MB por HAM).
- Salidas en `results/experimento11/`: un JSON por semilla y corte, `resumen.json` con medias e intervalos, `README.md` con las tablas, y cuatro figuras: clase 1-NN contra N por brazo, `d_nn` contra N, histograma de `compat` de M contra T, y rechazo fuera de dominio por brazo.

Lo que no se toca: `src/`, los `agent_*.pkl` oficiales, ningún experimento anterior.

## 11. Costo estimado

- Llenado: por semilla y corte, 9 memorias hetero (8 + 1). El registro es rápido; el corte N=200 completo tarda lo que tarda la etapa 5 sin codificar (segundos por memoria).
- Recalls: 411 consultas × 3 sorteos × 3 brazos × 4 cortes × 10 semillas ≈ 148 000 recalls de texto, más 656 × 3 brazos × 4 × 10 ≈ 79 000 de imagen. El barrido de exp8 hizo 5 760 recalls en 50 minutos con soporte escaso (0.5 s cada uno); con soporte normal es más rápido. Estimación conservadora: 30 horas de un núcleo, 2 a 3 horas con 10 procesos en paralelo y la GPU para decodificar.
- Propongo una pasada rápida primero: cortes {50, 200}, 3 semillas, 1 sorteo. Una hora. Sirve para verificar el script y ver si las predicciones van en la dirección esperada antes de gastar la corrida completa.

## 12. Decisiones que quedan al autor

1. Incluir T-oráculo (recomiendo sí).
2. Ampliar el banco fuera de dominio de 12 a 40 consultas escritas por el autor (recomiendo sí).
3. Juez principal 1-NN sobre las 6400 instancias (recomiendo sí; el clasificador queda como secundario).
4. Cortes N ∈ {25, 50, 100, 200} o solo {50, 200}.
5. Regla de respuesta de M: primera pista reconocida en el orden de la consulta, igual que el protocolo. Es la comparación justa; una regla "mejor pista" favorecería a M con información que T no usa.
6. Nombre y número del experimento: propongo experimento 11 (el 10 es el último).
