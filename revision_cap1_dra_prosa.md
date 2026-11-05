# Comentarios de la Dra. Olmos: Resumen, Abstract, Introducción y Capítulo 1

Base: `una-hetero` @ `6237119`, rama `cap1-dra`. Archivos tocados: `.tex_uacj/Resumen.tex`, `Abstract.tex`, `Introduccion.tex`, `Capitulo1.tex`; `.tex8/secciones/02`, `04`, `05` y `07` (y los `Capitulo2` a `5` regenerados). No se tocó `generar_capitulos.py`.

## Compilación y medidas

- `generar_capitulos.py`: «líneas de .tex8 que no aparecen en la salida: 0».
- `.tex_uacj` (XeLaTeX, tres pasadas y bibtex): 0 errores, 0 referencias indefinidas, 183 páginas (antes 180). Los tres `Overfull \vbox` del log están en el Capítulo 4 (páginas 111 a 163) y no vienen de este cambio.
- `.tex8` (pdflatex, tres pasadas y bibtex): 0 errores, 0 referencias indefinidas.
- Una página cada uno, medido con PyMuPDF (borde inferior de la última línea de texto):

| Página | Páginas | Texto hasta | Al borde inferior |
|---|---|---|---|
| Resumen | 1 (p. 7 del PDF) | 230.1 mm | 49.3 mm |
| Abstract | 1 (p. 8) | 230.2 mm | 49.2 mm |
| Introducción | 1 (p. 18) | 241.9 mm | 37.5 mm |

La Introducción llena la caja de texto hasta la última línea. Cualquier palabra más la pasa a una segunda página.

## Cifras del Resumen, verificadas

| Cifra | Fuente | Coincide |
|---|---|---|
| 26.25 → 98.75 % en 80 consultas | `results/fase1_tres_modulos/exp4_directory_formation/results_formation.csv:2` (`A_interleaved,1,0.2625`) y `:81` (`A_interleaved,80,0.9875`); columna `mature_acc` | sí |
| 96.8 frente a 96.9 % | `results/experimento11_protocolo_corregido/README.md:177` (N = 200: protocolo corregido 96.8, EHAM única 96.9) | sí |
| 3.1 frente a 10.9 % | `results/experimento11_protocolo_corregido/README.md:267` (imagen, otro dominio, N = 200: 3.0 → 3.1; M: 10.9) | sí |
| 38 de 40 | `results/lineas_base/README.md:110` y `:159-160` (acepta 2 de 40, las dos con un token del vocabulario) | sí (40 − 2) |

Ninguna se corrigió.

## Cambios de «uso» a «experiencia» (15)

| # | Lugar | Antes | Ahora |
|---|---|---|---|
| 1 | `Resumen.tex` | «módulos que aprenden con el uso quién sabe qué» | «módulos especialistas que aprenden de su experiencia a quién preguntar» (texto aprobado) |
| 2 | `Resumen.tex` | «el directorio emerge del uso» | «el directorio emerge de la experiencia» (texto aprobado) |
| 3 | `Abstract.tex` | «modules that learn through use who knows what» | «modules that learn from experience whom to ask» |
| 4 | `Abstract.tex` | «the directory emerges from use» | «the directory emerges from experience» |
| 5 | `Introduccion.tex` | «módulos especialistas que aprenden con el uso a quién preguntar» | «un directorio que emerge de la experiencia» (párrafo reescrito) |
| 6 | `Capitulo1.tex`, Definición del problema | «y aprende con el uso a quién preguntar» | «y aprende de la experiencia a quién preguntar» |
| 7 | `Capitulo1.tex`, Definición, parte 1 | «Que el directorio emerja del uso» | «Que el directorio emerja de la experiencia» |
| 8 | `Capitulo1.tex`, Justificación | «La primera es que el directorio se forma con el uso.» | «La primera es que el directorio emerge de la experiencia.» |
| 9 | `Capitulo1.tex`, Alcances | «Lo que se forma con el uso es el directorio.» | «Lo que emerge de la experiencia es el directorio.» |
| 10 | `Capitulo1.tex`, Preguntas | «y aprende con el uso a quién preguntar» | «y aprende de la experiencia a quién preguntar» |
| 11 | `.tex8/secciones/02_marco_teorico.tex:333` | «y lo que se forma con el uso es el directorio» | «y lo que emerge de la experiencia es el directorio» |
| 12 | `.tex8/secciones/04_metodologia.tex:15` | «el directorio se forma con el uso, desde vacío» | «el directorio emerge de la experiencia, desde vacío» |
| 13 | `.tex8/secciones/05_resultados.tex:73` | `\paragraph{El directorio se forma con el uso.}` | `\paragraph{El directorio emerge de la experiencia.}` |
| 14 | `.tex8/secciones/07_conclusiones.tex:8` | «el directorio emerge del uso y» | «el directorio emerge de la experiencia y» |
| 15 | `.tex8/secciones/07_conclusiones.tex:278` | «el directorio emerge del uso, y» | «el directorio emerge de la experiencia, y» |

En total son 15 apariciones: 5 en Resumen, Abstract e Introducción, que se reescribieron, y 10 cambios puntuales (5 en el Capítulo 1 y 5 en `.tex8`). El arco de la investigación decía «el directorio se forma con la experiencia» y ahora dice «emerge de la experiencia».

