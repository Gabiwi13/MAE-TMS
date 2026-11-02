# Propuesta viejo/nuevo: estructura y fundamento teórico (lectura de jurado)

**Estado:** pendiente de aprobación. No apliqué nada: la tesis, `una-hetero` en `df2f893`, está sin cambios, sin commit y sin push.

**Consolidación (2 nov 2026).** Este archivo ya trae lo que decidió la consolidación de las tres propuestas (`revision_jurado_INDICE.md`):
- Los 45 «Viejo» coinciden con el `.tex8` actual (script de cotejo, solo espacios normalizados).
- Los marcadores «reanálisis del banco» e «información mutua» están llenos con `results/reanalisis_jurado/salida.md` (tablas M3.1, M2.3 y M6.1).
- Toda frase con cifras del protocolo del experimento 11 lleva `[PENDIENTE: exp11 corregido]`, que va al final de la frase y cubre todas sus cifras del protocolo: son provisionales hasta la corrida con los directorios reiniciados.
- Los pasajes que también toca la propuesta de claridad traen el texto combinado (contenido de esta propuesta, forma de la de claridad). Cada uno lo dice en una línea **Consolidación**.
- Errores de hecho corregidos aquí: 5.3 (la información mutua es con el ganador maduro, y $H(G)$ no es $H_{\mathrm{dir}}$), 5.4 (99.1 y 99.2 %), 2.1 (el directorio de la comparación con la EHAM única es perspectival) y 4.4 y 7.6 (las 12 consultas de la sonda están dentro de las 40).

Atiende `jurado_wegner.md` (M1–M11 y el aviso de analogías), `jurado_estilo.md` (E1, E2, E6, E7 y 5.6) y `jurado_metodologia.md` M7.

**Lo que más pesa:**
1. **La asignación de información tiene una sola versión** en toda la tesis. El sistema modela dos de los tres procesos de Wegner: la actualización del directorio y la coordinación de la recuperación. La asignación la hace la etiqueta de clase y queda como trabajo futuro. Se retira `03:379-380`.
2. **Se separa lo que es de Wegner de lo que es del sistema**, con una tabla en 2.3 y con «en este sistema» en cada frase atribuida. Entra la mitad que faltaba de la definición de 1987. Los tres procesos con nombre se citan a 1995, con la definición de cada uno tomada del resumen de ese artículo.
3. **La especialización es asignada.** «Sin clasificadores supervisados» pasa a «sin clasificadores discriminativos en las decisiones de enrutamiento y rechazo». Se dice qué usa etiquetas: la partición del contenido y el codificador visual. La limitación nueva (k) deja lista la cifra del codificador sin pérdida de clase.
4. **«Los límites están en la representación, no en el mecanismo» se retira** del resumen, de 6.1 y de 07. Queda «buena parte de los límites está en la representación, y el mecanismo tiene límites propios». La forma final depende de las líneas base.
5. **6.4 y 6.5 se reescriben** con el aviso de analogía estructural al inicio y la salvedad del directorio compartido. 6.5 se reorienta hacia la memoria semántica y la denominación, porque el sistema guarda asociaciones de categoría, no episodios.
6. **Apartado 2.4 nuevo, «Trabajo relacionado»**, de una página. B1 y la partición aparecen ahí como reencuentros de principios conocidos.

**Cómo se verificaron las citas.** Los verificadores no pudieron abrir doi.org, Crossref, PsycNet ni las páginas de las editoriales, porque esos dominios no están permitidos en la red de esta sesión. Toda la verificación sale de resultados de búsqueda que muestran el registro: la URL de la editorial, PubMed, DBLP o arXiv, y su resumen.
- **V:** vi los metadatos en un resultado de búsqueda del registro.
- **V+:** además vi el contenido que se cita, en el resumen que muestra el registro.
- **V parcial:** algún campo (DOI, número o páginas) solo aparece en índices secundarios. Cada entrada dice cuál.

El presupuesto de búsquedas de este turno (200, compartido) se agotó antes de terminar. Las citas que no alcancé a verificar no se proponen; están al final, con el lugar donde irían. Un mensaje de seguimiento puede retomarlas.

**Convenciones de la propuesta:**
- `main:74-76` es `.tex8/main.tex`, líneas 74 a 76.
- `02:292-296` es `.tex8/secciones/02_marco_teorico.tex`; lo mismo para 01–07.
- Los «Viejo» están copiados del archivo; un script comprobó los 45 bloques y líneas de borde contra `df2f893`.
- Si un bloque se reemplaza entero y pasa de 30 líneas, doy el rango y su primera y última línea exactas.
- En el texto nuevo uso `\,\%`, como pide 5.4.

**Dependencias:**
- **Propuesta de términos y lengua (C1–C12, 5.1–5.5, 5.7).** Escribo sobre el texto de hoy y conservo sus términos («hemisferio», «fidelidad», «precisión», «fase A», «TME»); si esa propuesta los cambia, se aplica encima. Solo adelanto «rescate léxico» (C10) y «mecanismo transactivo» (5.7), en frases que reescribo de todos modos.
- **Metodología M1** (clase correcta sobre el total): no la toco. «Clasifica algo mejor» (`07:60-61`) y «La exactitud de clase también mejora» (`06:189-193`) quedan para la propuesta de cifras, que es `revision_jurado_metodologia_prosa.md`.
- **Etiquetas nuevas:** `sec:trabajo-relacionado`, `tab:wegner-sistema` y `eq:info-mutua-dir`. La limitación nueva es la (k); las demás letras no cambian.

---

## Parte 1. La asignación de información: una sola versión

### 1.1 Resumen
- **Dónde:** `main:74-76`
- **Viejo:**
```latex
La arquitectura modela los tres mecanismos de Wegner \cite{wegner1995computer}: la
actualización del directorio, la asignación de información y la coordinación de la
recuperación.
```
- **Nuevo** (va dentro del resumen completo de 9.1):
```latex
De los tres procesos que Wegner \cite{wegner1995computer} distingue, el sistema modela
dos: la actualización del directorio y la coordinación de la recuperación.
La asignación de información la hace la etiqueta de clase, que decide qué módulo guarda
cada imagen y cada palabra: la especialización de los módulos es asignada, y lo que se
forma con el uso es el directorio.
```
- **Por qué:** M1 y E1; es la primera de las cuatro versiones. «Mecanismos» pasa a «procesos», como en el resto.
- **Consolidación:** se aplica dentro de 9.1, donde los dos puntos de «cada palabra: la especialización» pasan a «, así que» (claridad 3.7).

### 1.2 Introducción: los tres procesos
- **Dónde:** `01:15-23`
- **Viejo:**
```latex
El modelo de Wegner identifica tres procesos principales \cite{wegner1995computer}.
Primero, la \emph{actualización del directorio}: tras cada interacción, los
miembros que la presenciaron registran quién supo responder.
Segundo, la \emph{asignación de información}: la información nueva se envía
hacia el miembro reconocido como referencia en ese dominio.
Tercero, la \emph{coordinación de recuperación}: las consultas futuras viajan directamente
a ese referente sin pasar por un intermediario.
En este trabajo, la transición de una \emph{fase temprana} mediada a una \emph{fase
madura} punto a punto es la señal de que el sistema transactivo ya quedó formado.
```
- **Nuevo:**
```latex
Wegner \cite{wegner1995computer} describe el sistema transactivo con la analogía de una
red de computadoras y distingue en él tres procesos: la \emph{actualización del
directorio}, en la que los miembros aprenden quién sabe qué en el grupo; la
\emph{asignación de información}, que asigna cada ítem de memoria a un miembro, y la
\emph{coordinación de la recuperación}, que planea cómo encontrar cada ítem.
Este trabajo modela dos de ellos.
En este sistema, el directorio se actualiza con cada consulta resuelta y lo anotan solo
los módulos que participaron en ella; la coordinación lleva la consulta del módulo por
el que entró al especialista, sin pasar por el mediador.
La asignación no se modela: la etiqueta de clase decide de antemano en qué módulo se
guarda cada imagen y cada palabra, y que el propio grupo decida dónde guardar lo nuevo
queda como trabajo futuro.
El paso de una \emph{fase temprana}, con mediador, a una \emph{fase madura}, punto a
punto, lo fija el protocolo tras un número dado de interacciones; el sistema no tiene
todavía un criterio propio para saber que su directorio ya basta.
```
- **Por qué:**
  - M1 y E1.
  - M2: «los miembros que la presenciaron» y «sin pasar por un intermediario» son rasgos del sistema y ahora van con «En este sistema».
  - M4: la madurez la fija el protocolo (01:22-23).
- **Fuente:** `wegner1995computer`, V+. El resumen, en el registro de Guilford, dice: *directory updating (learning who knows what in the group), information allocation (assigning memory items to group members), and retrieval coordination (planning how to find items…)*. La analogía con redes de computadoras también está en el resumen.

### 1.3 Marco teórico
- **Dónde:** `02:292-296` (punto «Asignación de información»). La enumeración entera se reemplaza en 2.1.

### 1.4 Arquitectura: se retira la suma como asignación
- **Dónde:** `03:377-381`
- **Viejo:**
```latex
El módulo ganador es $g = \arg\max_k \sum_{\text{tokens}} s_k$: la suma recorre las
pistas de la consulta, una por token.
En este sistema, esta suma hace el papel de la asignación de información de Wegner y
vive fuera de las memorias por diseño.
Si $s_k = 0$ para todos los módulos, el sistema emite un \textbf{rechazo}.
```
- **Nuevo:**
```latex
El módulo ganador es $g = \arg\max_k \sum_{\text{tokens}} s_k$; la suma recorre las
pistas de la consulta, una por token, y es una operación fuera de las memorias.
Si $s_k = 0$ para todos los módulos, el sistema emite un \textbf{rechazo}.
```
- **Consolidación:** absorbe la fila `03:377` de claridad 3.7 (dos puntos → punto y coma).
- **Por qué:** M1 pide retirarla. Elegir quién responde una consulta es coordinación de la recuperación, no asignación. Que la suma está fuera de las memorias se conserva, porque 5.6 la cuenta entre las operaciones externas.

### 1.5 Limitación (e)
- **Dónde:** `06:280-285`
- **Viejo:**
```latex
\paragraph{(e) Aprendizaje limitado después de formar el directorio.}
Una vez llena la memoria de contenido y formado el directorio, los módulos dejan de
registrar contenido nuevo: la fase madura enruta y recupera con lo aprendido.
El sistema aún no modela la asignación de información de Wegner (encaminar información
nueva al especialista que corresponde) ni la reorganización de las memorias de contenido
durante la operación madura.
```
- **Nuevo:**
```latex
\paragraph{(e) Asignación por etiqueta y aprendizaje limitado después de formar el directorio.}
La asignación de información de Wegner, decidir en qué miembro se guarda cada ítem, no
se modela: la etiqueta de clase decide qué módulo llena cada imagen y cada palabra.
La especialización de los módulos es por tanto asignada, como en la condición de
estructura asignada de Wegner, Erber y Raymond~\cite{wegner1991transactive}, donde los
experimentadores indicaban qué categorías debía recordar cada miembro de la pareja.
Una vez llena la memoria de contenido y formado el directorio, los módulos dejan de
registrar contenido nuevo: la fase madura enruta y recupera con lo aprendido, y las
memorias de contenido no se reorganizan durante la operación.
```
- **Por qué:** M1 y M3.
- **Fuente:** `wegner1991transactive`, V+. Resumen en PubMed: *For some pairs a memory structure was assigned (e.g., 1 partner should remember food items…)*.

### 1.6 Trabajo futuro, punto 2
- **Dónde:** `07:91-94`
- **Viejo:**
```latex
    \item \textbf{Aprendizaje en fase madura} (limitación (e)): que los módulos sigan
    registrando etiquetas, imágenes y asociaciones después de formar el directorio (la
    asignación de información de Wegner), y que el directorio se reorganice cuando un
    módulo sale del grupo o entra en él.
```
- **Nuevo:**
```latex
    \item \textbf{Asignación de información y aprendizaje en fase madura} (limitación
    (e)): que una imagen o una palabra nueva entre por cualquier módulo y el grupo la
    registre en el especialista que indique su directorio, sin la etiqueta de clase (la
    asignación de información de Wegner); que los módulos sigan registrando después de
    formar el directorio, y que el directorio se reorganice cuando un módulo sale del
    grupo o entra en él.
```
- **Por qué:** recoge como trabajo futuro el experimento opcional de M1.

---

## Parte 2. Qué es de Wegner y qué es del sistema

### 2.1 Sección 2.3: definición completa, tabla y procesos «en este sistema»
- **Dónde:** `02:268-311`. Se reemplaza el bloque entero; el párrafo de la entropía (313-322) va en 5.2.
- **Viejo, primera línea (268):** `\subsection{Memoria transactiva}`
- **Viejo, última línea (311):** `interacciones se vuelven punto a punto.`
- **Nuevo:**
```latex
\subsection{Memoria transactiva}
\label{sec:tmt}

Wegner~\cite{wegner1987transactive} define un sistema de memoria transactiva como un
conjunto de sistemas de memoria individuales en combinación con la comunicación que
ocurre entre los individuos (p.~186).
La primera mitad de la definición es la memoria de cada miembro; la segunda, lo que
hace de esas memorias un sistema.
En su modelo posterior, Wegner~\cite{wegner1995computer} compara el grupo con una red
de computadoras en la que cada miembro guarda parte de lo que el grupo sabe y lleva un
\emph{directorio} de quién sabe qué, separado del contenido.
En la red distingue tres procesos: la actualización del directorio (\emph{directory
updating}), en la que los miembros aprenden quién sabe qué en el grupo; la asignación
de información (\emph{information allocation}), que asigna cada ítem de memoria a un
miembro, y la coordinación de la recuperación (\emph{retrieval coordination}), que
planea cómo encontrar cada ítem.
La Tabla~\ref{tab:wegner-sistema} separa lo que este trabajo toma de cada fuente de lo
que decide EAM-TMS.

\begin{table}[H]
\centering
\caption{Lo que EAM-TMS toma de Wegner y lo que decide el sistema.
«---»: el elemento no se toma de esa fuente.}
\label{tab:wegner-sistema}
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{@{}p{2.6cm}p{3.1cm}p{3.6cm}p{5.6cm}@{}}
\toprule
& \textbf{Wegner (1987)} & \textbf{Wegner (1995)} & \textbf{Decisión de EAM-TMS} \\
\midrule
Sistema & memorias individuales y la comunicación entre individuos (p.~186) &
  memorias individuales enlazadas como computadoras en red &
  ocho módulos con una memoria de contenido y dos directorios cada uno; la
  comunicación es la consulta que un módulo reenvía a otro \\
Directorio & --- & lo que cada miembro sabe de quién sabe qué &
  memoria heteroasociativa de la pista a la identidad del módulo; perspectival en el
  sistema y en la comparación con una sola EHAM, compartido en los demás estudios de
  texto (Sección~\ref{sec:organizacion}) \\
Actualización del directorio & --- & aprender quién sabe qué en el grupo &
  registrar (pista, ganador) tras cada consulta resuelta; solo por interacción \\
Asignación de información & --- & asignar cada ítem de memoria a un miembro &
  no se modela: la etiqueta de clase decide qué módulo guarda cada imagen y cada palabra \\
Coordinación de la recuperación & --- & planear cómo encontrar cada ítem &
  el módulo de entrada suma su directorio y los de sus conocidos (lectura normalizada
  por conteo) y reenvía al de mayor puntuación \\
Mediador y fases & --- & --- &
  el TME media en la fase temprana; el paso a la fase madura lo fija el protocolo \\
Rechazo & --- & --- &
  si nadie tiene soporte para la consulta, el sistema no responde \\
\bottomrule
\end{tabular}
\end{table}

En este sistema, el directorio se actualiza solo por interacción: lo anotan los módulos
que participaron en cada consulta resuelta (Sección~\ref{sec:componentes}).
En los grupos de personas no es el único camino: los miembros también se reparten las
categorías que recordará cada uno según estereotipos de
género~\cite{hollingshead2003gender}, y los grupos que reciben información sobre las
habilidades de sus miembros, sin haber entrenado juntos, rinden como los que entrenaron
juntos~\cite{moreland2000exploring}.
La asignación de información no se modela: la hace la etiqueta de clase.
La especialización de cada módulo es por tanto asignada, como en la condición de
estructura asignada de Wegner, Erber y Raymond~\cite{wegner1991transactive}, y lo que
se forma con el uso es el directorio.
En la coordinación de la recuperación, cuando nadie tiene soporte para la consulta, el
grupo la rechaza; en este sistema, el rechazo es una respuesta válida.

Las dos fases son también una decisión de EAM-TMS.
En la \textbf{fase temprana} el grupo depende de un mediador, porque los miembros no
conocen aún las especialidades de los demás y las consultas se difunden a todos.
En la \textbf{fase madura}, cada módulo enruta con su directorio y los de sus
conocidos, y el mediador sale del circuito.
El paso de una a otra lo fija el protocolo experimental, tras un número dado de
interacciones; un criterio interno de madurez queda como trabajo futuro.
```
- **Por qué:**
  - M2: la tabla de tres columnas y la definición de 1987 completa.
  - Salen como atribuciones a Wegner: «tras cada interacción de recuperación exitosa» (02:285-287), «sin intervención de ningún coordinador central» (02:298-301) y «red de directorios compartidos» (02:281-282). Esa frase no está en el resumen de 1995 y choca con los directorios perspectivales.
  - Salen también «metadirectorio» y «todos los miembros mantienen» (menor).
  - M1 y M3: una sola versión de la asignación y de la especialización.
  - M4: la madurez la fija el protocolo.
  - E6: el «puente» de 02:277-279 pasa a 2.4.
  - M4 y E2: la tabla dice que en texto el directorio es compartido.
