# Lectura de jurado de la reestructura por fases: metodología y cifras

Base: `fases` @ `0aaa025`. Revisé el texto nuevo o movido de los Capítulos 1 a 5, el Resumen, el Abstract, la Introducción, `ConclusionObjetivoGeneral.tex` y el Apéndice A, y lo cotejé con `results/`, incluidas `results/fase1_tres_modulos/` y `results/mundo_real/`. Los capítulos 2 a 5 se regeneraron con `generar_capitulos.py`, que terminó sin error («líneas de .tex8 que no aparecen en la salida: 0»). En el contenedor no hay `xelatex`, así que no compilé; falta comprobar que el Resumen y el Abstract siguen cabiendo en una página (cada uno ganó unas cuatro palabras).

La revisión de estilo y de patrones la hace otra sesión. Aquí solo cambié cifras, etiquetas y afirmaciones que no coincidían con su fuente.

## Veredicto

El reporte aguanta la lectura de metodología y cifras con correcciones menores. Todas las cifras de la fase 1 coinciden con `results/fase1_tres_modulos/` (`exp3_corrected_routing/summary.json`, `exp4_directory_formation/results_formation.csv` y `report.md`, `ablation_mdir_bias/ablation_report.md`), y el texto no cita ninguna cifra de κ de la fase 1. Las de la fase 4 coinciden con los README de los experimentos 7, 8, 9, 10, 12, 17, 18, 19 y 22, y las de la fase 5, con `results/mundo_real/`. La fase 1 se rotula con su arquitectura en todas partes, ninguna comparación de tres contra ocho módulos se presenta como controlada y las limitaciones (m), (n) y (o) cubren la comparabilidad entre fases, la fase 5 sin cifras y exp9.

Lo que había que corregir:
- el cuadro «real» de la fase 5, que no tiene fuente en `results/`;
- tres descripciones del protocolo anterior que se contradecían entre capítulos;
- una cifra sin fuente («10 de 10»);
- dos afirmaciones de exp12 y del rechazo que decían más que sus resultados;
- etiquetas del Apéndice A.

## Contradicciones de las sesiones de redacción, resueltas con la fuente

1. **exp19: 80.5 frente a 79.6 %.** Vale **80.5 %**: es la única cifra con fuente versionada, en `results/experimento19/README.md:15` («etapa 7, ruteo visual de test (656) | 96.2 % | 80.5 %»), y es la que usan la Tabla `tab:codificador-sin-clase`, la fase 4 de Resultados y la Discusión. El 79.6 % solo está en `sintesis_26oct_a_1nov.md`, que no está versionado (`inventario_hallazgos.md:13` y `:421`), y no se cita en ningún capítulo. El 79.6 que aparece en `05_resultados.tex` es otra cosa: la cobertura del pliegue 10 de exp16 con el codificador por pliegue. Lo único por corregir era la nota «por conciliar» del Apéndice A (cambio M5).
2. **El cuadro rechazado de la fase 5.** `results/mundo_real/selftest_frame.png` es la versión de `8075a6f`; su SHA-256 empieza por `34aacdb8`. Muestra la interfaz del laboratorio con el encabezado «MAE realtime | vision entra por: apple | mic: on | 26 fps | q salir m mute». El cuadro es gris uniforme, con un ícono de ventana con candado al centro, sin ningún objeto ni escena. Arriba a la izquierda dice «RECHAZO (nadie la reconoce)». No hay candidato más cercano, ni ropa, ni habitación. El cuadro de webcam con una escena real y «REJECTED (closest: apple 0.00)» que describe `inventario_fase3_mundo_real.md:61` es otro archivo: `realtime_lab/selftest_frame.png`, regenerado en `f75dde3` (25 ago, SHA-256 `fb975aa0…`). Ese no se copió a `results/mundo_real/`. Resultados (`05_resultados.tex`, Cámara) y Conclusiones ya describían bien el cuadro gris. El Capítulo 1 (alcances) y la Metodología (fase 5, Pruebas) seguían hablando de «un cuadro real ajeno a ETH-80», y se alinearon con la fuente (cambios P1 y P2). Si el autor quiere citar la escena real, hay que copiar el archivo de `f75dde3` a `results/mundo_real/` y decir con qué versión del sistema se corrió. Se hizo el 25 de agosto, después de la v5 de julio.
3. **κ con tres módulos.** El texto no cita ninguna cifra de κ de la fase 1. La creencia 3 de la Discusión usa las cifras de ocho módulos ya corregidas (81.2 → 0.0 %, `tab:grid-iota-kappa`). El Apéndice A dice que de `fase1_tres_modulos/exp2_iota_kappa` solo vale lo de ι, como el README de esa carpeta. No hay nada que cambiar.
4. **exp9: «90 de 411 con 16 interacciones».** El texto usa 100, 302, 332 y 368 de 411 tras 16, 60, 120 y 240 interacciones, y 393 con el pizarrón. Coinciden con las filas «… transactivo» y «240 pizarrón», columna `todas`, de `results/experimento9/formacion_texto/curva.json`. El 90 es la fila «0 transactivo» o la de las reservadas con 16 interacciones, y no se cita.

