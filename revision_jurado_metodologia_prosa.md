# Propuesta viejo/nuevo: metodología y cifras (lectura de jurado)

**Estado:** pendiente de aprobación. No se aplicó nada: la tesis, `una-hetero` en `df2f893`, está sin cambios, sin commit y sin push.

**Alcance:** lo que pide `revision_jurado/jurado_metodologia.md` y no cubren `revision_jurado_estructura_prosa.md` ni `revision_jurado_claridad_prosa.md`:
- **M1:** clase correcta del experimento 11 sobre el total, McNemar, sin «clasifica algo mejor» ni «intervalos separados».
- **M2:** calibración con la diferencia madura menos temprana, las semillas que no varían y D y G como consultas más fáciles.
- **M3:** composición del banco y de la partición reservada.
- **M4:** solo la parte que nadie cubre: en el experimento 16 el codificador vio todos los objetos.
- **M5:** decisiones tomadas después de ver los datos y el $p$ fuera de dominio por corte.
- **Menores:** evocación estricta y azar, el total tras $\tau$ en el experimento 14 y las versiones que faltan.

**Convenciones:**
- `05:522-530` es `.tex8/secciones/05_resultados.tex`, líneas 522 a 530; lo mismo para 01–07 y `main`.
- Los «Viejo» están copiados del `.tex8` y un script los cotejó (solo espacios normalizados): coinciden todos.
- Los textos nuevos ya traen la forma de la propuesta de claridad: `\,\%`, comillas angulares, números en letra, «lectura normalizada» fuera de la calibración, «concordancia», «clase real», «configuración» y dos puntos explicativos cambiados (claridad 3.7).
- `[PENDIENTE: exp11 corregido]` va al final de la frase y cubre todas sus cifras del brazo del protocolo del experimento 11. Esas cifras son las de la corrida actual, en la que los directorios perspectivales no se reiniciaban entre trabajos (`salida.md`, tabla M1.5): son provisionales. Las de la EHAM única y el oráculo siguen valiendo.
- «Reanálisis» es `results/reanalisis_jurado/salida.md`; cada cifra dice de qué tabla sale.

**Adelanto del reanálisis sobre la corrida actual** (se confirma o cambia con exp11 corregido): sobre el total, el protocolo y la EHAM única empatan en clase correcta en los cuatro cortes. Con 200 imágenes por clase la diferencia es de +0.1 puntos [−2.9, +3.2], y ninguna prueba pareada es significativa, ni sobre el total ni sobre las respondidas ($p$ entre 0.09 y 1; tabla M1.2).

**Orden:** esta propuesta se aplica después de la de estructura y antes de la de claridad. No comparte ningún pasaje con la de estructura, solo bordes:
- M2.2 va justo después del texto de estructura 4.2;
- M1.6 sigue la frase de estructura 7.7;
- M2.9 y Me.2 rodean a estructura 9.3;
- M3.1 queda antes de estructura 2.4.

Con la de claridad sí comparte pasajes: cada punto dice qué absorbe, y la propuesta de claridad lo marca como absorbido.

---

## M1. Clase correcta en la comparación con una sola EHAM

### M1.1 Acierto de clase
- **Dónde:** `05:522-530`
- **Viejo:**
```latex
\paragraph{Acierto de clase.}
Con 25 imágenes por clase la EHAM única acierta la clase algo más que el protocolo
(97.6\,\% frente a 96.9\,\%), con intervalos de 95\,\% que se solapan ($[97.4, 97.8]$ y
$[96.3, 97.6]$).
Desde 50 el orden se invierte y los intervalos se separan (con 200, $[97.9, 98.6]$ para
el protocolo y $[96.7, 97.1]$ para la EHAM única).
Lo que cuesta elegir el módulo con el directorio en lugar de con la verdad de terreno, la
distancia del protocolo al oráculo, es de 3.1 puntos con 25 imágenes por clase y de 1.2
a 1.7 desde 50.
```
- **Nuevo:**
```latex
\paragraph{Acierto de clase.}
El protocolo deja sin responder entre el 1.3 y el 1.6\,\% de las 171 consultas
reservadas y la EHAM única las responde todas, así que el acierto de clase se da de dos
maneras, sobre las consultas respondidas y sobre el total, en el que la falta de
respuesta cuenta como fallo.
Sobre el total, la EHAM única acierta el 97.6, 97.5, 97.6 y 96.9\,\% con 25, 50, 100 y
200 imágenes por clase, y el protocolo, el 95.3, 97.4, 97.4 y 97.0\,\%
[PENDIENTE: exp11 corregido].
Las diez semillas no cambian las consultas, así que la comparación se hace pareada por
consulta, con McNemar exacto.
Con 200 imágenes por clase, la diferencia sobre el total es de +0.1 puntos, con un
intervalo de 95\,\% de $[-2.9, +3.2]$ por remuestreo de consultas, y en ningún corte es
significativa, ni sobre el total ni sobre las respondidas ($p \geq 0.09$)
[PENDIENTE: exp11 corregido].
En acierto de clase, los dos empatan [PENDIENTE: exp11 corregido].
Lo que cuesta elegir el módulo con el directorio en lugar de con la clase real, la
distancia del protocolo al oráculo sobre el total, es de 4.7 puntos con 25 imágenes por
clase y de 2.6 a 3.0 desde 50 [PENDIENTE: exp11 corregido].
```
- **Por qué:** M1. La tesis calcula la clase correcta sobre las consultas respondidas (`run_experiment11_monolithic.py:597`, filtro de `_rate` en 578-582), y los intervalos salen de diez medias por semilla, que no cuentan la variación entre consultas. Salen «algo más que» y «los intervalos se separan».
- **Fuente:**
  - Respuesta del protocolo, 98.4 / 98.7 / 98.7 / 98.7 % (de ahí el 1.3–1.6 %); clase sobre el total; distancia al oráculo sobre el total, 4.7 / 2.6 / 2.6 / 3.0: tabla M1.1.
  - +0.1 [−2.9, +3.2] y $p$ por consulta (total: 0.093, 0.804, 1, 0.664; respondidas: 0.359, 0.267, 0.424, 0.143): tabla M1.2.
  - Las semillas cambian el módulo de entrada (protocolo) y el muestreo del recuerdo (EHAM única), no las consultas: tabla M1.3 y su lectura en `revision_jurado/reanalisis_nube.md`.
- **Cruces:** absorbe claridad S61 en 05:528 («verdad de terreno» → «clase real»).
- **Si exp11 corregido cambia el resultado:** si la diferencia sale significativa en algún corte, la frase «En acierto de clase, los dos empatan» se cambia por el corte y el $p$. La estructura del párrafo, con las dos versiones y McNemar, se queda.

### M1.2 Pie de la Tabla 5
- **Dónde:** `05:482-485`
- **Viejo:**
```latex
    \caption{Una sola EHAM contra los especialistas, por número de imágenes de llenado
    por clase (media de 10 semillas). Texto: 171 consultas reservadas; clase correcta
    según el juez 1-NN, distancia a la instancia real más cercana y, en el protocolo,
    enrutamiento a la clase de la consulta. Imagen $\to$ texto: 80 imágenes de prueba;
```
- **Nuevo:**
```latex
    \caption{Una sola EHAM contra los especialistas, por número de imágenes de llenado
    por clase (media de diez semillas). Texto: 171 consultas reservadas; clase correcta
    según el juez 1-NN, sobre las consultas respondidas y sobre el total; distancia
    euclidiana, en el espacio latente continuo, a la instancia real más cercana de la
    clase de la consulta, sobre las respondidas, y, en el protocolo, respuesta y
    enrutamiento a la clase de la consulta [PENDIENTE: exp11 corregido]. Imagen $\to$
    texto: 80 imágenes de prueba;
```
- **Por qué:** M1 y la distancia de M1.7.
- **Cruces:** absorbe claridad S51 en el pie («distancia euclidiana, en el espacio latente continuo») y 3.3 («diez semillas»). Agrega «de la clase de la consulta» (claridad Parte 4, punto 11).

