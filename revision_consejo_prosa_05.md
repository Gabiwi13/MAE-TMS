# Propuesta viejo/nuevo: 05 Resultados (consejo de redacción)

**Estado:** pendiente de aprobación. Nada aplicado.

Lo que más pesa: (1) 05 gana una subsección «Generalización a objetos nuevos» con el 89.2 % que hoy solo vive en la limitación (e), aunque lo citan el resumen y las conclusiones; (2) «Línea base: una sola EHAM» pasa de tres párrafos con unas 40 cifras a una tabla y cuatro párrafos con título, con cada cifra cotejada contra `results/experimento11/` (la tabla agrega la fila de enrutamiento 97.0 % que cita la corrección de hechos E1); (3) seis secciones reciben la definición que les falta (las nueve condiciones, ι y κ, «containment inverso» y las columnas de la tabla de capacidad, el control de la formación, «cobertura de punta a punta», hetero y homo). No propongo la figura de formación del directorio: los archivos de `results/exp4_directory_formation/` no resuelven la duda del control crudo (ver P1.5). Dos textos de `revision_consejo_hechos.md` necesitan un ajuste (E15 y E5; ver «Avisos»).

Convenciones. Las líneas son las del `.tex8` actual. **[R]** = texto que resulta de aplicar el replanteamiento aprobado; **[H-En]** = texto que resulta de aplicar la corrección de hechos En. Los textos nuevos de las partes 1 y 2 conservan los términos de hoy (label, containment, ruteo, test); si apruebas la decisión T, la tabla de la parte 3 se aplica después, también sobre ellos. Quité las negritas de cifras en todos los párrafos que reescribo (ver P2.8). No toco 05:341–379 ni «Costo computacional».

---

## Parte 1. Reglas y estructura

### P1.1 Nueva subsección «Generalización a objetos nuevos» (va entre 05:392 y 05:394)

**Dónde:** después de la figura `fig:imagen-etiquetas` (05:392) y antes de `% ----` / «Línea base» (05:394–395).
**Viejo:** no existe; el resultado está en `06:295–307` (limitación (e)).
**Nuevo:**
```latex
% ---------------------------------------------------------------
\subsection{Generalización a objetos nuevos}
\label{sec:objetos-nuevos}

La partición principal separa imágenes, no objetos: los diez objetos de cada clase
aportan vistas al llenado y a la prueba (Sección~\ref{sec:dataset}), así que las cifras
anteriores miden vistas nuevas de objetos conocidos.
La generalización a objetos nuevos se midió aparte (experimento 16), con una validación
\textit{leave-one-object-out} de diez pliegues: en cada pliegue, el contenido y la fase A
se construyen con nueve objetos por clase, y sobre los mismos modelos se evalúan las 41
vistas del objeto reservado de cada clase y 41 vistas no usadas de los objetos que sí
contribuyeron.
La cobertura de punta a punta es del 89.2\,\% [85.1, 93.2] con objetos nuevos y del
95.5\,\% [95.1, 95.9] con objetos conocidos; la brecha es de 6.3 puntos [2.5, 10.4]
(intervalos de 95\,\% por remuestreo de los pliegues).
El enrutamiento correcto sobre las imágenes aceptadas es del 99.9\,\% en los dos bancos,
y los falsos enrutamientos con objetos nuevos son 2 de 3280 (un \texttt{cow} y un
\texttt{horse}, enviados a \texttt{dog}): la envolvente por coordenada cubre a un objeto
que no contribuyó a ella, y cuando no lo cubre lo rechaza.
La brecha no se reparte entre clases sino que se concentra en objetos concretos: 71 de
los 80 objetos reservados superan el 70\,\%, y nueve (dos manzanas, dos peras, dos
perros, una taza, un coche y una vaca) concentran el 57\,\% de los fallos.
```
**Por qué:** una cifra del resumen y de las conclusiones no puede vivir solo en una limitación; la discusión interpreta, no presenta (claridad 06–07, A2). Va después del hemisferio visual porque usa «cobertura de punta a punta», que P1.4 define. **Fuente:** `results/experimento16/README.md` (e2e 95.5 [95.1, 95.9] y 89.2 [85.1, 93.2]; brecha 6.3 [2.5, 10.4]; ruteo ok 99.9 en ambos; cow→dog 1, horse→dog 1; «bootstrap del 95 % sobre pliegues»; 41 vistas por clase, 328 por banco). 71 de 80, nueve objetos y 57 % (202 de 355 fallos) los verificó el revisor de cifras de 06 sobre `results/experimento16/raw/` (`cifras_06.md`); `veredicto.md` de exp16 está desactualizado («74 de 80»), no corregir hacia él. Cifra nueva en la tesis: [95.1, 95.9]. Lo que cambia fuera de 05 va en «Avisos».

### P1.2 «Línea base: una sola EHAM»: tabla y cuatro párrafos (05:398–440)

