# Lectura de jurado: estilo, estructura y patrones de texto generado

Base: `0aaa025` (rama `fases`). Alcance: Resumen, Abstract, Introducción, Capítulos 1 a 5 (los 2 a 5 desde `.tex8/secciones/`), Conclusión del objetivo general y Apéndice A. No se cambió ninguna cifra; las que se quitaron de un lugar siguen en Resultados (comprobado con un script: el parche no agrega ninguna cifra que no estuviera en la base, y la única que deja de aparecer, «36», era un derivado de 291/8 que se quitó junto con su frase). No se tocaron etiquetas `\label`, citas ni `generar_capitulos.py`.

## Dictamen

**Aprobable con los cambios de este parche.** El hilo de las cinco fases se lee de principio a fin: Cap. 1 (arco, problema en cinco partes, OE1–OE5, cinco preguntas), Cap. 3 (3.2 a 3.7, una sección por fase), Resultados (4.1.1 a 4.1.5, cada fase abre con el rótulo de su arquitectura), Discusiones y Conclusiones (una respuesta por fase). Las transiciones entre fases tienen una lógica clara: la fase 2 sale del sesgo de masa de la fase 1, la fase 3 abre con la lista de lo que cambió a la vez y la fase 4 con lo que ya se reportó en la fase 3. El texto nuevo no tiene énfasis sin respaldo ni antítesis de plantilla. Los problemas que quedaban eran estos:

1. **Repetición entre Resultados y Discusiones** (el problema más grande). Discusiones volvía a dar, con las mismas cifras, los experimentos 7, 8, 9, 10, 17, 18 y 19, las dos calibraciones, el principio de tamaño, el desglose por dominio y la comparación con la EHAM única (`06_discusion.tex:260-291`, `:339-352`, `:377-398`, `:417-424`, `:560-584`, `:603-607`, `:640-663`, `:676-681`, `:794-801`). Ahora deja la interpretación y remite a la sección de Resultados.
2. **Repetición entre Cap. 3 y Resultados**: la ablación de la fase 2 aparecía completa dos veces (`04_metodologia.tex:212-223` y `05_resultados.tex:109-119`), y la fase 5 se describía dos veces (`04:724-778` y `05:1746-1756`).
3. **Repeticiones dentro de un capítulo**: las consultas 201 a 400 y su nota al pie (`05:158-163`, repetidas en `:171-178`), el codificador por pliegue (`05:804-808`, repetido en `:826-859`), la EHAM única fuera de dominio (`06:789-792` y `:848-853`), la tercera vuelta de las diferencias del conjunto fijo (`06:892-898`) y la salvedad de las analogías (`06:257` y `:916-917`).
4. **Restos de historia de versiones**: creencia 8, «anterior a la revisión de las cifras… y se retiró» (`06:111-112`), y «protocolo corregido» (`ConclusionObjetivoGeneral.tex:46`). Los «corregido» del Apéndice A son el estado de cada carpeta, es decir, metodología, y se quedan.
5. **Términos y registro**: «transmisión» por el término definido «transacción» (`05:1537-1595`, `07:133`), el calco «verdad de terreno» (`05:1515`, `:1584`, `:1655`), «fidelidad» por «concordancia» (`07:201`) y «la segunda laptop», «etapas 6 a 8» (`07:226`).
6. **Convención de tablas**: la Tabla `tab:calibracion` (`\footnotesize`) se salía 2.9 pt del ancho (`05:199`). Era la única caja desbordada del documento.
7. **Muletilla «, así que»**: aparecía 15 veces en Resultados; quedan 9 (grep literal; el script, que solo cuenta tras coma o al inicio de oración, da 14 → 8).

**Páginas.** Compilado con XeLaTeX (TeX Live 2023) en las dos versiones: **181 → 178 páginas** (Discusiones 107–136 → 105–133; Conclusiones empieza en la 134 en vez de la 137). En texto corrido se quitan unas 1250 palabras, tres cuartas partes de Discusiones (9368 → 8433), lo que equivale a unas 4 páginas. Las tablas `[H]` de las creencias y de Resultados fijan cortes de página, y por eso el ahorro real es de 3. Hay 0 cajas `hbox` desbordadas (antes 2) y 0 referencias indefinidas. El Resumen, el Abstract y la Introducción no se tocaron y siguen en una página cada uno.

**Lo que se revisó y se deja.** «Sistemas multiagente» (`02_marco_teorico.tex:415`) nombra un campo de la literatura y no a los módulos. Los comienzos paralelos de las listas de protocolos y decisores (directo/encadenado/agregado; voto/centroide/vecino) son enumeraciones reales. «La lectura» abre 8 oraciones de Discusiones porque es un término definido (lectura B1, lectura inversa). La salvedad «cambiaron varias cosas a la vez» se repite por regla (rótulo de cada fase); solo se quitó donde se repetía dentro del mismo capítulo (`07:71-73`). El ritmo no es uniforme: la media de las oraciones va de 24 a 28 palabras, con una desviación de 14 a 19, y no se tocó.

**Para la sesión de cifras y metodología (no se tocó):** la limitación (m) daba «98.8\,\%» donde el resto dice 98.75; la frase salió con el recorte, pero conviene confirmarlo. El índice habla de 19 creencias y la Sección 4.2.1 tiene 18.

## Conteos por capítulo, antes → después

El script (`conteo.py`) está al final de este archivo. Cuenta sobre la prosa: quita comentarios, entornos `table`, `tabular`, `equation` y `align`, matemáticas en línea y comandos, y conserva los pies de figura y la prosa de las listas. Las oraciones se parten en «. ? !» seguidos de mayúscula. «así (conector)» cuenta «así,» y «así que» tras coma o al inicio de oración. «Prelim» = Resumen + Abstract + Introducción; «Cap3a/3b» = `03` y `04`; «Cap5» = `07` + `ConclusionObjetivoGeneral`. Solo se listan los patrones con alguna aparición; dieron 0 en todos los capítulos, antes y después: «sin embargo», «por lo tanto», «en este sentido», «cabe destacar/señalar», «es importante», «nótese», «de hecho», «en particular», «precisamente/justamente», «claramente/notablemente/sin duda», «robusto», «honesto», «lo que importa», «dicho de otro modo», «en otras palabras», «no X, sino Y», «versión anterior/jurado» y «agente».

| Patrón | Prelim | Cap1 | Cap2 | Cap3a(03) | Cap3b(04) | Res(05) | Disc(06) | Cap5(07+COG) | ApA | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| así (conector) | 0 | 1 | 0 | 0 | 5 | 14 → 8 | 5 → 3 | 1 | 0 | 26 → 18 |
| además | 0 | 1 | 3 | 1 | 5 | 3 | 3 → 2 | 0 | 0 | 16 → 15 |
| en cambio | 0 | 0 | 0 | 1 | 0 | 2 | 2 | 0 | 0 | 5 → 5 |
| es decir | 0 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 3 → 3 |
| por eso | 0 | 2 | 3 | 0 | 2 | 3 | 6 → 4 | 0 | 0 | 16 → 14 |
| conviene | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 2 → 2 |
| exactamente | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 3 → 3 |
| crucial/clave | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 → 1 |
| limpio/a | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 2 → 2 |
| en suma/en resumen | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 → 1 |
| a la vez | 1 | 1 | 0 | 0 | 2 | 3 | 2 | 1 | 0 | 10 → 10 |
| solo/sólo | 0 | 7 | 11 | 9 | 26 | 38 | 32 → 33 | 8 | 1 | 132 → 133 |
| también | 0 | 0 | 3 | 3 | 6 → 5 | 12 → 11 | 13 | 3 → 2 | 0 | 40 → 37 |
| «, no » | 0 | 0 | 1 | 0 | 1 | 3 | 3 | 0 | 0 | 8 → 8 |
| esta sección/este capítulo | 0 | 0 | 0 | 0 | 0 | 4 → 2 | 2 → 1 | 1 | 0 | 7 → 4 |
| Palabras | 820 | 2750 | 3086 | 2325 | 6843 → 6764 | 13519 → 13288 | 9368 → 8433 | 3436 → 3430 | 271 | |
| Oraciones | 34 | 112 | 114 | 84 | 256 → 251 | 521 → 511 | 336 → 307 | 124 | 6 | |
| Oraciones seguidas con la misma primera palabra | 1 | 8 | 8 | 6 | 16 | 37 → 36 | 35 → 32 | 3 | 0 | |
| Longitud media de oración (palabras) | 24.1 | 24.4 | 27.0 | 27.7 | 26.7 → 26.9 | 25.9 → 26.0 | 27.9 → 27.5 | 27.7 → 27.6 | 45.2 | |
| Desviación de la longitud | 10.3 | 17.0 | 13.6 | 13.7 | 19.1 → 19.2 | 14.6 → 14.5 | 16.1 → 15.8 | 16.7 | 28.3 | |