### M1.3 Filas de la Tabla 5
- **Dónde:** `05:495-504`
- **Viejo:**
```latex
        Medida & Brazo & 25 & 50 & 100 & 200 \\
        \midrule
        Clase correcta (\%)        & EHAM única & 97.6 & 97.5 & 97.6 & 96.9 \\
                                   & Protocolo  & 96.9 & 98.8 & 98.8 & 98.3 \\
                                   & Oráculo    & 100  & 100  & 100  & 100  \\
        \midrule
        Enrutamiento correcto (\%) & Protocolo  & 95.3 & 97.4 & 97.4 & 97.0 \\
        \midrule
        Distancia a la instancia   & EHAM única & 22.9 & 26.6 & 29.4 & 32.5 \\
        real más cercana           & Protocolo  & 19.0 & 20.7 & 23.8 & 27.0 \\
```
- **Nuevo:**
```latex
        Medida & Configuración & 25 & 50 & 100 & 200 \\
        \midrule
        Clase correcta,            & EHAM única & 97.6 & 97.5 & 97.6 & 96.9 \\
        respondidas (\%)           & Protocolo  & 96.9 & 98.8 & 98.8 & 98.3 \\
                                   & Oráculo    & 100  & 100  & 100  & 100  \\
        \midrule
        Clase correcta,            & EHAM única & 97.6 & 97.5 & 97.6 & 96.9 \\
        total (\%)                 & Protocolo  & 95.3 & 97.4 & 97.4 & 97.0 \\
                                   & Oráculo    & 100  & 100  & 100  & 100  \\
        \midrule
        Responde (\%)              & Protocolo  & 98.4 & 98.7 & 98.7 & 98.7 \\
        \midrule
        Enrutamiento correcto (\%) & Protocolo  & 95.3 & 97.4 & 97.4 & 97.0 \\
        \midrule
        Distancia a la instancia   & EHAM única & 22.9 & 26.6 & 29.4 & 32.5 \\
        más cercana de su clase    & Protocolo  & 19.0 & 20.7 & 23.8 & 27.0 \\
```
- **Por qué:** M1 pide las dos versiones junto con la cobertura.
- **Fuente:** tabla M1.1 (respondidas, total y «responde %»). El oráculo y la EHAM única responden el 100 %, así que sus dos filas coinciden.
- **Cruces:** absorbe claridad S61 («Brazo» → «Configuración») y S51 en la tabla. S51 proponía «Distancia euclidiana a la / instancia real más cercana (latente)»; aquí la unidad va en el pie, para que la celda quepa con «de su clase».
- **Nota:** todas las filas del protocolo, también las que no cambian de redacción (distancia, imagen → texto y fuera de dominio), esperan exp11 corregido; el marcador del pie las cubre.

### M1.4 Discusión: clase, cobertura y costo del directorio
- **Dónde:** `06:189-203`
- **Viejo:**
```latex
La exactitud de clase también mejora, pero poco.
Desde 50 imágenes por clase el protocolo acierta entre 98.3 y 98.8\,\% frente a
96.9--97.6\,\% de la EHAM única, con intervalos separados; con 25 la EHAM única queda
arriba (97.6 frente a 96.9\,\%, con intervalos que se solapan), porque el directorio
todavía enruta peor (95.3\,\% de enrutamiento correcto).

El precio es cobertura y un índice.
El especialista deja sin respuesta al 2.5\,\% de las imágenes de prueba con 200 por
clase, que la EHAM única responde: una de las 80 imágenes porque la contención es
estricta en las 64 coordenadas del latente y otra porque el recuerdo no devuelve palabras.
Es parte del rechazo residual del hemisferio visual (limitación (b)); el protocolo de
esta comparación, que forma su directorio visual sin variantes, responde al 81\,\%.
A eso se suman el error del directorio, de 1.2 a 1.7 puntos de clase desde 50 imágenes
por clase (3.1 con 25), y ocho veces las celdas de memoria: una heteroasociativa por
módulo en lugar de una.
```
- **Nuevo:**
```latex
En acierto de clase, los dos empatan.
Sobre el total de las 171 consultas reservadas, contando la falta de respuesta como
fallo, la diferencia entre el protocolo y la EHAM única no es significativa en ningún
corte (McNemar exacto, $p \geq 0.09$); con 200 imágenes por clase es de +0.1 puntos,
con un intervalo de 95\,\% de $[-2.9, +3.2]$ (Sección~\ref{sec:eham-unica})
[PENDIENTE: exp11 corregido].

La partición cuesta cobertura y requiere un directorio.
El especialista deja sin respuesta al 2.5\,\% de las imágenes de prueba con 200 por
clase, que la EHAM única responde: una de las 80 imágenes porque la contención es
estricta en las 64 coordenadas del latente y otra porque el recuerdo no devuelve palabras.
Es parte del rechazo residual del hemisferio visual (limitación (b)); el protocolo de
esta comparación, que forma su directorio visual sin variantes, responde al 81\,\%
[PENDIENTE: exp11 corregido].
A eso se suman el error del directorio, de 2.6 a 3.0 puntos de clase sobre el total
desde 50 imágenes por clase (4.7 con 25) [PENDIENTE: exp11 corregido], y ocho veces las
celdas de memoria, porque hay una heteroasociativa por módulo en lugar de una sola.
```
- **Por qué:** M1: sale «con intervalos separados» y la mejora de clase.
- **Fuente:** tablas M1.1 y M1.2. El 2.5 % es del oráculo (97.5 % responde, `tab:eham-unica`), que sigue valiendo; el 81 % es del protocolo.
- **Cruces:** absorbe «exactitud» → «acierto» (claridad 1.1), claridad S31 en 06:195 («La partición cuesta cobertura y requiere un directorio») y la fila `06:202` de claridad 3.7.