**Viejo:** 05:398–440, desde «Para medir qué aporta la partición en especialistas, se construyó una» hasta «50. Tablas completas en \texttt{results/experimento11/}.» Ya incluye E12 («se solapan») y E13 (`compat`), que aquí van aplicadas.
**Nuevo:**
```latex
Esta sección mide qué aporta repartir el contenido entre ocho especialistas frente a
guardarlo todo en una sola memoria.
Se construyó una EHAM única con los mismos pares etiqueta--latente que reciben los ocho
especialistas (25\,600 con 200 imágenes por clase y 16 variantes) y se evaluó con las
mismas operaciones de reconocimiento con compuerta y de recuerdo desde la etiqueta
(\texttt{recognize\_gated}, \texttt{recall\_from\_left}), sin ruteo.
Se compararon tres brazos: la \emph{EHAM única}; los especialistas con el módulo elegido
por la verdad de terreno (\emph{oráculo}, un techo), y el \emph{protocolo} transactivo
completo, que elige el módulo con el directorio.
Las consultas de texto son las 171 del banco que no se usaron para formar los
directorios (las otras 240 los forman); las de imagen, las primeras 10 imágenes de
prueba de cada clase.
Se corrieron 10 semillas con 25, 50, 100 y 200 imágenes por clase.
Cada recuerdo se juzga por la clase de la instancia real más cercana (juez 1-NN) y por
la distancia a ella.
Con 200 imágenes por clase, cuatro de los ocho especialistas reconstruidos son idénticos
bit a bit a las memorias del sistema; los otros cuatro difieren porque el experimento
recalcula los latentes en GPU, y el redondeo puede mover un registro al nivel vecino.
La Tabla~\ref{tab:eham-unica} resume los resultados; las tablas completas, con sus
intervalos, están en \texttt{results/experimento11/}.

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

\paragraph{Acierto de clase.}
Con 25 imágenes por clase la EHAM única acierta la clase algo más que el protocolo
(97.6\,\% frente a 96.9\,\%), con intervalos de 95\,\% que se solapan ($[97.4, 97.8]$ y
$[96.3, 97.6]$).
Desde 50 el orden se invierte y los intervalos se separan (con 200, $[97.9, 98.6]$ para
el protocolo y $[96.7, 97.1]$ para la EHAM única).
Lo que cuesta elegir el módulo con el directorio en lugar de con la verdad de terreno, la
distancia del protocolo al oráculo, es de 3.1 puntos con 25 imágenes por clase y de 1.2
a 1.7 desde 50.

\paragraph{Fidelidad del recuerdo.}
La respuesta de la EHAM única queda más lejos de la instancia real más cercana en los
cuatro cortes, pero su brecha con el oráculo no crece con el contenido: 4.6, 6.2, 6.1 y
5.7 (calculada antes de redondear).
Cuando la primera pista reconocida es una etiqueta compartida entre clases
(\emph{fruit}, \emph{animal}, \emph{red}; el 3.5\,\% de las respuestas), la EHAM única
acierta la clase entre el 48 y el 52\,\%, y ninguna clase por sí sola sostiene más del
74--77\,\% de las coordenadas de su patrón; el protocolo acierta entre el 79 y el
84\,\%, y el oráculo el 100\,\%.

\paragraph{Imagen $\to$ texto.}
La EHAM única responde más imágenes y se equivoca más de dominio: con 200 imágenes por
clase responde a todas, pero el 10.9\,\% con un dominio ajeno, frente al 4.1\,\% del
especialista elegido por el oráculo y el 3.0\,\% del protocolo, que en este experimento
forma su directorio visual sin variantes.

\paragraph{Fuera de dominio.}
La EHAM única acepta más consultas fuera de dominio a medida que crece el contenido; el
oráculo acepta 2 de 40 en todos los cortes, y el protocolo 4, que la doble compuerta de
contenido (el módulo destino debe contener la pista) baja a 2.
```
**Por qué:** es la subsección más difícil del capítulo: cifras por corte en prosa que no se pueden comparar, jerga sin presentar («brazos», «juez», «reservadas», «bit a bit los modelos oficiales») y remisión a un archivo externo en lugar de una tabla (claridad M23, antipatrones). Junté la tabla de claridad (con oráculo en imagen → texto) y la de antipatrones (con «dominio ajeno» y el protocolo en todos los cortes). También arregla la concordancia de 05:436–437 («el protocolo 4, que bajan a 2»).
**Fuente:** `results/experimento11/README.md`, bloques N = 25, 50, 100, 200 (cotejadas una por una). `d_nn` con más decimales en `resumen.json` (`d_nn_truth`): 22.860, 26.565, 29.404, 32.528 (EHAM única); 18.970, 20.675, 23.778, 26.976 (protocolo); 18.219, 20.380, **23.346**, 26.781 (oráculo). Dos correcciones a los revisores: el oráculo con 100 es **23.3**, no 23.4 (el README muestra 23.35, redondeo doble); e imagen → texto es sobre **80** imágenes, no 656 (`run_experiment11_monolithic.py:65`, `N_IMG_TEST = 10`, y `run_experiment9_member_loss.py:217`, primeras `per_class` de `test`; todos los porcentajes son múltiplos de 1.25). «Las otras 240»: formación T-protocolo, 233 registradas + 7 rechazadas. **Cifras nuevas en la tesis** (solo en la tabla): enrutamiento 95.3/97.4/97.4/97.0; distancias con 25, 50 y 100; protocolo responde 41.2/67.5/78.7; dominio ajeno con 25, 50 y 100. Si no las quieres, la tabla se reduce a la columna de 200 más la fila de clase correcta.

### P1.3 «Una memoria de contenido por módulo»: arquitecturas comparadas y términos definidos

**a) Apertura (05:445–453).**
**Viejo:**
```latex
Las versiones anteriores del sistema guardaban, junto a la memoria heteroasociativa de
cada módulo, dos memorias homoasociativas llenadas aparte, una por dominio, como fuente
de pesos.
Con el llenado imagen--etiqueta, la homo latente recibía los mismos registros que el
lado latente de la hetero, y su relación es idéntica, celda por celda en los ocho
módulos, a la lectura $\mathbf{R}^{R}$ de la ecuación~\eqref{eq:marginal}.
La homo de etiquetas registraba cada palabra una vez por su frecuencia y no una vez por
imagen: tiene el mismo soporte que $\mathbf{R}^{L}$, con conteos multiplicados por un
factor de 21 a 95 que varía entre celdas.
```
**Nuevo:**
```latex
Cada módulo guarda su contenido en una sola memoria heteroasociativa (en adelante, la
hetero), y las lecturas homoasociativas que usa se calculan de ella
(ecuación~\eqref{eq:marginal}).
Esta sección la compara con la arquitectura que guarda, junto a la hetero de cada
módulo, dos memorias homoasociativas llenadas aparte (las homo), una por dominio, como
fuente de pesos.
Con el llenado imagen--etiqueta, la homo latente recibe los mismos registros que el lado
latente de la hetero, y su relación es idéntica, celda por celda en los ocho módulos, a
la lectura $\mathbf{R}^{R}$.
La homo de etiquetas registra cada palabra una vez por su frecuencia y no una vez por
imagen: tiene el mismo soporte que $\mathbf{R}^{L}$, con conteos multiplicados por un
factor de 21 a 95 que varía entre celdas.
```
**Por qué:** el cambio a una sola hetero es la excepción permitida, pero «las versiones anteriores… guardaban» es la voz que la regla 3 prohíbe; contado como dos arquitecturas comparadas dice lo mismo. Presenta «hetero» y «homo», que hoy se usan sin presentar (claridad A4, cifras B7, consistencia 8.9 y 1.11).

**b) Definir «nombra» y «familiar» antes de usarlas (05:469–470).**
**Viejo:** «valor indefinido.» / «Sin lesión, las dos responden lo mismo consulta por consulta (2252 consultas): de las»
**Nuevo:** «valor indefinido. Por cada imagen se leen dos cosas: si el módulo la \emph{nombra} (la proyección imagen$\to$texto no deja columnas vacías) y si le es \emph{familiar} (la homo o la lectura latente la contienen).» / «Con las memorias intactas, las dos responden lo mismo consulta por consulta (2252 consultas): de las»
**Por qué:** hoy «nombra» y «reconocidas sin nombre» aparecen antes de su definición (que está en el pie de la tabla) y «lesión» un párrafo antes de presentarla (claridad M24). Las definiciones son las del pie de `tab:lesion`.

**c) La cuarta condición y los 17 valores (05:485–486 y 05:489).**
**Viejo:** «Mover el conteo de las celdas dañadas al borde, en lugar de borrarlo, conserva la familiaridad exacta en todo el rango.» / «suma las de los 17 valores de etiqueta.»
**Nuevo:** «Una cuarta condición, que no está en la tabla, pasa el conteo de cada celda dañada al borde en lugar de borrarlo, y conserva la familiaridad de las 800 imágenes en todo el rango.» / «suma las de los 17 valores de etiqueta (los 16 niveles y el indefinido).»
**Por qué:** la frase describe una condición que la tabla no muestra; «exacta» se cambia por la cifra. **Fuente:** `results/homo_marginal/README.md`, sección E, parte 2 («A desasociar»: 800 en todo f; «17 valores de palabra»); `02_marco_teorico.tex:240` (valor indefinido).

### P1.4 «Por qué ξ = 0» → «Más variantes, más cobertura», y la fase A (05:304–312 y 05:324–334)

**a) Fase A.** **Viejo [R + H-E8]:**
```latex
Sobre las imágenes aceptadas, la precisión del módulo visual fue del \textbf{99.9\%},
con un rechazo del \textbf{0.8\%} (4.2\% con 4 variantes en el experimento 13) y una
percepción rechazada antes de la memoria por el umbral de energía. Cada percepción
aceptada registra sus 16 variantes: el registro completo del TME quedó en
$[2048, 2016, 2016, 2016, 2016, 2032, 2048, 2048]$ con entropía de \textbf{3.000 bits}
al tercer decimal, el máximo con ocho módulos.
```
**Nuevo:**
```latex
Sobre las percepciones aceptadas, el enrutamiento visual acertó el 99.9\%, con un
rechazo del 0.8\% y una percepción rechazada antes de la memoria por el umbral de
energía.
Cada percepción aceptada registra sus 16 variantes; el registro completo del TME quedó
en $[2048, 2016, 2016, 2016, 2016, 2032, 2048, 2048]$, con entropía de 3.000 bits al
tercer decimal, el máximo con ocho módulos.
```
**Por qué:** no hay un «módulo visual»: el 99.9 % es el acierto del enrutamiento de la fase A (consistencia 1.9; `UNA_HETERO.md`, «Etapa 7, fase A: routing 99.9 %»). El 4.2 % de otro experimento, citado por número en la primera frase, pasa a (b), donde se entiende. La cadena de dos puntos se parte (claridad M18, antipatrones).

