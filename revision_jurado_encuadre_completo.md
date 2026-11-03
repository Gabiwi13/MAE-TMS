Hice la propuesta de encuadre completa y el orden único de aplicación. No edité la tesis ni `.tex_uacj`, no hice commit ni push y no creé ramas; el árbol sigue limpio en `una-hetero` (`6c1a9fb`).

- **Cotejo:** un script que solo normaliza los espacios comparó contra `.tex8` los 10 bloques «Viejo» y las 5 líneas ancla de las inserciones, y coinciden todos. También buscó en el texto de su propuesta los 15 fragmentos «Viejo» que cito de marcadores, metodología y planteamiento, y aparecen todos una vez.
- **Cifras:** todas salen de las propuestas, y las volví a cotejar contra `results/`. Hay una discrepancia en la tabla «ya no se sostiene» del encuadre: dice que el 1-NN acierta «21 a 24» imágenes que el sistema no da bien. `results/lineas_base/resumen_imagen.json` da 23 o 24 en los 25 decisores, así que en los textos uso «23», como el propio E4.
- **Las 3 secciones nuevas de 05** (`sec:lineas-base`, `sec:calibracion-fija` y `sec:codificador-sin-clase`) todavía no existen. Los textos nuevos las citan por esa etiqueta; la parte 3 dice dónde van y qué cifras deben traer.
- **Un pasaje sin punto en el encuadre:** la limitación (f), `06:291-300`, decía «el fallo es rechazo» con objetos nuevos, y eso ya no vale con el codificador por pliegue (33 falsos de 984). Escribí el texto combinado (parte 2, fila 11).
- **Entradas BibTeX nuevas:** `yassa2011pattern` y `goldstone1994influences` no estaban en ningún archivo. Escribí sus campos yo; hay que cotejarlos antes de aplicar.
- **Decisiones tuyas:** la pregunta del medio en E2 (recomiendo agregarla) y la cifra del 1.3 % de claridad S48 (recomiendo quitarla).

Convenciones: `main:57-104` es `.tex8/main.tex`, líneas 57 a 104; `06:5-24` es `.tex8/secciones/06_discusion.tex`, y así para 01 a 07. En LaTeX el marcador va como `[PENDIENTE: exp11 d\_nn]`.

---

# Parte 1. Los puntos del encuadre, viejo/nuevo

## E1. Resumen completo

- **Reemplaza** a estructura 9.1, y con ella 1.1 y la fila `main:62-63` de 3.4. Trae la forma de claridad que 9.1 ya absorbía.
- **Cambia respecto de 9.1:**
  - 97.0 pasa a 96.8, con la composición de las reservadas.
  - Salen el 93.0 dentro de muestra, el 20.5 → 13.8 de `apple` y «Las memorias operan en los dos sentidos».
  - El 89.2 del codificador común pasa al 89.3 del codificador por pliegue.
  - Entran la evaluación fija, las líneas base, lo que agrega la memoria, las dos condiciones y la clase frente a la EHAM única.
- **Viejo:** `main:57-104`, el bloque `abstract` entero. Va desplegado en el archivo.
- **Nuevo:**
```latex
\begin{abstract}
Un grupo que trabaja junto puede recordar más que cada uno de sus miembros por separado,
porque cada miembro guarda parte de lo que el grupo sabe y sabe a quién preguntar por el
resto.
Wegner \cite{wegner1987transactive} llamó a esta organización \emph{memoria
transactiva}.
Este trabajo pregunta si puede construirse con memorias asociativas, sin clasificadores
discriminativos en las decisiones de enrutamiento y rechazo, y qué agregan esas memorias
a las decisiones del sistema.
Presenta EAM-TMS (\textit{Entropic Associative Memory -- Transactive Memory System}), un
sistema distribuido de memoria transactiva construido con las Memorias Asociativas
Entrópicas de Pineda y Morales en su variante ponderada (W-EAM)
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
Las palabras entran como vectores fastText de 300 dimensiones
\cite{bojanowski2017fasttext}, con vocabulario extraído de ConceptNet 5.7
\cite{speer2017conceptnet} y \emph{cuantización por magnitud} en 16 niveles; las
imágenes, como códigos de un ResNet18 \cite{he2016resnet} entrenado con una pérdida de
clasificación auxiliar.
En la calibración, con un directorio compartido y un conjunto de consultas de texto que
nunca se registran en él, la fase madura alcanza a la temprana sin superarla de forma
robusta ($+0.2$ y $+1.3$ puntos con 200 y 291 consultas de formación), así que el
directorio reproduce la decisión de la fase temprana sin consultar a los ocho módulos.
Con directorios perspectivales y 171 consultas reservadas, el 96.8\,\% llega al módulo
correcto, sobre consultas que traen el nombre de su clase más a menudo que las de la
calibración (87.7 frente a 49.8\,\%).
Con imágenes, los directorios visuales envían al especialista correcto 631 de las 656
imágenes de prueba (96.2\,\%), vistas nuevas de objetos conocidos; rechazan el 3.5\,\% y
se equivocan en dos.
Con objetos que ningún módulo vio y un codificador reentrenado sin ellos, el 89.3\,\% de
las vistas llega al especialista y recibe respuesta, con 33 falsos enrutamientos en 984
[PENDIENTE: pliegues 10/10].
Lo que la memoria asociativa agrega no es acierto de clase.
Sobre las mismas representaciones, decisores sin memoria aciertan lo mismo en texto.
En las 80 consultas del protocolo completo, un voto por las palabras del vocabulario y los
cinco vecinos más cercanos aciertan el 79.4 y el 81.5\,\%, frente al 81.2\,\% del
sistema.
En imagen, un centroide o un vecino más cercano aciertan de 652 a 655 de las 656, sin
rechazar ninguna, y una sola memoria con las ocho clases acierta la clase en el
96.9\,\% de las reservadas.
Lo que agrega es rechazar sin un umbral ajustado y devolver el contenido asociado.
Los decisores de coseno aceptan las 40 consultas fuera de dominio y el sistema 2.
Frente a la memoria única, con 200 imágenes por clase, la partición en especialistas
acepta menos consultas fuera de dominio (2 frente a 8 de 40, con una segunda compuerta
que se agregó después de ver esas consultas); además, recuerda con más fidelidad
[PENDIENTE: exp11 d\_nn].
Esos resultados dependen de dos condiciones que no salen del mecanismo asociativo: la
lectura del directorio normalizada por conteo, sin la cual la fase madura queda 7.5
puntos por debajo de la temprana, y un latente en que cada coordenada separe las clases,
que da la pérdida de clase del codificador; sin ella, el enrutamiento visual baja al
70.4\,\%, con 169 falsos enrutamientos.
En cada módulo, la familiaridad y el nombre se leen de la misma memoria, y el daño al
azar los separa.
Con el 1\,\% de las celdas destruidas, el módulo deja de nombrar el 92\,\% de las
imágenes y sigue reconociéndolas todas.
La clase la deciden las representaciones; el mecanismo asociativo tiene además límites
propios, como la normalización externa que necesita la lectura del directorio y la
fragilidad del nombre ante el daño.
\end{abstract}
```
- **Fuentes:**
  - +0.2, +1.3 y −7.5 (82.2 − 89.7): calibración fija, tabla «Los 5 sorteos de E juntos».
  - 96.8 y 96.9: `ruteo.md`, «Texto», con N = 200. 87.7 y 49.8: `salida.md`, tabla M3.1.
  - 89.3 y 33 de 984: `tablas.md` de los pliegues, sobre 3 pliegues.
  - 79.4, 81.5, 81.25, 652–655 y 40 de 40: `lineas_base/README.md`.
  - 2 frente a 8: `ruteo.md`.
  - 70.4 y 169: `comparacion.md` del codificador sin clase. 92 %: `tab:lesion`.

