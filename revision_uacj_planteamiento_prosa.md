La propuesta está lista. Las cuatro piezas van abajo con su destino, el LaTeX y la fuente de cada cifra. No toqué la tesis ni `.tex_uacj`, no hice commit ni push. El árbol de trabajo está limpio en `una-hetero` (`6197bc3`). No compilé el LaTeX porque este contenedor no tiene `xelatex` ni `pdflatex`.

**Sobre la plantilla:** las instrucciones originales entre corchetes ya no están en el repositorio. El generador las reemplazó, y `.tex_uacj` entró a la historia ya generado en `6197bc3`. Por eso deduje lo que pide cada sección a partir de los títulos y de los marcadores del generador; los supuestos que tomé están en la lista S2.

**Convenciones:** uso `\,\%`, como las propuestas del jurado. También uso «sin clasificadores discriminativos en las decisiones de enrutamiento y rechazo» y «la especialización es asignada», que vienen de `revision_jurado_estructura_prosa.md` y siguen pendientes de tu aprobación (S3).


---

## 1. Capítulo 1, Planteamiento del Problema

**Destino:** `.tex_uacj/Capitulo1.tex`. Reemplaza todo, desde `\section{Antecedentes}` hasta el final del archivo.
- El bloque «Contribuciones principales» sale de Antecedentes (S4).
- El bloque «Estructura del documento» pasa al paso 5 de la Introducción.