**b) Párrafo del experimento 13.** **Viejo [H-E9]:** «\paragraph{Por qué $\xi = 0$.}» y el párrafo 05:325–334 con el texto de E9 («El experimento 13 lo mide sobre las 656 imágenes de test: … rutea mal dos de las 656 imágenes (Sección~\ref{sec:limitaciones}).»).
**Nuevo:**
```latex
\paragraph{Más variantes, más cobertura.}
El directorio visual no tolera huecos ($\xi = 0$; la razón está en la
Sección~\ref{sec:operaciones}): con $\xi = 2$, el ruteo del dominio propio baja a medida
que el módulo presencia más dominios ajenos (experimento 10).
La palanca para la cobertura es densificar el llenado, no tolerar huecos.
El experimento 13 lo mide sobre las 656 imágenes de test: registrar en el directorio 16
variantes por percepción, en lugar de una, lleva su aceptación del 73.6 al 96.2\,\% (con
4 variantes, 87.7\,\%); con 16 variantes también en el contenido, la \emph{cobertura de
punta a punta} (imágenes enrutadas a su clase cuyo destino además responde) pasa de 66.5
a 94.5\,\%, y el rechazo de la fase A baja del 4.2 al 0.8\,\%.
En ese experimento, con una o 4 variantes en el directorio no hay ruteos falsos y con 16
hay uno; el sistema, con sus 16 variantes, rutea mal dos de las 656 imágenes
(Sección~\ref{sec:limitaciones}).
```
**Por qué:** la justificación de ξ = 0 ya está en `03:484–489`; aquí basta remitir. «Cobertura de punta a punta» se usa aquí por primera vez y hoy solo se define en `06:240` (claridad M20). **Fuente:** `results/experimento13/README.md` («e2e: rutea a la clase correcta y el destino responde»; fase A: Vc4 43 de 1024 = 4.2 %, Vc16 8 de 1024 = 0.8 %; el 4.2 → 0.8 depende de las variantes del **contenido**, no del directorio, como advierte `cifras_05.md`, duda 4). Conservo «(experimento 10)», aunque su README solo dice «verificado» sin cifra (claridad propone quitarlo; ver Descartado).

### P1.5 Formación del directorio: qué es el control y cuánto cambia la velocidad (05:225–246)

**a) Apertura.** **Viejo (05:225–229):**
```latex
Para estudiar cómo el orden de las interacciones afecta la formación del directorio, se
evaluó la precisión madura completa en un \textit{snapshot} tras cada interacción $k$,
usando cuatro condiciones de presentación (intercalado, barajado con 5 semillas,
bloqueado por dominio, y control con puntuación cruda) sobre el subconjunto de 80
consultas.
```
**Nuevo:**
```latex
Se midió cuántas interacciones necesita el directorio para volverse utilizable y si
importa su orden: tras cada interacción $t$ de la fase temprana se evaluó la precisión
madura (lectura B1) sobre las 80 consultas, con el directorio tal como estaba en ese
momento, en cuatro condiciones: orden intercalado entre dominios, barajado (5 semillas),
bloqueado por dominio (todas las consultas de una clase y luego las de la siguiente) y
un control en orden intercalado que elige al ganador temprano con la puntuación cruda,
sin compuerta ni normalización.
```
**Por qué:** «control con puntuación cruda» se lee como la lectura cruda del directorio (72.5 % en 05:134), y no lo es: el control cambia la puntuación de la fase **temprana**; la madura se lee siempre con B1. «Snapshot» y «bloqueado» sin definir (claridad M15, léxico). $t$ en lugar de $k$, que en 03 es el índice de módulo (consistencia 4.2). **Fuente:** `run_experiment4.py:21–24` (condiciones; «C … todas las de una clase, luego la siguiente»; «D crudo (sin gate, sin norm) · orden original»), `:83–93` (`raw_score`), `:123–139` (`eval_mature` con `predict_normalized`).

**b) «Hallazgo principal».** **Viejo [R]:** «\paragraph{Hallazgo principal: con ocho módulos, 10 consultas por clase no bastan.} \textbf{Ninguna condición alcanza el umbral del 90\%} con este volumen de interacciones: todas convergen al 81.2\% final. No es un fallo de convergencia sino de evidencia disponible: con 8 dominios y consultas que comparten léxico, 10 interacciones por dominio no acumulan suficiente evidencia distintiva (el mismo protocolo con el banco completo alcanza 93.0\%, Sección~\ref{sec:calibracion}).»
**Nuevo:**
```latex
\paragraph{Con 10 consultas por clase, ninguna condición llega al 90\%.}
Todas convergen al 81.2\% final.
Con ocho dominios y consultas que comparten léxico, 10 interacciones por dominio no
acumulan suficiente evidencia distintiva; el mismo protocolo con el banco completo
alcanza el 93.0\% (Sección~\ref{sec:calibracion}).
```
**Por qué:** «Hallazgo principal:» en el título, «No es X sino Y» y negrita (antipatrones, claridad B1); «8 dominios» frente a «ocho» (forma). En la propuesta de replanteamiento.

**c) «El orden afecta la velocidad».** **Viejo [R]:** «Todas las condiciones convergen exactamente al mismo estado final: conteos $[46, 16, 40, 25, 30, 18, 21, 31]$ y entropía 2.914 bits, independientemente del orden de presentación. Esta invariancia del destino muestra que el directorio acumula evidencia conmutativa: el orden solo determina cuándo se vuelve utilizable, no qué se aprende.»
**Nuevo:**
```latex
Las cuatro condiciones terminan en el mismo estado: los conteos y la entropía de la
Sección~\ref{sec:proto-completo} (2.914 bits).
El orden sí cambia la velocidad: la precisión madura llega al 70\% tras 13 interacciones
en orden intercalado, tras 28 a 42 en orden barajado (según la semilla) y tras 59 en
orden bloqueado; al 75\%, tras 18, 40 a 51 y 71.
Esta invariancia del destino muestra que el directorio acumula evidencia conmutativa:
el orden solo determina cuándo se vuelve utilizable, no qué se aprende.
```
**Por qué:** tras el replanteamiento (que quita «k ≈ 13») el título habla de velocidad y el párrafo no da ninguna cifra de velocidad; el vector de conteos aparece por tercera vez (claridad M9). **Fuente:** `results/exp4_directory_formation/results_formation.csv`, primer $k$ con `mature_acc` ≥ 0.70 / ≥ 0.75: A 13/18; B 35, 30, 42, 28, 36 / 51, 45, 51, 46, 40; C 59/71; todas 0.8125 en $k$ = 80. **Cifras nuevas en la tesis**, dentro de muestra como toda la curva (lo declara E1).