Quedan dos apariciones fuera de los archivos asignados, que no toqué: `.tex8/main.tex:84` («que se forma con el uso es el directorio», en el abstract del `.tex8`) y `.tex8/secciones/01_introduccion.tex:76` («se forma con el uso»). Ninguna sale en el reporte UACJ.

## Capítulo 2 (Trabajo relacionado)

El párrafo «Memorias asociativas» describía a Kosko, Hopfield, Krotov y Ramsauer con una frase cada uno, lo mismo que ahora hacen los Antecedentes. Lo recorté a una lista con sus citas. No usé una remisión `Sección~\ref{...}` porque `.tex8` compila solo y no tiene los Antecedentes del Capítulo 1: la etiqueta quedaría indefinida en `.tex8`.

- **Antes:** «La EAM pertenece a la familia de la memoria asociativa no holográfica de Willshaw y colaboradores~\cite{willshaw1969nonholographic}, las memorias asociativas bidireccionales de Kosko~\cite{kosko1988bidirectional}, la red de Hopfield, que recupera un recuerdo completo a partir de una parte suficiente~\cite{hopfield1982neural}, la memoria distribuida dispersa~\cite{kanerva1988sparse}, las memorias densas, de mayor capacidad~\cite{krotov2016dense}, y las redes de Hopfield modernas, de estados continuos~\cite{ramsauer2021hopfield}.»
- **Ahora:** «La EAM pertenece a la familia de la memoria asociativa no holográfica de Willshaw y colaboradores~\cite{willshaw1969nonholographic}, la memoria distribuida dispersa~\cite{kanerva1988sparse} y las memorias de Kosko y de Hopfield, con las variantes densas y modernas de esta última~\cite{hopfield1982neural,kosko1988bidirectional,krotov2016dense,ramsauer2021hopfield}.»

Nada más cambió en el capítulo.

## Fuentes de los Antecedentes

Texto de cada fuente en `C:\Users\aq99l\Projects\cotejo_trabajo\corpus_cache\texto\<clave>.txt`. Todas las claves ya estaban en `.tex8/referencias.bib`.

| Trabajo | Clave | Texto disponible | Cifras y afirmaciones, con línea |
|---|---|---|---|
| Hopfield (1982) | `hopfield1982neural` | solo el resumen | componentes simples, procesamiento paralelo asíncrono, recuerdo completo desde una parte, generaliza, reconoce lo familiar, categoriza, corrige errores, poco sensible a fallas (`:53`). La capacidad de $0.14N$ y la fusión de recuerdos se citan de Krotov y Hopfield (`krotov2016dense.txt:40`). La limitación de las memorias conexionistas se cita de Pineda y colaboradores (`pineda2021entropic.txt:92`). |
| Kosko (1988) | `kosko1988bidirectional` | **no** (33 bytes, vacío) | Sin cifras. La descripción (dos capas, una matriz, la recuperación va y viene hasta estabilizarse) no tiene línea de respaldo en el corpus; la limitación se cita de `pineda2021entropic.txt:92`. |
| Krotov y Hopfield (2016) | `krotov2016dense` | completo | el problema de guardar más recuerdos que neuronas (`:14`); interacciones de orden mayor (`:14`, `:19`); capacidad no lineal (`:146`); dualidad con una red de una capa oculta y polinomios rectificados (`:12`); 2000 memorias (`:331`); todas las de potencia 3 por debajo del 1.6 % (`:336`); memorias aprendidas por retropropagación para minimizar el error de clasificación (`:333`). |
| Pineda, Fuentes y Morales (2021) | `pineda2021entropic` | completo | contraste entre memorias simbólicas y conexionistas, y las cinco propiedades (`:92`); una tabla por dígito (`:275`); unidad central de control que envía la operación a todas las tablas y recoge estado y entropía (`:185`, `:237`); al llenar, precisión alta y aceptación creciente (`:325`); semejanza con entropía baja y moderada (`:403`); con ruido, la precisión baja (`:401`). |
| Pineda y Morales (2022) | `pineda2022weighted` | completo | celdas encendidas o apagadas y el refuerzo de la W-EAM (`:82`); DIMEx100 (`:270`); 22 tablas (`:382`, `:548`); decisión por fuerza de la pista y entropía (`:392`); con 16 filas, 11 tablas que aceptan y cerca del 80 % de acierto, precisión y exhaustividad sobre 0.8 (`:392`); menor error fonético por rechazo de segmentos mal alineados (`:548`); mismos parámetros en las 22 tablas, pregunta abierta (`:548`). |
| Morales y Pineda (2025) | `morales2025missing` | solo el resumen | relación de cuatro dimensiones, plano indeterminado, pista faltante, tres métodos, MNIST con EMNIST, promesa para conjuntos grandes con pocos recursos (`:15`). Sin cifras. Que este sistema usa el tercer método sale de `.tex8/secciones/02_marco_teorico.tex` (Sección 2.2). |
| Hernández, Morales y Pineda (2026) | `hernandez2026cifar` | preprint de arXiv (2405.12500v1, título «Entropic associative memory for real world images») | datos anteriores estructurados (`:41`); una sola tabla con CIFAR-10 (`:41`, `:442`); el clasificador asigna la clase de lo recuperado (`:375`); cadenas de asociación (`:10`, `:442`); desempeño por debajo del clasificador (`:449`). Sin cifras, porque el texto es el preprint y el `.bib` cita la versión de *Pattern Recognition*; el preprint da 66.97 % de acierto (`:377`), que no usé. |

