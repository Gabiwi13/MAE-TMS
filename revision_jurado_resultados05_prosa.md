# Propuesta viejo/nuevo: resultados nuevos para 05

Todo está pendiente de tu aprobación. No toqué `.tex8`, no hice commit, no hice push y no creé ramas. Solo hice el `checkout` de `una-hetero` en `6c1a9fb`, y el árbol quedó limpio. `.tex8` es igual en `6197bc3` y en `6c1a9fb`, así que las líneas que citan las otras propuestas siguen valiendo. Los textos «Viejo» los copié de `.tex8/secciones/` en `6c1a9fb`.

## Lo que necesito que decidas

1. **Tres propuestas de marcadores quedan reemplazadas.** El punto R4 junta en un solo bloque M1.1, M1.2 (con las filas de M1.3) y M5.1 de `revision_jurado_marcadores.md`. Si apruebas R4, esos tres no se aplican aparte. El punto 4.2 de marcadores (`05:28-29`, que pasa de 97.0 a 96.8) no cambia.
2. **Redondeo.** Uso el de la tabla `tab:calibracion`, que redondea al par: 85.25 da 85.2 y 91.75 da 91.8. Así, 369/400 = 92.25 queda en **92.2** y 83.25 en **83.2**. El README de líneas base y el encuadre ponen 92.3 y 83.3, así que tienes que elegir una sola convención.
3. **Las 171 reservadas no se compararon con el protocolo corregido.** Las pruebas de McNemar del README de líneas base usan el protocolo de la corrida anterior (97.0 %), que no se repitió con los directorios corregidos. En el texto doy la media corregida (96.8) sin prueba de McNemar. La prueba consulta por consulta la hago contra la fase temprana, que no usa el directorio, y la declaro como análisis posterior.
4. **Cifras de `pear` calculadas por mí.** Las calculé de `results/lineas_base/filas_texto.json`, con la agregación por media: centroide 8.0, 5-NN 62.0/63.0, 1-NN 70.7/67.3 y fase temprana 70.0. No están en el README. Las pongo para que la cita a `sec:lineas-base` del punto E4 del encuadre tenga dónde apoyarse, y van declaradas como posteriores.
5. **El README de pliegues está desactualizado.** Habla de 2 pliegues, pero `tablas.md`, `resumen.json` y `raw/` tienen 3. Uso los 3. Tampoco dice si con el pliegue 3 se corrió el control opcional (reentrenar con todo el conjunto de entrenamiento). Lo trato como no corrido.
6. **El experimento 19 sí está en `results/`, así que lo cito.** Eso pide agregar «19» a la nota al pie de `04:156-160` (punto U3).
7. **Remuestreo con N = 100.** El extremo superior del intervalo para N = 100 en `resumen.json` es +1.95, con dos decimales (`ruteo.md` lo da como +2.0). Pongo +1.9, igual que marcadores M1.1, que vio el valor de más decimales (+1.949).
8. **El 1.3 % de `05:575` sigue sin resolver.** Es el punto 37 de marcadores y aquí no lo toco.
9. **La clase sobre las respondidas del protocolo corregido.** Se podría derivar de las filas de ruteo con la identidad que se comprobó en los raw oficiales. El README de exp11 la deja fuera, así que la marco como pendiente.

## Ubicación (resumen; el detalle está en R6)

Orden de 05 después de aplicar: `sec:calibracion` → **`sec:calibracion-fija`** → `sec:proto-completo` → `sec:param-iota-kappa` → `sec:formacion` → `sec:capacidad` → `sec:hemisferio-visual` → `sec:objetos-nuevos` (con **R5**) → **`sec:codificador-sin-clase`** → `sec:eham-unica` (con **R4**) → **`sec:lineas-base`** → `sec:una-memoria` → `sec:costo`.

---

## R1. Líneas base sin memoria asociativa

**Dónde:** es una inserción después de `05:551`, el último renglón de `sec:eham-unica`, y antes de `05:553` (`\subsection{Una memoria de contenido por módulo}`). No tiene «Viejo».