### M1.5 Fidelidad del recuerdo e imagen → texto
- **Dónde:** `05:532-540`
- **Viejo:**
```latex
\paragraph{Fidelidad del recuerdo.}
La respuesta de la EHAM única queda más lejos de la instancia real más cercana en los
cuatro cortes, pero su brecha con el oráculo no crece con el contenido: 4.6, 6.2, 6.1 y
5.7 (calculada antes de redondear).
Cuando la primera pista reconocida es una etiqueta compartida entre clases
(\emph{fruit}, \emph{animal}, \emph{red}; el 3.5\,\% de las respuestas), la EHAM única
acierta la clase entre el 48 y el 52\,\%, y ninguna clase por sí sola sostiene más del
74--77\,\% de las coordenadas de su patrón; el protocolo acierta entre el 79 y el
84\,\%, y el oráculo el 100\,\%.
```
- **Nuevo:**
```latex
\paragraph{Fidelidad del recuerdo.}
La respuesta de la EHAM única queda más lejos de la instancia real más cercana de la
clase de la consulta en los cuatro cortes, pero su brecha con el oráculo no crece con el
contenido: 4.6, 6.2, 6.1 y 5.7 (calculada antes de redondear).
Cuando la primera pista reconocida es una etiqueta compartida entre clases
(\emph{fruit}, \emph{animal}, \emph{red}; el 3.5\,\% de las respuestas), la EHAM única
acierta la clase entre el 48 y el 52\,\%, y ninguna clase por sí sola sostiene más del
74--77\,\% de las coordenadas de su patrón; el protocolo acierta entre el 79 y el
84\,\%, y el oráculo el 100\,\% [PENDIENTE: exp11 corregido].
```
- **Dónde:** `05:542-546`
- **Viejo:**
```latex
\paragraph{Imagen $\to$ texto.}
La EHAM única responde más imágenes y se equivoca más de dominio: con 200 imágenes por
clase responde a todas, pero el 10.9\,\% con un dominio ajeno, frente al 4.1\,\% del
especialista elegido por el oráculo y el 3.0\,\% del protocolo, que en este experimento
forma su directorio visual sin variantes.
```
- **Nuevo:**
```latex
\paragraph{Imagen $\to$ texto.}
La EHAM única responde más imágenes y se equivoca más de dominio.
Con 200 imágenes por clase responde a todas, pero el 10.9\,\% con un dominio ajeno,
frente al 4.1\,\% del especialista elegido por el oráculo y el 3.0\,\% del protocolo,
que en este experimento forma su directorio visual sin variantes
[PENDIENTE: exp11 corregido].
```
- **Por qué:** el 79–84 % y el 3.0 % son del brazo del protocolo. La distancia es a la instancia más cercana de la clase de la consulta (M1.7).
- **Cruces:** absorbe la fila `05:543` de claridad 3.7 (dos puntos → punto).

### M1.6 Conclusiones frente a la EHAM única
- **Dónde:** `07:58-63`. Es el final de la frase que empieza en 07:55 (estructura 7.7).
- **Viejo:**
```latex
con un dominio ajeno menos veces (3.0\% de las imágenes, frente a 10.9\% con 200 por
clase).
Desde 50 imágenes por clase también clasifica algo mejor (1.4 puntos con 200); con 25,
no.
A cambio cubre menos, y el directorio le cuesta de 1.2 a 1.7 puntos de clase respecto
del oráculo desde 50 imágenes por clase.
```
- **Nuevo:**
```latex
con un dominio ajeno menos veces (3.0\,\% de las imágenes, frente a 10.9\,\% con 200
por clase) [PENDIENTE: exp11 corregido].
En acierto de clase, sobre el total de las consultas, los dos empatan
[PENDIENTE: exp11 corregido].
A cambio cubre menos, y el directorio le cuesta de 2.6 a 3.0 puntos de clase sobre el
total respecto del oráculo desde 50 imágenes por clase [PENDIENTE: exp11 corregido].
```
- **Por qué:** M1: sale «clasifica algo mejor (1.4 puntos con 200)».
- **Fuente:** tablas M1.1 y M1.2.

### M1.7 Qué mide la distancia
- **Dónde:** `05:472-473`
- **Viejo:**
```latex
Cada recuerdo se juzga por la clase de la instancia real más cercana (juez 1-NN) y por
la distancia a ella.
```
- **Nuevo:**
```latex
Cada recuerdo se juzga por la clase de la instancia real más cercana (juez 1-NN) y por
la distancia euclidiana, en el espacio latente continuo, a la instancia real más
cercana de la clase de la consulta; las dos medidas se calculan sobre las consultas
respondidas, y la clase correcta se da también sobre el total.
```
- **Por qué:** «la distancia a ella» decía la distancia a la instancia más cercana de cualquier clase. El código mide la distancia a la más cercana de la clase de la consulta, y las dos coinciden solo cuando el juez acierta (claridad Parte 4, punto 11, que lo dejaba a otra propuesta). Las dos medidas usan como denominador las consultas respondidas.
- **Fuente:** `run_experiment9_member_loss.py:243-246` (`d_nn_target` sobre las instancias de la clase objetivo, con `np.linalg.norm` sobre el latente descuantizado); `run_experiment11_monolithic.py:434` (`d_nn_truth = d_nn_target`) y `:597-600` (denominador `responde` para `nn_ok` y `d_nn_truth`).

---

## M2. Calibración: formación del directorio y composición de las consultas

### M2.1 Cómo se evalúa y qué cambia la semilla
- **Dónde:** `05:19-23`
- **Viejo:**
```latex
Cada una se evaluó sobre el banco de 411 consultas, con $N \in \{50, 100, 200, 400\}$
consultas para formar el directorio y 5 semillas por celda.
La Tabla~\ref{tab:calibracion} da los resultados en $N = 400$; la
Figura~\ref{fig:mature-vs-n} muestra cómo crece la precisión madura con $N$, y la
Figura~\ref{fig:heatmap-condicion} da los mismos valores como mapa de calor.
```
- **Nuevo:**
```latex
Cada una se evaluó con $N \in \{50, 100, 200, 400\}$ consultas del banco de 411, que
forman el directorio.
En siete condiciones son las primeras $N$ consultas del banco; D y G sortean en cambio
consultas balanceadas entre clases de todo el banco (48, 96, 200 y 399, porque el
sorteo balanceado no siempre llega a $N$).
Se corrieron cinco semillas por celda, pero la semilla solo interviene en ese sorteo y
en el módulo de entrada de la fase madura, que no cambia el resultado porque los ocho
módulos leen el mismo directorio compartido; en las otras siete condiciones las cinco
semillas dan resultados idénticos.
La Tabla~\ref{tab:calibracion} da los resultados en $N = 400$; la
Figura~\ref{fig:mature-vs-n} muestra cómo cambia la precisión madura con $N$, y la
Figura~\ref{fig:heatmap-condicion} da los mismos valores como mapa de calor.
```
- **Por qué:** M2: en 7 de las 9 condiciones la desviación estándar es 0.
- **Fuente:** tabla M2.2 (7 de 9 condiciones con las 108 columnas idénticas en las cinco semillas) y su nota (`run_ablation.py`, líneas 244, 312-313 y 325); 48, 96, 200 y 399: tabla M2.1, columna «consultas evaluadas» de D y G.
- **Cruces:** absorbe claridad 3.3 en 05:20 («cinco semillas»).

### M2.2 Párrafo nuevo: formación y composición
- **Dónde:** después del texto de estructura 4.2 (que reemplaza 05:28-29) y antes de la tabla (05:31).
- **Nuevo:**
```latex

\paragraph{Formación del directorio y composición de las consultas.}
Al crecer $N$ cambian a la vez el directorio y las consultas evaluadas, y las primeras
$N$ consultas no son una muestra del banco.
Traen el nombre de su clase en el 10.0, 15.0, 15.0 y 49.8\,\% de los casos con
$N = 50$, 100, 200 y 400, y el sorteo de D y G, entre el 50.0 y el 51.7\,\%.
La precisión temprana, que no usa el directorio, sube con ellas del 78.0 al 90.0\,\%.
Las consultas 201 a 400, que traen el nombre de su clase en el 84.5\,\% de los casos,
aciertan 195 de 200 en la fase temprana (97.5\,\%), frente a 165 de las primeras 200.
Sobre las mismas consultas, la diferencia entre la fase madura con la lectura B1 y la
temprana es de 0, +4.0, +5.5 y +3.0 puntos con $N = 50$, 100, 200 y 400, así que la
mayor parte del ascenso de la madura, del 78.0 al 93.0\,\%, es el de la temprana.\footnote{Reanálisis del banco,
\texttt{results/reanalisis\_jurado/salida.md}, tablas M2.1, M2.3, M2.4 y M2.5. El nombre
de la clase cuenta si aparece como palabra de la consulta, también en plural.}
Con un conjunto evaluado fijo, independiente de $N$, la precisión madura es de
[PENDIENTE: calibración con conjunto fijo].
```
- **Por qué:** M2: reportar la diferencia madura menos temprana sobre las mismas consultas y separar la formación de la dificultad.
- **Fuente:**
  - 10.0 / 15.0 / 15.0 / 49.8 %: tabla M2.4, «nombre (con plural)».
  - 50.0–51.7 %: tabla M2.5 (medias por $N$).
  - 78.0 → 90.0 % y 0 / +4.0 / +5.5 / +3.0: tabla M2.1, condición B1.
  - 84.5 %, 195 de 200 y 39 + 44 + 82 = 165: tabla M2.3.
  - Que restar aciertos entre cortes es válido (el ganador temprano no depende de $N$): nota de M2.3.

