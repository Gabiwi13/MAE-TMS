# Propuesta viejo/nuevo: la tesis sin la comparación «de 3 a 8 módulos»

**Estado:** aprobada el 1 nov 2026; se aplica junto con las correcciones del consejo de redacción. Subtítulo aprobado: «Ocho módulos sobre ETH-80 completo».

**Decisión** (1 nov). La tesis presenta el sistema actual, de ocho módulos, sin contarse como «segunda versión» que escala desde tres. La pregunta de investigación pasa a ser si un sistema transactivo hecho de memorias asociativas entrópicas reparte, recuerda y rechaza con ocho dominios, y dónde están sus límites. Todo lo que comparaba con el sistema de tres módulos sale, porque ese sistema ya no existe y sus cifras no se pueden volver a medir.

**Qué no cambia:** ninguna cifra del sistema actual. Las comparaciones que son resultado de un experimento de la tesis se quedan: la ablación (lectura cruda contra B1), la comparación con una sola EHAM, el experimento 13 y la arquitectura con una sola memoria de contenido.

**Archivos:** `main.tex` (resumen), `01_introduccion.tex`, `05_resultados.tex`, `06_discusion.tex`, `07_conclusiones.tex`. El texto viejo se cita abreviado; los números de línea son los del `.tex8` actual.

---

## 1. Resumen (`main.tex:55–85`)

**Viejo:** empieza con «Este trabajo describe la segunda versión del sistema distribuido de memoria transactiva…», sigue con «El sistema escala de tres a ocho módulos especialistas…» y cierra con «Los resultados muestran que la maquinaria transactiva escala con el número de módulos; los límites observados provienen de la representación semántica y de la separabilidad del espacio latente, no del mecanismo asociativo.»

**Nuevo:**
```latex
Este trabajo presenta EAM-TMS, un sistema distribuido de memoria transactiva construido
con Memorias Asociativas Entrópicas en su variante ponderada (W-EAM)
\cite{pineda2021entropic,pineda2022weighted} y su extensión heteroasociativa (EHAM)
\cite{morales2024hetero,morales2025missing}.
El sistema tiene \textbf{ocho módulos especialistas}, uno por cada categoría del conjunto
de datos ETH-80 \cite{leibe2003eth80}
(\textit{apple}, \textit{car}, \textit{cow}, \textit{cup}, \textit{dog}, \textit{horse},
\textit{pear}, \textit{tomato}).
Cada módulo guarda su contenido en una sola memoria heteroasociativa entre palabras e
imágenes y lleva dos directorios, uno textual y uno visual, con las transacciones en que
participa.
Un mediador inicial (TME) coordina las interacciones tempranas y deja de ser necesario
cuando los directorios de los módulos bastan para enrutar.
Las memorias operan bidireccionalmente entre representaciones textuales (fastText 300D
\cite{bojanowski2017fasttext}, con vocabulario extraído de ConceptNet 5.7
\cite{speer2017conceptnet} y \emph{cuantización por magnitud} en 16 niveles)
e imágenes (codificadas por ResNet18 \cite{he2016resnet}).
La arquitectura modela computacionalmente los tres mecanismos de la Memoria Transactiva
de Wegner \cite{wegner1987transactive}: la actualización del directorio de experticia,
la asignación de información y la coordinación de la recuperación.
El sistema alcanza una precisión temprana del 90.0\% y una precisión madura del 93.0\%
con la lectura normalizada B1 del directorio (ablación de calibración, con un
directorio compartido; banco de 411 consultas, $N{=}400$, 5 semillas), y la lectura B1
reduce la participación del módulo \textit{apple} del 20.5\% de la lectura cruda al
13.8\% (ideal 12.5\%).
El hemisferio visual enruta el 96.2\% de las imágenes de prueba (631 de 656), con un
rechazo del 3.5\% y dos falsos enrutamientos; con objetos nunca vistos, la cobertura de
punta a punta es del 89.2\%, con dos falsos de 3280.
Frente a una sola memoria con las ocho clases, la partición en especialistas recuerda con
más fidelidad y acepta menos consultas fuera de dominio.
Los límites observados provienen de las representaciones (el léxico compartido entre
clases y la separabilidad del espacio latente), no del mecanismo asociativo.
```

**Por qué:** quita «segunda versión», «escala de tres a ocho» y «escala con el número de módulos». Agrega la memoria de contenido única, la generalización a objetos nuevos (89.2 %, ya en conclusiones) y la comparación con una sola EHAM, que sostienen la pregunta nueva con mediciones actuales. El «20.5 → 13.8» se queda: compara dos lecturas del mismo sistema (ablación).

---

## 2. Introducción (`01_introduccion.tex`)