- **Consolidación:**
  - Absorbe claridad S68 (02:302-303): sale «en vez de inventar un especialista».
  - «Lectura B1» pasa a «lectura normalizada por conteo» (claridad 1.2), y dos dos puntos explicativos pasan a «en la que» y «porque» (claridad 3.7).
  - **Corrección de hecho:** la tabla decía que el directorio es «compartido en los experimentos de texto». La comparación con una sola EHAM es de texto y usa directorios perspectivales (`04:279-281`), así que la celda dice ahora «perspectival en el sistema y en la comparación con una sola EHAM, compartido en los demás estudios de texto».
- **Fuente:**
  - `wegner1995computer`: V+ (ver 1.2).
  - `wegner1991transactive`: V+. *the performance of natural pairs was inferior to that of impromptu pairs when structure was assigned*.
  - `hollingshead2003gender`: V+. *participants with opposite-sex partners were more likely to assign categories based on gender stereotypes*.
  - `moreland2000exploring`: V+. Los grupos con información sobre las habilidades *performed comparably to groups whose members were trained together*.
  - **La p. 186 de 1987:** el dictamen la marca V+, pero en esta sesión solo la vi en fuentes secundarias. **Cotejarla con el capítulo antes de aplicar.** Es traducción propia y va sin comillas.
  - **El directorio se atribuye a 1995**, porque así consta en su resumen. No pude ver si el capítulo de 1987 usa la palabra.

### 2.2 Introducción: la definición de 1987
- **Dónde:** `01:4-13`
- **Viejo:**
```latex
Cuando un grupo de personas trabaja de manera coordinada durante el tiempo suficiente,
puede recordar más de lo que cualquiera de sus miembros recordaría por separado.
Wegner \cite{wegner1987transactive} llamó a este fenómeno
\textbf{memoria transactiva}: una forma de memoria compartida en la que cada individuo
almacena no solo sus propios conocimientos, sino también un \emph{directorio} que indica quién es reconocido
dentro del grupo como referente en cada dominio.
Cuando un miembro necesita información que no conoce, consulta ese directorio,
determina a quién preguntar y delega la recuperación.
El grupo funciona gracias a esa especialización: el conocimiento no necesita repetirse
en cada miembro, sino que se reparte entre ellos.
```
- **Nuevo:**
```latex
Cuando un grupo de personas trabaja de manera coordinada durante el tiempo suficiente,
puede recordar más de lo que cualquiera de sus miembros recordaría por separado.
Wegner \cite{wegner1987transactive} llamó a este fenómeno \textbf{memoria transactiva}
y la definió como un conjunto de sistemas de memoria individuales en combinación con la
comunicación que ocurre entre los individuos (p.~186).
En su modelo posterior \cite{wegner1995computer}, cada miembro guarda parte de lo que
el grupo sabe y lleva un \emph{directorio} de quién sabe qué.
Cuando un miembro necesita información que no conoce, consulta ese directorio,
determina a quién preguntar y delega la recuperación.
El conocimiento no necesita repetirse en cada miembro, porque se reparte entre ellos.
```
- **Por qué:** M2: faltaba la comunicación entre individuos. «El grupo funciona gracias a esa especialización» sale, porque aquí la especialización es asignada (M3).

### 2.3 Arquitectura
- **Dónde:** `03:73-77`
- **Viejo:**
```latex
Registrar una transacción es asociar la pista ($\mathbf{v}_q$ en $M^L_{\mathrm{dir}}$,
$\mathbf{z}_q$ en $M^R_{\mathrm{dir}}$) con el identificador $g$ del módulo ganador.
Registran solo quienes participaron: el módulo por el que entró la consulta y el
ganador; el TME las registra todas (la \emph{actualización del directorio} de Wegner,
por transacción).
```
- **Nuevo:**
```latex
Registrar una transacción es asociar la pista ($\mathbf{v}_q$ en
$M^{\mathrm{txt}}_{\mathrm{dir}}$, $\mathbf{z}_q$ en $M^{\mathrm{vis}}_{\mathrm{dir}}$)
con el identificador $g$ del módulo ganador.
Registran solo quienes participaron: el módulo por el que entró la consulta y el
ganador; el TME las registra todas.
En este sistema, esa es la \emph{actualización del directorio}, transacción por
transacción.
```
- **Consolidación:** notación de claridad 1.3 ($M^{\mathrm{txt}}_{\mathrm{dir}}$ y $M^{\mathrm{vis}}_{\mathrm{dir}}$ en 03:73-74).
- **Dónde:** `03:83-86`
- **Viejo:**
```latex
Esto permite la coordinación de la recuperación de Wegner también para imágenes: una
imagen puede entrar por \emph{cualquier} módulo, que consulta su $M^R_{\mathrm{dir}}$ y
los de los módulos que conoce y la reenvía al especialista, o la rechaza si nadie la
contiene (Sección~\ref{sec:operaciones}).
```
- **Nuevo:**
```latex
En este sistema, la coordinación de la recuperación vale también para imágenes.
Una imagen puede entrar por \emph{cualquier} módulo, que consulta su
$M^{\mathrm{vis}}_{\mathrm{dir}}$ y los de los módulos que conoce (los que vio ganar
alguna transacción) y la reenvía al especialista, o la rechaza si nadie la contiene
(Sección~\ref{sec:operaciones}).
```
- **Consolidación:** absorbe claridad S22 en 03:84-85 («los que vio ganar alguna transacción»), la notación de 1.3 y los dos puntos de 03:83 (claridad Parte 4, punto 7).
- **Por qué:** M2.

### 2.4 Metodología
- **Dónde:** `04:173-178`
- **Viejo:**
```latex
Las consultas varían en longitud y vocabulario (p.\ ej.\ ``a crunchy red apple'',
``a barking domestic pet'', ``a mug for liquid'') y cubren tanto descripciones
directas como perifrásticas; las clases con léxico compartido (\texttt{pear},
\texttt{tomato}) incluyen consultas con contenido \emph{distintivo}
(``a bosc pear with brown skin'', ``a tomato on the vine''), como en la comunicación
de un grupo de Wegner: quien pregunta aporta las señas del dominio.
```
- **Nuevo:**
```latex
Las consultas varían en longitud y vocabulario (p.\ ej.\ «a crunchy red apple»,
«a barking domestic pet», «a mug for liquid») y cubren tanto descripciones
directas como perifrásticas; las clases con léxico compartido (\texttt{pear},
\texttt{tomato}) incluyen consultas con contenido \emph{distintivo}
(«a bosc pear with brown skin», «a tomato on the vine»), en las que quien pregunta
aporta las señas del dominio.
```
- **Por qué:** M2. «Las señas del que pregunta» no es un constructo de Wegner. El vínculo pasa a 6.4 (sobrecarga de pistas).
- **Consolidación:** comillas angulares de claridad 3.2 (04:173, 04:174 y 04:177). Queda junto al punto M3 de `revision_jurado_metodologia_prosa.md`, que agrega una frase después de 04:172; no se tocan.

### 2.5 Otras frases atribuidas a Wegner
| Lugar | Qué atribuye | Dónde se resuelve |
|---|---|---|
| `06:81-83` | cita 1987 para los mecanismos | 4.4 (cita 1995) |
| `06:95-96` | «En el modelo de Wegner, el directorio se forma anotando…» | 4.4 |
| `06:105-106` | «En términos de Wegner… quien pregunta aporta las señas» | 4.4 |
| `06:167-169` | «En términos de Wegner, es justo el momento…» | 6.1 |
| `07:49-52` | «lo que la teoría de Wegner anticipa… comunicación distintiva» | 7.6 |
| `01:94-96` | «es la coordinación de recuperación de Wegner» | 9.2 |

---

## Parte 3. La especialización está asignada; «sin clasificadores supervisados»

### 3.1 Pregunta de investigación
- **Dónde:** `01:32-38`
- **Viejo:**
```latex
\begin{quote}
¿Puede un sistema de memoria transactiva construido sobre memorias asociativas
entrópicas repartir consultas de texto e imagen entre ocho especialistas, recordar el
contenido asociado y rechazar lo que no conoce, sin clasificadores supervisados? Y donde
aparezcan límites, ¿provienen del mecanismo asociativo o de las representaciones que lo
alimentan?
\end{quote}
```
- **Nuevo:**
```latex
\begin{quote}
¿Puede un sistema de memoria transactiva construido sobre memorias asociativas
entrópicas repartir consultas de texto e imagen entre ocho especialistas, recordar el
contenido asociado y rechazar lo que no conoce, sin clasificadores discriminativos en
las decisiones de enrutamiento y rechazo? Y donde aparezcan límites, ¿provienen del
mecanismo asociativo o de las representaciones que lo alimentan?
\end{quote}
```
- **Por qué:** M3 y metodología M4. La cabeza de entropía cruzada del codificador es un clasificador supervisado, aunque no decida nada.

### 3.2 Qué emerge y qué se impone
- **Dónde:** `01:55-60`
- **Viejo:**
```latex
Ninguna decisión del sistema sale de un clasificador entrenado ni de una optimización
numérica: registrar, reconocer, recuperar y enrutar son operaciones definidas
formalmente sobre las Memorias Asociativas Entrópicas
de Pineda y Morales en su variante ponderada (W-EAM)
\cite{pineda2021entropic,pineda2022weighted} y su extensión heteroasociativa (EHAM)
\cite{morales2025missing}.
```
- **Nuevo:**
```latex
Registrar, reconocer, recuperar y enrutar son operaciones definidas formalmente sobre
las Memorias Asociativas Entrópicas de Pineda y Morales en su variante ponderada
(W-EAM) \cite{pineda2021entropic,pineda2022weighted} y su extensión heteroasociativa
(EHAM) \cite{morales2025missing}, y las decisiones de enrutamiento y de rechazo no usan
ningún clasificador discriminativo.
Cuatro operaciones del sistema quedan fuera de las memorias: la suma de las
puntuaciones sobre los tokens, la normalización B1, el umbral de energía $\tau$ y el
rescate léxico (Secciones~\ref{sec:pipeline-semantico} a~\ref{sec:percepcion}
y~\ref{sec:operaciones}).
Dos piezas usan las etiquetas de clase: la partición del contenido, que decide qué
módulo guarda cada imagen y cada palabra, y el codificador visual, entrenado con una
pérdida de clasificación auxiliar (Sección~\ref{sec:percepcion}).
Por eso la especialización de los módulos es asignada, mientras que el directorio, que
registra qué módulo resolvió cada consulta, se forma con el uso.
```
- **Por qué:**
  - M3: separa lo que emerge (el directorio) de lo que se impone (la especialización).
  - 5.6: «ninguna decisión… ajena» no se sostiene con la suma, B1, τ y el rescate.
  - Metodología M4.
- **Nota:** si estorba la referencia triple, basta «(Secciones~\ref{sec:metodologia} y~\ref{sec:operaciones})».

### 3.3 Limitación nueva (k)
- **Dónde:** después de `06:336`, al final del archivo.
- **Nuevo:**
```latex

\paragraph{(k) Supervisión del codificador visual.}
El codificador se entrenó con la reconstrucción y una entropía cruzada de clasificación
de peso 0.1 (Sección~\ref{sec:percepcion}).
La cabeza clasificadora no participa en ninguna decisión, pero la pérdida moldea el
espacio latente sobre el que operan los directorios visuales y las memorias de
contenido: desde ese espacio, la cabeza auxiliar alcanza una precisión del 99.7\,\%.
Con un codificador entrenado sin esa pérdida, el enrutamiento de las 656 imágenes de
prueba es del [PENDIENTE: codificador sin pérdida de clase] (frente al 96.2\,\%), y la
cobertura de punta a punta con objetos nuevos, del [PENDIENTE: codificador sin pérdida
de clase] (frente al 89.2\,\%).
```
- **Por qué:** M3 y metodología M4. No digo cuánto depende el sistema de la supervisión.
- **Fuente:** 0.1 y 99.7 de `04:131-138`; 96.2 de `05:350`; 89.2 de `05:444`.
- **Nota:**
  - `results/experimento19/README.md:7` ya tiene el codificador con `CLS_WEIGHT=0` (RMSE 0.082). Lo que se corrió de punta a punta es la variante ImageNet + PCA.
  - Si el experimento pendiente no mide objetos nuevos, se quita la segunda mitad de la frase.

### 3.4 Las demás menciones
| Lugar | Viejo | Dónde |
|---|---|---|
| `main:62-63` | «sin clasificadores supervisados» | 9.1 |
| `07:9-10` | «sin clasificadores ni umbrales supervisados…» | 7.5 |
| `07:38-39` | «sin componentes supervisados de decisión» | 7.6 |
| `07:106-108` | «sin modelos supervisados en la toma de decisiones» | 7.8 |

---

## Parte 4. El directorio compartido, el orden y el 97.0 frente al 93.0

### 4.1 Arquitectura
- **Dónde:** `03:70-71`
- **Viejo:**
```latex
El TME conserva además sus propios $M^L_{\mathrm{dir}}$ y $M^R_{\mathrm{dir}}$, con el
registro completo del grupo; sirven de diagnóstico y ningún enrutamiento los consulta.
```
- **Nuevo:**
```latex
El TME conserva además sus propios $M^{\mathrm{txt}}_{\mathrm{dir}}$ y
$M^{\mathrm{vis}}_{\mathrm{dir}}$, con el registro completo del grupo; en el sistema con
directorios perspectivales sirven de diagnóstico y ningún enrutamiento los consulta.
En los experimentos de texto de calibración, protocolo completo, barrido
$\iota \times \kappa$ y formación del directorio, en cambio, cada transacción se
registra en un solo \emph{directorio compartido}, igual a ese registro completo, y con
él enrutan todos los módulos en la fase madura (Sección~\ref{sec:organizacion}).
```
- **Por qué:** E2 y M4. «Ningún enrutamiento los consulta» no vale para esos experimentos (`04:276-281`).
- **Consolidación:** notación de claridad 1.3 en 03:70.