### M2.3 Pie de la Figura 4
- **Dónde:** `05:72-79`
- **Viejo:**
```latex
    \caption{Precisión madura en función de $N$ para las condiciones de la
    Tabla~\ref{tab:calibracion} ($N$ consultas del banco de 411, media de 5 semillas; la
    banda es $\pm 1$ desviación estándar de G).
    Entre las condiciones que solo cambian la lectura, B1 es la mejor en todo el rango y
    la cruda (A) queda por debajo.
    G, que además balancea las consultas, queda por encima de B1 en todo el rango; D lo
    supera en $N = 50$ y $200$.
    F coincide con A en todos los puntos y no se dibuja.}
```
- **Nuevo:**
```latex
    \caption{Precisión madura en función de $N$ para las condiciones de la
    Tabla~\ref{tab:calibracion} ($N$ consultas del banco de 411, media de cinco semillas;
    la banda es $\pm 1$ desviación estándar de G).
    Entre las condiciones que no alteran las consultas, B1 es la mejor en todo el rango y
    la cruda (A) queda por debajo.
    G y D se evalúan sobre un sorteo balanceado de todo el banco, con consultas más
    fáciles que las primeras $N$ (su precisión temprana va del 88.8 al 91.2\,\%, frente al
    78.0 a 90.0\,\% de las demás); de ahí que G quede por encima de B1 en todo el rango y
    D lo supere en $N = 50$ y $200$.
    F coincide con A en todos los puntos y no se dibuja.}
```
- **Por qué:** M2: reinterpretar D y G.
- **Fuente:** tabla M2.1, columna «temprana %» (D y G: 91.25, 88.75, 90.50 y 90.48; las demás: 78.0, 83.0, 82.5 y 90.0).
- **Cruces:** absorbe claridad S13 en 05:75-76 («no alteran las consultas») y 3.3 en 05:74.

### M2.4 Párrafo de B1
- **Dónde:** `05:59-67`
- **Viejo:**
```latex
\paragraph{B1 es la corrección que no se puede sustituir.}
La lectura cruda del directorio (A) pierde 7.8 puntos frente a la lectura B1 (85.2\%
frente a 93.0\%).
Ninguna de las condiciones que actúan sobre los síntomas del sesgo y no sobre su causa
(B2, C, D, E32, E64) alcanza a B1; la más cercana, B2, queda a 1.2 puntos.
La combinación G supera a B1 por medio punto (93.5\% frente a 93.0\%), menos de lo que
G varía entre semillas (de 93.0 a 93.7\%; B1 da lo mismo con todas): una vez que la
puntuación mide evidencia por registro y no evidencia total, balancear las consultas y
depurar el vocabulario aportan poco.
```
- **Nuevo:**
```latex
\paragraph{Con $N = 400$, B1 es la mejor corrección individual.}
La lectura cruda del directorio (A) pierde 7.8 puntos frente a la lectura B1 (85.2\,\%
frente a 93.0\,\%).
Ninguna de las demás condiciones (B2, C, D, E32, E64) alcanza a B1; la más cercana, B2,
queda a 1.2 puntos.
La combinación G supera a B1 por medio punto (93.5\,\% frente a 93.0\,\%), pero se
evalúa sobre otras consultas, porque, como D, sortea consultas balanceadas de todo el
banco; sobre sus propias consultas, la fase madura supera a la temprana en 3.0 puntos
con B1 y en 3.05 con G.
G varía entre semillas, de 93.0 a 93.7\,\%, porque la semilla cambia su sorteo; B1 da
93.0\,\% con todas, porque en esa condición la semilla no cambia nada.
Una vez que la puntuación mide evidencia por registro y no evidencia total, balancear las
consultas y depurar el vocabulario aportan poco.
```
- **Por qué:** M2: G y B1 se comparan sobre consultas distintas, y «B1 da lo mismo con todas» no es estabilidad sino que la semilla no interviene.
- **Fuente:** tabla M2.1 (B1 +3.00 y G +3.05 con $N = 400$); tabla M2.2 (B1 sin variación; G con 53 de 108 columnas que varían). El 93.0–93.7 de G lo comprobó claridad S39 en el CSV.
- **Cruces:** absorbe claridad S15 (título), S14 en 05:62-63 y S39.

### M2.5 Discusión de B1
- **Dónde:** `06:55-57`
- **Viejo:**
```latex
Las condiciones que actúan sobre los síntomas (B2, C, D, E) quedan por debajo de B1, y
la combinación G, que suma correcciones a B1, gana solo medio punto, dentro del ruido
(Tabla~\ref{tab:calibracion}).
```
- **Nuevo:**
```latex
Con $N = 400$, las demás condiciones (B2, C, D, E32, E64) quedan por debajo de B1, y la
combinación G, que suma correcciones a B1, gana medio punto sobre otras consultas, más
fáciles; sobre las suyas, suma a la fase temprana lo mismo que B1, unos 3 puntos
(Sección~\ref{sec:calibracion}).
```
- **Por qué:** M2. «Dentro del ruido» venía de comparar con la variación entre semillas, que en G sale del sorteo.
- **Fuente:** tabla M2.1.
- **Cruces:** absorbe claridad S14 en 06:55-57. Queda justo después de estructura 5.5 (06:51-54).

### M2.6 Pie de la Figura 5
- **Dónde:** `05:86-90`
- **Viejo:**
```latex
    \caption{Precisión madura (\%) por condición de la Tabla~\ref{tab:calibracion} y
    número de consultas de formación $N$ (mismos datos que la
    Figura~\ref{fig:mature-vs-n}).
    Hasta $N = 200$, A, C, E32, E64 y F quedan entre 66 y 77\%, y B1 sube de 78 a 88\%
    (93\% con $N = 400$); D y G pasan del 86\% en todo el rango.}
```
- **Nuevo:**
```latex
    \caption{Precisión madura (\%) por condición de la Tabla~\ref{tab:calibracion} y
    número de consultas de formación $N$ (mismos datos que la
    Figura~\ref{fig:mature-vs-n}).
    Hasta $N = 200$, A, C, E32, E64 y F quedan entre 66 y 77\,\%, y B1 sube de 78 a
    88\,\% (93\,\% con $N = 400$); D y G, evaluadas sobre un sorteo balanceado con
    consultas más fáciles, pasan del 86\,\% en todo el rango.}
```
- **Por qué:** M2.
- **Fuente:** tabla M2.1 (madura de D y G, mínimo 86.46 con $N = 100$).

