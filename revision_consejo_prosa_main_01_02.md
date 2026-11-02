# Propuesta viejo/nuevo: resumen y portada, introducción y marco teórico (consejo de redacción)

**Estado:** pendiente de aprobación. Nada aplicado.

Lo que más pesa: dos errores de hecho en el marco teórico, los dos verificados en el código. La entropía de la EHAM se promedia sobre pares de características $(i, j)$, no sobre valores $(a_i, b_j)$ (1.6). El pasaje de la pista faltante dice que el sistema no usa los métodos de ese artículo, pero su recuperación por defecto, *sample-and-search*, es uno de ellos (1.7). El resumen se reordena: primero el problema, luego el método, los resultados y la conclusión. El texto nuevo parte del aprobado con los ajustes de A1, no agrega ninguna cifra y lista cada diferencia (1.2). En el marco, las lecturas de dominio pasan a ir antes de la proyección, que las usa, y $\kappa$ se explica después de definir $\Pi$; además se separan las dos medidas que hoy se llaman «entropía del directorio» (1.8 a 1.10).

**Orden de aplicación.** Primero el replanteamiento, luego hechos (A1, A6, B1), luego referencias si se aprueba, y al final esta propuesta. Los números de línea son los del `.tex8` actual. Si un pasaje cambia con el replanteamiento o los hechos, el «Viejo» cita el texto que resulta de ellos y lo dice. La propuesta de referencias toca varios de estos pasajes (A1, A2, A3, A4, M1, M2, M5, M7, B6). Donde se cruzan, lo marco y escribo el cambio para que funcione con o sin el de referencias.

---

## Parte 1. Reglas y estructura

### 1.1 Portada: subtítulo (ya aprobado)
- **Dónde:** `main.tex:46`
- **Viejo:** `\large Versión de 8 módulos (ETH-80 completo)\\[0.5em]`
- **Nuevo:** `\large Ocho módulos sobre ETH-80 completo\\[0.5em]`
- **Por qué:** lo aprobaste con el replanteamiento. Lo incluyo para que se aplique junto con lo demás.