**Nuevo:**
```latex

% ---------------------------------------------------------------
\subsection{Líneas base sin memoria asociativa}
\label{sec:lineas-base}

Esta sección mide qué agrega la memoria asociativa frente a decisores simples que usan
exactamente los mismos vectores que el sistema.
Los decisores, las particiones y los criterios de lectura se fijaron antes de correr.

\paragraph{Texto.}
Cada consulta se divide en tokens y se vectoriza con fastText como en el sistema
(Sección~\ref{sec:pipeline-semantico}), y los decisores la comparan con las 21
etiquetas de cada clase.
El \emph{voto} cuenta cuántos tokens de la consulta están en el vocabulario de cada
clase (sus etiquetas y sus alias por lema) y se abstiene si ninguno está.
El \emph{centroide} compara con la media de los vectores de las etiquetas de la clase,
simple o ponderada por la frecuencia con que cada etiqueta entra al llenado.
El vecino más cercano (1-NN) y los cinco más cercanos (5-NN) votan por la clase de las
etiquetas más cercanas por coseno.
Los decisores de similitud puntúan cada token por separado y suman, o comparan la media
de los vectores de la consulta.
Ninguno tiene umbral: aceptan toda consulta con algún token con vector.
Cuando varias clases empatan en el máximo, el acierto se cuenta como su esperanza bajo
un sorteo uniforme entre ellas.
Para comparar con el directorio se agregó una \emph{tabla de conteos}, que se forma con
las mismas consultas y el mismo ganador temprano que el directorio, pero cuenta los
tokens exactos de cada clase en lugar de registrarlos en una memoria, y se lee con la
misma normalización B1.
Se evaluaron las 400 consultas de la calibración, las 80 del protocolo completo y las
171 reservadas de la comparación con una sola EHAM (Sección~\ref{sec:eham-unica}),
además de las 40 consultas fuera de dominio.
Esas 40 se escribieron sin palabras del vocabulario, salvo las 12 de la sonda de rechazo
(Sección~\ref{sec:proto-completo}), que son anteriores a esa regla.
La Tabla~\ref{tab:lineas-base-texto} da los resultados.

\begin{table}[H]
    \centering
    \caption{Decisores sin memoria asociativa sobre los mismos vectores de los tokens, en
    las 400 consultas de la calibración, las 80 del protocolo completo y las 171
    reservadas de la comparación con una sola EHAM. Acierto sobre el total (\%), con la
    falta de respuesta como fallo; los empates en el máximo se resuelven por sorteo
    uniforme y se cuenta la esperanza, y entre paréntesis va el número de consultas
    empatadas. Vectores sin cuantizar; con la cuantización de 16 niveles el acierto
    cambia 1.3 puntos como máximo. \emph{Por token}: cada token puntúa y se suma;
    \emph{media}: se compara la media de los vectores de la consulta. La tabla de conteos
    y la fase madura se forman con las mismas 400 u 80 consultas que se evalúan y, en las
    reservadas, con las 240 de formación; en las reservadas, la fase madura es el
    protocolo con 200 imágenes por clase. Última columna: consultas fuera de dominio
    aceptadas, de 40 (entre paréntesis, con la doble compuerta; la tabla de conteos,
    formada con las 400, las 80 y las 240). Fuente: \texttt{results/lineas\_base/} y,
    para el protocolo, \texttt{results/experimento11\_protocolo\_corregido/ruteo/}.}
    \label{tab:lineas-base-texto}
    \small
    \begin{tabular}{lcccc}
        \toprule
        Decisor & 400 & 80 & 171 & Fuera de dominio \\
        \midrule
        Voto por vocabulario                & 87.1 (49) & 79.4 (10) & 95.1 (12) & 2 \\
        Centroide, por token                & 82.8      & 77.5      & 86.5      & 40 \\
        Centroide, media                    & 81.2      & 77.5      & 84.8      & 40 \\
        Centroide por frecuencia, por token & 83.8      & 78.8      & 87.7      & 40 \\
        Centroide por frecuencia, media     & 83.2      & 78.8      & 87.1      & 40 \\
        1-NN, por token                     & 80.8 (63) & 80.0 (8)  & 79.7 (44) & 40 \\
        1-NN, media                         & 85.6 (73) & 76.0 (23) & 95.1 (11) & 40 \\
        5-NN, por token                     & 84.0 (16) & 80.0 (2)  & 87.3 (9)  & 40 \\
        5-NN, media                         & 87.5 (52) & 81.5 (13) & 92.7 (11) & 40 \\
        \midrule
        Tabla de conteos                    & 92.2      & 78.8      & 94.7      & 8, 3 y 4 \\
        \midrule
        Fase temprana                       & 90.0      & 81.2      & 97.7      & 2 \\
        Fase madura, lectura B1             & 93.0      & 81.2      & 96.8      & 4 (2) \\
        \bottomrule
    \end{tabular}
\end{table}

\paragraph{En la clase de texto, los decisores sin memoria quedan al nivel del sistema.}
En las 80 consultas del protocolo completo, que traen el nombre de su clase en 11 casos,
el 5-NN sobre la media acierta el 81.5\,\%, el 1-NN por token el 80.0\,\% y el voto el
79.4\,\%, frente al 81.2\,\% de las fases temprana y madura.
McNemar exacto contra la fase madura no distingue al 5-NN (6 consultas que solo él
acierta frente a 12 que solo acierta el sistema, $p = 0.24$) ni al voto (1 frente a 7,
$p = 0.07$); en estas pruebas, un empate de la línea base cuenta como fallo.
En las 400 de la calibración, la fase madura (93.0\,\%) supera a todos los decisores
sin formación: el mejor, el 5-NN sobre la media con vectores cuantizados, acierta el
88.0\,\% (4 frente a 50, $p = 4 \cdot 10^{-11}$).
Esa ventaja viene de formar el directorio con las mismas 400 consultas que se evalúan,
porque la tabla de conteos formada igual acierta el 92.2\,\% y no se distingue del
directorio (5 frente a 8, $p = 0.58$); en las 80, acierta el 78.8\,\% (2 frente a 4,
$p = 0.69$).
En las 171 reservadas, que traen el nombre de su clase en 150 casos, el voto y el 1-NN
sobre la media aciertan el 95.1\,\%, la tabla de conteos formada con las 240 consultas
de formación el 94.7\,\%, la fase temprana el 97.7\,\% y el protocolo el 96.8\,\%.

\paragraph{Fuera de dominio, los decisores sin umbral lo aceptan todo.}
Los decisores de similitud aceptan las 40 consultas fuera de dominio; el voto y la fase
temprana aceptan 2, y el protocolo, 4, que la doble compuerta baja a 2.
Un umbral sobre la similitud separa bien los dos conjuntos: con la media de la consulta,
el área bajo la curva ROC entre las 171 reservadas y las 40 fuera de dominio va de 0.97
a 0.99.
Pero el umbral que deja pasar todas las reservadas acepta de 9 a 23 de las 40, y el que
deja pasar el 95\,\% de ellas, de 2 a 4; los dos se fijan con las consultas evaluadas, lo
que favorece a la línea base.

\paragraph{Análisis posterior: la compuerta es la pertenencia al vocabulario.}
Lo que sigue se analizó después de ver los resultados anteriores.
En los 3064 pares de token y clase que forman los tokens del banco y de las 40 consultas
fuera de dominio con las ocho clases, el reconocimiento con compuerta de la fase
temprana da soporte exactamente cuando el token está en el vocabulario de la clase: los
101 pares del vocabulario se aceptan y los 2963 de fuera se rechazan.
Por eso la fase temprana acepta las mismas consultas que el voto, consulta por consulta:
393 de 400, 76 de 80, 171 de 171 y 2 de 40.
Las dos fuera de dominio que pasan, «a kitchen appliance that heats food» (por
\textit{food}, a \texttt{apple}) y «a wooden table and chairs» (por \textit{table}, a
\texttt{cup}), son las únicas de las 40 con un token del vocabulario.
Lo que la fase temprana agrega sobre el voto es el desempate.
Todas las consultas en que difieren en acierto son empates del voto, y en ellos la fase
temprana acierta 34 de 49 en las 400 (el sorteo espera 22.5), 6 de 10 en las 80 (4.5) y
10 de 12 en las 171 (5.7).
En las 171, McNemar contra la fase temprana da $p = 0.002$ si el empate del voto cuenta
como fallo (0 frente a 10) y $p = 0.5$ si cuenta a su favor (2 frente a 0).
Un voto ponderado por la frecuencia relativa de cada etiqueta en el llenado de su clase
toma la misma decisión que la fase temprana en 380 de 400, 76 de 80 y 167 de 171
consultas, y acierta el 88.0, 80.0 y 96.5\,\%.
La clase difícil es la misma para todos los decisores: en las 400, un centroide acierta
\texttt{pear} el 8.0\,\% de las veces, el 5-NN sobre la media el 62.0 y el 63.0\,\%, y
el 1-NN sobre la media el 70.7 y el 67.3\,\% (sin cuantizar y cuantizados), frente al
70.0\,\% de la fase temprana.

\paragraph{Imagen.}
Los decisores de imagen usan los mismos latentes que el sistema: los de las 656
imágenes de prueba y, como puntos de cada clase, los 3200 del llenado (200 imágenes con
sus 16 variantes) o solo los 200 de las imágenes originales.
Son el centroide de la clase, el vecino más cercano y los cinco más cercanos, con
distancia euclidiana y coseno, y no tienen umbral.
El sistema enruta con los directorios visuales, con la misma regla de entrada y el mismo
umbral de energía de la Sección~\ref{sec:hemisferio-visual}.
La Tabla~\ref{tab:lineas-base-imagen} da los resultados.

\begin{table}[H]
    \centering
    \caption{Decisores sin memoria asociativa sobre los latentes de las 656 imágenes de
    prueba, con los puntos de cada clase tomados de los 3200 latentes del llenado (16
    variantes) o de los 200 de las imágenes originales (variante 0). Ninguno tiene umbral,
    así que no rechazan y todos sus errores son falsos. Discordantes: imágenes que solo
    acierta la línea base y que solo acierta el sistema, con 16 variantes; McNemar exacto
    da $p < 10^{-4}$ en todas las filas, también con la variante 0. Con los latentes
    cuantizados que ve el directorio, los aciertos cambian a lo sumo en una imagen. La
    cabeza del codificador no participa en el sistema. Fuente:
    \texttt{results/lineas\_base/}.}
    \label{tab:lineas-base-imagen}
    \small
    \begin{tabular}{lccccc}
        \toprule
        & \multicolumn{2}{c}{16 variantes} & \multicolumn{2}{c}{Variante 0} & \\
        \cmidrule(lr){2-3} \cmidrule(lr){4-5}
        Decisor & Aciertos & Falsos & Aciertos & Falsos & Discordantes \\
        \midrule
        Sistema (23 rechazos)  & 631 & 2 & ---  & --- & ---    \\
        Centroide euclidiano   & 652 & 4 & 652  & 4   & 23 / 2 \\
        Centroide coseno       & 653 & 3 & 653  & 3   & 23 / 1 \\
        1-NN euclidiano        & 655 & 1 & 652  & 4   & 24 / 0 \\
        1-NN coseno            & 655 & 1 & 654  & 2   & 24 / 0 \\
        5-NN euclidiano        & 655 & 1 & 654  & 2   & 24 / 0 \\
        5-NN coseno            & 655 & 1 & 654  & 2   & 24 / 0 \\
        \midrule
        Cabeza del codificador & 654 & 2 & ---  & --- & 23 / 0 \\
        \bottomrule
    \end{tabular}
\end{table}

\paragraph{En imagen, los decisores sin memoria superan al enrutamiento.}
Con las 16 variantes, los decisores aciertan de 652 a 655 de las 656 imágenes de prueba,
con 1 a 4 falsos, frente a 631 del sistema, con 2 falsos y 23 rechazos.
La línea base acierta sola 23 o 24 imágenes y el sistema de 0 a 3, con 16 variantes o
solo con la original, y McNemar exacto da $p < 10^{-4}$ en todos los casos.
El 1-NN euclidiano clasifica bien las 23 imágenes que el sistema rechaza, incluidas las
cuatro que no pasan el umbral de energía.
De los dos falsos del sistema, ambos de \texttt{horse} a \texttt{dog}, uno lo fallan
también todas las líneas base y el otro lo aciertan todas.
La cabeza clasificadora del codificador acierta 654.
Se cumple el criterio fijado antes de correr: un decisor simple sobre los mismos
latentes acierta al menos 631 imágenes con 2 falsos o menos, así que en la clase de
imagen el enrutamiento no agrega sobre el codificador.
El rechazo visual, que es lo que el directorio agregaría, no se puede valorar aquí,
porque no hay imágenes reales de otras categorías.
```

