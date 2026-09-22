# Experimento 13: propuesta de diseño para la augmentación del llenado visual

**Fecha:** 22 de septiembre de 2026
**Estado:** propuesta. No hay código nuevo ni corridas. Cada decisión abierta está marcada como **[decisión]**.

---

## 1. Qué falta y qué dice hoy el reporte

El reporte atribuye el 25 % de rechazo del ruteo visual de test a «la conjunción AND sobre las 64 coordenadas simultáneas» y propone como palanca «densificar el llenado con augmentación más rica» (`.tex8/secciones/06_discusion.tex:162-168`). La exploración del código muestra que ese 25 % se produce en dos compuertas distintas, y que ninguna es la memoria de contenido tal como se llena hoy:

| compuerta | dónde | qué contiene hoy | qué rechaza |
|---|---|---|---|
| directorio visual `mem_dir_R` | `route_transactive(..., modality="image", xi=0)` en la fase B de la etapa 7 (`src/stage7_bidirectional.py:165-201`) | un registro por percepción de la fase A, **sin augmentar**: 128 imágenes propias (`train[200:328]`) más lo presenciado de los demás, solo en entrada y ganador (v5) | 25.0 % (v4) / 26.4 % (v5) de las 656 de test; **19 %** en exp11 con 10 semillas |
| recall de la hetero `mem_dom_H` | `recall_from_right` → `project` de `hetero_associative_4d.py:446-464` (AND por celda sobre las 64 coordenadas, sin tolerancia) | 800 registros por clase: 200 imágenes × 4 variantes (original, espejo, ±12°) | **19 %** de lo que el contenido acepta (oráculo de exp11: acepta 97.5, responde 78.7) |
| contenido `mem_dom_R` | `recognize_gated_right` (containment marginal, ξ=0, `stage7_bidirectional.py:75-90`) | los mismos 800 registros | 2.5 % (oráculo de exp11) |

Es decir: la augmentación actual ya resolvió el containment marginal del contenido (97.5 %), pero **el directorio se forma sin ella** y **la conjunción de la hetero no la aprovecha del todo**. Sin este desglose, «augmentación más rica» podría aplicarse donde no hace falta.

Dos datos que fijan la expectativa:

- exp6 (`results/exp6_capacity/report.md`), sin variantes: la aceptación de test propio sube 0 → 0 → 1.9 → 20 → 55.6 % con N = 25 … 328 imágenes por clase, con 0 % de falsos aceptos en todo el rango. Con las 4 variantes y N = 200 (exp11) el contenido acepta 97.5 %. La densidad es la palanca, y hasta ahora no ha costado falsos.
- El split es por imagen (`src/stage1_dataset.py:136-140`): las 82 de test por clase son vistas nuevas de los mismos 10 objetos. Lo que se mide es generalización a vista nueva, no a objeto nuevo (hallazgo M4 de `results/auditoria_integral/report.md:36-37`).

## 2. Pregunta

**¿Cuánto rechazo de imágenes nuevas quita la augmentación en cada una de las dos compuertas, y a qué precio en falsos aceptos?** Con dos preguntas subordinadas: si basta con augmentar la formación del directorio (lo más barato: no toca las memorias oficiales) y si la familia de transformaciones importa o solo importa la cantidad.

## 3. Factores

**3.1 Familia de variantes (V).** Conjuntos anidados, deterministas, en orden fijo (como `_augment_variants`, `src/stage5_fill.py:62-70`):

| V | variantes |
|---|---|
| 1 | original |
| 4 | + espejo, rotación −12°, +12° (**oficial**) |
| 8 | + rotación −6°, +6°, escala 0.9 y 1.1 (recorte o relleno centrado a 128×128) |
| 12 | + espejo rotado ±12°, brillo 0.85 y 1.15 |
| 16 | + traslación ±6 px en x y en y |

