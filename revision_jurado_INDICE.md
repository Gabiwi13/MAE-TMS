# Índice de la ronda de redacción tras la lectura de jurado

## Estado

Consolidado y pendiente de aprobación del autor. No se aplicó nada a la tesis, no hay commit y no se corrió ningún experimento. La base es `una-hetero` en `df2f893`; el `.tex8` no cambió desde `62995a8`.

| Archivo | Qué es | Atiende |
|---|---|---|
| `revision_jurado_estructura_prosa.md` | propuesta de la nube, con las correcciones y los textos combinados de esta consolidación | dictamen de Wegner (M1–M11), estilo E1, E2, E6, E7 y 5.6, metodología M7 |
| `revision_jurado_metodologia_prosa.md` | propuesta nueva de esta consolidación | metodología M1, M2, M3, M4 (fuga de exp16), M5 y menores |
| `revision_jurado_claridad_prosa.md` | propuesta de la nube, con las notas de lo que absorbieron las otras dos | estilo C1–C12, 5.1–5.5 y 5.7 |
| `results/reanalisis_jurado/salida.md` | reanálisis verificado en esta máquina | fuente de las cifras nuevas (tablas M1.1 a X.2) |

Los scripts de cotejo quedaron fuera del repositorio, en la carpeta temporal de la sesión.

## Orden de aplicación

1. **Estructura**, completa. Reemplaza cinco bloques enteros (resumen, contribuciones, 2.3, 6.4 y 6.5) y agrega 2.4, la tabla de 2.3 y la limitación (k). Va primero porque, si se aplicara antes la de claridad, sus «Viejo» de bloque entero dejarían de coincidir.
2. **Metodología**, completa. No comparte ningún pasaje con la de estructura, solo bordes (M2.2 va después del texto de 4.2; M1.6 sigue la frase de 7.7), así que su lugar respecto de la anterior no cambia el resultado.
3. **Claridad, Parte 2**, sin los puntos o fragmentos marcados «Consolidación: absorbido». Sus «Viejo» siguen intactos, porque ninguno de los que quedan cae en un pasaje ya reemplazado.
4. **Claridad, Parte 3** (reglas mecánicas), por búsqueda en todo el texto y no por número de línea. En los textos combinados ya están aplicadas.
5. **Pasada de forma** sobre los pasajes de estructura que no cruzan con claridad: dos puntos explicativos y antítesis con el criterio de claridad 3.7 (decisión 7).
6. **Bibliografía:** las 35 entradas nuevas de estructura, más lo que diga la decisión 9.
7. **Compilar** (pdflatex, bibtex, pdflatex dos veces) y revisar referencias y citas indefinidas, cajas desbordadas y número de páginas.
8. **Llenar los marcadores** a medida que lleguen los experimentos (sección «Marcadores»).

## Conteo de puntos

| Propuesta | Puntos | Pasajes con «Viejo» | Inserciones sin «Viejo» | Líneas LaTeX nuevas |
|---|---|---|---|---|
| Estructura | 43 subsecciones (4 solo remiten a otras) | 40: 35 bloques y 5 bloques enteros, cotejados por su primera y última línea (45 fragmentos) | 3: limitación (k), trabajo futuro nuevo y 2.4 | 790, que reemplazan 416 |
| Metodología | 28 (M1: 7, M2: 9, M3: 2, M4: 1, M5: 5, menores: 4) | 31 | 1 (M2.2) | 291, que reemplazan 173 |
| Claridad | 71 en la Parte 2 (S1–S70 y S36b) y 8 reglas en la Parte 3 | 183 fragmentos (cada celda de tabla cuenta) y 32 sustituciones «X» → «Y» | — | — |

De la de claridad, 22 puntos y 13 filas de tabla quedan absorbidos, total o parcialmente, en textos combinados de las otras dos.

## Los «Viejo» que no coinciden

El cotejo, con espacios normalizados y nada más, dio:
- **Estructura:** 45 de 45 coinciden, en las líneas citadas.
- **Claridad:** 183 de 183 coinciden, en las líneas citadas. De las 32 sustituciones «X» → «Y» del resto del texto, una no coincidía: claridad 3.3 decía «Los 3 vecinos», con mayúscula, y en 03:487 dice «los 3 vecinos». Ya está corregida en el archivo.
- **Metodología:** 31 de 31 coinciden.