**La figura de formación no se propone.** Los archivos de `results/exp4_directory_formation/` no resuelven la duda: su `report.md` llama a D «crudo (control sesgo)» y la curva D coincide con la A en las 80 filas del CSV (lo comprobé fila por fila). Solo el script aclara que D cambia la puntuación temprana y no la lectura madura, de modo que no contradice el 72.5 %. Aun así, la leyenda de la figura («D · routing crudo (sesgo)», «5 seeds») haría leer lo contrario: habría que regenerarla antes de ponerla. Por eso doy los cruces solo en texto.

### P1.6 Calibración: qué son las nueve condiciones (05:17–22)

**Viejo:**
```latex
El estudio principal evalúa nueve condiciones de lectura del directorio transactivo
sobre el banco de 411 consultas, con $N \in \{50, 100, 200, 400\}$ consultas de
formación y 5 semillas por celda.
La Tabla~\ref{tab:calibracion} muestra los resultados en $N = 400$ (promedio de 5
semillas); la Figura~\ref{fig:mature-vs-n} muestra la curva completa de la fase madura
y la Figura~\ref{fig:heatmap-condicion} el mapa completo condición $\times$ $N$.
```
**Nuevo** (le sigue el párrafo «dentro de muestra» que agrega E1):
```latex
La calibración mide cómo debe leerse el directorio para que el enrutamiento maduro sea
confiable.
Se compararon nueve condiciones: la lectura cruda (A), dos normalizaciones por el conteo
de registros de cada módulo (B1, B2) y seis que actúan sobre otra cosa: un tope de
registros por módulo (C), consultas balanceadas (D), la cuantización (E32, E64), el
vocabulario (F) y la combinación de D, B1 y F (G).
Cada una se evaluó sobre el banco de 411 consultas, con $N \in \{50, 100, 200, 400\}$
consultas para formar el directorio y 5 semillas por celda.
La Tabla~\ref{tab:calibracion} da los resultados en $N = 400$; la
Figura~\ref{fig:mature-vs-n} muestra cómo crece la precisión madura con $N$, y la
Figura~\ref{fig:heatmap-condicion} da los mismos valores como mapa de calor.
```
**Por qué:** la sección no dice qué pregunta responde ni qué son las condiciones; «condiciones de lectura» engloba cosas que no son lecturas (claridad M2). No tomé la clasificación del revisor («cuatro cambian la lectura: A, B1, B2, C»): C es un tope al registro (`ablation_report.md`, P4, `max_ratio=3.0`).

### P1.7 Parámetros nativos: definir ι y κ y explicar la tabla (05:167–172 y 05:176–177)

**Viejo (05:167–172):** «Se realizó un barrido de cuadrícula con $\iota \in \{0, 0.25, 0.5, 1.0\}$ y $\kappa$ en $\{0\}$ más los cuantiles 10, 25, 50, 75, 90 y 100\,\% de la razón que compara la compuerta (activación media por celda de la proyección entre la media de la memoria), medida con $\iota = 0$ sobre los 260 pares token-módulo contenidos del subconjunto de 80 consultas: $\kappa \in \{0, 1.755, 1.801, 1.844, 1.937, 2.056, 2.107\}$. Los resultados se muestran en la Tabla~\ref{tab:grid-iota-kappa}.»
**Nuevo:**
```latex
Los dos parámetros propios de la EAM (Sección~\ref{sec:eam}) son la poda $\iota$, que
apaga durante la recuperación las celdas de peso menor que $\iota$ veces el peso medio
de las celdas no nulas, y el umbral relativo $\kappa$, que exige a la activación media
por celda de la proyección llegar a $\kappa$ veces la media de la memoria.
La pregunta es si alguno mejora la fase temprana o hace innecesaria la normalización B1.
Se barrió una cuadrícula con $\iota \in \{0, 0.25, 0.5, 1.0\}$ y siete valores de
$\kappa$: 0 y los cuantiles 10, 25, 50, 75, 90 y 100\,\% de esa razón, medida con
$\iota = 0$ sobre los 260 pares (token, módulo) del subconjunto de 80 consultas en que el
módulo contiene al token, lo que da
$\kappa \in \{0, 1.755, 1.801, 1.844, 1.937, 2.056, 2.107\}$.
La Tabla~\ref{tab:grid-iota-kappa} muestra la precisión temprana y el rechazo.
```
**Pie, viejo (05:176–177):** «Precisión temprana y, entre paréntesis, tasa de rechazo (\%) en función de $\iota$ y $\kappa$.}»
**Pie, nuevo:** «Precisión temprana y, entre paréntesis, tasa de rechazo (\%) en función de $\iota$ y $\kappa$ (80 consultas). Con $\iota \geq 0.25$ el valor no cambia con $\kappa$: la poda sube la razón que $\kappa$ compara por encima del mayor $\kappa$ del barrido.}»
**Por qué:** ι y κ se definieron 50 páginas antes; «260 pares token-módulo contenidos» es jerga; el lector ve «igual en todas las columnas» y la razón llega dos párrafos después (claridad M12, M13; forma, guion de «token-módulo»). Definiciones de `02_marco_teorico.tex:78–90`; mínimos de la razón con poda en `results/exp2_iota_kappa/report.md` (2.330, 2.785, 3.960 > 2.107).

### P1.8 Capacidad: «containment inverso» y las columnas de la tabla (05:252–255 y 05:259–263)

**Viejo (05:252–255):** «Se varió el número de imágenes registradas por clase $N \in \{25, 50, 100, 200, 328\}$ utilizando llenado imagen-por-imagen (\textit{imagen-etiqueta}). La aceptación se determinó por containment inverso con $\xi = 0$. Los \textit{falsos} son imágenes de otras clases presentadas al módulo.»
**Nuevo:**
```latex
Se varió el número de imágenes registradas por clase,
$N \in \{25, 50, 100, 200, 328\}$, con el llenado imagen por imagen
(\textit{imagen--etiqueta}).
Una imagen se acepta si la memoria del módulo la contiene desde el lado de la imagen
(containment inverso, con $\xi = 0$); los \textit{falsos} se miden con imágenes de otras
clases presentadas al módulo.
La Tabla~\ref{tab:capacidad} resume las métricas.
```
**Pie, viejo [H-E6]:** «Métricas de capacidad en función del número de imágenes registradas $N$ por clase. ``Enrutamiento'' es la precisión temprana sobre 80 consultas (reconocimiento por el contenido llenado con $N$ imágenes, sin directorio); ``Variedad $L_1$'' es la distancia media $L_1$ entre recuperaciones distintas; $H$ es la entropía de la memoria de contenido.}»
**Pie, nuevo:** «Métricas de capacidad en función del número de imágenes registradas $N$ por clase. ``Train propio'' y ``Test propio'': fracción de imágenes de la propia clase, de llenado y de prueba, que el módulo acepta; ``Falsos'': fracción de imágenes de otras clases que acepta. ``Enrutamiento'' es la precisión temprana sobre 80 consultas (reconocimiento por el contenido llenado con $N$ imágenes, sin directorio); ``Variedad $L_1$'' es la distancia media $L_1$ entre recuperaciones de una misma pista; $H$ es la entropía de la memoria de contenido.}»
**Por qué:** «containment inverso» no aparece antes en la tesis; tres columnas no se definen; la tabla no se cita en el texto (claridad M16, consistencia 6.1; forma, «imagen-por-imagen» y guion simple). **Fuente:** `run_experiment6.py:109–114` (`reverse_accept`: proyección desde el latente, ξ = 0), `:216–234` (`own_train` sobre las $N$ registradas, `own_test` sobre la prueba, `cross_false` con otras clases), `:237–252` (L1 entre pares de recuerdos de una misma pista por clase).

### P1.9 Protocolo completo: la diferencia 81.2 / 93.0 se avisa al principio (05:123–145)