### 4.2 Por qué el 97.0 % supera al 93.0 %
- **Dónde:** `05:28-29`
- **Viejo:**
```latex
Sobre 171 consultas reservadas, el protocolo transactivo del experimento 11 enruta
correctamente el 97.0\% con 200 imágenes por clase (Sección~\ref{sec:eham-unica}).
```
- **Nuevo:**
```latex
Sobre 171 consultas reservadas, el protocolo transactivo de la comparación con una sola
EHAM enruta correctamente el 97.0\,\% con 200 imágenes por clase
(Sección~\ref{sec:eham-unica}), con directorios perspectivales formados con las otras
240 consultas [PENDIENTE: exp11 corregido].
Esa cifra no se compara directamente con las de esta sección, porque aquí el directorio
es compartido y se evalúa sobre las consultas que lo formaron.
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
- **Por qué:** E2 y E8.
- **Fuente:**
  - 240 y 171: `05:468-469`.
  - Cola de cada lista: `04:186-187`.
  - Directorios perspectivales: `04:279-281`.
  - 97.0: `results/experimento11/README.md` (N = 200, T-protocolo, «ruteo ok»). Es del brazo del protocolo: provisional.
  - 87.7 (150 de 171) y 49.8 (199 de 400): tabla M3.1, columna «nombre (con plural)».
  - 84.5 y 195 de 200: tabla M2.3, tramo 201–400.
- **Consolidación:** el marcador `[PENDIENTE: reanálisis del banco]` queda lleno. El reanálisis cuenta tokens con una regla propia, no con spaCy (nota de M3.1); por eso la nota al pie dice cómo se cuenta.

### 4.3 La invariancia al orden es por construcción
- **Dónde:** `05:268-269`
- **Viejo:**
```latex
Esta invariancia del destino muestra que el directorio acumula evidencia conmutativa:
el orden solo determina cuándo se vuelve utilizable, no qué se aprende.
```
- **Nuevo:**
```latex
La invariancia del destino ocurre por construcción: el ganador de cada interacción lo
deciden las memorias de contenido, que no cambian durante la formación, y el registro
es una suma (ecuación~\eqref{eq:registro}), que no depende del orden de los sumandos.
El orden solo determina cuándo el directorio parcial se vuelve utilizable.
```
- **Por qué:** M5, 5.6 y metodología (menores).

### 4.4 Discusión 6.4 completa
- **Dónde:** `06:78-120`. Se reemplaza el bloque entero.
- **Viejo, primera línea (78):** `\subsection{Lectura desde la teoría de memoria transactiva de Wegner}`
- **Viejo, última línea (120):** `\end{itemize}`
- **Nuevo:**
```latex
\subsection{Lectura desde la teoría de memoria transactiva de Wegner}
\label{sec:disc-wegner}

Las analogías de esta sección y de la siguiente son estructurales, no causales.
Los módulos no son personas, y lo que se compara es la forma de una regularidad, no el
mecanismo que la produce.
Las lecturas de texto valen además para un directorio compartido, porque en la
calibración, el protocolo completo y la formación del directorio todos los módulos leen
un solo registro, igual al registro completo del TME (Sección~\ref{sec:componentes}).
En imagen los directorios son perspectivales, pero tras la formación visual el primer
círculo de cada módulo reúne los ocho directorios visuales
(Sección~\ref{sec:operaciones}), y entre ellos está cada transacción de la formación
visual, porque el ganador siempre la registra.
En la evaluación, el primer círculo cubre todo lo que registró el grupo, como un
directorio compartido.
Con directorios de cobertura parcial, sumar los de los conocidos iguala al registro
completo sin superarlo (experimento~10).
Si las curvas de formación se repiten con directorios perspectivales en texto, y
cuánto convergen entre sí los directorios de los módulos, no se midió.
En los grupos de personas, ese acuerdo es parte de lo que se mide: el consenso entre
miembros~\cite{austin2003transactive} y la convergencia de sus representaciones de quién
sabe qué, que Brandon y Hollingshead proponen como el estado óptimo del
sistema~\cite{brandon2004transactive}.
Con esas salvedades, los resultados de las Secciones~\ref{sec:calibracion},
\ref{sec:formacion}, \ref{sec:capacidad} y~\ref{sec:hemisferio-visual} se leen con los
procesos que nombra Wegner~\cite{wegner1995computer}:

\begin{itemize}
    \item \textbf{Conocerse cuesta interacción.}
    Con 10 consultas por dominio, la precisión madura queda en 81.2\,\%, y con unas 50
    llega al 93.0\,\%, las dos sobre las consultas que formaron el directorio.
    Sobre las mismas consultas, la diferencia entre la lectura normalizada y la fase
    temprana, que no usa el directorio, es de 0, +4.0, +5.5 y +3.0 puntos con 50, 100,
    200 y 400 consultas de formación (Sección~\ref{sec:calibracion}).
    Cuánto de la diferencia entre 81.2 y 93.0\,\% se debe a la formación y cuánto a que
    cambian las consultas evaluadas lo separa la calibración con un conjunto fijo
    ([PENDIENTE: calibración con conjunto fijo]).
    En equipos de trabajo, el sistema transactivo se desarrolla a lo largo del proyecto,
    y es más probable que surja cuando la experticia está repartida desde el inicio y
    los miembros se conocen~\cite{lewis2004knowledge}.
    Aquí el paso a la fase madura lo fija el protocolo tras un número dado de
    interacciones.
    Un criterio interno, como que la información mutua entre dominio y ganador
    (ecuación~\eqref{eq:info-mutua-dir}) deje de crecer, queda como trabajo futuro.

    \item \textbf{El orden de las experiencias no cambia el directorio final.}
    Las cuatro condiciones de presentación terminan en el mismo directorio, con los
    mismos conteos y la misma entropía, y el orden solo decide cuándo se vuelve
    utilizable (Sección~\ref{sec:formacion}).
    Es una propiedad del modelo y no dice nada de los grupos, porque cada ganador lo
    deciden las memorias de contenido, que no cambian durante la formación, y el registro
    es una suma.
    En las personas el directorio no parte de cero, porque los miembros también se
    reparten lo que recordará cada uno según estereotipos~\cite{hollingshead2003gender}.
    Para que el orden importara aquí, el registro tendría que dejar de ser una suma
    pura: con olvido, que restara peso a los registros antiguos; con saturación, al
    llegar las celdas al tope de los pesos (Sección~\ref{sec:eam}), o con una expectativa
    previa, como un ganador temprano que consultara el directorio parcial, de modo que
    lo ya registrado sesgara lo siguiente.

    \item \textbf{Las pistas compartidas degradan el enrutamiento.}
    Con la lectura normalizada, \texttt{car}, \texttt{cow}, \texttt{cup} y
    \texttt{tomato} quedan entre 98.0 y 100.0\,\% y \texttt{dog} en 93.9\,\%;
    \texttt{pear} (76.0\,\%), \texttt{horse} (88.0\,\%) y \texttt{apple} (88.2\,\%)
    pierden hacia la vecina con la que comparten etiquetas
    (Sección~\ref{sec:disc-dominancia}).
    En la memoria humana, la probabilidad de recordar un ítem baja con el número de
    ítems que comparten su pista de recuperación~\cite{watkins1975buildup}, y el tiempo
    para verificar un hecho crece con el número de hechos aprendidos sobre la misma
    persona o el mismo lugar~\cite{anderson1974retrieval}.
    En este sistema, \textit{fruit} está registrada en tres módulos y señala a los tres.
    La regla de rescate léxico, que solo admite tokens de la consulta como
    \textit{bark}, \textit{moo} o \textit{riding}, sube 21.7 puntos en las 46 consultas
    que toca (Sección~\ref{sec:pipeline-semantico}); una pista distintiva vale más que
    una compartida.

    \item \textbf{El directorio está separado del contenido.}
    Cada módulo guarda en su memoria de contenido \emph{qué} sabe y en sus directorios
    \emph{quién} sabe el resto.
    Quien espera poder volver a consultar una información recuerda menos la información
    y más dónde encontrarla~\cite{sparrow2011google}.
    En el cerebro hay propuestas de la misma forma: el hipocampo como índice de las
    áreas de la neocorteza que activó una experiencia~\cite{teyler1986hippocampal}, y el
    significado como reactivación de registros distribuidos y no como lectura de un
    almacén único~\cite{damasio1989time}.
    La analogía tiene un límite en el mediador.
    En texto, el directorio compartido con que enrutan los módulos es, en contenido, el
    registro del TME, así que en la fase madura sale del circuito el mediador y no su
    registro.

    \item \textbf{El rechazo se sostiene con ocho dominios, en lo medido.}
    Con siete clases contrarias por módulo, el contenido no acepta ningún falso con un
    latente por imagen, en ninguno de los tamaños de llenado probados, y con las 16
    variantes del experimento 13 acepta 5 de 656 imágenes de prueba, todas entre
    animales (vacas y caballos aceptados por \texttt{dog}, un caballo por
    \texttt{cow}).
    El directorio visual comete dos falsos enrutamientos de 656.
    En este sistema, lo que ningún módulo reconoce no se responde
    (Sección~\ref{sec:tmt}).
    El rechazo se midió con imágenes de las ocho clases, sondas sintéticas y las 40
    consultas fuera de dominio escritas para esta tesis, entre ellas las 12 de la sonda
    de rechazo; no se probó con fotografías reales de otras categorías.
\end{itemize}
```
- **Por qué:**
  - Aviso de analogías al inicio (menor).
  - M4: la salvedad del directorio compartido, la convergencia, el criterio de madurez y Lewis (2004).
  - Metodología M7: el perspectival reproduce al compartido.
  - M5: el orden y qué haría falta para que importara.
  - M2: se retiran 06:95-96 y 06:105-106, y la cita pasa a 1995.
  - M9: la sobrecarga de pistas, el efecto abanico y el directorio separado del contenido.
  - 5.6 y metodología M7: el rechazo, acotado a lo medido.
  - Metodología M2: sale «hace falta el banco completo».
  - E4: cambia el título repetido.
- **Consolidación:**
  - Absorbe claridad S65 (06:101-103: 98.0 a 100.0, 76.0 y 88.0) y S69 (06:117-119, que esta versión ya no repite), la sustitución «lectura B1» → «lectura normalizada» (06:101), «fase A» → «formación visual» y «mecanismos de Wegner»/«releen» de claridad Parte 4, punto 4, que aquí ya no aparecen.
  - Ocho dos puntos explicativos pasan a punto, «porque» o punto y coma (claridad 3.7); se quita «no lo decide el grupo:», que era antítesis y dos puntos a la vez.
  - Metodología M2: en «Conocerse cuesta interacción» entra la diferencia madura menos temprana sobre las mismas consultas (0, +4.0, +5.5 y +3.0 puntos; `salida.md`, tabla M2.1, condición B1).
  - **Corrección de hecho:** «las 12 consultas de la sonda de rechazo y 40 consultas fuera de dominio» las contaba por separado; las 40 incluyen las 12 (`04:187-188`).
- **Fuente:**
  - Las cifras ya están en 05 y 06.
  - Experimento 10 (`results/experimento10/README.md`): en imagen, el encadenado iguala al pizarrón (81.9 %) en todas las condiciones con algún registro ajeno. En texto, el agregado da de 91.0 a 94.3 % sobre las reservadas, frente a 93.6 %. El README dice que el 94.3 «no es una superación».
- **Citas:**
  - `austin2003transactive`: V parcial; el consenso consta en el título.
  - `brandon2004transactive`: V+; *convergence is the optimal state of transactive memory systems*.
  - `lewis2004knowledge`: V+; *teams with initially distributed expertise and familiar members are more likely to develop a TMS*.
  - `watkins1975buildup`: V+; *the probability of recalling an item declines with the number of items subsumed by its functional retrieval cue*.
  - `anderson1974retrieval`: V+; el tiempo de respuesta crece con las proposiciones ligadas a la persona o al lugar de la sonda.
  - `sparrow2011google`: V+; *lower rates of recall of the information itself and enhanced recall instead for where to access it*.
  - `teyler1986hippocampal`: V+ parcial.
  - `damasio1989time`: V+ parcial; *Meaning is reached by time-locked multiregional retroactivation of widespread fragment records*.

### 4.5 Trabajo futuro: punto nuevo
- **Dónde:** después de `07:98`.
- **Nuevo:**
```latex
    \item \textbf{Directorios perspectivales en texto y criterio de madurez}
    (Sección~\ref{sec:disc-wegner}): repetir la calibración y la curva de formación con
    directorios perspectivales, medir cuánto convergen entre sí los directorios de los
    módulos y que el paso a la fase madura lo decida un criterio interno, como que la
    información mutua entre dominio y ganador deje de crecer.
```
- **Por qué:** M4.

---

## Parte 5. La entropía del directorio

### 5.1 La tensión entre 02:130-132 y 02:316-319
- **Dónde:** `02:130-132`
- **Viejo:**
```latex
Si la entropía baja es deseable o no depende de la tarea: un directorio que debe señalar
sin ambigüedad a un especialista necesita entropía baja, y una memoria
de contenido que debe generalizar, un rango medio.
```
- **Nuevo:**
```latex
Si la entropía baja es deseable o no depende de la tarea: un directorio que debe señalar
sin ambigüedad a un especialista necesita poca incertidumbre sobre el módulo dada la
pista (Sección~\ref{sec:tmt}), y una memoria de contenido que debe generalizar, un rango
medio de entropía.
```
- **Por qué:** M6. Lo que debe ser bajo es la incertidumbre condicional, no la entropía de los conteos.

### 5.2 Sección 2.3: el párrafo de la entropía
- **Dónde:** `02:313-322`
- **Viejo:**
```latex
La \textbf{entropía del directorio} resume el estado del grupo.
No es la entropía de una memoria (ecuación~\eqref{eq:entropia}): se calcula sobre la
distribución de los registros entre módulos (ecuación~\eqref{eq:entropia-dir}).
En el registro completo del grupo (el del mediador, o el directorio compartido de la
calibración), el máximo $\log_2 K$ (con $K$ módulos; $\log_2 8 = 3$ bits) indica que la
experticia está repartida de forma pareja, y una entropía baja indica colapso hacia un
solo módulo o formación incompleta.
En el directorio de cada módulo el máximo no es el estado deseable: como cada uno
registra lo que presenció, su directorio se carga hacia sí mismo y queda por debajo del
máximo aunque el grupo esté balanceado.
```
- **Nuevo:**
```latex
La \textbf{entropía del directorio} resume cómo se reparten los registros entre
módulos (Sección~\ref{sec:operaciones}); no es la entropía de una memoria
(ecuación~\eqref{eq:entropia}).
En el registro completo del grupo (el del mediador, o el directorio compartido de la
calibración), el máximo, $\log_2 8 = 3$ bits con ocho módulos, indica que los registros
están repartidos de forma pareja, y una entropía baja indica colapso hacia un solo
módulo o formación incompleta.
Mide balance, no especialización: con un banco balanceado entre clases, un directorio
que anotara ganadores al azar también quedaría cerca del máximo.
Que el grupo esté especializado lo dice la relación entre el dominio de cada consulta y
el módulo que la ganó, que se mide con la información mutua entre ambos
(Sección~\ref{sec:operaciones}); es lo más cercano, en este sistema, a la
especialización que se mide en los grupos de personas~\cite{austin2003transactive}.
En el directorio de cada módulo el máximo no es el estado deseable: como cada uno
registra lo que presenció, su directorio se carga hacia sí mismo y queda por debajo del
máximo aunque el grupo esté balanceado.
```
- **Por qué:**
  - M6.
  - E4: 02 citaba una ecuación que aún no existía.
  - Lewis (2003) no la pude verificar; Austin (2003) lleva la especialización en el título.

### 5.3 Arquitectura: la información mutua
- **Dónde:** `03:446-461`
- **Viejo:**
```latex
\subsubsection*{Entropía del directorio}

Sea $c_k$ el número de registros del módulo $k$ en el directorio y
$C = \sum_k c_k$ el total.
La entropía del directorio resume el estado del grupo:
\begin{equation}
    H_{\mathrm{dir}} = -\sum_{k=0}^{K-1} p_k \log_2 p_k, \qquad p_k = \frac{c_k}{C}
    \label{eq:entropia-dir}
\end{equation}
Con $K=8$ módulos, el máximo es $\log_2 8 = 3$ bits, alcanzado cuando los ocho conteos
son iguales.
Esa lectura vale para un registro completo del grupo (el del TME y el directorio
compartido de los experimentos de texto, Sección~\ref{sec:organizacion}), donde una
entropía menor indica colapso hacia un módulo o formación incompleta.
No vale para el directorio de cada módulo, que registra todo lo que ganó y solo parte
de lo ajeno (Sección~\ref{sec:tmt}).
```
- **Nuevo:**
```latex
\subsubsection*{Entropía del directorio e información mutua}

Sea $c_k$ el número de registros del módulo $k$ en el directorio y
$C = \sum_k c_k$ el total.
La entropía del directorio resume cómo se reparten los registros entre módulos:
\begin{equation}
    H_{\mathrm{dir}} = -\sum_{k=0}^{K-1} p_k \log_2 p_k, \qquad p_k = \frac{c_k}{C}
    \label{eq:entropia-dir}
