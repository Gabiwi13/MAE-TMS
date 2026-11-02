# Propuesta viejo/nuevo: correcciones de hecho del consejo de redacción

**Estado:** pendiente de aprobación. Nada aplicado.

**Origen.** Cuatro revisores cotejaron cada cifra del `.tex8` contra `results/`, el código y los logs de la corrida del 30 oct: resumen + 01 + 07; 03 + 04; 05; 06. Aquí van solo los hallazgos de hecho (cifra mal atribuida, afirmación sin fuente, alcance no dicho, contradicción con una tabla), deduplicados. Volví a verificar cada cifra que se usa en el texto nuevo; la fuente va en cada punto. Claridad, léxico, antipatrones, figuras, referencias y ortografía van en propuestas aparte.

**Lo que más pesa.**
1. La causa «encoder» del sesgo hacia `apple` no tiene medición en `results/`, y la única medición de solapamiento latente (experimento 12) no la apoya. Tres revisores lo encontraron por separado. Está en 06, en 07 y **en el texto ya aprobado del replanteamiento** (§5b, §5c, §1): propongo ajustar ese texto antes de aplicarlo (parte A).
2. El 93.0 % de precisión madura se mide sobre las mismas consultas que formaron el directorio (dentro de muestra), y la tesis no lo dice en ningún lugar. Los README de la ablación, exp3 y exp4 sí lo declaran.
3. El 97.4 % de evocación se mide sobre las primeras 15 imágenes de prueba de cada clase (116 aceptadas), no sobre el test completo (`N_EVOKE = 15` en `src/stage7_bidirectional.py:40`).
4. El experimento de enriquecimiento de vocabulario (06:78–90: *sauce*, *bosc*, *World Cup*) no tiene archivo en `results/`.

Las líneas son las del `.tex8` actual (antes de aplicar el replanteamiento).

---

## A. Ajustes al texto aprobado del replanteamiento

El consejo revisó el texto nuevo de `revision_replanteamiento_prosa.md` como si estuviera aplicado. Estos ajustes se aplicarían junto con él.

### A1. Resumen (§1)

| Frase del texto aprobado | Ajuste | Por qué |
|---|---|---|
| «una precisión madura del 93.0\% con la lectura normalizada B1 del directorio (ablación de calibración, con un directorio compartido; banco de 411 consultas, $N{=}400$, 5 semillas)» | «…(ablación de calibración, con un directorio compartido, evaluada sobre las mismas consultas que lo formaron; banco de 411 consultas, $N{=}400$, 5 semillas)» | Dentro de muestra. `results/ablation_mdir_bias/ablation_report.md`, nota «Dentro de muestra». |
| «con objetos nunca vistos, la cobertura de punta a punta es del 89.2\%, con dos falsos de 3280.» | «con objetos nunca vistos, la cobertura de punta a punta es del 89.2\%, frente al 95.5\% de vistas nuevas de objetos conocidos, con dos falsos de 3280.» | 96.2 (ruteo) y 89.2 (punta a punta) no son comparables; el par comparable es 89.2 contra 95.5. `results/experimento16/README.md`: conocido 95.5 [95.1, 95.9], nuevo 89.2 [85.1, 93.2]. |
| «la partición en especialistas recuerda con más fidelidad y acepta menos consultas fuera de dominio.» | «la partición en especialistas recuerda con más fidelidad y, con la doble compuerta de contenido, acepta menos consultas fuera de dominio cuando el contenido crece (2 frente a 8 de 40 con 200 imágenes por clase).» | Sin compuerta el protocolo acepta 4 de 40 en todos los cortes, y la EHAM única 2 con 25 y 50. `results/experimento11/README.md`, «Fuera de dominio»: M 5.0, 5.0, 12.5, 20.0 %; protocolo 10.0 % sin compuerta y 5.0 % con compuerta. |
| «Los límites observados provienen de las representaciones (el léxico compartido entre clases y la separabilidad del espacio latente), no del mecanismo asociativo.» | «Los límites observados provienen de las representaciones (el léxico compartido entre clases vecinas y la cobertura del espacio latente ante objetos nuevos), no del mecanismo asociativo.» | «Separabilidad del latente» no tiene medición; la cobertura ante objetos nuevos sí (experimento 16). |

### A2. Discusión, apertura (§4a)

**Texto aprobado:** «…y el directorio visual alcanza el balance perfecto (3.000 de 3.000 bits) con dos falsos enrutamientos en 656, ambos del mismo objeto.»

**Ajuste:** «…y el registro completo de percepciones de la fase A queda balanceado (3.000 bits, el máximo con ocho módulos), mientras los directorios visuales de los módulos rutean la fase B con dos falsos enrutamientos en 656.»

**Por qué:** los 3.000 bits son del registro completo del TME (conteos de 2016 a 2048; entropía 2.99996). Los directorios que rutean son perspectivales y tienen de 2.22 a 2.41 bits. «Ambos del mismo objeto» depende de la decisión D2. Fuente: `logs_comparacion/stage7_bidirectional.log`.

