# Revisión contextual de patrones de redacción

**Estado: aprobada y aplicada.** Los problemas de contenido del final siguen sin tocar.

Base: `0e3a89e` (rama `una-hetero`). Alcance: `.tex8/secciones/02` a `07` (capítulos 2 a 5), `Capitulo1.tex`, `Introduccion.tex`, `Resumen.tex`, `Abstract.tex`, `ConclusionObjetivoGeneral.tex` y `ApendiceA.tex`. Se leyó todo dos veces: primero estructura y argumento, después patrones (plan de `texaudit`, secciones 7 y 8).

Reglas que se respetaron: ninguna cifra cambia, se agrega ni se quita, y tampoco cambian las referencias ni las citas (se comprobó por archivo comparando el multiconjunto de números, `\ref`, `\eqref` y `\cite` antes y después). Ningún término definido cambia. Resumen, Abstract e Introducción no se tocaron. Los capítulos 2 a 5 se editaron en `.tex8/secciones/` y se regeneraron con `python .tex_uacj/generar_capitulos.py`, que terminó sin error (0 líneas perdidas).

## Conteos antes y después

Método: script propio sobre `0e3a89e` y sobre el árbol modificado. Se quitan comentarios, matemáticas en línea, entornos `tabular`, `table`, `figure`, `equation`, `align` y `tikzpicture` (o sea, las leyendas de tablas y figuras no cuentan), y las órdenes `\ref`, `\cite` y `\label`. La oración se corta después de `.`, `!`, `?`, `:` o `;` seguidos de una mayúscula, y en cada `\item` y cada título. Una oración cuenta si tiene al menos tres palabras. «así» se cuenta como palabra, en cualquier posición; en este texto todas sus apariciones son «así que», salvo «queda así» (Cap. 1) y «un almacén así», «aun así» y «es así» (Discusión). Un comienzo cuenta si las dos primeras palabras de la oración coinciden, sin importar mayúsculas. El denominador es el número de oraciones del capítulo. El Capítulo 4 se separa en Resultados (05) y Discusión (06), como en la auditoría previa.

Diferencia con la auditoría previa: con este método, «así» da 17 en el Capítulo 4 y 9 en la Discusión (la auditoría previa dio 16 y 8); los comienzos coinciden: 11 «La Tabla», 8 «El directorio» y 7 «La lectura» en el Cap. 4, 7 «La memoria» en el Cap. 2 y 6 «El sistema» en el Cap. 5.

| Capítulo | Oraciones | «así» | «La Tabla» | «El directorio» | «La lectura» | «La memoria» | «El sistema» | «En este» | «Esta sección» |
|---|---|---|---|---|---|---|---|---|---|
| Resumen | 12 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| Abstract | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Introducción | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Cap. 1 | 69 | 2 | 0 | 1 | 0 | 0 | 1 | 1 | 0 |
| Cap. 2 | 120 → **118** | 0 | 1 | 0 | 0 | 7 → **6** | 0 | 1 | 0 |
| Cap. 3 | 182 | 2 | 0 | 1 | 1 | 0 | 0 | 3 → **2** | 2 |
| Cap. 4 (Resultados, 05) | 301 → **297** | 8 | 11 → **8** | 4 | 1 | 3 | 4 | 1 | 3 → **2** |
| Cap. 4 (Discusión, 06) | 211 | 9 → **7** | 0 | 4 | 6 | 0 | 1 | 7 → **5** | 0 |
| Cap. 5 | 93 → **91** | 0 | 0 | 2 | 2 | 0 | 6 → **5** | 0 | 0 |
| Apéndice A | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Lectura de la tabla: el número de oraciones baja donde se unieron o quitaron oraciones. Solo se corrigió donde la repetición se nota al leer, es decir, cuando dos o tres oraciones cercanas abren igual o cuando una oración solo anuncia una tabla. «El directorio» (8) y «La lectura» (7) en el Cap. 4 están repartidas en unas 50 páginas, y casi siempre son el sujeto natural, así que se dejaron. Lo mismo vale para el «así que» de Resultados: 8 apariciones en 1300 líneas, sin coincidir dos en un mismo párrafo. Se buscaron también «claramente», «notablemente», «crucial», «sin duda», «cabe destacar», «es importante», «en este sentido» y parecidas: no aparecen. El único énfasis de la lista que sí aparece es «de forma robusta» (3 veces, cambios 6, 14 y 22).

