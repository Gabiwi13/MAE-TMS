# Propuesta viejo/nuevo: ajuste a la plantilla UACJ 2024_1

**Estado:** aprobada y aplicada. Ninguna cifra cambia.

**Motivo:** la auditoría contra la plantilla (Downloads, 2024_1) encontró dos desvíos. (1) Capitulo3.tex:6 y :13 de la plantilla piden que las fases de la metodología sean secciones 3.3 en adelante; el reporte las tenía como 3.2.1–3.2.8. (2) Resumen.tex:6 pide «no más de una página» e Introduccion.tex:4 «una cuartilla»; el reporte las hacía caber con `\enlargethispage`, invadiendo el margen inferior. Se quita la ampliación y se recorta el texto.

## P1. Capítulo 3: las fases de la metodología como secciones 3.3 en adelante

`.tex_uacj/generar_capitulos.py`

Viejo:

```latex
"% <- 04\n" + apertura04 + resto04))
```

Nuevo:

```latex
"% <- 04\n" + apertura04 + mover_niveles(resto04, -1)))
```

## P2. Resumen: sin agrandar la página

`.tex_uacj/Resumen.tex`

Viejo:

```latex
\enlargethispage{5\baselineskip}
```

Nuevo:

```latex
(se borra la línea)
```

## P3. Resumen: módulos dentro de la oración de EAM-TMS

`.tex_uacj/Resumen.tex`

Viejo:

```latex
sobre las memorias de Pineda y Morales \cite{pineda2022weighted,morales2025missing}, con
ocho módulos, uno por clase de ETH-80~\cite{leibe2003eth80}.
Cada módulo guarda palabras e imágenes en una memoria heteroasociativa y directorios
formados con el uso, sin clasificadores discriminativos en sus decisiones.
```

Nuevo:

```latex
sobre las memorias de Pineda y Morales \cite{pineda2022weighted,morales2025missing}:
ocho módulos, uno por clase de ETH-80~\cite{leibe2003eth80}, cada uno con una memoria
heteroasociativa de palabras e imágenes y directorios formados con el uso, sin
clasificadores discriminativos.
```

## P4. Resumen: memoria única

`.tex_uacj/Resumen.tex`

Viejo:

```latex
96.9\,\% sobre 171 consultas reservadas), pero
```

Nuevo:

```latex
96.9\,\% en 171 consultas), pero
```

## P5. Resumen: rechazo

`.tex_uacj/Resumen.tex`

Viejo:

```latex
Rechaza lo que no conoce: acepta 2 de 40 consultas fuera de dominio, igual que un voto
por vocabulario y frente a las 40 de los decisores de coseno; con imágenes reales de
otras categorías no se midió.
```

Nuevo:

```latex
Rechaza lo que no conoce: acepta 2 de 40 consultas fuera de dominio, como un voto por
vocabulario, contra 40 de los decisores de coseno; con imágenes de otras categorías no
se midió.
```

## P6. Resumen: recuperación

`.tex_uacj/Resumen.tex`

Viejo:

```latex
más
cerca de una instancia real de su clase que la memoria única
```

Nuevo:

```latex
más
cerca de una instancia real que la memoria única
```

## P7. Resumen: imágenes

`.tex_uacj/Resumen.tex`

Viejo:

```latex
Con imágenes enruta bien el 96.2\,\% de 656 vistas nuevas, mientras que un centroide sobre
los mismos códigos acierta más, sin rechazar ninguna; ese enrutamiento depende de que el
codificador se entrenó con la clase, y sin ella cae al 70.4\,\%.
```

Nuevo:

```latex
Con imágenes enruta bien el 96.2\,\% de 656 vistas nuevas (un centroide acierta más), y
solo porque el codificador se entrenó con la clase: sin ella, 70.4\,\%.
```

## P7b. Resumen: texto

`.tex_uacj/Resumen.tex`

Viejo:

```latex
Al enrutar texto iguala a decisores simples sobre las mismas representaciones (81.2
frente a 76.0--81.5\,\% en 80 consultas).
```

Nuevo:

```latex
En texto iguala a decisores simples sobre las mismas representaciones (81.2 frente a
76.0--81.5\,\%).
```

## P7c. Resumen: espacio antes de las palabras clave

`.tex_uacj/Resumen.tex`

Viejo:

```latex
\smallskip
\noindent\textbf{Palabras clave}
```

Nuevo:

```latex
\noindent\textbf{Palabras clave}
```

## P8. Resumen: objetos nuevos

`.tex_uacj/Resumen.tex`

Viejo:

```latex
Con objetos que ningún módulo vio, la cobertura es del 89.2\,\%, y del 87.6\,\% si el
codificador tampoco los vio,
```

Nuevo:

