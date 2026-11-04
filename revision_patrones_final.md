# Auditoría final de patrones de texto generado

Base: `4e2ccc5` (rama `una-hetero`, 180 páginas). Alcance: Resumen, Abstract, Introducción, Capítulo 1 (con la Justificación aparte), Capítulos 2 a 5 desde `.tex8/secciones/`, Conclusión del objetivo general y Apéndice A. Reglas: `plan_reestructura/BRIEF_COMUN.md`, regla 6 de `plan_reestructura/INDICE_REESTRUCTURA_FASES.md`, `plan_reestructura/antipatrones.md`, sección 7 de `texaudit/PLAN.md` y la lectura anterior, `revision_jurado_fases_estilo.md`.

No se cambió ninguna cifra, etiqueta `\label`, cita ni término definido. Lo comprobé con un script sobre `git diff -U0 4e2ccc5`: en las líneas quitadas y en las nuevas aparecen los mismos números. Solo faltan «1», «32» y «64», que eran los rótulos B1, E32 y E64 de la lista que se cambió por una remisión (cambio P11). La única clave nueva es `\ref{fase2:lectura}`, que ya existe. Resumen, Abstract e Introducción no se tocaron. Tampoco se tocó `generar_capitulos.py`. Los capítulos 2 a 5 se regeneraron, y el script terminó sin error: «líneas de .tex8 que no aparecen en la salida: 0». En este contenedor no hay XeLaTeX, así que no pude compilar ni contar páginas. El parche quita 11 líneas netas de prosa, sin tablas ni figuras.

## Dictamen

**Se puede entregar con este parche.** Los conteos ya estaban bajos y siguen así. En todo el documento no hay «sin embargo», «cabe destacar», «es importante», «en este sentido», «nótese», «claramente», «robusto», «no X, sino Y» ni restos de historial de versiones, y tampoco aparece «agente». El único «clave» de los preliminares es «Palabras clave», y el de la Justificación es «la clave» de un índice. La longitud media de las oraciones va de 24 a 28 palabras, con una desviación de 14 a 19 en los capítulos, así que el ritmo no es uniforme.

Lo que pesaba estaba en el texto escrito hoy y no aparece en un recuento:

1. **Transiciones sin lógica.** Hay tres casos.
   - Un «Tampoco se sostuvo» venía sin una negación antes (`07_conclusiones.tex:205-207`).
   - Un «así que» hacía depender la falta de una comparación controlada de que no se guardaron los modelos (`05_resultados.tex:23-25`). La causa real es el cambio de arquitectura.
   - La Justificación anuncia tres propiedades y después agrega una cuarta, la trazabilidad, en el párrafo de la salvedad (`Capitulo1.tex:216-220`).
2. **Vaguedad.**
   - «casi siempre «en lo medido»» resume seis creencias matizadas, pero solo una de ellas lo dice (`06_discusion.tex:237-238`).
   - «En él» no tiene un antecedente claro (`07:38`).
   - «Medirlo así» no dice qué se mide (`Capitulo1.tex:220`).
   - «se rotulan así» no dice cómo (`05:5`).
3. **Conclusiones repetidas en un mismo capítulo.**
   - La Conclusión del objetivo general repite casi palabra por palabra `07:143-145` (`ConclusionObjetivoGeneral.tex:44-46`).
   - La salvedad del escalado aparece dos veces en el Cap. 3 (`04:20-23` y `04:259-260`).
   - La lista de las nueve condiciones de lectura está en el Cap. 3 y otra vez en Resultados (`05:130-133`), ahí con dos puntos anidados.
4. **Un resto de las reglas internas en el texto.** «Cada cifra de este capítulo va con la arquitectura de su fase» (`07:19`) es la regla 1 del brief, copiada como si fuera prosa.
5. **Un rótulo de fase equivocado.** «la ablación de la fase 1» (`05:110`) contradice el Cap. 3, donde la ablación es de la fase 2 y se hizo sobre el prototipo de la fase 1.

El parche tiene 19 cambios (P01 a P19). Ninguno cambia el sentido de una oración.

**Diez casos más claros** (archivo:línea en `4e2ccc5`):

| # | Lugar | Patrón |
|---|---|---|
| 1 | `.tex8/secciones/07_conclusiones.tex:205` | transición sin lógica («Tampoco» sin negación previa) |
| 2 | `.tex8/secciones/07_conclusiones.tex:19` | resto de una regla interna (metatexto) |
| 3 | `.tex8/secciones/06_discusion.tex:237` | vaguedad o generalización sin respaldo («casi siempre») |
| 4 | `.tex_uacj/Capitulo1.tex:216` | transición sin lógica (cuarta propiedad tras anunciar tres) y vaguedad («Medirlo así») |
| 5 | `.tex8/secciones/05_resultados.tex:23` | conector causal falso («así que») |
| 6 | `.tex_uacj/ConclusionObjetivoGeneral.tex:44` | conclusión repetida literal (`07:143`) |
| 7 | `.tex8/secciones/05_resultados.tex:130` | dos puntos en serie y repetición entre capítulos (`04:191-206`) |
| 8 | `.tex8/secciones/07_conclusiones.tex:38` | vaguedad (antecedente ambiguo) |
| 9 | `.tex8/secciones/04_metodologia.tex:259` | conclusión repetida en el mismo capítulo (`04:20-23`) |
| 10 | `.tex8/secciones/07_conclusiones.tex:39` | frase que anuncia «cuatro límites» y los reparte en dos oraciones con «;» |

## Conteos por capítulo, antes → después

Usé el script del final, que extiende el `conteo.py` de `revision_jurado_fases_estilo.md` con la misma limpieza de la prosa y el mismo corte de oraciones. Agrega cuatro grupos: frases que anuncian, énfasis sin respaldo, contrastes de plantilla y restos. También agrega dos puntos en serie, tríadas candidatas y oraciones muy largas y muy cortas.