**Comienzos de oración de dos palabras con 4 o más apariciones** (antes → después):

- **Cap2**: «En la» 8, «La entropía» 4 → «En la» 8, «La entropía» 4
- **Cap3b(04)**: «En el» 6, «Con el» 5, «El experimento» 4 → «En el» 6, «Con el» 5, «El experimento» 4
- **Res(05)**: «Con el» 13, «El directorio» 9, «La Tabla» 9, «En la» 8, «Con X» 7, «Con la» 7, «Lo que» 7, «Se compararon» 6, «En las» 6, «Sobre las» 5, «En el» 5, «El sistema» 5 → «Con el» 13, «El directorio» 9, «En la» 8, «Con X» 7, «Con la» 7, «Lo que» 7, «Se compararon» 6, «La Tabla» 6, «En las» 6, «Sobre las» 5, «En el» 5, «El sistema» 5
- **Disc(06)**: «La lectura» 9, «En la» 7, «Con un» 7, «El directorio» 6, «Lo que» 6, «En imagen» 6, «En este» 6, «En las» 5, «En texto» 5, «Las cifras» 4, «Con una» 4, «En el» 4 → «La lectura» 8, «En la» 7, «El directorio» 6, «Lo que» 6, «En este» 6, «En texto» 5, «En imagen» 5, «Con un» 5, «Las cifras» 4, «En el» 4, «En las» 4, «En los» 4

«solo» (132 → 133) y «también» (40 → 37) se dejaron: casi todos son restrictivos y llevan información («solo con la clase real», «solo dentro de muestra»), y cambiarlos sería variación artificial. «Con X» es «Con $N = …$» o «Con $\iota$…», un comienzo que imponen las condiciones experimentales. El único «clave» de los preliminares es «Palabras clave».

## Cambios aplicados (viejo, nuevo y patrón)

Archivo y línea en `0aaa025`. Los capítulos 2 a 5 de `.tex_uacj/` se regeneraron con `generar_capitulos.py`, que terminó sin error: «líneas de .tex8 que no aparecen en la salida: 0».

### E01 · `.tex8/secciones/04_metodologia.tex:2`

**Patrón:** conclusión repetida (misma oración que Cap. 1, Arco de la investigación).

Viejo:
```latex
\label{sec:metodologia}

La investigación avanzó en cinco fases, y cada una partió de lo que dejó la anterior.
En adelante,
```
Nuevo:
```latex
\label{sec:metodologia}

En adelante,
```

### E02 · `.tex8/secciones/04_metodologia.tex:212`

**Patrón:** repetición entre capítulos (Cap. 3 y Resultados: mismas cifras de la ablación en 3.4 y 4.1.2).

Viejo:
```latex
\paragraph{Por qué B1.}
Con tres módulos y $N = 80$, la lectura cruda dejó a \texttt{apple} el 78.75\,\% de las
decisiones maduras y una precisión madura del 53.75\,\%.
B1 la llevó al 98.75\,\%, por encima del 97.5\,\% de la fase temprana.
De las otras condiciones solas, F llegó al 80.0\,\% y B2 al 75.0\,\%, mientras que C,
D, E32 y E64 se quedaron entre el 52.8 y el 53.75\,\%.
G, que contiene a B1, dio el 98.72\,\%.
B1 se adoptó por ser la única corrección individual que alcanzaba el techo de la fase
temprana, y es una sola operación sobre un conteo que el directorio ya guarda.
Como el directorio se evaluó sobre las consultas que lo formaron, estas cifras también
son dentro de muestra
(\texttt{results/fase1\_tres\_modulos/ablation\_mdir\_bias/ablation\_report.md}).
```
Nuevo:
```latex
\paragraph{Por qué B1.}
B1 se adoptó por ser la única corrección individual que, con $N = 80$, alcanzaba el
techo de la fase temprana, y porque es una sola operación sobre un conteo que el
directorio ya guarda.
Como el directorio se evaluó sobre las consultas que lo formaron, la comparación es
dentro de muestra; sus cifras están en la Sección~\ref{sec:fase2-resultados}.
```

### E03 · `.tex8/secciones/04_metodologia.tex:729`

**Patrón:** vaguedad («con ella» ambiguo).

Viejo:
```latex
No es la arquitectura final, y no hay ninguna corrida con ella.
```
Nuevo:
```latex
No es la arquitectura final, y el laboratorio no se volvió a correr con esta.
```

### E04 · `.tex8/secciones/05_resultados.tex:4`

**Patrón:** transición sin lógica (la remisión apuntaba a la organización de la fase 3, no a las cinco fases).

Viejo:
```latex
Los resultados siguen las cinco fases de la Sección~\ref{sec:organizacion}.
```
Nuevo:
```latex
Los resultados siguen las cinco fases de la Sección~\ref{fase:arco}.
```

### E05 · `.tex8/secciones/05_resultados.tex:115`

**Patrón:** repetición entre capítulos (recibe las dos cifras que solo daba 3.4).

Viejo:
```latex
Dividir la puntuación entre el conteo de registros de cada módulo (B1) la llevaba al
98.75\,\%, dividirla entre su raíz (B2), al 75.0\,\%, y depurar el vocabulario (F), al
80.0\,\%; el tope de registros, las consultas balanceadas y la cuantización en 32 y 64
niveles quedaban entre el 52.8 y el 53.75\,\%
(\texttt{results/fase1\_tres\_modulos/ablation\_mdir\_bias/ablation\_report.md}).
```
Nuevo:
```latex
Dividir la puntuación entre el conteo de registros de cada módulo (B1) la llevaba al
98.75\,\%, por encima del 97.5\,\% de la fase temprana; dividirla entre su raíz (B2), al
75.0\,\%, y depurar el vocabulario (F), al 80.0\,\%.
El tope de registros, las consultas balanceadas y la cuantización en 32 y 64 niveles
quedaban entre el 52.8 y el 53.75\,\%, y G, que contiene a B1, en el 98.72\,\%
(\texttt{results/fase1\_tres\_modulos/ablation\_mdir\_bias/ablation\_report.md}).
```

### E06 · `.tex8/secciones/05_resultados.tex:155`

**Patrón:** repetición dentro del capítulo (las consultas 201 a 400 y su nota se repiten en el párrafo siguiente).

Viejo:
```latex
Las reservadas son la cola de la lista de cada clase (Sección~\ref{sec:banco}), no una
muestra al azar del banco, y que superen al 93.0\,\% de la lectura B1 depende de su
composición.
El 87.7\,\% de las reservadas trae el nombre de su clase, frente al 49.8\,\% de las 400
consultas de la calibración, y en la calibración misma las consultas 201 a 400, que lo
traen en el 84.5\,\% de los casos, aciertan 195 de 200 (97.5\,\%) ya en la fase
temprana, que no usa el directorio.\footnote{Reanálisis del banco,
\texttt{results/reanalisis\_jurado/salida.md}, tablas M3.1 y M2.3. El nombre de la clase
cuenta si aparece como palabra de la consulta, también en plural.}
```
Nuevo:
```latex
Las reservadas son la cola de la lista de cada clase (Sección~\ref{sec:banco}), no una
muestra al azar del banco, y que superen al 93.0\,\% de la lectura B1 depende de su
composición.
El 87.7\,\% de ellas trae el nombre de su clase, frente al 49.8\,\% de las 400
consultas de la calibración.
```

