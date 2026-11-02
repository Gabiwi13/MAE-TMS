# Consejo de redacción: índice de propuestas

**Estado (2 nov 2026):** aprobado y aplicado todo, con las decisiones recomendadas (G: «Gonzalez» sin tilde, como ya estaba). La tesis compila sin errores ni referencias indefinidas (42 páginas). Lo que salió al aplicar va en `revision_post_aplicacion_prosa.md`, también aplicada. Ya hecho, fuera de la prosa: la medición del costo (102.9 min en CPU, copiada a `results/computational_cost/nov2026_cpu/` con una `NOTA.md`) y la figura 15 regenerada con τ (`generate_paper_figures.py`, copiada a `.tex8/figuras/`).

**Cómo se hizo.** 21 revisores (13 en fable, 8 en haiku) revisaron la tesis por cifras, claridad, consistencia, figuras, referencias, léxico, antipatrones de IA y forma; 5 consolidadores (opus) juntaron sus reportes por sección; yo verifiqué las cifras de los hallazgos altos contra `results/` y el código. Los reportes crudos quedan fuera del repositorio.

## Archivos, en el orden en que se aplicarían

| # | Archivo | Qué trae | Cambios aprox. |
|---|---|---|---|
| 0 | `revision_replanteamiento_prosa.md` | Aprobado. Quita «segunda versión que escala de 3 a 8». | 25 |
| 1 | `revision_consejo_hechos.md` | Correcciones de hecho, con ajustes al texto aprobado del replanteamiento (parte A), y 3 decisiones. | 45 |
| 2 | `revision_consejo_referencias.md` | `.bib` (7) y citas que no respaldan su frase (10), lo atribuido a Wegner (4). | 21 |
| 3 | `revision_consejo_prosa_main_01_02.md` | Resumen reordenado, introducción, marco teórico (dos errores de hecho: H2, H3). | 40 |
| 4 | `revision_consejo_prosa_03_04.md` | Arquitectura y metodología: definiciones que faltan, duplicados, auditoría en estado final, directorio compartido (H1). | 60 + 37 de términos |
| 5 | `revision_consejo_prosa_05.md` | Resultados: subsección de objetos nuevos, tabla de la EHAM única, definiciones. | 50 + 19 de términos |
| 6 | `revision_consejo_prosa_06_07.md` | Discusión y conclusiones: limitaciones reordenadas, Wegner atado a cifras, trabajo futuro desde las limitaciones (H4). | 30 + 7 de términos |
| 7 | `revision_costo_fig15_prosa.md` | Sección del costo reescrita y texto de la figura 15. | 4 |
| 8 | `revision_consejo_figuras.md` | Código de las figuras (español, «Módulo», leyendas, fig11 y fig16) y diagramas TikZ. | 16 |

Cada propuesta de prosa trae su Parte 3 (términos, decisión T) y su Parte 4 (forma), para aprobar en bloque.

## Cruces ya resueltos

- **Limitación de la reconstrucción visual (06):** manda `referencias` U8. El artículo de CIFAR-10 no habla de «autoencoders más profundos», así que el punto 2.3 de `prosa_06_07` se reemplaza por U8.
- **Entradas degeneradas (06:248–253):** si apruebas `prosa_06_07` 1.2 (que parte la limitación (b) en dos), su nueva (c) sustituye a `costo_fig15` 2c.
- **Evocación en 06:243:** `prosa_06_07` 1.2 deja sin efecto `hechos` E10 en ese punto.
- **La cita de la EHAM** (`morales2024hetero` → `morales2025missing`, `referencias` U2) se aplica también sobre el texto nuevo del resumen.
- **Hechos corregidos por los consolidadores:** E5 (fueron tres condiciones a la fase madura, dos nativas) y E15 (la fase madura sube 2.5 puntos, no 2.6). Ya están corregidos en el archivo.

## Decisiones que te tocan (recomendación primero)

| # | Decisión | Recomendado | Alternativa y costo |
|---|---|---|---|
| D1 | Escala min-max del latente: el archivo con que se midió todo se calculó con 4 variantes; el código la recalcularía con 16 en una réplica desde cero (`hechos`, D1). | Declararlo en 04 y fijar el código a las variantes 0–3 (≈5 líneas). No cambia ninguna cifra. | Recalcular con 16 y re-correr la batería visual: decenas de horas. |
| D2 | Los dos falsos enrutamientos como vistas de `horse7`: no está en `results/`. | Quitar la identidad (3 frases). | Imprimir la lista por imagen de la etapa 7 y correrla (≈5 líneas de código y ≈40 min de CPU). |
| D3 | Presentar el experimento 12 para respaldar que el latente no explica el sesgo hacia `apple`. | No: el texto nuevo dice que no se midió. | Un párrafo y una tabla corta en 05. |
| T | Términos en español en la prosa: etiqueta, codificador, contención, enrutamiento, prueba, puntuación, recuperación, aumento de datos. | Sí, en bloque (≈70 sustituciones). | Dejar los anglicismos en cursiva como términos técnicos. |
| E | Expansión de la sigla: «EAM-TMS (*Entropic Associative Memory – Transactive Memory System*)». | Confirmar. | Otra expansión. |
| G | ¿«González» con tilde en la portada? | — | — |
| N | Cifras que entran nuevas en la tabla de la EHAM única (enrutamiento por corte, distancias con 25–100, dominio ajeno). | Tabla completa. | Solo la columna de 200 imágenes por clase. |
| S | La figura 16 muestra recuerdos muestreados; para que su pie no cambie al regenerarla, `random.seed(0)` fija (declarada, sin ajustar). | Sí. | Dejarla sin semilla y leer el conteo del pie de cada corrida. |
| R | Renombrar `fig04_…_N80.png` y `fig09_…_N80.png` a `_N400` (muestran N = 400). | Sí. | Dejar los nombres. |

## Costo de aplicar todo

- Unos 330 cambios en 8 archivos `.tex` y el `.bib`. Los aplicaría un agente por archivo (en paralelo entre archivos, en el orden de la tabla dentro de cada uno), y yo reviso el diff y compilo. Unos 60–90 min.
- Figuras: regenerar las 6 PNG con `--solo` toma unos 6 min; los dos diagramas TikZ hay que compilarlos y ajustarlos (unos 15 min).
- Después: el PDF para que lo revises, y la lectura de jurado en la nube (créditos hasta el 5 nov), que necesita commit y push antes.
