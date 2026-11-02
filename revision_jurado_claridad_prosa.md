# Propuesta viejo/nuevo: claridad, términos, notación y lengua (dictamen de estilo)

**Estado:** pendiente de aprobación. No se ha aplicado nada a la tesis, y no hay commit, push ni ramas nuevas.

**Base:** rama `una-hetero`, commit `df2f893`. El `.tex8` no cambió desde `62995a8`, así que las líneas del dictamen siguen valiendo. `03:372` es `.tex8/secciones/03_arquitectura.tex`, línea 372, y `main:88` es `.tex8/main.tex`, línea 88.

**Alcance:** C1–C12, 5.1–5.5 y 5.7 de `revision_jurado/jurado_estilo.md`. Quedan fuera E1–E9, 5.6 y los dictámenes de metodología y de Wegner, que van en la propuesta de estructura. Cuando una de mis frases cae en un pasaje que esa propuesta va a reescribir, lo digo en la Parte 4.

**Cómo leer:**
- Cada texto «Nuevo» ya trae aplicadas las decisiones de la Parte 1 y las reglas de la Parte 3 (`\,\%`, comillas angulares, nombres completos).
- Los conteos de la Parte 3 incluyen las apariciones que ya resuelve algún punto de la Parte 2.
- Un script cotejó los 181 fragmentos «Viejo» de las Partes 2 y 3 contra el `.tex`. Todos aparecen una sola vez, leyendo cada salto de línea como un espacio.

**Consolidación (2 nov 2026)** (detalle en `revision_jurado_INDICE.md`):
- El cotejo local encontró 183 fragmentos «Viejo» en las Partes 2 y 3 (las tablas cuentan cada celda): los 183 están en el `.tex8` actual, en las líneas citadas. De las 31 sustituciones «X» → «Y» del resto del texto, una no coincidía: «Los 3 vecinos» está en minúscula en 03:487; ya está corregida.
- Esta propuesta se aplica **después** de la de estructura y de la de metodología. Los puntos o filas que dicen **Consolidación: absorbido** ya están dentro de un texto combinado de esas propuestas y no se aplican aquí.
- Las reglas de la Parte 3 (`\,\%`, comillas, números en letra, «la hetero», anglicismos, dos puntos y sustituciones de 3.8) ya van aplicadas en los textos combinados. Sobre el resto del texto se aplican por búsqueda, no por número de línea, porque las otras dos propuestas mueven las líneas.
- S48 lleva ahora `[PENDIENTE: exp11 corregido]`: el 1.3 % de los destinos es del brazo del protocolo.

---

## Parte 1. Decisiones de términos y notación

### 1.1 Tabla de sustitución de términos (C1–C5, C10)

| Término actual | Decisión | Apariciones (archivo:línea) |
|---|---|---|
| «fidelidad» (del recuerdo: distancia a la instancia real) | **Se queda.** Pasa a ser el único sentido de «fidelidad». | main:98, 05:532, 06:183, 07:55 |
| «auditoría de fidelidad» | «auditoría de trazabilidad» | 01:98, 04:5–6, 04:215, 04:218 |
| «fidelidad temprana-madura», «fidelidad de la fase madura», «Fidelidad» (columna), símbolo $F$ | «concordancia temprana-madura» (abreviada «concordancia»), símbolo $\rho$ | 03:499, 03:501, 03:505–506, 03:508, 04:247, 05:44, 05:158, 07:15 |
| «fidelidad del procesamiento» | Sale (Parte 4, punto 1). | 07:81 |
| «precisión» / «exactitud» | **«precisión»** = fracción de aciertos (*accuracy*), definida una vez en 4.6 (S5). «Exactitud» sale. 02:134 deja de usar «precisión» en el sentido de *precision* (S4). | 02:134–135, 04:236, 06:189 |
| «lectura B1» fuera de la calibración | «lectura normalizada por conteo» (abreviada «lectura normalizada»). «B1» queda como etiqueta de la condición. | lista en 1.2 |
| «fase A» | «formación del directorio visual» (abreviada «formación visual») | 03:429, 04:42, 04:163, 05:334, 05:363, 05:440, 05:661, 06:13, 06:266 |
| «fase B» | «evaluación visual» | 04:47, 05:346, 05:661 |
| «fase de activación temprana», «fase de recuperación madura» | «fase temprana», «fase madura» | 04:239, 04:240 |
| «dos fases» del hemisferio visual | «dos etapas», para que «fase» quede solo para la temprana y la madura | 05:330 |
| «condiciones de lectura» (son nueve y solo tres cambian la lectura) | «condiciones de calibración» | 01:107, 04:266, 05:33 |
| «rescate de atención léxica» | «rescate léxico», como en 03:217 y 06:106 | 04:94, 06:316 |
| «llenado por instancias», «llenado imagen por imagen» | «llenado imagen-etiqueta», como en 03:187 y 03:384 | 05:241, 05:276–277 |
| «*sample-and-search*», `recall_with_sampling_n_search` | «*search and test*», el nombre del artículo; el identificador pasa a nota (S29) | 02:171–172, 02:259–260 |
| «índice» (por el directorio) | «directorio» | 06:195, 06:223 |
| «Enrutamiento» en la tabla de capacidad, que en realidad es la precisión temprana | «Precisión temprana» | 05:290, 05:299, 05:319 |
| «Enrutamiento de prueba» | «Enrutamiento visual» | 04:251 |
| «umbrales $\iota$ y $\kappa$» | «la poda $\iota$ y el umbral $\kappa$» ($\iota$ siempre es poda) | 02:158 |
| «enrutamientos falsos», «enrutamientos equivocados» (los dos de imagen) | «falsos enrutamientos», como en las otras siete apariciones | main:96, 05:364, 06:241 |
| «maquinaria (transactiva)» | «mecanismo transactivo» | 06:5, 06:8, 06:10, 06:176, 07:110 |
| «mecanismos de Wegner» | «procesos de Wegner», como en 01:15 y 02:281 | main:74, 06:82 (Parte 4, punto 4) |

**Consolidación:** en main:74, main:88-90, main:96, 01:78, 01:107-108, 05:440, 06:5-12, 06:82, 06:101, 06:189, 07:15, 07:37 y 07:110 estas sustituciones ya van dentro de los textos combinados de la propuesta de estructura o de la de metodología.

**Por qué «precisión» y no «exactitud».**
- Las figuras 4, 5 y 6 dicen «Precisión madura» en el eje (`fig02_mature_accuracy_vs_N.png`, `fig03_heatmap_condition_N.png` y `fig04_domain_accuracy_N400.png`). Con «exactitud» habría que regenerar las tres.
- «Precisión» solo choca con el sentido de *precision* en 02:134, y esa frase se reescribe (S4).
- En 06:189, «exactitud de clase» es la medida del juez 1-NN del experimento 11, que 05:522 ya llama «Acierto de clase».

**Por qué $\rho$ para la concordancia.** La condición F de la calibración aparece en las leyendas de las figuras 5 y 6 (`fig03` y `fig04`), y renombrarla obligaría a regenerarlas. $\rho$, $x$ y $\omega$ no se usan en la tesis.

### 1.2 La lectura normalizada por conteo (C3)

El nombre se define una vez, en 03:390–397 (S7), como «lectura normalizada por conteo (B1, por su nombre en el estudio de calibración)».

**Pasan a «lectura normalizada» (20 lugares):** main:88, main:90, 01:78, 03:98, 03:294 (nodo de la Figura 3), 03:327, 03:390, 03:395, 03:418, 03:425, 03:435, 04:240, 05:158, 05:250, 05:348, 06:10, 06:101, 07:15, 07:19 y 07:37.
- Los cambios que piden algo más que la sustitución están en S6–S8.
- En los demás, «la lectura B1» → «la lectura normalizada».
- En 03:425, «la suma de B1» → «la suma de la lectura normalizada».

**«B1» se queda** donde se compara con A, B2, C, D, E32, E64, F o G:
- la calibración (05:15–140, tabla y figuras);
- el barrido $\iota\times\kappa$ (05:187, 05:219, 05:235–237);
- las secciones 6.2–6.3 (06:40–69).

### 1.3 Notación (C8)

| Símbolo | Choque | Decisión mínima | Dónde |
|---|---|---|---|
| $q$ | (a) tamaño del alfabeto derecho; (b) subíndice de $\mathbf{v}_q$ y $\mathbf{z}_q$; (c) variable de consulta en la ecuación de la fidelidad | (a) se queda: es la notación de Morales y Pineda y la del código (`self.q`). (b) se queda, pero se declara que el subíndice marca la pista cuantizada (en el llenado no hay consulta: 03:175 y 03:189); ninguna fórmula junta (a) con (b). (c) pasa a $x$. | (b) se declara en 03:91–98 (S20); (c) va en S9 |
| $w$ como cota frente a $w_i$; $l$ como cota frente al índice $l$ | Ninguna ecuación usa las cotas, así que **se quitan los símbolos de cota** y queda «acotada superiormente». No se introduce $w_{\max}$, que ya se había descartado. $l$ queda solo como índice de valor. | 02:40–43, 02:150–151 (S16, S17) |
| $N$ | consultas de formación frente a imágenes por clase | $N$ = consultas (calibración y concordancia); **$I$ = imágenes por clase** en la sección de capacidad. La comparación con la EHAM única ya dice «imágenes por clase» con palabras. | 10 apariciones: 05:276, 05:285, 05:291, 05:299, 05:313 (dos veces), 05:317, 05:320, 05:321, 05:323. $N_{\mathrm{consultas}}$ de 03:505 pasa a $N$. |
| $F$ | ecuación de la fidelidad frente a la condición F | La condición se queda (está en las figuras); la ecuación pasa a $\rho$. | 03:505 (S9) |
| $\eta$ | reconocimiento (indicador 0/1, 02:59) frente a función que devuelve pesos (03:350 y 03:477) | $\eta$ queda solo para el reconocimiento. Los pesos se escriben con la función **$\omega(\mathbf{a}, \mathbf{R}) = (w_1,\ldots,w_n)$**, definida en la ecuación de los pesos. | 02:66–70, 03:350, 03:477 (S18) |
| Superíndices $L$/$R$ | En $M^L$ y $M^R$ significan «izquierda» y «derecha» de $M^H$. En $M^L_{\mathrm{dir}}$ y $M^R_{\mathrm{dir}}$ significan «texto» e «imagen», aunque en los directorios la pista va siempre a la izquierda. | **$M^{\mathrm{txt}}_{\mathrm{dir}}$ y $M^{\mathrm{vis}}_{\mathrm{dir}}$.** $M^L$, $M^R$ y $\mathbf{w}_R$ (03:477) se quedan. | 18 apariciones en 15 líneas: 03:49, 50, 53, 54, 66, 67, 70, 73, 74, 84, 294, 328, 393, 435 y 05:348 |
| fila / columna | 02:47 llama «columna» a $\mathbf{R}[i,\cdot]$, la de cada característica, como las fuentes; 03:372 dice «fila» para lo mismo. | «columna» | 03:372 (S19) |
| Normalización de los pesos | 02:227 normaliza por la suma (media unitaria); 03:353, por el máximo. | **Ocurren las dos, y la efectiva es la de 02:227.** El código del sistema divide entre el máximo (`src/stage6_interaction.py:178–183` y `src/hetero_memory.py:200–210`, «esto solo evita NaN y desbordes»). Después, `project()` multiplica por $n$ y divide entre la suma (`src/hetero_lib/hetero_associative_4d.py:448–452`), así que la división entre el máximo no cambia nada. 03:353 lo dice así (S19). | 03:353–354 |

**Revisado y sin cambio:**
- $L$ como longitud de la secuencia expandida (03:189–190) y $L_1$ (tabla de capacidad): ninguna fórmula los junta con $M^L$.
- $k$ como índice de valor (02:194–199) frente a $k$ como módulo (03): están en secciones distintas.
- $b{=}1$ (03:393) frente a $\mathbf{b}$ (02:180): el dictamen no los marca.

### 1.4 Siglas (C12)

| Sigla | Decisión | Dónde |
|---|---|---|
| EAM-TMS en el resumen | Se expande, como en 01:40–42. | main:63 (S43) |
| PCA | «análisis de componentes principales (PCA, por sus siglas en inglés)» | 06:31 (S44) |
| POS | «categoría gramatical (POS, por *part of speech*)», la primera vez | 06:317, 06:322 (S45) |

---

## Parte 2. Puntos viejo/nuevo

### C1–C4. Términos de métricas y fases

#### S1. Título de la contribución 4 (01:98)
- **Consolidación:** no se aplica: la contribución 4 sale (estructura 9.2, en `revision_jurado_estructura_prosa.md`).
- **Viejo:** «\item \textbf{Auditoría de fidelidad.}»
- **Nuevo:** «\item \textbf{Auditoría de trazabilidad.}»
- **Por qué:** C1. Si la propuesta de estructura saca la auditoría de las contribuciones (E7), el cambio pasa a 04:215.

#### S2. Apertura de la metodología (04:4–6)
- **Viejo:** «Este capítulo describe el conjunto de datos y su partición, la representación de texto y de imagen, el banco de consultas, los parámetros de las memorias, la auditoría de fidelidad, las métricas y la organización de los experimentos.»
- **Nuevo:** «Esta sección describe el conjunto de datos y su partición, la representación de texto y de imagen, el banco de consultas, los parámetros de las memorias, la auditoría de trazabilidad, las métricas y la organización de los experimentos.»
- **Por qué:** C1 y 5.3. El documento es `article` y no tiene capítulos.

#### S3. Auditoría (04:215 y 04:218)
- **Consolidación:** el título (04:215) se aplica aquí; la frase de 04:218 ya va con «trazabilidad» en estructura 7.4.
- **Viejo:** «\subsection{Auditoría de fidelidad}» / «La auditoría de fidelidad comprueba que las decisiones del sistema salen de operaciones»
- **Nuevo:** «\subsection{Auditoría de trazabilidad}» / «La auditoría de trazabilidad comprueba que las decisiones del sistema salen de operaciones»
- **Por qué:** C1. El resto del párrafo («datos fabricados», «vectores sintéticos») va en la Parte 4, punto 2.

#### S4. «Precisión» en el sentido de *precision* (02:133–136)
- **Viejo:** «La evidencia empírica de las fuentes ubica el óptimo de reconocimiento y recuperación constructiva en un rango \emph{intermedio} de entropía: baja entropía da precisión alta con exhaustividad (\textit{recall}) baja, alta entropía lo contrario \cite{pineda2023imagery}.»
- **Nuevo:** «La evidencia empírica de las fuentes ubica el óptimo de reconocimiento y recuperación constructiva en un rango \emph{intermedio} de entropía. Con entropía baja, el reconocimiento comete pocas aceptaciones falsas y muchas omisiones; con entropía alta ocurre lo contrario \cite{pineda2023imagery}.»
- **Por qué:** C2. «Precisión alta con exhaustividad baja» quiere decir pocas aceptaciones falsas y muchas omisiones. Con el cambio, «precisión» tiene un solo sentido en toda la tesis, y desaparece la glosa *recall* (5.2).