### E07 · `.tex8/secciones/05_resultados.tex:199`

**Patrón:** convención (tabla en \footnotesize que no cabía en el ancho: 2.9 pt).

Viejo:
```latex
        B1         & División entre conteo de registros por módulo  & 90.0 & 95.8 & \textbf{93.0} \\
```
Nuevo:
```latex
        B1         & División entre conteo de registros             & 90.0 & 95.8 & \textbf{93.0} \\
```

### E08 · `.tex8/secciones/05_resultados.tex:806`

**Patrón:** repetición dentro del capítulo (el codificador por pliegue tiene su propio párrafo enseguida).

Viejo:
```latex
(Sección~\ref{sec:percepcion}); con un codificador reentrenado sin el objeto reservado,
la cobertura de punta a punta con objetos nuevos es del 87.6\,\%, con 136 falsos
enrutamientos en 3280 vistas, frente a 2 del codificador común en los mismos pliegues.
La cobertura
```
Nuevo:
```latex
(Sección~\ref{sec:percepcion}).
La cobertura
```

### E09 · `.tex8/secciones/05_resultados.tex:1009`

**Patrón:** frase que anuncia («Esta sección mide»).

Viejo:
```latex
Esta sección mide qué aporta repartir el contenido entre ocho especialistas frente a
guardarlo todo en una sola memoria.
Se construyó una EHAM única
```
Nuevo:
```latex
Para medir qué aporta repartir el contenido entre ocho especialistas frente a guardarlo
todo en una sola memoria, se construyó una EHAM única
```

### E10 · `.tex8/secciones/05_resultados.tex:1170`

**Patrón:** muletilla («, así que» al cierre de oración; 15 en el capítulo).

Viejo:
```latex
En todos los pares el solapamiento va de 0.57 a 0.65, así que en esta representación no
hay pares disjuntos.
```
Nuevo:
```latex
En todos los pares el solapamiento va de 0.57 a 0.65; en esta representación no hay
pares disjuntos.
```

### E11 · `.tex8/secciones/05_resultados.tex:1195`

**Patrón:** muletilla («así que»).

Viejo:
```latex
Ninguno tiene umbral, así que aceptan toda consulta con algún token con vector.
```
Nuevo:
```latex
Ninguno tiene umbral, y todos aceptan cualquier consulta con algún token con vector.
```

### E12 · `.tex8/secciones/05_resultados.tex:1355`

**Patrón:** muletilla («así que»).

Viejo:
```latex
Un decisor simple sobre los mismos latentes acierta al menos 631 imágenes con 2 falsos o
menos, así que en la clase de imagen el enrutamiento no agrega sobre el codificador.
```
Nuevo:
```latex
Un decisor simple sobre los mismos latentes acierta al menos 631 imágenes con 2 falsos o
menos; en la clase de imagen, el enrutamiento no agrega nada sobre el codificador.
```

### E13 · `.tex8/secciones/05_resultados.tex:1365`

**Patrón:** frase que anuncia («Esta sección la compara»).

Viejo:
```latex
Esta sección la compara con la arquitectura que guarda, junto a la memoria
```
Nuevo:
```latex
Aquí se compara con la arquitectura que guarda, junto a la memoria
```

### E14 · `.tex8/secciones/05_resultados.tex:1515`

**Patrón:** cambio de registro (calco «verdad de terreno»; en Cap. 3 es «la clase real»).

Viejo:
```latex
Lo registra la verdad de terreno en lugar del ganador temprano, y el texto se evalúa
```
Nuevo:
```latex
Se registra con la clase real como ganador, en lugar del ganador temprano, y el texto se evalúa
```

### E15 · `.tex8/secciones/05_resultados.tex:1536`

**Patrón:** término definido («transacción», no «transmisión»).

Viejo:
```latex
Se corrió con un protocolo anterior, en el que los ocho módulos registran todas las
transmisiones y sus directorios
```
Nuevo:
```latex
Se corrió con un protocolo anterior, en el que los ocho módulos registran todas las
transacciones y sus directorios
```

### E16 · `.tex8/secciones/05_resultados.tex:1553`

**Patrón:** término definido («transacción»).

Viejo:
```latex
Al reconstruir el directorio con una fracción de las transmisiones ajenas, presenciar
```
Nuevo:
```latex
Al reconstruir el directorio con una fracción de las transacciones ajenas, presenciar
```

### E17 · `.tex8/secciones/05_resultados.tex:1560`

**Patrón:** término definido («transacción»).

Viejo:
```latex
Para reconstruir un dominio ajeno bastan de 4 a 8 transmisiones presenciadas, y para
```
Nuevo:
```latex
Para reconstruir un dominio ajeno bastan de 4 a 8 transacciones presenciadas, y para
```

### E18 · `.tex8/secciones/05_resultados.tex:1570`

**Patrón:** término definido («transacción»).

Viejo:
```latex
Cuando cada módulo registra todas las transmisiones, los ocho directorios son la misma
relación.
En este experimento el ganador registra siempre lo suyo y cada otro módulo registra una
transmisión con probabilidad
```
Nuevo:
```latex
Cuando cada módulo registra todas las transacciones, los ocho directorios son la misma
relación.
En este experimento el ganador registra siempre lo suyo y cada otro módulo registra una
transacción con probabilidad
```

### E19 · `.tex8/secciones/05_resultados.tex:1584`

**Patrón:** cambio de registro («verdad de terreno»).

Viejo:
```latex
Lo registra la verdad de terreno, el directorio visual no lleva variantes, y la imagen
```
Nuevo:
```latex
El ganador de cada registro es la clase real, el directorio visual no lleva variantes, y la imagen
```

### E20 · `.tex8/secciones/05_resultados.tex:1595`

**Patrón:** término definido («transacción»).

Viejo:
```latex
protocolo; $f$: probabilidad de registrar una transmisión ajena; $r$: radio en un
```
Nuevo:
```latex
protocolo; $f$: probabilidad de registrar una transacción ajena; $r$: radio en un
```

### E21 · `.tex8/secciones/05_resultados.tex:1655`

**Patrón:** cambio de registro («verdad de terreno»).

Viejo:
```latex
La formación se repitió con directorios perspectivales de texto, con la verdad de
terreno como ganador y el ruteo transactivo
```
Nuevo:
```latex
La formación se repitió con directorios perspectivales de texto, con la clase real
como ganador y el ruteo transactivo
```

### E22 · `.tex8/secciones/05_resultados.tex:1710`

**Patrón:** muletilla («así que»).

Viejo:
```latex
\texttt{cow} (91.2\,\%), así que el ajuste del codificador borra el atributo.
```
Nuevo:
```latex
\texttt{cow} (91.2\,\%); el ajuste del codificador borra el atributo.
```

### E23 · `.tex8/secciones/05_resultados.tex:1736`

**Patrón:** muletilla («así que»).

Viejo:
```latex
Los rasgos que distinguen color, textura y pelo dentro de una clase los comparten
especies distintas, así que la percepción que ayuda al especialista junta los dominios en
el directorio.
```
Nuevo:
```latex
Los rasgos que distinguen color, textura y pelo dentro de una clase los comparten
especies distintas, y con ellos la percepción que ayuda al especialista junta los
dominios en el directorio.
```

### E24 · `.tex8/secciones/05_resultados.tex:1746`

**Patrón:** repetición entre capítulos (la apertura de 4.1.5 repetía la descripción de 3.7 y el rótulo «demostración de integración»).