Una ambigüedad sin error: en S51, «En la línea siguiente de la tabla, «instancia real más cercana» → …» describe el contenido nuevo de 05:504, cuyo texto actual es «real más cercana». Ya no importa, porque S51 queda absorbido en M1.3.

## Cruces resueltos

En el contenido manda la propuesta de estructura (o la de metodología, en sus pasajes) y en la forma la de claridad. En todos los cruces se pudo combinar: el texto combinado está en el punto de estructura o de metodología, con una línea **Consolidación** que dice qué absorbe, y la propuesta de claridad lo marca como absorbido.

**Estructura × claridad (16 pasajes):**

| Pasaje | Estructura | Claridad absorbida |
|---|---|---|
| main:57-104, resumen | 9.1 (y 1.1) | S6, S43, 3.3 («5 semillas»), 3.4 («$N{=}400$»), «mecanismos» y «enrutamientos falsos» (1.1), 3.7 (main:58) |
| 01:69-114, contribuciones | 9.2 | S1, S8, S22 (01:95), S55 (01:103), fila 01:92 de 3.7, S13 (01:107), «nativos» (3.6), `\,\%` |
| 02:268-311, sección 2.3 | 2.1 | S68 (02:302-303), «lectura B1» en la tabla, «metadirectorio» (Parte 4, punto 16) |
| 03:70-71 | 4.1 | notación $M^{\mathrm{txt}}_{\mathrm{dir}}$ y $M^{\mathrm{vis}}_{\mathrm{dir}}$ (1.3) |
| 03:73-77 y 03:83-86 | 2.3 | notación (1.3), S22 (03:84-85), dos puntos de 03:83 |
| 03:377-381 | 1.4 | fila 03:377 de 3.7 |
| 04:173-178 | 2.4 | comillas angulares (3.2) |
| 04:218-219 | 7.4 | S3 (04:218) |
| 05:135-140 | 5.4 | filas 05:137 y 05:139-140 de 3.7 y S70; Parte 4, punto 10 |
| 06:5 y 06:8-12 | 7.1 | S63, «maquinaria» (1.1) |
| 06:78-120, discusión 6.4 | 4.4 | S65 (06:101-103), S69 (06:117-119), «releen» y «mecanismos» (Parte 4, punto 4), «fase A», ocho dos puntos |
| 06:122-171, discusión 6.5 | 6.1 | Parte 4, punto 8 («muestra… como Plaut mostró») |
| 07:17-22 | 9.3 | `\,\%` |
| 07:34-52 | 7.6 | S50, «lectura B1» (07:37), dos dos puntos |
| 07:77-83 | 9.4 | S55 (07:82), C1 (07:81), dos puntos de 07:78 |
| 2.4 nuevo (después de 02:322) | 8.1 | «lectura normalizada por conteo» (1.2); las glosas se quedan por el criterio de 3.6 |

**Metodología × claridad (20 pasajes):**

| Pasaje | Metodología | Claridad absorbida |
|---|---|---|
| 05:19-23 | M2.1 | 3.3 (05:20) |
| 05:59-67 | M2.4 | S15, S14 (05:62-63), S39 |
| 05:72-79 | M2.3 | S13 (05:75-76), 3.3 (05:74) |
| 05:368-372 | Me.1 | S62 (05:372) |
| 05:439-443 | M4.1 | S12 (05:440), fila 05:440 de 3.7 |
| 05:472-473 | M1.7 | Parte 4, punto 11 |
| 05:482-485 | M1.2 | S51 (pie), 3.3 («diez semillas») |
| 05:495-504 | M1.3 | S51 (tabla), «Brazo» → «Configuración» (3.6 y S61) |
| 05:522-530 | M1.1 | S61 (05:528) |
| 05:542-546 | M1.5 | fila 05:543 de 3.7 |
| 06:55-57 | M2.5 | S14 (06:55-57) |
| 06:183-187 | M5.2 | Parte 4, puntos 7 (06:183 y 06:186) y 11 |
| 06:189-203 | M1.4 | «exactitud» (1.1), S31 (06:195), fila 06:202 de 3.7 |
| 06:208-220 | M5.3 | fila 06:210 de 3.7, «enrutamientos equivocados» (1.1) |
| 06:254-257 | Me.3 | Parte 4, punto 7 (06:255) |
| 06:302-313 | M5.4 | S67 (06:303) |
| 04:182-189 | M3.2 | S46 (04:182-189) |
| 04:266-267 | M2.8 | S13 (04:266) |
| 07:12-16 | M2.9 | S10 (07:15), 3.3 (07:13), «lectura B1» |
| 07:88-90 | M5.5 | S67 (07:89) |

