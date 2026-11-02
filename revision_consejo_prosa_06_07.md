# Propuesta viejo/nuevo: 06 Discusión y 07 Conclusiones (consejo de redacción)

**Estado:** pendiente de aprobación. Nada aplicado.

Todo va escrito sobre el texto que resulta de aplicar el replanteamiento aprobado y la propuesta de hechos (A2–A5, E10, E12, F1–F7, G1–G3); cuando un pasaje cambia con ellos, el «Viejo» cita ese texto y lo marca. Lo que más pesa: **(1)** las limitaciones se reordenan: la (b) se parte en dos (cobertura y entradas degeneradas) y las letras corren una; el experimento 15 se queda en (a), más corto, porque llevarlo a 05 obligaría a escribir un resultado nuevo ahí; la limitación de la partición (hoy (e), después (f)) queda como interpretación y remite a la subsección nueva de 05. **(2)** El trabajo futuro sale de las limitaciones (cuatro puntos, con «reconocer sin nombrar» y la partición de validación). **(3)** Los vínculos con Wegner y la psicología se atan a cifras concretas, y el tercer punto de 6.4 usa el proceso de Wegner que la tesis define para consultas (coordinación de la recuperación, no asignación). Hay además un error de hecho que la propuesta de hechos no cubre, en la limitación (b): los cinco falsos de contenido no son «el par animal que ya confunde al texto» (cuatro los acepta `dog`).

**Dependencias.**
- La limitación (f) nueva usa `\ref{sec:objetos-nuevos}`, que crea el consolidador de 05. Si esa subsección no se aprueba, la (f) se queda como está hoy (con los cambios de léxico de la Parte 2). En `04:27`, «(experimento 16, Sección~\ref{sec:limitaciones})» debería pasar a «(Sección~\ref{sec:objetos-nuevos})»: es de 04.
- Decisión D2 (identidad `horse7`): si eliges D2(a), en la limitación (b) nueva se quita el paréntesis «(dos vistas de \texttt{horse7} a \texttt{dog}, que las contiene, así que la doble compuerta no las detiene)», y en 07 «ambos, vistas del mismo objeto hacia la clase vecina». En 6.1 y 6.4 ya no lo digo.
- Con estos textos, el cambio E10 en `06:243` sobra (la frase del 97.4 % sale de (b)), y la nota de F7 sobre `06:25` («con el ajuste A2 la frase desaparece») no se cumple: A2 no toca esa frase. La resuelvo en 1.5.

---

## Parte 1. Reglas y estructura

### 1.1 Limitación (a): más corta, con el experimento 15 dentro

- **Dónde:** `06:212–230`.
- **Viejo:** desde «\paragraph{(a) Fuga de consultas fuera de dominio en el hemisferio textual.}» hasta «(1.2 con $\delta = 0.05$, 8 con $\delta = 0.5$). La doble compuerta se queda como está.»
- **Nuevo:**
```latex
\paragraph{(a) Fuga de consultas fuera de dominio en el hemisferio textual.}
Una consulta fuera de dominio que comparte tokens con etiquetas legítimas pasa el
containment textual y llega a algún módulo: la sonda de rechazo deja pasar 2 de 12
(Sección~\ref{sec:proto-completo}), y en el banco de 40 de la comparación con la EHAM
única el directorio acepta 4, dos de ellas (\emph{piano}, \emph{thunderstorm}) hacia un
módulo que no las contiene.
La doble compuerta de contenido (el destino debe contener la consulta, no solo figurar
en el directorio) detiene esas dos y deja al protocolo en 2 de 40 en los cuatro cortes,
tantas como el oráculo; sobre las 171 consultas reservadas no quita ninguna respuesta,
porque las que rechaza (1.5\,\% con 200 imágenes por clase, 2.1\,\% con 25) eran
enrutamientos equivocados que el destino tampoco respondía.
Las dos que quedan las contiene el destino, y ninguna compuerta de containment las
separa de una consulta legítima.
Las alternativas medidas rinden menos (experimento 15, sobre las 171 reservadas): que el
contenido decida entre los tres mejores candidatos del directorio baja el acierto de
96.8 a 93.6\,\%, porque el índice calibrado compara mejor que la activación del
contenido, y abstenerse cuando la diferencia relativa entre las dos mejores
puntuaciones es menor que un umbral $\delta$ quita más de un acierto por cada error
evitado (1.2 con $\delta = 0.05$; 8 con $\delta = 0.5$).
```
- **Por qué:** dice cuál es la limitación y qué queda después de la compuerta; define $\delta$ (no estaba definido en ninguna parte); «las mismas que el oráculo» pasa a «tantas como», porque solo el conteo está verificado; sale «sin rechazar ninguna de las 16 consultas de referencia», que solo consta en un log y que las 171 reservadas dicen con más fuerza.
- **Para 05 (no lo propongo):** si se quisiera el experimento 15 en 05, irían las dos alternativas al final de `sec:eham-unica` y aquí quedarían las tres primeras frases. Es un resultado que hoy no está en 05. Cifras: `results/experimento15/README.md` (argmax 96.8, árbitro 93.6; curva de δ: 0.05 → −1.2 aciertos / −1.0 errores; 0.5 → −20.9 / −2.6); `results/experimento11/compuerta_reservadas.md` (2.05 % con 25, 1.52 % con 200, 0 respuestas perdidas).

### 1.2 Limitación (b) partida en (b) y (c); las letras siguientes corren una