Viejo:
```latex
Un laboratorio en tiempo real conectó el sistema a un micrófono y a una cámara.
Whisper \textit{small} transcribe la voz y el directorio enruta el texto; el canal
visual codifica un recorte del cuadro y lo enruta con el directorio visual del módulo de
entrada.
Se corrió con la versión v5 del sistema, de julio de 2026, con ocho módulos y tres
memorias de contenido por módulo, y no hay corridas con la arquitectura final.
Cada cifra es una sola medición, del 16 al 18 de julio, en el equipo de desarrollo, con
una GPU RTX 2050 solo para Whisper y el codificador y las memorias en CPU.
De las corridas no quedaron registros, JSON ni grabaciones, solo dos imágenes de prueba.
Es una demostración de integración y no tiene cifras de acierto
(\texttt{results/mundo\_real/}).
```
Nuevo:
```latex
Las cifras de esta fase son de la versión v5 del sistema, de julio de 2026, con ocho
módulos y tres memorias de contenido por módulo, y no de la arquitectura final
(Sección~\ref{fase5:laboratorio}).
Cada una es una sola medición, del 16 al 18 de julio, en el equipo de desarrollo.
De las corridas no quedaron registros, JSON ni grabaciones, solo dos imágenes de prueba
(\texttt{results/mundo\_real/}).
```

### E25 · `.tex8/secciones/06_discusion.tex:111`

**Patrón:** restos de historia de versiones («anterior a la revisión de las cifras», «se retiró»).

Viejo:
```latex
        \raggedright Una de ellas era anterior a la revisión de las cifras y no tenía
        fuente, y se retiró. La vigente,
```
Nuevo:
```latex
        \raggedright Una de ellas no tenía fuente en \texttt{results/} y no se cita.
        La vigente,
```

### E26 · `.tex8/secciones/06_discusion.tex:260`

**Patrón:** repetición entre capítulos (Resultados y Discusiones: cifras del experimento 7 repetidas de 4.1.4).

Viejo:
```latex
Para enrutar, el directorio se comporta como un índice que no mezcla lo que registra.
Un solo directorio con las pistas de texto y las de imagen en coordenadas disjuntas
enruta el texto igual que el directorio de texto solo (96.2\,\% en los dos), y sus
puntuaciones de texto son idénticas con o sin registros de imagen (experimento~7).
La relación acumula por par de rasgo y módulo, sin ningún término entre rasgos, y por
eso las dos mitades no forman una representación compartida.
Lo único que las acopla es el denominador de B1 cuando cuenta registros de cualquier
modalidad: con él, sumar imágenes baja el texto del 96.2 al 91.2\,\%, y al 88.8\,\% si
las imágenes son desiguales entre módulos; leído de la relación, el conteo de texto
deja el 96.2\,\%.
Con una consulta que trae texto e imagen, la mitad sin soporte veta a la otra, y el
directorio unificado acierta el 23.8\,\%, frente al 100.0\,\% de dos directorios
separados.
El texto de este experimento usa 32 niveles y se evalúa sobre las consultas que
formaron el directorio.

Leído al revés, del módulo a la pista, el directorio devuelve el dominio del módulo
(experimento~8).
La lectura acierta la clase con el dominio propio (80 de 80) y con uno ajeno que el
módulo presenció (112 de 112).
En el directorio, el especialista no tiene ningún privilegio.
Lo que devuelve es una envolvente y no un ejemplar: queda de 2.9 a 5.5 veces más lejos
de cualquier instancia real que las instancias entre sí.
Ante identidades que no pudieron ocurrir, como dos módulos ganando la misma pista, no
responde en ninguna de las 10 lecturas de cada una, y la falla es siempre callar.
Basta haber presenciado un registro ajeno para que reconstruya ese dominio el 59\,\% de
las veces, y con ocho, el 100\,\%, con la clase correcta desde el primero.
Más registros la ensanchan: la distancia a la instancia real más cercana va de 3.3 con
un registro por módulo a 20.5 con 800.
En ese experimento todos los módulos registran todas las transacciones y el directorio
visual tiene 981 registros sin variantes; el mecanismo no depende de eso, pero las
cifras no son del sistema final.
```
Nuevo:
```latex
Para enrutar, el directorio se comporta como un índice que no mezcla lo que registra.
Un solo directorio con pistas de texto y de imagen en coordenadas disjuntas enruta cada
modalidad igual que dos directorios separados, porque la relación acumula por par de
rasgo y módulo, sin ningún término entre rasgos (experimento~7,
Sección~\ref{sec:fase4-indice}).
Las dos mitades solo se tocan en el denominador de B1, cuando cuenta registros de las
dos, y en el veto conjuntivo, por el que la mitad sin soporte de una consulta emparejada
tumba a la otra; ninguno de los dos acoples es una representación compartida.

Leído al revés, del módulo a la pista, el directorio devuelve el dominio del módulo,
tanto el propio como uno ajeno que el módulo solo presenció (experimento~8).
En el directorio, el especialista no tiene ningún privilegio.
Lo que devuelve es una envolvente y no un ejemplar, más lejos de cualquier instancia
real que las instancias entre sí, y ante identidades que no pudieron ocurrir la falla es
siempre callar.
Un solo registro ajeno presenciado basta para empezar a reconstruir un dominio, y más
registros ensanchan la envolvente.
El experimento usa un protocolo anterior al final; el mecanismo no depende de eso, pero
las cifras no son del sistema final (limitación (o)).
```

### E27 · `.tex8/secciones/06_discusion.tex:340`

**Patrón:** repetición entre capítulos (cifras de las dos calibraciones, ya en 4.1.2).

Viejo:
```latex
    Con 10 consultas por dominio, la precisión madura queda en 81.2\,\%, y con unas 50
    llega al 93.0\,\%, las dos sobre las consultas que formaron el directorio.
    Sobre las mismas consultas, la diferencia entre la lectura normalizada y la fase
    temprana, que no usa el directorio, es de 0, +4.0, +5.5 y +3.0 puntos con 50, 100,
    200 y 400 consultas de formación (Sección~\ref{sec:calibracion}).
    Sobre un conjunto fijo de 120 consultas que nunca registran en el directorio, la
    precisión madura con la lectura normalizada sube del 78.9 al 91.0\,\% entre 50 y 291
    consultas de formación, así que la formación mejora la decisión en consultas que no
    vio.
    Con ese crecimiento la madura alcanza a la fase temprana, que sobre esas consultas
    acierta el 89.7\,\%, sin una ventaja que se sostenga entre sorteos; la diferencia pasa de $-10.7$
    puntos con 50 consultas a $+0.2$ con 200 y $+1.3$ con 291, y con 291 va de $-0.8$ a
    $+6.7$ según qué consultas se evalúen (Sección~\ref{sec:calibracion-fija}).
```
Nuevo:
```latex
    Con 10 consultas por dominio, la precisión madura queda en 81.2\,\%, y con unas 50
    llega al 93.0\,\%, las dos sobre las consultas que formaron el directorio; la mayor
    parte de ese ascenso es el de la fase temprana, que no usa el directorio
    (Sección~\ref{sec:calibracion}).
    Sobre un conjunto fijo de 120 consultas que nunca registran en el directorio, la
    formación mejora la decisión en consultas que no vio, pero solo hasta alcanzar a la
    fase temprana, sin una ventaja que se sostenga entre sorteos
    (Sección~\ref{sec:calibracion-fija}).
```

### E28 · `.tex8/secciones/06_discusion.tex:378`

**Patrón:** repetición entre capítulos (experimento 10 con las mismas cifras y la misma frase final que 4.1.4).