**Metodología × estructura:** ningún pasaje compartido. Hay seis bordes y tres alineaciones de contenido:
- **Bordes:** M2.2 va después de estructura 4.2; M1.6 sigue la frase de 7.7; M2.9 y Me.2 rodean a 9.3; M3.1 va antes de 2.4; M2.5 va después de 5.5, y M5.2 después de 7.3.
- **Alineaciones:**
  - estructura 4.4 y 7.6 toman la diferencia madura menos temprana de M2;
  - estructura 7.7, 9.1 y 9.2 dicen «con 200 imágenes por clase» por M5;
  - estructura 9.1 y 9.2 quitan «cinco semillas» por M2.

## Correcciones de hecho hechas en las propuestas

| Dónde | Qué decía | Qué dice ahora | Fuente |
|---|---|---|---|
| Estructura 5.3 | la información mutua entre el dominio de cada registro y «el módulo al que apunta», «donde $H(G)$ es $H_{\mathrm{dir}}$» | entre el dominio de la consulta y el ganador de la fase madura; $H(G)$ no es $H_{\mathrm{dir}}$ (2.906 frente a 2.974 bits en A con $N = 400$); se agrega el sesgo del estimador | tabla M6.1 y su nota: la cifra existente es la del ganador maduro, y la fase temprana no tiene matriz |
| Estructura 5.4 | «2.974 bits en A y 2.977 en G, el 99.1 % del máximo» | «el 99.1 y el 99.2 %» | 2.977/3 = 99.23 % (claridad Parte 4, punto 10) |
| Estructura 2.1 y 5.3 | directorio «compartido en los experimentos de texto» | perspectival también en la comparación con una sola EHAM, que es de texto; 5.3 dice «los estudios de texto que lo usan» | `04:276-281` |
| Estructura 4.4 y 7.6 | «las 12 consultas de la sonda y 40 consultas fuera de dominio», como si fueran 52 | las 40 incluyen las 12 | `04:187-188` |
| Estructura 9.2 | recuerdo «más cerca de la instancia real más cercana» | «… más cercana de la clase de la consulta» | `run_experiment9_member_loss.py:243-246`, `run_experiment11_monolithic.py:434` |
| Claridad 3.3 | «Los 3 vecinos» | «los 3 vecinos» | 03:487 |

## Marcadores

**Llenos con `results/reanalisis_jurado/salida.md`:**
- «reanálisis del banco», en estructura 4.2 y 9.3: tablas M3.1 (87.7 % de las reservadas trae el nombre de su clase, frente al 49.8 % de las 400) y M2.3 (las consultas 201–400 aciertan 195 de 200 en la fase temprana);
- «información mutua», en estructura 5.4, 5.5 y 9.4: tabla M6.1 (A 2.438 bits y 0.813; B1 2.649 y 0.883; G 2.668 y 0.889, con $N = 400$).

**Los que quedan (37 en textos LaTeX):**