### A3. Discusión, lectura desde Wegner (§4c, primer punto)

**Texto aprobado:** «Formar el directorio cuesta más donde las especialidades se solapan, como muestra el punto sobre la comunicación distintiva.»

**Ajuste:** «Los errores que quedan caen dentro de pares de módulos que comparten léxico, como muestra el punto sobre la comunicación distintiva.»

**Por qué:** lo medido es dónde caen los errores, no cuánto cuesta formar el directorio según el solapamiento.

### A4. Conclusiones, respuesta a la pregunta (§5b)

**Texto aprobado:** «Los límites encontrados están en las \emph{representaciones}: la asimetría léxica de la fuente de conocimiento, que fija el techo de las clases con vocabulario compartido, y la separabilidad del espacio latente del encoder, que explica buena parte del sesgo hacia \texttt{apple} con la lectura cruda.»

**Ajuste:**
```latex
Los límites encontrados están en las \emph{representaciones}.
En texto, el léxico que comparten clases vecinas concentra los errores que quedan
(\texttt{pear} $\to$ \texttt{apple} 9 y \texttt{horse} $\to$ \texttt{cow} 6 de 28) y
fija el techo de \texttt{pear} (76\%) y \texttt{horse} (88\%).
En imagen, la cobertura del espacio latente deja sin respuesta parte de las vistas de
objetos nuevos (89.2\% de punta a punta, frente a 95.5\% con objetos conocidos).
```
**Por qué:** la frase aprobada atribuye el sesgo al encoder sin medición (ver F1). Fuentes: `ablation_metrics.csv` (B1, N = 400: `cm_pear_apple` 9, `cm_horse_cow` 6, 28 errores; `mature_acc_pear` 0.76, `mature_acc_horse` 0.88); `experimento16/README.md`.

### A5. Conclusiones, lecciones (§5c, segundo punto)

**Texto aprobado:** «Segundo, los sesgos observados en un hemisferio pueden originarse en el otro: el sesgo ``léxico'' hacia \texttt{apple} era en buena parte solapamiento latente del encoder.»

**Ajuste:** «Segundo, un sesgo de lectura no es un sesgo de estructura: con la lectura cruda, \texttt{apple} gana el 20.5\% de las victorias aunque el directorio está casi balanceado (2.974 de 3.000 bits), y la normalización por conteo lo deja en 13.8\% sin tocar lo registrado.»

**Fuente:** `ablation_metrics.csv`: `winner_pct_apple` A 0.205, B1 0.1375; `mdir_entropy` A 2.9738.

### A6. Introducción, contribución 2 (§2e)

**Texto aprobado:** «Con esta representación, sin tocar la maquinaria asociativa, la precisión temprana de 8 clases es del 90.0\%.»

**Ajuste:** «Con esta representación, la precisión temprana sobre el banco de 411 consultas es del 90.0\% (Sección~\ref{sec:calibracion}).»

**Por qué:** no hay corrida que aísle el efecto de la cuantización; el 90.0 % es del sistema completo. Fuente: `ablation_report.md`, EarlyAcc 90.00 en N = 400.

---

## B. Introducción (`01_introduccion.tex`)

### B1. El encoder parte de ImageNet (01:64–65)
**Viejo:** «Las representaciones visuales las produce un encoder ResNet18 \cite{he2016resnet} preentrenado, cuya salida se cuantiza y almacena.»
**Nuevo:** «Las representaciones visuales las produce el encoder de un autoencoder ResNet18 \cite{he2016resnet}, inicializado con los pesos de ImageNet y entrenado sobre ETH-80 (Sección~\ref{sec:percepcion}); su salida se cuantiza y almacena.»
**Fuente:** `src/stage2_encoder.py:93` (`ResNet18_Weights.IMAGENET1K_V1`); `models/encoder.meta.json` (50 épocas, semilla 42).

---

## C. Arquitectura (`03_arquitectura.tex`)

### C1. Historia de versiones (03:4–5)
**Viejo:** «…del sistema distribuido de memoria transactiva en su versión de ocho módulos.»
**Nuevo:** «…del sistema distribuido de memoria transactiva de ocho módulos.»

### C2. «Preentrenados» (03:19–21)
**Viejo:** «ambos son preentrenados y sus pesos permanecen fijos durante la operación del sistema de memorias.»
**Nuevo:** «ambos se entrenan de antemano (Sección~\ref{sec:percepcion}) y sus pesos permanecen fijos durante la operación del sistema de memorias.»

### C3. Diagrama de la fase temprana: falta PROPN (03:217)
**Viejo:** `{spaCy\\lemas NOUN/ADJ\\+ rescate léxico}` → **Nuevo:** `{spaCy\\lemas NOUN/ADJ/PROPN\\+ rescate léxico}`
**Fuente:** `src/stage6_interaction.py:55` (`ACCEPTED_POS = {"NOUN", "ADJ", "PROPN"}`); 04:87–88 ya lo dice.