No usé `ramsauer2021hopfield` porque no tiene texto en el corpus. `pineda2023imagery` tampoco (215 bytes, una página de error), y `lopez2025hyperopt` solo tiene el resumen. Las dos siguen citadas en los Capítulos 2 a 4. `morales2024hetero` no está en el `.bib`.

## Dudas

1. **Sujeto en el Resumen aprobado.** En «la mezcla de dominios baja de 10.9 a 3.1 % de las imágenes y rechaza 38 de 40 consultas ajenas», el sujeto gramatical de «rechaza» es «la mezcla». Lo dejé tal cual porque el texto está aprobado. En el Abstract escribí «and the system rejects». Una corrección posible sería «…de las imágenes, y el sistema rechaza 38 de 40 consultas ajenas».
2. **El rechazo de 38 de 40.** Las 40 consultas se escribieron sin palabras del vocabulario (`results/lineas_base/README.md:44`), y en texto el rechazo equivale a la pertenencia al vocabulario. La limitación (a) ya lo dice, pero el Resumen da la cifra sin esa salvedad.
3. **Kosko sin texto.** La descripción de la memoria bidireccional no tiene respaldo en el corpus. Conviene cotejarla con el artículo.
4. **Hernández y colaboradores.** El texto disponible es el preprint, con otro título. Por eso el párrafo va sin cifras.
5. **Arco y objetivo general.** El arco abre ahora la Sección 1.3, antes del enunciado del objetivo general, que sigue siendo una oración en infinitivo sin cambios.

## Texto viejo y nuevo

### `.tex_uacj/Resumen.tex`

**Antes:**

```latex
\chapter*{Resumen}
\markboth{Resumen}{Resumen}
\thispagestyle{empty}
Una memoria asociativa entrópica tiene un techo: conforme se llena, su entropía crece,
acepta de más y recuerda peor.
Este trabajo reparte el contenido entre módulos que aprenden con el uso quién sabe qué,
como en la \emph{memoria transactiva} de Wegner~\cite{wegner1987transactive}, sobre las
memorias de Pineda y Morales \cite{pineda2022weighted,morales2025missing}, y lo estudia en cinco fases.
En un prototipo de tres módulos, con cuatro memorias cada uno, pistas cuantizadas por
signo y un mediador, el directorio emerge del uso: la fase madura acierta el 26.25\,\% de 80
consultas tras una interacción y el 98.75\,\% tras 80, dentro de muestra, y con el orden
bloqueado, 33.75\,\% mientras solo ve una clase.
Leerlo pide dividir entre los registros de cada módulo (B1); sin dividir, 53.75\,\%.
Con ocho módulos, uno por clase de ETH-80~\cite{leibe2003eth80} y con una memoria
heteroasociativa de palabras e imágenes, el sistema acierta lo mismo que una sola memoria (96.8 frente
a 96.9\,\%), pero responde menos con un dominio ajeno (3.1 frente a 10.9\,\% de las
imágenes).
En texto iguala a decisores simples sobre los mismos vectores (81.2 frente a
76.0--81.5\,\%) y acepta 2 de 40 consultas fuera de dominio, como un voto por vocabulario,
contra 40 de los decisores de coseno.
Leído al revés, el directorio devuelve la envolvente de cada dominio presenciado y no un
ejemplar.
Una imagen evoca una palabra de su clase el 96.0\,\% de las veces, y su nombre el
48.0\,\%.
Una demostración conecta voz y cámara en tiempo real, sin cifras de acierto.
Repartir evita el techo en fidelidad y mezcla de dominios; en acierto de clase empata.


\noindent\textbf{Palabras clave}: memoria transactiva, memoria asociativa entrópica, memoria
heteroasociativa, sistemas distribuidos, enrutamiento de consultas, recuperación
multimodal.
```

**Ahora:**

```latex
\chapter*{Resumen}
\markboth{Resumen}{Resumen}
\thispagestyle{empty}
Un grupo recuerda más que cada uno de sus miembros cuando cada uno sabe quién sabe qué;
Wegner~\cite{wegner1987transactive} llamó a esta organización \emph{memoria transactiva}.
Las memorias asociativas entrópicas de Pineda y Morales
\cite{pineda2022weighted,morales2025missing} guardan lo que registran como una tabla de
conteos, reconocen lo que tiene soporte, recuperan muestreando y rechazan lo que no
contienen.
Su límite es un techo: una sola memoria con todo el contenido, conforme se llena, acepta
de más y recuerda peor.
Aquí se reparte el contenido entre módulos especialistas que aprenden de su experiencia
a quién preguntar, en un sistema distribuido de memoria transactiva sin clasificadores
discriminativos.
El sistema se desarrolló en cinco fases: de un prototipo de tres módulos a ocho módulos
sobre ETH-80~\cite{leibe2003eth80}, cada uno con una memoria de palabras e imágenes, y a
una demostración con voz y cámara.
Con tres módulos, el directorio emerge de la experiencia: el acierto pasa del 26.25 al
98.75\,\% en 80 consultas, medido sobre las que lo forman.
Con ocho, el sistema acierta lo mismo que una sola memoria (96.8 frente a 96.9\,\%), pero
la mezcla de dominios baja de 10.9 a 3.1\,\% de las imágenes y rechaza 38 de 40 consultas
ajenas.
Repartir evita el techo en el recuerdo y no en el acierto.
Lo que aporta la memoria transactiva es un directorio que nadie programa, el rechazo y el
recuerdo en ambas direcciones; su acierto depende de un codificador visual entrenado con
la clase.


\noindent\textbf{Palabras clave}: memoria transactiva, memoria asociativa entrópica, memoria
heteroasociativa, sistemas distribuidos, enrutamiento de consultas, recuperación
multimodal.
```

