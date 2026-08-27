"""Valida el color-fix adaptativo integrado en route_frame: condiciones
de pantalla/brillo de test_phone_sim + cámara grisácea (como la webcam
del usuario). Reporta aciertos y cuántas veces se activó el fix."""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from router import Router, CLASSES  # noqa: E402
from test_phone_sim import make_frame, CONDS  # noqa: E402


def _quiet(*a, **k):
    pass


def grayish(img, k=0.5):
    """Cámara desaturada: mezcla hacia gris medio (pierde color/contraste)."""
    g = np.full_like(img, 128)
    return (img.astype(np.float32) * k
            + g.astype(np.float32) * (1 - k)).astype(np.uint8)


r = Router(entry_agent="apple", log=_quiet)
splits = json.loads(
    (Path(__file__).parent.parent / "data/eth80/splits.json").read_text())

N = 3
print(f"{'condicion':<16} aciertos  fix_activado")
for name, kw in CONDS.items():
    hits = fixes = 0
    for cls in CLASSES:
        for p in splits[cls]["test"][:N]:
            img = cv2.imread(p)
            res = r.route_frame(make_frame(img, **kw))
            hits += int(res["winner"] == cls)
            fixes += int(res["color_fix"])
    print(f"{name:<16} {hits:>2}/{N * 8:<6} {fixes}/{N * 8}")

for k, label in [(0.55, "grisacea fuerte"), (0.7, "grisacea media")]:
    hits = fixes = 0
    for cls in CLASSES:
        for p in splits[cls]["test"][:N]:
            img = grayish(cv2.imread(p), k)
            frame = cv2.copyMakeBorder(cv2.resize(img, (480, 480)),
                                       0, 0, 80, 80, cv2.BORDER_REPLICATE)
            res = r.route_frame(frame)
            hits += int(res["winner"] == cls)
            fixes += int(res["color_fix"])
    print(f"{label:<16} {hits:>2}/{N * 8:<6} {fixes}/{N * 8}")