## E2. La pregunta

- **Reemplaza** a estructura 3.1 y quita «solo» de `01:29`.
- **Decisión tuya:** la pregunta del medio. Recomiendo agregarla. Si no la quieres, se aplica estructura 3.1 y la primera frase pierde «y qué agregan ellas a las decisiones del sistema».
- **Viejo** (`01:29-38`):
```latex
Este trabajo pregunta si la organización que describe Wegner puede construirse solo con
estas memorias:

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
Este trabajo pregunta si la organización que describe Wegner puede construirse con
estas memorias y qué agregan ellas a las decisiones del sistema:

\begin{quote}
¿Puede un sistema de memoria transactiva construido sobre memorias asociativas
entrópicas repartir consultas de texto e imagen entre ocho especialistas, recordar el
contenido asociado y rechazar lo que no conoce, sin clasificadores discriminativos en
las decisiones de enrutamiento y rechazo? ¿Qué agrega la memoria asociativa frente a
decisores simples que usan las mismas representaciones? Y donde aparezcan límites,
¿provienen del mecanismo asociativo o de las representaciones que lo alimentan?
\end{quote}
```
- **Generador:** `generar_capitulos.py` exige que la línea antes del `quote` termine en «:». Este texto lo cumple.

## E3. Contribuciones

- **Reemplaza** a estructura 9.2.
- **Cambian la 1, la 3, la 4 y la 6.** La mezcla del 79–84 % sale de la 4 y queda en E9.
- **Viejo:** `01:69-114`, de `\subsection*{Contribuciones principales}` a `\end{enumerate}`.
- **Nuevo:**
```latex
\subsection*{Contribuciones principales}

Este trabajo aporta seis contribuciones:

\begin{enumerate}
    \item \textbf{Un sistema transactivo de ocho especialistas con decisiones legibles.}
    Se construye un sistema de ocho módulos, uno por cada clase de ETH-80, cada uno con
    una sola memoria de contenido heteroasociativa y dos directorios, y se evalúa con un
    banco de 411 consultas ($\approx$50 por dominio).
    El sistema modela dos de los tres procesos de Wegner, la actualización del
    directorio y la coordinación de la recuperación; la asignación de información la
    hace la etiqueta de clase.
    Cada decisión se lee en registros concretos de las memorias.
    Una pista se acepta solo si está registrada en el módulo (en los 3064 pares de token
    y módulo del banco y de las consultas fuera de dominio, la compuerta coincide con la
    pertenencia al vocabulario del módulo; Sección~\ref{sec:lineas-base}), y el
    enrutamiento suma las transacciones registradas en los directorios, con su lectura
    normalizada por conteo de registros (Sección~\ref{sec:operaciones}).
    Los directorios, esa lectura, el rechazo de lo que ninguna memoria contiene y la
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
    Con un conjunto evaluado fijo, el directorio formado toma la misma decisión que la
    fase temprana en el 92.5\,\% de las consultas del sorteo principal, con un acierto
    equivalente, sin consultar a los ocho módulos (Sección~\ref{sec:calibracion-fija}).

    \item \textbf{Comparación con una sola memoria para las ocho clases.}
    Con el mismo contenido, repartirlo entre ocho especialistas deja el mismo acierto de
    clase sobre las 171 consultas reservadas (96.8 frente a 96.9\,\% con 200 imágenes
    por clase) y, con 200 imágenes por clase, acepta menos consultas fuera de dominio (2
    frente a 8 de 40; Sección~\ref{sec:eham-unica}).
    El recuerdo queda más cerca de la instancia real más cercana de la clase de la
    consulta (27.0 frente a 32.5 con 200 imágenes por clase)
    [PENDIENTE: exp11 d\_nn].

    \item \textbf{Familiaridad y nombre de una sola memoria.}
    Las memorias homoasociativas de cada dominio se leen de la heteroasociativa
    (ecuación~\eqref{eq:marginal}), así que cada módulo necesita una sola memoria de
    contenido.
    De ella salen dos lecturas, la familiaridad y el nombre, que el daño al azar separa:
    con el 1\,\% de las celdas destruidas, el módulo nombra 64 de 800 imágenes y las
    reconoce todas (Sección~\ref{sec:una-memoria}).

    \item \textbf{Evaluación experimental, con lo que agrega la memoria.}
    Se mide qué agrega la memoria asociativa frente a decisores simples sobre las mismas
    representaciones (un voto por las palabras del vocabulario, centroides, vecinos más
    cercanos y una tabla de conteos; Sección~\ref{sec:lineas-base}), la calibración del
    directorio con un conjunto evaluado fijo (Sección~\ref{sec:calibracion-fija}) y el
    sistema visual con un codificador entrenado sin la pérdida de clase
    (Sección~\ref{sec:codificador-sin-clase}).
    Se miden además nueve condiciones de calibración del directorio, con cuatro
    cantidades de consultas de formación, el efecto de los parámetros propios de la
    memoria ($\iota$ y $\kappa$), cuántas interacciones hacen falta para formar el
    directorio, cuánto contenido admite cada módulo, el comportamiento con imágenes, la
    comparación con una sola memoria para las ocho clases y la verificación de una sola
    memoria de contenido por módulo, junto con el costo computacional de reproducir
    todos los resultados.
\end{enumerate}
```
- **Fuentes:**
  - 3064 pares: líneas base, análisis posterior, punto 1.
  - 92.5: calibración fija, sorteo E0, B1 con N = 200 y 291.
  - 27.0 y 32.5: `tab:eham-unica`, de la corrida anterior; por eso el marcador.

## E4. Apertura de 6.1

