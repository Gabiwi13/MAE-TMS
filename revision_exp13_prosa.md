# Revisión de prosa tras el experimento 13 (23 de septiembre de 2026)

Formato viejo / nuevo. Nada aplicado hasta aprobación. Cifras de `results/experimento13/README.md` y `veredicto.md`.

## A. `.tex8/secciones/06_discusion.tex`, limitación (b), líneas 169–182

**Viejo:**
```
\paragraph{(b) Cobertura visual residual limitada por el containment conjunto.}
El 25\% de rechazo del enrutamiento visual de test no proviene de huecos por
coordenada (625 de 656 imágenes tienen soporte marginal completo) sino de la conjunción
AND sobre las 64 coordenadas simultáneas, por lo que aumentar $\xi$ no lo reduce
($\xi$ satura en 2--3).
La palanca es densificar el llenado con augmentación más rica, manteniendo el criterio
conservador que hoy garantiza cero falsos enrutamientos.
En sentido inverso, el containment visual también tiene una fuga con \emph{entradas
degeneradas}: una imagen de color sólido uniforme obtiene soporte y se acepta
(Figura~\ref{fig:rechazo-imagenes}), presumiblemente porque el fondo liso de ETH-80
puebla esa región del espacio latente; las sondas estructuradas (ruido, píxeles
barajados) sí se rechazan.
Un criterio de varianza mínima de la pista latente, previo a la memoria, o la doble
compuerta del punto (a) aplicada al hemisferio visual, son mitigaciones candidatas.
```

**Nuevo:**
```
\paragraph{(b) Cobertura visual residual limitada por el containment conjunto.}
El 25\% de rechazo del enrutamiento visual de test no proviene de huecos por
coordenada (625 de 656 imágenes tienen soporte marginal completo) sino de la conjunción
AND sobre las 64 coordenadas simultáneas, por lo que aumentar $\xi$ no lo reduce
($\xi$ satura en 2--3).
La palanca es densificar, y el experimento 13 midió cuánto rinde. Son dos compuertas,
el directorio visual (formado en la fase A con una percepción por imagen) y el recall
de la hetero, y cada una cede solo con su propia augmentación: registrar 16 variantes
por percepción en el directorio lleva su aceptación de 73.6 a 96.2\,\%; llenar el
contenido con 16 variantes por imagen lleva la respuesta de la hetero de 76 a 96\,\%;
con las dos, la cobertura de punta a punta (ruteo correcto y respuesta) pasa de 66.5 a
94.5\,\% de las 656 imágenes de test, con rendimiento decreciente por escalón de
variantes. El precio no es cero: un ruteo equivocado de 656 (una vista frontal de
\texttt{horse} a \texttt{dog}, en las cinco semillas) y cinco imágenes aceptadas por un
especialista ajeno, siempre el par animal que ya confunde al texto. Son vistas nuevas
de los mismos objetos, porque el split es por imagen.
En sentido inverso, el containment visual también tiene una fuga con \emph{entradas
degeneradas}: una imagen de color sólido uniforme obtiene soporte y se acepta
(Figura~\ref{fig:rechazo-imagenes}), presumiblemente porque el fondo liso de ETH-80
puebla esa región del espacio latente; las sondas estructuradas (ruido, píxeles
barajados) sí se rechazan. Densificar agranda esa fuga: con 16 variantes la aceptan
tres especialistas en vez de uno y el directorio la rutea.
Un criterio de varianza mínima de la pista latente, previo a la memoria, es la
mitigación pendiente; la doble compuerta del punto (a) no la cerraría, porque el
contenido también la acepta.
```

## B. `.tex8/secciones/05_resultados.tex`, líneas 320–321

**Viejo:** «Por eso $\xi$ satura, y la palanca para ese residual es densificar el llenado, no aumentar la tolerancia.»

**Nuevo:** «Por eso $\xi$ satura, y la palanca para ese residual es densificar el llenado, no aumentar la tolerancia. El experimento 13 lo confirma: con 16 variantes por imagen en el contenido y por percepción en el directorio, el ruteo de test sube del 73.6\,\% del protocolo perspectival al 97.1\,\% y la cobertura de punta a punta de 66.5 a 94.5\,\%, con un falso ruteo de 656 (Sección~\ref{sec:limitaciones}).»

## C. `.tex8/secciones/07_conclusiones.tex`, trabajo futuro, ítem 1 (líneas 57–59)

