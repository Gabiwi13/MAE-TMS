# Grupo 4: `06_discusion.tex`, `07_conclusiones.tex` y `referencias.bib`

Fuentes: `revision_una_hetero_prosa.md` (§0, §4a–4c, §5), `revision_tesis_auditoria_prosa.md` (parte 3, A1–A13 y B1–B3) y `revision_pesos_homo_principal_prosa.md` (§3 y §4). Las líneas son las del archivo ya editado. No se compiló ni se hizo commit.

## Cambios aplicados

### `06_discusion.tex`

- Auditoría A13 → 06:11 («actualización perspectival del directorio»).
- Una-hetero §0, prefijos → 06:10 («heteroasociativos»).
- Decisión del autor, 50 % → 06:16–17 (quitado).
- Auditoría A1 → 06:21–23 (90.0 %).
- Pesos homo §3, línea 50 → 06:50 (85.2 frente a 93.0).
- Pesos homo §3, línea 56 → 06:56 (93.5 frente a 93.0).
- Pesos homo §3, línea 72 → 06:72 (13.8 %).
- Auditoría A2 → 06:73 (76 %).
- Pesos homo §3, línea 109 → 06:109 (93.0 %).
- Auditoría A3 → 06:122 («76 y 88\%»).
- Auditoría A4 → 06:129–138.
- Una-hetero §4a (subsección nueva) → 06:141–185, después de la subsección de Wegner.
- Auditoría A5 y decisión 12 → 06:190–212.
- Auditoría A6 → 06:229–230.
- Auditoría A7 → 06:232–235.
- Auditoría A8 → 06:238–239 (el resto del párrafo queda igual, como dice A8).
- Auditoría A9, primer bloque → 06:259–265.
- Auditoría A9, segundo bloque → 06:267–271.
- Auditoría A9, tercer bloque → 06:272–275.
- Auditoría A10 → 06:310–312.
- Auditoría A11 y decisión 13 → 06:317–327.
- Auditoría A12 → 06:332–333.
- Una-hetero §4b, limitación (i) → 06:347–352.
- Una-hetero §0, «agente» → «módulo» (17 apariciones) → 06:9, 38, 43, 44, 47, 51, 60, 63, 106, 107, 130, 219, 221, 225, 288, 343; la de la limitación (b) desapareció con A8, cuyo texto nuevo ya dice «módulo» (06:239).

### `07_conclusiones.tex`

- Una-hetero §0, «multi-agente» y «agentes» → 07:4–5.
- Una-hetero §0, prefijos → 07:6 («heteroasociativa»).
- Pesos homo §4, líneas 14–16 → 07:14–16 (93.0, 95.8 y 13.8 %); «el agente» → «el módulo» en 07:16.
- Auditoría B1 → 07:26–28 («por agente» → «por módulo»).
- Una-hetero §0 → 07:33 («de 3 a 8 módulos»).
- Auditoría B2 y decisión sobre el 50 % → 07:35–36.
- Pesos homo §4, línea 36 → 07:37–38 (20 % → 13.8 %).
- Auditoría B3 → 07:44–48.
- Una-hetero §5 (párrafo nuevo) → 07:50–57, después de «Frente a una EHAM única».
- Una-hetero §0, «agente» → «módulo» → 07:75 y 07:80.
- Una-hetero §0, «multi-agente» → 07:86–87.

### `referencias.bib`

- Una-hetero §4c → 11 entradas nuevas al final (`clark1996global`, `mayes2004associative`, `fortin2004recollection`, `old2008differential`, `eichenbaum2007medial`, `squire2007recognition`, `diana2007imaging`, `plaut2002graded`, `beauvois1982optic`, `brown1966tip`, `hart1965memory`). Ninguna clave estaba antes; el archivo queda con 25 entradas, sin duplicados.

## Ajustes y por qué