```latex
\chapter{Planteamiento del Problema}\label{cap:pp}

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
Una memoria entrópica opera sobre vectores cuantizados, así que necesita que alguien
le entregue las palabras y las imágenes como vectores.
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
El codificador se entrena con dos pérdidas: la reconstrucción y una entropía cruzada de
clase de peso 0.1 (Sección~\ref{sec:percepcion}).
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

\section{Definición del problema}
\label{sec:definicion-problema}

Para construir un sistema de memoria transactiva con memorias asociativas entrópicas
hay que resolver cuatro cosas.
La primera es cómo se reparte el contenido entre los especialistas y cómo se forma, con
el uso, el directorio que dice a quién preguntar.
La segunda es cómo pasa una consulta de texto o de imagen al especialista correcto,
primero con un mediador y después punto a punto.
La tercera es cómo se rechaza una consulta que ningún especialista contiene.
La cuarta es cómo se recupera, en ambos sentidos, lo que se asoció: la imagen a partir
de las palabras y las palabras a partir de la imagen.
Todo esto debe hacerse sin clasificadores discriminativos en las decisiones de
enrutamiento y rechazo.

Resolverlo no basta para saber qué aporta la memoria.
El problema incluye medir cuánto de cada resultado se debe al mecanismo asociativo y
cuánto a las representaciones: los vectores de palabras y su vocabulario, por un lado,
y el codificador visual y su supervisión de clase, por el otro.
La pregunta de investigación queda así:

\begin{quote}
¿Puede un sistema de memoria transactiva construido sobre memorias heteroasociativas
entrópicas enrutar consultas de texto e imagen entre ocho especialistas, recuperar el
contenido asociado en ambas direcciones y rechazar lo que no conoce, sin clasificadores
discriminativos en esas decisiones? ¿Qué agrega la memoria frente a decisores simples
sobre las mismas representaciones, y cuánto dependen sus resultados de esas
representaciones?
\end{quote}

\section{Objetivo general}\label{secc:og}

Construir un sistema distribuido de memoria transactiva de ocho módulos sobre memorias
heteroasociativas entrópicas, que enrute consultas de texto e imagen al módulo
especialista, recupere el contenido asociado en ambas direcciones y rechace lo que
ninguna memoria contiene, y medir su desempeño frente a decisores simples sobre las
mismas representaciones y frente a una sola memoria con las ocho clases.

\subsection{Objetivos específicos}

\begin{enumerate}
    \item \label{oe:arquitectura}
    Implementar la arquitectura: ocho módulos, uno por cada clase de ETH-80, cada uno con
    una memoria de contenido heteroasociativa entre palabras e imágenes y dos
    directorios, uno textual y uno visual; un mediador para la fase temprana y la
    coordinación punto a punto en la fase madura.
    Verificar que todas las decisiones salen de operaciones de las memorias y que una
    sola memoria de contenido por módulo basta para tomarlas.

    \item \label{oe:formacion}
    Medir el enrutamiento de texto en las fases temprana y madura sobre un conjunto de
    evaluación que no forma el directorio, en función del número de consultas de
    formación y de la lectura del directorio (cruda o normalizada por número de
    registros, B1).

    \item \label{oe:lineas-base}
    Comparar el enrutamiento de texto con decisores simples sobre los mismos vectores
    (voto por tokens del vocabulario, centroide, $k$ vecinos más cercanos y tabla de
    conteos) y con una sola memoria heteroasociativa para las ocho clases.

    \item \label{oe:rechazo}
    Medir el rechazo: cuántas de 40 consultas fuera de dominio acepta el sistema,
    frente a los decisores simples y a la memoria única, y qué pasa con entradas
    visuales sin estructura.

    \item \label{oe:recuperacion}
    Medir la recuperación en ambas direcciones: cuántas consultas de texto reciben una
    imagen y qué tan cerca queda de una imagen real de su clase, y cuántas imágenes
    evocan palabras de su dominio.

    \item \label{oe:vision}
    Medir el enrutamiento visual sobre las 656 imágenes de prueba y sobre objetos que
    ningún módulo vio, y cuantificar cuánto depende de la supervisión de clase del
    codificador.
\end{enumerate}

\section{Justificación}

Repartir consultas entre nodos especializados, sin que un coordinador central decida
cada una, es un problema de los sistemas distribuidos.
El modelo de Wegner propone una solución que viene de los grupos humanos: cada nodo
guarda lo suyo y aprende, con el uso, a quién mandar lo que no sabe.
Este trabajo construye esa solución con memorias cuyas operaciones están definidas
formalmente, y por eso cada decisión del sistema se puede rastrear hasta los conteos
que la produjeron.
Esa trazabilidad sirve para auditar el sistema y para explicar cada respuesta.

El rechazo importa por la misma razón.
Un sistema que responde a todo con alguna clase obliga a quien lo usa a adivinar cuándo
se equivocó.
Las memorias entrópicas contestan «no lo tengo» cuando una entrada no tiene soporte en
lo registrado, y este trabajo mide cuándo esa respuesta funciona y cuándo no.

La comparación con decisores simples tiene un valor práctico para la ingeniería.
Si un voto por palabras del vocabulario o un vecino más cercano aciertan lo mismo que la
memoria, la razón para usarla no es el acierto, sino lo que el voto o el vecino no
hacen: rechazar, recuperar el contenido asociado y dejar un registro de quién sabe qué.
Medirlo con los mismos vectores separa lo que aporta el mecanismo de lo que aporta la
representación, y orienta dónde conviene invertir: en la memoria o en el codificador.

Para la línea de trabajo de las memorias asociativas entrópicas, el sistema es una
aplicación nueva, con varios módulos que cooperan y una memoria heteroasociativa que
opera en ambas direcciones entre texto e imagen.

\section{Alcances y limitaciones}

\paragraph{Alcances.}
\begin{itemize}
    \item \textbf{Datos.} Las ocho clases de ETH-80, con 410 imágenes de $128\times128$
    píxeles por clase, divididas por archivo en 328 de entrenamiento y 82 de prueba
    (Sección~\ref{sec:dataset}).
    La generalización a objetos nuevos se mide aparte, reservando un objeto por clase
    (Sección~\ref{sec:objetos-nuevos}).
    \item \textbf{Texto.} Consultas en inglés: un banco de 411 consultas, unas 50 por
    clase, y 40 consultas fuera de dominio.
    El vocabulario de cada módulo sale de ConceptNet~5.7 y las palabras se representan
    con fastText.
    \item \textbf{Sistema.} Ocho módulos con una memoria de contenido heteroasociativa y
    dos directorios cada uno, un mediador en la fase temprana y coordinación punto a
    punto en la fase madura.
    La especialización es asignada: la etiqueta de clase decide qué módulo guarda cada
    imagen y cada palabra.
    Lo que se forma con el uso es el directorio.
    \item \textbf{Comparaciones.} Decisores simples sobre los mismos vectores, una sola
    memoria heteroasociativa con las ocho clases y un codificador entrenado sin la
    pérdida de clase.
    \item \textbf{Procesos de Wegner.} El sistema modela la actualización del directorio
    y la coordinación de la recuperación.
    La asignación de información la hace la etiqueta de clase.
\end{itemize}

\paragraph{Fuera del alcance.}
\begin{itemize}
    \item El aprendizaje después de formar el directorio y la reorganización del grupo
    cuando un módulo sale o entra.
    \item Imágenes de categorías ajenas a ETH-80.
    Sin ellas, el rechazo visual solo se mide con entradas sin estructura, como lienzos
    uniformes, ruido o desenfoques.
    \item Fotografías de otro origen, otros conjuntos de datos y consultas en otros
    idiomas.
    \item La varianza entre entrenamientos del codificador: cada condición usa un solo
    codificador.
\end{itemize}

\paragraph{Limitaciones.}
Las limitaciones medidas están en la Sección~\ref{sec:limitaciones}.
Las que más pesan en la lectura de los resultados son cuatro:
el codificador visual se entrenó con supervisión de clase (limitación (k));
la partición por imagen deja vistas de los mismos objetos en el llenado y en la prueba
(limitación (f));
el punto de control del codificador y el número de variantes se eligieron mirando el
conjunto de prueba (limitación (g));
y las consultas fuera de dominio que comparten palabras con el vocabulario de un
módulo pasan la compuerta textual (limitación (a)).
```