**De dónde sale cada cifra.** «LB» es `results/lineas_base/README.md`; «RT» es `resumen_texto.json`, «RI» `resumen_imagen.json` y «AP» `analisis_posterior_texto.json`, los tres en esa carpeta.

- **Método:** LB, «Diseño (escrito antes de correr)». Las 21 etiquetas por clase son los 168 puntos de LB, y coinciden con `results/reanalisis_jurado/salida.md`, tabla M3.2. Las 12 de la sonda anteriores a la regla están en LB, «Rechazo».
- **Tabla de texto:** RT, `tabla`, en crudo y con sus `empates`.
  - La diferencia máxima entre crudo y cuantizado es 1.25 (`centroide_frec|token`, en las 80). La calculé yo sobre RT.
  - Las fuera de dominio salen de RT, filas `ood40` con `acepta`. La tabla de conteos da 8, 3 y 4, en las filas `tabla_conteos[...]`.
  - El protocolo da 96.8 y «4 (2)»: `results/experimento11_protocolo_corregido/ruteo/ruteo.md`, tablas «Texto» y «Fuera de dominio», N = 200.
  - Fase temprana 97.66 y madura B1 93.0 / 81.25: RT.
- **Composición** (11, 199 y 150): RT, `composicion`, y LB, «Composición de las particiones».
- **McNemar:** RT, `mcnemar` (6/12, p = 0.238; 1/7, p = 0.070; 4/50, p = 3.8·10⁻¹¹; 5/8, p = 0.581; 2/4, p = 0.688). El 5-NN cuantizado de 88.04 está en RT.
- **Separabilidad:** RT, `separabilidad`. El AUROC va de 0.9709 a 0.9915; con el umbral del 100 % pasan de 9 a 23, y con el del 95 %, de 2 a 4.
- **Análisis posterior:** AP.
  - `compuerta_vs_vocabulario`: 101, 0, 0 y 2963.
  - `aceptacion_eam_vs_voto`.
  - `ood_aceptadas`.
  - `mcnemar_cotas` (res171: [0, 10, 0.00195] y [2, 0, 0.5]).
  - `voto_ponderado_por_frecuencia|rel`.
  - Los empates 34/49, 6/10 y 10/12, con su sorteo, salen de LB, «Análisis posterior», punto 2.
- **`pear`:** la calculé yo en esta sesión desde `filas_texto.json`, con el campo `esperado` y las 50 consultas de `pear` en `cal400`. Es posterior (aviso 4).
- **Imagen:** RI, `tabla`, con `acierto`, `falsos` y `mcnemar_vs_sistema`. El p más alto es 4.9·10⁻⁵ (1-NN euclidiano, variante 0). Las 23 rechazadas y los dos falsos están en LB, «Imagen».
- **Criterio:** LB, «Qué apoyaría o debilitaría cada lectura», punto «Imagen».

---

## R2. Calibración con un conjunto de evaluación fijo

**Dónde:** es una inserción después de `05:140` (`(Sección~\ref{sec:disc-b1}).`) y antes de `05:142`, el separador de `\subsection{Protocolo completo}`. No tiene «Viejo».