### `.tex_uacj/Abstract.tex`

**Antes:**

```latex
\chapter*{Abstract}
\markboth{Abstract}{Abstract}
\thispagestyle{empty}
An entropic associative memory has a ceiling: as it fills, its entropy grows, it accepts
too much and recalls worse.
This work splits the content among modules that learn through use who knows what, as in
Wegner's \emph{transactive memory}~\cite{wegner1987transactive}, on the memories of
Pineda and Morales \cite{pineda2022weighted,morales2025missing}, and studies it in five
phases.
In a three-module prototype, with four memories each, sign-quantized cues and a mediator,
the directory emerges from use: the mature phase routes correctly 26.25\,\% of 80 queries
after one interaction and 98.75\,\% after 80, in-sample, and with blocked order,
33.75\,\% while it sees one class.
Reading it requires dividing by each module's records (B1); without dividing, 53.75\,\%.
With eight modules, one per ETH-80 class~\cite{leibe2003eth80} and with a heteroassociative
memory of words and images, the system is as accurate as a single memory (96.8 against
96.9\,\%), but answers less often with a foreign domain (3.1 against 10.9\,\% of the
images).
On text it matches simple decision rules on the same vectors (81.2 against
76.0--81.5\,\%) and accepts 2 of 40 out-of-domain queries, like a vocabulary vote,
against 40 for the cosine rules.
Read backwards, the directory returns the envelope of each witnessed domain, not an
exemplar.
An image evokes a word of its class 96.0\,\% of the time, and its name 48.0\,\%.
A demonstration connects voice and camera in real time, with no accuracy figures.
Splitting avoids the ceiling in fidelity and domain mixing; in class accuracy it ties.


\noindent\textbf{Keywords}: transactive memory, entropic associative memory, heteroassociative
memory, distributed systems, query routing, multimodal retrieval.
```

**Ahora:**

```latex
\chapter*{Abstract}
\markboth{Abstract}{Abstract}
\thispagestyle{empty}
A group remembers more than each of its members when each one knows who knows what;
Wegner~\cite{wegner1987transactive} called this organization \emph{transactive memory}.
The entropic associative memories of Pineda and Morales
\cite{pineda2022weighted,morales2025missing} store what they register as a table of
counts, recognize what has support, retrieve by sampling and reject what they do not
contain.
Their limit is a ceiling: a single memory holding all the content, as it fills, accepts
too much and recalls worse.
Here the content is split among specialist modules that learn from experience whom to
ask, in a distributed transactive memory system without discriminative classifiers.
The system was developed in five phases: from a three-module prototype to eight modules
on ETH-80~\cite{leibe2003eth80}, each with a memory of words and images, and to a
demonstration with voice and camera.
With three modules, the directory emerges from experience: accuracy rises from 26.25 to
98.75\,\% over 80 queries, measured on the queries that form it.
With eight, the system is as accurate as a single memory (96.8 against 96.9\,\%), but
domain mixing falls from 10.9 to 3.1\,\% of the images, and the system rejects 38 of 40
out-of-domain queries.
Splitting avoids the ceiling in recall and not in accuracy.
What transactive memory contributes is a directory that nobody programs, rejection and
recall in both directions; its accuracy depends on a visual encoder trained with the
class.


\noindent\textbf{Keywords}: transactive memory, entropic associative memory, heteroassociative
memory, distributed systems, query routing, multimodal retrieval.
```

### `.tex_uacj/Introduccion.tex`

**Antes:**

```latex
\chapter*{Introducción}\label{introduccion}\label{sec:introduccion}
\thispagestyle{empty}
\markboth{Introducción}{Introducción}
Un grupo puede recordar más que cualquiera de sus miembros porque cada uno sabe quién
sabe qué.
Wegner~\cite{wegner1987transactive} llamó \emph{memoria transactiva} a esta organización
y después la describió como una red de computadoras~\cite{wegner1995computer}.
Las memorias asociativas entrópicas de Pineda y Morales
\cite{pineda2021entropic,pineda2022weighted,morales2025missing} guardan lo que registran
como conteos, reconocen, recuperan muestreando y rechazan lo que no contienen.
Una sola tiene un techo: su entropía crece con lo que guarda, y con ella las aceptaciones
falsas.
Este trabajo reparte el contenido entre módulos especialistas que aprenden con el uso a
quién preguntar, y lo estudia en cinco fases.
Un prototipo de tres módulos mostró que el directorio emerge de la experiencia, y con él
se eligió leerlo dividiendo entre los registros de cada módulo (B1).
Después se pasó a ocho módulos sobre ETH-80~\cite{leibe2003eth80}, cada uno con una
memoria heteroasociativa de palabras e imágenes.
En ese paso cambiaron varias cosas a la vez, y el efecto del tamaño se midió aparte, con
una sola memoria contra la partición y con memorias de dos y de ocho clases.
Con los ocho módulos se hicieron las comparaciones con decisores simples y con un
codificador sin la pérdida de clase, y se estudiaron propiedades como la lectura inversa
del directorio y la pérdida de un módulo.
La última fase es una demostración con voz y cámara en tiempo real, sin cifras de acierto.
El reparto evita el techo en la fidelidad del recuerdo y en la mezcla de dominios; en el
acierto de clase empata con la memoria única.
Los Capítulos~\ref{cap:pp} a~\ref{conclusiones} presentan el problema, el marco teórico,
el desarrollo por fases, los resultados y las conclusiones, y el Apéndice~\ref{apendiceA}
ubica los experimentos.
```

