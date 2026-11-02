# Propuesta viejo/nuevo: 03 Arquitectura y 04 Metodología (consejo de redacción)

**Estado:** pendiente de aprobación. Nada aplicado.

Lo que más pesa: (1) 04 define la **tasa de rechazo** con un «umbral de aceptación» que el sistema no tiene; lo verifiqué en `src/` (1.1). (2) La calibración, el protocolo completo, el barrido ι × κ y la curva de formación usan **un solo directorio compartido** (todos registran todo), no los directorios perspectivales que describe 03, y 04 no lo dice; va en un párrafo nuevo con los bancos auxiliares (16, 12, 171 y 40 consultas) (1.4). (3) La **auditoría** (04:207–224) queda en estado final, y el «pipeline de cuatro etapas» deja de hacer pasar cada consulta por ConceptNet (1.2, 1.3). (4) Lo que 03 y 04 dicen dos veces (τ, ξ = 0, entropías, lista de variantes) se queda en un solo lugar (1.12).

Las líneas son las del `.tex8` actual. Cuando un pasaje cambia con los hechos (`revision_consejo_hechos.md`), el texto nuevo ya los incluye y lo digo. **Regla para separar bloques:** en los textos nuevos de las partes 1 y 2 dejé los términos de la decisión T como están hoy (label, encoder, containment, ruteo, test, gateada…), para que la parte 3 se apruebe o rechace en bloque.

---

## Parte 1. Reglas y estructura

### 1.1 El rechazo no tiene umbral (04:235; 03:36–38 y 03:57–63)

**Dónde:** `04_metodologia.tex:235`
**Viejo:**
```latex
    \item \textbf{Tasa de rechazo}: fracción de consultas para las que ningún módulo supera el umbral de aceptación.
```
**Nuevo:**
```latex
    \item \textbf{Tasa de rechazo}: fracción de consultas que el sistema no asigna a
    ningún módulo. Con $\kappa = 0$ no hay umbral sobre la puntuación: se rechaza lo que
    no tiene soporte (en la fase temprana, $s_k = 0$ en los ocho módulos,
    ecuación~\eqref{eq:score-gated}; en la fase madura, ningún directorio alcanzable lo
    tiene o el destino no contiene la pista) y lo que no llega a ser pista (ningún token
    con vector fastText, o una imagen cuyo latente no alcanza $\tau$).
```
**Por qué:** el código rechaza por soporte cero, no por umbral: `src/stage6_interaction.py:165–192` (`recognize_gated` devuelve 0.0) y `:491–511` (`no_representable_tokens`, `mae_no_support` si `max == 0.0`); `src/stage8_mature.py:69–102` (`directory_no_support`, `content_no_support`); `src/stage7_bidirectional.py:185–193, 225–239` (energía y falta de soporte).

**Dónde:** `03_arquitectura.tex:57–63` (misma idea de umbral: «soporte suficiente»; de paso quita «one-hot» y distingue $g$ de $\mathbf{g}$)
**Viejo:**
```latex
Todas las memorias de directorio son heteroasociativas cuyo dominio derecho codifica la
identidad del módulo ganador.
El vector $\mathbf{g} \in \{0,1\}^{8}$ la codifica en one-hot: cada coordenada corresponde
a un módulo y toma valores binarios ($q{=}2$).
El estado ``desconocido'' no se codifica como una coordenada adicional; se obtiene
operacionalmente cuando ningún módulo alcanza soporte suficiente durante la lectura del
directorio.
```
**Nuevo:**
```latex
Todas las memorias de directorio son heteroasociativas, y su dominio derecho codifica
la identidad $g$ del módulo ganador con un vector $\mathbf{g} \in \{0,1\}^{8}$: una
coordenada binaria por módulo ($q{=}2$).
El estado ``desconocido'' no tiene coordenada propia: es el rechazo, y ocurre cuando
ningún módulo obtiene soporte en la lectura del directorio.
```
**Dónde:** pie de la Tabla 1, `03_arquitectura.tex:36–38` (decía lo mismo que 57–63)
**Viejo:** `El dominio derecho de los directorios tiene una coordenada binaria por módulo ($q{=}2$: ``conoce''\,/\,``no conoce''); no hay una clase explícita de \emph{desconocido}: el rechazo emerge cuando ningún módulo obtiene soporte.}`
**Nuevo:** `El dominio derecho de los directorios tiene una coordenada binaria por módulo ($q{=}2$: ``conoce''\,/\,``no conoce'').}`

### 1.2 Auditoría de fidelidad en estado final (04:207–224)

**Viejo:** de «Antes de producir los números citables se auditó que todas las decisiones del sistema» (210) hasta «únicamente para calcular métricas, nunca dentro del circuito de decisión.» (224), con «La auditoría encontró y corrigió un desvío real…», «El fallback quedó deshabilitado…, las memorias se rellenaron desde cero…» y «Los resultados de este reporte provienen exclusivamente de corridas posteriores a esa auditoría…».
**Nuevo** (título y `\label` sin cambio):
```latex
\subsection{Auditoría de fidelidad}
\label{sec:auditoria}

La auditoría de fidelidad comprueba que las decisiones del sistema salen de operaciones
de las memorias y que ningún número se apoya en datos fabricados:
\begin{itemize}
    \item El vocabulario no contiene vectores sintéticos: un label sin vector fastText
    real queda fuera del llenado, y la escala global $S = 0.1881$ se calcula solo sobre
    vectores reales.
    \item El código de las memorias de Pineda y Morales es idéntico byte a byte al
    original, salvo una guarda que evita cargar sus clasificadores y no toca ninguna
    operación de memoria.
    \item La clase correcta de cada consulta se usa solo para calcular métricas, nunca
    dentro del circuito de decisión.
\end{itemize}
Todos los números reportados salen de corridas de este sistema.
```
**Por qué:** regla 3; dice qué garantiza hoy el sistema, sin contar el error ni su corrección. Coincide con la contribución 4 aprobada (replanteamiento §2f). Mantengo el título «Auditoría de fidelidad» (la contribución 4 y 05:11 la nombran así). Fuente: `results/auditoria_integral/report.md:11, 71, 75`; `models/label_quant_scale.json` (0.18809).
**Dependiente (fuera de mis archivos, para el consolidador de 05):** `05:10–11` «todos los números provienen de corridas posteriores a la auditoría de fidelidad (Sección~\ref{sec:auditoria})» → «todos los números provienen de corridas del sistema descrito (Sección~\ref{sec:auditoria})».

### 1.3 El camino de la consulta no pasa por ConceptNet (04:54–55)