Total: **26 cambios**. Por capítulo: Cap. 1 1, Cap. 2 3, Cap. 3 1, Cap. 4 16, Cap. 5 5.

## Cambios

### 1. `.tex_uacj/Capitulo1.tex:42`

- **Capítulo:** Cap. 1
- **Patrón:** cambio de registro
- **Motivo:** «necesita que alguien le entregue» personifica y suena coloquial; se dice lo mismo sin el «alguien».

Viejo:

```latex
Una memoria entrópica opera sobre vectores cuantizados, así que necesita que alguien
le entregue las palabras y las imágenes como vectores.
```

Nuevo:

```latex
Una memoria entrópica opera sobre vectores cuantizados, así que las palabras y las
imágenes tienen que llegarle como vectores.
```

### 2. `.tex8/secciones/02_marco_teorico.tex:48` (se regenera en `.tex_uacj/Capitulo2.tex`)

- **Capítulo:** Cap. 2
- **Patrón:** comienzo repetido («La memoria»)
- **Motivo:** Dos oraciones seguidas empiezan con «La memoria»; la segunda se reordena desde su origen.

Viejo:

```latex
La memoria va formando abstracciones y prototipos a partir de esta superposición
estadística, sin que se impongan desde el exterior ni se calculen por separado.
```

Nuevo:

```latex
De esta superposición estadística van saliendo abstracciones y prototipos, sin que se
impongan desde el exterior ni se calculen por separado.
```

### 3. `.tex8/secciones/02_marco_teorico.tex:323` (se regenera en `.tex_uacj/Capitulo2.tex`)

- **Capítulo:** Cap. 2
- **Patrón:** ritmo entrecortado / transición
- **Motivo:** Cuatro oraciones cortas seguidas (una partida a media línea); se unen dos pares y se explicita la relación causal que ya estaba implícita.

Viejo:

```latex
En este sistema, el directorio se actualiza solo por interacción.
Lo anotan los módulos
que participaron en cada consulta resuelta (Sección~\ref{sec:componentes}).
En los grupos de personas no es el único camino.
Los miembros también se reparten las
categorías que recordará cada uno según estereotipos de
género
```

Nuevo:

```latex
En este sistema, el directorio se actualiza solo por interacción, y lo anotan los
módulos que participaron en cada consulta resuelta (Sección~\ref{sec:componentes}).
En los grupos de personas no es el único camino, porque los miembros también se
reparten las categorías que recordará cada uno según estereotipos de
género
```

### 4. `.tex8/secciones/02_marco_teorico.tex:400` (se regenera en `.tex_uacj/Capitulo2.tex`)

- **Capítulo:** Cap. 2
- **Patrón:** muletilla («reencuentra»)
- **Motivo:** «reencuentra» aparece dos veces en 20 líneas (l. 383 y 400) y otra vez como «reencuentro» en la Discusión; se deja la primera.

Viejo:

```latex
La ventaja de partir el contenido entre especialistas (Sección~\ref{sec:eham-unica})
reencuentra ese principio.
```

Nuevo:

```latex
La ventaja de partir el contenido entre especialistas (Sección~\ref{sec:eham-unica})
responde al mismo principio.
```

### 5. `.tex8/secciones/03_arquitectura.tex:92` (se regenera en `.tex_uacj/Capitulo3.tex`)

- **Capítulo:** Cap. 3
- **Patrón:** comienzo repetido («En este sistema»)
- **Motivo:** Dos párrafos seguidos abren con «En este sistema,» (l. 85 y 92); el contexto ya está dado.

Viejo:

```latex
En este sistema, la coordinación de la recuperación vale también para imágenes.
```

Nuevo:

```latex
La coordinación de la recuperación vale también para imágenes.
```

### 6. `.tex8/secciones/05_resultados.tex:433` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** énfasis sin respaldo («robusta»)
- **Motivo:** «de forma robusta» no dice qué se midió; se usa el criterio que el propio texto aplica en la Sección de calibración fija (positiva en 3 de 5 sorteos).