\end{equation}
Con $K=8$ módulos, el máximo es $\log_2 8 = 3$ bits, alcanzado cuando los ocho conteos
son iguales.
Esa lectura vale para un registro completo del grupo (el del TME y el directorio
compartido de los estudios de texto que lo usan, Sección~\ref{sec:organizacion}), donde
una entropía menor indica colapso hacia un módulo o formación incompleta.
No vale para el directorio de cada módulo, que registra todo lo que ganó y solo parte
de lo ajeno (Sección~\ref{sec:tmt}).
$H_{\mathrm{dir}}$ mide balance y es poco sensible.
Con un banco balanceado, un enrutamiento al azar también quedaría cerca de 3 bits, y
conteos que van de 112 a 186 registros dan 2.974 bits (Sección~\ref{sec:calibracion}).
La especialización la mide la información mutua entre el dominio $D$ de cada consulta
(su clase real, que solo se usa para medir) y el módulo $G$ que la gana en la fase
madura:
\begin{equation}
    I(D; G) = H(G) - H(G \mid D), \qquad
    H(G \mid D) = -\sum_{d} p(d) \sum_{k} p(k \mid d) \log_2 p(k \mid d),
    \label{eq:info-mutua-dir}
\end{equation}
donde las probabilidades son las frecuencias de la matriz de confusión de la fase
madura, sin los rechazos.
$H(G)$ es la entropía de los ganadores maduros y no coincide con $H_{\mathrm{dir}}$, que
cuenta los registros de la formación.
Dividida entre $H(D)$, vale 1 cuando cada módulo recibe un solo dominio y 0 cuando el
ganador no depende del dominio.
Con pocas consultas, este estimador sobrestima $I$ en unos $(K-1)^2/(2n\ln 2)$ bits, con
$n$ el número de consultas no rechazadas.
```
- **Por qué:** M6.
- **Fuente:** 112, 186 y 2.974 de `results/ablation_mdir_bias/ablation_report.md:151-156` (condición A: `apple` 186, `horse` 112), que el reanálisis reproduce (línea de referencia bajo la tabla M6.1).
- **Corrección de hecho (consolidación):** la versión de la nube definía $D$ y $G$ sobre los registros del directorio («el módulo $G$ al que apunta») y decía «donde $H(G)$ es $H_{\mathrm{dir}}$». La cifra que existe, la de `salida.md` (tabla M6.1), es con el ganador de la fase madura, leída de las columnas `cm_<verdad>_<ganador>`: la fase temprana no tiene matriz en el CSV. Con esa definición $H(G)$ no es $H_{\mathrm{dir}}$; en A con $N = 400$, $H(G) = 2.906$ y $H_{\mathrm{dir}} = 2.974$ bits. La normalización $I/H(D)$ es la del reanálisis, así que la última frase se queda. El término de sesgo es el de la nota de M6.1, con $8 \times 8$ celdas.
- **Consolidación:** dos dos puntos explicativos pasan a punto (claridad 3.7), y «los experimentos de texto» pasa a «los estudios de texto que lo usan», porque la comparación con la EHAM única es de texto y tiene directorios perspectivales.

### 5.4 Resultados
- **Dónde:** `05:135-140`
- **Viejo:**
```latex
\paragraph{Estado del directorio.}
La entropía del directorio transactivo es de 2.974 bits en la condición A y de 2.977 en
G, el 99.1\% del máximo ($\log_2 8 = 3$ bits): los conteos quedan casi parejos entre los
ocho módulos.
El sesgo que B1 corrige está en la lectura, no en los conteos
(Sección~\ref{sec:disc-b1}).
```
- **Nuevo:**
```latex
\paragraph{Estado del directorio.}
La entropía del directorio transactivo es de 2.974 bits en la condición A y de 2.977 en
G, el 99.1 y el 99.2\,\% del máximo ($\log_2 8 = 3$ bits), así que los conteos quedan
casi parejos entre los ocho módulos, aunque en A van de 186 registros (\texttt{apple}) a
112 (\texttt{horse}).
Esa cifra mide el reparto de los registros, no la especialización.
La especialización la da la información mutua entre el dominio de la consulta y el
módulo ganador en la fase madura (ecuación~\eqref{eq:info-mutua-dir}).
Con el mismo directorio, A y B1 tienen la misma entropía y distinta información mutua:
2.438 bits con la lectura cruda y 2.649 con B1, el 81.3 y el 88.3\,\% de $H(D)$; en G,
que evalúa otras consultas, es de 2.668 bits (88.9\,\%).
Se mide sobre las mismas consultas que formaron el directorio, y con $N = 400$ el
estimador la sobrestima en unos 0.09 bits.
Como los conteos quedan casi parejos, el sesgo que corrige B1 está en la lectura
(Sección~\ref{sec:disc-b1}).
```
- **Por qué:** M6. Además, el 186/112 deja de aparecer solo en la discusión (E5).
- **Fuente:** tabla M6.1 de `salida.md`, $N = 400$: A 2.438 bits (0.813), B1 2.649 (0.883), G 2.668 (0.889); sesgo esperado 0.088 (A y B1) y 0.089 (G). Los 186 y 112 son de la línea de referencia bajo M6.1 (condición A).
- **Consolidación:**
  - El marcador `[PENDIENTE: información mutua]` queda lleno.
  - **Corrección de hecho:** «el 99.1 % del máximo» solo vale para A (2.974/3 = 99.13 %); para G es 2.977/3 = 99.23 % (claridad Parte 4, punto 10).
  - Absorbe las filas `05:137` y `05:139–140` de claridad 3.7 y S70 (dos puntos → «así que»; la antítesis «en la lectura, no en los conteos» pasa a «Como los conteos quedan casi parejos»).

### 5.5 Discusión 6.2
- **Dónde:** `06:51-54`
- **Viejo:**
```latex
La brecha cruda-B1 es de 7.8 puntos con ocho módulos (85.2\% frente a 93.0\%), y la
entropía del directorio es alta incluso con la lectura cruda (2.974 de 3.000 bits): la
\emph{estructura} del directorio está casi balanceada, y el sesgo está en la
\emph{lectura}, donde B1 actúa.
```
- **Nuevo:**
```latex
La brecha cruda-B1 es de 7.8 puntos con ocho módulos (85.2\,\% frente a 93.0\,\%), y la
entropía del directorio es alta incluso con la lectura cruda (2.974 de 3.000 bits): los
conteos del directorio están casi balanceados, y el sesgo está en la \emph{lectura},
donde B1 actúa.
La entropía no dice si el directorio está especializado; eso lo dice la información
mutua entre dominio y ganador, que con el mismo directorio pasa de 2.438 bits con la
lectura cruda a 2.649 con B1 (Sección~\ref{sec:calibracion}).
```
- **Por qué:** M6.
- **Consolidación:** marcador lleno con la tabla M6.1 (A y B1, $N = 400$).

### 5.6 Conclusiones
- `07:78-80` va en 9.4.
- `07:23-24` (3.000 bits, «balanceado») no cambia: ahí la entropía dice balance, que es lo que mide.

---

## Parte 6. Las analogías de 6.5, hacia la memoria semántica y la denominación

### 6.1 Discusión 6.5 completa
- **Dónde:** `06:122-171`. Se reemplaza el bloque entero.
- **Viejo, primera línea (122):** `% ---------------------------------------------------------------`
- **Viejo, última línea (171):** `se dañó; en el sistema, con datos sin pareja, nunca se registró.`
- **Nuevo:**
```latex
% ---------------------------------------------------------------
\subsection{Una memoria por módulo: familiaridad, nombre y daño}
\label{sec:disc-una-memoria}

Como en la sección anterior, las analogías que siguen son estructurales, no causales.
Con una sola memoria de contenido, el sistema queda hecho solo de asociaciones: la de
contenido (etiqueta con imagen) dentro de cada módulo y la de directorio (pista con
módulo) entre ellos.
Lo que asocia la memoria de contenido son categorías, no episodios: cada latente se
registra con una etiqueta del vocabulario de su clase, asignada por turno
(Figura~\ref{fig:arq-llenado}), no con el nombre de esa imagen, y la memoria no completa
una imagen concreta a partir de parte de sus coordenadas
(Sección~\ref{sec:una-memoria}).
En la memoria episódica hay disociaciones de la misma forma, entre reconocer ítems y
reconocer asociaciones~\cite{mayes2004associative,old2008differential}, pero los
análogos más cercanos de este sistema están en la memoria semántica y en la
denominación.

Reconocer una pista no consulta un almacén aparte: es leer la asociación.
Es lo que proponen los modelos de emparejamiento global de la psicología, que leen la
familiaridad de un único almacén de huellas~\cite{clark1996global}: preguntarle a la
memoria conjunta si una imagen es familiar es emparejarla con todas las huellas,
cualquiera que sea su etiqueta, y eso es la suma de la ecuación~\eqref{eq:marginal}.
En MINERVA~2, por ejemplo, una pista contacta a la vez todas las huellas guardadas, y
la respuesta es la suma de las suyas~\cite{hintzman1984minerva}.
Un almacén así puede aceptar combinaciones de rasgos que nunca se registraron juntas, y
en las personas produce errores de conjunción: tomar por visto un estímulo nuevo hecho
con rasgos de estímulos que sí se vieron~\cite{reinitz1992memory}.
En este sistema, la contención por coordenada tiene esa forma: cada coordenada de la
pista solo necesita soporte en su propia columna, y por eso la envolvente cubre objetos
que no contribuyeron a ella (Sección~\ref{sec:objetos-nuevos}).
Si produce también falsos reconocimientos de combinaciones, no se midió.

La lesión de la Sección~\ref{sec:una-memoria} separa las dos lecturas: con daño al
azar en la única memoria, el módulo deja de nombrar mucho antes de dejar de reconocer
(Tabla~\ref{tab:lesion}).
Es una disociación simple, y su dirección sale de la construcción: nombrar exige que
cada coordenada de la imagen deje apoyo en cada coordenada de la etiqueta, mientras que
reconocer suma, en cada celda de la lectura, los 17 valores de etiqueta.
Una disociación simple puede deberse a que una lectura exige más que la
otra~\cite{shallice1988neuropsychology}, y un solo sistema dañado puede producir incluso
disociaciones dobles~\cite{plaut1995double}.
La lesión indica que dos lecturas de un mismo almacén se separan con el daño, como
encontró Plaut para la afasia óptica con un solo sistema semántico de especialización
gradual~\cite{plaut2002graded}, pero no que sean un solo proceso.
La caída del nombre tampoco es gradual: con el 1\,\% de las celdas destruidas, el
módulo ya no nombra el 92\,\% de las imágenes (Tabla~\ref{tab:lesion}).
Si la disociación se mantiene con un nombrar graduado, si aparece la inversa y si las
etiquetas evocadas derivan hacia las compartidas entre clases (\textit{fruit},
\textit{animal}) no se midió.

Que el nombre sea lo más frágil tiene análogos en la denominación.
En el reconocimiento de caras, el nombre es la última etapa: se reconoce la cara, se
accede a quién es y solo después al nombre~\cite{bruce1986understanding}, y una misma
palabra cuesta más recordarla como apellido que como oficio, como \textit{Baker} frente
a \textit{baker}~\cite{mcweeny1987putting}.
En este sistema el nombre es también la lectura que más exige: una conjunción sobre
todas las coordenadas.

