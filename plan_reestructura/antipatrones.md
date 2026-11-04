# Antipatrones de estructura (texto que suena a máquina)

Revisión de `main.tex` y `secciones/01` a `07` del `.tex8` (2370 líneas leídas enteras). Solo estructura; el vocabulario suelto lo ve otro revisor. No se cambia ninguna cifra ni ningún sentido. Las propuestas sobre texto que `revision_replanteamiento_prosa.md` ya reescribe van marcadas **«en la propuesta de replanteamiento»** y se refieren al texto nuevo de esa propuesta. La sección «Costo computacional» (`05:518–567`) no se revisó.

Ningún hallazgo es de severidad alta (no hay errores de hecho en este foco). Hay 10 de severidad media (claridad o repetición) y el resto es de estilo.

## 1. Conteos por patrón y archivo

«Ocurr.» cuenta todos los casos del patrón; «cambiar» los que conviene tocar (los demás son legítimos: tríadas de tres cosas reales, contrastes informativos, títulos de estructura).

| Patrón | main | 01 | 02 | 03 | 04 | 05 | 06 | 07 | Ocurr. | Cambiar |
|---|---|---|---|---|---|---|---|---|---|---|
| (a) Tríadas por reflejo | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 3 | 2 |
| (b) «no X, sino Y» / «X, no Y» | 1 | 0 | 6 | 5 | 6 | 14 | 17 | 2 | 51 | 20 |
| (c) Anuncio con dos puntos («La idea central es esta:») | 0 | 0 | 4 | 0 | 4 | 1 | 8 | 2 | 19 | 18 |
| (d) Cierre con moraleja o repetición | 0 | 0 | 2 | 3 | 4 | 8 | 6 | 2 | 25 | 25 |
| (e) `\paragraph{}` (total) | 0 | 0 | 0 | 3 | 4 | 21 | 9 | 6 | 43 | 17 |
| (e') Cifras o frases en `\textbf{}` dentro de la prosa | 1 | 3 | 0 | 0 | 1 | 14 | 0 | 8 | 27 | 27 |
| (f) Paralelismo repetido (Primero/Segundo/Tercero, series) | 0 | 1 | 0 | 0 | 0 | 1 | 2 | 1 | 5 | 4 |
| (g) Cadenas de «:», «;» y paréntesis en una oración | 0 | 0 | 2 | 1 | 3 | 4 | 6 | 1 | 17 | 14 |
| (h) Rayas de pausa / paréntesis apilados | 0 | 0 | 0 | 1 | 2 | 1 | 3 | 0 | 7 | 7 |
| (i) Absolutos sin cifra («perfecto», «exactamente», «limpia», «honesto») | 1 | 0 | 3 | 1 | 0 | 7 | 7 | 2 | 21 | 19 |
| (j) Misma idea repetida entre secciones (clústeres que tocan el archivo) | 3 | 5 | 2 | 5 | 7 | 11 | 13 | 4 | 16 clústeres | 16 |
| (k) Preguntas retóricas | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| (l) Párrafo de cifras paralelas donde cabe una tabla | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 0 | 3 | 3 |
| (m) Cierres grandilocuentes | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 1 | 4 | 4 |
| (n) Sobreexplicación (decir lo mismo dos veces seguidas) | 0 | 0 | 2 | 4 | 2 | 1 | 0 | 0 | 9 | 9 |
| (o) Metatexto («Esta sección describe», «Conviene precisar», «Nótese») | 0 | 1 | 6 | 2 | 4 | 2 | 2 | 0 | 17 | 17 |
| (p) Personificación que se puede leer literal | 0 | 0 | 1 | 1 | 1 | 2 | 0 | 0 | 5 | 4 |

Notas sobre los conteos:

- **Los patrones que más delatan el texto son (b), (d), (o) y (e).** El contraste «X, no Y» aparece 51 veces (una cada 46 líneas); en `05` y `06` cierra párrafo tras párrafo. El metatexto de apertura («Conviene precisar», «Una precisión de notación», «Cabe señalar», «Nótese») aparece 11 veces solo en `02` y `04`. En `05`, 21 `\paragraph{}` en 567 líneas: casi cada párrafo lleva titulito, y siete son eslóganes del hallazgo.
- (k): la única pregunta es la de investigación (`01:31–36`), que no es retórica. Nada que cambiar.
- (h): solo hay una raya de prosa (`04:98`). El problema de (h) aquí son los paréntesis, no las rayas.
- (i): las fórmulas «en todo el rango» (5 veces) van siempre con cifra; no se cuentan.
- `\paragraph{}` de `04` (cuatro etapas del pipeline), `07` (estructura de conclusiones) y las limitaciones (a)–(i) de `06` son de estructura y se quedan.

## 2. Repeticiones entre archivos (patrón j)

Dieciséis ideas aparecen con las mismas palabras en varias secciones. Aquí dónde se queda cada una y dónde se quita; los textos nuevos están en la sección 3.

| # | Idea | Dónde aparece | Propuesta |
|---|---|---|---|
| j1 | «los límites están en las representaciones, no en el mecanismo asociativo» | `main:83–85`, `01:34–35`, `06:15–22`, `07:34–39`, `07:60–61`, `07:89–90` (la propuesta de replanteamiento conserva cinco) | Se queda en resumen, pregunta y «Respuesta». Se quita de «Lecciones. Primero» y se acorta en el cierre (`07`). |
| j2 | Lista «directorios, lectura B1, rechazo por containment, actualización del directorio y coordinación punto a punto» | `01:76–77`, `06:10–12`, `07:31–33` (la propuesta la conserva en los tres) | Se queda en `06` y `07`; en la contribución 1 de `01` se resume. |
| j3 | Los tres procesos de Wegner, con nombre y definición | `main:72–74`, `01:16–22`, `02:271–295` | `02` es el tratamiento; `01` se reduce a una frase con remisión. |
| j4 | Por qué el directorio visual es propio y no un puente | `01:95–97`, `03:86–89` | Se queda en `03`; se quita de `01`. |
| j5 | «sin tocar la maquinaria / las memorias» | `01:84`, `04:40`, `06:22`, `07:61` | Se queda en `01` y `06`; `04` y `07` ya lo dicen de otro modo en las propuestas de abajo. |
| j6 | «no hay filtro léxico; la memoria decide» | `04:109–117`, `05:129–131`, `05:157–158`, `05:342–348`, `05:370` | Se queda en `04` (una vez) y en el pie de la figura 15; se quita de `05:129–131`, `05:158`, `05:348`. |
| j7 | «evidencia total → evidencia por registro» y «G supera a B1 por medio punto, dentro del ruido» | `03:458–459`, `05:56–58`, `06:45–46`, `06:54–56` | Se queda en `03` y `05`; se quita `06:54–56`. |
| j8 | Entropía 2.974: «sesgo de lectura, no de estructura» | `05:113–116`, `06:51–53` | Se queda la interpretación en `06`; en `05` solo la cifra. |
| j9 | «el orden afecta la velocidad, no el destino» | `05:240–246`, `06:108–112` | Se queda en `05`; `06` remite. |
| j10 | «10 consultas por clase no bastan; con el banco completo, 93.0 %» | `05:142–145`, `05:231–238`, `06:100–106` | Se queda `05:231–238` y `06`; se quita `05:142–145`. |
| j11 | Por qué $\xi = 0$ en el directorio visual | `03:484–489`, `04:191–195`, `05:324–329`, `06:233–235` | Se queda en `03` (definición) y `05` (experimento 10); `04` y `06` remiten. |
| j12 | Umbral de energía $\tau$: 16.61, 18.45, 10 %, 1 de 1024, 4 de 656 | `03:491–498`, `04:148–157`, `05:349–359`, `06:248–270` (en `06` el costo se dice dos veces: 258–260 y 267–270) | Se queda en `04` (método) y `05` (resultado); `03` conserva solo la regla; `06` conserva la mitigación medida (137 de 152) y dice el costo una vez. |
| j13 | Partición a nivel de imagen, diez objetos a ambos lados | `04:16–25`, `06:288–294` | Se queda en `04`; la limitación (e) remite. |
| j14 | Rescate léxico: 46 consultas, 43/46 contra 33/46, +21.7 | `04:96–106`, `06:324–332` | Se queda la cifra en las dos (una es el método, otra la limitación), pero `04` pierde la justificación de estatus, que es la de (g). |
| j15 | Selección del encoder sobre test | `04:135–141`, `06:312–322` | `04` lo dice en una frase y remite a (f). |
| j16 | Experimento 13: 73.6→96.2, 76→96, 66.5→94.5 | `05:329–334`, `06:236–243` | Se queda en `05`; `06` conserva solo 66.5→94.5 con remisión. |

Otras dos repeticiones menores: los dos falsos enrutamientos de `horse7` se cuentan cinco veces (`05:321–322`, `06:13–14`, `06:130–131`, `06:243–245`, `07:19–20`; sobra en `06:130–131`), y la lista de 15 variantes de augmentación está entera en `03:176–179` (pie de figura) y en `04:36–39`.

## 3. Cambios propuestos por archivo

Dentro de cada archivo, primero los de severidad media y luego los de estilo (baja).

### main.tex

- **Dónde:** `main.tex:61` (en la propuesta de replanteamiento, línea 23 del texto nuevo)
- **Texto actual:** `El sistema tiene \textbf{ocho módulos especialistas}, uno por cada categoría del conjunto`
- **Problema:** (e') negrita de énfasis dentro del resumen; el resumen no lleva negritas.
- **Propuesta:** `El sistema tiene ocho módulos especialistas, uno por cada categoría del conjunto`
- **Fuente:** no aplica.
- **Severidad:** baja.

- **Dónde:** `main.tex:83–85` (en la propuesta, líneas 49–50)
- **Texto actual:** `Los límites observados provienen de las representaciones (el léxico compartido entre clases y la separabilidad del espacio latente), no del mecanismo asociativo.`
- **Problema:** (j1) es la primera de cinco apariciones de la misma frase. Aquí se queda; el cambio está en `07` (abajo).
- **Propuesta:** sin cambio.
- **Severidad:** baja.

### 01_introduccion.tex

- **Dónde:** `01:16–24`
- **Texto actual:**
  ```latex
  El modelo de Wegner identifica tres procesos principales.
  Primero, la \emph{actualización del directorio}: tras cada interacción, los
  miembros que la presenciaron registran quién supo responder.
  Segundo, la \emph{asignación de información}: la información nueva se envía
  hacia el miembro reconocido como referencia en ese dominio.
  Tercero, la \emph{coordinación de recuperación}: las consultas futuras viajan directamente
  a ese referente sin pasar por un intermediario.
  La transición de una \emph{fase temprana} mediada a una \emph{fase madura} punto a punto
  es la señal de que el sistema transactivo ya quedó formado.
  ```
- **Problema:** (f)+(j3) «Primero: / Segundo: / Tercero:» con la misma estructura, y los tres procesos se vuelven a definir enteros en `02:271–295`.
- **Propuesta:**
  ```latex
  El modelo de Wegner distingue tres procesos, que la Sección~\ref{sec:tmt} detalla:
  la actualización del directorio (quien presenció una interacción registra quién supo
  responder), la asignación de información (lo nuevo va al miembro reconocido en ese
  dominio) y la coordinación de la recuperación (las consultas viajan a ese referente
  sin intermediario).
  Cuando el grupo pasa de una fase temprana mediada a una fase madura punto a punto, el
  sistema transactivo está formado.
  ```
- **Fuente:** no aplica.
- **Severidad:** baja.

- **Dónde:** `01:38–42` y `01:56`
- **Texto actual:** `\textbf{EAM-TMS}`, `\textbf{ocho módulos especialistas}`, `\textbf{Memorias Asociativas Entrópicas}`
- **Problema:** (e') negritas de énfasis en prosa corrida.
- **Propuesta:** conservar solo `\textbf{EAM-TMS}` (es el nombre que se define); quitar las otras dos negritas.
- **Severidad:** baja.

- **Dónde:** `01:95–97` (contribución 3)
- **Texto actual:**
  ```latex
      El directorio visual es propio porque un puente por la memoria de contenido del
      módulo de entrada hacia el directorio de texto no redirige cuando ese módulo no es
      el especialista: su memoria de contenido no contiene el latente ajeno.
  ```
- **Problema:** (j4) la misma justificación, con las mismas palabras, está en `03:86–89`; una lista de contribuciones no carga mecanismo.
- **Propuesta:** quitar (las tres líneas).
- **Severidad:** baja.

- **Dónde:** `01:76–78` (en la propuesta de replanteamiento, contribución 1, líneas 95–97 del texto nuevo)
- **Texto actual (propuesta):** `Los directorios, la lectura normalizada B1, el rechazo por containment y la coordinación punto a punto funcionan con los ocho dominios, con el registro por transacción y la coordinación de la contribución~3.`
- **Problema:** (j2) la lista de componentes vuelve igual en `06:10–12` y `07:31–33`.
- **Propuesta:** `La maquinaria transactiva (Sección~\ref{sec:arquitectura}) funciona con los ocho dominios sin ajustes por dominio.`
- **Severidad:** baja.

- **Dónde:** `01:124–127`
- **Texto actual:**
  ```latex
  La Sección~\ref{sec:metodologia} detalla la metodología experimental.
  La Sección~\ref{sec:resultados} reporta los resultados.
  La Sección~\ref{sec:discusion} discute los resultados.
  La Sección~\ref{sec:conclusiones} concluye y señala trabajo futuro.
  ```
- **Problema:** (o)+(f) cuatro frases idénticas de metatexto.
- **Propuesta:**
  ```latex
  Las Secciones~\ref{sec:metodologia} a~\ref{sec:conclusiones} presentan la metodología,
  los resultados, la discusión y las conclusiones con el trabajo futuro.
  ```
- **Severidad:** baja.

### 02_marco_teorico.tex

- **Dónde:** `02:24–25`
- **Texto actual:** `Esta distinción importa para el lector que verifique contra las fuentes: las definiciones que siguen corresponden a la variante ponderada, no a la booleana de 2021.`
- **Problema:** (o) apóstrofe al lector antes del dato.
- **Propuesta:** `Las definiciones que siguen corresponden a la variante ponderada, no a la booleana de 2021.`
- **Severidad:** baja.

- **Dónde:** `02:43–44`
- **Texto actual:** `La idea central es esta: la memoria \emph{no almacena patrones individuales} sino que acumula una \textbf{distribución de experiencias}.`
- **Problema:** (c)+(b) anuncio con dos puntos y «no X sino Y» con doble énfasis.
- **Propuesta:** `La memoria no almacena patrones individuales: acumula una distribución de experiencias.`
- **Severidad:** baja.

- **Dónde:** `02:69–76`
- **Texto actual:**
  ```latex
  Una precisión de notación: en las definiciones formales de las fuentes, $\eta$ devuelve
  un \emph{booleano} (aceptar/rechazar), y los $w_i$ son cantidades intermedias calculadas
  durante la prueba de aceptación.
  La implementación de referencia de Pineda \& Morales sí los expone como valor de
  retorno de primera clase (\texttt{recog\_weights}), y este trabajo los usa de esa
  manera: ponderan la proyección de la memoria heteroasociativa
  (véase la Sección~\ref{sec:hetero4d}).
  Es una diferencia de empaquetado, no de sustancia.
  ```
- **Problema:** (o) «Una precisión de notación:», (d)+(b) cierre con moraleja «de empaquetado, no de sustancia».
- **Propuesta:**
  ```latex
  En las definiciones formales de las fuentes, $\eta$ devuelve un booleano
  (aceptar/rechazar) y los $w_i$ son cantidades intermedias de la prueba de aceptación.
  La implementación de referencia de Pineda \& Morales los expone como valor de retorno
  (\texttt{recog\_weights}), y este trabajo los usa así: ponderan la proyección de la
  memoria heteroasociativa (Sección~\ref{sec:hetero4d}).
  ```
- **Severidad:** baja.

- **Dónde:** `02:81–87`
- **Texto actual:**
  ```latex
  La heteroasociativa de referencia define el criterio solo para un par de pistas; con
  una sola pista, este trabajo lo aplica a la proyección (Sección~\ref{sec:hetero4d}):
  compara la activación media por celda de $\Pi$, por coordenada de la pista, con
  $\kappa \cdot \bar{\mu}$ de la memoria de contenido.
  Ese es el $\kappa$ que barre la Sección~\ref{sec:param-iota-kappa}; el criterio
  homoasociativo no interviene: de las lecturas de dominio de la memoria de contenido
  (ecuación~\eqref{eq:marginal}) el sistema usa los pesos y no esa decisión.
  ```
- **Problema:** (g) dos oraciones seguidas con «;», paréntesis y «:» encadenados.
- **Propuesta:**
  ```latex
  La heteroasociativa de referencia define el criterio solo para un par de pistas.
  Con una sola pista, este trabajo lo aplica a la proyección (Sección~\ref{sec:hetero4d}):
  compara la activación media por celda de $\Pi$, por coordenada de la pista, con
  $\kappa \cdot \bar{\mu}$ de la memoria de contenido.
  Ese es el $\kappa$ que barre la Sección~\ref{sec:param-iota-kappa}.
  El criterio homoasociativo no interviene: de las lecturas de dominio de la memoria de
  contenido (ecuación~\eqref{eq:marginal}) el sistema usa los pesos, no esa decisión.
  ```
- **Severidad:** baja.

- **Dónde:** `02:110–113`
- **Texto actual:**
  ```latex
  Esta variación no es un error del modelo; es parte de cómo recuerda:
  \emph{recordar es muestrear}, no leer un valor determinista.
  Diferentes ejecuciones de $\beta$ sobre la misma pista y la misma memoria pueden producir
  resultados distintos.
  ```
- **Problema:** (b)+(g)+(d) «no es X; es Y: Z, no W» antes del hecho, y eslogan en cursiva.
- **Propuesta:**
  ```latex
  Dos ejecuciones de $\beta$ sobre la misma pista y la misma memoria pueden dar
  resultados distintos: la recuperación es un muestreo, no una lectura determinista.
  ```
- **Severidad:** baja.

- **Dónde:** `02:128–131`
- **Texto actual:**
  ```latex
  Conviene precisar que la entropía baja \emph{no} es intrínsecamente patológica: en las
  fuentes, una función totalmente determinada tiene entropía exactamente cero y es una
  memoria perfectamente bien formada, solo que rígida y reproductiva
  \cite{pineda2021entropic,morales2022manuscript}.
  ```
- **Problema:** (o) «Conviene precisar», (i) «exactamente cero», «perfectamente bien formada».
- **Propuesta:**
  ```latex
  La entropía baja no es patológica: en las fuentes, una función totalmente determinada
  tiene entropía cero y es una memoria bien formada, solo que rígida y reproductiva
  \cite{pineda2021entropic,morales2022manuscript}.
  ```
- **Severidad:** baja.

- **Dónde:** `02:132–134`
- **Texto actual:** `un directorio que debe señalar sin ambigüedad a un especialista \emph{quiere} baja ambigüedad, mientras que una memoria de contenido que debe generalizar quiere un rango medio.`
- **Problema:** (p) «quiere» en cursiva, dos veces, para una memoria.
- **Propuesta:** `un directorio que debe señalar sin ambigüedad a un especialista necesita entropía baja, y una memoria de contenido que debe generalizar, un rango medio.`
- **Severidad:** baja.

- **Dónde:** `02:167–170`
- **Texto actual:**
  ```latex
  Conviene ubicarlo con precisión: la proyección ponderada que se describe a continuación
  es el mecanismo \emph{general} de recuperación cuando sí existe una pista fuente con
  pesos; las soluciones a la pista faltante son el parche para el caso específico en que
  ni siquiera esa información existe.
  ```
- **Problema:** (o)+(g).
- **Propuesta:**
  ```latex
  La proyección ponderada que sigue es el mecanismo general de recuperación cuando existe
  una pista fuente con pesos; los métodos para la pista faltante cubren el caso en que no
  existe.
  ```
- **Severidad:** baja.

- **Dónde:** `02:203–206`
- **Texto actual:**
  ```latex
  La condición de anulación es la \textbf{conjunción AND}: una celda del resultado se
  anula si \emph{cualquiera} de las $n$ evidencias aporta cero.
  Esto implementa \emph{containment} estricto: la proyección solo produce masa donde
  todas las características de la pista tienen soporte simultáneo en la memoria.
  ```
- **Problema:** (n) dos frases con la misma información, cada una con su anuncio.
- **Propuesta:**
  ```latex
  La anulación es una conjunción: una celda del resultado se anula si cualquiera de las
  $n$ evidencias aporta cero, de modo que la proyección solo produce masa donde todas las
  características de la pista tienen soporte (\emph{containment} estricto).
  ```
- **Severidad:** baja.

- **Dónde:** `02:210–215`
- **Texto actual:**
  ```latex
  Sobre la atribución de esta regla: el nombre ``proyección AND-ponderada'' es de este
  trabajo, pero el mecanismo no es una síntesis propia; es exactamente la operación
  \texttt{project()} de la implementación de referencia de Pineda \& Morales (que este
  sistema incorpora sin modificaciones), donde la anulación conjuntiva y la suma ponderada
  por pesos normalizados son líneas literales de esa única función, operando sobre la
  relación ya podada por $\iota$.
  ```
- **Problema:** (o)+(b)+(i) «Sobre la atribución:», «no es una síntesis propia; es exactamente», «líneas literales de esa única función».
- **Propuesta:**
  ```latex
  El nombre ``proyección AND-ponderada'' es de este trabajo; el mecanismo es la operación
  \texttt{project()} de la implementación de referencia de Pineda \& Morales, que este
  sistema incorpora sin modificaciones: la anulación conjuntiva y la suma ponderada por
  pesos normalizados son líneas de esa función, sobre la relación ya podada por $\iota$.
  ```
- **Severidad:** baja.

- **Dónde:** `02:267–269`
- **Texto actual:** `Cabe señalar que este puente entre la teoría de Wegner y las memorias asociativas entrópicas es una contribución de este proyecto: los artículos de la línea EAM/EHAM no contienen nociones de directorio, de especialistas que cooperan ni de memoria transactiva.`
- **Problema:** (o).
- **Propuesta:** `Este puente entre la teoría de Wegner y las memorias asociativas entrópicas es una contribución de este proyecto: los artículos de la línea EAM/EHAM no contienen nociones de directorio, de especialistas que cooperan ni de memoria transactiva.`
- **Severidad:** baja.

- **Dónde:** `02:304–313`
- **Texto actual:** desde `La \textbf{entropía del directorio} resume el estado del sistema transactivo.` hasta `directorio se carga hacia sí mismo y queda por debajo del máximo aunque el grupo esté balanceado.`
- **Problema:** (n)+(j)+(i) el mismo párrafo, con ecuación, está en `03:500–518`; aquí además «especialización perfectamente balanceada».
- **Propuesta:**
  ```latex
  La \textbf{entropía del directorio} resume el estado del sistema transactivo: en el
  registro completo del grupo, el máximo $\log_2 K$ indica que la experticia se reparte
  pareja entre los $K$ módulos, y una entropía baja, colapso hacia un solo módulo o
  formación incompleta.
  En el directorio de cada módulo el máximo no es el estado deseable, porque cada uno
  registra lo que presenció y se carga hacia sí mismo (Sección~\ref{sec:operaciones}).
  ```
- **Severidad:** baja.

### 03_arquitectura.tex

- **Dónde:** `03:4–9`
- **Texto actual:**
  ```latex
  Esta sección describe la arquitectura completa del sistema distribuido de memoria
  transactiva en su versión de ocho módulos.
  Se presentan primero los componentes (Sección~\ref{sec:componentes}), luego los tres
  diagramas de flujo que muestran el llenado de memorias, la fase temprana y la fase
  madura (Sección~\ref{sec:diagramas}), y finalmente la formalización de todas las
  operaciones del sistema (Sección~\ref{sec:operaciones}).
  ```
- **Problema:** (o) metatexto que repiten los títulos de las subsecciones y `03:94–96`; además «en su versión de ocho módulos».
- **Propuesta:** quitar las seis líneas (la sección arranca en `\subsection{Componentes del sistema}`).
- **Severidad:** baja.

- **Dónde:** `03:36–38` (pie de la Tabla 1)
- **Texto actual:** `El dominio derecho de los directorios tiene una coordenada binaria por módulo ($q{=}2$: ``conoce''\,/\,``no conoce''); no hay una clase explícita de \emph{desconocido}: el rechazo emerge cuando ningún módulo obtiene soporte.}`
- **Problema:** (n)+(j) la prosa de `03:57–63` lo dice igual; en el pie sobra.
- **Propuesta:** `El dominio derecho de los directorios tiene una coordenada binaria por módulo ($q{=}2$: ``conoce''\,/\,``no conoce'').}`
- **Severidad:** baja.

- **Dónde:** `03:67–69`
- **Texto actual:** `Ambos apuntan al mismo destino (la identidad del módulo), pero las pistas viven en espacios distintos, por lo que requieren relaciones heteroasociativas separadas: una sola relación no admite dos formas de pista.`
- **Problema:** (n) la coda repite la causa recién dada.
- **Propuesta:** `Ambos apuntan al mismo destino (la identidad del módulo), pero las pistas viven en espacios distintos, por lo que requieren relaciones heteroasociativas separadas.`
- **Severidad:** baja.

- **Dónde:** `03:423–424`
- **Texto actual:** `La compuerta anula la puntuación si alguna fila del dominio derecho carece completamente de soporte: el módulo no opina sobre lo que no contiene.`
- **Problema:** (p)+(d) eslogan personificado dentro de una definición formal.
- **Propuesta:** `La compuerta anula la puntuación si alguna fila del dominio derecho carece de soporte.`
- **Severidad:** baja.

- **Dónde:** `03:433` y `03:452`
- **Texto actual:** `\paragraph{Justificación.}` (dos veces)
- **Problema:** (e) el mismo titulito mecánico dos veces en una página.
- **Propuesta:** quitar los dos `\paragraph{Justificación.}` y dejar correr el párrafo; o, si se quiere título, `\paragraph{Por qué la activación media es comparable.}` y `\paragraph{Por qué dividir entre el conteo.}`.
- **Severidad:** baja.

- **Dónde:** `03:493–498`
- **Texto actual:**
  ```latex
  El encoder lleva las entradas sin estructura (gris uniforme, desenfoque fuerte, contraste
  casi nulo) cerca del origen, donde caen dentro del soporte de \textit{cow}, \textit{dog}
  y \textit{horse}.
  $\tau = 16.61$ es la norma mínima de los 1600 originales del llenado (18.45) menos un
  margen del 10\%; rechaza una de las 1024 percepciones de la fase A y 4 de las 656
  imágenes de prueba.
  ```
- **Problema:** (j12) las mismas cifras y la misma explicación están en `04:148–157` (método) y en `05:349–359` (resultado); la arquitectura necesita solo la regla.
- **Propuesta:** quitar estas líneas y dejar `03:491–492` como `Antes de cualquier memoria visual, el latente continuo pasa un umbral de energía: si su norma es menor que $\tau = 16.61$, la imagen se rechaza (Sección~\ref{sec:percepcion}).`
- **Severidad:** baja.

- **Dónde:** `03:509–518`
- **Texto actual:**
  ```latex
  Con $K=8$ módulos, el máximo teórico es $\log_2 8 = 3$ bits,
  alcanzado cuando la especialización es perfectamente balanceada.
  Esa lectura vale para el registro completo del grupo (el del TME y el directorio
  compartido de los experimentos de calibración), donde una entropía menor indica o bien
  que un módulo acapara el directorio (colapso) o bien que está poco poblado (formación
  incompleta); el registro visual del TME queda en 3.000 bits.
  ```
- **Problema:** (g)+(h)+(i) tres paréntesis y un «;» en una oración; «perfectamente balanceada» con la cifra al lado.
- **Propuesta:**
  ```latex
  Con $K=8$ módulos, el máximo es $\log_2 8 = 3$ bits, alcanzado cuando los ocho módulos
  tienen el mismo número de registros.
  Esa lectura vale para el registro completo del grupo (el del TME y el directorio
  compartido de los experimentos de calibración).
  Ahí, una entropía menor indica que un módulo acapara el directorio o que está poco
  poblado; el registro visual del TME queda en 3.000 bits.
  ```
  (las líneas `03:515–518` siguen igual).
- **Severidad:** baja.

- **Dónde:** `03:547–548`
- **Texto actual:** `La necesidad del diccionario no es una debilidad del sistema sino una consecuencia directa de la naturaleza entrópica de la recuperación.`
- **Problema:** (b)+(d) cierre defensivo; las dos frases anteriores ya explican el diccionario.
- **Propuesta:** quitar.
- **Severidad:** baja.

- **Dónde:** `03:559–561`
- **Texto actual:**
  ```latex
  La fidelidad mide \emph{coincidencia con lo aprendido}, no acierto absoluto:
  un sistema con fidelidad alta conservó lo aprendido en la fase temprana al pasar
  a los directorios individuales.
  ```
- **Problema:** (n)+(b) la segunda mitad repite la primera.
- **Propuesta:** `La fidelidad mide coincidencia con lo aprendido en la fase temprana, no acierto absoluto.`
- **Severidad:** baja.

### 04_metodologia.tex

- **Dónde:** `04:44–45`
- **Texto actual:** `Cada percepción decide su ganador con la imagen original y registra sus 16 variantes con ese mismo ganador.`
- **Problema:** (p) la percepción no decide ni registra; se puede leer como si cada variante votara.
- **Propuesta:** `El ganador de cada percepción se decide con la imagen original, y sus 16 variantes se registran con ese ganador.`
- **Severidad:** media.

- **Dónde:** `04:96–106`
- **Texto actual:**
  ```latex
  El efecto de esta regla está medido y se declara como parte del protocolo: sobre el
  banco completo afecta a 46 consultas, que con el rescate aciertan 43/46 (93.5\%) y
  sin él 33/46 (71.7\%) --- \textbf{+21.7 puntos sobre las consultas afectadas}; sin
  él, cuatro de ellas se rechazan. Los diez cambios de ganador van todos hacia la clase
  correcta, y los tokens rescatados son de los más discriminativos (\texttt{bark},
  \texttt{moo}, \texttt{canine}, \texttt{riding}, \texttt{wheel}\ldots).
  Conviene precisar su estatus: la regla no decide el ganador (eso sigue siendo la
  proyección gateada de las memorias) ni censura token alguno, pero sí decide
  \emph{qué tokens entran como pista} con un criterio derivado del vocabulario que
  llenó las memorias, y por eso se reporta aquí con su delta en lugar de tratarse
  como un detalle de preprocesamiento neutro.
  ```
- **Problema:** (g)+(h)+(e')+(o)+(j14) en una oración: «:», raya, negrita y «;»; luego «Conviene precisar su estatus:» y la justificación que la limitación (g) repite.
- **Propuesta:**
  ```latex
  Sobre el banco completo la regla afecta a 46 consultas: con el rescate aciertan 43
  (93.5\%) y sin él 33 (71.7\%), y sin él cuatro se rechazan.
  Los diez cambios de ganador van todos hacia la clase correcta, y los tokens rescatados
  son de los más discriminativos (\texttt{bark}, \texttt{moo}, \texttt{canine},
  \texttt{riding}, \texttt{wheel}\ldots).
  La regla no decide el ganador ni censura tokens, pero sí decide qué tokens entran como
  pista con un criterio derivado del vocabulario que llenó las memorias; por eso se
  reporta con su efecto medido (limitación (g), Sección~\ref{sec:limitaciones}).
  ```
- **Fuente:** cifras sin cambio (43/46, 33/46, +21.7 se deduce).
- **Severidad:** media.

- **Dónde:** `04:4–6`
- **Texto actual:**
  ```latex
  Este capítulo describe el conjunto de datos, el pipeline de representación, los
  parámetros del sistema, la auditoría de fidelidad y las métricas usadas para evaluar el
  sistema EAM-TMS de ocho módulos.
  ```
- **Problema:** (o).
- **Propuesta:** quitar.
- **Severidad:** baja.

- **Dónde:** `04:17–23`
- **Texto actual:**
  ```latex
  La partición se realizó a nivel de archivo de imagen.
  Por tanto, no hay solapamiento de imágenes entre train y test, pero la partición
  principal no separa los objetos físicos de ETH-80: verificado sobre la partición
  persistida, \textbf{los diez objetos físicos de cada clase aportan vistas tanto a train
  como a test} (solape de instancias del 100\%), y toda imagen de prueba es una vista
  nueva de un objeto cuyas demás vistas participaron del llenado o de la formación del
  directorio.
  ```
- **Problema:** (g)+(e') una oración de seis líneas con «:», negrita y paréntesis.
- **Propuesta:**
  ```latex
  La partición se realizó a nivel de archivo de imagen, así que ninguna imagen está en
  train y en test a la vez.
  No separa los objetos físicos de ETH-80: verificado sobre la partición persistida, los
  diez objetos de cada clase aportan vistas a train y a test (solape de instancias del
  100\%), y toda imagen de prueba es una vista nueva de un objeto cuyas demás vistas
  participaron del llenado o de la formación del directorio.
  ```
- **Severidad:** baja.

- **Dónde:** `04:36–41`
- **Texto actual:**
  ```latex
      Cada imagen se registra junto con 15 variantes de \emph{augmentación} (16 patrones
      por imagen, 3200 por clase): espejo; rotaciones de $\pm 12^{\circ}$ de la imagen y
      de su espejo, y de $\pm 6^{\circ}$ de la imagen; escalas de 0.9 y 1.1; brillo de
      0.85 y 1.15, y desplazamientos de 6 píxeles en las cuatro direcciones. Esto
      densifica la distribución latente acumulada sin tocar el mecanismo de la memoria:
      es más percepción, no otro modelo.
  ```
- **Problema:** (j) la lista de variantes está entera en el pie de la Figura 1 (`03:176–179`); (b)+(d) cierre «es más percepción, no otro modelo».
- **Propuesta:**
  ```latex
      Cada imagen se registra junto con 15 variantes de \emph{augmentación} (16 patrones
      por imagen, 3200 por clase; la lista está en el pie de la
      Figura~\ref{fig:arq-llenado}).
      Esto densifica la distribución latente acumulada sin tocar el mecanismo de la memoria.
  ```
  Si se prefiere la lista aquí, quitarla del pie de la figura.
- **Severidad:** baja.

- **Dónde:** `04:80–81`
- **Texto actual:** `La misma escala se aplica en el llenado y en la consulta, lo que garantiza que ambos lados hablen el mismo alfabeto.`
- **Problema:** (n)+(d) metáfora que explica lo obvio.
- **Propuesta:** `La misma escala se aplica en el llenado y en la consulta.`
- **Severidad:** baja.

- **Dónde:** `04:109–117`
- **Texto actual:**
  ```latex
  El vocabulario de ConceptNet sirve para \emph{llenar} las memorias, no para decidir qué
  consultas son conocidas.
  Cada token de la consulta se convierte en una pista vectorial tomando su vector del
  modelo fastText completo, exista o no como etiqueta de ConceptNet.
  No se aplica ningún filtro de pertenencia léxica: una vez obtenida la pista, es la
  propia memoria la que, mediante el reconocimiento y el \textit{containment}, decide si
  hay soporte o se rechaza (puntuación cero).
  Solo queda fuera lo que no es representable: un token sin vector fastText real no genera
  pista, lo cual es una frontera del codificador lingüístico y no un rechazo de la memoria.
  ```
- **Problema:** (n)+(b)+(j6) tres frases para decir «no hay filtro»; es la primera de cinco apariciones de la idea.
- **Propuesta:**
  ```latex
  El vocabulario de ConceptNet sirve para llenar las memorias, no para decidir qué
  consultas son conocidas: cada token de la consulta se convierte en pista con su vector
  del modelo fastText completo, exista o no como etiqueta de ConceptNet, y es la memoria
  la que, por reconocimiento y \textit{containment}, le da soporte o lo rechaza
  (puntuación cero).
  Un token sin vector fastText real no genera pista; esa frontera es del codificador
  lingüístico.
  ```
- **Severidad:** baja.

- **Dónde:** `04:135–141`
- **Texto actual:**
  ```latex
  Una precisión de protocolo que debe declararse: no existe partición de validación
  separada, de modo que el punto de control ganador se selecciona por RMSE mínimo
  evaluado \emph{sobre el propio conjunto de prueba} (una evaluación cada 10 épocas,
  $\approx$5 candidatos).
  Es una selección de modelo sobre test, de alcance acotado, pero significa que el
  espacio latente con el que después se evalúa el hemisferio visual fue elegido
  mirando ese conjunto (Sección~\ref{sec:limitaciones}).
  ```
- **Problema:** (o)+(j15) anuncio y la misma valoración que la limitación (f).
- **Propuesta:**
  ```latex
  No existe partición de validación separada: el punto de control ganador se selecciona
  por RMSE mínimo sobre el propio conjunto de prueba (una evaluación cada 10 épocas,
  $\approx$5 candidatos); el alcance de esa selección se discute en la limitación (f)
  (Sección~\ref{sec:limitaciones}).
  ```
- **Severidad:** baja.

- **Dónde:** `04:191–196`
- **Texto actual:**
  ```latex
  En síntesis: $\iota > 0$ elimina conocimiento escaso pero válido antes de eliminar
  relaciones espurias; $\kappa$ solo rechaza: en todo el rango en que actúa baja la
  precisión y nunca la mejora; y $\xi > 0$ no se usa en el directorio visual porque,
  con directorios perspectivales, la tolerancia de un módulo dependería de lo que
  presenciaron los demás.
  Las cifras visuales de la Sección~\ref{sec:hemisferio-visual} se obtienen con $\xi = 0$.
  ```
- **Problema:** (g)+(o)+(j11) cadena «: ; : ;» que adelanta los resultados de `05:194–210` y repite la justificación de $\xi$ de `03:484–489`; la última línea repite `04:182–183`.
- **Propuesta:** quitar las seis líneas (`04:186–190` ya remiten a las secciones donde se justifican).
- **Severidad:** baja.

### 05_resultados.tex

- **Dónde:** `05:398–440` (párrafos 2 y 3 de «Línea base: una sola EHAM»)
- **Texto actual:** desde `Con 25 imágenes por clase la EHAM única acierta la clase algo más que el` (`05:411`) hasta `Tablas completas en \texttt{results/experimento11/}.` (`05:440`).
- **Problema:** (l)+(f)+(g) dos párrafos de 15 líneas con series paralelas de cuatro cifras por brazo («43.8, 75.0, 92.5 y 97.5 %», «78.7, 95.0, 98.8 y 100 %», «2, 2, 5 y 8», «4.6, 6.2, 6.1 y 5.7»); la tesis remite a un archivo externo en lugar de dar la tabla.
- **Propuesta:** insertar la tabla y acortar la prosa. Las cifras son las del README del experimento (ver Fuente); «Especialista» es el brazo que el README llama «T-oraculo».
  ```latex
  \begin{table}[H]
  \centering
  \caption{Una EHAM con las ocho clases (EHAM única) contra los especialistas con el
  módulo elegido por la verdad de terreno (oráculo) y el protocolo transactivo, por
  número de imágenes de llenado por clase. Texto$\to$imagen sobre las 171 consultas
  reservadas; imagen$\to$texto sobre las imágenes de prueba; fuera de dominio sobre 40
  consultas. Diez semillas; intervalos de 95\,\% en \texttt{results/experimento11/}.}
  \label{tab:eham-unica}
  \small
  \begin{tabular}{llcccc}
  \toprule
   & & 25 & 50 & 100 & 200 \\
  \midrule
  \multirow{3}{*}{Clase correcta, texto$\to$imagen (\%)}
   & EHAM única & 97.6 & 97.5 & 97.6 & 96.9 \\
   & Protocolo  & 96.9 & 98.8 & 98.8 & 98.3 \\
   & Oráculo    & 100  & 100  & 100  & 100 \\
  \midrule
  \multirow{3}{*}{Distancia a la instancia real más cercana}
   & EHAM única & 22.9 & 26.6 & 29.4 & 32.5 \\
   & Protocolo  & 19.0 & 20.7 & 23.8 & 27.0 \\
   & Oráculo    & 18.2 & 20.4 & 23.4 & 26.8 \\
  \midrule
  \multirow{3}{*}{Responde, imagen$\to$texto (\%)}
   & EHAM única   & 78.7 & 95.0 & 98.8 & 100 \\
   & Especialista & 43.8 & 75.0 & 92.5 & 97.5 \\
   & Protocolo    & 41.2 & 67.5 & 78.7 & 81.2 \\
  \midrule
  \multirow{3}{*}{Responde con dominio ajeno (\%)}
   & EHAM única   & 5.5 & 7.5 & 10.5 & 10.9 \\
   & Especialista & 0.1 & 1.9 & 2.6 & 4.1 \\
   & Protocolo    & 0.2 & 1.8 & 2.2 & 3.0 \\
  \midrule
  \multirow{3}{*}{Fuera de dominio aceptadas (de 40)}
   & EHAM única & 2 & 2 & 5 & 8 \\
   & Protocolo (con doble compuerta) & 4 (2) & 4 (2) & 4 (2) & 4 (2) \\
   & Oráculo    & 2 & 2 & 2 & 2 \\
  \bottomrule
  \end{tabular}
  \end{table}

  La Tabla~\ref{tab:eham-unica} resume la comparación.
  Con 25 imágenes por clase la EHAM única acierta la clase algo más que el protocolo
  (97.6 frente a 96.9\,\%; juez: vecino real más cercano), con intervalos de 95\,\% que
  casi se tocan ($[97.4, 97.8]$ y $[96.3, 97.6]$); desde 50 el orden se invierte y los
  intervalos se separan (con 200, $[97.9, 98.6]$ y $[96.7, 97.1]$); el oráculo acierta
  el 100\,\%.
  La respuesta de la EHAM única queda más lejos de la instancia real más cercana en los
  cuatro cortes, y la brecha con el oráculo no crece con el contenido (4.6, 6.2, 6.1 y
  5.7).
  Cuando la primera pista reconocida es una etiqueta compartida entre clases
  (\emph{fruit}, \emph{animal}, \emph{red}; el 3.5\,\% de las respuestas), la EHAM única
  acierta la clase entre el 48 y el 52\,\% y su patrón tiene soporte en una sola clase en
  el 74--77\,\% de las coordenadas; el protocolo, entre el 79 y el 84\,\%, y el oráculo,
  el 100\,\%.

  En imagen\,$\to$\,texto la EHAM única responde más y se equivoca más de dominio: con
  200, responde con un dominio ajeno el 10.9\,\% de las imágenes, frente al 4.1\,\% del
  especialista y el 3.0\,\% del protocolo, que en este experimento forma su directorio
  visual sin variantes y responde al 81\,\%.
  Fuera de dominio, la EHAM única acepta más a medida que crece el contenido; el oráculo
  acepta 2 en todos los cortes y el protocolo 4, que bajan a 2 con la doble compuerta de
  contenido (el módulo destino debe contener la pista).
  El precio del directorio, la distancia del protocolo al oráculo en clase, es de 3.1
  puntos con 25 imágenes por clase y de 1.2 a 1.7 desde 50.
  ```
- **Fuente:** `results/experimento11/README.md`, bloques «N = 25», «N = 50», «N = 100», «N = 200»: columnas «clase 1-NN» (97.6/96.9/100; 97.5/98.8/100; 97.6/98.8/100; 96.9/98.3/100), «d_nn» (22.86, 18.97, 18.22; 26.57, 20.67, 20.38; 29.40, 23.78, 23.35; 32.53, 26.98, 26.78), «responde» imagen→texto (78.7/43.8/41.2; 95.0/75.0/67.5; 98.8/92.5/78.7; 100/97.5/81.2), «otro dominio» (5.5/0.1/0.2; 7.5/1.9/1.8; 10.5/2.6/2.2; 10.9/4.1/3.0) y «acepta» fuera de dominio en % de 40 (5.0/5.0/10.0→5.0; 5.0/5.0/10.0→5.0; 12.5/5.0/10.0→5.0; 20.0/5.0/10.0→5.0). Todas coinciden con las cifras que hoy da la prosa.
- **Severidad:** media.

- **Dónde:** `05:341–365`
- **Texto actual (fragmentos a cambiar):**
  ```latex
  \paragraph{El rechazo y la salida semántica los decide la memoria.}
  Reconocimiento, rechazo y reconstrucción son operaciones de la propia memoria: el
  encoder ResNet18 solo convierte la imagen en una pista latente, y a partir de ahí la
  EAM decide.
  ```
  `cero en los ocho módulos y se rechazan, sin que intervenga ningún filtro externo.` (`05:348`)
  `contenido: es la excepción honesta del panel. El experimento 14 localizó la causa: el` (`05:349–350`)
  ```latex
  Que la reconstrucción difiera de la entrada es esperado y honesto: refleja que decide
  la distribución acumulada en la memoria.
  ```
  (`05:364–365`)
- **Problema:** (e)+(a)+(p)+(i)+(d)+(j6): título-eslogan; tríada aliterada «reconocimiento, rechazo y reconstrucción» (la reconstrucción la hace el decoder); «la EAM decide» y «sin que intervenga ningún filtro externo» repiten `04:113–115`; «honesta» y «esperado y honesto» califican el resultado en vez de darlo; la última frase es moraleja.
- **Propuesta:**
  ```latex
  \paragraph{Rechazo y salida semántica.}
  El encoder ResNet18 solo convierte la imagen en una pista latente; reconocimiento,
  rechazo y recuperación son operaciones de la memoria.
  ```
  `05:348`: `cero en los ocho módulos y se rechazan.`
  `05:349–350`: `contenido: es la excepción del panel. El experimento 14 localizó la causa: el`
  `05:364–365`: quitar.
- **Severidad:** media (el «honesto» es juicio del autor dentro de los resultados).

- **Dónde:** `05:4–8`
- **Texto actual:**
  ```latex
  Los resultados se presentan en este orden: el estudio de calibración del directorio
  (el estudio principal), el protocolo completo con los parámetros nativos, la
  formación del directorio, la capacidad de llenado, el hemisferio visual, la
  comparación con una sola EHAM, la memoria de contenido única por módulo y la
  medición del costo computacional.
  ```
- **Problema:** (o) repite el índice; `04:245–257` («Organización del experimento») ya lo enumera.
- **Propuesta:** quitar; dejar `05:9–11`.
- **Severidad:** baja.

- **Dónde:** `05:51`
- **Texto actual:** `\paragraph{B1 sigue siendo la corrección irreducible.}`
- **Problema:** (e)+(i) título-eslogan; «irreducible» no es una medida y «sigue siendo» es historia.
- **Propuesta:** `\paragraph{Lectura cruda contra B1.}`
- **Severidad:** baja.

- **Dónde:** `05:95`
- **Texto actual:** `\paragraph{El sesgo hacia \texttt{apple} quedó esencialmente resuelto.}`
- **Problema:** (e) título-eslogan (y resto de historia ya conocido; este es el texto nuevo concreto).
- **Propuesta:** `\paragraph{Participación de \texttt{apple}.}`
- **Severidad:** baja.

- **Dónde:** `05:112–117`
- **Texto actual:**
  ```latex
  \paragraph{Estado del directorio.}
  La entropía del directorio transactivo alcanza 2.974 bits en la condición A y 2.977
  bits en G, sobre un máximo teórico de 3.000 bits ($\log_2 8$): la especialización queda
  balanceada al 99.1\% incluso sin corrección, porque el desequilibrio de masas es un
  sesgo de \emph{lectura}, no de estructura.
  La fidelidad temprana-madura con B1 es del 95.8\%.
  ```
- **Problema:** (j8)+(b) la interpretación «sesgo de lectura, no de estructura» está, con las mismas palabras, en `06:51–53`.
- **Propuesta:**
  ```latex
  \paragraph{Estado del directorio.}
  La entropía del directorio transactivo alcanza 2.974 bits en la condición A y 2.977
  bits en G, sobre un máximo de 3.000 ($\log_2 8$); la fidelidad temprana-madura con B1
  es del 95.8\%.
  ```
- **Severidad:** baja.

- **Dónde:** `05:129–131`
- **Texto actual:**
  ```latex
  El rechazo no proviene de un filtro de vocabulario: cada token con representación
  fastText entra como pista, y es la propia memoria la que rechaza cuando ningún módulo
  obtiene soporte.
  ```
- **Problema:** (j6)+(b) repite `04:109–117`.
- **Propuesta:** quitar.
- **Severidad:** baja.

- **Dónde:** `05:142–145`
- **Texto actual:**
  ```latex
  Nótese que la fase madura sobre este subconjunto (81.2\%) es inferior a la del banco
  completo (93.0\%): con solo 10 consultas por clase, el directorio dispone de menos
  evidencia por dominio; la diferencia mide el efecto del volumen de interacciones, no un
  cambio de mecanismo.
  ```
- **Problema:** (o)+(j10)+(b) «Nótese que» y la misma explicación que `05:231–238`.
- **Propuesta:** quitar.
- **Severidad:** baja.

- **Dónde:** `05:157–161`
- **Texto actual:**
  ```latex
  La memoria rechazó \textbf{10 de 12} por containment puro (puntuación cero en los ocho
  módulos), sin regla léxica alguna.
  Las 2 restantes rutean porque comparten tokens con labels legítimos de algún dominio
  (p.ej.\ \textit{food}): la frontera entre ``fuera de dominio'' y ``comparte conceptos
  con el dominio'' es semántica, no léxica, y el diagnóstico la mide en lugar de esconderla.
  ```
- **Problema:** (d)+(b)+(e')+(j6) cierre con moraleja («y el diagnóstico la mide en lugar de esconderla»), «sin regla léxica alguna» por quinta vez, negrita.
- **Propuesta:**
  ```latex
  La memoria rechazó 10 de 12 por containment (puntuación cero en los ocho módulos).
  Las 2 restantes rutean porque comparten tokens con labels legítimos de algún dominio
  (p.ej.\ \textit{food}).
  ```
- **Severidad:** baja.

- **Dónde:** `05:210`
- **Texto actual:** `$\kappa$ no es una defensa contra el sesgo de masa.`
- **Problema:** (d)+(b) cierre que niega algo que nadie planteó.
- **Propuesta:** quitar.
- **Severidad:** baja.

- **Dónde:** `05:212`
- **Texto actual:** `\paragraph{Ninguna condición nativa sustituye a B1.}`
- **Problema:** (e) título-eslogan.
- **Propuesta:** `\paragraph{Lectura cruda contra B1 en el grid.}`
- **Severidad:** baja.

- **Dónde:** `05:231–238` (en la propuesta de replanteamiento, fila 231–234)
- **Texto actual (propuesta):**
  ```latex
  \paragraph{Hallazgo principal: con ocho módulos, 10 consultas por clase no bastan.}
  \textbf{Ninguna condición alcanza el umbral del 90\%} con este volumen de interacciones:
  todas convergen al 81.2\% final.
  No es un fallo de convergencia sino de evidencia disponible: con 8 dominios y consultas
  que comparten léxico, 10 interacciones por dominio no acumulan suficiente evidencia
  distintiva (el mismo protocolo con el banco completo alcanza 93.0\%,
  Sección~\ref{sec:calibracion}).
  ```
- **Problema:** (c)+(e)+(b)+(e') «Hallazgo principal:» en el título, «No es X sino Y:» y negrita.
- **Propuesta:**
  ```latex
  \paragraph{Diez consultas por clase no bastan.}
  Ninguna condición alcanza el umbral del 90\% con este volumen de interacciones: todas
  convergen al 81.2\% final.
  Con 8 dominios y consultas que comparten léxico, 10 interacciones por dominio no
  acumulan suficiente evidencia distintiva; el mismo protocolo con el banco completo
  alcanza 93.0\% (Sección~\ref{sec:calibracion}).
  ```
- **Severidad:** baja.

- **Dónde:** `05:240–241`
- **Texto actual:**
  ```latex
  \paragraph{El orden afecta la velocidad, no el destino.}
  Todas las condiciones convergen exactamente al mismo estado final: conteos
  ```
- **Problema:** (e)+(b)+(i) título-eslogan (que `06:108` repite) y «exactamente» con los conteos al lado.
- **Propuesta:**
  ```latex
  \paragraph{Efecto del orden.}
  Todas las condiciones convergen al mismo estado final: conteos
  ```
- **Severidad:** baja.

- **Dónde:** `05:284–287` (en la propuesta de replanteamiento, fila 284–287)
- **Texto actual (propuesta):** `\paragraph{Especificidad.} Con el llenado de un latente por imagen, la tasa de falsos aceptados es del \textbf{0\% en todo el rango} de $N$ probado, con siete clases contrarias por módulo: el containment inverso mantiene la discriminación exacta también a ocho clases.`
- **Problema:** (d)+(i)+(e') la coda repite la cifra con «exacta»; negrita.
- **Propuesta:** `\paragraph{Especificidad.} Con el llenado de un latente por imagen, la tasa de falsos aceptados es del 0\% en todo el rango de $N$ probado, con siete clases contrarias por módulo.`
- **Severidad:** baja.

- **Dónde:** `05:304–312` (la propuesta de replanteamiento ya quita «$\approx$50\% en la versión de tres módulos»)
- **Texto actual:**
  ```latex
  \paragraph{Fase A: formación con 1024 imágenes.}
  Se presentaron 1024 imágenes (128 por clase) en orden intercalado.
  Sobre las imágenes aceptadas, la precisión del módulo visual fue del \textbf{99.9\%},
  con un rechazo del \textbf{0.8\%} (4.2\% con 4 variantes en el experimento 13; $\approx$50\%
  en la versión de tres módulos) y una percepción rechazada antes de la memoria por el
  umbral de energía. Cada percepción aceptada registra sus 16 variantes: el registro
  completo del TME quedó en $[2048, 2016, 2016, 2016, 2016, 2032, 2048, 2048]$ con
  entropía de \textbf{3.000 bits}: el máximo teórico, especialización visual
  perfectamente balanceada.
  ```
- **Problema:** (g)+(i)+(e') dos «:» en la última oración, «perfectamente balanceada» tras «3.000 bits», tres negritas.
- **Propuesta:**
  ```latex
  \paragraph{Fase A: formación con 1024 imágenes.}
  Se presentaron 1024 imágenes (128 por clase) en orden intercalado.
  Sobre las imágenes aceptadas, la precisión del módulo visual fue del 99.9\%, con un
  rechazo del 0.8\% (4.2\% con 4 variantes en el experimento 13) y una percepción
  rechazada antes de la memoria por el umbral de energía.
  Cada percepción aceptada registra sus 16 variantes.
  El registro completo del TME quedó en $[2048, 2016, 2016, 2016, 2016, 2032, 2048, 2048]$,
  con entropía de 3.000 bits, el máximo.
  ```
- **Severidad:** baja.

- **Dónde:** `05:356`
- **Texto actual:** `No es cualquier fondo liso: de 12 sólidos de color se aceptan 2.`
- **Problema:** (b)+(c).
- **Propuesta:** `De 12 sólidos de color se aceptan 2.`
- **Severidad:** baja.

- **Dónde:** `05:515–516`
- **Texto actual:** `Ninguna lectura de la arquitectura con homo quedó fuera del alcance de una sola memoria por módulo.`
- **Problema:** (m)+(d) párrafo de una frase que cierra la subsección como sentencia.
- **Propuesta:** quitar, o pegarla al final del párrafo anterior (`05:487–489`) como `Ninguna lectura de la arquitectura con homo queda fuera del alcance de una sola memoria por módulo.`
- **Severidad:** baja.

- **Dónde:** negritas de cifras en prosa: `05:127`, `134`, `136`, `140`, `157`, `233`, `285`, `306`, `307`, `311`, `318`, `320`, `321`, `339`
- **Texto actual:** p.ej. `\textbf{precisión temprana del 81.2\%}`, `\textbf{10 de 12}`, `\textbf{631/656 = 96.2\%}`, `\textbf{113/116 = 97.4\%}`
- **Problema:** (e') catorce cifras en negrita dentro de párrafos; es resaltado mecánico, y los lectores de tesis esperan las cifras en texto normal o en tablas.
- **Propuesta:** quitar `\textbf{}` en las catorce; conservar las negritas de términos definidos (p.ej. `\textbf{zona de operación}`).
- **Severidad:** baja.

### 06_discusion.tex

- **Dónde:** `06:232–270` (limitación (b), un párrafo de 39 líneas)
- **Texto actual:** desde `La lectura del directorio visual es estricta ($\xi = 0$): con directorios` (`06:233`) hasta `cuesta cuatro aciertos de test.` (`06:270`).
- **Problema:** (g)+(j11)+(j12)+(j16)+(i)+(b)+(c): un solo párrafo con tres asuntos (lectura estricta y densificación; entradas degeneradas; umbral $\tau$); el costo de $\tau$ se dice dos veces en el mismo párrafo (`258–260` «a costa de cinco imágenes reales de 3280 … No es gratis: las cuatro de test…» y `267–270` «rechaza una percepción de 1024 … y cuatro imágenes de 656 … cuesta cuatro aciertos de test»); «El precio no es cero:» y «No es gratis:» en diez líneas; «siempre el par animal» para cinco casos; y `06:250` dice «presumiblemente porque el fondo liso de ETH-80 puebla esa región» cuando `05:350–355` ya da la causa medida por el experimento 14 (norma baja del latente), que el propio párrafo usa cuatro líneas después. Las cifras 73.6→96.2 y 76→96 están en `05:329–334`.
- **Propuesta:** tres párrafos; el costo de $\tau$ una vez; la causa de la fuga con la medición y no con «presumiblemente».
  ```latex
  \paragraph{(b) Cobertura visual residual limitada por el containment conjunto.}
  La lectura del directorio visual es estricta ($\xi = 0$; Sección~\ref{sec:operaciones}),
  y la palanca es densificar.
  Son dos compuertas, el directorio visual (formado con las percepciones de la fase A) y
  el recall de la hetero, y cada una cede solo con su propia augmentación: con 16
  variantes en las dos, la cobertura de punta a punta pasa de 66.5 a 94.5\,\% de las 656
  imágenes de test (experimento 13, Sección~\ref{sec:hemisferio-visual}), con rendimiento
  decreciente por escalón de variantes.
  El precio son dos ruteos equivocados de 656 (dos vistas de \texttt{horse7} a
  \texttt{dog}, que las contiene, así que la doble compuerta no las detiene) y, en el
  experimento, cinco imágenes aceptadas por un especialista ajeno, las cinco del par
  animal que ya confunde al texto; son vistas nuevas de los mismos objetos, porque el
  split es por imagen.

  El containment visual tiene además una fuga con \emph{entradas degeneradas}: una imagen
  de color sólido uniforme obtiene soporte y se acepta (Figura~\ref{fig:rechazo-imagenes})
  porque el encoder lleva las entradas sin estructura a latentes de norma baja, dentro de
  la envolvente de los animales (experimento 14, Sección~\ref{sec:hemisferio-visual});
  las sondas estructuradas (ruido, píxeles barajados) sí se rechazan.
  Densificar agranda esa fuga: con 16 variantes la aceptan tres especialistas en vez de
  uno y el directorio la rutea.
  La doble compuerta del punto (a) no la cerraría, porque el contenido también la acepta.

  El umbral de energía $\tau$ (Sección~\ref{sec:percepcion}) cierra el 90\,\% de esa fuga:
  137 de las 152 entradas degeneradas aceptadas por una clase ajena caen bajo $\tau$
  (grises de 104 a 168, desenfoques de radio $\geq 12$, contrastes $\leq 0.2$).
  La norma y la varianza del latente son equivalentes; la varianza de píxeles no sirve,
  porque un objeto desenfocado conserva contraste y pierde estructura.
  Lo que sobrevive al umbral son sobre todo confusiones de contenido entre clases (11 de
  15 son objetos desenfocados o de bajo contraste, como un \texttt{dog} desenfocado
  aceptado por \texttt{cow}); las otras cuatro son superficies casi uniformes de norma
  alta (un gris claro, dos colores sólidos y un gris con ruido).
  Su costo son cinco imágenes reales de 3280, todas vistas oscuras de \texttt{cow}: una
  percepción de la fase A y cuatro imágenes de test que el directorio ruteaba bien y su
  contenido aceptaba.
  ```
  Si se quiere conservar aquí «el ruteo de test queda en 96.2 %, la evocación en 97.4 % y el rechazo en 3.5 %», cabe como una línea tras «rendimiento decreciente por escalón de variantes».
- **Fuente:** cifras sin cambio; la cuenta 3280 = 1600 llenado + 1024 fase A + 656 test y «una percepción de la fase A y cuatro de test» salen de `04:155–157`. La causa de la fuga (norma baja) está en `05:350–355`; no abrí los archivos del experimento 14.
- **Severidad:** media (duplicación dentro del párrafo e inconsistencia «presumiblemente» contra «localizó la causa»).

- **Dónde:** `06:185–207` («Qué aporta la partición frente a una EHAM única», un párrafo de 23 líneas)
- **Texto actual:** desde `La comparación con la EHAM única acota lo que la maquinaria transactiva` hasta `las celdas.`
- **Problema:** (g)+(a)+(l)+(j) un solo párrafo con «;», «:» y paréntesis en casi cada oración; «fidelidad, coherencia y precisión» es tríada por reflejo (la frase siguiente habla solo de mezcla, y más abajo la precisión «mejora, pero poco»); repite cifras de `05:411–440`.
- **Propuesta:**
  ```latex
  La comparación con la EHAM única acota lo que la maquinaria transactiva aporta.
  Ante todo, fidelidad: la relación de una EHAM acumula por coordenada y valor, y dos
  conceptos distintos comparten valores cuantizados en muchas coordenadas, así que una
  memoria con varios dominios mezcla al recordar aunque las palabras difieran.
  Partir el contenido evita la mezcla porque la decisión de dominio ocurre antes del
  recall, en el directorio, y no dentro del sorteo.
  La respuesta de la EHAM única queda más lejos de la instancia real más cercana en todos
  los cortes (Tabla~\ref{tab:eham-unica}), sin tendencia con el contenido, y fuera de
  dominio acepta más cuanto más contiene, mientras que el protocolo con doble compuerta
  acepta 2 en todos los cortes.

  La exactitud de clase también mejora, pero poco: desde 50 imágenes por clase el
  protocolo acierta entre 98.3 y 98.8\,\% frente a 96.9--97.6\,\% de la EHAM única, con
  intervalos separados; con 25 la EHAM única queda arriba, porque el directorio todavía
  rutea peor (95.3\,\% de ruteo correcto).

  El precio es cobertura.
  El containment de un especialista es estricto en las 64 coordenadas del latente y deja
  sin respuesta al 2.5\,\% de las imágenes de prueba con 200 por clase, que la EHAM única
  responde; es parte del rechazo residual del hemisferio visual (limitación (b)).
  A eso se suman de 1.2 a 1.7 puntos del directorio desde 50 imágenes por clase (3.1 con
  25) y ocho veces las celdas.
  ```
  (Si no se adopta la tabla de `05`, la referencia `Tabla~\ref{tab:eham-unica}` se cambia por `Sección~\ref{sec:eham-unica}`.)
- **Severidad:** media.

- **Dónde:** `06:48–56` (en la propuesta de replanteamiento, 4b: «Dos datos sostienen esta lectura. Primero, …»)
- **Texto actual (propuesta más líneas 51–56 actuales):**
  ```latex
  Dos datos sostienen esta lectura. Primero, la brecha cruda-B1 es de 7.8 puntos con ocho
  módulos (85.2\% frente a 93.0\%).
  Segundo, la entropía del directorio es alta incluso en la condición cruda (2.974 de
  3.000 bits): la \emph{estructura} del directorio está bien formada y balanceada; el
  sesgo vive en la \emph{lectura}, exactamente donde B1 actúa.
  Las condiciones que manipulan síntomas (B2, C, D, E) vuelven a quedar por debajo, y la
  combinación G supera a B1 sola por medio punto (93.5\% frente a 93.0\%), dentro del
  ruido: una vez corregida la causa, las correcciones auxiliares aportan poco.
  ```
- **Problema:** (c)+(f)+(i)+(j7) anuncio «Dos datos sostienen esta lectura» con Primero/Segundo; «exactamente»; las dos últimas líneas repiten `05:56–58` palabra por palabra («supera a B1 sola por medio punto … dentro del ruido: una vez corregida la causa … aportan poco»); «vuelven a quedar» es historia.
- **Propuesta:**
  ```latex
  La brecha cruda-B1 es de 7.8 puntos con ocho módulos (85.2\% frente a 93.0\%), y la
  entropía del directorio es alta incluso en la condición cruda (2.974 de 3.000 bits):
  la estructura del directorio está balanceada y el sesgo vive en la lectura, donde B1
  actúa.
  Las condiciones que manipulan síntomas (B2, C, D, E) quedan por debajo
  (Tabla~\ref{tab:calibracion}).
  ```
- **Severidad:** media (repetición literal entre secciones).

- **Dónde:** `06:65–76`
- **Texto actual:**
  ```latex
  La explicación que salta a la vista es léxica: \texttt{apple} posee en ConceptNet el
  vocabulario genérico de fruta (\textit{fruit}, \textit{red}, \textit{green},
  \textit{round}, \textit{tree}).
  Pero no basta: el sesgo viene también del encoder, en cuyo espacio latente
  \texttt{pear} y \texttt{tomato} se solapan con \texttt{apple}.

  La conclusión corregida es que el sesgo era un efecto \emph{conjunto} de la
  separabilidad del espacio latente y de la asimetría léxica de la fuente de
  conocimiento, no de la segunda por sí sola.
  El hallazgo tiene una lectura metodológica: en un sistema bidireccional, un sesgo
  observado en el hemisferio semántico puede tener su causa parcial en el hemisferio
  visual, porque el llenado imagen-etiqueta acopla ambos espacios.
  ```
- **Problema:** (c)+(d)+(b) tres anuncios seguidos («La explicación que salta a la vista es léxica:», «Pero no basta:», «El hallazgo tiene una lectura metodológica:») y «La conclusión corregida» narra una conclusión anterior.
- **Propuesta:**
  ```latex
  Parte de la explicación es léxica: \texttt{apple} posee en ConceptNet el vocabulario
  genérico de fruta (\textit{fruit}, \textit{red}, \textit{green}, \textit{round},
  \textit{tree}).
  La otra parte está en el encoder, en cuyo espacio latente \texttt{pear} y
  \texttt{tomato} se solapan con \texttt{apple}.
  El sesgo es un efecto conjunto de la separabilidad del espacio latente y de la
  asimetría léxica de la fuente de conocimiento.
  En un sistema bidireccional, un sesgo observado en el hemisferio semántico puede tener
  su causa parcial en el hemisferio visual, porque el llenado imagen-etiqueta acopla
  ambos espacios.
  ```
- **Severidad:** media (incluye un resto de historia con texto nuevo).

- **Dónde:** `06:5` y `06:8`, `06:12–13` (en la propuesta de replanteamiento, 4a)
- **Texto actual (propuesta):** `\subsection{La maquinaria transactiva funciona con ocho dominios; la representación es el límite}`, `El resultado central es una separación limpia de responsabilidades.`, `y el directorio visual alcanza el balance perfecto (3.000 de 3.000 bits)`
- **Problema:** (e) título-eslogan con punto y coma; (i) «limpia», «perfecto» con la cifra al lado.
- **Propuesta:** `\subsection{Mecanismo y representación}`; `El resultado central es una separación de responsabilidades.`; `y el directorio visual alcanza el máximo de entropía (3.000 de 3.000 bits)`.
- **Severidad:** baja.

- **Dónde:** `06:37` y `06:40–41` (título en la propuesta de replanteamiento: «La normalización necesaria es B1»)
- **Texto actual:** `La lectura B1 del directorio transactivo no corrige un defecto: refleja cómo está construido el sistema.`
- **Problema:** (e) título-eslogan; (b)+(c) «no corrige un defecto: refleja».
- **Propuesta:** `\subsection{Por qué B1}`; `La lectura B1 del directorio refleja cómo está construido el sistema.`
- **Severidad:** baja.

- **Dónde:** `06:59`
- **Texto actual:** `\subsection{El sesgo hacia un módulo era un efecto conjunto: encoder y fuente de conocimiento}`
- **Problema:** (e)+(c) título que adelanta el hallazgo con dos puntos; «era» es historia.
- **Propuesta:** `\subsection{Origen del sesgo hacia \texttt{apple}}`
- **Severidad:** baja.

- **Dónde:** `06:85–86` (dentro del bloque `06:78–90`, resto de historia ya conocido; este es texto nuevo concreto)
- **Texto actual:** `El conocimiento del especialista debe estar en el idioma en que el grupo pregunta; acumular experticia que nadie consulta no mejora al grupo.`
- **Problema:** (d)+(m) aforismo que repite `06:78–80` («ayuda solo si el conocimiento nuevo coincide con el lenguaje de las consultas»).
- **Propuesta:** quitar.
- **Severidad:** baja.

- **Dónde:** `06:99–134` (lista de la lectura desde Wegner)
- **Texto actual:** los cuatro arranques en negrita: `\textbf{Un grupo más grande necesita más interacción para conocerse.}` (la propuesta: `\textbf{Conocerse cuesta interacción.}`), `\textbf{El orden de las experiencias afecta la velocidad, no el destino.}`, `\textbf{La comunicación distintiva forma mejor directorio.}`, `\textbf{El rechazo colectivo escala.}` (la propuesta: `\textbf{El rechazo colectivo se sostiene con ocho dominios.}`); y los cuerpos de `06:108–112`, `06:118–122`, `06:124–133`.
- **Problema:** (e) cuatro eslóganes en negrita; (j9) `108–112` repite `05:240–246`; (b)+(d) `120–122` «La palanca no es más vocabulario … sino mejores señas» repite `06:78–80`; (i)+(j)+(d) `126` «casi exacta», `130–133` repite los dos falsos de `horse7` (ya en `05:321–322`, `06:13–14`, `06:243–245`, `07:19–20`) y cierra con «el grupo sigue sin inventar referentes» (ya en `02:293–294`, `03:367`, `03:385–386`).
- **Propuesta:**
  ```latex
  \begin{itemize}
      \item \textbf{Interacción.}
      Con ocho módulos, 10 consultas por dominio dejan la precisión madura en 81.2\%, y
      hace falta el banco completo ($\approx$50 por dominio) para alcanzar el 93.0\%.
      Formar el directorio cuesta más donde las especialidades se solapan, como muestra el
      punto sobre las señas distintivas.

      \item \textbf{Orden.}
      Todas las condiciones de presentación convergen al mismo directorio
      (Sección~\ref{sec:formacion}): la estructura final depende de qué se presenció, y el
      orden solo determina cuándo el directorio se vuelve utilizable.

      \item \textbf{Señas distintivas.}
      Las clases cuyas consultas usan léxico exclusivo (\texttt{cup}, \texttt{tomato},
      \texttt{car}) alcanzan 98--100\%; las que preguntan con léxico compartido
      (\texttt{pear}, \texttt{horse}) quedan en 76 y 88\%.
      En términos de Wegner, la asignación de información funciona en la medida en que
      quien pregunta aporta las señas del dominio (véase el resultado de enriquecimiento,
      Sección~\ref{sec:disc-dominancia}).

      \item \textbf{Rechazo colectivo.}
      Con ocho especialistas y siete clases contrarias por módulo, el contenido acepta
      pocos falsos: ninguno con el llenado de un latente por imagen en todo el rango de
      $N$, y 5 de 656 imágenes de test con 16 variantes, todas entre animales (vacas y
      caballos aceptados por \texttt{dog}, un caballo por \texttt{cow}); el directorio
      visual comete dos falsos enrutamientos de 656, hacia la clase vecina.
  \end{itemize}
  ```
- **Severidad:** baja.

- **Dónde:** `06:142`
- **Texto actual:** `Reconocer una pista no consulta un almacén aparte: es leer la asociación.`
- **Problema:** (b)+(c).
- **Propuesta:** `Reconocer una pista es leer la asociación, sin consultar un almacén aparte.`
- **Severidad:** baja.

- **Dónde:** `06:226–230` (limitación (a))
- **Texto actual:**
  ```latex
  Un árbitro más amplio (que el contenido decida entre los tres mejores candidatos del
  directorio) empeora el ruteo de texto (96.8 $\to$ 93.6\,\% de acierto, experimento 15):
  el índice calibrado compara mejor que la activación del contenido, y la abstención por
  margen de score quita más de un acierto por cada error que evita, a cualquier umbral
  (1.2 con $\delta = 0.05$, 8 con $\delta = 0.5$). La doble compuerta se queda como está.
  ```
- **Problema:** (g)+(h) tres paréntesis, dos puntos y una coordinación en una oración.
- **Propuesta:**
  ```latex
  Un árbitro más amplio, en el que el contenido decide entre los tres mejores candidatos
  del directorio, empeora el ruteo de texto (96.8 $\to$ 93.6\,\%, experimento 15): el
  índice calibrado compara mejor que la activación del contenido.
  La abstención por margen de score quita más de un acierto por cada error que evita, a
  cualquier umbral (1.2 con $\delta = 0.05$, 8 con $\delta = 0.5$).
  La doble compuerta se queda como está.
  ```
- **Severidad:** baja.

- **Dónde:** `06:288–294` (limitación (e))
- **Texto actual:**
  ```latex
  \paragraph{(e) Partición a nivel de imagen.}
  La partición train/test se realizó a nivel de archivo de imagen, no a nivel de objeto
  físico de ETH-80; verificado sobre la partición persistida, los diez objetos de cada
  clase aportan vistas a ambos lados (solape de instancias del 100\%,
  Sección~\ref{sec:dataset}).
  Las cifras visuales de este reporte (96.2\% de enrutamiento, evocación top-3) miden
  por tanto generalización a \emph{vistas nuevas de objetos conocidos}.
  ```
- **Problema:** (j13) repite `04:16–25` casi palabra por palabra.
- **Propuesta:**
  ```latex
  \paragraph{(e) Partición a nivel de imagen.}
  La partición train/test es por archivo de imagen, no por objeto físico, y los diez
  objetos de cada clase aportan vistas a ambos lados (Sección~\ref{sec:dataset}); las
  cifras visuales de este reporte (96.2\% de enrutamiento, evocación top-3) miden
  generalización a \emph{vistas nuevas de objetos conocidos}.
  ```
  (`06:295–310` siguen igual.)
- **Severidad:** baja.

- **Dónde:** `06:305`
- **Texto actual:** `La brecha no vive en clases sino en objetos concretos: 71 de los 80 objetos reservados`
- **Problema:** (b).
- **Propuesta:** `La brecha se concentra en objetos concretos: 71 de los 80 objetos reservados`
- **Severidad:** baja.

### 07_conclusiones.tex

- **Dónde:** `07:85–90` (en la propuesta de replanteamiento, 5d)
- **Texto actual (propuesta):**
  ```latex
  En resumen, los resultados muestran que las Memorias Asociativas Entrópicas de Pineda y
  Morales son una base suficiente para construir un sistema distribuido de memoria
  transactiva de ocho especialistas, bidireccional y con rechazo controlado, sin recurrir a
  modelos de aprendizaje profundo supervisado para la toma de decisiones; y que sus límites
  viven en las representaciones que alimentan a las memorias, no en el mecanismo asociativo
  ni en la maquinaria transactiva.
  ```
- **Problema:** (m)+(j1)+(g) cierre de una sola oración de seis líneas con «; y que», y quinta aparición de «en las representaciones, no en el mecanismo».
- **Propuesta:**
  ```latex
  Las Memorias Asociativas Entrópicas de Pineda y Morales bastan para construir un
  sistema distribuido de memoria transactiva de ocho especialistas, bidireccional y con
  rechazo, sin modelos supervisados en la toma de decisiones.
  Sus límites están en las representaciones que alimentan a las memorias.
  ```
- **Severidad:** media (es el cierre de la tesis y repite literalmente el resumen y la «Respuesta»).

- **Dónde:** `07:12–28` («Logros principales»)
- **Texto actual (fragmentos):** `\textbf{precisión temprana del 90.0\%}`, `\textbf{precisión madura del 93.0\%}`, `\textbf{13.8\%}`, `\textbf{96.2\%}`, `\textbf{dos falsos enrutamientos}`, `\textbf{97.4\%}`, `su directorio alcanzó el balance perfecto: \textbf{3.000 de 3.000 bits} de entropía.`, `\textbf{89.2\%}`, y `La especificidad del contenido fue casi perfecta: con siete clases contrarias por módulo, ningún falso aceptado al llenar con un latente por imagen, y 5 de 656 imágenes de test (0.8\%), todas entre animales, con el llenado de 16 variantes.`
- **Problema:** (e')+(i)+(c) ocho negritas en un párrafo; «balance perfecto» y «casi perfecta» con la cifra al lado y anunciadas con dos puntos.
- **Propuesta:** quitar las ocho `\textbf{}`; `su directorio quedó en el máximo de entropía, 3.000 de 3.000 bits.`; y
  ```latex
  Con siete clases contrarias por módulo, el contenido no aceptó ningún falso al llenar
  con un latente por imagen, y aceptó 5 de 656 imágenes de test (0.8\%), todas entre
  animales, con el llenado de 16 variantes.
  ```
- **Severidad:** baja.

- **Dónde:** `07:30–31` (en la propuesta de replanteamiento, 5b)
- **Texto actual (propuesta):** `Sí: un sistema de memoria transactiva hecho solo de memorias asociativas entrópicas reparte, recuerda y rechaza en ocho dominios.`
- **Problema:** (c) «Sí:» es el anuncio con dos puntos antes de la revelación.
- **Propuesta:** `Un sistema de memoria transactiva hecho solo de memorias asociativas entrópicas reparte, recuerda y rechaza en ocho dominios.`
- **Severidad:** baja.

- **Dónde:** `07:59–67` (en la propuesta de replanteamiento, 5c)
- **Texto actual (propuesta):**
  ```latex
  \paragraph{Lecciones.}
  Primero, la representación pesa tanto como el mecanismo: los límites observados están
  en las representaciones, no en las memorias.
  Segundo, los sesgos observados en un hemisferio pueden originarse en el otro: el
  sesgo ``léxico'' hacia \texttt{apple} era en buena parte solapamiento latente del
  encoder.
  Tercero, la fidelidad del pipeline es un resultado en sí mismo: todos los números
  reportados son trazables a corridas del sistema actual, sin vectores sintéticos ni
  decisiones fuera de las memorias.
  ```
- **Problema:** (f)+(j1)+(c) «Primero: / Segundo: / Tercero:» y la primera lección repite la «Respuesta» de veinte líneas antes.
- **Propuesta:**
  ```latex
  \paragraph{Lecciones.}
  Los sesgos observados en un hemisferio pueden originarse en el otro: el sesgo
  ``léxico'' hacia \texttt{apple} era en buena parte solapamiento latente del encoder.
  Y la fidelidad del pipeline es un resultado en sí mismo: todos los números reportados
  son trazables a corridas del sistema actual, sin vectores sintéticos ni decisiones
  fuera de las memorias.
  ```
- **Severidad:** baja.

## 4. Dudas

- No abrí los archivos de los experimentos 13, 14 ni 16; las propuestas de `06` (b) y (e) solo reordenan cifras que ya están en la tesis. La sustitución de «presumiblemente porque el fondo liso…» por la causa medida se apoya en `05:350–355` («El experimento 14 localizó la causa»); si el autor prefiere la cautela, conviene entonces quitar «localizó la causa» de `05`, porque hoy las dos secciones se contradicen.
- La tabla propuesta para `05` redondea a un decimal las distancias del README (22.86 → 22.9, etc.) y omite los intervalos. La fila «Especialista» corresponde al brazo «T-oraculo» del README en imagen→texto (la prosa actual ya lo llama «el especialista»). La fila «Fuera de dominio» convierte los porcentajes del README (5.0, 12.5, 20.0 % de 40) en conteos (2, 5, 8), como hace la prosa.
- En `05:445–447` («Las versiones anteriores del sistema guardaban…») el relato de versión está amparado por la excepción de la regla 3 (cambio a una sola hetero); no propongo texto, pero «Las versiones anteriores» puede leerse como historia. Lo dejo al autor.
- Los conteos de la tabla 1 son de lectura, no de script: en (b) y (d) la frontera entre contraste informativo y giro retórico es de criterio, y otro lector puede mover tres o cuatro casos de columna.
- `\paragraph{}` de `04` (etapas del pipeline), `07` y las limitaciones (a)–(i) los dejo porque son estructura y no eslogan; si el autor quiere menos titulitos, los de `07:43` («Frente a una EHAM única») y `07:50` («Una memoria de contenido por módulo») podrían fundirse en «Logros principales».
