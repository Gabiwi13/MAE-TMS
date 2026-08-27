"""Exporta imágenes ETH-80 de test PRE-VALIDADAS para la prueba de
celular-frente-a-webcam: solo las que rutean correctamente a pantalla
completa (así, si fallan desde el celular, la causa es la condición de
pantalla, no la imagen). Ampliadas a 512² para verse grandes y llenar
el encuadre. Produce phone_test_images/ + zip + manifiesto."""
import json
import shutil
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))
from router import Router, CLASSES  # noqa: E402

PER_CLASS = 20
OUT = Path(__file__).parent / "phone_test_images"

r = Router(entry_agent="apple", log=lambda *a: None)
splits = json.loads(
    (Path(__file__).parent.parent / "data/eth80/splits.json").read_text())

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()

manifest = {}
for cls in CLASSES:
    kept, tried = 0, 0
    for p in splits[cls]["test"]:
        if kept >= PER_CLASS:
            break
        tried += 1
        img = cv2.imread(p)
        if img is None:
            continue
        # Validación: ¿rutea bien mostrada a pantalla completa?
        frame = cv2.copyMakeBorder(
            cv2.resize(img, (480, 480)), 0, 0, 80, 80,
            cv2.BORDER_REPLICATE)
        if r.route_frame(frame)["winner"] != cls:
            continue
        big = cv2.resize(img, (512, 512), interpolation=cv2.INTER_CUBIC)
        kept += 1
        cv2.imwrite(str(OUT / f"{cls}_{kept:02d}.png"), big)
    manifest[cls] = {"exportadas": kept, "revisadas": tried}
    print(f"{cls:<7} {kept}/{PER_CLASS} exportadas "
          f"(revisadas {tried} de {len(splits[cls]['test'])})")

(OUT / "LEEME.txt").write_text(
    "Imagenes ETH-80 de test PRE-VALIDADAS (rutean correctamente a\n"
    "pantalla completa con el directorio visual, entrada por apple).\n\n"
    "Uso: pasalas al celular, abre una a pantalla completa con el brillo\n"
    "al maximo, y muestrala a la webcam llenando el recuadro que dibuja\n"
    "python main.py. Nombre del archivo = clase esperada.\n\n"
    + json.dumps(manifest, indent=2), encoding="utf-8")

zip_path = shutil.make_archive(str(OUT), "zip", OUT)
total = sum(m["exportadas"] for m in manifest.values())
print(f"\ntotal {total} imagenes -> {OUT.name}\\ y {Path(zip_path).name}")
