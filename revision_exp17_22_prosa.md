# Revisión de prosa tras los experimentos 17 a 22 (18 de octubre de 2026)

**Estado:** pendiente de aprobación; nada aplicado. Cifras de `results/experimento17/` y `results/experimento22/` (esta rama), `MAE-TMS-exp18/results/experimento18` y `…/experimento19` (rama `exp18-heteroasociacion-significativa`), y `MAE-TMS-medico/results/{medico,medico_completo,medico_balanceado,experimento20,experimento21}` (rama `medico-demo`). Síntesis en `sintesis_exp17_a_exp22.md`.

**Decisión previa necesaria:** los resultados de exp18 a exp21 viven en otras ramas. Para citarlos en la prosa hay que integrarlos a esta rama (merge o copia de `results/`) o declararlos como experimentos complementarios fuera del sistema oficial. Los párrafos de abajo asumen lo segundo y remiten a su ubicación.

## A. `.tex8/secciones/04_metodologia.tex`, línea 220

**Viejo:** «\item \textbf{Evocación de dominio} (\textit{top-3 coseno}): fracción de imágenes para las que al menos una de las tres etiquetas más cercanas en el espacio fastText pertenece al vocabulario de la clase real (recuperación inversa imagen $\to$ palabras).»

**Nuevo:** «\item \textbf{Evocación de dominio} (\textit{top-3 coseno}): fracción de imágenes para las que al menos una de las tres etiquetas más cercanas en el espacio fastText pertenece al vocabulario de la clase real (recuperación inversa imagen $\to$ palabras). Mide si la palabra evocada es del dominio correcto, no si es una palabra específica de la imagen: el llenado empareja cada imagen con la siguiente etiqueta de la lista de su clase, de modo que la asociación imagen--palabra es significativa a nivel de clase y no de instancia (Sección~\ref{sec:limitaciones}, limitación (i)).»

## B. `.tex8/secciones/05_resultados.tex`, líneas 335–339

**Viejo:** «Sobre las imágenes de evaluación aceptadas, la evocación inversa (recuperación $\beta$ desde el latente, decodificada por similitud coseno top-3) produjo al menos una etiqueta del vocabulario de la clase real en \textbf{113/116 = 97.4\%} de los casos (85.3\% con el llenado de 4 variantes).»

**Nuevo:** «Sobre las imágenes de evaluación aceptadas, la evocación inversa (recuperación $\beta$ desde el latente, decodificada por similitud coseno top-3) produjo al menos una etiqueta del vocabulario de la clase real en \textbf{113/116 = 97.4\%} de los casos (85.3\% con el llenado de 4 variantes). En top-1 la etiqueta sigue siendo del dominio en el 96.0\,\%, pero el nombre de la clase es la primera palabra solo en el 48.0\,\% (con \texttt{apple} en 0 de 45 y \texttt{cup} en 3 de 45), y tres recuerdos de la misma imagen dan la misma primera palabra en el 38.9\,\% de los casos (experimento 17): la evocación devuelve una muestra de la envolvente del dominio, no una palabra.»

## C. `.tex8/secciones/06_discusion.tex`, limitaciones nuevas tras (h), línea 280

**Añadir:**

«\paragraph{(i) Evocación a nivel de clase, no de instancia.}
El llenado oficial empareja cada imagen con la siguiente etiqueta de la lista de su clase, así que ninguna palabra describe a una imagen concreta y la memoria no puede devolver una palabra específica (experimento 17). Con una palabra fija por objeto la memoria acierta el 40.8\,\% (azar 10\,\%) y solo el 51.2\,\% de las vistas que memorizó. Con palabras que sí describen la imagen (color, manchas, pelo, techo, etiquetadas a mano; experimentos 17 y 18) acierta en los objetos que vio, pero en objetos nuevos responde el valor mayoritario de su clase: el minoritario sale en el 1–6\,\% de los casos y no se rechaza. La envolvente generaliza la pertenencia y falla rechazando; dentro del dominio, el atributo lo decide la densidad y falla confundiendo hacia lo común.

\paragraph{(j) Una sola percepción para el índice y para el especialista.}
El encoder de 64 dimensiones no conserva de forma compartida entre objetos lo que varía dentro de una clase (manchas, pelo, techo; sonda de vecinos en el azar). La causa no es la pérdida de clase (un encoder reentrenado sin ella no las recupera), sino la compresión con reconstrucción (experimento 19). Con rasgos que sí las conservan (ResNet18 de ImageNet congelado más PCA), el índice se degrada: el enrutamiento visual baja de 96.2 a 80.5\,\% y los falsos suben de 2 a 83, mientras que el atributo en objetos nuevos gana unos cinco puntos sobre el azar. Además, sobre esos mismos rasgos la memoria generaliza el atributo mucho menos que un vecino más cercano (patrón de \texttt{cow}: 59 contra 91\,\% balanceado): su noción de parecido es la contención por coordenada, no la distancia (experimento 18).

