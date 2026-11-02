# Propuesta viejo/nuevo: referencias de toda la tesis (consejo de redacción)

**Estado:** pendiente de aprobación. Nada aplicado.

Las 25 entradas de `referencias.bib` existen y sus metadatos son correctos salvo detalles (verificado por el revisor contra Crossref, PubMed/Europe PMC, PMC y arXiv; `main.blg` sin advertencias). Lo que pesa son cuatro usos: el artículo de símbolos manuscritos se cita como ejemplo de W-EAM y usa la formulación booleana; la EHAM se cita dos veces (preprint y artículo publicado, que son la misma obra); los tres procesos de Wegner con esos nombres son del artículo de 1995, no del capítulo de 1987; y la modulación gaussiana se atribuye al trabajo de imaginería cuando la introduce la W-EAM de 2022. Además, varias decisiones de EAM-TMS (el mediador, las dos fases, el rechazo claro) se leen como parte del modelo de Wegner.

Todo lo que sigue sale de `referencias.md` (revisor de referencias) y de las partes sobre citas de `claridad_*.md` y `consistencia.md`. No añadí ninguna fuente que el revisor no haya verificado; la única entrada nueva (`wegner1995computer`) tiene sus metadatos verificados en Crossref.

Coordinación: varios pasajes los reescriben también las propuestas de prosa de 01–02 (`claridad_main_01_02` M10, M14, M23, M24, B1, B2) y de 06–07 (`claridad_06_07` B2, B5). Doy el cambio sobre el texto de hoy y, en cada caso, la regla para aplicarlo si gana el texto de prosa. En el resumen, los cambios van sobre el texto **ya aprobado del replanteamiento** (`revision_replanteamiento_prosa.md`, §1).

---

## Parte 1. Metadatos del `.bib`

| # | Entrada (línea) | Viejo | Nuevo | Fuente |
|---|---|---|---|---|
| B1 | `lopez2025hyperopt` (63) | `author  = {Juan Antonio López Rivera and Carlos Ignacio Hernández Castellanos and Rafael Morales and Luis A. Pineda},` | `author  = {{López Rivera}, Juan Antonio and {Hernández Castellanos}, Carlos Ignacio and Morales, Rafael and {Pineda Cortés}, Luis A.},` | Crossref 10.1038/s41598-025-22621-y (el cuarto autor publica como «Pineda Cortés»). Hoy el texto imprime «Rivera et al., 2025» (`main.bbl:121`). |
| B2 | `honnibal2020spacy` (125) | `author    = {Matthew Honnibal and Ines Montani and Sofie Van Landeghem and Adriane Boyd},` | `author    = {Honnibal, Matthew and Montani, Ines and {Van Landeghem}, Sofie and Boyd, Adriane},` | `CITATION.cff` de spaCy. Hoy imprime «Landeghem, S. V.» (`main.bbl:60`). |
| B3 | `honnibal2020spacy` (128–130) | `publisher = {Zenodo},` / `note      = {Software},` / `doi       = {10.5281/zenodo.1212303}` | `howpublished = {Software, Zenodo, \url{https://doi.org/10.5281/zenodo.1212303}}` | apalike no imprime `doi` ni `publisher` en `@misc`: hoy la entrada dice solo «Software.» y no hay cómo localizarla. |
| B4 | `leibe2003eth80` (100) | `pages     = {II--409--II--415},` | `pages     = {II-409--II-415},` | Crossref 10.1109/CVPR.2003.1211497. El guion de «II-409» es parte del número. |
| B5 | `brown1966tip` (243–251) | (sin `doi`) | añadir `doi     = {10.1016/S0022-5371(66)80040-3}` | Crossref. |
| B6 | `morales2024hetero` (42–50) | entrada completa | **quitar** (ver U2) | arXiv 2411.02438 y *Scientific Reports* 15:21850 tienen el mismo contenido. |
| B7 | (nueva) | — | ver U3 | Crossref 10.1521/soco.1995.13.3.319. |

---

## Parte 2. Citas que no respaldan la frase

