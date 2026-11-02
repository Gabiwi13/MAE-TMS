Los 37 marcadores quedan así: **17 llenados** (uno solo en parte), **6 siguen pendientes** y **14 los cubre el encuadre**. No edité la tesis, no hice commit, no hice push y no creé ramas. Solo hice el `checkout` de `una-hetero` en `6197bc3`, como pedía la preparación.

Lo que más pesa:
- **Con 25 imágenes por clase la EHAM única clasifica mejor que el protocolo**, por 4.4 puntos [−8.1, −0.9], así que el «empatan en todos los cortes» de M1 ya no vale; desde 50 sí empatan.
- **Con un conjunto de evaluación fijo, el directorio solo alcanza a la fase temprana, sin superarla.** El +3.0 a +5.5 de la tesis es dentro de muestra y no se reproduce.

Abreviaturas de las fuentes:
- **R11:** `results/experimento11_protocolo_corregido/ruteo/ruteo.md` (con `resumen.json`).
- **CAL:** `results/calibracion_evaluacion_fija/README.md`, tabla «Los 5 sorteos de E juntos» (comprobada contra `resumen.json`).
- **CSC:** `results/codificador_sin_clase/comparacion.md`.
- **LB:** `results/lineas_base/README.md`.
- **P16:** `results/objetos_nuevos_codificador_por_pliegue_parcial/tablas.md`.

## Tabla de los 37 marcadores