\paragraph{(k) Ancho de envolvente con registro desbalanceado.}
En un demo sobre MedMNIST+ (experimentos complementarios, rama \texttt{medico-demo}), registrar todo el train hace que los dominios grandes ensanchen su envolvente hasta contener a los chicos: la de radiografía de tórax contiene el 93\,\% de las imágenes de piel, melanoma cae de 175 a 37 de 223 y el rechazo de una modalidad nunca vista baja de 29.7 a 0\,\%. B1 no lo corrige porque no es un sesgo de conteo sino de ancho. Leer el directorio con el principio de tamaño (gana la envolvente más estrecha que contiene la pista) recupera piel y melanoma sin balancear el registro (experimento 20) y coincide con B1 cuando el registro es balanceado (experimento 22: 1 decisión distinta de 656). No recupera los dominios cuya envolvente no contiene la imagen.

\paragraph{(l) El rechazo es de cobertura.}
A igual aceptación de lo propio, la memoria rechaza un órgano nunca registrado como un detector de vecinos o de Mahalanobis (96.3 contra 97.7 y 96.6\,\%), pero rechaza poco una modalidad entera nunca vista (6–24\,\%, frente al 99.8–100\,\% de la probabilidad máxima de un clasificador lineal) y el cambio de hospital (31.8 contra 75.0\,\% de kNN) (experimento 20). El rechazo está integrado en el mismo mecanismo que enruta, pero no supera a los detectores estándar.»

## D. `.tex8/secciones/06_discusion.tex`, «Qué aporta la partición», línea 152

**Añadir al final:** «La misma comparación sobre MedMNIST+ (experimento 21, rama \texttt{medico-demo}), con etiquetas fastText del término de cada dominio, repite el patrón y lo acota. Con dominios visualmente separables la memoria única iguala a los especialistas (modalidad 93.4 contra 93.5\,\% balanceado; once órganos 90.7 contra 90.8). Con catorce hallazgos de radiografía de tórax, muy superpuestos, la partición casi la duplica (24.4 contra 13.1\,\%, azar 7.1): la memoria única mezcla al recordar y converge a una sola etiqueta. La ventaja de partir no es de exactitud general; aparece cuando los contenidos se pisan, y crece con el solapamiento, como predijo el experimento 12.»

## E. `.tex8/secciones/07_conclusiones.tex`, líneas 20–21

**Viejo:** «y una evocación de dominio del \textbf{97.4\%};»

**Nuevo:** «y una evocación de dominio del \textbf{97.4\%} en top-3 (la palabra de la clase es la primera solo en el 48\,\%: la evocación devuelve el dominio, no una palabra);»

## F. `.tex8/secciones/07_conclusiones.tex`, líneas 74–80

**Viejo:** «…sin recurrir a modelos de aprendizaje profundo supervisado para la toma de decisiones; y que, cuando el escalado encuentra límites, estos viven en las representaciones que alimentan a las memorias y no en el mecanismo asociativo ni en la maquinaria transactiva.»

**Nuevo:** «…sin recurrir a modelos de aprendizaje profundo supervisado para la toma de decisiones. Sus límites están en dos lugares: en las representaciones que alimentan a las memorias, que no conservan el detalle dentro de la clase, y en el propio reconocimiento por contención, que generaliza la pertenencia pero no los atributos y cuyo ancho de envolvente decide con registro desbalanceado. Lo que el sistema sostiene es una memoria semántica de caja blanca, basada en familiaridad, que enruta por categoría y se abstiene por falta de cobertura.»

## G. `.tex8/secciones/07_conclusiones.tex`, trabajo futuro, línea 71

**Añadir:**

«\item \textbf{Lectura del directorio por principio de tamaño}: reemplazar B1 por la regla que prefiere la envolvente más estrecha que contiene la pista, que corrige el sesgo de ancho con registro desbalanceado y coincide con B1 cuando está balanceado (experimentos 20 y 22).
\item \textbf{Percepciones por nivel}: una percepción invariante para el índice y otra sensible al detalle para cada especialista (experimento 19).
\item \textbf{Separación de patrones}: una expansión dispersa del latente antes de la memoria, para que las envolventes no se contengan entre sí y para acercarse a la recolección de instancias.»

## H. `README.md`, tabla, línea 129

**Viejo:** `| Image→labels evocation (top-3 hit) | **97.4%** (85.3% with the 4-variant fill) | |`

**Nuevo:** `| Image→labels evocation (top-3 domain hit) | **97.4%** (85.3% with the 4-variant fill) | top-1: domain 96.0%, class name 48.0%, same word across 3 recalls 38.9% (exp17) |`

## I. `CONTEXTO_SEP2026.md` §9 e `INICIO_NUEVA_SESION.md` §5 y §6

Una viñeta por experimento (17 a 22) con su ubicación y la cifra principal, igual que en la síntesis.
