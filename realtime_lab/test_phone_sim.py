"""¿Rutea una imagen ETH-80 mostrada desde un celular a la webcam?
Simulación: degradaciones típicas de pantalla-a-cámara sobre imágenes
de test reales, pasadas por el MISMO route_frame del lab."""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from router import Router, CLASSES  # noqa: E402


def make_frame(img, scale=1.0, bright=1.0, blur=0, glare=False, rot=0.0,
               bg=60):
    """Frame 480x640 con la imagen ocupando `scale` del recorte central
    (como una pantalla de celular que no llena el encuadre)."""
    frame = np.full((480, 640, 3), bg, dtype=np.uint8)
    s = int(480 * scale)
    im = cv2.resize(img, (s, s))
    if rot:
        m = cv2.getRotationMatrix2D((s / 2, s / 2), rot, 1.0)
        im = cv2.warpAffine(im, m, (s, s), borderValue=(bg,) * 3)
    im = np.clip(im.astype(np.float32) * bright, 0, 255).astype(np.uint8)
    if blur:
        im = cv2.GaussianBlur(im, (blur * 2 + 1,) * 2, 0)
    if glare:
        gl = np.zeros_like(im, dtype=np.float32)
        cv2.ellipse(gl, (int(s * 0.3), int(s * 0.25)),
                    (s // 4, s // 10), -30, 0, 360, (90, 90, 90), -1)
        im = np.clip(im.astype(np.float32) +
                     cv2.GaussianBlur(gl, (61, 61), 0), 0, 255
                     ).astype(np.uint8)
    y0 = (480 - s) // 2
    x0 = (640 - s) // 2
    frame[y0:y0 + s, x0:x0 + s] = im
    return frame


CONDS = {
    "limpia 100%":      dict(),
    "pantalla 70%":     dict(scale=0.7),
    "pantalla 50%":     dict(scale=0.5),
    "brillo alto":      dict(scale=0.7, bright=1.35),
    "brillo bajo":      dict(scale=0.7, bright=0.65),
    "desenfoque":       dict(scale=0.7, blur=2),
    "reflejo":          dict(scale=0.7, glare=True),
    "rotada 6 grados":  dict(scale=0.7, rot=6),
    "todo junto":       dict(scale=0.6, bright=1.2, blur=1, glare=True,
                             rot=4),
}

r = Router(entry_agent="apple", log=lambda *a: None)
splits = json.loads(
    (Path(__file__).parent.parent / "data/eth80/splits.json").read_text())

N_IMGS = 3
print(f"{'condicion':<16}", "  ".join(f"{c[:5]:<5}" for c in CLASSES),
      " aciertos")
for cond, kw in CONDS.items():
    row, hits = [], 0
    for cls in CLASSES:
        ok = 0
        for p in splits[cls]["test"][:N_IMGS]:
            img = cv2.imread(p)
            res = r.route_frame(make_frame(img, **kw))
            ok += int(res["winner"] == cls)
        hits += ok
        row.append(f"{ok}/{N_IMGS}")
    print(f"{cond:<16}", "  ".join(f"{x:<5}" for x in row),
          f" {hits}/{N_IMGS * len(CLASSES)}")
