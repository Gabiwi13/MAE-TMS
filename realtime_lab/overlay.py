"""Dibujo del overlay sobre el frame de la webcam (cv2 — texto ASCII).
Paleta: pasos validados para superficie oscura (las bandas del overlay
son negras translúcidas)."""
import cv2
import numpy as np

# DOMAIN_COLOR_DARK del experimento, hex → BGR
_HEX = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60",
        "cow": "#8e44ad", "cup": "#c9760a", "dog": "#16a085",
        "pear": "#7d8f22", "tomato": "#c0392b"}


def _bgr(cls):
    h = _HEX[cls].lstrip("#")
    return (int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16))


_WHITE, _GRAY, _RED = (245, 245, 245), (170, 170, 170), (60, 60, 220)
_FONT = cv2.FONT_HERSHEY_SIMPLEX


def _ascii(s):
    return s.encode("ascii", "replace").decode()


def _band(frame, y0, y1, alpha=0.55, x0=0, x1=None):
    """Banda negra translúcida (fondo de texto)."""
    sub = frame[y0:y1, x0:x1]
    frame[y0:y1, x0:x1] = (sub * (1 - alpha)).astype(np.uint8)


def draw_header(frame, fps, entry, muted, mic_error=None):
    _band(frame, 0, 28)
    cv2.putText(frame, _ascii(
        f"MAE realtime | vision entry: {entry} | "
        f"mic: {'MUTE' if muted else 'on'} | {fps:.0f} fps | "
        f"q quit  m mute  t voice-mode  e entry  +/- box"),
        (8, 19), _FONT, 0.45, _WHITE, 1, cv2.LINE_AA)
    if mic_error:
        _band(frame, 28, 50)
        cv2.putText(frame, _ascii(mic_error[:110]), (8, 44),
                    _FONT, 0.42, _RED, 1, cv2.LINE_AA)