Viejo:

```latex
(89.7\,\%), sin superarlo de forma robusta (Sección~\ref{sec:calibracion-fija}).
```

Nuevo:

```latex
(89.7\,\%), sin una ventaja que se sostenga entre sorteos
(Sección~\ref{sec:calibracion-fija}).
```

### 7. `.tex8/secciones/05_resultados.tex:437` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** conclusión repetida sin interpretación nueva
- **Motivo:** Título, «El orden sí cambia la velocidad» y «El orden solo determina cuándo…» dicen lo mismo tres veces; se quita la oración que repite el título y la explicación del destino pasa junto al destino. Las cifras quedan iguales.

Viejo:

```latex
Sección~\ref{sec:proto-completo} (2.914 bits).
El orden sí cambia la velocidad.
La precisión madura llega al 70\,\% tras 13 interacciones en orden intercalado, tras 28 a
42 en orden barajado (según la semilla) y tras 59 en orden bloqueado; al 75\,\%, tras 18,
40 a 51 y 71.
La invariancia del destino ocurre por construcción, porque el ganador de cada
interacción lo deciden las memorias de contenido, que no cambian durante la formación, y
el registro es una suma (ecuación~\eqref{eq:registro}), que no depende del orden de los
sumandos.
El orden solo determina cuándo el directorio parcial se vuelve utilizable.
```

Nuevo:

```latex
Sección~\ref{sec:proto-completo} (2.914 bits).
La invariancia del destino ocurre por construcción, porque el ganador de cada
interacción lo deciden las memorias de contenido, que no cambian durante la formación, y
el registro es una suma (ecuación~\eqref{eq:registro}), que no depende del orden de los
sumandos.
El orden solo determina cuándo el directorio parcial se vuelve utilizable.
La precisión madura llega al 70\,\% tras 13 interacciones en orden intercalado, tras 28 a
42 en orden barajado (según la semilla) y tras 59 en orden bloqueado; al 75\,\%, tras 18,
40 a 51 y 71.
```

### 8. `.tex8/secciones/05_resultados.tex:453, 456` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** comienzo repetido («La Tabla»)
- **Motivo:** Once oraciones empiezan con «La Tabla»; esta solo anuncia la tabla y la referencia cabe entre paréntesis.

Fragmento 1 (línea 453):

Viejo:

```latex
$I \in \{25, 50, 100, 200, 328\}$, con el llenado imagen-etiqueta.
```

Nuevo:

```latex
$I \in \{25, 50, 100, 200, 328\}$, con el llenado imagen-etiqueta
(Tabla~\ref{tab:capacidad}).
```

Fragmento 2 (línea 456):

Viejo:

```latex
clases presentadas al módulo.
La Tabla~\ref{tab:capacidad} resume las métricas.
```

Nuevo:

```latex
clases presentadas al módulo.
```

### 9. `.tex8/secciones/05_resultados.tex:941` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** sintaxis enredada (inciso explicativo)
- **Motivo:** Sujeto largo con un inciso que redefine el sujeto; se dice en orden directo.

Viejo:

```latex
Lo que cuesta elegir el módulo con el directorio en lugar de con la clase real, la
distancia del protocolo al oráculo sobre el total, es de 6.8 puntos con 25 imágenes por
clase y de 3.2 desde 50.
```

Nuevo:

```latex
Elegir el módulo con el directorio en lugar de con la clase real cuesta, sobre el
total, 6.8 puntos frente al oráculo con 25 imágenes por clase y 3.2 desde 50.
```

### 10. `.tex8/secciones/05_resultados.tex:988` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** comienzo repetido («Esta sección mide»)
- **Motivo:** Dos subsecciones seguidas abren con «Esta sección mide qué aporta/agrega…» (l. 851 y 988).

Viejo:

```latex
Esta sección mide qué agrega la memoria asociativa frente a decisores simples que usan
exactamente los mismos vectores que el sistema.
```

Nuevo:

```latex
La pregunta es qué agrega la memoria asociativa frente a decisores simples que usan
exactamente los mismos vectores que el sistema.
```