**Ahora:**

```latex
\chapter*{Introducción}\label{introduccion}\label{sec:introduccion}
\thispagestyle{empty}
\markboth{Introducción}{Introducción}
En un sistema distribuido con nodos especializados, cada consulta tiene que llegar al
nodo que sabe responderla~\cite{crespo2002routing,callan2000distributed}.
Los grupos de personas lo resuelven con una \emph{memoria
transactiva}~\cite{wegner1987transactive}, en la que cada miembro guarda lo que sabe y un
directorio de quién sabe qué, y Wegner la describió como una red de
computadoras~\cite{wegner1995computer}.

Entre las memorias asociativas, que devuelven un recuerdo completo a partir de una parte
de él~\cite{hopfield1982neural}, la entrópica~\cite{pineda2021entropic,pineda2022weighted}
guarda lo registrado como una tabla de conteos entre rasgos y valores.
Reconoce una pista cuando cada rasgo tiene soporte, recupera muestreando y rechaza lo que
no contiene, y su versión heteroasociativa (EHAM) recupera desde un dominio lo asociado en
otro~\cite{morales2025missing}.
Como la entropía crece con lo que la tabla guarda, una sola memoria con todo el contenido
rechaza y recuerda peor conforme se llena, y ese es su \emph{techo entrópico}.

Aquí, cada especialista es un \emph{módulo} con una memoria de contenido y un
\emph{directorio} que registra quién resolvió cada consulta presenciada.
Las consultas son palabras en inglés, representadas con
fastText~\cite{bojanowski2017fasttext}, o imágenes de las ocho clases de
ETH-80~\cite{leibe2003eth80}.

Este trabajo construye con esos módulos un sistema de memoria transactiva, lo hace crecer
por fases y lo compara con una sola memoria y con decisores simples.
A los sistemas computacionales les ofrece enrutar sin compuerta entrenada ni catálogo
escrito a mano, con un directorio que emerge de la experiencia y decisiones que se
rastrean hasta sus conteos.
Los Capítulos~\ref{cap:pp} a~\ref{conclusiones} presentan el problema, el marco teórico,
el desarrollo por fases, los resultados y las conclusiones, y el Apéndice~\ref{apendiceA}
ubica cada experimento.
```

### Capítulo 1, 1.1 Antecedentes (con el arco de la investigación en la versión vieja)

**Antes:**

```latex
\section{Antecedentes}

\paragraph{Memoria transactiva.}
Wegner~\cite{wegner1987transactive} describió la memoria transactiva como la memoria de
un grupo: cada miembro guarda lo que sabe y, además, un directorio de lo que saben los
demás.
El directorio no repite el contenido.
Solo indica a quién preguntar.
En un trabajo posterior, Wegner formuló el mismo fenómeno como un modelo de red de
computadoras~\cite{wegner1995computer} y nombró tres procesos: la actualización del
directorio, en la que los miembros anotan quién resolvió cada interacción; la asignación
de información, que lleva lo nuevo al miembro que corresponde; y la coordinación de la
recuperación, que envía cada consulta directamente al especialista.
La analogía entre un grupo de personas y una red de nodos especializados es, por lo
tanto, del propio Wegner.
Lo que su modelo deja abierto es con qué memoria se construye cada nodo y cómo se
forma su directorio.

\paragraph{Memorias asociativas entrópicas.}
Pineda, Fuentes y Morales propusieron una memoria asociativa que guarda lo registrado
como una tabla de frecuencias entre rasgos y valores~\cite{pineda2021entropic}.
Con esa tabla, la memoria hace tres operaciones: registrar una entrada, reconocerla
cuando cada uno de sus rasgos tiene soporte en lo registrado, y recuperar un patrón
muestreando los conteos.
Lo que no tiene soporte se rechaza, y la entropía de la tabla mide qué tan determinada
está la memoria.
La variante ponderada (W-EAM) apareció en el aprendizaje fonético~\cite{pineda2022weighted}
y se ha usado con símbolos manuscritos~\cite{morales2022manuscript}, en la imaginería
\cite{pineda2023imagery} y con las imágenes naturales de CIFAR-10~\cite{hernandez2026cifar};
la optimización multiobjetivo de sus hiperparámetros se estudió
en~\cite{lopez2025hyperopt}.
La extensión heteroasociativa (EHAM) guarda pares de objetos de dominios distintos en
una sola memoria, de modo que una pista en un dominio recupera el objeto asociado en el
otro, y propone cómo completar esa recuperación cuando solo se tiene la pista de uno de
los dos dominios~\cite{morales2025missing}.
Ninguno de estos trabajos usa directorios ni especialistas que cooperen
(Sección~\ref{sec:tmt}).

\paragraph{Representaciones.}
Una memoria entrópica opera sobre vectores cuantizados, así que las palabras y las
imágenes tienen que llegarle como vectores.
En este trabajo, las palabras son vectores fastText~\cite{bojanowski2017fasttext}, el
vocabulario de cada dominio sale de ConceptNet~5.7~\cite{speer2017conceptnet} y las
consultas se dividen en tokens con spaCy~\cite{honnibal2020spacy}.
Las imágenes son códigos de un autocodificador con la arquitectura ResNet18
\cite{he2016resnet}, que parte de los pesos de ImageNet y se entrena sobre
ETH-80~\cite{leibe2003eth80}.
ETH-80 tiene ocho categorías con diez objetos cada una, fotografiados desde 41 puntos
de vista, y varias de sus clases se parecen entre sí: \texttt{apple}, \texttt{pear} y
\texttt{tomato} son frutas redondas, y \texttt{cow}, \texttt{horse} y \texttt{dog} son
cuadrúpedos.
En el sistema de ocho módulos, el codificador se entrena con dos pérdidas: la
reconstrucción y una entropía cruzada de clase de peso 0.1 (Sección~\ref{sec:percepcion}).
La cabeza de clasificación no interviene en ninguna decisión del sistema, pero la
pérdida de clase da forma al espacio latente que las memorias guardan.

\paragraph{Qué falta.}
Hay, entonces, una teoría de la memoria de grupo que ya se pensó como red, y una familia
de memorias que reconocen, recuperan y rechazan con operaciones explícitas sobre
conteos.
No hay un sistema que las junte.
Tampoco hay una medida de lo que la memoria asociativa agrega cuando se la compara con
decisores simples que usan los mismos vectores, como un voto por palabras del
vocabulario o el vecino más cercano.
Sin esa comparación no se puede saber si un resultado se debe a la memoria o a la
representación que la alimenta.

\paragraph{Arco de la investigación.}
Este trabajo construyó ese sistema en cinco fases, y cada una partió de lo que dejó la
anterior.
La primera fue un prototipo de tres módulos (\texttt{apple}, \texttt{horse} y
\texttt{car}), con cuatro memorias por módulo, pistas de texto cuantizadas por signo y un
mediador, en el que se vio que el directorio se forma con la experiencia.
En ese prototipo, la lectura cruda del directorio favorecía al módulo con más registros,
y en la segunda fase se eligió leerlo dividiendo entre ellos (normalización B1).
La tercera pasó a las ocho clases de ETH-80, y al hacerlo cambiaron a la vez el
codificador, la cuantización, las memorias por módulo, el banco de consultas y el
mediador.
Por eso la comparación entre tres y ocho módulos no aísla el efecto de crecer, que se
mide con dos experimentos propios: una sola memoria contra la partición y una memoria de
dos clases contra una de ocho.
Con el sistema de ocho módulos, la cuarta fase estudió sus propiedades, entre ellas la
lectura inversa del directorio, la pérdida de un miembro y la evocación de palabras
desde imágenes.
La quinta conectó el sistema a la voz y a la cámara en tiempo real, como demostración
de integración.
```