def draw_vision_guide(frame, crop_frac, active_color):
    """Zona de análisis inconfundible: lo de afuera se oscurece, las
    esquinas son gruesas y un texto dice qué hacer ahí."""
    h, w = frame.shape[:2]
    s = max(32, int(min(h, w) * crop_frac))
    y0, x0 = (h - s) // 2, (w - s) // 2
    # oscurecer lo que NO se analiza
    mask = frame.copy()
    cv2.rectangle(mask, (x0, y0), (x0 + s, y0 + s), 0, -1)
    dim = (frame * 0.45).astype(np.uint8)
    outside = np.ones((h, w), dtype=bool)
    outside[y0:y0 + s, x0:x0 + s] = False
    frame[outside] = dim[outside]
    # esquinas gruesas estilo visor
    L = max(18, s // 8)
    for (cx, cy, dx, dy) in [(x0, y0, 1, 1), (x0 + s, y0, -1, 1),
                             (x0, y0 + s, 1, -1), (x0 + s, y0 + s, -1, -1)]:
        cv2.line(frame, (cx, cy), (cx + dx * L, cy), active_color, 3)
        cv2.line(frame, (cx, cy), (cx, cy + dy * L), active_color, 3)
    cv2.rectangle(frame, (x0, y0), (x0 + s - 1, y0 + s - 1),
                  active_color, 1)
    cv2.putText(frame, "fill this box with the image  (+/- size)",
                (x0, y0 - 8), _FONT, 0.45, active_color, 1, cv2.LINE_AA)
    return x0, y0, s


def draw_vision_label(frame, vis, crop_frac=1.0):
    """Etiqueta viva + guía de encuadre. Aunque rechace, muestra el
    candidato más cercano y su score — siempre se percibe algo."""
    color = _bgr(vis["winner"]) if (vis and vis.get("winner")) else _GRAY
    x0, y0, s = draw_vision_guide(frame, crop_frac, color)
    if vis is None:
        return
    if vis.get("winner"):
        cls = vis["winner"]
        txt = f"{cls.upper()}  {vis['scores'][cls]:.2f}"
    else:
        top = max(vis["scores"], key=vis["scores"].get)
        txt = (f"REJECTED  (closest: {top} "
               f"{vis['scores'][top]:.2f})")
    (tw, th), _ = cv2.getTextSize(txt, _FONT, 0.75, 2)
    x, y = 10, 62
    cv2.rectangle(frame, (x - 6, y - th - 8), (x + tw + 6, y + 8),
                  (20, 20, 20), -1)
    cv2.rectangle(frame, (x - 6, y - th - 8), (x + tw + 6, y + 8),
                  color, 2)
    cv2.putText(frame, txt, (x, y), _FONT, 0.75, color, 2, cv2.LINE_AA)


def draw_eye(frame, eye_bgr, color_fix=False):
    """Lo que el encoder REALMENTE recibió (128×128): borroso, con
    reflejo o mal encuadrado se ve aquí al instante."""
    if eye_bgr is None:
        return
    h = frame.shape[0]
    size = 96
    x, y1 = 10, h - 48
    y0 = y1 - size - 22
    _band(frame, y0 - 4, y1, alpha=0.65, x0=x - 4, x1=x + size + 8)
    frame[y0:y0 + size, x:x + size] = cv2.resize(eye_bgr, (size, size))
    cv2.rectangle(frame, (x, y0), (x + size - 1, y0 + size - 1),
                  _WHITE, 1)
    cv2.putText(frame, "what the eye sees" + (" [color-fixed]" if color_fix else ""), (x, y0 + size + 15),
                _FONT, 0.4, _GRAY, 1, cv2.LINE_AA)


def draw_subtitles(frame, partial, listening):
    """Subtítulo vivo abajo: parcial en gris mientras hablas."""
    h = frame.shape[0]
    if partial:
        _band(frame, h - 40, h)
        cv2.putText(frame, _ascii('"' + partial[-90:] + '"'),
                    (10, h - 14), _FONT, 0.6, _GRAY, 1, cv2.LINE_AA)
    elif listening:
        _band(frame, h - 40, h)
        cv2.putText(frame, "( listening... )", (10, h - 14),
                    _FONT, 0.6, _GRAY, 1, cv2.LINE_AA)


PANEL_W = 420
HEADER_H = 28


def compose_canvas(frame):
    """Ventana ancha: header + cámara a la izquierda + panel de sistema
    a la derecha (no todo tiene que vivir encima del video)."""
    h, w = frame.shape[:2]
    canvas = np.full((h + HEADER_H, w + PANEL_W, 3), (30, 28, 26),
                     dtype=np.uint8)
    canvas[HEADER_H:HEADER_H + h, :w] = frame
    return canvas


def _agent_chip(canvas, x, y, cls, dim=False):
    """Nombre del agente con su color; devuelve el ancho ocupado."""
    color = _bgr(cls) if not dim else (110, 110, 110)
    txt = cls.upper()
    (tw, th), _ = cv2.getTextSize(txt, _FONT, 0.62, 2)
    cv2.rectangle(canvas, (x - 4, y - th - 6), (x + tw + 4, y + 6),
                  (18, 18, 18), -1)
    cv2.rectangle(canvas, (x - 4, y - th - 6), (x + tw + 4, y + 6),
                  color, 2)
    cv2.putText(canvas, txt, (x, y), _FONT, 0.62, color, 2, cv2.LINE_AA)
    return tw + 14


def _redirect_line(canvas, x, y, entry, dest, rejected, label):
    """ENTRADA -> DESTINO con flecha; el corazón transactivo visible."""
    cv2.putText(canvas, label, (x, y - 24), _FONT, 0.4, _GRAY, 1,
                cv2.LINE_AA)
    w1 = _agent_chip(canvas, x, y, entry)
    ax = x + w1
    if rejected:
        cv2.putText(canvas, "-> REJECTED", (ax, y), _FONT, 0.6,
                    _GRAY, 2, cv2.LINE_AA)
        return
    color = _bgr(dest)
    cv2.arrowedLine(canvas, (ax + 2, y - 6), (ax + 44, y - 6), color, 2,
                    tipLength=0.35)
    w2 = _agent_chip(canvas, ax + 52, y, dest)
    note = ("redirects" if dest != entry else "stays (it is the expert)")
    cv2.putText(canvas, note, (ax + 52 + w2, y), _FONT, 0.4, _GRAY, 1,
                cv2.LINE_AA)


def draw_side_panel(canvas, cam_w, voice_mode, entry, route, evoked,
                    vision, counts, classes):
    """Panel de sistema: con quién interactúas y hacia dónde redirige,
    para voz y visión; barras del último ruteo; recuerdo evocado; M_dir
    de sesión aprendiendo."""
    x = cam_w + 14
    cv2.line(canvas, (cam_w + 4, HEADER_H), (cam_w + 4, canvas.shape[0]),
             (70, 70, 70), 1)

    # ---- VOZ ----
    y = HEADER_H + 34
    mode_txt = ("EARLY - the group (TME) decides and M_dir learns"
                if voice_mode == "early"
                else "MATURE - the entry agent's M_dir redirects")
    cv2.putText(canvas, f"VOICE [t] mode {voice_mode.upper()}", (x, y),
                _FONT, 0.55, _WHITE, 1, cv2.LINE_AA)
    cv2.putText(canvas, _ascii(mode_txt), (x, y + 18), _FONT, 0.38,
                _GRAY, 1, cv2.LINE_AA)
    y += 64
    if route is not None:
        if voice_mode == "mature" or route.get("mode") == "mature":
            _redirect_line(canvas, x, y, route.get("entry") or entry,
                           route.get("winner"), route.get("rejected"),
                           "who received -> who knows")
        else:
            lbl = "the group assigns to"
            cv2.putText(canvas, lbl, (x, y - 24), _FONT, 0.4, _GRAY, 1,
                        cv2.LINE_AA)
            if route.get("rejected"):
                cv2.putText(canvas, "REJECTED (" +
                            _ascii(route.get("reason", "")) + ")",
                            (x, y), _FONT, 0.6, _GRAY, 2, cv2.LINE_AA)
            else:
                _agent_chip(canvas, x, y, route["winner"])
        y += 20
        cv2.putText(canvas, _ascii('"' + route["query"][:44] + '"'),
                    (x, y), _FONT, 0.42, _WHITE, 1, cv2.LINE_AA)
        y += 20
        if route.get("scores"):
            mx = max(route["scores"].values()) or 1e-9
            for cls in classes:
                s = route["scores"][cls]
                win = cls == route.get("winner")
                color = _bgr(cls) if s > 0 else (80, 80, 80)
                cv2.putText(canvas, f"{cls:<7}", (x, y), _FONT, 0.42,
                            _WHITE if win else _GRAY, 1, cv2.LINE_AA)
                # 156 px de barra maxima: la etiqueta de score del ganador
                # queda a >=15 px de la columna del recuerdo evocado (xe).
                bar = int(156 * s / mx)
                cv2.rectangle(canvas, (x + 64, y - 9),
                              (x + 64 + max(bar, 1), y - 1), color, -1)
                if win:
                    cv2.putText(canvas, f"{s:.1f}",
                                (x + 68 + bar, y), _FONT, 0.38, color,
                                1, cv2.LINE_AA)
                y += 20
        y += 4
        cv2.putText(canvas,
                    f"stt {route.get('stt_ms', 0):.0f} ms + "
                    f"ruteo {route.get('ms', 0):.0f} ms", (x, y),
                    _FONT, 0.38, _GRAY, 1, cv2.LINE_AA)
        y += 16
    else:
        cv2.putText(canvas, "( speak: routes on pause )", (x, y),
                    _FONT, 0.45, _GRAY, 1, cv2.LINE_AA)
        y += 24

    # ---- recuerdo evocado (columna derecha del panel, no estorba) ----
    # Pista faltante (Morales & Pineda 2025): arriba el PROTOTIPO
    # (argmax del plano proyectado — la "plastilina" leida sin muestreo),
    # abajo el OBJETO DEFINIDO (sample-and-search, el recall oficial).
    # d = distancia retro-proyectada a la pista (menor = mejor).
    if evoked is not None:
        size = 88
        xe = x + 268
        # ye deja >=8 px entre la ultima caption (y2+size+28) y el titulo
        # de VISION (h-120) con camara 480p; a HEADER_H+104 el hueco era ~3 px.
        ye = HEADER_H + 96
        cls = evoked["cls"]
        if evoked.get("status") == "pending":
            cv2.putText(canvas, f"{cls}:", (xe, ye + 40), _FONT, 0.45,
                        _GRAY, 1, cv2.LINE_AA)
            cv2.putText(canvas, "recalling...", (xe, ye + 60), _FONT,
                        0.45, _GRAY, 1, cv2.LINE_AA)
        elif evoked.get("status") == "error":
            cv2.putText(canvas, f"{cls}:", (xe, ye + 40), _FONT, 0.45,
                        _GRAY, 1, cv2.LINE_AA)
            cv2.putText(canvas, "recall failed", (xe, ye + 60), _FONT,
                        0.45, _GRAY, 1, cv2.LINE_AA)
        elif evoked.get("img") is not None:
            if evoked.get("proto") is not None:
                cv2.putText(canvas, "prototype (raw plane)",
                            (xe, ye - 6), _FONT, 0.36, _GRAY, 1,
                            cv2.LINE_AA)
                canvas[ye:ye + size, xe:xe + size] = cv2.resize(
                    evoked["proto"], (size, size))
                cv2.rectangle(canvas, (xe, ye), (xe + size - 1,
                              ye + size - 1), _GRAY, 1)
                d_p = evoked.get("d_proto")
                if d_p is not None:
                    cv2.putText(canvas, f"d={d_p:.1f}",
                                (xe, ye + size + 14), _FONT, 0.36,
                                _GRAY, 1, cv2.LINE_AA)
            y2 = ye + size + 34
            cv2.putText(canvas, f"memory of {cls} (defined)",
                        (xe, y2 - 6), _FONT, 0.36, _bgr(cls), 1,
                        cv2.LINE_AA)
            canvas[y2:y2 + size, xe:xe + size] = cv2.resize(
                evoked["img"], (size, size))
            cv2.rectangle(canvas, (xe, y2), (xe + size - 1,
                          y2 + size - 1), _bgr(cls), 1)
            d_s = evoked.get("d_ss")
            cv2.putText(canvas,
                        f"'{_ascii(str(evoked.get('token')))}'"
                        + (f"  d={d_s:.1f}" if d_s is not None else ""),
                        (xe, y2 + size + 14), _FONT, 0.36, _GRAY, 1,
                        cv2.LINE_AA)
            cv2.putText(canvas, f"weight {evoked.get('weight', 0):.0f}",
                        (xe, y2 + size + 28), _FONT, 0.36, _GRAY, 1,
                        cv2.LINE_AA)
        else:
            cv2.putText(canvas, f"{cls}: cue", (xe, ye + 40), _FONT,
                        0.42, _GRAY, 1, cv2.LINE_AA)
            cv2.putText(canvas, "not recognized", (xe, ye + 60), _FONT,
                        0.42, _GRAY, 1, cv2.LINE_AA)

    # ---- VISION ----
    h = canvas.shape[0]
    yv = h - 120
    cv2.putText(canvas, f"VISION [e] entry: {entry}   [+/-] box",
                (x, yv), _FONT, 0.55, _WHITE, 1, cv2.LINE_AA)
    if vision is not None:
        _redirect_line(canvas, x, yv + 42, vision.get("entry") or entry,
                       vision.get("winner"), vision.get("winner") is None,
                       "who looks -> who recognizes")

    # ---- M_dir de sesion ----
    ys = h - 26
    row = "session M_dir: " + "  ".join(
        f"{c[:4]} {int(n)}" for c, n in zip(classes, counts))
    cv2.putText(canvas, _ascii(row), (x, ys), _FONT, 0.38, _GRAY, 1,
                cv2.LINE_AA)
    cv2.putText(canvas, "(learns from each phrase in early mode)",
                (x, ys + 16), _FONT, 0.34, (100, 100, 100), 1,
                cv2.LINE_AA)