**Nuevo:**
```latex

% ---------------------------------------------------------------
\subsection{Calibración con un conjunto de evaluación fijo}
\label{sec:calibracion-fija}

En la calibración, la fase madura se evalúa sobre las mismas $N$ consultas que formaron
el directorio, y esas consultas cambian con $N$.
Para separar la formación del directorio de la composición de lo que se evalúa, se fijó
un conjunto de evaluación de 15 consultas por clase (120), sorteadas dentro de cada
clase, que nunca registran en el directorio.
El directorio se forma con $N \in \{50, 100, 200, 291\}$ de las 291 consultas
restantes, sorteadas de nuevo en cada una de cinco semillas; con $N = 291$ entran todas y
solo cambia el orden.
Se compararon cuatro condiciones de la Tabla~\ref{tab:calibracion}: A, B1, D y G.
En D y G la formación toma $\lfloor N/8 \rfloor$ consultas por clase, o todas las de una
clase si no alcanzan, y queda en 48, 96, 200 y 286 consultas.
Todo se repitió con cinco sorteos del conjunto evaluado.
El diseño y los criterios de lectura se fijaron antes de correr.
La lógica de la calibración no cambia: con ella y $N = 400$ se reproducen la temprana
del 90.0\,\% y las maduras de 85.2 y 93.0\,\% de la Tabla~\ref{tab:calibracion}.
La fase temprana no usa el directorio; sobre el conjunto evaluado acierta el 92.5\,\% en
el sorteo principal y el 89.7\,\% en promedio de los cinco.
Con la formación sorteada, la fracción de consultas de formación que traen el nombre de
su clase queda entre el 46 y el 55\,\% para todo $N$.
La Tabla~\ref{tab:calibracion-fija} da los resultados.

\begin{table}[H]
    \centering
    \caption{Calibración con un conjunto de evaluación fijo de 120 consultas que no
    forman el directorio. $N$: consultas de formación. Sorteo principal: media de cinco
    semillas, con el intervalo t de Student del 95\,\% entre semillas para la madura y el
    intervalo del 95\,\% por remuestreo de las 120 consultas para la diferencia con la
    temprana, que acierta el 92.5\,\%. Cinco sorteos: media de las 25 corridas y, entre
    paréntesis, la menor y la mayor de las medias por sorteo; la temprana promedia
    89.7\,\%. Con $N = 291$, A y B1 usan todas las consultas de formación y no varían
    entre semillas. Fuente: \texttt{results/calibracion\_evaluacion\_fija/}.}
    \label{tab:calibracion-fija}
    \small
    \setlength{\tabcolsep}{4pt}
    \begin{tabular}{lrcccc}
        \toprule
        & & \multicolumn{2}{c}{Sorteo principal} & \multicolumn{2}{c}{Cinco sorteos} \\
        \cmidrule(lr){3-4} \cmidrule(lr){5-6}
        Condición & $N$ & Madura (\%) & Madura $-$ temprana & Madura (\%) & Madura $-$ temprana \\
        \midrule
        A  &  50 & 77.8 [74.1, 81.5] & $-14.7$ [$-20.0$, $-9.2$]  & 74.4 & $-15.3$ ($-19.8$ a $-11.8$) \\
        A  & 100 & 85.0 [81.3, 88.7] & $-7.5$ [$-12.7$, $-2.0$]   & 80.8 & $-8.8$ ($-12.8$ a $-4.8$) \\
        A  & 200 & 86.2 [83.6, 88.8] & $-6.3$ [$-11.3$, $-1.3$]   & 82.9 & $-6.8$ ($-9.8$ a $-2.5$) \\
        A  & 291 & 84.2              & $-8.3$ [$-15.0$, $-1.7$]   & 82.2 & $-7.5$ ($-10.8$ a $-1.7$) \\
        \midrule
        B1 &  50 & 81.5 [77.6, 85.4] & $-11.0$ [$-16.0$, $-5.7$]  & 78.9 & $-10.7$ ($-12.8$ a $-7.5$) \\
        B1 & 100 & 89.8 [86.6, 93.1] & $-2.7$ [$-6.8$, $+1.7$]    & 86.0 & $-3.7$ ($-7.5$ a $+1.0$) \\
        B1 & 200 & 91.7 [90.6, 92.7] & $-0.8$ [$-5.2$, $+3.3$]    & 89.8 & $+0.2$ ($-2.3$ a $+5.5$) \\
        B1 & 291 & 91.7              & $-0.8$ [$-5.8$, $+4.2$]    & 91.0 & $+1.3$ ($-0.8$ a $+6.7$) \\
        \midrule
        D  &  48 & 77.8 [65.8, 89.9] & $-14.7$ [$-19.8$, $-9.3$]  & 72.9 & $-16.8$ ($-20.3$ a $-13.7$) \\
        D  &  96 & 82.3 [76.3, 88.3] & $-10.2$ [$-15.3$, $-5.2$]  & 78.8 & $-10.9$ ($-12.2$ a $-9.3$) \\
        D  & 200 & 82.8 [78.2, 87.5] & $-9.7$ [$-14.7$, $-4.5$]   & 81.8 & $-7.9$ ($-10.0$ a $-3.5$) \\
        D  & 286 & 83.8 [83.3, 84.4] & $-8.7$ [$-14.8$, $-2.3$]   & 82.7 & $-7.0$ ($-10.2$ a $-0.8$) \\
        \midrule
        G  &  48 & 81.8 [75.1, 88.6] & $-10.7$ [$-15.5$, $-5.7$]  & 79.7 & $-9.9$ ($-11.3$ a $-7.2$) \\
        G  &  96 & 88.0 [82.9, 93.1] & $-4.5$ [$-9.2$, $+0.3$]    & 86.1 & $-3.6$ ($-5.7$ a $+0.5$) \\
        G  & 200 & 91.0 [89.3, 92.7] & $-1.5$ [$-5.3$, $+2.5$]    & 89.9 & $+0.3$ ($-1.5$ a $+4.2$) \\
        G  & 286 & 91.8 [90.7, 93.0] & $-0.7$ [$-5.2$, $+3.8$]    & 91.3 & $+1.7$ ($-0.7$ a $+6.3$) \\
        \bottomrule
    \end{tabular}
\end{table}

\paragraph{La formación mejora la madura en consultas que no vio, hasta alcanzar a la
temprana.}
Con la lectura B1 y el conjunto evaluado fijo, la precisión madura sube del 78.9 al
91.0\,\% entre 50 y 291 consultas de formación, en promedio de los cinco sorteos.
Ese crecimiento no puede venir de la composición, porque las consultas evaluadas son las
mismas para todo $N$.
Pero la madura solo alcanza a la temprana: la diferencia pasa de $-10.7$ puntos con 50
consultas a $+0.2$ con 200 y $+1.3$ con 291.
En el sorteo principal es de $-0.8$ con 200 y con 291, con intervalos de unos $\pm 5$
puntos, y con 291 va de $-0.8$ a $+6.7$ según el sorteo: es positiva en tres de los
cinco ($+0.8$, $+0.8$ y $+6.7$) y de $-0.8$ en los otros dos.
La ventaja de la madura sobre la temprana en la calibración, medida sobre las consultas
que formaron el directorio (93.0 frente a 90.0\,\% con $N = 400$ y 88.0 frente a
82.5\,\% con $N = 200$, Sección~\ref{sec:calibracion}), no se reproduce con un conjunto
fijo.
Lo que sí se reproduce es la decisión: con 200 y 291 consultas de formación, la fase
madura con B1 coincide con la temprana en el 92.5\,\% de las consultas evaluadas del
sorteo principal, sin consultar a los ocho módulos.

\paragraph{D y G no tienen ventaja propia.}
Con las mismas consultas de formación disponibles, balancear la formación no mejora la
lectura: D queda por debajo de A salvo con la formación más grande (82.7 frente a
82.2\,\%), y G igual que B1 (91.3 frente a 91.0\,\%).
En la calibración, D y G se sortean del banco completo, donde cerca de la mitad de las
consultas trae el nombre de su clase, frente al 10 a 15\,\% de las primeras 50 a 200 que
evalúan las otras condiciones, y su fase temprana ya es más alta (91.2 frente a
78.0\,\% con $N = 50$).

\paragraph{La lectura B1 sí se sostiene.}
B1 supera a la lectura cruda con todos los $N$ y en todos los sorteos: por 4.5, 5.2, 7.0
y 8.8 puntos en promedio con 50, 100, 200 y 291 consultas de formación, y por 2.8 como
mínimo en un sorteo.
Sin ella, la madura nunca alcanza a la temprana: con la formación más grande queda 7.5
puntos por debajo (de $-10.8$ a $-1.7$ según el sorteo).
```

**De dónde sale cada cifra.** «CF» es `results/calibracion_evaluacion_fija/README.md` y «RJ» su `resumen.json`.

- **Diseño y control:** CF, «Diseño» y «Control» (90.0, 85.25 y 93.0, que en la tesis son 85.2 y 93.0). La temprana de 92.5 y 89.7 sale de RJ, `temprana_E`, y de la nota de CF. El 46–55 % está en CF, «Composición». Los N reales de D y G (48, 96, 200 y 286) están en RJ, `N_real`.
- **Sorteo principal:** RJ, `por_semilla_E["0"]`, campos `madura_E.media`, `ic95_t`, `dif_madura_menos_temprana.media` y `dif_bootstrap_E_ic95`.
- **Cinco sorteos:**
  - La media de las 25 corridas la recalculé de RJ como media de las cinco medias por sorteo, y coincide con la tabla «Los 5 sorteos de E juntos» de CF.
  - La menor y la mayor de las diferencias por sorteo también las calculé de RJ. Las de B1 y G coinciden con CF; las de A y D no están en CF.
- **Tres de cinco con N = 291:** RJ, `B1_N291` por sorteo (−0.83, +0.83, +6.67, +0.83 y −0.83).
- **Concordancia de 92.5:** RJ, sorteo 0, `B1_N200` y `B1_N291`, `fidelidad_E`.
- **Dentro de muestra:** 93.0 y 90.0 vienen de `tab:calibracion`; 88.0 y 82.5, de `results/reanalisis_jurado/salida.md`, tabla M2.1 (B1, N = 200).
- **D y G en la calibración:** `salida.md`, tablas M2.4 (10.0, 15.0 y 15.0 %), M2.5 (de 50.0 a 51.7 %) y M2.1 (temprana de D y G 91.25 frente a 78.0 con N = 50).
- **B1 − A:** lo calculé de RJ (4.53, 5.17, 6.97 y 8.83; el mínimo por sorteo es 2.83, sorteo 4 con N = 50). CF da solo el rango de 4.5 a 8.8. El −7.5 y su rango (−10.8 a −1.7) salen de RJ, `A_N291`.
- La tabla tiene 6 columnas con intervalos. Si se sale del margen, se cambia `\small` por `\footnotesize`.

---

## R3. Codificador sin pérdida de clase

**Dónde:** es una inserción después de R5 (que va tras `05:453`) y antes de `05:455`, el separador de `\subsection{Línea base: una sola EHAM...}`. No tiene «Viejo».