- **Reemplaza** a estructura 7.1 y absorbe claridad S63, «maquinaria», «fase A» en `06:13`, «lectura B1» y los dos puntos de `06:8` y `06:21`.
- **Sin cambio:** `06:19` (la binarización por signo) es la decisión 15, y las figuras de `06:26-37` no se tocan.
- **Viejo:** `06:5-24`, desde el título `\subsection{La maquinaria transactiva funciona con ocho dominios; la representación es el límite}` hasta «(Sección~\ref{sec:disc-dominancia}).».
- **Nuevo:**
```latex
\subsection{El mecanismo transactivo funciona con ocho dominios; la clase la decide la representación}
\label{sec:disc-escala}

El mecanismo transactivo funciona con ocho dominios: los directorios
heteroasociativos, la lectura normalizada, el rechazo por contención, la actualización
perspectival del directorio ---en imagen--- y la coordinación punto a punto operan sin
ajustes por dominio.
En imagen, el registro completo de percepciones de la formación visual queda balanceado
(3.000 bits, el máximo con ocho módulos), y los directorios visuales de los módulos
enrutan las imágenes de prueba con dos falsos enrutamientos en 656
(Sección~\ref{sec:hemisferio-visual}).
En texto, las pistas se cuantizan por magnitud sobre una escala global
(Sección~\ref{sec:pipeline-semantico}), que puebla los 16 niveles del alfabeto (una
binarización por signo usaría 2), y con esa representación la precisión temprana sobre
el banco de 411 consultas es del 90.0\,\%.

Qué clase recibe cada consulta, en cambio, lo decide sobre todo la representación.
En texto, el solapamiento entre dominios es propiedad del léxico (tres frutas, tres
animales), persiste en el espacio de los vectores (Figura~\ref{fig:espacio-semantico}) y
en él cae la mayoría de los errores que quedan (Sección~\ref{sec:disc-dominancia}).
Con los mismos vectores y otros decisores, \texttt{pear} sigue siendo la clase difícil
en las 400 consultas de la calibración.
Un centroide la acierta el 8.0\,\% de las veces, los cinco vecinos más cercanos entre
el 62 y el 63\,\% y el vecino más cercano entre el 67 y el 71\,\%, frente al 70.0\,\% de
la fase temprana y al 76\,\% de la lectura normalizada (Sección~\ref{sec:lineas-base}).
En imagen, un centroide o un vecino más cercano sobre los mismos latentes aciertan de
652 a 655 de las 656 imágenes de prueba, sin rechazar ninguna, frente a 631 del sistema
(Sección~\ref{sec:lineas-base}); la separación entre clases la hace el codificador.
Con un codificador entrenado sin la pérdida de clase y el mismo mecanismo, el
enrutamiento visual baja del 96.2 al 70.4\,\% y los falsos enrutamientos suben de 2 a
169 de 656 (Sección~\ref{sec:codificador-sin-clase}).

El mecanismo tiene también límites propios.
La lectura del directorio necesita una normalización externa
(Sección~\ref{sec:disc-b1}); la contención estricta por coordenada rechaza 23 imágenes
de prueba que un vecino más cercano sobre los mismos latentes clasifica bien
(Sección~\ref{sec:disc-lineas-base}); el nombre se pierde con un daño del 1\,\%
(limitación (j)), y el contenido visual da soporte a entradas sin estructura
(limitación (c)).
```
- **Fuente de `pear`:** `filas_texto.json`, partición cal400, agregación `media`:
  - centroide 8.0;
  - 5nn 62.0 y 63.0;
  - 1nn 70.7 y 67.3;
  - fase temprana 70.0.
  - La tabla de conteos da 82.0, que queda fuera, como en el encuadre.

## E5. Subsección nueva de 06, después de `06:203` y antes de `06:205` (`\subsection{Limitaciones}`)

```latex

% ---------------------------------------------------------------
\subsection{Qué agrega la memoria asociativa frente a decisores simples}
\label{sec:disc-lineas-base}

La Sección~\ref{sec:lineas-base} compara el sistema con decisores que no usan memoria y
operan sobre los mismos vectores: un voto por las palabras del vocabulario de cada
clase, centroides, vecinos más cercanos y una tabla de conteos de tokens.
La comparación separa lo que aporta el mecanismo asociativo de lo que aportan las
representaciones.

\paragraph{En la clase, no agrega.}
En las 80 consultas del protocolo completo, en las que solo 11 traen el nombre de su
clase, el voto acierta el 79.4\,\% y los cinco vecinos más cercanos el 81.5\,\%, frente
al 81.2\,\% del sistema.
La razón está en la compuerta.
En los 3064 pares de token y módulo del banco y de las consultas fuera de dominio, la
memoria reconoce un token exactamente cuando está en el vocabulario del módulo, así que
decide quién vota igual que una búsqueda léxica.
Entre las clases que reciben algún voto, la activación media desempata, y con eso la
fase temprana gana 2.9 puntos al voto con desempate al azar en las 400 consultas de la
calibración (90.0 frente a 87.1\,\%); un voto ponderado por la frecuencia relativa de
cada etiqueta toma la misma decisión que la fase temprana en 380 de esas 400 consultas.
El directorio tampoco se distingue de contar tokens.
Una tabla de conteos formada con las mismas 400 consultas y la misma normalización
acierta el 92.3\,\%, frente al 93.0\,\% de la fase madura ($p = 0.58$).
En imagen, un centroide o un vecino más cercano sobre los mismos latentes aciertan de
652 a 655 de las 656 imágenes de prueba, frente a 631 del sistema, y el vecino más
cercano clasifica bien las 23 que el sistema rechaza.

\paragraph{Agrega rechazo sin un umbral ajustado.}
Los decisores de similitud no tienen umbral y aceptan las 40 consultas fuera de dominio;
el sistema acepta 2.
Un umbral de coseno fijado con los datos de evaluación separa bien las reservadas de las
fuera de dominio (AUROC de 0.97 a 0.99), pero el umbral que no pierde ninguna reservada
deja pasar de 9 a 23 de las 40.
En texto, este rechazo vale lo que una búsqueda léxica, porque la compuerta es la
pertenencia al vocabulario y las consultas fuera de dominio se escribieron sin palabras
de él; las dos que el sistema acepta son las únicas que tienen una.
Su ventaja aparece frente a un almacén único.
La EHAM única acepta 2, 2, 5 y 8 de las 40 con 25, 50, 100 y 200 imágenes por clase, y
el protocolo con doble compuerta 2 en todos los cortes (Sección~\ref{sec:eham-unica});
la diferencia es significativa con 200 imágenes por clase ($p = 0.031$) y no con 100
($p = 0.25$), y la segunda compuerta se decidió después de ver esas consultas
(limitación (g)).
En los modelos de emparejamiento global, la familiaridad es una suma sobre todas las
huellas guardadas~\cite{clark1996global}.
La EHAM única hace esa suma sobre las ocho clases, y cuanto más contiene, más consultas
ajenas encuentran soporte.
El rechazo visual no se probó con fotografías reales de otras categorías.

\paragraph{Agrega recuerdo.}
Un decisor devuelve una clase; la memoria devuelve además el contenido asociado.
De texto a imagen, con 200 imágenes por clase, el recuerdo del protocolo queda a 27.0
de la instancia real más cercana de la clase de la consulta, frente a 32.5 de la EHAM
única y 26.8 del oráculo (Sección~\ref{sec:eham-unica}) [PENDIENTE: exp11 d\_nn].
De imagen a texto, 113 de las 116 imágenes evocan una palabra de su dominio (97.4\,\%),
frente a un 34.8\,\% de tres palabras tomadas al azar de los ocho vocabularios
(Sección~\ref{sec:hemisferio-visual}).
El recuerdo depende de que el directorio acierte el módulo.
Con el codificador entrenado sin la pérdida de clase, una imagen bien enrutada evoca su
dominio en 80 de 81 casos, y una mal enrutada, en 7 de 32
(Sección~\ref{sec:codificador-sin-clase}).

\paragraph{Lo sostienen dos condiciones externas al mecanismo asociativo.}
La primera es la lectura normalizada del directorio.
Con un conjunto evaluado fijo, supera a la lectura cruda en todos los tamaños de
formación, por 4.5 a 8.8 puntos, y sin ella la fase madura queda 7.5 puntos por debajo
de la temprana con la formación más grande (Sección~\ref{sec:calibracion-fija}).
La segunda es un latente en que cada coordenada separe las clases, porque la contención
compara coordenada por coordenada.
Sin la pérdida de clase, la clase sigue en el latente (una sonda lineal la acierta en
el 94.2\,\%), pero repartida en combinaciones de coordenadas.
La separación por coordenada, medida como la varianza entre las medias de clase sobre la
varianza dentro de cada clase, baja de una mediana de 5.34 a 0.24, y la fracción de
imágenes de prueba que contiene también otra memoria sube del 0.5 al 82.9\,\%
(Sección~\ref{sec:codificador-sin-clase}).
La segunda condición tiene análogos en la memoria humana.
El hipocampo separa patrones parecidos antes de guardarlos~\cite{yassa2011pattern}, y
aprender categorías aumenta la sensibilidad a las dimensiones que las
distinguen~\cite{goldstone1994influences}; en este sistema, esa separación la hace el
codificador entrenado con la clase, antes de que la memoria registre nada.

\paragraph{El directorio localiza; no decide mejor.}
Con un conjunto evaluado fijo, el directorio formado con unas 200 consultas toma la
misma decisión que la fase temprana en el 92.5\,\% de las consultas que no vio (sorteo
principal), con un acierto equivalente.
La diferencia con la temprana es de $+0.2$ puntos con 200 consultas de formación y de
$+1.3$ con 291, y ninguna diferencia positiva se sostiene entre sorteos
(Sección~\ref{sec:calibracion-fija}).
Lo que el directorio aporta es encontrar al especialista sin difundir la consulta a los
ocho módulos.
Es la coordinación de la recuperación tal como la define Wegner, planear cómo encontrar
cada ítem~\cite{wegner1995computer}, y tiene la forma de lo que Sparrow y colaboradores
encontraron en las personas, que recuerdan mejor dónde está una información que la
información misma~\cite{sparrow2011google}.
En simulaciones de grupos, saber quién sabe qué conviene más en grupos grandes y en
entornos de tarea o de conocimiento cambiantes~\cite{ren2006contingent}.
Aquí son ocho módulos con contenido fijo y especialización asignada, como en la
condición de estructura asignada de Wegner, Erber y Raymond~\cite{wegner1991transactive},
así que no hay mucho que ganar en acierto.

En suma, la clase la deciden las representaciones: el vocabulario en texto y el
codificador entrenado con la clase en imagen.
Lo que la memoria asociativa agrega es el rechazo sin umbral ajustado, el recuerdo del
contenido asociado y decisiones que se leen en sus registros.
Como en las Secciones~\ref{sec:disc-wegner} y~\ref{sec:disc-una-memoria}, las analogías
de esta sección son estructurales, no causales.
```
- **Fuentes:**
  - Líneas base: proto80, el análisis posterior (puntos 1 a 3), el McNemar de cal400, la separabilidad y la imagen.
  - `ruteo.md`: 2, 2, 5 y 8 de 40.
  - `salida.md`: $p$ en M5.1 y el azar de 34.8 en E.1.
  - `tab:eham-unica`: 27.0, 32.5 y 26.8.
  - Codificador sin clase: 80 de 81, 7 de 32, 94.2, y el diagnóstico de 5.34 → 0.24 y 0.5 → 82.9.
  - Calibración fija: 4.5–8.8, −7.5, +0.2, +1.3 y 92.5.