**Fuentes de las cifras de la pieza 1:**

| cifra | fuente |
|---|---|
| 10 objetos, 41 vistas, 410 imágenes de 128×128, 328/82 | `.tex8/secciones/04_metodologia.tex:17-23` |
| 656 imágenes de prueba | `04_metodologia.tex:48` |
| peso 0.1 de la entropía cruzada | `results/codificador_sin_clase/README.md` («MSE + 0.1·CE») |
| 411 consultas, unas 50 por clase | contribución 1 de `01_introduccion.tex`; `src/eval_bank.py` |
| 40 consultas fuera de dominio | `results/experimento11/README.md` |
| sin imágenes reales de otras categorías | `results/lineas_base/README.md`, «Lectura», Imagen |
| un codificador por condición | `results/codificador_sin_clase/README.md`, «Límites» |

---

## 2. Introducción de una cuartilla

**Destino:** `.tex_uacj/Introduccion.tex`. Reemplaza el marcador `[PENDIENTE: recortar a una cuartilla]` y los tres párrafos de 01 que lo siguen.

Son unas 400 palabras. Los cinco pasos que supuse son: contexto, problema, objetivo, cómo se abordó y organización del documento.

```latex
\chapter*{Introducción}\label{introduccion}\label{sec:introduccion}
\thispagestyle{empty}

Un grupo que trabaja junto el tiempo suficiente recuerda más que cualquiera de sus
miembros por separado, porque cada uno sabe quién sabe qué y a quién preguntar.
Wegner~\cite{wegner1987transactive} llamó \emph{memoria transactiva} a esta
organización, y más tarde la describió como un modelo de red de
computadoras~\cite{wegner1995computer}.
Desde los sistemas computacionales, la idea es la de una red de nodos especializados
que aprenden, con el uso, a enviarse las consultas sin un coordinador central.

Las memorias asociativas entrópicas de Pineda y Morales
\cite{pineda2021entropic,pineda2022weighted,morales2025missing} guardan lo que registran
como conteos de frecuencia, reconocen una entrada cuando sus rasgos tienen soporte en
esos conteos, recuperan muestreándolos y rechazan lo que no contienen.
Este trabajo pregunta si con ellas se puede construir un sistema de memoria
transactiva, y qué agrega la memoria cuando se la compara con decisores simples que usan
las mismas representaciones.

El objetivo es construir un sistema de ocho módulos especialistas que enrute consultas
de texto e imagen, recupere el contenido asociado en ambas direcciones y rechace lo que
no conoce, sin clasificadores discriminativos en esas decisiones, y medir su desempeño.

El sistema, EAM-TMS, tiene un módulo por cada clase del conjunto ETH-80
\cite{leibe2003eth80}.
Cada módulo guarda palabras e imágenes de su clase en una sola memoria
heteroasociativa y lleva dos directorios, uno textual y uno visual.
Las palabras entran como vectores fastText~\cite{bojanowski2017fasttext} y las imágenes
como códigos de un autocodificador ResNet18~\cite{he2016resnet}.
Un mediador reparte las consultas mientras los directorios se forman; después, los
módulos se las envían entre sí.
El sistema se evalúa con un banco de 411 consultas de texto, 40 consultas fuera de
dominio, 656 imágenes de prueba y objetos que ningún módulo vio.
Se compara con decisores simples sobre los mismos vectores, con una sola memoria para
las ocho clases y con un codificador entrenado sin la pérdida de clase.

El Capítulo~\ref{cap:pp} plantea el problema, los objetivos y los alcances.
El Capítulo~\ref{sec:marco_teorico} presenta las memorias asociativas entrópicas, su
extensión heteroasociativa y el modelo de Wegner.
El Capítulo~3 describe la arquitectura y la metodología experimental, el Capítulo~4
reporta y discute los resultados, y el Capítulo~\ref{conclusiones} responde a la
pregunta de investigación y al objetivo general, y propone el trabajo futuro.
```

