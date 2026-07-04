"""
Exportación a video (MP4) de las animaciones de ruteo de la app.

Renderiza server-side (PIL → imageio/ffmpeg) las mismas fases que las
animaciones HTML de app_tme, consumiendo EXCLUSIVAMENTE los datos ya
decididos por la MAE (scores, ganador, redirección, imágenes evocadas):
el video visualiza, nunca re-decide.

Tres modos, uno por animación de la app:
  render_early_video   fase temprana (broadcast TME → scores → ganador →
                       registro en M_dir → recall)
  render_mature_video  fase madura (entrada → consulta M_dir B1 →
                       redirección punto a punto → recall)
  render_image_video   hemisferio visual (imagen → latente → M_dir_R B1 →
                       redirige/rechaza → etiquetas + reconstrucción)
"""
import io
import os
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 960, 608   # divisibles por 16 (macro-block de h264)
FPS = 12
BG = (16, 19, 50)
PANEL = (24, 28, 68)
BORDER = (48, 54, 112)
TEXT = (232, 234, 246)
MUTED = (141, 147, 200)
GOLD = (255, 213, 79)
BLUE = (125, 164, 255)
VIOLET = (91, 61, 245)
GREEN = (14, 124, 102)
RED = (255, 107, 107)


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()


def _ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def _np_to_pil(arr, size):
    img = Image.fromarray((np.clip(np.asarray(arr, dtype=float), 0, 1)
                           * 255).astype(np.uint8))
    return img.resize(size)


# ---------------------------------------------------------------------------
# Lienzo base y componentes
# ---------------------------------------------------------------------------

def _canvas(title, phase):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((24, 14), title, font=_font(17, True), fill=TEXT)
    up = phase.upper()
    f = _font(12)
    if d.textlength(up, font=f) > 430:      # no invadir el título
        f = _font(10)
    tw = d.textlength(up, font=f)
    d.text((W - 24 - tw, 18), up, font=f, fill=MUTED)
    return img, d


def _agent_layout(classes):
    """Posiciones de las cajas de agentes: 2 filas x 4 columnas."""
    pos = {}
    for i, cls in enumerate(classes):
        row, col = divmod(i, 4)
        pos[cls] = (40 + col * 230, 268 + row * 104)
    return pos


def _agent_box(d, xy, cls, color, bar_frac, score_txt, state="idle",
               tag=None, mdir_txt=None):
    """Caja de agente: swatch + nombre, barra de score, texto y estado."""
    x, y = xy
    w, h = 200, 88
    border = {"win": GOLD, "entry": BLUE, "reject": RED}.get(state, BORDER)
    width = 4 if state in ("win", "entry", "reject") else 2
    fill = PANEL if state != "lose" else (18, 20, 48)
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=fill,
                        outline=border, width=width)
    name_col = TEXT if state != "lose" else (108, 112, 150)
    d.rectangle([x + 12, y + 12, x + 24, y + 24], fill=color)
    d.text((x + 32, y + 9), cls, font=_font(15, True), fill=name_col)
    if tag:
        tw = d.textlength(tag, font=_font(9, True))
        d.text((x + w - 12 - tw, y + 12), tag, font=_font(9, True),
               fill=border)
    # barra de score
    bx0, bx1, by = x + 12, x + w - 12, y + 42
    d.rounded_rectangle([bx0, by, bx1, by + 10], radius=5, fill=(13, 15, 41))
    if bar_frac > 0:
        d.rounded_rectangle([bx0, by, bx0 + (bx1 - bx0) * min(bar_frac, 1.0),
                             by + 10], radius=5, fill=color)
    d.text((x + 12, y + 58), score_txt, font=_font(12), fill=MUTED)
    if mdir_txt:
        tw = d.textlength(mdir_txt, font=_font(11, True))
        d.text((x + w - 12 - tw, y + 58), mdir_txt, font=_font(11, True),
               fill=GOLD)


