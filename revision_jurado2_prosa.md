# Propuesta viejo/nuevo: segunda lectura del jurado (prosa)

**Estado:** aprobada y aplicada. Para que el Resumen cupiera en una página, el autor aprobó dos recortes sobre B1: «Un grupo recuerda más que cada uno de sus miembros cuando cada uno sabe quién sabe qué» y «(81.2 frente a 76.0--81.5\,\% en 80 consultas)». El Resumen y el Abstract van sin número de página, como la Introducción, porque las palabras clave chocaban con él.

**Base:** `6b127f6` más el parche A. Las líneas son las del árbol con A aplicado. `07:17` es `.tex8/secciones/07_conclusiones.tex`, línea 17; al lado va la línea del `.tex_uacj/CapituloN.tex` que genera `generar_capitulos.py`. Los cambios a los capítulos 2 a 5 se hacen en `.tex8/secciones/` y se regeneran.

**Cómo se cotejó:** cada «Viejo» aparece una sola vez en su archivo (lo comprobó el script que aplicó B). Cada cifra nueva o movida trae su archivo de `results/`.

---

## Parte 1. Cambios del parche B

### B1. Resumen: enrutamiento de texto y rechazo

- **Dónde:** `.tex_uacj/Resumen.tex:15`
- **Viejo:**
```latex
Al enrutar texto, el sistema iguala a decisores simples que usan las mismas
representaciones (96.8\,\% sobre 171 consultas reservadas, contra 96.9\,\% de una sola
memoria con las ocho clases).
Rechaza lo que no conoce: acepta 2 de 40 consultas fuera de dominio, contra las 40 de los
decisores de coseno.
```
- **Nuevo:**
```latex
Al enrutar texto, el sistema iguala a decisores simples sobre las mismas
representaciones (81.2 frente a 76.0--81.5\,\% en 80 consultas que casi nunca nombran su
clase) y a una sola memoria con las ocho clases (96.8 frente a 96.9\,\% sobre 171
consultas reservadas).
Rechaza lo que no conoce: acepta 2 de 40 consultas fuera de dominio, igual que un voto
por vocabulario y frente a las 40 de los decisores de coseno; con imágenes reales de
otras categorías no se midió.
```
- **Fuente:** `results/lineas_base/README.md` (proto80: sistema 81.25; decisores 76.0 a 81.5; 11 de 80 con el nombre de la clase; voto y fase temprana aceptan las mismas 2 de 40, compuerta = pertenencia al vocabulario en los 3064 pares); `results/experimento11_protocolo_corregido/ruteo/ruteo.md` (N = 200: 96.8 frente a 96.9).

### B2. Resumen: objetos nuevos

- **Dónde:** `.tex_uacj/Resumen.tex:26`
- **Viejo:**
```latex
Con objetos que ningún módulo vio, la cobertura es del 89.2\,\%, y del 87.6\,\% si el
codificador tampoco los vio.
```
- **Nuevo:**
```latex
Con objetos que ningún módulo vio, la cobertura es del 89.2\,\%, y del 87.6\,\% si el
codificador tampoco los vio, pero con 136 falsos enrutamientos de 3280 en lugar de 2.
```
- **Fuente:** `results/objetos_nuevos_codificador_por_pliegue/README.md`, tabla de comparación: falsos ruteos con objeto nuevo 2 frente a 136 de 3280 (4.1 %; el porcentaje se omite por espacio).

### B3. Abstract: enrutamiento de texto y rechazo

- **Dónde:** `.tex_uacj/Abstract.tex:14`
- **Viejo:**
```latex
When routing text, the system matches simple decision rules that use the same
representations (96.8\,\% on 171 held-out queries, against 96.9\,\% for a single memory
holding the eight classes).
It rejects what it does not know: it accepts 2 of 40 out-of-domain queries, against all
40 for the cosine rules.
```
- **Nuevo:**
```latex
When routing text, the system matches simple decision rules on the same
representations (81.2 against 76.0--81.5\,\% on 80 queries that seldom name their class)
and a single memory holding the eight classes (96.8 against 96.9\,\% on 171 held-out
queries).
It rejects what it does not know: it accepts 2 of 40 out-of-domain queries, like a
vocabulary vote, against all 40 for the cosine rules; rejection of real images from
other categories was not measured.
```
- **Fuente:** Las mismas que en el Resumen.

### B4. Abstract: objetos nuevos

- **Dónde:** `.tex_uacj/Abstract.tex:25`
- **Viejo:**
```latex
On objects no module has seen, coverage is 89.2\,\%, and 87.6\,\% when the encoder has not
seen them either.
```
- **Nuevo:**
```latex
On objects no module has seen, coverage is 89.2\,\%, and 87.6\,\% when the encoder has not
seen them either, but with 136 false routings of 3280 instead of 2.
```
- **Fuente:** Las mismas que en el Resumen.

### B5. Objetivo general, arquitectura

- **Dónde:** `.tex_uacj/ConclusionObjetivoGeneral.tex:9`
- **Viejo:**
```latex
Registrar, reconocer, recuperar y enrutar son operaciones de las memorias
(Sección~\ref{sec:operaciones}).
Una sola memoria de contenido por módulo basta: los pesos de cada dominio se leen de la
memoria heteroasociativa, y con ellos el sistema toma las mismas decisiones que con
memorias homoasociativas separadas (Sección~\ref{sec:una-memoria}).
```
- **Nuevo:**
```latex
Registrar, reconocer, recuperar y enrutar son operaciones de las memorias
(Sección~\ref{sec:operaciones}); la suma por tokens, la lectura B1, el umbral $\tau$ y el
rescate léxico operan fuera de ellas (Sección~\ref{sec:auditoria}).
Una sola memoria de contenido por módulo basta: los pesos de cada dominio se leen de la
memoria heteroasociativa, y con ellos el sistema toma las mismas decisiones que con
memorias homoasociativas separadas en imagen y casi todas en texto (cambian algunos
destinos del protocolo y una consulta de 80 en la curva de capacidad;
Sección~\ref{sec:una-memoria}).
```
- **Fuente:** Las cuatro operaciones externas: Sección de auditoría (`04_metodologia.tex`, «Fuera de las memorias quedan cuatro operaciones»). Decisiones: Sección de una memoria (`05_resultados.tex`, «Cambian algunos destinos del protocolo … y una consulta de 80 en la curva de capacidad»); `results/homo_marginal/README.md` (imagen: 0 decisiones distintas).