- **Dónde:** `06:232–270` (un solo párrafo de 39 líneas).
- **Viejo:** desde «\paragraph{(b) Cobertura visual residual limitada por el containment conjunto.}» hasta «cuesta cuatro aciertos de test.» (con F6 aplicado en `06:256–258`).
- **Nuevo:**
```latex
\paragraph{(b) Cobertura visual limitada por la lectura estricta.}
La lectura del directorio visual es estricta ($\xi = 0$): con directorios
perspectivales, los huecos tolerados dependerían de lo que presenció cada módulo.
Para cubrir más, el sistema densifica.
El directorio visual y la recuperación de la heteroasociativa son dos compuertas, y
cada una cede solo con sus propias variantes (experimento 13, sobre las 656 imágenes de
prueba): registrar en el directorio 16 variantes por percepción, en lugar de una, lleva
su aceptación de 73.6 a 96.2\,\%; llenar el contenido con 16 variantes por imagen, en
lugar de 4, lleva la respuesta de la heteroasociativa de 76 a 96\,\%; con las dos, la
cobertura de punta a punta (enrutamiento correcto y respuesta) pasa de 66.5 a
94.5\,\%, con rendimiento decreciente por escalón de variantes.
El sistema usa 16 variantes en las dos y aun así rechaza el 3.5\,\% de las imágenes de
prueba (Sección~\ref{sec:hemisferio-visual}).
Densificar tiene un costo: dos enrutamientos equivocados de 656 (dos vistas de
\texttt{horse7} a \texttt{dog}, que las contiene, así que la doble compuerta no las
detiene) y, en el experimento, cinco imágenes aceptadas por un especialista ajeno,
todas entre animales y cuatro de ellas por \texttt{dog}.
Son vistas nuevas de los mismos objetos, porque la partición es por imagen
(limitación (f)).

\paragraph{(c) Fuga con entradas degeneradas.}
El contenido visual da soporte también a entradas sin estructura, como un lienzo gris
uniforme, porque el encoder las lleva a latentes de norma baja que caen dentro de la
envolvente de los animales (Sección~\ref{sec:hemisferio-visual}); las sondas
estructuradas (ruido, píxeles barajados) sí se rechazan.
Densificar agranda esa fuga: en el experimento 13, con 16 variantes, a la sonda de color
sólido la aceptan tres especialistas en vez de uno y el directorio la enruta.
El umbral de energía (Sección~\ref{sec:percepcion}) cierra el 90\,\% de la fuga
(experimento 14): 137 de las 152 entradas degeneradas aceptadas por una clase ajena caen
bajo $\tau$ (grises de 104 a 168, contrastes $\leq 0.2$ y desenfoques fuertes: todos
los de radio $\geq 12$ y buena parte de los menores).
Como criterio, la norma y la varianza del latente son equivalentes; la varianza de
píxeles no sirve, porque un objeto desenfocado conserva contraste y pierde estructura.
De las 15 entradas que sobreviven, 11 son objetos desenfocados o de bajo contraste que
acepta otra clase (como un \texttt{dog} desenfocado aceptado por \texttt{cow}) y cuatro
son superficies casi uniformes de norma alta (un gris claro, dos colores sólidos y un
gris con ruido); la doble compuerta del punto (a) no las cerraría, porque el contenido
también las acepta.
El umbral cuesta cinco imágenes reales de 3280, todas vistas oscuras de \texttt{cow}:
una percepción de la fase A y cuatro imágenes de prueba que el directorio enrutaba bien
y su contenido aceptaba.
```
- **Por qué:** un párrafo con tres asuntos y el costo de $\tau$ dicho dos veces («No es gratis», «cuesta cuatro aciertos»); sale la frase que repetía 05 («el ruteo de test queda en 96.2 %, la evocación en 97.4 %…»); «presumiblemente porque el fondo liso» contradecía a `05:350–353`, que da la causa medida; el valor de $\tau$ (16.6 aquí, 16.61 en 03–05) se remite a 04.
- **Error de hecho (no está en la propuesta de hechos):** «siempre el par animal que ya confunde al texto» no se cumple: de los cinco falsos de contenido, cuatro los acepta `dog` (cow → dog 2, horse → dog 2) y uno `cow`; en texto la confusión animal es `horse` → `cow`. Fuente: `results/experimento13/raw/Vc16_N200_Vd16_s42.json` («ajenos»: dog 4, cow 1); `ablation_metrics.csv`, B1, `cm_horse_cow` 6.
- **Cifras nuevas en el texto:** «en lugar de una» y «en lugar de 4» salen de `results/experimento13/README.md` (A0/A1: Vd 1 → 16, 73.6 → 96.2; A2: Vc 4 → 16, responde 76.2 → 96.2), como en E9.
- **Renumeración:** (c) Calidad de la reconstrucción → (d); (d) Aprendizaje → (e); (e) Partición → (f); (f) Selección → (g); (g) Regla de admisión → (h); (h) Fuente de conocimiento (la de F2) → (i); (i) Fragilidad del nombre → (j). Las referencias por letra están solo en 06 («limitación (b)» en 6.6 y «punto (a)» en la nueva (c), que no cambian) y en los textos nuevos de esta propuesta, que ya usan las letras nuevas.
- **Para 05 (no lo propongo):** del experimento 14, 05 tiene la causa y los grises; el 137 de 152, los 15 que sobreviven y la comparación norma/varianza solo están aquí. Llevarlos a 05 sería escribir resultados nuevos.

### 1.3 Limitación (f) (hoy (e)): interpretación que remite a 05

- **Dónde:** `06:288–310`.
- **Viejo:** desde «\paragraph{(e) Partición a nivel de imagen.}» hasta «fotos de otro origen son otra pregunta.»
- **Nuevo:**
```latex
\paragraph{(f) Partición por imagen.}
La partición entre entrenamiento y prueba separa archivos de imagen, no objetos
físicos: los diez objetos de cada clase aportan vistas a ambos lados
(Sección~\ref{sec:dataset}).
Las cifras visuales principales (96.2\% de enrutamiento, evocación de dominio) miden por
tanto generalización a \emph{vistas nuevas de objetos conocidos}.
Con objetos nuevos, la cobertura de punta a punta baja del 95.5 al 89.2\,\%
(Sección~\ref{sec:objetos-nuevos}), y lo que se pierde es respuesta, no acierto: la
envolvente por coordenada cubre a la mayoría de los objetos que no contribuyeron a ella,
rechaza las vistas que no cubre en lugar de enviarlas a otra clase, y la brecha se
concentra en unos pocos objetos, no en clases.
Con diez objetos por clase, ``objeto nuevo'' sigue siendo un objeto de la misma
colección fotografiado en las mismas condiciones; fotos de otro origen son otra
pregunta.
```
- **Por qué:** el 89.2 % pasa a su subsección de 05 (consolidador de 05) y la limitación queda como interpretación; quita además la repetición de `04:16–25`, «a nivel de» ×3, «train/test», «este reporte» y las comillas «» (la tesis usa ``…''). Cifras: las de `06:298–307` (95.5, 89.2; 99.9 % de acierto sobre aceptadas; 71 de 80 objetos; nueve concentran el 57 %).