### 1.2 Resumen: primero el problema, después el sistema (sobre el texto aprobado con A1)
- **Dónde:** `main.tex:57–85` (entre `\begin{abstract}` y `\end{abstract}`)
- **Viejo:** el texto del replanteamiento §1 con los cuatro ajustes de A1 de hechos:
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
  directorio compartido, evaluada sobre las mismas consultas que lo formaron; banco de 411
  consultas, $N{=}400$, 5 semillas), y la lectura B1 reduce la participación del módulo
  \textit{apple} del 20.5\% de la lectura cruda al 13.8\% (ideal 12.5\%).
  El hemisferio visual enruta el 96.2\% de las imágenes de prueba (631 de 656), con un
  rechazo del 3.5\% y dos falsos enrutamientos; con objetos nunca vistos, la cobertura de
  punta a punta es del 89.2\%, frente al 95.5\% de vistas nuevas de objetos conocidos, con
  dos falsos de 3280.
  Frente a una sola memoria con las ocho clases, la partición en especialistas recuerda con
  más fidelidad y, con la doble compuerta de contenido, acepta menos consultas fuera de
  dominio cuando el contenido crece (2 frente a 8 de 40 con 200 imágenes por clase).
  Los límites observados provienen de las representaciones (el léxico compartido entre
  clases vecinas y la cobertura del espacio latente ante objetos nuevos), no del mecanismo
  asociativo.
  ```
- **Nuevo:**
  ```latex
  Un grupo que trabaja junto recuerda más que cada uno de sus miembros por separado: cada
  miembro sabe quién sabe qué y a quién preguntar.
  Wegner \cite{wegner1987transactive} llamó a esta organización \emph{memoria
  transactiva}.
  Este trabajo pregunta si puede construirse solo con memorias asociativas, sin
  clasificadores supervisados, y presenta EAM-TMS, un sistema distribuido de memoria
  transactiva construido con las Memorias Asociativas Entrópicas de Pineda y Morales en su
  variante ponderada (W-EAM) \cite{pineda2021entropic,pineda2022weighted} y su extensión
  heteroasociativa (EHAM) \cite{morales2024hetero,morales2025missing}.
  El sistema tiene ocho módulos especialistas, uno por cada categoría del conjunto de datos
  ETH-80 \cite{leibe2003eth80}
  (\textit{apple}, \textit{car}, \textit{cow}, \textit{cup}, \textit{dog}, \textit{horse},
  \textit{pear}, \textit{tomato}).
  Cada módulo guarda su contenido en una sola memoria heteroasociativa entre palabras e
  imágenes y lleva dos directorios, uno textual y uno visual, con las transacciones en que
  participa.
  La arquitectura modela los tres mecanismos de Wegner: la actualización del directorio,
  la asignación de información y la coordinación de la recuperación.
  Un mediador central coordina la fase temprana y deja de ser necesario en la fase madura,
  cuando los directorios de los módulos bastan para enrutar.
  Las memorias operan en los dos sentidos, de palabras a imágenes y de imágenes a
  palabras.
  Las palabras entran como vectores fastText de 300 dimensiones
  \cite{bojanowski2017fasttext}, con vocabulario extraído de ConceptNet 5.7
  \cite{speer2017conceptnet} y \emph{cuantización por magnitud} en 16 niveles; las
  imágenes, como códigos de un ResNet18 \cite{he2016resnet}.
  En el estudio de calibración, con un directorio compartido y un banco de 411 consultas
  de texto ($N{=}400$ consultas de formación, 5 semillas), el 90.0\% de las consultas
  llega al módulo correcto en la fase temprana y el 93.0\% en la fase madura con la
  lectura del directorio normalizada por número de registros (B1); la cifra madura se
  mide sobre las mismas consultas que formaron el directorio.
  La lectura B1 reduce la participación del módulo \textit{apple} del 20.5\% de la
  lectura cruda al 13.8\% (ideal 12.5\%).
  Con imágenes, los directorios visuales envían al especialista correcto el 96.2\% de las
  656 imágenes de prueba (631), rechazan el 3.5\% y se equivocan en dos.
  Con objetos que ningún módulo vio, el 89.2\% de las vistas llega al especialista y
  recibe respuesta, frente al 95.5\% con vistas nuevas de objetos conocidos, con dos
  enrutamientos falsos en 3280.
  Frente a una sola memoria con las ocho clases, la partición en especialistas recuerda con
  más fidelidad y, si además el módulo destino debe contener la consulta, acepta menos
  consultas fuera de dominio cuando el contenido crece (2 frente a 8 de 40 con 200
  imágenes por clase).
  Los límites observados provienen de las representaciones (el léxico compartido entre
  clases vecinas y la cobertura del espacio latente ante objetos nuevos), no del mecanismo
  asociativo.
  ```
- **Diferencias con el texto aprobado y A1** (todas las cifras siguen; no hay ninguna nueva):
  1. El resumen abre con el fenómeno y la pregunta, tomados de `01:4–10` y de la pregunta aprobada. El texto aprobado empieza con «Este trabajo presenta EAM-TMS».
  2. «con Memorias Asociativas Entrópicas» pasa a «con las Memorias Asociativas Entrópicas de Pineda y Morales».
  3. Se quita la negrita de «ocho módulos especialistas».
  4. La frase de los tres mecanismos va antes del mediador. Pierde «computacionalmente» y «de experticia» (en `01:17` y `02:274` es «actualización del directorio»). Su cita pasa a la primera oración. Si se aprueba A3 de referencias, ahí va `\cite{wegner1995computer}`.
  5. «Un mediador inicial (TME) coordina las interacciones tempranas» pasa a «Un mediador central coordina la fase temprana … en la fase madura». Es «central» como en `01:45`. La sigla TME se quita porque el resumen no la vuelve a usar. Se nombran las dos fases porque la frase de resultados las usa.
  6. El paréntesis técnico «(fastText 300D …) e imágenes (codificadas por ResNet18)» pasa a dos frases: «en los dos sentidos…» y «Las palabras entran como vectores fastText de 300 dimensiones…».
  7. En la frase de resultados, «precisión temprana/madura» se dice como lo que mide: el porcentaje que «llega al módulo correcto» (`04:233–234`). «Lectura normalizada B1» pasa a «lectura del directorio normalizada por número de registros (B1)», según la ecuación `eq:b1`. El paréntesis de condiciones va al principio de la frase. «Ablación de calibración» pasa a «estudio de calibración», el nombre que usa `05:17`. La salvedad de A1 sobre las consultas de formación se queda.
  8. «El hemisferio visual enruta» pasa a «los directorios visuales envían al especialista correcto». «Cobertura de punta a punta» pasa a «llega al especialista y recibe respuesta», según `06:240`. «Dos falsos de 3280» pasa a «dos enrutamientos falsos en 3280».
  9. «Con la doble compuerta de contenido» pasa a «si además el módulo destino debe contener la consulta», que es la definición de `05:437`.
- **Por qué:** el lector externo lee hoy el sistema antes del problema y no puede descifrar ocho términos de la frase de cifras (hemisferio, punta a punta, B1, compuerta…). Además se juntan cuatro cambios menores sobre este mismo texto: «directorio de experticia» y «mediador central» (de consistencia), la negrita (de antipatrones) y «Memoria Transactiva» con mayúscula (de forma). Si prefieres conservar el orden aprobado, aplica solo A1, las diferencias 3 a 5 y la fila del resumen de la Parte 4.

### 1.3 Introducción: decir qué es una memoria asociativa entrópica antes de la pregunta
- **Dónde:** `01:26–29`. Texto del replanteamiento §2a.
- **Viejo (aprobado):**
  ```latex
  Este trabajo pregunta si esa organización puede construirse solo con memorias
  asociativas:
  ```
- **Nuevo** (la cita de la pregunta sigue igual):
  ```latex
  Las memorias asociativas entrópicas de Pineda y Morales (Sección~\ref{sec:eam}) guardan
  lo que registran como conteos de frecuencia: aceptan una entrada cuando sus rasgos
  tienen soporte en lo registrado, recuerdan muestreando esos conteos y rechazan lo que no
  contienen, sin ningún clasificador entrenado.
  Este trabajo pregunta si la organización que describe Wegner puede construirse solo con
  estas memorias:
  ```
- **Por qué:** el lector pasa de un párrafo sobre grupos humanos a una pregunta sobre «memorias asociativas entrópicas» sin saber qué son. La descripción viene de `02:43–60` y `02:103–111`. «Esa organización» cambia a «la organización que describe Wegner» porque la nueva oración la separa de su antecedente.

### 1.4 Introducción: la sigla EAM-TMS no se desarrolla
- **Dónde:** `01:38–42`. Incluye el cambio 2b del replanteamiento.
- **Viejo (con 2b):**
  ```latex
  El sistema construido, denominado \textbf{EAM-TMS} (sistema distribuido de memorias
  heteroasociativas entrópicas especializadas con una arquitectura de enrutamiento
  semántico y recuperación asociativa multimodal basada en la teoría de memoria
  transactiva), se compone de
  \textbf{ocho módulos especialistas}, uno por cada categoría del conjunto ETH-80
  ```
- **Nuevo:**
  ```latex
  El sistema construido, \textbf{EAM-TMS} (\textit{Entropic Associative Memory --
  Transactive Memory System}: sistema de memoria transactiva sobre memorias asociativas
  entrópicas), se compone de ocho módulos especialistas, uno por cada categoría del
  conjunto ETH-80
  ```
- **Por qué:** el paréntesis actual es el título de la tesis, no lo que significan las letras, y «TMS» no se desarrolla en ningún lugar. La expansión sale de `README.md:5` («models Wegner's (1987) Transactive Memory System») y de `02:7` (EAM). Confirma que esa es la expansión que quieres. También se quita la negrita de énfasis, según antipatrones.

### 1.5 Contribución 3: definir «perspectivales» y quitar la justificación repetida de 03
- **Dónde:** `01:87–97`
- **Viejo:**
  ```latex
      \item \textbf{Directorios perspectivales por módulo.}
      Cada módulo incorpora, junto al de texto, un directorio heteroasociativo visual
      propio ($M^R_{\mathrm{dir}}$), y en ambos registra solo las transacciones en que
      participó, como módulo de entrada o como ganador.
      Una frase o una imagen puede entrar por \emph{cualquier} módulo, que suma su
      directorio y los de los módulos que conoce y la redirige punto a punto al
      especialista, replicando para las dos modalidades la coordinación de recuperación
      de Wegner.
      El directorio visual es propio porque un puente por la memoria de contenido del
      módulo de entrada hacia el directorio de texto no redirige cuando ese módulo no es
      el especialista: su memoria de contenido no contiene el latente ajeno.
  ```
- **Nuevo:**
  ```latex
      \item \textbf{Directorios perspectivales por módulo.}
      Cada módulo lleva dos directorios heteroasociativos, uno de texto y uno visual
      (Sección~\ref{sec:componentes}), y en ambos registra solo las transacciones en que
      participó, como módulo de entrada o como ganador: cada módulo sabe de los demás lo
      que presenció, y por eso los directorios se llaman \emph{perspectivales}.
      Una frase o una imagen puede entrar por \emph{cualquier} módulo, que suma su
      directorio y los de los módulos que conoce y la redirige punto a punto al
      especialista; es la coordinación de recuperación de Wegner, en las dos modalidades.
  ```
- **Por qué:** «perspectivales» va en el título y no se define hasta `03:78`. Además, $M^R_{\mathrm{dir}}$ no está definido aquí, y la razón del «puente» repite `03:86–89` con las mismas palabras. El gerundio «replicando» es un calco.

### 1.6 Marco: la entropía de la EHAM se promedia sobre $(i, j)$, no sobre $(a_i, b_j)$ (alta)
- **Dónde:** `02:155–158`
- **Viejo:** `material relajada con umbrales $\iota$ y $\kappa$, y la entropía es el promedio de las` / `entropías de Shannon por par de características $(a_i, b_j)$ \cite{morales2025missing}.`
- **Nuevo:**
  ```latex
  material relajada con umbrales $\iota$ y $\kappa$, y la entropía es el promedio, sobre
  los pares de características $(i, j)$, de la entropía de Shannon del plano
  $\mathbf{R}[i, j, \cdot, \cdot]$ \cite{morales2025missing}.
  ```
- **Por qué:** $a_i$ y $b_j$ son valores, no características. **Verificado:** `src/hetero_lib/hetero_associative_4d.py:601–611` recorre `i in range(n)` y `j in range(p)` y calcula la entropía de `relation[i, j, :, :]`. Según `:116–119`, la entropía de la memoria es la media de esas entropías. El revisor de referencias confirma que el artículo dice «por par de características».

### 1.7 Marco: el sistema sí usa un método de la pista faltante (hecho; alta)
- **Dónde:** `02:167–170` y `02:221–223`. No está en la revisión de hechos: salió al verificar M23 y B11 de claridad, que proponían decir lo contrario.
- **Viejo (167–170):**
  ```latex
  Conviene ubicarlo con precisión: la proyección ponderada que se describe a continuación
  es el mecanismo \emph{general} de recuperación cuando sí existe una pista fuente con
  pesos; las soluciones a la pista faltante son el parche para el caso específico en que
  ni siquiera esa información existe.
  ```
- **Nuevo (167–170):**
  ```latex
  La proyección ponderada que se describe a continuación produce ese plano a partir de la
  pista fuente y sus pesos; para elegir un objeto del plano, este sistema usa el tercer
  método, que es la recuperación por defecto de la implementación de referencia
  (\texttt{recall\_with\_sampling\_n\_search}).
  ```
- **Viejo (221–223):** `La recuperación heteroasociativa $\beta$ aplica muestreo por columna sobre $\Pi$ y,` / `cuando es necesario, una búsqueda local (\emph{sample-and-search}) para mejorar la` / `calidad del patrón recuperado.`
- **Nuevo (221–223):**
  ```latex
  La recuperación heteroasociativa $\beta$ muestrea $\Pi$ columna a columna varias veces,
  conserva la muestra que, proyectada de regreso, más se parece a la pista, y la mejora
  con una búsqueda local en su vecindad (\emph{sample-and-search}).
  ```
- **Por qué:** el texto dice que el sistema usa un mecanismo «general» y que los métodos de la pista faltante son un «parche» para otro caso. Pero toda recuperación hetero del sistema es ese caso: hay pista en un dominio y ninguna en el otro. Además, el sistema usa el tercer método del artículo. «Cuando es necesario» tampoco es cierto: la búsqueda local corre siempre.
- **Fuentes:**
  - `src/hetero_memory.py:28–36`: «Sample-and-Search (SS) … Es el recall original de Pineda & Morales y el default de este sistema».
  - `src/hetero_memory.py:91, 106`: `method="sample_search"` por defecto. Las etapas 5 a 8 llaman sin `method`.
  - `src/hetero_lib/hetero_associative_4d.py:310–335`: muestreo y luego búsqueda en la vecindad.
  - `:467–478`: la distancia se mide proyectando el candidato de regreso.
  - `src/hetero_lib/commons.py:82`: `sampling_without_search = False`.
  - `.SMTex/secciones/02_marco_teorico.tex:134–137`, otro borrador tuyo: «… \emph{es} sample-and-search».
- **Nota:** los nombres de los métodos en 165–166 los corrige la propuesta de referencias (M2): el tercero es *search-and-test*, que en el cuerpo del artículo se llama *sample-and-search*. Sobre ese texto, quita también «límite» en «para ese caso límite», porque es el caso de toda recuperación del sistema. No leí el artículo; los nombres salen del reporte de referencias y del código.

### 1.8 Marco: las lecturas de dominio, antes de la proyección que las usa
- **Dónde:** `02:186–188` y la subsección `02:225–256`.
- **Cambio de orden:** mover la subsección «Las memorias de dominio como lecturas de la heteroasociativa» (líneas 225–256, completa, con su ecuación `eq:marginal`) a continuación de «Registro heteroasociativo» (después de la línea 182), antes de «Proyección AND-ponderada».
- **Viejo (186–188):**
  ```latex
  Sea $\mathbf{a}$ una pista izquierda con pesos por dimensión $\mathbf{w}$
  (ecuación~\eqref{eq:pesos}), calculados sobre la lectura del dominio izquierdo de la
  propia memoria (ecuación~\eqref{eq:marginal}).
  ```
- **Nuevo (186–188):**
  ```latex
  Sea $\mathbf{a}$ una pista izquierda con pesos por dimensión $\mathbf{w}$, calculados
  con la ecuación~\eqref{eq:pesos} sobre la lectura $\mathbf{R}^{L}$ de la propia memoria
  (ecuación~\eqref{eq:marginal}).
  ```
- **Por qué:** la proyección usa una lectura y una ecuación que el lector encuentra dos subsecciones después. Con el nuevo orden van registro, lecturas, proyección y recuperación. El texto movido no cambia, salvo lo de 2.7.

### 1.9 Marco: el párrafo de $\iota$ y $\kappa$ usa $\Pi$ antes de definirla
- **Dónde:** `02:78–91` y un párrafo nuevo al final de «Proyección AND-ponderada» (después de la línea 223).
- **Viejo (78–91):**
  ```latex
  El parámetro $\kappa$ define un umbral de reconocimiento relativo: en la memoria
  homoasociativa se considera reconocido si el peso medio $\bar{w} \geq \kappa \cdot \bar{\mu}$,
  donde $\bar{\mu}$ es la media global de la memoria.
  La heteroasociativa de referencia define el criterio solo para un par de pistas; con
  una sola pista, este trabajo lo aplica a la proyección (Sección~\ref{sec:hetero4d}):
  compara la activación media por celda de $\Pi$, por coordenada de la pista, con
  $\kappa \cdot \bar{\mu}$ de la memoria de contenido.
  Ese es el $\kappa$ que barre la Sección~\ref{sec:param-iota-kappa}; el criterio
  homoasociativo no interviene: de las lecturas de dominio de la memoria de contenido
  (ecuación~\eqref{eq:marginal}) el sistema usa los pesos y no esa decisión.
  El parámetro $\iota$ controla la poda: en la \emph{relación operativa} de la memoria,
  cualquier celda con peso $< \iota \cdot (\text{suma}/\text{celdas no cero})$ se
  apaga temporalmente durante la recuperación, eliminando ruido estadístico de baja
  frecuencia sin modificar la relación acumulada $\mathbf{R}$.
  ```
- **Nuevo (78–91):**
  ```latex
  El parámetro $\iota$ controla la poda.
  Para cada característica $i$ se toma el peso medio de sus celdas no nulas,
  $\bar{r}_i = \sum_j \mathbf{R}[i,j] \,/\, |\{j : \mathbf{R}[i,j] > 0\}|$, y toda celda
  con $\mathbf{R}[i,j] < \iota\,\bar{r}_i$ se apaga al reconocer y al recuperar.
  La relación acumulada $\mathbf{R}$ no cambia: la poda quita los valores poco frecuentes
  solo de la \emph{relación operativa} con la que la memoria responde.

  El parámetro $\kappa$ fija un umbral de reconocimiento relativo: la memoria
  homoasociativa acepta la pista solo si, además de contenerla, el peso medio
  $\bar{w} = \frac{1}{n}\sum_i w_i$ alcanza $\kappa \cdot \bar{\mu}$, donde $\bar{\mu}$ es
  la media global de la memoria.
  De las lecturas de dominio de la memoria de contenido (ecuación~\eqref{eq:marginal}),
  este sistema usa los pesos y no esa decisión; el $\kappa$ que barre la
  Sección~\ref{sec:param-iota-kappa} actúa sobre la proyección heteroasociativa
  (Sección~\ref{sec:hetero4d}).
  ```
- **Nuevo (después de 223):**
  ```latex
  La memoria heteroasociativa de referencia define el umbral $\kappa$ solo para un par de
  pistas.
  Con una sola pista, este trabajo lo aplica a la proyección: compara la activación media
  por celda de $\Pi$, por coordenada de la pista, con $\kappa \cdot \bar{\mu}$ de la
  memoria de contenido.
  ```
- **Por qué:** es el párrafo más difícil del marco. Usa $\Pi$, la proyección y la ecuación marginal antes de que existan, no define $\bar{w}$ y no dice que la poda es por característica. Ahora la parte de $\kappa$ que es de este trabajo va donde $\Pi$ ya está definida.
- **Fuentes:**
  - Poda por característica: `src/hetero_lib/associative.py:313–322` (`mean = iota*s/count` sobre `relation[i, :]`).
  - «Al reconocer», además de al recuperar: `associative.py:229–231` (la prueba de contención usa la relación podada) y `hetero_associative_4d.py:443–458` (contención y proyección también la usan).
  - $\bar{w}$: `associative.py:202` (`kappa*self.mean <= np.mean(weights)`).

### 1.10 Marco: «entropía del directorio» nombra dos medidas
- **Dónde:** `02:304–313`
- **Viejo:**
  ```latex
  La \textbf{entropía del directorio} resume el estado del sistema transactivo.
  En el registro completo del grupo, la entropía máxima $\log_2 K$ (siendo $K$ el número
  de módulos; $\log_2 8 = 3$ bits con ocho módulos) indica especialización perfectamente
  balanceada, y una entropía baja, colapso hacia un solo módulo o formación incompleta.
  A diferencia de la entropía de una memoria de contenido, aquí el diagnóstico se hace
  sobre la \emph{distribución de registros entre módulos}, y en el registro completo el
  estado deseable es el máximo: que el grupo reparta la experticia de forma pareja.
  En el directorio de cada módulo no lo es: si cada uno registra lo que presenció, su
  directorio se carga hacia sí mismo y queda por debajo del máximo aunque el grupo esté
  balanceado.
  ```
- **Nuevo:**
  ```latex
  La \textbf{entropía del directorio} resume el estado del grupo.
  No es la entropía de una memoria (ecuación~\eqref{eq:entropia}): se calcula sobre la
  distribución de los registros entre módulos (ecuación~\eqref{eq:entropia-dir}).
  En el registro completo del grupo (el del mediador, o el directorio compartido de la
  calibración), el máximo $\log_2 K$ (con $K$ módulos; $\log_2 8 = 3$ bits) indica que la
  experticia está repartida de forma pareja, y una entropía baja indica colapso hacia un
  solo módulo o formación incompleta.
  En el directorio de cada módulo el máximo no es el estado deseable: como cada uno
  registra lo que presenció, su directorio se carga hacia sí mismo y queda por debajo del
  máximo aunque el grupo esté balanceado.
  ```
- **Por qué:** `02:132–134` dice que un directorio quiere entropía baja, y aquí que debe estar en el máximo. Son medidas distintas (la ecuación 6 contra `eq:entropia-dir`) y el texto no lo dice. También se ajustan otros detalles:
  - «Registro completo» queda definido, según `03:511–512`.
  - «En el directorio de cada módulo no lo es» deja de tener un antecedente dudoso.
  - Sale «perfectamente balanceada», según léxico y hechos E8.
  - La frase sin verbo de la línea 307 recupera el verbo, según forma.

### 1.11 Marco: qué asocia un directorio
- **Dónde:** `02:171–172`
- **Viejo:** `El presente sistema usa la EHAM como sustrato de asociación texto$\leftrightarrow$imagen` / `y como base para los directorios heteroasociativos módulo$\leftrightarrow$especialidad.`
- **Nuevo:**
  ```latex
  El presente sistema usa la EHAM para la memoria de contenido de cada módulo, que asocia
  texto e imagen en los dos sentidos, y para sus directorios, que asocian una pista (una
  palabra o una imagen) con la identidad del módulo que ganó la consulta.
  ```
- **Por qué:** el directorio no asocia un módulo con una especialidad, sino una pista con el módulo ganador (`03:57–58`). La idea equivocada la tiene que deshacer la Sección 3. Con este cambio también sobra el párrafo que claridad proponía agregar al final de 2.3 (M22).

---

## Parte 2. Claridad y estilo

### 2.1 Introducción: el párrafo del TME
- **Dónde:** `01:45–52`
- **Viejo:**
  ```latex
  Un mediador central denominado TME (\textit{Transactive Memory Expert}) coordina la fase
  temprana y registra en sus propios directorios qué módulo responde a cada tipo de
  consulta.
  Conforme cada módulo acumula en sus memorias de directorio internas (una textual y una
  visual) las transacciones en que participa, el TME deja de hacer falta: en la fase
  madura, cualquier módulo puede determinar, con su directorio y los de los módulos que
  conoce, a quién reenviar una consulta desconocida, sea una frase o una imagen, sin
  intervención del mediador.
  ```
- **Nuevo:**
  ```latex
  Cada módulo guarda las palabras y las imágenes de su categoría en una sola memoria de
  contenido y lleva dos directorios, uno textual y uno visual, donde anota las
  transacciones en que participa.
  Un mediador central denominado TME (\textit{Transactive Memory Expert}) coordina la fase
  temprana y registra en sus propios directorios qué módulo responde a cada tipo de
  consulta.
  Conforme se llenan los directorios de los módulos, el TME deja de hacer falta: en la fase
  madura los módulos se reenvían entre sí las consultas, sean frases o imágenes, sin
  intervención del mediador.
  ```
- **Por qué:** la segunda oración junta cuatro ideas, y «consulta desconocida» no dice para quién. Además, la memoria de contenido aparece por primera vez de golpe en la contribución 1. El detalle de cómo se reenvía queda en la contribución 3.

### 2.2 Contribución 1 (sobre el texto aprobado 2d)
- **Dónde:** `01:72–78`
- **Viejo (aprobado):**
  ```latex
      \item \textbf{Un sistema transactivo de ocho especialistas.}
      Ocho módulos, uno por cada clase de ETH-80, cada uno con una sola memoria de
      contenido heteroasociativa y dos directorios, evaluados con un banco de 411
      consultas ($\approx$50 por dominio).
      Los directorios, la lectura normalizada B1, el rechazo por containment y la
      coordinación punto a punto funcionan con los ocho dominios, con el registro por
      transacción y la coordinación de la contribución~3.
  ```
- **Nuevo:**
  ```latex
      \item \textbf{Un sistema transactivo de ocho especialistas.}
      Se construye un sistema de ocho módulos, uno por cada clase de ETH-80, cada uno con
      una sola memoria de contenido heteroasociativa y dos directorios, y se evalúa con un
      banco de 411 consultas ($\approx$50 por dominio).
      Los directorios, su lectura normalizada por número de registros (B1,
      Sección~\ref{sec:operaciones}), el rechazo de lo que ninguna memoria contiene y la
      coordinación punto a punto de la contribución~3 funcionan con los ocho dominios.
  ```
- **Por qué:** la primera oración no tiene verbo, B1 y «containment» no están definidos en la introducción, y «con el registro por transacción y la coordinación de la contribución 3» queda colgando. Antipatrones proponía resumir la lista en «la maquinaria transactiva». La conservo porque es su primera mención y dice qué funciona.

### 2.3 Contribución 2 (sobre el texto aprobado 2e con A6)
- **Dónde:** `01:80–86`
- **Viejo (aprobado con A6):**
  ```latex
      \item \textbf{Cuantización por magnitud de las pistas semánticas.}
      Las pistas fastText se cuantizan por magnitud, $v/S$ sobre una escala global
      persistida, y pueblan los 16 niveles; una binarización por signo usaría solo 2.
      Con esta representación, la precisión temprana sobre el banco de 411 consultas es del
      90.0\% (Sección~\ref{sec:calibracion}).
  ```
- **Nuevo:**
  ```latex
      \item \textbf{Cuantización por magnitud de las pistas semánticas.}
      Cada vector fastText se divide entre una escala global $S$, la misma en el llenado y
      en las consultas, se recorta a $[-1, 1]$ y se reparte en los 16 niveles
      (Sección~\ref{sec:pipeline-semantico}); una binarización por signo usaría solo 2.
      Con esta representación, la precisión temprana sobre el banco de 411 consultas es del
      90.0\% (Sección~\ref{sec:calibracion}).
  ```
- **Por qué:** «$v/S$» no se entiende sin definir $S$, y «persistida» es un calco de *persisted*. La descripción sale de `04:75–80`. La frase de A6 no cambia.

### 2.4 Contribución 5 (sobre el texto aprobado 2g)
- **Dónde:** `01:107–112`
- **Viejo (aprobado):**
  ```latex
      \item \textbf{Evaluación experimental.}
      Se reportan el estudio de calibración del directorio (9 condiciones $\times$
      $N \in \{50,100,200,400\}$ $\times$ 5 semillas), el barrido de parámetros nativos
      $\iota \times \kappa$, la curva de formación del directorio, la curva de capacidad
      de llenado, el hemisferio visual completo, la comparación con una sola EHAM y la
      verificación de una sola memoria de contenido por módulo, junto con el costo
      computacional de la reproducción íntegra.
  ```
- **Nuevo:**
  ```latex
      \item \textbf{Evaluación experimental.}
      Se miden nueve condiciones de lectura del directorio (con cuatro cantidades de
      consultas de formación y cinco semillas), el efecto de los parámetros nativos de la
      memoria ($\iota$ y $\kappa$), cuántas interacciones hacen falta para formar el
      directorio, cuánto contenido admite cada módulo, el comportamiento con imágenes, la
      comparación con una sola memoria para las ocho clases y la verificación de una sola
      memoria de contenido por módulo, junto con el costo computacional de reproducir
      todos los resultados.
  ```
- **Por qué:** es una lista de nombres internos ($N$, «hemisferio visual», EHAM, «curva de capacidad») que dice cómo se llama cada experimento y no qué mide. No se agrega ninguna cifra; se quitan los valores de $N$.

### 2.5 Introducción: estructura del documento
- **Dónde:** `01:117–127`
- **Viejo:**
  ```latex
  El documento se organiza de la siguiente manera.
  La Sección~\ref{sec:marco_teorico} presenta los fundamentos teóricos: la EAM de Pineda
  \& Morales y su variante ponderada, la memoria heteroasociativa 4D y el modelo de
  memoria transactiva de Wegner.
  La Sección~\ref{sec:arquitectura} describe en detalle la arquitectura EAM-TMS de ocho
  módulos, incluyendo los diagramas de flujo del llenado, la fase temprana y la fase
  madura, así como la formalización de todas las operaciones del sistema.
  La Sección~\ref{sec:metodologia} detalla la metodología experimental.
  La Sección~\ref{sec:resultados} reporta los resultados.
  La Sección~\ref{sec:discusion} discute los resultados.
  La Sección~\ref{sec:conclusiones} concluye y señala trabajo futuro.
  ```
- **Nuevo:**
  ```latex
  La Sección~\ref{sec:marco_teorico} presenta los fundamentos: la memoria asociativa
  entrópica de Pineda y Morales y su variante ponderada, su extensión heteroasociativa
  (EHAM) y el modelo de memoria transactiva de Wegner.
  La Sección~\ref{sec:arquitectura} describe la arquitectura EAM-TMS de ocho módulos, con
  los diagramas de flujo del llenado, la fase temprana y la fase madura, y la
  formalización de las operaciones del sistema.
  La Sección~\ref{sec:metodologia} detalla la metodología experimental, la
  Sección~\ref{sec:resultados} reporta los resultados, la Sección~\ref{sec:discusion} los
  discute y señala las limitaciones, y la Sección~\ref{sec:conclusiones} concluye y señala
  trabajo futuro.
  ```
- **Por qué:** junta las propuestas de tres revisores:
  - Cuatro frases idénticas de metatexto y una primera frase que repite el título de la subsección (antipatrones).
  - «Incluyendo» como preposición, más «en detalle» y «todas», que sobran (léxico).
  - «Memoria heteroasociativa 4D» frente al nombre que se define en 02, EHAM (consistencia).

### 2.6 Marco: «Esta variación» no tiene antecedente
- **Dónde:** `02:103–117`
- **Viejo:**
  ```latex
  El valor recuperado $\hat{a}_i$ se obtiene \textbf{muestreando} esta distribución:
  $\hat{a}_i \sim p_i(\cdot)$.
  Esta modulación gaussiana corresponde al mecanismo de recuperación vigente desde el
  trabajo de imaginería \cite{pineda2023imagery} (el artículo base de 2021 empleaba
  distribuciones triangulares, hoy superadas); es la versión implementada en el código de
  referencia que este sistema utiliza.

  Esta variación no es un error del modelo; es parte de cómo recuerda:
  \emph{recordar es muestrear}, no leer un valor determinista.
  Diferentes ejecuciones de $\beta$ sobre la misma pista y la misma memoria pueden producir
  resultados distintos.
  El parámetro $\sigma$ controla la dispersión del muestreo: …
  ```
- **Nuevo:** la oración «Esta modulación gaussiana…» (105–108) pasa al final del párrafo, después de «…falsas recolecciones \cite{pineda2023imagery}.» (línea 117), con el texto que deje la propuesta de referencias (A4), que la reescribe. Las líneas 110–113 quedan así:
  ```latex
  Por eso dos ejecuciones de $\beta$ sobre la misma pista y la misma memoria pueden dar
  resultados distintos; esa variación es parte de cómo recuerda la memoria:
  \emph{recordar es muestrear}, no leer un valor fijo.
  ```
  La línea en blanco 109 se quita: 103–104, las nuevas 110–113, 114–117 y la oración movida forman un solo párrafo.
- **Por qué:** «Esta variación» se lee como si hablara de la modulación gaussiana de la oración anterior. En realidad habla de que dos recuerdos difieren, y eso se dice después. Antipatrones señaló el mismo pasaje por el «no es X; es Y».

### 2.7 Marco: «centinelas», «borde» y «valor indefinido» son la misma cosa
- **Dónde:** `02:153–154` (una cláusula) y `02:229–242`
- **Viejo (153–154):** `donde los tamaños $(m+1)$ y $(q+1)$ incorporan \emph{centinelas} en la última posición` / `para representar funciones parciales (características no definidas).`
- **Nuevo (153–154):**
  ```latex
  donde los tamaños $(m+1)$ y $(q+1)$ reservan la última posición de cada alfabeto para
  un \emph{valor indefinido}, que representa características sin valor (funciones
  parciales); esas celdas forman el \emph{borde} del tensor.
  ```
  (La cláusula es idéntica en el texto de M1 de referencias, que cambia lo anterior de la oración; el reemplazo vale en los dos casos).
- **Viejo (229–242):**
  ```latex
  Cada registro de la ecuación~\eqref{eq:registro-hetero} suma una unidad en
  $(i, j, a_i, b_j)$ para \emph{todas} las coordenadas $j$ del otro dominio; fijada
  cualquier $j$, sumar sobre sus valores cuenta cuántas veces se registró cada valor en
  cada característica:
  \begin{equation}
      …
  \end{equation}
  descontando el 1 con que arranca el borde.
  El índice $l = q$ (o $k = m$) es el valor indefinido que la memoria reserva para
  funciones parciales: lo que llega sin pareja (una imagen sin palabra, una palabra sin
  imagen) se registra ahí y entra en la suma.
  ```
- **Nuevo (229–242;** la ecuación no cambia, salvo la coma final, que pasa a punto):
  ```latex
  Cada registro de la ecuación~\eqref{eq:registro-hetero} suma una unidad en
  $(i, j, a_i, b_j)$ para \emph{todas} las coordenadas $j$ del otro dominio.
  Por eso, fijada cualquier $j$, sumar sobre los valores $l$ del otro dominio cuenta
  cuántas veces se registró cada valor $k$ en cada característica $i$, sea cual sea la $j$
  elegida:
  \begin{equation}
      …
  \end{equation}
  El índice $l = q$ (o $k = m$) es el valor indefinido, el borde: lo que llega sin pareja
  (una imagen sin palabra, una palabra sin imagen) se registra ahí y entra en la suma.
  Las celdas del borde arrancan en 1, y la lectura descuenta ese 1.
  ```
- **Por qué:** el lector no sabe que los tres nombres son lo mismo, y llega a «descontando el 1 con que arranca el borde» antes de saber qué es el borde. «Centinela» es jerga de programación. **Fuente:** `hetero_associative_4d.py:690–699` (`_set_margins` pone el borde en 1) y `src/associative_memory.py:169` (`- 1  # el borde arranca en 1`).