### C4. Diagrama de la fase madura sin τ ni compuerta (03:326–358)
El pie y el texto describen el umbral de energía τ y la compuerta de contenido del destino; el diagrama no los dibuja. Propuesta: dos nodos (`Imagen: $\|\mathbf{z}\| \ge \tau$` entre la consulta y el módulo de entrada; `Texto: contiene la pista` entre el destino y el recall), con flechas al rechazo. Va junto con el rediseño de diagramas de la propuesta de figuras, porque el revisor de figuras encontró además que el diagrama de la fase temprana queda a escala 0.41 (letra de unos 3 pt).
**Fuente:** `src/stage7_bidirectional.py:225–228`; `src/stage8_mature.py:93–102`.

### C5. «Para equiparar escalas» (03:405)
**Viejo:** «y se normalizan $w_i \leftarrow w_i / \max_j w_j$ para equiparar escalas.»
**Nuevo:** «y se normalizan $w_i \leftarrow w_i / \max_j w_j$ (la proyección es invariante a esa escala; ecuación~\eqref{eq:normalizacion-pesos}).»
**Fuente:** `src/hetero_lib/hetero_associative_4d.py:452` (la proyección vuelve a normalizar a media unitaria).

---

## D. Metodología (`04_metodologia.tex`)

### D1. Candidatos unidireccionales sin fuente (04:62–65)
**Viejo:** «(\texttt{pear} tiene 68 candidatos crudos, frente a 11 si se busca en un solo sentido; \texttt{tomato}, 86 frente a 12)»
**Nuevo:** «(\texttt{pear} reúne 68 candidatos crudos y \texttt{tomato} 86)»
**Por qué:** 68 y 86 están en `cache/conceptnet_extracted.json`; el caché unidireccional ya no existe y 11 y 12 no tienen archivo. Medirlos pediría volver a leer las 34 M de aserciones de ConceptNet.

### D2. Labels y candidatos: cifras exactas (04:69–70, 04:136–138, 06:315)
- «con $\approx$21 labels efectivos» → «con 21 labels efectivos cada una» (los ocho `labels_*.json` tienen 21).
- «(una evaluación cada 10 épocas, $\approx$5 candidatos)» → «(una evaluación cada 10 épocas: cinco candidatos)»; igual en 06:315. Fuente: `src/stage2_encoder.py:37, 237–245`.

### D3. Tokens rescatados (04:99–101)
**Viejo:** «y los tokens rescatados son de los más discriminativos (\texttt{bark}, \texttt{moo}, \texttt{canine}, \texttt{riding}, \texttt{wheel}\ldots).»
**Nuevo:** «y los tokens rescatados con más frecuencia son \texttt{bark}, \texttt{riding}, \texttt{drink}, \texttt{canine} y \texttt{drive}.»
**Fuente:** `results/rescate_lexico/README.md:16` («Tokens rescatados más frecuentes: bark, riding, drink, canine, drive, run, moo, racing»); «más discriminativos» no se midió.

### D4. Consultas de ejemplo que no están en el banco (04:166–170)
**Viejo:** «(p.ej.\ ``a red crunchy fruit'', ``a barking domestic pet'', ``a mug for drinking coffee'') … (``a bosc pear with a narrow neck'', ``tomato on the vine'')»
**Nuevo:** «(p.\ ej.\ ``a crunchy red apple'', ``a barking domestic pet'', ``a mug for liquid'') … (``a bosc pear with brown skin'', ``a tomato on the vine'')»
**Fuente:** `src/eval_bank.py:26, 120, 149, 194, 219` (literales). Dos de las viejas eran consultas de la etapa 6, no del banco.

### D5. El encoder parte de ImageNet (04:122–124)
Agregar «con el \textit{backbone} inicializado con los pesos de ImageNet» a la descripción del autoencoder (misma fuente que B1).

### D6. Escala min-max del latente → decisión D1 (abajo).

---

## E. Resultados (`05_resultados.tex`)

### E1. Dentro de muestra (05:20–22 y pie de la tabla 05:26–27)
**Pie, viejo:** «($N = 400$, media de 5 semillas, banco de 411 consultas)» → **nuevo:** «($N = 400$, media de 5 semillas, 400 consultas del banco de 411)».
**Agregar tras la línea 22:**
```latex
En este estudio, como en el protocolo completo y en la curva de formación, la fase
madura se evalúa sobre las mismas $N$ consultas cuyos tokens formaron el directorio:
mide si el directorio reproduce lo que registró, no si generaliza a consultas nuevas.
Sobre 171 consultas reservadas, el protocolo transactivo del experimento 11 rutea
correctamente el 97.0\% con 200 imágenes por clase (Sección~\ref{sec:eham-unica}).
```
**Fuente:** `ablation_report.md`, `exp3_corrected_routing/report.md`, `exp4_directory_formation/report.md` (nota «Dentro de muestra»); `ablation_metrics.csv` (las matrices de confusión suman 400 por semilla); `experimento11/README.md`, N = 200, T-protocolo, «ruteo ok» 97.0 [96.6, 97.4].