| # | Punto | Marcador | Estado | Cifra | Fuente |
|---|---|---|---|---|---|
| 1 | Estructura 3.3 (k), 1.º | codificador | llenado | ruteo de prueba 70.4 % (462/656) frente a 96.2 | CSC, «ruteo de test (656)» |
| 2 | Estructura 3.3 (k), 2.º | codificador | llenado | objeto nuevo 59.3 % [55.5, 62.9] frente a 89.2 | CSC, «exp16, objeto nuevo, punta a punta» |
| 3 | Estructura 4.2 | exp11 | llenado | 96.8 % [96.3, 97.4] con N = 200 (era 97.0) | R11, «Texto», ruteo ok |
| 4 | Estructura 4.4 | calibración | llenado, **cambia de sentido** | madura B1 78.9 → 91.0; temprana 89.7; diferencia −10.7 → +1.3 | CAL |
| 5–6 | Estructura 7.1 (6.1), dos | líneas base | lo cubre el encuadre | LB no da `pear` por clase, solo el total (ver nota 1) | LB |
| 7 | Estructura 7.3 | exp11 | sigue pendiente | 79–84 % con pista compartida: el solo ruteo no mide ese subconjunto | R11, «Qué no cubre» |
| 8 | Estructura 7.6 (07) | codificador | lo cubre el encuadre | 70.4 %, 169 falsos | CSC |
| 9 | Estructura 7.6 (07) | líneas base | lo cubre el encuadre | `pear`: no reportado | LB |
| 10 | Estructura 7.6 (07) | calibración | lo cubre el encuadre | fuera de muestra +1.3 con N = 291 (de −0.8 a +6.7 según el sorteo); el +3.0 es dentro de muestra | CAL |
| 11 | Estructura 7.8 (07) | líneas base | lo cubre el encuadre | ver nota 1 | LB |
| 12 | Estructura 9.1 (resumen), 1.º | exp11 | lo cubre el encuadre | 96.8 % | R11 |
| 13 | Estructura 9.1 (resumen), 2.º | exp11 | lo cubre el encuadre | fuera de dominio 2 frente a 8 de 40, confirmado; fidelidad (d_nn) y mezcla, pendientes | R11 |
| 14 | Estructura 9.1 (resumen), 3.º | líneas base | lo cubre el encuadre | ver nota 1 | LB |
| 15 | Estructura 9.2 (contribuciones) | exp11 | lo cubre el encuadre | fuera de dominio confirmado; 27.0 frente a 32.5 (d_nn) y 79–84 %, pendientes | R11 |
| 16 | Estructura 9.3 (07) | exp11 | lo cubre el encuadre | 96.8 % | R11 |
| 17 | M1.1, 1.º | exp11 | llenado | protocolo sobre el total 93.2 / 96.8 / 96.8 / 96.8 | R11, «Texto» |
| 18 | M1.1, 2.º | exp11 | llenado, **cambia de sentido** | N = 200: −0.1 [−2.9, +2.9], p = 0.86; N = 25: −4.4 [−8.1, −0.9] | R11, «Protocolo contra EHAM única» |
| 19 | M1.1, 3.º | exp11 | llenado, **cambia de sentido** | empatan desde 50; con 25 acierta más la EHAM única | ídem |
| 20 | M1.1, 4.º | exp11 | llenado | distancia al oráculo 6.8 con 25 y 3.2 desde 50 | R11 y oráculo al 100 % en `results/experimento11/README.md` |
| 21 | M1.2 (pie de la Tabla 5) | exp11 | llenado en parte | total, responde y enrutamiento llenos; respondidas y distancia del protocolo quedan «[P]» (dependen de d_nn) | R11 |
| 22 | M1.4, 1.º | exp11 | llenado, **cambia de sentido** | como el 18 | R11 |
| 23 | M1.4, 2.º | exp11 | llenado | imagen, responde 81.2 % con N = 200 (sin cambio) | R11, «Imagen» |
| 24 | M1.4, 3.º | exp11 | llenado | 3.2 desde 50 (6.8 con 25) | R11 |
| 25 | M1.5, 1.º | exp11 | sigue pendiente | 79–84 % con pista compartida: no lo mide el solo ruteo | R11 |
| 26 | M1.5, 2.º | exp11 | sigue pendiente | 3.0 % de dominio ajeno: depende de la evocación muestreada (los 3200 destinos visuales no cambian) | R11 |
| 27–29 | M1.6 (07), tres | exp11 | lo cubre el encuadre | 3.0 %, pendiente; empatan desde 50 y con 25 gana la EHAM; 3.2 desde 50 | R11 |
| 30 | M2.2 | calibración | llenado, **cambia de sentido** | 78.9 / 86.0 / 89.8 / 91.0; temprana 89.7 | CAL |
| 31 | M2.7 (05:256-260) | calibración | llenado | 78.9 → 91.0, hasta la temprana | CAL |
| 32 | M4.1 | exp16 por pliegue | sigue pendiente | 3 de 10 pliegues. Provisional: objeto nuevo 89.3 % [87.2, 91.2], 33 falsos de 984 | P16 |
| 33 | M5.1, 1.º | exp11 | llenado, confirma | protocolo 4 de 40 y 2 con la compuerta, en los cuatro cortes | R11, «Fuera de dominio» |
| 34 | M5.1, 2.º | exp11 | llenado, confirma | p = 0.031 / 0.25 / 1 y 0.22 sin cambio (las 1600 filas son iguales a las viejas) | R11 y reanálisis M5.1 |
| 35 | M5.2 | exp11 | llenado, confirma | p = 0.031 | ídem |
| 36 | M5.3 | exp11 | sigue pendiente | el solo ruteo no recalcula la doble compuerta sobre las 171 (1.5 y 2.1 %, de `results/experimento11/compuerta_reservadas.md`, con los directorios acumulados) | — |
| 37 | Claridad S48 | exp11 | sigue pendiente | ningún experimento recalcula el 1.3 % entre arquitecturas con el protocolo corregido; probablemente haya que quitar la cifra | — |

