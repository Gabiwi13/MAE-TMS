# Grupo 2: `03_arquitectura.tex`

Fuentes: `revision_una_hetero_prosa.md` (UH), `revision_tesis_auditoria_prosa.md` (AUD), `revision_pesos_homo_principal_prosa.md` (PH). Las líneas son las del archivo ya editado. Sin compilar, sin commit, sin tocar PNG.

## Aplicados tal cual

- UH §0, «multi-agente» → `03:4–5` («sistema distribuido de memoria transactiva en su versión de ocho módulos»)
- UH 2a, cuenta de memorias → `03:14–15` (26 memorias, tres por módulo)
- UH 2b, pie y filas de `tab:memorias` → `03:29–31` y `03:45–48` (pie con `eq:marginal`; se va la frase de las homo; `\multirow{3}` con solo `M^H_dom` y los dos directorios)
- AUD A1, directorios del TME → `03:70–71`
- AUD A2, quién registra → `03:72–85`
- AUD A4, variantes del llenado en el pie de `fig:arq-llenado` → `03:176–183`
- UH 2c, pie de `fig:arq-llenado` → `03:171` y `03:184–185`
- UH 2d, nodos de `fig:arq-temprana` → `03:226–228` (`Módulo 0/k/7 … $w$ y $\Pi$ de $M^H$`)
- UH 2d + AUD A5, pie de `fig:arq-temprana` → `03:292–297`
- AUD A5, nodo y nota de `fig:arq-temprana` → `03:276` («Entrada, ganador y TME») y `03:280` («Anota quien participó»)
- AUD A6, nodos de `fig:arq-madura` → `03:328` («Módulo de\\entrada») y `03:331` («propio y de conocidos», ξ = 0)
- AUD A7, pie de `fig:arq-madura` → `03:376–386`
- UH 2e, paso 1 del ruteo → `03:399–402` (`\eta(\mathbf{v}_q, M^L)` con `eq:marginal`)
- AUD A8, conteos → `03:455` ([46, 16, 40, 25, 30, 18, 21, 31]; los comprobé en `results/exp3_corrected_routing/report.md` y `exp4_directory_formation/report.md` de la copia)
- AUD A9, dónde vive `c_k` → `03:460–464`
- AUD A11, lectura visual estricta y umbral τ (reemplaza la subsección de ξ = 2) → `03:482–498`
- AUD A12, entropía del directorio → `03:509–518`
- UH 2f, evocación inversa, paso 1 → `03:526–530`
- AUD A13, diccionario de la evocación → `03:536–538`
- AUD A14, definición de fidelidad → `03:552–554`
- Regla «agente» → «módulo»: las 53 líneas (56 apariciones) del archivo, incluidos «Agente 0/$k$/7», «Agente $k$ (×8)», «Agente de entrada» y «Agente destino», y los comentarios del TikZ. No queda ninguna. En este archivo no hay «miembros» de Wegner.
- Prefijos sin guion: `03:32, 46–48, 51–52, 57, 69, 456, 532` («heteroasociativa/s», «Heteroasociativa» en la tabla). Las líneas con «homo-asociativa» salieron con 2b y 2e.

## Aplicados con ajuste