Las columnas son las unidades pedidas:
- **Justif.**: `Capitulo1.tex`, desde `\section{Justificación}` hasta `\section{Alcances…}`.
- **Cap1 sin Just.**: el resto del capítulo.
- **Concl.**: `07` más `ConclusionObjetivoGeneral` (el Capítulo 5 sin Difusión).
- **Cap3** y **Cap4**: los dos archivos de `.tex8` que forma cada uno, por separado, para poder compararlos con la lectura anterior.

Las tríadas son candidatas del tipo «A, B y C», con uno a tres palabras por miembro. Las revisé una por una, y todas son enumeraciones reales (conteos 27/27/26, órdenes de llegada, listas de patrones o de experimentos). Los dos puntos en serie del Cap. 3 (04) y de las Conclusiones son introducciones de listas (`itemize` y `enumerate`), no explicaciones encadenadas. El 14 → 15 del Cap. 3 se debe a que P07 quitó la oración que separaba dos de esas introducciones. Los patrones que dieron 0 antes y después se omiten de la tabla: «por lo tanto», «sin embargo», «de hecho», «en particular», «dicho de otro modo», «cabe/es importante/vale la pena», «en este sentido/nótese», «claramente/notablemente/sin duda», «robusto/sólido», «no X, sino Y», «versión anterior/jurado», «agente», los restos conversacionales y, en el Abstract, «crucial/key/robust/clearly/notably» y «not X but Y».

| Patrón | Resumen | Abstract | Intro | Cap1 sin Just. | Justif. | Cap2 | Cap3 (03) | Cap3 (04) | Cap4 Res. (05) | Cap4 Disc. (06) | Concl. (07+COG) | ApA | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Muletillas** | | | | | | | | | | | | | |
| así (conector) | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 5 → 4 | 9 → 8 | 3 | 1 → 0 | 0 | 19 → 16 |
| además | 0 | 0 | 0 | 1 | 0 | 3 | 1 | 5 | 3 | 2 | 0 | 0 | 15 |
| en cambio | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 2 | 2 | 0 | 0 | 6 |
| es decir | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 3 |
| por eso | 0 | 0 | 0 | 1 | 0 | 3 | 0 | 3 | 3 | 4 | 0 | 0 | 14 |
| a la vez | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 2 | 3 | 2 | 1 | 0 | 10 |
| también | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 5 | 12 | 13 | 2 → 1 | 0 | 38 → 37 |
| solo/sólo | 1 | 0 | 0 | 7 | 3 | 11 | 9 | 26 | 38 | 33 | 8 | 1 | 137 |
| en suma/en resumen | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| *subtotal* | 1 | 0 | 1 | 11 | 4 | 20 | 14 | 47 → 46 | 72 → 71 | 60 | 12 → 10 | 1 | 243 → 239 |
| **Frases que anuncian** | | | | | | | | | | | | | |
| esta sección/este capítulo | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 1 → 0 | 0 | 4 → 3 |
| a continuación/como se verá | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| anuncio con «:» («son cuatro:») | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lo que importa/la respuesta es | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| *subtotal* | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 2 | 2 | 1 → 0 | 0 | 7 → 6 |
| **Énfasis sin respaldo** | | | | | | | | | | | | | |
| crucial/clave/fundamental/esencial | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| exactamente/precisamente/justamente | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 3 |
| limpio/perfecto/honesto | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 2 |
| realmente/simplemente/enorme… | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| *subtotal* | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 3 | 1 | 0 | 0 | 8 |
| **Contrastes de plantilla** | | | | | | | | | | | | | |
| «X, no Y» / «X, no solo Y» | 0 | 0 | 0 | 0 | 1 → 0 | 2 | 0 | 1 | 3 | 4 | 0 | 0 | 11 → 10 |
| «no es X; es Y» | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| *subtotal* | 0 | 0 | 0 | 0 | 1 → 0 | 2 | 1 | 1 | 3 | 4 | 0 | 0 | 12 → 11 |
| **Estructura y ritmo** | | | | | | | | | | | | | |
| Oraciones seguidas con la misma primera palabra | 1 | 0 | 0 | 7 | 1 | 8 | 6 | 15 | 36 | 32 | 3 → 2 | 0 | |
| Oraciones con dos o más «:» | 0 | 0 | 0 | 0 | 0 | 3 | 2 | 4 | 3 → 2 | 0 | 1 | 1 | |
| Pares de oraciones seguidas con «:» | 0 | 0 | 0 | 2 → 1 | 1 → 0 | 5 | 3 | 14 → 15 | 5 | 3 | 9 | 0 | |
| Tríadas «A, B y C» (candidatas) | 1 | 0 | 0 | 2 | 0 | 1 | 0 | 5 | 11 | 10 | 3 | 0 | |
| Palabras | 285 | 260 | 283 | 2434 → 2435 | 498 → 518 | 3086 | 2325 | 6793 → 6770 | 13345 → 13308 | 8460 → 8455 | 3433 → 3420 | 271 | |
| Oraciones | 11 | 11 | 12 | 98 | 20 | 114 | 84 | 252 → 251 | 512 | 307 | 124 → 125 | 6 | |
| Longitud media (palabras) | 25.9 | 23.6 | 23.6 | 24.7 | 24.9 → 25.9 | 27.0 | 27.7 | 26.9 → 27.0 | 26.0 | 27.5 | 27.7 → 27.3 | 45.2 | |
| Desviación de la longitud | 13.6 | 11.8 | 5.8 | 17.9 | 14.3 → 13.9 | 13.6 | 13.7 | 19.2 → 19.3 | 14.5 | 15.7 | 16.7 → 16.6 | 28.3 | |
| Oraciones de 50 palabras o más | 1 | 0 | 0 | 10 | 2 | 10 | 7 | 21 | 28 → 27 | 20 | 15 → 14 | 1 | |
| Oraciones de 8 palabras o menos | 0 | 0 | 0 | 19 | 1 | 10 | 5 | 27 | 51 | 25 | 19 → 18 | 0 | |

