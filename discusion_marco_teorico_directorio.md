# El directorio como memoria: marco teórico, tesis y experimentos 9 y 10

**Fecha:** 14 de septiembre de 2026
**Contexto:** Continúa la discusión del 30 de agosto (`discusion_directorio_entropico.md`). La pregunta de fondo es qué clase de cosa es el directorio, por qué "memoria directorio" suena ambiguo, y qué lugar ocupa el TME. Aquí se fija un marco teórico, se derivan de él dos tesis con predicciones refutables, y se reportan los experimentos 9 y 10 que las ponen a prueba.

---

## 1. El problema

Tres hechos del sistema, verificados en código y en los experimentos 7 y 8:

1. **El directorio contiene contenido.** Leído por identidad (`recall_domain`), reconstruye el dominio del agente al 100%, propio o ajeno. Guarda quién ganó y una envolvente de qué ganó (exp8).
2. **Hay nueve copias de la misma relación.** Cada agente registra todos los broadcasts, y el TME también. Los ocho `mem_dir_R` son iguales bit a bit (`np.array_equal`, exp8); el del TME lo es por construcción (`process_query`, etapa 7).
3. **El TME no está en la teoría.** Para Wegner el sistema transactivo es el conjunto de memorias individuales, directorios y procesos de comunicación. En el código, `TME` es un pizarrón de fase temprana que sostiene dos directorios.

De ahí la ambigüedad: el directorio es una memoria, todos los directorios son la misma memoria, y el mediador que los sostiene es una novena copia con nombre propio. El problema no es terminológico. Es que el diseño no distingue entre dos cosas que la teoría sí distingue.

## 2. Marco

### 2.1 Eje: división del trabajo epistémico (Putnam, Wegner)

Putnam (1975) formula la división del trabajo lingüístico: un hablante usa "olmo" y "haya" sin poder distinguirlos, porque hay expertos que sí pueden y a ellos difiere. Una comunidad funciona con conocimiento distribuido más una relación de deferencia. Wegner (1987, 1995) es la versión psicológica y grupal: memorias individuales especializadas, más un directorio de quién sabe qué, más tres procesos (actualización del directorio, asignación de información, coordinación de la recuperación). Wegner recupera la expresión "mente de grupo" pero la define como propiedad del sistema de individuos que se comunican, no como una entidad aparte. El TME como entidad no está en Wegner. Está en nuestro código.

### 2.2 Los dos modos de conocer (Russell)

Russell (1910) distingue conocimiento por familiaridad (*acquaintance*), la relación directa con el objeto, del conocimiento por descripción, saber que existe algo que satisface cierta descripción sin haberlo tenido delante. En el sistema:

- El especialista conoce su dominio por familiaridad: vivió las instancias, su memoria de contenido es la distribución de lo percibido.
- Los demás conocen ese dominio por descripción: presenciaron que el especialista ganaba y guardaron una envolvente de qué ganaba. Exp8 midió esa envolvente sin nombrarla: correctamente ubicada (vecino más cercano y centroide de la clase pedida siempre) y a la vez fuera de la nube de instancias reales (2.9 a 5.5 veces más lejos de cualquier instancia de lo que las instancias están entre sí, medido con la pista de identidad corregida).

Wegner llama a esto codificación superficial contra profunda. La tesis de Russell es que la descripción no reemplaza a la familiaridad: uno puede saber *que* hay un dominio y *quién* lo tiene sin poder responder *como* él. Eso es comprobable.

### 2.3 Ícono e índice, y el nombre como designador rígido (Peirce, Kripke)

Peirce distingue tres modos de significar: el ícono representa por semejanza, el índice señala por contigüidad o conexión causal, el símbolo por convención (Peirce, en Buchler, 1955). La memoria de contenido es icónica: el espacio de valores tiene métrica, niveles vecinos se parecen, y por eso la indeterminación ahí es generalización. El directorio es un índice: la pista y la identidad quedan asociadas porque co-ocurrieron, no porque se parezcan.