### E2. «La mayoría» es la mitad (05:85)
«la mayoría \texttt{pear} $\to$ \texttt{apple} (9)» → «la mitad \texttt{pear} $\to$ \texttt{apple} (9)». 9 de 18.

### E3. «2.2 puntos» (05:101)
**Viejo:** «y con B1 ningún módulo se desvía más de 2.2 puntos del ideal.»
**Nuevo:** «y con B1 el módulo que más se aleja del ideal es \texttt{pear}, a 2.25 puntos (10.25\%).»
**Fuente:** `ablation_metrics.csv`, B1, N = 400, `winner_pct_pear` 0.1025 (verificado).

### E4. Pie de la figura 2 (05:65–66)
**Viejo:** «D y G, que además balancean las consultas, superan a B1 en $N = 50$.»
**Nuevo:** «G, que además balancea las consultas, queda por encima de B1 en todo el rango; D lo supera en $N = 50$ y $200$.»
**Fuente:** `ablation_report.md`, tabla por N (G 91.7/90.0/93.2/93.5 contra B1 78/87/88/93; D 90.0 y 89.2 en 50 y 200).

### E5. «En todas las celdas del grid» no se midió (05:212–215)
**Viejo:** «En todas las celdas del grid, la lectura madura cruda queda por debajo de la lectura B1 (72.5\% frente a 81.2\% en la línea base; 80.0\% frente a 83.8\% en la mejor condición nativa).»
**Nuevo:** «En las dos condiciones nativas llevadas hasta la fase madura, la lectura cruda queda por debajo de B1: 72.5\% frente a 81.2\% en la línea base y 80.0\% frente a 83.8\% en la mejor condición nativa ($\iota = 0.25$, $\kappa = 0$).»
**Fuente:** `results/exp2_iota_kappa/results_downstream.csv` (3 filas: las dos nativas y la división entre la media de la memoria, que no es nativa); el grid de 28 celdas tiene solo la fase temprana.

### E6. Tabla de capacidad: qué es «Enrutamiento» (05:261)
**Viejo:** «``Enrutamiento'' es la precisión del directorio de labels;»
**Nuevo:** «``Enrutamiento'' es la precisión temprana sobre 80 consultas (reconocimiento por el contenido llenado con $N$ imágenes, sin directorio);»
**Fuente:** `run_experiment6.py:121–136, 181–182` (`early_accuracy`). Coincide con 81.2 % del protocolo temprano. Lo mismo en 05:290 («El enrutamiento de labels crece…» → «La precisión temprana crece…»).

### E7. La entropía no crece «de forma logarítmica» (05:291–292)
**Viejo:** «la entropía de la memoria de contenido crece de forma logarítmica con $N$»
**Nuevo:** «la entropía de la memoria de contenido crece con $N$ y se satura (3.65, 4.37, 4.95, 5.20 y 5.32 bits)»
**Fuente:** `results/exp6_capacity/results_capacity.csv`.

### E8. Fase A: «perfectamente balanceada» (05:310–312)
**Viejo:** «con entropía de \textbf{3.000 bits}: el máximo teórico, especialización visual perfectamente balanceada.»
**Nuevo:** «con entropía de \textbf{3.000 bits} al tercer decimal, el máximo con ocho módulos.»
**Fuente:** log de la etapa 7 (entropía 2.99996).

### E9. Experimento 13: el 73.6 % es con una variante, no con 4 (05:329–334)
**Viejo:** «El experimento 13 lo mide: con 16 variantes por percepción en el directorio, frente a 4, el directorio visual acepta el 96.2\,\% de las imágenes de test en lugar del 73.6\,\%, y con 16 variantes también en el contenido la cobertura de punta a punta pasa de 66.5 a 94.5\,\%. Con 4 variantes no hay ruteos falsos; con 16, el sistema rutea mal dos de las 656 imágenes (Sección~\ref{sec:limitaciones}).»
**Nuevo:**
```latex
El experimento 13 lo mide sobre las 656 imágenes de test: registrar en el directorio 16
variantes por percepción, en lugar de una, lleva su aceptación del 73.6 al 96.2\,\%
(con 4 variantes, 87.7\,\%), y con 16 variantes también en el contenido la cobertura de
punta a punta pasa de 66.5 a 94.5\,\%. En ese experimento, con una o 4 variantes en el
directorio no hay ruteos falsos y con 16 hay uno; el sistema, con sus 16 variantes,
rutea mal dos de las 656 imágenes (Sección~\ref{sec:limitaciones}).
```
**Fuente:** `results/experimento13/README.md`: A0 (Vd = 1) 73.6, falso 0.0; A1 Vd = 4 87.7, falso 0.0; A1 Vd = 16 96.2, falso 0.2; A3 V = 16 punta a punta 94.5 (verificado).