El estado intermedio, reconocer sin poder nombrar, también tiene análogos.
En la afasia óptica, el paciente identifica un objeto por la vista pero no puede
nombrarlo desde ella~\cite{beauvois1982optic}.
En la experiencia de la punta de la lengua, la persona sabe que conoce la palabra y
recupera partes de ella, como la primera letra o el número de sílabas, sin
alcanzarla~\cite{brown1966tip}; y la sensación de saber anticipa con bastante acierto qué
se reconocerá aunque no se haya podido recordar~\cite{hart1965memory}.
En este sistema el estado aparece en cuanto hay datos sin pareja: de 800 imágenes
registradas sin palabra, 78 quedan reconocidas sin nombre (Sección~\ref{sec:una-memoria}).
La lectura de familiaridad las distingue de un rechazo; el protocolo de respuesta
todavía no las usa.
El equivalente de la punta de la lengua sería un acceso parcial, una fracción de
columnas con soporte, y esa fracción no se midió; tampoco si la familiaridad predice un
enrutamiento correcto, como la sensación de saber predice el reconocimiento.
En este sistema, sería el momento de consultar el directorio: el módulo sabe que conoce
el objeto y necesita a quien sepa el nombre.
En los pacientes la asociación existía y se dañó; en el sistema, con datos sin pareja,
nunca se registró.
```
- **Por qué:**
  - M7: el emparejamiento es por turno (03:188-190) y la memoria no completa ítems (05:592-595).
    - Salen las ratas de Fortin, la asignación perirrinal/hipocampal y «caras con nombres hablados», que el jurado no confirmó.
    - YR y el envejecimiento quedan en una frase, con su salvedad, para conservar el vínculo.
    - Entran el almacén compuesto (MINERVA 2) y los errores de conjunción.
  - M8: la disociación simple viene de la construcción y son dos lecturas de un almacén, no un proceso. La caída no es gradual, y los controles que faltan se nombran sin anunciar resultados.
  - Menores: la punta de la lengua como acceso parcial y la sensación de saber frente al enrutamiento.
  - M9: Bruce y Young (1986) y McWeeny et al. (1987).
  - M2: 06:167-169 queda «en este sistema».
- **Citas:**
  - `hintzman1984minerva`: V+ parcial; *a retrieval cue contacts all memory traces simultaneously*.
  - `reinitz1992memory`: V+; *Subjects will often claim to have previously seen a new stimulus if they have previously seen stimuli containing its component features*.
  - `shallice1988neuropsychology`: V. No vi el libro; el *Précis* del autor menciona *resource differences among tasks*.
  - `plaut1995double`: V+; doble disociación en una red *that… has no separable components*.
  - `bruce1986understanding`: V+; *…accessed from person identity nodes, and subsequently name codes are retrieved*.
  - `mcweeny1987putting`: V+; resumen parafraseado (Baker/baker).
- **Cifras:**
  - 1 % y 92 % (64 de 800): `tab:lesion` (`results/homo_marginal/lesion.json`).
  - 78 de 800: `05:590-591`.
  - 17 valores: `05:610`.
- **Bib:** `fortin2004recollection`, `eichenbaum2007medial`, `diana2007imaging` y `squire2007recognition` quedan sin citar. Conviene quitarlas del `.bib`.
- **Consolidación:** «muestra… como Plaut mostró… no muestra» pasa a «indica… como encontró Plaut… pero no», que es lo que pide claridad Parte 4, punto 8 (repetición cercana). Los demás dos puntos explicativos de este bloque se dejan para la pasada de forma final (índice).

### 6.2 Limitación (j)
- **Dónde:** `06:331-336`
- **Viejo:**
```latex
\paragraph{(j) Fragilidad del nombre ante daño.}
La proyección exige que cada coordenada de la imagen deje apoyo en cada coordenada de la
etiqueta, y no tolera ninguna columna vacía.
Destruir al azar el 1\,\% de las celdas de la memoria de contenido deja sin nombre al
92\,\% de las imágenes emparejadas, y el 5\,\% a todas
(Tabla~\ref{tab:lesion}); el reconocimiento, en cambio, sobrevive.
```
- **Nuevo:**
```latex
\paragraph{(j) Fragilidad del nombre ante daño.}
La proyección exige que cada coordenada de la imagen deje apoyo en cada coordenada de la
etiqueta, y no tolera ninguna columna vacía.
Destruir al azar el 1\,\% de las celdas de la memoria de contenido deja sin nombre al
92\,\% de las imágenes emparejadas, y el 5\,\% a todas
(Tabla~\ref{tab:lesion}); el reconocimiento, en cambio, sobrevive.
La diferencia de redundancia entre las dos lecturas viene de la construcción, así que la
disociación no prueba dos procesos (Sección~\ref{sec:disc-una-memoria}); un nombrar
graduado, que tolere una fracción de columnas vacías, y un daño difuso en lugar de al
azar quedan por medir.
```
- **Por qué:** M8.

### 6.3 Conclusiones
- **Dónde:** `07:72-75`
- **Viejo:**
```latex
Reconocer sin poder nombrar, que en las personas tiene análogos como la afasia óptica o
la experiencia de la punta de la lengua (Sección~\ref{sec:disc-una-memoria}), surge en
él de una sola memoria: con daño al azar, el módulo deja de nombrar mucho antes de
dejar de reconocer.
```
- **Nuevo:**
```latex
Reconocer sin poder nombrar, que en las personas tiene análogos como la afasia óptica,
la experiencia de la punta de la lengua o la dificultad para recordar nombres propios
(Sección~\ref{sec:disc-una-memoria}), surge en él de una sola memoria con dos lecturas:
con daño al azar, el módulo deja de nombrar mucho antes de dejar de reconocer, porque
nombrar es una conjunción sobre todas las coordenadas y reconocer, una suma.
```
- **Por qué:** M7 y M8.

---

## Parte 7. Las afirmaciones infladas

### 7.1 Discusión 6.1
- **Dónde:** `06:5`
- **Viejo:**
```latex
\subsection{La maquinaria transactiva funciona con ocho dominios; la representación es el límite}
```
- **Nuevo:**
```latex
\subsection{El mecanismo transactivo funciona con ocho dominios; buena parte de los límites está en la representación}
```
- **Dónde:** `06:8-12`
- **Viejo:**
```latex
El resultado central separa dos responsabilidades: la maquinaria transactiva funciona
con ocho dominios, y los límites aparecen en la \emph{representación}.
Los componentes de la maquinaria (los directorios heteroasociativos, la lectura B1, el
rechazo por contención, la actualización perspectival del directorio (en imagen) y la
coordinación punto a punto) funcionan sin ajustes por dominio.
```
- **Nuevo:**
```latex
El mecanismo transactivo funciona con ocho dominios: los directorios
heteroasociativos, la lectura normalizada, el rechazo por contención, la actualización
perspectival del directorio ---en imagen--- y la coordinación punto a punto operan sin
ajustes por dominio.
Buena parte de los límites medidos están en la \emph{representación}: el léxico que
comparten las clases vecinas en texto y la cobertura del espacio latente con objetos
nuevos en imagen.
El mecanismo tiene también límites propios: la lectura del directorio necesita una
normalización externa (Sección~\ref{sec:disc-b1}), el nombre se pierde con un daño
del 1\,\% (limitación (j)) y el contenido visual da soporte a entradas sin estructura
(limitación (c)).
Separar las dos responsabilidades exige probar otros decisores sobre los mismos
vectores.
Con un clasificador por centroide, \texttt{pear} queda en [PENDIENTE: líneas base], y
con $k$ vecinos más cercanos en [PENDIENTE: líneas base], frente al 76\,\% de la lectura
normalizada.
```
- **Por qué:** M10, 5.6 y metodología M7. Los paréntesis anidados pasan a rayas (5.4).
- **Consolidación:** absorbe claridad S63 (06:10-12; «la lectura B1» → «la lectura normalizada», «maquinaria» → «mecanismo transactivo», rayas) y la sustitución de «maquinaria» en 06:5 y 06:8. Los dos puntos que quedan introducen enumeraciones.
- **Cuando lleguen las líneas base:**
  - Si `pear` queda cerca del 76 % con los dos decisores, el título puede pasar a «…; el límite de clase está en la representación».
  - Si sube, el título queda como aquí.

### 7.2 Discusión 6.2
- **Dónde:** `06:43-49`
- **Viejo:**
```latex
La lectura B1 del directorio transactivo no corrige un defecto: refleja cómo está
construido el sistema.
Cuando los módulos especialistas acumulan números desiguales de interacciones, la
puntuación cruda del directorio favorece de forma constante al módulo más activo con
independencia del contenido semántico de la consulta.
Dividir entre el conteo normaliza la evidencia a \textit{evidencia por interacción},
comparable entre módulos con historiales de exposición distintos.
```
- **Nuevo:**
```latex
La lectura B1 corrige un sesgo de la lectura cruda, no de lo registrado.
Cuando los módulos especialistas acumulan números desiguales de interacciones, la
puntuación cruda del directorio favorece de forma constante al módulo más activo con
independencia del contenido semántico de la consulta.
Dividir entre el conteo normaliza la evidencia a \textit{evidencia por interacción},
comparable entre módulos con historiales de exposición distintos.
Leída como frecuencia, la puntuación cruda se parece a la de la pista junto con el
módulo, y la B1 a la de la pista dado el módulo: B1 quita el peso de cuántas veces
registró cada módulo.
En este banco, con unas 50 consultas por dominio, ese peso no informa sobre la consulta;
con dominios de tamaños muy desiguales sí informaría, y B1 lo descartaría.
```
- **Por qué:** 5.6 («no corrige un defecto» choca con 05:118-119) y los menores sobre B1 (P(pista, k) frente a P(pista | k), prior inflado, tasas base). El precedente bibliográfico va en 2.4.

### 7.3 Discusión 6.6
- **Dónde:** `06:178-182`
- **Viejo:**
```latex
Lo primero es no mezclar: la relación de una EHAM acumula por coordenada y valor, y dos
conceptos distintos comparten valores cuantizados en muchas coordenadas, así que una
memoria con varios dominios mezcla al recordar aunque las palabras difieran.
Partir el contenido evita la mezcla porque el dominio se decide antes de la
recuperación, en el directorio, y no al muestrear la memoria.
```
- **Nuevo:**
```latex
Lo primero es mezclar menos: la relación de una EHAM acumula por coordenada y valor, y
dos conceptos distintos comparten valores cuantizados en muchas coordenadas, así que una
memoria con varios dominios mezcla al recordar aunque las palabras difieran.
Partir el contenido reduce la mezcla porque el dominio se decide antes de la
recuperación, en el directorio, y no al muestrear la memoria; cuando el directorio se
equivoca de módulo, la mezcla reaparece como error de dominio.
Con una etiqueta compartida como primera pista, el protocolo acierta la clase entre el
79 y el 84\,\%, y la EHAM única entre el 48 y el 52\,\% (Sección~\ref{sec:eham-unica})
[PENDIENTE: exp11 corregido].
Es un reencuentro de un principio conocido en las memorias asociativas
(Sección~\ref{sec:trabajo-relacionado}).
```
- **Por qué:** 5.6 y M11.
- **Fuente:** `05:537-540`; `results/experimento11/README.md` (T-protocolo 78.6–84.3; M 47.8–52.2).
- **Consolidación:** el 79–84 % es del brazo del protocolo; la cifra de la EHAM única sigue valiendo.

### 7.4 Metodología: la auditoría
- **Dónde:** `04:218-219`
- **Viejo:**
```latex
La auditoría de fidelidad comprueba que las decisiones del sistema salen de operaciones
de las memorias y que ningún número se apoya en datos fabricados:
```
- **Nuevo:**
```latex
La auditoría de trazabilidad comprueba que las operaciones de memoria son las de la
implementación de referencia, que el vocabulario no contiene vectores sintéticos y que
la clase correcta no entra al circuito de decisión:
```
- **Consolidación:** absorbe claridad S3 en 04:218 («auditoría de trazabilidad»). El título de 04:215 lo cambia S3 aparte.
- **Dónde:** `04:230`
- **Viejo:**
```latex
Todos los números reportados salen de corridas de este sistema.
```
- **Nuevo:**
```latex
Fuera de las memorias quedan cuatro operaciones, declaradas en la arquitectura: la suma
de las puntuaciones sobre los tokens, la lectura B1, el umbral de energía $\tau$ y el
rescate léxico.
Todos los números reportados salen de corridas de este sistema, con sus tablas en
\texttt{results/}.
```
- **Por qué:**
  - 5.6.
  - El nombre de la auditoría lo cambia C1.
  - No digo «reproducibles» porque metodología M6 sigue abierta.

### 7.5 Conclusiones: apertura
- **Dónde:** `07:8-10`
- **Viejo:**
```latex
El sistema cubre las ocho categorías de ETH-80 y opera de forma bidireccional
texto $\leftrightarrow$ imagen con rechazo claro en ambas direcciones, sin clasificadores
ni umbrales supervisados en la toma de decisiones.
```
- **Nuevo:**
```latex
El sistema cubre las ocho categorías de ETH-80 y opera en los dos sentidos,
texto $\leftrightarrow$ imagen, con rechazo explícito en ambos: no responde cuando
nadie tiene soporte para la consulta.
Las decisiones de enrutamiento y de rechazo no usan clasificadores discriminativos; la
partición del contenido usa las etiquetas de clase y el codificador visual se entrenó
con una pérdida de clasificación auxiliar.
Del modelo de Wegner, el sistema implementa la actualización del directorio y la
coordinación de la recuperación; la asignación de información la hace la etiqueta.
```
- **Por qué:** 5.6, M3, M1 y E7.

### 7.6 Conclusiones: respuesta a la pregunta
- **Dónde:** `07:34-52`
- **Viejo:**
```latex
\paragraph{Respuesta a la pregunta de investigación.}
Sí: un sistema de memoria transactiva hecho solo de memorias asociativas entrópicas
reparte, recuerda y rechaza en ocho dominios.
Los directorios, la lectura B1, el rechazo por contención, la actualización del
directorio y la coordinación punto a punto funcionan sin componentes supervisados de
decisión.
El rechazo tiene dos fugas medidas: consultas que comparten tokens con un dominio, y
entradas visuales sin estructura, que el umbral de energía cierra en su mayor parte
(limitaciones (a) y (c)).
Los límites encontrados están en las \emph{representaciones}.
En texto, el léxico que comparten clases vecinas concentra los errores que quedan
(\texttt{pear} $\to$ \texttt{apple} 9 y \texttt{horse} $\to$ \texttt{cow} 6 de 28) y
fija el techo de \texttt{pear} (76\%) y \texttt{horse} (88\%).
En imagen, la cobertura del espacio latente deja sin respuesta parte de las vistas de
objetos nuevos (89.2\% de punta a punta, frente a 95.5\% con objetos conocidos).
Formar el directorio cuesta lo que la teoría de Wegner anticipa: interacción (con 10
consultas por dominio la precisión madura queda en 81.2\%, y hacen falta unas 50 para
llegar al 93.0\%) y comunicación distintiva (las clases que preguntan con léxico
compartido pierden hacia su vecina).
```
- **Nuevo:**
```latex
\paragraph{Respuesta a la pregunta de investigación.}
Sí, con dos salvedades.
Un sistema de memoria transactiva hecho de memorias asociativas entrópicas reparte,
recuerda y rechaza en ocho dominios: los directorios, la lectura normalizada, el
rechazo por contención, la actualización del directorio y la coordinación punto a punto
funcionan sin clasificadores discriminativos en las decisiones de enrutamiento y
rechazo.
La primera salvedad es lo que no sale de las memorias: la especialización la asigna la
etiqueta de clase, el codificador visual se entrenó con una pérdida de clasificación
auxiliar, y la suma por tokens, la normalización del directorio, el umbral $\tau$ y el
rescate léxico operan fuera de ellas (limitación (k): [PENDIENTE: codificador sin
pérdida de clase]).
La segunda es el alcance del rechazo, que tiene dos fugas medidas: consultas que
comparten tokens con un dominio y entradas visuales sin estructura, que el umbral de
energía cierra en su mayor parte (limitaciones (a) y (c)).
Además, el rechazo se midió con las 40 consultas fuera de dominio, entre ellas las 12 de
la sonda de rechazo, y con sondas visuales sintéticas, no con fotografías reales de
otras categorías.

Buena parte de los límites encontrados están en las \emph{representaciones}.
En texto, el léxico que comparten clases vecinas concentra los errores que quedan
(\texttt{pear} $\to$ \texttt{apple} 9 y \texttt{horse} $\to$ \texttt{cow} 6 de 28) y
fija el techo de \texttt{pear} (76\,\%) y \texttt{horse} (88\,\%); con los mismos
vectores y otros decisores, \texttt{pear} queda en [PENDIENTE: líneas base].
En imagen, la cobertura del espacio latente deja sin respuesta parte de las vistas de
objetos nuevos (89.2\,\% de punta a punta, frente a 95.5\,\% con objetos conocidos).
El mecanismo tiene también límites propios: necesita una normalización externa en la
lectura del directorio, el nombre se pierde con un daño del 1\,\% y el contenido visual
da soporte a entradas sin estructura.
Formar el directorio cuesta interacción.
Con 10 consultas por dominio la precisión madura queda en 81.2\,\% y con unas 50 llega
al 93.0\,\%, las dos sobre las consultas que lo formaron, que en cada caso son otras;
sobre las mismas consultas, la fase madura supera a la temprana en 3.0 puntos con 400
consultas de formación ([PENDIENTE: calibración con conjunto fijo]).
Y las consultas de las clases con léxico compartido se van hacia la clase vecina, como
en la sobrecarga de pistas de la memoria humana~\cite{watkins1975buildup}.
```
- **Por qué:** M10, 5.6, metodología M7, M3, M2 (07:49-52) y metodología M2.
- **Consolidación:**
  - Absorbe claridad S50 (07:51-52; «las clases que preguntan» → «las consultas de las clases… se van hacia la clase vecina») y «lectura B1» → «lectura normalizada» (07:37).
  - **Corrección de hecho:** «40 consultas fuera de dominio, las 12 de la sonda» las contaba por separado; las 40 incluyen las 12 (`04:187-188`).
  - Metodología M2: «que en cada caso son otras» y los 3.0 puntos de la diferencia madura menos temprana (`salida.md`, tabla M2.1, B1 con $N = 400$).
  - Dos dos puntos explicativos pasan a punto (claridad 3.7).
- **Cuando lleguen las líneas base:** si `pear` sigue cerca del 76 %, «Buena parte de los límites» puede pasar a «Los límites de clase».

### 7.7 Conclusiones: «no mezcla dominios»
- **Dónde:** `07:55-57`
- **Viejo:**
```latex
Con el mismo contenido, el sistema transactivo recuerda con más fidelidad, no
mezcla dominios cuando la pista es compartida, acepta menos consultas fuera de
dominio cuando el contenido crece y en imagen responde
```
- **Nuevo:**
```latex
Con el mismo contenido, el sistema transactivo recuerda con más fidelidad, mezcla
menos los dominios cuando la pista es compartida (acierta la clase entre el 79 y el
84\,\% de esas consultas, frente al 48--52\,\% de la EHAM única), acepta menos
consultas fuera de dominio con 200 imágenes por clase y en imagen responde
```
- **Por qué:** 5.6.
- **Fuente:** `05:537-540`.
- **Nota:** 07:60-61 queda para la propuesta de cifras (M1).
- **Consolidación:**
  - La frase sigue en 07:58-59 y termina con la cifra del protocolo (3.0 %); el punto M1.6 de `revision_jurado_metodologia_prosa.md` pone ahí `[PENDIENTE: exp11 corregido]`, que cubre toda la frase (fidelidad, 79–84 y fuera de dominio son del protocolo).
  - Metodología M5: «cuando el contenido crece» pasa a «con 200 imágenes por clase», el único corte en que la diferencia es significativa ($p = 0.031$; `salida.md`, tabla M5.1).

### 7.8 Conclusiones: cierre
- **Dónde:** `07:106-110`
- **Viejo:**
```latex
En resumen, las Memorias Asociativas Entrópicas de Pineda y Morales bastan para
construir un sistema distribuido de memoria transactiva de ocho especialistas,
bidireccional y con rechazo claro, sin modelos supervisados en la toma de decisiones.
Sus límites están en las representaciones que alimentan a las memorias, no en el
mecanismo asociativo ni en la maquinaria transactiva.
```
- **Nuevo:**
```latex
En resumen, las Memorias Asociativas Entrópicas de Pineda y Morales bastan para
construir un sistema distribuido de memoria transactiva de ocho especialistas,
bidireccional y con rechazo explícito, sin clasificadores discriminativos en las
decisiones de enrutamiento y rechazo.
El sistema modela la actualización del directorio y la coordinación de la
recuperación; la especialización la asigna la etiqueta de clase.
Buena parte de sus límites están en las representaciones que alimentan a las memorias,
y el mecanismo asociativo tiene los suyos, medidos en este
trabajo [PENDIENTE: líneas base].
```
- **Por qué:** M10, M3, 5.6 y metodología M7.

---

## Parte 8. Apartado 2.4 «Trabajo relacionado»

### 8.1 Texto nuevo
- **Dónde:** después de `02:322`, al final del archivo.
- **Nuevo:**
```latex