**Nuevo:**
```latex

% ---------------------------------------------------------------
\subsection{Codificador sin pérdida de clase}
\label{sec:codificador-sin-clase}

El codificador del sistema se entrena con la reconstrucción y una entropía cruzada de
clase de peso 0.1 (Sección~\ref{sec:percepcion}).
La cabeza clasificadora no participa en ninguna decisión, pero la pérdida moldea el
espacio latente sobre el que operan las memorias.
Para medir cuánto depende de ella el hemisferio visual, se entrenó otro codificador con
la misma receta (arquitectura, 50 épocas, semilla 42 y selección del punto de control) y
peso 0 en la entropía cruzada; su cabeza se entrena sobre el latente sin modificar el
codificador, como una sonda.
Su RMSE es de 0.082, frente a 0.110 en el del sistema, y una sonda lineal acierta la
clase desde su latente en el 94.2\,\% de los casos, frente al 99.7\,\% de la cabeza del
sistema.
La escala del latente, el umbral de energía (con la misma regla, $\tau = 13.79$), las
memorias de contenido, los directorios visuales, las fases de texto y el
experimento~16 se regeneraron con el código del sistema, sin ajustes.
Antes de correr se fijó que la pérdida de clase sostiene el índice visual si el
enrutamiento de prueba queda en el 88\,\% o menos (el punto medio entre el sistema y el
experimento~19), si los falsos llegan a 20 de 656 o si la cobertura de punta a punta con
objetos nuevos baja al 80\,\% o menos.
La Tabla~\ref{tab:codificador-sin-clase} da los resultados, junto con los del
experimento~19, que cambia el codificador entero por la ResNet18 de ImageNet sin
reentrenar, seguida de un análisis de componentes principales a 64 dimensiones ajustado
con las imágenes de entrenamiento.

\begin{table}[H]
    \centering
    \caption{Hemisferio visual con el codificador del sistema (reconstrucción y entropía
    cruzada de peso 0.1), con uno entrenado sin la pérdida de clase y con la ResNet18 de
    ImageNet sin reentrenar (experimento~19). Fase A: 1024 imágenes; prueba: 656.
    Evocación: top-3 sobre las primeras 15 imágenes de prueba de cada clase que el
    enrutamiento acepta, con una pasada de muestreo en las dos primeras columnas.
    Experimento~16: cobertura de punta a punta con intervalo del 95\,\% por remuestreo de
    los pliegues, y falsos enrutamientos sobre 3280 imágenes por banco. El diagnóstico se
    calculó después de ver el enrutamiento, sobre las imágenes de prueba que pasan el
    umbral de energía (652 y 656) y los 1600 originales del llenado. Fuente:
    \texttt{results/codificador\_sin\_clase/} y \texttt{results/experimento19/}.}
    \label{tab:codificador-sin-clase}
    \small
    \setlength{\tabcolsep}{4pt}
    \begin{tabular}{lccc}
        \toprule
        Medida & Sistema & Sin pérdida de clase & ImageNet \\
        \midrule
        Fase A: acierto al formar los directorios (\%) & 99.9 & 81.0 & 90.2 \\
        Prueba: enrutamiento correcto (\%)             & 96.2 & 70.4 & 80.5 \\
        Prueba: falsos enrutamientos (de 656)          & 2    & 169  & 83   \\
        Prueba: rechazo (\%)                           & 3.5  & 3.8  & 6.9  \\
        Evocación de dominio (\%)                      & 97.4 (113/116) & 77.0 (87/113) & 83.5 \\
        Exp.~16, objeto conocido (\%)        & 95.5 [95.1, 95.9] & 69.9 [68.0, 71.6] & 76.3 [74.7, 77.7] \\
        Exp.~16, objeto nuevo (\%)           & 89.2 [85.1, 93.2] & 59.3 [55.5, 62.9] & 60.8 [58.3, 63.1] \\
        Exp.~16, falsos con objeto conocido (\%) & 0.1 (3)   & 23.6 (773) & ---  \\
        Exp.~16, falsos con objeto nuevo (\%)    & 0.1 (2)   & 30.2 (992) & 14.4 \\
        \midrule
        \multicolumn{4}{l}{\emph{Diagnóstico}} \\
        La memoria propia contiene la imagen (\%)        & 98.6     & 98.3      & --- \\
        Alguna memoria ajena la contiene (\%)            & 0.5      & 82.9      & --- \\
        Separación por coordenada, mediana de 64         & 5.34     & 0.24      & --- \\
        Coordenadas con separación mayor que 1           & 64       & 5         & --- \\
        Niveles ocupados por clase y coordenada (de 32)  & 8.1--12.5 & 15.5--20.2 & --- \\
        \bottomrule
    \end{tabular}
\end{table}

\paragraph{Sin la pérdida de clase, el fallo visual deja de ser rechazo.}
Se cumplen los tres criterios: el enrutamiento de prueba baja del 96.2 al 70.4\,\%, los
falsos suben de 2 a 169 de 656 y la cobertura de punta a punta con objetos nuevos baja
del 89.2 al 59.3\,\%.
El rechazo de prueba casi no cambia (3.5 y 3.8\,\%); lo que crece son los falsos, del 0.3
al 25.8\,\%.
Se concentran entre animales y hacia \texttt{dog}: 34 vienen de \texttt{horse}, 31 de
\texttt{cow} y 11 de \texttt{car}, y otros 15 van de \texttt{horse} a \texttt{cow}.
El directorio ya nace sesgado: en la fase A, que acierta el 81.0\,\%, el TME registra
2880 percepciones a \texttt{dog} y 1616 a \texttt{horse}, frente a 2016--2048 por
módulo con el codificador del sistema.
La evocación cae por el enrutamiento y no por la memoria: una imagen bien enrutada evoca
su dominio en 80 de 81 casos, y una mal enrutada, en 7 de 32.
El texto no pasa por el codificador, y las fases de texto dan los mismos 16 ganadores y
la misma fidelidad (16 de 16) que con el codificador del sistema.
Quitar solo la pérdida de clase cuesta más enrutamiento que cambiar el codificador
entero por el de ImageNet (70.4 frente a 80.5\,\%, con 169 frente a 83 falsos); con
objetos nuevos, la cobertura queda casi igual (59.3 frente a 60.8\,\%), con el doble de
falsos (30.2 frente a 14.4\,\%).

\paragraph{Diagnóstico posterior: la separación por coordenada.}
Este diagnóstico se agregó después de ver el enrutamiento.
La sonda lineal muestra que, sin la pérdida de clase, la clase sigue en el latente, pero
la contención compara coordenada por coordenada.
Como medida de cuánto separa las clases cada coordenada, se tomó la varianza entre las
medias de clase sobre la varianza dentro de las clases, en los 1600 originales del
llenado.
Con el codificador del sistema, la mediana de las 64 coordenadas es 5.34 y todas pasan
de 1; sin la pérdida de clase, la mediana es 0.24 y solo 5 pasan de 1.
Cada clase ocupa casi el doble de niveles por coordenada (de 15.5 a 20.2 de 32, frente a
8.1 a 12.5).
La memoria propia contiene casi las mismas imágenes de prueba (98.3 y 98.6\,\%), pero
alguna memoria ajena contiene también el 82.9\,\% de ellas, frente al 0.5\,\%.
La compuerta de contenido deja de excluir, y el directorio, formado con el 19\,\% de las
percepciones mal asignadas, enruta mal.

\paragraph{Lo que no separa.}
Los dos codificadores parten de los pesos de ImageNet, que se entrenaron con etiquetas de
ImageNet, y los dos vieron los diez objetos de cada clase, así que la comparación con
objetos nuevos tiene la misma fuga en las dos columnas (Sección~\ref{sec:objetos-nuevos}).
Hay un solo codificador por condición, con una semilla, sin varianza entre
entrenamientos.
```

**De dónde sale cada cifra.** «CSC» es `results/codificador_sin_clase/README.md`, «CMP» es `comparacion.md` en esa carpeta y «E19» es `results/experimento19/README.md`.

- **Receta, RMSE, sonda y τ:** CSC, «Diseño», y la tabla de resultados (τ 13.79).
- **Criterios y punto medio:** CSC, «Qué apoyaría cada lectura».
- **Columnas del sistema y sin clase:** CMP, todas las filas (falsos de exp16 en % con su conteo). El rechazo en ImageNet (6.9 %) y la fase A (90.2 %) salen de E19, tabla «El índice pierde».
- **Exp19:** E19, tabla «El índice pierde» (80.5, 83, 90.2, 83.5, 76.3, 60.8 y 14.4) y punto 2 de «Dos encoders probados» (PCA a 64, solo con entrenamiento).
- **Falsos por par:** CMP, «Falsos de test, sin clase».
- **Registros a dog y horse (2880 y 1616), evocación (80/81 y 7/32), texto (16/16):** CSC, «Resultados».
- **Diagnóstico:** CSC, tabla «Diagnóstico», comprobada contra `diag_envolventes_{oficial,sinclase}.json`: `propia_acepta` 0.986 y 0.983, `alguna_ajena_acepta` 0.0046 y 0.829, con `n_test_con_energia` 652 y 656.
- **El 19 %:** 100 − 81.0, de CSC.
- **Límites:** CSC, «Qué no separa este experimento» y «Límites».
- La pasada de evocación con semilla 0 es la de CSC, «Cambios durante la corrida», punto 1. La de la etapa 7 sin semilla dio 84/113, y no la pongo.

