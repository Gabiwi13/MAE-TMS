# realtime_lab — MAE con sentidos en tiempo real

Experimento **aislado** del experimento base (que queda intacto, con sus
modelos en solo-lectura): la memoria transactiva recibiendo entrada
sensorial **continua** — nada de grabar-enviar-esperar.

**Decisiones de diseño** (16 jul 2026):
- Plataforma: **ventana nativa Python** (OpenCV + sounddevice).
- Voz: **escucha continua** — subtítulos vivos mientras hablas, ruteo
  automático al detectar pausa.
- Cámara: **etiqueta viva** sobre el video (~4 análisis/s) con rechazo
  honesto cuando ningún especialista reconoce.

## Por qué es viable en tiempo real

| Operación | Costo medido/estimado |
|---|---|
| Whisper `small` GPU (RTX 2050, frase corta) | **0.6 s** (medido) |
| Scoring de texto `recognize` (8 agentes) | milisegundos (proyección) |
| ResNet18 encode 128×128 (torch CPU) | ~30–60 ms |
| Ruteo visual `mem_dir_R.route` | milisegundos |

Lo único lento del experimento base es la **reconstrucción** (recall
estocástico, 127 iter → ~1 min); el ruteo en vivo **no la necesita**.
Presupuesto: pausa→ruteo **< 1 s**; frame→etiqueta **< 250 ms**.

## Arquitectura

```
main.py            ventana OpenCV (~30 fps): video + overlays + panel
 ├─ audio_worker   hilo · sounddevice InputStream 16 kHz mono, bloques 30 ms
 │                 → VAD Silero (integrado en faster-whisper, sin dep extra)
 │                 → subtítulo parcial ~1/s mientras hay habla
 │                 → fin de habla (~600 ms de silencio) → transcripción
 │                   final (task=translate, es/en → en) → cola de frases
 ├─ vision_worker  hilo · cv2.VideoCapture → cada ~250 ms: encode_pil →
 │                 quantize_latent_global → mem_dir_R.predict_tolerant +
 │                 route → (clase, scores) con suavizado (mayoría de 5)
 ├─ router.py      puente solo-lectura al experimento: carga agentes/TME,
 │                 scoring de texto, directorio visual, M_dir de sesión
 │                 del lab (en memoria, nunca toca models/)
 └─ overlay.py     dibujo: subtítulos, barras de score por agente
                   (DOMAIN_COLOR), etiqueta viva o banner RECHAZO
```

Tres hilos (audio, visión, UI) con colas thread-safe; modelos cargados
una sola vez al inicio.

## Qué se reusa (ya validado en la app, ver `salvaged_voice_camera.py`)

- `load_whisper`: GPU vía **preload ctypes** de los DLLs nvidia-pip
  (`os.add_dll_directory` no basta) + validación con inferencia de
  silencio + fallback CPU int8.
- `transcribe` con `task=translate` (hablar español o inglés → texto
  inglés, el idioma del vocabulario fastText).
- Detección de silencio / rescate de ganancia baja (`wav_stats`,
  `_amplify_wav`) — adaptar de WAV a chunks del stream.
- La dramaturgia del show En Vivo (barras que compiten, ganador 👑,
  rechazo honesto) como lenguaje visual del overlay.
- `reference/app_tme_con_voz_y_envivo.py`: respaldo completo de la app
  con todo integrado, por si hay que consultar contexto.

## Hitos

1. **M1 — Esqueleto**: ventana OpenCV con cámara en vivo + contador FPS.
2. **M2 — Voz**: escucha continua (subtítulo vivo) + ruteo al pausar,
   primero a consola, luego overlay con barras de score.
3. **M3 — Visión**: etiqueta viva con suavizado temporal + rechazo.
4. **M4 — Pulido**: panel con historial de ruteos y M_dir de sesión;
   teclas (`q` salir, `m` silenciar mic, `espacio` congelar frame y
   correr evocación completa como extra opcional).
5. **M5 — Medición**: latencias reales (pausa→ruteo, frame→etiqueta),
   tasa de rechazo con webcam vs imágenes ETH-80 mostradas a cámara —
   mini-informe.

## Riesgos conocidos

- **Micrófono en Windows**: el permiso de "apps de escritorio" en
  Configuración → Privacidad → Micrófono aplica también a sounddevice
  (WASAPI). El lab debe detectar RMS≈0 al arrancar y avisar con
  instrucciones (lección ya aprendida en la app).
- **Webcam ≠ ETH-80**: se espera RECHAZO frecuente con objetos reales;
  mostrar imágenes del dataset a la cámara es el caso de demostración.
  El rechazo ES un resultado (especificidad del directorio visual).
- **torch CPU** para ResNet18: suficiente a 128×128; si no, bajar la
  frecuencia de análisis (el video sigue fluido — solo se analiza cada
  N frames).

## Dependencias nuevas

`sounddevice`, `opencv-python` (VAD: Silero, ya incluido en
faster-whisper). Ver `requirements.txt` de esta carpeta.

## Uso (M1+M2+M3 construidos)

```bash
cd realtime_lab
python main.py                # ventana: cámara + escucha continua
python main.py --entry cow    # agente de entrada del hemisferio visual
python main.py --selftest 8   # verificación sin ventana (frame + reporte)
python main.py --wavtest x.wav  # inyecta un WAV por el camino del mic
```
Teclas: `q` salir · `m` silenciar micrófono.

## Resultados verificados (16 jul 2026)