### 1.4 Limitación (e) (hoy (d)): el proceso de Wegner con el nombre que define la tesis

- **Dónde:** `06:285–286`.
- **Viejo:** «El sistema aún no modela \emph{transactive encoding} ni la reorganización de memorias de contenido durante la operación madura.»
- **Nuevo:** «El sistema aún no modela la asignación de información de Wegner (encaminar información nueva al especialista que corresponde) ni la reorganización de las memorias de contenido durante la operación madura.»
- **Por qué:** «transactive encoding» no se define en la tesis; 02:281–283 llama «asignación de información» a ese proceso.

### 1.5 Apertura de la discusión (6.1)

- **Dónde:** `06:8–25` (texto del replanteamiento §4a con A2, más `06:23–25`, que el replanteamiento deja igual).
- **Viejo (resultante):**
```latex
El resultado central es una separación limpia de responsabilidades.
Con ocho dominios, los componentes de la maquinaria transactiva (los directorios
heteroasociativos, la lectura B1, el rechazo por containment, la actualización
perspectival del directorio y la coordinación punto a punto) funcionan sin ajustes por
dominio, y el registro completo de percepciones de la fase A queda balanceado (3.000
bits, el máximo con ocho módulos), mientras los directorios visuales de los módulos
rutean la fase B con dos falsos enrutamientos en 656.
Los límites aparecen en la \emph{representación}.
Una binarización por signo usaría 2 de los 16 niveles del alfabeto; la cuantización por
magnitud sobre una escala global (Sección~\ref{sec:pipeline-semantico}) los puebla
todos, y con ella la precisión temprana es del 90.0\% \emph{sin tocar una línea de la
maquinaria asociativa}.
La Figura~\ref{fig:espacio-semantico} muestra el espacio semántico resultante: los
solapamientos entre dominios persisten (son propiedades del léxico), pero la
representación ya no los agrava.
```
- **Nuevo:**
```latex
El resultado central separa dos responsabilidades: la maquinaria transactiva funciona
con ocho dominios, y los límites aparecen en la \emph{representación}.
Los componentes de la maquinaria (los directorios heteroasociativos, la lectura B1, el
rechazo por containment, la actualización perspectival del directorio y la
coordinación punto a punto) funcionan sin ajustes por dominio.
En imagen, el registro completo de percepciones de la fase A queda balanceado
(3.000 bits, el máximo con ocho módulos), y los directorios visuales de los módulos
enrutan las imágenes de prueba con dos falsos enrutamientos en 656
(Sección~\ref{sec:hemisferio-visual}).
En texto, las pistas se cuantizan por magnitud sobre una escala global
(Sección~\ref{sec:pipeline-semantico}), que puebla los 16 niveles del alfabeto (una
binarización por signo usaría 2), y con esa representación la precisión temprana sobre
el banco de 411 consultas es del 90.0\%.
Lo que la representación no quita es el solapamiento entre dominios: la
Figura~\ref{fig:espacio-semantico} muestra que persiste, porque es propiedad del léxico
(tres frutas, tres animales), y en él cae la mayoría de los errores que quedan
(Sección~\ref{sec:disc-dominancia}).
```
- **Por qué:** «ya no los agrava» es historia; «sin tocar una línea de la maquinaria» atribuye el 90.0 % a la cuantización sin corrida que lo aísle (mismo motivo que A6 en 01); el lector sabe desde la primera frase qué dos responsabilidades se separan; sale «limpia». Fuente de «la mayoría»: `ablation_metrics.csv`, B1, N = 400: 18 de 28 errores entre frutas y 6 `horse` → `cow`.

### 1.6 Lectura desde Wegner (6.4): cada punto atado a su resultado

- **Dónde:** `06:96–134` (texto del replanteamiento §4c con A3, F2 y F3).
- **Viejo:** la introducción «Los resultados de las Secciones~\ref{sec:calibracion} y~\ref{sec:formacion} releen los mecanismos de Wegner~\cite{wegner1987transactive} con un grupo de ocho miembros:» y los cuerpos del segundo, tercero y cuarto punto (el primero queda como lo dejan §4c y A3).
- **Nuevo** (bloque completo):
```latex
Los resultados de las Secciones~\ref{sec:calibracion}, \ref{sec:formacion},
\ref{sec:capacidad} y~\ref{sec:hemisferio-visual} releen los mecanismos de
Wegner~\cite{wegner1987transactive} con un grupo de ocho miembros:

\begin{itemize}
    \item \textbf{Conocerse cuesta interacción.}
    Con ocho módulos, 10 consultas por dominio dejan la precisión madura en 81.2\%, y
    hace falta el banco completo ($\approx$50 por dominio) para alcanzar el 93.0\%.
    Los errores que quedan caen dentro de pares de módulos que comparten léxico, como
    muestra el punto sobre la comunicación distintiva.

    \item \textbf{El orden de las experiencias afecta la velocidad, no el destino.}
    Todas las condiciones de presentación convergen al mismo directorio: mismos
    conteos, misma entropía.
    En el modelo de Wegner, el directorio se forma anotando quién respondió en cada
    interacción presenciada; aquí cada anotación se suma a las anteriores, así que el
    directorio final depende de \emph{qué} se presenció, y el orden solo decide cuándo
    se vuelve utilizable.

    \item \textbf{La comunicación distintiva forma mejor directorio.}
    Con la lectura B1, \texttt{car}, \texttt{cow}, \texttt{cup} y \texttt{tomato}
    quedan en 98--100\% y \texttt{dog} en 93.9\%; \texttt{pear} (76\%), \texttt{horse}
    (88\%) y \texttt{apple} (88.2\%) pierden hacia la vecina con la que comparten
    etiquetas (Sección~\ref{sec:disc-dominancia}).
    En términos de Wegner, la coordinación de la recuperación funciona en la medida en
    que quien pregunta aporta las señas del dominio: la regla de rescate léxico, que
    solo admite tokens de la consulta como \textit{bark}, \textit{moo} o
    \textit{riding}, sube 21.7 puntos en las 46 consultas que toca
    (Sección~\ref{sec:pipeline-semantico}).

    \item \textbf{El rechazo colectivo se sostiene con ocho dominios.}
    Con siete clases contrarias por módulo, el contenido no acepta ningún falso con un
    latente por imagen, en ninguno de los tamaños de llenado probados, y con las 16
    variantes del experimento 13 acepta 5 de 656 imágenes de prueba, todas entre
    animales (vacas y caballos aceptados por \texttt{dog}, un caballo por
    \texttt{cow}).
    El directorio visual comete dos falsos enrutamientos de 656, hacia una clase vecina.
    Es el rechazo claro de la Sección~\ref{sec:tmt}: lo que ningún módulo reconoce no se
    responde, y los errores que quedan caen en clases vecinas.
\end{itemize}
```
- **Por qué:** la introducción solo citaba dos de las cuatro secciones que interpreta; el segundo punto repetía 05 sin decir qué tiene que ver con Wegner y ahora lo dice (la actualización del directorio es una suma); el tercero usaba «asignación de información», que en `02:281–283` y `01:19–22` es encaminar información nueva, cuando lo medido es el enrutamiento de consultas (coordinación de la recuperación, `02:288–291`); el tercero ya no repite las confusiones que 6.3 (F1) da con cifras; el cuarto dice de dónde sale el «5 de 656» (como G2 en 07), evita la $N$ de dos significados, quita «casi exacta», «sigue sin» y la identidad `horse7` (D2), y ata el punto al rechazo claro del marco teórico. Lo que F3 dejaba aquí (`apple` → `pear` 3 y → `tomato` 3) sigue en la matriz de 05.