Los capítulos 3 y 4 de `.tex_uacj` no tienen `\label` de capítulo, así que los nombro por su número.

---

## 3. Resumen, palabras clave y *abstract*

**Destinos:**
- **Resumen:** `.tex_uacj/Resumen.tex`. Reemplaza el texto que va desde `% <- resumen de main.tex` hasta `\textbf{Palabras clave}: [PENDIENTE]`.
- **Abstract:** archivo nuevo, `.tex_uacj/Abstract.tex`. En `tesis_uacj.tex` hay que descomentar `%\include{Abstract} [Opcional]`.

```latex
\chapter*{Resumen}
\markboth{chapter name}{Sinopsis}

Un grupo que trabaja junto puede recordar más que cada uno de sus miembros porque cada
miembro sabe quién sabe qué y a quién preguntar; Wegner~\cite{wegner1987transactive}
llamó a esta organización \emph{memoria transactiva}.
Este trabajo construye EAM-TMS, un sistema distribuido de memoria transactiva sobre las
memorias asociativas entrópicas de Pineda y Morales, en su variante ponderada y su
extensión heteroasociativa \cite{pineda2022weighted,morales2025missing}, y mide qué
agrega la memoria frente a decisores simples que usan las mismas representaciones.
El sistema tiene ocho módulos, uno por cada clase de ETH-80~\cite{leibe2003eth80}.
Cada módulo guarda palabras e imágenes de su clase en una sola memoria heteroasociativa
y lleva un directorio textual y uno visual, que se forman con el uso.
La especialización es asignada por la etiqueta de clase, y ninguna decisión de
enrutamiento o rechazo pasa por un clasificador discriminativo.
Al enrutar texto, el sistema iguala a los decisores simples: sobre 80 consultas acierta
el 81.25\,\%, contra 79.4\,\% del voto por tokens del vocabulario y 81.5\,\% de los
cinco vecinos más cercanos, y sobre 171 consultas reservadas, el 96.8\,\%, contra 96.9\,\% de
una sola memoria con las ocho clases.
Rechaza lo que no conoce: acepta 2 de 40 consultas fuera de dominio, contra las 40 que
aceptan los decisores de coseno y 8 de la memoria única; su compuerta textual coincide
con la pertenencia al vocabulario.
Recupera en ambas direcciones: responde con una imagen al 98.7\,\% de las consultas
reservadas, con una fidelidad de [PENDIENTE: exp11 d\_nn], y 113 de 116 imágenes
enrutadas evocan palabras de su dominio.
Con imágenes, enruta al especialista el 96.2\,\% de 656 vistas nuevas, con dos errores,
mientras que el centroide y los vecinos más cercanos sobre los mismos códigos aciertan
del 99.4 al 99.8\,\% sin rechazar ninguna.
Ese enrutamiento depende de la supervisión del codificador: sin la pérdida de clase, cae
al 70.4\,\% con 169 errores.
Con objetos que ningún módulo vio, la cobertura de punta a punta es de
[PENDIENTE: pliegues].
La memoria asociativa no acierta más que un decisor simple; aporta el rechazo, la
recuperación en ambas direcciones y un directorio que registra quién sabe qué.

\hfill

\textbf{Palabras clave}: memoria transactiva, memoria asociativa entrópica, memoria
heteroasociativa, sistemas distribuidos, enrutamiento de consultas, recuperación
multimodal.
```