## E6. Apertura de 07

- **Reemplaza** a estructura 7.5.
- **Viejo** (`07:8-10`):
```latex
El sistema cubre las ocho categorías de ETH-80 y opera de forma bidireccional
texto $\leftrightarrow$ imagen con rechazo claro en ambas direcciones, sin clasificadores
ni umbrales supervisados en la toma de decisiones.
```
- **Nuevo:**
```latex
El sistema cubre las ocho categorías de ETH-80 y opera en los dos sentidos,
texto $\leftrightarrow$ imagen, con rechazo explícito en ambos, y no responde cuando
nadie tiene soporte para la consulta.
Las decisiones de enrutamiento y de rechazo no usan clasificadores discriminativos; la
partición del contenido usa las etiquetas de clase, y el codificador visual se entrenó
con una pérdida de clasificación auxiliar, de la que depende el enrutamiento visual.
Del modelo de Wegner, el sistema implementa la actualización del directorio y la
coordinación de la recuperación; la asignación de información la hace la etiqueta.
```

## E7. Resultados principales

- **Reemplaza** el bloque entero: metodología M2.9 y Me.2, y estructura 9.3.
- **Sale** el «suma 3.0 puntos», porque es una cifra dentro de muestra.
- **Viejo:** `07:12-32`, de `\paragraph{Resultados principales.}` a «…con el llenado de 16 variantes del experimento 13.».
- **Nuevo:**
```latex
\paragraph{Resultados principales.}
Sobre el banco de 411 consultas ($N = 400$), el sistema alcanza una
\textbf{precisión temprana del 90.0\,\%} y una \textbf{precisión madura del 93.0\,\%}
con la lectura normalizada del directorio, con una concordancia temprana-madura del
95.8\,\%; la fase madura se evalúa sobre las consultas que formaron el directorio.
Con un conjunto evaluado fijo, de consultas que nunca se registran en el directorio, la
fase madura alcanza a la temprana sin superarla de forma robusta ($+0.2$ puntos con 200
consultas de formación y $+1.3$ con 291), y con la lectura cruda queda 7.5 puntos por
debajo (Sección~\ref{sec:calibracion-fija}).
Sobre 171 consultas reservadas, con directorios perspectivales, el protocolo enruta
correctamente el 96.8\,\% con 200 imágenes por clase (Sección~\ref{sec:eham-unica});
que supere a la cifra dentro de muestra depende de la composición de las reservadas,
que traen el nombre de su clase en el 87.7\,\% de los casos, frente al 49.8\,\% de las
consultas de la calibración.
La lectura normalizada deja la participación de \texttt{apple}, el módulo que la lectura
cruda favorece (20.5\,\%), en \textbf{13.8\,\%} (ideal 12.5\,\%).
En la dirección inversa, el hemisferio visual enruta el \textbf{96.2\,\%} de las 656
imágenes de prueba, vistas nuevas de objetos conocidos, con \textbf{dos falsos
enrutamientos} (99.7\,\% de precisión sobre las aceptadas), y el registro completo de
sus percepciones queda balanceado, con \textbf{3.000 bits} de entropía, el máximo con
ocho módulos.
Sobre las primeras 15 imágenes de prueba de cada clase (116 aceptadas), la evocación de
dominio es del \textbf{97.4\,\%}, frente a un azar del 34.8\,\%.
Sobre objetos físicos nunca vistos (\textit{leave-one-object-out}, diez pliegues), la
cobertura de punta a punta es del \textbf{89.2\,\%}, seis puntos por debajo de la de
vistas nuevas de objetos conocidos, con dos falsos enrutamientos de 3280.
Ese codificador había visto vistas de todos los objetos; con uno reentrenado sin el
objeto reservado, la cobertura con objetos nuevos es del 89.3\,\% y los falsos
enrutamientos suben a 33 de 984 [PENDIENTE: pliegues 10/10].
Con siete clases contrarias por módulo, el contenido no acepta ningún falso al llenar
con un latente por imagen (curva de capacidad) y acepta 5 de 656 imágenes de prueba
(0.8\,\%), todas entre animales, con el llenado de 16 variantes del experimento 13.
Sobre los mismos vectores, decisores sin memoria aciertan la clase tanto como el sistema
en texto, y más en imagen, sin rechazar nada (Sección~\ref{sec:lineas-base}).
```

## E8. Respuesta a la pregunta