**Viejo (05:123–124):** «El protocolo completo (fase temprana $\to$ formación del directorio $\to$ fase madura con el TME apagado) se corrió sobre el subconjunto de 80 consultas (10 por clase).»
**Nuevo:** la misma frase, más: «Mide lo mismo que la calibración con el protocolo del sistema, pero el directorio se forma con 10 consultas por dominio en lugar de unas 50; por eso su precisión madura es menor que la del banco completo (Sección~\ref{sec:formacion}).»

**Viejo (05:126–145):** «\paragraph{Fase temprana.}» … hasta «…la diferencia mide el efecto del volumen de interacciones, no un cambio de mecanismo.»
**Nuevo:**
```latex
\paragraph{Fase temprana.}
El sistema alcanzó una precisión temprana del 81.2\% con una tasa de rechazo del 5.0\%;
los rechazos los decide la memoria, sin filtro de vocabulario
(Sección~\ref{sec:pipeline-semantico}).

\paragraph{Fase madura.}
Con la lectura B1, la precisión madura fue del 81.2\% y la fidelidad temprana-madura del
92.5\%; con la lectura cruda, la precisión madura baja al 72.5\%.
El directorio terminó con los conteos $[46, 16, 40, 25, 30, 18, 21, 31]$ para
(\texttt{apple}, \texttt{car}, \texttt{cow}, \texttt{cup}, \texttt{dog}, \texttt{horse},
\texttt{pear}, \texttt{tomato}) y una entropía de 2.914 bits sobre un máximo de 3.000.
```
**Por qué:** el lector llega a 81.2 % después de 93.0 % y la explicación aparece al final, con «Nótese», repetida en 05:231–238 (claridad M1, M7, M9; antipatrones j10). «Sin filtro de vocabulario» repite `04:108–117`: queda una cláusula con remisión (antipatrones j6). Cinco negritas menos.

### P1.10 Apertura del capítulo (05:4–11)

**Viejo:** «Los resultados se presentan en este orden: el estudio de calibración del directorio (el estudio principal), … y la medición del costo computacional. Salvo indicación en contrario, los experimentos usan los parámetros de la Sección~\ref{sec:parametros}; todos los números provienen de corridas posteriores a la auditoría de fidelidad (Sección~\ref{sec:auditoria}).»
**Nuevo:**
```latex
Las secciones siguen el orden de la Sección~\ref{sec:organizacion}.
Salvo indicación en contrario, los experimentos usan los parámetros de la
Sección~\ref{sec:parametros}, y todos los números son trazables a corridas del sistema
actual (Sección~\ref{sec:auditoria}).
```
**Por qué:** la lista repite `04:248–257` (antipatrones) y tendría que cambiar con la subsección nueva; «posteriores a la auditoría» fecha los resultados respecto de un evento (consistencia 8.4; mismo giro que el replanteamiento 2f).

### P1.11 «Especificidad»: resto de historia en el texto aprobado (05:284–287)

**Viejo [R]:** «\paragraph{Especificidad.} Con el llenado de un latente por imagen, la tasa de falsos aceptados es del \textbf{0\% en todo el rango} de $N$ probado, con siete clases contrarias por módulo: el containment inverso mantiene la discriminación exacta también a ocho clases.»
**Nuevo:** «\paragraph{Especificidad.} Con el llenado de un latente por imagen, la tasa de falsos aceptados es del 0\% en todo el rango de $N$ probado, con siete clases contrarias por módulo.»
**Por qué:** «también a ocho clases» es la comparación con tres módulos que el replanteamiento quita en el resto; la coda repite el 0 % con un adjetivo (léxico, antipatrones). En la propuesta de replanteamiento.

### P1.12 «Agente ganador» en la figura 9

La regla 1 se rompe en la leyenda de `fig09_winner_distribution_N80.png`. No tiene texto aquí: va en la propuesta de figuras (`figuras.md`, T2), junto con los rótulos en inglés de las figuras 2, 3, 4 y 9 y el nombre `_N80`.

---

## Parte 2. Claridad y estilo

### P2.1 Calibración

**a) Cuerpo del párrafo de B1 (05:52–58).** **Viejo [R + H-E15]:** «La lectura cruda del directorio (A) pierde 7.8 puntos frente a la lectura normalizada por conteo (85.2\% frente a 93.0\%), y ninguna condición que manipula síntomas (B2, C, D, E32, E64) la alcanza; la más cercana, B2, queda a 1.2 puntos. La combinación G supera a B1 sola por medio punto (93.5\% frente a 93.0\%), dentro del ruido de cinco semillas: una vez corregida la causa (evidencia por registro en vez de evidencia total), el balanceo de consultas y la curación de vocabulario aportan poco.»
**Nuevo:**
```latex
La lectura cruda del directorio (A) pierde 7.8 puntos frente a la lectura B1 (85.2\%
frente a 93.0\%).
Ninguna de las condiciones que actúan sobre los síntomas del sesgo y no sobre su causa
(B2, C, D, E32, E64) alcanza a B1; la más cercana, B2, queda a 1.2 puntos.
La combinación G supera a B1 por medio punto (93.5\% frente a 93.0\%), menos de lo que
G varía entre semillas (de 93.0 a 93.7\%; B1 da lo mismo con todas): una vez que la
puntuación mide evidencia por registro y no evidencia total, balancear las consultas y
depurar el vocabulario aportan poco.
```
**Por qué:** «manipula síntomas» y «la causa» quedan sin decir de qué hasta el final; «dentro del ruido de cinco semillas» cuando B1 es determinista y solo D y G varían (claridad A1, cifras B4, consistencia 1.10; «cinco»/«5», forma). **Fuente:** `ablation_metrics.csv`, N = 400: G 0.9298 a 0.9373 por semilla; B1 0.93 en las cinco. Cifras nuevas: 93.0 y 93.7.

**b) Desglose por dominio (05:79–86).** **Viejo [H-E2]:** «Con la lectura B1 en $N = 400$, la precisión madura por dominio fue: \texttt{cow}, \texttt{cup} y \texttt{tomato} 100\%, \texttt{car} 98\%, \texttt{dog} 93.9\%, \texttt{apple} 88.2\%, \texttt{horse} 88\% y \texttt{pear} 76\% (Figura~\ref{fig:dominio}). … concentran 18 de los 28 errores residuales, la mitad \texttt{pear} $\to$ \texttt{apple} (9); …»
**Nuevo:** «Con la lectura B1 en $N = 400$, cinco dominios quedan por encima del 90\% (\texttt{cow}, \texttt{cup} y \texttt{tomato} 100\%, \texttt{car} 98\%, \texttt{dog} 93.9\%) y tres por debajo: \texttt{apple} 88.2\%, \texttt{horse} 88\% y \texttt{pear} 76\% (Figura~\ref{fig:dominio}). … concentran 18 de los 28 errores que deja B1, la mitad \texttt{pear} $\to$ \texttt{apple} (9); …» (lo demás igual).
**Por qué:** ocho cifras seguidas no dejan ver el patrón; «errores residuales» no se definió (claridad M5).