**Nota 1, para la sesión de encuadre (líneas base):**
- En texto, los decisores sin memoria empatan con el sistema. En las 80 del protocolo, 5nn da 81.5 y el voto 79.4, frente a 81.25.
- La tabla de conteos de tokens exactos no se distingue del directorio: 92.3 frente a 93.0, p = 0.58.
- En imagen, centroide y kNN sobre los mismos latentes aciertan 652–655 de 656, frente a 631 del sistema.
- Esto choca con las frases sobre el mecanismo en 6.1, 07 y el resumen.
- `pear` por clase no está en ninguna tabla; habría que sacarlo de `filas_texto.json`.
- Las comparaciones de LB sobre las 171 reservadas usan el T-protocolo viejo (97.0).

## Puntos llenados: viejo y nuevo

### Estructura 3.3, limitación nueva (k)
- **Dónde:** inserción después de `06:336` (último renglón, limitación (j)); no tiene «Viejo».
- **Nuevo:**
```latex

\paragraph{(k) Supervisión del codificador visual.}
El codificador se entrenó con la reconstrucción y una entropía cruzada de clasificación
de peso 0.1 (Sección~\ref{sec:percepcion}).
La cabeza clasificadora no participa en ninguna decisión, pero la pérdida moldea el
espacio latente sobre el que operan los directorios visuales y las memorias de
contenido: desde ese espacio, la cabeza auxiliar alcanza una precisión del 99.7\,\%.
Con un codificador entrenado sin esa pérdida, el enrutamiento de las 656 imágenes de
prueba es del 70.4\,\% (frente al 96.2\,\%), y la cobertura de punta a punta con
objetos nuevos, del 59.3\,\% (frente al 89.2\,\%).
Además, el fallo deja de ser rechazo.
Los falsos enrutamientos de prueba pasan de 2 a 169 de 656, y el rechazo queda casi
igual (3.8 frente a 3.5\,\%).
La clase sigue en el espacio latente (una sonda lineal la acierta en el 94.2\,\%),
pero repartida en combinaciones de coordenadas, y la contención compara coordenada por
coordenada.
```
- **Fuente:**
  - 70.4, 2 → 169 falsos y rechazo 3.5 → 3.8: CSC, filas «ruteo de test (656)», «falsos ruteos de test» y «rechazo de test».
  - 59.3: CSC, fila «exp16, objeto nuevo, punta a punta».
  - 94.2: `results/codificador_sin_clase/README.md`, «Diseño».
  - Los dos codificadores vieron los diez objetos, así que 59.3 y 89.2 se comparan con la misma fuga.
  - Las tres últimas frases son un agregado mío, no las pedía el marcador; se pueden quitar.