| Marcador | Depende de | Dónde | Cuántos |
|---|---|---|---|
| `[PENDIENTE: exp11 corregido]` | exp11 con el brazo del protocolo corregido (directorios reiniciados entre trabajos) | estructura 4.2, 7.3, 9.1 (dos), 9.2 y 9.3; metodología M1.1 (cuatro), M1.2, M1.4 (tres), M1.5 (dos), M1.6 (tres), M5.1 (dos), M5.2 y M5.3; claridad S48 | 24 |
| `[PENDIENTE: líneas base]` | líneas base de centroide y kNN | estructura 7.1 (dos), 7.6, 7.8 y 9.1 | 5 |
| `[PENDIENTE: calibración con conjunto fijo]` | calibración con un conjunto de evaluación fijo | estructura 4.4 y 7.6; metodología M2.2 y M2.7 | 4 |
| `[PENDIENTE: codificador sin pérdida de clase]` | codificador sin pérdida de clase | estructura 3.3 (dos) y 7.6 | 3 |
| `[PENDIENTE: exp16 con codificador por pliegue]` | exp16 con el codificador reentrenado por pliegue | metodología M4.1 | 1 |

Notas sobre los marcadores:
- `exp11 corregido` va al final de la frase y cubre todas sus cifras del protocolo. Son las de la corrida actual: la frase dice lo que el reanálisis da hoy, con el empate en clase, y se confirma o se corrige. Las cifras de la EHAM única y del oráculo no llevan marcador.
- El marcador de exp16 es nuevo. Ninguna propuesta cubría que el codificador del experimento 16 vio los objetos reservados. Si la cifra cambia, hay que tocar también el 89.2 % de `05:444-446`, `06:293`, `07:27-29` y `07:48`, el del resumen (estructura 9.1) y el de la limitación (k).
- El experimento 15 (`06:221-226`, 171 reservadas) no lleva marcador. Según su código (`run_experiment15_arbiter.py`, `run_text` y `form_directories` de exp13), reinicia los directorios en cada semilla. Es una lectura del código; no lo corrí.

## Citas nuevas (estructura)

Revisión con script, sin consultar la web:
- **Forma:** las 35 entradas están bien formadas, con las llaves cerradas y los campos obligatorios de su tipo. La excepción es `mccloskey1989catastrophic`, un `@incollection` sin `publisher`, con el que BibTeX avisa.
- **Claves:** ninguna repite una de `referencias.bib`, ni hay claves repetidas entre las nuevas. Ningún DOI ni título coincide con una entrada existente.
- **Citas:** cada `\cite` de los textos nuevos de las tres propuestas tiene entrada, nueva o existente, y las 35 nuevas se citan en algún texto.
- **Estado de verificación:** las 35 lo declaran (V, V+, V parcial o combinaciones). Ninguna queda sin estado.
- **Por cotejar antes de aplicar**, según la propia propuesta:
  - la p. 186 de Wegner (1987);
  - los campos marcados «V parcial»: `austin2003transactive`, `palazzolo2006coevolution` y `crespo2002routing`, más volumen y páginas de `lewis2004knowledge` y `brandon2004transactive`, y el DOI de `watkins1975buildup`;
  - la editorial de `mccloskey1989catastrophic`.
- **Etiquetas:** todas las referencias cruzadas de los textos nuevos tienen etiqueta, existente o nueva (`sec:trabajo-relacionado`, `tab:wegner-sistema`, `eq:info-mutua-dir` y `eq:concordancia`).
- **Estilo:** `apalike` no imprime `doi`, `url` ni `eprint`.

## Convenciones

- **«Agente»:** solo aparecía en estructura 8.1, «Los agentes intermediarios (*middle-agents*)», que pasa a «Los intermediarios». «Sistemas multiagente» se queda como nombre del campo (decisión 10).
- **Prefijos:** ningún prefijo con guion en los textos nuevos.
- **Estado final:** los textos nuevos no cuentan versiones de la tesis. M5.1, M5.3 y M5.4 dicen que la doble compuerta se agregó después de ver las 40 consultas: es lo que pide M5 (declarar decisiones posteriores a ver los datos), no historia de versiones, y no lleva fechas ni hashes.
- **Términos en español:** sí, salvo nombres propios de métodos (McNemar), las glosas de 2.4 que nombran conceptos de las fuentes y los identificadores de versión en `\texttt`.
- **Nombre del asistente:** no aparece en ninguno de los archivos de esta ronda ni en las ramas (búsqueda sin distinguir mayúsculas).

## Decisiones del autor

La recomendada va primero. Los tiempos de edición son estimaciones; los de cómputo salen de corridas anteriores.

