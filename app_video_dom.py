"""
Grabación EXACTA de las animaciones HTML de la app a video MP4.

En lugar de una réplica dibujada, se carga el MISMO HTML que la app muestra
en Streamlit (build_flow_animation / build_mature_animation /
build_image_to_labels_animation) en un Edge headless y se captura el
screencast del compositor (Chrome DevTools Protocol): mismo DOM, mismo CSS,
mismos emojis y easing — pixel por pixel lo que se ve en la app.

La captura corre en un SUBPROCESO (este mismo archivo como script) para no
tocar el event loop de Streamlit. Los frames JPEG con timestamp se
re-muestrean a fps constante y se codifican a MP4 h264 (imageio/ffmpeg).

API para la app:
    record_animation_html(html, height, fps=15, max_seconds=60) -> bytes
"""
import base64
import io
import json
import os
import subprocess
import sys
import tempfile
import time

FPS_DEFAULT = 15


def record_animation_html(html: str, height: int, fps: int = FPS_DEFAULT,
                          max_seconds: int = 60) -> bytes:
    """Graba el HTML de una animación en un navegador headless y devuelve
    los bytes del MP4. Lanza RuntimeError si la captura falla (la app cae
    entonces al renderer PIL)."""
    fd_h, html_path = tempfile.mkstemp(suffix=".html")
    fd_m, mp4_path = tempfile.mkstemp(suffix=".mp4")
    os.close(fd_h); os.close(fd_m)
    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        r = subprocess.run(
            [sys.executable, os.path.abspath(__file__), html_path, mp4_path,
             str(height), str(fps), str(max_seconds)],
            capture_output=True, text=True, timeout=max_seconds + 120)
        if r.returncode != 0:
            raise RuntimeError(
                f"captura DOM falló (rc={r.returncode}): "
                f"{(r.stderr or r.stdout)[-400:]}")
        with open(mp4_path, "rb") as f:
            data = f.read()
        if len(data) < 1000:
            raise RuntimeError("captura DOM produjo un MP4 vacío")
        return data
    finally:
        for p in (html_path, mp4_path):
            try:
                os.unlink(p)
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Subproceso de captura
# ---------------------------------------------------------------------------

def _capture(html_path: str, mp4_path: str, height: int, fps: int,
             max_seconds: int) -> None:
    import numpy as np
    from PIL import Image
    import imageio
    from playwright.sync_api import sync_playwright

    html = open(html_path, encoding="utf-8").read()
    frames = []          # [(timestamp, jpeg_bytes)]

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1020, "height": height})
        page.set_content(html, wait_until="load")

        cdp = page.context.new_cdp_session(page)

        def on_frame(params):
            frames.append((params["metadata"]["timestamp"],
                           base64.b64decode(params["data"])))
            try:
                cdp.send("Page.screencastFrameAck",
                         {"sessionId": params["sessionId"]})
            except Exception:
                pass

        cdp.on("Page.screencastFrame", on_frame)
        cdp.send("Page.startScreencast",
                 {"format": "jpeg", "quality": 88, "everyNthFrame": 1})

        # La animación autoarranca ~0.3 s tras load y termina poniendo
        # 'done' en #plabel (ambos templates, incluido el caso de rechazo).
        t0 = time.time()
        while time.time() - t0 < max_seconds:
            page.wait_for_timeout(300)
            try:
                done = page.evaluate(
                    "() => { const l = document.getElementById('plabel');"
                    " return !!l && l.textContent.includes('done'); }")
            except Exception:
                done = False
            if done and time.time() - t0 > 3:
                page.wait_for_timeout(700)   # sostener el frame final
                break

        cdp.send("Page.stopScreencast")
        rect = page.evaluate(
            "() => { const a = document.getElementById('anim');"
            " const r = a.getBoundingClientRect();"
            " return {x: r.x, y: r.y, w: r.width, h: r.height}; }")
        browser.close()

    if len(frames) < 5:
        raise RuntimeError(f"solo {len(frames)} frames capturados")

    # Recorte al card de la animación, dimensiones pares para h264.
    x, y = int(max(rect["x"], 0)), int(max(rect["y"], 0))
    w, h = int(rect["w"]) // 2 * 2, int(rect["h"]) // 2 * 2

    # Re-muestreo a fps constante: para cada tick, el último frame emitido.
    frames.sort(key=lambda f: f[0])
    t_start, t_end = frames[0][0], frames[-1][0]
    n_ticks = max(int((t_end - t_start) * fps), 1) + 1
    decoded = {}

    def frame_at(ts):
        idx = 0
        for i, (t, _) in enumerate(frames):
            if t <= ts:
                idx = i
            else:
                break
        if idx not in decoded:
            img = Image.open(io.BytesIO(frames[idx][1])).convert("RGB")
            decoded[idx] = np.asarray(img.crop((x, y, x + w, y + h)))
        return decoded[idx]

    with imageio.get_writer(mp4_path, fps=fps, codec="libx264",
                            quality=8, pixelformat="yuv420p") as wr:
        for k in range(n_ticks):
            wr.append_data(frame_at(t_start + k / fps))


if __name__ == "__main__":
    _capture(sys.argv[1], sys.argv[2], int(sys.argv[3]),
             int(sys.argv[4]), int(sys.argv[5]))