### 1.7 6.3 (texto de F1): no repetir el argumento de 6.2

- **Dónde:** subsección `sec:disc-dominancia`, texto nuevo de F1.
- **Viejo (F1):** «La puntuación cruda favorece al que más registró aunque la estructura del directorio esté casi balanceada (2.974 de 3.000 bits); la lectura B1, que divide entre los registros, deja a \texttt{apple} en 13.8\% (ideal 12.5\%).»
- **Nuevo:** «La puntuación cruda favorece al que más registró (Sección~\ref{sec:disc-b1}); la lectura B1, que divide entre los registros, deja a \texttt{apple} en 13.8\% (ideal 12.5\%).»
- **Por qué:** el 2.974 de 3.000 y «sesgo de lectura, no de estructura» ya son el centro de 6.2, en la página anterior.

### 1.8 6.5: etiqueta para poder citarla y tabla de la lesión

- **Dónde:** `06:137` y `06:148–149`.
- **Viejo:** «\subsection{Una memoria por módulo: familiaridad, nombre y daño}» y «…con daño al azar en la única memoria, el módulo deja de nombrar mucho antes de dejar de reconocer.»
- **Nuevo:** «\subsection{Una memoria por módulo: familiaridad, nombre y daño}» + «\label{sec:disc-una-memoria}», y «…el módulo deja de nombrar mucho antes de dejar de reconocer (Tabla~\ref{tab:lesion}).»
- **Por qué:** 07 (una memoria y trabajo futuro) remite a esta subsección; la tabla es el resultado en que descansan las analogías con YR, las ratas y la afasia óptica.

### 1.9 07, respuesta a la pregunta: las fugas del rechazo y el costo de Wegner con cifras

- **Dónde:** `07:30–41` (texto del replanteamiento §5b con A4).
- **Viejo (resultante):** «Sí: un sistema de memoria transactiva hecho solo de memorias asociativas entrópicas reparte, recuerda y rechaza en ocho dominios. Los directorios, la lectura B1, el rechazo por containment, la actualización del directorio y la coordinación punto a punto funcionan sin componentes supervisados de decisión. Los límites encontrados están en las \emph{representaciones}. En texto, […] En imagen, […] (89.2\% de punta a punta, frente a 95.5\% con objetos conocidos). El costo de repartir el conocimiento aparece donde la teoría de Wegner lo predice: el grupo necesita interacciones, y distintivas, para formar su directorio.»
- **Nuevo** (las frases de A4 sin cambio):
```latex
\paragraph{Respuesta a la pregunta de investigación.}
Sí: un sistema de memoria transactiva hecho solo de memorias asociativas entrópicas
reparte, recuerda y rechaza en ocho dominios.
Los directorios, la lectura B1, el rechazo por containment, la actualización del
directorio y la coordinación punto a punto funcionan sin componentes supervisados de
decisión.
El rechazo tiene dos fugas medidas: consultas que comparten tokens con un dominio, y
entradas visuales sin estructura, que el umbral de energía cierra en su mayor parte
(limitaciones (a) y (c)).
Los límites encontrados están en las \emph{representaciones}.
En texto, el léxico que comparten clases vecinas concentra los errores que quedan
(\texttt{pear} $\to$ \texttt{apple} 9 y \texttt{horse} $\to$ \texttt{cow} 6 de 28) y
fija el techo de \texttt{pear} (76\%) y \texttt{horse} (88\%).
En imagen, la cobertura del espacio latente deja sin respuesta parte de las vistas de
objetos nuevos (89.2\% de punta a punta, frente a 95.5\% con objetos conocidos).
Formar el directorio cuesta lo que la teoría de Wegner anticipa: interacción (con 10
consultas por dominio la precisión madura queda en 81.2\%, y hacen falta unas 50 para
llegar al 93.0\%) y comunicación distintiva (las clases que preguntan con léxico
compartido pierden hacia su vecina).
```
- **Por qué:** la pregunta incluye «rechazar lo que no conoce» y la respuesta no decía que el rechazo tiene fugas medidas; la frase de Wegner («interacciones, y distintivas») queda atada a los dos resultados de 6.4 que la sostienen.