**[decisión]** La familia. Recomiendo esta: geometría primero (es lo que cambia entre vistas de ETH-80: pose y escala), fotometría después y poca (el fondo liso hace que brillo y contraste muevan el latente hacia la región de «color sólido» que hoy se acepta en falso, `06_discusion.tex:169-173`). Se pre-registra y no se cambia después de ver resultados.

**3.2 Dónde se aplica (A).**

| brazo | contenido (`mem_dom_H`, `mem_dom_R`) | directorio (`mem_dir_R`, fase A) |
|---|---|---|
| A0 oficial | V = 4 | V = 1 |
| A1 solo directorio | V = 4 (las memorias oficiales, bit a bit) | V |
| A2 solo contenido | V | V = 1 |
| A3 ambos | V | V |

A1 es el brazo barato y el que ataca la compuerta grande sin tocar `models/`. A2 aísla la conjunción de la hetero. A3 es la combinación. **[decisión]** Correr los cuatro; A0 es el control y sale gratis de A1 con V = 4 en el contenido y V = 1 en el directorio.

**3.3 Cantidad de imágenes de llenado.** Se mantiene N = 200 (`train[:200]`) para el contenido y `train[200:328]` para la fase A, como en el protocolo oficial, para no mezclar el efecto de la augmentación con el de más imágenes distintas. exp6 ya midió el efecto de N sin variantes. **[decisión]** Añadir un solo punto extra, N = 328 con V = 4 en el contenido, para saber si 128 imágenes reales más valen lo mismo que 3 variantes de cada una. Recomiendo sí: son 1312 registros más y una fila en la tabla.

## 4. Cómo se construye cada brazo (sin pasar por la etapa 5)

- Codificación: el encoder oficial (`load_encoder`), sobre las variantes generadas en PIL a partir de la imagen ya redimensionada a 128×128, como hace `stage5_fill.get_instance_latents`. En GPU son segundos. Los latentes continuos de cada V se guardan en `results/experimento13/latents_V{V}.json` con rutas relativas; el orden es image-major con variantes contiguas.
- Cuantización: `quantize_latent_global` con los **stats oficiales** `models/latent_global_stats.json`, en float32 (trampa conocida). No se recalculan los stats por V: cambiarlos cambiaría la representación y el control de bit a bit.
- Contenido: `build_specialists` de exp11 (`run_experiment11_monolithic.py:152-163`) con `VARIANTS = V`; para V = 4 el control `same_as_official` debe dar 8/8 (regresión).
- Directorio: la fase A de la etapa 7 (`stage7_bidirectional.py:138-152`) reescrita como función que recibe la lista de percepciones; con augmentación, cada percepción registra sus V variantes con el mismo ganador (el ganador se decide con la variante original, `recognize_gated_right`, como hoy). Protocolo v5: registran entrada, ganador y TME. Orden intercalado por clase, semilla del orden como en la etapa 7.
- Costo: cada registro de hetero cuesta ~80 ms. V = 16 en contenido: 3200 × 8 = 25 600 registros ≈ 34 min por brazo; total de contenidos (V = 1, 8, 12, 16 y N = 328) ≈ 1.5 h. Los directorios son `DirectoryMemory` y cuestan segundos. Cache por (V, N) como en exp11.

## 5. Bancos

- **Test visual completo:** las 656 imágenes de test (82 por clase), codificadas una vez y guardadas en `results/experimento13/test_latents.json`. Hoy solo hay 20 por clase en caché (`results/experimento7/latents_cache.json`); es la primera cosa que hay que producir.
- **Falsos entre dominios:** las mismas 656 evaluadas contra cada especialista ajeno (exp6 parte «falsos»), y el ruteo con entrada no especialista (`CLASSES[(ci+1) % K]`, como la etapa 7).
- **Sondas sintéticas:** las de la figura de rechazo de la etapa 7 (ruido, píxeles barajados, color sólido uniforme), para vigilar que densificar no abra la fuga de «color sólido». **[decisión]** Incluirlas; son 3 por clase y cuestan nada.
- **Semillas:** el llenado es determinista; la aleatoriedad está en el orden de la fase A y en la entrada del ruteo. 5 semillas (42–46). **[decisión]** 5 o 10; recomiendo 5, los intervalos de exp11 con 10 fueron de décimas.