**Viejo:**
```latex
Cada consulta en lenguaje natural transita por un pipeline de cuatro etapas antes de
llegar a las memorias asociativas.
```
**Nuevo:**
```latex
Las pistas de texto salen de dos caminos con la misma representación.
El vocabulario que llena las memorias se extrae de ConceptNet, se vectoriza con
fastText y se cuantiza por magnitud; una consulta en lenguaje natural se divide en
tokens con spaCy, y cada token se vectoriza con el mismo fastText y se cuantiza con la
misma escala.
```
**Por qué:** ninguna consulta pasa por ConceptNet (`src/stage3_conceptnet.py`, `stage4_fasttext.py` construyen el vocabulario; `src/stage6_interaction.py:455–478` procesa la consulta). Los cuatro párrafos se quedan en su orden: primero el camino del vocabulario, después el de la consulta. El título de la subsección va en la parte 3 (pipeline).

### 1.4 Qué consultas y qué directorio usa cada experimento (04:172–175 y 04:248–257)

**Dónde:** `04_metodologia.tex:172–175`
**Viejo:**
```latex
Para los experimentos de protocolo completo (Secciones~\ref{sec:proto-completo}
a~\ref{sec:formacion}) se usa el subconjunto de las primeras 80 consultas
(10 por clase); el estudio de calibración (Sección~\ref{sec:calibracion}) usa el banco
completo.
```
**Nuevo:**
```latex
Los experimentos de protocolo completo (Secciones~\ref{sec:proto-completo}
a~\ref{sec:formacion}) usan las primeras 80 consultas (10 por clase), y el estudio de
calibración (Sección~\ref{sec:calibracion}), hasta 400.
Otros tres bancos se usan una sola vez: las 16 consultas de la reproducción por etapas
(\texttt{TEST\_QUERIES}, 2 por dominio) y 12 consultas representables que describen
objetos fuera de los ocho dominios, ambas en la Sección~\ref{sec:proto-completo}; y, en
la comparación con una sola EHAM (Sección~\ref{sec:eham-unica}), una partición del
banco (las primeras 30 consultas de cada clase forman los directorios y las 171
restantes quedan reservadas para evaluar) más 40 consultas fuera de dominio: las 12
anteriores y 28 de objetos y escenas de categorías ausentes de ETH-80, sin palabras
del vocabulario de labels.
```
**Fuente:** `src/stage6_interaction.py:620–641` (16, 2 por dominio) y `results/exp3_corrected_routing/report.md:24`; `run_rejection_probe.py:51–64` y `results/rejection_probe/summary.json` (12); `run_experiment11_monolithic.py:63, 88–100` (30 por clase: 240 / 171) y `results/experimento11/compuerta_reservadas.md:3` («171 × 10 por corte»); `results/experimento11/consultas_fuera_dominio.txt` (40; encabezado: las 12 primeras son las de la sonda, 28 nuevas sin palabras del vocabulario de etiquetas ni animales o plantas); `run_ablation.py:242–265` (calibración: primeras $N$ o $N/8$ por dominio, $N \le 400$).
**Nota:** que la fase madura de la calibración se mide dentro de muestra ya lo agrega el hecho E1, en 05:22. Si lo prefieres en la metodología, esa frase se mueve aquí.

**Dónde:** `04_metodologia.tex:248–257` (§Organización: una frase de diez líneas que repite el orden de 05:4–8, y falta el alcance del directorio)
**Viejo:** de «La evaluación se organiza en un estudio principal de calibración del directorio» hasta «reproducción completa (Sección~\ref{sec:costo}).»
**Nuevo:**
```latex
La evaluación sigue el orden de la Sección~\ref{sec:resultados}.
El estudio principal es la calibración del directorio (9 condiciones de lectura
$\times$ $N \in \{50, 100, 200, 400\}$ consultas $\times$ 5 semillas).
Le siguen cuatro estudios de caracterización (protocolo completo, parámetros nativos
$\iota \times \kappa$, formación del directorio y capacidad de llenado,
Secciones~\ref{sec:proto-completo} a~\ref{sec:capacidad}), el hemisferio visual
(Sección~\ref{sec:hemisferio-visual}), la comparación con una sola EHAM
(Sección~\ref{sec:eham-unica}), la verificación de una sola memoria de contenido por
módulo (Sección~\ref{sec:una-memoria}) y el costo computacional de la reproducción
completa (Sección~\ref{sec:costo}).
En la calibración, el protocolo completo, el barrido $\iota \times \kappa$ y la
formación del directorio, cada transacción de texto se registra en un solo
\emph{directorio compartido}, igual al registro completo del TME.
Los directorios perspectivales de la Sección~\ref{sec:componentes}, en los que solo
registran el módulo de entrada y el ganador, se usan en el hemisferio visual y en la
comparación con una sola EHAM.
```
**Fuente (verificado en el código):** registran todos: `run_ablation.py:310–313`, `run_experiment3.py:121–125`; un solo directorio: `run_experiment2_iota_kappa.py:224–227`, `run_experiment4.py:163–167`. Perspectivales: `src/stage6_interaction.py:258–278` (`register_transaction`), usado en `src/stage7_bidirectional.py:199–201` y `run_experiment11_monolithic.py:292, 315`.
**Por qué:** el resumen aprobado y 03:511–512 hablan de «directorio compartido» y ningún capítulo lo explica; un lector supone que el 93.0 % sale de los directorios perspectivales de 03. Esto no está en los hechos. **Toca cómo se leen** 06:10–12 y 07:31–33 (la lista de componentes que «funcionan con ocho dominios»): en texto, la lectura B1 y el 93.0 % son con el directorio compartido; el directorio perspectival de texto se mide en el experimento 11 (97.0 % sobre 171 reservadas, hecho E1).

### 1.5 Restos de historia pequeños

| Dónde | Viejo | Nuevo |
|---|---|---|
| 03:453–455 | «La especialización real produce masas desiguales entre módulos: en la corrida del protocolo completo de 8 clases los conteos finales fueron $[46, 16, 40, 25, 30, 18, 21, 31]$.» | «La especialización real produce masas desiguales entre módulos: al final del protocolo completo (Sección~\ref{sec:proto-completo}) los conteos del directorio fueron $[46, 16, 40, 25, 30, 18, 21, 31]$.» |
| 04:152 | «Se introdujo porque el encoder lleva las entradas sin» | «Hace falta porque el encoder lleva las entradas sin» |

**Por qué:** «de 8 clases» supone corridas con otro número de clases; «se introdujo» cuenta un cambio. (04:89 «Se añadió» se resuelve en 2.1.)

### 1.6 Apertura de 04 y definición de «hemisferio» (04:4–6)

**Viejo:**
```latex
Este capítulo describe el conjunto de datos, el pipeline de representación, los
parámetros del sistema, la auditoría de fidelidad y las métricas usadas para evaluar el
sistema EAM-TMS de ocho módulos.
```
**Nuevo:**
```latex
Este capítulo describe el conjunto de datos y su partición, la representación de texto
y de imagen, el banco de consultas, los parámetros de las memorias, la auditoría de
fidelidad, las métricas y la organización de los experimentos.
En adelante, \emph{hemisferio textual} es el camino que va de una frase a los
directorios de texto y a las memorias de contenido, y \emph{hemisferio visual}, el que
va de una imagen a los directorios visuales y a las memorias de contenido.
```
**Por qué:** la lista omitía tres subsecciones, y «hemisferio» se usa en 04–07 (y en el resumen) sin definirse nunca.