#### S5. Definición de «precisión» y nombre de las fases en las métricas (04:236–240)
- **Viejo:** «Se emplearon las siguientes métricas:» … «\item \textbf{Precisión temprana} (\textit{early accuracy}): fracción de consultas para las que el módulo ganador en la fase de activación temprana coincide con la clase real.» / «\item \textbf{Precisión madura} (\textit{mature accuracy}): ídem tras la fase de recuperación madura, con la lectura B1 o la cruda del directorio.»
- **Nuevo:** «Se emplearon las siguientes métricas. En este trabajo, \emph{precisión} es siempre la fracción de aciertos sobre las consultas o imágenes evaluadas o, cuando se indica, sobre las aceptadas.» … «\item \textbf{Precisión temprana}: fracción de consultas en las que el módulo ganador de la fase temprana coincide con la clase real.» / «\item \textbf{Precisión madura}: la misma fracción en la fase madura, con la lectura normalizada o con la cruda del directorio.»
- **Por qué:** C2, C3, C4, 5.2 (glosas) y 5.4 («ídem»). La definición también cubre la precisión sobre las aceptadas (04:252–253, 05:352 y 07:22).

#### S6. Lectura normalizada en el resumen (main:85–91)
- **Consolidación:** absorbido en estructura 9.1 (resumen completo), que trae este texto.
- **Viejo:** «el 90.0\% de las consultas llega al módulo correcto en la fase temprana y el 93.0\% en la fase madura con la lectura del directorio normalizada por número de registros (B1); la cifra madura se mide sobre las mismas consultas que formaron el directorio. La lectura B1 reduce la participación del módulo \texttt{apple} del 20.5\% de la lectura cruda al 13.8\% (ideal 12.5\%).»
- **Nuevo:** «el 90.0\,\% de las consultas llega al módulo correcto en la fase temprana y el 93.0\,\% en la fase madura, con la lectura del directorio normalizada por conteo, que divide la puntuación de cada módulo entre su número de registros; la cifra madura se mide sobre las mismas consultas que formaron el directorio. La lectura normalizada reduce la participación del módulo \texttt{apple} del 20.5\,\% de la lectura cruda al 13.8\,\% (ideal 12.5\,\%).»
- **Por qué:** C3. El resumen no debe usar una etiqueta de la calibración que el lector aún no conoce. El resumen también lo toca la propuesta de estructura (E1 y E7), que debe conservar este nombre.

#### S7. Definición de la lectura normalizada (03:390–397)
- **Viejo:** «\subsubsection*{Lectura B1 del directorio}» … «Sea $\Pi^{\mathrm{dir}}_k(\mathbf{v}_q)$ la proyección de la pista $\mathbf{v}_q$ en el directorio $M^L_{\mathrm{dir}}$ del módulo, restringida al bit $b=1$ (``el módulo $k$ conoce''). La puntuación B1 se define como:»
- **Nuevo:** «\subsubsection*{Lectura normalizada por conteo}» … «Sea $\Pi^{\mathrm{dir}}_k(\mathbf{v}_q)$ la proyección de la pista $\mathbf{v}_q$ en el directorio $M^{\mathrm{txt}}_{\mathrm{dir}}$ del módulo, restringida al bit $b=1$ («el módulo $k$ conoce»). La \textbf{lectura normalizada por conteo} (B1, por su nombre en el estudio de calibración de la Sección~\ref{sec:calibracion}) da al módulo $k$ la puntuación:»
- **Por qué:** C3, como propone el dictamen. 01:78 y 03:98 remiten aquí.

#### S8. Lectura normalizada en la introducción y en la notación (01:78–79 y 03:96–98)
- **Consolidación:** 01:78-79 va absorbido en estructura 9.2; 03:96-98 se aplica aquí.
- **Viejo:** «Los directorios, su lectura normalizada por número de registros (B1, Sección~\ref{sec:operaciones}), el rechazo» / «y $\hat{s}_k$, la que un directorio da al módulo $k$ con la lectura B1 (Sección~\ref{sec:operaciones}).»
- **Nuevo:** «Los directorios, su lectura normalizada por conteo de registros (Sección~\ref{sec:operaciones}), el rechazo» / «y $\hat{s}_k$, la que un directorio da al módulo $k$ con la lectura normalizada por conteo (Sección~\ref{sec:operaciones}).»
- **Por qué:** C3. 03:96 también cambia en S20.

#### S9. Concordancia temprana-madura (03:499–508)
- **Viejo:** «\subsubsection*{Fidelidad de la fase madura}» «La \textbf{fidelidad} se define como la fracción de consultas en la fase madura en las que la coordinación de la recuperación, desde el módulo de entrada, llega al mismo módulo ganador que la fase temprana: \begin{equation} F = \frac{|\{q : g^{\mathrm{maduro}}(q) = g^{\mathrm{temprano}}(q)\}|}{N_{\mathrm{consultas}}} \label{eq:fidelidad} \end{equation} La fidelidad mide coincidencia con lo aprendido en la fase temprana, no acierto absoluto.»
- **Nuevo:** «\subsubsection*{Concordancia temprana-madura}» «La \textbf{concordancia temprana-madura} es la fracción de consultas en las que la coordinación de la recuperación, desde el módulo de entrada, llega en la fase madura al mismo módulo ganador que en la fase temprana: \begin{equation} \rho = \frac{|\{x : g^{\mathrm{maduro}}(x) = g^{\mathrm{temprano}}(x)\}|}{N} \label{eq:concordancia} \end{equation} donde $x$ recorre las $N$ consultas evaluadas. La concordancia mide coincidencia con lo aprendido en la fase temprana, no acierto.»
- **Por qué:**
  - C1: la métrica tiene nombre propio.
  - C8: $q$ deja de ser variable, $F$ deja de chocar con la condición F y $N$ queda solo para consultas.
  - La etiqueta `eq:fidelidad` no se cita en ninguna parte, así que cambiarla es seguro.

#### S10. Concordancia en las métricas (04:247)
- **Consolidación:** 07:15 va absorbido en el punto M2.9 de `revision_jurado_metodologia_prosa.md`; 04:247, 05:44 y 05:158 se aplican aquí.
- **Viejo:** «\item \textbf{Fidelidad temprana-madura}: concordancia entre la clase ganadora en fase temprana y la clase ganadora en fase madura.»
- **Nuevo:** «\item \textbf{Concordancia temprana-madura} (ecuación~\eqref{eq:concordancia}): fracción de consultas cuyo ganador en la fase madura es el mismo que en la fase temprana.»
- **Por qué:** C1. En la columna de la Tabla 2 (05:44, «Fidelidad (\%)» → «Concordancia (\%)»), en 05:158 y en 07:15 solo cambia la palabra.

#### S11. Partición del conjunto de datos (04:34–49)
- **Viejo:** «\item \textbf{Llenado} (\textit{filling}): imágenes \texttt{train[0:200]} de cada clase, con las que se llena la memoria de contenido del módulo especialista.» … «\item \textbf{Interacciones visuales} (\emph{fase A}): imágenes \texttt{train[200:328]} de cada clase (1024 en total, 128 por clase), con las que se forma el directorio visual.» … «\item \textbf{Evaluación} (\emph{fase B}): las 82 imágenes de prueba (\texttt{test}) de cada clase (656 en total), nunca vistas durante el llenado ni la formación del directorio.»
- **Nuevo:** «\item \textbf{Llenado}: las 200 primeras imágenes de entrenamiento de cada clase, con las que se llena la memoria de contenido del módulo especialista.» … «\item \textbf{Formación del directorio visual} (en adelante, \emph{formación visual}): las 128 imágenes de entrenamiento restantes de cada clase (1024 en total), con las que se forma el directorio visual.» … «\item \textbf{Evaluación visual}: las 82 imágenes de prueba de cada clase (656 en total), nunca vistas durante el llenado ni la formación del directorio.»
- **Por qué:** C4, C12 (identificadores de código) y 5.2 (glosa *filling*). `train[0:200]` son las 200 primeras imágenes de entrenamiento y `train[200:328]` las 128 restantes (328 = 200 + 128).

#### S12. Las dos etapas del hemisferio visual (05:330–334 y 05:346)
- **Consolidación:** la frase de 05:440 va absorbida en el punto M4.1 de `revision_jurado_metodologia_prosa.md`; lo demás se aplica aquí.
- **Viejo:** «El hemisferio visual opera en dos fases: formación (registro de percepciones reales de \texttt{train[200:328]} en los directorios visuales) y evaluación (enrutamiento de las 656 imágenes de prueba mediante el directorio visual por módulo).» / «\paragraph{Fase A: formación con 1024 imágenes.}» / «\paragraph{Fase B: enrutamiento de imágenes de prueba.}»
- **Nuevo:** «El hemisferio visual opera en dos etapas: la formación del directorio visual, que registra percepciones reales de las 128 imágenes de entrenamiento restantes de cada clase, y la evaluación visual, que enruta las 656 imágenes de prueba con el directorio visual de cada módulo.» / «\paragraph{Formación del directorio visual con 1024 imágenes.}» / «\paragraph{Evaluación visual con las 656 imágenes de prueba.}»
- **Por qué:** C4. Con «etapas», «fase» queda solo para la temprana y la madura. Las demás apariciones de «fase A» y «fase B» solo cambian de nombre (1.1 y 3.8), con dos casos que cambian un poco más:
  - en 05:440, «el contenido y la fase A se construyen» → «el contenido y el directorio visual se construyen»;
  - en 05:661, «(fase A con 1024 imágenes, fase B con 656, evocación)» → «(formación con 1024 imágenes, evaluación con 656, evocación)».

### C5–C7. Calibración

