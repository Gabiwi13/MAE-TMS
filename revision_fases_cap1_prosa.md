# Revisión por fases: Capítulo 1 y partes preliminares (`cap1`)

Base: `59cca47` (rama `una-hetero`). Archivos tocados: `.tex_uacj/Capitulo1.tex`, `.tex_uacj/Resumen.tex`, `.tex_uacj/Abstract.tex` y `.tex_uacj/Introduccion.tex`. `python .tex_uacj/generar_capitulos.py` termina sin error («líneas de .tex8 que no aparecen en la salida: 0»). No hay `xelatex` en el contenedor, así que la página única se controla con el conteo de caracteres.

## 1. Largo de las partes preliminares

Caracteres Unicode del archivo completo (incluye encabezado y palabras clave, que no cambian).

| archivo | antes | después | diferencia |
|---|---|---|---|
| `Resumen.tex` | 1893 | 1881 | -12 |
| `Abstract.tex` | 1870 | 1795 | -75 |
| `Introduccion.tex` | 1959 | 1947 | -12 |

`Capitulo1.tex` (sin límite de página): 12807 → 18585 caracteres.

Las tres partes preliminares conservan el mismo número de `\cite` (tres grupos en el Resumen y el Abstract, cuatro en la Introducción, como antes), y ninguna usa `\enlargethispage`.

## 2. Correspondencia de etiquetas de objetivos (vieja → nueva)

| vieja | nueva | qué pasó |
|---|---|---|
| `oe:arquitectura` | `oe:escalado` | la arquitectura de ocho módulos y la memoria única por módulo pasan al objetivo de escalado (fase 3) |
| `oe:formacion` | `oe:emergencia` y `oe:lectura` | la formación del directorio pasa a la fase 1 (tres módulos); la lectura cruda contra B1, a la fase 2; la formación con ocho módulos sobre el conjunto fijo queda en `oe:escalado` |
| `oe:lineas-base` | `oe:escalado` | comparación con decisores simples y con la memoria única |
| `oe:rechazo` | `oe:escalado` | rechazo de las 40 consultas fuera de dominio |
| `oe:recuperacion` | `oe:escalado` | recuperación en ambas direcciones |
| `oe:vision` | `oe:escalado` | enrutamiento visual, objetos nuevos y codificador sin clase |
| — | `oe:hallazgos` | nuevo (fase 4) |
| — | `oe:mundo-real` | nuevo (fase 5) |

Numeración: `oe:emergencia` = 1, `oe:lectura` = 2, `oe:escalado` = 3, `oe:hallazgos` = 4, `oe:mundo-real` = 5.

Las seis etiquetas viejas se eliminan de `Capitulo1.tex`. Hoy las cita `ConclusionObjetivoGeneral.tex` (líneas 7, 19, 34, 48, 61 y 69); quedarán como referencias sin definir hasta que la sesión de Conclusiones aplique esta tabla.

Etiquetas nuevas además de las de objetivos: `fase:preguntas` (sección «Preguntas de investigación») y `fase:pi-emergencia`, `fase:pi-lectura`, `fase:pi-escalado`, `fase:pi-hallazgos` y `fase:pi-mundo-real` (una pregunta por objetivo). Se conservan `cap:pp`, `sec:definicion-problema`, `secc:og`, `introduccion` y `sec:introduccion`.

## 3. Fuente de cada cifra nueva o que se conserva

