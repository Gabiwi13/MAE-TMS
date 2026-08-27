"""Hoja de impresión para la prueba webcam: PDF carta 300 dpi con
imágenes ETH-80 pre-validadas en grande (2×2 por página ≈ 8.5 cm por
imagen — suficiente para llenar el recuadro de análisis a ~25 cm de la
cámara). Papel mate > pantalla: sin brillo propio, sin moiré."""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from router import CLASSES  # noqa: E402  (solo la lista, sin cargar modelos)

DPI = 300
PAGE = (int(8.5 * DPI), int(11 * DPI))          # carta 2550×3300
MARGIN = 130
CELL = 2                                          # 2×2 por página
IMG_PX = 1000                                     # ≈ 8.5 cm a 300 dpi
PER_CLASS = 2                                     # 8 clases × 2 = 16 imgs

SRC = Path(__file__).parent / "phone_test_images"
OUT = Path(__file__).parent / "hoja_impresion_eth80.pdf"

cells_per_page = CELL * CELL
gap_x = (PAGE[0] - 2 * MARGIN - CELL * IMG_PX) // (CELL - 1)
gap_y = (PAGE[1] - 2 * MARGIN - CELL * IMG_PX) // (CELL - 1)

items = []
for cls in CLASSES:
    for i in range(1, PER_CLASS + 1):
        p = SRC / f"{cls}_{i:02d}.png"
        if p.exists():
            items.append((cls, i, p))

pages = []
for start in range(0, len(items), cells_per_page):
    page = Image.new("RGB", PAGE, "white")
    draw = ImageDraw.Draw(page)
    draw.text((MARGIN, 40),
              "EAM-TMS · hoja de prueba webcam (ETH-80 pre-validadas) · "
              "imprimir a color, papel mate si es posible",
              fill=(120, 120, 120))
    for k, (cls, i, p) in enumerate(items[start:start + cells_per_page]):
        r, c = divmod(k, CELL)
        x = MARGIN + c * (IMG_PX + gap_x)
        y = MARGIN + r * (IMG_PX + gap_y)
        img = cv2.imread(str(p))
        big = cv2.resize(img, (IMG_PX, IMG_PX),
                         interpolation=cv2.INTER_CUBIC)
        page.paste(Image.fromarray(big[:, :, ::-1]), (x, y))
        draw.rectangle([x - 2, y - 2, x + IMG_PX + 1, y + IMG_PX + 1],
                       outline=(200, 200, 200), width=2)
        draw.text((x, y + IMG_PX + 14), f"{cls} #{i}",
                  fill=(110, 110, 110))
    pages.append(page)

# El Pillow instalado no registra JPEG (KeyError al guardar PDF);
# matplotlib como backend de PDF funciona con la misma calidad.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

with PdfPages(OUT) as pdf:
    for page in pages:
        fig = plt.figure(figsize=(8.5, 11), dpi=DPI)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.imshow(np.asarray(page))
        ax.axis("off")
        pdf.savefig(fig)
        plt.close(fig)
print(f"{len(items)} imagenes en {len(pages)} paginas -> {OUT.name}")