#### S13. Nombre de las condiciones y pie de la Figura 4 (05:33 y 05:75–76)
- **Consolidación:** el pie de la Figura 4 (05:75-76) va absorbido en M2.3 de `revision_jurado_metodologia_prosa.md`; 05:33 se aplica aquí; 01:107 va en estructura 9.2 y 04:266 en M2.8 de `revision_jurado_metodologia_prosa.md`.
- **Viejo:** «\caption{Precisión bajo distintas condiciones de lectura del directorio» / «Entre las condiciones que solo cambian la lectura, B1 es la mejor en todo el rango y la cruda (A) queda por debajo.»
- **Nuevo:** «\caption{Precisión bajo las condiciones de calibración» / «Entre las condiciones que no alteran las consultas, B1 es la mejor en todo el rango y la cruda (A) queda por debajo.»
- **Por qué:**
  - C5: C, D, E32, E64, F y G no son lecturas.
  - En `ablation_metrics.csv`, B1 supera a A, B2, C, E32, E64 y F con los cuatro valores de $N$:
    - B1: 78.0, 87.0, 88.0 y 93.0.
    - B2: 76.0, 82.0, 82.0 y 91.75.
    - C: 74.0, 77.0, 74.5 y 88.0.
    - E64: 68.0, 71.0, 73.5 y 89.75.
  - Solo D y G, que alteran las consultas, lo superan en algún punto.
- **Sustitución simple en otros dos lugares:**
  - 01:107: «nueve condiciones de lectura del directorio» → «nueve condiciones de calibración del directorio».
  - 04:266: «9 condiciones de lectura» → «9 condiciones de calibración». La cifra se queda porque es factor de un producto con $\times$.

#### S14. B2 no es un síntoma (05:62–63 y 06:55–57)
- **Consolidación:** los dos fragmentos van absorbidos en `revision_jurado_metodologia_prosa.md`: 05:62-63 en M2.4 y 06:55-57 en M2.5.
- **Viejo:** «Ninguna de las condiciones que actúan sobre los síntomas del sesgo y no sobre su causa (B2, C, D, E32, E64) alcanza a B1; la más cercana, B2, queda a 1.2 puntos.» / «Las condiciones que actúan sobre los síntomas (B2, C, D, E) quedan por debajo de B1, y la combinación G, que suma correcciones a B1, gana solo medio punto, dentro del ruido (Tabla~\ref{tab:calibracion}).»
- **Nuevo:** «Ninguna de las demás condiciones (B2, C, D, E32, E64) alcanza a B1; la más cercana, B2, queda a 1.2 puntos.» / «Con $N = 400$, las demás condiciones (B2, C, D, E32, E64) quedan por debajo de B1, y la combinación G, que suma correcciones a B1, gana solo medio punto, menos de lo que varía entre semillas (Tabla~\ref{tab:calibracion}).»
- **Por qué:**
  - C6: B2 divide entre la raíz del conteo, así que actúa sobre la misma causa que B1.
  - C7: con $N = 50$ y con $N = 200$, D supera a B1.
  - Cifras comprobadas en el CSV (media de cinco semillas, $N = 400$):
    - B1 da 93.0 y B2 91.75. La diferencia es 1.25, que se redondea a 1.2 igual que 85.25 → 85.2.
    - G varía entre 93.0 y 93.7.
  - «Menos de lo que varía entre semillas» repite lo que ya dice 05:64–65.

#### S15. Título del párrafo de B1 (05:59)
- **Consolidación:** absorbido en M2.4 de `revision_jurado_metodologia_prosa.md`, con el mismo título.
- **Viejo:** «\paragraph{B1 es la corrección que no se puede sustituir.}»
- **Nuevo:** «\paragraph{Con $N = 400$, B1 es la mejor corrección individual.}»
- **Por qué:** C7. En el CSV:
  - D supera a B1 con $N = 50$ (90.0 frente a 78.0) y con $N = 200$ (89.2 frente a 88.0).
  - D queda por debajo con $N = 100$ (86.5 frente a 87.0) y con $N = 400$ (87.3 frente a 93.0).
  - G supera a B1 en todo el rango, pero es una combinación.

### C8. Notación

#### S16. Cota de los pesos en la EAM (02:40–43)
- **Viejo:** «La acumulación está acotada superiormente (pesos en $\{0,\ldots,w\}$), tal como define la fuente heteroasociativa \cite{morales2025missing}, cuyos autores describen esta operación como una forma de la regla de aprendizaje de Hebb; la W-EAM original fija los pesos en $\{0,\ldots,l\}$ \cite{pineda2022weighted}.»
- **Nuevo:** «La acumulación está acotada superiormente, tal como definen la W-EAM original \cite{pineda2022weighted} y la fuente heteroasociativa \cite{morales2025missing}, cuyos autores describen esta operación como una forma de la regla de aprendizaje de Hebb.»
- **Por qué:** C8. Ya no quedan $w$ como cota junto a $w_i$, ni $l$ como cota junto al índice $l$ de las ecuaciones (6), (8) y (10). Ninguna ecuación usa el valor de la cota.

#### S17. Cota en la EHAM (02:150–151)
- **Viejo:** «En el artículo la relación es $h \subseteq A \times B \times V \times Z$ con pesos en $\{0,\ldots,w\}$; la implementación de referencia la almacena en un tensor»
- **Nuevo:** «En el artículo la relación es $h \subseteq A \times B \times V \times Z$, con pesos acotados; la implementación de referencia la almacena en un tensor»
- **Por qué:** C8, por lo mismo que S16.

#### S18. Función de pesos $\omega$ (02:66–70, 03:350 y 03:477)
- **Viejo:** «Durante el reconocimiento se computan además los \textbf{pesos por dimensión}: \begin{equation} w_i = \mathbf{R}[i,\, a_i] \label{eq:pesos} \end{equation}» / «\mathbf{w} = \eta(\mathbf{v}_q,\; M^L)» / «$\mathbf{w}_R = \eta(\mathbf{z}_q,\; M^R)$»
- **Nuevo:** «Durante el reconocimiento se computan además los \textbf{pesos por dimensión}, que este trabajo escribe como la función $\omega$: \begin{equation} \omega(\mathbf{a}, \mathbf{R}) = (w_1, \ldots, w_n), \qquad w_i = \mathbf{R}[i,\, a_i] \label{eq:pesos} \end{equation}» / «\mathbf{w} = \omega(\mathbf{v}_q,\; M^L)» / «$\mathbf{w}_R = \omega(\mathbf{z}_q,\; M^R)$»
- **Por qué:** C8. En 02:59, $\eta$ devuelve 0 o 1, como dice 02:73–74; en 03 devolvía pesos. Con $\omega$, $\eta$ conserva un solo sentido.

#### S19. Fila o columna y normalización de los pesos (03:353–354 y 03:372–373)
- **Viejo:** «y se normalizan $w_i \leftarrow w_i / \max_j w_j$ (la proyección es invariante a esa escala; ecuación~\eqref{eq:normalizacion-pesos}).» / «La compuerta anula la puntuación si alguna fila del dominio derecho carece de soporte: el módulo no opina sobre lo que no contiene.»
- **Nuevo:** «y la proyección los normaliza a media unitaria (ecuación~\eqref{eq:normalizacion-pesos}); la división previa entre el máximo, que hace el código del sistema para evitar desbordes, no cambia el resultado.» / «La compuerta anula la puntuación si alguna columna del dominio derecho (una característica $j$) carece de soporte, de modo que el módulo no opina sobre lo que no contiene.»
- **Por qué:**
  - C8, comprobado en `src/`:
    - `src/stage6_interaction.py:178–183` divide entre el máximo.
    - `project()` (`src/hetero_lib/hetero_associative_4d.py:452`) calcula `w = cue.size*weights/sum_weights`, que es la ecuación (9), `eq:normalizacion-pesos`.
    - El docstring de `src/hetero_memory.py:201` dice que la división entre el máximo «solo evita NaN y desbordes».
  - En la ecuación (13), `eq:score-gated`, la suma $\sum_l \Pi_k[j,l]$ recorre los valores de la característica $j$, que 02:47 llama «columna».

#### S20. Párrafo de notación (03:91–98)
- **Viejo:** «Una consulta de texto produce una pista por token, $\mathbf{v}_q \in \{0,\ldots,15\}^{300}$: el vector fastText del token, cuantizado por magnitud. Una imagen produce una pista, $\mathbf{z}_q \in \{0,\ldots,31\}^{64}$: su latente cuantizado. $g$ es el módulo ganador de una transacción;»
- **Nuevo:** «Una consulta de texto produce una pista por token, $\mathbf{v}_q \in \{0,\ldots,15\}^{300}$, que es el vector fastText del token cuantizado por magnitud. Una imagen produce una pista, $\mathbf{z}_q \in \{0,\ldots,31\}^{64}$, que es su latente cuantizado. El subíndice $q$ indica que la pista está cuantizada, también en el llenado, y no es el tamaño de alfabeto $q$ de la Sección~\ref{sec:hetero4d}. El módulo ganador de una transacción es $g$;»
- **Por qué:** C8 ($q$), 5.4 (la oración empezaba con el símbolo $g$) y 5.7 (dos puntos).

#### S21. Imágenes por clase: $I$ (05:276–323)
- **Viejo:** «$N \in \{25, 50, 100, 200, 328\}$, con el llenado imagen por imagen (\textit{imagen--etiqueta}).»
- **Nuevo:** «$I \in \{25, 50, 100, 200, 328\}$, con el llenado imagen-etiqueta.»
- **Por qué:** C8 y C10 (llenado). Las otras nueve apariciones de $N$ en la sección también pasan a $I$: 05:285, 05:291, 05:299, 05:313 (dos veces), 05:317, 05:320, 05:321 y 05:323. Las de 05:313 y 05:323 van completas en S36 y S38.

### C9. Términos usados antes de definirlos

#### S22. «Los módulos que conoce» (01:95 y 03:84–85)
- **Consolidación:** 01:95 va absorbido en estructura 9.2 y 03:84-85 en estructura 2.3.
- **Viejo:** «directorio y los de los módulos que conoce y la redirige punto a punto al» / «que consulta su $M^R_{\mathrm{dir}}$ y los de los módulos que conoce y la reenvía al especialista»
- **Nuevo:** «directorio y los de los módulos que ha visto ganar alguna transacción y la redirige punto a punto al» / «que consulta su $M^{\mathrm{vis}}_{\mathrm{dir}}$ y los de los módulos que conoce (los que vio ganar alguna transacción) y la reenvía al especialista»
- **Por qué:** C9. La definición estaba en 03:419, tres páginas después. Coincide con el código: `known_by` (`src/stage6_interaction.py:301–305`) toma los módulos con conteo positivo en el directorio del dueño.

#### S23. Pie de la Figura 3 cuando falta soporte (03:329–331)
- **Viejo:** «si nadie en ese círculo tiene soporte, la consulta pasa a los conocidos.»
- **Nuevo:** «si nadie en ese círculo tiene soporte, la consulta pasa al conocido con más registros.»
- **Por qué:** C9 y C10. El pie dice «a los conocidos» y 03:421, «al conocido con más registros». El código hace lo segundo (`src/stage6_interaction.py:301–322`): `known_by` ordena por conteo descendente y la cola empieza por el primero.

#### S24. «Lecturas de dominio» antes de su definición (02:89–92)
- **Viejo:** «De las lecturas de dominio de la memoria de contenido (ecuación~\eqref{eq:marginal}), este sistema usa los pesos y no esa decisión; el $\kappa$ que barre la Sección~\ref{sec:param-iota-kappa} actúa sobre la proyección heteroasociativa (Sección~\ref{sec:hetero4d}).»
- **Nuevo:** «Este sistema usa de esta memoria los pesos, pero no esa decisión (Sección~\ref{sec:hetero4d}); el $\kappa$ que barre la Sección~\ref{sec:param-iota-kappa} actúa sobre la proyección heteroasociativa.»
- **Por qué:** C9. La ecuación de las lecturas está en 02:196, cien líneas después. Basta con remitir a 2.2.

#### S25. «Etiquetas fuertes» (04:72–74)
- **Viejo:** «y los empates se ordenan por similitud coseno al centroide de las etiquetas fuertes de la clase.»
- **Nuevo:** «y los empates se ordenan por similitud coseno al centroide de las etiquetas de la clase con masa asociativa de al menos 2.»
- **Por qué:** C9. Es lo que dice `src/stage3_conceptnet.py:439–446`: «labels fuertes de la clase (masa >= 2)».

#### S26. «Puente» (03:87–89)
- **Viejo:** «Un puente desde la memoria de contenido del módulo de entrada hacia su directorio de texto no serviría: cuando el módulo de entrada no es el especialista, su memoria de contenido no contiene el latente ajeno y el puente no redirige.»
- **Nuevo:** «Traducir la imagen a palabras con la memoria de contenido del módulo de entrada, para enrutarlas con su directorio de texto, no serviría, porque cuando el módulo de entrada no es el especialista, su memoria de contenido no contiene el latente ajeno y no produce palabras que enrutar.»
- **Por qué:** C9: «puente» no estaba definido. También quita unos dos puntos (5.7).

#### S27. «Sesgo de masa» y «contención inversa» (05:233 y 05:278–279)
- **Viejo:** «$\kappa$ no es una defensa contra el sesgo de masa.» / «(contención inversa, con $\xi = 0$)»
- **Nuevo:** «El umbral $\kappa$ tampoco corrige el sesgo hacia los módulos con más registros en el directorio.» / «(con $\xi = 0$)»
- **Por qué:** C9. El sesgo es el que corrige B1 (03:402–409). «Contención inversa» sobra, porque la misma frase ya dice «desde el lado de la imagen». También se evita una oración que empieza con un símbolo (5.4).

#### S28. «Envolvente por coordenada» (05:386–388): va en S41
La definición entra en su primera aparición, dentro del párrafo largo de S41: «es decir, que en cada coordenada toman un valor que esas memorias ya tienen registrado». Es la contención con $\xi = 0$ de 02:55–56. Esa definición cubre las apariciones de 05:449, 06:250 y 06:295.

### C10. Un mismo objeto con varios nombres

#### S29. El método de recuperación (02:169–172 y 02:257–260)
- **Viejo:** «para elegir un objeto del plano, este sistema usa el tercer método, que es la recuperación por defecto de la implementación de referencia (\texttt{recall\_with\_sampling\_n\_search}).» / «y la mejora con una búsqueda local en su vecindad (\emph{sample-and-search}, el tercer método de la pista faltante, que el resumen del artículo llama \emph{search and test}).»
- **Nuevo:** «para elegir un objeto del plano, este sistema usa el tercer método, \emph{search and test}, que es la recuperación por defecto de la implementación de referencia\footnote{Función \texttt{recall\_with\_sampling\_n\_search}.}.» / «y la mejora con una búsqueda local en su vecindad; es el método \emph{search and test} de la pista faltante.»
- **Por qué:** C10 y C12. Había tres nombres para un solo método. Se queda el del artículo y el identificador pasa a nota.

#### S30. $\iota$ es poda, también al reconocer (02:156–158 y 05:183–186)
- **Viejo:** «el reconocimiento es la misma implicación material relajada con umbrales $\iota$ y $\kappa$, y la entropía» / «son la poda $\iota$, que apaga durante la recuperación las celdas de peso menor que $\iota$ veces el peso medio de las celdas no nulas, y el umbral relativo $\kappa$, que exige a la activación media por celda de la proyección llegar a $\kappa$ veces la media de la memoria.»
- **Nuevo:** «el reconocimiento es la misma implicación material relajada, con la poda $\iota$ y el umbral $\kappa$, y la entropía» / «son la poda $\iota$, que apaga al reconocer y al recuperar las celdas de peso menor que $\iota$ veces el peso medio de las celdas no nulas, y el umbral relativo $\kappa$, que exige que la activación media por celda de la proyección llegue a $\kappa$ veces la media de la memoria.»
- **Por qué:**
  - C10: $\iota$ se llamaba «umbral» en 02 y «poda» en 05.
  - 02:81 dice «al reconocer y al recuperar», y el código lo confirma: `containment()` y `project()` usan `_full_iota_relation` (`src/hetero_lib/hetero_associative_4d.py:444` y `:457`).
  - 5.3: «exige a… llegar».

#### S31. «Índice» por «directorio» (06:195 y 06:223)
- **Consolidación:** 06:195 va absorbido en M1.4 de `revision_jurado_metodologia_prosa.md`; 06:223 se aplica aquí.
- **Viejo:** «El precio es cobertura y un índice.» / «porque el índice calibrado compara mejor que la activación del contenido,»
- **Nuevo:** «La partición cuesta cobertura y requiere un directorio.» / «porque el directorio, con su lectura normalizada, compara mejor que la activación del contenido,»
- **Por qué:** C10 y C11 (06:195). El «índice calibrado» es el directorio con B1.

#### S32. «Enrutamiento» en la tabla de capacidad (05:290–293, 05:299 y 05:319)
- **Viejo:** «``Enrutamiento'' es la precisión temprana sobre 80 consultas (reconocimiento por el contenido llenado con $N$ imágenes, sin directorio); ``Variedad $L_1$'' es la distancia media $L_1$ entre recuperaciones de una misma pista; $H$ es la entropía de la memoria de contenido.}» / «Variedad $L_1$ & Enrutamiento (\%) & $H$ (bits)» / «\paragraph{Enrutamiento y entropía.}»
- **Nuevo:** ««Precisión temprana»: sobre 80 consultas, con el ganador elegido por el contenido llenado con $I$ imágenes, sin directorio. «Variedad $L_1$»: diferencia absoluta media por coordenada, en niveles de cuantización (de 32), entre 12 recuperaciones de una misma pista. $H$: entropía de la memoria de contenido.}» / «Variedad $L_1$ & Precisión temprana (\%) & $H$ (bits)» / «\paragraph{Precisión temprana, variedad y entropía.}»
- **Por qué:**
  - C10: la tabla llamaba «Enrutamiento» a la precisión temprana.
  - C12: «Variedad $L_1$» no tenía unidad. Comprobado en `run_experiment6.py:66` y `:250`: son 12 recuperaciones por pista, y la medida es `np.abs(arr[i] - arr[j]).mean()` sobre latentes cuantizados, promediada por pares.
  - El comentario de la columna va en S38.

#### S33. 94.5 frente a 95.5 % (05:444–446)
- **Viejo:** «La cobertura de punta a punta es del 89.2\,\% [85.1, 93.2] con objetos nuevos y del 95.5\,\% [95.1, 95.9] con objetos conocidos; la brecha es de 6.3 puntos [2.5, 10.4] (intervalos de 95\,\% por remuestreo de los pliegues).»
- **Nuevo:** el texto viejo se queda y se le agrega: «La cifra con objetos conocidos no coincide con el 94.5\,\% del experimento 13 porque se mide sobre otro banco y con otros modelos. Aquí es la media de diez pliegues, cada uno con modelos construidos con nueve objetos por clase y evaluado sobre 41 vistas no usadas de cada clase; el experimento 13 mide sobre las 656 imágenes de prueba, con sus propios modelos.»
- **Por qué:** C10. La fuente está en `results/`:
  - `results/experimento13/README.md:41`: con 16 variantes en el contenido y en el directorio, la cobertura de punta a punta es de 94.5 [94.4, 94.5], sobre las 656 imágenes de prueba.
  - `results/experimento16/README.md:3` y `:7`: 95.5 [95.1, 95.9], sobre 41 vistas no usadas de los objetos que contribuyeron, por clase y por pliegue, con el contenido y la fase A construidos con nueve objetos.

  Las dos cifras miden la cobertura de punta a punta sobre vistas nuevas de objetos conocidos, pero con bancos y modelos distintos. No cambia ninguna cifra.

#### S34. El llenado y la división entre la media (05:239–242)
- **Viejo:** «También se probó dividir la puntuación temprana de cada módulo entre la media de su memoria de contenido ($\div$\texttt{mem.mean}): \emph{empeora} la fase temprana (76.2\%) y distorsiona los conteos del directorio, porque con el llenado por instancias las masas de contenido ya están igualadas por construcción y esa corrección sobra.»
- **Nuevo:** «También se probó dividir la puntuación temprana de cada módulo entre la media de su memoria de contenido. Esa división \emph{empeora} la fase temprana (76.2\,\%) y distorsiona los conteos del directorio, porque con el llenado imagen-etiqueta las masas de contenido ya están igualadas por construcción y la corrección sobra.»
- **Por qué:** C10 (llenado), C12 (identificador) y 5.7 (dos puntos).