### 1.7 Los tres conjuntos de imágenes, las fases A y B y las 16 variantes (04:31–48; 03:479)

**Viejo (04:31–48):** desde «Dentro de la fase de alimentación, se definieron 3 particiones disjuntas con propósitos distintos:» hasta «(656 en total), nunca vistas durante el llenado ni la formación del directorio.» + `\end{itemize}`.
**Nuevo:**
```latex
Las 410 imágenes de cada clase se reparten en tres conjuntos disjuntos:
\begin{itemize}
    \item \textbf{Llenado} (\textit{filling}): imágenes \texttt{train[0:200]} de cada
    clase, con las que se llena la memoria de contenido del módulo especialista.
    Cada imagen se registra en 16 variantes (3200 patrones por clase): la original y 15
    transformaciones, que son el espejo; rotaciones de $\pm 12^{\circ}$ de la imagen y
    de su espejo, y de $\pm 6^{\circ}$ de la imagen; escalas de 0.9 y 1.1; brillo de
    0.85 y 1.15, y desplazamientos de 6 píxeles en las cuatro direcciones.
    Las variantes densifican la distribución latente acumulada sin cambiar el mecanismo
    de la memoria.
    \item \textbf{Interacciones visuales} (\emph{fase A}): imágenes
    \texttt{train[200:328]} de cada clase (1024 en total, 128 por clase), con las que se
    forma el directorio visual.
    El ganador de cada percepción lo decide la puntuación de las ocho memorias de
    contenido sobre la imagen original, y sus 16 variantes se registran con ese ganador.
    \item \textbf{Evaluación} (\emph{fase B}): las 82 imágenes de prueba (\texttt{test})
    de cada clase (656 en total), nunca vistas durante el llenado ni la formación del
    directorio.
\end{itemize}
```
**Dónde:** `03_arquitectura.tex:479`
**Viejo:** «En imagen, durante la fase A cada módulo vio ganar a los otros siete, de modo que el»
**Nuevo:** «En imagen, durante la formación del directorio visual (fase A, Sección~\ref{sec:dataset}) cada módulo vio ganar a los otros siete, de modo que el»
**Por qué:** «fase de alimentación» no existe en la tesis; «fase A/B» se usa en 03 y 04 y se define en 05:304; «15 variantes» (03:177, 04:36) contra «16 variantes» (03:80, 04:45, 05, 06, 07) confunde (forma_04 lo marcó como posible error): son 16 contando la original. Agrega cómo se decide el ganador visual, que ni 03 ni 04 decían (`src/stage7_bidirectional.py:182–203`: `recognize_gated_right` de los ocho, `argmax`, registro de las 16 variantes). Quita el eslogan «es más percepción, no otro modelo» y la personificación «cada percepción decide su ganador».

### 1.8 Conjunto de datos: estructura de ETH-80 y numeración de experimentos (04:15–29)

**Viejo:** desde «Cada clase cuenta con 410 imágenes de $128\times128$ píxeles.» (15) hasta «en cada pliegue se reserva un objeto por clase y el sistema se construye con los otros nueve.» (28–29), con la oración de seis líneas «Por tanto, no hay solapamiento de imágenes entre train y test, pero la partición principal no separa los objetos físicos de ETH-80: verificado sobre la partición persistida, \textbf{los diez objetos físicos…} …».
**Nuevo:**
```latex
Cada clase tiene diez objetos físicos fotografiados desde 41 puntos de vista: 410
imágenes de $128\times128$ píxeles.
Las imágenes de cada clase se dividieron por archivo en 328 de entrenamiento y 82 de
prueba: ninguna imagen está en los dos lados, pero los diez objetos de cada clase
aportan vistas a ambos (solape de instancias del 100\%).
Toda imagen de prueba es, por tanto, una vista nueva de un objeto cuyas demás vistas
participaron del llenado o de la formación del directorio, y las cifras del hemisferio
visual sobre esta partición miden generalización a \emph{vistas nuevas de objetos
conocidos}.
La generalización a objetos nuevos se midió aparte con una validación
\textit{leave-one-object-out} de diez pliegues (experimento~16\footnote{Los
experimentos se citan con el número de su carpeta en \texttt{results/}, donde están el
protocolo y las tablas completas: 10 (tolerancia $\xi$ con directorios
perspectivales), 11 (comparación con una sola EHAM), 13 (variantes por percepción), 14
(umbral de energía), 15 (árbitro por contenido) y 16 (objetos nuevos).},
Sección~\ref{sec:limitaciones}): en cada pliegue se reserva un objeto por clase y el
sistema se construye con los otros nueve.
```
**Por qué:** el lector no sabe de dónde salen las 410 imágenes ni qué es «experimento 16» (los números 10–16 se usan en 04–06 sin definirse). Parte una oración de seis líneas y quita «verificado sobre la partición persistida». Fuente: `results/experimento16/README.md` («41 vistas del objeto reservado»); encabezados de `results/experimento{10,13,14,15,16}/README.md`.

### 1.9 Notación usada antes de definirse (nuevo párrafo al final de §Componentes, tras 03:89)

**Nuevo:**
```latex
\paragraph{Notación.}
Una consulta de texto produce una pista por token, $\mathbf{v}_q \in
\{0,\ldots,15\}^{300}$: el vector fastText del token, cuantizado por magnitud.
Una imagen produce una pista, $\mathbf{z}_q \in \{0,\ldots,31\}^{64}$: su latente
cuantizado.
$g$ es el módulo ganador de una transacción; $s_k$, la puntuación que el módulo $k$ da
a una pista con su memoria de contenido, y $\hat{s}_k$, la que un directorio da al
módulo $k$ con la lectura B1 (Sección~\ref{sec:operaciones}).
```
**Por qué:** las Figuras 1–3 usan $\mathbf{v}_q$, $\mathbf{z}_q$, $g$, $s_k$ y B1 antes de 03:395 y 03:522; «pista» nombraba a la vez un token y la consulta entera (véase también 2.7, 03:395 y 03:428).

### 1.10 Falta la recuperación texto → imagen (nueva subsección antes de 03:520)

**Nuevo:**
```latex
\subsubsection*{Recuperación de contenido (texto $\to$ imagen)}

El módulo destino aplica la recuperación $\beta$ de su memoria de contenido desde la
izquierda, con la primera pista de la consulta que esa memoria reconoce y con los pesos
que lee de $M^L$; el resultado es un latente muestreado $\hat{\mathbf{z}}_q$ que el
decoder convierte en imagen.
```
**Por qué:** las Figuras 2 y 3 dibujan «Recall β» y §Operaciones no dice con qué pista ni con qué pesos. Fuente: `src/stage8_mature.py:111–122` y `src/stage6_interaction.py:528–541` (recorre los tokens y se queda con el primero que `recall_from_left` reconoce); `src/hetero_memory.py:57–60, 90–103` (pesos de la lectura del dominio izquierdo).

