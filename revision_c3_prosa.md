# Revisión de prosa tras la corrida larga de imagen→texto y la doble compuerta (22 de septiembre de 2026)

Formato viejo / nuevo, como en `revision_fase3_prosa.md`. Nada de esto está aplicado; se aplica tras aprobación. Cifras de `results/experimento11/README.md` (10 semillas, 4 cortes) y del recálculo fuera de dominio con la columna «acepta con compuerta».

## Cifras nuevas que sustentan los cambios

Imagen→texto, 80 imágenes de prueba por semilla, 10 semillas:

| medida | brazo | N=25 | N=50 | N=100 | N=200 |
|---|---|---|---|---|---|
| responde (%) | M | 5.0 | 53.7 | 81.2 | 96.2 |
| | T-oráculo | 0.0 | 5.0 | 45.0 | 78.7 |
| | T-protocolo | 0.0 | 3.7 | 42.5 | 72.5 |
| dominio de otra clase (%) | M | 0.0 | 2.6 | 4.9 | 8.9 |
| | T-oráculo | 0.0 | 0.0 | 0.4 | 1.2 |
| | T-protocolo | 0.0 | 0.0 | 0.5 | 1.6 |
| acepta (homo latente; protocolo: directorio) (%) | M | 86.2 | 98.8 | 98.8 | 100 |
| | T-oráculo | 57.5 | 85.0 | 93.8 | 97.5 |
| | T-protocolo | 41.2 | 66.2 | 75.0 | 81.2 |

En N=200, precisión del dominio cuando responde: M 90.9 (antes 91.7 con 5 semillas), oráculo 98.5 (98.7), protocolo 97.8 (98.2). Dominio correcto: 87.4 / 77.5 / 70.9.

Fuera de dominio (40 consultas, aceptadas por semilla, igual en las 10):

| brazo | N=25 | N=50 | N=100 | N=200 |
|---|---|---|---|---|
| M | 2 | 2 | 3 | 3 |
| T-oráculo | 2 | 2 | 2 | 2 |
| T-protocolo (directorio) | 3 | 4 | 4 | 4 |
| T-protocolo con compuerta | 2 | 2 | 2 | 2 |

La compuerta atrapa `a piano with black and white keys` → dog (N ≥ 50) y `a thunderstorm with heavy rain` → car (todos los cortes), en las diez semillas; no toca a M ni al oráculo. Etapa 8 con la compuerta: 16/16, ninguna consulta legítima rechazada. Con los modelos oficiales v5, las 40 consultas las rechaza el propio directorio (sonda del 21 de septiembre): la fuga vive en los directorios reconstruidos de exp11, no en los oficiales.

---

## A. `results/experimento11/veredicto.md`

**A1. Línea 3, corridas.**

Viejo: «**Corridas:** 21 de septiembre de 2026. Texto→imagen: cortes N ∈ {25, 50, 100, 200} imágenes por clase (×4 variantes), 10 semillas (42–51), 3 sorteos por consulta, 171 consultas reservadas.»

Nuevo: «**Corridas:** 21 y 22 de septiembre de 2026. Texto→imagen: cortes N ∈ {25, 50, 100, 200} imágenes por clase (×4 variantes), 10 semillas (42–51), 3 sorteos por consulta, 171 consultas reservadas. Imagen→texto: los mismos cortes y semillas, 10 imágenes de prueba por clase. Fuera de dominio: 40 consultas, con y sin doble compuerta de contenido en el protocolo.»

**A2. Tabla de las curvas, filas de fuera de dominio (líneas 24–26).** Añadir una fila:

`| | T-protocolo con compuerta | 2 | 2 | 2 | 2 |`

**A3. Criterio 3 (línea 36).** Añadir al final del punto:

«Con la doble compuerta de contenido (el agente destino debe contener la pista, no solo el directorio señalarlo) el protocolo baja a 2 de 40 en los cuatro cortes, las mismas dos que el oráculo.»

**A4. Sección «Imagen → texto» (líneas 52–67).**

Viejo (encabezado): «## Imagen → texto (corte 200, 5 semillas, 10 imágenes de test por clase)»

Nuevo: «## Imagen → texto (cuatro cortes, 10 semillas, 10 imágenes de test por clase)»

Viejo (tabla, columna por columna): responde 96.2 / 78.8 / 72.5; hit laxo 95.2 / 78.8 / 72.5; hit estricto 93.0 / 78.5 / 71.5; dominio correcto 88.2 / 77.8 / 71.2; dominio de otra clase 8.0 / 1.0 / 1.2; precisión 91.7 / 98.7 / 98.2.