**Viejo:** «\item \textbf{Augmentación más rica del llenado visual}: reducir el 25\% de rechazo residual de test, que proviene del containment conjunto y no responde a $\xi$.»

**Nuevo:** «\item \textbf{Criterio de varianza mínima de la entrada visual}: la augmentación del llenado ya se midió (experimento 13: cobertura de 66.5 a 94.5\,\% con 16 variantes en contenido y directorio, a costa de un falso ruteo de 656 y de que la sonda de color sólido se acepte más); falta cerrar esa fuga de entradas degeneradas antes de la memoria y decidir si el llenado con 16 variantes pasa a ser el oficial.»

## D. `README.md`, tabla de resultados (línea 125)

Añadir una fila después de «Visual routing (test, mem_dir_R)»:

`| Visual routing with 16 augmentation variants in content and directory (exp13) | **97.1%** routing · **94.5%** end-to-end (from 73.6 / 66.5) | 1 false route of 656; not adopted as the official fill (`results/experimento13/`) |`

## E. `CONTEXTO_SEP2026.md`

§9, viñeta nueva antes de «Experimento 12»:

«- Experimento 13 (22–23 de septiembre, `run_experiment13_augmentation.py`, `results/experimento13/`, diseño en `propuesta_exp13_augmentacion_visual.md`): augmentación del llenado visual, 13 combinaciones × 5 semillas sobre las 656 de test. El 25 % de rechazo son dos compuertas: el directorio visual (formado sin augmentar) y el recall de la hetero (conjunción de `project`); cada una cede solo con su augmentación. Solo directorio: aceptación 73.6 → 96.2 % con la cobertura total estancada en 76 %; solo contenido: respuesta de la hetero 76 → 96 % con el directorio en 77 %; ambas con 16 variantes: punta a punta 66.5 → 94.5 %, 1 falso ruteo de 656 (`horse7` frontal → dog en las 5 semillas) y 5 aceptaciones por un ajeno; la sonda de color sólido pasa de 1 a 3 especialistas y el directorio la rutea. 128 imágenes reales más rinden como 4 variantes para la hetero y nada para el directorio. Los latentes van en GPU con las variantes 0–3 oficiales (control 8/8; el encoder en GPU cambia 148 de 409 600 niveles). `evoke_labels` cuesta 17 s por imagen (búsqueda por muestreo de `recall_from_right`): «responde» se decide con una proyección y la evocación completa va sobre 5 por clase. No adoptado como llenado oficial.»

§8 Pendiente, dos viñetas nuevas:

«- Decidir si el llenado con 16 variantes (contenido y fase A) pasa a ser el oficial: rehacer etapa 5 y fase A, re-verificar 8/8 y 16/16, re-correr lo que depende de `models/` (exp8, exp9, exp11, app) y actualizar las cifras de 75 % / 0 falsos del reporte.
- Criterio de varianza mínima de la entrada visual, medido con las tres sondas y las 656 de test (que no rechace ninguna imagen real); cierra la fuga de color sólido que exp13 hizo crecer.»

## F. `INICIO_NUEVA_SESION.md`

§5, fila nueva: `| exp13 | augmentación del llenado visual: dos compuertas, punta a punta 66.5 → 94.5 % con 16 variantes, 1 falso ruteo de 656 | run_experiment13_augmentation.py, results/experimento13/ |`

§6, bloque nuevo tras Exp12: «**Exp13:** el rechazo visual son dos compuertas (directorio y recall de la hetero) y cada una cede solo con su augmentación; con 16 variantes en las dos, ruteo 73.6 → 97.1 % y punta a punta 66.5 → 94.5 %, con 1 falso ruteo de 656 y la sonda de color sólido aceptada por 3 especialistas. No adoptado como llenado oficial.»

§7, comandos: corregir `$env:CUDA_VISIBLE_DEVICES=""` por `$env:CUDA_VISIBLE_DEVICES="-1"` (la vacía no oculta la GPU) y añadir:
```
# exp13 (reanudable; latentes y contenido en caché; ~50 min de llenados + ~4 h de evaluación con 2 procesos)
python run_experiment13_augmentation.py --seeds 42-46 --workers 2
python run_experiment13_augmentation.py --report-only
```

§8, trampa nueva: «- **`evoke_labels` / `recall_from_right` cuestan ~17 s por imagen** (búsqueda por muestreo de `hetero_lib`, 3000 proyecciones); para medir cobertura basta una proyección (`hetero_recognizes` de exp13), la evocación completa solo para leer etiquetas.»

§9, las dos viñetas de E.