### 2.8 Marco: el aparte sobre `recog_weights`
- **Dónde:** `02:69–76`
- **Viejo:**
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
- **Nuevo:**
  ```latex
  En las definiciones formales de las fuentes, $\eta$ devuelve solo aceptar o rechazar, y
  los $w_i$ son cantidades intermedias de esa prueba; la implementación de referencia de
  Pineda y Morales los devuelve (\texttt{recog\_weights}), y este trabajo los usa para
  ponderar la proyección de la memoria heteroasociativa (Sección~\ref{sec:hetero4d}).
  ```
- **Por qué:** junta tres revisores: el metatexto «Una precisión de notación:» y la moraleja «de empaquetado, no de sustancia» (antipatrones), y los calcos «de primera clase» y «empaquetado» (léxico).

### 2.9 Marco: la atribución de `project()`
- **Dónde:** `02:210–215`
- **Viejo:**
  ```latex
  Sobre la atribución de esta regla: el nombre ``proyección AND-ponderada'' es de este
  trabajo, pero el mecanismo no es una síntesis propia; es exactamente la operación
  \texttt{project()} de la implementación de referencia de Pineda \& Morales (que este
  sistema incorpora sin modificaciones), donde la anulación conjuntiva y la suma ponderada
  por pesos normalizados son líneas literales de esa única función, operando sobre la
  relación ya podada por $\iota$.
  ```