### C11. Frases que obligan a releer

#### S35. Lectura estricta del directorio visual (03:437–440)
- **Viejo:** «No tolera huecos: en un directorio perspectival, una coordenada queda sin registro para todos los módulos según lo que el dueño del directorio presenció de los demás, así que una tolerancia $\xi > 0$ dependería de esa historia y no del módulo (Sección~\ref{sec:hemisferio-visual}).»
- **Nuevo:** «No tolera huecos. En un directorio perspectival, las coordenadas que quedan sin registro para cada módulo dependen de lo que el dueño del directorio presenció de ese módulo; una tolerancia $\xi > 0$ dependería entonces de esa historia y no del módulo consultado (Sección~\ref{sec:hemisferio-visual}).»
- **Por qué:** C11. «Para todos los módulos según lo que…» se leía como si todos tuvieran los mismos huecos.

#### S36. Generalización con el volumen de llenado (05:310–313)
- **Viejo:** «Con $\xi = 0$ el sistema no generaliza desde cero; la generalización a imágenes de prueba aparece a medida que el llenado cubre más del espacio latente de la clase (del 0\% en $N = 25$ al 56\% en $N = 328$), sin necesidad de ajustar $\xi > 0$ en el contenido.»
- **Nuevo:** «Con $\xi = 0$ y 25 o 50 imágenes por clase, el módulo no acepta ninguna imagen de prueba de su clase. La aceptación crece a medida que el llenado cubre más del espacio latente de la clase, del 0\,\% con $I = 25$ al 56\,\% con $I = 328$, sin tolerar huecos en el contenido.»
- **Por qué:** C11: «no generaliza desde cero» no decía qué pasa. Los datos son de la columna «Prueba propia» de la Tabla 4: 0, 0, 2, 20 y 56.

#### S36b. Sonda de rechazo fuera de dominio (05:174–177)
- **Viejo:** «Las 2 restantes se enrutan porque comparten tokens con etiquetas legítimas de algún dominio (p.\ ej.\ \textit{food}): la frontera entre ``fuera de dominio'' y ``comparte conceptos con el dominio'' es semántica, no léxica.»
- **Nuevo:** «Las 2 restantes se enrutan porque comparten tokens con etiquetas legítimas de algún dominio (p.\ ej.\ \textit{food}). Distinguir una consulta fuera de dominio de una que comparte conceptos con el dominio es una cuestión semántica, y la contención, que trabaja token por token, no la resuelve.»
- **Por qué:**
  - C11: «la frontera… es semántica, no léxica» no decía qué consecuencia tiene, y los tokens compartidos sí son léxicos. La frase nueva dice qué no resuelve la contención.
  - Que la contención trabaja token por token está en 03:343 y 03:377.
  - También quita una antítesis y unos dos puntos.

#### S37. Banco del rescate léxico (04:94 y 04:101–103)
- **Viejo:** «Un \emph{rescate de atención léxica} recupera un token» / «Sobre el banco completo la regla afecta a 46 consultas: con el rescate aciertan 43 (93.5\%) y sin él 33 (71.7\%), diez aciertos más (21.7 puntos), y sin él cuatro se rechazan.»
- **Nuevo:** «Un \emph{rescate léxico} recupera un token» / «Sobre el banco completo, la regla cambia el resultado de 46 consultas. Con el rescate aciertan 43 (93.5\,\%); sin él aciertan 33 (71.7\,\%) y cuatro se rechazan. La diferencia es de diez aciertos (21.7 puntos).»
- **Por qué:** C10 (nombre) y C11. Las cifras cuadran: 43/46 = 93.48 %, 33/46 = 71.74 % y la diferencia es de 21.74 puntos.

#### S38. Comentario de la variedad y punto de operación (05:320–324)
- **Viejo:** «La precisión temprana crece con $N$ y se estabiliza en torno al 81\% desde $N = 200$; la entropía de la memoria de contenido crece con $N$ y se satura (3.65, 4.37, 4.95, 5.20 y 5.32 bits), coherente con la acumulación de variedad. El sistema opera con $N = 200$: ahí la precisión temprana ya se estabilizó, y quedan \texttt{train[200:328]} para las interacciones visuales (Sección~\ref{sec:dataset}).»
- **Nuevo:** «La precisión temprana crece con $I$ y se estabiliza en torno al 81\,\% desde $I = 200$; la entropía de la memoria de contenido crece con $I$ y se satura (3.65, 4.37, 4.95, 5.20 y 5.32 bits), coherente con la acumulación de variedad. La distancia entre recuperaciones de una misma pista (Variedad $L_1$) se mantiene entre 1.74 y 1.91 niveles hasta $I = 200$ y sube a 2.18 con $I = 328$. El sistema opera con $I = 200$, porque ahí la precisión temprana ya se estabilizó y quedan 128 imágenes de entrenamiento por clase para la formación visual (Sección~\ref{sec:dataset}).»
- **Por qué:**
  - C12: la columna «Variedad $L_1$» no se comentaba. La frase nueva solo lee la Tabla 4; si el autor prefiere, la columna puede salir.
  - C8 ($I$), C12 (identificador) y 5.7 (dos puntos).
  - La duda sobre «coherente con la acumulación de variedad» va en la Parte 4, punto 21.

#### S39. G frente a B1 (05:64–67)
- **Consolidación:** absorbido en M2.4 de `revision_jurado_metodologia_prosa.md`, que además explica por qué G varía y B1 no.
- **Viejo:** «La combinación G supera a B1 por medio punto (93.5\% frente a 93.0\%), menos de lo que G varía entre semillas (de 93.0 a 93.7\%; B1 da lo mismo con todas): una vez que la puntuación mide evidencia por registro y no evidencia total, balancear las consultas y depurar el vocabulario aportan poco.»
- **Nuevo:** «La combinación G supera a B1 por medio punto (93.5\,\% frente a 93.0\,\%). Es menos de lo que G varía entre semillas, de 93.0 a 93.7\,\%; B1 da 93.0\,\% con todas. Una vez que la puntuación mide evidencia por registro y no evidencia total, balancear las consultas y depurar el vocabulario aportan poco.»
- **Por qué:** C11. Cifras comprobadas en el CSV: con $N = 400$, G da 93.0 como mínimo y 93.7 como máximo, y B1 da 93.0 en las cinco semillas.

#### S40. Léxico compartido de las frutas (05:99–103)
- **Viejo:** «Las clases de fruta comparten léxico genérico (\textit{fruit} las tres, \textit{pome} \texttt{apple} y \texttt{pear}, \textit{red} \texttt{apple} y \texttt{tomato}) y concentran 18 de los 28 errores que deja B1, la mitad \texttt{pear} $\to$ \texttt{apple} (9); el otro foco es \texttt{horse} $\to$ \texttt{cow} (6).»
- **Nuevo:** «Las clases de fruta comparten léxico genérico: \textit{fruit} aparece en las tres, \textit{pome} en \texttt{apple} y \texttt{pear}, y \textit{red} en \texttt{apple} y \texttt{tomato}. Entre ellas caen 18 de los 28 errores que deja B1, la mitad de \texttt{pear} hacia \texttt{apple} (9). El otro foco es \texttt{horse} hacia \texttt{cow} (6).»
- **Por qué:** C11. En la matriz de confusión de B1 con $N = 400$ (CSV), los 18 errores entre frutas son 3 de `apple→pear`, 3 de `apple→tomato`, 9 de `pear→apple` y 3 de `pear→tomato`; `horse→cow` da 6.

#### S41. El rechazo y la salida semántica (05:374–400)
- **Viejo:** «Reconocimiento, rechazo y reconstrucción son operaciones de la propia memoria: el codificador ResNet18 solo convierte la imagen en una pista latente, y a partir de ahí la EAM decide. La Figura~\ref{fig:rechazo-imagenes} ilustra el rechazo: imágenes reales que la memoria contiene se aceptan, mientras que imágenes reales no contenidas y las sondas sintéticas de ruido y de píxeles barajados reciben puntuación cero en los ocho módulos y se rechazan, sin que intervenga ningún filtro externo. La tercera sonda, un lienzo gris uniforme, no llega a la memoria: la norma de su latente (10.7) queda por debajo del umbral de energía $\tau = 16.61$ (Sección~\ref{sec:percepcion}), igual que una vista real de \texttt{cow} del panel. Sin ese umbral, el contenido sí le daría soporte. El experimento 14 localizó la causa: el codificador lleva las entradas sin estructura (gris uniforme, un objeto desenfocado o sin contraste) a latentes de norma baja que caen dentro de la envolvente por coordenada de los animales. Los grises de nivel 120 a 160 (el del panel, 127, cae en ese tramo) los aceptan a la vez \texttt{cow}, \texttt{dog} y \texttt{horse}, aunque la instancia real más cercana está a entre 2.4 y 2.9 veces la mediana de la distancia intraclase. No es cualquier fondo liso: de 12 sólidos de color se aceptan 2. Esos grises tienen norma de 10.7 a 13.0, y el umbral los rechaza. Las entradas degeneradas que sí pasan el umbral se discuten en la Sección~\ref{sec:limitaciones}. La Figura~\ref{fig:imagen-etiquetas} muestra la salida semántica: para cada imagen aceptada, la reconstrucción es lo que la memoria \emph{evoca} (decodificación de la recuperación desde la lectura latente $M^R$), no la imagen de entrada, y el sistema devuelve las etiquetas asociadas. Que la reconstrucción difiera de la entrada es esperado y honesto: refleja que decide la distribución acumulada en la memoria.»
- **Nuevo:**

  > Reconocimiento, rechazo y reconstrucción son operaciones de la propia memoria. El codificador ResNet18 solo convierte la imagen en una pista latente, y a partir de ahí decide la EAM. La Figura~\ref{fig:rechazo-imagenes} ilustra el rechazo. Las imágenes reales que la memoria contiene se aceptan. Las que no contiene, y las sondas sintéticas de ruido y de píxeles barajados, reciben puntuación cero en los ocho módulos y se rechazan sin ningún filtro externo. La tercera sonda, un lienzo gris uniforme, no llega a la memoria, porque la norma de su latente (10.7) queda por debajo del umbral de energía $\tau = 16.61$ (Sección~\ref{sec:percepcion}); lo mismo le ocurre a una vista real de \texttt{cow} del panel.
  >
  > Sin ese umbral, el contenido sí le daría soporte al lienzo gris. El experimento 14 localizó la causa. El codificador lleva las entradas sin estructura (gris uniforme, un objeto desenfocado o sin contraste) a latentes de norma baja que caen dentro de la envolvente por coordenada de los animales, es decir, que en cada coordenada toman un valor que esas memorias ya tienen registrado. Los grises de nivel 120 a 160 (el del panel, 127, cae en ese tramo) los aceptan a la vez \texttt{cow}, \texttt{dog} y \texttt{horse}, aunque la instancia real más cercana está a una distancia de entre 2.4 y 2.9 veces la mediana de la distancia intraclase. De 12 colores lisos se aceptan solo 2. Esos grises tienen norma de 10.7 a 13.0, y el umbral los rechaza. Las entradas degeneradas que sí pasan el umbral se discuten en la Sección~\ref{sec:limitaciones}.
  >
  > \paragraph{Salida semántica.} La Figura~\ref{fig:imagen-etiquetas} muestra, para cada imagen aceptada, la reconstrucción que la memoria \emph{evoca} (la decodificación de la recuperación desde la lectura latente $M^R$) y las etiquetas que devuelve el sistema. Que la reconstrucción difiera de la entrada es lo esperado, porque la decide la distribución acumulada en la memoria.
- **Por qué:**
  - C11 (párrafo largo) y C9 (envolvente).
  - 5.2 («sólidos de color»), 5.3 («está a entre») y 5.5 («esperado y honesto»).
  - 5.7: quita siete dos puntos y dos antítesis. Una es «no la imagen de entrada», que ya dice el pie de la Figura 9 (`fig16`); la otra, «No es cualquier fondo liso:».

#### S42. Cobertura de punta a punta (04:255–257)
- **Viejo:** «\item \textbf{Cobertura de punta a punta} (hemisferio visual): fracción de las imágenes de prueba enrutadas a su clase cuyo módulo destino además responde: la recuperación $\beta$ desde el latente lo reconoce.»
- **Nuevo:** «\item \textbf{Cobertura de punta a punta} (hemisferio visual): fracción de las imágenes de prueba que se enrutan a su clase y a las que, además, responde el módulo destino. El módulo responde cuando su recuperación $\beta$ desde el latente no deja columnas vacías en la proyección.»
- **Por qué:** C11. Había dos dos puntos y un «lo» ambiguo. El criterio es el de `results/experimento13/README.md:3`: «proyección sin filas vacías, el criterio de `recall_from_right`». Lo mismo que 05:599 y 05:618 ya llaman «columnas».

#### S43. Sigla en el resumen (main:62–63)
- **Consolidación:** absorbido en estructura 9.1, que ya expandía la sigla.
- **Viejo:** «y presenta EAM-TMS, un sistema distribuido de memoria transactiva»
- **Nuevo:** «y presenta EAM-TMS (\textit{Entropic Associative Memory -- Transactive Memory System}), un sistema distribuido de memoria transactiva»
- **Por qué:** C12.

#### S44. PCA (06:31)
- **Viejo:** «Izquierda: proyección PCA 2D, con la envolvente»
- **Nuevo:** «Izquierda: proyección en las dos primeras componentes principales (PCA, por sus siglas en inglés), con la envolvente»
- **Por qué:** C12.

#### S45. POS (06:316–317)
- **Viejo:** «El rescate de atención léxica (Sección~\ref{sec:pipeline-semantico}) admite tokens que el filtro gramatical (POS) descarta si figuran en el vocabulario»
- **Nuevo:** «El rescate léxico (Sección~\ref{sec:pipeline-semantico}) admite tokens que el filtro de categoría gramatical (POS, por \textit{part of speech}) descarta si figuran en el vocabulario»
- **Por qué:** C10 y C12. Con esto queda cubierta también 06:322 («etiqueta POS de diccionario»).