## 6. Métricas, por brazo y V

Sobre las 656 de test:

1. **Contenido acepta:** `recognize_gated_right(especialista propio) > 0`.
2. **Responde:** `recall_from_right` reconoce (conjunción de la hetero).
3. **Hit top-3 estricto y dominio ajeno:** como exp11 (`image_strict`).
4. **Directorio acepta y rutea bien:** `route_transactive` desde entrada no especialista, ξ = 0; `acepta`, `ruteo_ok`, saltos.
5. **Falsos:** aceptación del contenido por especialistas ajenos; ruteos a otra clase; aceptación de las sondas sintéticas.
6. **Densidad:** celdas no nulas de `mem_dom_R` y de `mem_dir_R` por coordenada (la variable que la augmentación mueve), para poder decir «X registros más llenan Y celdas más».

Compuesta: **cobertura de punta a punta** = rutea bien y responde (lo que hoy es 81.2 × 72.5/81.2 ≈ 72 % en exp11).

## 7. Predicciones, con el mecanismo

- **P1 (directorio).** A1 sube la aceptación del directorio de ~74–81 % hacia la del contenido (97 %) al crecer V, porque el directorio rechaza por huecos marginales (`support_gaps`, ξ = 0) y cada variante llena celdas nuevas de las mismas 64 coordenadas. Los falsos ruteos siguen en 0: las variantes de una imagen de la clase c registran al ganador c.
- **P2 (hetero).** A2 sube «responde» de 79 % hacia «acepta» (97 %) más despacio que P1, porque el AND de `project` exige que el par (coordenada del latente, coordenada de la etiqueta) esté registrado, y las variantes de una imagen entran con la misma secuencia de etiquetas: densifican el lado del latente, no el cruce.
- **P3 (precio).** Los falsos entre dominios se mantienen en 0 mientras la familia sea geométrica; la fotometría (V = 12) es el primer punto donde puede aparecer aceptación de sondas de color sólido o de una clase ajena, sobre todo apple↔tomato.
- **P4 (N = 328 contra V = 4).** 128 imágenes reales más rinden más que 3 variantes por imagen para la hetero (traen vistas nuevas de verdad) y menos para el directorio (que ya presenció esas imágenes en la fase A).

## 8. Criterio de refutación

La hipótesis del reporte («la augmentación del llenado reduce el rechazo residual manteniendo cero falsos») queda **refutada** si, con V = 16 en A3, se cumple cualquiera de: (a) la cobertura de punta a punta no sube al menos 10 puntos sobre A0; (b) los falsos ruteos o los falsos aceptos de contenido superan el 1 % de las 656; (c) alguna sonda sintética pasa a aceptarse en más de la mitad de las clases. Queda **confirmada** si la cobertura sube ≥ 10 puntos con falsos ≤ 1 % y sondas sin cambio. Entre medias, se reporta la curva y dónde se quiebra.

## 9. Qué no decide

- Generalización a objetos nuevos (leave-object-out): requiere otro split y otro llenado. **[decisión]** Dejarlo fuera de este experimento y anotarlo; o añadir un brazo con el objeto 10 de cada clase reservado (410 registros menos por clase y un banco de 41 × 8 imágenes). Recomiendo fuera: cambia dos cosas a la vez.
- Si conviene cambiar `models/`: este experimento mide; el cambio del llenado oficial sería una etapa 5 nueva con re-verificación de 8/8 y de las etapas 6–8, y se decide después.

## 10. Entregables

`run_experiment13_augmentation.py` (reanudable, caché por (V, N), `--workers`, `--report-only`), `results/experimento13/{README.md, resumen.json, raw/, fig1_cobertura_vs_V.png, fig2_falsos_vs_V.png, veredicto.md}`, y la prosa viejo/nuevo para la limitación (b) y el trabajo futuro del `.tex8`.