| cifra | dónde va | arquitectura | fuente |
|---|---|---|---|
| 26.25 % de acierto maduro tras 1 interacción | Resumen, Abstract | fase 1 (tres módulos, cuatro memorias, signo, TME, banco de 80) | `results/fase1_tres_modulos/exp4_directory_formation/results_formation.csv:2` |
| 98.75 % tras 80 interacciones, dentro de muestra | Resumen, Abstract | fase 1 | `results/fase1_tres_modulos/exp4_directory_formation/results_formation.csv:81`; `report.md:12` |
| 33.75 % con el orden bloqueado por clase | Resumen, Abstract | fase 1 | `results/fase1_tres_modulos/exp4_directory_formation/results_formation.csv:501-503` |
| banco de 80 consultas (27/27/26) | Capítulo 1 (OE1, alcances) | fase 1 | `results/fase1_tres_modulos/experimento1/informe.md:10` |
| 53.75 % con la lectura cruda (98.75 % con B1) | Resumen, Abstract | fase 1 y 2 (mismo prototipo), N = 80 | `results/fase1_tres_modulos/ablation_mdir_bias/ablation_report.md:27,31` |
| 96.8 % del sistema contra 96.9 % de la memoria única (clase, N = 200) | Resumen, Abstract | fase 3, sistema final | `results/experimento11_protocolo_corregido/README.md:177` (versión corregida del protocolo, como pide la errata del índice) |
| 3.1 % contra 10.9 % de imágenes con dominio ajeno | Resumen, Abstract | fase 3, sistema final | `results/experimento11_protocolo_corregido/README.md:267,274` |
| 81.2 % del sistema contra 76.0–81.5 % de los decisores simples en texto (proto80) | Resumen, Abstract | fase 3, sistema final | `results/lineas_base/README.md:125,127,130,197` |
| 2 de 40 consultas fuera de dominio aceptadas (igual que el voto), contra 40 de los decisores de coseno | Resumen, Abstract | fase 3, sistema final | `results/lineas_base/README.md:119-130` (última columna), `:159` |
| el directorio leído al revés devuelve la envolvente del dominio presenciado y no un ejemplar (sin cifra en el Resumen) | Resumen, Abstract | fase 4; protocolo anterior (todos los módulos registran todo), el mecanismo no depende de eso | `results/experimento8/README.md:16-18,43` |
| la palabra evocada desde una imagen es del vocabulario de su clase en el 96.0 % y es el nombre de la clase en el 48.0 % (top-1) | Resumen, Abstract | fase 4, sistema final | `results/experimento17/parte_a_resumen.txt:1,3,6,8` (339 lecturas reconocidas de 116 imágenes enrutadas) |
| voz y cámara en tiempo real, sin cifras de acierto | Resumen, Abstract, Introducción, Capítulo 1 | fase 5, versión v5 (tres memorias de contenido por módulo) | `results/mundo_real/README.md:9-13` |
| Whisper traduce al inglés lo dicho en español o en inglés | Capítulo 1 (alcances) | fase 5, v5 | `results/mundo_real/realtime_lab_README.md:36,55` |
| cuadro real ajeno a ETH-80 | Capítulo 1 (alcances) | fase 5, v5 | `results/mundo_real/selftest_frame.png` (un cuadro, sin protocolo) |
| 410 imágenes por clase, 328/82, 411 consultas, 40 fuera de dominio, peso 0.1 de la pérdida de clase | Capítulo 1 | sistema final | sin cambio respecto de la base; vienen de las Secciones `sec:dataset` y `sec:percepcion` |

Cifras que quité del Resumen y del Abstract por espacio, todas con fuente vigente y que siguen en el Capítulo 4: 98.7 % de consultas con imagen, distancias 27.2 contra 32.5, 113 de 116 imágenes que evocan su dominio, 96.2 % de 656 vistas, 70.4 % sin la pérdida de clase, 89.2 % y 87.6 % con objetos nuevos y 136 de 3280 falsos.

## 4. Lo que no pude sostener o dejé fuera

- **exp9 (pérdida de un miembro)** no entra en el Resumen: usa el protocolo anterior y la salvedad no cabía en una página. El Capítulo 1 lo nombra como tema de la fase 4 sin cifras.
- **exp10 (directorios perspectivales)** tampoco entra en el Resumen, por la misma razón (protocolo anterior, directorio visual sin variantes).
- **Formación con ocho módulos (81.2 %, no llega al 90 %)** no entra en el Resumen; queda como parte de OE3.
- **Latencias de la fase 5 (336 + 302 ms, 54 ms por cuadro)** no entran en las preliminares: son de una sola medición de julio, sin salida cruda.
- La pregunta de investigación única de la base se convirtió en una pregunta general (en prosa, al inicio de la nueva sección) más cinco preguntas, una por objetivo.