### 1.10 07, una memoria de contenido: el vínculo con la psicología, concreto

- **Dónde:** `07:55–57`.
- **Viejo:** «Cada módulo necesita una memoria de contenido y dos directorios; reconocer sin poder nombrar, que en las personas tiene análogos clínicos y cotidianos, surge en él de una sola memoria.»
- **Nuevo:**
```latex
Cada módulo necesita una memoria de contenido y dos directorios.
Reconocer sin poder nombrar, que en las personas tiene análogos como la afasia óptica o
la experiencia de la punta de la lengua (Sección~\ref{sec:disc-una-memoria}), surge en
él de una sola memoria: con daño al azar, el módulo deja de nombrar mucho antes de
dejar de reconocer.
```
- **Por qué:** «análogos clínicos y cotidianos» no dice cuáles ni con qué resultado se comparan; los dos análogos y la lesión ya están en 6.5 con sus citas. (La frase anterior, con G3, no cambia.)

### 1.11 07, lecciones: sin la primera, que repite la respuesta

- **Dónde:** `07:59–67` (texto del replanteamiento §5c con A5).
- **Viejo (resultante):** «\paragraph{Lecciones.} Primero, la representación pesa tanto como el mecanismo: los límites observados están en las representaciones, no en las memorias. Segundo, un sesgo de lectura no es un sesgo de estructura: […] sin tocar lo registrado. Tercero, la fidelidad del pipeline es un resultado en sí mismo: […] decisiones fuera de las memorias.»
- **Nuevo:**
```latex
\paragraph{Lecciones.}
Un sesgo de lectura no es un sesgo de estructura: con la lectura cruda, \texttt{apple}
gana el 20.5\% de las victorias aunque el directorio está casi balanceado (2.974 de
3.000 bits), y la normalización por conteo lo deja en 13.8\% sin tocar lo registrado.
Y la fidelidad del pipeline es un resultado en sí mismo: todos los números reportados
son trazables a corridas del sistema actual, sin vectores sintéticos ni decisiones
fuera de las memorias.
```
- **Por qué:** «los límites están en las representaciones, no en las memorias» ya está en la respuesta (veinte líneas antes) y en el cierre; las otras dos lecciones quedan con su texto aprobado (A5 y §5c).

### 1.12 07, trabajo futuro: sale de las limitaciones

- **Dónde:** `07:69–81` (con F2 en el primer punto).
- **Viejo:** «Los siguientes pasos más relevantes son:» y los tres puntos (Fuentes de conocimiento complementarias a ConceptNet; Aprendizaje en fase madura, con «\emph{transactive encoding} y \emph{transactive retrieval} en sentido amplio»; Rotación de módulos).
- **Nuevo:**
```latex
\paragraph{Trabajo futuro.}
Los siguientes pasos salen de las limitaciones de la Sección~\ref{sec:limitaciones}:
\begin{enumerate}
    \item \textbf{Partición de validación} (limitación (g)): elegir el punto de control
    del encoder y el número de variantes sin mirar el conjunto de prueba, y volver a
    medir el hemisferio visual con esa partición.
    \item \textbf{Aprendizaje en fase madura} (limitación (e)): que los módulos sigan
    registrando etiquetas, imágenes y asociaciones después de formar el directorio (la
    asignación de información de Wegner), y que el directorio se reorganice cuando un
    módulo sale del grupo o entra en él.
    \item \textbf{Reconocer sin nombrar como consulta al directorio}
    (Sección~\ref{sec:disc-una-memoria}): cuando un módulo reconoce una imagen pero no
    puede nombrarla, que pregunte el nombre a quien lo sepa, como en el modelo de
    Wegner, en lugar de no responder.
    \item \textbf{Fuentes de conocimiento complementarias a ConceptNet} (limitación
    (i)): medir si conocimiento alineado al lenguaje de las consultas eleva el techo de
    las clases con léxico compartido (\texttt{pear} 76\%, \texttt{horse} 88\%).
\end{enumerate}
```
- **Por qué:** la limitación de la partición dice «queda pendiente» y no aparecía aquí; 6.5 dice que reconocer sin nombrar «es justo el momento en que un miembro del grupo debería consultar el directorio» y tampoco; la rotación de módulos no salía de ninguna limitación y se une al aprendizaje madura; «transactive encoding/retrieval» se cambia por el proceso que define 02; el punto de ConceptNet dice «medir» porque F2 deja dicho que no se midió. Un quinto punto posible, si lo quieres: fotos de otro origen (limitación (f)).

---

## Parte 2. Claridad y estilo

### 2.1 6.2, segundo párrafo: sin repetir 05 palabra por palabra

- **Dónde:** `06:48–56` (texto del replanteamiento §4b con F7).
- **Viejo (resultante):** «Dos datos sostienen esta lectura. Primero, la brecha cruda-B1 es de 7.8 puntos con ocho módulos (85.2\% frente a 93.0\%). Segundo, la entropía del directorio es alta incluso en la condición cruda (2.974 de 3.000 bits): la \emph{estructura} del directorio está bien formada y balanceada; el sesgo vive en la \emph{lectura}, exactamente donde B1 actúa. Las condiciones que manipulan síntomas (B2, C, D, E) quedan por debajo, y la combinación G supera a B1 sola por medio punto (93.5\% frente a 93.0\%), dentro del ruido: una vez corregida la causa, las correcciones auxiliares aportan poco.»
- **Nuevo:**
```latex
La brecha cruda-B1 es de 7.8 puntos con ocho módulos (85.2\% frente a 93.0\%), y la
entropía del directorio es alta incluso con la lectura cruda (2.974 de 3.000 bits): la
\emph{estructura} del directorio está casi balanceada, y el sesgo está en la
\emph{lectura}, donde B1 actúa.
Las condiciones que actúan sobre los síntomas (B2, C, D, E) quedan por debajo de B1, y
la combinación G, que suma correcciones a B1, gana solo medio punto, dentro del ruido
(Tabla~\ref{tab:calibracion}).
```
- **Por qué:** la última frase repetía `05:56–58` («supera a B1 sola por medio punto… aportan poco»); sobran el anuncio «Dos datos… Primero/Segundo», «exactamente» y «vive».