Nuevo (N=200): responde 96.2 / 78.7 / 72.5; hit laxo 95.2 / 78.7 / 72.5; hit estricto 92.8 / 78.0 / 71.5; dominio correcto 87.4 / 77.5 / 70.9; dominio de otra clase 8.9 / 1.2 / 1.6; precisión 90.9 / 98.5 / 97.8. Encabezado de la columna de medida: «medida (sobre 800 imágenes por brazo, N=200)».

Añadir después de la tabla:

«Por corte, la cobertura crece con el contenido en los tres brazos: el especialista responde el 0, 5, 45 y 79 % con 25, 50, 100 y 200 imágenes por clase; la EHAM única, el 5, 54, 81 y 96 %. La ventaja de cobertura de la EHAM única es máxima en N=50 (49 puntos) y baja a 17.5 en N=200. Su dominio ajeno sube con N (0, 2.6, 4.9, 8.9 %); el de los especialistas queda entre 0 y 1.6 %.»

Viejo (párrafo, línea 65): «[…] A cambio, el 8% de sus respuestas tienen dominio de otra clase: […] Los especialistas se equivocan de dominio el 1%. […]»

Nuevo: «[…] A cambio, el 9% de sus respuestas tienen dominio de otra clase: […] Los especialistas se equivocan de dominio entre el 1 y el 2%. […]» (el resto del párrafo no cambia: 21% fuera del soporte, 19% en el directorio y otro 9% en el recall siguen valiendo).

**A5. «Lo que este experimento no decide», primera viñeta (línea 75).**

Viejo: «- La especificidad fuera de dominio (P3): con 40 consultas la diferencia entre la EHAM única y los especialistas es una consulta. Lo que sí aparece es que el directorio deja pasar dos consultas que el contenido rechaza (`a piano with black and white keys` → dog, `a thunderstorm with heavy rain` → car, en las diez semillas): el índice de texto es relativo (16 niveles sobre 300 rasgos, exp10) y acepta pistas que la memoria de contenido no contiene. Es la fuga de la limitación (a) del reporte y el argumento para la doble compuerta.»

Nuevo: «- La especificidad fuera de dominio (P3): con 40 consultas la diferencia entre la EHAM única y los especialistas es una consulta. Lo que sí aparece es que el directorio deja pasar dos consultas que el contenido rechaza (`a piano with black and white keys` → dog, `a thunderstorm with heavy rain` → car, en las diez semillas): el índice de texto es relativo (16 niveles sobre 300 rasgos, exp10) y acepta pistas que la memoria de contenido no contiene. Es la fuga de la limitación (a) del reporte. La doble compuerta de contenido (el destino debe contener la pista; columna «acepta con compuerta» del README, campo `acepta_compuerta` en `raw/*_o0.json`) la cierra en este banco: el protocolo acepta 2 de 40 en los cuatro cortes, las dos originales con palabras del vocabulario (`food`, `table`), que también acepta el contenido. Lo que no se midió es cuánta cobertura legítima cuesta la compuerta sobre las 171 reservadas; en las 16 consultas de la etapa 8 no rechaza ninguna.»

**A6. Segunda viñeta (línea 76).**

Viejo: «- El hemisferio imagen→texto se corrió en versión corta (un corte, 5 semillas, 80 imágenes de test). Con los cuatro cortes se vería si la cobertura del especialista sube con N como en exp6.»

Nuevo: «- El hemisferio imagen→texto con los cuatro cortes confirma que la cobertura del especialista sube con N (0 → 79 %), como en exp6, y que la de la EHAM única sube antes (5 → 96 %). No decide si siguen subiendo más allá de 200 imágenes por clase, que es el máximo del split.»

## B. `CONTEXTO_SEP2026.md`

**B1. Línea 129 (fuera de dominio).** Añadir al final: «Recalculado el 22 de septiembre con la doble compuerta de contenido: el protocolo baja a 2/40 en los cuatro cortes, el nivel del oráculo; la columna «acepta» quedó idéntica.»

**B2. Nueva viñeta después de la 129:**

«- Imagen→texto largo (22 de septiembre, 134 min con 6 procesos): cuatro cortes × diez semillas × 80 imágenes de prueba. La cobertura del especialista sube con N (responde 0, 5, 45, 79 %) y la de la EHAM única antes (5, 54, 81, 96 %); el dominio ajeno de la EHAM única sube con N (0 → 8.9 %), el de los especialistas queda en 1.2–1.6 %. En N=200 las cifras de 5 semillas apenas se mueven (dominio ajeno 8.0 → 8.9).»

**B3. Nueva viñeta:**