- **Reemplaza** a estructura 7.6.
- **Conserva** el `\paragraph{Respuesta a la pregunta de investigación.}` exacto, que el generador usa para partir 07.
- **Viejo:** `07:34-52`, de ese `\paragraph` a «…pierden hacia su vecina).».
- **Nuevo:**
```latex
\paragraph{Respuesta a la pregunta de investigación.}
Sí, se puede.
Un sistema de memoria transactiva hecho de memorias asociativas entrópicas reparte,
recuerda y rechaza en ocho dominios: los directorios, la lectura normalizada, el
rechazo por contención, la actualización del directorio y la coordinación punto a punto
funcionan sin clasificadores discriminativos en las decisiones de enrutamiento y
rechazo.
No todo sale de las memorias.
La especialización la asigna la etiqueta de clase, el codificador visual se entrenó con
una pérdida de clasificación auxiliar, y la suma por tokens, la normalización del
directorio, el umbral $\tau$ y el rescate léxico operan fuera de ellas (limitación (k)).
El rechazo tiene dos fugas medidas, consultas que comparten tokens con un dominio y
entradas visuales sin estructura, que el umbral de energía cierra en su mayor parte
(limitaciones (a) y (c)).
Se midió con las 40 consultas fuera de dominio, entre ellas las 12 de la sonda de
rechazo, y con sondas visuales sintéticas, no con fotografías reales de otras
categorías.

Frente a decisores simples sobre las mismas representaciones, la memoria asociativa no
agrega acierto de clase.
En las 80 consultas del protocolo completo, un voto por las palabras del vocabulario y
los cinco vecinos más cercanos aciertan el 79.4 y el 81.5\,\%, frente al 81.2\,\% del
sistema, y en imagen un centroide o un vecino más cercano aciertan de 652 a 655 de las
656 imágenes de prueba, frente a 631 (Sección~\ref{sec:disc-lineas-base}).
Lo que agrega es un rechazo sin umbral ajustado.
Los decisores de coseno aceptan las 40 consultas fuera de dominio y el sistema 2, aunque
en texto ese rechazo vale lo que una búsqueda léxica.
Agrega también el recuerdo del contenido asociado, un rechazo que no empeora cuando
crece el contenido, a diferencia de una sola memoria con las ocho clases, y decisiones
que se leen en los registros de sus memorias.

Los límites vienen de las dos partes.
La clase la decide sobre todo la representación.
En texto, el léxico que comparten clases vecinas concentra los errores que quedan
(\texttt{pear} $\to$ \texttt{apple} 9 y \texttt{horse} $\to$ \texttt{cow} 6 de 28), y
\texttt{pear} es difícil para todos los decisores.
Con los mismos vectores, un centroide la acierta el 8.0\,\% de las veces y los vecinos
más cercanos entre el 62 y el 71\,\%, frente al 70.0\,\% de la fase temprana y al
76\,\% de la lectura normalizada.
En imagen, sin la pérdida de clase del codificador, el enrutamiento baja al 70.4\,\%.
El mecanismo tiene también límites propios: necesita la normalización externa del
directorio, su contención estricta por coordenada cuesta cobertura (rechaza 23 imágenes
que un vecino más cercano clasifica bien), el nombre se pierde con un daño del 1\,\% y
el contenido visual da soporte a entradas sin estructura.
El directorio funciona como un índice que localiza al especialista.
Formarlo cuesta interacción.
Con un conjunto evaluado fijo, la fase madura sube del 78.9 al 91.0\,\% entre 50 y 291
consultas de formación, hasta alcanzar a la temprana (89.7\,\%) sin superarla.
Y las consultas de las clases con léxico compartido se van hacia la clase vecina, como
en la sobrecarga de pistas de la memoria humana~\cite{watkins1975buildup}.
```

## E9. Frente a una EHAM única

- **Reemplaza** a estructura 7.7 y metodología M1.6.
- **Viejo** (`07:54-63`):
```latex
\paragraph{Frente a una EHAM única.}
Con el mismo contenido, el sistema transactivo recuerda con más fidelidad, no
mezcla dominios cuando la pista es compartida, acepta menos consultas fuera de
dominio cuando el contenido crece y en imagen responde
con un dominio ajeno menos veces (3.0\% de las imágenes, frente a 10.9\% con 200 por
clase).
Desde 50 imágenes por clase también clasifica algo mejor (1.4 puntos con 200); con 25,
no.
A cambio cubre menos, y el directorio le cuesta de 1.2 a 1.7 puntos de clase respecto
del oráculo desde 50 imágenes por clase.
```
- **Nuevo:**
```latex
\paragraph{Frente a una EHAM única.}
Con el mismo contenido, el sistema transactivo y una sola memoria con las ocho clases
aciertan la clase lo mismo desde 50 imágenes por clase.
Con 200, sobre el total de las 171 consultas reservadas, aciertan el 96.8 y el
96.9\,\% (diferencia de $-0.1$ puntos, $[-2.9, +2.9]$); con 25, la EHAM única acierta
más (97.6 frente a 93.2\,\%), porque el directorio todavía enruta peor.
El sistema transactivo recuerda con más fidelidad, mezcla menos los dominios cuando la
pista es compartida (acierta la clase entre el 79 y el 84\,\% de esas consultas, frente
al 48--52\,\% de la EHAM única) y en imagen responde con un dominio ajeno menos veces
(3.0\,\% de las imágenes, frente a 10.9\,\% con 200 por clase) [PENDIENTE: exp11 d\_nn].
Con 200 imágenes por clase acepta menos consultas fuera de dominio (2 frente a 8 de 40,
$p = 0.031$), mientras que la EHAM única acepta más cuanto más contiene (2, 2, 5 y 8);
la segunda compuerta que da esa ventaja se decidió después de ver esas consultas
(limitación (g)).
A cambio cubre menos, porque en imagen responde al 81.2\,\% de las imágenes, frente al
100\,\% de la EHAM única, y elegir el módulo con el directorio le cuesta 3.2 puntos de
clase sobre el total respecto del oráculo desde 50 imágenes por clase (6.8 con 25).
```

## E10. Trabajo futuro, después de `07:101` y antes del `\end{enumerate}` de `07:102`

El banco escrito por terceros ya está en metodología M5.5, así que aquí solo queda el rechazo con fotografías reales.
```latex
    \item \textbf{Rechazo con imágenes reales de otras categorías}
    (Sección~\ref{sec:disc-lineas-base}): medir cuántas fotografías de objetos ajenos a
    las ocho clases aceptan los directorios visuales y las memorias de contenido, frente
    a los decisores simples sobre los mismos latentes, que no rechazan ninguna; el
    rechazo visual de este trabajo solo se probó con sondas sintéticas.
```

## E11. Cierre