### M2.7 Protocolo completo y curva de formación
- **Dónde:** `05:148-150`
- **Viejo:**
```latex
Mide lo mismo que la calibración con el protocolo del sistema, pero el directorio se
forma con 10 consultas por dominio en lugar de unas 50; por eso su precisión madura es
menor que la del banco completo (Sección~\ref{sec:formacion}).
```
- **Nuevo:**
```latex
Mide lo mismo que la calibración con el protocolo del sistema, pero el directorio se
forma con 10 consultas por dominio en lugar de unas 50, y las consultas evaluadas son
las 80 primeras del banco, que traen el nombre de su clase en el 13.8\,\% de los casos,
frente al 49.8\,\% de las 400 de la calibración (Sección~\ref{sec:banco}).
Por eso su precisión madura no se compara directamente con la del banco completo
(Sección~\ref{sec:formacion}).
```
- **Dónde:** `05:256-260`
- **Viejo:**
```latex
\paragraph{Con 10 consultas por clase, ninguna condición llega al 90\%.}
Todas convergen al 81.2\% final.
Con ocho dominios y consultas que comparten léxico, 10 interacciones por dominio no
acumulan suficiente evidencia distintiva; el mismo protocolo con el banco completo
alcanza el 93.0\% (Sección~\ref{sec:calibracion}).
```
- **Nuevo:**
```latex
\paragraph{Con 10 consultas por clase, ninguna condición llega al 90\,\%.}
Todas convergen al 81.2\,\% final, la misma precisión que da la fase temprana sobre
estas 80 consultas (Sección~\ref{sec:proto-completo}).
La calibración llega al 93.0\,\% con las 400 primeras consultas, pero sobre otras
consultas, más fáciles, en las que la fase temprana ya acierta el 90.0\,\%
(Sección~\ref{sec:calibracion}).
Cuánto se debe a formar el directorio con más interacciones lo separa la calibración
con un conjunto fijo [PENDIENTE: calibración con conjunto fijo].
```
- **Por qué:** M2: retirar «hace falta el banco completo» en sus dos formas de 05.
- **Fuente:** 13.8 % (11 de 80) y 49.8 %: tabla M3.1, con plural; 81.2 % temprana y madura: `05:153` y `05:158`; 90.0 %: tabla M2.1.

### M2.8 Organización
- **Dónde:** `04:266-267`
- **Viejo:**
```latex
El estudio principal es la calibración del directorio (9 condiciones de lectura
$\times$ $N \in \{50, 100, 200, 400\}$ consultas $\times$ 5 semillas).
```
- **Nuevo:**
```latex
El estudio principal es la calibración del directorio (9 condiciones de calibración
$\times$ $N \in \{50, 100, 200, 400\}$ consultas $\times$ 5 semillas, que solo cambian
el resultado en D y G).
```
- **Fuente:** tabla M2.2.
- **Cruces:** absorbe la sustitución de claridad S13 en 04:266; la cifra «5» se queda porque es factor de un producto (claridad 3.3).

### M2.9 Conclusiones: resultados principales
- **Dónde:** `07:12-16`
- **Viejo:**
```latex
\paragraph{Resultados principales.}
Sobre el banco de 411 consultas ($N = 400$, 5 semillas), el sistema alcanza una
\textbf{precisión temprana del 90.0\%} y una \textbf{precisión madura del 93.0\%} con
la lectura B1 del directorio, con una fidelidad temprana-madura del 95.8\%; la fase
madura se evalúa sobre las consultas que formaron el directorio.
```
- **Nuevo:**
```latex
\paragraph{Resultados principales.}
Sobre el banco de 411 consultas ($N = 400$), el sistema alcanza una
\textbf{precisión temprana del 90.0\,\%} y una \textbf{precisión madura del 93.0\,\%}
con la lectura normalizada del directorio, con una concordancia temprana-madura del
95.8\,\%; la fase madura se evalúa sobre las consultas que formaron el directorio, y
sobre ellas el directorio suma 3.0 puntos a la fase temprana.
```
- **Por qué:** M2. Las semillas salen porque con la lectura normalizada no cambian nada.
- **Fuente:** tabla M2.1 (B1, $N = 400$: +3.00) y tabla M2.2.
- **Cruces:** absorbe claridad S10 en 07:15 («concordancia»), 3.8 («lectura normalizada»), 3.3 y 3.1. Queda justo antes de estructura 9.3.

---

## M3. Composición del banco y de la partición reservada

Las cifras de 05:28-29 y 07:17-18 (por qué el 97.0 % de las reservadas supera al 93.0 %) ya están en estructura 4.2 y 9.3.

### M3.1 Alineación del banco con el vocabulario
- **Dónde:** `04:170-172`
- **Viejo:**
```latex
Se construyó un banco de \textbf{411 consultas} en lenguaje natural con su clase
correcta conocida, aproximadamente 50 por dominio,
presentadas de forma intercalada.
```
- **Nuevo:**
```latex
Se construyó un banco de \textbf{411 consultas} en lenguaje natural con su clase
correcta conocida, aproximadamente 50 por dominio,
presentadas de forma intercalada.
El banco está alineado con el vocabulario de llenado.
De las 411 consultas, 402 contienen una palabra del vocabulario de su clase, 367 una
palabra que solo está en ese vocabulario y 208 el nombre de la clase.\footnote{Reanálisis
del banco, \texttt{results/reanalisis\_jurado/salida.md}, tabla M3.1. Una palabra cuenta
si aparece como palabra de la consulta, también en plural; el sistema tokeniza con
spaCy, así que la cuenta es una aproximación.}
```
- **Por qué:** M3: 399 de 411 consultas tienen una palabra del vocabulario de su clase y 362 una exclusiva (cuenta exacta del dictamen).
- **Fuente:** tabla M3.1, «con plural»: 402 (97.8 %), 367 (89.3 %) y 208 (50.6 %). Se usa la cuenta con plural para que coincida con el 87.7 % de las reservadas; la exacta da 399, 362 y 203.
- **Nota:** el dictamen pregunta quién escribió el banco y con qué acceso al vocabulario. El repositorio no lo dice (`src/eval_bank.py` solo trae las listas); lo tiene que contestar el autor (índice, decisiones).

### M3.2 La partición reservada
- **Dónde:** `04:182-189`
- **Viejo:**
```latex
Otros tres bancos se usan una sola vez: las 16 consultas de la reproducción por etapas
(\texttt{TEST\_QUERIES}, 2 por dominio) y 12 consultas representables que describen
objetos fuera de los ocho dominios, ambas en la Sección~\ref{sec:proto-completo}; y, en
la comparación con una sola EHAM (Sección~\ref{sec:eham-unica}), una partición del
banco (las primeras 30 consultas de cada clase forman los directorios y las 171
restantes quedan reservadas para evaluar) más 40 consultas fuera de dominio: las 12
anteriores y 28 de objetos y escenas de categorías ausentes de ETH-80, sin palabras
del vocabulario de etiquetas.
```
- **Nuevo:**
```latex
Otros tres bancos se usan una sola vez.
La Sección~\ref{sec:proto-completo} usa las 16 consultas de referencia del sistema (dos
por dominio) y 12 consultas representables que describen objetos fuera de los ocho
dominios.
La comparación con una sola EHAM (Sección~\ref{sec:eham-unica}) usa una partición del
banco, en la que las primeras 30 consultas de cada clase forman los directorios y las 171
restantes quedan reservadas para evaluar, más 40 consultas fuera de dominio: las 12
anteriores y 28 de objetos y escenas de categorías ausentes de ETH-80, sin palabras del
vocabulario de etiquetas.
Las reservadas son la cola de la lista de cada clase, no una muestra al azar, y no
representan al banco.
El 87.7\,\% de ellas trae el nombre de su clase, frente al 24.2\,\% de las 240 de
formación, el 13.8\,\% de las 80 primeras y el 49.8\,\% de las 400 de la
calibración.\footnote{Reanálisis del banco, tabla M3.1.}
```
- **Por qué:** M3: las reservadas son la cola de cada lista y por eso el 97.0 % fuera de muestra supera al 93.0 % dentro de muestra (E2 del dictamen de estilo).
- **Fuente:** tabla M3.1, con plural (150 de 171, 58 de 240, 11 de 80 y 199 de 400); que las reservadas son exactamente la cola de cada lista: encabezado de M3 en `salida.md` («True»).
- **Cruces:** absorbe claridad S46 en 04:182-189 (párrafo partido, sin `TEST\_QUERIES`, «dos por dominio»). Queda después de estructura 2.4 (04:173-178), sin tocarlo.