```latex
\chapter*{Abstract}
\markboth{chapter name}{Abstract}

A group that works together can remember more than any of its members because each
member knows who knows what and whom to ask; Wegner~\cite{wegner1987transactive} called
this organization \emph{transactive memory}.
This work builds EAM-TMS, a distributed transactive memory system on the entropic
associative memories of Pineda and Morales, in their weighted variant and their
heteroassociative extension \cite{pineda2022weighted,morales2025missing}, and measures
what the memory adds over simple decision rules that use the same representations.
The system has eight modules, one per ETH-80 class~\cite{leibe2003eth80}.
Each module stores the words and images of its class in a single heteroassociative
memory and keeps a textual and a visual directory, both formed through use.
Specialization is assigned by the class label, and no routing or rejection decision
goes through a discriminative classifier.
When routing text, the system matches the simple rules: on 80 queries it is correct
81.25\,\% of the time, against 79.4\,\% for token voting over the vocabulary and
81.5\,\% for five nearest neighbours, and on 171 held-out queries it reaches 96.8\,\%, against 96.9\,\%
for a single memory holding the eight classes.
It rejects what it does not know: it accepts 2 of 40 out-of-domain queries, against all
40 for the cosine rules and 8 for the single memory; its textual gate coincides with
vocabulary membership.
It retrieves in both directions: it answers 98.7\,\% of the held-out queries with an
image, with a fidelity of [PENDING: exp11 d\_nn], and 113 of 116 routed images evoke
words from their domain.
With images, it routes 96.2\,\% of 656 new views to the right specialist, with two
errors, while the centroid and nearest-neighbour rules on the same codes are correct
99.4 to 99.8\,\% of the time and reject none.
That routing depends on the encoder's supervision: without the class loss it drops to
70.4\,\%, with 169 errors.
On objects no module has seen, end-to-end coverage is [PENDING: folds].
The associative memory is not more accurate than a simple rule; what it adds is
rejection, retrieval in both directions and a directory that records who knows what.

\hfill

\textbf{Keywords}: transactive memory, entropic associative memory, heteroassociative
memory, distributed systems, query routing, multimodal retrieval.
```

**Fuentes de las cifras de la pieza 3:**

| cifra | fuente |
|---|---|
| 81.25; voto 79.4; 5-NN media 81.5 (80 consultas) | `results/lineas_base/README.md`, tabla de texto, columna proto80 |
| 96.8 frente a 96.9 (171 consultas, N = 200) | `results/experimento11_protocolo_corregido/README.md`, «Resultados del solo ruteo» |
| 2 de 40 con la doble compuerta; memoria única 20 % = 8 de 40 con N = 200 | ídem, «Fuera de dominio» |
| los decisores de coseno aceptan 40 de 40 | `lineas_base/README.md`, columna «ood40 acepta» |
| la compuerta coincide con la pertenencia al vocabulario | `lineas_base/README.md`, «Análisis posterior», punto 1 |
| 98.7 % responde | `experimento11_protocolo_corregido/README.md`, cobertura del protocolo corregido |
| 113 de 116 | `results/hemisferio_visual/README.md:3` |
| 631 de 656 (96.2 %), 2 falsos; 652–655 de los decisores simples, 0 rechazos | `lineas_base/README.md`, tabla de imagen |
| 70.4 %, 169 falsos | `results/codificador_sin_clase/README.md` |

