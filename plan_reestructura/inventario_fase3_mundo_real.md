# Inventario de evidencia: fase 3, interacción con el mundo real (voz y cámara)

Solo lectura. Rutas relativas a `MAE-TMS` salvo que diga `una-hetero` (worktree `MAE-TMS-una-hetero`). Las líneas de `realtime_lab/README.md` y `.SMTex/` son las del árbol actual (rama `exp7-directorio-unificado`), que coinciden con `origin/v5-multimodal` después de la auditoría.

Aviso de nombres: en `CONTEXTO_SEP2026.md:102` y `:128`, «fase 3» es la reescritura de la prosa del 21 de septiembre, no este laboratorio. Conviene ponerle otro nombre en el reporte, por ejemplo «extensión en tiempo real».

## 0. Dónde está

| Pieza | Ubicación | Estado |
|---|---|---|
| Laboratorio | `realtime_lab/` (README, `main.py`, `audio_worker.py`, `stt.py`, `router.py`, `overlay.py`, tres `test_*.py`) | introducido en `8075a6f`/`b18cc53` (30 jul 2026); presente en HEAD y en una-hetero |
| Reporte de la extensión | `.SMTex/` (main + 7 secciones + 3 figuras), «Julio 2026» (`.SMTex/main.tex:49`) | no hay PDF compilado en el árbol |
| Auditoría | `una-hetero/results/auditoria_integral/report.md` (idéntica a la de `MAE-TMS`) | 2 ago 2026, rama `v5-multimodal` (`report.md:3`) |
| Material de las pruebas físicas | `phone_test_images/`, `hoja_impresion_eth80.pdf` | en `.gitignore:34-36`; no están en disco |
| Grabaciones, WAV, logs o JSON de las corridas del lab | ninguno | no existen en `realtime_lab/`, `results/` ni `research_notes/` |

No hay en `una-hetero/results/` ni en `MAE-TMS/results/` ninguna carpeta de audio, voz, cámara, tiempo real ni latencia. `results/hemisferio_visual/` es el log de la etapa 7 sobre imágenes ETH-80 digitales, sin fotos de cámara.

## 1. Qué hace el laboratorio

- **Plataforma:** ventana nativa en Python (OpenCV y sounddevice), con tres hilos: audio, visión e interfaz (`realtime_lab/README.md:8`, `:29-48`).
- **Voz:** micrófono a 16 kHz mono en bloques de 30 ms (`audio_worker.py:16-17`). La segmentación es un VAD propio por energía con piso de ruido adaptativo (`audio_worker.py:2`, `:35`, `:80-83`). La frase se cierra tras 0.6 s de silencio (`audio_worker.py:20`). Whisper `small` corre con faster-whisper en GPU float16, con respaldo a CPU int8 (`stt.py:25-31`), en `task="translate"` (se habla español o inglés y sale texto en inglés), con beam 5 en los finales y `vad_filter=False` (`stt.py:42-44`). Muestra subtítulos parciales mientras uno habla.
- **Enrutamiento por voz** (`README.md:182-196`; `.SMTex/secciones/01_introduccion.tex:66-74`), con dos modos:
  - temprano: difusión del TME, en la que los 8 módulos puntúan y el directorio de sesión aprende de cada frase;
  - maduro: el módulo de entrada consulta su M_dir con lectura B1 (`route_multi`) y redirige o rechaza, con el TME apagado.
- **Respuesta:** evocación asíncrona en un hilo aparte (recall de la memoria y luego el decoder), con prototipo y objeto definido y sus distancias (`main.py:195-218`; `.SMTex/secciones/05_resultados.tex:181-190`).
- **Cámara:** recorte central ajustable (55 % por omisión), luego ResNet18 a 128×128, latente cuantizado y directorio visual del módulo de entrada (`predict_tolerant`/`route`, ξ = 2). Se analiza cada ~250 ms con mayoría de 5, hay rechazo con el candidato más cercano y un recuadro de «lo que ve el ojo» (`README.md:37-39`, `:141-159`). Si el intento crudo se rechaza, se reintenta con corrección de color «reintentar con lentes» (`README.md:161-177`).
- **Hardware:** GPU NVIDIA RTX 2050 solo para Whisper, y CPU para el encoder y las memorias (`.SMTex/secciones/04_metodologia.tex:11-15`). No está claro si es la misma máquina de la tesis, que reporta un Intel Core Ultra 7 265HX (`una-hetero/.tex_uacj/Capitulo4.tex:1268`).
- **Versión del sistema:** v5 multimodal (julio de 2026), con 8 módulos sobre ETH-80. Cada módulo tiene 3 memorias de contenido: la hetero `mem_dom` y dos homo, `mem_dom_L`/`mem_dom_R` (`git show 8075a6f:src/stage5_fill.py:216-228`; `git show 8075a6f:realtime_lab/router.py:46-47`), más M_dir textual, directorio visual `mem_dir_R` y TME.
  - En la rama actual el router sigue cargando las 3 memorias (`realtime_lab/router.py:46-48`).
  - En una-hetero se adaptó a una sola hetero por módulo (commit `0c70824`, diff de `router.py`; `una-hetero/UNA_HETERO.md:13`).
  - No hay ninguna corrida del lab documentada con esa versión.