### 2a. Pregunta de investigación (líneas 26–36)

**Viejo:** «Un reporte previo de este proyecto mostró que un sistema de tres módulos especialistas… Este reporte técnico aborda la pregunta que ese resultado deja abierta:» y la cita «¿La maquinaria transactiva … \emph{escala} cuando el número de módulos especialistas crece de tres a ocho…? Y si aparecen límites, ¿provienen del mecanismo asociativo o de las representaciones que lo alimentan?»

**Nuevo:**
```latex
Este trabajo pregunta si esa organización puede construirse solo con memorias
asociativas:

\begin{quote}
¿Puede un sistema de memoria transactiva construido sobre memorias asociativas
entrópicas repartir consultas de texto e imagen entre ocho especialistas, recordar el
contenido asociado y rechazar lo que no conoce, sin clasificadores supervisados? Y donde
aparezcan límites, ¿provienen del mecanismo asociativo o de las representaciones que lo
alimentan?
\end{quote}
```

### 2b. Línea 41

**Viejo:** «…se compone en esta versión de» → **Nuevo:** «…se compone de»

### 2c. Encabezado de contribuciones (línea 70)

**Viejo:** «Este trabajo aporta cinco contribuciones concretas respecto a la versión anterior:» → **Nuevo:** «Este trabajo aporta cinco contribuciones:»

### 2d. Contribución 1 (líneas 72–78)

**Viejo:** «\textbf{Escalado a ocho módulos especialistas.} El sistema pasa de 3 a 8 categorías…, con el encoder visual reentrenado de forma determinista, el vocabulario semántico regenerado y el banco de evaluación extendido a 411 consultas… escalan a ocho módulos, con el registro por transacción y la coordinación de la contribución~3.»

**Nuevo:**
```latex
    \item \textbf{Un sistema transactivo de ocho especialistas.}
    Ocho módulos, uno por cada clase de ETH-80, cada uno con una sola memoria de
    contenido heteroasociativa y dos directorios, evaluados con un banco de 411
    consultas ($\approx$50 por dominio).
    Los directorios, la lectura normalizada B1, el rechazo por containment y la
    coordinación punto a punto funcionan con los ocho dominios, con el registro por
    transacción y la coordinación de la contribución~3.
```

### 2e. Contribución 2 (líneas 80–86)

**Viejo:** «La binarización por signo de fastText (que usaba 2 de los 16 niveles disponibles) se reemplaza por una cuantización por magnitud $v/S$…»

**Nuevo:**
```latex
    \item \textbf{Cuantización por magnitud de las pistas semánticas.}
    Las pistas fastText se cuantizan por magnitud, $v/S$ sobre una escala global
    persistida, y pueblan los 16 niveles; una binarización por signo usaría solo 2.
    Con esta representación, sin tocar la maquinaria asociativa, la precisión temprana de
    8 clases es del 90.0\%.
```

### 2f. Contribución 4 (líneas 100–106)

**Viejo:** «…Se auditó que ninguna decisión provenga de mecanismos ajenos a las memorias: se eliminó el único vector sintético del vocabulario (que además distorsionaba la escala global de cuantización), … y todos los números reportados provienen de corridas posteriores a esa auditoría…»

**Nuevo:**
```latex
    \item \textbf{Auditoría de fidelidad del pipeline.}
    Ninguna decisión proviene de mecanismos ajenos a las memorias: el vocabulario no
    contiene vectores sintéticos, el código de Pineda \& Morales permanece byte-idéntico
    (salvo una guarda que evita cargar sus clasificadores y no toca ninguna operación de
    memoria), y todos los números reportados son trazables a corridas del sistema
    actual, sobre datos no fabricados.
```

### 2g. Contribución 5 (líneas 107–112)

**Viejo:** «\textbf{Evaluación experimental del sistema escalado.} Se reportan el estudio de calibración…, junto con el costo computacional de la reproducción íntegra.»

**Nuevo:**
```latex
    \item \textbf{Evaluación experimental.}
    Se reportan el estudio de calibración del directorio (9 condiciones $\times$
    $N \in \{50,100,200,400\}$ $\times$ 5 semillas), el barrido de parámetros nativos
    $\iota \times \kappa$, la curva de formación del directorio, la curva de capacidad
    de llenado, el hemisferio visual completo, la comparación con una sola EHAM y la
    verificación de una sola memoria de contenido por módulo, junto con el costo
    computacional de la reproducción íntegra.
```

---

## 3. Resultados (`05_resultados.tex`)