- **Reemplaza** a estructura 7.8. Al texto del encuadre le agregué la frase de los dos procesos de 7.8.
- **Viejo** (`07:106-110`):
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
Frente a decisores simples sobre las mismas representaciones, esas memorias no
clasifican mejor; lo que aportan es un rechazo que no necesita umbral ajustado, el
recuerdo del contenido asociado y decisiones que se leen en sus registros.
La clase la deciden las representaciones, y el mecanismo necesita dos cosas que no
salen de él: la normalización por conteo del directorio y un código en que cada
coordenada separe las clases.
```

---

# Parte 2. Cruces y su resolución

**Reglas:**
- En el contenido manda el encuadre y en la forma, claridad. Lo de la UACJ va en `.tex_uacj`.
- Donde marcadores llenó un punto, su versión reemplaza el «Nuevo» original.
- Los cruces que ya resolvió el índice no cambian, salvo los que caen en un pasaje del encuadre.

| # | Pasaje | Lo tocan | Resolución |
|---|---|---|---|
| 1 | `main:57-104` | estructura 9.1, 1.1 y 3.4; claridad (absorbida); metodología M2, M3 y M5; marcadores 12–14; E1 | **E1** |
| 2 | `main:47`, `main:50` | claridad S54 | Sin cruce; la fecha la decides tú (decisión 16) |
| 3 | `01:29-38` | estructura 3.1; E2; borde con 3.2 | **E2**. Si no quieres la pregunta del medio: 3.1, quitando «solo» |
| 4 | `01:69-114` | estructura 9.2; claridad (absorbida); marcadores 15; E3 | **E3** |
| 5 | `06:5-24` | estructura 7.1; claridad S63, 1.1, 3.8 y Parte 4, puntos 7 y 18; marcadores 5–6; E4 | **E4**, con la forma de claridad |
| 6 | `06:78-120` | estructura 4.4 en su versión de marcadores; fila de `06:86-88` | **Versión de marcadores.** Solo cambia la referencia: `\ref{sec:calibracion}` → `\ref{sec:calibracion-fija}` en «…según qué consultas se evalúen» |
| 7 | `06:178-182` | estructura 7.3 | Se aplica, con el marcador como `exp11 d\_nn` |
| 8 | `06:183-187` | M5.2 en su versión de marcadores | Versión de marcadores |
| 9 | `06:189-203` + E5 | M1.4 en su versión de marcadores; fila de `06:189-193`; E5 | **M1.4 de marcadores**, y E5 va después sin compartir líneas |
| 10 | `06:208-220` | M5.3 | Se aplica, con el marcador como `exp11 d\_nn` |
| 11 | `06:291-300`, limitación (f) | claridad S67; nota de M4.1; fila de `06:294-296` | **Texto combinado** (abajo) |
| 12 | después de `06:336`, limitación (k) | 3.3 en su versión de marcadores; encuadre (2 → 169); E5 | **Texto combinado** (abajo): las frases de la sonda salen porque las trae E5 |
| 13 | `07:8-10` | estructura 7.5; E6 | **E6** |
| 14 | `07:12-32` | M2.9, Me.2, 9.3; claridad (absorbida); marcadores 16; E7 | **E7** |
| 15 | `07:34-52` | estructura 7.6; claridad S50; marcadores 8–10; E8 | **E8** |
| 16 | `07:54-63` | estructura 7.7; M1.6 (marcadores 27–29); E9 | **E9** |
| 17 | `07:85-102` | M5.5, estructura 1.6 y 4.5, claridad 3.6, E10 | No comparten líneas; **E10 deja el banco de terceros a M5.5** |
| 18 | `07:106-110` | estructura 7.8; claridad 1.1 y Parte 4, punto 6; E11 | **E11**, con la frase de 7.8 |
| 19 | `05:28-29` | estructura 4.2 en su versión de marcadores (96.8) | Versión de marcadores |
| 20 | párrafo M2.2 | M2.2 en su versión de marcadores; `sec:calibracion-fija` | Si la sección nueva trae las cifras, la cola de M2.2 se reduce (abajo) |
| 21 | `05:256-260` | M2.7 en su versión de marcadores | La referencia pasa a `sec:calibracion-fija` |
| 22 | `05:439-443` | M4.1; marcadores 32; encuadre | M4.1 lleno con la cifra provisional (abajo) |
| 23 | `05:482-546` | M1.2, M1.3 y M1.5 | Sus marcadores y las celdas «[P]» pasan a `exp11 d\_nn` |
| 24 | término «índice» | claridad 1.1; E8 | No se usa «índice» como nombre del directorio; en E8 solo aparece como comparación |
| 25 | `sparrow2011google` en 06 | estructura 4.4; E5 | Distinto pasaje y distinto uso; E5 no repite la frase de 4.4 |
| 26 | `.tex_uacj` Resumen y Abstract | planteamiento, pieza 3; E1 | Cuatro ajustes (abajo) |
| 27 | `.tex_uacj` Cap. 1, la pregunta | pieza 1; E2 | **E2**: la misma pregunta en los dos documentos |
| 28 | `.tex_uacj` Cap. 1, Antecedentes | pieza 1; estructura 1.2, 2.1 y 2.2 | **Estructura**: la pieza 1 usaba definiciones que estructura retiró (abajo) |
| 29 | `.tex_uacj` Cap. 1, objetivo 1 y limitaciones | pieza 1; estructura 3.2 y 7.4; M5.4; claridad S67 | Texto combinado (abajo) |
| 30 | `.tex_uacj` Cap. 5 | pieza 4; E8 | Cambian el marcador y «del mediador» → «de la fase temprana» |

### Textos combinados

**Fila 11, limitación (f).** Viejo: `06:291-300`, de «Las cifras visuales principales (96.2\% de enrutamiento…» a «…fotos de otro origen son otra pregunta.».
```latex
Las cifras visuales principales (96.2\,\% de enrutamiento, evocación de dominio) miden
por tanto generalización a \emph{vistas nuevas de objetos conocidos}.
Con objetos nuevos, la cobertura de punta a punta baja del 95.5 al 89.2\,\%
(Sección~\ref{sec:objetos-nuevos}), pero en esa medición el codificador había visto
vistas de todos los objetos.
Con un codificador reentrenado sin el objeto reservado, la cobertura con objetos nuevos
es del 89.3\,\%, y el fallo ya no es solo rechazo: hay 33 falsos enrutamientos en 984
vistas, frente a 1 con el codificador común en los mismos pliegues
[PENDIENTE: pliegues 10/10].
Con diez objetos por clase, «objeto nuevo» sigue siendo un objeto de la misma
colección fotografiado en las mismas condiciones; la generalización a fotos de otro
origen no se midió.
```

**Fila 12, limitación (k).** Va después de `06:336`.
```latex