### Estructura 4.2
- **Dónde:** `05:28-29`
- **Viejo:**
```latex
Sobre 171 consultas reservadas, el protocolo transactivo del experimento 11 enruta
correctamente el 97.0\% con 200 imágenes por clase (Sección~\ref{sec:eham-unica}).
```
- **Nuevo:**
```latex
Sobre 171 consultas reservadas, el protocolo transactivo de la comparación con una sola
EHAM enruta correctamente el 96.8\,\% con 200 imágenes por clase
(Sección~\ref{sec:eham-unica}), con directorios perspectivales formados con las otras
240 consultas.
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
- **Fuente:** R11, tabla «Texto», N = 200, protocolo corregido, ruteo ok 96.8 [96.3, 97.4].

### Estructura 4.4, discusión 6.4 completa
- **Dónde:** `06:78-120`. Primera línea: `\subsection{Lectura desde la teoría de memoria transactiva de Wegner}`. Última línea: `\end{itemize}`.
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
    Sobre un conjunto fijo de 120 consultas que nunca registran en el directorio, la
    precisión madura con la lectura normalizada sube del 78.9 al 91.0\,\% entre 50 y 291
    consultas de formación, así que la formación mejora la decisión en consultas que no
    vio.
    Con ese crecimiento la madura alcanza a la fase temprana, que sobre esas consultas
    acierta el 89.7\,\%, sin superarla de forma robusta; la diferencia pasa de $-10.7$
    puntos con 50 consultas a $+0.2$ con 200 y $+1.3$ con 291, y con 291 va de $-0.8$ a
    $+6.7$ según qué consultas se evalúen (Sección~\ref{sec:calibracion}).
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
- **Fuente:**
  - CAL: madura B1 78.9 → 91.0, diferencia −10.7 / +0.2 / +1.3.
  - Temprana 89.7: la nota bajo la misma tabla de CAL.
  - De −0.8 a +6.7: la fila «B1, madura − temprana (rango…)».
  - Solo cambia el primer ítem.

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
200 imágenes por clase, y el protocolo, el 93.2, 96.8, 96.8 y 96.8\,\%.
Las diez semillas no cambian las consultas, así que la diferencia se acompaña de un
intervalo de 95\,\% por remuestreo de consultas.
Desde 50 imágenes por clase, los dos empatan en acierto de clase; la diferencia es de
$-0.7$ puntos con 50 y con 100 ($[-3.3, +2.0]$ y $[-3.4, +1.9]$) y de $-0.1$ con 200
($[-2.9, +2.9]$).
Con 25, la EHAM única acierta 4.4 puntos más ($[-8.1, -0.9]$).
McNemar exacto sobre los pares de semilla, consulta y sorteo da $p = 0.86$ con 200
imágenes por clase y $p < 0.05$ con 25, 50 y 100, pero trata como independientes las
treinta repeticiones de cada consulta y es optimista.
Lo que cuesta elegir el módulo con el directorio en lugar de con la clase real, la
distancia del protocolo al oráculo sobre el total, es de 6.8 puntos con 25 imágenes por
clase y de 3.2 desde 50.
```
- **Fuente:**
  - R11, «Texto»: clase sobre el total y responde 98.4–98.7.
  - R11, «Protocolo contra EHAM única» y `resumen.json`, `pruebas`. Con 100, el extremo superior es +1.949, que redondea a +1.9; el README pone +2.0 por doble redondeo.
  - Oráculo 100 %: `results/experimento11/README.md`, filas T-oraculo, un brazo que no usa directorio.
  - Distancia al oráculo: 100 − 93.16 = 6.84 y 100 − 96.84 = 3.16.
  - El McNemar por consulta del reanálisis (tabla M1.2) no se recalculó con el protocolo corregido. Por eso el texto se apoya en el intervalo por consulta y quita «ni sobre las respondidas».

### M1.2 Pie de la Tabla 5 (llenado en parte)
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
    enrutamiento a la clase de la consulta [PENDIENTE: exp11 corregido, d\_nn: celdas
    «[P]» del protocolo]. Imagen $\to$ texto: 80 imágenes de prueba;
```
- **Filas de M1.3 (`05:495-504`), Viejo:**
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
- **Filas de M1.3, Nuevo:**
```latex
        Medida & Configuración & 25 & 50 & 100 & 200 \\
        \midrule
        Clase correcta,            & EHAM única & 97.6 & 97.5 & 97.6 & 96.9 \\
        respondidas (\%)           & Protocolo  & [P]  & [P]  & [P]  & [P]  \\
                                   & Oráculo    & 100  & 100  & 100  & 100  \\
        \midrule
        Clase correcta,            & EHAM única & 97.6 & 97.5 & 97.6 & 96.9 \\
        total (\%)                 & Protocolo  & 93.2 & 96.8 & 96.8 & 96.8 \\
                                   & Oráculo    & 100  & 100  & 100  & 100  \\
        \midrule
        Responde (\%)              & Protocolo  & 98.4 & 98.7 & 98.7 & 98.7 \\
        \midrule
        Enrutamiento correcto (\%) & Protocolo  & 93.2 & 96.8 & 96.8 & 96.8 \\
        \midrule
        Distancia a la instancia   & EHAM única & 22.9 & 26.6 & 29.4 & 32.5 \\
        más cercana de su clase    & Protocolo  & [P]  & [P]  & [P]  & [P]  \\