---

## R4. Exp11 corregido: `tab:eham-unica` y su texto

R4 reemplaza las propuestas M1.1, M1.2 (con las filas de M1.3) y M5.1 de marcadores (aviso 1). Pasan a las cifras corregidas las que dependen solo del enrutamiento: clase sobre el total, «responde», enrutamiento, destinos visuales y fuera de dominio. Van con `[PENDIENTE: exp11 d\_nn]` las que dependen del recuerdo: clase sobre las respondidas, distancia, dominio ajeno y el 79–84 %. La EHAM única y el oráculo no usan el directorio y no cambian.

### R4.1 Método
- **Dónde:** `05:471`
- **Viejo:**
```latex
Se corrieron 10 semillas con 25, 50, 100 y 200 imágenes por clase.
```
- **Nuevo:**
```latex
Se corrieron 10 semillas con 25, 50, 100 y 200 imágenes por clase; en cada semilla y
corte, el protocolo forma sus directorios de texto y de imagen desde cero.
```
- **Fuente:** `experimento11_protocolo_corregido/README.md`, «Corrección» y «Solo ruteo» (directorios nuevos en cada semilla y corte).

### R4.2 Fuentes de la tabla
- **Dónde:** `05:477-478`
- **Viejo:**
```latex
La Tabla~\ref{tab:eham-unica} resume los resultados; las tablas completas, con sus
intervalos, están en \texttt{results/experimento11/}.
```
- **Nuevo:**
```latex
La Tabla~\ref{tab:eham-unica} resume los resultados; las tablas completas, con sus
intervalos, están en \texttt{results/experimento11/} y, para el enrutamiento del
protocolo, en \texttt{results/experimento11\_protocolo\_corregido/ruteo/}.
```

### R4.3 La tabla
- **Dónde:** `05:480-520`
- **Viejo:**
```latex
\begin{table}[H]
    \centering
    \caption{Una sola EHAM contra los especialistas, por número de imágenes de llenado
    por clase (media de 10 semillas). Texto: 171 consultas reservadas; clase correcta
    según el juez 1-NN, distancia a la instancia real más cercana y, en el protocolo,
    enrutamiento a la clase de la consulta. Imagen $\to$ texto: 80 imágenes de prueba;
    fracción respondida y fracción respondida con el dominio de otra clase. Fuera de
    dominio: consultas aceptadas de 40; entre paréntesis, con la doble compuerta de
    contenido.}
    \label{tab:eham-unica}
    \small
    \begin{tabular}{llcccc}
        \toprule
        & & \multicolumn{4}{c}{Imágenes por clase} \\
        \cmidrule(lr){3-6}
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
                                   & Oráculo    & 18.2 & 20.4 & 23.3 & 26.8 \\
        \midrule
        Imagen $\to$ texto:        & EHAM única & 78.7 & 95.0 & 98.8 & 100  \\
        responde (\%)              & Oráculo    & 43.8 & 75.0 & 92.5 & 97.5 \\
                                   & Protocolo  & 41.2 & 67.5 & 78.7 & 81.2 \\
        \midrule
        Imagen $\to$ texto:        & EHAM única & 5.5  & 7.5  & 10.5 & 10.9 \\
        dominio ajeno (\%)         & Oráculo    & 0.1  & 1.9  & 2.6  & 4.1  \\
                                   & Protocolo  & 0.2  & 1.8  & 2.2  & 3.0  \\
        \midrule
        Fuera de dominio           & EHAM única & 2     & 2     & 5     & 8     \\
        aceptadas (de 40)          & Protocolo  & 4 (2) & 4 (2) & 4 (2) & 4 (2) \\
                                   & Oráculo    & 2     & 2     & 2     & 2     \\
        \bottomrule
    \end{tabular}
\end{table}
```
- **Nuevo:**
```latex
\begin{table}[H]
    \centering
    \caption{Una sola EHAM contra los especialistas, por número de imágenes de llenado
    por clase (media de 10 semillas). Texto: 171 consultas reservadas; clase correcta
    según el juez 1-NN, sobre las consultas respondidas y sobre el total (la falta de
    respuesta cuenta como fallo); distancia a la instancia real más cercana y, en el
    protocolo, respuesta y enrutamiento a la clase de la consulta. Imagen $\to$ texto: 80
    imágenes de prueba; fracción respondida y fracción respondida con el dominio de otra
    clase. Fuera de dominio: consultas aceptadas de 40; entre paréntesis, con la doble
    compuerta de contenido. [P]: [PENDIENTE: exp11 d\_nn].}
    \label{tab:eham-unica}
    \small
    \begin{tabular}{llcccc}
        \toprule
        & & \multicolumn{4}{c}{Imágenes por clase} \\
        \cmidrule(lr){3-6}
        Medida & Brazo & 25 & 50 & 100 & 200 \\
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
        Enrutamiento correcto (\%) & Protocolo  & 93.2 & 96.8 & 96.8 & 96.8 \\
        \midrule
        Distancia a la instancia   & EHAM única & 22.9 & 26.6 & 29.4 & 32.5 \\
        real más cercana           & Protocolo  & [P]  & [P]  & [P]  & [P]  \\
                                   & Oráculo    & 18.2 & 20.4 & 23.3 & 26.8 \\
        \midrule
        Imagen $\to$ texto:        & EHAM única & 78.7 & 95.0 & 98.8 & 100  \\
        responde (\%)              & Oráculo    & 43.8 & 75.0 & 92.5 & 97.5 \\
                                   & Protocolo  & 41.2 & 67.5 & 78.7 & 81.2 \\
        \midrule
        Imagen $\to$ texto:        & EHAM única & 5.5  & 7.5  & 10.5 & 10.9 \\
        dominio ajeno (\%)         & Oráculo    & 0.1  & 1.9  & 2.6  & 4.1  \\
                                   & Protocolo  & [P]  & [P]  & [P]  & [P]  \\
        \midrule
        Fuera de dominio           & EHAM única & 2     & 2     & 5     & 8     \\
        aceptadas (de 40)          & Protocolo  & 4 (2) & 4 (2) & 4 (2) & 4 (2) \\
                                   & Oráculo    & 2     & 2     & 2     & 2     \\
        \bottomrule
    \end{tabular}
\end{table}
```
- **Fuente:**
  - `ruteo.md`, tabla «Texto»: protocolo corregido, ruteo ok y clase sobre el total 93.2 / 96.8 / 96.8 / 96.8; responde 98.4 / 98.7 / 98.7 / 98.7; EHAM única 97.6 / 97.5 / 97.6 / 96.9.
  - El oráculo en texto, al 100 % en «responde» y en clase: `salida.md`, tabla M1.1.
  - `ruteo.md`, «Imagen»: el protocolo responde 41.2 / 67.5 / 78.7 / 81.2, igual que antes (los 3200 destinos son idénticos).
  - `ruteo.md`, «Fuera de dominio»: 10 % y 5 %, o sea 4 (2); EHAM única 5 / 5 / 12.5 / 20 %, o sea 2 / 2 / 5 / 8.
  - La clase «respondidas» de la EHAM es igual a su total, porque responde el 100 % (`ruteo.md`).