def _chips(d, items, y, color=VIOLET, upto=None):
    x = 40
    f = _font(13, True)
    for i, txt in enumerate(items):
        if upto is not None and i >= upto:
            break
        w = d.textlength(txt, font=f) + 22
        if x + w > W - 40:
            break
        d.rounded_rectangle([x, y, x + w, y + 26], radius=13, fill=color)
        d.text((x + 11, y + 5), txt, font=f, fill=(255, 255, 255))
        x += w + 10


def _dot(d, p0, p1, t, color=GOLD, r=6):
    t = _ease(t)
    x = p0[0] + (p1[0] - p0[0]) * t
    y = p0[1] + (p1[1] - p0[1]) * t
    d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def _result_strip(d, img_arr, lines, ref_arr=None, canvas=None):
    d.rounded_rectangle([32, 470, W - 32, 588], radius=12, fill=(20, 23, 58),
                        outline=BORDER, width=1)
    tx = 52
    if img_arr is not None and canvas is not None:
        canvas.paste(_np_to_pil(img_arr, (96, 96)), (52, 481))
        d.rectangle([52, 481, 148, 577], outline=GOLD, width=2)
        tx = 170
    for i, (txt, col, bold) in enumerate(lines):
        d.text((tx, 486 + i * 24), txt, font=_font(13, bold), fill=col)
    if ref_arr is not None and canvas is not None:
        canvas.paste(_np_to_pil(ref_arr, (96, 96)), (W - 150, 481))
        d.rectangle([W - 150, 481, W - 54, 577], outline=BORDER, width=2)
        d.text((W - 150, 460), "ETH-80 ref", font=_font(10), fill=MUTED)


def _encode(frames, fps=FPS):
    """Frames RGB (np.uint8) → bytes MP4 (h264, yuv420p)."""
    import imageio
    fd, path = tempfile.mkstemp(suffix=".mp4")
    os.close(fd)
    try:
        with imageio.get_writer(path, fps=fps, codec="libx264",
                                quality=8, pixelformat="yuv420p") as wr:
            for f in frames:
                wr.append_data(f)
        with open(path, "rb") as fh:
            return fh.read()
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Modo 1: fase temprana
# ---------------------------------------------------------------------------

