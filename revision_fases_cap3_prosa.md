# Revisión por fases, parte `cap3`: Capítulo 3, Desarrollo del Proyecto

Base: `59cca47` (`una-hetero`). Archivos tocados: `.tex8/secciones/03_arquitectura.tex`, `.tex8/secciones/04_metodologia.tex`, el bloque del Capítulo 3 de `.tex_uacj/generar_capitulos.py` y `.tex_uacj/Capitulo3.tex` (regenerado). `generar_capitulos.py` termina con código 0 y «líneas de .tex8 que no aparecen en la salida: 0»; `Capitulo2.tex`, `Capitulo4.tex` y `Capitulo5.tex` salen idénticos a la base. No hay `xelatex` en el entorno: se revisó el balance de llaves, de `\begin`/`\end` y de `$`.

## 1. Mapa de secciones (plantilla UACJ)

| antes | ahora |
|---|---|
| 3.1 Producto propuesto (3.1.1 Componentes, 3.1.2 Diagramas, 3.1.3 Operaciones) | igual; cambia el párrafo de apertura y la justificación de B1 pasa a 3.4 |
| 3.2 Descripción de la metodología (párrafo de apertura) | 3.2 con 3.2.1 Las cinco fases (tabla del arco) y 3.2.2 Métricas de evaluación |
| — | 3.3 Fase 1: prototipo de tres módulos |
| «Lectura normalizada por conteo» (justificación) en 3.1.3; nueve condiciones en «Organización» | 3.4 Fase 2: lectura del directorio |
| 3.3 a 3.8 y 3.10 (Conjunto de datos … Auditoría, Organización) | 3.5 Fase 3: escalado a ocho módulos, con 3.5.1 a 3.5.7 |
| 3.9 Métricas de evaluación | 3.2.2 |
| — | 3.6 Fase 4: experimentos de propiedades |
| — | 3.7 Fase 5: laboratorio en tiempo real |

Las subsecciones 3.5.1 a 3.5.6 (Conjunto de datos, Representación de texto, Percepción visual, Banco, Parámetros, Auditoría) conservan su texto sin cambios; solo bajan un nivel en `.tex8` (de `\subsection` a `\subsubsection`). En `.tex_uacj` siguen siendo `\subsection`, así que la línea `\subsection{Conjunto de datos}` sigue apareciendo en `Capitulo3.tex`.

## 2. Generador

Antes, el bloque partía `04_metodologia.tex` en `\subsection{Conjunto de datos}`. Ahora parte en `\subsection{Fase 1: prototipo de tres módulos}`: lo anterior (apertura, «Las cinco fases» y «Métricas») queda dentro de «Descripción de la metodología» sin cambiar de nivel, y de la fase 1 en adelante todo sube un nivel (cada fase es `\section`; los métodos de la fase 3, `\subsection`). Los bloques de los capítulos 2, 4 y 5 no se tocaron.

## 3. Texto viejo y nuevo

### 3.1 `03_arquitectura.tex`, apertura

Viejo:
```latex
Esta sección describe la arquitectura completa del sistema distribuido de memoria
transactiva de ocho módulos.
Se presentan primero los componentes (Sección~\ref{sec:componentes}), luego los tres
diagramas de flujo que muestran el llenado de memorias, la fase temprana y la fase
madura (Sección~\ref{sec:diagramas}), y finalmente la formalización de todas las
operaciones del sistema (Sección~\ref{sec:operaciones}).
```
Nuevo (quita el metatexto, patrón (o) de `antipatrones.md`, y ubica el producto en el arco):
```latex
El producto propuesto es el sistema de ocho módulos con el que cerró la fase 3, más los
cambios que dejaron los experimentos de la fase 4 (Sección~\ref{sec:metodologia}).
Con él se obtuvieron las cifras de ocho módulos del reporte, salvo donde se indica otra
versión.
```

### 3.2 `03_arquitectura.tex`, «Lectura normalizada por conteo»

La definición y la ecuación `eq:b1` se quedan en 3.1.3, porque el Capítulo 1, el Capítulo 2 y `ConclusionObjetivoGeneral.tex` citan B1 como parte de `sec:operaciones`. El párrafo «Por qué dividir entre el conteo» pasa a 3.4 (Fase 2), con los conteos de tres módulos además de los de ocho. En su lugar queda:
```latex
Esta es la \textbf{única normalización externa} del sistema de directorios.
El conteo $c_k$ se guarda como un contador aparte, pero no agrega información, porque es el
número de veces que se registró «conoce» para el módulo $k$, el mismo en todas las
características de la relación.
La razón para dividir entre el conteo y la comparación con las demás lecturas que se
probaron forman la fase 2 (Sección~\ref{fase2:lectura}).
```

### 3.3 Apertura de la metodología

Viejo:
```latex
\section{Metodología}
\label{sec:metodologia}

Esta sección describe el conjunto de datos y su partición, la representación de texto
y de imagen, el banco de consultas, los parámetros de las memorias, la auditoría de
trazabilidad, las métricas y la organización de los experimentos.
En adelante, \emph{hemisferio textual} es el camino que va de una frase a los
directorios de texto y a las memorias de contenido, y \emph{hemisferio visual}, el que
va de una imagen a los directorios visuales y a las memorias de contenido.
El término nombra un camino de procesamiento y no supone ninguna lateralización.
```