### E10. Evocación: sobre qué imágenes (05:336–339 y pie de la figura 16, 05:389–390)
**Párrafo, viejo:** «Sobre las imágenes de evaluación aceptadas, la evocación inversa…»
**Nuevo:** «Sobre las primeras 15 imágenes de test de cada clase que el ruteo acepta (116 de 120), la evocación inversa desde el módulo destino…»
**Pie, viejo:** «Sobre el test completo, con el directorio, la evocación acierta el 97.4\%.»
**Nuevo:** «Con el directorio, sobre las primeras 15 imágenes de test de cada clase que el ruteo acepta (116), la evocación acierta el 97.4\% (113).»
**Fuente:** `src/stage7_bidirectional.py:40` (`N_EVOKE = 15`) y `:243`; log de la etapa 7: «113/116 = 97.4%» (verificado). Lo mismo en 06:243, 06:293, 07:20–21 y 04:241 (métrica).

### E11. Razón de distancia de los grises (05:353–355)
**Viejo:** «Los grises de nivel 120 a 160 (el del panel, 127, cae en ese tramo) los aceptan a la vez \texttt{cow}, \texttt{dog} y \texttt{horse}, aunque la instancia real más cercana está a entre 2.4 y 4.4 veces la mediana de la distancia intraclase.»
**Nuevo:** «…aunque la instancia real más cercana está a entre 2.4 y 2.9 veces la mediana de la distancia intraclase.»
**Fuente:** `results/experimento14/README.md`, grises 120–160: 13.9/5.7 a 16.5/5.7 (verificado); el 4.4 es del gris 104 (29.5/6.7), que acepta solo `dog`.
**Nota:** este párrafo y el pie de la figura 15 describen el gris aceptado; cambian cuando se regenere la figura con τ (va en la propuesta de figuras).

### E12. Los intervalos se solapan (05:411–413 y 06:198–199)
«con intervalos de 95\,\% que casi se tocan» → «con intervalos de 95\,\% que se solapan». En 06: «con intervalos que casi se tocan» → «con intervalos que se solapan».
**Fuente:** `experimento11/README.md`, N = 25: [97.4, 97.8] y [96.3, 97.6] comparten [97.4, 97.6] (verificado).

### E13. Qué mide el máximo de `compat` (05:423–424)
**Viejo:** «y su patrón tiene soporte en una sola clase en el 74--77\,\% de las coordenadas;»
**Nuevo:** «y ninguna clase por sí sola sostiene más del 74--77\,\% de las coordenadas de su patrón;»
**Fuente:** `run_experiment11_monolithic.py:320–326` (definición de `compat`); `experimento11/README.md`, compat máx 0.74–0.77.

### E14. «Quedaron iguales en todos los experimentos» (05:455–462)
**Viejo:** «Contención, rechazo, ruteo visual y fidelidad quedaron iguales en todos los experimentos. Solo cambian los recuerdos y las evocaciones muestreados, tanto como al cambiar la semilla, y una parte pequeña de los destinos tempranos donde el directorio se forma con las lecturas de etiquetas (el 1.3\,\% en la línea base de la sección anterior).»
**Nuevo:**
```latex
En imagen, contención, rechazo, ruteo y evocación dan las mismas decisiones imagen por
imagen (631 de 656 en el ruteo de test, 113 de 116 en la evocación).
En texto cambian los recuerdos muestreados, tanto como al cambiar la semilla, y una
parte pequeña de las decisiones donde pesan las lecturas de etiquetas: el 1.3\,\% de
los destinos del protocolo en la comparación con una sola EHAM, una consulta de 80 en
la curva de capacidad con 50 imágenes por clase, y las columnas con $\kappa > 0$ del
barrido, cuyos cuantiles se recalculan sobre la lectura.
```
**Fuente:** `UNA_HETERO.md` («Verificación»; grupo 1: exp6 N = 50, 71.2 → 72.5 %, y cuantiles de κ; grupo 2: 273 de 20 520 = 1.3 %).

### E15. Restos de historia con texto nuevo
- 05:51–52: «\paragraph{B1 sigue siendo la corrección irreducible.} Igual que en el sistema de tres módulos, la lectura cruda…» → «\paragraph{B1 es la corrección que no se puede sustituir.} La lectura cruda…» (la segunda mitad ya está en el replanteamiento).
- 05:95: «\paragraph{El sesgo hacia \texttt{apple} quedó esencialmente resuelto.}» → «\paragraph{Con B1, la participación de \texttt{apple} queda cerca del ideal.}»
- 05:96: «Con el encoder determinista oficial y el vocabulario por masa asociativa, la participación…» → «La participación…».
- 05:197–199: «pero la mejora no se traslada de forma sustancial a la fase madura (B1: 83.8\% frente a 81.2\%) y el patrón destructivo reaparece:» → «y en la fase madura sube de 81.2 a 83.8\% con B1; una poda mayor destruye:» (sin la resta: los valores son 81.25 y 83.75, y la diferencia es 2.5).
- 05:293: «La \textbf{zona de operación} se mantiene en $N = 200$» → «La \textbf{zona de operación} es $N = 200$».