Viejo:
```latex
Cuando cada módulo registra solo una parte de lo ajeno, el grupo recupera el
enrutamiento del registro completo (experimento~10).
En imagen, un módulo sin soporte pasa la consulta a los módulos que conoce, en orden de
cuántos registros les vio ganar.
Así el grupo acierta el 81.9\,\% de las imágenes de prueba sin ningún error, lo mismo
que el registro completo, aunque cada módulo presencie al azar uno de cada 64 registros
ajenos y los directorios difieran en el 83\,\% de sus celdas.
El costo son 3.56 consultas adicionales en promedio.
En texto, pasar la consulta no basta, porque decide el primero con soporte y la decisión
de texto es comparativa.
Con uno de cada 64 registros, el encadenado se equivoca en el 20.7\,\% de las consultas
reservadas.
Sumar las puntuaciones normalizadas de todos los conocidos recupera la comparación:
91.0\,\% con uno de cada 32 registros, frente al 93.6\,\% del registro completo, y
94.3\,\% con uno de cada cuatro, cuatro consultas de diferencia en una de tres semillas.
Encadenar da alcance y sumar da comparación.
En un anillo en que cada módulo conoce solo a sus dos vecinos, la suma, que no sale de
la vecindad, acierta el 56.4\,\% de las reservadas, y el encadenado, que llega a todo el
grupo por transitividad, el 73.9\,\%.
Esta corrida usa el directorio visual sin variantes, por eso el registro completo
acierta el 81.9\,\% y no el 96.2\,\%, y el registro lo dicta la clase verdadera.
```
Nuevo:
```latex
Cuando cada módulo registra solo una parte de lo ajeno, el grupo recupera el
enrutamiento del registro completo (experimento~10,
Tabla~\ref{tab:fase4-perspectiva}).
En imagen basta con que un módulo sin soporte pase la consulta a los módulos que
conoce, en orden de cuántos registros les vio ganar: el grupo iguala al registro
completo aunque cada módulo presencie al azar uno de cada 64 registros ajenos, y lo
paga con consultas adicionales.
En texto, pasar la consulta no basta, porque decide el primero con soporte y la decisión
de texto es comparativa; sumar las puntuaciones normalizadas de todos los conocidos
recupera la comparación.
En un anillo en que cada módulo conoce solo a sus dos vecinos ocurre lo contrario, porque
la suma no sale de la vecindad y el encadenado llega a todo el grupo por transitividad.
Encadenar da alcance y sumar da comparación.
La corrida usa el directorio visual sin variantes y un registro dictado por la clase
verdadera (limitación (o)).
```

### E29 · `.tex8/secciones/06_discusion.tex:417`

**Patrón:** repetición entre capítulos (experimento 9, cifras de 4.1.4).

Viejo:
```latex
Al quitar un módulo, el directorio le sigue enviando las consultas de su dominio
(experimento~9): en texto, 229 de las 411 consultas del banco (55.7\,\%), con un
directorio formado con las 16 consultas de la fase temprana, y en imagen, 65 de 80.
El grupo pierde la respuesta y conserva la ubicación.
Darle la consulta al segundo mejor del directorio es la peor política.
De texto a imagen responde el 24.5\,\% de las veces, siempre con la clase del sustituto
(\texttt{tomato} por \texttt{apple}, \texttt{cow} por \texttt{horse}), y de imagen a
texto no responde nunca, porque la imagen ajena no cabe en su contenido.
```
Nuevo:
```latex
Al quitar un módulo, el directorio le sigue enviando las consultas de su dominio
(experimento~9, Sección~\ref{sec:fase4-perspectiva}), y el grupo pierde la respuesta y
conserva la ubicación.
Darle la consulta al segundo mejor del directorio es la peor política.
De texto a imagen responde el 24.5\,\% de las veces, siempre con la clase del sustituto
(\texttt{tomato} por \texttt{apple}, \texttt{cow} por \texttt{horse}), y de imagen a
texto no responde nunca, porque la imagen ajena no cabe en su contenido.
```

### E30 · `.tex8/secciones/06_discusion.tex:723`

**Patrón:** repetición dentro del capítulo (decisores de imagen y codificador sin clase, repetidos en 4.2.8 y en la limitación (k)).

Viejo:
```latex
En imagen, un centroide o un vecino más cercano sobre los mismos latentes aciertan de
652 a 655 de las 656 imágenes de prueba, sin rechazar ninguna, frente a 631 del sistema
(Sección~\ref{sec:lineas-base}); la separación entre clases la hace el codificador.
Con un codificador entrenado sin la pérdida de clase y el mismo mecanismo, el
enrutamiento visual baja del 96.2 al 70.4\,\% y los falsos enrutamientos suben de 2 a
169 de 656 (Sección~\ref{sec:codificador-sin-clase}).
```
Nuevo:
```latex
En imagen, la separación entre clases la hace el codificador: decisores simples sobre
los mismos latentes aciertan más imágenes que el sistema
(Sección~\ref{sec:disc-lineas-base}), y sin la pérdida de clase el mismo mecanismo
enruta mucho peor (limitación (k)).
```

### E31 · `.tex8/secciones/06_discusion.tex:759`

**Patrón:** repetición entre capítulos (cifras de color de la fase 5, ya en 4.1.5).

Viejo:
```latex
El corrimiento de color de la impresora y la cámara llevó a una corrección que solo
actúa tras un rechazo, y en simulación enruta bien 22, 18 y 15 de 24 imágenes con
degradación nula, media y fuerte.
```
Nuevo:
```latex
El corrimiento de color de la impresora y la cámara llevó a una corrección que solo
actúa tras un rechazo y que, en simulación, recupera buena parte de las imágenes
degradadas (Sección~\ref{sec:fase5-resultados}).
```

### E32 · `.tex8/secciones/06_discusion.tex:848`

**Patrón:** repetición dentro del capítulo (EHAM única fuera de dominio, ya dicho al abrir 4.2.8).

Viejo:
```latex
La ventaja de este rechazo aparece frente a un almacén único.
La EHAM única acepta 2, 2, 5 y 8 de las 40 con 25, 50, 100 y 200 imágenes por clase, y
el protocolo con doble compuerta 2 en todos los cortes (Sección~\ref{sec:eham-unica});
la diferencia es significativa con 200 imágenes por clase ($p = 0.031$) y no con 100
($p = 0.25$), y la segunda compuerta se decidió después de ver esas consultas
(limitación (g)).
```
Nuevo:
```latex
La ventaja de este rechazo aparece frente a un almacén único, que acepta más consultas
ajenas cuanto más contiene (Sección~\ref{sec:eham-unica}).
```

### E33 · `.tex8/secciones/06_discusion.tex:893`

**Patrón:** repetición dentro del capítulo (tercera vez que se dan las diferencias del conjunto fijo).

Viejo:
```latex
Con un conjunto evaluado fijo, el directorio formado con unas 200 consultas toma la
misma decisión que la fase temprana en el 92.5\,\% de las consultas que no vio (sorteo
principal), con un acierto equivalente.
La diferencia con la temprana es de $+0.2$ puntos con 200 consultas de formación y de
$+1.3$ con 291, y ninguna diferencia positiva se sostiene entre sorteos
(Sección~\ref{sec:calibracion-fija}).
```
Nuevo:
```latex
Con un conjunto evaluado fijo, el directorio formado con unas 200 consultas toma la
misma decisión que la fase temprana en el 92.5\,\% de las consultas que no vio (sorteo
principal), con un acierto equivalente y sin una diferencia positiva que se sostenga
entre sorteos (Sección~\ref{sec:calibracion-fija}).
```

### E34 · `.tex8/secciones/06_discusion.tex:915`

**Patrón:** conclusión repetida (la salvedad de las analogías ya abre 4.2.2 «para esta sección y las siguientes»).

Viejo:
```latex
pertenencia al vocabulario, y en imagen depende del umbral de energía $\tau$.
Como en las Secciones~\ref{sec:disc-wegner} y~\ref{sec:disc-una-memoria}, las analogías
de esta sección son estructurales, no causales.
```
Nuevo:
```latex
pertenencia al vocabulario, y en imagen depende del umbral de energía $\tau$.
```

### E35 · `.tex8/secciones/06_discusion.tex:1119`

**Patrón:** repetición entre capítulos (curvas de formación de 3 y 8 módulos, ya en 4.1.3).

Viejo:
```latex
Con tres módulos, la precisión madura cruza el 90\,\% tras 13 interacciones en orden
intercalado y termina en 98.8\,\%; con ocho y 10 consultas por clase, ninguna condición
llega al 90\,\% y todas terminan en 81.2\,\% (Sección~\ref{sec:formacion}).
Esa diferencia no se puede atribuir al número de módulos.
```
Nuevo:
```latex
De ahí que la diferencia entre las curvas de formación con tres y con ocho módulos
(Sección~\ref{sec:formacion}) no se pueda atribuir al número de módulos.
```

### E36 · `.tex8/secciones/07_conclusiones.tex:72`

**Patrón:** conclusión repetida (la lista de cambios del escalado se da cuatro párrafos arriba).