### U1. El trabajo de símbolos manuscritos no usa la W-EAM (alta)
- **Dónde:** `02:17–20`
- **Viejo:**
```latex
La variante que este trabajo utiliza es la \textbf{EAM ponderada} (W-EAM), introducida
en el aprendizaje fonético \cite{pineda2022weighted} y empleada desde entonces en toda
la línea de trabajo del grupo, desde símbolos manuscritos hasta imágenes naturales de
CIFAR-10 \cite{morales2022manuscript,pineda2023imagery,hernandez2026cifar}: la memoria
```
- **Nuevo:**
```latex
La variante que este trabajo utiliza es la \textbf{EAM ponderada} (W-EAM), introducida
en el aprendizaje fonético \cite{pineda2022weighted} y empleada desde entonces en la
línea de trabajo del grupo, de la imaginería a las imágenes naturales de
CIFAR-10 \cite{pineda2023imagery,hernandez2026cifar}: la memoria
```
- **Por qué:** Morales et al. 2022 (PLOS ONE) usa el registro booleano y deja la ponderación como trabajo futuro; además es anterior a la W-EAM. Sigue citado en `02:131`, donde sí respalda la frase.
- **Si gana `claridad_main_01_02` M10:** en su última oración, «de los símbolos manuscritos a las imágenes de CIFAR-10 \cite{morales2022manuscript,pineda2023imagery,hernandez2026cifar}» → «de la imaginería a las imágenes de CIFAR-10 \cite{pineda2023imagery,hernandez2026cifar}».

### U2. El preprint y el artículo de la EHAM son la misma obra (alta)
- **Por qué:** arXiv 2411.02438 (nov. 2024) y *Scientific Reports* 15:21850 (2025) tienen el mismo resumen en sustancia: relación 4D, problema de la pista faltante, los mismos tres métodos y los mismos datos. Citar los dos sugiere dos fuentes independientes.

| Dónde | Viejo | Nuevo |
|---|---|---|
| Resumen (texto del replanteamiento, §1, su línea 22; hoy `main.tex:60`) | `\cite{morales2024hetero,morales2025missing}.` | `\cite{morales2025missing}.` |
| `01:59` | `\cite{morales2024hetero,morales2025missing}.` | `\cite{morales2025missing}.` |
| `02:143` | `Pineda~\cite{morales2024hetero,morales2025missing}` | `Pineda~\cite{morales2025missing}` |
| `07:7` | `(EHAM)~\cite{pineda2021entropic,pineda2022weighted,morales2024hetero,morales2025missing}.` | `(EHAM)~\cite{pineda2021entropic,pineda2022weighted,morales2025missing}.` |

y quitar la entrada `morales2024hetero` (B6). Si gana `claridad_06_07` B2 (la apertura de 07 sin citas), la fila de `07:7` sobra.

### U3. Los tres procesos de Wegner con esos nombres son de 1995 (alta)
- **Por qué:** *directory updating*, *information allocation* y *retrieval coordination* los nombra Wegner en su modelo de red de 1995; el capítulo de 1987 introduce la memoria transactiva y el directorio de «quién sabe qué». La atribución se apoya en fuentes secundarias (ver Parte 5, punto 1).
- **Entrada nueva** (metadatos verificados en Crossref):
```bibtex
@article{wegner1995computer,
  author  = {Daniel M. Wegner},
  title   = {A computer network model of human transactive memory},
  journal = {Social Cognition},
  volume  = {13},
  number  = {3},
  pages   = {319--339},
  year    = {1995},
  doi     = {10.1521/soco.1995.13.3.319}
}
```

| Dónde | Viejo | Nuevo |
|---|---|---|
| Resumen (texto del replanteamiento, §1, su línea 37; hoy `main.tex:73`) | `de Wegner \cite{wegner1987transactive}: la actualización del directorio de experticia,` | `de Wegner \cite{wegner1987transactive,wegner1995computer}: la actualización del directorio de experticia,` |
| `01:16` | `El modelo de Wegner identifica tres procesos principales.` | `El modelo de Wegner identifica tres procesos principales \cite{wegner1995computer}.` |
| `02:271` | `Los tres procesos fundamentales son:` | `Los tres procesos fundamentales, en la formulación de Wegner como red de directorios compartidos \cite{wegner1995computer}, son:` |

Si gana `claridad_main_01_02` B2 (versión corta de `01:16–24`), la cita va tras «Wegner distingue tres procesos». Las citas de 1987 que hablan del concepto (`01:7`, `02:261`, `06:97`, `06:176`) no cambian.