### 1.11 Métricas que 05–07 y el resumen usan sin definir (04:240)

**Viejo:**
```latex
    \item \textbf{Enrutamiento de test} (hemisferio visual): fracción de imágenes de prueba asignadas correctamente por el directorio visual, junto con la precisión sobre las imágenes aceptadas.
```
**Nuevo:**
```latex
    \item \textbf{Enrutamiento de test} (hemisferio visual): fracción de las imágenes de
    prueba que el directorio visual asigna al módulo de su clase. Se acompaña de la
    precisión sobre las imágenes aceptadas (sin contar los rechazos) y del número de
    \emph{falsos enrutamientos}, imágenes asignadas a otra clase.
    \item \textbf{Cobertura de punta a punta} (hemisferio visual): fracción de las
    imágenes de prueba enrutadas a su clase cuyo módulo destino además responde: la
    recuperación $\beta$ desde el latente lo reconoce.
```
**Fuente:** `results/experimento13/README.md:3` («Responde: `recall_from_right` del especialista propio reconoce»; «e2e: rutea a la clase correcta y el destino responde»). La evocación de dominio (04:241) ya la corrige el hecho E10.

### 1.12 Lo que 03 y 04 dicen dos veces: queda en un solo lugar

| Qué | Dónde queda | Qué sale |
|---|---|---|
| Lista de las 15 transformaciones | 04 §Conjunto de datos (1.7) | pie de la Fig. 1 (03:176–179) |
| Extracción de ConceptNet (bidireccional, masa, filtro) | 04 §Pipeline (04:57–70) | pie de la Fig. 1 (03:172–174) |
| Valor de τ, su cálculo y sus rechazos (16.61, 18.45, 10 %, 1 de 1024, 4 de 656) | 04 §Percepción (04:148–157) | 03:493–498 |
| Razón de ξ = 0 | 03 (texto llano); evidencia en 05:324–328 | 04:191–196 |
| Lectura de la entropía del directorio | 02:304–313 (ya está) y fórmula en 03 | 03:511–516 se acorta |
| Entropías 2.22–2.41 bits y registros 2016–2048 / 144–368 | 05, párrafo «Fase A» | 03:517–518 |
| 3.000 bits del TME | 05:310–311 (ya está) | 03:514 |

**a) Pie de la Figura 1 (03:171–185).**
**Viejo:** desde «\caption{Llenado de la memoria de contenido (etapas 3--5).» hasta «ecuación~\eqref{eq:marginal}; no se llenan.}»
**Nuevo:**
```latex
\caption{Llenado de la memoria de contenido.
La rama semántica toma el vocabulario de cada clase de ConceptNet y cuantiza sus
vectores fastText por magnitud sobre una escala global guardada $S$
(Sección~\ref{sec:pipeline-semantico}).
La rama visual cuantiza los códigos ResNet18 de las 200 imágenes de llenado por clase,
cada una en sus 16 variantes (Sección~\ref{sec:dataset}): 3200 registros por clase.
El registro en $M^H_{\mathrm{dom}}$ sigue el esquema \emph{imagen-etiqueta}:
el latente $i$-ésimo (cada variante cuenta como uno) se registra emparejado con el label
$\mathbf{v}_q^{(i \bmod L)}$ de la secuencia expandida por frecuencias
(de longitud $L$), de modo que cada clase aporta el mismo número de registros.
Las lecturas $M^L$ y $M^R$ (punteadas) se calculan de $M^H_{\mathrm{dom}}$ con la
ecuación~\eqref{eq:marginal}; no se llenan.}
```
Quita además «(etapas 3--5)», numeración que la tesis nunca define.

**b) τ en 03 (03:491–498).**
**Viejo:**
```latex
Antes de cualquier memoria visual, el latente continuo pasa un umbral de energía: si su
norma es menor que $\tau$, la imagen se rechaza.
El encoder lleva las entradas sin estructura (gris uniforme, desenfoque fuerte, contraste
casi nulo) cerca del origen, donde caen dentro del soporte de \textit{cow}, \textit{dog}
y \textit{horse}.
$\tau = 16.61$ es la norma mínima de los 1600 originales del llenado (18.45) menos un
margen del 10\%; rechaza una de las 1024 percepciones de la fase A y 4 de las 656
imágenes de prueba.
```
**Nuevo:**
```latex
Antes de cualquier memoria visual, el latente continuo pasa un umbral de energía: si su
norma es menor que $\tau = 16.61$, la imagen se rechaza.
El valor de $\tau$ y por qué hace falta están en la Sección~\ref{sec:percepcion}.
```
(Las clases que aceptan los grises, `cow`, `dog` y `horse`, siguen en 05:353.)

**c) ξ = 0 en 03 (03:484–489)** (corrige además «sería hueco»).
**Viejo:**
```latex
El directorio visual $M^R_{\mathrm{dir}}$ usa la misma lectura B1, con $\xi = 0$ como el
de texto.
No tolera huecos porque, en directorios perspectivales, una coordenada sería hueco si
su valor nunca se registró en ese directorio, para ningún módulo, y eso depende de lo
que el dueño del directorio presenció de los demás: la tolerancia no sería una
propiedad del módulo.
```
**Nuevo:**
```latex
El directorio visual $M^R_{\mathrm{dir}}$ usa la misma lectura B1 que el de texto, con
$\xi = 0$.
No tolera huecos: en un directorio perspectival, una coordenada queda sin registro para
todos los módulos según lo que el dueño del directorio presenció de los demás, así que
una tolerancia $\xi > 0$ dependería de esa historia y no del módulo
(Sección~\ref{sec:hemisferio-visual}).
```

**d) Parámetros en 04 (04:181–196).**
**Viejo:**
```latex
Los parámetros de la EAM se fijaron en:
$\iota = 0$, $\kappa = 0$, $\sigma = 0.1$, y tolerancia de reconocimiento
$\xi = 0$ en los dos hemisferios, también en el directorio visual.
Estos valores siguen el modelo W-EAM y su extensión heteroasociativa, descritos en el
marco teórico.
La propia línea W-EAM ha mostrado que estos hiperparámetros admiten optimización
automática multi-objetivo \cite{lopez2025hyperopt}; aquí se fijan por barrido directo,
cuya justificación experimental se presenta en la Sección~\ref{sec:param-iota-kappa}
(barrido $\iota \times \kappa$) y en la Sección~\ref{sec:hemisferio-visual}
($\xi$ visual).
En síntesis: $\iota > 0$ elimina conocimiento escaso pero válido antes de eliminar
relaciones espurias; $\kappa$ solo rechaza: en todo el rango en que actúa baja la
precisión y nunca la mejora; y $\xi > 0$ no se usa en el directorio visual porque,
con directorios perspectivales, la tolerancia de un módulo dependería de lo que
presenciaron los demás.
Las cifras visuales de la Sección~\ref{sec:hemisferio-visual} se obtienen con $\xi = 0$.
```
**Nuevo:**
```latex
Los parámetros de la EAM se fijaron en $\iota = 0$, $\kappa = 0$, $\sigma = 0.1$ y
tolerancia de reconocimiento $\xi = 0$, iguales en las memorias de contenido y en los
directorios de texto y visuales.
Estos valores siguen el modelo W-EAM y su extensión heteroasociativa
(Sección~\ref{sec:marco_teorico}).
La propia línea W-EAM ha mostrado que estos hiperparámetros admiten optimización
automática multiobjetivo \cite{lopez2025hyperopt}; aquí se fijan por barrido directo,
cuya justificación experimental se presenta en la Sección~\ref{sec:param-iota-kappa}
(barrido $\iota \times \kappa$) y en la Sección~\ref{sec:hemisferio-visual}
($\xi$ visual).
```