### 2.2 6.6, la partición frente a una EHAM única: tres párrafos

- **Dónde:** `06:185–207` (con E12 y F5).
- **Viejo:** desde «La comparación con la EHAM única acota lo que la maquinaria transactiva aporta. Ante todo es fidelidad, coherencia y precisión:» hasta «y ocho veces las celdas.»
- **Nuevo:**
```latex
La comparación de la Sección~\ref{sec:eham-unica} acota lo que aporta la maquinaria
transactiva.
Lo primero es no mezclar: la relación de una EHAM acumula por coordenada y valor, y dos
conceptos distintos comparten valores cuantizados en muchas coordenadas, así que una
memoria con varios dominios mezcla al recordar aunque las palabras difieran.
Partir el contenido evita la mezcla porque el dominio se decide antes de la
recuperación, en el directorio, y no al muestrear la memoria.
Se ve en la fidelidad: la respuesta de la EHAM única queda más lejos de la instancia
real más cercana en todos los cortes (de 4.6 a 6.2 más que el oráculo), sin tendencia
con el contenido.
Y se ve fuera de dominio: la EHAM única acepta más cuanto más contiene (de 2 a 8 de 40
consultas), y el protocolo con doble compuerta acepta 2 en todos los cortes.

La exactitud de clase también mejora, pero poco.
Desde 50 imágenes por clase el protocolo acierta entre 98.3 y 98.8\,\% frente a
96.9--97.6\,\% de la EHAM única, con intervalos separados; con 25 la EHAM única queda
arriba (97.6 frente a 96.9\,\%, con intervalos que se solapan), porque el directorio
todavía enruta peor (95.3\,\% de enrutamiento correcto).

El precio es cobertura y un índice.
El especialista deja sin respuesta al 2.5\,\% de las imágenes de prueba con 200 por
clase, que la EHAM única responde: 1.2 puntos porque la contención es estricta en las
64 coordenadas del latente y 1.3 porque el recuerdo no devuelve palabras.
Es parte del rechazo residual del hemisferio visual (limitación (b)); el protocolo de
esta comparación, que forma su directorio visual sin variantes, responde al 81\,\%.
A eso se suman el error del directorio, de 1.2 a 1.7 puntos de clase desde 50 imágenes
por clase (3.1 con 25), y ocho veces las celdas de memoria: una heteroasociativa por
módulo en lugar de una.
```
- **Por qué:** un párrafo de 23 líneas; la tríada «fidelidad, coherencia y precisión» no se cumple («coherencia» no vuelve a aparecer); «sorteo» y «ocho veces las celdas» no se entienden sin el código; no remitía a la sección de 05. Cifras sin cambio; «una heteroasociativa por módulo» sale de `results/experimento11/README.md` (misma forma de memoria por especialista).

### 2.3 Limitación (d) (hoy (c)): la cabeza de clasificación solo entrena

- **Dónde:** `06:272–280`.
- **Viejo:** desde «\paragraph{(c) Calidad de la reconstrucción visual.} El decoder, entrenado con un término de reconstrucción MSE dentro de una pérdida que incluye una cabeza auxiliar de clasificación,» hasta «y puede abordarse de forma independiente.»
- **Nuevo:**
```latex
\paragraph{(d) Calidad de la reconstrucción visual.}
Las reconstrucciones son suaves y sin detalle de alta frecuencia
(Figura~\ref{fig:imagen-etiquetas}).
Es un efecto de cómo se entrenó el autoencoder, con un término de reconstrucción MSE y
una cabeza auxiliar de clasificación que solo interviene en el entrenamiento, no en las
decisiones; no es un efecto del sistema de memorias y puede corregirse por separado.
Puede compararse con la reconstrucción e imaginación en EAM de Pineda y
Morales~\cite{pineda2023imagery} y con la memoria EAM sobre imágenes naturales de
CIFAR-10~\cite{hernandez2026cifar}, que enfrenta la misma disyuntiva con autoencoders
más profundos.
```
- **Por qué:** el lector acaba de leer «sin clasificadores» (07, G1) y tropieza con la cabeza de clasificación sin saber que no decide (`04:127–130`); una frase con causa, efecto y dos citas; «compromiso» por *trade-off*.

### 2.4 07, resultados principales: frases más cortas, un solo tiempo verbal

- **Dónde:** `07:12–28` (con G2).
- **Viejo:** desde «\paragraph{Logros principales.} Sobre el banco de 411 consultas ($N = 400$, 5 semillas; la fase madura se evalúa sobre las consultas que formaron el directorio), el sistema alcanzó…» hasta «…con el llenado de 16 variantes del experimento 13.»
- **Nuevo:**
```latex
\paragraph{Resultados principales.}
Sobre el banco de 411 consultas ($N = 400$, 5 semillas), el sistema alcanza una
\textbf{precisión temprana del 90.0\%} y una \textbf{precisión madura del 93.0\%} con
la lectura B1 del directorio, con una fidelidad temprana-madura del 95.8\%; la fase
madura se evalúa sobre las consultas que formaron el directorio.
Sobre 171 consultas reservadas, el protocolo enruta correctamente el 97.0\% con 200
imágenes por clase (experimento 11).
La lectura B1 deja la participación de \texttt{apple}, el módulo que la lectura cruda
favorece (20.5\%), en \textbf{13.8\%} (ideal 12.5\%).
En la dirección inversa, el hemisferio visual enruta el \textbf{96.2\%} de las 656
imágenes de prueba, con \textbf{dos falsos enrutamientos} (99.7\% de precisión sobre
las aceptadas; ambos, vistas del mismo objeto hacia la clase vecina), y el registro
completo de sus percepciones queda balanceado: \textbf{3.000 bits} de entropía, el
máximo con ocho módulos.
Sobre las primeras 15 imágenes de prueba de cada clase (116 aceptadas), la evocación de
dominio es del \textbf{97.4\%}.
Sobre objetos físicos nunca vistos (\textit{leave-one-object-out}, diez pliegues), la
cobertura de punta a punta es del \textbf{89.2\%}, seis puntos por debajo de la de
vistas nuevas de objetos conocidos, con dos falsos enrutamientos de 3280.
Con siete clases contrarias por módulo, el contenido no acepta ningún falso al llenar
con un latente por imagen (curva de capacidad) y acepta 5 de 656 imágenes de prueba
(0.8\%), todas entre animales, con el llenado de 16 variantes del experimento 13.
```
- **Por qué:** con G2 las dos primeras frases quedaban de cinco y seis cifras con dos «con» encadenados; se mezclaban «alcanzó», «es» y «fue»; «Logros» y «casi perfecta» califican lo que las cifras ya dicen. Cifras y alcances: los de G2, sin cambio.