En la Justificación, el «clave» es el de un índice («lo que coincide con su clave»). El único «a continuación» del Cap. 2 (`02:169`) presenta una ecuación. Los «exactamente» de `05:1172`, `05:1272` y `06:773` significan «si y solo si». Los dos «limpias» son el nombre de una condición de la simulación de color. Nada de eso es énfasis.

**Comienzos de oración de dos palabras con 4 o más apariciones** (sin cambios, salvo Conclusiones):

- **Cap2**: «En la» 8, «La entropía» 4
- **Cap3 (04)**: «En el» 8, «Con el» 5
- **Cap4 Res. (05)**: «Con el» 13, «El directorio» 9, «En la» 8, «Con X» 7, «Con la» 7, «Lo que» 7, «Se compararon» 6, «La Tabla» 6, «En las» 6, «Sobre las» 5, «En el» 5, «El sistema» 5, «Con objetos» 5, «La fase» 4, «Formación del» 4
- **Cap4 Disc. (06)**: «La lectura» 8, «En la» 7, «El directorio» 6, «Lo que» 6, «En este» 6, «En texto» 5, «En imagen» 5, «Con un» 5, «Las cifras» 4, «En el» 4, «En las» 4, «En los» 4, «El rechazo» 4
- **Concl. (07+COG)**: ninguno → «En el» 4. Una de esas oraciones es la de P14, «En el directorio queda…», que cambia un «En él» ambiguo. Ninguna de las cuatro va seguida de otra con el mismo comienzo.

Las series de tres o más oraciones seguidas con la misma primera palabra son 10. Todas son enumeraciones con un comienzo impuesto: los tres decisores (`05`, «El voto / El centroide / El vecino»), los tres protocolos («En el directo / En el encadenado / En el agregado»), «En imagen / En texto / En un anillo» y el paso de `07` a la Conclusión del objetivo general.

### Comparación con `revision_jurado_fases_estilo.md`

Comparé con la columna «después» de esa lectura, corriendo su `conteo.py` sin cambios sobre `4e2ccc5` y sobre este parche:

| Medida (script anterior) | Lectura anterior | `4e2ccc5` | Este parche |
|---|---|---|---|
| así (conector), total | 18 | 19 | 16 |
| así, Res(05) | 8 | 9 | 8 |
| así, Cap3b(04) | 5 | 5 | 4 |
| así, Cap5(07+COG) | 1 | 1 | 0 |
| por eso, total | 14 | 14 | 14 |
| en cambio, total | 5 | 6 | 6 |
| también, total | 37 | 38 | 37 |
| solo/sólo, total | 133 | 137 | 137 |
| esta sección/este capítulo | 4 | 4 | 3 |
| «, no » | 8 | 8 | 8 |
| Palabras, Cap1 | 2750 | 2932 | 2953 |
| Oraciones seguidas con la misma palabra, Cap1 | 8 | 8 | 8 |
| Longitud media / desviación, Cap1 | 24.4 / 17.0 | 24.7 / 17.3 | 24.9 / 17.3 |
| Longitud media / desviación, Res(05) | 26.0 / 14.5 | 26.0 / 14.5 | 26.0 / 14.5 |
| Longitud media / desviación, Disc(06) | 27.5 / 15.8 | 27.5 / 15.7 | 27.5 / 15.7 |
| Longitud media / desviación, Cap5 | 27.6 / 16.7 | 27.7 / 16.7 | 27.3 / 16.6 |

Las diferencias entre la lectura anterior y `4e2ccc5` vienen de dos cambios posteriores a esa lectura. Uno es la integración del parche de cifras (`f809ed6`), que dejó un «así» más en Resultados y un «En el» más en el 04. El otro es la Justificación nueva (`4fec3dd`), que suma 182 palabras al Cap. 1, un «en cambio» y tres «solo». La Justificación nueva no tiene muletillas fuera de esas, ni énfasis, ni frases que anuncian. Sus problemas son de lógica (P03 y P04) y de un contraste con dos puntos (P02).

## Cambios aplicados (viejo, nuevo y patrón)

Archivo y línea en `4e2ccc5`.

### P01 · `.tex_uacj/Capitulo1.tex:100` (Definición del problema)

**Patrón:** dos puntos en serie. La oración anterior ya explica el techo con dos puntos.

Viejo:
```latex
La solución que se propone es la de la memoria transactiva: repartir el contenido entre
especialistas, cada uno con menos variedad que guardar, y aprender con el uso a quién
preguntar.
```
Nuevo:
```latex
La solución que se propone es la de la memoria transactiva, que reparte el contenido
entre especialistas, cada uno con menos variedad que guardar, y aprende con el uso a
quién preguntar.
```

### P02 · `.tex_uacj/Capitulo1.tex:208` (Justificación)

**Patrón:** contraste de plantilla («X, no solo Y») después de dos puntos. Ahora dice contra qué se contrasta.

Viejo:
```latex
La tercera es que cada especialista es una memoria
declarativa~\cite{pineda2022weighted}: guarda y devuelve contenido, no solo una etiqueta.
```
Nuevo:
```latex
La tercera es que cada especialista es una memoria
declarativa~\cite{pineda2022weighted}, que guarda y devuelve contenido donde un
clasificador daría solo una etiqueta.
```

### P03 · `.tex_uacj/Capitulo1.tex:216-220` (Justificación)