Viejo:
```latex
81.2\,\% con ocho, no se puede atribuir al número de módulos, porque en el paso cambiaron
también el codificador, la cuantización, las memorias, el banco y el mediador.
```
Nuevo:
```latex
81.2\,\% con ocho, no se puede atribuir al número de módulos, por los cambios simultáneos
del escalado.
```

### E37 · `.tex8/secciones/07_conclusiones.tex:133`

**Patrón:** término definido («transacción»).

Viejo:
```latex
con una de cada 64 transmisiones ajenas presenciadas); en texto lo iguala sumar los
```
Nuevo:
```latex
con una de cada 64 transacciones ajenas presenciadas); en texto lo iguala sumar los
```

### E38 · `.tex8/secciones/07_conclusiones.tex:201`

**Patrón:** término definido (la métrica es la concordancia temprana-madura, no la fidelidad).

Viejo:
```latex
También cambió la fidelidad de 10 de 10 del primer prototipo, que contaba dos rechazos
como coincidencias.
```
Nuevo:
```latex
También cambió la concordancia de 10 de 10 del primer prototipo, que contaba dos
rechazos como coincidencias.
```

### E39 · `.tex8/secciones/07_conclusiones.tex:226`

**Patrón:** cambio de registro y vaguedad («la segunda laptop», «etapas 6 a 8» sin definir).

Viejo:
```latex
    Con los tiempos de las etapas 6 a 8 medidos en septiembre en la segunda laptop, cada
    número de módulos y semilla costaría unos 17 minutos.
```
Nuevo:
```latex
    Con los tiempos de la fase temprana, el hemisferio visual y la fase madura, medidos en
    septiembre en otra computadora portátil, cada número de módulos y semilla costaría
    unos 17 minutos.
```

### E40 · `.tex_uacj/ConclusionObjetivoGeneral.tex:45`

**Patrón:** término definido (en el resto del reporte es «protocolo final»).

Viejo:
```latex
anteriores al sistema final, y la pérdida de un miembro está por repetirse con el
protocolo corregido.
```
Nuevo:
```latex
anteriores al sistema final, y la pérdida de un miembro está por repetirse con el
protocolo final.
```

### E41 · `.tex8/secciones/05_resultados.tex:580`

**Patrón:** repetición dentro del capítulo (cifras de las dos calibraciones y de la fase 1, ya en 4.1.1 y 4.1.2).

Viejo:
```latex
La calibración llega al 93.0\,\% con las 400 primeras consultas, pero sobre otras
consultas, más fáciles, en las que la fase temprana ya acierta el 90.0\,\%
(Sección~\ref{sec:calibracion}).
Con un conjunto evaluado fijo, formar el directorio con más interacciones sube la
precisión madura del 78.9 al 91.0\,\% entre unas 6 y 36 consultas de formación por
clase (50 y 291 en total), hasta el nivel de la fase temprana sobre esas consultas
(89.7\,\%), sin una ventaja que se sostenga entre sorteos
(Sección~\ref{sec:calibracion-fija}).
Con tres módulos, la misma curva, sobre 80 consultas de unas 27 por clase, cruzaba el
90\,\% tras 13 interacciones y terminaba en el 98.75\,\%
(Sección~\ref{sec:fase1-resultados}).
Entre las dos corridas cambiaron también el banco, el codificador, la cuantización y el
registro del directorio, así que la diferencia no se atribuye al número de módulos.
```
Nuevo:
```latex
La calibración llega al 93.0\,\% con las 400 primeras consultas, que son más fáciles, y
con un conjunto evaluado fijo la madura solo alcanza a la temprana
(Secciones~\ref{sec:calibracion} y~\ref{sec:calibracion-fija}).
Con tres módulos, la misma curva cruzaba el 90\,\% tras 13 interacciones
(Sección~\ref{sec:fase1-resultados}), pero entre las dos corridas cambiaron también el
banco, el codificador, la cuantización y el registro del directorio, y la diferencia no
se atribuye al número de módulos.
```

### E42 · `.tex8/secciones/06_discusion.tex:560`

**Patrón:** repetición entre capítulos (Resultados y Discusiones: cifras ya dadas en 4.1.2, calibración).

Viejo:
```latex
La brecha cruda-B1 es de 7.8 puntos con ocho módulos (85.2\,\% frente a 93.0\,\%), y la
entropía del directorio es alta incluso con la lectura cruda (2.974 de 3.000 bits).
Los conteos del directorio están casi balanceados, y el sesgo está en la
\emph{lectura}, donde B1 actúa.
La entropía no dice si el directorio está especializado; eso lo dice la información
mutua entre dominio y ganador, que con el mismo directorio pasa de 2.438 bits con la
lectura cruda a 2.649 con B1 (Sección~\ref{sec:calibracion}).
Con $N = 400$, las demás condiciones (B2, C, D, E32, E64) quedan por debajo de B1, y la
combinación G, que suma correcciones a B1, gana medio punto sobre otras consultas, más
fáciles; sobre las suyas, suma a la fase temprana lo mismo que B1, unos 3 puntos
(Sección~\ref{sec:calibracion}).
```
Nuevo:
```latex
Con ocho módulos, la entropía del directorio es casi máxima incluso con la lectura
cruda, y los conteos están casi balanceados; el sesgo está en la \emph{lectura}, donde
B1 actúa.
La entropía no dice si el directorio está especializado; eso lo dice la información
mutua entre dominio y ganador, que con el mismo directorio sube con B1.
Las correcciones que se suman a B1 no agregan nada que se sostenga: G gana medio punto
sobre otras consultas, más fáciles, y sobre las suyas suma a la fase temprana lo mismo
que B1 (Sección~\ref{sec:calibracion}).
```

### E43 · `.tex8/secciones/06_discusion.tex:574`

**Patrón:** repetición entre capítulos (Resultados y Discusiones: cifras ya dadas en 4.1.2, principio de tamaño).

Viejo:
```latex
Una lectura que, entre los módulos que contienen la pista, elige al de envolvente más
estrecha (la menor suma, sobre las coordenadas, del logaritmo del número de niveles con
soporte), a la que el experimento~22 llama principio de tamaño, decide igual que B1
sobre los mismos directorios.
En imagen acierta el 96.3\,\% de las 656 imágenes de prueba, frente al 96.2\,\% de B1,
con una sola decisión distinta, y en texto el 28.5\,\%, frente al 28.7\,\%, con 8 de 411
decisiones distintas.
Los directorios de texto de esa comparación se formaron solo con las 16 consultas de la
fase temprana, y por eso rechazan el 59.4\,\%; la comparación entre lecturas usa los
mismos directorios y vale igual, pero con directorios de texto bien formados no se
corrió.
```
Nuevo:
```latex
Una lectura que, entre los módulos que contienen la pista, elige al de envolvente más
estrecha, a la que el experimento~22 llama principio de tamaño, decide igual que B1
sobre los mismos directorios, salvo en una de 656 imágenes y en 8 de 411 consultas
(Sección~\ref{sec:fase2-tamano}); con directorios de texto formados con más consultas
no se probó.
```

### E44 · `.tex8/secciones/06_discusion.tex:604`

**Patrón:** repetición entre capítulos (Resultados y Discusiones: cifras ya dadas en 4.1.2, desglose por dominio).

Viejo:
```latex
Con la lectura normalizada, \texttt{car}, \texttt{cow}, \texttt{cup} y
\texttt{tomato} quedan entre 98.0 y 100.0\,\% y \texttt{dog} en 93.9\,\%;
\texttt{pear} (76.0\,\%), \texttt{horse} (88.0\,\%) y \texttt{apple} (88.2\,\%)
pierden hacia la vecina con la que comparten etiquetas.
```
Nuevo:
```latex
Con la lectura normalizada, las tres clases que quedan bajo el 90\,\% pierden hacia la
vecina con la que comparten etiquetas (Figura~\ref{fig:dominio}).
```

### E45 · `.tex8/secciones/06_discusion.tex:641`

**Patrón:** repetición entre capítulos (Resultados y Discusiones: cifras ya dadas en 4.1.4, experimento 17).