### 2.5 07, frente a una EHAM única: el costo en claro

- **Dónde:** `07:44–48`.
- **Viejo:** «…acepta menos consultas fuera de dominio cuando el contenido crece y en imagen se equivoca de dominio unas tres veces menos. Desde 50 imágenes por clase también clasifica algo mejor (1.4 puntos con 200); con 25, no. A cambio cubre menos y paga un índice.»
- **Nuevo:**
```latex
…acepta menos consultas fuera de dominio cuando el contenido crece y en imagen responde
con un dominio ajeno menos veces (3.0\% de las imágenes, frente a 10.9\% con 200 por
clase).
Desde 50 imágenes por clase también clasifica algo mejor (1.4 puntos con 200); con 25,
no.
A cambio cubre menos, y el directorio le cuesta de 1.2 a 1.7 puntos de clase respecto
del oráculo desde 50 imágenes por clase.
```
- **Por qué:** «paga un índice» solo se entiende recordando 6.6; «unas tres veces» no dice contra qué (10.9/3.0 = 3.6; 10.9/4.1 = 2.7). Cifras de `05:431–433` y `05:438–440`.

### 2.6 Cierre de 07

- **Dónde:** `07:85–90` (texto del replanteamiento §5d).
- **Viejo (resultante):** «En resumen, los resultados muestran que las Memorias Asociativas Entrópicas de Pineda y Morales son una base suficiente para construir un sistema distribuido de memoria transactiva de ocho especialistas, bidireccional y con rechazo controlado, sin recurrir a modelos de aprendizaje profundo supervisado para la toma de decisiones; y que sus límites viven en las representaciones que alimentan a las memorias, no en el mecanismo asociativo ni en la maquinaria transactiva.»
- **Nuevo:**
```latex
En resumen, las Memorias Asociativas Entrópicas de Pineda y Morales bastan para
construir un sistema distribuido de memoria transactiva de ocho especialistas,
bidireccional y con rechazo claro, sin modelos supervisados en la toma de decisiones.
Sus límites están en las representaciones que alimentan a las memorias, no en el
mecanismo asociativo ni en la maquinaria transactiva.
```
- **Por qué:** una frase de seis líneas con «; y que»; «rechazo controlado» no aparece en otra parte (02:292 define «rechazo claro»); «viven».

### 2.7 Cambios pequeños

| Dónde | Viejo | Nuevo | Por qué |
|---|---|---|---|
| `06:45–46` | «Dividir entre el conteo normaliza la evidencia a \textit{evidencia por interacción}, que es una medida justa para comparar módulos con historiales de exposición distintos.» | «Dividir entre el conteo normaliza la evidencia a \textit{evidencia por interacción}, comparable entre módulos con historiales de exposición distintos.» | «justa» es un juicio; lo que se dice es «comparable». |
| `06:151–155` | «La paciente YR, con una lesión selectiva del hipocampo, reconoce ítems pero falla en asociaciones entre tipos distintos de información, como caras con nombres hablados~\cite{mayes2004associative}; en ratas, la lesión del hipocampo suprime el recuerdo y deja la familiaridad~\cite{fortin2004recollection}; y con la edad, la memoria de asociaciones se deteriora más que la de ítems~\cite{old2008differential}.» | «La paciente YR, con una lesión selectiva del hipocampo, reconoce ítems pero falla en asociaciones entre tipos distintos de información, como caras con nombres hablados~\cite{mayes2004associative}. En ratas, la lesión del hipocampo suprime el recuerdo y deja la familiaridad~\cite{fortin2004recollection}; con la edad, la memoria de asociaciones se deteriora más que la de ítems~\cite{old2008differential}.» | Tres hallazgos y tres citas en una oración. |
| `06:316–319` | «adoptadas después de ver el experimento 13, que mide sobre las 656 imágenes de test (son el valor más alto de su rejilla, no un óptimo ajustado). La lectura del directorio visual es estricta ($\xi = 0$) y no deja tolerancia que ajustar.» | «adoptadas después de ver el barrido de variantes (experimento 13), que mide sobre las 656 imágenes de prueba (16 es el mayor valor probado, no un óptimo ajustado). La lectura del directorio visual no tiene tolerancia que ajustar ($\xi = 0$, limitación (b)).» | El paréntesis había que releerlo; la frase de $\xi$ repetía la apertura de (b). |
| `06:320–322` | «…pero inflan potencialmente las cifras visuales reportadas; la corrección de protocolo (partición train/val/test) es directa y queda pendiente.» | «…pero pueden inflar las cifras visuales reportadas; la corrección (una partición de validación aparte) es directa y queda pendiente.» | «potencialmente» es calco; la partición la retoma el trabajo futuro. |
| `06:325–326` | «admite tokens mal etiquetados por el POS si figuran en el vocabulario que llenó las memorias» | «admite tokens que el filtro gramatical (POS) descarta si figuran en el vocabulario que llenó las memorias» | «mal etiquetados por el POS» no se entiende sin 04:89–90. |

(En `06:315` se aplica además D2 de hechos: «$\approx$5 candidatos» → «cinco candidatos».)

---

## Parte 3. Términos (decisión T)

Se aplica sobre el texto final de 06 y 07, incluidos los textos nuevos de las Partes 1 y 2. En esos textos nuevos ya uso enrutamiento/enrutar, etiqueta, prueba, partición, puntuación, recuperación y variantes, que la tesis ya usa en otros lugares, así que valen aunque rechaces T. Dejé **containment**, **encoder**, **autoencoder** y **pipeline** como están, para que los decidas aquí.