```
- **Fuente:**
  - R11, «Texto».
  - Fuera de este «Viejo», las filas del protocolo «Imagen → texto: responde» (41.2 / 67.5 / 78.7 / 81.2) y «Fuera de dominio» (4 (2)) no cambian (R11, «Imagen» y «Fuera de dominio»).
  - «Dominio ajeno» del protocolo (`05:514`) sigue pendiente.

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
En acierto de clase, los dos empatan desde 50 imágenes por clase.
Sobre el total de las 171 consultas reservadas, contando la falta de respuesta como
fallo, la diferencia entre el protocolo y la EHAM única es de $-0.7$ puntos con 50 y con
100 imágenes por clase y de $-0.1$ con 200, con intervalos de 95\,\% por remuestreo de
consultas que incluyen el cero.
Con 25, la EHAM única acierta 4.4 puntos más ($[-8.1, -0.9]$), porque el directorio
todavía enruta peor (93.2\,\% de enrutamiento correcto;
Sección~\ref{sec:eham-unica}).

La partición cuesta cobertura y requiere un directorio.
El especialista deja sin respuesta al 2.5\,\% de las imágenes de prueba con 200 por
clase, que la EHAM única responde: una de las 80 imágenes porque la contención es
estricta en las 64 coordenadas del latente y otra porque el recuerdo no devuelve palabras.
Es parte del rechazo residual del hemisferio visual (limitación (b)); el protocolo de
esta comparación, que forma su directorio visual sin variantes, responde al 81\,\%.
A eso se suman el error del directorio, de 3.2 puntos de clase sobre el total desde 50
imágenes por clase (6.8 con 25), y ocho veces las celdas de memoria, porque hay una
heteroasociativa por módulo en lugar de una sola.
```
- **Fuente:** la misma de M1.1. El 81 % es R11, «Imagen», responde 81.2 con N = 200; los 3200 destinos son idénticos a los viejos. El 2.5 % es del oráculo.

### M2.2 Formación del directorio y composición (inserción)
- **Dónde:** después del texto de estructura 4.2 (que reemplaza `05:28-29`) y antes de la tabla (`05:31`); no tiene «Viejo».
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
Con un conjunto evaluado fijo, independiente de $N$ ---15 consultas por clase que nunca
registran en el directorio, con la formación sorteada entre las 291 restantes---, la
precisión madura con la lectura B1 es del 78.9, 86.0, 89.8 y 91.0\,\% con $N = 50$,
100, 200 y 291, y la temprana sobre esas consultas, del 89.7\,\%.
La formación mejora la madura en consultas que no vio, pero solo hasta alcanzar a la
temprana; la diferencia es de $-10.7$, $-3.7$, $+0.2$ y $+1.3$ puntos, y con $N = 291$
va de $-0.8$ a $+6.7$ según qué consultas se evalúen.
La lectura B1 supera a la cruda en todos los $N$, por 4.5 a 8.8 puntos, y G queda igual
que B1 (91.3 frente a 91.0\,\% con la formación más grande).\footnote{Calibración con
un conjunto de evaluación fijo, \texttt{results/calibracion\_evaluacion\_fija/README.md},
tabla «Los 5 sorteos de E juntos»: media de cinco sorteos del conjunto evaluado, con
cinco semillas cada uno.}
```
- **Fuente:** CAL. Que B1 supera a A sale de «Lectura», «B1 contra A». Comprobado contra `resumen.json`.

### M2.7, segundo pasaje
El pasaje de `05:148-150` no lleva marcador y queda como en la propuesta.
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
Con un conjunto evaluado fijo, formar el directorio con más interacciones sube la
precisión madura del 78.9 al 91.0\,\% entre unas 6 y 36 consultas de formación por
clase (50 y 291 en total), hasta el nivel de la fase temprana sobre esas consultas
(89.7\,\%), sin superarlo de forma robusta (Sección~\ref{sec:calibracion}).
```
- **Fuente:** CAL. «Unas 6 y 36 por clase» es 50/8 y 291/8.