## Cambios mecánicos (aplicados directamente)

| # | Archivo (fuente `.tex8` → salida) | Viejo | Nuevo | Fuente |
|---|---|---|---|---|
| M1 | `06_discusion.tex`, limitación (m) → `Capitulo4.tex:2916` | «termina en 98.8 %» | «termina en 98.75 %» | `fase1_tres_modulos/exp3_corrected_routing/summary.json` (`mature_acc_b1` 0.9875); así lo dan la fase 1 de Resultados y las Conclusiones |
| M2 | `05_resultados.tex`, experimento 10 → `Capitulo4.tex:1627` | «El ruteo directo se queda en el 10.2 %, … mientras f es menor que 1/8» | «se queda entre el 10.2 y el 10.4 %» | `results/experimento10/README.md:24-25`: f = 1/64 da 10.2 y f = 1/16 da 10.4 |
| M3 | `05_resultados.tex`, experimento 12 → `Capitulo4.tex:1173` | «En todos los pares el solapamiento va de 0.57 a 0.65» | «el solapamiento de las etiquetas va de 0.57 a 0.65, y el latente, de 0.35 a 0.50» | `results/experimento12/README.md`, columnas «solap. etiquetas» (0.574 a 0.652) y «solap. latente» (0.348 a 0.500) |
| M4 | `07_conclusiones.tex` → `Capitulo5.tex:203` | «También cambió la fidelidad de 10 de 10 del primer prototipo, que contaba dos rechazos como coincidencias.» | «También cambió la coincidencia completa entre fases del primer prototipo, que contaba dos rechazos como coincidencias.» | El 10/10 solo está en el mensaje del commit `3f665ab` (`creencias_iniciales.md`, fila 2) y no tiene fuente en `results/` (regla 2 del brief). La creencia 2 de la Discusión ya lo decía sin la cifra |
| M5 | `ApendiceA.tex:316`, `experimento19` | «Vigente; dos cifras de enrutamiento (80.5 y 79.6 %) por conciliar.» | «Vigente; enrutamiento de prueba del 80.5 % (`README.md`).» | `results/experimento19/README.md:15` (punto 1 de arriba) |
| M6 | `ApendiceA.tex:280`, `experimento7` | arquitectura «final (lectura); texto en 32 niveles» | «8 anterior: registro por la clase verdadera y directorio visual sin variantes; texto en 32 niveles» | `results/experimento7/README.md:4,7`: maestro de registro = verdad de terreno; pool visual de la etapa 7. La limitación (o) y la creencia 6 ya lo ponían con el protocolo anterior |
| M7 | `07_conclusiones.tex` → `Capitulo5.tex:41` | «Esta respuesta tiene tres límites.» | «Esta respuesta tiene cuatro límites.» | El párrafo enumera cuatro: dentro de muestra, techo de la fase temprana, necesita B1 y no se repite con ocho módulos |
| M8 | `ConclusionObjetivoGeneral.tex:20-22` | «(91.0 frente a 89.7 % con 291 consultas de formación) y coincide con su decisión en el 92.5 %» | «… y, en el sorteo principal, coincide con su decisión en el 92.5 %» | El 91.0 y el 89.7 son medias de cinco sorteos (`tab:calibracion-fija`); el 92.5 % es del sorteo principal (`05_resultados.tex`, «Lo que sí se reproduce es la decisión») |

## Propuestas de afirmación (aplicadas en el mismo parche; las aprueba el autor)

### P1. Capítulo 1, Alcances, demostración en tiempo real (`Capitulo1.tex:244-247`)
- **Viejo:** «Toca como demostración lo que la evaluación excluye: Whisper traduce al inglés frases dichas en español o en inglés, y la cámara entrega cuadros reales, entre ellos uno ajeno a ETH-80.»
- **Nuevo:** «Toca como demostración parte de lo que la evaluación excluye: Whisper admite frases en español y las traduce al inglés, aunque la frase probada de punta a punta fue en inglés, y la cámara entrega cuadros de imágenes impresas y un cuadro gris sin objeto, ajeno a ETH-80.»
- **Fuente:**
  - `results/mundo_real/selftest_frame.png` (punto 2 de arriba);
  - `results/mundo_real/realtime_lab_README.md:36,55` (`task=translate`, «es/en → en»);
  - `results/mundo_real/smtex_05_resultados.tex`, «Cadena de voz»: el WAV dice «Farm animal that gives milk», en inglés.