#### S46. Párrafos largos de la metodología (04:143–147 y 04:182–189)
- **Consolidación:** 04:182-189 va absorbido en M3.2 de `revision_jurado_metodologia_prosa.md`; 04:143-147 se aplica aquí.
- **Viejo (04:143–147):** «Los vectores latentes se cuantizaron a $m = 32$ niveles mediante normalización global min-max con un margen del 10\%, calculada solo sobre el conjunto de llenado (\texttt{train[0:200]} por clase) con el original, el espejo y las rotaciones de $\pm 12^{\circ}$ de cada imagen (6400 latentes), y se guarda con el modelo; lo que cae fuera del rango se recorta al nivel extremo.»
- **Nuevo:** «Los vectores latentes se cuantizaron a $m = 32$ niveles con una normalización global min-max con un margen del 10\,\%. El rango se calculó solo sobre las 200 imágenes de llenado de cada clase, con la original, el espejo y las rotaciones de $\pm 12^{\circ}$ de cada una (6400 latentes), y se guardó con el modelo. Lo que cae fuera del rango se recorta al nivel extremo.»
- **Viejo (04:182–189):** «Otros tres bancos se usan una sola vez: las 16 consultas de la reproducción por etapas (\texttt{TEST\_QUERIES}, 2 por dominio) y 12 consultas representables que describen objetos fuera de los ocho dominios, ambas en la Sección~\ref{sec:proto-completo}; y, en la comparación con una sola EHAM (Sección~\ref{sec:eham-unica}), una partición del banco (las primeras 30 consultas de cada clase forman los directorios y las 171 restantes quedan reservadas para evaluar) más 40 consultas fuera de dominio: las 12 anteriores y 28 de objetos y escenas de categorías ausentes de ETH-80, sin palabras del vocabulario de etiquetas.»
- **Nuevo:** «Otros tres bancos se usan una sola vez. La Sección~\ref{sec:proto-completo} usa las 16 consultas de referencia del sistema (dos por dominio) y 12 consultas representables que describen objetos fuera de los ocho dominios. La comparación con una sola EHAM (Sección~\ref{sec:eham-unica}) usa una partición del banco, en la que las primeras 30 consultas de cada clase forman los directorios y las 171 restantes quedan reservadas para evaluar, más 40 consultas fuera de dominio: las 12 anteriores y 28 de objetos y escenas de categorías ausentes de ETH-80, sin palabras del vocabulario de etiquetas.»
- **Por qué:** C11 (párrafos largos) y C12 (`train[0:200]` y `TEST_QUERIES`). Los 6400 latentes son 1600 imágenes × 4 variantes.

#### S47. Formación del directorio (05:248–254)
- **Viejo:** «Se midió cuántas interacciones necesita el directorio para volverse utilizable y si importa su orden: tras cada interacción $t$ de la fase temprana se evaluó la precisión madura (lectura B1) sobre las 80 consultas, con el directorio tal como estaba en ese momento, en cuatro condiciones: orden intercalado entre dominios, barajado (5 semillas), bloqueado por dominio (todas las consultas de una clase y luego las de la siguiente) y un control en orden intercalado que elige al ganador temprano con la puntuación cruda, sin compuerta ni normalización.»
- **Nuevo:** «Se midió cuántas interacciones necesita el directorio para volverse utilizable y si importa su orden. Tras cada interacción $t$ de la fase temprana se evaluó la precisión madura (lectura normalizada) sobre las 80 consultas, con el directorio tal como estaba en ese momento. Se compararon cuatro condiciones: orden intercalado entre dominios; orden barajado (cinco semillas); orden bloqueado por dominio, con todas las consultas de una clase antes que las de la siguiente, y un control en orden intercalado que elige al ganador temprano con la puntuación cruda, sin compuerta ni normalización.»
- **Por qué:** C11, C3 y 5.4 (números en letra). La propuesta de estructura toca 05:262–270 (M5, «por construcción»), pero no este párrafo.

#### S48. Batería con una sola memoria (05:569–579)
- **Consolidación:** se aplica aquí, con `[PENDIENTE: exp11 corregido]` al final de la frase del 1.3 %, que es del brazo del protocolo. Antes de aplicar «con la batería completa de experimentos», comprobar el menor del dictamen de metodología: los experimentos 10 y 15 no se habrían vuelto a correr con una sola memoria, y sus carpetas en `results/` son del 28 oct, anteriores al cambio a una sola memoria (`0c70824`, 1 nov). Si se confirma, «salvo los experimentos 10 y 15».
- **Viejo:** «Se volvió a correr la batería completa con una sola memoria de contenido por módulo, leyendo los pesos de la hetero.» … «En texto cambian los recuerdos muestreados, tanto como al cambiar la semilla, y una parte pequeña de las decisiones donde pesan las lecturas de etiquetas: el 1.3\,\% de los destinos del protocolo en la comparación con una sola EHAM (Sección~\ref{sec:eham-unica}), una consulta de 80 en la curva de capacidad con 50 imágenes por clase, y las columnas con $\kappa > 0$ del barrido, cuyos cuantiles se recalculan sobre la lectura. Todas las cifras de este documento son las de una sola memoria de contenido.»
- **Nuevo:** «Las dos arquitecturas se compararon con la batería completa de experimentos.» … «En texto cambian los recuerdos muestreados, tanto como al cambiar la semilla, y una parte pequeña de las decisiones en que pesan las lecturas de etiquetas. Cambia el 1.3\,\% de los destinos del protocolo en la comparación con una sola EHAM (Sección~\ref{sec:eham-unica}) [PENDIENTE: exp11 corregido] y una consulta de 80 en la curva de capacidad con 50 imágenes por clase. También cambian las columnas con $\kappa > 0$ del barrido, cuyos cuantiles se recalculan sobre la lectura.»
- **Por qué:**
  - 5.1: «se volvió a correr» y la frase de 05:579 son huellas de versiones.
  - C11: la frase era larga y llevaba dos puntos.
  - Que la frase de 05:579 tampoco vale para los experimentos 10 y 15 va en la Parte 4, punto 9.

#### S49. Imágenes sin pareja y lesión (05:589–595 y 05:601–604)
- **Viejo:** «consultas): de las 800 imágenes sin palabra, la hetero nombra 722 por su parecido con las emparejadas y 78 quedan reconocidas sin nombre. Ninguna de las dos recupera una imagen concreta a partir de la mitad de sus coordenadas: lo completado queda» / «Con una sola memoria y el daño al azar, la familiaridad leída de la hetero tampoco cae mientras queda algo que nombrar: entre el 5 y el 25\,\% de celdas destruidas el módulo ya no nombra ninguna imagen y reconoce 795 a 800 de 800.»
- **Nuevo:** «consultas). De las 800 imágenes sin palabra, la memoria heteroasociativa nombra 722 por su parecido con las emparejadas, y 78 quedan reconocidas sin nombre. Ninguna de las dos recupera una imagen concreta a partir de la mitad de sus coordenadas. Lo completado queda» / «Con una sola memoria y daño al azar, la familiaridad leída de la memoria heteroasociativa tampoco cae mientras el daño es moderado. Con el 5 y el 25\,\% de celdas destruidas, el módulo ya no nombra ninguna imagen y aún reconoce 800 y 795 de las 800.»
- **Por qué:**
  - C11 y 5.7.
  - «Mientras queda algo que nombrar» contradecía su propio ejemplo: con el 5 y el 25 % ya no queda nada que nombrar y la familiaridad sigue.
  - Cifras de la Tabla 6: 800 con $f = 0.05$ y 795 con $f = 0.25$.
  - Si el autor quería decir otra cosa, conviene que lo aclare.

#### S50. El paréntesis de «comunicación distintiva» (07:49–52)
- **Consolidación:** absorbido en estructura 7.6.
- **Viejo:** «y comunicación distintiva (las clases que preguntan con léxico compartido pierden hacia su vecina).»
- **Nuevo:** «y comunicación distintiva (las consultas de las clases con léxico compartido se van hacia la clase vecina).»
- **Por qué:** C11: las clases no preguntan. El resto de la frase, que atribuye a Wegner la «comunicación distintiva», lo decide la propuesta de estructura (Parte 4, punto 15).

### C12. Tablas, figuras e identificadores

#### S51. Distancia sin unidad en la Tabla 5 (05:483–485 y 05:503–504)
- **Consolidación:** absorbido en M1.2 y M1.3 de `revision_jurado_metodologia_prosa.md`, que agregan «de la clase de la consulta» (Parte 4, punto 11).
- **Viejo:** «clase correcta según el juez 1-NN, distancia a la instancia real más cercana y, en el protocolo,» / «Distancia a la instancia   & EHAM única»
- **Nuevo:** «clase correcta según el juez 1-NN, distancia euclidiana, en el espacio latente continuo, a la instancia real más cercana y, en el protocolo,» / «Distancia euclidiana a la   & EHAM única». En la línea siguiente de la tabla, «instancia real más cercana» → «instancia real más cercana (latente)».
- **Por qué:** C12. Comprobado en `run_experiment9_member_loss.py:239–246`, el `Judge` que usa `run_experiment11_monolithic.py:378`: descuantiza el latente recuperado y mide con `np.linalg.norm`. Hay un matiz de contenido en la Parte 4, punto 11.

#### S52. Tabla 7 (costo), Figura 1 y Figura 8 (05:649, 05:663, 03:191 y 05:405)
- **Viejo:** «(etapas 1 a 8, solo CPU)» / «Sistema completo (etapas 1--8)» / «Las lecturas $M^L$ y $M^R$ (punteadas) se calculan de» / «Rechazo de imágenes en el hemisferio visual (sin filtro léxico), con el umbral»
- **Nuevo:** «(solo CPU)» / «Sistema completo» / «Las lecturas $M^L$ y $M^R$ (con trazo discontinuo) se calculan de» / «Rechazo de imágenes en el hemisferio visual, con el umbral»
- **Por qué:** C12.
  - Las «etapas 1 a 8» son los `stage1`–`stage8` de `src/`, y la tesis nunca las define; 05:642 ya dice qué abarca la medición.
  - Los nodos son `dashed`, es decir, de trazo discontinuo, no punteados.
  - El filtro léxico no aplica a imágenes.

#### S53. Identificadores de código en la prosa (02:73–76, 02:248, 05:165 y 05:463–464)
- **Viejo:** «la implementación de referencia de Pineda y Morales los devuelve (\texttt{recog\_weights}), y este trabajo» / «Es la operación \texttt{project()} de la implementación de referencia de Pineda y Morales» / «Con las 16 consultas de referencia del sistema (\texttt{TEST\_QUERIES}, 2 por dominio),» / «(\texttt{recognize\_gated}, \texttt{recall\_from\_left}), sin enrutamiento.»
- **Nuevo:** «la implementación de referencia de Pineda y Morales los devuelve\footnote{Función \texttt{recog\_weights}.}, y este trabajo» / «Es la operación de proyección de la implementación de referencia de Pineda y Morales\footnote{Función \texttt{project()}.}» (la llamada va antes de la coma, como en 02:214) / «Con las 16 consultas de referencia del sistema (dos por dominio),» / «(ecuación~\eqref{eq:score-gated} y Sección~\ref{sec:operaciones}), sin enrutamiento.»
- **Por qué:** C12.
  - Los identificadores de 05:324 van en S38, y los de 04:34, 04:43, 04:47, 04:145, 04:183 y 05:331 en S11, S12 y S46.
  - Las rutas `results/...` (04:156–160, 05:478 y 05:650) y los números de experimento dependen de E8 y se dejan a la propuesta de estructura.

### 5.1. Huellas de versiones

#### S54. Subtítulo y fecha (main:47 y main:50)
- **Viejo:** «\large Ocho módulos sobre ETH-80 completo\\[0.5em]» / «\date{Julio 2026}»
- **Nuevo:** «\large Ocho módulos sobre el conjunto ETH-80\\[0.5em]» / «\date{julio de 2026}»
- **Por qué:** 5.1 y 5.4. En español el mes va con minúscula y con «de». La fecha en sí (E9) la decide el autor.

#### S55. «Sistema actual» (01:103, 05:6–7 y 07:82)
- **Consolidación:** 01:103 sale con la contribución 4 (estructura 9.2) y 07:82 sale con la frase (estructura 9.4); 05:6-7 se aplica aquí.
- **Viejo:** «números reportados son trazables a corridas del sistema actual, sobre datos no fabricados.» / «y todos los números son trazables a corridas del sistema actual (Sección~\ref{sec:auditoria}).» / «reportados son trazables a corridas del sistema actual, sin vectores sintéticos ni»
- **Nuevo:** «…trazables a corridas de este sistema, sobre datos no fabricados.» / «y todos los números son trazables a corridas de este sistema (Sección~\ref{sec:auditoria}).» / «…trazables a corridas de este sistema, sin vectores sintéticos ni»
- **Por qué:** 5.1. «Datos no fabricados» (5.6) y la frase de 07:81–83 (C1) se dejan a la propuesta de estructura (Parte 4, puntos 1 y 2).

#### S56. «Ninguna sintética» (04:75–76)
- **Viejo:** «de modo que las ocho clases quedan con 21 etiquetas efectivas cada una y ninguna sintética.»
- **Nuevo:** «de modo que las ocho clases quedan con 21 etiquetas cada una, todas con vector real.»
- **Por qué:** 5.1. 03:488–489 confirma 168 entradas, que son 8 × 21.

#### S57. Las homoasociativas en las conclusiones (07:66–70)
- **Viejo:** «Las memorias homoasociativas que acompañaban a la heteroasociativa resultaron ser lecturas de ella: con los pesos leídos de la hetero, el sistema toma las mismas decisiones, y, ante el mismo daño en todas las memorias, la familiaridad leída de la hetero resiste más que la de una memoria homo aparte (con el 1\,\% de las celdas destruidas, 800 frente a 416 de 800 imágenes).»
- **Nuevo:** «Las memorias homoasociativas que la implementación de referencia llena aparte equivalen a lecturas de la heteroasociativa. Con los pesos leídos de la memoria heteroasociativa, el sistema toma las mismas decisiones y, ante el mismo daño en todas las memorias, la familiaridad leída de ella resiste más que la de una memoria homoasociativa aparte (con el 1\,\% de las celdas destruidas, 800 frente a 416 de 800 imágenes).»
- **Por qué:** 5.1 («acompañaban… resultaron ser») y 5.7. El paso de homoasociativa más heteroasociativa a una sola heteroasociativa es la excepción que la convención permite mencionar, pero aquí se dice como hecho y no como historia. 02:213–216 ya presenta así la implementación de referencia.

#### S58. Las homoasociativas en resultados (05:556–561)
- **Viejo:** «Cada módulo guarda su contenido en una sola memoria heteroasociativa (en adelante, la hetero), y las lecturas homoasociativas que usa se calculan de ella (ecuación~\eqref{eq:marginal}). Esta sección la compara con la arquitectura que guarda, junto a la hetero de cada módulo, dos memorias homoasociativas llenadas aparte (las homo), una por dominio, como fuente de pesos.»
- **Nuevo:** «Cada módulo guarda su contenido en una sola memoria heteroasociativa, y las lecturas homoasociativas que usa se calculan de ella (ecuación~\eqref{eq:marginal}). Esta sección la compara con la arquitectura que guarda, junto a la memoria heteroasociativa de cada módulo, dos memorias homoasociativas llenadas aparte, una por dominio, como fuente de pesos.»
- **Por qué:** 5.1. Sin las abreviaturas, el resto de la sección sigue la regla 3.5.

### 5.2. Anglicismos que obligan a reescribir la frase

#### S59. Recuperaciones imaginativas (02:110–112)
- **Viejo:** «valores altos favorecen recuperaciones imaginativas al costo de falsas recolecciones \cite{pineda2023imagery}.»
- **Nuevo:** «valores altos favorecen recuperaciones imaginativas a costa de falsos recuerdos \cite{pineda2023imagery}.»