### B6. Objetivo general, formación del directorio

- **Dónde:** `.tex_uacj/ConclusionObjetivoGeneral.tex:22`
- **Viejo:**
```latex
El directorio reproduce, entonces, la decisión del mediador sin difundir la consulta a
todos los módulos, con el mismo acierto.
```
- **Nuevo:**
```latex
El directorio coincide, entonces, con la decisión del mediador en el 92.5\,\% de las
consultas evaluadas (sorteo principal), con un acierto equivalente y sin difundir la
consulta a todos los módulos.
```
- **Fuente:** `results/calibracion_evaluacion_fija/README.md`, sorteo principal E0: fidelidad de B1 92.5 con N = 200 y N = 291.

### B7. Objetivo general, decisores simples

- **Dónde:** `.tex_uacj/ConclusionObjetivoGeneral.tex:31`
- **Viejo:**
```latex
Sobre las 80 consultas más difíciles del banco, en las que solo 11 traen el nombre de
```
- **Nuevo:**
```latex
Sobre las 80 consultas del protocolo completo, en las que solo 11 traen el nombre de
```
- **Fuente:** Nombre que usa el resto del reporte (`05_resultados.tex`, `06_discusion.tex`, `07_conclusiones.tex`); son las primeras 80 del banco, no una selección por dificultad (`results/lineas_base/README.md`, partición proto80).

### B8. Objetivo general, rechazo

- **Dónde:** `.tex_uacj/ConclusionObjetivoGeneral.tex:44`
- **Viejo:**
```latex
De las 40 consultas fuera de dominio, el sistema acepta 2 con 25, 50, 100 y 200 imágenes
por clase.
La memoria única acepta 2, 2, 5 y 8 de 40 con esos mismos tamaños, y los
decisores de coseno aceptan las 40.
```
- **Nuevo:**
```latex
De las 40 consultas fuera de dominio, el sistema, con la doble compuerta, acepta 2 con
25, 50, 100 y 200 imágenes por clase, y la memoria única 2, 2, 5 y 8; la segunda
compuerta se decidió después de ver estas consultas (limitación (g)).
Los decisores de coseno aceptan las 40.
```
- **Fuente:** `results/experimento11_protocolo_corregido/README.md` (solo ruteo, fuera de dominio: protocolo con compuerta 5 % = 2 de 40 en los cuatro cortes; EHAM única 5.0, 5.0, 12.5 y 20.0 % = 2, 2, 5 y 8 de 40); limitación (g).

### B9. Objetivo específico 1

- **Dónde:** `.tex_uacj/Capitulo1.tex:116`
- **Viejo:**
```latex
    Verificar que todas las decisiones salen de operaciones de las memorias y que una
    sola memoria de contenido por módulo basta para tomarlas.
```
- **Nuevo:**
```latex
    Identificar qué decisiones salen de operaciones de las memorias y cuáles de
    componentes externos, y verificar que una sola memoria de contenido por módulo basta
    para tomarlas.
```
- **Fuente:** Sin cifras.

### B10. Limitaciones en el planteamiento

- **Dónde:** `.tex_uacj/Capitulo1.tex:220`
- **Viejo:**
```latex
el punto de control del codificador y el número de variantes se eligieron mirando el
conjunto de prueba (limitación (g));
```
- **Nuevo:**
```latex
el punto de control del codificador y el número de variantes se eligieron con el
conjunto de prueba (limitación (g));
```
- **Fuente:** Sin cifras.

### B11. Introducción, organización

- **Dónde:** `.tex_uacj/Introduccion.tex:33`
- **Viejo:**
```latex
Capítulos~\ref{sec:marco_teorico} a~\ref{conclusiones} presentan el marco teórico, el
desarrollo, los resultados y las conclusiones.
```
- **Nuevo:**
```latex
Capítulos~\ref{sec:marco_teorico} a~\ref{conclusiones} presentan el marco teórico, el
desarrollo, los resultados y las conclusiones, y el Apéndice~\ref{apendiceA} ubica cada
experimento citado.
```
- **Fuente:** Etiqueta `apendiceA` en `ApendiceA.tex:1`.

### B12. Subtítulo

- **Dónde:** `.tex_uacj/tesis_uacj.tex:65`
- **Viejo:**
```latex
{\large Ocho módulos sobre ETH-80 completo}
```
- **Nuevo:**
```latex
{\large Ocho módulos sobre el conjunto ETH-80}
```
- **Fuente:** Sin cifras.

### B13. Apéndice A, archivos fuera del repositorio