**e) Entropía en 03 (03:509–518).**
**Viejo:** desde «Con $K=8$ módulos, el máximo teórico es $\log_2 8 = 3$ bits,» hasta «registros propios contra 144--368 de cada otro módulo.»
**Nuevo:**
```latex
Con $K=8$ módulos, el máximo es $\log_2 8 = 3$ bits, alcanzado cuando los ocho conteos
son iguales.
Esa lectura vale para un registro completo del grupo (el del TME y el directorio
compartido de los experimentos de texto, Sección~\ref{sec:organizacion}), donde una
entropía menor indica colapso hacia un módulo o formación incompleta.
No vale para el directorio de cada módulo, que registra todo lo que ganó y solo parte
de lo ajeno (Sección~\ref{sec:tmt}).
```
**Pasa a 05**, al final del párrafo «Fase A» (sobre el texto que deja el hecho E8): «Los directorios visuales de cada módulo quedan entre 2.22 y 2.41 bits, con 2016--2048 registros propios contra 144--368 de cada otro módulo, como corresponde a un registro perspectival.» Fuente: `logs_comparacion/stage7_bidirectional.log:27–34` (pear 2.223, cup 2.412; mínimo ajeno 144 en dog, máximo 368 en cup), según cifras_03_04. Ojo: está en el log de la etapa 7, no en `results/`.

**Por qué (1.12 entero):** acorta 03 sin perder nada; cada cifra queda una vez, en el capítulo que le toca (método en 04, resultado en 05).

### 1.13 Orden en §Componentes (03:14–16 y 03:65–89)

**a) Decir qué guarda un módulo antes de contar memorias (03:14–16).**
**Viejo:**
```latex
El sistema EAM-TMS contiene en total \textbf{26 memorias asociativas} (tres por módulo
$\times$ ocho módulos, más dos en el TME).
La Tabla~\ref{tab:memorias} resume todas las memorias, sus dominios y sus dimensiones.
```
**Nuevo:**
```latex
Cada uno de los ocho módulos guarda su contenido en una sola memoria heteroasociativa
$M^H_{\mathrm{dom}}$, que asocia labels con latentes de imagen, y lleva dos directorios,
uno para pistas de texto y otro para pistas de imagen; el TME lleva otros dos.
En total son \textbf{26 memorias asociativas} (tres por módulo, más dos del TME); la
Tabla~\ref{tab:memorias} resume sus dominios y dimensiones.
```

**b) Partir el párrafo de siete ideas (03:65–89).**
**Viejo:** desde «Cada módulo mantiene \emph{dos} directorios, uno por modalidad de la pista:» hasta «no contiene el latente ajeno.»
**Nuevo:**
```latex
Cada módulo mantiene \emph{dos} directorios, uno por modalidad de la pista: el de
\textbf{texto} $M_{\mathrm{dir}}$ (pista de etiqueta $300\times16$) y el \textbf{visual}
$M^R_{\mathrm{dir}}$ (pista de latente $64\times32$). Ambos apuntan al mismo destino (la
identidad del módulo), pero las pistas viven en espacios distintos, por lo que requieren
relaciones heteroasociativas separadas.
El TME conserva además sus propios $M^L_{\mathrm{dir}}$ y $M^R_{\mathrm{dir}}$, con el
registro completo del grupo; sirven de diagnóstico y ningún ruteo los consulta.

Registrar una transacción es asociar la pista ($\mathbf{v}_q$ en $M_{\mathrm{dir}}$,
$\mathbf{z}_q$ en $M^R_{\mathrm{dir}}$) con el identificador $g$ del módulo ganador.
Registran solo quienes participaron: el módulo por el que entró la consulta y el
ganador; el TME las registra todas (la \emph{actualización del directorio} de Wegner,
por transacción).
Los directorios son, por tanto, \emph{perspectivales}: cada módulo sabe de los demás lo
que los vio ganar.
En el directorio visual, cada percepción se registra con sus 16 variantes
(Sección~\ref{sec:dataset}) y el mismo ganador.

Esto permite la coordinación de la recuperación de Wegner también para imágenes: una
imagen puede entrar por \emph{cualquier} módulo, que consulta su $M^R_{\mathrm{dir}}$ y
los de los módulos que conoce y la reenvía al especialista, o la rechaza si nadie la
contiene (Sección~\ref{sec:operaciones}).
Un puente desde la memoria de contenido del módulo de entrada hacia su directorio de
texto no serviría: cuando el módulo de entrada no es el especialista, su memoria de
contenido no contiene el latente ajeno y el puente no redirige.
```
**Por qué:** el lector recibía 26 memorias y una tabla antes de saber qué guarda un módulo; el párrafo de 25 líneas obligaba a releer. Corrige un error de notación (decía «un par $(\mathbf{v}_q, g)$» también para el directorio visual, donde la pista es $\mathbf{z}_q$), cambia «\emph{directory updating}» por el nombre que usan 01:17 y 02:274 y quita la coda repetida «una sola relación no admite dos formas de pista» y «no-especialista».

---

## Parte 2. Claridad y estilo

### 2.1 spaCy y el rescate (04:85–106; incluye el hecho D3)

