# Revisión de prosa tras el experimento 14 (23 de septiembre de 2026)

Formato viejo / nuevo, aprobada en el chat antes de aplicarse. Cifras de `results/experimento14/README.md` y `veredicto.md`.

## A. `.tex8/secciones/05_resultados.tex`, líneas 339–343

**Viejo:** «La tercera sonda sintética, un lienzo de color sólido uniforme, \emph{sí} obtiene soporte y se acepta: es la excepción honesta del panel, presumiblemente porque las imágenes de ETH-80 contienen grandes regiones de fondo liso y un latente degenerado pero uniforme cae dentro de la distribución acumulada. Esta fuga con entradas degeneradas se retoma en la Sección~\ref{sec:limitaciones}.»

**Nuevo:** «La tercera sonda sintética, un lienzo de color sólido uniforme, \emph{sí} obtiene soporte y se acepta: es la excepción honesta del panel. El experimento 14 localizó la causa: no es el fondo liso (los sólidos negro, blanco, de colores y del color de fondo de ETH-80 se rechazan) sino que el encoder colapsa toda entrada sin estructura, el gris medio, un objeto desenfocado o sin contraste, en un mismo latente cerca del origen, y ese punto cae dentro de la envolvente por coordenada de \texttt{horse}, a tres veces la distancia intraclase de cualquier instancia registrada. Esta fuga con entradas degeneradas se retoma en la Sección~\ref{sec:limitaciones}.»

## B. `.tex8/secciones/06_discusion.tex`, limitación (b), líneas 191–193

**Viejo:** «Un criterio de varianza mínima de la pista latente, previo a la memoria, es la mitigación pendiente; la doble compuerta del punto (a) no la cerraría, porque el contenido también la acepta.»

**Nuevo:** «El experimento 14 midió la mitigación: un umbral sobre la norma del latente continuo, fijado con el mínimo de las imágenes de llenado y un margen del 10\,\% ($\tau = 16.6$), cierra el 94\,\% de esa fuga (79 de las 83 entradas degeneradas aceptadas por una clase ajena caen bajo $\tau$: grises medios, desenfoques de radio $\geq 8$, contrastes $\leq 0.2$) y el 88\,\% con el llenado de 16 variantes, a costa de cinco imágenes reales de 3280, todas vistas oscuras de \texttt{cow} que el directorio ya rechazaba. La norma y la varianza del latente son equivalentes; la varianza de píxeles no sirve, porque un objeto desenfocado conserva contraste y pierde estructura. Lo que sobrevive al umbral son confusiones de contenido entre clases (un \texttt{dog} desenfocado aceptado por \texttt{cow}), no entradas degeneradas. La doble compuerta del punto (a) no la cerraría, porque el contenido también la acepta.»

## C. `.tex8/secciones/07_conclusiones.tex`, trabajo futuro, ítem 1 (líneas 57–61)

**Viejo:** «\item \textbf{Criterio de varianza mínima de la entrada visual}: la augmentación del llenado ya se midió (experimento 13: cobertura de 66.5 a 94.5\,\% con 16 variantes en contenido y directorio, a costa de un falso ruteo de 656 y de que la sonda de color sólido se acepte más); falta cerrar esa fuga de entradas degeneradas antes de la memoria y decidir si el llenado con 16 variantes pasa a ser el oficial.»

**Nuevo:** «\item \textbf{Adoptar en el pipeline lo medido en los experimentos 13 y 14}: el llenado con 16 variantes en contenido y directorio (cobertura de 66.5 a 94.5\,\%, un falso ruteo de 656) y el umbral de energía mínima del latente en la codificación de la percepción (cierra el 94\,\% de la fuga de entradas degeneradas por cinco imágenes reales). Ambos están medidos y ninguno instalado; instalarlos exige rehacer la etapa 5, la fase A y las verificaciones.»

## D. `CONTEXTO_SEP2026.md`

§9, viñeta nueva antes de «Experimento 12»: «- Experimento 14 (23 de septiembre, `run_experiment14_latent_energy.py`, `results/experimento14/`, diseño en `propuesta_exp14_energia_latente.md`): criterio de energía mínima del latente. La fuga de «color sólido» es una región cerca del origen del latente (norma 10–17) donde el encoder colapsa las entradas sin estructura (grises 112–128, desenfoque de radio ≥ 8, contraste ≤ 0.2) y que la envolvente de `horse` contiene (79 de 83 aceptaciones por clase ajena; la instancia real más cercana está a 3 veces la distancia intraclase). τ = 16.6 (mínimo del llenado, margen 10 %) cierra el 94 % de esa fuga (88 % con 16 variantes, donde la comparten dog, horse y cow) y cuesta 5 imágenes reales de 3280, todas vacas oscuras que el directorio ya rechazaba (una de la fase A refuta la letra del criterio pre-registrado). Norma y desviación del latente equivalen; la desviación de píxeles deja pasar el desenfoque; los niveles vivos no separan. No instalado en el pipeline.»

§8 Pendiente: la viñeta «Criterio de varianza mínima…» se sustituye por «- Instalar el criterio de energía mínima del latente (τ = 16.6, junto a `latent_global_stats.json`) en `image_to_latent` de la etapa 7 y en `encode_pil` de la app, y re-correr la etapa 7 (la fase A pierde una percepción).»

## E. `INICIO_NUEVA_SESION.md`

§5, fila nueva: `| exp14 | energía mínima del latente: τ = 16.6 cierra el 94 % de la fuga de entradas degeneradas por 5 imágenes reales de 3280 | run_experiment14_latent_energy.py, results/experimento14/ |`

§6, bloque nuevo tras Exp13: «**Exp14:** la fuga de «color sólido» es una región cerca del origen del latente que la envolvente de `horse` contiene (no una instancia); τ = 16.6 sobre la norma cierra el 94 % (88 % con 16 variantes) a costa de 5 vacas oscuras que el directorio ya rechazaba. La desviación de píxeles no sirve. No instalado.»

§7, comando: `python run_experiment14_latent_energy.py   # minutos; requiere cache/exp13/Vc16_N200.pkl`

§9: la misma sustitución que en D.