**Ahora:**

```latex
\section{Antecedentes}

Los tres primeros trabajos son memorias asociativas de la tradición de las redes
neuronales; los cuatro siguientes, la memoria asociativa entrópica y sus aplicaciones.

\paragraph{Red de Hopfield.}
Hopfield~\cite{hopfield1982neural} buscó propiedades de cómputo que surgieran de forma
colectiva en un sistema con muchos componentes simples e iguales, las neuronas.
Su modelo, basado en aspectos de la neurobiología y fácil de llevar a circuitos integrados,
evoluciona por procesamiento paralelo asíncrono, y de esa evolución sale una memoria
direccionable por contenido que devuelve un recuerdo completo a partir de cualquier parte
suficientemente grande de él.
La misma red generaliza, reconoce lo familiar, categoriza y corrige errores, y la falla
de un componente le afecta poco.
Su límite es la capacidad.
Con patrones aleatorios guarda del orden de $0.14N$ recuerdos, con $N$ neuronas, y si se
le dan más, recuerdos vecinos se funden en un estado que no corresponde a
ninguno~\cite{krotov2016dense}.
Además, según Pineda y colaboradores, las memorias de esta tradición no guardan una
representación declarativa, no rechazan lo que no contienen y reproducen en lugar de
construir~\cite{pineda2021entropic}.
La memoria entrópica pertenece a esta familia, y la fusión de recuerdos en una red que
guarda demasiado es un techo del mismo tipo que el que en este trabajo motiva repartir el
contenido.

\paragraph{Memoria asociativa bidireccional.}
La red de Hopfield asocia cada patrón consigo mismo.
Kosko~\cite{kosko1988bidirectional} quiso asociar pares de patrones distintos y propuso
una memoria de dos capas unidas por una sola matriz de conexiones, en la que un patrón en
una capa evoca su par en la otra y la recuperación va y viene entre ambas hasta
estabilizarse.
Basta una pista de cualquiera de los dos lados para recuperar el otro.
Comparte la limitación que Pineda y colaboradores señalan en las memorias conexionistas:
no tiene una operación para rechazar lo que no guarda~\cite{pineda2021entropic}.
Es el antecedente más directo de la memoria de contenido de cada módulo desde la fase 3,
que recupera la imagen a partir de las palabras y las palabras a partir de la imagen.

\paragraph{Memorias asociativas densas.}
Para reconocer patrones con poco error, una red de Hopfield tendría que guardar muchos más
recuerdos que neuronas, y la red estándar solo funciona bien en el caso contrario.
Krotov y Hopfield~\cite{krotov2016dense} quitaron esa restricción agregando a la función
de energía interacciones de orden mayor que el cuadrático, con lo que la capacidad crece
de forma no lineal con el tamaño de la red.
También mostraron que estas memorias equivalen a una red neuronal de una capa oculta, con
funciones de activación como los polinomios rectificados.
En los dígitos manuscritos de MNIST, con 2000 memorias, todas las redes de potencia 3
quedaron por debajo del 1.6\,\% de error de prueba.
En esa prueba las memorias se aprenden por retropropagación para reducir el error de
clasificación, y lo que la red entrega es una etiqueta.
Representan la opción de ganar capacidad dentro de una sola memoria.
La de este trabajo es la contraria, repartir el contenido entre memorias que devuelven el
contenido mismo.

\paragraph{Memoria asociativa entrópica.}
Pineda, Fuentes y Morales~\cite{pineda2021entropic} partieron de un contraste.
Las memorias simbólicas de las computadoras son declarativas pero no asociativas, y las
conexionistas son asociativas y distribuidas pero no declarativas, no rechazan y
reproducen.
Buscaron un modelo con las cinco propiedades que atribuyen a la memoria natural, que es
asociativa, declarativa y distribuida, construye lo que recupera y rechaza directamente lo
que no contiene.
Lo construyeron con tablas de rasgos por valores, en las que reconocer es una prueba de
contención, recuperar construye un objeto nuevo y la entropía mide la indeterminación de
lo guardado.
Para los dígitos de MNIST usaron una tabla por dígito, y una unidad central de control
enviaba cada operación a las diez tablas y recogía su estado y su entropía.
Al llenar las tablas, la precisión del reconocimiento siguió alta mientras la memoria
aceptaba cada vez más de lo que sí contenía, y lo recuperado se parecía a la pista con
entropía baja o moderada.
El límite que reportan es un rango.
Si la entropía sube demasiado, por ejemplo al agregar ruido, la información se confunde y
la precisión cae.
En este reporte, el techo entrópico es el extremo alto de ese rango, y la unidad central
que consulta todas las tablas se cambia por módulos que aprenden a quién preguntar.

\paragraph{Memoria entrópica ponderada.}
En la formulación original cada celda de la tabla estaba encendida o apagada, y todo lo
guardado pesaba lo mismo.
Pineda y Morales~\cite{pineda2022weighted} agregaron un mecanismo de aprendizaje en el que
cada registro refuerza las celdas que usa, de modo que la tabla cuenta (W-EAM).
La aplicaron al aprendizaje fonético del español de México, con el corpus DIMEx100 y 22
tablas, una por fonema.
Para decidir qué tabla responde, el sistema pondera la fuerza de la pista con la entropía
de cada tabla que la acepta.
Con tablas de 16 filas, la decisión elegía entre 11 tablas que aceptaban la pista y
acertaba cerca del 80\,\% de las veces; la precisión y la exhaustividad (\textit{recall}) del sistema
pasaron de 0.8.
Frente a la red neuronal sola, la memoria bajó el error fonético rechazando segmentos mal
alineados.
Los autores usaron los mismos parámetros en las 22 tablas y dejan abierto si convendría
ajustarlos por fonema.
La W-EAM es la memoria sobre la que se construyen los módulos de este trabajo, y elegir
entre varias tablas que aceptan la misma pista es el problema que aquí resuelve el
directorio con lo que registró en interacciones anteriores.

\paragraph{Memoria heteroasociativa entrópica.}
Morales y Pineda~\cite{morales2025missing} extendieron la memoria entrópica al caso
heteroasociativo, con pares de objetos de dominios o modalidades distintos guardados en
una relación de cuatro dimensiones.
Al recuperar, la pista de un dominio selecciona en el otro un plano de memoria muy
indeterminado, y no queda pista con qué sacar de él un objeto.
Los autores llaman a esto el problema de la pista faltante y proponen tres métodos
incrementales para resolverlo: el aleatorio, muestrear y probar, y buscar y probar.
Lo evaluaron con dígitos manuscritos de MNIST asociados a letras de EMNIST, de modo que un
dígito recupera su letra y una letra su dígito, y concluyen que el modelo promete guardar,
reconocer y recuperar conjuntos muy grandes de objetos con pocos recursos de cómputo.
En esa evaluación los dos dominios son imágenes de caracteres manuscritos.
En este trabajo la EHAM es la memoria de contenido de cada módulo desde la fase 3, donde
asocia palabras con imágenes en ambos sentidos, y también forma sus directorios; para
elegir el objeto del plano se usa el tercer método.

\paragraph{Imágenes naturales.}
Los experimentos anteriores con la memoria entrópica usaban datos estructurados y
homogéneos, como dígitos y letras manuscritos, ropa y fonemas.
Hernández, Morales y Pineda~\cite{hernandez2026cifar} probaron la W-EAM con las imágenes
de animales y vehículos de CIFAR-10, más complejas, guardadas todas en una sola tabla sin
importar su clase.
Un autocodificador produce los rasgos y, como la tabla no clasifica, un clasificador
asigna la clase de cada objeto recuperado.
La memoria guardó, reconoció y recuperó esas imágenes, y formó cadenas de asociación en
las que cada recuerdo sirve de pista al siguiente, con objetos recordados, asociados a
otra clase o imaginados.
Su desempeño con estas imágenes quedó por debajo del clasificador, mientras que en los
trabajos anteriores los dos eran parecidos.
Corresponde al caso de una sola memoria con todas las clases, que aquí se compara con la
partición en módulos, y en él la clase final la pone un clasificador; el sistema de este
trabajo no usa clasificadores para enrutar ni para rechazar.

\paragraph{Qué falta.}
Ninguno de estos trabajos reparte el contenido entre memorias que aprendan a quién
preguntar.
Las memorias conexionistas enfrentan el límite de capacidad con una red más grande o
entrenada, y las entrópicas consultan todas sus tablas o guardan todo en una.
La teoría de Wegner tiene la organización que falta, pero no dice con qué memoria se
construye cada nodo ni cómo se forma su directorio.
Tampoco hay una medida de lo que agrega la memoria asociativa frente a decisores simples
que usan los mismos vectores, como un voto por palabras del vocabulario o el vecino más
cercano, y sin ella no se puede saber si un resultado se debe a la memoria o a la
representación que la alimenta.
```