### M5.1 Fuera de dominio
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
destino debe contener la pista) baja a 2.
La doble compuerta se agregó después de ver, en estas mismas 40 consultas, las dos que
el directorio enviaba a un módulo que no las contiene (limitación (g)).
Con McNemar exacto, la diferencia entre la EHAM única y el protocolo con doble compuerta
solo es significativa con 200 imágenes por clase ($p = 0.031$, con seis consultas que
acepta solo la EHAM única y ninguna que acepte solo el protocolo); con 100, $p = 0.25$,
y con 25 y 50, $p = 1$.
Sin la segunda compuerta, con 200 imágenes por clase, $p = 0.22$.
```
- **Fuente:**
  - R11, «Fuera de dominio»: protocolo 10 % y 5 %; EHAM única 5 / 5 / 12.5 / 20 %. Las 1600 filas son idénticas a las viejas.
  - Los $p$ por consulta son los del reanálisis M5.1.
  - Se comprueban con R11, filas `ood`: con N = 200 y compuerta, 60 pares contra 0, es decir 6 consultas contra 0 en diez semillas iguales; con 100, 3 contra 0; sin compuerta con 200, 5 contra 1.

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
compuerta se decidió después de ver estas consultas (limitación (g)).
```
- **Fuente:** la misma de M5.1. El 4.6–6.2 compara la EHAM única con el oráculo, que no usan directorio.

## «Nuevo» que cambiaron de sentido

1. **M1.1 y M1.4 (y M1.6, en el encuadre).** «En ningún corte es significativa; los dos empatan» pasa a «empatan desde 50; con 25 la EHAM única acierta 4.4 puntos más [−8.1, −0.9]». Con 200, la diferencia pasa de +0.1 a −0.1.
2. **M1.1 y M1.4, el costo del directorio.** La distancia al oráculo sube de 4.7 a 6.8 con 25, y de 2.6–3.0 a 3.2 desde 50.
3. **Estructura 4.4, M2.2 y M2.7, la calibración.** La formación sí mejora la madura en consultas que no vio (78.9 → 91.0 con evaluación fija), pero solo alcanza a la temprana (89.7). La ventaja dentro de muestra (+3.0 a +5.5) no se reproduce, y el signo de la diferencia cambia según el sorteo. Además, G no supera a B1.
4. **Estructura 3.3 (k).** No anticipaba nada, pero el resultado es fuerte: sin la pérdida de clase, el fallo visual deja de ser rechazo (169 falsos de 656). Lo agregué como frase nueva y se puede quitar.
5. **Para la sesión de encuadre** (no los toqué):
   - las líneas base de la nota 1 contradicen «el mecanismo aporta» en texto e imagen;
   - el «+3.0 puntos» de 7.6 es dentro de muestra;
   - el 97.0 de 9.1 y 9.3 pasa a 96.8.

## Comprobaciones
- **El `.tex8` no cambió:** `git diff df2f893 6197bc3 -- .tex8` sale vacío.
- **Todos los «Viejo» de los puntos que toco existen tal cual en `.tex8`**, en las líneas citadas y también en `df2f893`. Son 4.2, M1.1 a M1.6, M2.7, M5.1, M5.2, M5.3 y M4.1, más 7.1, 7.3, 7.6, 7.8 y 9.3 de estructura (cotejo con espacios normalizados). Los bordes de 4.4 (06:78 y 06:120) y los puntos de inserción (06:336, que es el último renglón, y 05:31) también coinciden.
- **Ninguna cifra nueva queda sin fuente.** Las únicas derivadas son la distancia al oráculo (100 − la clase sobre el total) y los $p$ de M5.1 (pares divididos entre diez semillas idénticas); las dos vienen explicadas en su fuente.