El lado derecho del directorio es además un nombre. Kripke (1980) muestra que un nombre propio es un designador rígido: refiere al mismo individuo sin contenido descriptivo. Por eso no hay nada "entre manzana y perro", y por eso la indeterminación en el lado derecho no puede ser generalización, solo error. Esto ya estaba en la discusión del 30 de agosto como intuición ("la identidad no tiene métrica"). Con Peirce y Kripke tiene nombre y linaje.

El correlato neurocientífico es exacto. La teoría del índice hipocampal (Teyler y DiScenna, 1986; Teyler y Rudy, 2007) propone que el hipocampo no guarda el contenido sino un índice a los patrones corticales que lo componen, y que una pista parcial que activa el índice reinstala el patrón completo. Los sistemas complementarios (McClelland, McNaughton y O'Reilly, 1995) explican por qué el índice tiene que ser disperso y separado, distinto del contenido distribuido y superpuesto: para apuntar sin interferir. La lectura inversa de exp8 es una reinstalación por índice.

### 2.4 Metamemoria: un sustrato, dos niveles (Nelson y Narens)

Nelson y Narens (1990) definen la metamemoria con dos niveles, objeto y meta, y dos flujos: monitoreo (el meta observa al objeto) y control (el meta actúa sobre el objeto). El directorio monitorea (cuentas por agente, quién ganó qué) y controla (rutea). Que use el mismo sustrato MAE que la memoria de contenido no es una confusión: es la tesis. Lo que cambia de nivel a nivel no es la maquinaria sino el tipo de signo que vive en cada lado, icónico en el contenido, indicial en el directorio. "El directorio es una memoria per se" deja de ser una objeción y pasa a ser la definición de metamemoria.

### 2.5 La dinámica: internalización o artefacto (Vygotsky, Hutchins)

Vygotsky (1978) enuncia que toda función psicológica superior aparece dos veces: primero entre personas, después dentro de cada una. El TME de la fase temprana es un andamio en el sentido de Wood, Bruner y Ross (1976): sostiene la coordinación mientras el grupo no puede sostenerla solo, y se retira. Que en la fase madura "el TME deje de ser necesario" es internalización.

Pero Vygotsky también implica que cada quien internaliza lo que participó, desde su posición. El sistema actual contradice eso: los ocho directorios son la misma relación. Es una internalización sin perspectiva, que equivale a no haberla hecho.

La alternativa es Hutchins (1995): la cognición distribuida vive también en artefactos compartidos, y un directorio común que nadie internaliza es un artefacto legítimo, un pizarrón que el grupo consulta. Clark y Chalmers (1998) generalizan el punto: un recurso externo que se consulta de manera fiable es parte del proceso cognitivo. El sistema tiene que decidir cuál de las dos cosas es el directorio, porque hoy es las dos a medias.

### 2.6 El principio, reformulado

La discusión del 30 de agosto propuso: *la entropía pertenece al contenido; la decisión pertenece a la identidad*. Con Peirce se lee mejor: **la entropía vive en el ícono, la decisión en el índice.** Un sistema de memorias icónicas e indeterminadas necesita al menos un órgano indicial y nítido que las coordine.

## 3. Tesis, predicciones, refutaciones

### Tesis A (Russell): la descripción rutea pero no reemplaza a la familiaridad

**Experimento 9, pérdida de un miembro.** Se quita un agente k. Las consultas de su dominio entran por un sobreviviente. El directorio sigue señalando a k, porque el índice no se pierde con el miembro. El grupo puede: rechazar (sabe que k sabía y no está), sustituir (el mejor sobreviviente responde con su contenido) o describir (un sobreviviente responde con la envolvente de k desde su directorio). Referencia: vivido, el recall del especialista presente.

Predicciones:
- El índice sobrevive: las consultas de k siguen ruteadas a k aunque k no esté.
- La descripción conserva la clase (el juez y el vecino real la ubican en k) pero no la fidelidad: queda más lejos de las instancias reales que el recall vivido.
- La descripción no depende de la pista: la misma envolvente para "manzana roja" que para "manzana verde". La familiaridad sí responde a la pista. Se mide como dispersión entre consultas distintas contra dispersión entre repeticiones de la misma consulta.
- La sustitución confabula: responde con la clase del sustituto, o rechaza.

Refutación: si la envolvente es indistinguible del recall vivido en fidelidad y en dependencia de la pista, entonces el directorio ya contiene el contenido, los especialistas sobran, y la tesis transactiva entera se cae. Por eso el juez no puede ser solo el clasificador, que exp8 mostró permisivo (80/80).

### Tesis B (Vygotsky contra Hutchins): perspectiva y encadenamiento

**Experimento 10, directorios perspectivales.** Cada agente presencia solo una parte de los broadcasts ajenos, al azar con probabilidad f o solo los de sus vecinos en un anillo de radio r. Los directorios dejan de ser iguales. El grupo rutea directo (sin soporte, rechaza; protocolo actual) o encadenado (sin soporte, pregunta a los agentes que conoce, por familiaridad, y la consulta salta). Referencia: un pizarrón único con todos los registros.

Predicciones:
- Con f pequeño el ruteo directo colapsa en rechazo: nadie rutea lo que no presenció (exp4).
- El encadenado recupera el acierto del pizarrón con pocos saltos ya con fracciones chicas, porque exp8 mostró que presenciar el 6% de lo ajeno basta para tener soporte.
- Los directorios divergen (Jaccard entre soportes) sin que el acierto encadenado baje: perspectiva sin pérdida.

Lectura de los dos resultados posibles:
- Si el encadenado alcanza al pizarrón con pocos saltos, la internalización parcial basta. El TME sobra como artefacto: el sistema transactivo es la red de directorios perspectivales (Vygotsky).
- Si el acierto encadenado se degrada o los saltos explotan, el grupo necesita el pizarrón. El TME queda rehabilitado como artefacto compartido, no como mediador que desaparece (Hutchins).

El diseño actual de nueve copias no puede decir ninguna de las dos cosas.

### Lo que el marco excluye

El "TME generalista" (un noveno agente lleno con las ocho clases) no prueba ninguna tesis: su resultado se deduce de la curva de capacidad de exp6 y de la quimera de exp8. Queda fuera.

## 4. Resultados

Corridas de la noche del 13 al 14 de septiembre de 2026. Detalle, tablas por clase y figuras en `results/experimento9/README.md` y `results/experimento10/README.md`.

### 4.1 Experimento 9: la tesis A no se sostiene como se formuló, y se reformula

Se quitó cada uno de los ocho agentes y las 411 consultas del banco entraron por un sobreviviente.

- **El índice sobrevive al miembro.** El directorio rutea a k igual que antes (55.7% del banco en texto, 81% en imagen; el resto lo rechaza o lo manda a otro, como con k presente). No sabe que k no está. La pérdida transactiva es asimétrica: se pierde la respuesta, no la ubicación.
- **La sustitución confabula o calla.** Cuando el mejor sobreviviente responde (24.5%), responde siempre con su propia clase (tomate por manzana, vaca por caballo). En imagen→texto no responde nunca.
- **La descripción responde siempre y conserva la clase siempre.** Latente decodificado: 100% en la clase perdida por los dos jueces, a 19.3 de la instancia real más cercana contra 21.9 del especialista (12% más cerca), con 9.3 niveles vivos por coordenada contra 8.4 (11% más). Etiquetas evocadas desde una imagen: 100% en el vocabulario del dominio perdido, igual que el especialista, que sin embargo responde menos (89% contra 100%).
- **La descripción no depende de la pista; el especialista, apenas.** La dispersión entre consultas distintas casi iguala a la dispersión entre sorteos de la misma consulta (32.3 contra 31.3), y la razón F con corrección de Bessel da 1.14 en el especialista y 1.00 en la descripción, contra 1.00 del nulo. "Manzana roja" y "manzana verde" producen en el especialista la misma envolvente.

La predicción central de la tesis A era que la descripción se distinguiría de la familiaridad por menor fidelidad y por no depender de la pista. Se distingue en la dirección contraria en fidelidad (es mejor) y apenas en dependencia de la pista. La causa está en el llenado, no en la maquinaria: las etiquetas de ConceptNet son del dominio y no de la imagen, y cada etiqueta se empareja con una instancia arbitraria, así que la memoria de contenido nunca recibió pares con correspondencia y solo puede devolver la envolvente del dominio (lo que exp5 llamó prototipo emergente). Para *reproducir*, el especialista y el testigo saben lo mismo.

**Dónde vive entonces la familiaridad.** Una sonda sobre el mismo banco: el especialista reconoce el 98.3% de las consultas de su dominio con su contenido; un no-especialista, el 16%; el directorio de 52 registros rutea el 55.7%. El 43.6% de lo que el especialista reconoce, el directorio no lo presenció. La familiaridad no está en lo que el especialista reproduce sino en lo que reconoce: acepta pistas de su dominio que nadie le vio ganar, mientras el testigo solo conoce lo presenciado. Russell se reformula sin abandonarse: conocer por familiaridad es poder decir "esto es mío" ante lo nunca visto; conocer por descripción es poder decir "esto era de él" ante lo que se le vio. La distinción es de cobertura del reconocimiento, no de fidelidad de la reproducción.

Consecuencia para la idea del TME con dominio: un miembro que sabe todo por descripción puede sostener las respuestas del grupo cuando falta un especialista, con la misma clase y mejor fidelidad. Lo que no puede es reconocer lo que no vio ganar. Y la peor política para el grupo es redirigir al segundo mejor.

### 4.2 Experimento 10: Vygotsky gana en imagen; en texto gana si la consulta compara

Cada agente presenció solo parte de los broadcasts ajenos (al azar con probabilidad f, o solo los de sus vecinos en un anillo de radio r). Los directorios divergieron hasta en el 83% de sus celdas. Tres protocolos contra el pizarrón (un directorio con todo): directo (sin soporte, rechaza), encadenado (sin soporte, pregunta a los que conoce hasta que alguien tiene soporte) y agregado (pregunta a todos los conocidos y suma scores).

- **Imagen.** El encadenado iguala al pizarrón (81.9%, cero errores) en toda condición con f>0 o r≥1, incluso con f=1/64. El costo es el salto: 3.5 consultas extra con f=1/64, 1.9 con anillo r=1, 0.5 con f=1/2. El ruteo directo, en cambio, se queda en el piso del dominio propio (10%) hasta f=1/8: nadie rutea lo que no presenció.
- **Texto.** El encadenado elimina el rechazo pero deja errores del 20 al 33% con f pequeño, porque la contención de texto es laxa: un directorio que solo se conoce a sí mismo acepta una pista ajena el 20% de las veces y, sin competidores, el argmax la manda al propio dominio. El agregado sí alcanza al pizarrón: 91% en consultas reservadas desde f=1/32 (pizarrón 93.6) y 94.3% con f=1/4, que iguala al pizarrón dentro del ruido (cuatro consultas en una semilla). La ventaja del pizarrón no era tener los registros sino tener a los competidores juntos; sumar perspectivas parciales lo reconstruye.
- **Alcance y comparación.** El encadenado llega a todo el grupo por transitividad pero decide con la primera perspectiva; el agregado decide comparando pero solo hasta los conocidos directos (con anillo r=1 cae al 55%). Un protocolo transactivo completo necesita las dos operaciones.

Lectura: la internalización perspectival basta (Vygotsky) siempre que la coordinación de la recuperación, el tercer proceso de Wegner, sea una consulta a los conocidos y no una consulta a un artefacto. El pizarrón (Hutchins) no aporta nada que la red de directorios parciales no pueda reconstruir, en imagen desde f=1/64 y en texto desde f=1/32. Lo que sí aporta es ahorro: una consulta en vez de hasta ocho.

Dos hallazgos laterales. La diferencia entre modalidades es de resolución del signo, no de arquitectura: con 32 niveles sobre 64 rasgos el directorio es un índice absoluto (cabe o no cabe), con 16 niveles sobre 300 es relativo (quién cabe mejor), lo que conecta con exp1 y exp7. Y la tolerancia xi es una propiedad del grupo: sus huecos se definen sobre el soporte de todos los agentes, así que en directorios perspectivales cambia con lo que presenciaron los demás.

### 4.3 Balance

| tesis | predicción | resultado |
|---|---|---|
| A. La descripción rutea pero no reemplaza a la familiaridad | descripción: misma clase, menor fidelidad, sin dependencia de la pista; vivido: dependiente de la pista | **Refutada en su forma original.** Misma clase (100%), fidelidad mejor en la descripción (19.3 contra 21.9), y la dependencia de la pista es nula en la descripción y débil en el especialista (F 1.00 contra 1.14). La familiaridad se desplaza al reconocimiento: 98% contra 16% contra 56% del directorio. |
| B. Internalización perspectival contra artefacto | el encadenado recupera al pizarrón con pocos saltos | **Confirmada en imagen** (81.9%, cero errores desde f=1/64). **Confirmada en texto con consulta comparativa** (agregado, 91–94% desde f=1/32). El pizarrón ahorra consultas, no acierto. |

Lo que cambia en el encuadre de los reportes:
1. El TME de la fase temprana es un andamio que se internaliza. En la fase madura no hace falta como artefacto: la red de directorios perspectivales más una coordinación de la recuperación (encadenar, agregar) recupera su función. El diseño actual de nueve copias idénticas debería reemplazarse por directorios que registran lo que cada agente presenció.
2. El directorio es metamemoria: contiene una descripción del dominio de cada agente (Russell, codificación superficial de Wegner) que basta para responder en su ausencia con la clase correcta. El privilegio del especialista es de reconocimiento, no de reproducción.
3. La idea del "TME con dominio" queda definida y acotada: un miembro que sabe todo por descripción puede sostener respuestas, no reconocimientos. Para que el especialista reproduzca mejor que el testigo haría falta un llenado con correspondencia etiqueta-instancia, que los datos actuales (ConceptNet por dominio) no tienen.

### 4.4 Cambio de protocolo aplicado (14 de septiembre)

Con el balance anterior, el protocolo oficial pasó a directorios perspectivales:

- **Actualización por transacción** (`register_transaction`, etapas 6 y 7): registran la transacción el agente por el que entró la consulta, el ganador y el TME. El TME conserva el registro completo solo como diagnóstico; ningún ruteo de la fase madura lo consulta.
- **Coordinación de la recuperación** (`route_transactive`, etapas 7 y 8 y la app): el agente de entrada agrega su directorio y los de los agentes que conoce; si nadie de ese círculo tiene soporte, la consulta pasa a los conocidos y cada uno agrega el suyo.
- **Lectura visual estricta** (xi=0), por la razón de exp10.

Resultado de re-correr las etapas 6, 7 y 8 con la regla nueva:

| medida | antes (v4, nueve copias) | ahora (v5, perspectival) |
|---|---|---|
| directorios visuales por agente | idénticos, 981 registros cada uno | ~120 propios + 11–22 de cada otro, entropía ≈2.3 bits (registro completo 3.0) |
| ruteo visual de test (656 imágenes) | 75.0%, rechazo 25%, 0 errores | 73.6%, rechazo 26.4%, 0 errores; decide en el primer círculo (todos se conocen) |
| evocación imagen→etiquetas (top-3) | 85.3% | 85.3% |
| fidelidad temprana↔madura (16 consultas) | 100% | 100% |

Con el llenado de 16 variantes y el umbral de energía (23 de septiembre): ruteo 96.2 %, rechazo 3.5 %, 2 errores de 656; evocación 97.4 %; fidelidad 16/16.

Los 1.4 puntos de ruteo visual los cuesta xi=0, no la perspectiva. En texto, con 16 consultas de fase temprana, tres agentes quedan conociéndose solo a sí mismos (apple, car, horse) y aun así la fase madura rutea las 16 consultas igual que la temprana, porque los que sí conocen a otros alcanzan a todos por encadenamiento.

## 5. Bibliografía comentada

Cada entrada dice qué aporta al marco y dónde leerla. Las marcadas **[acceso abierto]** tienen el texto completo en línea sin suscripción. Las referencias se verificaron el 14 de septiembre de 2026 contra las fuentes enlazadas.

**Putnam, H. (1975).** The meaning of 'meaning'. En K. Gunderson (ed.), *Language, Mind, and Knowledge* (Minnesota Studies in the Philosophy of Science, vol. 7, pp. 131–193). University of Minnesota Press.
Aporta la división del trabajo lingüístico: el significado se sostiene en una comunidad con expertos y deferencia. Es el antecedente filosófico directo del directorio de Wegner.
[PhilPapers](https://philpapers.org/rec/PUTTMO) · [PDF del curso MIT 24.09x](https://courses.edx.org/asset-v1:MITx+24.09x+3T2015+type@asset+block/16_putnam_meaning_of__meaning_.pdf) **[acceso abierto]**

**Wegner, D. M. (1987).** Transactive memory: A contemporary analysis of the group mind. En B. Mullen y G. R. Goethals (eds.), *Theories of Group Behavior* (pp. 185–208). Springer.
El texto fundacional: directorio como etiquetas y ubicaciones, codificación superficial y profunda, tres procesos transactivos, y la mente de grupo como propiedad del sistema y no como entidad.
[SpringerLink](https://link.springer.com/chapter/10.1007/978-1-4612-4634-3_9) · [PDF en el sitio de Wegner (Harvard)](https://dtg.sites.fas.harvard.edu/DANWEGNER/pub/Wegner%20Transactive%20Memory.pdf) **[acceso abierto]**

**Wegner, D. M. (1995).** A computer network model of human transactive memory. *Social Cognition, 13*(3), 319–339.
Formaliza el directorio con la metáfora de red: actualización del directorio, asignación de información, coordinación de la recuperación. Es el vocabulario de `update_directory` y del ruteo.
[Harvard Scholar](https://scholar.harvard.edu/dwegner/publications/computer-network-model-human-transactive-memory) · [PDF](https://scholar.harvard.edu/files/dwegner/files/wegner_computer_network_model_1995.pdf) **[acceso abierto]**

**Russell, B. (1910).** Knowledge by acquaintance and knowledge by description. *Proceedings of the Aristotelian Society, 11*, 108–128. Reimpreso en *Mysticism and Logic* (1918).
La distinción que define la tesis A: el especialista conoce por familiaridad, los demás por descripción. Exp9 la operacionaliza.
[Oxford Academic](https://academic.oup.com/aristotelian/article/11/1/108/1807043) · [PDF (Univ. Nantes)](http://ifac.univ-nantes.fr/IMG/pdf/russell_knowledge_by_acquaintance_and_knowledge_by_description.pdf) **[acceso abierto, dominio público]** · [Resumen en la IEP](https://iep.utm.edu/knowacq/)

**Peirce, C. S. (1955).** Logic as semiotic: The theory of signs. En J. Buchler (ed.), *Philosophical Writings of Peirce* (pp. 98–119). Dover. (Manuscritos de 1897 y 1903.)
Ícono, índice y símbolo. El contenido es icónico, el directorio es indicial. De ahí que la entropía sea generalización en uno y error en el otro.
[PhilPapers](https://philpapers.org/rec/PEILAS) · [Entrada de la SEP sobre la semiótica de Peirce](https://plato.stanford.edu/entries/peirce-semiotics/) **[acceso abierto]**

**Kripke, S. A. (1980).** *Naming and Necessity*. Harvard University Press. (Conferencias de 1970, publicadas primero en 1972.)
El nombre como designador rígido, sin contenido descriptivo. Es la razón formal de que el lado derecho del directorio no admita indeterminación.
[Entrada de la SEP sobre designadores rígidos](https://plato.stanford.edu/entries/rigid-designators/) **[acceso abierto]**

**Nelson, T. O., y Narens, L. (1990).** Metamemory: A theoretical framework and new findings. En G. H. Bower (ed.), *The Psychology of Learning and Motivation* (vol. 26, pp. 125–173). Academic Press.
Nivel objeto y nivel meta, monitoreo y control. Resuelve la objeción "el directorio es una memoria per se": lo es, y por eso es metamemoria.
[Semantic Scholar](https://www.semanticscholar.org/paper/ae843e607257efc4a106343a774e2927da974c6a)

**Teyler, T. J., y DiScenna, P. (1986).** The hippocampal memory indexing theory. *Behavioral Neuroscience, 100*(2), 147–154.
El hipocampo como índice a patrones corticales; una pista parcial reinstala el patrón. La lectura inversa de exp8 es esto.
[PubMed](https://pubmed.ncbi.nlm.nih.gov/3008780/)

**Teyler, T. J., y Rudy, J. W. (2007).** The hippocampal indexing theory and episodic memory: Updating the index. *Hippocampus, 17*(12), 1158–1169.
Revisión veinte años después, con la evidencia acumulada. Más legible que el original.
[Wiley](https://onlinelibrary.wiley.com/doi/10.1002/hipo.20350) · [PDF (Whitman College)](http://people.whitman.edu/~herbrawt/hippocampus.pdf) **[acceso abierto]**

**McClelland, J. L., McNaughton, B. L., y O'Reilly, R. C. (1995).** Why there are complementary learning systems in the hippocampus and neocortex: Insights from the successes and failures of connectionist models of learning and memory. *Psychological Review, 102*(3), 419–457.
Por qué el índice tiene que ser disperso y separado, y el contenido distribuido y superpuesto. Es el argumento de arquitectura detrás del principio "entropía en el contenido, decisión en la identidad".
[PubMed](https://pubmed.ncbi.nlm.nih.gov/7624455/)

**Vygotsky, L. S. (1978).** *Mind in Society: The Development of Higher Psychological Processes* (M. Cole, V. John-Steiner, S. Scribner y E. Souberman, eds.). Harvard University Press.
La ley de la doble aparición: primero entre personas, después dentro de cada una (p. 57). Es la lectura del TME como andamio que se internaliza, y la exigencia de que la internalización sea perspectival.

**Wood, D., Bruner, J. S., y Ross, G. (1976).** The role of tutoring in problem solving. *Journal of Child Psychology and Psychiatry, 17*(2), 89–100.
Introduce el andamiaje (*scaffolding*): el tutor sostiene lo que el aprendiz no puede solo y se retira. El TME de la fase temprana en una palabra.
[Wiley](https://acamh.onlinelibrary.wiley.com/doi/10.1111/j.1469-7610.1976.tb00381.x) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/932126/)

**Hutchins, E. (1995).** *Cognition in the Wild*. MIT Press.
Cognición distribuida entre personas y artefactos, con la navegación de un buque como caso. Es la alternativa a Vygotsky para el directorio: un pizarrón compartido que nadie internaliza del todo.
[MIT Press](https://mitpress.mit.edu/9780262581462/cognition-in-the-wild/) · [PhilPapers](https://philpapers.org/rec/HUTCIT)

**Clark, A., y Chalmers, D. (1998).** The extended mind. *Analysis, 58*(1), 7–19.
Un recurso externo consultado de manera fiable es parte del proceso cognitivo. Generaliza el argumento del artefacto.
[Oxford Academic](https://academic.oup.com/analysis/article-abstract/58/1/7/153111) · [PhilPapers](https://philpapers.org/rec/CLATEM)

Las entradas BibTeX están en `bibliografia_marco_teorico.bib`.