#### S60. Costo computacional (05:641–644)
- **Viejo:** «Se midió el tiempo de pared (\textit{wall-clock}) de reproducir el sistema completo desde cero, de la partición del conjunto de datos a la fase madura, en una laptop con un Intel Core Ultra 7 265HX (20 hilos lógicos) y 16.6~GB de RAM, con la GPU oculta: todo corre en CPU.»
- **Nuevo:** «Se midió el tiempo real transcurrido de reproducir el sistema completo desde cero, de la partición del conjunto de datos a la fase madura, en una computadora portátil con un Intel Core Ultra 7 265HX (20 hilos lógicos) y 16.6~GB de RAM, con la GPU deshabilitada, de modo que todo corre en CPU.»

#### S61. Brazos y verdad de terreno (05:465–467 y 05:528)
- **Consolidación:** 05:528 va absorbido en M1.1 de `revision_jurado_metodologia_prosa.md`; 05:465-467 se aplica aquí, y «Configuración» de la Tabla 5 ya está en M1.3.
- **Viejo:** «Se compararon tres brazos: la \emph{EHAM única}; los especialistas con el módulo elegido por la verdad de terreno (\emph{oráculo}, un techo), y el \emph{protocolo} transactivo completo» / «Lo que cuesta elegir el módulo con el directorio en lugar de con la verdad de terreno, la»
- **Nuevo:** «Se compararon tres configuraciones: la \emph{EHAM única}; los especialistas con el módulo elegido por la clase real (\emph{oráculo}, un techo), y el \emph{protocolo} transactivo completo» / «Lo que cuesta elegir el módulo con el directorio en lugar de con la clase real, la»
- **Por qué:** 5.2. En la Tabla 5, «Brazo» pasa a «Configuración» (05:495).

### 5.3. Gramática

#### S62. Concordancias, régimen y fórmulas fijas

| Línea | Viejo | Nuevo |
|---|---|---|
| 02:143–144 | «a dominios o modalidades distintas.» | «a dominios o modalidades distintos.» |
| 02:217–218 | «leer esos pesos de la heteroasociativa deja las mismas decisiones.» | «leer esos pesos de la heteroasociativa produce las mismas decisiones.» |
| 03:408–409 | «La división por $c_k + 1$ convierte \emph{evidencia total} en \emph{evidencia por registro}, haciendo que la puntuación refleje calidad de especialización y no cantidad.» | «La división por $c_k + 1$ convierte \emph{evidencia total} en \emph{evidencia por registro}, de modo que la puntuación refleja la calidad de la especialización.» |
| 05:10 | «\subsection{Calibración del directorio a ocho módulos}» | «\subsection{Calibración del directorio con ocho módulos}» |
| 05:191 | «módulo contiene al token, lo que da» | «módulo contiene el token, lo que da» |
| 05:372 | «vocabulario de la clase real en 113 de 116 (97.4\%) de los casos.» | «vocabulario de la clase real en 113 de los 116 casos (97.4\,\%).» (absorbida en Me.1 de `revision_jurado_metodologia_prosa.md`) |
| 05:449–450 | «\texttt{horse}, enviados a \texttt{dog}): la envolvente por coordenada cubre a un objeto que no contribuyó a ella, y cuando no lo cubre lo rechaza.» | «\texttt{horse}, enviados a \texttt{dog}). La envolvente por coordenada cubre un objeto que no contribuyó a ella, y cuando no lo cubre, lo rechaza.» |

- **Por qué:** 5.3. En 03:409 hay además un gerundio de posterioridad y una antítesis (5.7). Las demás faltas del dictamen están en otros puntos:
  - «exige a… llegar», en S30;
  - «está a entre», en S41;
  - «cubre a» de 06:295, en S67;
  - «Este capítulo», en S2.

### 5.4. Ortotipografía que no es mecánica

#### S63. Paréntesis anidados (06:10–12)
- **Consolidación:** absorbido en estructura 7.1.
- **Viejo:** «Los componentes de la maquinaria (los directorios heteroasociativos, la lectura B1, el rechazo por contención, la actualización perspectival del directorio (en imagen) y la coordinación punto a punto) funcionan sin ajustes por dominio.»
- **Nuevo:** «Los componentes del mecanismo transactivo —los directorios heteroasociativos, la lectura normalizada, el rechazo por contención, la actualización perspectival del directorio (en imagen) y la coordinación punto a punto— funcionan sin ajustes por dominio.»
- **Por qué:** 5.4, 5.7 («maquinaria») y C3. Lo que la frase afirma lo decide la propuesta de estructura (Parte 4, punto 5).

#### S64. Oraciones que empiezan con un símbolo (04:153 y 05:617)
- **Viejo:** «$\tau$ es el mínimo de esa norma sobre las 1600 imágenes originales del llenado» / «(100 por módulo). $f$: fracción de celdas de la hetero destruidas al azar.»
- **Nuevo:** «El umbral $\tau$ es el mínimo de esa norma sobre las 1600 imágenes originales del llenado» / «(100 por módulo). La fracción de celdas de la memoria heteroasociativa destruidas al azar es $f$.»
- **Por qué:** 5.4. Los casos de 03:96 y 05:233 están en S20 y S27.

#### S65. Decimales en una misma enumeración (05:95–98, 05:120–121, 05:221–222, 05:226–227 y 06:101–103)

| Línea | Viejo | Nuevo |
|---|---|---|
| 05:95–98 | «(\texttt{cow}, \texttt{cup} y \texttt{tomato} 100\%, \texttt{car} 98\%, \texttt{dog} 93.9\%) y tres por debajo: \texttt{apple} 88.2\%, \texttt{horse} 88\% y \texttt{pear} 76\%» | «(\texttt{cow}, \texttt{cup} y \texttt{tomato} 100.0\,\%, \texttt{car} 98.0\,\%, \texttt{dog} 93.9\,\%) y tres por debajo: \texttt{apple} 88.2\,\%, \texttt{horse} 88.0\,\% y \texttt{pear} 76.0\,\%» |
| 05:120–121 | «y el módulo que más se aleja del ideal es \texttt{pear}, a 2.25 puntos (10.25\%).» | «y el módulo que más se aleja del ideal es \texttt{pear}, con el 10.2\,\%.» |
| 05:221–222 | «Una poda mayor destruye: $\iota = 0.5$ pierde 6 puntos con un rechazo del 11\%, y $\iota = 1.0$ rechaza el 86\%.» | «Una poda mayor perjudica. Con $\iota = 0.5$, la precisión temprana baja 6.2 puntos y el rechazo sube al 11.2\,\%, y con $\iota = 1.0$ se rechaza el 86.2\,\%.» |
| 05:226–227 | «Con $\iota = 0$, $\kappa$ solo rechaza: a medida que sube, la precisión baja de 81.2\% a 0.0\% y el rechazo sube de 5.0\% a 100\%, y ninguna columna mejora la línea base.» | «Con $\iota = 0$, $\kappa$ solo rechaza. A medida que sube, la precisión baja de 81.2\,\% a 0.0\,\% y el rechazo sube de 5.0\,\% a 100.0\,\%, sin que ninguna columna mejore la línea base.» |
| 06:101–103 | «quedan en 98--100\% y \texttt{dog} en 93.9\%; \texttt{pear} (76\%), \texttt{horse} (88\%) y \texttt{apple} (88.2\%) pierden» | «quedan entre 98.0 y 100.0\,\% y \texttt{dog} en 93.9\,\%; \texttt{pear} (76.0\,\%), \texttt{horse} (88.0\,\%) y \texttt{apple} (88.2\,\%) pierden» (absorbida en estructura 4.4) |

- **Por qué:** 5.4, y en el caso de «destruye:», también 5.5. Cifras verificadas:
  - Precisión madura por dominio con B1 y $N = 400$ (CSV): 88.24 / 98.0 / 100 / 100 / 93.88 / 88.0 / 76.0 / 100.
  - Tabla 3: 81.2 − 75.0 = 6.2, con rechazos de 11.2 y 86.2.
  - `pear` = 10.25. Se redondea a 10.2 con la regla que la tesis ya sigue, «al par»: 85.25 → 85.2, 13.75 → 13.8, 91.75 → 91.8.
- «A 2.25 puntos» sale porque se deduce del ideal, y redondeado daría 2.3. Si el autor prefiere conservarlo, que diga «a 2.2 puntos (10.2 %)».
- Las demás menciones de `pear` 76 % y `horse` 88 % (06:73, 06:327, 07:46 y 07:101) no están en enumeraciones con decimales y se quedan como están.

#### S66. «15 transformaciones, que son» (04:36–39)
- **Viejo:** «Cada imagen se registra en 16 variantes (3200 patrones por clase): la original y 15 transformaciones, que son el espejo; rotaciones de $\pm 12^{\circ}$ de la imagen y de su espejo, y de $\pm 6^{\circ}$ de la imagen; escalas de 0.9 y 1.1; brillo de 0.85 y 1.15, y desplazamientos de 6 píxeles en las cuatro direcciones.»
- **Nuevo:** «Cada imagen se registra en 16 variantes (3200 patrones por clase), la original y 15 transformaciones de ella: el espejo; las rotaciones de $\pm 12^{\circ}$ de la imagen y de su espejo, y de $\pm 6^{\circ}$ de la imagen; las escalas de 0.9 y 1.1; los brillos de 0.85 y 1.15, y los desplazamientos de 6 píxeles en las cuatro direcciones.»
- **Por qué:** 5.4. La suma da 15: 1 + 4 + 2 + 2 + 2 + 4.

### 5.5. Registro coloquial

#### S67. Frases coloquiales

| Línea | Viejo | Nuevo |
|---|---|---|
| 02:204 | «Las celdas del borde arrancan en 1, y la lectura descuenta ese 1.» | «Las celdas del borde se inicializan en 1, y la lectura descuenta ese 1.» |
| 04:141–142 | «así que el espacio latente con el que se evalúa el hemisferio visual se eligió mirando ese conjunto» | «así que el espacio latente con el que se evalúa el hemisferio visual se eligió con información de ese conjunto» |
| 05:354–358 | «\paragraph{Más variantes, más cobertura.} El directorio visual no tolera huecos ($\xi = 0$; la razón está en la Sección~\ref{sec:operaciones}): con $\xi = 2$, el enrutamiento del dominio propio baja a medida que el módulo presencia más dominios ajenos (experimento 10). La palanca para la cobertura es densificar el llenado, no tolerar huecos.» | «\paragraph{Más variantes, más cobertura.} El directorio visual no tolera huecos ($\xi = 0$; la razón está en la Sección~\ref{sec:operaciones}). Con $\xi = 2$, el enrutamiento del dominio propio baja a medida que el módulo presencia más dominios ajenos (experimento 10). Para ganar cobertura, el sistema densifica el llenado en lugar de tolerar huecos.» |
| 05:581 | «Para buscar algo que las memorias homo hicieran y la hetero no, se compararon las dos» | «Para comprobar si las memorias homoasociativas aportan alguna lectura que la heteroasociativa no tenga, se compararon las dos» |
| 05:668–674 | «La parte más cara no es el entrenamiento del codificador, la única con gradientes y retropropagación (21.5 min), sino las memorias: el llenado de las ocho memorias de contenido y el hemisferio visual suman 77.4 minutos, tres cuartas partes del total. Ninguna de las dos entrena nada: registran vectores cuantizados en las memorias (200 imágenes por 16 variantes en cada módulo) y los leen para decidir.» | «La parte más cara son las memorias. El llenado de las ocho memorias de contenido y el hemisferio visual suman 77.4 minutos, tres cuartas partes del total, frente a los 21.5 minutos del entrenamiento del codificador, la única parte con gradientes y retropropagación. Ninguna de las dos etapas ajusta parámetros: registran vectores cuantizados en las memorias (200 imágenes por 16 variantes en cada módulo) y los leen para decidir.» |
| 06:294–297 | «(Sección~\ref{sec:objetos-nuevos}), y lo que se pierde es respuesta, no acierto: la envolvente por coordenada cubre a la mayoría de los objetos que no contribuyeron a ella, rechaza las vistas que no cubre en lugar de enviarlas a otra clase, y la brecha se concentra en unos pocos objetos, no en clases.» | «(Sección~\ref{sec:objetos-nuevos}), pero el acierto sobre las imágenes aceptadas se mantiene (99.9\,\% en los dos bancos). La envolvente por coordenada cubre la mayoría de los objetos que no contribuyeron a ella y rechaza las vistas que no cubre en lugar de enviarlas a otra clase; la brecha se concentra en unos pocos objetos.» |
| 06:298–300 | «Con diez objetos por clase, ``objeto nuevo'' sigue siendo un objeto de la misma colección fotografiado en las mismas condiciones; fotos de otro origen son otra pregunta.» | «Con diez objetos por clase, «objeto nuevo» sigue siendo un objeto de la misma colección fotografiado en las mismas condiciones; la generalización a fotos de otro origen no se midió.» |
| 06:303 | «Dos elementos del protocolo se eligieron mirando el conjunto de prueba, por ausencia» | «Dos elementos del protocolo se eligieron con información del conjunto de prueba, por ausencia» (absorbida en M5.4 de `revision_jurado_metodologia_prosa.md`) |
| 07:89 | «del codificador y el número de variantes sin mirar el conjunto de prueba, y volver a» | «del codificador y el número de variantes sin usar el conjunto de prueba, y volver a» (absorbida en M5.5 de `revision_jurado_metodologia_prosa.md`) |

- **Por qué:** 5.5, y también 5.7 (antítesis y dos puntos).
  - En 05:358 y 06:294–297 se reescriben las tres antítesis; solo queda el contraste «en lugar de».
  - En 06:294 se agrega el 99.9 %: es la cifra de 05:447 en la que se apoyaba «no acierto», así que la afirmación no cambia.
  - En 05:672, la etapa visual sí decide, pero ninguna de las dos etapas ajusta parámetros.
  - «Releen» (06:82) va en la Parte 4, punto 4.

### 5.7. Rasgos de texto generado

#### S68. El estribillo «no inventa referentes» (02:302–303, 03:301 y 03:333–334)
- **Consolidación:** 02:302-303 va absorbido en estructura 2.1; 03:301 y 03:333-334 se aplican aquí.
- **Viejo:** «En este sistema, cuando ningún módulo reconoce el dominio de la consulta, el grupo la rechaza en vez de inventar un especialista; el rechazo es una respuesta válida.» / «{RECHAZO\\(el grupo no inventa\\referentes)}» / «Si ningún directorio alcanzable tiene soporte, o el destino no contiene la pista, el sistema rechaza: el grupo no inventa referentes.}»
- **Nuevo:** «En este sistema, cuando ningún módulo reconoce el dominio de la consulta, el grupo la rechaza, y el rechazo es una respuesta válida.» / «{RECHAZO}» / «Si ningún directorio alcanzable tiene soporte, o el destino no contiene la pista, el sistema rechaza la consulta.}»
- **Por qué:** 5.7. 02:298–303 también entra en la propuesta de estructura (M2, «sin coordinador central»); aquí solo cambia el estribillo.