## 5. Citas que harían falta y no están en el `.bib`

- Whisper (Radford et al., 2023, «Robust Speech Recognition via Large-Scale Weak Supervision»): se nombra en OE5 sin `\cite`.
- Nelson y Narens (metamemoria): OE4 habla de «metamemoria» sin cita; la cita le toca a la sesión de Discusiones.

## 6. Revisión de patrones

- Se quitó el «no es X, sino Y» de la Justificación («la razón para usarla no es el acierto, sino…» → «la razón para usarla está en lo que el voto o el vecino no hacen»).
- Se quitó el cierre «Repartir evita el techo …, no en acierto» y quedó «…; en acierto de clase empata».
- Las cinco partes del problema van en una lista con rótulo, en lugar de «La primera… La segunda…».
- Sin «agente», sin la marca prohibida, porcentajes con `\,\%`, términos definidos sin cambio (módulo, directorio, fase temprana y madura, B1, EHAM, TME).

## 7. Texto viejo y nuevo

### `Resumen.tex`

**Viejo (59cca47):**

```latex
\chapter*{Resumen}
\markboth{Resumen}{Resumen}
\thispagestyle{empty}
Una memoria asociativa entrópica tiene un techo: conforme se llena, su entropía crece,
acepta de más y recuerda peor.
Este trabajo reparte el contenido entre especialistas que saben quién sabe qué, como en
la \emph{memoria transactiva} de Wegner~\cite{wegner1987transactive}, y construye EAM-TMS
sobre las memorias de Pineda y Morales \cite{pineda2022weighted,morales2025missing}:
ocho módulos, uno por clase de ETH-80~\cite{leibe2003eth80}, cada uno con una memoria
heteroasociativa de palabras e imágenes y directorios formados con el uso, sin
clasificadores discriminativos.
Frente a una sola memoria con las ocho clases acierta lo mismo (96.8 frente a
96.9\,\% en 171 consultas), pero responde menos veces con un dominio ajeno
(3.1 frente a 10.9\,\% de las imágenes).
En texto iguala a decisores simples sobre las mismas representaciones (81.2 frente a
76.0--81.5\,\%).
Rechaza lo que no conoce: acepta 2 de 40 consultas fuera de dominio, como un voto por
vocabulario, contra 40 de los decisores de coseno; con imágenes de otras categorías no
se midió.
Recupera en ambas direcciones: responde con una imagen al 98.7\,\% de las consultas, más
cerca de una instancia real que la memoria única (27.2 contra 32.5), y 113
de 116 imágenes evocan su dominio.
Con imágenes enruta bien el 96.2\,\% de 656 vistas nuevas (un centroide acierta más), y
solo porque el codificador se entrenó con la clase: sin ella, 70.4\,\%.
Con objetos que ningún módulo vio cubre el 89.2\,\%, y el 87.6\,\% si el codificador
tampoco los vio, con 136 falsos enrutamientos de 3280, no 2.
Repartir evita el techo en fidelidad y mezcla de dominios, no en acierto.


\noindent\textbf{Palabras clave}: memoria transactiva, memoria asociativa entrópica, memoria
heteroasociativa, sistemas distribuidos, enrutamiento de consultas, recuperación
multimodal.
```

**Nuevo:**

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
bloqueado por clase, 33.75\,\%.
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

### `Abstract.tex`

**Viejo (59cca47):**