Nuevo (apertura, 3.2.1 y 3.2.2):
```latex
\section{Metodología}
\label{sec:metodologia}

La investigación avanzó en cinco fases, y cada una partió de lo que dejó la anterior.
En adelante, \emph{hemisferio textual} es el camino que va de una frase a los
directorios de texto y a las memorias de contenido, y \emph{hemisferio visual}, el que
va de una imagen a los directorios visuales y a las memorias de contenido.
El término nombra un camino de procesamiento y no supone ninguna lateralización.

% ---------------------------------------------------------------
\subsection{Las cinco fases}
\label{fase:arco}

La fase 1 (junio de 2026) construyó un prototipo con tres módulos, uno por clase de
ETH-80 (\texttt{apple}, \texttt{horse} y \texttt{car}), para comprobar que el
directorio se forma con el uso, desde vacío, con lo que el TME media en la fase
temprana.
La fase 2, con el mismo prototipo, comparó varias maneras de leer el directorio en la
fase madura y adoptó la lectura normalizada por conteo, B1.
En la fase 3 (julio) el sistema pasó a las ocho clases de ETH-80.
Ese paso cambió a la vez el número de módulos, el codificador, la cuantización de las
pistas de texto, las memorias por módulo y el banco de consultas, así que las cifras de
las fases 1 y 2 no se comparan con las de ocho módulos como si fueran un experimento
controlado.
La evidencia controlada sobre el tamaño sale de dos comparaciones hechas dentro del
sistema de ocho módulos: una sola EHAM contra la partición en módulos (experimento~11)
y una EHAM de dos clases contra una de ocho (experimento~12).
De agosto a noviembre, la fase 4 estudió las propiedades del sistema de ocho módulos
más allá del acierto.
Cuatro de sus resultados se incorporaron al sistema: los directorios perspectivales,
las 16 variantes por imagen, el umbral de energía y una sola memoria de contenido por
módulo.
El sistema que queda es el de la Sección~\ref{sec:arquitectura}.
Antes de esos cambios, en julio, la fase 5 conectó la versión v5 del sistema a un
micrófono y a una cámara.
Es una demostración de integración, sin cifras de acierto.
La Tabla~\ref{fase:tab-arco} resume la arquitectura de cada fase.

\begin{table}[H]
\centering
\caption[Arquitectura de cada fase de la investigación]{Arquitectura de cada fase de
la investigación.
Las memorias por módulo cuentan las de contenido y los directorios.
En la fase 3, la primera cifra es la del sistema de julio y la segunda, la del sistema
final.
En la fase 4, tres experimentos (8, 9 y 10) usan el protocolo anterior, con cinco
memorias por módulo y directorios iguales en todos los módulos.
La fase 2 adoptó B1 con tres módulos; su verificación con ocho usa la arquitectura de
la fase 3.}
\label{fase:tab-arco}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}p{2.3cm}cp{1.6cm}p{2.2cm}p{3.6cm}p{2.6cm}@{}}
\toprule
Fase & Módulos & Memorias por módulo & Cuantización del texto & Mediador y registro &
Banco \\
\midrule
1. Prototipo & 3 & 4 & por signo (2 de 16 niveles) & TME; directorio compartido &
80 consultas (27/27/26) \\
2. Lectura del directorio & 3 & 4 & por signo & TME; directorio compartido &
80 consultas, $N$ de 10 a 80 \\
3. Escalado & 8 & 5 / 3 & por magnitud (16 niveles) &
TME; directorio compartido / perspectival & 411 consultas; 656 imágenes de prueba \\
4. Propiedades & 8 & 3 & por magnitud & TME; directorios perspectivales &
411 consultas; 656 imágenes de prueba \\
5. Tiempo real (v5) & 8 & 5 & por magnitud & TME en el modo temprano &
frases habladas y cuadros de cámara \\
\bottomrule
\end{tabular}
\end{table}

% ---------------------------------------------------------------
\subsection{Métricas de evaluación}
\label{sec:metricas}

Las métricas son las mismas en todas las fases.
Con el número de módulos $K$ cambia la referencia.
El azar es $1/K$, y la entropía máxima del directorio es $\log_2 K$, que vale 1.585 bits
con tres módulos y 3 con ocho.
En este trabajo, \emph{precisión} es siempre la fracción de aciertos sobre las consultas
o imágenes evaluadas o, cuando se indica, sobre las aceptadas.

\begin{itemize}
    \item \textbf{Precisión temprana}: fracción de consultas en las que el módulo ganador de la fase temprana coincide con la clase real.
    \item \textbf{Precisión madura}: la misma fracción en la fase madura, con la lectura normalizada o con la cruda del directorio.
    \item \textbf{Tasa de rechazo}: fracción de consultas que el sistema no asigna a
    ningún módulo. Con $\kappa = 0$ no hay umbral sobre la puntuación; se rechaza lo que
    no tiene soporte (en la fase temprana, $s_k = 0$ en todos los módulos,
    ecuación~\eqref{eq:score-gated}; en la fase madura, ningún directorio alcanzable lo
    tiene o el destino no contiene la pista) y lo que no llega a ser pista (ningún token
    con vector fastText, o una imagen cuyo latente no alcanza $\tau$).
    \item \textbf{Concordancia temprana-madura} (ecuación~\eqref{eq:concordancia}): fracción de consultas cuyo ganador en la fase madura es el mismo que en la fase temprana.
    \item \textbf{Entropía del directorio} (ecuación~\eqref{eq:entropia-dir}): entropía de Shannon de la distribución de \textit{conteos} de los módulos especialistas, con máximo $\log_2 K$.
    \item \textbf{Conteos por módulo}: número de registros acumulados en el directorio transactivo por cada módulo especialista.
    \item \textbf{Participación del ganador}: fracción de victorias maduras obtenidas por cada módulo; el ideal balanceado es $1/K$, 12.5\,\% con ocho módulos.
    \item \textbf{Enrutamiento visual} (hemisferio visual): fracción de las imágenes de
    prueba que el directorio visual asigna al módulo de su clase. Se acompaña de la
    precisión sobre las imágenes aceptadas (sin contar los rechazos) y del número de
    \emph{falsos enrutamientos}, imágenes asignadas a otra clase.
    \item \textbf{Cobertura de punta a punta} (hemisferio visual): fracción de las
    imágenes de prueba que se enrutan a su clase y a las que, además, responde el módulo
    destino. El módulo responde cuando su recuperación $\beta$ desde el latente no deja
    columnas vacías en la proyección.
    \item \textbf{Evocación de dominio} (\textit{top-3 coseno}): sobre las primeras 15 imágenes de prueba de cada clase que el enrutamiento acepta, fracción de imágenes para las que al menos una de las tres etiquetas más cercanas en el espacio fastText pertenece al vocabulario de la clase real (recuperación inversa imagen $\to$ palabras). Una palabra compartida por dos vocabularios cuenta como acierto para las dos clases.
\end{itemize}

La fase 5 no usa estas métricas.
De ella se reportan latencias medidas una vez y el resultado de pruebas cualitativas
(Sección~\ref{fase5:laboratorio}).
```