«- Doble compuerta de contenido en la fase madura textual (22 de septiembre, commit 3538b4a): tras `route_transactive`, el agente destino debe dar `recognize_gated > 0` para alguna pista; si no, rechazo con motivo `content_no_support` conservando el destino señalado. En `stage8_mature.route_mature`, en los tres backends de la pestaña 4 de la app y en `ood_rows_for` de exp11 (campo `acepta_compuerta`, sin tocar `acepta`). Etapa 8: 16/16. En la app con los modelos oficiales v5 las 40 consultas fuera de dominio las rechaza el propio directorio. De paso: `route_mature` mandaba el latente a cuda y la app tiene el decodificador en CPU; ahora usa el dispositivo del decodificador.»

**B4. Sección 8 «Pendiente» (líneas 134–138).**

Viejo: las tres viñetas (tex8, deck, imagen→texto).

Nuevo:
«- Deck externo de Drive (`exp7-10_literatura_corta (2).pptx`): lista viejo/nuevo entregada el 22 de septiembre (envolvente 2.9 a 5.5, descripción 19.3 contra 21.9 y familiaridad, 3.5 saltos); sin aplicar.
- Medir el costo de la doble compuerta sobre el banco reservado de exp11 (171 consultas), si se quiere cerrar la limitación (a) del reporte con las dos cifras.»

## C. `INICIO_NUEVA_SESION.md`

**C1. Título y §1.** «estado al 21 de septiembre» → «estado al 22 de septiembre»; «último commit 6365c91» → el último de esta ronda.

**C2. §5, tabla.** Añadir dos filas:

`| imagen→texto largo | 4 cortes × 10 semillas; cobertura del especialista 0 → 79 % con N | results/experimento11/README.md |`
`| compuerta | doble compuerta de contenido en la fase madura textual; protocolo fuera de dominio 4/40 → 2/40 | stage8_mature.py, app_tme.py, run_experiment11_monolithic.py |`

**C3. §6, tabla de exp11 (líneas 54–55).**

Viejo: `| imagen→texto: responde / dominio ajeno (%) | 96 / 8 | 79 / 1 | 72 / 1 |` y `| fuera de dominio aceptadas (de 40) | 3 | 2 | 4 |`

Nuevo: `| imagen→texto: responde / dominio ajeno (%) | 96 / 9 | 79 / 1 | 72 / 2 |`, `| fuera de dominio aceptadas (de 40) | 3 | 2 | 4 |`, `| fuera de dominio con doble compuerta | 3 | 2 | 2 |`

Línea 57, añadir al final: «Con la doble compuerta el protocolo acepta 2/40 en los cuatro cortes. Imagen→texto con los cuatro cortes: la cobertura del especialista sube 0 → 79 % con N; la EHAM única 5 → 96 % y su dominio ajeno 0 → 9 %.»

**C4. §7, comando de imagen (línea 73).** `--cuts 200 --seeds 42-46 --img-per-class 10 --workers 12` → `--cuts 200,50,100,25 --seeds 42-51 --img-per-class 10 --workers 6` (con Chrome abierto caben 6; 134 min).

**C5. §8, trampas.** Añadir: «- **Streamlit no recarga los módulos de `src/` importados dentro de `main()`** (`from stage8_mature import route_mature`): tras editar uno hay que reiniciar el servidor, no basta con recargar la página.»

**C6. §9, pendiente.** Sustituir las cinco viñetas por las dos de B4.

## D. `.tex8`

**D1. `secciones/05_resultados.tex`, líneas 394–396.**

Viejo: «En imagen\,$\to$\,texto la EHAM única responde al 96\,\% de las imágenes de prueba frente al 79\,\% del especialista, y responde con un dominio ajeno el 8\,\% frente al 1\,\%.»

Nuevo: «En imagen\,$\to$\,texto la EHAM única responde al 96\,\% de las imágenes de prueba frente al 79\,\% del especialista, y responde con un dominio ajeno el 9\,\% frente al 1\,\%; la cobertura de ambas crece con el contenido (el especialista responde el 0, 5, 45 y 79\,\% con 25, 50, 100 y 200 imágenes por clase; la EHAM única, el 5, 54, 81 y 96\,\%). Fuera de dominio, sobre 40 consultas, el protocolo acepta 4 y la EHAM única 3; con la doble compuerta de contenido (el agente destino debe contener la pista) el protocolo acepta 2, como el oráculo.»

**D2. `secciones/06_discusion.tex`, limitación (a), líneas 154–160.**