#### S69. Repeticiones cercanas (01:124–127, 03:103 y 06:115–119)
- **Consolidación:** 06:115-119 va absorbido en estructura 4.4; 01:124-127 y 03:103 se aplican aquí.
- **Viejo:** «la Sección~\ref{sec:discusion} los discute y señala las limitaciones, y la Sección~\ref{sec:conclusiones} concluye y señala trabajo futuro.» / «Los tres diagramas siguientes muestran las tres etapas operativas del sistema:» / «El directorio visual comete dos falsos enrutamientos de 656. Es el rechazo de la Sección~\ref{sec:tmt}: lo que ningún módulo reconoce no se responde, y los falsos del contenido caen entre animales.»
- **Nuevo:** «la Sección~\ref{sec:discusion} los discute junto con las limitaciones, y la Sección~\ref{sec:conclusiones} cierra con el trabajo futuro.» / «Los diagramas siguientes muestran las tres etapas operativas del sistema:» / «El directorio visual comete dos falsos enrutamientos de 656. Es el rechazo de la Sección~\ref{sec:tmt}: lo que ningún módulo reconoce no se responde.»
- **Por qué:** 5.7. En 06:119 se repetía «entre animales», que ya está en 06:114–115. La repetición de 05:451–453 se resuelve en S70; las de 06:8–12 y 06:152–153 van en la Parte 4.

#### S70. Antítesis «X, no Y»

Conté 48 construcciones de los tipos «X, no Y», «X y no Y», «no X: Y», «no X, sino Y» y «no X, pero Y». De ellas, 17 están en pasajes de la propuesta de estructura (Parte 4, punto 6) y 31 en mi ámbito. Con esas 31:
- 9 ya se reescriben en otros puntos:
  - 05:62 (S14);
  - 05:177 (S36b);
  - 05:391 y 05:397 (S41);
  - 03:409 (S62);
  - 05:358, 05:669, 06:294 y 06:297 (S67).
- 13 se reescriben con la tabla de abajo.
- 9 se conservan.

**Se conservan** porque cada una aclara una confusión probable:
- 02:25 (la variante ponderada, no la booleana);
- 02:247 (el nombre es de este trabajo, el mecanismo no);
- 03:33 (las lecturas no son memorias);
- 03:439 (la tolerancia dependería de la historia, no del módulo; S35);
- 03:508 (la concordancia no es acierto);
- 04:113 (el vocabulario sirve para llenar, no para decidir);
- 05:27 (la medición es dentro de muestra);
- 06:288 (la partición es por imagen);
- 06:308 (16 no es un óptimo).

**Se reescriben:**

| Línea | Viejo | Nuevo |
|---|---|---|
| 02:45–46 | «La memoria no almacena patrones individuales: acumula una \textbf{distribución de experiencias}.» | «La memoria acumula una \textbf{distribución de experiencias}.» |
| 02:50–51 | «La memoria va formando abstracciones y prototipos a partir de esta superposición estadística; no se imponen desde el exterior ni se calculan de forma separada.» | «La memoria va formando abstracciones y prototipos a partir de esta superposición estadística, sin que se impongan desde el exterior ni se calculen por separado.» |
| 03:62 | «El estado ``desconocido'' no tiene coordenada propia: es el rechazo, y ocurre cuando» | «El estado «desconocido» no tiene coordenada propia; corresponde al rechazo, que ocurre cuando» |
| 03:191–192 | «se calculan de $M^H_{\mathrm{dom}}$ con la ecuación~\eqref{eq:marginal}; no se llenan.}» | «se calculan de $M^H_{\mathrm{dom}}$ con la ecuación~\eqref{eq:marginal}.}» |
| 03:479–481 | «El reconocimiento visual usa solo esa lectura, no la proyección hacia las etiquetas: el lado de etiquetas, cuantizado por magnitud, es más disperso y rechazaría imágenes que el lado latente sí contiene.» | «El reconocimiento visual usa solo esa lectura. La proyección hacia las etiquetas rechazaría imágenes que el lado latente sí contiene, porque el lado de etiquetas, cuantizado por magnitud, es más disperso.» |
| 03:493–495 | «La recuperación $\beta$ devuelve una \emph{muestra} de la distribución de etiquetas acumulada por el módulo, no una palabra exacta: el vector muestreado puede no coincidir con ningún vector almacenado.» | «La recuperación $\beta$ devuelve una \emph{muestra} de la distribución de etiquetas acumulada por el módulo, y el vector muestreado puede no coincidir con ningún vector almacenado.» |
| 04:72–73 | «(la suma de los pesos de todas sus aserciones, no el máximo)» | «(la suma de los pesos de todas sus aserciones)» |
| 04:120–121 | «Solo queda fuera lo que no es representable: un token sin vector fastText real no genera pista, lo cual es una frontera del codificador lingüístico y no un rechazo de la memoria.» | «Solo queda fuera lo que no es representable. Un token sin vector fastText real no genera pista y, por tanto, no llega a la memoria.» |
| 05:139–140 | «El sesgo que B1 corrige está en la lectura, no en los conteos (Sección~\ref{sec:disc-b1}).» | «El sesgo que corrige B1 está, por tanto, en la lectura (Sección~\ref{sec:disc-b1}).» (absorbida en estructura 5.4) |
| 05:436–438 | «La partición principal separa imágenes, no objetos: los diez objetos de cada clase aportan vistas al llenado y a la prueba (Sección~\ref{sec:dataset}), así que las cifras anteriores miden vistas nuevas de objetos conocidos.» | «En la partición principal, los diez objetos de cada clase aportan vistas al llenado y a la prueba (Sección~\ref{sec:dataset}), así que las cifras anteriores miden vistas nuevas de objetos conocidos.» |
| 05:451–453 | «La brecha no se reparte entre clases sino que se concentra en objetos concretos: 71 de los 80 objetos reservados superan el 70\,\%, y nueve (dos manzanas, dos peras, dos perros, una taza, un coche y una vaca) concentran el 57\,\% de los fallos.» | «La brecha se concentra en objetos concretos. De los 80 objetos reservados, 71 superan el 70\,\%, y nueve (dos manzanas, dos peras, dos perros, una taza, un coche y una vaca) reúnen el 57\,\% de los fallos.» |
| 05:565–567 | «La homo de etiquetas registra cada palabra una vez por su frecuencia y no una vez por imagen: tiene el mismo soporte que $M^{L}$, con conteos multiplicados por un factor de 21 a 95 que varía entre celdas.» | «La memoria homoasociativa de etiquetas registra cada palabra tantas veces como indica su frecuencia, mientras que la heteroasociativa la registra una vez por imagen. Por eso tiene el mismo soporte que $M^{L}$, con conteos multiplicados por un factor de 21 a 95 que varía entre celdas.» |
| 06:272–274 | «una cabeza auxiliar de clasificación que solo interviene en el entrenamiento, no en las decisiones; no es un efecto del sistema de memorias y puede abordarse por separado.» | «una cabeza auxiliar de clasificación que solo interviene en el entrenamiento; puede abordarse por separado del sistema de memorias.» |

- **Por qué:**
  - 02:45: las oraciones siguientes ya explican que lo acumulado es una distribución de frecuencias por columna.
  - 05:139: la oración anterior ya dice que los conteos quedan casi parejos, y 06:53–54 repite el contraste.
  - 05:436: 06:288 dice lo mismo con antítesis, y esa se conserva.
  - 05:451: además quita la repetición «concentra… concentran».
  - 06:272: el párrafo 6.7(d) ya atribuye el efecto al entrenamiento del autocodificador.

**Saldo:** de las 48 quedan 9 en mi ámbito y 17 en el de estructura. Para llegar a un tercio (16), la propuesta de estructura tendría que conservar como mucho 7 de sus 17. Muchas están en afirmaciones que esa propuesta va a moderar.

---

## Parte 3. Reglas mecánicas

**3.1. Porcentaje con espacio fino.** Todo número seguido de `\%` pasa a llevar `\,\%`.
- Hay 120 apariciones sin espacio en 89 líneas: 8 en main, 1 en 01, 6 en 04, 44 en 05, 13 en 06 y 17 en 07.
- Ya llevan espacio fino 43 apariciones en 36 líneas.
- `\%` sin número delante, como en los encabezados del tipo «Temprana (\%)», se queda como está.

**3.2. Comillas angulares.** Las comillas inglesas `` ``…'' `` pasan a «…» en UTF-8, que `T1` admite. Son 21 pares en 16 líneas: 02:247, 03:40, 03:62, 03:394, 03:412, 04:99, 04:173, 04:174, 04:177, 05:169, 05:176–177, 05:287, 05:288, 05:290, 05:291 y 06:298.

**3.3. Números en letra.**
- «Semillas» va siempre con el número en letra. Son 10 cambios:
  - «5 semillas» → «cinco semillas» en main:86, 05:20, 05:34, 05:74, 05:109, 05:128, 05:251 y 07:13;
  - «10 semillas» → «diez semillas» en 05:471 y 05:483.

  01:108 ya dice «cinco». La única excepción es 04:266–267, «(9 condiciones … $\times$ 5 semillas)», porque ahí las cifras son factores de un producto.
  - **Consolidación:** main:86 y 01:108 pierden la mención de las semillas (estructura 9.1 y 9.2, por metodología M2); 05:20, 05:74, 07:13 y 05:483 van ya en letra dentro de M2.1, M2.3, M2.9 y M1.2 de `revision_jurado_metodologia_prosa.md`.
- «2 por dominio» → «dos por dominio» en 04:183 y 05:165 (S46 y S53).
- «los 3 vecinos» → «los tres vecinos» en 03:487. (Consolidación: el «Viejo» decía «Los», con mayúscula; en 03:487 va en minúscula.)
- Dentro de una misma enumeración no se mezclan cifras y letras. En 05:364–365, «con una o 4 variantes en el directorio no hay enrutamientos falsos y con 16 hay uno;» → «con 1 o 4 variantes en el directorio no hay falsos enrutamientos, y con 16 hay uno;».
- Se quedan en cifras los conteos que se comparan con otras cifras («2 de 40», «10 por clase» junto a «unas 50») y los valores de parámetros.

**3.4. Signos y guiones.**
- «$N{=}400$» → «$N = 400$» en main:86, como en el resto del texto.
- «imagen--etiqueta» → «imagen-etiqueta» en 05:277 y 05:562.
- «etiqueta--latente» → «etiqueta-latente» en 05:461.

En español, una pareja de sustantivos se une con guion, como en «temprana-madura».

**3.5. «La hetero» y «las homo».** En prosa, tablas y pies pasan a los nombres completos:
- «la memoria heteroasociativa», o «la heteroasociativa» si ya se nombró en la misma oración;
- «la memoria homoasociativa» / «las memorias homoasociativas»;
- «homo latente» → «memoria homoasociativa latente»; «homo de etiquetas» → «memoria homoasociativa de etiquetas».

Detalles:
- Son 32 apariciones, en 05:556–626 y 07:66–70: 13 de «hetero», 17 de «homo» y 2 de «Homo».
- Encabezados de la Tabla 6 (05:626) y su pie (05:620–621): «Familiar, homo intacta» → «Familiar, homoasociativa intacta»; «Familiar, homo dañada» → «Familiar, homoasociativa dañada».
- Se quedan la etiqueta `eq:registro-hetero` y la URL del repositorio `hetero`.

**3.6. Anglicismos de una o pocas palabras (5.2).**

| Cambio | Líneas |
|---|---|
| «nativos» / «nativa» → «propios» / «propia» | 01:108, 04:268, 05:180 (título y entrada del índice), 05:235, 05:236, 05:238 |
| «alineado al lenguaje» → «alineado con el lenguaje» | 07:100 |
| «eliminaría la alineación al costo medido» → «eliminaría la alineación a costa de la pérdida medida» | 06:322–323 |
| «color sólido» / «colores sólidos» → «color liso» / «colores lisos» | 06:253, 06:262 (05:391 va en S41) |
| «Brazo» → «Configuración», en la Tabla 5 | 05:495 (absorbida en M1.3 de `revision_jurado_metodologia_prosa.md`) |
| «fastText\\subword 300D» → «fastText\\300 dimensiones», en el nodo de la Figura 1 | 03:136 |

**Glosas que se suprimen** (siete):
- (\textit{containment}), 02:241;
- (\textit{directory updating}), 03:240, en la Figura 2;
- (\textit{filling}), 04:34;
- (\textit{early accuracy}) y (\textit{mature accuracy}), 04:239–240;
- (\textit{winner share}), 04:250;
- (\textit{wall-clock}), 05:641.

Las de 04:34, 04:239–240 y 05:641 ya van en S11, S5 y S60.

**Glosas que se quedan:** las que nombran conceptos de la fuente (*missing cue problem* y los tres procesos de Wegner en 02:285–298) y la que expande una sigla (*Transactive Memory Expert*).

**3.7. Dos puntos explicativos (5.7).**

**Criterio:**
- Los dos puntos se quedan cuando introducen una enumeración, una ecuación, una definición en una lista o una leyenda de pie («Arriba:», «Nombra:»), y en los títulos.
- Se cambian cuando unen dos oraciones y la segunda explica la primera. Pasan entonces a punto, «porque», «así que», «de modo que» o punto y coma.

**Conteo.** En la prosa (sin TikZ ni matemáticas) hay 233 «: »:
- 37 se quitan, en neto, en los puntos de la Parte 2;
- 41 se quitan con la lista de abajo;
- 49 están en pasajes de la propuesta de estructura (Parte 4, punto 7);
- los 106 restantes se quedan. Son de enumeración, ecuación, definición en lista, leyenda o título, más unos pocos de definición con énfasis (02:63, 02:85, 02:239, 04:68 y 04:150).

En mi ámbito, los dos puntos explicativos bajan de unos 80 a casi ninguno. Cuántos queden en total depende de lo que conserve la propuesta de estructura.

**Lista de 41 cambios** (fragmento viejo → nuevo):