def render_early_video(trace, classes, colors, ref_img=None) -> bytes:
    """Video de la fase temprana desde el trace REAL de la app."""
    colors = {c: _hex(colors[c]) for c in classes}
    query = trace["query"]
    tokens = list(trace["per_token"].keys())
    scores = {c: float(trace["avg_scores"][c]) for c in classes}
    winner = trace["winner"]
    n_tok = int(trace["n_tokens"])
    rec = trace.get("final_recalled_img")
    mx = max(max(scores.values()), 1e-9)
    pos = _agent_layout(classes)
    tme = (W // 2, 196)
    frames = []

    def base(phase, chips_upto=None, bar=0.0, state_of=None, mdir=False,
             dots=None, show_scores=True):
        img, d = _canvas("EAM-TMS · fase temprana (TME activo)", phase)
        d.text((40, 48), f'"{query}"', font=_font(15), fill=TEXT)
        _chips(d, tokens, 84, upto=chips_upto)
        # nodo TME
        d.ellipse([tme[0] - 34, tme[1] - 34, tme[0] + 34, tme[1] + 34],
                  fill=(29, 37, 102), outline=(107, 121, 232), width=3)
        d.text((tme[0] - 17, tme[1] - 10), "TME", font=_font(14, True),
               fill=TEXT)
        for c in classes:
            p = (pos[c][0] + 100, pos[c][1])
            d.line([tme, p], fill=(58, 63, 120), width=2)
        if dots is not None:
            for c in classes:
                _dot(d, tme, (pos[c][0] + 100, pos[c][1]), dots,
                     color=colors[c])
        for c in classes:
            st = state_of(c) if state_of else "idle"
            frac = (scores[c] / mx) * bar if show_scores else 0.0
            stxt = f"{scores[c] * bar:.1f}" if show_scores and bar > 0 else "—"
            _agent_box(d, pos[c], c, colors[c], frac, stxt, state=st,
                       tag="GANADOR" if st == "win" else None,
                       mdir_txt=f"M_dir +{n_tok}" if (mdir and st == "win")
                       else ("M_dir +reg" if mdir else None))
        return img, d

    for k in range(8):                                   # tokens
        img, _ = base("1 · descomposición en pistas",
                      chips_upto=int(len(tokens) * (k + 1) / 8 + 0.99),
                      show_scores=False)
        frames.append(np.asarray(img))
    for k in range(12):                                  # broadcast
        img, _ = base("2 · broadcast v_q a TODOS los agentes",
                      dots=(k + 1) / 12, show_scores=False)
        frames.append(np.asarray(img))
    for k in range(16):                                  # scores
        img, _ = base("3 · M_dom_L pesos → M_dom_H score (gate de containment)",
                      bar=_ease((k + 1) / 16))
        frames.append(np.asarray(img))
    st_win = lambda c: "win" if c == winner else "lose"
    for k in range(8):                                   # ganador
        img, _ = base("4 · argmax → ganador", bar=1.0, state_of=st_win)
        frames.append(np.asarray(img))
    for k in range(10):                                  # registro M_dir
        img, _ = base("5 · registro (v_q → ganador) en TME y TODOS los M_dir",
                      bar=1.0, state_of=st_win, mdir=True)
        frames.append(np.asarray(img))
    for k in range(22):                                  # resultado
        img, d = base("6 · recall en el ganador → decoder", bar=1.0,
                      state_of=st_win, mdir=True)
        lines = [(f"ganador: {winner.upper()}   ·   score "
                  f"{scores[winner]:.2f}", GOLD, True),
                 ("recall M_dom_H → latente 64D → decoder → imagen"
                  if rec is not None else
                  "el ganador no reconoció la pista (sin recall)",
                  MUTED, False),
                 ("la imagen es EVOCADA por la MAE, no la entrada",
                  MUTED, False)]
        _result_strip(d, rec, lines, ref_arr=ref_img, canvas=img)
        frames.append(np.asarray(img))
    return _encode(frames)


# ---------------------------------------------------------------------------
# Modo 2: fase madura
# ---------------------------------------------------------------------------

def render_mature_video(query, tokens, entry, dest, scores, classes,
                        colors, recalled_img=None) -> bytes:
    """Video de la fase madura (M_dir del agente de entrada, lectura B1)."""
    colors = {c: _hex(colors[c]) for c in classes}
    mx = max(max(scores.values()), 1e-9)
    pos = _agent_layout(classes)
    redirected = entry != dest
    frames = []

    def base(phase, bar=0.0, states=None, dot_t=None, badge=False):
        img, d = _canvas("EAM-TMS · fase madura (TME apagado)", phase)
        d.text((40, 48), f'"{query}"', font=_font(15), fill=TEXT)
        _chips(d, tokens, 84)
        # TME apagado
        d.ellipse([W // 2 - 30, 166, W // 2 + 30, 226], fill=(28, 30, 52),
                  outline=(70, 74, 110), width=2)
        d.text((W // 2 - 15, 186), "TME", font=_font(13, True),
               fill=(96, 100, 140))
        d.text((W // 2 - 32, 230), "apagado", font=_font(10), fill=MUTED)
        if badge:
            btxt = f"{entry} consulta SU M_dir  ·  lectura B1 (÷count+1)"
            bw = d.textlength(btxt, font=_font(12, True)) + 24
            d.rounded_rectangle([(W - bw) / 2, 128, (W + bw) / 2, 154],
                                radius=8, fill=(36, 31, 84),
                                outline=(107, 121, 232))
            d.text(((W - bw) / 2 + 12, 133), btxt, font=_font(12, True),
                   fill=(207, 212, 255))
        for c in classes:
            st = states(c) if states else ("entry" if c == entry else "idle")
            frac = (scores.get(c, 0.0) / mx) * bar
            stxt = f"{scores.get(c, 0.0) * bar:.3f}" if bar > 0 else "—"
            _agent_box(d, pos[c], c, colors[c], frac, stxt, state=st,
                       tag={"entry": "ENTRADA", "win": "DESTINO"}.get(st))
        if dot_t is not None:
            p0 = (pos[entry][0] + 100, pos[entry][1] + 44)
            p1 = (pos[dest][0] + 100, pos[dest][1] + 44)
            d.line([p0, p1], fill=GOLD, width=3)
            _dot(d, p0, p1, dot_t)
        return img, d

    for k in range(8):
        frames.append(np.asarray(base("1 · la consulta entra por "
                                      f"{entry} (arbitrario)")[0]))
    for k in range(10):
        frames.append(np.asarray(base("2 · consulta a su directorio "
                                      "transactivo", badge=True)[0]))
    for k in range(16):
        frames.append(np.asarray(base("3 · scores B1 por especialista "
                                      "(route_multi de la MAE)",
                                      bar=_ease((k + 1) / 16),
                                      badge=True)[0]))
    st_f = lambda c: ("win" if c == dest else
                      "entry" if c == entry else "lose")
    if redirected:
        for k in range(12):
            frames.append(np.asarray(base(f"4 · redirige {entry} → {dest} "
                                          "(punto a punto)", bar=1.0,
                                          states=st_f,
                                          dot_t=(k + 1) / 12)[0]))
    else:
        for k in range(8):
            frames.append(np.asarray(base("4 · entrada = especialista: se "
                                          "queda la consulta", bar=1.0,
                                          states=st_f)[0]))
    for k in range(22):
        img, d = base("5 · recall en el destino", bar=1.0, states=st_f,
                      dot_t=1.0 if redirected else None)
        lines = [((f"{entry}  →  {dest.upper()}" if redirected
                   else f"{dest.upper()} (entrada = especialista)"),
                  GOLD, True),
                 (f"score B1 {scores.get(dest, 0.0):.3f} · M_dir congelado, "
                  "sin aprendizaje", MUTED, False),
                 ("recall punto a punto → decoder"
                  if recalled_img is not None else
                  "el destino no reconoció la pista (sin recall)",
                  MUTED, False)]
        _result_strip(d, recalled_img, lines, canvas=img)
        frames.append(np.asarray(img))
    return _encode(frames)


# ---------------------------------------------------------------------------
# Modo 3: hemisferio visual (imagen → etiquetas)
# ---------------------------------------------------------------------------

def render_image_video(input_img, z_q, scores, entry, winner, labels,
                       classes, colors, recon_img=None) -> bytes:
    """Video del flujo imagen → etiquetas (ruteo por mem_dir_R, B1 + ξ)."""
    colors = {c: _hex(colors[c]) for c in classes}
    mx = max(max(scores.values()), 1e-9)
    pos = _agent_layout(classes)
    z = np.asarray(z_q).ravel()
    rejected = winner is None
    frames = []

    def base(phase, latent_frac=0.0, bar=0.0, states=None, dot_t=None,
             chips_n=0):
        img, d = _canvas("EAM-TMS · hemisferio visual (imagen → etiquetas)",
                         phase)
        img.paste(_np_to_pil(input_img, (86, 86)), (40, 52))
        d.rectangle([40, 52, 126, 138], outline=(107, 121, 232), width=2)
        d.text((40, 142), "pista (imagen)", font=_font(10), fill=MUTED)
        d.text((150, 86), "→", font=_font(22, True), fill=MUTED)
        d.rounded_rectangle([190, 62, 320, 126], radius=12,
                            fill=(29, 37, 102), outline=(107, 121, 232),
                            width=2)
        d.text((212, 76), "ResNet18", font=_font(14, True), fill=TEXT)
        d.text((222, 98), "(el ojo)", font=_font(11), fill=MUTED)
        d.text((334, 86), "→", font=_font(22, True), fill=MUTED)
        # grid latente 8x8 (z_q real)
        gx, gy, cell = 380, 58, 11
        n_on = int(64 * latent_frac)
        for i in range(64):
            cx, cy = gx + (i % 8) * cell, gy + (i // 8) * cell
            if i < n_on:
                t = float(z[i]) / 31.0
                col = (int(26 + 98 * t), int(29 + 135 * t), int(61 + 194 * t))
            else:
                col = (26, 29, 61)
            d.rectangle([cx, cy, cx + cell - 1, cy + cell - 1], fill=col)
        d.text((378, 148), "z_q ∈ [0,31]⁶⁴", font=_font(10), fill=MUTED)
        # etiquetas evocadas
        if chips_n:
            d.text((520, 60), "etiquetas evocadas (recall inverso, top-3):",
                   font=_font(11), fill=MUTED)
            _x = 520
            for lb in labels[:chips_n]:
                wch = d.textlength(lb, font=_font(13, True)) + 22
                d.rounded_rectangle([_x, 80, _x + wch, 106], radius=13,
                                    fill=GREEN)
                d.text((_x + 11, 85), lb, font=_font(13, True),
                       fill=(255, 255, 255))
                _x += wch + 8
        d.text((40, 236), f"entrada: {entry} · consulta SU directorio visual "
                          "mem_dir_R (B1, ξ=2 — funciones parciales)",
               font=_font(12), fill=(207, 212, 255))
        for c in classes:
            st = states(c) if states else ("entry" if c == entry else "idle")
            frac = (scores.get(c, 0.0) / mx) * bar
            stxt = f"{scores.get(c, 0.0) * bar:.3f}" if bar > 0 else "—"
            _agent_box(d, pos[c], c, colors[c], frac, stxt, state=st,
                       tag={"entry": "ENTRADA", "win": "DESTINO",
                            "reject": ""}.get(st))
        if dot_t is not None and not rejected:
            p0 = (pos[entry][0] + 100, pos[entry][1] + 44)
            p1 = (pos[winner][0] + 100, pos[winner][1] + 44)
            d.line([p0, p1], fill=GOLD, width=3)
            _dot(d, p0, p1, dot_t)
        return img, d

    for k in range(12):
        frames.append(np.asarray(base("1 · percepción → latente cuantizado",
                                      latent_frac=(k + 1) / 12)[0]))
    for k in range(8):
        frames.append(np.asarray(base(f"2 · z_q llega al agente de entrada "
                                      f"({entry})", latent_frac=1.0)[0]))
    for k in range(16):
        frames.append(np.asarray(base("3 · scores B1 del directorio visual",
                                      latent_frac=1.0,
                                      bar=_ease((k + 1) / 16))[0]))
    if rejected:
        st_f = lambda c: "reject"
        for k in range(24):
            img, d = base("4 · RECHAZADA — nadie la conoce", latent_frac=1.0,
                          bar=1.0, states=st_f)
            _result_strip(d, None, [
                ("RECHAZADA — mem_dir_R sin soporte", RED, True),
                ("ningún especialista conoce esta percepción", MUTED, False),
                ("el grupo no inventa referente", MUTED, False)], canvas=img)
            frames.append(np.asarray(img))
    else:
        st_f = lambda c: ("win" if c == winner else
                          "entry" if c == entry else "lose")
        for k in range(12):
            frames.append(np.asarray(base(
                f"4 · redirige {entry} → {winner} (punto a punto)",
                latent_frac=1.0, bar=1.0, states=st_f,
                dot_t=(k + 1) / 12)[0]))
        for k in range(24):
            img, d = base("5 · evoke_labels + reconstrucción",
                          latent_frac=1.0, bar=1.0, states=st_f, dot_t=1.0,
                          chips_n=len(labels[:3]))
            _result_strip(d, recon_img, [
                (f"{entry}  →  {winner.upper()}", GOLD, True),
                (f"B1 {scores.get(winner, 0.0):.3f} · etiquetas: "
                 + "  ".join(labels[:3]), TEXT, False),
                ("la reconstrucción la evoca la MAE (mem_dom_R.recall), "
                 "no es la entrada", MUTED, False)], canvas=img)
            frames.append(np.asarray(img))
    return _encode(frames)