---

## 4. Capítulo 5, «Con respecto al objetivo general»

**Destino:** `.tex_uacj/Capitulo5.tex`. Reemplaza `[PENDIENTE: 07 no tiene este material; …]`.

```latex
El objetivo general (Sección~\ref{secc:og}) se cumplió.
El sistema se construyó y se midió contra decisores simples, contra una sola memoria con
las ocho clases y contra un codificador sin la pérdida de clase.
Lo que dejaron esas comparaciones se resume por objetivo específico.

\paragraph{Arquitectura (objetivo~\ref{oe:arquitectura}).}
El sistema tiene ocho módulos, cada uno con una memoria de contenido heteroasociativa
y dos directorios, y un mediador que deja de intervenir en la fase madura.
Registrar, reconocer, recuperar y enrutar son operaciones de las memorias
(Sección~\ref{sec:operaciones}).
Una sola memoria de contenido por módulo basta: los pesos de cada dominio se leen de la
memoria heteroasociativa, y con ellos el sistema toma las mismas decisiones que con
memorias homoasociativas separadas (Sección~\ref{sec:una-memoria}).

\paragraph{Formación del directorio (objetivo~\ref{oe:formacion}).}
Sobre conjuntos de 120 consultas que nunca forman el directorio, la fase madura con la
lectura B1 sube del 78.9\,\% con 50 consultas de formación al 91.0\,\% con 291, y la
temprana es del 89.7\,\% (promedio de cinco sorteos del conjunto de evaluación).
Con unas 200 consultas, la fase madura alcanza a la temprana: la diferencia es de
$+0.2$ puntos con 200 y de $+1.3$ con 291, y ninguna diferencia positiva se sostiene
entre sorteos.
El directorio reproduce, entonces, la decisión del mediador sin difundir la consulta a
todos los módulos, con el mismo acierto.
La lectura B1 supera a la cruda con todos los tamaños de formación y en todos los
sorteos, por 4.5 a 8.8 puntos en promedio; sin ella, la fase madura nunca alcanza a la
temprana.

\paragraph{Frente a decisores simples y a una memoria única
(objetivo~\ref{oe:lineas-base}).}
En texto, el sistema acierta lo mismo que los decisores simples.
Sobre las 80 consultas más difíciles del banco, en las que solo 11 traen el nombre de
su clase, acierta el 81.25\,\%, y el voto por tokens del vocabulario, el centroide y los
vecinos más cercanos dan entre 76.0 y 81.5\,\%.
Sobre las 171 consultas reservadas, con 200 imágenes por clase, enruta bien el
96.8\,\% y la memoria única clasifica bien el 96.9\,\% (diferencia de $-0.1$ puntos,
$p = 0.86$).
Lo que la memoria agrega sobre el voto en texto es el desempate entre las clases que
contienen algún token de la consulta: 2.9 puntos sobre las 400 consultas de
calibración (90.0 frente a 87.1\,\%).
Una tabla de conteos de tokens formada con las mismas consultas no se distingue del
directorio (92.3 frente a 93.0\,\%, $p = 0.58$).

\paragraph{Rechazo (objetivo~\ref{oe:rechazo}).}
De las 40 consultas fuera de dominio, el sistema acepta 2 con 25, 50, 100 y 200 imágenes
por clase.
La memoria única acepta 5.0, 5.0, 12.5 y 20.0\,\% con esos mismos tamaños, y los
decisores de coseno aceptan las 40.
La compuerta textual coincide con la pertenencia al vocabulario en los 3064 pares de
token y clase examinados, de modo que un voto léxico rechaza las mismas consultas.
Las dos que pasan son las únicas que comparten una palabra con el vocabulario de un
módulo (limitación (a)).
En imagen, el umbral de energía y la contención rechazan buena parte de las entradas sin
estructura (limitación (c)).
El rechazo de imágenes reales de otras categorías no se midió.

\paragraph{Recuperación en ambas direcciones (objetivo~\ref{oe:recuperacion}).}
De texto a imagen, el sistema responde con una imagen al 98.7\,\% de las 171 consultas
reservadas, y la memoria única al 100\,\%.
La distancia de la imagen recordada a la imagen real más cercana de su clase es
[PENDIENTE: exp11 d\_nn].
De imagen a texto, 113 de las 116 imágenes enrutadas entre las 15 primeras de cada clase
evocan palabras de su dominio (97.4\,\%).

\paragraph{Imágenes y codificador (objetivo~\ref{oe:vision}).}
Los directorios visuales envían al especialista el 96.2\,\% de las 656 imágenes de
prueba (631), rechazan 23 y se equivocan en dos.
El centroide y los vecinos más cercanos sobre los mismos códigos aciertan de 652 a 655
sin rechazar ninguna, y el vecino más cercano acierta las 23 que el sistema rechaza.
Con un codificador entrenado sin la pérdida de clase, el enrutamiento cae al 70.4\,\%,
los errores suben de 2 a 169 y la cobertura de punta a punta con objetos nuevos baja del
89.2 al 59.3\,\%.
La separación entre clases la hace el codificador supervisado, y la propiedad de
fallar con un rechazo en lugar de un error depende de esa supervisión.
Con objetos que ningún módulo vio, la cobertura es del 89.2\,\% frente al 95.5\,\% con
vistas nuevas de objetos conocidos, pero el codificador sí había visto esos objetos;
con un codificador reentrenado sin el objeto reservado, la cobertura es de
[PENDIENTE: pliegues].

\paragraph{En suma.}
El sistema enruta como un decisor simple y, además, rechaza lo que no contiene,
recupera en ambas direcciones y guarda un registro de quién sabe qué.
Su acierto lo ponen las representaciones: el vocabulario en texto y el codificador
supervisado en imagen.
```