Viejo:
```latex
concreta solo a medias (experimento~17).
La primera palabra evocada está en el vocabulario de la clase en el 96.0\,\% de las
lecturas, pero es el nombre de la clase en el 48.0\,\%, y sale la misma en tres
recuerdos solo en el 38.9\,\% de las imágenes.
El resultado sigue al llenado, que empareja cada imagen con la siguiente palabra del
vocabulario de su clase.
Cuando a cada objeto se le asigna una palabra propia y todas sus vistas se registran con
ella, la memoria acierta esa palabra en el 40.8\,\% de las vistas nuevas (azar del
10\,\%) y en el 51.2\,\% de las vistas que registró: distingue objetos dentro de la
clase, pero los objetos de una clase se pisan en la envolvente.
```
Nuevo:
```latex
concreta solo a medias (experimento~17, Sección~\ref{sec:fase4-imagen-palabra}).
El resultado sigue al llenado, que empareja cada imagen con la siguiente palabra del
vocabulario de su clase.
Cuando a cada objeto se le asigna una palabra propia, la memoria la acierta por encima
del azar y lejos de siempre: distingue objetos dentro de la clase, pero los objetos de
una clase se pisan en la envolvente.
```

### E46 · `.tex8/secciones/06_discusion.tex:652`

**Patrón:** repetición entre capítulos (Resultados y Discusiones: cifras ya dadas en 4.1.4, experimentos 17 y 18).

Viejo:
```latex
Con el color, la memoria responde lo común.
En vistas nuevas de objetos conocidos, la lectura normalizada acierta el 74.4\,\%, frente
al 55.5\,\% de responder siempre el color más registrado del módulo.
En objetos nuevos, la lectura por soporte acierta el 57.8\,\%, frente al 49.5\,\% de
esa base, y los objetos de
color minoritario fallan: una manzana verde se responde como roja.
Con un atributo visible, como el patrón, el pelo o el techo (experimento~18), pasa lo
mismo.
En vistas nuevas de objetos conocidos, la lectura normalizada separa algo (de 62.7 a
72.3\,\% balanceado), y en objetos nuevos la memoria responde el valor mayoritario en el
98 al 99\,\% de las vistas y acierta el minoritario en el 1 al 6\,\%.
En las vacas, con cuatro objetos manchados y cuatro lisos, acierta el 8\,\%.
```
Nuevo:
```latex
Con el color, la memoria responde lo común.
Supera a responder siempre el color más registrado del módulo, pero en objetos nuevos
los de color minoritario fallan: una manzana verde se responde como roja.
Con un atributo visible, como el patrón, el pelo o el techo (experimento~18), pasa lo
mismo, y en objetos nuevos la memoria responde casi siempre el valor mayoritario del
módulo.
```

### E47 · `.tex8/secciones/06_discusion.tex:677`

**Patrón:** repetición entre capítulos (Resultados y Discusiones: cifras ya dadas en 4.1.4, experimento 19).

Viejo:
```latex
ajuste), el índice pierde mucho y el especialista gana poco (experimento~19).
El enrutamiento de las 656 imágenes de prueba baja del 96.2 al 80.5\,\%, los falsos
enrutamientos suben de 2 a 83 y, con objetos nuevos, la cobertura de punta a punta
baja del 89.2 al 60.8\,\%; el atributo de objetos nuevos queda unos 5 puntos sobre el
azar.
```
Nuevo:
```latex
ajuste), el índice pierde mucho y el especialista gana poco (experimento~19): el
enrutamiento de prueba baja del 96.2 al 80.5\,\%, y el atributo de objetos nuevos queda
unos 5 puntos sobre el azar.
```

### E48 · `.tex8/secciones/06_discusion.tex:795`

**Patrón:** repetición entre capítulos (Resultados y Discusiones: cifras ya dadas en 4.1.3, comparación con una sola EHAM).

Viejo:
```latex
Sobre el total de las 171 consultas reservadas, contando la falta de respuesta como
fallo, la diferencia entre el protocolo y la EHAM única es de $-0.7$ puntos con 50 y con
100 imágenes por clase y de $-0.1$ con 200, con intervalos de 95\,\% por remuestreo de
consultas que incluyen el cero.
Con 25, la EHAM única acierta 4.4 puntos más ($[-8.1, -0.9]$), porque el directorio
todavía enruta peor (93.2\,\% de enrutamiento correcto;
Sección~\ref{sec:eham-unica}).
```
Nuevo:
```latex
Sobre el total de las 171 consultas reservadas, contando la falta de respuesta como
fallo, la diferencia entre el protocolo y la EHAM única tiene intervalos que incluyen el
cero desde 50 imágenes por clase; con 25 gana la EHAM única, porque el directorio
todavía enruta peor (Sección~\ref{sec:eham-unica}).
```

### E49 · `.tex8/secciones/06_discusion.tex:452`

**Patrón:** repetición dentro del capítulo (la limitación (f) da las mismas cifras).

Viejo:
```latex
Si el codificador tampoco vio el objeto, la cobertura queda en 87.6\,\% y el fallo deja
de ser solo rechazo: hay 136 falsos enrutamientos en 3280 vistas, frente a 2 con el
codificador común (limitación (f)).
```
Nuevo:
```latex
Si el codificador tampoco vio el objeto, el fallo deja de ser solo rechazo
(limitación (f)).
```

### E50 · `.tex8/secciones/06_discusion.tex:955`

**Patrón:** repetición entre capítulos (Resultados y Discusiones: cifras ya dadas en 4.1.3, hemisferio visual).

Viejo:
```latex
cada una cede solo con sus propias variantes (Sección~\ref{sec:hemisferio-visual},
sobre las 656 imágenes de prueba): registrar en el directorio 16 variantes por
percepción, en lugar de una, lleva su aceptación de 73.6 a 96.2\,\%; llenar el
contenido con 16 variantes por imagen, en
lugar de 4, lleva la respuesta de la heteroasociativa de 76 a 96\,\%; con las dos, la
cobertura de punta a punta (enrutamiento correcto y respuesta) pasa de 66.5 a
94.5\,\%, con rendimiento decreciente por escalón de variantes.
```
Nuevo:
```latex
cada una cede solo con sus propias variantes, con rendimiento decreciente por escalón
de variantes (Sección~\ref{sec:hemisferio-visual}).
```

### E51 · `.tex8/secciones/06_discusion.tex:1025`

**Patrón:** dos puntos en serie y repetición (cifras de objetos nuevos ya en 4.1.3).

Viejo:
```latex
Con objetos nuevos, la cobertura de punta a punta baja del 95.5 al 89.2\,\%
(Sección~\ref{sec:objetos-nuevos}), pero en esa medición el codificador había visto
vistas de todos los objetos.
Con un codificador reentrenado sin el objeto reservado, la cobertura con objetos nuevos
es del 87.6\,\%, y el fallo ya no es solo rechazo: hay 136 falsos enrutamientos en 3280
vistas, frente a 2 con el codificador común en los mismos pliegues.
```
Nuevo:
```latex
Con objetos nuevos, la cobertura de punta a punta baja del 95.5 al 89.2\,\%, pero en
esa medición el codificador había visto vistas de todos los objetos; reentrenado sin el
objeto reservado, el fallo ya no es solo rechazo, y los falsos enrutamientos pasan de 2
a 136 en 3280 vistas (Sección~\ref{sec:objetos-nuevos}).
```

### E52 · `.tex8/secciones/06_discusion.tex:1092`

**Patrón:** repetición entre capítulos (Resultados y Discusiones: cifras ya dadas en 4.1.3, codificador sin pérdida de clase).

Viejo:
```latex
Con un codificador entrenado sin esa pérdida, el enrutamiento de las 656 imágenes de
prueba es del 70.4\,\% (frente al 96.2\,\%), y la cobertura de punta a punta con
objetos nuevos, del 59.3\,\% (frente al 89.2\,\%).
El fallo deja además de ser rechazo, porque los falsos enrutamientos de prueba pasan de
2 a 169 de 656 y el rechazo queda casi igual (3.8 frente a 3.5\,\%;
Sección~\ref{sec:codificador-sin-clase}).
```
Nuevo:
```latex
Con un codificador entrenado sin esa pérdida, el enrutamiento de las 656 imágenes de
prueba baja del 96.2 al 70.4\,\%, y el fallo deja de ser rechazo, porque los falsos
enrutamientos pasan de 2 a 169 de 656 (Sección~\ref{sec:codificador-sin-clase}).
```