### U4. La modulación gaussiana la introduce la W-EAM de 2022 (alta)
- **Dónde:** `02:105–108`
- **Viejo:**
```latex
Esta modulación gaussiana corresponde al mecanismo de recuperación vigente desde el
trabajo de imaginería \cite{pineda2023imagery} (el artículo base de 2021 empleaba
distribuciones triangulares, hoy superadas); es la versión implementada en el código de
referencia que este sistema utiliza.
```
- **Nuevo:**
```latex
Esta modulación gaussiana es la recuperación de la W-EAM \cite{pineda2022weighted}
(la EAM de 2021 usaba una distribución triangular \cite{pineda2021entropic}) y es la
que implementa el código de referencia que este sistema utiliza.
```
- **Fuente:** texto completo PMC9537336 (2022: distribución normal centrada en la pista; dice que la EAM original usaba una triangular); PMC7994563 (2021, distribución triangular). El artículo de 2023 la usa, no la estrena; sigue citado en `02:117` y `02:137`, donde sí respalda la frase.
- **Si gana `claridad_main_01_02` M14:** su última oración «La modulación gaussiana es la vigente desde el trabajo de imaginería \cite{pineda2023imagery} (el artículo de 2021 usaba distribuciones triangulares)…» → «La modulación gaussiana es la recuperación de la W-EAM \cite{pineda2022weighted} (la EAM de 2021 usaba una distribución triangular \cite{pineda2021entropic})…».