Métricas, viejo (cambian la entropía máxima y la participación, que ahora dependen de $K$; «los ocho módulos» pasa a «todos los módulos»; se agrega la nota de la fase 5):
```latex
\subsection{Métricas de evaluación}
\label{sec:metricas}

Se emplearon las siguientes métricas. En este trabajo, \emph{precisión} es siempre la
fracción de aciertos sobre las consultas o imágenes evaluadas o, cuando se indica, sobre
las aceptadas.

\begin{itemize}
    \item \textbf{Precisión temprana}: fracción de consultas en las que el módulo ganador de la fase temprana coincide con la clase real.
    \item \textbf{Precisión madura}: la misma fracción en la fase madura, con la lectura normalizada o con la cruda del directorio.
    \item \textbf{Tasa de rechazo}: fracción de consultas que el sistema no asigna a
    ningún módulo. Con $\kappa = 0$ no hay umbral sobre la puntuación; se rechaza lo que
    no tiene soporte (en la fase temprana, $s_k = 0$ en los ocho módulos,
    ecuación~\eqref{eq:score-gated}; en la fase madura, ningún directorio alcanzable lo
    tiene o el destino no contiene la pista) y lo que no llega a ser pista (ningún token
    con vector fastText, o una imagen cuyo latente no alcanza $\tau$).
    \item \textbf{Concordancia temprana-madura} (ecuación~\eqref{eq:concordancia}): fracción de consultas cuyo ganador en la fase madura es el mismo que en la fase temprana.
    \item \textbf{Entropía del directorio}: entropía de Shannon de la distribución de \textit{conteos} de los módulos especialistas, con máximo $\log_2(8) = 3$ bits.
    \item \textbf{Conteos por módulo}: número de registros acumulados en el directorio transactivo por cada módulo especialista.
    \item \textbf{Participación del ganador}: fracción de victorias maduras obtenidas por cada módulo; el ideal balanceado es $1/8 = 12.5$\,\%.
    \item \textbf{Enrutamiento visual} (hemisferio visual): fracción de las imágenes de
    prueba que el directorio visual asigna al módulo de su clase. Se acompaña de la
    precisión sobre las imágenes aceptadas (sin contar los rechazos) y del número de
    \emph{falsos enrutamientos}, imágenes asignadas a otra clase.
    \item \textbf{Cobertura de punta a punta} (hemisferio visual): fracción de las
    imágenes de prueba que se enrutan a su clase y a las que, además, responde el módulo
    destino. El módulo responde cuando su recuperación $\beta$ desde el latente no deja
    columnas vacías en la proyección.
    \item \textbf{Evocación de dominio} (\textit{top-3 coseno}): sobre las primeras 15 imágenes de prueba de cada clase que el enrutamiento acepta, fracción de imágenes para las que al menos una de las tres etiquetas más cercanas en el espacio fastText pertenece al vocabulario de la clase real (recuperación inversa imagen $\to$ palabras). Una palabra compartida por dos vocabularios cuenta como acierto para las dos clases.
\end{itemize}
```


### 3.4 Fase 1 (nueva)
```latex
\subsection{Fase 1: prototipo de tres módulos}
\label{fase1:prototipo}

El prototipo usó tres clases de ETH-80, \texttt{apple}, \texttt{horse} y \texttt{car}.
El codificador era un ResNet18 con latente de 64 dimensiones, entrenado con las 984
imágenes de entrenamiento de esas tres clases, 328 por clase.
Cada módulo llevaba cuatro memorias:
\begin{itemize}
    \item una heteroasociativa de contenido entre etiquetas y latentes,
    $(300, 16 \leftrightarrow 64, 32)$;
    \item una homoasociativa de etiquetas, $(300, 16)$, y otra de latentes, $(64, 32)$,
    de las que salían los pesos de reconocimiento;
    \item un directorio de texto, $(300, 16 \to 3, 2)$.
\end{itemize}
El TME llevaba un directorio de texto y el único directorio visual del sistema.
Las pistas de texto se cuantizaban por signo, de modo que cada componente del vector
fastText pasaba a $-1$ o $+1$ y ocupaba 2 de los 16 niveles de la memoria.
Cada memoria de contenido se llenó por instancias, con 200 imágenes de su clase.
Un primer llenado con un solo latente promediado por clase se había descartado porque
la memoria devolvía siempre el mismo recuerdo
(\texttt{results/fase1\_tres\_modulos/exp5\_entropic\_prototype}).
Los parámetros eran $\iota = \kappa = \xi = 0$ y $\sigma = 0.1$, los mismos del sistema
final.

En la fase temprana, el TME difundía cada consulta a los tres módulos, cada uno la
puntuaba con la activación media con compuerta de contención (la de la
ecuación~\eqref{eq:score-gated}) y ganaba el de mayor puntuación.
Cada token de la consulta se registraba con el ganador en los cuatro directorios, el
del TME y los de los tres módulos, que recibían los mismos registros y formaban así un
solo \emph{directorio compartido}.
En la fase madura, con el TME apagado, la consulta entraba por un módulo al azar
(semilla 42), que la enrutaba con su directorio y la lectura B1.

El banco tenía 80 consultas en lenguaje natural con su clase conocida (27 de
\texttt{apple}, 27 de \texttt{horse} y 26 de \texttt{car}).
El protocolo completo pasaba las 80 por la fase temprana para formar el directorio y
después evaluaba la fase madura sobre las mismas 80, así que la evaluación es dentro de
muestra.

\paragraph{Formación del directorio.}
El estudio central de la fase sigue al directorio desde que está vacío.
Una interacción es una consulta del banco que pasa por la fase temprana y se registra.
Después de cada interacción $k$ se congela una copia del directorio y se evalúa con ella
la fase madura sobre las 80 consultas.
De cada $k$ se guardan la precisión madura, el rechazo, la entropía de los conteos y los
conteos por módulo.
Se probaron cuatro órdenes de las experiencias:
\begin{itemize}
    \item A, el orden original del banco, intercalado entre las tres clases;
    \item B, cinco órdenes barajados al azar;
    \item C, bloqueado por clase: las 27 consultas de \texttt{apple}, luego las 27 de
    \texttt{horse} y al final las 26 de \texttt{car};
    \item D, el orden de A con la puntuación cruda en la fase temprana, sin compuerta y
    sin normalización, como control del sesgo de masa.
\end{itemize}
Se toma como transición el primer $k$ con precisión madura de al menos el 90\,\%, y se
anota también el $k$ desde el que esa precisión se sostiene.
La curva se evalúa sobre las mismas consultas que forman el directorio, de modo que mide
cuánto del banco cubren los tokens ya registrados y no generalización a consultas
nuevas.
Las cifras de esta fase se obtuvieron con su arquitectura (tres módulos, cuatro memorias
por módulo, cuantización por signo, TME mediador y banco de 80) y se guardan en
\texttt{results/fase1\_tres\_modulos/}.
Con el código actual, escrito para ocho clases, no se reproducen, y los pesos del
codificador de tres clases no se guardaron.
```