- **Nuevo** (las líneas 216–219 siguen igual):
  ```latex
  El nombre ``proyección AND-ponderada'' es de este trabajo; el mecanismo no.
  Es la operación \texttt{project()} de la implementación de referencia de Pineda y
  Morales, que este sistema incorpora sin modificaciones: la anulación conjuntiva y la suma
  ponderada por pesos normalizados son líneas de esa función, aplicadas sobre la relación
  ya podada por $\iota$.
  ```
- **Por qué:** junta tres revisores: el metatexto «Sobre la atribución:», el «no es…; es exactamente» y «líneas literales de esa única función» (antipatrones y léxico), y el «\&» (forma).

### 2.10 Cambios pequeños

| Dónde | Viejo | Nuevo | Por qué |
|---|---|---|---|
| `01:13` | `El sistema funciona gracias a esa especialización` | `El grupo funciona gracias a esa especialización` | Habla del grupo humano; «el sistema» se lee como el computacional, que aún no aparece. |
| `01:54–56` | `El sistema no emplea ningún mecanismo de optimización numérica en la toma de decisiones.` / `Todas las operaciones (registro, reconocimiento, recuperación y enrutamiento) son` / `operaciones definidas formalmente sobre las \textbf{Memorias Asociativas Entrópicas}` | `Ninguna decisión del sistema sale de un clasificador entrenado ni de una optimización` / `numérica: registrar, reconocer, recuperar y enrutar son operaciones definidas` / `formalmente sobre las Memorias Asociativas Entrópicas` | Se alinea con la pregunta («sin clasificadores supervisados»). Quita la repetición «operaciones … son operaciones» y la negrita de énfasis. |
| `01:99–105` (texto aprobado 2f) | `el vocabulario no` / `contiene vectores sintéticos, el código de Pineda \& Morales permanece byte-idéntico` / `(salvo una guarda que evita` | `el vocabulario no` / `contiene vectores sintéticos (de relleno, para etiquetas sin vector fastText), el código de Pineda y Morales permanece idéntico byte a byte` / `(salvo una condición que evita` | «Guarda» y «byte-idéntico» son calcos. «Vectores sintéticos» no se entiende sin la auditoría (`04:212–214`). |
| `02:9` | `Una \textbf{pista} es una función discreta` | `Una \textbf{pista}, lo que se presenta a la memoria para registrarlo o para preguntar por él, es una función discreta` | Dice para qué sirve la pista. |
| `02:15` | `una función característica $R : A \times V \to \{0, 1\}$ y el registro se realiza por` | `una función característica $R : A \times V \to \{0, 1\}$, sobre características ($A$) y valores ($V$), y el registro se realiza por` | $A$ y $V$ no se definen. (Las líneas 17–20 las toca A1 de referencias). |
| `02:24–25` | `Esta distinción importa para el lector que verifique contra las fuentes: las` / `definiciones que siguen corresponden a la variante ponderada, no a la booleana de 2021.` | `Las definiciones que siguen corresponden a la variante ponderada, no a la booleana de 2021.` | Metatexto dirigido al lector. |
| `02:43–44` | `La idea central es esta: la memoria \emph{no almacena` / `patrones individuales} sino que acumula una \textbf{distribución de experiencias}.` | `La memoria no almacena patrones individuales: acumula una` / `\textbf{distribución de experiencias}.` | Anuncio con dos puntos y doble énfasis. |
| `02:45–46` | `Cada columna $\mathbf{R}[i, \cdot]$ se convierte progresivamente en una distribución de` | `Cada vector $\mathbf{R}[i, \cdot]$ (la \emph{columna} de la característica $i$, como la llaman las fuentes) se convierte progresivamente en una distribución de` | Con $\mathbf{R} \in \mathbb{N}^{n \times m}$, $\mathbf{R}[i,\cdot]$ es una fila. «Columna» es el uso de las fuentes y del código (`associative.py:313–316`), y se usa en todo el marco. |
| `02:58–59` | (tras la ecuación) `Es una \emph{implicación material relajada}: la pista se acepta si cada una de sus` | `donde $\mathbf{1}[\cdot]$ vale 1 si la condición se cumple y 0 si no.` / `Es una \emph{implicación material relajada}: la pista se acepta si cada una de sus` | $\mathbf{1}[\cdot]$ no se define. |
| `02:128–130` | `Conviene precisar que la entropía baja \emph{no} es intrínsecamente patológica: en las` / `fuentes, una función totalmente determinada tiene entropía exactamente cero y es una` / `memoria perfectamente bien formada, solo que rígida y reproductiva` | `La entropía baja \emph{no} es un defecto por sí misma: en las` / `fuentes, una función totalmente determinada tiene entropía cero y es una` / `memoria bien formada, solo que rígida y reproductiva` | Muletilla, metáfora médica y dos absolutos (léxico y antipatrones). |
| `02:132–134` | `sin ambigüedad a un especialista \emph{quiere} baja ambigüedad, mientras que una memoria` / `de contenido que debe generalizar quiere un rango medio.` | `sin ambigüedad a un especialista necesita entropía baja, y una memoria` / `de contenido que debe generalizar, un rango medio.` | «Quiere» personifica, y «ambigüedad» se repite en la misma oración (antipatrones y forma). |
| `02:136–137` | `baja entropía da precisión alta` / `con recall bajo` | `baja entropía da precisión alta` / `con exhaustividad (\textit{recall}) baja` | Aquí *recall* es la métrica y no la operación $\beta$. «Cobertura», que proponía claridad, ya significa otra cosa en la tesis («cobertura de punta a punta»). |
| `02:139` | `\subsection{Memoria Heteroasociativa 4D}` | `\subsection{Memoria Heteroasociativa Entrópica}` | El título no coincide con el nombre que define `02:142`. La etiqueta `sec:hetero4d` se queda. |
| `02:163–164` | `el plano queda` / `ampliamente indeterminado` | `el plano queda` / `en gran parte indeterminado` | Calco de *largely*. |
| `02:253` | `las memorias autoasociativas se llenan aparte` | `las memorias homoasociativas se llenan aparte` | Es el único «autoasociativa» de la tesis; en el resto se dice «homoasociativa». |
| `02:255` | `leer esos pesos de la hetero deja las` | `leer esos pesos de la heteroasociativa deja las` | «La hetero» no está presentada como abreviatura en este punto. |
| `02:267` | `Cabe señalar que este puente entre la teoría de Wegner y las memorias asociativas` | `Este puente entre la teoría de Wegner y las memorias asociativas` | Muletilla. |