- **Dónde:** `.tex_uacj/ApendiceA.tex:6`
- **Viejo:**
```latex
Todas las cifras del reporte salen de esas carpetas del repositorio del proyecto, salvo
la comparación con la batería completa, marcada «sin carpeta», cuyos registros están en
\texttt{logs\_comparacion/}.
```
- **Nuevo:**
```latex
Todas las cifras del reporte salen de esas carpetas del repositorio del proyecto, salvo
la comparación con la batería completa, marcada «sin carpeta», cuyos registros están en
\texttt{logs\_comparacion/}.
Quedan fuera del repositorio los modelos entrenados (\texttt{models/*.pt} y
\texttt{models/*.pkl}), los registros por consulta (\texttt{raw/}) del protocolo
transactivo del experimento 11 (23\,MB) y los codificadores reentrenados por pliegue,
como declaran el \texttt{.gitignore} y los README de esas carpetas.
```
- **Fuente:** `.gitignore` (models/*.pkl, models/*.pt); `results/experimento11_protocolo_corregido/README.md` («raw/ no se copió a este repositorio (23 MB, 480 archivos)»); `results/objetos_nuevos_codificador_por_pliegue/README.md` («Fuera de git, en models/codificador_por_pliegue/pliegue_<k>/»). `LEEME_RESTAURAR.md` no existe en `6b127f6` ni en `origin/una-hetero`: no se cita.

### B14. Apéndice A, reanálisis

- **Dónde:** `.tex_uacj/ApendiceA.tex:26`
- **Viejo:**
```latex
Relecturas del banco y de corridas ya versionadas pedidas por la lectura de
jurado, como cuántas consultas traen el nombre de su clase.
```
- **Nuevo:**
```latex
Relecturas del banco y de corridas ya versionadas, como cuántas consultas traen
el nombre de su clase.
```
- **Fuente:** Sin cifras.

### B15. Apéndice A, calibración

- **Dónde:** `.tex_uacj/ApendiceA.tex:30`
- **Viejo:**
```latex
Sesgo del directorio hacia un módulo bajo nueve condiciones de lectura y
registro (A a G),
```
- **Nuevo:**
```latex
Sesgo del directorio hacia un módulo bajo nueve condiciones de calibración
(A a G),
```
- **Fuente:** Sin cifras.

### B16. Apéndice A, protocolo

- **Dónde:** `.tex_uacj/ApendiceA.tex:128`
- **Viejo:**
```latex
\raggedright Protocolo corregido (exp.~11) & \raggedright \ref{sec:eham-unica},
\ref{sec:lineas-base} &
\raggedright El experimento 11 con los directorios perspectivales reiniciados en cada
trabajo. &
```
- **Nuevo:**
```latex
\raggedright Protocolo transactivo (exp.~11) & \raggedright \ref{sec:eham-unica},
\ref{sec:lineas-base} &
\raggedright El protocolo transactivo del experimento 11, con directorios perspectivales
formados desde cero en cada semilla y corte. &
```
- **Fuente:** Sin cifras; `results/experimento11_protocolo_corregido/README.md` («directorios nuevos en cada (semilla, corte)»).

### B17. Conclusiones, resultados principales

- **Dónde:** `07:17` (`.tex_uacj/Capitulo5.tex:18`)
- **Viejo:**
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
```
- **Nuevo:**
```latex
\paragraph{Resultados principales.}
Con conjuntos evaluados fijos de 120 consultas que nunca se registran en el directorio,
la fase madura con la lectura normalizada alcanza el \textbf{91.0\,\%} con 291 consultas
de formación, frente al \textbf{89.7\,\%} de la temprana (promedio de cinco sorteos), sin
superarla de forma robusta ($+0.2$ puntos con 200 consultas de formación y $+1.3$ con
291); con la lectura cruda queda 7.5 puntos por debajo
(Sección~\ref{sec:calibracion-fija}).
Dentro de muestra, sobre 400 consultas del banco de 411 que también forman el
directorio, la precisión temprana es del 90.0\,\% y la madura del 93.0\,\%, con una
concordancia temprana-madura del 95.8\,\%.
```
- **Fuente:** `results/calibracion_evaluacion_fija/README.md`, cinco sorteos: B1 91.0 con N = 291, temprana 89.7, diferencias +0.2 y +1.3; A 82.2 (−7.5). `results/ablation_mdir_bias/ablation_report.md`: N = 400, temprana 90.0, B1 93.0, fidelidad 95.75.

### B18. Conclusiones, cita del experimento 13

- **Dónde:** `07:48` (`.tex_uacj/Capitulo5.tex:49`)
- **Viejo:**
```latex
(0.8\,\%), todas entre animales, con el llenado de 16 variantes del experimento 13.
```
- **Nuevo:**
```latex
(0.8\,\%), todas entre animales, con el llenado de 16 variantes
(Sección~\ref{sec:hemisferio-visual}).
```
- **Fuente:** `results/experimento13/veredicto.md` (b): 5 imágenes aceptadas por un especialista ajeno (0.8 %). La cifra se agrega a la Sección del hemisferio visual en este mismo parche.

### B19. Conclusiones, rechazo

- **Dónde:** `07:76` (`.tex_uacj/Capitulo5.tex:78`)
- **Viejo:**
```latex
Lo que agrega es un rechazo sin umbral ajustado.
Los decisores de coseno aceptan las 40 consultas fuera de dominio y el sistema 2, aunque
en texto ese rechazo vale lo que una búsqueda léxica.
```
- **Nuevo:**
```latex
Lo que agrega es un rechazo que en texto no usa umbral, aunque equivale a la pertenencia
al vocabulario, y que en imagen depende del umbral de energía $\tau$.
Los decisores de coseno aceptan las 40 consultas fuera de dominio y el sistema 2, como un
voto por vocabulario; frente a la EHAM única, la ventaja depende de una segunda
compuerta decidida después de ver esas consultas (limitación (g)).
```
- **Fuente:** `results/lineas_base/README.md` (compuerta = pertenencia al vocabulario en los 3064 pares; voto y EAM aceptan las mismas 2 de 40); limitación (g).

### B20. Conclusiones, formación del directorio

- **Dónde:** `07:99` (`.tex_uacj/Capitulo5.tex:101`)
- **Viejo:**
```latex
consultas de formación, hasta alcanzar a la temprana (89.7\,\%) sin superarla.
```
- **Nuevo:**
```latex
consultas de formación, hasta alcanzar a la temprana (89.7\,\%), sin una ventaja que se
sostenga entre sorteos ($+1.3$ puntos con 291; de $-0.8$ a $+6.7$ según el sorteo).
```
- **Fuente:** `results/calibracion_evaluacion_fija/README.md`, cinco sorteos: B1 madura − temprana con N = 291, +1.3 (−0.8 a +6.7).

### B21. Conclusiones, EHAM única

- **Dónde:** `07:104` (`.tex_uacj/Capitulo5.tex:106`)
- **Viejo:**
```latex
Con el mismo contenido, el sistema transactivo y una sola memoria con las ocho clases
aciertan la clase lo mismo desde 50 imágenes por clase.
Con 200, sobre el total de las 171 consultas reservadas, aciertan el 96.8 y el
96.9\,\% (diferencia de $-0.1$ puntos, $[-2.9, +2.9]$); con 25, la EHAM única acierta
más (97.6 frente a 93.2\,\%), porque el directorio todavía enruta peor.
El sistema transactivo recuerda con más fidelidad, mezcla menos los dominios cuando la
pista es compartida (acierta la clase entre el 54 y el 71\,\% de esas consultas, frente
al 48--52\,\% de la EHAM única) y en imagen responde con un dominio ajeno menos veces
(3.1\,\% de las imágenes, frente a 10.9\,\% con 200 por clase).
```
- **Nuevo:**
```latex
Con el mismo contenido, en el acierto de clase del sistema transactivo y de una sola
memoria con las ocho clases, la diferencia por consulta no excluye el cero desde 50
imágenes por clase ($-0.7$, $-0.7$ y $-0.1$ puntos con 50, 100 y 200), aunque McNemar
por pares, que trata como independientes las repeticiones de cada consulta, favorece a
la EHAM única con 50 y 100.
Con 200, sobre el total de las 171 consultas reservadas, aciertan el 96.8 y el
96.9\,\% ($[-2.9, +2.9]$); con 25, la EHAM única acierta más (97.6 frente a 93.2\,\%),
porque el directorio todavía enruta peor.
El sistema transactivo recuerda con más fidelidad, mezcla menos los dominios cuando la
pista es compartida (desde 50 imágenes por clase acierta la clase en el 70--71\,\% de
esas consultas, frente al 48--52\,\% de la EHAM única, sobre el 4\,\% de las consultas;
con 25 los intervalos se solapan) y en imagen responde con un dominio ajeno menos veces
(3.1\,\% de las imágenes, frente a 10.9\,\% con 200 por clase).
```
- **Fuente:** `results/experimento11_protocolo_corregido/README.md`, solo ruteo: P − M −0.7 [−3.3, +2.0], −0.7 [−3.4, +2.0], −0.1 [−2.9, +2.9]; McNemar p = 0.039 y 0.020 con 50 y 100. `tablas_nuevas/README.md`: pista compartida, protocolo 70.0, 70.0, 71.4 y EHAM única 47.8, 52.2, 51.1 desde N = 50; fracción 4.1 %; con N = 25, [47.1, 62.7] frente a [42.8, 54.4].

### B22. Conclusiones, una memoria y lesión

- **Dónde:** `07:124` (`.tex_uacj/Capitulo5.tex:126`)
- **Viejo:**
```latex
Con los pesos leídos de la memoria heteroasociativa, el sistema toma las mismas
decisiones y, ante el mismo daño en todas las memorias, la familiaridad leída de ella
resiste más que la de una memoria homoasociativa aparte (con el 1\,\% de las celdas
destruidas, 800 frente a 416 de 800 imágenes).
```
- **Nuevo:**
```latex
Con los pesos leídos de la memoria heteroasociativa, el sistema toma las mismas
decisiones en imagen y casi todas en texto (cambian algunos destinos del protocolo y una
consulta de 80 en la curva de capacidad).
Ante la misma fracción de celdas destruidas en todas las memorias, la familiaridad
leída de ella resiste más que la de una memoria homoasociativa aparte (con el 1\,\% de
las celdas destruidas, 800 frente a 416 de 800 imágenes), por construcción: cada celda
de la lectura suma las de los 17 valores de etiqueta, y una celda de la memoria
homoasociativa es un punto único.
```
- **Fuente:** Sección de una memoria (`05_resultados.tex`: «Cambian algunos destinos del protocolo…», «una celda de la lectura suma las de los 17 valores de etiqueta»); Tabla de lesión (800 y 416 con f = 0.01); limitación (j).

### B23. Conclusiones, información mutua

- **Dónde:** `07:142` (`.tex_uacj/Capitulo5.tex:144`)
- **Viejo:**
```latex
ganador, que con $N = 400$ llega al 88.3\,\% de su máximo con la lectura normalizada y al
81.3\,\% con la cruda.
```
- **Nuevo:**
```latex
ganador, que con $N = 400$, sobre las consultas que formaron el directorio, llega al
88.3\,\% de su máximo con la lectura normalizada y al 81.3\,\% con la cruda; el estimador
la sobrestima en unos 0.09 bits.
```
- **Fuente:** `05_resultados.tex`, calibración: «Se mide sobre las mismas consultas que formaron el directorio, y con N = 400 el estimador la sobrestima en unos 0.09 bits».

### B24. Trabajo futuro, bancos nuevos

- **Dónde:** `07:148` (`.tex_uacj/Capitulo5.tex:154`)
- **Viejo:**
```latex
    \item \textbf{Partición de validación y bancos nuevos} (limitación (g)): elegir el
```
- **Nuevo:**
```latex
    \item \textbf{Partición de validación y bancos nuevos} (limitaciones (g) y (l)): elegir el
```
- **Fuente:** Sin cifras.

### B25. Trabajo futuro, bancos nuevos

- **Dónde:** `07:151` (`.tex_uacj/Capitulo5.tex:157`)
- **Viejo:**
```latex
    imagen y fuera de dominio con bancos nuevos, escritos por terceros, y con una
    partición reservada sorteada en lugar de la cola de la lista de cada clase.
```
- **Nuevo:**
```latex
    imagen y fuera de dominio con bancos nuevos, escritos por terceros sin acceso al
    vocabulario, y con una partición reservada sorteada en lugar de la cola de la lista
    de cada clase.
```
- **Fuente:** Sin cifras; no contradice el dato del autor (el banco actual lo generó un modelo de lenguaje y lo revisó el autor).

### B26. Conclusiones, párrafo final

- **Dónde:** `07:193` (`.tex_uacj/Capitulo5.tex:199`)
- **Viejo:**
```latex
Frente a decisores simples sobre las mismas representaciones, esas memorias no
clasifican mejor; lo que aportan es un rechazo que no necesita umbral ajustado, el
recuerdo del contenido asociado y decisiones que se leen en sus registros.
```
- **Nuevo:**
```latex
Frente a decisores simples sobre las mismas representaciones, esas memorias no
clasifican mejor; lo que aportan es el recuerdo del contenido asociado, decisiones que
se leen en sus registros y un rechazo que en texto no usa umbral, aunque equivale a la
pertenencia al vocabulario, y en imagen depende del umbral de energía $\tau$.
```
- **Fuente:** `results/lineas_base/README.md` (compuerta = pertenencia al vocabulario).

### B27. Discusión, cita del experimento 13

- **Dónde:** `06:202` (`.tex_uacj/Capitulo4.tex:1495`)
- **Viejo:**
```latex
    latente por imagen, en ninguno de los tamaños de llenado probados, y con las 16
    variantes del experimento 13 acepta 5 de 656 imágenes de prueba, todas entre
    animales (vacas y caballos aceptados por \texttt{dog}, un caballo por
    \texttt{cow}).
```
- **Nuevo:**
```latex
    latente por imagen, en ninguno de los tamaños de llenado probados, y con 16
    variantes acepta 5 de 656 imágenes de prueba, todas entre animales (vacas y caballos
    aceptados por \texttt{dog}, un caballo por \texttt{cow};
    Sección~\ref{sec:hemisferio-visual}).
```
- **Fuente:** `results/experimento13/veredicto.md` (b) y párrafo «El precio».

### B28. Discusión, rechazo

- **Dónde:** `06:370` (`.tex_uacj/Capitulo4.tex:1663`)
- **Viejo:**
```latex
\paragraph{Agrega rechazo sin un umbral ajustado.}
```
- **Nuevo:**
```latex
\paragraph{Agrega rechazo sin umbral en texto.}
```
- **Fuente:** Sin cifras.

### B29. Discusión, en suma

- **Dónde:** `06:444` (`.tex_uacj/Capitulo4.tex:1737`)
- **Viejo:**
```latex
Lo que la memoria asociativa agrega es el rechazo sin umbral ajustado, el recuerdo del
contenido asociado y decisiones que se leen en sus registros.
```
- **Nuevo:**
```latex
Lo que la memoria asociativa agrega es el recuerdo del contenido asociado, decisiones que
se leen en sus registros y un rechazo que en texto no usa umbral, aunque equivale a la
pertenencia al vocabulario, y en imagen depende del umbral de energía $\tau$.
```
- **Fuente:** `results/lineas_base/README.md` (compuerta = pertenencia al vocabulario).

### B30. Limitación (a)

- **Dónde:** `06:453` (`.tex_uacj/Capitulo4.tex:1746`)
- **Viejo:**
```latex
Una consulta fuera de dominio que comparte tokens con etiquetas legítimas pasa la
contención textual y llega a algún módulo.
```
- **Nuevo:**
```latex
Una consulta fuera de dominio que comparte tokens con etiquetas legítimas pasa la
contención textual y llega a algún módulo.
Las 40 consultas fuera de dominio casi no los tienen: las 28 que se agregaron a las 12
de la sonda se escribieron sin ninguna palabra del vocabulario de etiquetas, y solo 2 de
las 40 contienen una.
El rechazo textual es así, en parte, consecuencia de cómo se construyó el banco
(limitación (l)), porque la compuerta coincide con la pertenencia al vocabulario
(Sección~\ref{sec:lineas-base}).
```
- **Fuente:** `results/experimento11/consultas_fuera_dominio.txt` (cabecera: regla de las 28 nuevas, «sin ninguna palabra del vocabulario de etiquetas»); `results/lineas_base/README.md` (ood40: 2 con algún token de algún vocabulario; compuerta = vocabulario).

### B31. Limitación (a), cita del experimento 15

- **Dónde:** `06:466` (`.tex_uacj/Capitulo4.tex:1759`)
- **Viejo:**
```latex
Las alternativas medidas rinden menos (experimento 15, sobre las 171 reservadas): que el
contenido decida entre los tres mejores candidatos del directorio baja el acierto de
```
- **Nuevo:**
```latex
Las alternativas medidas rinden menos (Sección~\ref{sec:eham-unica}, sobre las 171
reservadas): que el contenido decida entre los tres mejores candidatos del directorio
baja el acierto de
```
- **Fuente:** Sin cifras nuevas; la cifra 96.8 → 93.6 se agrega a la Sección de la EHAM única.

### B32. Limitación (b), cita del experimento 13

- **Dónde:** `06:478` (`.tex_uacj/Capitulo4.tex:1771`)
- **Viejo:**
```latex
cada una cede solo con sus propias variantes (experimento 13, sobre las 656 imágenes de
prueba): registrar en el directorio 16 variantes por percepción, en lugar de una, lleva
su aceptación de 73.6 a 96.2\,\%; llenar el contenido con 16 variantes por imagen, en
```
- **Nuevo:**
```latex
cada una cede solo con sus propias variantes (Sección~\ref{sec:hemisferio-visual},
sobre las 656 imágenes de prueba): registrar en el directorio 16 variantes por
percepción, en lugar de una, lleva su aceptación de 73.6 a 96.2\,\%; llenar el
contenido con 16 variantes por imagen, en
```
- **Fuente:** Sin cifras nuevas; la cifra 76 → 96 se agrega a la Sección del hemisferio visual.

### B33. Limitación (c), cita del experimento 14

- **Dónde:** `06:501` (`.tex_uacj/Capitulo4.tex:1794`)
- **Viejo:**
```latex
clases (experimento 14), porque 137 de las 152 entradas degeneradas aceptadas por una
clase ajena caen bajo $\tau$ (grises de 104 a 168, contrastes $\leq 0.2$ y desenfoques
```
- **Nuevo:**
```latex
clases (Sección~\ref{sec:hemisferio-visual}), porque 137 de las 152 entradas
degeneradas aceptadas por una clase ajena caen bajo $\tau$ (grises de 104 a 168,
contrastes $\leq 0.2$ y desenfoques
```
- **Fuente:** Sin cifras nuevas; la cifra 137 de 152 se agrega a la Sección del hemisferio visual.

### B34. Limitación (g), cita del experimento 13

- **Dónde:** `06:562` (`.tex_uacj/Capitulo4.tex:1855`)
- **Viejo:**
```latex
    \item las 16 variantes del llenado, adoptadas después de ver el barrido de variantes
    del experimento 13, que mide sobre las 656 imágenes de prueba (16 es el mayor valor
    probado, no un óptimo ajustado);
```
- **Nuevo:**
```latex
    \item las 16 variantes del llenado, adoptadas después de ver el barrido de variantes
    de la Sección~\ref{sec:hemisferio-visual}, que mide sobre las 656 imágenes de
    prueba (16 es el mayor valor probado, no un óptimo ajustado);
```
- **Fuente:** Sin cifras.

### B35. Limitación (g)

- **Dónde:** `06:575` (`.tex_uacj/Capitulo4.tex:1868`)
- **Viejo:**
```latex
Ninguna de estas decisiones introduce un mecanismo ajeno a las memorias, pero pueden
inflar las cifras reportadas.
```
- **Nuevo:**
```latex
Dos de ellas, la lectura B1 y el rescate léxico, operan fuera de las memorias
(Sección~\ref{sec:auditoria}), y todas pueden inflar las cifras reportadas.
```
- **Fuente:** Sección de auditoría (cuatro operaciones fuera de las memorias).

### B36. Limitación (l), nueva

- **Dónde:** `06:619` (`.tex_uacj/Capitulo4.tex:1912`)
- **Viejo:**
```latex
Por qué ocurre se discute en la Sección~\ref{sec:disc-lineas-base}.
```
- **Nuevo:**
```latex
Por qué ocurre se discute en la Sección~\ref{sec:disc-lineas-base}.

\paragraph{(l) Autoría de los bancos de consultas.}
Las 411 consultas del banco y las 40 fuera de dominio se generaron con un modelo de
lenguaje, y el autor las revisó.
De las 28 fuera de dominio que se agregaron a las 12 de la sonda de rechazo consta la
regla con que se escribieron: objetos y escenas de categorías ausentes de ETH-80, sin
ninguna palabra del vocabulario de etiquetas y sin animales ni plantas.
Del banco de 411 no consta con qué acceso al vocabulario se generó; está alineado con
él, porque 402 de las 411 consultas contienen una palabra del vocabulario de su clase
(Sección~\ref{sec:banco}).
Las cifras de texto miden el sistema sobre consultas cercanas a su vocabulario; con un
banco escrito por terceros sin acceso a él no se midió.
```
- **Fuente:** Dato del autor (modelo de lenguaje y revisión). Regla de las 28: cabecera de `results/experimento11/consultas_fuera_dominio.txt`. 402 de 411: Sección del banco (`04_metodologia.tex`, reanálisis M3.1). Del banco de 411 no consta el acceso al vocabulario (`src/eval_bank.py` solo trae las listas; `revision_jurado_metodologia_prosa.md:543`).

### B37. Figura del espacio semántico, sale de la Discusión

- **Dónde:** `06:45` (`.tex_uacj/Capitulo4.tex:1338`)
- **Viejo:**
```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{fig11_semantic_space.png}
    \caption[Espacio semántico de las etiquetas de llenado]{Espacio semántico de las etiquetas de llenado de las ocho clases (vectores
    fastText del vocabulario de la Sección~\ref{sec:pipeline-semantico}).
    Izquierda: proyección en las dos primeras componentes principales (PCA, por sus
    siglas en inglés), con la envolvente y el centroide (estrella) de cada clase; se rotulan solo las etiquetas que comparten dos o tres clases (\textit{fruit},
    \textit{pome}, \textit{red}, \textit{animal}, \textit{mammal} y \textit{table}).
    Derecha: proporción de las 300 componentes que cae en cada uno de los 16 niveles de
    la cuantización por magnitud, para la etiqueta con el nombre de cada clase.}
    \label{fig:espacio-semantico}
\end{figure}
```
- **Nuevo:**
```latex
(se quita; el bloque pasa a 04, ver el punto siguiente)
```
- **Fuente:** Sin cifras.

### B38. Figura del espacio semántico, entra en la Metodología

- **Dónde:** `04:89` (`.tex_uacj/Capitulo3.tex:635`)
- **Viejo:**
```latex
Con esto quedan poblados los 16 niveles (Figura~\ref{fig:espacio-semantico}).
```
- **Nuevo:**
```latex
Con esto quedan poblados los 16 niveles (Figura~\ref{fig:espacio-semantico}).

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{fig11_semantic_space.png}
    \caption[Espacio semántico de las etiquetas de llenado]{Espacio semántico de las etiquetas de llenado de las ocho clases (vectores
    fastText del vocabulario de la Sección~\ref{sec:pipeline-semantico}).
    Izquierda: proyección en las dos primeras componentes principales (PCA, por sus
    siglas en inglés), con la envolvente y el centroide (estrella) de cada clase; se rotulan solo las etiquetas que comparten dos o tres clases (\textit{fruit},
    \textit{pome}, \textit{red}, \textit{animal}, \textit{mammal} y \textit{table}).
    Derecha: proporción de las 300 componentes que cae en cada uno de los 16 niveles de
    la cuantización por magnitud, para la etiqueta con el nombre de cada clase.}
    \label{fig:espacio-semantico}
\end{figure}
```
- **Fuente:** Sin cifras.

### B39. Hemisferio visual, variantes (cifra antes solo en la limitación (b))

- **Dónde:** `05:542` (`.tex_uacj/Capitulo4.tex:545`)
- **Viejo:**
```latex
El experimento 13 lo mide sobre las 656 imágenes de prueba.
Registrar en el directorio 16 variantes por percepción, en lugar de una, lleva su
aceptación del 73.6 al 96.2\,\% (con 4 variantes, 87.7\,\%); con 16 variantes también en
el contenido, la \emph{cobertura de punta a punta} (imágenes enrutadas a su clase cuyo
destino además responde) pasa de 66.5 a 94.5\,\%, y el rechazo en la formación visual
baja del 4.2 al 0.8\,\%.
En ese experimento, con 1 o 4 variantes en el directorio no hay falsos enrutamientos, y
con 16 hay uno; el sistema, con sus 16 variantes, enruta mal dos de las 656 imágenes
(Sección~\ref{sec:limitaciones}).
```
- **Nuevo:**
```latex
Un barrido del número de variantes lo mide sobre las 656 imágenes de prueba.
Registrar en el directorio 16 variantes por percepción, en lugar de una, lleva su
aceptación del 73.6 al 96.2\,\% (con 4 variantes, 87.7\,\%), y llenar el contenido con 16
variantes por imagen, en lugar de 4, lleva la respuesta de la memoria heteroasociativa
del 76.2 al 96.2\,\%; con las dos, la \emph{cobertura de punta a punta} (imágenes
enrutadas a su clase cuyo destino además responde) pasa de 66.5 a 94.5\,\%, y el rechazo
en la formación visual baja del 4.2 al 0.8\,\%.
En ese barrido, con 1 o 4 variantes en el directorio no hay falsos enrutamientos, y con
16 hay uno; con 16 variantes en el contenido, un especialista ajeno acepta 5 de las 656
imágenes (0.8\,\%), todas entre animales.
El sistema, con sus 16 variantes, enruta mal dos de las 656 imágenes
(Sección~\ref{sec:limitaciones}).
```
- **Fuente:** `results/experimento13/veredicto.md`: «contenido responde (hetero)» 76.2 con 4 variantes y 96.2 con 16; (b) 5 imágenes aceptadas por un especialista ajeno (0.8 %), todas entre animales («El precio»).

### B40. Hemisferio visual, cita del experimento 14

- **Dónde:** `05:581` (`.tex_uacj/Capitulo4.tex:584`)
- **Viejo:**
```latex
El experimento 14 localizó la causa.
```
- **Nuevo:**
```latex
Un banco de 231 entradas degeneradas localizó la causa.
```
- **Fuente:** `results/experimento14/veredicto.md` («Banco degenerado de 231 entradas»).

### B41. Hemisferio visual, umbral de energía (cifra antes solo en la limitación (c))

- **Dónde:** `05:590` (`.tex_uacj/Capitulo4.tex:593`)
- **Viejo:**
```latex
Esos grises tienen norma de 10.7 a 13.0, y el umbral los rechaza.
Las entradas degeneradas que sí pasan el umbral se discuten en la
Sección~\ref{sec:limitaciones}.
```
- **Nuevo:**
```latex
Esos grises tienen norma de 10.7 a 13.0, y el umbral los rechaza.
En todo el banco, de las 152 entradas que acepta una clase ajena, 137 caen bajo $\tau$.
Las que sí pasan el umbral se discuten en la Sección~\ref{sec:limitaciones}.
```
- **Fuente:** `results/experimento14/banco_degenerado.json`: entradas con `acepta` y alguna clase de `contenido` distinta de la de origen = 152; de ellas, `pasa_norma` falso = 137 (recontado para este parche; mismo criterio que `revision_tesis_auditoria_prosa.md:1548`).

### B42. Objetos nuevos, cita del experimento 13

- **Dónde:** `05:651` (`.tex_uacj/Capitulo4.tex:654`)
- **Viejo:**
```latex
La cifra con objetos conocidos no coincide con el 94.5\,\% del experimento 13 porque se
mide sobre otro banco y con otros modelos.
Aquí es la media de diez pliegues, cada uno con modelos construidos con nueve objetos
por clase y evaluado sobre 41 vistas no usadas de cada clase; el experimento 13 mide
sobre las 656 imágenes de prueba, con sus propios modelos.
```
- **Nuevo:**
```latex
La cifra con objetos conocidos no coincide con el 94.5\,\% de la
Sección~\ref{sec:hemisferio-visual} porque se mide sobre otro banco y con otros modelos.
Aquí es la media de diez pliegues, cada uno con modelos construidos con nueve objetos
por clase y evaluado sobre 41 vistas no usadas de cada clase; aquel barrido mide sobre
las 656 imágenes de prueba, con sus propios modelos.
```
- **Fuente:** Sin cifras nuevas.

### B43. EHAM única, fuera de dominio (cifra antes solo en la limitación (a))

- **Dónde:** `05:973` (`.tex_uacj/Capitulo4.tex:976`)
- **Viejo:**
```latex
Sin la segunda compuerta, con 200 imágenes por clase, $p = 0.22$.
```
- **Nuevo:**
```latex
Sin la segunda compuerta, con 200 imágenes por clase, $p = 0.22$.
Dos alternativas a la segunda compuerta, aplicadas a la misma salida del enrutamiento
con 200 imágenes por clase, cuestan acierto en las 171 reservadas: que el contenido
decida entre los tres mejores candidatos del directorio baja el acierto del 96.8 al
93.6\,\%, y abstenerse cuando la diferencia relativa entre las dos mejores puntuaciones
es menor que un umbral $\delta$ quita más de un acierto por cada error evitado
(\texttt{results/experimento15/}).
```
- **Fuente:** `results/experimento15/README.md`: argmax 96.8, árbitro 93.6; curva de δ (δ = 0.05: acierto 96.8 → 95.6, error 3.2 → 2.2).

---

## Parte 2. Títulos cortos de figuras y tablas (parche A)

Los 26 `\caption` pasan a `\caption[corto]{largo}`. El corto es el que va en el índice de figuras y en el de tablas; el largo no cambia. Líneas del árbol con A aplicado (la figura del espacio semántico pasa a 04 con el parche B).

| # | Dónde | Etiqueta | Título corto |
|---|---|---|---|
| 1 | `02:291` | `tab:wegner-sistema` | Lo que EAM-TMS toma de Wegner y lo que decide el sistema |
| 2 | `03:34` | `tab:memorias` | Las 26 memorias asociativas del sistema EAM-TMS |
| 3 | `03:194` | `fig:arq-llenado` | Llenado de la memoria de contenido |
| 4 | `03:272` | `fig:arq-temprana` | Fase temprana: aprendizaje mediado por el TME |
| 5 | `03:335` | `fig:arq-madura` | Fase madura: recuperación punto a punto |
| 6 | `05:71` | `tab:calibracion` | Precisión bajo las condiciones de calibración |
| 7 | `05:114` | `fig:mature-vs-n` | Precisión madura en función de $N$ por condición de calibración |
| 8 | `05:130` | `fig:heatmap-condicion` | Precisión madura por condición y número de consultas de formación |
| 9 | `05:154` | `fig:dominio` | Precisión madura por dominio y condición de calibración |
| 10 | `05:173` | `fig:winner` | Módulos ganadores en fase madura por condición de calibración |
| 11 | `05:224` | `tab:calibracion-fija` | Calibración con un conjunto de evaluación fijo |
| 12 | `05:360` | `tab:grid-iota-kappa` | Precisión temprana y tasa de rechazo en función de $\iota$ y $\kappa$ |
| 13 | `05:461` | `tab:capacidad` | Métricas de capacidad en función de las imágenes registradas por clase |
| 14 | `05:604` | `fig:rechazo-imagenes` | Rechazo de imágenes en el hemisferio visual |
| 15 | `05:618` | `fig:imagen-etiquetas` | Salida semántica imagen $\to$ etiquetas |
| 16 | `05:702` | `tab:objetos-nuevos-pliegue` | Objetos nuevos por pliegue, con el codificador del sistema y uno reentrenado |
| 17 | `05:763` | `tab:codificador-sin-clase` | Hemisferio visual con tres codificadores |
| 18 | `05:875` | `tab:eham-unica` | Una sola EHAM contra los especialistas, por imágenes de llenado |
| 19 | `05:1011` | `tab:lineas-base-texto` | Decisores sin memoria asociativa sobre los vectores de los tokens |
| 20 | `05:1114` | `tab:lineas-base-imagen` | Decisores sin memoria asociativa sobre los latentes de las imágenes |
| 21 | `05:1226` | `tab:lesion` | Lesión de la memoria de contenido |
| 22 | `05:1263` | `tab:costo` | Costo computacional de reproducir el sistema desde cero |
| 23 | `06:48` | `fig:espacio-semantico` | Espacio semántico de las etiquetas de llenado |
| 24 | `.tex_uacj/ApendiceA.tex:13` | `tab:exp-texto` | Experimentos del hemisferio textual y del directorio |
| 25 | `.tex_uacj/ApendiceA.tex:64` | `tab:exp-visual` | Experimentos del hemisferio visual |
| 26 | `.tex_uacj/ApendiceA.tex:116` | `tab:exp-comparaciones` | Comparaciones con otras arquitecturas y decisores, y costo |

---

## Parte 3. Lo que no se aplicó tal cual, y por qué

- **Rango de los decisores simples (Resumen, Abstract).** El texto propuesto decía «79.4–81.5 %». En las 80 consultas del protocolo completo los decisores dan de 76.0 (1-NN con la media) a 81.5 (5-NN con la media); 79.4 es el voto, y quedan fuera el centroide (77.5) y el centroide por frecuencia (78.8) (`results/lineas_base/README.md`). Va «76.0–81.5», el mismo rango que `ConclusionObjetivoGeneral.tex`.
- **«Las 80 consultas más difíciles».** Son las primeras 80 del banco (partición proto80), no una selección por dificultad; solo 11 traen el nombre de su clase. En la conclusión del objetivo general va «las 80 consultas del protocolo completo», como en el resto del reporte; en el Resumen y el Abstract, que no definen ese protocolo, «80 consultas que casi nunca nombran su clase» / «80 queries that seldom name their class».
- **Rechazo «en imagen depende … de una segunda compuerta».** La segunda compuerta de contenido se aplica al texto (consultas fuera de dominio del experimento 11), no a la imagen. Queda: en texto no usa umbral y equivale a la pertenencia al vocabulario; frente a la EHAM única, la ventaja depende de esa segunda compuerta (limitación (g)); en imagen depende del umbral de energía $\tau$.
- **Objetos nuevos en el Resumen y el Abstract.** Se omite «(4.1 %)» por espacio; quedan «136 falsos enrutamientos de 3280 en lugar de 2».
- **Rechazo en `Resumen.tex:28-29`.** No cambia: la frase «aporta el rechazo» va después de la que ya dice que el rechazo es el de un voto por vocabulario.
- **Limitación (a), «las 40 fuera de dominio se escribieron sin palabras del vocabulario».** Solo las 28 nuevas se escribieron con esa regla (cabecera de `results/experimento11/consultas_fuera_dominio.txt`); las 12 de la sonda son anteriores, y 2 de las 40 tienen una palabra del vocabulario. Se escribe así.
- **Limitación (l), acceso al vocabulario.** Del banco de 411 no consta en el repositorio con qué acceso al vocabulario se generó (`src/eval_bank.py` solo trae las listas, y `revision_jurado_metodologia_prosa.md:543` ya lo anotaba). De las 12 consultas de la sonda tampoco consta la regla. No se afirma nada sobre eso.
- **«Escritos por terceros» (trabajo futuro).** No contradice el dato del autor; se precisa «sin acceso al vocabulario».
- **Apéndice A, `LEEME_RESTAURAR.md`.** No existe en `6b127f6` ni en `origin/una-hetero`, así que no se cita.
- **`07:48`, remisión a la Sección del hemisferio visual.** Esa sección no reportaba las 5 de 656 imágenes aceptadas por un especialista ajeno; el parche B la agrega allí (B, `05:542`) para que la remisión sea válida.
- **Tres cifras que solo estaban en Limitaciones.** Se reportan en la Sección 4.1 con su fuente: 76 → 96 % y 5 de 656 en el hemisferio visual (`results/experimento13/veredicto.md`), 137 de 152 en el mismo apartado (`results/experimento14/banco_degenerado.json`) y 96.8 → 93.6 % en la EHAM única (`results/experimento15/README.md`). Las limitaciones (a), (b) y (c) remiten a esas secciones.
- **Citas por número de experimento que se quedan.** `05:540` (experimento 10: ninguna sección reporta su resultado), `05:638` (la sección de objetos nuevos nombra el experimento que reporta; su tabla y dos párrafos lo usan como nombre), `05:1177` (lista de experimentos fuera de la comparación con la batería completa) y `06:498` (la sonda de color liso con 16 variantes solo está en la limitación (c)). La nota al pie de `04:161` sigue explicando la numeración.
- **Otras cosas vistas y no tocadas.** `05:166` conserva «(ideal 12.5 %)»: ahí es el ideal balanceado de la métrica (1/8). `07:62` remite las operaciones externas a la «limitación (k)», que trata de la supervisión del codificador; la remisión natural sería la Sección de auditoría.
- **Largo del Resumen y del Abstract.** Con B, el cuerpo del Resumen pasa de 1723 a 1945 caracteres de fuente (unos 1830 de texto impreso) y el del Abstract de 1677 a 1878 (unos 1763). Hay que comprobar al compilar que siguen cabiendo en una página con `\enlargethispage{3\baselineskip}`; la Introducción gana una línea.