| Prueba | Resultado |
|---|---|
| WAV inyectado → VAD → Whisper → ruteo | "Farm animal that gives milk" → **cow** · stt 336 ms + ruteo 302 ms ≈ **0.6 s** |
| Evocación (recall MAE → decoder), asíncrona | imagen del recuerdo en **~2 s** tras el ruteo (token `farm`, peso 9142); aparece junto a la referencia ETH-80 sin congelar video ni voz |
| Render con webcam | 26 fps; análisis visual 54 ms/frame |
| Micrófono nativo (WASAPI) | **SÍ entrega señal** (Realtek array, RMS 0.0013) — el silencio que veíamos era del navegador |
| Frames ETH-80 reales por route_frame | car→car ✓; cow/dog→rechazo — consistente con el 47.1% de ruteo visual conocido de 8 clases (límite del experimento, no del lab) |

**Pendiente del entorno**: Windows tenía la CÁMARA bloqueada para apps
de escritorio (el frame llega como placeholder gris con candado) →
Configuración → Privacidad y seguridad → Cámara → activar acceso
general y para apps de escritorio. El rechazo ante ese frame gris fue,
de hecho, comportamiento correcto del directorio.

## Prueba física con la cámara (17 jul)

- El celular NO funcionó (calidad de cámara + condiciones de pantalla;
  la simulación `test_phone_sim.py` ya lo anticipaba: el encuadre y el
  brillo colapsan el ruteo; `test_phone_rescue.py` mide los rescates).
- Nuevo soporte: **`hoja_impresion_eth80.pdf`** (4 páginas carta,
  16 imágenes pre-validadas a ~8.5 cm, 300 dpi — imprimir a color en
  papel mate). El papel elimina brillo de pantalla y moiré; queda
  llenar el recuadro de análisis con el recorte impreso.
- `phone_test_images/` (160 imágenes 512² pre-validadas + zip) sigue
  disponible por si se reintenta con otra pantalla.
- Overlay de evocación: se muestra **solo** la reconstrucción de
  memoria (`recall_from_left(token) → decoder`), sin la foto ETH-80 de
  referencia al lado — mostrarla hacía parecer que la imagen venía del
  encoder y no de la memoria.

## UI v2 de visión (tras la prueba física — voz ✓, visión ✗)

Diagnóstico del fallo visual: el recuadro de análisis era **toda la
altura del video** (480 px) — para llenarlo con una impresión de
8.5 cm había que acercarla más allá de la distancia de enfoque de la
webcam. Cambios:

- **Recuadro ajustable** (default 55% del lado menor; teclas `+`/`-`)
  → la impresión lo llena a ~20-30 cm, donde la webcam sí enfoca.
- **Guía inconfundible**: lo de fuera del recuadro se oscurece,
  esquinas gruesas estilo visor, texto "llena este recuadro".
- **«Lo que ve el ojo»** (abajo-izquierda): el 128×128 exacto que
  recibe el encoder, en vivo — borroso/reflejo/desencuadre se ven al
  instante y responden "¿es la cámara o la imagen?" con evidencia.
- **Feedback en rechazo**: muestra el candidato más cercano y su score
  en gris — siempre se percibe qué está considerando.

Verificado headless: frame sintético con cow llenando el recuadro 55%
→ rutea (98 ms); frame vacío → RECHAZO con candidato más cercano.

## Color: «reintentar con lentes» (18 jul) + UI en inglés

Diagnóstico de la prueba física #2 (solo cow fiable, apple/dog una
vez): la cadena impresora+cámara grisácea desplaza el latente; las
clases sobreviven según su margen (cow = objeto más grande = menos
fondo distorsionado visible).

- **Política de color** en `route_frame`: intento 1 crudo; si el
  directorio rechaza, intento 2 con normalización de momentos RGB a
  los de ETH-80 (`_color_fix`, sin umbral). Un detector por distancia
  de momentos NO funciona: medido, las distribuciones limpia/grisácea
  se traslapan (p50 24.2 vs 27.1). El reintento no puede dañar
  entradas limpias porque solo corre tras un rechazo.
- **Validación** (`test_colorfix.py`): limpia 22/24 (fix solo 1/24);
  cámara grisácea fuerte 15/24 (era ~0); media 18/24. El overlay
  marca "[color-fixed]" bajo el ojo cuando el rescate actuó.
- **Toda la UI en inglés** (overlay, panel, consola); los valores
  internos de modo son "early"/"mature".

## Sistema transactivo completo + panel lateral (17 jul)

La ventana ahora es cámara + **panel de sistema** (1060 px de ancho):

- **Voz con dos modos** (tecla `t`):
  - `temprana` — broadcast TME: los 8 agentes puntúan con M_dom y el
    grupo asigna; cada frase **se registra** en el M_dir de sesión
    (el directorio aprende en vivo — contadores al pie del panel).
  - `madura` — protocolo stage8: el **agente de entrada** consulta su
    M_dir entrenado (`route_multi`, B1) y **redirige** al especialista
    o rechaza (`directory_no_support`). El TME está apagado.
- **Entrada → redirección visible** para voz y visión: chips de color
  "APPLE → COW · redirige" / "se queda (es el experto)" / "RECHAZO".
- Tecla `e` cicla el agente de entrada (afecta voz madura y visión).
- Verificado: "farm animal…" — temprana TME→cow + registro [cow:3];
  madura entrada=apple → cow (routed=True, 56 ms); entrada=cow → cow
  (routed=False). Visión: entrada=apple → cow con imagen al 55%.