**Viejo:** desde «\paragraph{Procesamiento de consultas con spaCy.}» hasta «como un detalle de preprocesamiento neutro.» (con «Se añadió un…», «POS», «deduplicación estable», la raya «---», «Conviene precisar su estatus:»).
**Nuevo:**
```latex
\paragraph{Procesamiento de consultas con spaCy.}
Las consultas en lenguaje natural se procesan con spaCy~\cite{honnibal2020spacy}: se
lematizan, se conservan los tokens de categoría gramatical \texttt{NOUN}, \texttt{ADJ}
o \texttt{PROPN}, se eliminan las palabras vacías y cada token se conserva una sola vez,
en su orden.
Un \emph{rescate de atención léxica} recupera un token que el etiquetador gramatical
descartó si, aislado, se etiqueta como \texttt{NOUN}, \texttt{ADJ} o \texttt{PROPN}, o
si es un label registrado en las memorias; este segundo criterio solo \emph{admite}
pistas, nunca descarta ninguna.
El rescate corrige errores del etiquetador en frases nominales cortas (p.\ ej.\
\texttt{pear} etiquetado como verbo en ``a bosc pear\ldots''), que de otro modo
quitarían la pista más distintiva de la consulta.
Sobre el banco completo la regla afecta a 46 consultas: con el rescate aciertan 43
(93.5\%) y sin él 33 (71.7\%), diez aciertos más (21.7 puntos), y sin él cuatro se
rechazan.
Los diez cambios de ganador van todos hacia la clase correcta, y los tokens rescatados
con más frecuencia son \texttt{bark}, \texttt{riding}, \texttt{drink}, \texttt{canine}
y \texttt{drive}.
La regla no decide el ganador, que sale de la proyección gateada de las memorias, pero
sí decide qué tokens entran como pista, con un criterio tomado del vocabulario que llenó
las memorias; por eso se reporta con su efecto medido (limitación (g),
Sección~\ref{sec:limitaciones}).
```
**Por qué:** una oración con dos puntos, raya, negrita y punto y coma; «POS» sin desarrollar; «Se añadió» (regla 3); muletilla. «Diez aciertos más (21.7 puntos)» evita que el lector reste 93.5 − 71.7 = 21.8 (10/46 = 21.74). La lista de tokens es la del hecho D3.

### 2.2 Percepción visual (04:123–141; incluye los hechos D2 y D5)

**Viejo:** desde «Para obtener representaciones latentes de las imágenes se entrenó un autoencoder» hasta «mirando ese conjunto (Sección~\ref{sec:limitaciones}).» (con «(no es un \textit{masked autoencoder}…)», «MSE + 0.1·CE», «RMSE» sin desarrollar, «Una precisión de protocolo que debe declararse:» y «$\approx$5 candidatos»).
**Nuevo:**
```latex
Para obtener representaciones latentes de las imágenes se entrenó sobre las ocho clases
un autoencoder convolucional con encoder basado en ResNet18~\cite{he2016resnet},
inicializado con los pesos de ImageNet.
El espacio latente tiene dimensión 64.
La pérdida suma el error cuadrático medio de reconstrucción (MSE) y una entropía
cruzada de clasificación (CE) con peso 0.1; la cabeza clasificadora solo guía el
entrenamiento del codificador y \textbf{no participa} en el enrutamiento ni en la
recuperación del sistema de memorias.
El entrenamiento es \emph{determinista} (semilla 42 en \texttt{torch}, \texttt{numpy} y
\texttt{random}, con cuDNN determinista), de modo que una réplica desde cero es
reproducible; el encoder alcanza una raíz del error cuadrático medio (RMSE) de 0.110 y
una precisión de la cabeza auxiliar del 99.7\%.
No hay partición de validación separada: el punto de control se elige por RMSE mínimo
sobre el propio conjunto de prueba (una evaluación cada 10 épocas: cinco candidatos),
así que el espacio latente con el que se evalúa el hemisferio visual se eligió mirando
ese conjunto (limitación (f), Sección~\ref{sec:limitaciones}).
```
**Por qué:** siglas sin desarrollar, muletilla de apertura y la misma valoración que la limitación (f). Quita el paréntesis del *masked autoencoder*: la tesis nunca escribe «MAE» y responde a una duda que el lector no tiene (si quieres conservarlo por el nombre del repositorio, di por qué). D5 va en español («inicializado con los pesos de ImageNet») y D2 («cinco candidatos») ya está dentro. 04:142–146 (escala min-max) no se toca aquí: depende de la decisión D1 de los hechos.

### 2.3 Coordinación de la fase madura (03:468–474)

**Viejo:**
```latex
En la fase madura, el módulo de entrada suma la lectura B1 de su directorio y la de los
directorios de los módulos que conoce (los que vio ganar alguna transacción) y reenvía
al de mayor puntuación.
Si nadie en ese círculo tiene soporte, la consulta pasa al conocido con más registros,
que suma a su vez los directorios de sus propios conocidos que aún no se consultaron, y
así hasta encontrar soporte o agotar a los alcanzables; si ninguno lo tiene, el sistema
rechaza.
```
**Nuevo:**
```latex
En la fase madura, el módulo de entrada suma la lectura B1 de su directorio y la de los
directorios de los módulos que conoce (los que vio ganar alguna transacción) y reenvía
al de mayor puntuación.
Si nadie en ese círculo tiene soporte, la consulta pasa al conocido con más registros,
que suma a su vez los directorios de sus propios conocidos aún no consultados.
El paso se repite hasta encontrar soporte; si ningún módulo alcanzable lo tiene, el
sistema rechaza.
```
**Por qué:** cuatro decisiones encadenadas en una frase.

### 2.4 Cambios pequeños en 03