| Dónde | Viejo | Nuevo |
|---|---|---|
| `06:30` (pie de la figura 11) | «del espacio semántico de los labels de las ocho clases» | «del espacio semántico de las etiquetas de las ocho clases» |
| `06:314` | «el punto de control del encoder» | «el punto de control del codificador» |
| `06:315` | «(RMSE mínimo sobre test entre» | «(RMSE mínimo sobre el conjunto de prueba entre» |
| 6.1 (1.5), (a) ×2 (1.1), 07 respuesta (1.9) | «containment» | «contención» (en (a): «pasa la contención textual», «ninguna compuerta de contención»; en 6.1 y 07: «el rechazo por contención») |
| 6.3 (texto de F1), (c) (1.2), trabajo futuro (1.12) | «encoder» | «codificador» |
| (d) (2.3) | «el autoencoder», «autoencoders más profundos» | «el autocodificador», «autocodificadores más profundos» |
| 07 lecciones (1.11) | «la fidelidad del pipeline» | «la fidelidad del procesamiento» |

Si apruebas T, quedan de 06 y 07 sin anglicismos en prosa salvo «token» (término de PLN, se queda) y las glosas en cursiva.

---

## Parte 4. Forma

| Dónde | Viejo | Nuevo |
|---|---|---|
| `06:331` | «(p.ej.\ solo la etiqueta POS de diccionario)» | «(p.\ ej.\ solo la etiqueta POS de diccionario)» |
| `06:308` | «objeto nuevo» entre comillas latinas | ``objeto nuevo'' (la tesis usa ``…'' en los otros 18 casos; ya va así en 1.3) |
| `07:25` | «con 2 falsos enrutamientos de 3280» | «con dos falsos enrutamientos de 3280» (ya va así en 2.4) |
| `07:23` | «(leave-one-object-out, diez pliegues)» | «(\textit{leave-one-object-out}, diez pliegues)» (ya va así en 2.4) |

---

## Descartado

**claridad_06_07.md**
- A1, textos para 07 (5b «separabilidad… entre los animales», 5c «los dos hemisferios fallan en el mismo lugar»): los sustituyen A4/A5 de hechos; «comparten envolvente latente» tampoco tiene medición.
- A2, subsección de 05: la propone el consolidador de 05; aquí solo tomé la (f) como interpretación.
- M2, mover el experimento 15 a 05: obliga a escribir un resultado nuevo en 05 (ver 1.1).
- M4, frase opcional de Wegner en 6.2: agrega una afirmación nueva.
- M9, las tres lecciones nuevas: la primera usa la envolvente latente sin medir, la segunda se apoyaba en el enriquecimiento que F2 quita, la tercera repite el párrafo «Una memoria»; me quedé con quitar la lección que repite.
- M11, lista de experimentos al final de 04: es de 04; aquí cada experimento se nombra por lo que hace antes del número.
- M12: va en T y en los textos nuevos.
- M13, mover la figura 11 a 04: la cita primero `04:83` y su panel dice «quantize_binary» (consistencia 7.5), así que va con 04 y con la propuesta de figuras.
- M14: es G3 de hechos.
- M15, quitar todas las cifras de 6.1: A2 las precisa; solo quité «ambos del mismo objeto» (D2).
- B2, quitar las citas de la apertura de 07: gusto; G1 ya edita esa frase.
- B4, texto para `06:174–175`: lo sustituye F4 de hechos.

**cifras_06.md / cifras_main_01_07.md** (bajos)
- cifras_06 n.º 12 («5.7» en `05:420`): es de 05.
- cifras_main B2 («5 semillas» no mueven A ni B1): no es un error; el revisor mismo propone dejarlo.
- El resto de sus hallazgos está en hechos (A1–A6, E3, E10, E12, F1–F7, G1–G3).

**lexico.md**
- «En términos de Wegner» → «En el modelo de Wegner» (`06:118`, `06:176`): es español correcto.
- «la extensión natural» (`06:339–340`): F2 quita la frase.
- «Rotación de módulos: explorar…» (`07:79`): el punto se une al de aprendizaje madura (1.12).
- «el único enriquecimiento que ayudó» (`07:72–74`): F2 lo quita.
- Mayúsculas de «Memorias Asociativas Entrópicas» (consistencia 7.4, en el cierre): es una decisión para toda la tesis, no de 07.

**antipatrones.md**
- Títulos «Mecanismo y representación» (6.1) y «Por qué B1» (6.2): son títulos ya aprobados en el replanteamiento.
- Su texto para `06:65–76`: conserva la causa «encoder», que F1 quita.
- Renombrar los cuatro puntos de 6.4 («Interacción», «Orden»…): gusto.
- `06:142` («no consulta un almacén aparte: es leer la asociación»): el contraste es informativo.
- Quitar las ocho `\textbf{}` de los resultados de 07: en conclusiones marcan las cifras principales; gusto.
- Quitar «Sí:» de la respuesta (`07:30`): responde a una pregunta de sí o no.
- Fundir «Frente a una EHAM única» y «Una memoria» en los resultados: cambia la estructura de 07 sin ganar claridad.

**consistencia.md**
- 6.5, «(limitación (b), Sección~\ref{sec:limitaciones})»: la letra basta dentro de 06.
- 4.4, $\tau$ = 16.61 en `06:255`: la (c) nueva remite a 04 y no repite el valor.

**forma_07.md**
- «3280» → «3.280»: falso positivo (sin separador hasta cuatro cifras; «3.000 bits» es entropía con tres decimales).
- `07:32–33` «de 3 a 8», `07:36` «90\%», `07:61–62` «observados»: los quita el replanteamiento.
- Cursiva en «containment», «encoder», «pipeline», «labels» (`07:32`, `37`, `64`, `65`, `76`): se resuelven con T (o, si la rechazas, con una sola regla para toda la tesis).

**forma_06.md**: sin errores; separador decimal y formato de porcentaje no se tocan (plantilla UACJ).