## 2. Evaluaciones con cifras

Todas vienen de corridas del 16 al 18 de julio de 2026 con los modelos v5. Ninguna tiene log, JSON ni archivo de salida guardado. La única fuente es el README (las anotó el autor a mano) y el `.SMTex` que las copia.

| Medición | Cifra | Fuente | Estado |
|---|---|---|---|
| Transcripción, frase corta en GPU | 336 ms | `README.md:113`; `.SMTex/secciones/05_resultados.tex:19` | vigente para v5; sin archivo crudo; n = 1 frase |
| Enrutamiento de texto (8 módulos) | 302 ms | `README.md:113`; `05_resultados.tex:20` | igual |
| Fin de habla a decisión | ≈ 0.6 s | `README.md:19`, `:113`; `05_resultados.tex:21` | igual |
| Evocación asíncrona | ~2 s (token `farm`, peso 9142) | `README.md:114`; `05_resultados.tex:27`, `:50-51` | antes «≈2.1 s» sin fuente (M9); el dato crudo de 2089 ms no está en el repo (`auditoria report.md:51-52`) |
| Análisis visual por cuadro / interfaz | 54 ms / 26 fps | `README.md:115`; `05_resultados.tex:23-24` | vigente para v5; sin archivo crudo |
| Micrófono WASAPI en reposo | RMS 0.0013 | `README.md:116`; `05_resultados.tex:66` | sonda, no evaluación |
| Redirección madura apple → cow | 56 ms, `routed=True` | `README.md:194-196`; `05_resultados.tex:47` | n = 1 |
| Cuadro sintético con cow al 55 % | rutea en 98 ms | `README.md:158-159`; `05_resultados.tex:72` | n = 1, sin cámara |
| Cuadros ETH-80 por `route_frame` | car → car; cow/dog → rechazo | `README.md:117` | cualitativo (3 casos) |
| Hemisferio visual del sistema base | «75.0 % de ruteo, 25 % de rechazo» | `README.md:117`; `.SMTex/01_introduccion.tex:9`, `05_resultados.tex:76-77`, `06_discusion.tex:99-103` | **obsoleta**: la cifra vigente es 631/656 = 96.2 % (`una-hetero/results/hemisferio_visual/stage7_bidirectional.log:26`; `.tex_uacj/Capitulo4.tex:535`) |
| La misma, versión previa | «47.1 % de ruteo visual» | `git show 8075a6f:realtime_lab/README.md:113` | **retractada** (M7); ya no aparece en HEAD |
| Política de color, banco simulado de 24 imágenes de test ETH-80 | limpia 22/24 (el reintento actuó en 1/24); grisácea media 18/24; grisácea fuerte 15/24 (antes «~0») | `README.md:174-175`; `.SMTex/05_resultados.tex:102-104` | vigente para v5; el script existe (`test_colorfix.py`) pero su salida no se guardó; «~0» es aproximado; degradación simulada, no cámara |
| Detector por distancia de momentos | medianas 24.2 contra 27.1 (se traslapan) | `README.md:171-172`; `05_resultados.tex:116-117` | hallazgo negativo; sin archivo crudo |
| Prueba física con celular | falló | `README.md:127-129`; `.SMTex/04_metodologia.tex:48-51` | cualitativo, sin conteo |
| Prueba física con hoja impresa n.º 1 | «solo cow fiable» | `.SMTex/05_resultados.tex:85`; `04_metodologia.tex:60` | cualitativo |
| Prueba física con hoja impresa n.º 2 | «solo cow fiable, apple/dog una vez» | `README.md:163-164` | cualitativo; tras la corrección de color no se repitió la prueba física |
| Voz en la prueba física | «voz ✓, visión ✗» | `README.md:141` | cualitativo, sin frases ni conteos |

**Lo que no existe:**
- tasa de error de transcripción (WER) o de palabras;
- porcentaje de aciertos de enrutamiento por voz en un banco de frases habladas;
- distribución de latencias (todas son mediciones únicas);
- conteo de aciertos con cámara física;
- fotos guardadas de objetos reales.

La frase de voz evaluada de punta a punta se inyectó desde un WAV, no se habló en vivo (`.SMTex/04_metodologia.tex:22-25`, `05_resultados.tex:41-43`). La de la Figura `panel_prototipo_definido.png` muestra en pantalla «stt 0 ms + ruteo 105 ms», lo que indica que se metió como texto y no pasó por Whisper. Lo dice la imagen; no hay fuente escrita.