---

## Parte 3. Términos (decisión T)

Solo los sitios de mis tres archivos, sobre el texto que resulta del replanteamiento y los hechos.

| Línea | Viejo | Nuevo |
|---|---|---|
| `01:60` | `embeddings fastText` | `vectores de palabras fastText` |
| `01:64` (texto de hechos B1) | `el encoder de un autoencoder ResNet18` | `el codificador de un autocodificador ResNet18` |
| `01:77` (texto aprobado 2d) | `el rechazo por containment` | `el rechazo por contención` (solo si no se toma 2.2, que ya lo quita) |
| `01:99` (texto aprobado 2f) | `\item \textbf{Auditoría de fidelidad del pipeline.}` | `\item \textbf{Auditoría de fidelidad.}` (como se titula 4.6) |
| `02:205` | `Esto implementa \emph{containment} estricto:` | `Esto implementa una \emph{contención} estricta (\textit{containment}):` |

---

## Parte 4. Forma

| Dónde | Viejo | Nuevo | Tipo |
|---|---|---|---|
| `02:1` | `\section{Marco Teórico}` | `\section{Marco teórico}` | Mayúscula en título. El resto de los títulos de la tesis lleva mayúscula solo en la inicial. |
| `02:258` | `\subsection{Memoria Transactiva}` | `\subsection{Memoria transactiva}` | Igual. `06:93` escribe «memoria transactiva». |
| `01:57`, `02:72`, `02:212` y la contribución 4 aprobada (2f) | `Pineda \& Morales` | `Pineda y Morales` | «\&» en prosa española. `02:72` y `02:212` ya van con «y» si se aprueban 2.8 y 2.9. En `01:57`, la propuesta de referencias (B6) sugiere «Pineda y colaboradores». |
| `main:72`, línea del texto aprobado del resumen: «de la Memoria Transactiva» | `Memoria Transactiva` | `memoria transactiva` | Mayúscula inconsistente (`01:8`, `02:261`). Solo si no se toma 1.2, que ya lo resuelve. |
| `main:63–64` y `main:78` (líneas del resumen aprobado), `01:43–44` | `\textit{apple}`, … | `\texttt{apple}`, … | Nombres de clase: el resto de la tesis usa `\texttt` (71 contra 24, según consistencia). Conviene aprobarlo junto con el resto de la tesis. |
| `main:48` | `Gabriel Gonzalez` | `Gabriel González` | Confirmar: solo si tu apellido lleva tilde. |