### Capítulo 1, 1.2 Definición del problema (apertura)

**Antes:**

```latex
\section{Definición del problema}
\label{sec:definicion-problema}

Una memoria asociativa entrópica guarda lo que registra como una tabla de frecuencias,
y su entropía crece con lo que guarda.
Con entropía baja, el reconocimiento comete pocas aceptaciones falsas; con entropía alta
acepta de más y la recuperación se vuelve menos precisa
\cite{pineda2021entropic,morales2022manuscript}.
Una sola memoria con todo el contenido tiene, entonces, un techo: conforme se llena,
rechaza peor y recuerda con menos fidelidad.
La solución que se propone es la de la memoria transactiva, que reparte el contenido
entre especialistas, cada uno con menos variedad que guardar, y aprende con el uso a
quién preguntar.
El problema tiene cinco partes, en el orden en que se estudiaron.
\begin{enumerate}
    \item \textbf{Emergencia.} Que el directorio emerja del uso: sin saber de antemano
    quién sabe qué, los módulos tienen que aprender a quién preguntar registrando quién
    resolvió cada consulta, primero con un mediador y después punto a punto.
    
```

**Ahora:**

```latex
\section{Definición del problema}
\label{sec:definicion-problema}

Con entropía baja, el reconocimiento de una memoria asociativa entrópica comete pocas
aceptaciones falsas; con entropía alta acepta de más y la recuperación se vuelve menos
precisa \cite{pineda2021entropic,morales2022manuscript}.
Como la entropía crece con lo que se guarda, una sola memoria con todo el contenido tiene
un techo: conforme se llena, rechaza peor y recuerda con menos fidelidad.
La solución que se propone es la de la memoria transactiva, que reparte el contenido
entre especialistas, cada uno con menos variedad que guardar, y aprende de la experiencia
a quién preguntar.
El problema tiene cinco partes, en el orden en que se estudiaron.
\begin{enumerate}
    \item \textbf{Emergencia.} Que el directorio emerja de la experiencia: sin saber de antemano
    quién sabe qué, los módulos tienen que aprender a quién preguntar registrando quién
    resolvió cada consulta, primero con un mediador y después punto a punto.
    
```