---

## M4. Objetos nuevos: el codificador vio todos los objetos

### M4.1 Experimento 16
- **Dónde:** `05:439-443`
- **Viejo:**
```latex
La generalización a objetos nuevos se midió aparte (experimento 16), con una validación
\textit{leave-one-object-out} de diez pliegues: en cada pliegue, el contenido y la fase A
se construyen con nueve objetos por clase, y sobre los mismos modelos se evalúan las 41
vistas del objeto reservado de cada clase y 41 vistas no usadas de los objetos que sí
contribuyeron.
```
- **Nuevo:**
```latex
La generalización a objetos nuevos se midió aparte (experimento 16), con una validación
\textit{leave-one-object-out} de diez pliegues.
En cada pliegue, el contenido y el directorio visual se construyen con nueve objetos por
clase, y sobre los mismos modelos se evalúan las 41 vistas del objeto reservado de cada
clase y 41 vistas no usadas de los objetos que sí contribuyeron.
El codificador, en cambio, es el mismo en todos los pliegues y se entrenó con las 328
imágenes de entrenamiento de cada clase, que incluyen vistas de los diez objetos
(Sección~\ref{sec:percepcion}); con un codificador reentrenado sin el objeto reservado,
la cobertura de punta a punta con objetos nuevos es del
[PENDIENTE: exp16 con codificador por pliegue].
```
- **Por qué:** M4: exp16 no reentrena el codificador por pliegue, así que el objeto «nuevo» lo vio el codificador. La propuesta de estructura cubre la supervisión del codificador (limitación (k)), no esta fuga.
- **Fuente:** `run_experiment16_leave_object_out.py:68` (`load_encoder()` una vez para todos los pliegues); 328 por clase: `04:20`; los diez objetos aportan vistas a entrenamiento y prueba: `04:21-22`; 2624 = 8 × 328 imágenes de entrenamiento del codificador: `tab:costo`.
- **Cruces:** absorbe claridad S12 en 05:440 («el contenido y el directorio visual se construyen») y la fila `05:440` de claridad 3.7.
- **Nota:** si la cifra por pliegue cambia, también cambian el 89.2 % y la brecha de 6.3 puntos en `05:444-446`, `06:293`, `07:27-29` y `07:48`, en el resumen (estructura 9.1) y en la limitación (k) (estructura 3.3).

---

## M5. Decisiones tomadas después de ver los datos

### M5.1 Resultados fuera de dominio
- **Dónde:** `05:548-551`
- **Viejo:**
```latex
\paragraph{Fuera de dominio.}
La EHAM única acepta más consultas fuera de dominio a medida que crece el contenido; el
oráculo acepta 2 de 40 en todos los cortes, y el protocolo 4, que la doble compuerta de
contenido (el módulo destino debe contener la pista) baja a 2.
```
- **Nuevo:**
```latex
\paragraph{Fuera de dominio.}
La EHAM única acepta más consultas fuera de dominio a medida que crece el contenido (2,
2, 5 y 8 de 40 con 25, 50, 100 y 200 imágenes por clase); el oráculo acepta 2 de 40 en
todos los cortes, y el protocolo 4, que la doble compuerta de contenido (el módulo
destino debe contener la pista) baja a 2 [PENDIENTE: exp11 corregido].
La doble compuerta se agregó después de ver, en estas mismas 40 consultas, las dos que
el directorio enviaba a un módulo que no las contiene (limitación (g)).
Con McNemar exacto, la diferencia entre la EHAM única y el protocolo con doble compuerta
solo es significativa con 200 imágenes por clase ($p = 0.031$, con seis consultas que
acepta solo la EHAM única y ninguna que acepte solo el protocolo); con 100, $p = 0.25$,
y con 25 y 50, $p = 1$.
Sin la segunda compuerta, con 200 imágenes por clase, $p = 0.22$
[PENDIENTE: exp11 corregido].
```
- **Por qué:** M5: el $p \approx 0.03$ del dictamen vale solo con $N = 200$ y depende de una compuerta decidida con estos datos.
- **Fuente:**
  - 2 / 2 / 5 / 8 aceptadas por la EHAM única, 4 y 2 del protocolo, $p$ por corte (1.000, 1.000, 0.250, 0.031) y sin la segunda compuerta (0.500, 0.500, 1.000, 0.219): tabla M5.1.
  - Orden de las decisiones: `4732739` (21 sep 2026, 18:16; exp11 fuera de dominio con 40 consultas: «el directorio deja pasar dos que el contenido rechaza») y `ddddeff` (21 sep 2026, 22:03; «Doble compuerta de contenido en la fase madura textual»). Los dos commits están en la historia de `una-hetero`.

### M5.2 Discusión: fidelidad y fuera de dominio
- **Dónde:** `06:183-187`
- **Viejo:**
```latex
Se ve en la fidelidad: la respuesta de la EHAM única queda más lejos de la instancia
real más cercana en todos los cortes (de 4.6 a 6.2 más que el oráculo), sin tendencia
con el contenido.
Y se ve fuera de dominio: la EHAM única acepta más cuanto más contiene (de 2 a 8 de 40
consultas), y el protocolo con doble compuerta acepta 2 en todos los cortes.
```
- **Nuevo:**
```latex
Se ve en la fidelidad.
La respuesta de la EHAM única queda más lejos de la instancia real más cercana de la
clase de la consulta en todos los cortes (de 4.6 a 6.2 más que el oráculo), sin
tendencia con el contenido.
Y se ve fuera de dominio, donde la EHAM única acepta más cuanto más contiene (de 2 a 8
de 40 consultas) y el protocolo con doble compuerta acepta 2 en todos los cortes; la
diferencia solo es significativa con 200 imágenes por clase ($p = 0.031$), y la segunda
compuerta se decidió después de ver estas consultas (limitación (g))
[PENDIENTE: exp11 corregido].
```
- **Por qué:** M5 y la distancia de M1.7.
- **Fuente:** tabla M5.1; 4.6–6.2 es la EHAM única contra el oráculo (`05:533-535`) y sigue valiendo.
- **Cruces:** los dos dos puntos (06:183 y 06:186) estaban en la lista de claridad Parte 4, punto 7. Queda justo después de estructura 7.3 (06:178-182).