**c) Participación de `apple` (05:96–102).** **Viejo [H-E15 + H-E3]:** «La participación de \texttt{apple} bajo la lectura B1 es del \textbf{13.8\%} (ideal 12.5\%) y \texttt{pear} queda en 76\% (Figura~\ref{fig:winner}). La misma figura muestra que bajo la lectura cruda (A) \texttt{apple} captura el 20.5\% de las victorias: es el sesgo de lectura que B1 corrige, y con B1 el módulo que más se aleja del ideal es \texttt{pear}, a 2.25 puntos (10.25\%). El análisis de este hallazgo se desarrolla en la Sección~\ref{sec:disc-dominancia}.»
**Nuevo:**
```latex
La Figura~\ref{fig:winner} muestra qué fracción de las victorias maduras se lleva cada
módulo.
Con la lectura cruda (A), \texttt{apple} se lleva el 20.5\%: es el sesgo de lectura que
B1 corrige.
Con B1 baja al 13.8\% (ideal 12.5\%), y el módulo que más se aleja del ideal es
\texttt{pear}, a 2.25 puntos (10.25\%).
La Sección~\ref{sec:disc-dominancia} analiza el origen del sesgo.
```
**Por qué:** el orden natural es cruda → B1; «pear queda en 76 %» es precisión, no participación, y no sale de esa figura; «captura» es calco (claridad A2, léxico). El título es el de E15.

**d) Estado del directorio (05:113–117).** **Viejo:** «La entropía del directorio transactivo alcanza 2.974 bits en la condición A y 2.977 bits en G, sobre un máximo teórico de 3.000 bits ($\log_2 8$): la especialización queda balanceada al 99.1\% incluso sin corrección, porque el desequilibrio de masas es un sesgo de \emph{lectura}, no de estructura. La fidelidad temprana-madura con B1 es del 95.8\%.»
**Nuevo:** «La entropía del directorio transactivo es de 2.974 bits en la condición A y de 2.977 en G, el 99.1\% del máximo ($\log_2 8 = 3$ bits): los conteos quedan casi parejos entre los ocho módulos. El sesgo que B1 corrige está en la lectura, no en los conteos (Sección~\ref{sec:disc-b1}).»
**Por qué:** «balanceada al 99.1 %» no dice que es 2.974/3; la explicación se desarrolla en `06:51–53` y aquí basta remitir; la fidelidad repite una celda de la tabla (claridad M6, antipatrones j8).

**e) Pie de la figura 3 (05:73–74).** **Viejo:** «\caption{Mapa de calor de precisión madura por condición experimental y número de consultas $N$.}» **Nuevo:** «\caption{Precisión madura por condición y número de consultas de formación $N$. Solo B1, D y G quedan por encima del 85\% desde $N = 100$; A y F coinciden en todas las celdas.}»
**Por qué:** el pie repite el título y no dice qué mirar (claridad M4). **Fuente:** `ablation_report.md`, tabla por N (B1 87/88/93, D 86.5/89.2/87.3, G 90/93.2/93.5 desde N = 100; las demás bajan del 85 % en alguna celda; A = F).

### P2.2 Protocolo completo

**a) Réplica (05:147–151).** **Viejo:** «\paragraph{Réplica con las 16 consultas del pipeline oficial.} La réplica con las 16 \texttt{TEST\_QUERIES} (2 por dominio) enruta correctamente 15 de las 16, con al menos un acierto en cada clase y conteos $[12, 6, 6, 7, 5, 5, 4, 7]$;»
**Nuevo:** «\paragraph{Réplica con las 16 consultas de referencia.} Con las 16 consultas de referencia del sistema (\texttt{TEST\_QUERIES}, 2 por dominio), el enrutamiento acierta 15 de 16, con al menos un acierto en cada clase y conteos $[12, 6, 6, 7, 5, 5, 4, 7]$;» (sigue igual).
**Por qué:** «pipeline oficial» y un nombre de código sin presentar; `06:222` las llama «consultas de referencia» (claridad M10). Resuelve también el «pipeline» de este sitio (decisión T).

**b) Sonda de rechazo (05:154–161).** **Viejo:** «Como diagnóstico separado del benchmark, se presentaron 12 consultas \emph{representables} (todas producen vectores fastText reales) que describen objetos fuera de los ocho dominios. La memoria rechazó \textbf{10 de 12} por containment puro (puntuación cero en los ocho módulos), sin regla léxica alguna. Las 2 restantes rutean porque comparten tokens con labels legítimos de algún dominio (p.ej.\ \textit{food}): la frontera entre ``fuera de dominio'' y ``comparte conceptos con el dominio'' es semántica, no léxica, y el diagnóstico la mide en lugar de esconderla.»
**Nuevo:**
```latex
Aparte del banco, se presentaron 12 consultas \emph{representables} (todas tienen vector
fastText) que describen objetos fuera de los ocho dominios.
La memoria rechazó 10 de 12 por containment (puntuación cero en los ocho módulos).
Las 2 restantes rutean porque comparten tokens con labels legítimos de algún dominio
(p.\ ej.\ \textit{food}): la frontera entre ``fuera de dominio'' y ``comparte conceptos
con el dominio'' es semántica, no léxica.
```
**Por qué:** «en lugar de esconderla» es autoelogio; «sin regla léxica alguna» se dice por quinta vez; «benchmark», «puro», negrita (claridad M11, léxico, antipatrones; «p. ej.», forma).

### P2.3 Parámetros nativos

**a) Efecto de ι (05:195–199).** **Viejo [H-E15]:** «Con la cuantización por magnitud, una poda ligera ($\iota = 0.25$) mejora marginalmente la fase temprana (82.5\% frente a 81.2\%) al eliminar algo de ruido de baja frecuencia, y en la fase madura sube 2.6 puntos (B1: 83.8\% frente a 81.2\%); una poda mayor destruye: $\iota = 0.5$ pierde 6 puntos con un rechazo del 11\%, y $\iota = 1.0$ rechaza el 86\%.»
**Nuevo:**
```latex
Una poda ligera ($\iota = 0.25$) quita algo de ruido de baja frecuencia: la fase
temprana pasa de 81.2 a 82.5\% y la madura con B1 de 81.2 a 83.8\% (la
Tabla~\ref{tab:grid-iota-kappa} solo da la fase temprana).
Una poda mayor destruye: $\iota = 0.5$ pierde 6 puntos con un rechazo del 11\%, y
$\iota = 1.0$ rechaza el 86\%.
```
**Por qué:** «Con la cuantización por magnitud» supone otra cuantización anterior; «marginalmente» es adjetivo donde hay cifras; el 83.8 % no está en la tabla y el lector lo busca; una frase con cuatro ideas (claridad A3, léxico). Doy los valores y no la diferencia: la de E15 está mal (ver Avisos). **Fuente:** `results/exp2_iota_kappa/results_downstream.csv`.

**b) División entre la media de la memoria (05:216–219).** **Viejo [H-E5]:** «En las dos condiciones llevadas hasta la fase madura, la lectura cruda … ($\iota = 0.25$, $\kappa = 0$). La calibración alternativa por división entre la media de la memoria ($\div$\texttt{mem.mean}) \emph{empeora} la fase temprana (76.2\%) y distorsiona los conteos del directorio: con el llenado por instancias las masas de contenido ya están igualadas por construcción y esa corrección sobra.»
**Nuevo:** «En las dos condiciones nativas llevadas hasta la fase madura, la lectura cruda … ($\iota = 0.25$, $\kappa = 0$). También se probó dividir la puntuación temprana de cada módulo entre la media de su memoria de contenido ($\div$\texttt{mem.mean}): \emph{empeora} la fase temprana (76.2\%) y distorsiona los conteos del directorio, porque con el llenado por instancias las masas de contenido ya están igualadas por construcción y esa corrección sobra.»
**Por qué:** la normalización `÷mem.mean` nunca se presentó (claridad M14); «nativas» corrige el texto de E5 (ver Avisos). **Fuente:** `results_downstream.csv` (fila «÷mem.mean», `norm_upstream=True`, early 0.7625).