**Patrón:** transición sin lógica y vaguedad. Después de anunciar «tres propiedades», la trazabilidad aparecía como una cuarta, al principio del párrafo de la salvedad. Además, «Medirlo así» no tenía referente. La trazabilidad pasa al párrafo de la tercera propiedad, la memoria declarativa, porque sale de sus operaciones formales. La salvedad queda sola y dice qué se compara.

Viejo (al final del párrafo de la tercera propiedad, y después):
```latex
El sistema responde con una imagen o con palabras, reconoce por contención y contesta
«no lo tengo» cuando la entrada no tiene soporte.
Un índice exacto solo encuentra lo que coincide con su clave y no sirve para imágenes;
[…]

Como las operaciones de la memoria están definidas formalmente, cada decisión se puede
rastrear hasta los conteos que la produjeron.
Ninguna de estas propiedades promete más acierto: sobre los mismos vectores, decisores
simples aciertan lo mismo en texto y más en imagen.
Medirlo así separa lo que aporta el mecanismo de lo que aporta la representación.
```
Nuevo:
```latex
El sistema responde con una imagen o con palabras, reconoce por contención y contesta
«no lo tengo» cuando la entrada no tiene soporte.
Como las operaciones de la memoria están definidas formalmente, cada una de esas
decisiones se puede rastrear hasta los conteos que la produjeron.
Un índice exacto solo encuentra lo que coincide con su clave y no sirve para imágenes;
[…]

Ninguna de estas propiedades promete más acierto: sobre los mismos vectores, decisores
simples aciertan lo mismo en texto y más en imagen.
La comparación con esos decisores separa lo que aporta el mecanismo de lo que aporta la
representación.
```

### P04 · `.tex_uacj/Capitulo1.tex:222` (Justificación)

**Patrón:** transición sin lógica. El párrafo anunciaba que las fases muestran «de dónde salió cada decisión», y su última oración trata de la demostración con voz y cámara, que no decide nada del sistema final. Ahora la primera oración cubre las dos cosas.

Viejo:
```latex
Contar la investigación por fases deja ver de dónde salió cada decisión del sistema
final.
```
Nuevo:
```latex
Contar la investigación por fases deja ver de dónde salió cada decisión del sistema
final y qué le falta para recibir entradas del mundo real.
```

### P05 · `.tex8/secciones/04_metodologia.tex:148`

**Patrón:** muletilla («así que»). El «dentro de muestra» se queda, pero sin el conector.

Viejo:
```latex
después evaluaba la fase madura sobre las mismas 80, así que la evaluación es dentro de
muestra.
```
Nuevo:
```latex
después evaluaba la fase madura sobre esas mismas 80, dentro de muestra.
```

### P06 · `.tex8/secciones/04_metodologia.tex:240`

**Patrón:** cambio de registro (jerga de git en la prosa). El término original se queda entre paréntesis.

Viejo:
```latex
El paso de tres a ocho módulos ocupa 22 commits, de \texttt{b281f9c} (1 de julio de
```
Nuevo:
```latex
El paso de tres a ocho módulos ocupa 22 revisiones del repositorio (\textit{commits}), de \texttt{b281f9c} (1 de julio de
```

### P07 · `.tex8/secciones/04_metodologia.tex:259`

**Patrón:** conclusión repetida en el mismo capítulo. La Sección «Las cinco fases» (`04:20-26`) ya dice que el paso cambió todo a la vez y que las cifras no se comparan. La lista de cambios de la fase 3 basta para mostrarlo. Tal como hizo la lectura anterior en `07:71-73`, el rótulo se conserva una vez por capítulo.

Viejo:
```latex
\end{itemize}
Como todo cambió junto, la diferencia entre las cifras de tres y de ocho módulos no se
puede atribuir al número de módulos.
```
Nuevo:
```latex
\end{itemize}
```

### P08 · `.tex8/secciones/05_resultados.tex:4-5` (apertura de Resultados)

**Patrón:** vaguedad («se rotulan así») y repetición. Diez líneas después, la fase 1 abre con su rótulo completo. La oración nueva dice lo que hace cada fase de la sección. Las cinco lo cumplen (`05:16`, `:109`, `:442`, `:1485`, `:1737`).

Viejo:
```latex
Los resultados siguen las cinco fases de la Sección~\ref{fase:arco}.
Las cifras de la fase 1 son de su propia arquitectura, con tres módulos, y se rotulan así.
```
Nuevo:
```latex
Los resultados siguen las cinco fases de la Sección~\ref{fase:arco}, y cada fase abre
con la arquitectura de la que salen sus cifras.
```

### P09 · `.tex8/secciones/05_resultados.tex:23`

**Patrón:** conector causal falso. Que no se guardaran los modelos explica que las cifras no se volvieran a medir, pero no explica que no se comparen. Eso se debe a la arquitectura distinta, que se da en las líneas 16 a 18.

Viejo:
```latex
Los modelos de esa fase no se guardaron y el código actual fija ocho clases, así que
estas cifras no se volvieron a medir ni se comparan como experimento controlado con las
del sistema final.
```
Nuevo:
```latex
Los modelos de esa fase no se guardaron y el código actual fija ocho clases, de modo que
estas cifras no se volvieron a medir.
Tampoco se comparan como experimento controlado con las del sistema final.
```

### P10 · `.tex8/secciones/05_resultados.tex:110`

**Patrón:** rótulo de fase inconsistente. El Cap. 3 (`04:192`) dice que la ablación de la lectura es la fase 2 y que se corrió sobre el prototipo de la fase 1. «La ablación de la fase 1» la ponía en la fase equivocada.

Viejo:
```latex
En la ablación de la fase 1, con la arquitectura de la sección anterior, cinco semillas
```
Nuevo:
```latex
En la ablación sobre el prototipo de la fase 1, con la arquitectura de la sección anterior, cinco semillas
```