### 11. `.tex8/secciones/05_resultados.tex:1118, 1155` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** comienzo repetido («La Tabla»)
- **Motivo:** Oración que solo anuncia la tabla; la referencia pasa a la oración que da sus cifras.

Fragmento 1 (línea 1118):

Viejo:

```latex
umbral de energía de la Sección~\ref{sec:hemisferio-visual}.
La Tabla~\ref{tab:lineas-base-imagen} da los resultados.
```

Nuevo:

```latex
umbral de energía de la Sección~\ref{sec:hemisferio-visual}.
```

Fragmento 2 (línea 1155):

Viejo:

```latex
con 1 a 4 falsos, frente a 631 del sistema, con 2 falsos y 23 rechazos.
```

Nuevo:

```latex
con 1 a 4 falsos, frente a 631 del sistema, con 2 falsos y 23 rechazos
(Tabla~\ref{tab:lineas-base-imagen}).
```

### 12. `.tex8/secciones/05_resultados.tex:1267, 1291` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** comienzo repetido («La Tabla»)
- **Motivo:** Igual que el anterior: la referencia pasa a la oración que da el total.

Fragmento 1 (línea 1267):

Viejo:

```latex
de modo que todo corre en CPU.
La Tabla~\ref{tab:costo} resume los tiempos.
```

Nuevo:

```latex
de modo que todo corre en CPU.
```

Fragmento 2 (línea 1291):

Viejo:

```latex
El sistema completo se reproduce en 102.9 minutos.
```

Nuevo:

```latex
El sistema completo se reproduce en 102.9 minutos (Tabla~\ref{tab:costo}).
```

### 13. `.tex8/secciones/06_discusion.tex:8` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** repetición del título y dos puntos explicativos
- **Motivo:** La primera oración repite literalmente el título de la subsección y abre con dos puntos; se queda solo la enumeración.

Viejo:

```latex
El mecanismo transactivo funciona con ocho dominios: los directorios
heteroasociativos, la lectura normalizada, el rechazo por contención, la actualización
perspectival del directorio ---en imagen--- y la coordinación punto a punto operan sin
ajustes por dominio.
```

Nuevo:

```latex
Los directorios heteroasociativos, la lectura normalizada, el rechazo por contención,
la actualización perspectival del directorio ---en imagen--- y la coordinación punto a
punto operan con los ocho dominios sin ajustes por dominio.
```

### 14. `.tex8/secciones/06_discusion.tex:131` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** énfasis sin respaldo («robusta»)
- **Motivo:** Mismo caso que el cambio 6; la oración sigue con el rango por sorteo, que es lo que respalda la afirmación.

Viejo:

```latex
acierta el 89.7\,\%, sin superarla de forma robusta; la diferencia pasa de $-10.7$
```

Nuevo:

```latex
acierta el 89.7\,\%, sin una ventaja que se sostenga entre sorteos; la diferencia pasa de $-10.7$
```

### 15. `.tex8/secciones/06_discusion.tex:298` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** transición sin relación clara / muletilla («reencuentro»)
- **Motivo:** «Es un reencuentro de un principio» es torpe, y «Se ve en la fidelidad» no dice qué se ve; se nombra el sujeto (la menor mezcla).

Viejo:

```latex
Es un reencuentro de un principio conocido en las memorias asociativas
(Sección~\ref{sec:trabajo-relacionado}).
Se ve en la fidelidad.
```

Nuevo:

```latex
Es un principio conocido en las memorias asociativas
(Sección~\ref{sec:trabajo-relacionado}).
La menor mezcla se ve también en la fidelidad.
```

### 16. `.tex8/secciones/06_discusion.tex:263` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** fórmula repetida («tiene análogos»)
- **Motivo:** Dos oraciones temáticas seguidas terminan en «tiene análogos» (l. 255 y 263).

Viejo:

```latex
El estado intermedio, reconocer sin poder nombrar, también tiene análogos.
```

Nuevo:

```latex
El estado intermedio, reconocer sin poder nombrar, también se observa en las personas.
```

### 17. `.tex8/secciones/06_discusion.tex:270` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** comienzo repetido («En este sistema»)
- **Motivo:** Tres oraciones en 20 líneas abren con «En este sistema» (l. 260, 270 y 278).