---

## F. Discusión (`06_discusion.tex`)

### F1. El sesgo hacia `apple`: lo que sí está medido (06:58–76)
**Viejo:** la subsección «El sesgo hacia un módulo era un efecto conjunto: encoder y fuente de conocimiento», desde el título hasta «…porque el llenado imagen-etiqueta acopla ambos espacios.»
**Nuevo:**
```latex
\subsection{El sesgo hacia un módulo: masa del directorio y léxico compartido}
\label{sec:disc-dominancia}

Con la lectura cruda, \texttt{apple} gana el 20.5\% de las victorias maduras y
\texttt{cow} el 17.0\%: son los dos módulos con más registros en el directorio (186 y
181, frente a 112 de \texttt{horse}).
La puntuación cruda favorece al que más registró aunque la estructura del directorio
esté casi balanceada (2.974 de 3.000 bits); la lectura B1, que divide entre los
registros, deja a \texttt{apple} en 13.8\% (ideal 12.5\%).
Lo que B1 no corrige es léxico.
De los 28 errores que quedan, 9 son \texttt{pear} $\to$ \texttt{apple} y 6
\texttt{horse} $\to$ \texttt{cow}, pares que comparten etiquetas genéricas
(\textit{fruit} y \textit{pome}; \textit{animal} y \textit{mammal}), y \texttt{pear}
se queda en 76\%.
Si el espacio latente del encoder contribuye también al sesgo no se midió en este
trabajo.
```
**Por qué:** «el sesgo viene también del encoder, en cuyo espacio latente pear y tomato se solapan con apple» no tiene medición en `results/`. Venía del reentrenamiento de una versión anterior. La única medición de solapamiento latente (experimento 12, que la tesis no presenta) da apple–tomato como el par de `apple` menos solapado (0.348) y la brecha no sigue al solapamiento latente (ρ = 0.21, p = 0.29).
**Fuente (verificado):** `ablation_metrics.csv`, N = 400: A `winner_pct_apple` 0.205, `winner_pct_cow` 0.17; registros apple 186, cow 181, horse 112; `mdir_entropy` 2.9738; B1 `winner_pct_apple` 0.1375, `cm_pear_apple` 9, `cm_horse_cow` 6, `mature_acc_pear` 0.76; `labels_*.json` (fruit y pome en apple y pear; animal y mammal en cow y horse).

### F2. El enriquecimiento de vocabulario no tiene archivo (06:78–90, 06:120–122, limitación h, 07:72–74)
- **06:78–90** («Del trabajo sobre el vocabulario queda un resultado…» hasta «…podaba \textit{drink} y \textit{mug}).»): **quitar**.
- **06:120–122, viejo:** «La palanca no es más vocabulario del especialista sino mejores señas del que consulta, como muestra el resultado de enriquecimiento (Sección~\ref{sec:disc-dominancia}).» **Nuevo:** «Las señas del que consulta pesan: la regla de rescate léxico, que solo admite tokens de la consulta como \textit{bark}, \textit{moo} o \textit{riding}, sube 21.7 puntos en las 46 consultas que toca (Sección~\ref{sec:pipeline-semantico}).»
- **Limitación (h), nuevo:** «El vocabulario de ConceptNet es asimétrico entre clases, y el techo de las clases de léxico compartido (\texttt{pear} 76\%, \texttt{horse} 88\%) depende de la distintividad de las consultas del banco tanto como del vocabulario del módulo. Este trabajo no midió si enriquecer el vocabulario de una clase lo corrige.»
- **07:72–74, viejo:** «…con conocimiento alineado al lenguaje de las consultas, único tipo de enriquecimiento que demostró ayudar.» **Nuevo:** «…con conocimiento alineado al lenguaje de las consultas.»
**Fuente:** búsqueda de *bosc*, *anjou*, *World Cup*, *enriquec*, *sauce* en `results/`: sin artefactos del experimento. `results/rescate_lexico/README.md`: 46 consultas, 43 contra 33, +21.7.