```latex
\chapter*{Abstract}
\markboth{Abstract}{Abstract}
\thispagestyle{empty}
An entropic associative memory has a ceiling: as it fills, its entropy grows, it accepts
too much and recalls worse.
This work splits the content among specialists that know who knows what, as in Wegner's
\emph{transactive memory}~\cite{wegner1987transactive}, and builds EAM-TMS on the
memories of Pineda and Morales \cite{pineda2022weighted,morales2025missing}: eight
modules, one per ETH-80 class~\cite{leibe2003eth80}, each with a heteroassociative memory
of words and images and directories formed through use, with no discriminative
classifier.
Against a single memory holding the eight classes it is as accurate (96.8 against
96.9\,\% on 171 queries), but answers with a foreign domain less often (3.1
against 10.9\,\% of the images).
On text it matches simple decision rules on the same representations (81.2 against
76.0--81.5\,\%).
It rejects what it does not know: it accepts 2 of 40 out-of-domain queries, like a
vocabulary vote, against all 40 for the cosine rules; real images from other
categories were not tested.
It retrieves in both directions: it answers 98.7\,\% of the queries with an image, closer
to a real instance of its class than the single memory (27.2 against 32.5), and 113 of
116 images evoke their domain.
With images it routes 96.2\,\% of 656 new views correctly (a centroid is more accurate),
only because the encoder was trained with the class: without it, 70.4\,\%.
On objects no module has seen, coverage is 89.2\,\%, and 87.6\,\% when the encoder has not
seen them either, with 136 false routings of 3280, not 2.
Splitting avoids the ceiling in recall fidelity and domain mixing, not in accuracy.


\noindent\textbf{Keywords}: transactive memory, entropic associative memory, heteroassociative
memory, distributed systems, query routing, multimodal retrieval.
```

**Nuevo:**

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
after one interaction and 98.75\,\% after 80, in-sample, and with class-blocked order,
33.75\,\%.
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

### `Introduccion.tex`

**Viejo (59cca47):**

```latex
\chapter*{Introducción}\label{introduccion}\label{sec:introduccion}
\thispagestyle{empty}
\markboth{Introducción}{Introducción}
Un grupo puede recordar más que cualquiera de sus miembros porque cada uno sabe quién
sabe qué.
Wegner~\cite{wegner1987transactive} llamó \emph{memoria transactiva} a esta organización
y después la describió como una red de computadoras~\cite{wegner1995computer}: nodos
especializados que aprenden, con el uso, a enviarse las consultas.
Las memorias asociativas entrópicas de Pineda y Morales
\cite{pineda2021entropic,pineda2022weighted,morales2025missing} guardan lo que registran
como conteos, reconocen una entrada cuando sus rasgos tienen soporte, recuperan
muestreando y rechazan lo que no contienen.
Hasta donde sabemos, no se han usado para repartir el conocimiento entre especialistas.
Una sola de ellas tiene un techo: su entropía crece con lo que
guarda, y con ella las aceptaciones falsas.
Este trabajo pregunta si repartir el contenido entre especialistas que saben quién sabe
qué evita ese techo, y qué agrega la memoria frente a decisores simples.

El producto es EAM-TMS: ocho módulos, uno por clase de ETH-80~\cite{leibe2003eth80}, cada
uno con una memoria heteroasociativa de palabras e imágenes y directorios formados con el
uso, que enrutan consultas de texto e imagen, recuperan en ambas direcciones y rechazan
lo que no conocen sin clasificadores discriminativos.
Se evalúa con 411 consultas de texto, 40 fuera de dominio, 656 imágenes de prueba y
objetos nuevos, frente a una sola memoria con las ocho clases, decisores
simples y un codificador sin la pérdida de clase.
El valor del trabajo está en mostrar dónde evita el reparto el techo (fidelidad del
recuerdo y mezcla de dominios) y dónde no (acierto de clase).
Los Capítulos~\ref{cap:pp} a~\ref{conclusiones} presentan el problema, el marco teórico,
el desarrollo, los resultados y las conclusiones, y el Apéndice~\ref{apendiceA} ubica los
experimentos.
```

**Nuevo:**

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