- **Razón:** no hay ninguna frase en español probada ni ningún cuadro real ajeno a ETH-80 en `results/`.

### P2. Metodología, fase 5, Pruebas (`04_metodologia.tex` → `Capitulo3.tex:1311-1312`)
- **Viejo:** «…y en una hoja impresa con 16 imágenes, y un cuadro real ajeno a ETH-80 se pasó por el directorio visual.»
- **Nuevo:** «…y en una hoja impresa con 16 imágenes, y se pasó por el directorio visual un cuadro gris sin objeto, ajeno a ETH-80 (`selftest_frame.png`).»
- **Fuente:** `results/mundo_real/selftest_frame.png`. Ahora coincide con `05_resultados.tex` (Cámara, `Capitulo4.tex:1782-1784`) y con las Conclusiones (fase 5).

### P3. Metodología, fase 4, protocolo anterior (`04_metodologia.tex` → `Capitulo3.tex:1129-1138`)
- **Viejo:** «Los experimentos 8, 9 y 10 se corrieron antes de que el sistema adoptara los directorios perspectivales y una sola memoria de contenido. Usan el protocolo anterior, en el que todos los módulos registran todas las transacciones y sus directorios son idénticos, con el directorio visual llenado sin variantes y con las memorias homoasociativas al lado de la heteroasociativa. Los mecanismos que miden no dependen de las memorias homoasociativas, pero sus cifras no son las del sistema final. El experimento 9 se reporta con esa salvedad.»
- **Nuevo:** «Los experimentos 7 a 10 se corrieron antes de que el sistema adoptara los directorios perspectivales y una sola memoria de contenido, con el directorio visual llenado sin variantes. En el 8 y el 9 todos los módulos registran todas las transacciones, sus directorios son idénticos y las memorias homoasociativas están al lado de la heteroasociativa; el 10 parte de ese registro para medir directorios que divergen. Los experimentos 7, 8 y 10 miden sobre todo directorios. En el 9 el sustituto reconoce y evoca con sus memorias homoasociativas, que el sistema final ya no tiene, y por eso se reporta con esa salvedad. Ninguno da cifras del sistema final.»
- **Fuente:**
  - `results/experimento9/README.md:64`: «`evoke_labels` exige que la homo latente del sustituto contenga la imagen»;
  - `results/experimento10/README.md:23-31`: los directorios difieren hasta en el 83 % de sus celdas;
  - `results/experimento7/README.md:7`.
- **Razón:**
  - el texto viejo decía que los mecanismos no dependen de las homoasociativas, y la limitación (o) dice lo contrario para exp9 («el sustituto reconoce con una memoria que el sistema final ya no tiene»);
  - describía exp10 con «directorios idénticos», que es justo lo que ese experimento cambia;
  - dejaba fuera a exp7, que la Discusión pone en el mismo grupo («Los experimentos 7 a 10…»).

### P4. Tabla `fase:tab-arco`, pie (`04_metodologia.tex` → `Capitulo3.tex:582-584`)
- **Viejo:** «En la fase 4, tres experimentos (8, 9 y 10) usan el protocolo anterior, con cinco memorias por módulo y directorios iguales en todos los módulos.»
- **Nuevo:** «En la fase 4, los experimentos 7 a 10 usan un protocolo anterior al final, con el registro dictado por la clase verdadera o por todos los módulos y el directorio visual sin variantes; el 8 y el 9 llevan cinco memorias por módulo.»
- **Fuente y razón:** las mismas de P3, y la limitación (o) (`Capitulo4.tex:2943-2945`).

### P5. Discusión, partir el contenido: salvedad del rechazo (`06_discusion.tex` → `Capitulo4.tex:2417-2419`)
- **Viejo:** «Contra una EHAM única con las ocho clases, la partición empata en clase desde 50 imágenes por clase y gana en fidelidad, en rechazo y en no mezclar.»
- **Nuevo:** «…y gana en fidelidad y en no mezclar, y en rechazo con la salvedad de la limitación (g).»
- **Fuente:** `05_resultados.tex`, «Fuera de dominio» (sección `sec:eham-unica`). La diferencia solo es significativa con 200 imágenes por clase y con la doble compuerta (p = 0.031), y la doble compuerta se agregó después de ver esas 40 consultas. Sin ella, p = 0.22 (`results/experimento11_protocolo_corregido/`). Así lo dicen ya las Conclusiones y el encuadre aprobado (`1136610`).