### F3. La comunicación distintiva, con todos los datos (06:114–118)
**Viejo:** «Las clases cuyas consultas usan léxico exclusivo (\texttt{cup}, \texttt{tomato}, \texttt{car}) alcanzan 98--100\%; las que preguntan con léxico compartido (\texttt{pear}, \texttt{horse}) quedan en 76 y 88\%.»
**Nuevo:** «Con la lectura B1, \texttt{car}, \texttt{cow}, \texttt{cup} y \texttt{tomato} quedan en 98--100\% y \texttt{dog} en 93.9\%; las que pierden son \texttt{pear} (76\%), \texttt{horse} (88\%) y \texttt{apple} (88.2\%), y pierden hacia una vecina con la que comparten etiquetas: \texttt{pear} $\to$ \texttt{apple} (9 de sus 12 errores), \texttt{horse} $\to$ \texttt{cow} (6 de 6), \texttt{apple} $\to$ \texttt{pear} y $\to$ \texttt{tomato} (3 y 3).»
**Por qué:** la versión vieja deja fuera a `cow` (100 %, comparte léxico con `horse`) y a `apple` (88.2 %). Fuente: `ablation_metrics.csv`, B1, N = 400.

### F4. «Hoy se trata igual que un rechazo» contradice 05 (06:174–175)
**Viejo:** «En este sistema el estado aparece en cuanto hay datos sin pareja, y hoy se trata igual que un rechazo.»
**Nuevo:** «En este sistema el estado aparece en cuanto hay datos sin pareja: de 800 imágenes registradas sin palabra, 78 quedan reconocidas sin nombre (Sección~\ref{sec:una-memoria}). La lectura de familiaridad las distingue de un rechazo; el protocolo de respuesta todavía no las usa.»
**Fuente:** `results/homo_marginal/README.md`, sección E, parte 1.

### F5. De qué se compone el 2.5 % sin respuesta (06:200–203)
**Viejo:** «El precio es cobertura: el containment de un especialista es estricto en las 64 coordenadas del latente y deja sin respuesta al 2.5\,\% de las imágenes de prueba con 200 por clase»
**Nuevo:** «El precio es cobertura: el especialista deja sin respuesta al 2.5\,\% de las imágenes de prueba con 200 por clase, 1.2 puntos porque la contención es estricta en las 64 coordenadas del latente y 1.3 porque el recuerdo no devuelve palabras»
**Fuente:** `experimento11/README.md`, N = 200, imagen → texto, T-oráculo: acepta 98.8, responde 97.5 (verificado).

### F6. Desenfoques bajo τ (06:256–258)
«desenfoques de radio $\geq 12$» → «desenfoques fuertes (todos los de radio $\geq 12$ y buena parte de los menores)». Fuente: `experimento14/README.md`, normas por entrada.

### F7. Restos de historia con texto nuevo
- 06:54: «vuelven a quedar por debajo» → «quedan por debajo».
- 06:25 «la representación ya no los agrava»: el replanteamiento §4a deja esa frase igual y A2 no la toca. La reescribe la propuesta de prosa de 06–07 (punto 1.5).

---

## G. Conclusiones (`07_conclusiones.tex`)

El replanteamiento reescribe la apertura, la respuesta a la pregunta, las lecciones y el cierre; con los ajustes A4 y A5. Quedan estos, en «Logros», «Frente a una EHAM única» y «Una memoria de contenido».

### G1. Alcance de «sin supervisión» (07:9–10)
**Viejo:** «…con rechazo claro en ambas direcciones, sin clasificadores externos ni umbrales supervisados.»
**Nuevo:** «…con rechazo claro en ambas direcciones, sin clasificadores ni umbrales supervisados en la toma de decisiones.»
**Por qué:** el encoder se entrena con una cabeza de clasificación ($\text{MSE} + 0.1\cdot\text{CE}$), que no decide nada en el sistema (04:126–134).

### G2. Logros: dentro de muestra, evocación, balance y atribuciones (07:13–28)
- 07:13: «Sobre el banco de 411 consultas ($N = 400$, 5 semillas), el sistema alcanzó…» → «Sobre el banco de 411 consultas ($N = 400$, 5 semillas; la fase madura se evalúa sobre las consultas que formaron el directorio), el sistema alcanzó…». Y tras «(ideal 12.5\%).» agregar: «Sobre 171 consultas reservadas, el protocolo rutea correctamente el 97.0\% con 200 imágenes por clase (experimento 11).»
- 07:20–21: «y una evocación de dominio del \textbf{97.4\%};» → «y, sobre las primeras 15 imágenes de prueba de cada clase (116 aceptadas), una evocación de dominio del \textbf{97.4\%};».
- 07:21–22: «su directorio alcanzó el balance perfecto: \textbf{3.000 de 3.000 bits} de entropía.» → «el registro completo de sus percepciones quedó balanceado: \textbf{3.000 bits} de entropía, el máximo con ocho módulos.»
- 07:26–28: «ningún falso aceptado al llenar con un latente por imagen, y 5 de 656 imágenes de test (0.8\%), todas entre animales, con el llenado de 16 variantes.» → «ningún falso aceptado al llenar con un latente por imagen (curva de capacidad), y 5 de 656 imágenes de test (0.8\%), todas entre animales, con el llenado de 16 variantes del experimento 13.»
**Fuentes:** E1, E10, E8; `results/experimento13/README.md` (A3 V = 16: falso contenido 0.8); `exp6_capacity/results_capacity.csv` (`cross_false` 0.0).