### R4.4 Acierto de clase
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
reservadas y la EHAM única las responde todas, así que el acierto de clase se da sobre
las consultas respondidas y sobre el total, donde la falta de respuesta cuenta como
fallo.
Sobre el total, la EHAM única acierta el 97.6, 97.5, 97.6 y 96.9\,\% con 25, 50, 100 y
200 imágenes por clase, y el protocolo, el 93.2, 96.8, 96.8 y 96.8\,\%, igual que su
enrutamiento correcto.
Desde 50 imágenes por clase los dos empatan: la diferencia es de $-0.7$ puntos con 50 y
con 100 ($[-3.3, +2.0]$ y $[-3.4, +1.9]$, intervalos del 95\,\% por remuestreo de
consultas) y de $-0.1$ con 200 ($[-2.9, +2.9]$).
Con 25, la EHAM única acierta 4.4 puntos más ($[-8.1, -0.9]$).
McNemar exacto sobre los pares de semilla, consulta y sorteo da $p = 0.86$ con 200
imágenes por clase y $p < 0.05$ con 25, 50 y 100, pero trata como independientes las
treinta repeticiones de cada consulta y es optimista.
Sobre las respondidas, el acierto del protocolo es [PENDIENTE: exp11 d\_nn].
Lo que cuesta elegir el módulo con el directorio en lugar de con la clase real, la
distancia del protocolo al oráculo sobre el total, es de 6.8 puntos con 25 imágenes por
clase y de 3.2 desde 50.
```
- **Fuente:**
  - `ruteo.md`, «Texto», y «Protocolo contra EHAM única»: P − M = −4.44 [−8.09, −0.92], −0.66 [−3.29, +1.97], −0.74 [−3.39, +1.95] y −0.08 [−2.88, +2.88]; p = 6·10⁻²⁷, 0.039, 0.020 y 0.862.
  - Lo cotejé con `ruteo/resumen.json`, `pruebas`.
  - Las treinta repeticiones son 10 semillas × 3 sorteos.
  - Distancia al oráculo: 100 − 93.2 y 100 − 96.8.

### R4.5 Fidelidad del recuerdo
- **Dónde:** `05:532-540`
- **Viejo:**
```latex
\paragraph{Fidelidad del recuerdo.}
La respuesta de la EHAM única queda más lejos de la instancia real más cercana en los
cuatro cortes, pero su brecha con el oráculo no crece con el contenido: 4.6, 6.2, 6.1 y
5.7 (calculada antes de redondear).
Cuando la primera pista reconocida es una etiqueta compartida entre clases
(\emph{fruit}, \emph{animal}, \emph{red}; el 3.5\,\% de las respuestas), la EHAM única
acierta la clase entre el 48 y el 52\,\%, y ninguna clase por sí sola sostiene más del
74--77\,\% de las coordenadas de su patrón; el protocolo acierta entre el 79 y el
84\,\%, y el oráculo el 100\,\%.
```
- **Nuevo:**
```latex
\paragraph{Fidelidad del recuerdo.}
La respuesta de la EHAM única queda más lejos de la instancia real más cercana que la
del oráculo en los cuatro cortes, y esa brecha no crece con el contenido: 4.6, 6.2, 6.1 y
5.7 (calculada antes de redondear).
La distancia del protocolo es [PENDIENTE: exp11 d\_nn].
Cuando la primera pista reconocida es una etiqueta compartida entre clases
(\emph{fruit}, \emph{animal}, \emph{red}; el 3.5\,\% de las respuestas), la EHAM única
acierta la clase entre el 48 y el 52\,\%, y ninguna clase por sí sola sostiene más del
74--77\,\% de las coordenadas de su patrón; el oráculo acierta el 100\,\%, y el
protocolo, [PENDIENTE: exp11 d\_nn].
```
- **Fuente:** las cifras de la EHAM y del oráculo no usan el directorio (`experimento11_protocolo_corregido/README.md`, «Lectura del código»). Lo que pongo pendiente lo está porque `ruteo.md` no recalcula d_nn ni el subconjunto con pista compartida («Qué no cubre»).

### R4.6 Imagen → texto
- **Dónde:** `05:542-546`
- **Viejo:**
```latex
\paragraph{Imagen $\to$ texto.}
La EHAM única responde más imágenes y se equivoca más de dominio: con 200 imágenes por
clase responde a todas, pero el 10.9\,\% con un dominio ajeno, frente al 4.1\,\% del
especialista elegido por el oráculo y el 3.0\,\% del protocolo, que en este experimento
forma su directorio visual sin variantes.
```
- **Nuevo:**
```latex
\paragraph{Imagen $\to$ texto.}
La EHAM única responde más imágenes y se equivoca más de dominio: con 200 imágenes por
clase responde a todas, pero el 10.9\,\% con un dominio ajeno, frente al 4.1\,\% del
especialista elegido por el oráculo y el [PENDIENTE: exp11 d\_nn] del protocolo.
El protocolo, que en este experimento forma su directorio visual sin variantes, responde
el 81.2\,\% de las imágenes con 200 por clase y enruta a su clase todas las que acepta.
```
- **Fuente:** `ruteo.md`, «Imagen»: acepta 81.2 y responde 81.2, y el ruteo ok es del 100 % en los cuatro cortes.

### R4.7 Fuera de dominio
Es el Nuevo de marcadores M5.1, sin cambios.
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
  - `salida.md`, tabla M5.1, fila N = 200: 8, 2, 6 solo EHAM, 0 solo protocolo, p = 0.031, y sin compuerta p = 0.219.
  - Las otras filas de M5.1 dan p = 0.25 y 1.
  - `ruteo.md`, «Fuera de dominio», muestra que las 1600 filas del corregido son iguales a las viejas.

---

## R5. Objetos nuevos con el codificador por pliegue

**Dónde:** es una inserción después de `05:453` (`perros, una taza, un coche y una vaca) concentran el 57\,\% de los fallos.`), al final de `sec:objetos-nuevos`. No tiene «Viejo». Si apruebas M4.1 de metodología, su marcador `[PENDIENTE: exp16 con codificador por pliegue]` (en `05:439-443`) puede remitir a este párrafo.

**Nuevo:**
```latex

\paragraph{Con un codificador que no vio el objeto reservado.}
El codificador es el mismo en todos los pliegues y se entrenó con vistas de los diez
objetos de cada clase, así que el objeto reservado es nuevo para las memorias pero no
para el codificador.
En los pliegues 1 a 3 de 10 se reentrenó el codificador sin ninguna imagen de los
objetos reservados del pliegue, con la receta del sistema, y se recalcularon con la
misma regla la escala del latente y el umbral de energía; la lógica del experimento~16
no cambia.
Los tres codificadores cumplen los criterios del sistema, con un RMSE de 0.105 a 0.112 y
una cabeza auxiliar del 99.5 al 99.7\,\%.
La Tabla~\ref{tab:objetos-nuevos-pliegue} los compara con el codificador del sistema en
los mismos pliegues [PENDIENTE: pliegues 10/10].
La cobertura de punta a punta con objetos conocidos baja en los tres pliegues, 2.0 puntos
en promedio.
Con objetos nuevos queda en el 89.3\,\%, frente al 87.5\,\%: baja en los pliegues 1 y 2 y
sube en el 3, donde la cobertura de \texttt{apple3} pasa del 0 al 100\,\%.
Lo que cambia son los falsos: con objetos nuevos pasan de 1 a 33 de 984 (3.4\,\%), todos
entre animales, y 22 son de un solo objeto, \texttt{horse2}, cuya cobertura baja del 80
al 27\,\%.
La cabeza clasificadora del codificador de ese pliegue, que el sistema no usa, asigna 23
de sus 41 vistas a \texttt{cow}, 15 a \texttt{horse} y 3 a \texttt{dog}; el enrutamiento
manda 17 a \texttt{cow}, 12 a \texttt{horse} y 5 a \texttt{dog}, y rechaza 7.
Con los criterios del experimento~16, la razón entre las coberturas con objetos nuevos
y conocidos (0.96) basta para sostener la generalización, pero los falsos pasan del
2\,\% que se fijó antes de correr como señal de que la fuga infla la cifra, sin llegar al
5\,\% (6.7\,\% en el pliegue 2), y la dejan en la zona intermedia
[PENDIENTE: pliegues 10/10].
Reentrenar en cada pliegue también cambia el número de imágenes de entrenamiento, el
equipo (GPU en lugar de CPU) y la escala del latente, y no se separó cuánto cuesta eso
por sí solo.