### `Capitulo1.tex`

**Viejo (59cca47):**

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

Una memoria asociativa entrópica guarda lo que registra como una tabla de frecuencias,
y su entropía crece con lo que guarda.
Con entropía baja, el reconocimiento comete pocas aceptaciones falsas; con entropía alta
acepta de más y la recuperación se vuelve menos precisa
\cite{pineda2021entropic,morales2022manuscript}.
Una sola memoria con todo el contenido tiene, entonces, un techo: conforme se llena,
rechaza peor y recuerda con menos fidelidad.
La solución que se propone es la de la memoria transactiva: repartir el contenido entre
especialistas, cada uno con menos variedad que guardar, y aprender con el uso a quién
preguntar.
Para que ese reparto funcione hay que resolver cuatro cosas.
La primera es cómo se reparte el contenido entre los especialistas y cómo se forma, con
el uso, el directorio que dice a quién preguntar.
La segunda es cómo pasa una consulta de texto o de imagen al especialista correcto,
primero con un mediador y después punto a punto.
La tercera es cómo se rechaza una consulta que ningún especialista contiene.
La cuarta es cómo se recupera, en ambos sentidos, lo que se asoció: la imagen a partir
de las palabras y las palabras a partir de la imagen.
Todo esto debe hacerse sin clasificadores discriminativos en las decisiones de
enrutamiento y rechazo.

Resolverlo no basta.
Hay que medir, frente a una sola memoria con el mismo contenido, si el reparto evita el
techo, y cuánto de cada resultado se debe al mecanismo asociativo y cuánto a las
representaciones: los vectores de palabras y su vocabulario, por un lado,
y el codificador visual y su supervisión de clase, por el otro.
La pregunta de investigación queda así:

\begin{quote}
¿Evita un sistema de memoria transactiva, que reparte el contenido entre ocho memorias
heteroasociativas entrópicas especializadas y aprende con el uso a quién preguntar, el
techo entrópico de una sola memoria con todo el contenido? ¿Puede hacerlo enrutando
consultas de texto e imagen, recuperando el contenido asociado en ambas direcciones y
rechazando lo que no conoce, sin clasificadores discriminativos en esas decisiones? ¿Qué
agrega la memoria frente a decisores simples sobre las mismas representaciones, y cuánto
dependen sus resultados de esas representaciones?
\end{quote}

\section{Objetivo general}\label{secc:og}

Construir un sistema distribuido de memoria transactiva de ocho módulos sobre memorias
heteroasociativas entrópicas, que enrute consultas de texto e imagen al módulo
especialista, recupere el contenido asociado en ambas direcciones y rechace lo que
ninguna memoria contiene, y medir, frente a una sola memoria con las ocho clases, si el
reparto evita el techo entrópico y, frente a decisores simples sobre las mismas
representaciones, qué agrega la memoria.

\subsection{Objetivos específicos}