| Línea | Viejo | Nuevo | Por qué |
|---|---|---|---|
| 32–33 | `Para cada memoria se indica $(n_L, m_L \leftrightarrow n_R, m_R)$, o $(n_L, m_L \to n_R, m_R)$ cuando la relación es unidireccional.` | `Para cada memoria se indica $(n, m \leftrightarrow p, q)$, como en la Sección~\ref{sec:hetero4d}, o $(n, m \to p, q)$ cuando la relación es unidireccional.` | Misma notación que 02:149–150 |
| 94–96 | «Los tres diagramas siguientes muestran las tres etapas operativas del sistema: el llenado de la memoria de contenido, la recuperación mediada por el TME (fase temprana) y la recuperación punto a punto (fase madura).» | «Los tres diagramas siguientes muestran las tres etapas operativas del sistema: el llenado de la memoria de contenido (Figura~\ref{fig:arq-llenado}), la recuperación mediada por el TME (fase temprana, Figura~\ref{fig:arq-temprana}) y la recuperación punto a punto (fase madura, Figura~\ref{fig:arq-madura}).» | Las Figuras 2 y 3 no se citan en ningún lugar |
| 294 | «con la proyección de su memoria hetero, ponderada» | «con la proyección de su memoria heteroasociativa, ponderada» | «hetero» no se ha presentado como abreviatura |
| 395 | «Para un módulo $k$ dada una pista $\mathbf{v}_q$ (representación semántica cuantizada),» | «Para un módulo $k$, dada una pista $\mathbf{v}_q$ (un token de la consulta, cuantizado),» | Pista = un token; coma |
| 423–424 | «carece completamente de soporte» | «carece de soporte» | La ecuación ya lo dice |
| 428–430 | «El módulo ganador es $g = \arg\max_k \sum_{\text{tokens}} s_k$ (la suma recorre todos los tokens semánticos de la pista; esta agregación multi-token es el protocolo de asignación de información de Wegner y vive fuera de las memorias por diseño).» | «El módulo ganador es $g = \arg\max_k \sum_{\text{tokens}} s_k$: la suma recorre las pistas de la consulta, una por token. Esta suma es el protocolo de asignación de información de Wegner y vive fuera de las memorias por diseño.» | «tokens de la pista» contradecía 395; «multi-token» |
| 433 y 452 | `\paragraph{Justificación.}` (dos veces en una página) | 433: `\paragraph{Por qué la activación media es comparable.}`; 452: `\paragraph{Por qué dividir entre el conteo.}` | Titulito repetido |
| 461–463 | «El conteo $c_k$ lo lleva la memoria de directorio como un contador aparte de la relación, pero no agrega información: es la masa que la relación acumula en la columna ``conoce'' del módulo $k$, igual para cualquier característica.» | «El conteo $c_k$ se guarda como un contador aparte, pero no agrega información: es el número de veces que se registró ``conoce'' para el módulo $k$, el mismo en todas las características de la relación.» | Había que releerla |
| 464 | «Su necesidad se demuestra empíricamente en la Sección~\ref{sec:calibracion}.» | «La Sección~\ref{sec:calibracion} mide su efecto.» | Verbo de reseña |
| 529–530 | «El reconocimiento visual usa solo esa lectura y no la proyección hacia las etiquetas (cuyo lado, con la cuantización por magnitud, es más disperso y rechazaría de más).» | «El reconocimiento visual usa solo esa lectura, no la proyección hacia las etiquetas: el lado de etiquetas, cuantizado por magnitud, es más disperso y rechazaría imágenes que el lado latente sí contiene.» | Paréntesis difícil |
| 545–546 | «interpreta esa muestra en términos del vocabulario conocido.» | «interpreta esa muestra con el vocabulario conocido.» | Calco |
| 547–548 | «La necesidad del diccionario no es una debilidad del sistema sino una consecuencia directa de la naturaleza entrópica de la recuperación.» | quitar | Cierre defensivo; las dos frases anteriores ya lo explican |
| 559–561 | «La fidelidad mide \emph{coincidencia con lo aprendido}, no acierto absoluto: un sistema con fidelidad alta conservó lo aprendido en la fase temprana al pasar a los directorios individuales.» | «La fidelidad mide coincidencia con lo aprendido en la fase temprana, no acierto absoluto.» | La segunda mitad repite la primera |

**Notación del directorio de texto** ($M_{\mathrm{dir}}$ en el módulo, $M^L_{\mathrm{dir}}$ en el TME: la misma memoria con dos nombres). Propongo $M^L_{\mathrm{dir}}$ en todas partes, en par con $M^L$/$M^R$ y con $M^R_{\mathrm{dir}}$: `$M_{\mathrm{dir}}$` → `$M^L_{\mathrm{dir}}$` en 03:47 (tabla), 66 y 73 (o sus lugares en el texto de 1.13b), 379 (pie de la Fig. 3) y 443. El nodo de la Fig. 3 (03:331) va con la propuesta de figuras.

### 2.5 Cambios pequeños en 04

| Línea | Viejo | Nuevo | Por qué |
|---|---|---|---|
| 77 | «\textbf{escala global persistida}» | «\textbf{escala global guardada}» | Calco de programación (*persisted*) |
| 80–83 | «La misma escala se aplica en el llenado y en la consulta, lo que garantiza que ambos lados hablen el mismo alfabeto. Con esto los 16 niveles se pueblan efectivamente (véase la Figura~\ref{fig:espacio-semantico}).» | «La misma escala se aplica en el llenado y en la consulta. Con esto quedan poblados los 16 niveles (Figura~\ref{fig:espacio-semantico}).» | Metáfora mezclada; «efectivamente» calco |
| 163–164 | «con etiqueta de clase correcta conocida (\textit{ground truth}), aproximadamente 50 por dominio,» | «con su clase correcta conocida, aproximadamente 50 por dominio,» | «etiqueta» aquí chocaba con la etiqueta del vocabulario |
| 170–171 (tras D4) | «, reflejando la comunicación realista de un grupo de Wegner: quien pregunta aporta las señas del dominio.» | «, como en la comunicación de un grupo de Wegner: quien pregunta aporta las señas del dominio.» | Gerundio adjetivo; «realista» sin medida |
| 198 y 201 | «los pesos por rasgo» / «en cada rasgo» | «los pesos por característica» / «en cada característica» | 02 los llama «características» |
| 234 | «con lectura de directorio corregida por conteo (B1) o cruda.» | «con la lectura B1 o la cruda del directorio.» | El resto de la tesis dice «lectura B1» |
| 239 | «fracción de victorias maduras capturadas por cada módulo» | «fracción de victorias maduras obtenidas por cada módulo» | Calco |

---

## Parte 3. Términos (decisión T)

Solo prosa y pies de 03 y 04; los nodos TikZ, `\texttt{}`, `\label{}` y ecuaciones no se tocan. «(1.x)» marca una aparición que está dentro de un texto nuevo de las partes 1 o 2: si ambos se aprueban, el cambio se aplica sobre ese texto nuevo. «sale con 1.x» = el término desaparece si se aprueba ese punto.

| Línea | Viejo | Nuevo |
|---|---|---|
| 03:18 | un encoder ResNet18 | un codificador ResNet18 |
| 03:19 | un decoder convolucional | un decodificador convolucional |
| 03:34 | El dominio \emph{label} | El dominio \emph{etiqueta} |
| 03:71 (1.13b) | ningún ruteo los consulta | ningún enrutamiento los consulta |
| 03:181 (1.12a) | con el label $\mathbf{v}_q^{(i \bmod L)}$ | con la etiqueta $\mathbf{v}_q^{(i \bmod L)}$ |
| 03:177 | 15 variantes de augmentación | sale con 1.12a |
| 03:393 | `\subsubsection*{Score de enrutamiento (gated)}` | `\subsubsection*{Puntuación de enrutamiento con compuerta}` |
| 03:399 | en la lectura de labels | en la lectura de etiquetas |
| 03:414 | compuerta de containment | compuerta de contención |
| 03:436 | con la misma augmentación, emparejadas con la secuencia de labels | con las mismas variantes, emparejadas con la secuencia de etiquetas |
| 03:493 | El encoder lleva | sale con 1.12b (si no: El codificador lleva) |
| 03:520 | (imagen $\to$ labels) | (imagen $\to$ etiquetas) |
| 03:523 | la recuperación de labels | la recuperación de etiquetas |
| 03:537–538 | entre los labels de los ocho vocabularios … como labels asociados a la imagen | entre las etiquetas de los ocho vocabularios … como etiquetas asociadas a la imagen |
| 03:542 | la distribución de labels | la distribución de etiquetas |
| 03 (1.10) | que el decoder convierte | que el decodificador convierte |
| 03 (1.13a) | asocia labels con latentes | asocia etiquetas con latentes |
| 04:4, 04:54 | pipeline | sale con 1.6 y 1.3 |
| 04:18, 20–21 | train y test; tanto a train como a test | sale con 1.8 (si no: entrenamiento y prueba; tanto al entrenamiento como a la prueba) |
| 04:36 | variantes de \emph{augmentación} | sale con 1.7 |
| 04:51 | `\subsection{Pipeline semántico}` | `\subsection{Representación de texto: vocabulario y consultas}` (el `\label` se queda) |
| 04:66, 68 | cada label; los labels fuertes | cada etiqueta; las etiquetas fuertes |
| 04:70 (tras D2) | 21 labels efectivos cada una y ninguno sintético | 21 etiquetas efectivas cada una y ninguna sintética |
| 04:91 (2.1) | un label registrado | una etiqueta registrada |
| 04:103 (2.1) | proyección gateada | proyección con compuerta |
| 04:114 | el \textit{containment} | la contención |
| 04:120 | `\subsection{Percepción visual: encoder ResNet-18}` | `\subsection{Percepción visual: codificador ResNet18}` |
| 04:123–124, 133 (2.2) | autoencoder … con encoder … el encoder alcanza | autocodificador … con codificador … el codificador alcanza |
| 04:139 | sobre test | sale con 2.2 |
| 04:152 | el encoder lleva | el codificador lleva |
| 04:157 | ruteaba | enrutaba |
| 04:203 | el containment, y con él | la contención, y con ella |
| 04:240 (1.11) | Enrutamiento de test | Enrutamiento de prueba |
| 04 (1.2, 1.4) | un label sin vector; vocabulario de labels | una etiqueta sin vector; vocabulario de etiquetas |