### P2.4 Capacidad: «zona de operación» (05:290–294)

**Viejo [H-E6 + H-E7 + H-E15]:** «La precisión temprana crece con la cobertura y se estabiliza en torno al 81\% desde $N = 200$; la entropía de la memoria de contenido crece con $N$ y se satura (3.65, 4.37, 4.95, 5.20 y 5.32 bits), coherente con la acumulación de variedad real. La \textbf{zona de operación} es $N = 200$, que además reserva \texttt{train[200:328]} para las interacciones visuales.»
**Nuevo:** «La precisión temprana crece con $N$ y se estabiliza en torno al 81\% desde $N = 200$; la entropía de la memoria de contenido crece con $N$ y se satura (3.65, 4.37, 4.95, 5.20 y 5.32 bits), coherente con la acumulación de variedad. El sistema opera con $N = 200$: ahí la precisión temprana ya se estabilizó, y quedan \texttt{train[200:328]} para las interacciones visuales (Sección~\ref{sec:dataset}).»
**Por qué:** «zona de operación» no se define; «cobertura» tiene aquí otro sentido que en 5.6; «real» de relleno (claridad A5, M17; léxico).

### P2.5 Hemisferio visual: fase B (05:318–322)

**Viejo:** «El resultado fue \textbf{631/656 = 96.2\%} de imágenes correctamente asignadas, con un rechazo del 3.5\% (23 imágenes, cuatro de ellas antes de la memoria por el umbral de energía) y \textbf{dos falsos enrutamientos} (0.3\%): sobre las imágenes aceptadas, la precisión es del \textbf{99.7\%}. Los dos falsos son dos vistas del mismo objeto (\texttt{horse7}, frontal y 035-135) enviadas a \texttt{dog}, que las contiene.»
**Nuevo:** «El resultado fue de 631 de 656 imágenes (96.2\%) asignadas correctamente, 23 rechazadas (3.5\%; cuatro de ellas antes de la memoria, por el umbral de energía) y dos falsos enrutamientos (0.3\%); sobre las aceptadas, la precisión es del 99.7\%. Los dos falsos son dos vistas del mismo objeto (\texttt{horse7}, la frontal y la \texttt{035-135} en la nomenclatura de ETH-80) enviadas a \texttt{dog}, que las contiene.»
**Por qué:** cuatro negritas y una fórmula en prosa; «035-135» sin explicar (claridad M19). La segunda frase depende de la decisión D2 de hechos (identidad de `horse7`): si la quitas, se va entera.

### P2.6 Cambios pequeños

| Dónde | Viejo | Nuevo | Por qué |
|---|---|---|---|
| 05:30–31 (pie `tab:calibracion`) | `F no tiene efecto: el vocabulario por masa asociativa no contiene los labels polisémicos que curaría (Apple~Inc.), así que $F \equiv A$.` | `F coincide con A: el vocabulario por masa asociativa no contiene los labels polisémicos (los de Apple~Inc.) que la depuración quitaría.` | notación $\equiv$ en prosa; «curaría» es calco (claridad M3, léxico) |
| 05:41 | `Cap de número máximo de registros por módulo` | `Tope de registros por módulo` | anglicismo |
| 05:45 | `Vocabulario curado ($\equiv$ A)` | `Vocabulario depurado ($\equiv$ A)` | calco de *curated* |
| 05:46 | `G (D+B1+F) & Combinación` | `G & D + B1 + F` | la descripción repetía el nombre |
| 05:279 | `\paragraph{Generalización por cobertura.}` | `\paragraph{Generalización con el volumen de llenado.}` | «cobertura» significa otra cosa en 5.6 (claridad M17) |
| 05:336 | `\paragraph{Evocación de labels: imagen $\to$ palabras.}` | `\paragraph{Evocación de dominio: imagen $\to$ palabras.}` | nombre de la métrica en `04:241` y `07:21` (consistencia 1.3) |
| 05:339 [H-E10] | `\textbf{113/116 = 97.4\%}` | `113 de 116 (97.4\%)` | negrita y fórmula en prosa |
| 05:461 [H-E14] | `el 1.3\,\% de los destinos del protocolo en la comparación con una sola EHAM` | `el 1.3\,\% de los destinos del protocolo en la comparación con una sola EHAM (Sección~\ref{sec:eham-unica})` | remisión explícita (consistencia 6.2) |
| 05:478 | `La Tabla~\ref{tab:lesion} destruye una fracción de las celdas de la hetero.` | `La Tabla~\ref{tab:lesion} muestra qué pasa al destruir al azar una fracción $f$ de las celdas de la hetero.` | la tabla no destruye nada (léxico, claridad M24) |
| 05:515–516 | `Ninguna lectura de la arquitectura con homo quedó fuera del alcance de una sola memoria por módulo.` (párrafo suelto) | pegarla al final del párrafo 05:478–489 como `Ninguna lectura de la arquitectura con homo queda fuera del alcance de una sola memoria por módulo.` | cierre suelto en pasado (antipatrones) |

### P2.7 Restos sin cambio de texto propio

`05:226` «snapshot», `05:154` «benchmark», `05:142` «Nótese», `05:292` «real», `05:161` «esconderla», `05:311` «perfectamente», `05:213` «grid»: quedan resueltos por P1.5, P2.2, P1.9, P2.4 y por E8 y E5 de hechos.

### P2.8 Negritas de cifras