Viejo: «La sonda de rechazo (Sección~\ref{sec:proto-completo}) muestra que 2 de 12 consultas fuera de dominio rutean hacia algún agente porque comparten tokens con labels legítimos. Con la cuantización por magnitud y directorios densos, el containment textual pasa con más facilidad que en la versión binaria, y la frontera semántica queda expuesta. Una doble compuerta de contenido (verificar que el agente destino contenga la consulta, no solo que el directorio la señale) es la mitigación diseñada pendiente de evaluación.»

Nuevo: «La sonda de rechazo (Sección~\ref{sec:proto-completo}) muestra que 2 de 12 consultas fuera de dominio rutean hacia algún agente porque comparten tokens con labels legítimos; con el banco de 40 consultas de la comparación con la EHAM única, el directorio del protocolo acepta 4, y en 2 de ellas (\emph{piano}, \emph{thunderstorm}) el agente destino no contiene la consulta. Con la cuantización por magnitud y directorios densos, el containment textual pasa con más facilidad que en la versión binaria, y la frontera semántica queda expuesta. Una doble compuerta de contenido (verificar que el agente destino contenga la consulta, no solo que el directorio la señale) cierra esa fuga: el protocolo acepta 2 de 40 en los cuatro cortes, las mismas que el oráculo, sin rechazar ninguna de las 16 consultas de referencia de la fase madura. Su costo sobre el banco reservado no se midió.»

**D3. `secciones/07_conclusiones.tex`, líneas 37–41** (ya propuesto en el chat): encabezado propio y «ocho veces menos» → «siete veces menos» (8.9 contra 1.2 con diez semillas).

Nuevo:
```
\paragraph{Frente a una EHAM única.}
Con el mismo contenido, el sistema transactivo no clasifica mejor; recuerda
con más fidelidad, no mezcla dominios cuando la pista es compartida y se
equivoca de dominio siete veces menos, a cambio de cubrir menos y de pagar un
índice.
```

**D4. `secciones/07_conclusiones.tex`, trabajo futuro, ítem 1 (líneas 56–58).**

Viejo: «\item \textbf{Doble compuerta de contenido en la fase madura textual}: cerrar la fuga de consultas fuera de dominio verificando el containment en el agente destino, no solo la señal del directorio.»

Nuevo: «\item \textbf{Costo de la doble compuerta de contenido}: la compuerta ya cierra la fuga fuera de dominio (Sección~\ref{sec:limitaciones}); falta medir cuánta cobertura legítima cuesta sobre el banco reservado.»

## E. `hallazgos_exp7_a_exp11.pptx`

**E1. Diapositiva 4.** Ya aplicado: «2.9 a 5.9 veces» → «2.9 a 5.5 veces» (decisión del plan; sin commit).

**E2. Diapositiva 7, tabla.** «imagen→texto: dominio correcto si responde | 92 | 99 | 98» → «91 | 98 | 98»; «imagen→texto: dominio de otra clase | 8 | 1 | 1» → «9 | 1 | 2». Las demás filas no cambian.

**E3. Diapositiva 8, cuarta viñeta.**

Viejo: «• En imagen→texto la EHAM única cubre más (96 vs 79) porque el containment del especialista es estricto en 64 coordenadas; el rechazo residual del 25% que reportaba la tesis es un costo de partir, no de la memoria»

Nuevo: «• En imagen→texto la EHAM única cubre más (96 vs 79) porque el containment del especialista es estricto en 64 coordenadas; la cobertura de los dos sube con N (el especialista 0 → 79 %, la EHAM única 5 → 96 %) y el rechazo residual del 25% que reportaba la tesis es un costo de partir, no de la memoria»

**E4. Diapositiva 12.**

Viejo: título «Pendiente» y las cinco viñetas (fase 3, fase 4, banco OOD e imagen→texto, exp12, app).

Nuevo: título «Cerrado después del deck, y pendiente», viñetas:
«• Fases 3 y 4: prosa reescrita con aprobación; la contradicción se resolvió restringiendo «no entrópico» al ruteo (salida 5.1)
• Exp11: banco de 40 consultas fuera de dominio (EHAM única 3, oráculo 2, protocolo 4); imagen→texto con los cuatro cortes: la cobertura del especialista sube 0 → 79 % con N
• Doble compuerta de contenido en la fase madura textual: el protocolo baja a 2/40, el nivel del oráculo; etapa 8 sigue 16/16
• Exp12: la brecha crece con el solapamiento de soportes en etiquetas (ρ 0.45, p 0.017); las 28 brechas son positivas
• App: fase temprana en vivo con directorios perspectivales; modelos v5 en models/
• Pendiente: costo de la compuerta sobre el banco reservado; deck externo de Drive»