**Fuentes de las cifras de la pieza 4:**

| cifra | fuente |
|---|---|
| 120 consultas fijas; 78.9 → 91.0; temprana 89.7; +0.2 y +1.3; B1 > A por 4.5 a 8.8 | `results/calibracion_evaluacion_fija/README.md`, «Los 5 sorteos de E juntos» y «Lectura» |
| mismas decisiones con los pesos de la hetero | `results/homo_marginal/README.md:40` |
| 11 de 80 traen el nombre; decisores entre 76.0 y 81.5 | `lineas_base/README.md`, tablas de composición y de texto |
| 96.8 / 96.9, −0.1, p = 0.86 | `experimento11_protocolo_corregido/README.md` |
| desempate +2.9; tabla de conteos 92.3 frente a 93.0, p = 0.58 | `lineas_base/README.md`, «Análisis posterior», punto 2; McNemar cal400 |
| 2 de 40 en los cuatro cortes; memoria única 5.0/5.0/12.5/20.0; 3064 pares | `experimento11_protocolo_corregido/README.md`; `lineas_base/README.md` |
| 98.7 % de respuesta frente a 100 % de la memoria única | `experimento11_protocolo_corregido/README.md`; `results/experimento11/README.md` |
| 631, 23 rechazos, 2 falsos; 652–655; el 1-NN acierta las 23 | `lineas_base/README.md`, «Imagen: 656 imágenes de prueba» |
| 70.4 %, 2 → 169, 89.2 → 59.3 | `results/codificador_sin_clase/README.md` |
| 89.2 frente a 95.5 | `results/experimento16/README.md:7-8` |

---

## Marcadores