1. **Cuándo aplicar.**
   - (a) **Recomendada:** aplicar ya todo, con los marcadores visibles, y llenarlos al llegar cada experimento. Costo: la aplicación completa ahora (abajo) y de una a dos horas para llenar los 37 marcadores.
   - (b) Esperar a los cinco experimentos. Costo: el mismo trabajo, bloqueado hasta el último. Como referencia, la parte de texto de exp11, con sus tres configuraciones, tardó 694 min en la última corrida (`logs_comparacion/grupo2/tiempos.txt`).
2. **Si exp11 corregido confirma el empate en clase.**
   - (a) **Recomendada:** dejar M1 como está (dos versiones, McNemar y «los dos empatan») y apoyar la partición en la fidelidad, la mezcla con pistas compartidas y el fuera de dominio con 200 imágenes. Costo: llenar los 24 marcadores, una hora.
   - (b) Si algún corte sale significativo, reescribir las frases de empate de M1.1, M1.4 y M1.6. Costo: media hora más.
3. **Líneas base léxica, de coseno de fastText y de tabla de conteos (M3).** No están entre los experimentos en curso.
   - (a) **Recomendada:** correrlas. Son cálculos sobre el banco, sin memorias, y el jurado pregunta por ellas en la defensa. Costo: unas horas de código, minutos de cómputo y un párrafo con una tabla.
   - (b) Declararlas como limitación. Costo: veinte minutos, y la pregunta queda abierta en la defensa.
4. **Partición reservada estratificada (M3).**
   - (a) **Recomendada:** declarar la composición (M3.2) y dejar el sorteo estratificado como trabajo futuro (M5.5). Costo: nada más.
   - (b) Rehacer exp11 con un sorteo estratificado. Costo: otra corrida de la parte de texto (del orden de 694 min) y reescribir estructura 4.2 y 9.3, M1, M3.2 y M5.
5. **Evocación estricta sobre las 116 imágenes.**
   - (a) **Recomendada:** dejar Me.1, con la versión estricta del oráculo de exp11 y el nivel de azar. Costo: nada más.
   - (b) Volver a correr la etapa 7 guardando las etiquetas por imagen. Costo: unos 40 min de CPU (hemisferio visual en la Tabla 7) y una frase.
6. **«Hemisferio» (dictamen de Wegner; claridad Parte 4, punto 14).**
   - (a) **Recomendada:** conservarlo y agregar en 04:7-9 que nombra un camino, no una lateralización. Costo: cinco minutos.
   - (b) Cambiarlo por «vía» en todo el texto: 26 líneas en cinco archivos, más revisar si alguna figura lo lleva escrito. Costo: unos 30 minutos.
7. **Pasada de forma sobre los pasajes de estructura que no cruzan con claridad.** En los textos nuevos de estructura quedan 60 «: », la mayoría en pasajes que no cruzan (13 en 6.1, 7 en 8.1 y 5 en 2.1), y parte de las 17 antítesis de claridad Parte 4, puntos 6 y 7. Una parte de esos dos puntos introduce enumeraciones y se queda.
   - (a) **Recomendada:** hacerla al aplicar, con el criterio de claridad 3.7. Costo: una hora.
   - (b) Dejarlos. Costo: nada, pero el dictamen de estilo los marcó (5.7).
8. **Citas por cotejar.**
   - (a) **Recomendada:** cotejar la p. 186 de Wegner (1987), los campos «V parcial» y la editorial de McCloskey y Cohen antes de aplicar. Costo: alrededor de una hora con acceso a las editoriales.
   - (b) Aplicar con lo verificado. Costo: nada, con el riesgo de un error bibliográfico ante el jurado.
   - Aparte, las 14 citas que pidió el jurado y la nube no alcanzó a verificar (tabla al final de las entradas BibTeX de estructura) piden otra sesión de verificación, de unas dos horas, o quedar fuera.
9. **Entradas sin citar** (`fortin2004recollection`, `eichenbaum2007medial`, `diana2007imaging` y `squire2007recognition`, que 6.5 deja de citar).
   - (a) **Recomendada:** quitarlas del `.bib`. Costo: cinco minutos.
   - (b) Dejarlas: `apalike` no imprime entradas que nadie cita.