| Línea | Viejo | Nuevo |
|---|---|---|
| 52 | «Igual que en el sistema de tres módulos, la lectura cruda del directorio (A) pierde…» | «La lectura cruda del directorio (A) pierde…» |
| 231–234 | «\paragraph{Hallazgo principal: a ocho módulos, 10 consultas por clase no bastan.} A diferencia del sistema de tres módulos (donde el orden intercalado cruzaba el umbral del 90\% en $k \approx 13$ interacciones), \textbf{ninguna condición alcanza el umbral del 90\%}…» | «\paragraph{Hallazgo principal: con ocho módulos, 10 consultas por clase no bastan.} \textbf{Ninguna condición alcanza el umbral del 90\%}…» |
| 244–245 | «Esta invariancia del destino replica el resultado de tres módulos y confirma que el directorio acumula evidencia conmutativa…» | «Esta invariancia del destino muestra que el directorio acumula evidencia conmutativa…» |
| 284–287 | «\paragraph{Especificidad perfecta.} La tasa de falsos aceptados es del \textbf{0\% en todo el rango} de $N$ probado, ahora con siete clases contrarias por módulo en lugar de dos: …» | «\paragraph{Especificidad.} Con el llenado de un latente por imagen, la tasa de falsos aceptados es del \textbf{0\% en todo el rango} de $N$ probado, con siete clases contrarias por módulo: …» |
| 307–308 | «(4.2\% con 4 variantes en el experimento 13; $\approx$50\% en la versión de tres módulos)» | «(4.2\% con 4 variantes en el experimento 13)» |

La frase del costo (línea 551, «El crecimiento respecto a la versión de tres módulos…») se reescribe con la tabla nueva del costo.

---

## 4. Discusión (`06_discusion.tex`)

### 4a. Título y apertura (líneas 5–23)

**Viejo:** «\subsection{La maquinaria transactiva escala; la representación era el límite}» y «El resultado central de esta versión es una separación limpia de responsabilidades. Al pasar de tres a ocho módulos, \emph{ningún} componente de la maquinaria transactiva requirió cambios de mecanismo: … Lo que sí golpeó el escalado fue la \emph{representación}: la binarización por signo no separa bien ocho clases. La causa no estaba en las memorias sino en el alfabeto: $\mathrm{sign}(v)$ usaba 2 de los 16 niveles disponibles, y ocho categorías con léxico solapado … no caben en ese margen.»

**Nuevo:**
```latex
\subsection{La maquinaria transactiva funciona con ocho dominios; la representación es el límite}
\label{sec:disc-escala}

El resultado central es una separación limpia de responsabilidades.
Con ocho dominios, los componentes de la maquinaria transactiva (los directorios
heteroasociativos, la lectura B1, el rechazo por containment, la actualización
perspectival del directorio y la coordinación punto a punto) funcionan sin ajustes por
dominio, y el directorio visual alcanza el balance perfecto (3.000 de 3.000 bits) con
dos falsos enrutamientos en 656, ambos del mismo objeto.
Los límites aparecen en la \emph{representación}.
Una binarización por signo usaría 2 de los 16 niveles del alfabeto; la cuantización por
magnitud sobre una escala global (Sección~\ref{sec:pipeline-semantico}) los puebla
todos, y con ella la precisión temprana es del 90.0\% \emph{sin tocar una línea de la
maquinaria asociativa}.
```
El párrafo sigue igual desde «La Figura~\ref{fig:espacio-semantico} muestra el espacio semántico resultante…».

**Por qué:** quita «esta versión», «al pasar de tres a ocho», «golpeó el escalado» y la afirmación de que la binarización por signo no separa ocho clases, que hoy no tiene fuente. El `\label` no cambia, así que las referencias siguen valiendo.

### 4b. B1 (líneas 38 y 48–50)

**Viejo:** «\subsection{La normalización necesaria sigue siendo B1, también a ocho módulos}» y «El escalado refuerza esta lectura en dos direcciones. Primero, la brecha cruda-B1 persiste con $K = 8$ (85.2\% frente a 93.0\%): el sesgo de masa no era un artefacto del caso de tres módulos.»

**Nuevo:** «\subsection{La normalización necesaria es B1}» y «Dos datos sostienen esta lectura. Primero, la brecha cruda-B1 es de 7.8 puntos con ocho módulos (85.2\% frente a 93.0\%).»

### 4c. Lectura desde Wegner (líneas 96–106 y 124)

**Viejo (introducción):** «…releen los mecanismos de Wegner~\cite{wegner1987transactive} a una escala de grupo mayor:» → **Nuevo:** «…releen los mecanismos de Wegner~\cite{wegner1987transactive} con un grupo de ocho miembros:»