### M5.3 Limitación (a)
- **Dónde:** `06:208-220`
- **Viejo:**
```latex
\paragraph{(a) Fuga de consultas fuera de dominio en el hemisferio textual.}
Una consulta fuera de dominio que comparte tokens con etiquetas legítimas pasa la
contención textual y llega a algún módulo: la sonda de rechazo deja pasar 2 de 12
(Sección~\ref{sec:proto-completo}), y en el banco de 40 de la comparación con la EHAM
única el directorio acepta 4, dos de ellas (\emph{piano}, \emph{thunderstorm}) hacia un
módulo que no las contiene.
La doble compuerta de contenido (el destino debe contener la consulta, no solo figurar
en el directorio) detiene esas dos y deja al protocolo en 2 de 40 en los cuatro cortes,
tantas como el oráculo; sobre las 171 consultas reservadas no quita ninguna respuesta,
porque las que rechaza (1.5\,\% con 200 imágenes por clase, 2.1\,\% con 25) eran
enrutamientos equivocados que el destino tampoco respondía.
Las dos que quedan las contiene el destino, y ninguna compuerta de contención las
separa de una consulta legítima.
```
- **Nuevo:**
```latex
\paragraph{(a) Fuga de consultas fuera de dominio en el hemisferio textual.}
Una consulta fuera de dominio que comparte tokens con etiquetas legítimas pasa la
contención textual y llega a algún módulo.
La sonda de rechazo deja pasar 2 de 12 (Sección~\ref{sec:proto-completo}), y en el
banco de 40 de la comparación con la EHAM única el directorio acepta 4, dos de ellas
(\emph{piano}, \emph{thunderstorm}) hacia un módulo que no las contiene.
La doble compuerta de contenido (el destino debe contener la consulta, no solo figurar
en el directorio), que se agregó después de ver esas dos fugas, las detiene y deja al
protocolo en 2 de 40 en los cuatro cortes, tantas como el oráculo; sobre las 171
consultas reservadas no quita ninguna respuesta, porque las que rechaza (1.5\,\% con
200 imágenes por clase, 2.1\,\% con 25) eran falsos enrutamientos que el destino
tampoco respondía [PENDIENTE: exp11 corregido].
Las dos que quedan las contiene el destino, y ninguna compuerta de contención las
separa de una consulta legítima.
```
- **Por qué:** M5: declarar que la compuerta es posterior a ver esas fugas.
- **Fuente:** commits `4732739` y `ddddeff` (M5.1); *piano* y *thunderstorm* son las dos que acepta el protocolo sin la segunda compuerta y no con ella (lista bajo la tabla M5.1, con $N = 200$).
- **Cruces:** absorbe la fila `06:210` de claridad 3.7 y «enrutamientos equivocados» → «falsos enrutamientos» (claridad 1.1, aplicada también a 06:218).

### M5.4 Limitación (g)
- **Dónde:** `06:302-313`
- **Viejo:**
```latex
\paragraph{(g) Selección de modelo e hiperparámetro sobre el conjunto de prueba.}
Dos elementos del protocolo se eligieron mirando el conjunto de prueba, por ausencia
de una partición de validación separada: el punto de control del codificador (RMSE
mínimo sobre el conjunto de prueba entre cinco candidatos, Sección~\ref{sec:percepcion})
y las 16 variantes del llenado, adoptadas después de ver el barrido de variantes
(experimento 13), que mide sobre las 656 imágenes de prueba (16 es el mayor valor
probado, no un óptimo ajustado).
La lectura del directorio visual no tiene tolerancia que ajustar ($\xi = 0$,
limitación (b)).
Ambas selecciones son de alcance acotado y ninguna introduce un mecanismo ajeno a las
memorias, pero pueden inflar las cifras visuales reportadas; la corrección (una
partición de validación aparte) es directa y queda pendiente.
```
- **Nuevo:**
```latex
\paragraph{(g) Decisiones tomadas con los datos de evaluación.}
No hay una partición de validación separada, y varias decisiones del protocolo se
tomaron con información de los mismos datos con que se reportan los resultados:
\begin{itemize}
    \item el punto de control del codificador, por RMSE mínimo sobre el conjunto de
    prueba entre cinco candidatos (Sección~\ref{sec:percepcion});
    \item las 16 variantes del llenado, adoptadas después de ver el barrido de variantes
    del experimento 13, que mide sobre las 656 imágenes de prueba (16 es el mayor valor
    probado, no un óptimo ajustado);
    \item la lectura B1 y la regla de rescate léxico, elegidas sobre el mismo banco de
    consultas con que se evalúan (Secciones~\ref{sec:calibracion}
    y~\ref{sec:pipeline-semantico});
    \item las 200 imágenes de llenado por clase, elegidas con la precisión temprana sobre
    las 80 consultas (Sección~\ref{sec:capacidad});
    \item la doble compuerta de contenido, agregada después de ver dos fugas en las
    mismas 40 consultas fuera de dominio con que se mide (limitación (a)).
\end{itemize}
La lectura del directorio visual no tiene tolerancia que ajustar ($\xi = 0$,
limitación (b)).
Ninguna de estas decisiones introduce un mecanismo ajeno a las memorias, pero pueden
inflar las cifras reportadas.
La corrección es separar una partición de validación y confirmar las cifras finales con
bancos nuevos que no se hayan usado para decidir nada; queda pendiente.
```
- **Por qué:** M5: el dictamen enumera el punto de control, las 16 variantes, B1, el rescate léxico, $N = 200$ y la doble compuerta.
- **Fuente:** punto de control: `04:139-142`; 16 variantes: `06:306-308`; B1 sobre el banco de la calibración: `05:13-23`; rescate sobre el banco completo: `04:101-103`; 200 imágenes por la precisión temprana sobre 80 consultas: `05:290-291` y `05:323`; compuerta: commits de M5.1.
- **Cruces:** absorbe claridad S67 en 06:303 («mirando» → «con información de»). Las referencias a la limitación (g) en `04:142` y `07:88` siguen valiendo, porque la letra no cambia.

### M5.5 Trabajo futuro, punto 1
- **Dónde:** `07:88-90`
- **Viejo:**
```latex
    \item \textbf{Partición de validación} (limitación (g)): elegir el punto de control
    del codificador y el número de variantes sin mirar el conjunto de prueba, y volver a
    medir el hemisferio visual con esa partición.
```
- **Nuevo:**
```latex
    \item \textbf{Partición de validación y bancos nuevos} (limitación (g)): elegir el
    punto de control del codificador, el número de variantes, la lectura del directorio y
    las compuertas sin usar el conjunto de prueba, y confirmar las cifras de texto, de
    imagen y fuera de dominio con bancos nuevos, escritos por terceros.
```
- **Por qué:** M5 («confirmar al final con bancos nuevos e intactos») y M3 («idealmente, un banco nuevo escrito por terceros»).
- **Cruces:** absorbe claridad S67 en 07:89 («sin mirar» → «sin usar»).

---

## Menores