### U5. El tope de la suma y la regla de Hebb están en la EHAM, no en la W-EAM (media)
- **Dónde:** `02:39–41`
- **Viejo:**
```latex
La acumulación está acotada superiormente (suma con tope $w$) para evitar desbordamiento,
tal como definen las fuentes \cite{pineda2022weighted,morales2025missing}; los autores
describen esta operación como una forma de la regla de aprendizaje de Hebb.
```
- **Nuevo:**
```latex
La acumulación está acotada superiormente (pesos en $\{0,\ldots,w\}$), tal como define
la fuente heteroasociativa \cite{morales2025missing}, cuyos autores describen esta
operación como una forma de la regla de aprendizaje de Hebb; la W-EAM original fija
los pesos en $\{0,\ldots,l\}$ \cite{pineda2022weighted}.
```
- **Fuente:** PMC9537336 (2022: pesos en {0,…,l}, sin suma con tope ni mención de Hebb) y PMC12216516 (2025: pesos en {0,…,w}, «a form of Hebb's learning rule»). «Para evitar desbordamiento» es justificación de la tesis, no de las fuentes. (Si se aprueba el cambio de letra de `consistencia` 4.5, $w \to \omega$ aquí.)

### U6. Los centinelas son de la implementación, no del artículo (media)
- **Dónde:** `02:151–154`
- **Viejo:**
```latex
La relación se almacena en un tensor
$\mathbf{R} \in \mathbb{N}^{n \times p \times (m+1) \times (q+1)}$,
donde los tamaños $(m+1)$ y $(q+1)$ incorporan \emph{centinelas} en la última posición
para representar funciones parciales (características no definidas).
```
- **Nuevo:**
```latex
En el artículo la relación es $h \subseteq A \times B \times V \times Z$ con pesos en
$\{0,\ldots,w\}$; la implementación de referencia la almacena en un tensor
$\mathbf{R} \in \mathbb{N}^{n \times p \times (m+1) \times (q+1)}$,
donde los tamaños $(m+1)$ y $(q+1)$ incorporan \emph{centinelas} en la última posición
para representar funciones parciales (características no definidas).
```
- **Fuente:** PMC12216516, definición de la memoria heteroasociativa (sin valor indefinido ni centinelas).

### U7. Nombres de los métodos de la pista faltante (media)
- **Dónde:** `02:165–166`
- **Viejo:**
```latex
Los autores proponen los métodos \emph{random-and-test}, \emph{sample-and-test} y
\emph{search-and-test} para ese caso límite.
```
- **Nuevo:**
```latex
Los autores proponen los métodos \emph{random}, \emph{sample and test} y
\emph{search and test} para ese caso límite.
```
- **Fuente:** resumen de arXiv 2411.02438 y de PMC12216516. «Random-and-test» no aparece en el artículo.
- **Si gana `claridad_main_01_02` M23:** en su texto, «\emph{random-and-test}, \emph{sample-and-test} y \emph{search-and-test}» → «\emph{random}, \emph{sample and test} y \emph{search and test}».

### U8. Limitación (c): lo que dice el artículo de CIFAR-10 (media)
- **Dónde:** `06:272–280` (junta `referencias` M3 y `claridad_06_07` B5)
- **Viejo:**
```latex
\paragraph{(c) Calidad de la reconstrucción visual.}
El decoder, entrenado con un término de reconstrucción MSE dentro de una pérdida que
incluye una cabeza auxiliar de clasificación, produce reconstrucciones suaves sin
detalle de alta frecuencia (cf.\ la reconstrucción e imaginación en EAM de Pineda y
Morales~\cite{pineda2023imagery}, y la memoria EAM sobre imágenes naturales de
CIFAR-10~\cite{hernandez2026cifar}, que enfrenta el mismo compromiso con
autoencoders más profundos).
Es un efecto de la función de pérdida del autoencoder, no del sistema de memorias, y
puede abordarse de forma independiente.
```
- **Nuevo:**
```latex
\paragraph{(c) Calidad de la reconstrucción visual.}
Las reconstrucciones son suaves y sin detalle de alta frecuencia
(Figura~\ref{fig:imagen-etiquetas}).
Es un efecto de cómo se entrenó el autoencoder, con un término de reconstrucción MSE y
una cabeza auxiliar de clasificación que solo interviene en el entrenamiento, no en las
decisiones; no es un efecto del sistema de memorias y puede abordarse por separado.
Sobre la reconstrucción en la EAM, véanse la imaginería de Pineda y
Morales~\cite{pineda2023imagery} y la memoria de imágenes naturales de
CIFAR-10~\cite{hernandez2026cifar}, donde entrenar el autoencoder junto con el
clasificador degrada la reconstrucción y por eso se entrenan por separado.
```
- **Por qué:** el artículo de CIFAR-10 no habla de «autoencoders más profundos»; lo que reporta es que el entrenamiento conjunto perjudica al autoencoder. La propuesta de `claridad_06_07` B5 conservaba «el mismo compromiso con autoencoders más profundos»: aquí se corrige. La letra (c) pasa a (d) si se aprueba la partición de limitaciones de `claridad_06_07` M1.
- **Fuente:** arXiv 2405.12500v1 (preprint de `hernandez2026cifar`; ver Parte 5, punto 2). Que la cabeza de clasificación solo entrena: `04:126–134` y hechos G1.

### U9. Diana et al. 2007 no disputa la asignación; la matiza desde el mismo lado (media)
- **Dónde:** `06:156–159`
- **Viejo:**
```latex
En el cerebro, estas disociaciones suelen atribuirse a estructuras distintas, la corteza
perirrinal para la familiaridad y el hipocampo para unir
dominios~\cite{eichenbaum2007medial}, aunque esa asignación está en
disputa~\cite{squire2007recognition,diana2007imaging}.
```
- **Nuevo:**
```latex
En el cerebro, estas disociaciones suelen atribuirse a estructuras distintas, la corteza
perirrinal para la familiaridad y el hipocampo para unir ítem y
contexto~\cite{eichenbaum2007medial,diana2007imaging}, aunque esa asignación está en
disputa~\cite{squire2007recognition}.
```
- **Fuente:** resúmenes PubMed 17707683 (Diana: modelo de unión de ítem y contexto; perirrinal para la familiaridad), 17417939 (Eichenbaum), 17948032 (Squire: la perspectiva alternativa).

### U10. ConceptNet 5.7 con el artículo de la 5.5 (baja)
- **Dónde:** `04:58`
- **Viejo:** `Se consultó ConceptNet~5.7~\cite{speer2017conceptnet} con las relaciones \texttt{IsA},`
- **Nuevo:** `Se consultó ConceptNet~5.7 (la versión 5.5 se describe en \cite{speer2017conceptnet}) con las relaciones \texttt{IsA},`
- **Por qué:** es la cita estándar, pero el artículo describe la 5.5. Basta decirlo una vez; las demás menciones (`main`, `01:62`, `03:24`) quedan igual.

---

## Parte 3. Lo que se atribuye a Wegner sin respaldo

Ninguna afirmación de psicología o neurociencia de 06 está sin cita: las de `06:143–173` las verificó el revisor una por una (Clark y Gronlund, Mayes, Fortin, Old y Naveh-Benjamin, Eichenbaum, Squire, Plaut, Beauvois, Brown y McNeill, Hart). Los problemas están en cómo se presenta a Wegner.

### W1. Decisiones de EAM-TMS leídas como parte del modelo de Wegner (media)
Wegner no describe un mediador central, dos fases ni un rechazo del grupo; son decisiones de este sistema y van dentro de la exposición de su modelo. Ninguna fuente verificada las respalda, así que se marcan como propias.

| Dónde | Viejo | Nuevo |
|---|---|---|
| `01:13–14` | `El sistema funciona gracias a esa especialización: el conocimiento no necesita repetirse en cada miembro,` / `sino que se reparte entre ellos, y la coordinación entre pares reemplaza gradualmente a cualquier mediador central.` | `El grupo funciona gracias a esa especialización: el conocimiento no necesita repetirse en cada miembro, sino que se reparte entre ellos.` (incluye `claridad_main_01_02` B1) |
| `01:23–24` | `La transición de una \emph{fase temprana} mediada a una \emph{fase madura} punto a punto` / `es la señal de que el sistema transactivo ya quedó formado.` | `En este trabajo, la transición de una \emph{fase temprana} mediada a una \emph{fase madura} punto a punto es la señal de que el sistema transactivo ya quedó formado.` (si gana `claridad_main_01_02` B2, ya lo dice) |
| `02:284–286` | `En la fase temprana este enrutamiento puede requerir un mediador que evalúe las` / `capacidades de cada miembro; en la fase madura el propio directorio del emisor` / `basta para determinarlo.` | `En este sistema, en la fase temprana este enrutamiento lo hace un mediador (el TME); en la fase madura basta el propio directorio del emisor.` |
| `02:292–294` | `El \textbf{rechazo claro}, cuando ningún miembro reconoce el dominio de la` / `consulta, es un comportamiento válido del grupo y evita que el sistema invente` / `especialistas inexistentes.` | `En este sistema, cuando ningún módulo reconoce el dominio de la consulta, el grupo la rechaza en vez de inventar un especialista; el rechazo es una respuesta válida.` (es el texto de `claridad_main_01_02` M24) |
| `02:297` | `En la \textbf{fase temprana}, el grupo depende de un mediador: los miembros` | `En EAM-TMS, en la \textbf{fase temprana} el grupo depende de un mediador: los miembros` |

La primera fila quita además la idea del mediador del párrafo que describe a los grupos humanos; el mediador aparece en `01:45` como parte del sistema.

### W2. «Excede la suma de sus partes» y «recuerda más» (baja)
Wegner dice que la memoria del grupo puede ser más compleja y potencialmente más eficaz que la de cualquiera de sus miembros; no habla de la suma ni lo afirma como hecho general.

| Dónde | Viejo | Nuevo |
|---|---|---|
| `01:4–6` | `Cuando un grupo de personas trabaja de manera coordinada durante el tiempo suficiente,` / `recuerda más de lo que cualquiera de sus miembros podría` / `recordar de forma individual.` | `Cuando un grupo de personas trabaja de manera coordinada durante el tiempo suficiente, puede recordar más de lo que cualquiera de sus miembros recordaría por separado.` |
| `02:261–263` | `…describe cómo` / `los grupos desarrollan sistemas de memoria distribuida cuya capacidad excede la suma` / `de sus partes.` | `…describe cómo los grupos desarrollan sistemas de memoria distribuida que pueden ser más eficaces que la memoria de cualquiera de sus miembros.` |

Fuente: página de Wegner sobre memoria transactiva (Harvard), consultada por el revisor.

### W3. *Transactive encoding* y *transactive retrieval* (baja; suavizar)
El revisor no pudo confirmar esos términos en el capítulo de 1987 (Parte 5, punto 1), así que en lugar de citar se dice qué falta sin atribuir el término.

| Dónde | Viejo | Nuevo |
|---|---|---|
| `06:285–286` | `El sistema aún no modela \emph{transactive encoding} ni la reorganización de memorias` / `de contenido durante la operación madura.` | `El sistema aún no reparte información nueva entre los módulos ni reorganiza sus memorias de contenido durante la operación madura.` |
| `07:75–78` | `sigan almacenando labels, imágenes y asociaciones después de formar el directorio,` / `cubriendo \emph{transactive encoding} y \emph{transactive retrieval} en sentido` / `amplio.` | `sigan almacenando labels, imágenes y asociaciones después de formar el directorio.` |

Si el autor confirma los términos en el capítulo de 1987, puede dejarlos con `\cite{wegner1987transactive}` en `06:285`.

### W4. «Es el protocolo de asignación de información de Wegner» (baja; suavizar)
- **Dónde:** `03:428–430`
- **Viejo:** `El módulo ganador es $g = \arg\max_k \sum_{\text{tokens}} s_k$ (la suma recorre todos` / `los tokens semánticos de la pista; esta agregación multi-token es el protocolo de` / `asignación de información de Wegner y vive fuera de las memorias por diseño).`
- **Nuevo:** `El módulo ganador es $g = \arg\max_k \sum_{\text{tokens}} s_k$ (la suma recorre todos los tokens semánticos de la pista; en este sistema hace el papel de la asignación de información de Wegner y vive fuera de las memorias por diseño).`
- **Por qué:** Wegner no describe un protocolo de suma por tokens; es la forma en que este sistema realiza ese proceso.

---

## Parte 4. Entradas sin citar y citas sin entrada

Hoy, ninguna: las 25 entradas se citan al menos una vez y las 56 citas resuelven (`main.blg`: 25 entradas, `warning$ -- 0`; `main.log` sin citas indefinidas). Con esta propuesta:
- `morales2024hetero` deja de citarse y se quita (U2, B6).
- `wegner1995computer` entra y se cita tres veces (U3).
- `morales2022manuscript` sigue citada en `02:131` aunque salga de `02:20` (U1).

De las candidatas de `bibliografia_marco_teorico.bib` que revisó el revisor, solo `wegner1995computer` respalda una frase de la tesis; las demás (Nelson y Narens, Teyler, McClelland, Putnam, Kripke, Vygotsky, Hutchins, Clark y Chalmers…) no hacen falta.

---

## Parte 5. Lo que el revisor dejó sin verificar

1. **Wegner 1987, texto completo:** no está en línea. Que los tres procesos con esos nombres sean del artículo de 1995 se apoya en fuentes secundarias (Sage Encyclopedia of Group Processes, Richter y Lechner, iResearchNet) y en que ninguna descripción del capítulo los nombra. Tampoco se confirmó la redacción sobre *transactive encoding/retrieval*. La página de Wegner fecha el capítulo en 1986; Springer y Crossref, en 1987 (se conserva 1987).
2. **`hernandez2026cifar`:** se leyó el preprint arXiv 2405.12500, no la versión de *Pattern Recognition*. U8 vale si la versión publicada no cambió el autoencoder.
3. **`speer2017conceptnet`:** páginas 4444–4451 sin confirmar en fuente primaria (AAAI y DBLP bloquean el acceso automatizado); coinciden con la cita habitual.
4. **`hart1965memory` y `brown1966tip`:** sin resumen accesible; el contenido se cotejó con fuentes secundarias y coincide con lo que dice la tesis.
5. **`leibe2003eth80`:** el tamaño de 128×128 píxeles (`04:15`) solo lo confirma un tutorial del conjunto de datos; el artículo da 8 × 10 × 41.
6. **`morales2025missing`:** no se leyeron la discusión ni las referencias; U5, U6, U7 y la verificación de `02:216–219` salen de las secciones de definición y métodos.
7. **`pineda2022weighted`:** la ausencia de Hebb y del tope de suma se verificó en el texto principal; el material suplementario no.
8. **`nelson1990metamemory`** (candidata, no se usa): editor Bower sin confirmar.
9. **W1, fila `01:13–14`:** la extiendo yo con el mismo criterio que el revisor aplicó a `01:23` y `02:284–297` (ninguna fuente consultada describe un mediador en Wegner); no es un hallazgo suyo aparte.

---

## Descartado

- `referencias` B5 (apalike imprime «and», «pages», «In» en inglés y omite los DOI; cambiar a `apacite` o biblatex-apa): es una decisión de estilo que va con la plantilla de la UACJ.
- `referencias` B6 («de Pineda y Morales» en `01:57` y `07:85`, cuando el artículo de 2021 es de Pineda, Fuentes y Morales): la frase nombra la W-EAM y la EHAM, que sí son de Pineda y Morales, no el artículo de 2021. El «\&» de `01:57` lo cubre `consistencia` 1.14.
- `referencias` A3, variante «en su formulación como red de directorios» en `01:16`: basta la cita al final de la frase.
- `referencias` A1, paréntesis «(el trabajo sobre símbolos manuscritos usa aún la formulación booleana)»: `morales2022manuscript` sigue citado donde corresponde y el paréntesis añade historia que el pasaje no necesita.
- `referencias` M2, paréntesis «(sample-and-search en el cuerpo del artículo)»: detalle que el lector no necesita; se usan los nombres del resumen.
- `referencias` B9: incluido en U9.
- `number = {1}` en `speer2017conceptnet` y `eichenbaum2007medial`, `address`/`publisher` en `leibe2003eth80`: opcionales; no cambian lo que se imprime de forma que importe.
- `referencias` A2, alternativa de conservar el preprint con una nota: no aporta nada que el artículo publicado no tenga.