### 3.5 Fase 2 (nueva)
```latex
\subsection{Fase 2: lectura del directorio}
\label{fase2:lectura}

La puntuación cruda de una proyección heteroasociativa crece con la masa de registros,
por lo que un módulo con más registros en el directorio obtiene ventaja sin mérito.
Las masas son desiguales porque la especialización lo es: con tres módulos, el
directorio del protocolo completo terminó con los conteos $[78, 65, 53]$, y con ocho,
con $[46, 16, 40, 25, 30, 18, 21, 31]$ (Sección~\ref{sec:proto-completo}).
La división por $c_k + 1$ de la ecuación~\eqref{eq:b1} convierte \emph{evidencia total}
en \emph{evidencia por registro}, de modo que la puntuación refleja la calidad de la
especialización.

\paragraph{Condiciones de lectura.}
Para elegir la lectura se compararon nueve condiciones sobre el prototipo de la fase 1.
Además de la lectura cruda, dos condiciones dividen la puntuación del directorio entre el
conteo de cada módulo y seis actúan sobre otra parte del sistema:
\begin{itemize}
    \item A, la lectura cruda, sin normalizar;
    \item B1, la división entre el conteo más uno (ecuación~\eqref{eq:b1});
    \item B2, la división entre la raíz cuadrada del conteo;
    \item C, un tope de registros: ningún módulo acumula más de tres veces los registros
    del que menos tiene;
    \item D, consultas balanceadas, $\lfloor N/3 \rfloor$ por clase e intercaladas;
    \item E32 y E64, directorios con 32 y 64 niveles en lugar de 16;
    \item F, el vocabulario depurado, sin las etiquetas de Apple~Inc.\
    (\textit{computer}, \textit{mac}, \textit{macintosh}) ni \textit{eden};
    \item G, la combinación de D, B1 y F.
\end{itemize}
Cada condición se corrió con $N \in \{10, 20, 40, 80\}$ consultas, que forman el
directorio y sobre las que se evalúa la fase madura, con cinco semillas.
Con la cuantización por signo, E32 y E64 solo cambian el índice de los dos niveles que
se usan, así que su patrón de bits es el de A.

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

\paragraph{Verificación con ocho módulos.}
Con el sistema de ocho módulos, la elección se revisó de tres formas.
La primera repite las nueve condiciones con $N \in \{50, 100, 200, 400\}$ consultas del
banco de 411 y cinco semillas (Sección~\ref{sec:calibracion}).
Las semillas solo cambian el resultado en D y G, que sortean sus consultas.
Con la cuantización por magnitud, E32 y E64 sí cambian la resolución.
La segunda fija un conjunto de evaluación de 120 consultas que nunca forman el
directorio, para separar la formación del directorio de la composición de lo evaluado
(Sección~\ref{sec:calibracion-fija}).
La tercera (experimento~22) compara B1 con el principio de tamaño, que entre los
módulos cuyo directorio contiene la pista elige el de envolvente más estrecha, con
puntuación $-\sum_i \log|\mathrm{soporte}_i|$.
Solo lee los directorios oficiales, sin cambiarlos, sobre las 656 imágenes de prueba y
las 411 consultas del banco.
La predicción, fijada antes de correr, era que con un registro balanceado las dos
lecturas toman las mismas decisiones.
```

### 3.6 Fase 3, apertura (nueva)
```latex
\subsection{Fase 3: escalado a ocho módulos}
\label{fase3:escalado}

El paso de tres a ocho módulos ocupa 22 commits, de \texttt{b281f9c} (1 de julio de
2026) a \texttt{d5b93fa} (14 de julio).
Cambiaron a la vez:
\begin{itemize}
    \item las clases, que pasan a ser las ocho de ETH-80;
    \item el codificador, reentrenado con las 2624 imágenes de entrenamiento de las ocho
    clases y, desde el 5 de julio, con entrenamiento determinista;
    \item la cuantización de las pistas de texto, que pasa de signo a magnitud con una
    escala global guardada (Sección~\ref{sec:pipeline-semantico});
    \item las memorias por módulo, de cuatro a cinco, porque cada módulo gana su propio
    directorio visual;
    \item el llenado, con 200 imágenes por clase en cuatro variantes (la original, el
    espejo y las rotaciones de $\pm 12^{\circ}$);
    \item el vocabulario de ConceptNet, ordenado por masa asociativa, con un tope de
    etiquetas por clase y una lista que quita los sentidos ajenos a la clase (los de
    Apple~Inc.);
    \item el banco, de 80 a 411 consultas, unas 50 por clase;
    \item las referencias de las métricas, con azar de 1/8 y entropía máxima de 3 bits.
\end{itemize}
Como todo cambió junto, la diferencia entre las cifras de tres y de ocho módulos no se
puede atribuir al número de módulos.

Después de julio el sistema siguió con ocho módulos y recibió cuatro cambios que salieron
de la fase 4 (Sección~\ref{fase4:propiedades}):
\begin{itemize}
    \item los directorios perspectivales con coordinación transactiva de la recuperación
    (14 de septiembre, experimento~10), que llevaron también a la lectura visual estricta,
    con $\xi = 0$;
    \item las 16 variantes por imagen (23 de septiembre, experimento~13);
    \item el umbral de energía $\tau$ (23 de septiembre, experimento~14);
    \item una sola memoria heteroasociativa de contenido por módulo, con las
    homoasociativas convertidas en lecturas de ella (del 30 de octubre al 1 de noviembre).
\end{itemize}
Los métodos que siguen son los de ese sistema final.
```

### 3.7 Organización del experimento

Viejo:
```latex
\subsection{Organización del experimento}
\label{sec:organizacion}

La Sección~\ref{sec:resultados} presenta los estudios en este orden.
El estudio principal es la calibración del directorio (9 condiciones de calibración
$\times$ $N \in \{50, 100, 200, 400\}$ consultas $\times$ cinco semillas, que solo cambian
el resultado en D y G).
Le siguen la misma calibración con un conjunto de evaluación fijo, que no forma el
directorio (Sección~\ref{sec:calibracion-fija}), y cuatro estudios de caracterización
(protocolo completo, parámetros propios $\iota \times \kappa$, formación del directorio y
capacidad de llenado, Secciones~\ref{sec:proto-completo} a~\ref{sec:capacidad}).
Después vienen el hemisferio visual (Sección~\ref{sec:hemisferio-visual}), la
generalización a objetos nuevos (Sección~\ref{sec:objetos-nuevos}), el hemisferio visual
con un codificador entrenado sin la pérdida de clase
(Sección~\ref{sec:codificador-sin-clase}), la comparación con una sola EHAM
(Sección~\ref{sec:eham-unica}), la comparación con decisores sin memoria asociativa sobre
los mismos vectores (Sección~\ref{sec:lineas-base}), la verificación de una sola memoria
de contenido por módulo (Sección~\ref{sec:una-memoria}) y el costo computacional de la
reproducción completa (Sección~\ref{sec:costo}).
En las dos calibraciones, el protocolo completo, el barrido $\iota \times \kappa$ y la
formación del directorio, cada transacción de texto se registra en un solo
\emph{directorio compartido}, igual al registro completo del TME.
Los directorios perspectivales de la Sección~\ref{sec:componentes}, en los que solo
registran el módulo de entrada y el ganador, se usan en el hemisferio visual y en la
comparación con una sola EHAM.
```