10. **«Sistemas multiagente» en 2.4.**
    - (a) **Recomendada:** conservarlo, porque nombra un campo y no a los módulos. Costo: nada.
    - (b) Reescribir el párrafo sin la palabra. Costo: diez minutos.
11. **Experimentos 10 y 15 con una sola memoria** (claridad S48 y el menor del dictamen). Sus carpetas en `results/` son del 28 oct, anteriores al cambio a una sola memoria (`0c70824`, 1 nov), cuyo mensaje dice «Toda la bateria re-corrida».
    - (a) **Recomendada:** comprobarlo en `logs_comparacion/` y, si no se volvieron a correr, escribir «salvo los experimentos 10 y 15». Costo: un cuarto de hora.
    - (b) Volver a correrlos. Costo de cómputo que no conozco.
12. **Quién escribió el banco y con qué acceso al vocabulario** (pregunta de defensa, M3). El repositorio no lo dice. Hace falta una frase del autor después de M3.1. Costo: cinco minutos.
13. **Experimento 19 en la limitación (k)** (M4).
    - (a) **Recomendada:** esperar al codificador sin pérdida de clase y citar entonces los dos juntos. Costo: media hora al llegar.
    - (b) Citarlo ya. Costo: cotejar sus cifras en `results/experimento19/` (no las verifiqué) y un párrafo, media hora.
14. **Nombre del TME** (dictamen de Wegner, menor).
    - (a) **Recomendada:** conservar la sigla y aclarar en 03 que el «experto» es el mediador, no un especialista. Costo: cinco minutos.
    - (b) Renombrarlo «mediador» en las 33 apariciones y en los nodos TikZ. Costo: unos 45 minutos.
15. **Puntos de claridad que piden una aclaración del autor:** Parte 4, puntos 13 (frase de la lesión), 17 («recordar es muestrear»), 18 (la binarización por signo, repetida y sin medir), 19 (números de experimento y rutas de `results/`), 20 y 21 (lectura de la columna «Variedad $L_1$»). Costo: media hora en total.
16. **Paratexto (E9)**, que no cubre ninguna propuesta: portada con la UACJ, el programa y el grado; fecha; resumen en inglés; palabras clave; lista de siglas; Figura 11 citada en 04, y figuras 2 y 3 que repiten datos. Costo: unas dos horas, sobre todo por el resumen en inglés.

## Costo de aplicarlo todo

- **Volumen de fuente:** las propuestas de estructura y metodología cambian 1081 líneas LaTeX por 589, unas 490 líneas netas más. Es del orden de 8 a 10 páginas sobre las 42 actuales, estimado por líneas; hay que compilar para saberlo. La de claridad cambia 183 fragmentos en la Parte 2 y aplica las reglas mecánicas: 120 porcentajes, 21 pares de comillas, 32 «hetero» u «homo», 41 dos puntos y las sustituciones de 3.8. No alarga el texto.
- **Edición:**
  - estructura, una hora y media a dos, por los cinco bloques enteros, la sección 2.4 y la tabla;
  - metodología, una hora;
  - claridad, Parte 2 sin lo absorbido, una hora;
  - reglas mecánicas, una hora con búsqueda asistida y revisión;
  - pasada de forma, una hora;
  - bibliografía, un cuarto de hora más el cotejo de la decisión 8;
  - compilar y revisar, de media hora a una hora.

  En total, de 6 a 8 horas de edición.
- **Después:** de una a dos horas para llenar los 37 marcadores cuando lleguen los cinco experimentos, más lo que agreguen las decisiones 3, 4, 5 y 11 si se eligen las opciones con cómputo.

## Lo que el dictamen de metodología pide y ninguna propuesta cubre

Está en la tabla final de `revision_jurado_metodologia_prosa.md`:
- líneas base (decisión 3);
- partición estratificada y banco de terceros (decisión 4);
- experimento 19 (decisión 13);
- modelos con hashes y réplica desde cero (M6);
- el menor de $\iota$;
- las siete condiciones efectivas;
- los detalles de la lesión, de imagen → texto, del costo del rescate y de la concordancia;
- el commit de `hetero_lib`.