**Viejo (primer punto):** «\textbf{Un grupo más grande necesita más interacción para conocerse.} Con tres módulos, 10 consultas por dominio bastaban para cruzar el 90\%…; con ocho módulos ese mismo volumen se queda en 81.2\%, y hace falta el banco completo… El costo de formación del directorio crece con el número de especialidades y con el solapamiento entre ellas, no solo con el número de miembros.»

**Nuevo:**
```latex
    \item \textbf{Conocerse cuesta interacción.}
    Con ocho módulos, 10 consultas por dominio dejan la precisión madura en 81.2\%, y
    hace falta el banco completo ($\approx$50 por dominio) para alcanzar el 93.0\%.
    Formar el directorio cuesta más donde las especialidades se solapan, como muestra el
    punto sobre la comunicación distintiva.
```

**Viejo (último punto):** «\textbf{El rechazo colectivo escala.}» → **Nuevo:** «\textbf{El rechazo colectivo se sostiene con ocho dominios.}»

**Por qué:** «crece con el número de especialidades» comparaba grupos de 3 y 8; sin esa comparación no hay medición que lo sostenga. Lo del solapamiento sí lo sostiene el punto de la comunicación distintiva (98–100 % contra 76 y 88 %).

---

## 5. Conclusiones (`07_conclusiones.tex`)

### 5a. Apertura (líneas 4–7)

**Viejo:** «Este trabajo describió la versión de ocho módulos de EAM-TMS, un sistema distribuido de memoria transactiva construido sobre…» → **Nuevo:** «Este trabajo presentó EAM-TMS, un sistema distribuido de memoria transactiva de ocho módulos construido sobre…»

### 5b. Respuesta a la pregunta de investigación (líneas 30–41)

**Viejo:** «La maquinaria transactiva \emph{escala}: directorios, … pasan de 3 a 8 módulos sin cambios de mecanismo. Los límites encontrados estaban en las \emph{representaciones}: la binarización por signo (resuelta con la cuantización por magnitud…), la separabilidad del espacio latente del encoder (cuyo reentrenamiento resolvió el sesgo hacia \texttt{apple}: 20\% $\to$ 13.8\%), y la asimetría léxica… El costo de la escala aparece donde la teoría de Wegner lo predice: un grupo con más especialidades necesita más interacciones, y más distintivas, para formar su directorio.»

**Nuevo:**
```latex
\paragraph{Respuesta a la pregunta de investigación.}
Sí: un sistema de memoria transactiva hecho solo de memorias asociativas entrópicas
reparte, recuerda y rechaza en ocho dominios.
Los directorios, la lectura B1, el rechazo por containment, la actualización del
directorio y la coordinación punto a punto funcionan sin componentes supervisados de
decisión.
Los límites encontrados están en las \emph{representaciones}: la asimetría léxica de la
fuente de conocimiento, que fija el techo de las clases con vocabulario compartido, y la
separabilidad del espacio latente del encoder, que explica buena parte del sesgo hacia
\texttt{apple} con la lectura cruda.
El costo de repartir el conocimiento aparece donde la teoría de Wegner lo predice: el
grupo necesita interacciones, y distintivas, para formar su directorio.
```

### 5c. Lecciones (líneas 59–67)

**Viejo:** «\paragraph{Lecciones de esta versión.} Primero, la representación pesa tanto como el mecanismo: dos de los tres límites observados se resolvieron cambiando representaciones sin tocar las memorias. Segundo, … Tercero, la fidelidad del pipeline es un resultado en sí mismo: la auditoría que eliminó el único vector sintético del sistema también corrigió la escala global de cuantización, e hizo trazables todos los números reportados.»

**Nuevo:**
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

### 5d. Cierre (líneas 84–90)

**Viejo:** «…construir un sistema distribuido de memoria transactiva que escala a ocho especialistas, bidireccional y con rechazo controlado, …; y que, cuando el escalado encuentra límites, estos viven en las representaciones que alimentan a las memorias y no en el mecanismo asociativo ni en la maquinaria transactiva.»

**Nuevo:**
```latex
En resumen, los resultados muestran que las Memorias Asociativas Entrópicas de Pineda y
Morales son una base suficiente para construir un sistema distribuido de memoria
transactiva de ocho especialistas, bidireccional y con rechazo controlado, sin recurrir a
modelos de aprendizaje profundo supervisado para la toma de decisiones; y que sus límites
viven en las representaciones que alimentan a las memorias, no en el mecanismo asociativo
ni en la maquinaria transactiva.
```

---

## Lo que se queda

- El subtítulo de la portada, «Versión de 8 módulos (ETH-80 completo)», que ya aprobaste con el título. Si prefieres otro sin la palabra «versión», por ejemplo «Ocho módulos sobre ETH-80 completo», es un cambio de una línea.
- La sección del costo computacional: se reescribe con la medición nueva.
