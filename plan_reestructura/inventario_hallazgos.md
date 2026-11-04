# Inventario de hallazgos con el sistema escalado (parte 4 del reporte)

Solo lectura, 4 nov 2026. No se cambió de rama ni se modificó nada.

## Cómo leer las referencias

- `UH/` = `C:\Users\aq99l\Projects\MAE-TMS-una-hetero\` (rama `una-hetero`). Las carpetas `results/` se leyeron del disco.
- `MED/` = `C:\Users\aq99l\Projects\MAE-TMS-medico\` (rama `medico-demo`). Ahí están exp25 a exp29, que no existen en `UH/results/`.
- `MT/` = `C:\Users\aq99l\Projects\MAE-TMS\`.
- `S7-16` = `git show ea9069c:sintesis_exp7_a_exp16.md` (rama `exp7-directorio-unificado`).
- `S17-22` = `git show 4c9cf01:sintesis_exp17_a_exp22.md`.
- `SMED` = `MT/sintesis_medico_exp20_a_exp27.md` (sin versionar).
- `S26OCT` = `UH/sintesis_26oct_a_1nov.md` (sin versionar; está en `UH/`, no en `MT/`).
- `UNA` = `UH/UNA_HETERO.md` (qué se volvió a correr con una sola hetero).
- `C4` = `UH/.tex_uacj/Capitulo4.tex`.
- «Bib»: si la cita del vínculo natural está en `UH/.tex8/referencias.bib`. Nelson y Narens, Russell, Vygotsky, Hutchins, Wood-Bruner-Ross, Peirce, Kripke, Putnam, Tenenbaum-Griffiths, Yonelinas y McClelland **no están** en la bibliografía. Teyler y DiScenna y los tres Wegner sí.

## Arquitectura: qué cuenta como «una hetero final»

Según `UNA:13`, con una sola hetero se volvieron a correr exp2-6, 9, 11, 12, 13, 16, 17, 18, 21, la ablación, la sonda de rechazo y el industrial monolítico. `UNA:15` lista los que ya tenían una sola memoria de contenido (una homo latente por módulo): los demos médico e industrial, el piloto de módulos y exp24. Los experimentos que solo leen directorios (exp7, exp8, exp10, exp22) no dependen de las homo, pero algunos usan un protocolo anterior (todos los agentes registran todo, directorio visual sin variantes). Las carpetas del 2-3 nov (`lineas_base`, `codificador_sin_clase`, `objetos_nuevos_codificador_por_pliegue`, `experimento11_protocolo_corregido`, `hemisferio_visual`) son del sistema final.

Etiquetas usadas abajo:
- **final**: una hetero, 16 variantes, umbral de energía, directorios perspectivales.
- **final (lectura)**: solo lee los modelos o directorios oficiales, así que es independiente de las homo.
- **anterior**: protocolo o memorias de antes. Se dice qué difiere.
- **otros datos**: MedMNIST+ o VisA, con módulos de una memoria de contenido.

---

## Tema 1. El directorio como índice y metamemoria (4 fichas)

**Lo más fuerte:** exp8 (la lectura inversa devuelve una envolvente), exp7 (el índice no mezcla modalidades) y el par exp15 + líneas base (el índice compara mejor que el contenido, pero equivale a contar).

### exp7 · `UH/results/experimento7`
- **Pregunta.** ¿Un directorio unificado de texto e imagen forma una representación compartida?
- **Hallazgo.** No. La relación es por (rasgo, módulo) y no tiene término rasgo-rasgo, así que las mitades son independientes. Con una consulta emparejada, el veto conjuntivo hace que una mitad sin soporte tumbe a la otra.
- **Cifras.**
  - Texto: 96.2 % unificado y 96.2 % separado (`README.md:14`, `:17`).
  - Scores de texto de A y C idénticos (diferencia máxima 0; `README.md:32`).
  - Emparejada: 23.8 % contra 100.0 % con dos directorios (`README.md:26-27`).
  - El único acople es el denominador de B1 tomado de `_counts`: 96.2 → 91.2 → 88.8 %; leído de la relación se queda en 96.2 % (`README.md:41-43`).
- **Arquitectura.** Final (lectura), pero con el texto en 32 niveles y evaluado dentro de muestra (`README.md:7`).
- **Estado.** Vigente. El costo del denominador se corrigió a `_counts` en 3080b37 (`S26OCT:14`).
- **Vínculo.** «La entropía vive en el ícono, la decisión en el índice»: Peirce para las dos caras y Kripke para el nombre como designador (`S7-16:7`). Ninguno está en Bib.
- **En el reporte.** Falta.

### exp8 · `UH/results/experimento8`
- **Pregunta.** ¿Qué devuelve el directorio leído al revés (módulo → pista)?
- **Hallazgo.** Reconstruye el dominio del módulo, igual de bien para el propio que para uno ajeno que se presenció. Lo que devuelve no es un ejemplar sino la envolvente coordenada a coordenada. Responde todo o nada, nunca mal.
- **Cifras.**
  - Vivido 80/80, directorio propio 80/80, ajeno presenciado 112/112 (`README.md:16-18`).
  - Lo recuperado queda de 2.9 a 5.5 veces más lejos de cualquier instancia que las instancias entre sí (`README.md:43`).
  - Cara «no ganó»: masa 7:1 (`README.md:60-61`). Ningún módulo explica más del 63 % de sus coordenadas, contra el 100 % de la cara «sí» (`README.md:78-79`).
  - Identidades imposibles: 0/10 respuestas (`README.md:89-91`).
  - Basta presenciar 1 broadcast para responder el 59 %; con 8, el 100 %, con precisión de 1.00 (`README.md:100-103`).
  - Con más registros la figura se ensancha: 3.3 → 20.5 de 1 a 800 registros (`README.md:114`, `:124`).
  - Para reconstruir bastan 4-8 presenciados; para rutear directo hacen falta 64-128 (`README.md:139-147`).
- **Arquitectura.** Anterior: todos los agentes registran todos los broadcasts, así que los 8 directorios son idénticos (`README.md:20`), y el directorio visual tiene 981 registros sin variantes (`README.md:5`). El mecanismo no depende de eso.
- **Estado.** Vigente como mecanismo. Las cifras de fidelidad se rehicieron con la pista nan (`README.md:43`, `:72`). No se volvió a correr con el sistema final.
- **Vínculo.**
  - Metamemoria de Nelson y Narens: un nivel meta con un modelo del nivel objeto. No está en Bib.
  - Se aparta del índice hipocampal de Teyler y DiScenna en que sí tiene contenido. Está en Bib y se cita en `C4:1478`.
  - Fuente de los dos: `S7-16:9`.
- **En el reporte.** Falta. `C4:589` y `C4:665` usan «envolvente» para el contenido, no para la lectura inversa.

### exp15 · `UH/results/experimento15`
- **Pregunta.** ¿El contenido elige mejor que el directorio entre sus candidatos? ¿Sirve abstenerse por margen?
- **Hallazgo.** No en los dos casos. El índice, calibrado por conteos, compara mejor que la activación del contenido. Los errores de texto son confusiones de vocabulario compartido, no empates estrechos.
- **Cifras.**
  - Argmax 96.8 % contra árbitro 93.6 % (`README.md:11-12`).
  - El margen quita alrededor de un acierto por cada error que evita (`veredicto.md:10`).
  - En imagen, el árbitro es la doble compuerta: quita el falso de `horse7` (`veredicto.md:12`, `:20`).
- **Arquitectura.** Anterior (homo + hetero con pesos homo). No se volvió a correr con una hetero; `C4:1187-1188` lo excluye.
- **Estado.** Vigente. Ojo: `veredicto.md:9` conserva 90.6 % (de antes de los pesos homo) y el README ya dice 93.6 % (`S26OCT:33`).
- **Vínculo.** Ninguno externo. Es «la decisión vive en el índice» (`S7-16:31`).
- **En el reporte.** Sí, como alternativa a la segunda compuerta (`C4:979-984`, `C4:1759-1765`).

### Líneas base · `UH/results/lineas_base`
- **Pregunta.** ¿Qué agrega la memoria asociativa sobre decisores simples con los mismos vectores?
- **Hallazgo.** En texto, la compuerta equivale a pertenecer al vocabulario, y el directorio equivale a una tabla de conteos. Lo que agrega es rechazo sin umbral y recuerdo. En imagen, los decisores simples superan al enrutamiento.
- **Cifras.**
  - 101 de 3064 pares token-clase se aceptan y todos están en el vocabulario; no hay discrepancias (`README.md:158`).
  - Tabla de conteos 92.3 % contra el directorio, p = 0.58 (`README.md:199`).
  - Umbral de coseno: AUROC de 0.97 a 0.99, pero deja pasar de 9 a 23 de las 40 fuera de dominio (`README.md:203`).
  - Imagen: 631 del sistema contra 652-655 de los decisores (`README.md:180-187`, `:205`).
- **Arquitectura.** Final.
- **Estado.** Vigente.
- **Vínculo.** El directorio localiza pero no decide mejor: Wegner 1995 (coordinación de la recuperación) y Sparrow 2011 (`C4:1716-1721`). Los dos en Bib.
- **En el reporte.** Sí (`C4:987-1169`, `C4:1628-1734`).

---

## Tema 2. La perspectiva y la pérdida de un miembro (4 fichas)

**Lo más fuerte:** exp10 (los directorios parciales encadenados igualan al pizarrón), exp9 (se pierde la respuesta, no la ubicación) y exp25 (la organización se sostiene con otra memoria debajo).

### exp10 · `UH/results/experimento10`
- **Pregunta.** Si cada módulo registra solo lo que presencia, ¿el grupo recupera el enrutamiento del pizarrón (Vygotsky contra Hutchins)?
- **Hallazgo.** Sí.
  - En imagen, encadenar los directorios parciales iguala al pizarrón con cero errores, aunque los directorios difieran en el 83 % de sus celdas.
  - En texto hace falta agregar los puntajes, porque la decisión es comparativa.
  - Encadenar da alcance y agregar da comparación: son operaciones distintas.
- **Cifras.**
  - Imagen, f = 1/64: encadenado 81.9 % igual al pizarrón (81.9), con 3.56 saltos y divergencia de 0.83 (`README.md:24`).
  - Texto reservadas, agregado con f = 1/32: 91.0 contra 93.6 del pizarrón (`README.md:54`). Con f = 1/4, 94.3, que es igualación dentro del ruido (`README.md:57`, `:63`).
  - Anillo r = 1: el agregado da 56.4 y el encadenado 73.9 (`README.md:45`, `:59`).
  - Con ξ = 2, el dominio propio baja al subir f (`README.md:9`).
- **Arquitectura.** Anterior: directorio visual sin variantes (pizarrón 81.9 %) y maestro de registro igual a la verdad de terreno (`README.md:8`). El protocolo perspectival se volvió el oficial (`S7-16:15`).
- **Estado.** Vigente. `v1_sin_agregado/` es la versión previa.
- **Vínculo.**
  - El TME como andamio (Wood, Bruner y Ross) que se internaliza (Vygotsky 1978); el pizarrón de Hutchins 1995 solo ahorra consultas (`S7-16:15`; `README.md:4`). Ninguno en Bib.
  - `SMED:75`: es una propiedad de la arquitectura de Wegner.
- **En el reporte.** Parcial. Solo el efecto de ξ = 2 (`C4:542-543`) y que sumar directorios iguala al registro completo (`C4:1406-1407`). Falta el resultado central (encadenado, agregado, alcance contra comparación).

### exp9 · `UH/results/experimento9`
- **Pregunta.** ¿Qué queda cuando se pierde un especialista: rechazo, sustitución o descripción?
- **Hallazgo.**
  - El índice sobrevive y sigue apuntando al ausente: se pierde la respuesta, no la ubicación.
  - Sustituir por el segundo mejor confabula o calla.
  - Describir (la lectura inversa del directorio) conserva la clase siempre y con más fidelidad.
  - Lo que solo tiene el especialista es reconocer: «esto es mío» frente a «esto era de él».
- **Cifras.**
  - El directorio rutea 229 consultas a k (55.7 %) (`README.md:23`).
  - Sustitución: responde el 24.5 % y acierta la clase en 0 %. Descripción: responde el 100 % con clase al 100 %, a 19.3 de las instancias contra 21.9 del vivido (`README.md:33-35`).
  - El especialista reconoce el 98.3 % de su dominio, un no especialista el 16.1 % (`README.md:72-73`).
  - La tesis A (el especialista reproduce mejor) no se sostiene (`README.md:82`).
  - Con directorios perspectivales en texto (`formacion_texto/curva.json`): llegan al perdido 90 de 411 (`:21`, «0 transactivo»), 302 (`:93`, 60), 332 (`:129`, 120) y 368 (`:165`, 240). El pizarrón con 240 llega a 393 (`:153`).
- **Arquitectura.** Anterior: directorios globales y `mem_dom_H` y la homo latente del sustituto (`README.md:9`, `:64`). Con una hetero solo se volvió a correr la sonda de fase 2, con las mismas cifras (`UNA:63`). `formacion_texto/` es la actualización perspectival.
- **Estado.**
  - Vigente con correcciones: el 98.5 % sin semilla se corrigió (`README.md:64`) y F con Bessel (`README.md:54`).
  - **No está claro:** `S26OCT:38` dice «90 de 411 con 16 interacciones», pero en `curva.json` 90 corresponde a «0 transactivo» (`:21`) y con 16 da 100 (`:57`).
- **Vínculo.** Russell 1910 (familiaridad contra descripción; no está en Bib) y la pérdida transactiva de Wegner 1987 (en Bib como `wegner1987transactive`). Fuentes: `README.md:4`, `S7-16:13`.
- **En el reporte.** Falta.

### exp25 · `MED/results/experimento25`
- **Pregunta.** Con las mismas transacciones, ¿la MAE es la mejor memoria para la organización transactiva?
- **Hallazgo.** No. Un directorio de prototipos rutea mejor, incorpora un dominio nuevo con 8 transacciones y, por gossip, comunica una fracción mínima. Lo que se sostiene es la organización, no la memoria.
- **Cifras.**
  - Órganos: MAE B1 93.3 contra prototipos 96.6 (`README.md:11`). Modalidad: 93.0 contra 98.4 (`README.md:14`).
  - Comunicación: MAE 11.6 MB contra gossip 0.4 MB (`README.md:19`).
  - Ingreso con 8 transacciones: MAE 41 % contra prototipos 98 % (`README.md:28`).
  - Fondo de ojo en modalidad: MAE 24 % contra 0-1 % (`README.md:32`).
  - Veredicto (`README.md:50`).
- **Arquitectura.** Otros datos (MedMNIST+).
- **Estado.** **Corregido en parte.** La fila de pérdida de un miembro no mide nada: el ausente seguía respondiendo, y P4 queda sin probar (`README.md:23`, `:39`). `SMED:72` todavía cita esa fila como hallazgo (93-100 %).
- **Vínculo.** «La aportación defendible es la arquitectura transactiva; la MAE no es su mejor implementación» (`SMED:75`, `:79`).
- **En el reporte.** Falta.

### Piloto de módulos · `UH/results/piloto_modulos`
- **Pregunta.** ¿El sistema aprende cuál módulo lo hace mejor solo con sus transacciones (24 módulos, VisA)?
- **Hallazgo.** Sí. Con la lectura éxitos / intentos, el 79.0 % de las consultas va al mejor módulo. Pero consulta 19 de 24 módulos y queda 7.5 puntos bajo el router central: resultado intermedio.
- **Cifras.** 79.0 contra 52.6 de la lectura oficial y 71.6 del kNN central (`README.md:5`, `:37`, `:58`).
- **Arquitectura.** Otros datos.
- **Estado.** Vigente. `SMED:92` cita 73.4 % y 2.5 lecturas, que no coinciden con este README; puede ser otra etapa (etapa1/etapa2), y no se verificó.
- **Vínculo.** «El primer paso hacia la mitad dinámica de Wegner» (`SMED:92`).
- **En el reporte.** Falta.

---

## Tema 3. Reconocer y recordar: envolvente, contención y familiaridad (7 fichas)

**Lo más fuerte:** exp16 con el codificador por pliegue (generaliza por envolvente y falla rechazando, con matiz), exp14 (acepta lo que su envolvente cubre, no lo que se parece) y la lesión de `homo_marginal` (nombra antes de dejar de reconocer).

### exp13 · `UH/results/experimento13`
- **Pregunta.** ¿Augmentar el llenado visual reduce el rechazo sin falsos?
- **Hallazgo.** Hay dos compuertas (el directorio y la conjunción del recuerdo), y cada una cede solo con su propia densificación. El precio aparece donde se tocan las envolventes vecinas.
- **Cifras.**
  - De punta a punta, A3: 18.4 → 74.8 → 94.5 (`veredicto.md:16`). +28.0 puntos (`:26`).
  - 1 falso ruteo y 5 aceptaciones ajenas de 656 (`:27`). El color sólido pasa de 1 a 3 especialistas (`:28`).
  - Los falsos son siempre los mismos (`horse7` → dog) (`:40`). Las dos compuertas (`:34`).
- **Arquitectura.** Final (con una hetero, mismas decisiones en 42 640 filas; `UNA:123`).
- **Estado.** Vigente. El control contra los oficiales y la cifra «323364/8 clases» del README están mal (`UNA:131-134`).
- **Vínculo.** «Reconocer es una conjunción de 64 soportes por coordenada» (`S7-16:23`). Sin cita externa.
- **En el reporte.** Sí (`C4:539-556`, `C4:1767-1785`, `C4:1792-1794`).

### exp14 · `UH/results/experimento14`
- **Pregunta.** ¿Un umbral de energía del latente cierra la fuga de entradas degeneradas, y cuánto cuesta?
- **Hallazgo.**
  - El codificador colapsa lo que no tiene estructura cerca del origen. Ese punto cae dentro del soporte de `horse` sin ninguna instancia cerca: la memoria acepta lo que su envolvente cubre, no lo que se parece a algo visto.
  - El umbral externo τ cierra casi toda la fuga.
- **Cifras.**
  - τ = 16.6 (`veredicto.md:3`).
  - Costo: 5 imágenes reales de 3280, todas vacas oscuras (`:7`). Cierra el 94 % de la fuga entre clases (`:8`).
  - La fuga está a 15-19 de la instancia más cercana, tres veces la mediana intraclase de 5.8 (`:16`).
  - El directorio nunca rutea las entradas cercanas al origen (`:24`).
  - Con 16 variantes: acepta 180 y quedan 33 tras τ (`README.md:27`).
- **Arquitectura.** Anterior (corrida v5 con 4 variantes y contenido V16 de exp13; `veredicto.md:3`). La contención no depende de los pesos (`S26OCT:24`). τ forma parte del sistema final.
- **Estado.** Vigente. `veredicto.md` (103/83 aceptadas) es anterior a las cifras de 16 variantes del README y de `C4:597` (152/137).
- **Vínculo.** Mismo mecanismo que exp8 visto desde la entrada (`S7-16:25`). El reporte lo liga a los errores de conjunción (Reinitz 1992) y a MINERVA 2 (`C4:1524-1531`, en Bib).
- **En el reporte.** Sí (`C4:581-598`, `C4:1787-1811`).

### exp16 · `UH/results/experimento16`
- **Pregunta.** ¿La envolvente generaliza a objetos que nunca contribuyeron a ella?
- **Hallazgo.** Cabe el 89 % de las veces y, cuando no cabe, se rechaza. La brecha vive en objetos concretos, no en clases.
- **Cifras.**
  - De punta a punta: 95.5 % con objeto conocido contra 89.2 % con objeto nuevo; brecha de 6.3 [2.5, 10.4] (`README.md:7-8`, `:17`).
  - 2 falsos de 3280 (`veredicto.md:7`).
  - Lo peor es apple3 al 0 % (`veredicto.md:27`). P1 (las frutas generalizan mejor) se refuta (`:27`).
- **Arquitectura.** Final (mismas decisiones con una hetero; `UNA:124`).
- **Estado.** Vigente, matizado por la ficha siguiente.
- **Vínculo.** «Generalizar es caer dentro de una envolvente formada por otros» (`S7-16:27`). El reporte lo liga a Clark 1996 y Reinitz 1992 (`C4:1519-1531`).
- **En el reporte.** Sí (`C4:638-669`).

### Codificador por pliegue · `UH/results/objetos_nuevos_codificador_por_pliegue`
- **Pregunta.** ¿exp16 se sostiene si el codificador tampoco vio el objeto reservado?
- **Hallazgo.** La cobertura casi no cambia, pero el fallo deja de ser solo rechazo.
- **Cifras.**
  - De punta a punta con objeto nuevo: 87.6 % [84.3, 91.0] (`README.md:77`, `:86`).
  - Falsos: de 2 a 136 de 3280 (`:88`). Cuatro objetos reúnen la mitad (`:126`).
  - El criterio de exp16 queda en la zona intermedia (`:161`).
- **Arquitectura.** Final.
- **Estado.** Vigente. **Corrige** «el fallo es rechazo» de exp16.
- **Vínculo.** Ninguno propio.
- **En el reporte.** Sí (`C4:671-738`, `C4:1845-1847`).

### Una memoria por módulo y lesión · `UH/results/homo_marginal`
- **Pregunta.** ¿Las homo guardan algo que la hetero no tenga? ¿Qué pasa al dañar la memoria?
- **Hallazgo.**
  - Las homo son la marginal de la hetero. Lo que llega sin pareja cabe en el borde de valor indefinido.
  - Con daño al azar, el módulo deja de nombrar mucho antes de dejar de reconocer.
- **Cifras.**
  - El efecto de reemplazar las homo es 47 veces menor que el de cambiar la semilla (`README.md:44`).
  - Borde más marginal = homo oficial en los 8 agentes (`:123`, `:129`).
  - 78 de 800 imágenes quedan reconocidas sin nombre (`:184`).
  - Con f = 0.05 nombra 0 y reconoce 800 de 800 (`:199-206`, `:211`). La homo aparte es la más frágil (`:212`).
- **Arquitectura.** Final: justifica la arquitectura de una hetero.
- **Estado.** Vigente.
- **Vínculo.**
  - La familiaridad es una lectura de la asociación (`S26OCT:70`).
  - En el reporte: Clark 1996, Hintzman 1984, Shallice 1988, Plaut 1995 y 2002, Bruce y Young 1986, McWeeny 1987, Beauvois 1982, Brown y McNeill 1966 y Hart 1965, todos en Bib (`C4:1518-1580`).
- **En el reporte.** Sí (`C4:1171-1261`, `C4:1501-1580`).

### Codificador sin pérdida de clase · `UH/results/codificador_sin_clase`
- **Pregunta.** ¿Cuánto depende el índice visual de la pérdida de clase del codificador?
- **Hallazgo.** Mucho. La clase sigue en el latente, pero repartida en combinaciones de coordenadas, y la contención compara coordenada por coordenada. Las envolventes se tocan y el fallo pasa de rechazo a confusión.
- **Cifras.**
  - Ruteo de 96.2 a 70.4 %, y falsos de 2 a 169 (`README.md:60-61`).
  - Objeto nuevo 59.3 % (`:70`).
  - Una memoria ajena también contiene la imagen: 0.5 → 82.9 % (`:86`). Separación por coordenada: 5.34 → 0.24 (`:88`).
  - La evocación cae por el ruteo: 80 de 81 bien ruteadas contra 7 de 32 mal ruteadas (`:97`).
- **Arquitectura.** Final.
- **Estado.** Vigente.
- **Vínculo.** Separación de patrones del hipocampo (Yassa y Stark 2011) y aprendizaje de categorías (Goldstone 1994), en Bib (`C4:1703-1707`).
- **En el reporte.** Sí (`C4:741-849`, `C4:1695-1707`).

### exp29 · `MED/results/experimento29`
- **Pregunta.** ¿La MAE dañada reproduce la demencia semántica (ambiente de Rogers 2004)?
- **Hallazgo.** No. Solo sabe callarse: la conjunción por coordenada hace que pierda el nombre entero en vez de decir el de un vecino. La frecuencia actúa como umbral, no como sesgo.
- **Cifras.**
  - En los 24 niveles, 0 errores semánticos (`README.md:45`). Q1: 0.0 contra 8.9 % de los pacientes (`:31`).
  - Criterio refutado (`:67`). Lectura (`:76-77`). El PDP de Rogers sigue siendo el mejor (`:79`).
- **Arquitectura.** Otros datos (rasgos binarios, sin variantes).
- **Estado.** Vigente. Es un resultado negativo.
- **Vínculo.** Rogers et al. 2004, Woollams 2008 y Hodges 1995 (`README.md:5`, `:77`). No se comprobó si están en Bib. Ninguna síntesis lo cubre.
- **En el reporte.** Falta. Conecta con la limitación (j) y la fragilidad del nombre (`C4:1892-1901`).

---

## Tema 4. El tamaño, el ancho de la envolvente y la partición (8 fichas)

**Lo más fuerte:** exp20 parte 1 con exp22 (el principio de tamaño corrige el sesgo de ancho y equivale a B1 donde B1 funciona), exp11 corregido (partir compra fidelidad, rechazo y no mezclar, no clase) y exp21 en tórax (la memoria única converge a un atractor).

### exp11 y protocolo corregido · `UH/results/experimento11`, `UH/results/experimento11_protocolo_corregido`
- **Pregunta.** ¿Una sola EHAM con el mismo contenido iguala al sistema transactivo?
- **Hallazgo.** En clase empatan desde N = 50, y con N = 25 gana la EHAM única. Partir compra fidelidad, menos dominio ajeno, rechazo fuera de dominio y no mezclar cuando la pista es compartida. Cuesta cobertura y ocho veces las celdas.
- **Cifras.**
  - Clase sobre el total, P − M: −4.4 con N = 25, −0.7 con 50 y 100, −0.1 con 200 (p = 0.86) (`protocolo_corregido/README.md:174-177`).
  - d_nn del protocolo menos M con N = 200: −5.39 [−6.30, −4.49] (`:262`).
  - Clase con pista compartida: 71.4 contra 51.1 de M (`:265`).
  - Fuera de dominio: M 20.0 % contra P 5 % (`:199`).
  - Imagen: P − M de −16.3 en cobertura (`:193`).
- **Arquitectura.** Final (cachés de una hetero; `protocolo_corregido/README.md:29`).
- **Estado.**
  - **Corregido.** Los directorios se acumulaban entre trabajos del Pool (`protocolo_corregido/README.md:7`).
  - `S26OCT:35` («el protocolo gana desde N = 50») quedó superado por la corrección.
  - `experimento11/veredicto.md` es de 4 variantes.
- **Vínculo.** «Una EHAM que ha decidido antes de recordar» (`S7-16:19`). El reporte lo trata como un principio conocido de las memorias asociativas (`C4:1597-1598`).
- **En el reporte.** Sí (`C4:851-984`, `C4:1583-1626`).

### exp12 · `UH/results/experimento12` y `UH/results/controles_uniformes/experimento12`
- **Pregunta.** ¿La ventaja de partir crece con el solapamiento entre dos dominios?
- **Hallazgo.** Ya no. Con 16 variantes, la brecha de fidelidad no sigue al solapamiento, pero el error de clase sí. Crece con cuántos dominios se mezclan.
- **Cifras.**
  - Brecha contra solapamiento: ρ 0.01, p 0.95 (`README.md:13`).
  - Error de clase contra solapamiento: ρ 0.49, p 0.008 (`README.md:15`).
  - Brecha media: M2 2.54 contra M8 5.66; M8 queda peor que M2 en 26 de 28 pares (`UNA:106-107`, `:110`).
  - Con pesos uniformes, ρ 0.06 (`control.md:8`).
- **Arquitectura.** Final.
- **Estado.** **Corregido.** `veredicto.md` conserva ρ 0.45 (`UNA:112`). La frase «exp12 a escala: crece con el solapamiento» de `S17-22:41` y `SMED:38` queda desactualizada (`S26OCT:42`).
- **Vínculo.** Ninguno.
- **En el reporte.** Falta.

### exp20, parte 1 · `UH/results/experimento20`
- **Pregunta.** ¿Leer el directorio con el principio de tamaño corrige el sesgo de ancho que deja B1?
- **Hallazgo.** Sí, entre los agentes que contienen la pista. No crea contención: la envolvente chica que no contiene la imagen no se recupera. Hay dos fallas separables, el sesgo de ancho y la falta de contención.
- **Cifras.**
  - Piel: 736 → 1785 de 2005 (`README.md:11`).
  - Melanoma: 37 → 147 de 223 (`README.md:15`).
  - Mama y tórax no se recuperan (`README.md:22`).
  - Lectura (`README.md:25`).
- **Arquitectura.** Otros datos.
- **Estado.** Vigente. Según `S26OCT:83`, el script de fuera de distribución no se volvió a correr tras los pesos homo. Afecta a la parte 3, no a la parte 1.
- **Vínculo.** Principio de tamaño de Tenenbaum y Griffiths 2001 (`README.md:7`, `S17-22:28`). No está en Bib.
- **En el reporte.** Falta.

### exp22 · `UH/results/experimento22`
- **Pregunta.** ¿El principio de tamaño rompe algo en ETH-80, donde el registro está balanceado?
- **Hallazgo.** No: equivale a B1. Es candidato a reemplazarla.
- **Cifras.**
  - Imagen: 96.2 contra 96.3, con 1 decisión distinta de 656, a favor (`resumen.txt:4`, `:6`, `:8`).
  - Texto: 28.7 contra 28.5, con 8 de 411 decisiones distintas (`resumen.txt:11`, `:13`, `:15`). Los directorios oficiales de texto solo tienen 16 consultas (`README.md:10`).
- **Arquitectura.** Final (lectura) de los modelos del 23 sep (`README.md:3`).
- **Estado.** Vigente. No se probó con directorios de texto bien formados (`README.md:12`).
- **Vínculo.** Tenenbaum y Griffiths 2001.
- **En el reporte.** Falta. El reporte dice «La normalización necesaria es B1» (`C4:1345`).

### exp21 · `UH/results/experimento21`
- **Pregunta.** ¿Varias memorias guardan más que una (MedMNIST+)?
- **Hallazgo.** Con dominios separables, la memoria única iguala a la partición. Con 14 hallazgos superpuestos de tórax, la partición casi la duplica, porque la memoria única converge a un atractor («pleural thickening»).
- **Cifras.**
  - Modalidad 93.4 contra 93.5 (`resumen.txt:12`, `:14`).
  - Tórax 13.1 contra 24.4, con azar de 7.1 (`resumen.txt:36`, `:38`). El atractor (`:37`).
  - La predicción por palabras compartidas no se cumple (`README.md:19`).
- **Arquitectura.** Final (M con una hetero; mismo `resumen.txt`; `UNA:125`).
- **Estado.** Vigente con una errata: el README cita mama 88.5 (`README.md:16`), pero `resumen.txt:8` da 86.5 (`UNA:125`, `:129`).
- **Vínculo.** «Falsas memorias por mezcla» (`SMED:87`). Sin cita.
- **En el reporte.** Falta.

### Demo médico: ancho de la envolvente · `UH/results/medico_completo`, `UH/results/medico_balanceado`
- **Pregunta.** ¿Qué pasa con un registro desbalanceado?
- **Hallazgo.** Lo grande se traga a lo chico: la envolvente ancha contiene a las chicas. B1 no lo corrige porque no es un sesgo de conteo sino de ancho. Con un registro balanceado vuelve el triaje con abstención.
- **Cifras.**
  - La envolvente de tórax contiene el 93 % de las imágenes de piel y el 89 % de las de mama (`medico_completo/README.md:30-31`).
  - Melanoma 37/223 (`:14`). Fondo de ojo rechazado 0 % (`:18`). B1 no lo corrige (`:41`).
  - Balanceado: 99.6 % de lo respondido en modalidad (`medico_balanceado/README.md:12`), melanoma 175/223 (`:17`).
- **Arquitectura.** Otros datos.
- **Estado.** Vigente. Según `S26OCT:78`, los README médicos citan cifras de antes de los pesos homo.
- **Vínculo.** Efecto de tipicidad y descuido de la tasa base (`SMED:82-87`). Sin cita.
- **En el reporte.** Falta.

### Industrial monolítico · `UH/results/industrial_monolitica`
- **Pregunta.** En VisA, ¿una memoria única rutea y detecta como la partición?
- **Hallazgo.** Rutea igual, pero detecta menos de la mitad: partir estrecha las envolventes.
- **Cifras.**
  - Ruteo 99.1 % (`README.md:21`).
  - Detección con parches: 14.6 contra 39.3 (`README.md:5`, `:63-64`).
  - Envolvente de U: 28.0 de 32 niveles, contra 19.5 de cada especialista (`README.md:70`).
- **Arquitectura.** Final (idéntico con una hetero; `UNA:62`).
- **Estado.** Vigente.
- **Vínculo.** Ninguno.
- **En el reporte.** Falta.

### exp28 · `MED/results/experimento28`
- **Pregunta.** ¿Más datos ayudan en mama? ¿Igualar el registro cambia algo?
- **Hallazgo.** La memoria necesita más datos que los demás y aun así no llega. Igualar el registro cambia sensibilidad por especificidad: es el ancho de exp20 dentro de una modalidad.
- **Cifras.**
  - Memoria balanceada 77.3 contra 85-86 de los métodos por distancia (`README.md:19`, `:79`).
  - La revisión de la memoria no tiene valor propio (`README.md:74`).
- **Arquitectura.** Otros datos.
- **Estado.** Vigente. Ninguna síntesis lo cubre.
- **Vínculo.** Ninguno.
- **En el reporte.** Falta.

---

## Tema 5. Imagen y palabra: evocación de dominio contra palabra (4 fichas)

**Lo más fuerte:** exp17 (la evocación da el dominio, no la palabra), exp18 (la pertenencia generaliza, el atributo no) y exp19 (la tensión entre el índice y el especialista).

### Hemisferio visual (referencia) · `UH/results/hemisferio_visual`
- **Pregunta.** ¿Cuáles son las cifras de referencia del sistema final?
- **Hallazgo.** Fase A 99.9 %, fase B 631/656 y evocación 113/116. Es una referencia, no un hallazgo propio.
- **Cifras.** `README.md:3`; `C4:520-537`, `C4:558-562`.
- **Arquitectura.** Final.
- **Estado.** Vigente.
- **Vínculo.** Ninguno.
- **En el reporte.** Sí (`C4:510-635`). `C4:563` ya admite que la evocación «es laxa».

### exp17 · `UH/results/experimento17`
- **Pregunta.** ¿La evocación imagen → palabra devuelve una palabra específica?
- **Hallazgo.** Da el dominio, no la palabra. Por construcción, el llenado empareja cada imagen con la siguiente palabra de la clase. Con una palabra por objeto, los objetos se pisan en la envolvente. El color no generaliza más allá del color mayoritario del módulo, y falla confundiendo, no rechazando.
- **Cifras.**
  - Top-1 en el vocabulario 96.0 %, nombre de la clase 48.0 %, el mismo top-1 en 3 recuerdos 38.9 % (`parte_a_resumen.txt:6-8`, `:25`).
  - Palabra arbitraria por objeto: 40.8 % (azar 10), y 51.2 % en las vistas memorizadas (`README.md:33`).
  - El latente lleva el color: 41.1 contra 47.0 de medirlo directo (`README.md:45-48`).
  - Color en objetos conocidos: 74.4 contra una base de 55.5 (`README.md:61`, `:63`). En objetos nuevos: 57.8 contra 49.5 (`README.md:71`, `:73`). Los minoritarios fallan (`README.md:77`).
- **Arquitectura.** Final (B y C idénticos con una hetero; A cambia 1 imagen; `UNA:121-122`).
- **Estado.** Vigente.
- **Vínculo.** Dos procesos del reconocimiento: hay familiaridad y no hay recolección (`S17-22:50`). Sin cita en Bib.
- **En el reporte.** Falta.

### exp18 · `UH/results/experimento18`
- **Pregunta.** Si cada imagen se asocia con un atributo que tiene (patrón, pelo, techo), ¿lo devuelve en objetos nuevos?
- **Hallazgo.**
  - En objetos vistos, sí en parte.
  - En objetos nuevos responde el valor mayoritario, sin rechazar.
  - Hay dos cuellos de botella: el codificador borra el atributo, y aun con rasgos que lo traen, la contención no generaliza como un kNN.
  - La lectura tolerante baja el rechazo, pero casi no transfiere el atributo.
- **Cifras.**
  - Conocidos, normalizado balanceado: 62.7 a 72.3 % (`README.md:20-22`).
  - Nuevos: el valor mayoritario sale en 98-99 % y el minoritario en 1-6 % (`README.md:30-32`, `:36`). En cow acierta el 8 % (`:38`).
  - La sonda de vecinos da azar (`:48-53`). ResNet18-IN sin ajuste sí separa (cow 91.2) (`:70-72`).
  - Memoria contra kNN con los mismos rasgos: cow 59 contra 91 (`:94`).
  - Lectura tolerante (`:104-107`, `:113`).
- **Arquitectura.** Final (idéntico fila por fila; `UNA:120`).
- **Estado.** Vigente. Las lecturas son de conjunto cerrado, no recuerdos (`README.md:14`).
- **Vínculo.**
  - «La envolvente generaliza la pertenencia; el atributo lo decide la densidad» (`S17-22:11`).
  - «Contención por coordenada, no distancia» (`S17-22:16`).
  - Responder lo común se parece al efecto de tipicidad y al descuido de la tasa base (`SMED:82-87`).
  - Falta la predicación: Russell y Putnam (`S17-22:51`). Ninguno en Bib.
- **En el reporte.** Falta.

### exp19 · `UH/results/experimento19`
- **Pregunta.** Con una percepción que conserva el detalle (ResNet18-IN + PCA), ¿qué gana el especialista y qué pierde el índice?
- **Hallazgo.** El índice pierde mucho y el especialista gana poco. Una sola percepción no sirve a las dos partes: el índice necesita invariancia dentro de la clase y el especialista, sensibilidad.
- **Cifras.**
  - Ruteo 96.2 → 80.5; falsos 2 → 83 (`README.md:15-17`).
  - Objeto nuevo 89.2 → 60.8, con 14.4 % de falsos (`:22-23`).
  - Atributo: unos 5 puntos sobre el azar (`:44`). La tensión (`:48`). Hipótesis de dos percepciones (`:51`).
- **Arquitectura.** Anterior: copia `MAE-TMS-exp18`, de antes de una hetero. `S26OCT:34` da 79.6 con pesos homo.
- **Estado.** Vigente. El reporte usa 80.5 (`C4:787`); no está claro cuál corresponde al sistema final.
- **Vínculo.** Sistemas complementarios: las envolventes como el lado neocortical, sin el hipocampal (`S17-22:50`). Sin cita.
- **En el reporte.** Sí como columna «ImageNet» (`C4:767-804`, `C4:822-825`). Falta la lectura de la tensión entre índice y especialista y el lado del atributo.

---

## Tema 6. Límites: rechazo, ambigüedad y rivales (6 fichas)

**Lo más fuerte:** exp23 (tres estados de respuesta sin umbral), exp20 parte 3 (el rechazo es de cobertura, no superior) y exp24 (no supera a ningún rival actual con los mismos rasgos).

### Sonda de rechazo · `UH/results/rejection_probe`
- **Pregunta.** ¿La memoria rechaza sola las consultas fuera de dominio?
- **Hallazgo.** Rechaza 10 de 12 por contención pura. Las 2 que pasan tienen soporte real.
- **Cifras.** `report.md:26-27`, `:32`.
- **Arquitectura.** Final (igual con una hetero; `UNA:39`).
- **Estado.** Vigente. El `.md` de 3 clases quedó obsoleto (`report.md:3-10`).
- **Vínculo.** Ninguno.
- **En el reporte.** Sí (`C4:336-339`).

### exp20, parte 3 · `UH/results/experimento20`
- **Pregunta.** A igual aceptación de lo propio, ¿la memoria rechaza lo ajeno mejor que kNN, Mahalanobis o MSP?
- **Hallazgo.** No. Es un detector de cobertura: rechaza bien un órgano ajeno dentro de su modalidad y poco una modalidad entera fuera de su espacio.
- **Cifras.**
  - Lejano: fondo de ojo 24.2 contra MSP 100 (`README.md:37`); OCT 5.9 (`:39`); tórax de otro hospital 31.8 contra kNN 75.0 (`:40`).
  - Cercano: órgano ajeno 96.3 contra 97.7 de kNN (`:47`).
  - Hernia: nadie la detecta (`:46`).
  - Lectura (`:50-51`).
- **Arquitectura.** Otros datos.
- **Estado.** Vigente. No se volvió a correr tras los pesos homo (`S26OCT:83`).
- **Vínculo.** «Falla rechazando» describe la pertenencia, pero no es una ventaja (`S17-22:35`).
- **En el reporte.** Falta. El reporte advierte que el rechazo visual no se probó con fotos reales (`C4:1168-1169`, `C4:1675`).

### exp23 · `UH/results/experimento23`
- **Pregunta.** ¿El conjunto de especialistas que contienen la imagen sirve como respuesta?
- **Hallazgo.** Sí como mecanismo, no como herramienta.
  - La memoria responde en tres estados sin umbral: desconocido, claro y ambiguo. El estado predice el error.
  - A igual tamaño de lista no supera a kNN ni al clasificador.
  - El conformal marginal da listas más cortas, aunque la memoria cubre más lo raro.
- **Cifras.**
  - Argmax, claro contra ambiguo: órganos 97.3 → 69.9, piel 88.0 → 58.2. La verdad está en el conjunto ambiguo en el 95 % (`README.md:9-12`).
  - Igual tamaño de lista (`:20-23`).
  - En placas con varios hallazgos, el conjunto contiene a 2 o más presentes en el 72.1 % (azar 46.3) (`:32`).
  - Conformal: tórax 5.34 contra 8.74 candidatos (`:53`). Lo raro: neumonía 27 contra 7 (`:58`, `:63`).
- **Arquitectura.** Otros datos.
- **Estado.** Vigente, superado en parte por exp24 A (Mondrian).
- **Vínculo.** «Declara su incertidumbre en tres estados sin calibrar», análogo del sentimiento de saber (`SMED:85-87`). El reporte cita Hart 1965 para otra cosa (`C4:1567-1568`).
- **En el reporte.** Falta.

### exp24 · `UH/results/experimento24`
- **Pregunta.** Con los mismos rasgos, ¿la memoria gana a Mondrian, a los métodos incrementales, a Hopfield moderno o a HDC en alguna propiedad?
- **Hallazgo.** En ninguna. La contención por coordenada decide peor que la similitud. El principio de tamaño falla cuando todas las envolventes se solapan.
- **Cifras.**
  - Mondrian cubre la peor clase de tórax en el 88.0 %, la memoria en el 27.1 % (`README.md:11`, `:16`).
  - Incremental: 35.9 contra 75.6-86.4 (`:24-29`). Con rasgos ajustados, 93.1 contra 97.0 (`:38`).
  - Tamaño 35.9 contra la regla oficial 65.4 (`:37`, `:45`).
  - Lectura (`:44-47`).
- **Arquitectura.** Otros datos (sin cambio con una hetero; `UNA:15`).
- **Estado.** Vigente. No se volvió a correr tras los pesos homo (`S26OCT:83`).
- **Vínculo.** Ninguno.
- **En el reporte.** Falta.

### exp26 · `MED/results/experimento26`
- **Pregunta.** ¿Los modelos de fundación congelados (BiomedCLIP, RAD-DINO) mejoran el sistema médico?
- **Hallazgo.** No reemplazan al encoder ajustado. La MAE es la más sensible a la calidad de los rasgos. El rechazo de lo ajeno depende de la percepción.
- **Cifras.**
  - Órganos: 43.2 contra la mejor cabeza 83.7 (`README.md:14`).
  - Fondo de ojo rechazado al 99.9 % con BiomedCLIP (`:22`).
  - La brecha entre MAE y prototipos crece, al revés de lo predicho (`:28`).
- **Arquitectura.** Otros datos.
- **Estado.** Vigente.
- **Vínculo.** Ninguno.
- **En el reporte.** Falta.

### exp27 · `MED/results/experimento27`
- **Pregunta.** ¿RAD-DINO ajustado rompe el techo de tórax?
- **Hallazgo.** El techo está en los datos, cerca de 35 % balanceado. Con rasgos ajustados, la MAE se acerca a los prototipos.
- **Cifras.**
  - MAE 30.1 contra prototipos 34.8, AUROC 0.753 (`README.md:11`).
  - La resolución no suma (`:25`). Lectura (`:31-32`).
- **Arquitectura.** Otros datos.
- **Estado.** Vigente.
- **Vínculo.** Ninguno.
- **En el reporte.** Falta.

---

## Conteo

| Tema | Fichas | En `C4` | Parcial | Faltan |
|---|---|---|---|---|
| 1. Directorio como índice y metamemoria | 4 | 2 (exp15, líneas base) | 0 | 2 (exp7, exp8) |
| 2. Perspectiva y pérdida de un miembro | 4 | 0 | 1 (exp10) | 3 (exp9, exp25, piloto) |
| 3. Reconocer y recordar | 7 | 6 | 0 | 1 (exp29) |
| 4. Tamaño, ancho y partición | 8 | 1 (exp11) | 0 | 7 (exp12, exp20 parte 1, exp22, exp21, médico, industrial monolítico, exp28) |
| 5. Imagen y palabra | 4 | 1 (hemisferio visual) | 1 (exp19) | 2 (exp17, exp18) |
| 6. Límites | 6 | 1 (sonda de rechazo) | 0 | 5 (exp20 parte 3, exp23, exp24, exp26, exp27) |
| **Total** | **33** | **11** | **2** | **20** |

De los 20 que faltan, 7 son de ETH-80 con 8 módulos (exp7, exp8, exp9, exp12, exp17, exp18 y exp22) y 13 son de otros datos (MedMNIST+ o VisA).

## Los 5 hallazgos que más fuerza darían a la sección

1. **exp8. El directorio leído al revés es metamemoria.** Devuelve la envolvente del dominio, no un ejemplar, igual para el propio que para el ajeno presenciado. Falla callando, nunca respondiendo mal. Falta en el reporte.
2. **exp10. Los directorios perspectivales sin centro igualan al pizarrón.** Con encadenado en imagen y agregado en texto; alcance y comparación son operaciones distintas. Está solo de pasada en el reporte.
3. **exp9. Al perder un miembro, se pierde la respuesta y no la ubicación.** La sustitución confabula y la descripción conserva la clase. La familiaridad es reconocer: 98.3 % contra 16.1 %. Falta, y conviene volver a correrlo con directorios perspectivales y una hetero.
4. **exp17 con exp18. La evocación da el dominio, no la palabra.** La pertenencia generaliza; el atributo lo decide la densidad y falla confundiendo hacia lo común. Falta.
5. **exp20 parte 1 con exp22. El principio de tamaño corrige el sesgo de ancho y equivale a B1 donde B1 funciona** (1 decisión distinta de 656). Falta, y obliga a matizar «la normalización necesaria es B1» (`C4:1345`).

Ya están en el reporte y sirven de ancla: exp11 corregido (decidir antes de recordar), exp16 con el codificador por pliegue (generaliza por envolvente) y la lesión de `homo_marginal`.

## Lo que no está claro o está desactualizado

- `S26OCT:38` (90 de 411 con 16 interacciones) no coincide con `experimento9/formacion_texto/curva.json`: 90 corresponde a «0 transactivo» (`:21`) y con 16 da 100 (`:57`).
- `experimento21/README.md:16` cita mama 88.5; el `resumen.txt:8` actual da 86.5.
- `experimento15/veredicto.md:9` (90.6) y `experimento12/veredicto.md` (ρ 0.45) son anteriores a sus README.
- `SMED:72` usa la fila de pérdida de exp25, que no mide pérdida (`MED/results/experimento25/README.md:23`).
- `S17-22:41` y `SMED:38` dicen que la ventaja de partir crece con el solapamiento. exp12 ya no lo sostiene (`S26OCT:42`), aunque el resultado de tórax en exp21 sigue en pie.
- exp8, exp9 y exp10 se corrieron con un protocolo anterior: directorios globales, directorio visual sin variantes y homo. Sus mecanismos no dependen de las homo, pero sus cifras no son las del sistema final.
- exp19: el reporte usa 80.5 y `S26OCT:34` da 79.6 con pesos homo. No está claro cuál es la vigente.
- `SMED:92` (piloto, 73.4 % y 2.5 lecturas) no coincide con `piloto_modulos/README.md:5` (79.0 %). Puede ser otra etapa; no se verificó.
- Vínculos naturales sin cita en Bib: Nelson y Narens, Russell, Vygotsky, Hutchins, Wood-Bruner-Ross, Peirce, Kripke, Putnam, Tenenbaum-Griffiths, dos procesos y sistemas complementarios. Las de exp29 (Rogers, Woollams, Hodges) no se comprobaron.
- No se revisaron a fondo y quedan fuera de las fichas: `cascada_modulos`, `deriva_olvido`, `olvido_privacidad`, `etapa1_ruteo_dirigido`, `etapa2_evidencia`, `cierre_mae`, `enrutador_flota`, `industrial`, `industrial_clip`, `replica_ablaciones`, `red_sintetica` y `parametros_mae`. El catálogo los ubica en VisA (aplicaciones). `missing_cue` (pista faltante) tampoco tiene ficha.
- Pertenecen a otras partes del arco y no se fichan aquí: exp1 (3 módulos), la ablación, exp2-6, `calibracion_evaluacion_fija` y `rescate_lexico` (lectura B1 y escalado).