### P11 · `.tex8/secciones/05_resultados.tex:130`

**Patrón:** dos puntos en serie (anidados en la misma oración) y repetición entre capítulos. Las nueve condiciones se definen con una línea cada una en `04:191-206`.

Viejo:
```latex
Se compararon nueve condiciones: la lectura cruda (A), dos normalizaciones por el conteo
de registros de cada módulo (B1, B2) y seis que actúan sobre otra cosa: un tope de
registros por módulo (C), consultas balanceadas (D), la cuantización (E32, E64), el
vocabulario (F) y la combinación de D, B1 y F (G).
```
Nuevo:
```latex
Se compararon las nueve condiciones de la ablación con tres módulos, de A a G
(Sección~\ref{fase2:lectura}).
```

### P12 · `.tex8/secciones/06_discusion.tex:237` (creencias, 4.2.1)

**Patrón:** vaguedad, o una generalización sin respaldo. De las seis creencias matizadas, solo la 9 dice «en lo medido» (`06:124`), así que «casi siempre» no se sostiene. La oración siguiente ya da los alcances concretos.

Viejo:
```latex
Las seis matizadas (4, 6, 9, 14, 16 y 18) conservan la idea con un alcance menor, casi
siempre «en lo medido».
```
Nuevo:
```latex
Las seis matizadas (4, 6, 9, 14, 16 y 18) conservan la idea con un alcance menor.
```

### P13 · `.tex8/secciones/07_conclusiones.tex:19`

**Patrón:** resto de una regla interna, como metatexto. Es la regla 1 del brief («Cada cifra va con la arquitectura de su fase») copiada al texto. La oración siguiente, que dice qué cambió entre fases, se queda.

Viejo:
```latex
Cada cifra de este capítulo va con la arquitectura de su fase.
Entre el prototipo y el sistema final cambiaron a la vez el codificador, la cuantización
```
Nuevo:
```latex
Entre el prototipo y el sistema final cambiaron a la vez el codificador, la cuantización
```

### P14 · `.tex8/secciones/07_conclusiones.tex:38`

**Patrón:** vaguedad. «En él» tenía como antecedentes posibles «el bloqueado», «el orden» o las cuentas.

Viejo:
```latex
En él queda a quién vio ganar cada pista, y lo que no presenció no lo enruta.
```
Nuevo:
```latex
En el directorio queda a quién vio ganar cada pista, y lo que no presenció no lo enruta.
```

### P15 · `.tex8/secciones/07_conclusiones.tex:39-45`

**Patrón:** frase que anuncia sin cumplir de forma visible y muletilla. Se anunciaban «cuatro límites», pero tres iban en una sola oración con «así que» y «;», y no se podían contar. Ahora cada límite es una oración.

Viejo:
```latex
Esta respuesta tiene cuatro límites.
La curva se midió sobre las mismas 80 consultas que forman el directorio, así que mide
cuánto del banco cubren los tokens ya registrados; el techo lo pone la fase temprana
(98.73\,\% acumulado frente al 98.75\,\% de la madura), y sin la lectura B1 la fase
madura no lo alcanza.
La formación con ocho módulos no repite el umbral: […]
```
Nuevo:
```latex
Esta respuesta tiene cuatro límites.
La curva se midió sobre las mismas 80 consultas que forman el directorio y mide cuánto
del banco cubren los tokens ya registrados.
El techo lo pone la fase temprana (98.73\,\% acumulado frente al 98.75\,\% de la
madura).
Sin la lectura B1, la fase madura no lo alcanza.
Por último, la formación con ocho módulos no repite el umbral: […]
```

### P16 · `.tex8/secciones/07_conclusiones.tex:61-66`

**Patrón:** transición sin lógica (orden). La interpretación («B1 opera fuera de las memorias y corrige un sesgo…») quedaba entre dos cifras de la verificación con ocho módulos. Ahora van primero las dos verificaciones con ocho módulos (conjunto fijo y participación de `apple`), luego el principio de tamaño y al final la interpretación. Solo se movieron líneas.

Viejo (orden):
```latex
(Sección~\ref{sec:calibracion-fija}).
Leer el directorio con el principio de tamaño da en ETH-80, […]
B1 opera fuera de las memorias y corrige un sesgo de la lectura sin tocar lo registrado.
En el sistema de ocho módulos, la lectura cruda le da a \texttt{apple} el 20.5\,\% de las
[…] en el 13.8\,\% (Sección~\ref{sec:calibracion}).
```
Nuevo (orden):
```latex
(Sección~\ref{sec:calibracion-fija}).
En el sistema de ocho módulos, la lectura cruda le da a \texttt{apple} el 20.5\,\% de las
[…] en el 13.8\,\% (Sección~\ref{sec:calibracion}).
Leer el directorio con el principio de tamaño da en ETH-80, […]
B1 opera fuera de las memorias y corrige un sesgo de la lectura sin tocar lo registrado.
```

### P17 · `.tex8/secciones/07_conclusiones.tex:168`

**Patrón:** frase que anuncia, con muletilla («también»). El párrafo abría diciendo que algo se midió. Ahora abre con lo que se encontró, igual que los párrafos vecinos («Reconocer y recordar se separan…», «De una imagen el sistema recupera el dominio…»). Las dos cifras que siguen lo respaldan: acepta 2 de 12 consultas ajenas y rechaza 23 imágenes que un vecino acierta.

Viejo:
```latex
Los límites del rechazo también se midieron.
```
Nuevo:
```latex
El rechazo por contención falla en los dos sentidos.
```

### P18 · `.tex8/secciones/07_conclusiones.tex:205`