### P6. Discusión, experimento 12 (`06_discusion.tex` → `Capitulo4.tex:2423-2428`)
- **Viejo:** «La brecha sí crece con el número de dominios mezclados: en promedio es de 2.54 con dos clases y de 5.66 con ocho, y la memoria de ocho queda peor en 26 de los 28 pares. Una memoria con más dominios mezcla más al recordar aunque sus dominios se solapen poco.»
- **Nuevo:** «La brecha sí es mayor con más dominios mezclados: en promedio es de 2.54 con dos clases y de 5.66 con ocho, y la memoria de ocho queda peor en 26 de los 28 pares. Una memoria con más dominios mezcla más al recordar, y en estos pares, cuyo solapamiento de etiquetas va de 0.57 a 0.65, la brecha no depende de cuánto se solapen.»
- **Fuente:** `results/experimento12/README.md`: ρ = 0.01, solapamientos de 0.574 a 0.652. El mismo README dice «no hay pares disjuntos».
- **Razón:**
  - «aunque sus dominios se solapen poco» no se midió, porque ningún par se solapa poco;
  - con dos puntos (2 y 8 clases), «crece con el número» dice más que «es mayor con más».

### P7. Resultados, experimento 12: salvedad del contenido (`05_resultados.tex` → `Capitulo4.tex:1175-1180`)
- **Viejo:** «Con la misma arquitectura y la misma medida, la fidelidad de una memoria baja con el número de clases que guarda (`results/experimento12/README.md`).»
- **Nuevo:** «Con la misma arquitectura y la misma medida, la fidelidad de una memoria baja con el número de clases que guarda. Como las dos llevan 200 imágenes por clase, M8 guarda también cuatro veces más registros que M2; en la EHAM única, con ocho clases, la brecha con el oráculo queda entre 4.6 y 6.2 de 25 a 200 imágenes por clase (Sección `sec:eham-unica`; `results/experimento12/README.md`).»
- **Fuente:**
  - `results/experimento12/README.md`: M2 con N = 200 y el mismo llenado que exp11; M8 es la EHAM de ocho clases de exp11;
  - brechas 4.6, 6.2, 6.1 y 5.7 en `05_resultados.tex`, «Fidelidad del recuerdo».
- **Razón:** el índice presenta exp12 como evidencia controlada del tamaño. Lo es en arquitectura y medida, pero el número de clases y el total de registros cambian juntos. Hay que decirlo, y exp11 muestra que, con ocho clases, cuadruplicar el contenido mueve poco la brecha.

### P8. Resumen y Abstract, orden bloqueado (`Resumen.tex:11-12`, `Abstract.tex:43-44`)
- **Viejo:** «…y el 98.75 % tras 80, dentro de muestra, y con el orden bloqueado por clase, 33.75 %.» / «…in-sample, and with class-blocked order, 33.75 %.»
- **Nuevo:** «…y con el orden bloqueado, 33.75 % mientras solo ve una clase.» / «…and with blocked order, 33.75 % while it sees one class.»
- **Fuente:** `fase1_tres_modulos/exp4_directory_formation/results_formation.csv`, filas `C_blocked`. El 33.75 % se mantiene de k = 13 a 27, mientras solo llegan consultas de `apple`. El final del orden bloqueado es 98.75 %, igual que el intercalado (`report.md`).
- **Razón:** como estaba, se leía como el resultado final del orden bloqueado.
- **Pendiente:** comprobar en el PDF que el Resumen y el Abstract sigan en una página.

### P9. Discusión, creencias iniciales: la que quedó fuera (`06_discusion.tex` → `Capitulo4.tex:2046-2047`)
- **Viejo:** «Quedaron fuera las creencias que no constan en ningún documento del proyecto.»
- **Nuevo:** «Quedó fuera una decimonovena creencia, de la aplicación industrial, que los resultados de este reporte no tocan.»
- **Fuente:** `plan_reestructura/creencias_iniciales.md`, fila 19 (resumen de CIFIN, fallas pequeñas). Sí consta en un documento, pero es de la aplicación industrial, que la decisión 1 del autor deja fuera. Las tablas tienen 18 filas y el índice pedía «las 19».

