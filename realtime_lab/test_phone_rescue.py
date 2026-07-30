"""¿Se rescata el ruteo de pantalla-de-celular con preprocesamiento del
«ojo»? (a) recorte exacto de la región de la imagen; (b) normalización
de color/brillo por canal a los momentos de la imagen de entrenamiento.
No toca la MAE: son lentes para el encoder."""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from router import Router, CLASSES  # noqa: E402
from test_phone_sim import make_frame, CONDS  # noqa: E402


def color_match(img, ref_mean, ref_std):
    x = img.astype(np.float32)
    for c in range(3):
        m, s = x[:, :, c].mean(), x[:, :, c].std() + 1e-6
        x[:, :, c] = (x[:, :, c] - m) / s * ref_std[c] + ref_mean[c]
    return np.clip(x, 0, 255).astype(np.uint8)


r = Router(entry_agent="apple", log=lambda *a: None)
splits = json.loads(
    (Path(__file__).parent.parent / "data/eth80/splits.json").read_text())

# Momentos de referencia: promedio de una imagen de train por clase
refs = [cv2.imread(splits[c]["train"][0]).astype(np.float32)
        for c in CLASSES]
ref_mean = np.mean([im.mean(axis=(0, 1)) for im in refs], axis=0)
ref_std = np.mean([im.std(axis=(0, 1)) for im in refs], axis=0)

N = 3
hard = {k: v for k, v in CONDS.items() if k != "limpia 100%"}
print(f"{'condicion':<16} {'sin rescate':<12} {'crop':<8} "
      f"{'crop+color':<10}")
for cond, kw in hard.items():
    base = crop = both = 0
    for cls in CLASSES:
        for p in splits[cls]["test"][:N]:
            img = cv2.imread(p)
            frame = make_frame(img, **kw)
            base += int(r.route_frame(frame)["winner"] == cls)
            # (a) recorte exacto de la región donde está la imagen
            s = int(480 * kw.get("scale", 1.0))
            y0, x0 = (480 - s) // 2, (640 - s) // 2
            region = frame[y0:y0 + s, x0:x0 + s]
            fr2 = cv2.resize(region, (480, 480))
            fr2 = cv2.copyMakeBorder(fr2, 0, 0, 80, 80,
                                     cv2.BORDER_REPLICATE)
            crop += int(r.route_frame(fr2)["winner"] == cls)
            # (b) recorte + normalización de color
            fr3 = cv2.resize(color_match(region, ref_mean, ref_std),
                             (480, 480))
            fr3 = cv2.copyMakeBorder(fr3, 0, 0, 80, 80,
                                     cv2.BORDER_REPLICATE)
            both += int(r.route_frame(fr3)["winner"] == cls)
    t = N * len(CLASSES)
    print(f"{cond:<16} {base:>2}/{t:<9} {crop:>2}/{t:<5} {both:>2}/{t}")