**Mismo criterio, fuera de la lista del brief** (aprobar o rechazar con el bloque):

| Línea | Viejo | Nuevo |
|---|---|---|
| 03:22 | con embeddings fastText 300D | con vectores fastText de 300 dimensiones |
| 03:544 | ningún embedding almacenado | ningún vector almacenado |
| 04:143 | calculada exclusivamente sobre el pool de llenado | calculada solo sobre el conjunto de llenado (sobre el texto que deje D1) |

---

## Parte 4. Forma

| Línea | Viejo | Nuevo | Error |
|---|---|---|---|
| 03:45 | `Módulo $k$ (×8)` | `Módulo $k$ ($\times 8$)` | símbolo fuera de modo matemático (el resto usa `$\times$`) |
| 03:88 | no-especialista | no especialista | prefijo con guion (sale con 1.13b) |
| 03:395 | Para un módulo $k$ dada una pista | Para un módulo $k$, dada una pista | coma (va en 2.4) |
| 03:429 | multi-token | multitoken | prefijo con guion (sale con 2.4) |
| 03:486 | una coordenada sería hueco | una coordenada sería un hueco | falta el artículo (sale con 1.12c) |
| 04:93 | `(p.ej.\` | `(p.\ ej.\` | abreviatura (va en 2.1) |
| 04:120, 124 | ResNet-18 | ResNet18 | el resto de la tesis escribe ResNet18 (04:120 también en la parte 3) |
| 04:187 | multi-objetivo | multiobjetivo | prefijo con guion (va en 1.12d) |

---

## Descartado

- **claridad A4, cifras 2, consistencia 8.1** (03:4–5 «en su versión de ocho módulos»): ya está en el hecho C1.
- **antipatrones: quitar el párrafo de apertura de 03 (03:4–9) y el de 04 (04:4–6)**: un mapa breve del capítulo es normal en una tesis; 03 queda con C1, y 04 con 1.6, que además define «hemisferio».
- **claridad M1, versión completa** (rehacer 03:14–25 con dominios, alfabetos y componentes): tomé solo la primera frase (1.13a) y el recorte del pie (1.1); el resto no acorta.
- **claridad M3** (un párrafo por diagrama en el cuerpo y pies cortos de las Figs. 2 y 3): alarga 03; tomé las referencias (2.4) y el pie corto de la Fig. 1 (1.12a). La regla $i \bmod L$ se queda en el pie de la Fig. 1, que es donde se dibuja.
- **claridad M4** (definir en 04 las «etapas 1–8» de los scripts): basta quitar «(etapas 3–5)»; la tabla de costo nueva decide si numera etapas.
- **claridad M6, M7, B8; consistencia 1.3 (nodos «Recall β», «Decoder», «Encoder», «hetero», «(+ augmentación)», «ubicación», $M_{\mathrm{dir}}$ en 03:331)**: van a la propuesta de figuras. Dato para ella: «ubicación» es el tercer elemento de la terna de Wegner (imagen, etiquetas, ubicación) que devuelve la consulta, es decir, el módulo que responde (`src/stage6_interaction.py:442`).
- **claridad M13 como lista numerada**: tomado como tres frases (2.3), sin lista.
- **claridad M22** (glosa de σ): σ ya está en 02 (operación β).
- **claridad M23** (mover 04:198–204 a 03): no acorta; solo «rasgo» → «característica» (2.5).
- **claridad M27, frase extra sobre pesos todos cero**: detalle de implementación que da el mismo resultado que la compuerta; el resto de 03:405 ya lo cubre el hecho C5.
- **claridad M30, antipatrones j4** (el puente en 01 y 03): el arreglo está en 01, fuera de mis archivos.
- **claridad B1: quitar las glosas *early accuracy*, *mature accuracy*, *winner share* (04:233, 234, 239)**: léxico las da por correctas (glosa en cursiva junto al término español).
- **claridad dudas 6 y 8** (qué es la «frecuencia» de la secuencia de etiquetas; valor del tope $w$): no encontré la fuente sin correr nada; quedan como pregunta al autor.
- **antipatrones 03:423–424, quitar «el módulo no opina sobre lo que no contiene»**: es una glosa útil y coherente con el lenguaje de Wegner; solo sale «completamente».
- **antipatrones 04:109–117** (comprimir «sin filtro de vocabulario»): ahorra dos líneas; es de gusto.
- **léxico 04:69–70 «efectivos»**: calco leve; D2 ya toca la frase.
- **consistencia 4.3, alternativa mínima** ($M_{\mathrm{dir}}$ también en el TME): elegí la simétrica, $M^L_{\mathrm{dir}}$ (2.4).
- **consistencia 4.5** ($L$ como superíndice y como longitud de la secuencia): el contexto lo distingue.
- **consistencia 5.1 en 04:241** (evocación sobre 15 imágenes por clase): ya está en el hecho E10.
- **cifras_03_04, hallazgos bajos 9–12**: los cuatro ya están en los hechos (D2, D2, C2, C5); los medios y altos también (C3, C4, D1, D3, D4, E11).
- **forma_03, «3.000 bits» como separador de miles y separador decimal / formato de porcentaje**: falso positivo (es una entropía con tres decimales); el resto se decide con la plantilla de la UACJ.
- **forma_04, 04:166 «p.ej.»**: ya lo corrige el hecho D4.