### Capítulo 1, 1.3 Objetivo general (el arco pasa a la apertura)

**Antes:**

```latex
\section{Objetivo general}\label{secc:og}

Construir un sistema distribuido de memoria transactiva sobre memorias asociativas
entrópicas y estudiarlo por fases, desde un prototipo de tres módulos hasta ocho módulos
sobre ETH-80 con una memoria heteroasociativa cada uno, y medir, frente a una sola
memoria con las ocho clases, si el reparto evita el techo entrópico y, frente a decisores
simples sobre las mismas representaciones, qué agrega la memoria.
```

**Ahora:**

```latex
\section{Objetivo general}\label{secc:og}

La investigación siguió cinco fases, y cada una partió de lo que dejó la anterior.
La primera fue un prototipo de tres módulos (\texttt{apple}, \texttt{horse} y
\texttt{car}), con cuatro memorias por módulo, pistas de texto cuantizadas por signo y un
mediador, en el que se vio que el directorio emerge de la experiencia.
En ese prototipo, la lectura cruda del directorio favorecía al módulo con más registros,
y en la segunda fase se eligió leerlo dividiendo entre ellos (normalización B1).
La tercera pasó a las ocho clases de ETH-80, y al hacerlo cambiaron a la vez el
codificador, la cuantización, las memorias por módulo, el banco de consultas y el
mediador.
Por eso la comparación entre tres y ocho módulos no aísla el efecto de crecer, que se
mide con dos experimentos propios: una sola memoria contra la partición y una memoria de
dos clases contra una de ocho.
Con el sistema de ocho módulos, la cuarta fase estudió sus propiedades, entre ellas la
lectura inversa del directorio, la pérdida de un miembro y la evocación de palabras
desde imágenes.
La quinta conectó el sistema a la voz y a la cámara en tiempo real, como demostración
de integración.
Cada fase respondió una pregunta que dependía de la anterior, porque no se puede leer un
directorio que no se ha formado ni estudiar las propiedades de un sistema que todavía no
escala.
De ahí que haya un objetivo específico por fase, y que el objetivo general las reúna.

Construir un sistema distribuido de memoria transactiva sobre memorias asociativas
entrópicas y estudiarlo por fases, desde un prototipo de tres módulos hasta ocho módulos
sobre ETH-80 con una memoria heteroasociativa cada uno, y medir, frente a una sola
memoria con las ocho clases, si el reparto evita el techo entrópico y, frente a decisores
simples sobre las mismas representaciones, qué agrega la memoria.
```