## Observaciones sin cambio
- `05_resultados.tex`, Cámara (`Capitulo4.tex:1782`): «El cuadro que entrega la cámara cuando el sistema operativo le bloquea el acceso» interpreta el ícono del candado; no hay una fuente escrita que lo diga. Si el autor prefiere no interpretar: «Un cuadro gris uniforme, con el ícono de un candado y sin ningún objeto, …».
- Ese cuadro gris es, en la práctica, un lienzo uniforme, del tipo de las sondas sintéticas que ya mide la fase 3. Con él, la fase 5 no agrega evidencia de rechazo con escenas reales. Las Conclusiones (fase 5) y la limitación (n) ya no lo presentan como tal.
- La pérdida de un miembro: «El grupo pierde la respuesta y conserva la ubicación» (Resultados, Discusión y Conclusiones). Junto a «la descripción responde el 100 %» puede leerse como contradicción. Se refiere a la respuesta del especialista, que es como lo dice `results/experimento9/README.md:27,79`. Lo dejo a la sesión de estilo.
- Creencias 1 y 2: «92.5 %» de coincidencia temprana-madura con ocho módulos es del sorteo principal, con 200 y 291 consultas de formación. Coincide en número con el 92.5 % de acierto temprano del pie de `tab:calibracion-fija`, que es otra medida. No es error, pero conviene no ponerlas juntas.

## Cifras cotejadas sin cambio (muestra)
- **Fase 1, `exp3_corrected_routing/summary.json`:**
  - 97.5 % temprana y 1.25 % de rechazo (1 por frontera léxica y 0 de la EAM);
  - 98.75 % madura B1 y 53.75 % cruda;
  - 97.5 % de concordancia, cuentas [78, 65, 53] y 1.567 bits.
- **Fase 1, `exp4_directory_formation/results_formation.csv` y `report.md`:**
  - todas las filas de `tab:fase1-formacion` (A y C, k = 1, 3, 13, 27, 40, 47, 67 y 80);
  - barajado: primer k de 15 a 24, sostenido de 24 a 44;
  - control crudo: 93.75 %, [84, 67, 45], 72.15 % acumulado.
- **Fase 2, `fase1_tres_modulos/ablation_mdir_bias/ablation_report.md`:**
  - A 53.75 %, B1 98.75 %, B2 75.0 %, F 80.0 %, G 98.72 % y D 52.82 %;
  - ganadores: apple 78.75 %, horse 17.5 % y car 2.5 %.
- **exp22, `results/experimento22/README.md`:**
  - imagen 96.2/3.5/0.3 contra 96.3/3.5/0.2, con 1 decisión distinta;
  - texto 28.7 contra 28.5, con 8 decisiones distintas (3 a favor del tamaño, 4 de B1);
  - 59.4 % de rechazo.
- **exp12:** brecha media 2.54 y 5.66 (recalculada de la tabla, 28 pares); 26 de 28; excepciones car–dog y car–horse; 93.9, 97.6 y 99.0; ρ 0.01, 0.21 y 0.49.
- **exp7:** 96.2, 81.9, 236 tokens, 23.8 contra 100, 91.2 y 88.8.
- **exp8:** 80/80, 80/80 y 112/112; de 2.9 a 5.5; 9 a 63 de 64; 59 % y 100 %; 3.3, 18.5 y 20.5; 10.4, 62.1 y 81.9.
- **exp10:** las 24 celdas de `tab:fase4-perspectiva`; 3.56 y 1.89 saltos; 83 %; 20.7 %; 91.0 y 93.6.
- **exp9:** 229 (55.7 %), 65 de 80 (81.3 %), 24.5, 19.3 contra 21.9, 89.2, 98.3, 16.1 y 52 registros; N240: 18.8, 27.6 y 35.2.
- **exp17:** 96.0, 48.0, 38.9, 0.025, 40.8, 51.2, 41.1, 47.0, 74.4, 55.5, 57.8 y 49.5.
- **exp18:** 62.7 a 72.3, 98 a 99, 1 a 6, 8 %, 91.2, 59.0, 65.9, 84.1, 90 contra 63; +8.5 y +4.7.
- **exp19:** 80.5, 2 → 83, 60.8, 14.4, 53.2, 44.8, 47.6, 75.6, 66.8 y 63.1 a 100.
- **Fase 5, `results/mundo_real/README.md`, `realtime_lab_README.md` y `smtex_05_resultados.tex`:** 336 ms, 302 ms, ≈0.6 s, 56 ms, ≈2 s, 54 ms, 26 fps, 22/18/15 de 24 y ≈0 sin rescate.
- **Comparación con la EHAM única (exp11 corregido):** 96.8 contra 96.9 %, p = 0.86; 71.4 contra 51.1 (`experimento11_protocolo_corregido/comparacion.md:108`, `experimento11/README.md:121`); 3.1 contra 10.9; 2 y 8 de 40.

## Etiquetas y citas
No se agregó ni se quitó ninguna `\label` ni ningún `\cite`.