**Imágenes reales fuera de ETH-80:** solo `realtime_lab/selftest_frame.png` (regenerada el 25 ago, commit `f75dde3`). Es un cuadro de webcam real (ropa y habitación) que el sistema rechaza con «REJECTED (closest: apple 0.00)». Es un único cuadro, sin protocolo, y sirve solo como demostración.

## 3. Observaciones de la auditoría

Según la auditoría, los tres lotes están aplicados (`report.md:94-104`). Lo comprobé en el código actual:

- **M6** (VAD Silero declarado): **cerrada**. `README.md:32-35` y `:93-95` describen el VAD por energía, y `.SMTex/02_marco_teorico.tex:48-51` dice que Silero existe pero está desactivado (`vad_filter=False`). Ya no se menciona Silero en la introducción ni en la arquitectura.
- **M7** (47.1 %): **cerrada** en el README (`README.md:117` dice 75.0 %/25 %). Pero el 75.0 % que la sustituyó también está obsoleto frente al 96.2 % vigente (ver tabla).
- **M9** (2.1 s): **cerrada** en el texto (`05_resultados.tex:27` dice ≈ 2 s). La medición cruda sigue sin estar en el repo.
- **M10** (teclas): cerrada (`README.md:106-107`).
- **M4** (partición por imagen, solape de instancias del 100 %): declarada en `.SMTex/06_discusion.tex:100-107`. En la tesis actual existe además el leave-object-out (exp16), que el `.SMTex` no conoce.

**Lo que habría que corregir antes de citarlo:**
1. Cambiar «75.0 %/25 % de rechazo residual» por la cifra vigente, o decir que el lab se midió con la versión v5 del sistema.
2. Las cifras del sistema base en `.SMTex/01_introduccion.tex:7-10` (98.75, 88.0, 93.2, 75.0) son de v5. No las verifiqué contra las vigentes, salvo la visual.
3. No hay ninguna corrida del lab con la versión final de una sola hetero, así que todas las latencias son de la arquitectura de 3 memorias por módulo.
4. Las cifras no tienen archivo crudo. Para citarlas como resultado conviene guardar la salida de `--wavtest`, `--selftest` y `test_colorfix.py` en `results/`.
5. La tesis declara fuera del alcance justo lo que toca el lab: «Fotografías de otro origen… y consultas en otros idiomas» (`.tex_uacj/Capitulo1.tex:221-222`) y «no se probó con fotografías reales de otras categorías» (`Capitulo4.tex:1497`, `:1675`; `Capitulo5.tex:79`, `:200-203`). Si el lab entra como objetivo, hay que ajustar esas frases.

## 4. ¿Se puede reportar hoy sin experimentos nuevos?

Sí, pero solo como **demostración de integración**, con las latencias como mediciones únicas en un equipo y las pruebas físicas como diagnóstico cualitativo, no como evaluación cuantitativa.

**Se puede afirmar:**
- la cadena voz → Whisper → enrutamiento por memoria → evocación funciona de punta a punta en ≈ 0.6 s más ~2 s asíncronos (n = 1, WAV inyectado);
- la visión corre a 26 fps con 54 ms por análisis;
- el rechazo funciona ante un cuadro real ajeno a ETH-80 (1 cuadro);
- la cámara física con impresiones solo fue fiable con cow;
- la corrección de color recupera 15/24 en simulación.

**No se puede afirmar:**
- exactitud de la transcripción;
- exactitud del enrutamiento por voz;
- tasa de aciertos con la cámara;
- que el lab funcione con la versión final de una sola hetero.

Todo esto entra como limitación. Para que sea un objetivo cuantitativo haría falta al menos:
- un banco de frases habladas con WER y acierto de enrutamiento;
- latencias repetidas con su distribución;
- un conteo físico con la hoja impresa;
- todo corrido con los modelos finales.

## 5. ¿Lo menciona el reporte `.tex_uacj`?

No. En `una-hetero/.tex_uacj/` las búsquedas de «Whisper», «voz», «cámara», «webcam», «micrófono» y «realtime» dan cero resultados en los `.tex`. «Tiempo real» aparece solo en el sentido de tiempo transcurrido de cómputo (`ApendiceA.tex:160`, `Capitulo4.tex:1266`). «Multimodal» aparece en el título (`tesis_uacj.tex:66`), en `Difusion.tex:4`, en `Resumen.tex:32` y en `Abstract.tex:31`, pero se refiere a texto más imagen, no a voz ni cámara. La percepción descrita es solo ResNet18 sobre imágenes (`Capitulo3.tex:24-29`).

Nota aparte, fuera de la tarea: `Capitulo3.tex:22` todavía dice «26 memorias asociativas (tres por módulo, más dos del TME)» en el worktree una-hetero.