\subsection{Trabajo relacionado}
\label{sec:trabajo-relacionado}

Repartir el conocimiento entre especialistas y elegir cuál responde tiene varias
tradiciones.

\paragraph{Mezcla de expertos.}
Una mezcla de expertos (\textit{mixture of experts}) reparte los casos entre varias
redes, cada una de las cuales aprende a manejar un subconjunto de
ellos~\cite{jacobs1991adaptive}, con variantes en árbol entrenadas con el algoritmo
EM~\cite{jordan1994hierarchical} y, a gran escala, compuertas que eligen para cada
ejemplo pocos expertos~\cite{shazeer2017outrageously} o uno solo~\cite{fedus2022switch}.
EAM-TMS comparte la estructura pero no el aprendizaje: sus especialistas son memorias
llenadas por clase, y su directorio se forma registrando quién resolvió cada consulta,
sin gradientes.
Las mezclas dispersas agregan una pérdida auxiliar para repartir la carga entre
expertos~\cite{fedus2022switch}; la lectura normalizada por conteo
(Sección~\ref{sec:operaciones}) reencuentra ese problema, el del módulo que gana por
tener más registros, y lo resuelve dividiendo entre el conteo.

\paragraph{Memorias asociativas.}
La EAM pertenece a la familia de la memoria asociativa no holográfica de Willshaw y
colaboradores~\cite{willshaw1969nonholographic}, las memorias asociativas bidireccionales
de Kosko~\cite{kosko1988bidirectional}, la red de Hopfield, que recupera un recuerdo
completo a partir de una parte suficiente~\cite{hopfield1982neural}, la memoria
distribuida dispersa~\cite{kanerva1988sparse}, las memorias densas, de mayor
capacidad~\cite{krotov2016dense}, y las redes de Hopfield modernas, de estados
continuos~\cite{ramsauer2021hopfield}.
Se distingue por guardar distribuciones de frecuencia por característica, reconocer
por contención y recordar muestreando (Sección~\ref{sec:eam}).
Cuando una sola memoria guarda muchos patrones aparecen estados metaestables que los
mezclan~\cite{amit1985spin,ramsauer2021hopfield}, y en las redes conexionistas lo
aprendido después puede interferir de forma catastrófica con lo anterior al entrenar en
secuencia~\cite{mccloskey1989catastrophic}.
La ventaja de partir el contenido entre especialistas (Sección~\ref{sec:eham-unica})
reencuentra ese principio: con un dominio por memoria, al recordar se mezclan menos
patrones de otros dominios.

\paragraph{Memoria transactiva computacional.}
La memoria transactiva ya se ha simulado: un modelo computacional muestra que saber qué
saben los demás conviene más a los grupos grandes y en entornos de tarea o de
conocimiento cambiantes~\cite{ren2006contingent}, y otros modelan la coevolución de las
redes de comunicación y de conocimiento de un grupo~\cite{palazzolo2006coevolution}.
EAM-TMS no simula un grupo para estudiar su desempeño: lo construye con memorias
asociativas que resuelven consultas de texto e imagen.
Este puente entre la teoría de Wegner y las memorias asociativas entrópicas es una
contribución de este trabajo: los artículos de la línea EAM/EHAM no contienen nociones
de directorio, de especialistas que cooperan ni de memoria transactiva.

\paragraph{Sistemas multiagente.}
En la red de contratos (\textit{contract net}), las tareas se reparten por negociación:
un gestor anuncia la tarea, los nodos ofertan y el gestor adjudica~\cite{smith1980contract},
como en la fase temprana, donde el TME difunde la consulta y gana el módulo con más
soporte.
Los intermediarios (\textit{middle-agents}) procesan anuncios de lo que ofrece
cada proveedor, solicitudes o ambas cosas, y median entre quien pide y quien
provee~\cite{decker1997middle}; el TME se les parece, pero aquí nadie anuncia lo que
sabe: el registro se llena observando quién resolvió cada consulta.

\paragraph{Enrutamiento distribuido y búsqueda federada.}
En las redes entre pares, los índices de enrutamiento evitan tanto un índice central
como inundar la red: cada nodo guarda un índice, proporcional al número de vecinos y no
al de documentos, para decidir a quién reenviar la consulta~\cite{crespo2002routing},
como hace en la fase madura cada módulo con su directorio y los de sus conocidos.
En la recuperación de información distribuida hay que elegir, entre muchas bases de
texto, en cuáles buscar~\cite{callan2000distributed}; el directorio de EAM-TMS hace esa
elección con una memoria asociativa.
```
- **Por qué:**
  - M11 y E6; el «puente» (antes 02:277-279) pasa aquí.
  - B1 aparece como reencuentro del balance de carga, y la partición, de los estados mezcla y la interferencia.
  - Sale en unas 46 líneas impresas a 11 pt: una página.
  - Las glosas en inglés se quedan la primera vez, porque son el nombre con que se buscan. Si 5.2 las suprime, se quitan.
- **Citas:**
  - `jacobs1991adaptive`: V+ parcial; *each of which learns to handle a subset of the complete set of training cases*.
  - `jordan1994hierarchical`: V+; *tree-structured architecture*… *EM*.
  - `shazeer2017outrageously`: V+ parcial; *sparse combination of these experts… for each example*.
  - `fedus2022switch`: V+ (arXiv); *route to only a single expert*; *To encourage a balanced load across experts we add an auxiliary loss*.
  - `willshaw1969nonholographic`: V.
  - `kosko1988bidirectional`: V.
  - `hopfield1982neural`: V+; *entire memory from any subpart of sufficient size*.
  - `kanerva1988sparse`: V.
  - `krotov2016dense`: V+; *many more patterns than the number of neurons*.
  - `ramsauer2021hopfield`: V+ parcial; *continuous states*; *metastable states averaging over a subset of patterns*.
  - `amit1985spin`: V+; *These metastable states correspond to specific mixings of the embedded patterns*.
  - `mccloskey1989catastrophic`: V+; *…when networks are trained sequentially*.
  - `ren2006contingent`: V+.
  - `palazzolo2006coevolution`: V parcial; se cita por el título.
  - `smith1980contract`: V+; *Task distribution is affected by a negotiation process*. Anuncio, oferta y adjudicación vienen de la copia del artículo en la página del autor.
  - `decker1997middle`: V+; *matchmakers… that process advertisements, blackboard agents that collect requests, and brokers that process both*.
  - `crespo2002routing`: V parcial; el contenido viene de una copia del artículo.
  - `callan2000distributed`: V+; *access to many searchable text databases*.
- **Lo que no entró:** la normalización por tamaño de colección (Si y Callan, 2003), que sería el precedente más directo de B1. No la verifiqué.
- **Consolidación:**
  - «La lectura B1» pasa a «la lectura normalizada por conteo», porque 2.4 va antes de la definición de 03 (claridad 1.2).
  - «Los agentes intermediarios» pasa a «Los intermediarios», por la convención de no usar «agente» en la prosa; el término de la fuente queda en la glosa. «Sistemas multiagente» se queda como nombre del campo (decisión del autor en el índice).
  - Las glosas en inglés se quedan: nombran conceptos de las fuentes, que es el criterio de claridad 3.6 para conservarlas.

### 8.2 Introducción: estructura del documento
- **Dónde:** `01:118-120`
- **Viejo:**
```latex
La Sección~\ref{sec:marco_teorico} presenta los fundamentos: la memoria asociativa
entrópica de Pineda y Morales y su variante ponderada, su extensión heteroasociativa
(EHAM) y el modelo de memoria transactiva de Wegner.
```
- **Nuevo:**
```latex
La Sección~\ref{sec:marco_teorico} presenta los fundamentos: la memoria asociativa
entrópica de Pineda y Morales y su variante ponderada, su extensión heteroasociativa
(EHAM), el modelo de memoria transactiva de Wegner, con lo que este sistema toma de él,
y el trabajo relacionado.
```

---

## Parte 9. Resumen, introducción y conclusiones con la misma historia

La historia común:
- la pregunta, sin clasificadores discriminativos en las decisiones;
- dos procesos de Wegner y la especialización asignada;
- la cifra dentro de muestra junto con la de las reservadas;
- seis contribuciones, sin la auditoría;
- los límites, repartidos entre la representación y el mecanismo.

### 9.1 Resumen completo
- **Dónde:** `main:57-104`. Se reemplaza el bloque entero.
- **Viejo, primera línea (57):** `\begin{abstract}`
- **Viejo, última línea (104):** `\end{abstract}`
- **Nuevo:**
```latex
\begin{abstract}
Un grupo que trabaja junto puede recordar más que cada uno de sus miembros por separado,
porque cada miembro guarda parte de lo que el grupo sabe y sabe a quién preguntar por el
resto.
Wegner \cite{wegner1987transactive} llamó a esta organización \emph{memoria
transactiva}.
Este trabajo pregunta si puede construirse con memorias asociativas, sin clasificadores
discriminativos en las decisiones de enrutamiento y rechazo, y presenta EAM-TMS
(\textit{Entropic Associative Memory -- Transactive Memory System}), un sistema
distribuido de memoria transactiva construido con las Memorias Asociativas Entrópicas
de Pineda y Morales en su variante ponderada (W-EAM)
\cite{pineda2021entropic,pineda2022weighted} y su extensión heteroasociativa (EHAM)
\cite{morales2025missing}.
El sistema tiene ocho módulos especialistas, uno por cada categoría del conjunto de datos
ETH-80 \cite{leibe2003eth80}
(\texttt{apple}, \texttt{car}, \texttt{cow}, \texttt{cup}, \texttt{dog}, \texttt{horse},
\texttt{pear}, \texttt{tomato}).
Cada módulo guarda su contenido en una sola memoria heteroasociativa entre palabras e
imágenes y lleva dos directorios, uno textual y uno visual, con las transacciones en que
participa.
De los tres procesos que Wegner \cite{wegner1995computer} distingue, el sistema modela
dos: la actualización del directorio y la coordinación de la recuperación.
La asignación de información la hace la etiqueta de clase, que decide qué módulo guarda
cada imagen y cada palabra, así que la especialización de los módulos es asignada y lo
que se forma con el uso es el directorio.
Un mediador central coordina la fase temprana y deja de ser necesario en la fase madura,
cuando los directorios de los módulos bastan para enrutar.
Las memorias operan en los dos sentidos, de palabras a imágenes y de imágenes a
palabras.
Las palabras entran como vectores fastText de 300 dimensiones
\cite{bojanowski2017fasttext}, con vocabulario extraído de ConceptNet 5.7
\cite{speer2017conceptnet} y \emph{cuantización por magnitud} en 16 niveles; las
imágenes, como códigos de un ResNet18 \cite{he2016resnet} entrenado con una pérdida de
clasificación auxiliar.
En el estudio de calibración, con un directorio compartido y un banco de 411 consultas
de texto ($N = 400$ consultas de formación), el 90.0\,\% de las consultas llega al
módulo correcto en la fase temprana y el 93.0\,\% en la fase madura, con la lectura del
directorio normalizada por conteo, que divide la puntuación de cada módulo entre su
número de registros; la cifra madura se mide sobre las mismas consultas que formaron el
directorio.
Con directorios perspectivales y 171 consultas reservadas, el 97.0\,\% llega al módulo
correcto, sobre consultas que traen el nombre de su clase más a menudo que las de la
calibración (87.7 frente a 49.8\,\%) [PENDIENTE: exp11 corregido].
La lectura normalizada reduce la participación del módulo \texttt{apple} del 20.5\,\% de
la lectura cruda al 13.8\,\% (ideal 12.5\,\%).
Con imágenes, los directorios visuales envían al especialista correcto 631 de las 656
imágenes de prueba (96.2\,\%), vistas nuevas de objetos conocidos; rechazan el 3.5\,\% y
se equivocan en dos.
Con objetos que ningún módulo vio, el 89.2\,\% de las vistas llega al especialista y
recibe respuesta, frente al 95.5\,\% con vistas nuevas de objetos conocidos, con dos
falsos enrutamientos en 3280.
Frente a una sola memoria con las ocho clases, la partición en especialistas recuerda con
más fidelidad, mezcla menos las clases cuando la pista es compartida y, con 200 imágenes
por clase, acepta menos consultas fuera de dominio (2 frente a 8 de 40, con una segunda
compuerta que se agregó después de ver esas consultas) [PENDIENTE: exp11 corregido].
En cada módulo, la familiaridad y el nombre se leen de la misma memoria, y el daño al
azar los separa.
Con el 1\,\% de las celdas destruidas, el módulo deja de nombrar el 92\,\% de las
imágenes y sigue reconociéndolas todas.
Buena parte de los límites observados provienen de las representaciones, el léxico
compartido entre clases vecinas y la cobertura del espacio latente ante objetos nuevos
[PENDIENTE: líneas base]; el mecanismo asociativo tiene también límites propios, como la
normalización externa que necesita la lectura del directorio y la fragilidad del nombre
ante el daño.
\end{abstract}
```
- **Por qué:**
  - M1, M3, M10 y E7: misma historia que 01 y 07, ahora con el 97.0 %.
  - Metodología (menores): «vistas nuevas de objetos conocidos» junto al 96.2.
  - C12: se expande EAM-TMS.
  - E3: sale «si además el módulo destino debe contener la consulta», porque el sistema siempre aplica la doble compuerta y el 2 de 40 es con ella.
- **Fuente:** todas las cifras ya están en la tesis, salvo las del reanálisis.
  - 97.0: `05:28-29` (brazo del protocolo: provisional).
  - 87.7 y 49.8: `salida.md`, tabla M3.1 (con plural).
  - 2 y 8 de 40: `tab:eham-unica`; $p = 0.031$ solo con 200 imágenes por clase: tabla M5.1.
  - 64 de 800 y 800 de 800: `tab:lesion`.
- **Nota:** el resumen crece unas ocho líneas. Si sobra algo, propongo quitar «Las memorias operan en los dos sentidos…».
- **Consolidación:**
  - Absorbe claridad S6 (main:85-91: «normalizada por conteo, que divide…»; «La lectura normalizada reduce…»), S43 (EAM-TMS expandida, que esta versión ya traía), 3.3 («5 semillas»), 3.4 («$N{=}400$» → «$N = 400$»), «mecanismos» → «procesos» (claridad Parte 4, punto 4) y «enrutamientos falsos» → «falsos enrutamientos» (main:96).
  - Metodología M2: sale «5 semillas», porque con la lectura B1 las cinco semillas dan el mismo resultado (`salida.md`, tabla M2.2).
  - Metodología M3: el 97.0 % va con la composición de las reservadas.
  - Metodología M5: «cuando el contenido crece» pasa a «con 200 imágenes por clase», con la compuerta declarada.
  - Dos dos puntos explicativos pasan a «porque» y a punto (claridad 3.7; main:58 y el de la lesión).

### 9.2 Contribuciones, sin la auditoría
- **Dónde:** `01:69-114`. Se reemplaza el bloque entero.
- **Viejo, primera línea (69):** `\subsection*{Contribuciones principales}`
- **Viejo, última línea (114):** `\end{enumerate}`
- **Nuevo:**
```latex
\subsection*{Contribuciones principales}

Este trabajo aporta seis contribuciones:

\begin{enumerate}
    \item \textbf{Un sistema transactivo de ocho especialistas.}
    Se construye un sistema de ocho módulos, uno por cada clase de ETH-80, cada uno con
    una sola memoria de contenido heteroasociativa y dos directorios, y se evalúa con un
    banco de 411 consultas ($\approx$50 por dominio).
    El sistema modela dos de los tres procesos de Wegner, la actualización del
    directorio y la coordinación de la recuperación; la asignación de información la
    hace la etiqueta de clase.
    Los directorios, su lectura normalizada por conteo de registros
    (Sección~\ref{sec:operaciones}), el rechazo de lo que ninguna memoria contiene y la
    coordinación punto a punto de la contribución~3 funcionan con los ocho dominios.

    \item \textbf{Cuantización por magnitud de las pistas semánticas.}
    Cada vector fastText se divide entre una escala global $S$, la misma en el llenado y
    en las consultas, se recorta a $[-1, 1]$ y se reparte en los 16 niveles
    (Sección~\ref{sec:pipeline-semantico}); una binarización por signo usaría solo 2.
    Con esta representación, la precisión temprana sobre el banco de 411 consultas es del
    90.0\,\% (Sección~\ref{sec:calibracion}).

    \item \textbf{Directorios perspectivales por módulo.}
    Cada módulo lleva dos directorios heteroasociativos, uno de texto y uno visual
    (Sección~\ref{sec:componentes}), y en ambos registra solo las transacciones en que
    participó, como módulo de entrada o como ganador.
    Así, cada módulo sabe de los demás lo que presenció, y por eso los directorios se
    llaman \emph{perspectivales}.
    Una frase o una imagen puede entrar por \emph{cualquier} módulo, que suma su
    directorio y los de los módulos que ha visto ganar alguna transacción y la redirige
    punto a punto al especialista; en este sistema, esa es la coordinación de la
    recuperación, en las dos modalidades.

    \item \textbf{Comparación con una sola memoria para las ocho clases.}
    Con el mismo contenido, repartirlo entre ocho especialistas deja el recuerdo más
    cerca de la instancia real más cercana de la clase de la consulta (27.0 frente a
    32.5 con 200 imágenes por clase), mezcla menos las clases cuando la primera pista es
    una etiqueta compartida (el protocolo acierta la clase entre el 79 y el 84\,\% de
    esas consultas, la EHAM única entre el 48 y el 52\,\%) y, con 200 imágenes por
    clase, acepta menos consultas fuera de dominio (2 frente a 8 de 40;
    Sección~\ref{sec:eham-unica}) [PENDIENTE: exp11 corregido].

    \item \textbf{Familiaridad y nombre de una sola memoria.}
    Las memorias homoasociativas de cada dominio se leen de la heteroasociativa
    (ecuación~\eqref{eq:marginal}), así que cada módulo necesita una sola memoria de
    contenido.
    De ella salen dos lecturas, la familiaridad y el nombre, que el daño al azar separa:
    con el 1\,\% de las celdas destruidas, el módulo nombra 64 de 800 imágenes y las
    reconoce todas (Sección~\ref{sec:una-memoria}).

    \item \textbf{Evaluación experimental.}
    Se miden nueve condiciones de calibración del directorio, con cuatro cantidades de
    consultas de formación, el efecto de los parámetros propios de la memoria ($\iota$ y
    $\kappa$), cuántas interacciones hacen falta para formar el directorio, cuánto
    contenido admite cada módulo, el comportamiento con imágenes, la comparación con una
    sola memoria para las ocho clases y la verificación de una sola memoria de contenido
    por módulo, junto con el costo computacional de reproducir todos los resultados.
