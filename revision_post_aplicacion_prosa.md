# Propuesta viejo/nuevo: lo que salió al aplicar el consejo

**Estado:** aprobada y aplicada el 2 nov 2026 (P1–P11).

Al aplicar las propuestas aprobadas, los agentes encontraron frases que ninguna propuesta cubría y que chocan con un dato o con el texto ya aplicado. Verifiqué cada una contra los datos. Las líneas son las del `.tex8` ya aplicado.

## Hechos

### P1. Léxico compartido de las frutas (05:98–99)
- **Viejo:** «Las clases de fruta comparten el léxico genérico (\textit{fruit}, \textit{red}, \textit{green}, \textit{round}, \textit{tree}) y concentran 18 de los 28 errores»
- **Nuevo:** «Las clases de fruta comparten léxico genérico (\textit{fruit} las tres, \textit{pome} \texttt{apple} y \texttt{pear}, \textit{red} \texttt{apple} y \texttt{tomato}) y concentran 18 de los 28 errores»
- **Fuente:** en `labels_{apple,pear,tomato}.json`, *green*, *round* y *tree* solo aparecen en `apple`. Lo compartido es: entre `apple` y `pear`, *fruit* y *pome*; entre `apple` y `tomato`, *fruit* y *red*; entre `pear` y `tomato`, *fruit*.

### P2. Pie de la Figura 5 (05:88)
- **Viejo:** «Hasta $N = 200$, A, C, E32, E64 y F quedan entre 66 y 77\%; B1 sube de 78 a 93\%, y D y G pasan del 86\% en todo el rango.»
- **Nuevo:** «Hasta $N = 200$, A, C, E32, E64 y F quedan entre 66 y 77\%, y B1 sube de 78 a 88\% (93\% con $N = 400$); D y G pasan del 86\% en todo el rango.»
- **Fuente:** `results/ablation_mdir_bias/ablation_metrics.csv`, media de 5 semillas. B1: 78.0, 87.0, 88.0 y 93.0 con N = 50, 100, 200 y 400. D: 86.5 como mínimo. G: 90.0 como mínimo.

### P3. Los dos falsos enrutamientos visuales (06:117–119)
- **Viejo:** «El directorio visual comete dos falsos enrutamientos de 656, hacia una clase vecina. Es el rechazo claro de la Sección~\ref{sec:tmt}: lo que ningún módulo reconoce no se responde, y los errores que quedan caen en clases vecinas.»
- **Nuevo:** «El directorio visual comete dos falsos enrutamientos de 656. Es el rechazo de la Sección~\ref{sec:tmt}: lo que ningún módulo reconoce no se responde, y los falsos del contenido caen entre animales.»
- **Por qué:**
  - «Hacia una clase vecina» sale de la misma nota de trabajo que `horse7`, que se quitó por D2.
  - W1 ya quitó el término «rechazo claro» de 02.
  - Que los cinco falsos de contenido caen entre animales sí consta (`results/experimento13/raw/Vc16_N200_Vd16_s42.json`, H4).

### P4. De qué se compone el 2.5 % (06:196–198)
- **Viejo:** «…que la EHAM única responde: 1.2 puntos porque la contención es estricta en las 64 coordenadas del latente y 1.3 porque el recuerdo no devuelve palabras.»
- **Nuevo:** «…que la EHAM única responde: una de las 80 imágenes porque la contención es estricta en las 64 coordenadas del latente y otra porque el recuerdo no devuelve palabras.»
- **Por qué:** cada parte es una imagen de 80 (1.25 puntos), y el texto la redondeaba una vez hacia abajo y otra hacia arriba. Fuente: `results/experimento11/README.md`, N = 200, imagen → texto: el sistema acepta 98.8 % y responde 97.5 %.

### P5. Directorio perspectival en la apertura de la discusión (06:10–11)
- **Viejo:** «…el rechazo por contención, la actualización perspectival del directorio y la coordinación punto a punto…»
- **Nuevo:** «…el rechazo por contención, la actualización perspectival del directorio (en imagen) y la coordinación punto a punto…»
- **Por qué:** en texto, el directorio es compartido (H1, Sección~\ref{sec:organizacion}). Los directorios perspectivales solo se miden en el hemisferio visual y en la comparación con una sola EHAM.

## Coherencia con lo ya aplicado

### P6. Primera frase del resumen (main:57)
- **Viejo:** «Un grupo que trabaja junto recuerda más que cada uno de sus miembros por separado»
- **Nuevo:** «Un grupo que trabaja junto puede recordar más que cada uno de sus miembros por separado»
- **Por qué:** W2 ya suavizó esta misma afirmación en 01:4, porque Wegner no la da como hecho general.

### P7. *Sample-and-search* ligado al tercer método (02:257–259)
- **Viejo:** «…y la mejora con una búsqueda local en su vecindad (\emph{sample-and-search}).»
- **Nuevo:** «…y la mejora con una búsqueda local en su vecindad (\emph{sample-and-search}, el tercer método de la pista faltante, que el resumen del artículo llama \emph{search and test}).»
- **Por qué:** 02:166 nombra el método como *search and test* y 02:259 como *sample-and-search*, y el texto no dice que son el mismo. Fuente: `src/hetero_memory.py:28–35` y la nota de `prosa_main_01_02` 1.7.

### P8. Remisiones circulares entre 04 y 05 (04:265)
- **Viejo:** «La evaluación sigue el orden de la Sección~\ref{sec:resultados}.»
- **Nuevo:** «La Sección~\ref{sec:resultados} presenta los estudios en este orden.»
- **Por qué:** 05:4 remite a `sec:organizacion` para el orden, y 04:265 remite de vuelta a 05. Con el cambio, el orden lo da la lista de 04.

### P9. «Guarda» (04:225)
- **Viejo:** «salvo una guarda que evita cargar sus clasificadores»
- **Nuevo:** «salvo una condición que evita cargar sus clasificadores»
- **Por qué:** en 01 ya se aplicó el mismo cambio de término.

### P10. Nodo de la Figura 1 (03:137)
- **Viejo:** `{$v/S$, escala\\global persistida}`
- **Nuevo:** `{$v/S$, escala\\global guardada}`
- **Por qué:** el pie de la figura y 04 ya dicen «guardada».

## Trazabilidad

### P11. El log de la etapa 7 a `results/`
Lo que 05 dice de los directorios visuales sale del log de la etapa 7 de la corrida oficial del 26 oct: entre 2.22 y 2.41 bits, 2016–2048 registros propios contra 144–368 de cada otro módulo, y el registro completo con 3.000 bits. Ese log no está en `results/`. Propongo copiarlo a `results/hemisferio_visual/stage7_bidirectional.log`, sin cambios (57 líneas), con un README de dos líneas que diga de qué corrida es. Comprobé que el log trae las mismas cifras que 05 (631/656, los 8 directorios y las cuentas).

## Revisado y sin cambio

- **Los nombres de Wegner sin `\cite` en 03 y 06:** los tres procesos se introducen con `wegner1995computer` en 01:15. Las menciones posteriores remiten a esa.
- **El tope $w$ junto a los pesos $w_i$:** la propuesta de referencias descartó $w_{\max}$, y la notación sigue igual.
- **Mover la figura 11 de 06 a 04:** era opcional y no se hizo.