\paragraph{(k) Supervisión del codificador visual.}
El codificador se entrenó con la reconstrucción y una entropía cruzada de clasificación
de peso 0.1 (Sección~\ref{sec:percepcion}).
La cabeza clasificadora no participa en ninguna decisión, pero la pérdida moldea el
espacio latente sobre el que operan los directorios visuales y las memorias de
contenido; desde ese espacio, la cabeza auxiliar alcanza una precisión del 99.7\,\%.
Con un codificador entrenado sin esa pérdida, el enrutamiento de las 656 imágenes de
prueba es del 70.4\,\% (frente al 96.2\,\%), y la cobertura de punta a punta con
objetos nuevos, del 59.3\,\% (frente al 89.2\,\%).
El fallo deja además de ser rechazo, porque los falsos enrutamientos de prueba pasan de
2 a 169 de 656 y el rechazo queda casi igual (3.8 frente a 3.5\,\%;
Sección~\ref{sec:codificador-sin-clase}).
Por qué ocurre se discute en la Sección~\ref{sec:disc-lineas-base}.
```

**Fila 20, cola de M2.2.** Solo si `sec:calibracion-fija` trae las cifras. Reemplaza desde «Con un conjunto evaluado fijo, independiente de $N$ ---15 consultas…» hasta el final de la nota «…cinco semillas cada uno.}»:
```latex
Con un conjunto evaluado fijo, independiente de $N$, la formación mejora la fase madura
en consultas que no vio, pero solo hasta alcanzar a la temprana
(Sección~\ref{sec:calibracion-fija}).
```

**Fila 22, M4.1.** Reemplaza la frase que termina en «es del [PENDIENTE: exp16 con codificador por pliegue].»:
```latex
la cobertura de punta a punta con objetos nuevos es del 89.3\,\%, con 33 falsos
enrutamientos en 984 vistas, frente a 1 del codificador común en los mismos pliegues
[PENDIENTE: pliegues 10/10].
```

**Filas 26 a 30, sobre el texto de `revision_uacj_planteamiento_prosa.md`.**
- **Resumen, fuera de dominio.** «Rechaza lo que no conoce: acepta 2 de 40… con la pertenencia al vocabulario.» pasa a:
```latex
Rechaza lo que no conoce.
Acepta 2 de 40 consultas fuera de dominio, contra las 40 que aceptan los decisores de
coseno y, con 200 imágenes por clase, 8 de la memoria única, con una segunda compuerta
que se agregó después de ver esas consultas; su compuerta textual coincide con la
pertenencia al vocabulario.
```
- **Resumen, B1 y pliegues.** «Con objetos que ningún módulo vio, la cobertura de punta a punta es de [PENDIENTE: pliegues].» pasa a:
```latex
En texto, el directorio necesita su lectura normalizada por conteo, y sin ella la fase
madura queda 7.5 puntos por debajo de la temprana.
Con objetos que ningún módulo vio y un codificador reentrenado sin ellos, la cobertura
de punta a punta es del 89.3\,\%, con 33 falsos enrutamientos en 984 vistas
[PENDIENTE: pliegues 10/10].
```
  Además, «Recupera en ambas direcciones: responde» pasa a «Recupera en ambas direcciones, y responde».
- **Abstract**, los mismos tres cambios:
  - «It rejects what it does not know. It accepts 2 of 40 out-of-domain queries, against all 40 for the cosine rules and, with 200 images per class, 8 for the single memory, with a second gate added after seeing those queries; its textual gate coincides with vocabulary membership.»
  - «In text, the directory needs its count-normalized reading, and without it the mature phase stays 7.5 points below the early phase. On objects no module has seen, with an encoder retrained without them, end-to-end coverage is 89.3\,\%, with 33 false routings in 984 views [PENDING: folds 10/10].»
  - «It retrieves in both directions, and it answers».
- **Capítulo 1, la pregunta.** El `quote` de «Definición del problema» se sustituye por el de E2.
- **Capítulo 1, Antecedentes.** Desde «Wegner~\cite{wegner1987transactive} describió la memoria transactiva…» hasta «…que envía cada consulta directamente al especialista.»:
```latex
Wegner~\cite{wegner1987transactive} definió la memoria transactiva como un conjunto de
sistemas de memoria individuales en combinación con la comunicación que ocurre entre los
individuos (p.~186).
En un trabajo posterior la formuló como un modelo de red de
computadoras~\cite{wegner1995computer}, en el que cada miembro guarda parte de lo que el
grupo sabe y lleva un directorio de quién sabe qué.
El directorio no repite el contenido.
Solo indica a quién preguntar.
En ese modelo, Wegner distingue tres procesos: la actualización del directorio, en la
que los miembros aprenden quién sabe qué en el grupo; la asignación de información, que
asigna cada ítem de memoria a un miembro, y la coordinación de la recuperación, que
planea cómo encontrar cada ítem.
```
- **Capítulo 1, objetivo 1.** «Verificar que todas las decisiones salen de operaciones de las memorias y que una sola memoria…» pasa a «Verificar que las decisiones de enrutamiento y rechazo no usan clasificadores discriminativos, declarar las operaciones que quedan fuera de las memorias y comprobar que una sola memoria de contenido por módulo basta para tomarlas.»
- **Capítulo 1, limitaciones.** «el punto de control del codificador y el número de variantes se eligieron mirando el conjunto de prueba (limitación (g));» pasa a «varias decisiones del protocolo, entre ellas el punto de control del codificador y el número de variantes, se tomaron con información de los datos de evaluación (limitación (g));».
- **Capítulo 5.**
  - «es de [PENDIENTE: pliegues]» pasa a «es del 89.3\,\%, con 33 falsos enrutamientos en 984 vistas [PENDIENTE: pliegues 10/10]».
  - «la decisión del mediador» pasa a «la decisión de la fase temprana».

---

# Parte 3. Orden único de aplicación

**Reglas generales:**
1. Cada archivo se aplica de abajo hacia arriba, y los «Viejo» se buscan por texto.
2. En cada pasaje se aplica el texto que ganó en la parte 2. Los puntos de claridad marcados como absorbidos no se aplican aparte.
3. Al terminar los puntos de cada archivo:
   - las reglas mecánicas de claridad (Parte 3) se aplican por búsqueda;
   - la pasada de forma (decisión 7) se hace solo sobre los textos de estructura que no cruzan con claridad.

**`main.tex`**
1. **E1.**
2. Claridad S54 en la portada.

**`01_introduccion.tex`**
1. Estructura 8.2 (`01:118-120`).
2. Claridad S69 (`01:124-127`).
3. **E3.**
4. Estructura 3.2 (`01:55-60`).
5. Claridad 3.7 en `01:51`.
6. **E2.**
7. Claridad 3.7 en `01:26`.
8. Estructura 1.2 (`01:15-23`).
9. Estructura 2.2 (`01:4-13`).
10. Reglas mecánicas y pasada de forma.

**`02_marco_teorico.tex`** (el encuadre no lo toca)
1. Estructura 8.1, que va después de `02:322`.
2. Estructura 5.2.
3. Estructura 2.1.
4. Claridad S29, 3.7, S62, S67, S30, S17 y S4, de abajo hacia arriba.
5. Estructura 5.1.
6. Claridad S59, S24, S53, S18, S70, S16 y las filas 3.7 que quedan.
7. Reglas mecánicas y pasada de forma.

**`03_arquitectura.tex`** (el encuadre no lo toca)
1. Claridad S9, S70 y S18.
2. Estructura 5.3.
3. Claridad S35, S62 y 3.7.
4. Claridad S7.
5. Estructura 1.4.
6. Claridad S19, S68, S23, S52, 3.6, S69, S8, S20 y S26.
7. Estructura 2.3.
8. Estructura 4.1.
9. Claridad S70 y 3.7 en `03:60-62`.
10. La notación 1.3, por búsqueda.
11. Decisión 14.
12. Reglas mecánicas.

**`04_metodologia.tex`** (el encuadre no lo toca)
1. M2.8.
2. Claridad S42, S10 y S5.
3. Estructura 7.4.
4. Claridad S3.
5. M3.2.
6. Estructura 2.4.
7. M3.1, más tu frase (decisión 12).
8. Claridad S64, S46, S67, S70, S37.
9. Me.4.
10. Claridad S56, S25, S11 (con S66) y 3.7.
11. Me.4 en `04:15`.
12. Decisión 6.
13. Claridad S2.
14. Reglas mecánicas.

Hueco: ninguna propuesta describe en 04 el método de las tres evaluaciones nuevas. Si sus secciones no lo traen, falta una frase en `sec:organizacion`.

**`05_resultados.tex`**
1. **Los puntos, de abajo hacia arriba:**
   - claridad S67, S52, S60, S64, S49 y S48 (S48 según la parte 4);
   - claridad S70 y S58;
   - M5.1, M1.5 (con sus marcadores como `exp11 d\_nn`), M1.1, M1.3, M1.2 y M1.7, con S61 y S53;
   - claridad S70, S62 y S33;
   - **M4.1**, lleno como en la fila 22;
   - claridad S70, S52, S41 y Me.1;
   - claridad 3.3, 3.7, S67, S12, S38, S36, S32 y S21;
   - estructura 4.3;
   - M2.7 (fila 21);
   - claridad S47, S34, S27, S65, S62, S30, S36b, S53 y S10;
   - M2.7 en `05:148-150`;
   - estructura 5.4;
   - claridad S65 y S40;
   - M2.6, M2.3 y M2.4;
   - claridad S13;
   - **M2.2** y **4.2**, en su versión de marcadores;
   - M2.1;
   - claridad S62 y S55.
2. **Aquí entran las tres secciones nuevas**, ya con los «Viejo» de 05 aplicados:

| Etiqueta | Dónde | Cifras que debe traer, porque los textos de esta entrega las citan con su `\ref` |
|---|---|---|
| `sec:calibracion-fija` | después de `sec:calibracion`, antes de `\subsection{Protocolo completo}` (`05:143`) | 120 consultas fijas; madura de 78.9 a 91.0; temprana 89.7; +0.2 y +1.3; −7.5 con la lectura cruda; B1 sobre A por 4.5 a 8.8; concordancia del 92.5 en E0 |
| `sec:codificador-sin-clase` | después de `sec:objetos-nuevos`, antes de `sec:eham-unica` (`05:456`) | 462 de 656 (70.4); falsos de 2 a 169; rechazo de 3.5 a 3.8; objeto nuevo 59.3; sonda 94.2; separación de 5.34 a 0.24; otra memoria de 0.5 a 82.9; 80 de 81 y 7 de 32 |
| `sec:lineas-base` | después de `sec:eham-unica`, antes de `sec:una-memoria` (`05:553`) | proto80: 79.4, 81.5 y 81.2 (11 de 80 con el nombre); 3064 pares; 90.0 frente a 87.1; 380 de 400; 92.3 frente a 93.0, $p = 0.58$; 40 de 40; AUROC 0.97–0.99; de 9 a 23; 652–655 frente a 631 y las 23 rechazadas; `pear` 8.0, 62–63, 67–71 y 70.0 |

   La posición la decide la propuesta que las trae. Las etiquetas no pueden cambiar.
3. Reglas mecánicas sobre todo 05, incluidas las secciones nuevas.

**`06_discusion.tex`**
1. **Limitación (k)** (fila 12).
2. Estructura 6.2.
3. Claridad 3.6 y S45.
4. M5.4.
5. **Limitación (f)** (fila 11), en lugar de claridad S67 ahí.
6. Claridad S70, 3.8 y 3.6.
7. Me.3, con claridad 3.7 y 3.6.
8. Claridad 1.1 y 3.7.
9. Claridad S31.
10. M5.3.
11. **E5.**
12. M1.4 de marcadores.
13. M5.2 de marcadores.
14. Estructura 7.3.
15. Claridad 1.1 en `06:176`.
16. Estructura 6.1.
17. Estructura 4.4 de marcadores (fila 6).
18. M2.5.
19. Estructura 5.5.
20. Estructura 7.2.
21. Claridad S44.
22. **E4.**
23. Reglas mecánicas y pasada de forma.

**`07_conclusiones.tex`**
1. **E11.**
2. **E10.**
3. Claridad 3.6.
4. Estructura 4.5.
5. Estructura 1.6.
6. M5.5.
7. Estructura 9.4.
8. Estructura 6.3.
9. Claridad S57.
10. **E9.**
11. **E8.**
12. **E7.**
13. **E6.**
14. Reglas mecánicas.

**`referencias.bib`**
1. Las 35 entradas de estructura, después del cotejo de la decisión 8.
2. Las 2 del encuadre, cuyos campos escribí yo y hay que cotejar con los registros que enlaza el encuadre:
```bibtex
@article{yassa2011pattern,
  author  = {Yassa, Michael A. and Stark, Craig E. L.},
  title   = {Pattern separation in the hippocampus},
  journal = {Trends in Neurosciences},
  year    = {2011}, volume = {34}, number = {10}, pages = {515--525},
  doi     = {10.1016/j.tins.2011.06.006}
}
@article{goldstone1994influences,
  author  = {Goldstone, Robert L.},
  title   = {Influences of categorization on perceptual discrimination},
  journal = {Journal of Experimental Psychology: General},
  year    = {1994}, volume = {123}, number = {2}, pages = {178--200},
  doi     = {10.1037/0096-3445.123.2.178}
}
```
3. Decisión 9: quitar las cuatro entradas que quedan sin citar.

**Después de `.tex8`**
1. Compilar y revisar referencias indefinidas. Hay una etiqueta nueva mía, `sec:disc-lineas-base`, y las tres de 05.
2. Correr `generar_capitulos.py`. E2 y E8 cumplen sus requisitos.
3. Aplicar las piezas del planteamiento con las filas 26 a 30, siempre después del generador, porque este sobrescribe `Introduccion.tex`, `Capitulo1.tex`, `Capitulo5.tex` y `Resumen.tex`. Después no hay que volver a correrlo.
4. Descomentar `\include{Abstract}`.
5. Hacer la pasada 3.7 sobre las piezas del planteamiento.

---

# Parte 4. Marcadores que quedan

| Marcador | Depende de | Dónde | Cuántos |
|---|---|---|---|
| `[PENDIENTE: exp11 d\_nn]` | la corrida completa de exp11 con recuerdo: d_nn, mezcla 79–84, dominio ajeno 3.0, clase sobre las respondidas y la doble compuerta sobre las 171 | E1, E3, E5 y E9; estructura 7.3; M1.2 (que cubre las 8 celdas «[P]» de M1.3), M1.5 (dos) y M5.3; en `.tex_uacj`, Resumen, Abstract y Cap. 5 | 9 en `.tex8` (más 8 celdas) y 3 en `.tex_uacj` |
| `[PENDIENTE: pliegues 10/10]` | exp16 con el codificador por pliegue, hoy en 3 de 10 (provisional: 89.3 %, 33 de 984) | E1, E7, M4.1 y la limitación (f); en `.tex_uacj`, Resumen, Abstract y Cap. 5 | 4 en `.tex8` y 3 en `.tex_uacj` |
| `[PENDIENTE: exp11 corregido]` | ninguna corrida en curso (el 1.3 % de destinos entre arquitecturas) | claridad S48 | 1. Recomiendo quitar la cifra junto con la decisión 11 |

**Qué hacer cuando lleguen:**
- **exp11 d_nn:** se actualizan el 27.0, el 79–84, el 3.0 y las celdas de la Tabla 5. Si la fidelidad deja de favorecer al protocolo, también cambian «recuerda con más fidelidad» (E1, E3, E9) y «Agrega recuerdo» (E5).
- **pliegues 10/10:** cambian el 89.3 y el 33 de 984, que pasa a contarse sobre 3280. El 89.2 del codificador común sigue valiendo, porque es otra medida.

**Fuera de la tesis:**
- El README de los pliegues parciales dice 2 pliegues, pero hay 3.
- El paratexto UACJ (`tesis_uacj.tex`, Agradecimientos, Dedicatoria y Apéndice A) sigue con sus `[PENDIENTE]`.