```latex
Con objetos que ningún módulo vio cubre el 89.2\,\%, y el 87.6\,\% si el codificador
tampoco los vio,
```

## P9. Resumen: cierre

`.tex_uacj/Resumen.tex`

Viejo:

```latex
Repartir evita el techo en fidelidad y mezcla de dominios, no en acierto; la memoria
aporta el rechazo, el recuerdo en ambas direcciones y un registro de quién sabe qué.
```

Nuevo:

```latex
Repartir evita el techo en fidelidad y mezcla de dominios, no en acierto.
```

## P9b. Resumen: primera oración

`.tex_uacj/Resumen.tex`

Viejo:

```latex
Una memoria asociativa entrópica con todo el contenido tiene un techo: conforme se
llena, su entropía crece, acepta de más y recuerda con menos fidelidad.
```

Nuevo:

```latex
Una memoria asociativa entrópica tiene un techo: conforme se llena, su entropía crece,
acepta de más y recuerda peor.
```

## P9c. Resumen: acierto frente a la memoria única

`.tex_uacj/Resumen.tex`

Viejo:

```latex
Frente a una sola memoria con las ocho clases acierta la clase lo mismo
```

Nuevo:

```latex
Frente a una sola memoria con las ocho clases acierta lo mismo
```

## P9d. Resumen: evocación

`.tex_uacj/Resumen.tex`

Viejo:

```latex
y 113
de 116 imágenes evocan palabras de su dominio.
```

Nuevo:

```latex
y 113
de 116 imágenes evocan su dominio.
```

## P9e. Resumen: falsos con objetos nuevos

`.tex_uacj/Resumen.tex`

Viejo:

```latex
pero con 136 falsos enrutamientos de 3280 en lugar de 2.
```

Nuevo:

```latex
con 136 falsos enrutamientos de 3280, no 2.
```

## P10. Abstract: sin agrandar la página

`.tex_uacj/Abstract.tex`

Viejo:

```latex
\enlargethispage{5\baselineskip}
```

Nuevo:

```latex
(se borra la línea)
```

## P11. Abstract: módulos dentro de la oración de EAM-TMS

`.tex_uacj/Abstract.tex`

Viejo:

```latex
memories of Pineda and Morales \cite{pineda2022weighted,morales2025missing}, with eight
modules, one per ETH-80 class~\cite{leibe2003eth80}.
Each module keeps words and images in a heteroassociative memory and directories formed
through use, with no discriminative classifier in its decisions.
```

Nuevo:

```latex
memories of Pineda and Morales \cite{pineda2022weighted,morales2025missing}: eight
modules, one per ETH-80 class~\cite{leibe2003eth80}, each with a heteroassociative memory
of words and images and directories formed through use, with no discriminative
classifier.
```

## P12. Abstract: memoria única

`.tex_uacj/Abstract.tex`

Viejo:

```latex
96.9\,\% on 171 held-out queries), but
```

Nuevo:

```latex
96.9\,\% on 171 queries), but
```

## P13. Abstract: imágenes

`.tex_uacj/Abstract.tex`

Viejo:

```latex
With images it routes 96.2\,\% of 656 new views correctly, while a centroid on the same
codes is more accurate and rejects none; that routing depends on the encoder having been
trained with the class, and without it drops to 70.4\,\%.
```

Nuevo:

```latex
With images it routes 96.2\,\% of 656 new views correctly (a centroid is more accurate),
only because the encoder was trained with the class: without it, 70.4\,\%.
```

## P13b. Abstract: texto

`.tex_uacj/Abstract.tex`

Viejo:

```latex
When routing text it matches simple decision rules on the same representations (81.2
against 76.0--81.5\,\% on 80 queries).
```

Nuevo:

```latex
On text it matches simple decision rules on the same representations (81.2 against
76.0--81.5\,\%).
```

## P13c. Abstract: espacio antes de las palabras clave

`.tex_uacj/Abstract.tex`

Viejo:

```latex
\smallskip
\noindent\textbf{Keywords}
```

Nuevo:

```latex
\noindent\textbf{Keywords}
```

## P14. Abstract: cierre

`.tex_uacj/Abstract.tex`

Viejo:

```latex
Splitting avoids the ceiling in recall fidelity and domain mixing, not in accuracy; the
memory adds rejection, two-way recall and a record of who knows what.
```

Nuevo:

```latex
Splitting avoids the ceiling in recall fidelity and domain mixing, not in accuracy.
```

## P14b. Abstract: primera oración

`.tex_uacj/Abstract.tex`

Viejo:

```latex
An entropic associative memory holding all the content has a ceiling: as it fills, its
entropy grows, it accepts too much and it recalls less faithfully.
```

Nuevo:

```latex
An entropic associative memory has a ceiling: as it fills, its entropy grows, it accepts
too much and recalls worse.
```

## P14c. Abstract: rechazo

`.tex_uacj/Abstract.tex`

Viejo:

```latex
rejection of real images from
other categories was not measured.
```

Nuevo:

```latex
real images from other
categories were not tested.
```

## P14d. Abstract: evocación

`.tex_uacj/Abstract.tex`

Viejo:

```latex
116 images evoke words from their domain.
```

Nuevo:

```latex
116 images evoke their domain.
```

## P14e. Abstract: falsos con objetos nuevos

`.tex_uacj/Abstract.tex`

Viejo:

```latex
but with 136 false routings of 3280 instead of 2.
```

Nuevo:

```latex
with 136 false routings of 3280, not 2.
```

## P15. Introducción: sin agrandar la página

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
\enlargethispage{5\baselineskip}
```

Nuevo:

```latex
(se borra la línea)
```

## P16. Introducción: primera oración

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
Un grupo que trabaja junto puede recordar más que cualquiera de sus miembros por
separado, porque cada uno sabe quién sabe qué y a quién preguntar.
```

Nuevo:

```latex
Un grupo puede recordar más que cualquiera de sus miembros porque cada uno sabe quién
sabe qué.
```

## P16b. Introducción: un solo párrafo de antecedentes y novedad más corta

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
especializados que aprenden, con el uso, a enviarse las consultas.

Las memorias asociativas entrópicas de Pineda y Morales
```

Nuevo:

```latex
especializados que aprenden, con el uso, a enviarse las consultas.
Las memorias asociativas entrópicas de Pineda y Morales
```

## P16c. Introducción: novedad

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
Hasta donde sabemos, en su línea de trabajo no se han usado para repartir el
conocimiento entre varios especialistas.
```

Nuevo:

```latex
Hasta donde sabemos, no se han usado para repartir el conocimiento entre especialistas.
```

## P17. Introducción: el producto

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
El producto es EAM-TMS: ocho módulos, uno por clase de ETH-80~\cite{leibe2003eth80}, que
guardan palabras e imágenes en una sola memoria heteroasociativa, se envían consultas de
texto e imagen mediante directorios formados con el uso, recuperan en ambas direcciones y
rechazan lo que no conocen, sin clasificadores discriminativos en esas decisiones.
Se evalúa con 411 consultas de texto, 40 fuera de dominio, 656 imágenes de prueba y
objetos que ningún módulo vio, y se compara con decisores simples, con una sola memoria
para las ocho clases y con un codificador entrenado sin la pérdida de clase.
```

Nuevo:

```latex
El producto es EAM-TMS: ocho módulos, uno por clase de ETH-80~\cite{leibe2003eth80}, cada
uno con una memoria heteroasociativa de palabras e imágenes y directorios formados con el
uso, que enrutan consultas de texto e imagen, recuperan en ambas direcciones y rechazan
lo que no conocen sin clasificadores discriminativos.
Se evalúa con 411 consultas de texto, 40 fuera de dominio, 656 imágenes de prueba y
objetos que ningún módulo vio, frente a una sola memoria con las ocho clases, decisores
simples y un codificador sin la pérdida de clase.
```

## P18. Introducción: organización

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
El Capítulo~\ref{cap:pp} plantea el problema y los objetivos; los
Capítulos~\ref{sec:marco_teorico} a~\ref{conclusiones} presentan el marco teórico, el
desarrollo, los resultados y las conclusiones, y el Apéndice~\ref{apendiceA} ubica cada
experimento citado.
```

Nuevo:

```latex
Los Capítulos~\ref{cap:pp} a~\ref{conclusiones} presentan el problema, el marco teórico,
el desarrollo, los resultados y las conclusiones, y el Apéndice~\ref{apendiceA} ubica los
experimentos.
```

## P18b. Introducción: el techo

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
Una sola de ellas con todo el contenido tiene un techo:
```

Nuevo:

```latex
Una sola de ellas tiene un techo:
```

## P18c. Introducción: objetos nuevos

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
656 imágenes de prueba y
objetos que ningún módulo vio, frente
```

Nuevo:

```latex
656 imágenes de prueba y
objetos nuevos, frente
```

## P18d. Introducción: valor del trabajo

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
y dónde no (acierto de clase), y qué aporta la memoria
frente a un decisor simple.
```

Nuevo:

```latex
y dónde no (acierto de clase).
```

## P18e. Introducción: el valor del trabajo sigue al párrafo del producto

`.tex_uacj/Introduccion.tex`

Viejo:

```latex
un codificador sin la pérdida de clase.

El valor del trabajo
```

Nuevo:

```latex
un codificador sin la pérdida de clase.
El valor del trabajo
```