### G3. La familiaridad resiste más «ante el mismo daño» (07:52–54)
**Viejo:** «…y ante daño la familiaridad leída de la hetero resiste más que una memoria homo aparte.»
**Nuevo:** «…y, ante el mismo daño en todas las memorias, la familiaridad leída de la hetero resiste más que la de una memoria homo aparte (con el 1\,\% de las celdas destruidas, 800 frente a 416 de 800 imágenes).»
**Por qué:** una homo aparte e intacta conserva 800 de 800 en todo el rango; la frase sin la condición contradice esa columna de la tabla de lesión. Fuente: `results/homo_marginal/README.md`, sección E, parte 2. La misma frase está en `revision_una_hetero_prosa.md:499`.

---

## H. Hechos que salieron al consolidar (el texto nuevo está en las propuestas de prosa)

| # | Hallazgo | Verificado | Dónde está el texto nuevo |
|---|---|---|---|
| H1 | En texto, la calibración, el protocolo completo, el barrido ι × κ y la curva de formación registran cada transacción en el directorio de **todos** los módulos: en la práctica, un directorio compartido. Los directorios perspectivales de 03 solo se usan en el hemisferio visual y en el experimento 11 (texto sobre 171 consultas reservadas). 04 no lo dice, y el lector supone que el 93.0 % sale de directorios perspectivales. | `run_ablation.py:309–312`, `run_experiment3.py:122–125`; el experimento 11 usa `route_transactive`. | `revision_consejo_prosa_03_04.md`, punto 1.4 (párrafo nuevo en 04). |
| H2 | La entropía de la EHAM se promedia sobre pares de características $(i, j)$, no sobre valores $(a_i, b_j)$ (02:155–158). | `src/hetero_lib/hetero_associative_4d.py:601–611`. | `revision_consejo_prosa_main_01_02.md`, 1.6. |
| H3 | 02:167–170 dice que los métodos de la pista faltante son «el parche» para otro caso; la recuperación por defecto del sistema, *sample-and-search*, es uno de ellos, y la búsqueda local corre siempre, no «cuando es necesario» (02:221–223). | `src/hetero_memory.py:28–35, 91, 106`. | `revision_consejo_prosa_main_01_02.md`, 1.7. |
| H4 | Limitación (b): «siempre el par animal que ya confunde al texto» no se cumple. De los cinco falsos de contenido del experimento 13, cuatro los acepta `dog` (dos vacas, dos caballos) y uno `cow` (`horse8`). | `results/experimento13/raw/Vc16_N200_Vd16_s42.json`. | `revision_consejo_prosa_06_07.md`, 1.2. |

---

## Decisiones que te tocan

**D1. Escala min-max del latente.** La tesis (04:142–145) dice que la escala se calculó con cuatro variantes por imagen, y es verdad para el archivo con que se midió todo: `models/latent_global_stats.json` (del 5 de julio) coincide con las variantes 0–3. Pero el código (`src/stage5_fill.py:119–145`) reutiliza ese archivo si existe y, si no existe, lo recalcula con lo que haya en el pool de llenado, que hoy son 16 variantes. Una réplica desde cero cuantizaría el latente con otra escala. Esto ya pasó en la medición del costo, que partió de cero; para el cronómetro no importa.
- **(a) Declararlo y fijar el código** (recomendado). En la tesis: «…con el original, el espejo y las rotaciones de $\pm 12^{\circ}$ de cada imagen (6400 latentes), y se guarda con el modelo». En el código: que `compute_global_latent_stats` use las variantes 0–3. Costo: una edición de texto y unas cinco líneas de código, cuando termine la medición. No cambia ninguna cifra.
- **(b) Recalcular con 16 y volver a llenar.** Cambia la cuantización de todo el hemisferio visual: habría que re-correr la batería visual (decenas de horas, como la re-corrida de una hetero). No lo recomiendo ahora.

**D2. Los dos falsos enrutamientos son vistas de `horse7`.** Lo dicen 05:321–322, 06 y 07, pero el log de la etapa 7 solo imprime 631/656, sin las imágenes; la identidad consta en una nota de trabajo del 23 sep.
- **(a) Quitar la identidad** y dejar «dos falsos enrutamientos» (recomendado si no quieres correr nada). Costo: tres frases.
- **(b) Verificarla.** Sacar la lista por imagen de la etapa 7 y guardarla en `results/`. Costo: unas 5 líneas de código para imprimirla y una corrida de la etapa 7 en CPU (unos 38 min), después de la medición del costo.

**D3. El experimento 12 no está en la tesis.** El texto nuevo de F1 no lo cita, para no meter un experimento que la tesis no presenta. Si prefieres conservar la evidencia de que el latente no explica el sesgo, habría que presentar el experimento 12 en resultados (un párrafo y una tabla corta).