\begin{enumerate}
    \item \label{oe:arquitectura}
    Implementar la arquitectura: ocho módulos, uno por cada clase de ETH-80, cada uno con
    una memoria de contenido heteroasociativa entre palabras e imágenes y dos
    directorios, uno textual y uno visual; un mediador para la fase temprana y la
    coordinación punto a punto en la fase madura.
    Identificar qué decisiones salen de operaciones de las memorias y cuáles de
    componentes externos, y verificar que una sola memoria de contenido por módulo basta
    para tomarlas.

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
el punto de control del codificador y el número de variantes se eligieron con el
conjunto de prueba (limitación (g));
y las consultas fuera de dominio que comparten palabras con el vocabulario de un
módulo pasan la compuerta textual (limitación (a)).
```

**Nuevo:**

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

\section{Definición del problema}
\label{sec:definicion-problema}

Una memoria asociativa entrópica guarda lo que registra como una tabla de frecuencias,
y su entropía crece con lo que guarda.
Con entropía baja, el reconocimiento comete pocas aceptaciones falsas; con entropía alta
acepta de más y la recuperación se vuelve menos precisa
\cite{pineda2021entropic,morales2022manuscript}.
Una sola memoria con todo el contenido tiene, entonces, un techo: conforme se llena,
rechaza peor y recuerda con menos fidelidad.
La solución que se propone es la de la memoria transactiva: repartir el contenido entre
especialistas, cada uno con menos variedad que guardar, y aprender con el uso a quién
preguntar.
El problema tiene cinco partes, en el orden en que se estudiaron.
\begin{enumerate}
    \item \textbf{Emergencia.} Que el directorio emerja del uso: sin saber de antemano
    quién sabe qué, los módulos tienen que aprender a quién preguntar registrando quién
    resolvió cada consulta, primero con un mediador y después punto a punto.
    \item \textbf{Lectura.} Cómo leer el directorio, porque un módulo con más registros
    acumula más soporte y una lectura cruda lo favorece aunque no sea el especialista.
    \item \textbf{Escalado.} Que el mecanismo funcione con ocho módulos: enrutar consultas
    de texto e imagen, rechazar lo que ningún módulo contiene y recuperar en ambos
    sentidos lo asociado (la imagen a partir de las palabras y las palabras a partir de la
    imagen), sin clasificadores discriminativos en las decisiones de enrutamiento y
    rechazo.
    \item \textbf{Propiedades.} Qué hace el sistema escalado más allá de enrutar, y cómo
    se lee eso desde el modelo de Wegner y desde lo que se sabe de la memoria humana.
    \item \textbf{Mundo real.} Si el sistema puede recibir entradas que no vienen del
    conjunto de datos, como la voz y las imágenes de una cámara.
\end{enumerate}

Resolver estas partes no basta.
Hay que medir, frente a una sola memoria con el mismo contenido, si el reparto evita el
techo, y cuánto de cada resultado se debe al mecanismo asociativo y cuánto a las
representaciones: los vectores de palabras y su vocabulario, por un lado,
y el codificador visual y su supervisión de clase, por el otro.
Las preguntas de investigación (Sección~\ref{fase:preguntas}) siguen las cinco partes.

\section{Objetivo general}\label{secc:og}

Construir un sistema distribuido de memoria transactiva sobre memorias asociativas
entrópicas y estudiarlo por fases, desde un prototipo de tres módulos hasta ocho módulos
sobre ETH-80 con una memoria heteroasociativa cada uno, y medir, frente a una sola
memoria con las ocho clases, si el reparto evita el techo entrópico y, frente a decisores
simples sobre las mismas representaciones, qué agrega la memoria.

\subsection{Objetivos específicos}

\begin{enumerate}
    \item \label{oe:emergencia}
    \textbf{Emergencia (fase 1).}
    Comprobar que el directorio emerge de la experiencia, con un prototipo de tres módulos
    (\texttt{apple}, \texttt{horse} y \texttt{car}; cuatro memorias por módulo, pistas
    cuantizadas por signo, TME mediador y un banco de 80 consultas): medir el enrutamiento
    de la fase madura en función del número de interacciones y del orden en que llegan.

    \item \label{oe:lectura}
    \textbf{Lectura del directorio (fase 2).}
    Determinar cómo leer el directorio comparando, en el prototipo de tres módulos, la
    lectura cruda con lecturas normalizadas por el número de registros, elegir una (B1) y
    comprobar con ocho módulos, sobre un conjunto de evaluación que no forma el
    directorio, si la elección se sostiene.

    \item \label{oe:escalado}
    \textbf{Escalado (fase 3).}
    Comprobar que el sistema funciona con ocho módulos, uno por clase de ETH-80, cada uno
    con una memoria de contenido heteroasociativa entre palabras e imágenes y dos
    directorios, uno textual y uno visual: medir la formación del directorio, el
    enrutamiento de texto e imagen, el rechazo, la recuperación en ambas direcciones y el
    enrutamiento de objetos que ningún módulo vio; compararlo con una sola memoria con las
    ocho clases y con decisores simples sobre los mismos vectores; y cuantificar cuánto
    depende el enrutamiento visual de la supervisión de clase del codificador.

    \item \label{oe:hallazgos}
    \textbf{Hallazgos (fase 4).}
    Caracterizar las propiedades del sistema de ocho módulos (el directorio como
    metamemoria, la perspectiva de cada módulo y la pérdida de un miembro, la envolvente
    con que reconoce y recuerda, el tamaño y la partición, la relación entre imagen y
    palabra, y sus límites) y leerlas desde el modelo de Wegner, la psicología y la
    neurociencia de la memoria.

    \item \label{oe:mundo-real}
    \textbf{Mundo real (fase 5).}
    Integrar al sistema la voz, transcrita con Whisper, y la cámara en tiempo real, como
    demostración de integración: registrar las latencias de la cadena y qué pasa con
    entradas ajenas a ETH-80, sin evaluar el acierto.
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
memoria, la razón para usarla está en lo que el voto o el vecino no hacen: rechazar,
recuperar el contenido asociado y dejar un registro de quién sabe qué.
Medirlo con los mismos vectores separa lo que aporta el mecanismo de lo que aporta la
representación, y orienta dónde conviene invertir: en la memoria o en el codificador.

Contar la investigación por fases deja ver de dónde salió cada decisión del sistema
final.
La lectura B1, por ejemplo, se eligió con tres módulos y se volvió a medir con ocho.
La demostración con voz y cámara muestra qué piezas hay que agregar para que las
consultas lleguen de un micrófono o de una cámara, y dónde falla el sistema cuando la
imagen no viene de ETH-80.

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
    El prototipo de la fase 1 usa tres de esas clases.
    \item \textbf{Texto.} Consultas en inglés: un banco de 411 consultas, unas 50 por
    clase, y 40 consultas fuera de dominio.
    El prototipo de tres módulos usa un banco propio de 80 consultas.
    El vocabulario de cada módulo sale de ConceptNet~5.7 y las palabras se representan
    con fastText.
    \item \textbf{Sistema.} En las fases 3 y 4, ocho módulos con una memoria de contenido
    heteroasociativa y dos directorios cada uno, un mediador en la fase temprana y
    coordinación punto a punto en la fase madura.
    En las fases 1 y 2, el prototipo de tres módulos descrito en el objetivo
    específico~\ref{oe:emergencia}.
    La especialización es asignada: la etiqueta de clase decide qué módulo guarda cada
    imagen y cada palabra.
    Lo que se forma con el uso es el directorio.
    \item \textbf{Comparaciones.} Decisores simples sobre los mismos vectores, una sola
    memoria heteroasociativa con las ocho clases, una memoria de dos clases contra una de
    ocho y un codificador entrenado sin la pérdida de clase.
    \item \textbf{Procesos de Wegner.} El sistema modela la actualización del directorio
    y la coordinación de la recuperación.
    La asignación de información la hace la etiqueta de clase.
    \item \textbf{Demostración en tiempo real.} La fase 5 usa la versión del sistema de
    julio de 2026, con tres memorias de contenido por módulo.
    Toca como demostración lo que la evaluación excluye: Whisper traduce al inglés frases
    dichas en español o en inglés, y la cámara entrega cuadros reales, entre ellos uno
    ajeno a ETH-80.
    Sus latencias son mediciones únicas, sin salida cruda guardada.
\end{itemize}

\paragraph{Fuera del alcance.}
\begin{itemize}
    \item El aprendizaje después de formar el directorio y la reorganización del grupo
    cuando un módulo sale o entra.
    La pérdida de un módulo se estudia como lesión, sin que el grupo vuelva a formar su
    directorio.
    \item Una comparación que cambie solo el número de módulos.
    Entre el prototipo de tres módulos y el sistema de ocho cambiaron varias cosas a la
    vez, el prototipo no se puede volver a correr con el código del sistema final y los
    pesos de su codificador no se guardaron.
    \item En la evaluación, las imágenes de categorías ajenas a ETH-80, las fotografías de
    otro origen y las consultas en otros idiomas.
    Sin ellas, el rechazo visual solo se mide con entradas sin estructura, como lienzos
    uniformes, ruido o desenfoques; la fase 5 las toca solo como demostración, sin conteo
    de aciertos.
    \item Otros conjuntos de datos.
    Las aplicaciones médica e industrial siguen en curso y solo se mencionan entre la
    difusión y los productos derivados, al final del Capítulo~\ref{conclusiones}.
    \item La varianza entre entrenamientos del codificador: cada condición usa un solo
    codificador.
\end{itemize}

\paragraph{Limitaciones.}
Las limitaciones medidas están en la Sección~\ref{sec:limitaciones}.
Las que más pesan en la lectura de los resultados del sistema de ocho módulos son cuatro:
el codificador visual se entrenó con supervisión de clase (limitación (k));
la partición por imagen deja vistas de los mismos objetos en el llenado y en la prueba
(limitación (f));
el punto de control del codificador y el número de variantes se eligieron con el
conjunto de prueba (limitación (g));
y las consultas fuera de dominio que comparten palabras con el vocabulario de un
módulo pasan la compuerta textual (limitación (a)).
A estas se suman las que vienen de comparar fases.
La formación del directorio con tres módulos se midió dentro de muestra, sobre las mismas
80 consultas que lo forman, y sus cifras no se comparan como experimento controlado con
las del sistema de ocho módulos.
La fase 5 no tiene tasa de error de transcripción ni aciertos con voz o con cámara.

\section{Preguntas de investigación}\label{fase:preguntas}

La pregunta general es si un sistema de memoria transactiva, que reparte el contenido
entre memorias heteroasociativas entrópicas especializadas y aprende con el uso a quién
preguntar, evita el techo entrópico de una sola memoria con todo el contenido, y qué
agrega esa memoria frente a decisores simples sobre las mismas representaciones.
Cada objetivo específico tiene su pregunta.

\begin{enumerate}
    \item \label{fase:pi-emergencia}
    ¿Emerge el directorio de la experiencia en un prototipo de tres módulos, y cuántas
    interacciones y qué orden de llegada necesita la fase madura para enrutar las
    consultas sin el mediador? (Objetivo~\ref{oe:emergencia}.)
    \item \label{fase:pi-lectura}
    ¿Qué lectura del directorio corrige la ventaja del módulo con más registros, y se
    sostiene esa lectura al pasar de tres a ocho módulos?
    (Objetivo~\ref{oe:lectura}.)
    \item \label{fase:pi-escalado}
    Con ocho módulos, ¿enruta el sistema consultas de texto e imagen, rechaza lo que no
    conoce y recupera en ambas direcciones sin clasificadores discriminativos en esas
    decisiones? ¿En qué evita el reparto el techo de una sola memoria con las ocho clases,
    qué agrega la memoria frente a decisores simples y cuánto dependen sus resultados de
    las representaciones? (Objetivo~\ref{oe:escalado}.)
    \item \label{fase:pi-hallazgos}
    ¿Qué propiedades muestra el sistema de ocho módulos en el directorio, en la
    perspectiva de cada módulo, en la relación entre reconocer y recordar, en el efecto
    del tamaño, en la relación entre imagen y palabra y en sus límites, y qué
    correspondencia tienen con la memoria transactiva y con la memoria humana?
    (Objetivo~\ref{oe:hallazgos}.)
    \item \label{fase:pi-mundo-real}
    ¿Puede el sistema recibir consultas por voz e imágenes de una cámara en tiempo real,
    con qué latencias, y qué hace con entradas que no vienen de ETH-80?
    (Objetivo~\ref{oe:mundo-real}.)
\end{enumerate}
```