**Patrón:** transición sin lógica. La oración siguiente empieza con «Tampoco se sostuvo», y la anterior afirmaba un logro. Ahora dice qué se esperaba y qué pasó, de modo que «Tampoco» tiene a qué referirse. Se conserva la fórmula «fidelidad, menos mezcla y rechazo», que es la de `ConclusionObjetivoGeneral.tex:32`.

Viejo:
```latex
Partir el contenido entre especialistas dio fidelidad, menos mezcla y rechazo, con el
mismo acierto de clase que una sola memoria.
Tampoco se sostuvo que todas las decisiones fueran operaciones de memoria, […]
```
Nuevo:
```latex
De partir el contenido entre especialistas se esperaba más acierto de clase que con una
sola memoria; dio el mismo, junto con fidelidad, menos mezcla y rechazo.
Tampoco se sostuvo que todas las decisiones fueran operaciones de memoria, […]
```

### P19 · `.tex_uacj/ConclusionObjetivoGeneral.tex:44`

**Patrón:** conclusión repetida casi palabra por palabra en el mismo capítulo. `07:143-145` («Estos experimentos de lectura inversa, perspectiva y pérdida de un miembro usan protocolos anteriores al sistema final…») está en la sección anterior del Capítulo 5. Aquí queda solo lo que importa para el veredicto del objetivo: lo que falta repetir.

Viejo:
```latex
Los experimentos de lectura inversa, perspectiva y pérdida de un miembro usan protocolos
anteriores al sistema final, y la pérdida de un miembro está por repetirse con el
protocolo final.
```
Nuevo:
```latex
La pérdida de un miembro, medida con un protocolo anterior al sistema final, está por
repetirse con el protocolo final.
```

## Lo que vi y no toqué

**Repeticiones que impone una regla.**
- La salvedad del escalado («cambiaron varias cosas a la vez») aparece en `Capitulo1.tex:78` y `:278`, `Introduccion.tex:19`, `04:20`, `05:443`, `06:70`, `:597` y `:1045`, y `07:20`. Con P07 queda una vez por capítulo, salvo en Discusiones, donde las tres apariciones son una celda de la Tabla de creencias, el tema del tamaño y la limitación (m). Cada una sostiene una afirmación distinta.
- La «evidencia controlada del tamaño» (EHAM única y 2 contra 8 clases) aparece en `Capitulo1.tex:81`, `04:24`, `05:447`, `07:85` y `ConclusionObjetivoGeneral.tex:34`. Es el rótulo de la fase 3 que pide la regla 3 del brief.
- «Dentro de muestra» para la fase 1 aparece en `04:148` y `:169`, `05:97-100`, `07:40` y `ConclusionObjetivoGeneral.tex:10`. Es el rótulo de la fase 1, y en `04:169` y `05:99` agrega la interpretación (cobertura del banco y no generalización).
- «Demostración de integración» para la fase 5 se repite en cada capítulo, también por regla.

**Paralelismos de enumeración.** «La primera es que… / La segunda es que… / La tercera es que…» aparece en la Justificación (`Capitulo1.tex:190`, `:200` y `:208`), en la verificación de B1 (`04:220-234`) y en las dos condiciones de `06:817-824`. Las tres son enumeraciones anunciadas con su número, de cosas que sí son distintas. Cambiarlas sería variación artificial.

**Resumen de sección en Discusiones.** `06:852-856` («En suma, la clase la deciden las representaciones…») resume los cuatro párrafos anteriores, y las Conclusiones (`07:105-118`) y la Justificación lo retoman. Cierra el tema «Qué aporta la partición» y es el único sitio de Discusiones que dice que en imagen el rechazo depende de $\tau$. Lo dejé.

**Títulos de párrafo con contraste.** «El orden afecta la velocidad, no el destino» (`05:585`), «El directorio localiza; no decide mejor» (`06:835`) y «En la clase, no agrega» (`06:767`) son títulos que enuncian el hallazgo. Las lecturas anteriores los conservaron, y su contraste es informativo.

**Muletillas que llevan información.**
- Quedan 16 «así que» (8 en Resultados) y 14 «por eso», casi todos con una relación causal real.
- «solo» (137) y «también» (37) casi siempre restringen: «solo con la clase real», «solo dentro de muestra».
- «entonces» aparece dos veces en el Cap. 1 (`:60` y `:98`), en párrafos distintos.

**Negritas en la prosa.** `04:281` («ocho clases»), `:336` («masa asociativa»), `:348` («escala global guardada»), `:413` («no participa»), `:431` («umbral de energía») y `:452` («411 consultas»), más 12 en el Cap. 2 y 8 en el 03. Casi todas marcan un término en su definición. «no participa» es un énfasis, pero subraya la salvedad principal sobre el codificador, que el jurado tiene que ver. Es texto anterior a la reestructura, ya revisado dos veces.

**Ritmo de la Introducción.** La desviación de la longitud es de 5.8 (12 oraciones de 17 a 32 palabras). Es la más uniforme del documento, pero se lee bien, y la Introducción no puede crecer. Cambiar la longitud de las oraciones solo para mover esa cifra sería variación artificial.

**Resumen y Abstract.** No tienen patrones que pesen. «y no un ejemplar» (Resumen:21) y «not an exemplar» son contrastes informativos.

**Verbos de cumplimiento.** En la Conclusión del objetivo general, «se cumplió» se repite una vez por objetivo. Es la función de esa sección.

**«versión v5».** Es redundante, pero es el nombre del sistema de julio en todo el reporte.