Nuevo (lista los estudios de la fase 3 en el orden de 4.1.3 del índice, manda las calibraciones a la fase 2 y agrega el diseño de exp12):
```latex
\subsubsection{Organización del experimento}
\label{sec:organizacion}

Los resultados de la Sección~\ref{sec:resultados} siguen el orden de las fases.
Los estudios de la fase 3 son, en este orden, el protocolo completo, los parámetros
propios $\iota \times \kappa$, la formación del directorio y la capacidad de llenado
(Secciones~\ref{sec:proto-completo} a~\ref{sec:capacidad}); el hemisferio visual
(Sección~\ref{sec:hemisferio-visual}); la generalización a objetos nuevos
(Sección~\ref{sec:objetos-nuevos}); el hemisferio visual con un codificador entrenado
sin la pérdida de clase (Sección~\ref{sec:codificador-sin-clase}); la comparación con
una sola EHAM (Sección~\ref{sec:eham-unica}); la comparación de una EHAM de dos clases
con una de ocho; la verificación de una sola memoria de contenido por módulo
(Sección~\ref{sec:una-memoria}); la comparación con decisores sin memoria asociativa
sobre los mismos vectores (Sección~\ref{sec:lineas-base}), y el costo computacional de
la reproducción completa (Sección~\ref{sec:costo}).
Las dos calibraciones pertenecen a la fase 2 (Sección~\ref{fase2:lectura}).

La comparación de dos clases contra ocho (experimento~12) recorre los 28 pares de
clases.
Para cada par, una EHAM llenada solo con esas dos clases, con 200 imágenes por clase y
el llenado de la comparación con una sola EHAM, responde las consultas reservadas de
las dos clases, con cinco semillas y tres sorteos.
Sobre las mismas consultas y semillas responden también el especialista y la EHAM de
ocho clases.
La brecha de fidelidad mide cuánto más lejos de la instancia real más cercana queda el
recuerdo de cada EHAM que el del especialista.
De cada par se mide además el solapamiento de los soportes de las dos clases (Jaccard
medio por coordenada), en el lado de las etiquetas y en el latente.
La predicción registrada antes de correr era que la brecha crece con el solapamiento.

En las dos calibraciones, el protocolo completo, el barrido $\iota \times \kappa$ y la
formación del directorio, cada transacción de texto se registra en un solo
\emph{directorio compartido}, igual al registro completo del TME.
Los directorios perspectivales de la Sección~\ref{sec:componentes}, en los que solo
registran el módulo de entrada y el ganador, se usan en el hemisferio visual y en la
comparación con una sola EHAM.
```

### 3.8 Fase 4 (nueva)
```latex
\subsection{Fase 4: experimentos de propiedades}
\label{fase4:propiedades}

Con el sistema de ocho módulos se diseñaron experimentos que preguntan qué hace el
sistema además de acertar.
Se agrupan en seis temas.
Los temas de reconocer y recordar (envolvente, contención y familiaridad) y de los
límites del rechazo usan estudios de la fase 3 ya descritos: los objetos nuevos, el
codificador sin pérdida de clase, el umbral de energía, la verificación de una sola
memoria de contenido y la sonda de rechazo.
Los otros cuatro temas tienen experimentos propios, que se describen abajo; los
resultados están en la Sección~\ref{sec:resultados}.

Varios de estos experimentos estudian el directorio y no la elección del ganador.
En ellos el directorio se forma con la clase real como ganador de cada transacción, para
separar lo que el directorio guarda del acierto de la fase temprana.
Los experimentos 8, 9 y 10 se corrieron antes de que el sistema adoptara los directorios
perspectivales y una sola memoria de contenido.
Usan el protocolo anterior, en el que todos los módulos registran todas las
transacciones y sus directorios son idénticos, con el directorio visual llenado sin
variantes y con las memorias homoasociativas al lado de la heteroasociativa.
Los mecanismos que miden no dependen de las memorias homoasociativas, pero sus cifras
no son las del sistema final.
El experimento~9 se reporta con esa salvedad.

\paragraph{El directorio como índice.}
En el experimento~7, un solo directorio recibe pistas de texto y de imagen, para ver si
forma una representación compartida de las dos modalidades.
Su relación tiene 364 características, 300 de texto (recuantizadas a 32 niveles con la
misma escala global) y 64 del latente.
La mitad que falta en cada pista se registra y se consulta como valor indefinido, que la
proyección salta.
El directorio se forma de tres maneras, solo con texto, solo con imagen y con pares de
texto e imagen, y se compara con dos directorios separados.
El texto usa las 80 consultas de los estudios de protocolo, evaluadas dentro de muestra.
La imagen se forma con las 128 imágenes de entrenamiento por clase de la formación
visual y se evalúa con 20 imágenes de prueba por clase.
La lectura es B1.

El experimento~8 lee el directorio en el sentido inverso, de la identidad de un módulo a
una pista en su dominio, con la recuperación $\beta$ desde la derecha.
Se comparan tres respuestas para cada clase: la de la memoria de contenido del
especialista con su propia etiqueta (lo vivido), la del directorio con el dominio propio
y la del directorio con un dominio ajeno que el módulo presenció.
Las juzgan el clasificador latente del codificador y el vecino más cercano entre las
6400 instancias reales del llenado.
Dos barridos completan el diseño, uno sobre cuántas transacciones ajenas presenció el
módulo, de 0 a 128, y otro sobre cuántos registros tiene el directorio, de 1 a 800 por
módulo.
Un control pregunta por identidades que ningún módulo tiene.

\paragraph{La perspectiva y la pérdida de un miembro.}
El experimento~10 compara un grupo cuyos módulos solo registran lo que presencian con un
registro único del grupo, el pizarrón.
El ganador siempre registra lo suyo.
Un módulo que no ganó registra la transacción de dos maneras según la condición: al
azar con probabilidad $f \in \{0, 1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1\}$, con tres
semillas, o solo si el ganador está a distancia $r \le 4$ en un anillo de los ocho
módulos.
Cada consulta entra por cada uno de los ocho módulos y se resuelve con cuatro
protocolos:
\begin{itemize}
    \item directo, en el que el módulo de entrada consulta su directorio y rechaza si no
    hay soporte;
    \item encadenado, en el que la consulta sin soporte pasa a los módulos conocidos, por
    orden de familiaridad, hasta que alguno tiene soporte;
    \item agregado, en el que el módulo de entrada suma las puntuaciones normalizadas de
    todos sus conocidos y elige la mayor;
    \item pizarrón, el directorio único con todos los registros, como referencia.
\end{itemize}
El texto se forma con 30 consultas por clase (240) y se evalúa también con las 171
reservadas; la imagen se forma con 128 latentes de entrenamiento por clase y se evalúa
con 20 de prueba por clase, con $\xi = 0$.
Además del acierto, se miden los saltos del encadenado y la divergencia de Jaccard entre
los soportes de cada par de directorios.

En el experimento~9 se quita un módulo $k$, y las consultas de su dominio entran por un
sobreviviente, que las enruta como en la fase madura.
Sobre las consultas que el directorio sigue mandando a $k$ se comparan tres políticas
del grupo sin $k$:
\begin{itemize}
    \item sustitución, en la que responde con su propio contenido el sobreviviente de
    mayor puntuación en el directorio;
    \item descripción, en la que el sobreviviente responde con lo que presenció de $k$,
    leyendo su directorio en el sentido inverso del experimento~8;
    \item rechazo, no responder.
\end{itemize}
La referencia es la respuesta de $k$ presente.
Se usan las 411 consultas del banco, con tres repeticiones porque la recuperación
muestrea, y 10 imágenes de prueba por clase.
En el sentido texto $\to$ imagen la respuesta se juzga por su clase y por su distancia
a la instancia real más cercana del dominio perdido.
En el sentido imagen $\to$ texto acierta si alguna de las tres palabras evocadas
pertenece al vocabulario de ese dominio.
Una sonda aparte mide cuánto del dominio de $k$ reconoce el especialista frente a un
módulo que no lo es.

\paragraph{El tamaño y la partición.}
Las dos mediciones controladas de este tema son la comparación con una sola EHAM y la
de dos clases contra ocho, descritas en la Sección~\ref{sec:organizacion}.
La lectura por el principio de tamaño (experimento~22) está con la fase 2
(Sección~\ref{fase2:lectura}).

\paragraph{La imagen y la palabra.}
La evocación de dominio cuenta como acierto que una de tres palabras sea de la clase.
Para saber si la evocación devuelve una palabra específica, el experimento~17 usa tres
condiciones:
\begin{itemize}
    \item A, los modelos oficiales con top-1 en lugar de top-3, sobre las mismas 118
    imágenes de prueba de la evocación de dominio y con tres recuerdos por imagen;
    \item B, un llenado nuevo en el que todas las vistas del objeto $k$ de cada clase se
    registran con la $k$-ésima palabra exclusiva del vocabulario de la clase, con 200
    imágenes y 16 variantes por clase, donde el azar es del 10\,\%;
    \item C, el color como palabra, con 80 objetos etiquetados a mano por su color
    dominante y una paleta de ocho colores.
\end{itemize}
Las respuestas se leen de cuatro formas: la recuperación oficial con el vecino por
coseno, el prototipo (el valor más probable de cada coordenada), el soporte (la
probabilidad media que la proyección da a cada palabra candidata) y el soporte dividido
entre el de la memoria completa, que es el análogo de B1 y se fijó antes de correr.
Se evalúa en el módulo de la clase verdadera.

El experimento~18 asocia cada imagen con una característica que el objeto tiene, con
una memoria heteroasociativa por eje y clase: patrón (liso, con manchas o decorado) en
\texttt{cow}, \texttt{horse}, \texttt{dog} y \texttt{cup}; techo (convertible o fijo)
en \texttt{car}, y pelo (rizado o liso) en \texttt{dog}.
Las etiquetas se pusieron a mano por objeto y solo entran los objetos claros en cada
eje.
Cada memoria se llena con 200 vistas en 16 variantes, se evalúa con vistas nuevas de
objetos conocidos y con objetos nuevos en una validación \textit{leave-one-object-out}
de 52 pliegues.
Las lecturas son las de soporte del experimento~17, que eligen entre las palabras del
eje y no ejecutan un recuerdo.
Se compara con un $k$-vecinos sobre los mismos latentes y sobre los rasgos de un ResNet18
de ImageNet sin ajustar.

Con el experimento~19 se mide qué gana el especialista y qué pierde el índice cuando la
percepción conserva el detalle dentro de la clase.
Cambia el codificador por un ResNet18 de ImageNet congelado y un análisis de componentes
principales a 64 dimensiones, ajustado solo con las 2624 imágenes de entrenamiento.
Con ese codificador se corren de nuevo el llenado, las dos fases, el hemisferio visual,
los objetos nuevos (diez pliegues) y el experimento~18.
Se corrió en una copia del sistema anterior a la memoria de contenido única.
```