Regla: ninguna cifra en negrita dentro de la prosa de 05 (la tabla conserva la del 93.0 de B1). Con P1.4, P1.5, P1.9, P1.11, P2.1c, P2.2b, P2.4, P2.5 y la fila 05:339 de P2.6 ya no queda ninguna (antipatrones e'; claridad B2 proponía conservar una por subsección; elegí la regla simple porque cada cifra principal ya está en una tabla o en el título).

---

## Parte 3. Términos (decisión T)

Se aplica en bloque si apruebas la decisión T. Incluye los sitios que vienen de textos nuevos (míos o de hechos). Fuera de esta tabla, 05 no tiene «encoder», «recall», «gated» ni «augmentación» en prosa dentro de mi alcance (05:96 lo quita E15; 05:343 y 05:351 están en 341–379; «augmentación» solo en el costo).

| Línea | Viejo | Nuevo |
|---|---|---|
| 05:22+ (párrafo de E1) | `rutea correctamente el 97.0\%` | `enruta correctamente el 97.0\%` |
| 05:30 (P2.6) | `los labels polisémicos` | `las etiquetas polisémicas` |
| 05:38 | `Score de activación sin normalizar` | `Puntuación de activación sin normalizar` |
| 05:157 (P2.2b) | `por containment (puntuación cero` | `por contención (puntuación cero` |
| 05:159 (P2.2b) | `Las 2 restantes rutean porque comparten tokens con labels legítimos` | `Las 2 restantes se enrutan porque comparten tokens con etiquetas legítimas` |
| 05:254 (P1.8) | `(containment inverso, con $\xi = 0$)` | `(contención inversa, con $\xi = 0$)` |
| 05:261 (pie, P1.8) | ` ``Train propio'' y ``Test propio'': ` | ` ``Llenado propio'' y ``Prueba propia'': ` |
| 05:268 | `Train propio (\%) & Test propio (\%)` | `Llenado propio (\%) & Prueba propia (\%)` |
| 05:280 | `la generalización a imágenes de test` | `la generalización a imágenes de prueba` |
| 05:302 | `656 imágenes de test mediante` | `656 imágenes de prueba mediante` |
| 05:314 | `Fase B: enrutamiento de imágenes de test.` | `Fase B: enrutamiento de imágenes de prueba.` |
| 05:315 | `Las 656 imágenes de test se enrutaron` | `Las 656 imágenes de prueba se enrutaron` |
| 05:327 (P1.4b) | `el ruteo del dominio propio` | `el enrutamiento del dominio propio` |
| 05:329 (P1.4b) | `sobre las 656 imágenes de test` | `sobre las 656 imágenes de prueba` |
| 05:333 (P1.4b) | `no hay ruteos falsos y con 16 hay uno; el sistema, con sus 16 variantes, rutea mal dos` | `no hay enrutamientos falsos y con 16 hay uno; el sistema, con sus 16 variantes, enruta mal dos` |
| 05:337 [H-E10] | `imágenes de test de cada clase que el ruteo acepta` | `imágenes de prueba de cada clase que el enrutamiento acepta` |
| 05:389–390 [H-E10] | `imágenes de test de cada clase que el ruteo acepta` | `imágenes de prueba de cada clase que el enrutamiento acepta` |
| 05:402 (P1.2) | `sin ruteo` | `sin enrutamiento` |
| 05:457 [H-E14] | `contención, rechazo, ruteo y evocación` / `en el ruteo de test` | `contención, rechazo, enrutamiento y evocación` / `en el enrutamiento de prueba` |

`05:147` «pipeline» lo resuelve P2.2a. `\texttt{}` (`recognize\_gated`, `recall\_from\_left`, `TEST\_QUERIES`, `train[200:328]`) no se toca.

---

## Parte 4. Forma

Todos los errores de `forma_05.md` caen en párrafos que ya reescribo; ninguno queda suelto.

| Línea | Error | Dónde queda corregido |
|---|---|---|
| 57 | «cinco semillas» frente a «5 semillas» | P2.1a (la frase ya no lleva el número) |
| 160 | «p.ej.\» | P2.2b («p.\ ej.\») |
| 170 | «token-módulo» con guion | P1.7 («pares (token, módulo)») |
| 228 | coma antes de «y» en enumeración | P1.5a |
| 235 [R] | «8 dominios» frente a «ocho» | P1.5b |
| 253 | «imagen-por-imagen», «imagen-etiqueta» | P1.8 («imagen por imagen», «imagen--etiqueta») |
| 405 | «diez semillas» frente a «5 semillas» | P1.2 («10 semillas») |
| 436–437 | «el protocolo 4, que bajan a 2» (concordancia) | P1.2 («que la doble compuerta … baja a 2») |

---

## Descartado

- Claridad M1, lista de dos aclaraciones en la apertura: la de los dos bancos ya está en `04:172–175`; el aviso 81.2/93.0 va al protocolo (P1.9), donde se lee justo antes de la cifra.
- Claridad M2, «cuatro cambian la lectura (A, B1, B2, C)»: C es un tope al registro, no una lectura (`ablation_report.md`, P4).
- Claridad M3, «Pistas cuantizadas en 32 niveles»: no verifiqué qué cuantizan E32/E64 (`ablation_report.md`, P5: «ya no prueban lo que su nombre sugiere»); queda «Cuantización en 32 niveles».
- Claridad M3, correspondencia de nombres de código en el pie de la tabla 1: las figuras se regeneran con los nombres de la tabla (`figuras.md`, T1).
- Claridad M7, versión larga («cada consulta entra por un módulo y se enruta punto a punto»): exp3 y exp4 instrumentan un directorio compartido; no lo afirmo.
- Claridad M9, figura de la curva de formación: no se resuelve con `results/exp4_directory_formation/` (P1.5).
- Claridad M20, quitar «(experimento 10)»: la afirmación tiene fuente («verificado» en su README), aunque sin cifra; la dejo y queda como duda.
- Claridad M23, «656 imágenes» en el pie y 23.4 en la tabla: son 80 imágenes y 23.3 (P1.2).
- Claridad M24, «se muestrea por separado, de su propia distribución»: paráfrasis sin ganancia; queda «se sortea de su propia columna».
- Claridad M25 y consistencia 6.3, nota al pie sobre los números de experimento: va en la primera mención, que está en 04 (Avisos).
- Claridad M21, M22, B4; léxico 05:345, 349–350, 356, 364–365; antipatrones 05:341–365 y 05:356: fuera de mi alcance (05:341–379).
- Claridad A6, M27, B3; cifras B8; consistencia 2 y 7.5: figuras PNG, en `figuras.md`.
- Antipatrones, quitar «$\kappa$ no es una defensa contra el sesgo de masa» (05:210): responde la pregunta de la sección (P1.7) y la hipótesis de exp2.
- Antipatrones, títulos «Lectura cruda contra B1», «Lectura cruda contra B1 en el grid», «Efecto del orden»: los títulos actuales dicen el hallazgo; el de 05:51 ya lo cambia E15.
- Léxico 05:51 «Ninguna otra lectura alcanza a B1» y consistencia 8.5 «B1 es la corrección irreducible»: se aplica el título de E15.
- Léxico «precio del directorio» → «costo»: la frase nueva de P1.2 dice «lo que cuesta».
- Consistencia 4.1, $N_{\mathrm{img}}$ en capacidad: la sección define $N$ en su primera línea; el cambio toca tabla, prosa y `06:127` por poca ganancia.
- Consistencia 4.5, $f$ → $\phi$ en la tabla de lesión: el pie define $f$ ahí mismo.
- Consistencia 5.2, «(en la corrida oficial, 633 de 656)» tras el 96.2 % de exp13: E9 ya atribuye la cifra al experimento 13.
- Consistencia 7.2 y forma 05:331, `\,\%` contra `\%`: se decide con la plantilla de la UACJ.
- Cifras B1, redondeo al par en la tabla 1: nadie recalcula medias de cinco semillas desde la tabla; ganancia mínima.

---

## Avisos (hechos y otros archivos)

1. **E15 de hechos, «sube 2.6 puntos»:** la diferencia es de 2.5 (0.8375 − 0.8125 en `results/exp2_iota_kappa/results_downstream.csv`; 2.6 sale de restar valores ya redondeados). P2.3a da los dos valores sin la diferencia; si E15 se aplica sin P2.3a, poner 2.5.
2. **E5 de hechos, «En las dos condiciones llevadas hasta la fase madura»:** fueron tres; la tercera (`÷mem.mean`) también queda por debajo de B1 (63.7 contra 77.5 %, mismo CSV). P2.3b dice «las dos condiciones nativas».
3. **E1 de hechos** remite el 97.0 % a `sec:eham-unica`, que hoy no lo muestra; la fila «Enrutamiento correcto» de P1.2 lo pone ahí.
4. **Para 04:** `04:27` «(experimento 16, Sección~\ref{sec:limitaciones})» → «(Sección~\ref{sec:objetos-nuevos})»; en `04:248–257` agregar «la generalización a objetos nuevos (Sección~\ref{sec:objetos-nuevos})» tras el hemisferio visual (P1.10 remite a esa lista); la nota al pie sobre los números de experimento va en su primera mención.
5. **Para 06–07:** la limitación (e) queda como interpretación y remite a `sec:objetos-nuevos` (claridad 06–07, A2). En exp11, imagen → texto es sobre 80 imágenes (10 por clase): el «2.5 % de las imágenes de prueba» de `06:202` son 2 de 80.
6. **Control de la formación:** la curva D de exp4 coincide con la A en las 80 interacciones (CSV comparado fila por fila): en este banco, la puntuación temprana cruda elige los mismos ganadores que la de compuerta. No lo afirmo en la tesis porque ningún README lo dice; si quieres la figura, hay que regenerarla con una leyenda que lo diga.