---

## Descartado

- **Claridad M5** (`01:54–65` reescrito completo): tomé solo la primera frase (2.10). El resto ya lo cubren T (`embeddings`, `encoder`), hechos B1 (ImageNet) y referencias B6 (autoría).
- **Claridad M10** (reordenar la definición de W-EAM, `02:14–25`): las líneas 17–20 las reescribe referencias A1 por una cita equivocada, y M10 la copiaba. Tomé solo la glosa de $A$ y $V$ y el corte del metatexto.
- **Claridad M11 y consistencia 4.5** (tope $w$ que choca con $w_i$): referencias M7 reescribe esa oración y conserva $w$, el símbolo del artículo. Si se aplica, conviene escribir el tope como $w_{\max}$.
- **Claridad M19** (containment → contención): va en la Parte 3.
- **Claridad M22** (agregar al final de 2.3 cómo se materializa el directorio): lo cubre 1.11.
- **Claridad M23 y B11** (decir que el sistema no usa los métodos de la pista faltante): es falso según el código. Los reemplaza 1.7.
- **Claridad M24, claridad B2 (fases) y antipatrones `01:16–24`**: la atribución del mediador, las fases y el rechazo a Wegner la corrige referencias M5 en `01:23`, `02:284`, `02:292` y `02:297`, y referencias A3 cambia la cita de `01:16`. La compresión del párrafo de los tres procesos es de gusto.
- **Claridad B4** («EAM, por sus siglas en inglés»): de gusto. Tomé solo la glosa de «pista».
- **Claridad B7** («cuando se dispone de la pista»): agregaría una afirmación que el revisor no verificó (su duda D7).
- **Claridad B12** («metadirectorio» → «directorio»): consistencia 1.7 lo deja porque es la paráfrasis de Wegner, que lo explica.
- **Claridad B13** (`02:247–250`, la frase del módulo de un solo dominio): no estorba la lectura.
- **Claridad M1, en su versión original**: la rehíce sobre el texto con A1 (1.2). Además decía «los módulos leen sus directorios», y la calibración usa un directorio compartido. También quitaba «bidireccionalmente», «300» y «por magnitud», que se quedan.
- **Claridad B15** («datos no fabricados» → «datos reales»): «no fabricados» es más preciso. Tomé el resto (2.10).
- **Antipatrones `01:76–78`** (j2, «la maquinaria transactiva» en vez de la lista): ver 2.2.
- **Antipatrones `02:203–206`** (fundir dos frases de la conjunción): de gusto; la oración entra en la Parte 3.
- **Antipatrones `02:81–87`** (partir oraciones): lo reemplaza 1.9.
- **Antipatrones `02:304–313`** (versión corta): no separa las dos medidas de entropía; tomé 1.10.
- **Antipatrones `main:83–85`**: sin cambio, como propone el revisor.
- **Léxico `main:81–82`** («perfectamente balanceado»): la frase desaparece con el replanteamiento.
- **Léxico `02:167–170`** («Conviene ubicarlo», «parche») **y antipatrones del mismo pasaje**: lo reemplaza 1.7.
- **Léxico `02:271`** («fundamentales»): referencias A3 reescribe esa oración.
- **Consistencia 4.2** ($k$ → $u$ en `eq:marginal`): cambiaría una ecuación; la confusión con el índice de módulo de la Sección 3 es menor.
- **Consistencia 4.5** ($\mathbf{R}^L$ frente a $M^L$): el pie de `tab:memorias` (03) ya los liga con `eq:marginal`.
- **Consistencia 7.4 y forma `main:58`** («Memorias Asociativas Entrópicas» en minúscula): es el nombre del modelo, con sigla, y forma 02 lo acepta. Solo bajo «Memoria Transactiva».
- **Consistencia 7.2 y 7.6, y forma `main:82`** («3.000» como separador de miles; `\,\%`): falsos positivos, o decisiones que se toman con la plantilla de la UACJ.
- **Forma `main:49`** («Julio 2026»): la fecha se pone después. Al ponerla, va «julio de 2026».
- **Forma 01** (cifras o palabras: «3 a 8», «2 de los 16», «8 clases»): casi todas desaparecen con el replanteamiento; el resto es criterio.
- **Forma 02** («miembro» en la parte de Wegner, «computan»): «miembro» es el vocabulario de Wegner para el grupo humano, y «computan» es correcto.