| Línea | Viejo | Nuevo |
|---|---|---|
| 01:26 | «como conteos de frecuencia: aceptan una entrada» | «como conteos de frecuencia. Aceptan una entrada» |
| 01:51 | «el TME deja de hacer falta: en la fase madura» | «el TME deja de hacer falta, y en la fase madura» |
| 01:92 | «como módulo de entrada o como ganador: cada módulo sabe» | «como módulo de entrada o como ganador. Así, cada módulo sabe» (absorbida en estructura 9.2) |
| 02:15 | «el registro es \emph{booleano}: la memoria almacena» | «el registro es \emph{booleano}; la memoria almacena» |
| 02:21 | «\cite{pineda2023imagery,hernandez2026cifar}: la memoria» | «\cite{pineda2023imagery,hernandez2026cifar}. En ella, la memoria» |
| 02:82 | «no cambia: la poda quita los valores» | «no cambia, porque la poda quita los valores» |
| 02:109 | «controla la dispersión del muestreo: $\sigma = 0$ concentra» | «controla la dispersión del muestreo. Con $\sigma = 0$ se concentra» |
| 02:124 | «La entropía resume el estado de la memoria: una memoria con entropía alta» | «La entropía resume el estado de la memoria. Una memoria con entropía alta» |
| 02:164 | «\cite{morales2025missing}: cuando la pista fuente selecciona» | «\cite{morales2025missing}. Cuando la pista fuente selecciona» |
| 02:202 | «es el valor indefinido, el borde: lo que llega sin pareja» | «es el valor indefinido, el borde. Lo que llega sin pareja» |
| 02:241 | «Esto implementa una \emph{contención} estricta (\textit{containment}): la proyección» | «Esto implementa una \emph{contención} estricta, porque la proyección» |
| 02:245 | «se ha registrado en la memoria: las características muy frecuentes» | «se ha registrado en la memoria, de modo que las características muy frecuentes» |
| 02:249 | «que este sistema incorpora sin modificaciones: la anulación conjuntiva» | «que este sistema incorpora sin modificaciones. La anulación conjuntiva» |
| 02:264 | «este trabajo lo aplica a la proyección: compara la activación media» | «este trabajo lo aplica a la proyección y compara la activación media» |
| 03:60 | «$\mathbf{g} \in \{0,1\}^{8}$: una coordenada binaria por módulo» | «$\mathbf{g} \in \{0,1\}^{8}$, que tiene una coordenada binaria por módulo» |
| 03:78 | «\emph{perspectivales}: cada módulo sabe de los demás» | «\emph{perspectivales}, porque cada módulo sabe de los demás» |
| 03:186 | «(Sección~\ref{sec:dataset}): 3200 registros por clase.» | «(Sección~\ref{sec:dataset}), en total 3200 registros por clase.» |
| 03:377 | «s_k$: la suma recorre las» | «s_k$; la suma recorre las» (absorbida en estructura 1.4) |
| 03:403 | «masas desiguales entre módulos: al final del protocolo» | «masas desiguales entre módulos. Al final del protocolo» |
| 03:411 | «pero no agrega información: es el» | «pero no agrega información, porque es el» |
| 04:18 | «desde 41 puntos de vista: 410» | «desde 41 puntos de vista, en total 410» |
| 04:20–21 | «82 de prueba: ninguna imagen» | «82 de prueba. Ninguna imagen» |
| 04:28 | «(Sección~\ref{sec:objetos-nuevos}): en cada pliegue» | «(Sección~\ref{sec:objetos-nuevos}); en cada pliegue» |
| 04:117 | «filtro de pertenencia léxica: una vez obtenida la pista» | «filtro de pertenencia léxica. Una vez obtenida la pista» |
| 04:139 | «No hay partición de validación separada: el punto de control» | «No hay partición de validación separada, y el punto de control» |
| 04:140 | «(una evaluación cada 10 épocas: cinco candidatos)» | «(una evaluación cada 10 épocas, es decir, cinco candidatos)» |
| 04:211 | «Los pesos solo cambian magnitudes: la contención» | «Los pesos solo cambian magnitudes; la contención» |
| 04:242 | «no hay umbral sobre la puntuación: se rechaza lo que» | «no hay umbral sobre la puntuación; se rechaza lo que» |
| 05:37 | «F coincide con A: el vocabulario por masa asociativa» | «F coincide con A porque el vocabulario por masa asociativa» |
| 05:118 | «se lleva el 20.5\%: es el sesgo de lectura» | «se lleva el 20.5\,\%; ese es el sesgo de lectura» |
| 05:137 | «($\log_2 8 = 3$ bits): los conteos quedan» | «($\log_2 8 = 3$ bits), así que los conteos quedan» (absorbida en estructura 5.4) |
| 05:199 | «el valor no cambia con $\kappa$: la poda sube» | «el valor no cambia con $\kappa$, porque la poda sube» |
| 05:230 | «$\kappa$ no actúa en este rango: la poda concentra» | «$\kappa$ no actúa en este rango, porque la poda concentra» |
| 05:359 | «sobre las 656 imágenes de prueba: registrar en el directorio» | «sobre las 656 imágenes de prueba. Registrar en el directorio» |
| 05:440 | «de diez pliegues: en cada pliegue, el contenido y la fase A» | «de diez pliegues. En cada pliegue, el contenido y el directorio visual» (absorbida en M4.1 de `revision_jurado_metodologia_prosa.md`) |
| 05:543 | «se equivoca más de dominio: con 200 imágenes por» | «se equivoca más de dominio. Con 200 imágenes por» (absorbida en M1.5 de `revision_jurado_metodologia_prosa.md`) |
| 05:609 | «es lo primero que se pierde: una celda de la homo» | «es lo primero que se pierde, porque una celda de la memoria homoasociativa» |
| 06:202 | «ocho veces las celdas de memoria: una heteroasociativa por módulo en lugar de una.» | «ocho veces las celdas de memoria, porque hay una heteroasociativa por módulo en lugar de una sola.» (absorbida en M1.4 de `revision_jurado_metodologia_prosa.md`) |
| 06:210 | «llega a algún módulo: la sonda de rechazo» | «llega a algún módulo. La sonda de rechazo» (absorbida en M5.3 de `revision_jurado_metodologia_prosa.md`) |
| 06:229 | «es estricta ($\xi = 0$): con directorios perspectivales,» | «es estricta ($\xi = 0$), porque con directorios perspectivales» |
| 06:252–253 | «Densificar agranda esa fuga: en el experimento 13, con 16 variantes, a la sonda de color sólido la aceptan» | «Densificar agranda esa fuga. En el experimento 13, con 16 variantes, a la sonda de color liso la aceptan» |

**3.8. Términos de la Parte 1 que son sustitución simple.** Se aplican tal como dice la tabla 1.1. Los conteos incluyen las apariciones que ya resuelve algún punto de la Parte 2.
- «fidelidad» en el sentido de concordancia: 8 apariciones. Fuera de S9 y S10 quedan tres sustituciones simples: 05:44, 05:158 y 07:15.
- «fase A» y «fase B»: 12 apariciones en 11 líneas. Fuera de S11, S12 y la lista 3.7 quedan cinco:
  - 03:429: «(fase A, Sección~\ref{sec:dataset})» → «(Sección~\ref{sec:dataset})», porque la frase ya dice «formación del directorio visual»;
  - 04:163: «de la fase A» → «de la formación visual»;
  - 05:363: «el rechazo de la fase A» → «el rechazo en la formación visual»;
  - 06:13: «de percepciones de la fase A» → «de percepciones de la formación visual»;
  - 06:266: «una percepción de la fase A» → «una percepción de la formación visual».
- Las demás sustituciones simples, con su número de apariciones:

| Sustitución | Apariciones |
|---|---|
| «condiciones de lectura» | 3 |
| «lectura B1» | 20 |
| «maquinaria» | 5 |
| «enrutamientos falsos» / «enrutamientos equivocados» | 3 |
| $M^L_{\mathrm{dir}}$ / $M^R_{\mathrm{dir}}$ | 18 |
| $N$ → $I$ | 10 |
| «nativos» / «nativa» | 6 |

---

## Parte 4. Para la propuesta de estructura

Aquí van las frases que piden un cambio de contenido o que están en pasajes que esa propuesta reescribe. No las reescribo. Dejo dicho qué decidí en términos, para que las dos propuestas no se contradigan.

**Consolidación, punto por punto:**
- Resueltos en los textos combinados: 1 (estructura 9.4), 2 (estructura 9.2 y 7.4), 3 (estructura 9.1), 4 (estructura 9.1 y 4.4), 5 (estructura 7.1 y 7.8), 8 (estructura 6.1), 10 (estructura 5.4, corregido a «el 99.1 y el 99.2 %»), 11 (metodología M1.2, M1.3, M1.5, M1.7 y M5.2; estructura 9.2), 12 (metodología M1.4), 15 (estructura 2.4, 7.6 y 9.2) y 16 (estructura 2.1).
- En parte: 6 y 7. Las antítesis y los dos puntos de los pasajes combinados ya siguen 3.7; los demás pasajes de estructura piden una pasada de forma al aplicar (índice).
- Quedan para el autor: 9 (si exp10 y exp15 se volvieron a correr), 13, 14 («hemisferio»), 17, 18, 19, 20 y 21 (índice, decisiones).

1. **07:81–83, «Y la fidelidad del procesamiento es un resultado en sí mismo…».** C1 y 5.6 piden suprimirla, y es la misma afirmación que E7 saca de las contribuciones. Si se conserva en alguna forma, debe decir «trazabilidad», no «fidelidad».
2. **01:98–104 y 04:215–230 (auditoría).** La contribución 4 depende de E7; si se queda, se titula «Auditoría de trazabilidad» (S1). Quedan por decidir tres cosas de contenido:
   - «vectores sintéticos (de relleno, para etiquetas sin vector fastText)» es huella de una versión que los tenía (5.1);
   - «datos no fabricados» y «ningún número se apoya en datos fabricados» caen en 5.6;
   - «Ninguna decisión proviene de mecanismos ajenos a las memorias» cae en 5.6 y en M3: la suma, B1, $\tau$ y el rescate quedan fuera de las memorias.
3. **main:85–104 (resumen).** Usé «lectura normalizada por conteo» (S6) y expandí EAM-TMS (S43). Si E1 y E7 reescriben el resumen, esos dos cambios deben conservarse.
4. **main:74 y 06:82, «mecanismos de Wegner».**
   - La decisión de término es «procesos», como en 01:15 y 02:281.
   - Las dos frases están en E1 y M2: main:74–76 trata la asignación de información, y 06:81–83 cita la obra de 1987 para los tres procesos.
   - En 06:82, «releen» (5.5) debería pasar a «interpretan» cuando se reescriba.
5. **06:5–12 y 07:106–110, «la maquinaria transactiva funciona…; la representación es el límite».** Cambié «maquinaria» por «mecanismo transactivo» (S63 y tabla 1.1). La afirmación cae en 5.6, M7 y M10, así que le toca a estructura. En 06:8–12 se repite «funciona… funcionan» (5.7), y la reescritura debería quitarlo.
6. **Antítesis en pasajes de estructura (17):** main:102, 01:12–13, 02:108, 02:126, 02:314, 04:81–82, 05:262, 05:269, 06:43, 06:92, 06:129, 06:152, 06:170, 06:182, 06:214, 07:78 y 07:109–110. Para llegar a un tercio del total (16 de 48), conviene conservar como mucho 7. Algunas ya caen con otros puntos:
   - E4: el título repetido de 05:262 y 06:92;
   - M5: 05:269, «por construcción»;
   - M6: 02:126, 02:314 y 07:78;
   - M10: main:102 y 07:109.
7. **Dos puntos en pasajes de estructura (49), que no toqué:**
   - main:58 y main:74;
   - 01:7, 01:12, 01:56 y 01:99;
   - 02:126, 02:130, 02:278, 02:288, 02:306, 02:310, 02:314 y 02:320;
   - 03:83 y 03:426;
   - 04:81, 04:162, 04:178 y 04:221;
   - 05:263 y 05:265;
   - 06:8, 06:21, 06:43, 06:52, 06:64, 06:93, 06:106, 06:118, 06:126–170 (ocho en las analogías), 06:178, 06:183, 06:186, 06:221, 06:234, 06:255 y 06:282;
   - 07:49, 07:74, 07:78 y 07:81.

   La reescritura de esos pasajes debería seguir el criterio de 3.7.
8. **06:152–153, «muestra… como Plaut mostró».** Es una repetición cercana (5.7) dentro de las analogías, que quedan fuera de mi alcance. Basta con «como encontró Plaut».
9. **05:579, «Todas las cifras de este documento son las de una sola memoria de contenido».** La suprimo por 5.1 (S48). Además, el dictamen de metodología señala que los experimentos 10 y 15 no se volvieron a correr con una sola memoria, así que la frase tampoco es cierta. La propuesta de estructura decide cómo declararlo, por ejemplo en E8 o en la nota de los experimentos.
10. **05:136–137, «2.974 bits en la condición A y de 2.977 en G, el 99.1 % del máximo».** El 99.1 % solo vale para A: 2.974/3 = 99.13 %, mientras que 2.977/3 = 99.23 %. Hay que corregir la cifra («el 99.1 y el 99.2 % del máximo»), y eso es un cambio de contenido.
11. **Distancia del experimento 11 (05:472–473 y Tabla 5).** 05:473 dice que la distancia se mide a la instancia real más cercana, sea de la clase que sea («y por la distancia a ella»). El código mide la distancia a la instancia más cercana de la clase de la consulta: `d_nn_truth` = `d_nn_target`, en `run_experiment11_monolithic.py:434` y `:600`, y en `run_experiment9_member_loss.py:246`. Las dos distancias coinciden cuando el juez 1-NN acierta, pero no en general. En S51 solo agregué la unidad.
12. **06:189–193, «La exactitud de clase también mejora, pero poco».** Cambié «exactitud» por «acierto». El dictamen de metodología (M1) muestra que sobre las 171 consultas la clase correcta empata, así que la frase quizá deba salir. Si se queda, debe decir «acierto».
13. **05:601–604, lesión.** Reescribí «mientras queda algo que nombrar» porque contradecía su propio ejemplo (S49). Si el autor quería decir otra cosa, le toca precisarlo.
14. **«Hemisferio visual / textual».** El dictamen de Wegner sugiere «vía» o «rama». No lo toqué, para que se decida una sola vez.
15. **07:49–52 y 04:176–178, «comunicación distintiva» y «las señas del dominio» atribuidas a Wegner (M2).** Solo corregí el paréntesis de 07:51–52 (S50). En 01:94–96 («es la coordinación de recuperación de Wegner») solo cambié «los módulos que conoce» (S22).
16. **02:276, «metadirectorio» (C10).** Debería pasar a «directorio», pero la frase está en el párrafo de Wegner que reescribe la propuesta de estructura. El dictamen de Wegner, en sus observaciones menores, dice que el término no aparece en Wegner. Conviene que la reescritura no lo conserve.
17. **02:108, «\emph{recordar es muestrear}, no leer un valor fijo».** Es antítesis y lema a la vez. El dictamen de Wegner pide atribuirlo o apoyarlo en una fuente, así que no lo toqué.
18. **«La binarización por signo usaría 2» (01:85, 04:81–82 y 06:19; E4).** Se repite tres veces y nunca se midió. No lo toqué.
19. **Números de experimento y rutas `results/...` (E8).** Mis puntos dejan «experimento 10, 13, 14, 15 y 16» como están, y no tocan la nota de 04:156–160 ni las rutas de 05:478 y 05:650.
20. **El 94.5 frente al 95.5 % (S33).** La frase nueva dice que el experimento 13 mide «con sus propios modelos». El dictamen de metodología agrega que su llenado difiere del oficial en 30–58 mil celdas por clase. Si la propuesta de estructura cita esa diferencia, la frase de S33 puede incorporarla.
21. **05:320–322, «coherente con la acumulación de variedad».** La frase interpreta el crecimiento de la entropía como acumulación de variedad. Pero la columna «Variedad $L_1$» de la misma tabla, que mide la variedad entre recuperaciones, no crece hasta $I = 200$: 1.90, 1.86, 1.74 y 1.91, y luego 2.18. En S38 dejé la interpretación como está y solo agregué la lectura de la columna. El autor decide si se mantiene, se precisa («variedad de lo registrado») o sale.
