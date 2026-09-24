# Revisión de prosa tras el experimento 16, leave-one-object-out (24 de septiembre de 2026)

**Estado:** pendiente de aprobación. Cifras de `results/experimento16/README.md` y `veredicto.md` (10 pliegues): objeto nuevo 89.2 % de punta a punta [85.1, 93.2] contra 95.5 % de objeto conocido con los mismos modelos; brecha 6.3 [2.5, 10.4]; 2 falsos ruteos de 3280 (0.1 %); ruteo correcto sobre aceptadas 99.9 % en los dos bancos; por objeto, 74 de 80 por encima del 70 %.

## A. `.tex8/secciones/04_metodologia.tex`, líneas 18–27

**Viejo:** «Por tanto, no hay solapamiento de imágenes entre train y test, pero no se impone una separación leave-object-out entre objetos físicos de ETH-80. La consecuencia, verificada sobre la partición persistida, es que \textbf{los diez objetos físicos de cada clase aportan vistas tanto a train como a test} (solape de instancias del 100\%): toda imagen de prueba es una vista nueva de un objeto cuyas demás vistas participaron del llenado o de la formación del directorio. Las cifras del hemisferio visual de este reporte miden, en consecuencia, generalización a \emph{vistas nuevas de objetos conocidos}, no a objetos nuevos; la partición leave-one-object-out, protocolo estándar de ETH-80, queda declarada como trabajo futuro (Sección~\ref{sec:limitaciones}).»

**Nuevo:** «Por tanto, no hay solapamiento de imágenes entre train y test, pero la partición principal no separa los objetos físicos de ETH-80: verificado sobre la partición persistida, \textbf{los diez objetos físicos de cada clase aportan vistas tanto a train como a test} (solape de instancias del 100\%), y toda imagen de prueba es una vista nueva de un objeto cuyas demás vistas participaron del llenado o de la formación del directorio. Las cifras del hemisferio visual sobre esa partición miden generalización a \emph{vistas nuevas de objetos conocidos}. La generalización a objetos nuevos se midió aparte con una validación leave-one-object-out de diez pliegues (experimento 16, Sección~\ref{sec:limitaciones}): en cada pliegue se reserva un objeto por clase y el sistema se construye con los otros nueve.»

## B. `.tex8/secciones/06_discusion.tex`, limitación (e), líneas 236–240

**Viejo:** «Las cifras visuales de este reporte (96.2\% de enrutamiento, evocación top-3) miden por tanto generalización a \emph{vistas nuevas de objetos conocidos}, no a objetos nuevos. Una validación más estricta deberá usar particiones leave-object-out para medir generalización a instancias completamente no vistas.»

**Nuevo:** «Las cifras visuales de este reporte (96.2\% de enrutamiento, evocación top-3) miden por tanto generalización a \emph{vistas nuevas de objetos conocidos}. La generalización a objetos nuevos se midió con una validación leave-one-object-out de diez pliegues (experimento 16): con el contenido y la fase A construidos con nueve objetos por clase, las 41 vistas del objeto reservado obtienen una cobertura de punta a punta del 89.2\,\% [85.1, 93.2], frente al 95.5\,\% de vistas nuevas de los objetos conocidos evaluadas sobre los mismos modelos; la brecha es de 6.3 puntos [2.5, 10.4] y los falsos enrutamientos son 2 de 3280 (\texttt{cow} y \texttt{horse} a \texttt{dog}). La envolvente por coordenada cubre a un objeto que no contribuyó a ella, y cuando no lo cubre lo rechaza: el ruteo correcto sobre las aceptadas es del 99.9\,\% en los dos bancos. La brecha no vive en clases sino en objetos concretos: 74 de los 80 objetos reservados superan el 70\,\% y seis (dos manzanas, dos peras, un perro, una taza) concentran el resto. Con diez objetos por clase, «objeto nuevo» sigue siendo un objeto de la misma colección fotografiado en las mismas condiciones; fotos de otro origen son otra pregunta.»

## C. `.tex8/secciones/07_conclusiones.tex`, trabajo futuro, líneas 61–62

**Viejo:** «\item \textbf{Partición leave-object-out}: validar la generalización visual sobre objetos físicos completamente no vistos.»

**Nuevo:** se elimina (hecho; queda en la limitación (e) y en la metodología).

## D. `.tex8/secciones/07_conclusiones.tex`, logros principales (tras la frase del hemisferio visual, línea 22)

**Añadir:** «Sobre objetos físicos nunca vistos (leave-one-object-out, diez pliegues) la cobertura de punta a punta es del \textbf{89.2\%}, seis puntos por debajo de la de vistas nuevas de objetos conocidos, con 2 falsos enrutamientos de 3280.»

## E. `README.md`, tabla (tras la fila de evocación, línea 129)

`| Leave-one-object-out (exp16, 10 folds) | **89.2%** end-to-end on unseen objects (95.5% on unseen views of known objects, same models) | 2 false routes of 3280; gap 6.3 pts lives in 6 of 80 objects (`results/experimento16/`) |`

## F. `CONTEXTO_SEP2026.md` §9 (viñeta nueva) e `INICIO_NUEVA_SESION.md` §5 y §6

CONTEXTO: «- Experimento 16 (24 de septiembre, `run_experiment16_leave_object_out.py`, `results/experimento16/`, diseño en `propuesta_exp16_leave_object_out.md`): leave-one-object-out, 10 pliegues (uno por objeto de cada clase, en el orden de la clase: car numera 1, 2, 3, 5, 6, 7, 9, 11, 12, 14), contenido y fase A con 9 objetos, ~49 min por pliegue con 2 procesos. Objeto nuevo 89.2 % de punta a punta contra 95.5 % de objeto conocido sobre los mismos modelos (razón 0.93 [0.89, 0.97]; criterio ≥ 0.75), 2 falsos de 3280 (cow → dog, horse → dog), brecha 6.3 [2.5, 10.4]. La brecha vive en objetos: apple3 0 %, pear9 10 %, apple10 32 %, dog10 49 %; horse y tomato generalizan mejor que apple y pear (P1 al revés). Latentes de las 410 × 16 por clase en `latentes.npy` (fuera de git, 25 s en GPU).»

INICIO §5: `| exp16 | leave-one-object-out: objeto nuevo 89.2 % de punta a punta contra 95.5 % conocido, 2 falsos de 3280 | run_experiment16_leave_object_out.py, results/experimento16/ |`

INICIO §6: «**Exp16:** la envolvente generaliza a objetos nunca vistos: 89.2 % de punta a punta (95.5 % en vistas nuevas de objetos conocidos, mismos modelos), brecha 6.3, 0.1 % de falsos; el fallo es rechazo. Seis objetos de 80 concentran la brecha.»