### 3.9 Fase 5 (nueva)
```latex
\subsection{Fase 5: laboratorio en tiempo real}
\label{fase5:laboratorio}

La fase 5 conectó el sistema a un micrófono y a una cámara para ver si funciona con
entradas continuas.
Usa la versión v5 del sistema, de julio de 2026, con ocho módulos que llevan tres
memorias de contenido cada uno (la heteroasociativa y dos homoasociativas), un
directorio de texto y un directorio visual, más el TME.
No es la arquitectura final, y no hay ninguna corrida con ella.
El laboratorio carga los modelos en modo de solo lectura y corre en una ventana de
Python con tres hilos, uno para el audio, uno para la visión y uno para la interfaz.

\paragraph{Voz.}
El micrófono entrega audio a 16\,kHz en un canal, en bloques de 30\,ms.
Un detector de voz propio compara la energía de cada bloque con un piso de ruido que se
adapta en los silencios, y cierra la frase tras unos 600\,ms de silencio.
La frase cerrada la transcribe Whisper \textit{small}, con la biblioteca
\textit{faster-whisper} en la GPU y respaldo en la CPU.
La transcripción usa el modo de traducción: se puede hablar en español o en inglés, y
sale texto en inglés, el idioma del vocabulario de fastText.
Mientras se habla aparecen subtítulos parciales.
La frase transcrita entra al hemisferio textual en uno de dos modos.
En el temprano, el TME la difunde a los ocho módulos y la registra en un directorio de
sesión, que vive en memoria y no toca los modelos guardados.
En el maduro, el TME está apagado, y el módulo de entrada consulta su directorio con la
lectura B1 y redirige al especialista o rechaza.
Tras el enrutamiento, la memoria del destino evoca una imagen en un hilo aparte, que el
decodificador dibuja sin detener el video ni la escucha.

\paragraph{Cámara.}
Cada 250\,ms, aproximadamente, se toma el recuadro central del cuadro, que por omisión
ocupa el 55\,\% del lado menor, y se pasa a $128 \times 128$ píxeles al codificador.
El latente cuantizado consulta el directorio visual del módulo de entrada con la lectura
tolerante de la versión v5, y la etiqueta que se muestra es la mayoría de los últimos
cinco análisis.
Si el directorio rechaza el cuadro, se intenta otra vez con los momentos de color RGB
normalizados a los de ETH-80, y si lo rechaza de nuevo, la interfaz muestra el candidato
más cercano.
Como el segundo intento solo corre tras un rechazo, no cambia las decisiones sobre los
cuadros que el directorio ya aceptaba.

\paragraph{Pruebas.}
Whisper corrió en una GPU NVIDIA RTX 2050, y el codificador y las memorias, en la CPU.
La cadena de voz de punta a punta se probó con un archivo WAV inyectado por el camino
del micrófono, con la frase «Farm animal that gives milk», en los dos modos y con dos
módulos de entrada.
Se midieron una vez la latencia de la transcripción y la del enrutamiento, el tiempo de
análisis de un cuadro y la tasa de cuadros de la interfaz.
La política de color se probó en simulación, sobre 24 imágenes de prueba de ETH-80 en
tres condiciones: limpias, con un tono grisáceo medio y con uno fuerte.
Con la cámara física se mostraron imágenes de ETH-80 en la pantalla de un teléfono y en
una hoja impresa con 16 imágenes, y un cuadro real ajeno a ETH-80 se pasó por el
directorio visual.
Las mediciones son del 16 al 18 de julio de 2026 y no quedó registro crudo de ellas;
lo que se conserva está en \texttt{results/mundo\_real/}.
No se midieron la tasa de error de la transcripción, el acierto del enrutamiento con voz
ni el acierto con la cámara física.
Por eso la fase 5 es una demostración de integración.
Las consultas habladas en español y las imágenes de otro origen quedan fuera del alcance
de la evaluación del sistema.
```