| marcador | dónde | qué lo llena |
|---|---|---|
| `[PENDIENTE: exp11 d\_nn]` / `[PENDING: exp11 d\_nn]` | Resumen, *abstract*, Cap. 5 (recuperación) | la corrida completa del exp11 con los directorios reiniciados y con recuerdo: d_nn del protocolo frente a la memoria única |
| `[PENDIENTE: pliegues]` / `[PENDING: folds]` | Resumen, *abstract*, Cap. 5 (imágenes) | exp16 con el codificador reentrenado en los 10 pliegues: cobertura de punta a punta con objeto nuevo y falsos ruteos |
| «limitación (k)» | Cap. 1, Limitaciones | la limitación (k) de `revision_jurado_estructura_prosa.md` 3.3, que no existe en 06 hasta que se aplique. Sus marcadores se llenan con 70.4 % y 59.3 % de `results/codificador_sin_clase` |

## Supuestos que debes confirmar

1. **S1. Dónde vive el texto.** `generar_capitulos.py` reescribe `Capitulo1.tex`, `Introduccion.tex`, `Resumen.tex` y `Capitulo5.tex` desde cero, así que lo que se pegue a mano se perdería al regenerar. Hay dos opciones: que el generador incluya estas piezas desde archivos propios (por ejemplo, `.tex_uacj/propios/`), o que deje de escribir esos cuatro archivos. Nada de esta propuesta va a `.tex8`.
2. **S2. Las instrucciones de la plantilla.** Supuse que la Introducción pide cinco pasos: contexto, problema, objetivo, cómo se abordó y organización del documento. También supuse que el Resumen pide problema, método, resultados y conclusión en una página. Si la plantilla original dice otra cosa, se ajustan.
3. **S3. Términos de la propuesta de estructura.** Las frases «sin clasificadores discriminativos…», «la especialización es asignada» y «el sistema modela dos de los tres procesos de Wegner» dependen de que apruebes `revision_jurado_estructura_prosa.md`.
4. **S4. Contribuciones.** Antecedentes ya no lleva el bloque de contribuciones de 01. Tienes que decidir dónde van las contribuciones nuevas de la otra sesión dentro de la plantilla.
5. **S5. Coherencia con la otra sesión.** El Resumen y el capítulo 5 deben coincidir con el resumen y las conclusiones que reescribe la otra sesión.
6. **S6. Qué cifras representan al texto.** Usé las 80 consultas difíciles y las 171 reservadas. Dejé fuera el 93.0 de las 400 consultas, porque esa cifra se mide sobre las mismas consultas que formaron el directorio.
7. **S7. «8 de 40» de la memoria única.** Lo convertí del 20.0 % con N = 200. Con N = 25 y 50, la memoria única acepta 2 de 40, igual que el sistema.
8. **S8. «98.7 %».** Sale de la compuerta del recuerdo en el solo ruteo, verificada fila a fila contra la respuesta oficial. Dice que hay respuesta, no qué tan buena es la imagen.
9. **S9. Pliegues: 2 o 3.** El README de los pliegues describe dos, pero `resumen.json`, `por_pliegue.csv` y `raw/` ya traen el pliegue 3, y el commit dice «3 de 10». No usé ninguna cifra de los pliegues.
10. **S10. Entradas degeneradas sin cifra.** La limitación (c) de 06 dice que el umbral cierra el 90 % de la fuga (137 de 152). `results/experimento14/veredicto.md` da 83 % y 94 %, con otros denominadores. Por eso remití a (c) sin cifra. Conviene revisar esa cifra en 06.
11. **S11. Rechazo visual con imágenes reales de otras categorías.** Lo puse como fuera de alcance porque no se midió. Si quieres, se puede agregar como limitación (l).
12. **S12. Justificación sin citas.** Las afirmaciones sobre trazabilidad y sobre el valor del rechazo son argumentos sin fuente. No agregué ninguna llave nueva a `referencias.bib`.
13. **S13. Lo que dejan fuera los objetivos.** No incluí objetivos sobre costo computacional, ι y κ, ni capacidad. Si los quieres, se agrega un séptimo objetivo.