Viejo:

```latex
En este sistema el estado aparece en cuanto hay datos sin pareja.
```

Nuevo:

```latex
Aquí el estado aparece en cuanto hay datos sin pareja.
```

### 18. `.tex8/secciones/06_discusion.tex:278` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** comienzo repetido («En este sistema»)
- **Motivo:** Tercera apertura igual en el párrafo; el sujeto real de la oración es el estado intermedio.

Viejo:

```latex
En este sistema, sería el momento de consultar el directorio, porque el módulo sabe que
```

Nuevo:

```latex
Ese estado intermedio sería el momento de consultar el directorio, porque el módulo sabe que
```

### 19. `.tex8/secciones/06_discusion.tex:366` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** referencia ambigua
- **Motivo:** «Su ventaja» puede leerse como la de la búsqueda léxica o la del vocabulario; se nombra el rechazo.

Viejo:

```latex
Su ventaja aparece frente a un almacén único.
```

Nuevo:

```latex
La ventaja de este rechazo aparece frente a un almacén único.
```

### 20. `.tex8/secciones/06_discusion.tex:425` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** muletilla («así que») y arranque flojo («Aquí son»)
- **Motivo:** Se dice la condición primero y se quita el «así que» final.

Viejo:

```latex
Aquí son ocho módulos con contenido fijo y especialización asignada, como en la
condición de estructura asignada de Wegner, Erber y Raymond~\cite{wegner1991transactive},
así que no hay mucho que ganar en acierto.
```

Nuevo:

```latex
Con ocho módulos de contenido fijo y especialización asignada, como en la condición de
estructura asignada de Wegner, Erber y Raymond~\cite{wegner1991transactive}, no hay
mucho que ganar en acierto.
```

### 21. `.tex8/secciones/06_discusion.tex:599` (se regenera en `.tex_uacj/Capitulo4.tex`)

- **Capítulo:** Cap. 4
- **Patrón:** muletilla («así que»)
- **Motivo:** Causa antes de la consecuencia, sin el conector repetido.

Viejo:

```latex
La diferencia de redundancia entre las dos lecturas viene de la construcción, así que la
disociación no prueba dos procesos
```

Nuevo:

```latex
Como la diferencia de redundancia entre las dos lecturas viene de la construcción, la
disociación no prueba dos procesos
```

### 22. `.tex8/secciones/07_conclusiones.tex:21` (se regenera en `.tex_uacj/Capitulo5.tex`)

- **Capítulo:** Cap. 5
- **Patrón:** énfasis sin respaldo («robusta»)
- **Motivo:** Mismo caso que el cambio 6; el contexto inmediato ya habla de sorteos y da las diferencias.

Viejo:

```latex
superarla de forma robusta ($+0.2$ puntos
```

Nuevo:

```latex
superarla de forma sostenida ($+0.2$ puntos
```

### 23. `.tex8/secciones/07_conclusiones.tex:90, 100, 104` (se regenera en `.tex_uacj/Capitulo5.tex`)

- **Capítulo:** Cap. 5
- **Patrón:** conclusión repetida y transición sin relación
- **Motivo:** La última oración del párrafo («Y las consultas de las clases con léxico compartido se van hacia la clase vecina…») repite lo dicho seis líneas antes y llega tras hablar del directorio; la cita pasa a la oración original. Se unen también dos oraciones cortas sobre el directorio.

Fragmento 1 (línea 90):

Viejo:

```latex
6 de 28), y
\texttt{pear} es difícil para todos los decisores.
```

Nuevo:

```latex
6 de 28),
como en la sobrecarga de pistas de la memoria humana~\cite{watkins1975buildup}, y
\texttt{pear} es difícil para todos los decisores.
```

Fragmento 2 (línea 100):

Viejo:

```latex
El directorio funciona como un índice que localiza al especialista.
Formarlo cuesta interacción.
```

Nuevo:

```latex
El directorio funciona como un índice que localiza al especialista, y formarlo cuesta
interacción.
```

Fragmento 3 (línea 104):

Viejo:

```latex
sostenga entre sorteos ($+1.3$ puntos con 291; de $-0.8$ a $+6.7$ según el sorteo).
Y las consultas de las clases con léxico compartido se van hacia la clase vecina, como
en la sobrecarga de pistas de la memoria humana~\cite{watkins1975buildup}.
```

Nuevo:

```latex
sostenga entre sorteos ($+1.3$ puntos con 291; de $-0.8$ a $+6.7$ según el sorteo).
```

### 24. `.tex8/secciones/07_conclusiones.tex:109` (se regenera en `.tex_uacj/Capitulo5.tex`)

- **Capítulo:** Cap. 5
- **Patrón:** sintaxis enredada
- **Motivo:** El complemento «en el acierto de clase…» va antes del sujeto y obliga a releer.

Viejo:

```latex
Con el mismo contenido, en el acierto de clase del sistema transactivo y de una sola
memoria con las ocho clases, la diferencia por consulta no excluye el cero desde 50
imágenes por clase
```

Nuevo:

```latex
Con el mismo contenido, la diferencia por consulta en el acierto de clase entre el
sistema transactivo y una sola memoria con las ocho clases no excluye el cero desde 50
imágenes por clase
```

### 25. `.tex_uacj/ConclusionObjetivoGeneral.tex:7`

- **Capítulo:** Cap. 5
- **Patrón:** comienzo repetido («El sistema»)
- **Motivo:** «El sistema» abre las oraciones de las l. 2 y 7.

Viejo:

```latex
El sistema tiene ocho módulos, cada uno con una memoria de contenido heteroasociativa
y dos directorios, y un mediador que deja de intervenir en la fase madura.
```

Nuevo:

```latex
Son ocho módulos, cada uno con una memoria de contenido heteroasociativa y dos
directorios, y un mediador que deja de intervenir en la fase madura.
```

### 26. `.tex_uacj/ConclusionObjetivoGeneral.tex:74`

- **Capítulo:** Cap. 5
- **Patrón:** término definido
- **Motivo:** «los errores» puede leerse como errores totales (rechazos incluidos); los 169 son falsos enrutamientos, el término que usa el resto del reporte (Sección~\ref{sec:codificador-sin-clase}).

Viejo:

```latex
los errores suben de 2 a 169
```

Nuevo:

```latex
los falsos enrutamientos suben de 2 a 169
```

## Problemas de contenido vistos y no tocados

Se anotan para que el autor decida. No se corrigieron porque tocan cifras, referencias o el peso de una afirmación.