\end{enumerate}
```
- **Por qué:**
  - E7: la auditoría es método, y ya está en `sec:auditoria`. Con ella salen «Ninguna decisión proviene de mecanismos ajenos» y «datos no fabricados» (5.6).
  - Entran como contribuciones la comparación con la EHAM única y la disociación entre familiaridad y nombre.
  - La 3 lleva «en este sistema» (M2).
  - La 2 y la 6 no cambian.
- **Fuente:**
  - 27.0 y 32.5: `tab:eham-unica` (d_nn 26.98 y 32.53 en `results/experimento11/README.md`). El 27.0 es del brazo del protocolo: provisional.
  - 79–84 y 48–52: `05:537-540`.
  - Distancia a la instancia más cercana de la clase de la consulta: `run_experiment11_monolithic.py:434` guarda `d_nn_truth = d_nn_target`, que `run_experiment9_member_loss.py:243-246` calcula sobre las instancias de la clase objetivo.
- **Nota:** la contribución 4 evita a propósito la clase correcta, que depende de M1.
- **Consolidación:**
  - Absorbe claridad S1 y S55 (01:98-104, que aquí sale), S8 (01:78: «lectura normalizada por conteo de registros»), S22 (01:95: «los módulos que ha visto ganar alguna transacción»), la fila `01:92` de 3.7, S13 («nueve condiciones de calibración»), «nativos» → «propios» (3.6) y `\,\%` en la contribución 2.
  - Metodología M2: sale «y cinco semillas» de la contribución 6, porque en siete de las nueve condiciones las semillas dan el mismo resultado.
  - Metodología M5: «cuando el contenido crece» pasa a «con 200 imágenes por clase».
  - **Corrección de hecho:** «la instancia real más cercana» pasa a «la instancia real más cercana de la clase de la consulta», que es lo que mide el código (claridad Parte 4, punto 11).

### 9.3 Conclusiones: resultados principales
- **Dónde:** `07:17-18`
- **Viejo:**
```latex
Sobre 171 consultas reservadas, el protocolo enruta correctamente el 97.0\% con 200
imágenes por clase (experimento 11).
```
- **Nuevo:**
```latex
Sobre 171 consultas reservadas, con directorios perspectivales, el protocolo enruta
correctamente el 97.0\,\% con 200 imágenes por clase (Sección~\ref{sec:eham-unica})
[PENDIENTE: exp11 corregido]; que supere a la cifra dentro de muestra depende de la
composición de las reservadas, que traen el nombre de su clase en el 87.7\,\% de los
casos, frente al 49.8\,\% de las consultas de la calibración.
```
- **Dónde:** `07:21-22`
- **Viejo:**
```latex
En la dirección inversa, el hemisferio visual enruta el \textbf{96.2\%} de las 656
imágenes de prueba, con \textbf{dos falsos enrutamientos} (99.7\% de precisión sobre
```
- **Nuevo:**
```latex
En la dirección inversa, el hemisferio visual enruta el \textbf{96.2\,\%} de las 656
imágenes de prueba, vistas nuevas de objetos conocidos, con \textbf{dos falsos
enrutamientos} (99.7\,\% de precisión sobre
```
- **Por qué:** E2, E7 y metodología (menores).
- **Fuente:** 87.7 y 49.8: `salida.md`, tabla M3.1 (con plural).
- **Consolidación:** marcador `[PENDIENTE: reanálisis del banco]` lleno; `\,\%` de claridad 3.1.

### 9.4 Lecciones, sin la auditoría
- **Dónde:** `07:77-83`
- **Viejo:**
```latex
\paragraph{Lecciones.}
Un sesgo de lectura no es un sesgo de estructura: con la lectura cruda, \texttt{apple}
gana el 20.5\% de las victorias aunque el directorio está casi balanceado (2.974 de
3.000 bits), y la normalización por conteo lo deja en 13.8\% sin tocar lo registrado.
Y la fidelidad del procesamiento es un resultado en sí mismo: todos los números
reportados son trazables a corridas del sistema actual, sin vectores sintéticos ni
decisiones fuera de las memorias.
```
- **Nuevo:**
```latex
\paragraph{Lecciones.}
Un sesgo de lectura no es un sesgo de lo registrado.
Con la lectura cruda, \texttt{apple} gana el 20.5\,\% de las victorias aunque los
conteos del directorio están casi parejos (2.974 de 3.000 bits), y la normalización por
conteo lo deja en 13.8\,\% sin tocar lo registrado.
Y la entropía de los conteos mide balance, no especialización; la especialización del
directorio la mide la información mutua entre el dominio de la consulta y el módulo
ganador, que con $N = 400$ llega al 88.3\,\% de su máximo con la lectura normalizada y al
81.3\,\% con la cruda.
```
- **Por qué:** E7 y 5.6. La frase de 07:81 la suprime también C1. M6.
- **Fuente:** tabla M6.1, B1 y A con $N = 400$ (0.883 y 0.813 de $H(D)$).
- **Consolidación:** marcador `[PENDIENTE: información mutua]` lleno; absorbe claridad S55 en 07:82 (la frase sale) y los dos puntos explicativos de 07:78 y 07:81 (claridad Parte 4, punto 7).

---

## Entradas BibTeX nuevas

**Estados:**
- **V:** metadatos vistos en el resultado de búsqueda del registro.
- **V+:** además, el contenido citado.
- **V parcial:** los campos que se indican solo aparecen en índices secundarios; cotejarlos antes de aplicar.

Donde no vi el nombre de pila, van iniciales.

```bibtex
@article{wegner1991transactive,
  author  = {Wegner, D. M. and Erber, R. and Raymond, P.},
  title   = {Transactive memory in close relationships},
  journal = {Journal of Personality and Social Psychology},
  volume  = {61},
  number  = {6},
  pages   = {923--929},
  year    = {1991},
  doi     = {10.1037/0022-3514.61.6.923}
}

@article{hollingshead2003gender,
  author  = {Hollingshead, Andrea B. and Fraidin, Samuel N.},
  title   = {Gender stereotypes and assumptions about expertise in transactive memory},
  journal = {Journal of Experimental Social Psychology},
  volume  = {39},
  number  = {4},
  pages   = {355--363},
  year    = {2003},
  doi     = {10.1016/S0022-1031(02)00549-8}
}

@article{moreland2000exploring,
  author  = {Moreland, R. L. and Myaskovsky, L.},
  title   = {Exploring the performance benefits of group training: Transactive memory or improved communication?},
  journal = {Organizational Behavior and Human Decision Processes},
  volume  = {82},
  number  = {1},
  pages   = {117--133},
  year    = {2000},
  doi     = {10.1006/obhd.2000.2891}
}

@article{lewis2004knowledge,
  author  = {Lewis, Kyle},
  title   = {Knowledge and performance in knowledge-worker teams: A longitudinal study of transactive memory systems},
  journal = {Management Science},
  volume  = {50},
  number  = {11},
  pages   = {1519--1533},
  year    = {2004},
  doi     = {10.1287/mnsc.1040.0257}
}

@article{austin2003transactive,
  author  = {Austin, John R.},
  title   = {Transactive memory in organizational groups: The effects of content, consensus, specialization, and accuracy on group performance},
  journal = {Journal of Applied Psychology},
  volume  = {88},
  number  = {5},
  pages   = {866--878},
  year    = {2003},
  doi     = {10.1037/0021-9010.88.5.866}
}

@article{brandon2004transactive,
  author  = {Brandon, David P. and Hollingshead, Andrea B.},
  title   = {Transactive memory systems in organizations: Matching tasks, expertise, and people},
  journal = {Organization Science},
  volume  = {15},
  number  = {6},
  pages   = {633--644},
  year    = {2004},
  doi     = {10.1287/orsc.1040.0069}
}

@article{sparrow2011google,
  author  = {Sparrow, Betsy and Liu, Jenny and Wegner, Daniel M.},
  title   = {Google effects on memory: Cognitive consequences of having information at our fingertips},
  journal = {Science},
  volume  = {333},
  number  = {6043},
  pages   = {776--778},
  year    = {2011},
  doi     = {10.1126/science.1207745}
}

@article{ren2006contingent,
  author  = {Ren, Yuqing and Carley, Kathleen M. and Argote, Linda},
  title   = {The contingent effects of transactive memory: When is it more beneficial to know what others know?},
  journal = {Management Science},
  volume  = {52},
  number  = {5},
  pages   = {671--682},
  year    = {2006},
  doi     = {10.1287/mnsc.1050.0496}
}

@article{palazzolo2006coevolution,
  author  = {Palazzolo, Edward T. and Serb, Dana A. and She, Yuechuan and Su, Chunke and Contractor, Noshir S.},
  title   = {Coevolution of communication and knowledge networks in transactive memory systems: Using computational models for theoretical development},
  journal = {Communication Theory},
  volume  = {16},
  number  = {2},
  pages   = {223--250},
  year    = {2006},
  doi     = {10.1111/j.1468-2885.2006.00269.x}
}

@article{hintzman1984minerva,
  author  = {Hintzman, Douglas L.},
  title   = {{MINERVA} 2: A simulation model of human memory},
  journal = {Behavior Research Methods, Instruments, \& Computers},
  volume  = {16},
  number  = {2},
  pages   = {96--101},
  year    = {1984},
  doi     = {10.3758/BF03202365}
}

@article{reinitz1992memory,
  author  = {Reinitz, Mark Tippens and Lammers, W. J. and Cochran, B. P.},
  title   = {Memory-conjunction errors: Miscombination of stored stimulus features can produce illusions of memory},
  journal = {Memory \& Cognition},
  volume  = {20},
  number  = {1},
  pages   = {1--11},
  year    = {1992},
  doi     = {10.3758/BF03208247}
}

@book{shallice1988neuropsychology,
  author    = {Shallice, Tim},
  title     = {From Neuropsychology to Mental Structure},
  publisher = {Cambridge University Press},
  address   = {Cambridge},
  year      = {1988},
  doi       = {10.1017/CBO9780511526817}
}

@article{plaut1995double,
  author  = {Plaut, David C.},
  title   = {Double dissociation without modularity: Evidence from connectionist neuropsychology},
  journal = {Journal of Clinical and Experimental Neuropsychology},
  volume  = {17},
  number  = {2},
  pages   = {291--321},
  year    = {1995},
  doi     = {10.1080/01688639508405124}
}

@article{bruce1986understanding,
  author  = {Bruce, Vicki and Young, Andy},
  title   = {Understanding face recognition},
  journal = {British Journal of Psychology},
  volume  = {77},
  number  = {3},
  pages   = {305--327},
  year    = {1986},
  doi     = {10.1111/j.2044-8295.1986.tb02199.x}
}

@article{mcweeny1987putting,
  author  = {McWeeny, K. H. and Young, A. W. and Hay, D. C. and Ellis, A. W.},
  title   = {Putting names to faces},
  journal = {British Journal of Psychology},
  volume  = {78},
  number  = {2},
  pages   = {143--149},
  year    = {1987},
  doi     = {10.1111/j.2044-8295.1987.tb02235.x}
}

@article{watkins1975buildup,
  author  = {Watkins, Olga C. and Watkins, Michael J.},
  title   = {Buildup of proactive inhibition as a cue-overload effect},
  journal = {Journal of Experimental Psychology: Human Learning and Memory},
  volume  = {1},
  number  = {4},
  pages   = {442--452},
  year    = {1975}
}

@article{anderson1974retrieval,
  author  = {Anderson, John Robert},
  title   = {Retrieval of propositional information from long-term memory},
  journal = {Cognitive Psychology},
  volume  = {6},
  number  = {4},
  pages   = {451--474},
  year    = {1974},
  doi     = {10.1016/0010-0285(74)90021-8}
}

@article{teyler1986hippocampal,
  author  = {Teyler, T. J. and DiScenna, P.},
  title   = {The hippocampal memory indexing theory},
  journal = {Behavioral Neuroscience},
  volume  = {100},
  number  = {2},
  pages   = {147--154},
  year    = {1986}
}

@article{damasio1989time,
  author  = {Damasio, Antonio R.},
  title   = {Time-locked multiregional retroactivation: A systems-level proposal for the neural substrates of recall and recognition},
  journal = {Cognition},
  volume  = {33},
  number  = {1--2},
  pages   = {25--62},
  year    = {1989},
  doi     = {10.1016/0010-0277(89)90005-X}
}

@article{jacobs1991adaptive,
  author  = {Jacobs, Robert A. and Jordan, Michael I. and Nowlan, Steven J. and Hinton, Geoffrey E.},
  title   = {Adaptive mixtures of local experts},
  journal = {Neural Computation},
  volume  = {3},
  number  = {1},
  pages   = {79--87},
  year    = {1991},
  doi     = {10.1162/neco.1991.3.1.79}
}

@article{jordan1994hierarchical,
  author  = {Jordan, Michael I. and Jacobs, Robert A.},
  title   = {Hierarchical mixtures of experts and the {EM} algorithm},
  journal = {Neural Computation},
  volume  = {6},
  number  = {2},
  pages   = {181--214},
  year    = {1994},
  doi     = {10.1162/neco.1994.6.2.181}
}

@inproceedings{shazeer2017outrageously,
  author        = {Shazeer, Noam and Mirhoseini, Azalia and Maziarz, Krzysztof and Davis, Andy and Le, Quoc V. and Hinton, Geoffrey E. and Dean, Jeff},
  title         = {Outrageously large neural networks: The sparsely-gated mixture-of-experts layer},
  booktitle     = {5th International Conference on Learning Representations ({ICLR} 2017), Conference Track Proceedings},
  publisher     = {OpenReview.net},
  year          = {2017},
  eprint        = {1701.06538},
  archivePrefix = {arXiv}
}

@article{fedus2022switch,
  author  = {Fedus, William and Zoph, Barret and Shazeer, Noam},
  title   = {Switch Transformers: Scaling to trillion parameter models with simple and efficient sparsity},
  journal = {Journal of Machine Learning Research},
  volume  = {23},
  number  = {120},
  pages   = {1--39},
  year    = {2022},
  url     = {http://jmlr.org/papers/v23/21-0998.html}
}

@article{willshaw1969nonholographic,
  author  = {Willshaw, D. J. and Buneman, O. P. and Longuet-Higgins, H. C.},
  title   = {Non-holographic associative memory},
  journal = {Nature},
  volume  = {222},
  number  = {5197},
  pages   = {960--962},
  year    = {1969},
  doi     = {10.1038/222960a0}
}

@article{kosko1988bidirectional,
  author  = {Kosko, Bart},
  title   = {Bidirectional associative memories},
  journal = {IEEE Transactions on Systems, Man, and Cybernetics},
  volume  = {18},
  number  = {1},
  pages   = {49--60},
  year    = {1988},
  doi     = {10.1109/21.87054}
}

@article{hopfield1982neural,
  author  = {Hopfield, J. J.},
  title   = {Neural networks and physical systems with emergent collective computational abilities},
  journal = {Proceedings of the National Academy of Sciences of the United States of America},
  volume  = {79},
  number  = {8},
  pages   = {2554--2558},
  year    = {1982},
  doi     = {10.1073/pnas.79.8.2554}
}

@book{kanerva1988sparse,
  author    = {Kanerva, Pentti},
  title     = {Sparse Distributed Memory},
  publisher = {MIT Press},
  address   = {Cambridge, MA},
  year      = {1988},
  isbn      = {0-262-11132-2}
}

@inproceedings{krotov2016dense,
  author        = {Krotov, Dmitry and Hopfield, John J.},
  title         = {Dense associative memory for pattern recognition},
  booktitle     = {Advances in Neural Information Processing Systems 29 ({NIPS} 2016)},
  pages         = {1172--1180},
  year          = {2016},
  eprint        = {1606.01164},
  archivePrefix = {arXiv}
}

@inproceedings{ramsauer2021hopfield,
  author        = {Ramsauer, Hubert and Sch{\"a}fl, Bernhard and Lehner, Johannes and Seidl, Philipp and Widrich, Michael and Gruber, Lukas and Holzleitner, Markus and Adler, Thomas and Kreil, David P. and Kopp, Michael K. and Klambauer, G{\"u}nter and Brandstetter, Johannes and Hochreiter, Sepp},
  title         = {Hopfield networks is all you need},
  booktitle     = {9th International Conference on Learning Representations ({ICLR} 2021)},
  year          = {2021},
  eprint        = {2008.02217},
  archivePrefix = {arXiv}
}

@article{amit1985spin,
  author  = {Amit, Daniel J. and Gutfreund, Hanoch and Sompolinsky, H.},
  title   = {Spin-glass models of neural networks},
  journal = {Physical Review A},
  volume  = {32},
  number  = {2},
  pages   = {1007--1018},
  year    = {1985},
  doi     = {10.1103/PhysRevA.32.1007}
}

@incollection{mccloskey1989catastrophic,
  author    = {McCloskey, M. and Cohen, N. J.},
  title     = {Catastrophic interference in connectionist networks: The sequential learning problem},
  booktitle = {Psychology of Learning and Motivation},
  volume    = {24},
  pages     = {109--165},
  year      = {1989},
  doi       = {10.1016/S0079-7421(08)60536-8}
}

@article{smith1980contract,
  author  = {Smith, Reid G.},
  title   = {The contract net protocol: High-level communication and control in a distributed problem solver},
  journal = {IEEE Transactions on Computers},
  volume  = {C-29},
  number  = {12},
  pages   = {1104--1113},
  year    = {1980},
  doi     = {10.1109/TC.1980.1675516}
}

@inproceedings{decker1997middle,
  author    = {Decker, Keith and Sycara, Katia and Williamson, Mike},
  title     = {Middle-agents for the {I}nternet},
  booktitle = {Proceedings of the Fifteenth International Joint Conference on Artificial Intelligence ({IJCAI}-97)},
  volume    = {1},
  pages     = {578--582},
  address   = {Nagoya, Japan},
  year      = {1997},
  url       = {https://www.ijcai.org/proceedings/1997/85}
}

@inproceedings{crespo2002routing,
  author    = {Crespo, Arturo and Garcia-Molina, Hector},
  title     = {Routing indices for peer-to-peer systems},
  booktitle = {Proceedings of the 22nd International Conference on Distributed Computing Systems ({ICDCS} 2002)},
  pages     = {23--32},
  year      = {2002},
  url       = {https://ieeexplore.ieee.org/document/1022239}
}

@incollection{callan2000distributed,
  author    = {Callan, Jamie},
  title     = {Distributed information retrieval},
  booktitle = {Advances in Information Retrieval: Recent Research from the Center for Intelligent Information Retrieval},
  editor    = {Croft, W. Bruce},
  series    = {The Information Retrieval Series},
  volume    = {7},
  pages     = {127--150},
  publisher = {Springer},
  address   = {Boston, MA},
  year      = {2000},
  doi       = {10.1007/0-306-47019-5_5}
}
```

| Clave | Estado | Registro | Por cotejar |
|---|---|---|---|
| `wegner1991transactive` | V+ | [PubMed 1774630](https://pubmed.ncbi.nlm.nih.gov/1774630/) | — |
| `hollingshead2003gender` | V+ | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0022103102005498) | — |
| `moreland2000exploring` | V+ | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0749597800928917) | el DOI concuerda con el PII |
| `lewis2004knowledge` | V parcial, V+ | [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.1040.0257) | volumen y páginas (solo RePEc) |
| `austin2003transactive` | V parcial | [PubMed 14516250](https://pubmed.ncbi.nlm.nih.gov/14516250/) (título) | volumen, páginas y DOI |
| `brandon2004transactive` | V parcial, V+ | [INFORMS](https://pubsonline.informs.org/doi/10.1287/orsc.1040.0069) | volumen y páginas (solo RePEc) |
| `sparrow2011google` | V+ | [PubMed 21764755](https://pubmed.ncbi.nlm.nih.gov/21764755), [Science](https://www.science.org/doi/10.1126/science.1207745) | nombres de pila |
| `ren2006contingent` | V+ | [INFORMS](https://pubsonline.informs.org/doi/10.1287/mnsc.1050.0496), DBLP | — |
| `palazzolo2006coevolution` | V parcial | [Oxford Academic](https://academic.oup.com/ct/article/16/2/223/4098757) | página final y DOI |
| `hintzman1984minerva` | V+ parcial | [Springer](https://link.springer.com/article/10.3758/BF03202365) | — |
| `reinitz1992memory` | V+ | [Springer](https://link.springer.com/article/10.3758/BF03208247) | tercer autor |
| `shallice1988neuropsychology` | V | [Cambridge Core](https://www.cambridge.org/core/books/from-neuropsychology-to-mental-structure/EC50DDFA1C20683B98DC1D731D578468) | contenido |
| `plaut1995double` | V+ | [PubMed 7629273](https://pubmed.ncbi.nlm.nih.gov/7629273/) | — |
| `bruce1986understanding` | V+ | [Wiley](https://bpspsychub.onlinelibrary.wiley.com/doi/abs/10.1111/j.2044-8295.1986.tb02199.x) | — |
| `mcweeny1987putting` | V+ | [Wiley](https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/j.2044-8295.1987.tb02235.x) | iniciales |
| `watkins1975buildup` | V parcial, V+ | [Ovid](https://www.ovid.com/journals/jephln/pdf/00004787-197507000-00012~buildup-of-proactive-inhibition-as-a-cue-overload-effect), [ERIC](https://eric.ed.gov/?id=ej123687) | DOI (no apareció, no lo pongo) e iniciales |
| `anderson1974retrieval` | V+ | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0010028574900218) | — |
| `teyler1986hippocampal` | V, V+ parcial | [PubMed 3008780](https://pubmed.ncbi.nlm.nih.gov/3008780/) | DOI: no apareció; `bibliografia_marco_teorico.bib` trae uno |
| `damasio1989time` | V+ parcial | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/001002778990005X) | — |
| `jacobs1991adaptive` | V+ parcial | [MIT Press Direct](https://direct.mit.edu/neco/article/3/1/79/5560/Adaptive-Mixtures-of-Local-Experts) | — |
| `jordan1994hierarchical` | V+ | [MIT Press Direct](https://direct.mit.edu/neco/article/6/2/181/5779/Hierarchical-Mixtures-of-Experts-and-the-EM) | — |
| `shazeer2017outrageously` | V+ parcial | [DBLP](https://dblp.org/rec/conf/iclr/ShazeerMMDLHD17), arXiv 1701.06538 | URL de OpenReview (omitida) |
| `fedus2022switch` | V+ | [JMLR](https://jmlr.org/papers/v23/21-0998.html), arXiv 2101.03961 | — |
| `willshaw1969nonholographic` | V | [Nature](https://www.nature.com/articles/222960a0) | — |
| `kosko1988bidirectional` | V | [ACM DL](https://dl.acm.org/doi/10.1109/21.87054), DBLP | no apareció en IEEE Xplore |
| `hopfield1982neural` | V+ | [PNAS](https://www.pnas.org/doi/10.1073/pnas.79.8.2554) | — |
| `kanerva1988sparse` | V | [MIT Press](https://mitpress.mit.edu/9780262514699/sparse-distributed-memory/) y catálogos universitarios | — |
| `krotov2016dense` | V+ | [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2016/hash/eaae339c4d89fc102edd9dbdb6a28915-Abstract.html), DBLP (páginas) | — |
| `ramsauer2021hopfield` | V+ parcial | [DBLP](https://dblp.org/rec/conf/iclr/RamsauerSLSWGHA21) (13 autores), arXiv | — |
| `amit1985spin` | V parcial, V+ | [APS](https://link.aps.org/doi/10.1103/PhysRevA.32.1007) | número y página final (repositorio de la Universidad Hebrea). Los estados mezcla son metaestables: por eso el texto lo dice. |
| `mccloskey1989catastrophic` | V+ | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0079742108605368) | editor y editorial (no vistos, no los pongo). **Consolidación:** `@incollection` sin `publisher` hace que BibTeX avise; hay que agregar la editorial tras cotejarla. |
| `smith1980contract` | V+ | [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/1675516/) | — |
| `decker1997middle` | V+ | [IJCAI](https://ijcai.org/proceedings/1997/85) | páginas: 578–582 en IJCAI, 578–583 en DBLP |
| `crespo2002routing` | V parcial | [IEEE Xplore 1022239](https://ieeexplore.ieee.org/document/1022239/), DBLP | DOI: no lo vi escrito, por eso va la URL |
| `callan2000distributed` | V+ | [Springer](https://link.springer.com/chapter/10.1007/0-306-47019-5_5) | — |

**Entradas existentes:**
- `wegner1995computer`: V+ en esta sesión ([Guilford](https://guilfordjournals.com/doi/10.1521/soco.1995.13.3.319)).
- `wegner1987transactive`: el registro coincide ([Springer](https://link.springer.com/chapter/10.1007/978-1-4612-4634-3_9), pp. 185–208), pero la cita de la p. 186 no la vi en el capítulo.
- Quedan sin citar `fortin2004recollection`, `eichenbaum2007medial`, `diana2007imaging` y `squire2007recognition`.

**Revisión de la consolidación** (script, sin consultar la web):
- Las 35 entradas tienen las llaves cerradas y los campos obligatorios de su tipo, salvo `mccloskey1989catastrophic` (`@incollection` sin `publisher`).
- Ninguna clave nueva repite una de `referencias.bib`, ni hay claves repetidas entre las nuevas; ningún DOI ni título coincide con una entrada existente.
- Todos los `\cite` de los textos nuevos tienen entrada, nueva o existente, y las 35 entradas nuevas se citan en algún texto nuevo.
- Las 35 declaran su estado (V, V+, V parcial o combinaciones). Ninguna queda sin estado.
- `main.tex` usa `apalike`, que no imprime `doi`, `url` ni `eprint`: esos campos no estorban, pero tampoco salen en la bibliografía.

### Citas que pidió el jurado y no propongo (sin verificar)

| Cita | Para qué | Dónde iría |
|---|---|---|
| Hodges et al. (1992); Rogers et al. (2004) | demencia semántica, anomia, deriva hacia supraordinadas | 6.5, «Que el nombre sea lo más frágil…» |
| Warrington y Shallice (1984); Farah y McClelland (1991) | déficits de categoría | 6.4, punto de las pistas compartidas |
| Hinton y Shallice (1991) | degradación gradual | 6.5, «La caída del nombre tampoco es gradual» |
| Murdock (1982); Humphreys, Bain y Pike (1989); Hintzman (1988) | almacén único compuesto | 6.5, párrafo de MINERVA 2 |
| Dunn y Kirsner (1988) | asociación inversa | 6.5, junto a Shallice |
| McClelland et al. (1995); Frankland y Bontempi (2005) | consolidación: el mediador deja de hacer falta | 6.4, directorio separado del contenido |
| Reder y Ritter (1992); Koriat (1993) | sensación de saber por familiaridad | 6.5, estado intermedio |
| Glucksberg y McCloskey (1981) | decidir rápido «no sé» | 6.4, rechazo |
| Bottger (1984) | tiempo de palabra frente a experticia | 6.2, junto a B1 |
| Si y Callan (2003) | normalización por tamaño de colección | 2.4, precedente de B1 |
| Lewis (2003) | especialización, credibilidad, coordinación | 2.3, entropía |
| Asch (1946) | primeras impresiones | 6.4, orden |
| Hollingshead (1998) | recuperación en parejas | 6.4 (M2) |
| Weldon y Bellinger (1997); Rajaram y Pereira-Pasarin (2010) | inhibición colaborativa | resumen y 01:4-5 |

---

## Marcadores `[PENDIENTE: …]`

| Marcador | Dónde | Qué falta | Estado tras la consolidación |
|---|---|---|---|
| `[PENDIENTE: codificador sin pérdida de clase]` | 3.3 (dos veces); 7.6 | enrutamiento de prueba y cobertura con objetos nuevos con el codificador sin pérdida de clase | queda: depende del codificador sin pérdida de clase |
| `[PENDIENTE: reanálisis del banco]` | 4.2 (`05:28-29`); 9.3 (`07:17-18`) | composición de las 171 reservadas y por qué su 97.0 % supera al 93.0 % | lleno con M3.1 y M2.3 |
| `[PENDIENTE: información mutua]` | 5.4 (dos veces); 5.5; 9.4 | I(dominio; ganador) del directorio de calibración, en bits y normalizada | lleno con M6.1 |
| `[PENDIENTE: líneas base]` | 7.1 (dos veces); 7.6; 7.8; 9.1 | `pear` con centroide y con kNN sobre los mismos vectores; decide la redacción final de 6.1, 07 y el resumen | queda: depende de las líneas base de centroide y kNN |
| `[PENDIENTE: calibración con conjunto fijo]` | 4.4; 7.6 | precisión madura con pocas y con muchas consultas de formación, sobre un conjunto fijo. No estaba en la lista de marcadores: lo agregué porque metodología M2 pide retirar «hace falta el banco completo». | queda: depende de la calibración con conjunto fijo |
| `[PENDIENTE: exp11 corregido]` | 4.2; 7.3; 9.1 (dos veces); 9.2; 9.3; y 7.7 por la frase que sigue en 07:58-59 | cifras del brazo del protocolo del experimento 11 | nuevo en la consolidación: depende de exp11 con los directorios reiniciados |

---

## Lo que queda fuera de esta propuesta

- **Otra propuesta:** términos, notación y lengua (C1–C12, 5.1–5.5, 5.7), incluidos «hemisferio» y el nombre del TME.
- **Propuesta de cifras:** metodología M1 (`06:189-193` y `07:60-61`), en `revision_jurado_metodologia_prosa.md`.
- **Estructura:**
  - E3 en 05 y en la tabla 5;
  - E4, salvo lo que tocan 4.4 y 5.2;
  - E5: exp15 y «de 76 a 96 %»;
  - E8, salvo donde reescribo;
  - E9.
- **Menores del dictamen de Wegner:**
  - «recordar es muestrear» (`02:108`);
  - la Author Correction de Pineda, Fuentes y Morales (2021);
  - ConceptNet 5.5 frente a 5.7;
  - la ecuación o página para `02:252-260`;
  - la identidad de las lecturas marginales mientras no se sature ninguna celda.