**Para el autor o la sesión de cifras (contenido, no estilo):**
- `07_conclusiones.tex:131` dice «Registrar solo lo que cada módulo presencia no le cuesta acierto al grupo», y dos líneas después da 91.0 frente a 93.6\,\% en texto. Resultados (`05:1615`) presenta esas cifras sin decir que sean iguales. Conviene suavizarlo, por ejemplo con «casi no le cuesta acierto», o dar la diferencia.
- `Capitulo1.tex:192` (Justificación) da «con tres módulos el directorio supera el 90\,\% de acierto tras 13 interacciones» sin decir que es dentro de muestra. La regla 1 del brief pide rotular las cifras de la fase 1. Sugiero agregar «sobre las mismas consultas que lo forman» o «dentro de muestra».

## Script de conteo

Uso: `python patrones.py <raiz_repo> [--json salida] [--casos triadas_casos|dp_casos]`.

```python
"""Recuento de patrones de texto generado por capítulo.
Uso: python patrones.py <raiz_repo> [--json salida] [--casos patron]
Prosa: igual que conteo.py de revision_jurado_fases_estilo.md (quita comentarios, tablas,
ecuaciones, matemáticas en línea y comandos; conserva captions y listas). Oraciones: . ? !
seguidos de mayúscula. La Justificación es Capitulo1.tex desde \\section{Justificación}
hasta \\section{Alcances...}; «Cap1» es el resto del capítulo."""
import re, sys, json, collections, statistics as st
from pathlib import Path

R = Path(sys.argv[1])


def rd(f):
    return (R / f).read_text(encoding="utf-8")


def cap1(parte):
    t = rd(".tex_uacj/Capitulo1.tex")
    a = t.index("\\section{Justificación}")
    b = t.index("\\section{Alcances")
    return t[a:b] if parte == "just" else t[:a] + t[b:]


UNID = {
    "Resumen": lambda: rd(".tex_uacj/Resumen.tex"),
    "Abstract": lambda: rd(".tex_uacj/Abstract.tex"),
    "Intro": lambda: rd(".tex_uacj/Introduccion.tex"),
    "Cap1-sinJ": lambda: cap1("resto"),
    "Justif": lambda: cap1("just"),
    "Cap2": lambda: rd(".tex8/secciones/02_marco_teorico.tex"),
    "Cap3(03)": lambda: rd(".tex8/secciones/03_arquitectura.tex"),
    "Cap3(04)": lambda: rd(".tex8/secciones/04_metodologia.tex"),
    "Cap4-Res(05)": lambda: rd(".tex8/secciones/05_resultados.tex"),
    "Cap4-Disc(06)": lambda: rd(".tex8/secciones/06_discusion.tex"),
    "Concl(07+COG)": lambda: rd(".tex8/secciones/07_conclusiones.tex") + "\n" + rd(".tex_uacj/ConclusionObjetivoGeneral.tex"),
    "ApA": lambda: rd(".tex_uacj/ApendiceA.tex"),
}

GRUPOS = {
 "muletillas": {
  "así (conector)": r"(?:^|[.;:]\s+|,\s*)así[, ]",
  "además": r"\bademás\b", "en cambio": r"\ben cambio\b", "es decir": r"\bes decir\b",
  "por eso": r"\bpor eso\b", "por lo tanto": r"\bpor lo tanto\b", "sin embargo": r"\bsin embargo\b",
  "de hecho": r"\bde hecho\b", "en particular": r"\ben particular\b", "a la vez": r"\ba la vez\b",
  "también": r"\btambién\b", "solo/sólo": r"\bs[oó]lo\b", "en suma/en resumen": r"\ben (?:suma|resumen)\b",
  "dicho de otro modo/en otras palabras": r"\b(?:dicho de otro modo|en otras palabras)\b",
 },
 "anuncian": {
  "cabe/es importante/vale la pena": r"\b(?:cabe (?:destacar|señalar|notar|precisar|mencionar)|es importante|vale la pena|conviene (?:precisar|señalar|notar|aclarar|recordar|subrayar))\b",
  "en este sentido/nótese": r"\b(?:en este sentido|n[óo]tese|obsérvese)\b",
  "esta sección/este capítulo": r"\b(?:esta sección|este capítulo|esta subsección|este apartado)\b",
  "a continuación/como se verá": r"\b(?:a continuación|como se verá|más adelante se|se verá que)\b",
  "anuncio con «:» («es esta:», «son dos:»)": r"\b(?:es|son|fue|fueron|está|queda|quedan) (?:esta|este|estos|estas|la siguiente|el siguiente|doble|triple|dos|tres|cuatro|simple|sencill[oa])\s*:",
  "lo que importa/la idea es": r"\b(?:lo que importa|la idea (?:central |clave )?es|la respuesta es|el punto es|la clave es)\b",
 },
 "énfasis": {
  "claramente/notablemente/sin duda": r"\b(?:claramente|notablemente|sin duda|indudablemente|evidentemente)\b",
  "crucial/clave/fundamental/esencial": r"\b(?:crucial(?:es)?|clave|fundamental(?:es|mente)?|esencial(?:es|mente)?)\b",
  "robusto/sólido": r"\b(?:robust[oa]s?|robustez|s[óo]lid[oa]s?)\b",
  "exactamente/precisamente/justamente": r"\b(?:exactamente|precisamente|justamente)\b",
  "limpio/perfecto/honesto": r"\b(?:limpi[oa]s?|limpiamente|perfect[oa]s?|perfectamente|honest[oa]s?)\b",
  "realmente/verdaderamente/simplemente": r"\b(?:realmente|verdaderamente|simplemente|totalmente|enorme(?:s|mente)?|drástic[oa]s?|radical(?:es|mente)?)\b",
 },
 "contraste": {
  "«no X, sino Y»": r"\bno [^.;:]{1,80}?,? sino\b",
  "«X, no Y»": r"\w, no (?:el|la|los|las|un|una|de|del|en|por|al|a|que|como|con|solo)\b",
  "«no es X; es Y»": r"\bno (?:es|son|fue|era)\b[^.]{1,60}?[;:] (?:es|son|fue|era)\b",
 },
 "residuos": {
  "versión anterior/jurado": r"\b(?:versi[oó]n anterior|tras el jurado|del jurado|antes dec[ií]a|ahora dice)\b",
  "agente": r"\bagentes?\b",
  "conversacional (veamos, ojo, ahora bien, bueno)": r"\b(?:veamos|ojo|ahora bien|bueno,|pues bien|como ya dijimos|como vimos)\b",
 },
}
EN = {
 "EN énfasis (crucial, key, robust, clearly, notably)": r"\b(?:crucial|key|robust(?:ly)?|clearly|notably|remarkably|significantly)\b",
 "EN «not X but Y»": r"\bnot [^.;:]{1,60}?,? but\b",
}


def prosa(t):
    t = re.sub(r"(?<!\\)%.*", "", t)
    t = re.sub(r"\\begin\{(table\*?|tabular\*?|equation\*?|align\*?|tikzpicture|lstlisting)\}.*?\\end\{\1\}", " ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " X ", t)
    t = re.sub(r"\\(?:ref|label|cite[pt]?|eqref|includegraphics|url|href)\*?(?:\[[^\]]*\])?\{[^}]*\}", " ", t)
    t = re.sub(r"\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?", " ", t)
    t = re.sub(r"\\[a-zA-Z@]+\*?", " ", t)
    t = re.sub(r"[{}~]", " ", t).replace("\\,", "").replace("\\%", "%")
    return t


def oraciones(t):
    t = re.sub(r"\s+", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+(?=[«¿(]?[A-ZÁÉÍÓÚÑ])", t) if len(s.split()) > 2]


def palabras(s):
    return re.sub(r"[^\wáéíóúñü ]", " ", s).split()


# tríada: «A, B y C» con 1-3 palabras por miembro, sin cuarto miembro antes
TRIADA = re.compile(r"(?<![,\w] )(?<!, )\b(\w+(?: \w+){0,2}), (\w+(?: \w+){0,2}),? (?:y|o|e|and|or) (\w+(?: \w+){0,2})\b")


def triadas(s):
    out = []
    for m in TRIADA.finditer(s):
        pre = s[:m.start()].rstrip()
        if pre.endswith(","):
            continue  # serie de cuatro o más
        out.append(m.group(0))
    return out


def analiza(txt, en=False):
    low = txt.lower()
    ors = oraciones(txt)
    res = {}
    for g, pats in GRUPOS.items():
        res[g] = {k: len(re.findall(p, low, re.M)) for k, p in pats.items()}
    if en:
        res["inglés"] = {k: len(re.findall(p, low)) for k, p in EN.items()}
    firsts = [(palabras(s) or [""])[0] for s in ors]
    c2 = collections.Counter(" ".join(palabras(s)[:2]) for s in ors)
    dp2 = [s for s in ors if s.count(":") >= 2]
    dpcons = sum(1 for a, b in zip(ors, ors[1:]) if ":" in a and ":" in b)
    tri = [t for s in ors for t in triadas(s)]
    lens = [len(s.split()) for s in ors]
    return dict(
        palabras=len(txt.split()), oraciones=len(ors), grupos=res,
        consecutivas=sum(1 for a, b in zip(firsts, firsts[1:]) if a and a == b),
        top2=[x for x in c2.most_common(15) if x[1] >= 4],
        dos_puntos_2mas=len(dp2), dos_puntos_consecutivas=dpcons,
        triadas=len(tri), triadas_casos=tri,
        media=round(st.mean(lens), 1) if lens else 0, de=round(st.pstdev(lens), 1) if lens else 0,
        largas_50=sum(1 for x in lens if x >= 50), cortas_8=sum(1 for x in lens if x <= 8),
        dp_casos=dp2,
    )


out = {u: analiza(prosa(f()), en=(u == "Abstract")) for u, f in UNID.items()}
if "--json" in sys.argv:
    Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(out, ensure_ascii=False, indent=1))
if "--casos" in sys.argv:
    k = sys.argv[sys.argv.index("--casos") + 1]
    for u, d in out.items():
        for c in d.get(k, []):
            print(u, "|", c)
    sys.exit()

U = list(UNID)
print("| Patrón | " + " | ".join(U) + " | Total |")
print("|---" * (len(U) + 2) + "|")
for g in GRUPOS:
    print(f"| **{g}** |" + " |" * (len(U) + 1))
    for k in GRUPOS[g]:
        v = [out[u]["grupos"][g][k] for u in U]
        if sum(v) or "--todo" in sys.argv:
            print(f"| {k} | " + " | ".join(map(str, v)) + f" | {sum(v)} |")
    tot = [sum(out[u]["grupos"][g].values()) for u in U]
    print(f"| *subtotal {g}* | " + " | ".join(map(str, tot)) + f" | {sum(tot)} |")
for k in EN:
    print(f"| {k} | " + " | ".join(str(out[u].get('grupos', {}).get('inglés', {}).get(k, '–')) for u in U) + " | |")
for lab in ("consecutivas", "dos_puntos_2mas", "dos_puntos_consecutivas", "triadas", "palabras", "oraciones", "media", "de", "largas_50", "cortas_8"):
    print(f"| {lab} | " + " | ".join(str(out[u][lab]) for u in U) + " | |")
print()
for u in U:
    print(u, "top2:", out[u]["top2"])
```

## Ajustes de contenido aprobados por el autor (4 nov)
1. `07_conclusiones.tex`: «no le cuesta acierto al grupo» pasa a «le cuesta poco acierto al grupo», porque en texto queda 91.0 frente a 93.6 %.
2. `Capitulo1.tex`, Justificación: la cifra de la fase 1 («supera el 90 % tras 13 interacciones») dice ahora que se midió sobre las mismas consultas que forman el directorio.