## 4. Fuente de cada cifra nueva

`F1/` = `results/fase1_tres_modulos/`. Todas las cifras de 3.3 y 3.4 son de la arquitectura de la fase 1 (tres módulos, cuatro memorias por módulo, cuantización por signo, TME mediador, banco de 80) y se rotulan así en el texto.

| cifra | dónde va | fuente |
|---|---|---|
| 984 imágenes de entrenamiento del codificador de tres clases (328 por clase) | 3.3 | `F1/computational_cost/report.md:44`; 328 = 984/3 y es la N máxima de `F1/experimento1/informe.md:86` |
| cuatro memorias por módulo y sus dimensiones; directorio visual solo en el TME | 3.3, Tabla del arco | `git show origin/v3-experimento1:README.md` (bloque «Architecture per agent (4 AMRs)»); `F1/README.md` |
| cuantización por signo, 2 de 16 niveles | 3.3, 3.4 | `F1/ablation_mdir_bias/ablation_report.md` (P1 y P5) |
| llenado por instancias con 200 imágenes por clase | 3.3 | `F1/experimento1/informe.md:3-4` |
| llenado promediado descartado (1 recuerdo distinto de 12) | 3.3, sin cifra en el texto | `F1/exp5_entropic_prototype/report.md:22-24` |
| ι = κ = ξ = 0, σ = 0.1; banco de 80 (27/27/26) | 3.3, Tabla del arco | `F1/experimento1/informe.md:10-11` |
| entrada al azar con semilla 42; registros idénticos en los cuatro directorios | 3.3 | `F1/exp3_corrected_routing/report.md:6-8`; `F1/exp4_directory_formation/report.md` (notas de instrumentación) |
| órdenes A, B (cinco semillas), C (27, 27, 26) y D (crudo, sin compuerta ni normalización); umbral del 90 % | 3.3 | docstring de `git show origin/v3-experimento1:run_experiment4.py:9-24`; `F1/exp4_directory_formation/report.md` |
| entropía máxima 1.585 bits con tres módulos | 3.2.2 | `F1/exp3_corrected_routing/report.md` (tabla) |
| conteos [78, 65, 53] | 3.4 | `F1/exp3_corrected_routing/summary.json:7-11` |
| conteos de ocho módulos [46, 16, 40, 25, 30, 18, 21, 31] | 3.4 (ya estaba en 3.1.3) | `results/exp3_corrected_routing/summary.json`; texto vigente de `sec:proto-completo` |
| nueve condiciones; C con tope de 3×; D con ⌊N/3⌋; F sin computer, mac, macintosh y eden; N ∈ {10, 20, 40, 80}; cinco semillas | 3.4 | `F1/ablation_mdir_bias/ablation_report.md:22-59, 95, 104, 126` |
| A 53.75 %, apple 78.75 % de las decisiones, B1 98.75 %, B2 75.0 %, C 53.75 %, D 52.82 %, E32 y E64 53.75 %, F 80.0 %, G 98.72 % (N = 80) | 3.4 | `F1/ablation_mdir_bias/ablation_report.md:11, 27, 31, 35, 39, 43, 47, 51, 55, 59` |
| temprana 97.5 % | 3.4 | `F1/exp3_corrected_routing/summary.json:2` |
| verificación con ocho: N ∈ {50, 100, 200, 400}; 120 consultas fijas | 3.4 | texto vigente de `sec:calibracion` y `sec:calibracion-fija` (`results/ablation_mdir_bias`, `results/calibracion_evaluacion_fija`) |
| exp22: −Σ log\|soporte\|, 656 imágenes y 411 consultas, predicción fijada antes | 3.4 | `results/experimento22/README.md:3-8` |
| 22 commits de `b281f9c` (1 jul) a `d5b93fa` (14 jul) | 3.5 | `git log origin/v3-experimento1..origin/v4-8clases`; `plan_reestructura/inventario_fase2_escalado.md` §1 |
| 2624 imágenes del codificador de ocho clases | 3.5 | `results/computational_cost/nov2026_cpu/report.md:28` |
| entrenamiento determinista desde el 5 jul | 3.5 | commit `af2c6de`; inventario §1 |
| magnitud con escala global; de cuatro a cinco memorias; llenado ×4 (original, espejo, ±12°); tope y lista de polisemia; banco de 411 | 3.5 | mensajes de `b281f9c` y `cbe57d8`; `git show origin/v4-8clases:README.md:16-24, 41`; inventario §1 |
| azar 1/8 y 3 bits | 3.5, 3.2.2 | commit `0a75c3e`; `results/exp3_corrected_routing/report.md:22` |
| perspectivales el 14 sep; 16 variantes y τ el 23 sep; una sola hetero del 30 oct al 1 nov | 3.5 | commits `a423950`, `cc37d2e`, `b0542ab`, `0c70824`; inventario §1; carpetas `results/experimento10`, `experimento13`, `experimento14`, `homo_marginal` |
| exp12: 28 pares, N = 200, semillas 42 a 46, 3 sorteos, Jaccard por coordenada, predicción registrada | 3.5.7 | `results/experimento12/README.md:3-7` |
| exp7: 364 características, texto a 32 niveles, mitad indefinida, 80 consultas, 128 imágenes por clase para formar y 20 de prueba, B1 | 3.6 | `results/experimento7/README.md:3-8` |
| exp8: lectura inversa, juez clasificador y vecino entre 6400 instancias, barridos de 0 a 128 y de 1 a 800 | 3.6 | `results/experimento8/README.md:3-8, 95-114` |
| exp10: f ∈ {0, 1/64, …, 1}, tres semillas, anillo r ≤ 4, cuatro protocolos, 240 y 171 consultas, 128 y 20 imágenes, ξ = 0 | 3.6 | `results/experimento10/README.md:6-15` |
| exp9: tres políticas, 411 consultas con tres repeticiones, 10 imágenes por clase, jueces | 3.6 | `results/experimento9/README.md:6-15` |
| exp17: 118 imágenes, tres recuerdos, palabra k-ésima, 200 × 16, azar 10 %, 80 objetos, ocho colores, cuatro lecturas | 3.6 | `results/experimento17/README.md:3-12, 13-15, 27-29, 39-41` |
| exp18: ejes, 200 vistas × 16 variantes, 52 pliegues, lecturas de conjunto cerrado | 3.6 | `results/experimento18/README.md:3-14` |
| exp19: ResNet18 de ImageNet + PCA a 64 con 2624 imágenes; etapas 5 a 8, exp16 (10 pliegues) y exp18; copia anterior a una hetero | 3.6 | `results/experimento19/README.md:3-8` |
| laboratorio v5, tres memorias de contenido por módulo, sin corrida con la arquitectura final | 3.7 | `results/mundo_real/README.md:9` |
| 16 kHz, bloques de 30 ms, VAD por energía con piso adaptativo, ~600 ms de silencio, traducción es/en → en, respaldo en CPU, tres hilos, directorio de sesión, dos modos | 3.7 | `results/mundo_real/realtime_lab_README.md:31-36, 41, 47, 54-55, 182-196` |
| ~250 ms, recuadro del 55 %, mayoría de 5, candidato más cercano, reintento de color | 3.7 | `results/mundo_real/realtime_lab_README.md:37-39, 148, 155, 159, 167-172` |
| RTX 2050 para Whisper y CPU para el resto | 3.7 | `results/mundo_real/smtex_05_resultados.tex:13` |
| WAV «Farm animal that gives milk», dos modos y dos entradas | 3.7 | `results/mundo_real/smtex_05_resultados.tex:40-47` |
| 24 imágenes en tres condiciones de color; hoja con 16 imágenes; teléfono; cuadro real | 3.7 | `results/mundo_real/realtime_lab_README.md` (secciones del 17 y 18 jul); `results/mundo_real/selftest_frame.png` |
| mediciones del 16 al 18 jul, sin registro crudo; lo que no se midió | 3.7 | `results/mundo_real/README.md:11-13` |