- **Prefijos y «módulo» en los bloques nuevos.** El texto nuevo de A4 decía «por agente»; va «por módulo». El de §5 decía «homo-asociativas» y «hetero-asociativa»; van sin guion. El texto de §4a ya venía con «módulo» y sin palabras con guion.
- **50 % en 06:16.** Quedó «la precisión temprana de 8 clases caía y dos clases colapsaban a 0\%». Ninguna propuesta trae texto nuevo para esta frase; solo se quitó la cifra.
- **B2 sin el 50 %.** Quedó «que llevó la precisión temprana al 88\%; el llenado de 16 variantes la subió a 90\%». Ver «Para el autor», punto 1.
- **Decisión 12 en A5.** La media frase va justo después de «que la EHAM única responde». Dice «el protocolo de esta comparación» y no «de este experimento» ni «de exp11», porque el párrafo no nombra el experimento y la tesis no lo llama «experimento 11» en la prosa.
- **A11 y decisión 13, limitación (f).** El texto nuevo de A11 trae historia de versiones («también se había fijado así ($\xi = 2$), pero la versión actual lee estricto»). La regla del estado final la saca. Las 16 variantes ocupan el lugar de $\xi = 2$ como segundo elemento elegido mirando test, así que «Dos elementos» y «Ambas selecciones» se conservan. Texto nuevo: «…y las 16 variantes del llenado, adoptadas después de ver el experimento 13, que mide sobre las 656 imágenes de test (son el valor más alto de su rejilla, no un óptimo ajustado). La lectura del directorio visual es estricta ($\xi = 0$) y no deja tolerancia que ajustar.» Lo del valor más alto sale de la duda 4 de la auditoría; lo comprobé en `results/experimento13/README.md`, donde la rejilla es V ∈ {1, 4, 8, 12, 16}. La referencia a `sec:parametros` desaparece con la frase de $\xi$.
- **A9, primer bloque.** El texto nuevo sigue con «La norma y la varianza del latente…» del párrafo viejo, que se queda.
- **4a.** Antes del `\subsection` va el comentario separador `% ----`, como en las demás subsecciones. La propuesta no le pone `\label` y no se lo agregué.
- **Formato BibTeX.** Las entradas van con un campo por línea, como el resto del archivo. Los datos son los de la propuesta (Brown y McNeill sin DOI y con el volumen 5, como dice §4c).
- **Reflujo** de 07:37–39, para que «y la» no quedara sola en su línea.

## No aplicados

- **Pesos homo §5 (opcional, metaconocimiento perspectival).** Es opcional y no está en la lista de decisiones.
- **Pesos homo §6 y §7.** Tocan documentos fuera de la tesis; §7 dice que la línea 111 de 06 no se toca.
- **Dudas de la auditoría sin decisión del autor.** La duda 6 (agregar `apple` a A3) no se aplicó: A3 quedó como su «Nuevo». La duda 7 (el «625 de 656») no hace falta aquí, porque A8 quita esa frase de 06.
- **Una-hetero §0, `main.tex`, título y demás archivos:** son de otros grupos.

## Para el autor

### Pasajes con historia de versiones que ninguna propuesta cubre (no se tocaron)

- 06:8: «El resultado central de esta versión…».
- 06:9: «Al pasar de tres a ocho módulos…». Solo cambió «agentes» por «módulos».
- 06:15–17: «con la binarización por signo heredada de la versión anterior…». Ya no tiene el 50 %, pero sigue contando la versión anterior.
- 06:51: «…no era un artefacto del caso de tres módulos».
- 06:63–74: «Las corridas iniciales…», el reentrenamiento del encoder, «subió de ≈52 % a 86 %… (76 % con el llenado de 16 variantes)». A2 y pesos homo §3 solo actualizaron las cifras.
- 06:106–107: «Con tres módulos, 10 consultas por dominio bastaban…» (sistema de tres módulos).
- 06:224: «…que en la versión binaria».
- 06:247: «Esta versión adopta las 16 variantes». A8 dice que ese resto del párrafo queda igual, pero la frase dice «esta versión».
- 06:257–258: «con 16 variantes la aceptan tres especialistas en vez de uno». Puede ser resultado de exp13 o exp14 y no historia; conviene revisarlo.
- 07:4: «la versión de ocho módulos». Va en línea con el título, que conserva «Versión de 8 módulos».
- 07:16: «el módulo históricamente sesgado».
- 07:32–33: «pasan de 3 a 8 módulos sin cambios de mecanismo».
- 07:35–36: B2 compara versiones: el 88 % sale del historial de git (`57e61f3~1`, llenado de 4 variantes), y «el llenado de 16 variantes la subió a 90\%» cuenta el cambio. Lo apliqué como propuso la auditoría, sin el 50 %. Si se prefiere el estado final puro, en línea con A1: «(resuelta con la cuantización por magnitud: la precisión temprana es del 90\%)».
- 07:59: «\paragraph{Lecciones de esta versión.}».

### Otras observaciones

1. **Etiquetas de otros archivos.** `eq:marginal`, `sec:una-memoria` y `tab:lesion` todavía no están definidas en el `.tex8`: las agregan los grupos de 02 y 05. Hasta que lleguen, 06 da referencias indefinidas.
2. **«módulos externos de clasificación» (07:9).** Ahora que «módulo» es la pieza del sistema, la frase puede leerse ambigua. Una opción: «sin clasificadores externos».
3. **«miembros» para piezas del sistema.** «no solo con el número de miembros» (06:111) y «Rotación de miembros» (07:79) hablan de los módulos, no de los miembros de Wegner. La regla solo cambia «agente», así que los dejé.
4. **Errata sin tocar (07:62–63).** Dice «la sesgo ``léxico''»; debería ser «el sesgo».
5. **«hoy» en 4a (06:179).** El texto dice «y hoy se trata igual que un rechazo». No es historia de versiones, pero el adverbio fecha el texto. Lo dejé como venía.