### Me.1 Evocación: criterio estricto y azar
- **Dónde:** `05:368-372`
- **Viejo:**
```latex
\paragraph{Evocación de dominio: imagen $\to$ palabras.}
Sobre las primeras 15 imágenes de prueba de cada clase que el enrutamiento acepta (116 de
120), la evocación inversa desde el módulo destino (recuperación $\beta$ desde el
latente, decodificada por similitud coseno top-3) produjo al menos una etiqueta del
vocabulario de la clase real en 113 de 116 (97.4\%) de los casos.
```
- **Nuevo:**
```latex
\paragraph{Evocación de dominio: imagen $\to$ palabras.}
Sobre las primeras 15 imágenes de prueba de cada clase que el enrutamiento acepta (116 de
120), la evocación inversa desde el módulo destino (recuperación $\beta$ desde el
latente, decodificada por similitud coseno top-3) produjo al menos una etiqueta del
vocabulario de la clase real en 113 de los 116 casos (97.4\,\%).
La medida es laxa y casi la implica el enrutamiento.
Cuenta como acierto una palabra que la clase comparte con otras, y con el especialista
correcto casi no falla.
En la comparación con una sola EHAM, con el especialista elegido por la clase real, la
evocación acierta el 100\,\% de las imágenes respondidas en los cuatro cortes, y entre
el 98.2 y el 100.0\,\% con un criterio estricto, que solo cuenta las palabras exclusivas
de la clase.
Tres palabras tomadas al azar de los ocho vocabularios (159 palabras distintas) aciertan
el 34.8\,\% con el criterio laxo y el 32.1\,\% con el estricto.
```
- **Por qué:** menor del dictamen: la métrica es laxa (top-3, palabras compartidas) y casi queda implicada por el enrutamiento; conviene la versión estricta y el nivel de azar.
- **Fuente:** azar laxo 34.8 % y estricto 32.1 % (media): tabla E.1; oráculo, laxo 100.0 en los cuatro cortes y estricto 100.0, 98.8, 98.5 y 98.2 sobre las respondidas: tabla E.2; 159 palabras: encabezado de E.1 y `03:488`.
- **Cruces:** absorbe la fila `05:372` de claridad S62 («113 de los 116 casos (97.4 %)»).
- **Nota:** la versión estricta sobre estas 116 imágenes no se puede calcular con lo versionado, porque el log de la etapa 7 no guarda las etiquetas de cada imagen (nota bajo E.1). Pedirla es volver a correr la etapa 7 guardándolas (índice, decisiones).

### Me.2 Conclusiones: evocación
- **Dónde:** `07:25-26`
- **Viejo:**
```latex
Sobre las primeras 15 imágenes de prueba de cada clase (116 aceptadas), la evocación de
dominio es del \textbf{97.4\%}.
```
- **Nuevo:**
```latex
Sobre las primeras 15 imágenes de prueba de cada clase (116 aceptadas), la evocación de
dominio es del \textbf{97.4\,\%}, frente a un azar del 34.8\,\%.
```
- **Fuente:** tabla E.1.

### Me.3 Lo que deja pasar el umbral de energía
- **Dónde:** `06:254-257`
- **Viejo:**
```latex
El umbral de energía (Sección~\ref{sec:percepcion}) cierra el 90\,\% de la fuga
(experimento 14): 137 de las 152 entradas degeneradas aceptadas por una clase ajena caen
bajo $\tau$ (grises de 104 a 168, contrastes $\leq 0.2$ y desenfoques fuertes: todos
los de radio $\geq 12$ y buena parte de los menores).
```
- **Nuevo:**
```latex
El umbral de energía (Sección~\ref{sec:percepcion}) cierra el 90\,\% de la fuga entre
clases (experimento 14), porque 137 de las 152 entradas degeneradas aceptadas por una
clase ajena caen bajo $\tau$ (grises de 104 a 168, contrastes $\leq 0.2$ y desenfoques
fuertes: todos los de radio $\geq 12$ y buena parte de los menores).
Del banco de 231 entradas degeneradas, la memoria acepta 180, y tras $\tau$ siguen
aceptadas 33: las 15 que acepta una clase ajena y 18 que solo acepta su propia clase.
```
- **Por qué:** menor del dictamen: junto a «cierra el 90 %», dar el total.
- **Fuente:** tabla X.1, fila «norma»: 231, 180, 33, 15, 18, 152 y 137.
- **Cruces:** el dos puntos de 06:255 estaba en la lista de claridad Parte 4, punto 7. Queda justo después de la fila `06:252–253` de claridad 3.7, que no se toca.

### Me.4 Versiones que faltan
- **Dónde:** `04:15`
- **Viejo:**
```latex
Se utilizó el conjunto de datos ETH-80~\cite{leibe2003eth80} completo, con sus
```
- **Nuevo:**
```latex
Se utilizó el conjunto de datos ETH-80~\cite{leibe2003eth80} completo, en su versión
\texttt{eth80-cropped-close128}, con sus
```
- **Dónde:** `04:79-80`
- **Viejo:**
```latex
Cada etiqueta del vocabulario se representó con su vector crudo de 300 dimensiones del
modelo fastText preentrenado~\cite{bojanowski2017fasttext}.
```
- **Nuevo:**
```latex
Cada etiqueta del vocabulario se representó con su vector crudo de 300 dimensiones del
modelo fastText preentrenado en inglés con subpalabras
(\texttt{fasttext-wiki-news-subwords-300})~\cite{bojanowski2017fasttext}.
```
- **Dónde:** `04:90`
- **Viejo:**
```latex
Las consultas en lenguaje natural se procesan con spaCy~\cite{honnibal2020spacy}: se
```
- **Nuevo:**
```latex
Las consultas en lenguaje natural se procesan con spaCy~3.8.14 y su modelo
\texttt{en\_core\_web\_sm}~3.8.0~\cite{honnibal2020spacy}: se
```
- **Por qué:** menor del dictamen («Versiones que faltan»).
- **Fuente:**
  - ETH-80: `src/stage1_dataset.py:15-16` (`eth80-cropped-close128.tgz`).
  - fastText: `src/stage4_fasttext.py:3` y `:23-24` (`fasttext-wiki-news-subwords-300.gz`); «EN» en `src/stage3_conceptnet.py:232`.
  - spaCy: `requirements.txt` fija `spacy==3.8.14`; el modelo `en_core_web_sm` (`src/stage6_interaction.py:52`) no está fijado, y la versión instalada en el entorno es la 3.8.0 (`en_core_web_sm-3.8.0.dist-info` en `.venv`). Conviene fijarla en `requirements.txt`.
- **Nota:** el commit de `hetero_lib`, que el dictamen también pide, no entra aquí (índice).

---

## Lo que el dictamen de metodología pide y queda fuera de las tres propuestas

| Punto | Qué pide | Dónde queda |
|---|---|---|
| M3 | líneas base léxica, de coseno de fastText y de tabla de conteos | no están entre los experimentos en curso; decisión del autor en el índice |
| M3 | partición reservada por sorteo estratificado y banco escrito por terceros | decisión del autor; M3.2 declara la composición y M5.5 lo deja como trabajo futuro |
| M4 | reportar el experimento 19 (ImageNet + PCA) | decisión del autor; la nota de estructura 3.3 lo menciona |
| M6 | modelos publicados con sus hashes, réplica desde cero y README raíz | no es texto de la tesis. El log de la etapa 7 ya está versionado (`9737e49`) |
| menor | $\iota = 0.25$ rinde más y se elige $\iota = 0$; 05:217-223 lee diferencias de una o dos consultas de 80 | sin propuesta |
| menor | F ≡ A y G = D + B1: son siete condiciones efectivas | sin propuesta; M2.1 dice que siete condiciones evalúan las mismas consultas |
| menor | 05:579 «todas las cifras son de una sola memoria» | claridad S48 la quita; queda comprobar si exp10 y exp15 se volvieron a correr |
| menor | línea de control del README de exp13; llenado distinto del oficial | no es texto de la tesis |
| menor | lesión: mismo daño en memorias de tamaño distinto, lectura de la primera coordenada, fracciones agregadas tras el piloto | sin propuesta |
| menor | imagen → texto con coberturas distintas; costo del rescate con sus dos vías; concordancia que cuenta un rechazo doble como coincidencia; «ideal 12.5 %» frente a la proporción real | sin propuesta |
| menor | commit de `hetero_lib` | sin propuesta |