El Capítulo 3 no da resultados de las fases 3 a 5: las latencias, la política de color y todas las cifras de los experimentos 7 a 22 quedan para el Capítulo 4.

## 5. Lo que no se pudo sostener o se dejó fuera

- **Partición 328/82 de la fase 1.** Las 82 imágenes de prueba por clase no tienen fuente en `results/fase1_tres_modulos/` (el inventario las toma de `6001770:conclusiones_experimento1.md`, que no está en `results/`). Se dejó solo «984 imágenes, 328 por clase».
- **Experimento ι × κ con tres módulos.** No entra en la fase 2. El inventario marca la conclusión «κ inerte» como error de programación (`29f401c`) y la tabla de `F1/exp2_iota_kappa/report.md` tiene la firma de ese error (columnas de κ idénticas), aunque `F1/README.md` diga que la copia es la corregida. Esa contradicción hay que resolverla antes de citarlo.
- **Sonda de rechazo, hemisferio visual y capacidad de tres módulos.** No entran: la sonda está declarada obsoleta, el hemisferio visual de tres módulos sale de un log anterior al saneamiento del 22 jun que no está en `results/`, y el índice no los pide en 4.1.1.
- **Binarización por signo con ocho clases** (50 % contra 84.7 %). Solo existe en el mensaje de `b281f9c`; no entra.
- **Fecha de la vuelta a ξ = 0 en el directorio visual.** No hay commit identificado; el texto la liga a los directorios perspectivales por la razón que ya da 3.1.3, sin fecha.
- **Detalles del laboratorio que solo están en el código** (`float16` en la GPU, ξ = 2 en la lectura visual): no entran porque no están en `results/mundo_real/`; el texto dice «la lectura tolerante de la versión v5».
- **MedMNIST+ y VisA** (exp20, 21, 23, 24 y los demos): fuera, según la decisión 1 del autor. Por eso 3.6 no describe esos experimentos, y los temas 3 y 6 del inventario de hallazgos remiten a estudios de la fase 3.

## 6. Etiquetas y citas

- **Conservadas:** todas las de `03_arquitectura.tex` y `04_metodologia.tex` en la base. `sec:metodologia`, `sec:metricas`, `sec:dataset`, `sec:pipeline-semantico`, `fig:espacio-semantico`, `sec:percepcion`, `sec:banco`, `sec:parametros`, `sec:auditoria` y `sec:organizacion` siguen en 04; `eq:b1` sigue en 03. Se comprobó que todo `\ref`/`\eqref` de `.tex_uacj/*.tex` resuelve.
- **Nuevas (prefijo `fase`):** `fase:arco`, `fase:tab-arco`, `fase1:prototipo`, `fase2:lectura`, `fase3:escalado`, `fase4:propiedades`, `fase5:laboratorio`.
- **Eliminadas:** ninguna.
- **Citas:** no se agregó ningún `\cite`. No hace falta ninguna nueva para el Capítulo 3; Whisper y faster-whisper se nombran sin cita (no están en `referencias.bib`; si se quiere citar Whisper, sería Radford et al. 2023, que habría que verificar y agregar).

## 7. Para la integración

- El orden de los estudios de la fase 3 en `sec:organizacion` sigue 4.1.3 del índice: protocolo completo, ι × κ, formación, capacidad, hemisferio visual, objetos nuevos, codificador sin clase, EHAM única, dos clases contra ocho, una memoria por módulo, líneas base y costo. Hoy el Capítulo 4 pone las líneas base antes de «una memoria por módulo»; `05_resultados.tex:4` dice que sigue el orden de `sec:organizacion`, así que la sesión del Capítulo 4 y esta deben coincidir.
- El diseño de exp12 quedó en la fase 3 (3.5.7) y el de exp22 en la fase 2 (3.4), como en 4.1.3 y 4.1.2 del índice; 3.6 remite a los dos.
- La frase final de 3.7 deja fuera del alcance de la evaluación las consultas habladas en español y las imágenes de otro origen, en línea con 1.5.

## 8. Revisión de patrones (regla 6 del índice)

Se revisó el texto nuevo contra la lista. Se quitaron el metatexto de apertura de 03, una cadena de «:» y «;» (los cambios posteriores a julio pasaron a lista), cinco dos puntos explicativos seguidos en la fase 1 y la fase 4, un «así» de muletilla y los comienzos repetidos «El experimento N pregunta» (quedan dos «El experimento N» con verbos distintos). No hay «no es X, sino Y», ni énfasis sin cifra, ni `\textbf` nuevo en la prosa. Los términos módulo, directorio, compuerta, fase temprana y madura, B1, EHAM y TME no cambian. La palabra prohibida no aparece en el parche.