\begin{table}[H]
    \centering
    \caption{Experimento~16 en los pliegues 1 a 3 de 10, con el codificador del sistema y
    con uno reentrenado sin los objetos reservados de cada pliegue
    [PENDIENTE: pliegues 10/10]. Cobertura de punta a punta (\%) sobre las 328 vistas de
    cada banco, y falsos enrutamientos con objetos nuevos, de 328 por pliegue. $\tau$:
    umbral de energía del codificador del pliegue (16.61 en el del sistema). Fuente:
    \texttt{results/objetos\_nuevos\_codificador\_por\_pliegue\_parcial/}.}
    \label{tab:objetos-nuevos-pliegue}
    \small
    \setlength{\tabcolsep}{4pt}
    \begin{tabular}{lccccccc}
        \toprule
        & & \multicolumn{2}{c}{Objeto conocido} & \multicolumn{2}{c}{Objeto nuevo}
          & \multicolumn{2}{c}{Falsos, objeto nuevo} \\
        \cmidrule(lr){3-4} \cmidrule(lr){5-6} \cmidrule(lr){7-8}
        Pliegue & $\tau$ & Sistema & Por pliegue & Sistema & Por pliegue & Sistema & Por pliegue \\
        \midrule
        1 & 17.05 & 95.7 & 94.2 & 94.2 & 89.6 & 0 & 5  \\
        2 & 10.10 & 94.5 & 91.8 & 89.0 & 87.2 & 0 & 22 \\
        3 & 15.48 & 96.0 & 94.2 & 79.3 & 91.2 & 1 & 6  \\
        \midrule
        Media o suma & & 95.4 & 93.4 & 87.5 & 89.3 & 1 & 33 \\
        \bottomrule
    \end{tabular}
\end{table}
```

**De dónde sale cada cifra.** Todo está en `results/objetos_nuevos_codificador_por_pliegue_parcial/`.

- **Tabla y τ:** `por_pliegue.csv` (`e2e_*`, `falsos_*` y `tau`), con las medias de `tablas.md` («Contra exp16 oficial»: 95.4, 93.4, 87.5, 89.3, 1 y 33 de 984).
- **RMSE y cabeza:** `por_pliegue.csv` (0.1054–0.1118 y 99.49–99.66).
- **−2.0:** `tablas.md`, «diferencia (pliegue − oficial)» de objeto conocido.
- **apple3 (0 → 100) y horse2 (80 → 27, 22 falsos):** `tablas.md`, «Por objeto reservado», y `por_objeto.csv`.
- **horse2 23/15/3 y 17/12/5/7:** `destinos_objeto_nuevo.json`, llave `2|horse2`.
- **Todos entre animales:** `tablas.md`, «Falsos ruteos».
- **Razón 0.96:** `tablas.md`.
- **Criterios (2 % y 5 %, razón ≥ 0.75):** README de la carpeta, «Qué apoyaría cada lectura».
- **6.7 %:** 22/328, en `resumen.json` (`falso_ruteo`, máximo 0.067).
- **Receta y GPU:** README, «Diseño».
- El control opcional lo doy por no corrido (aviso 5).

---

## R6. Ubicación y cambios a 04

### Orden en 05

| Bloque | Dónde | Por qué ahí |
|---|---|---|
| R2 `sec:calibracion-fija` | inserción después de `05:140` | Corrige la lectura de la calibración que la precede. |
| R5 párrafo y `tab:objetos-nuevos-pliegue` | inserción después de `05:453` | Es parte de la misma medida de objetos nuevos. |
| R3 `sec:codificador-sin-clase` | después de R5, antes de `05:455` | Usa la fase A, la fase B y el experimento 16, que se presentan justo antes. |
| R4 | reemplazos en `05:471`, `05:477-478`, `05:480-520`, `05:522-530`, `05:532-540`, `05:542-546` y `05:548-551` | La sección no se mueve. |
| R1 `sec:lineas-base` | inserción después de `05:551`, antes de `05:553` | Es la segunda línea base. Usa las 171 reservadas y el protocolo de `sec:eham-unica`, y queda en el mismo orden que la subsección `sec:disc-lineas-base` de 06 (E5 del encuadre, después de `06:203`). |

### U1. Lista de organización
- **Dónde:** `04:268-275`. No se cruza con M2.8 de metodología, que toca `04:266-267`. La sustitución de claridad de «nativos» por «propios» en `04:268` se aplica aparte.
- **Viejo:**
```latex
Le siguen cuatro estudios de caracterización (protocolo completo, parámetros nativos
$\iota \times \kappa$, formación del directorio y capacidad de llenado,
Secciones~\ref{sec:proto-completo} a~\ref{sec:capacidad}), el hemisferio visual
(Sección~\ref{sec:hemisferio-visual}), la generalización a objetos nuevos
(Sección~\ref{sec:objetos-nuevos}), la comparación con una sola EHAM
(Sección~\ref{sec:eham-unica}), la verificación de una sola memoria de contenido por
módulo (Sección~\ref{sec:una-memoria}) y el costo computacional de la reproducción
completa (Sección~\ref{sec:costo}).
```
- **Nuevo:**
```latex
Le siguen la misma calibración con un conjunto de evaluación fijo, que no forma el
directorio (Sección~\ref{sec:calibracion-fija}), y cuatro estudios de caracterización
(protocolo completo, parámetros nativos $\iota \times \kappa$, formación del directorio y
capacidad de llenado, Secciones~\ref{sec:proto-completo} a~\ref{sec:capacidad}).
Después vienen el hemisferio visual (Sección~\ref{sec:hemisferio-visual}), la
generalización a objetos nuevos (Sección~\ref{sec:objetos-nuevos}), el hemisferio visual
con un codificador entrenado sin la pérdida de clase
(Sección~\ref{sec:codificador-sin-clase}), la comparación con una sola EHAM
(Sección~\ref{sec:eham-unica}), la comparación con decisores sin memoria asociativa sobre
los mismos vectores (Sección~\ref{sec:lineas-base}), la verificación de una sola memoria
de contenido por módulo (Sección~\ref{sec:una-memoria}) y el costo computacional de la
reproducción completa (Sección~\ref{sec:costo}).
```

### U2. Directorio compartido
- **Dónde:** `04:276-278`
- **Viejo:**
```latex
En la calibración, el protocolo completo, el barrido $\iota \times \kappa$ y la
formación del directorio, cada transacción de texto se registra en un solo
\emph{directorio compartido}, igual al registro completo del TME.
```
- **Nuevo:**
```latex
En las dos calibraciones, el protocolo completo, el barrido $\iota \times \kappa$ y la
formación del directorio, cada transacción de texto se registra en un solo
\emph{directorio compartido}, igual al registro completo del TME.
```
- **Fuente:** la calibración fija usa la lógica de `run_ablation.py` sin cambios (`calibracion_evaluacion_fija/README.md`), y en esa lógica cada transacción se registra en los ocho directorios (`salida.md`, nota de la tabla M2.2). Estructura 2.1 y 5.3 citan `04:276-281` y no cambian estas líneas.

### U3. Nota al pie de los experimentos (solo si citas el 19)
- **Dónde:** `04:160`
- **Viejo:**
```latex
(umbral de energía), 15 (árbitro por contenido) y 16 (objetos nuevos).},
```
- **Nuevo:**
```latex
(umbral de energía), 15 (árbitro por contenido), 16 (objetos nuevos) y 19 (codificador
de ImageNet sin reentrenar).},
```

### Ajustes a otras propuestas (opcionales, para que citen la sección nueva)
- **Marcadores M2.2:** su segunda nota al pie («Calibración con un conjunto de evaluación fijo, \texttt{results/...}») puede pasar a «(Sección~\ref{sec:calibracion-fija})».
- **Marcadores M2.7 y Estructura 4.4:** dan las cifras de la evaluación fija con «(Sección~\ref{sec:calibracion})». Con R2 aprobado, la referencia correcta es `sec:calibracion-fija`.

## Marcadores que deja esta propuesta

| Marcador | Dónde | Cuántos |
|---|---|---|
| `[PENDIENTE: exp11 d\_nn]` | R4.3 (pie, define «[P]»), R4.4, R4.5 (dos), R4.6 | 5 |
| `[PENDIENTE: pliegues 10/10]` | R5 (párrafo, dos; pie de tabla, uno) | 3 |

En LaTeX, el guion bajo de `d_nn` tiene que ir escapado (`d\_nn`) dentro del marcador.