1. **Cifra repetida en la misma subsección.** `05_resultados.tex:44-47` y `:57-58` dicen lo mismo: las consultas 201 a 400 traen el nombre de su clase en el 84.5\,% de los casos y aciertan 195 de 200 (97.5\,%) en la fase temprana. Las notas al pie de las líneas 47-49 y 62-64 repiten la misma aclaración («El nombre de la clase cuenta si aparece como palabra de la consulta, también en plural»), que también está en `04_metodologia.tex:194-197`. Quitar la primera mención acortaría la apertura de la calibración, pero quitaría una aparición de cifras, y eso no cabe en esta revisión.
2. **Porcentaje de pistas compartidas.** `07_conclusiones.tex:119` dice «sobre el 4\,% de las consultas»; `05_resultados.tex:952` dice «el 3.5\,% de las respuestas». Cambian el redondeo y el denominador (consultas o respuestas). Conviene que digan lo mismo.
3. **Remisión a una limitación que no corresponde.** `07_conclusiones.tex:61-64`: la oración termina en «(limitación (k))», pero solo la parte del codificador es la limitación (k). La suma por tokens, la normalización, $\tau$ y el rescate léxico están en la Sección de auditoría y en las limitaciones (g) y (h).
4. **Resumen y Abstract no dicen lo mismo.** El Abstract agrega «on 80 queries that seldom name their class», y el Resumen no tiene nada equivalente. En los dos, «(27.2 frente a 32.5)» no dice que es una distancia euclidiana en el espacio latente. Corregirlo cambiaría la longitud de páginas que ya caben justas.
5. **«El nombre se pierde con un daño del 1\,%».** `06_discusion.tex:41` y `07_conclusiones.tex:98` dicen eso, pero la Tabla de lesión y la limitación (j) dan el 92\,% de imágenes sin nombre con el 1\,% y el 100\,% con el 5\,%. Como resumen se entiende, pero exagera un poco.
6. **Afirmación vaga.** `03_arquitectura.tex:422-423`: «de modo que la puntuación refleja la calidad de la especialización». Lo que la división garantiza, por definición, es que la puntuación no crezca con el número de registros. «Calidad de la especialización» no se mide en ninguna parte. Hacerla más precisa cambiaría la afirmación, por eso no se tocó.
7. **Conclusión repetida casi palabra por palabra.** «un rechazo que en texto no usa umbral, aunque equivale a la pertenencia al vocabulario, y en imagen depende del umbral de energía $\tau$» aparece en `06_discusion.tex:431-433`, `07_conclusiones.tex:78-79` y `07_conclusiones.tex:209-211`, y la tríada «recuerdo, decisiones legibles en los registros, rechazo» vuelve en el Resumen, la Introducción y `ConclusionObjetivoGeneral.tex:84-85`. Es el mensaje central y se entiende que se repita en la síntesis, pero tres veces en dos capítulos seguidos se nota. Si se recorta, es decisión del autor.
8. **Pasaje repetido entre capítulos.** La frase sobre la especialización asignada «como en la condición de estructura asignada de Wegner, Erber y Raymond» y «la asignación de información no se modela; la hace la etiqueta» está en `Capitulo1.tex:191-199`, `02_marco_teorico.tex:332-335`, `06_discusion.tex:425-426` y en la limitación (e), `06_discusion.tex:526-531`. Las cuatro dicen lo mismo, sin agregar nada.
9. **La salvedad «estructurales, no causales» aparece tres veces.** Está en `06_discusion.tex:95`, `:205` y `:434-435`. Es una salvedad deliberada y no se tocó. Bastaría con una sola declaración, al principio de la Sección de lectura desde Wegner, que cubra las tres secciones.
10. **Transición débil en la Justificación.** `Capitulo1.tex:158`: «El rechazo importa por la misma razón». La razón anterior es la trazabilidad, que sirve para auditar y explicar. Lo que sigue habla de no obligar al usuario a adivinar cuándo se equivocó el sistema. La relación existe, pero no es la misma razón.

## Problemas de contenido 1 a 4: corrección aprobada y aplicada

1. **Pistas compartidas.** Las dos cifras son fracción de respuestas, pero de brazos distintos: EHAM única y oráculo 3.5\,%, protocolo 4.1\,% desde 50 (`results/experimento11_protocolo_corregido/tablas_nuevas/README.md`). En Resultados se nombran las dos; en Conclusiones, «sobre el 4.1\,\% de sus respuestas».
2. **Limitación (k).** Ahora solo cubre el codificador; la suma por tokens, la normalización, $\tau$ y el rescate léxico remiten a la Sección de auditoría.
3. **Daño del 1\,%.** En la Discusión y en las Conclusiones: «destruir al azar el 1\,\% de las celdas deja sin nombre al 92\,\% de las imágenes», como la limitación (j) y la Tabla de lesión.
4. **Abstract.** Se quitó «that seldom name their class», para que diga lo mismo que el Resumen.

## Traducciones casi literales del Marco Teórico: corrección aprobada y aplicada

La búsqueda web del cotejo (60 oraciones en español sin coincidencia; 10 traducidas al inglés) mostró tres oraciones casi literales de los resúmenes de sus fuentes, todas citadas, y una paráfrasis que omitía una condición. Se reformularon en `02_marco_teorico.tex` con las mismas citas:

1. Mezcla de expertos (`jacobs1991adaptive`): la red de compuerta decide qué especialista atiende cada caso.
2. Interferencia catastrófica (`mccloskey1989catastrophic`): la red que aprende tareas una tras otra puede perder lo que ya sabía.
3. Índices de enrutamiento (`crespo2002routing`): resumen por vecino de los documentos por tema; el índice crece con los vecinos, no con los documentos.
4. Ren et al. (`ren2006contingent`): el beneficio en grupos grandes y entornos cambiantes es en rapidez; en calidad ganan más los grupos pequeños. Tomado del resumen del artículo; conviene confirmarlo en el texto completo.
