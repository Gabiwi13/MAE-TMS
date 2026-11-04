# Propuesta viejo/nuevo: encuadre del techo entrópico

**Estado:** aprobada y aplicada. Ninguna cifra es nueva: todas salen de la Sección de la EHAM única (`05_resultados.tex`, exp. 11 con el protocolo corregido) y de `07_conclusiones.tex`.

**Idea:** la pregunta no es construir el directorio, que es la solución propuesta, sino si repartir el contenido entre especialistas evita el techo entrópico de una sola memoria. Los datos lo sostienen en fidelidad del recuerdo, en mezcla de dominios y en que la memoria única rechaza peor cuanto más contiene, no en acierto de clase (hasta 200 imágenes por clase y ocho clases).

## E1. Definición del problema: el techo como problema y el reparto como solución

`.tex_uacj/Capitulo1.tex`

Viejo:

```latex
Para construir un sistema de memoria transactiva con memorias asociativas entrópicas
hay que resolver cuatro cosas.
```

Nuevo:

```latex
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
```

## E2. Definición del problema: qué hay que medir

`.tex_uacj/Capitulo1.tex`

Viejo:

```latex
Resolverlo no basta para saber qué aporta la memoria.
El problema incluye medir cuánto de cada resultado se debe al mecanismo asociativo y
cuánto a las representaciones:
```

Nuevo:

```latex
Resolverlo no basta.
Hay que medir, frente a una sola memoria con el mismo contenido, si el reparto evita el
techo, y cuánto de cada resultado se debe al mecanismo asociativo y cuánto a las
representaciones:
```

## E3. Pregunta de investigación

`.tex_uacj/Capitulo1.tex`

Viejo:

```latex
¿Puede un sistema de memoria transactiva construido sobre memorias heteroasociativas
entrópicas enrutar consultas de texto e imagen entre ocho especialistas, recuperar el
contenido asociado en ambas direcciones y rechazar lo que no conoce, sin clasificadores
discriminativos en esas decisiones? ¿Qué agrega la memoria frente a decisores simples
sobre las mismas representaciones, y cuánto dependen sus resultados de esas
representaciones?
```

Nuevo:

```latex
¿Evita un sistema de memoria transactiva, que reparte el contenido entre ocho memorias
heteroasociativas entrópicas especializadas y aprende con el uso a quién preguntar, el
techo entrópico de una sola memoria con todo el contenido? ¿Puede hacerlo enrutando
consultas de texto e imagen, recuperando el contenido asociado en ambas direcciones y
rechazando lo que no conoce, sin clasificadores discriminativos en esas decisiones? ¿Qué
agrega la memoria frente a decisores simples sobre las mismas representaciones, y cuánto
dependen sus resultados de esas representaciones?
```

## E4. Objetivo general

`.tex_uacj/Capitulo1.tex`

Viejo:

```latex
ninguna memoria contiene, y medir su desempeño frente a decisores simples sobre las
mismas representaciones y frente a una sola memoria con las ocho clases.
```

Nuevo:

```latex
ninguna memoria contiene, y medir, frente a una sola memoria con las ocho clases, si el
reparto evita el techo entrópico y, frente a decisores simples sobre las mismas
representaciones, qué agrega la memoria.
```

## E5. Introducción: la pregunta

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
Este trabajo pregunta si con ellas se puede construir un sistema de memoria transactiva,
y qué agrega la memoria frente a decisores simples que usan las mismas representaciones.
```

Nuevo:

```latex
Una sola de ellas con todo el contenido tiene un techo: su entropía crece con lo que
guarda, y con ella las aceptaciones falsas.
Este trabajo pregunta si repartir el contenido entre especialistas que saben quién sabe
qué evita ese techo, y qué agrega la memoria frente a decisores simples.
```

## E6. Introducción: el valor del trabajo

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
El valor del trabajo está en mostrar qué aporta una memoria asociativa a un sistema
distribuido (rechazo, recuperación en ambas direcciones y decisiones trazables a sus
registros) y qué no aporta (más acierto que un decisor simple).
```

Nuevo:

```latex
El valor del trabajo está en mostrar dónde evita el reparto el techo (fidelidad del
recuerdo y mezcla de dominios) y dónde no (acierto de clase), y qué aporta la memoria
frente a un decisor simple.
```

## E7. Resumen: apertura con el techo

`.tex_uacj/Resumen.tex`

Viejo:

```latex
Un grupo recuerda más que cada uno de sus miembros cuando cada uno sabe quién sabe qué;
Wegner~\cite{wegner1987transactive} llamó a esta organización \emph{memoria transactiva}.
Este trabajo construye EAM-TMS, un sistema distribuido de memoria transactiva sobre las
memorias asociativas entrópicas de Pineda y Morales
\cite{pineda2022weighted,morales2025missing}, con ocho módulos, uno por clase de
ETH-80~\cite{leibe2003eth80}.
```

Nuevo:

```latex
Una memoria asociativa entrópica con todo el contenido tiene un techo: conforme se
llena, su entropía crece, acepta de más y recuerda con menos fidelidad.
Este trabajo reparte el contenido entre especialistas que saben quién sabe qué, como en
la \emph{memoria transactiva} de Wegner~\cite{wegner1987transactive}, y construye EAM-TMS
sobre las memorias de Pineda y Morales \cite{pineda2022weighted,morales2025missing}, con
ocho módulos, uno por clase de ETH-80~\cite{leibe2003eth80}.
```

## E7b. Resumen: módulos en una oración más corta (para que quepa)

`.tex_uacj/Resumen.tex`

Viejo:

```latex
Cada módulo guarda palabras e imágenes de su clase en una sola memoria heteroasociativa
y lleva directorios que se forman con el uso; ninguna decisión de enrutamiento o rechazo
pasa por un clasificador discriminativo.
```

Nuevo:

```latex
Cada módulo guarda palabras e imágenes en una memoria heteroasociativa y directorios
formados con el uso, sin clasificadores discriminativos en sus decisiones.
```

## E7c. Resumen: dos líneas más de página (ya no lleva número de página)

`.tex_uacj/Resumen.tex`

Viejo:

```latex
\enlargethispage{3\baselineskip}
```

Nuevo:

```latex
\enlargethispage{5\baselineskip}
```

## E8. Resumen: resultado frente a la memoria única

`.tex_uacj/Resumen.tex`

Viejo:

```latex
Al enrutar texto, el sistema iguala a decisores simples sobre las mismas
representaciones (81.2 frente a 76.0--81.5\,\% en 80 consultas) y a una sola memoria con las ocho clases (96.8 frente a 96.9\,\% sobre 171
consultas reservadas).
```

Nuevo:

```latex
Frente a una sola memoria con las ocho clases acierta la clase lo mismo (96.8 frente a
96.9\,\% sobre 171 consultas reservadas), pero responde menos veces con un dominio ajeno
(3.1 frente a 10.9\,\% de las imágenes).
Al enrutar texto iguala a decisores simples sobre las mismas representaciones (81.2
frente a 76.0--81.5\,\% en 80 consultas).
```

## E9. Resumen: cierre

`.tex_uacj/Resumen.tex`

Viejo:

```latex
La memoria asociativa no acierta más que un decisor simple: aporta el rechazo, la
recuperación en ambas direcciones y un directorio que registra quién sabe qué.
```

Nuevo:

```latex
Repartir evita el techo en fidelidad y mezcla de dominios, no en acierto; la memoria
aporta el rechazo, el recuerdo en ambas direcciones y un registro de quién sabe qué.
```

## E10. Abstract: apertura con el techo

`.tex_uacj/Abstract.tex`

Viejo:

```latex
A group that works together can remember more than any of its members, because each
member knows who knows what; Wegner~\cite{wegner1987transactive} called this
organization \emph{transactive memory}.
This work builds EAM-TMS, a distributed transactive memory system on the entropic
associative memories of Pineda and Morales \cite{pineda2022weighted,morales2025missing},
with eight modules, one per ETH-80 class~\cite{leibe2003eth80}.
```

Nuevo:

```latex
An entropic associative memory holding all the content has a ceiling: as it fills, its
entropy grows, it accepts too much and it recalls less faithfully.
This work splits the content among specialists that know who knows what, as in Wegner's
\emph{transactive memory}~\cite{wegner1987transactive}, and builds EAM-TMS on the
memories of Pineda and Morales \cite{pineda2022weighted,morales2025missing}, with eight
modules, one per ETH-80 class~\cite{leibe2003eth80}.
```

## E10b. Abstract: módulos en una oración más corta

`.tex_uacj/Abstract.tex`

Viejo:

```latex
Each module stores the words and images of its class in a single heteroassociative
memory and keeps directories formed through use; no routing or rejection decision goes
through a discriminative classifier.
```

Nuevo:

```latex
Each module keeps words and images in a heteroassociative memory and directories formed
through use, with no discriminative classifier in its decisions.
```

## E10c. Abstract: dos líneas más de página (ya no lleva número de página)

`.tex_uacj/Abstract.tex`

Viejo:

```latex
\enlargethispage{3\baselineskip}
```

Nuevo:

```latex
\enlargethispage{5\baselineskip}
```

## E11. Abstract: resultado frente a la memoria única

`.tex_uacj/Abstract.tex`

Viejo:

```latex
When routing text, the system matches simple decision rules on the same
representations (81.2 against 76.0--81.5\,\% on 80 queries)
and a single memory holding the eight classes (96.8 against 96.9\,\% on 171 held-out
queries).
```

Nuevo:

```latex
Against a single memory holding the eight classes it is as accurate (96.8 against
96.9\,\% on 171 held-out queries), but answers with a foreign domain less often (3.1
against 10.9\,\% of the images).
When routing text it matches simple decision rules on the same representations (81.2
against 76.0--81.5\,\% on 80 queries).
```

## E11b. Abstract: cierre

`.tex_uacj/Abstract.tex`

Viejo:

```latex
The associative memory is not more accurate than a simple rule: what it adds is
rejection, retrieval in both directions and a directory that records who knows what.
```

Nuevo:

```latex
Splitting avoids the ceiling in recall fidelity and domain mixing, not in accuracy; the
memory adds rejection, two-way recall and a record of who knows what.
```

## E12. Conclusión del objetivo general: orden de las comparaciones

`.tex_uacj/ConclusionObjetivoGeneral.tex`

Viejo:

```latex
El sistema se construyó y se midió contra decisores simples, contra una sola memoria con
las ocho clases y contra un codificador sin la pérdida de clase.
```

Nuevo:

```latex
El sistema se construyó y se midió contra una sola memoria con las ocho clases, para ver
si el reparto evita el techo entrópico, contra decisores simples y contra un codificador
sin la pérdida de clase.
```

## E13. Conclusiones: respuesta a la pregunta

`.tex8/secciones/07_conclusiones.tex`

Viejo:

```latex
\paragraph{Respuesta a la pregunta de investigación.}
Sí, se puede.
```

Nuevo:

```latex
\paragraph{Respuesta a la pregunta de investigación.}
El reparto evita el techo de una sola memoria en lo que ese techo afecta, y no en el
acierto de clase.
Con el mismo contenido, la EHAM única acepta más consultas fuera de dominio cuanto más
contiene, responde con un dominio ajeno más veces y recuerda más lejos de una instancia
real de la clase, mientras que el acierto de clase es el mismo desde 50 imágenes por
clase (Sección~\ref{sec:eham-unica}); la ventaja del sistema en ese rechazo depende de
una compuerta decidida después de ver esas consultas (limitación (g)).
Hasta 200 imágenes por clase y con ocho clases, la memoria única no llega a un techo en el
acierto; dónde lo alcanza queda por medir.
El reparto, además, se puede hacer sin clasificadores.
```

## E14. Trabajo futuro: curva del techo (nuevo punto en la lista de recomendaciones)

```latex
\item Curva del techo entrópico: llenar la EHAM única con más clases y más
    contenido que en este trabajo, hasta encontrar dónde cae el acierto de clase, y
    comparar ahí con el reparto entre especialistas.
```