- **AUD A3 + decisión 3** → `03:86–89`. Sin «nuevo en esta versión», sin «evaluada previamente» y sin «0 %». Queda como razón de diseño: «Cada módulo tiene un directorio visual, y no un puente por el $M^H_{\mathrm{dom}}$ del módulo de entrada hacia el directorio de texto, porque ese puente no redirige cuando el módulo de entrada no es el especialista: la memoria de contenido de un no-especialista no contiene el latente ajeno». Dice lo mismo que la frase que el grupo 1 puso en `01`.
- **UH 2c, flechas de las lecturas** → `03:157–159`. El Nuevo dibujaba `(MH) -- (ML)` y `(MH) -- (MR)`. Como `MH` queda justo debajo de `ML`, la flecha a `ML` salía de `MH.north`, donde llega la ruta de registro λ(v_q, z_q). Las dos líneas quedaban sobre el mismo eje, y la de `MR` salía de `MH.south`, donde llega la ruta visual. Por eso salen de `MH.east` y suben y bajan por la derecha: `(MH.east) -- ++(0.45,0) |- (ML.east)` y lo mismo hacia `MR.east`. Siguen punteadas, como pide la propuesta. Se quitan las flechas `qL → ML` y `qR → MR`, con sus rótulos $\mathbf{v}_q\in[0,15]^{300}$ y $\mathbf{z}_q\in[0,31]^{64}$, como en el Nuevo. Los nodos `ML` y `MR` son `box, dashed` con «$M^L$ / $M^R$ \\ lectura de $M^H$» (`03:131, 143`).
- **Figura de la fase temprana (decisión 16, AUD A5 y duda 9)** → `03:216` y `03:270–287`. Quité las tres flechas punteadas de «Actualización de directorio» a los módulos 0, k y 7. Las reemplacé por dos:
  - al módulo de entrada: el nodo «Consulta» ahora dice «Consulta\\(entra por un\\módulo al azar)», y una punteada gris va de `dir_update.west` a `query.south`, rotulada «módulo de entrada»;
  - al ganador: una punteada gris va de `dir_update.east` al nodo «arg max … ganador g». Pasa por debajo de la nota de Wegner para no cruzar la columna de módulos y entra por debajo, 0.6 cm a la derecha del centro, para no chocar con la llegada de s_7. Va rotulada «ganador g». Usa las coordenadas `gin` y `regw`; la nota pasó a llamarse `(nota)`.

  El TME sigue con su flecha sólida a `dir_update`, y el rótulo dice «Entrada, ganador y TME registran λ(v_q, g)». No agregué un nodo nuevo de «Módulo de entrada» porque alargaba la fila unos 3.9 cm y el `\resizebox` encogía más la figura, que ya es la más ancha.
- **AUD A10** → `03:466–480`. Igual al Nuevo, salvo «(Ecuación~\eqref{eq:score-gated})», que va con minúscula, como el resto del archivo y como UH.

## No aplicados

- AUD A11, la frase opcional sobre el texto con ξ = 0 («en texto, además, la tolerancia agravaría la fuga…»): la propuesta la deja a elección del autor y no hay decisión. Con A11 se pierde la única referencia a `sec:limitaciones` desde este archivo; no rompe nada.
- AUD F2, F3 y la duda 4 (reemplazadas): no caen en este archivo.
- PH: ningún bloque cae en `03` (1a y 1b van en 04; lo demás, en 05, 06 y 07).
- Recorte min–max (decisión 10) y τ 90 % con 137 de 152 (decisión 7): no aparecen en `03`. A11 da τ = 16.61 y sus rechazos (1 de 1024 y 4 de 656), sin el porcentaje de fuga.
- Costo computacional: no hay nada en `03`.

## Historia de versiones que dejé para el autor

Ninguna. Después de aplicar, no queda en `03` ningún pasaje con historia de versiones. Busqué «versión», «anterior», «previ-», «nuevo», «antes», «ya no», «variantes», «evaluad-», «descart-» y fechas. Lo que queda es:
- «en su versión de ocho módulos» (`03:5`): es la que fija UH §0;
- «El mediador ya no participa en la recuperación» (`03:363`): habla de fase temprana contra madura, no de versiones;
- «16 variantes» (`03:80`) y «15 variantes» (`03:177`): describen el llenado actual.

## Para revisar

- `03:95` dice «el llenado de las memorias de dominio» al presentar el diagrama cuyo pie ahora es «Llenado de la memoria de contenido». No es falso: las $M^H_{\mathrm{dom}}$ de los ocho módulos son memorias de dominio. Ninguna propuesta lo cubre y no lo toqué. `06:288` usa la misma expresión.
- Pie de `tab:memorias`: «Para las heteroasociativas se indica…» se queda como estaba. Ahora todas las memorias de la tabla son heteroasociativas, así que la frase ya no distingue nada.
- No compilé. Las llaves cuadran igual que en el original: sobra una `}`, la de `\right\}` en la figura madura. Los 17 `\begin` tienen su `\end`. Las rutas nuevas del TikZ usan solo `calc` y `positioning`, que el archivo ya usaba. Conviene mirar las dos figuras al compilar.