### E53 · `.tex8/secciones/05_resultados.tex:333`

**Patrón:** comienzo repetido («La Tabla~… da los resultados»; 9 comienzos con «La Tabla» en el capítulo).

Viejo:
```latex
su clase queda entre el 46 y el 55\,\% para todo $N$.
La Tabla~\ref{tab:calibracion-fija} da los resultados.
```
Nuevo:
```latex
su clase queda entre el 46 y el 55\,\% para todo $N$
(Tabla~\ref{tab:calibracion-fija}).
```

### E54 · `.tex8/secciones/05_resultados.tex:508`

**Patrón:** comienzo repetido («La Tabla~… da los resultados»; 9 comienzos con «La Tabla» en el capítulo).

Viejo:
```latex
$\kappa \in \{0, 1.755, 1.801, 1.844, 1.937, 2.056, 2.107\}$.
La Tabla~\ref{tab:grid-iota-kappa} muestra la precisión temprana y el rechazo.
```
Nuevo:
```latex
$\kappa \in \{0, 1.755, 1.801, 1.844, 1.937, 2.056, 2.107\}$
(Tabla~\ref{tab:grid-iota-kappa}).
```

### E55 · `.tex8/secciones/05_resultados.tex:1202`

**Patrón:** comienzo repetido («La Tabla~… da los resultados»; 9 comienzos con «La Tabla» en el capítulo).

Viejo:
```latex
Se evaluaron las 400 consultas de la calibración, las 80 del protocolo completo y las
171 reservadas de la comparación con una sola EHAM (Sección~\ref{sec:eham-unica}),
además de las 40 consultas fuera de dominio.
Esas 40 se escribieron sin palabras del vocabulario, salvo las 12 de la sonda de rechazo
(Sección~\ref{sec:proto-completo}), que son anteriores a esa regla.
La Tabla~\ref{tab:lineas-base-texto} da los resultados.
```
Nuevo:
```latex
Se evaluaron las 400 consultas de la calibración, las 80 del protocolo completo y las
171 reservadas de la comparación con una sola EHAM (Sección~\ref{sec:eham-unica}),
además de las 40 consultas fuera de dominio (Tabla~\ref{tab:lineas-base-texto}).
Esas 40 se escribieron sin palabras del vocabulario, salvo las 12 de la sonda de rechazo
(Sección~\ref{sec:proto-completo}), que son anteriores a esa regla.
```

## Script de conteo

```python
"""Cuenta muletillas, énfasis, anuncios y comienzos repetidos por capítulo.
Uso: python conteo.py <raiz_repo> [--json salida]
Prosa: quita comentarios, entornos table/tabular/equation/align/figure (salvo caption),
matemáticas en línea y comandos; las oraciones se parten por . ? ! seguidos de mayúscula."""
import re, sys, json, collections
from pathlib import Path
R = Path(sys.argv[1])
CAPS = {
 "Prelim": [".tex_uacj/Resumen.tex", ".tex_uacj/Abstract.tex", ".tex_uacj/Introduccion.tex"],
 "Cap1": [".tex_uacj/Capitulo1.tex"],
 "Cap2": [".tex8/secciones/02_marco_teorico.tex"],
 "Cap3a(03)": [".tex8/secciones/03_arquitectura.tex"],
 "Cap3b(04)": [".tex8/secciones/04_metodologia.tex"],
 "Res(05)": [".tex8/secciones/05_resultados.tex"],
 "Disc(06)": [".tex8/secciones/06_discusion.tex"],
 "Cap5(07+COG)": [".tex8/secciones/07_conclusiones.tex", ".tex_uacj/ConclusionObjetivoGeneral.tex"],
 "ApA": [".tex_uacj/ApendiceA.tex"],
}
MUL = {
 "así (conector)": r"(?:^|[.;:]\s+|,\s*)así[, ]",
 "además": r"\bademás\b", "en cambio": r"\ben cambio\b", "es decir": r"\bes decir\b",
 "por eso": r"\bpor eso\b", "por lo tanto": r"\bpor lo tanto\b", "sin embargo": r"\bsin embargo\b",
 "en este sentido": r"\ben este sentido\b", "cabe": r"\bcabe (?:destacar|señalar|notar|precisar)",
 "es importante": r"\bes importante\b", "conviene": r"\bconviene\b", "nótese": r"\bn[óo]tese\b",
 "de hecho": r"\bde hecho\b", "en particular": r"\ben particular\b",
 "precisamente/justamente": r"\b(?:precisamente|justamente)\b", "exactamente": r"\bexactamente\b",
 "claramente/notablemente": r"\b(?:claramente|notablemente|sin duda)\b",
 "crucial/clave": r"\b(?:crucial|clave)\b", "robusto/a": r"\brobust[oa]s?\b",
 "limpio/a": r"\blimpi[oa]s?\b", "honesto": r"\bhonest[oa]s?\b",
 "en suma/en resumen": r"\ben (?:suma|resumen)\b", "lo que importa": r"\blo que importa\b",
 "dicho de otro modo": r"\bdicho de otro modo\b", "en otras palabras": r"\ben otras palabras\b",
 "a la vez": r"\ba la vez\b", "solo/sólo": r"\bs[oó]lo\b", "también": r"\btambién\b",
 "«no X, sino Y»": r"\bno [^.;:]{1,60}?, sino\b", "«, no »": r"\w, no (?:el|la|los|las|un|una|de|del|en|por|al|a)\b",
 "esta sección/este capítulo": r"\b(?:esta sección|este capítulo|esta subsección|este apartado)\b",
 "versión anterior/jurado": r"\b(?:versi[oó]n anterior|tras el jurado|del jurado|antes dec[ií]a|ahora dice)\b",
 "agente": r"\bagentes?\b",
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
out = {}
for cap, fs in CAPS.items():
    txt = prosa("\n".join((R / f).read_text(encoding="utf-8") for f in fs))
    low = txt.lower()
    ors = oraciones(txt)
    m = {k: len(re.findall(p, low, re.M)) for k, p in MUL.items()}
    c1 = collections.Counter(re.sub(r"[^\wáéíóúñü ]", "", s).split()[0] for s in ors if s.split())
    c2 = collections.Counter(" ".join(re.sub(r"[^\wáéíóúñü ]", "", s).split()[:2]) for s in ors)
    # consecutivos con la misma primera palabra
    firsts = [re.sub(r"[^\wáéíóúñü ]", "", s).split()[0] if re.sub(r"[^\wáéíóúñü ]", "", s).split() else "" for s in ors]
    consec = sum(1 for a, b in zip(firsts, firsts[1:]) if a == b and a not in ("",))
    lens = [len(s.split()) for s in ors]
    import statistics as st
    out[cap] = dict(palabras=len(txt.split()), oraciones=len(ors), muletillas=m,
                    top1=c1.most_common(8), top2=[x for x in c2.most_common(12) if x[1] >= 4],
                    consecutivas_misma_palabra=consec,
                    long_media=round(st.mean(lens), 1), long_de=round(st.pstdev(lens), 1))
if "--json" in sys.argv:
    Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(out, ensure_ascii=False, indent=1))
keys = list(MUL)
print("| Patrón | " + " | ".join(CAPS) + " | Total |"); print("|---" * (len(CAPS) + 2) + "|")
for k in keys:
    v = [out[c]["muletillas"][k] for c in CAPS]; print(f"| {k} | " + " | ".join(map(str, v)) + f" | {sum(v)} |")
for lab in ("palabras", "oraciones", "consecutivas_misma_palabra", "long_media", "long_de"):
    print(f"| {lab} | " + " | ".join(str(out[c][lab]) for c in CAPS) + " | |")
print()
for c in CAPS:
    print(c, "top1:", out[c]["top1"]); print("   top2:", out[c]["top2"])
```
