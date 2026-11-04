"""
Figuras de la arquitectura mixta: diagrama del sistema y comparación con modelos
especializados. Todas las cifras salen de los informes de results/ (se listan en datos.csv).

Uso: python make_figuras_arquitectura.py
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).parent
OUT = ROOT / "results" / "figuras_arquitectura_mixta"

# Paleta de referencia (validada en su orden), tinta y superficies del modo claro.
SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
C_MAE, C_MAHA, C_KNN, C_MAE2, C_MAG, C_GREEN = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"
plt.rcParams.update({"font.family": "Segoe UI", "font.size": 10, "text.color": INK, "axes.edgecolor": AXIS,
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": INK2, "figure.facecolor": SURFACE,
                     "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE})

# (figura, panel, método, valor, fuente)
DATA = [
    ("deteccion_auroc", "Global ResNet18", "MAE leída en grado (κ, log-frecuencias)", 0.789, "parametros_mae, confirmación"),
    ("deteccion_auroc", "Global ResNet18", "Mahalanobis (PaDiM global)", 0.800, "parametros_mae, confirmación"),
    ("deteccion_auroc", "Global ResNet18", "kNN / PatchCore", 0.784, "parametros_mae, confirmación"),
    ("deteccion_auroc", "Global ResNet18", "MAE contención estricta", 0.547, "parametros_mae, confirmación"),
    ("deteccion_auroc", "Global WideResNet50", "MAE leída en grado (κ, log-frecuencias)", 0.756, "parametros_mae, confirmación"),
    ("deteccion_auroc", "Global WideResNet50", "Mahalanobis (PaDiM global)", 0.768, "parametros_mae, confirmación"),
    ("deteccion_auroc", "Global WideResNet50", "kNN / PatchCore", 0.746, "parametros_mae, confirmación"),
    ("deteccion_auroc", "Global WideResNet50", "MAE contención estricta", 0.535, "parametros_mae, confirmación"),
    ("deteccion_auroc", "Parches ResNet18", "MAE leída en grado (κ, log-frecuencias)", 0.695, "parametros_mae, confirmación"),
    ("deteccion_auroc", "Parches ResNet18", "Mahalanobis (PaDiM global)", 0.637, "parametros_mae, confirmación"),
    ("deteccion_auroc", "Parches ResNet18", "kNN / PatchCore", 0.830, "parametros_mae, confirmación (PatchCore)"),
    ("deteccion_auroc", "Parches ResNet18", "MAE contención estricta", 0.675, "parametros_mae, confirmación"),
    ("red_especializada", "detección (%)", "MAE sobre la red (buenas y malas)", 90.5, "cierre_mae, parte 2"),
    ("red_especializada", "detección (%)", "Cabeza de la red especializada", 93.0, "cierre_mae, parte 2"),
    ("red_especializada", "detección (%)", "kNN de dos clases", 87.1, "cierre_mae, parte 2"),
    ("red_especializada", "falsa alarma (%)", "MAE sobre la red (buenas y malas)", 1.8, "cierre_mae, parte 2"),
    ("red_especializada", "falsa alarma (%)", "Cabeza de la red especializada", 3.4, "cierre_mae, parte 2"),
    ("red_especializada", "falsa alarma (%)", "kNN de dos clases", 1.1, "cierre_mae, parte 2"),
    ("sistema", "fallas que pasan (%)", "Arquitectura mixta (MAE + PatchCore)", 37.9, "enrutador_flota, B1"),
    ("sistema", "fallas que pasan (%)", "PatchCore con la pieza conocida (ideal)", 39.2, "enrutador_flota, B1 (oráculo)"),
    ("sistema", "fallas que pasan (%)", "kNN + PatchCore", 39.2, "enrutador_flota, B1"),
    ("sistema", "fallas que pasan (%)", "kNN con umbral + PatchCore", 38.3, "enrutador_flota, B1"),
    ("sistema", "sanas detenidas (%)", "Arquitectura mixta (MAE + PatchCore)", 8.9, "enrutador_flota, B1: 100 - 91.1 que pasan"),
    ("sistema", "sanas detenidas (%)", "PatchCore con la pieza conocida (ideal)", 7.6, "enrutador_flota, B1: 100 - 92.4"),
    ("sistema", "sanas detenidas (%)", "kNN + PatchCore", 7.6, "enrutador_flota, B1: 100 - 92.4"),
    ("sistema", "sanas detenidas (%)", "kNN con umbral + PatchCore", 8.3, "enrutador_flota, B1: 100 - 91.7"),
    ("sistema", "sanas a revisión (%)", "Arquitectura mixta (MAE + PatchCore)", 1.6, "enrutador_flota, B1"),
    ("sistema", "sanas a revisión (%)", "PatchCore con la pieza conocida (ideal)", 0.0, "enrutador_flota, B1"),
    ("sistema", "sanas a revisión (%)", "kNN + PatchCore", 0.0, "enrutador_flota, B1"),
    ("sistema", "sanas a revisión (%)", "kNN con umbral + PatchCore", 1.0, "enrutador_flota, B1"),
    ("sistema", "pieza nueva desconocida (%)", "Arquitectura mixta (MAE + PatchCore)", 100.0, "enrutador_flota, B2 (12 pliegues)"),
    ("sistema", "pieza nueva desconocida (%)", "kNN + PatchCore", 0.0, "enrutador_flota, B2 (12 pliegues)"),
    ("sistema", "pieza nueva desconocida (%)", "kNN con umbral + PatchCore", 100.0, "enrutador_flota, B2 (12 pliegues)"),
    ("privacidad", "AUROC del ataque de pertenencia", "MAE (conteos agregados)", 0.507, "olvido_privacidad, media de 4 dominios"),
    ("privacidad", "AUROC del ataque de pertenencia", "NCM (media por clase)", 0.494, "olvido_privacidad, media de 4 dominios"),
    ("privacidad", "AUROC del ataque de pertenencia", "Gaussiana (Mahalanobis)", 0.587, "olvido_privacidad, media de 4 dominios"),
    ("privacidad", "AUROC del ataque de pertenencia", "kNN (guarda ejemplares)", 1.000, "olvido_privacidad, media de 4 dominios"),
]


def val(fig, panel, method):
    return next(v for f, p, m, v, _ in DATA if f == fig and p == panel and m == method)


# ---------- diagrama ----------

def box(ax, x, y, w, h, title, lines, kind):
    face = {"mae": "#e9f1fb", "std": "#f1f0ec", "human": "#fdf0e9", "log": "#f6f6f3"}[kind]
    edge = {"mae": C_MAE, "std": AXIS, "human": C_MAHA, "log": AXIS}[kind]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=face, ec=edge, lw=1.4 if kind != "log" else 1.0))
    ax.text(x + 0.25, y + h - 0.3, title, fontsize=11, fontweight="bold", va="top", color=INK)
    for k, s in enumerate(lines):
        ax.text(x + 0.25, y + h - 0.95 - 0.38 * k, s, fontsize=8.8, va="top", color=INK2)


def arrow(ax, a, b, label=None, off=(0, 0.12), color=INK2):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14, lw=1.4, color=color,
                                 shrinkA=2, shrinkB=2))
    if label:
        ax.text((a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1], label, fontsize=8.5, color=INK2,
                ha="center", va="bottom")


def flow_diagram():
    fig, ax = plt.subplots(figsize=(15.5, 7.6))
    ax.set_xlim(0, 31)
    ax.set_ylim(0, 15.2)
    ax.axis("off")
    ax.text(0.2, 15.0, "Arquitectura mixta: memoria asociativa entrópica (MAE) como filtro de dominio delante de detectores especializados",
            fontsize=14, fontweight="bold", va="top")
    ax.text(0.2, 14.35, "Azul: componentes de la MAE · gris: componentes estándar · naranja: revisión humana. Cifras medidas en VisA (12 piezas).",
            fontsize=9.5, color=INK2, va="top")
    top, h = 9.3, 3.8
    box(ax, 0.2, top + 1.2, 3.4, 2.4, "Pieza en la línea", ["imagen 224 × 224"], "std")
    box(ax, 4.7, top + 0.6, 5.4, 3.0, "1 · Percepción", ["ResNet18 de ImageNet, congelada", "PCA a 64 coordenadas", "cuantización en 32 niveles"], "std")
    box(ax, 11.5, top, 6.4, h, "2 · Capa MAE (contenido)", ["un especialista por tipo de pieza", "(tabla de conteos 64 × 32)",
                                                       "contención: «¿de qué pieza es?»", "rechazo directo de lo desconocido",
                                                       "98.4 % a su pieza · 0 confusiones", "100 % de abstención ante piezas nuevas"], "mae")
    box(ax, 19.4, top, 5.1, h, "3 · Elección del módulo", ["tabla de éxitos / intentos", "por módulo de la pieza",
                                                       "olvido exacto en ventana:", "se adapta a la deriva",
                                                       "(contar supera a los", "directorios transactivos)"], "mae")
    box(ax, 25.8, top, 5.0, h, "4 · Detector de la pieza", ["solo piezas sanas:", "PatchCore WRN50 (AUROC 0.886)",
                                                        "con fallas etiquetadas:", "red especializada (AUROC 0.994)",
                                                        "→ buena / mala + mapa"], "std")
    box(ax, 11.5, 4.9, 6.4, 2.75, "Revisión humana", ["«pieza desconocida»: ningún especialista",
                                                     "la contiene (en vez de reportarla como", "falla de otra pieza)"], "human")
    box(ax, 19.4, 4.9, 11.4, 2.75, "5 · Bitácora auditable", ["hash de la imagen · versión de la memoria (hash de los conteos)",
                                                             "especialista que respondió · coordenadas fuera de la envolvente",
                                                             "módulo y puntaje del detector · veredicto → misma versión, misma decisión"], "log")
    box(ax, 0.2, 0.6, 30.6, 3.1, "Operaciones de la capa MAE (sin reentrenar redes)",
        ["Registrar una pieza nueva: se crea su especialista con piezas sanas; el contenido de los demás no cambia.",
         "Olvidar un lote o un consentimiento retirado: se restan exactamente sus conteos (0 diferencias contra reconstruir; 0.09 s contra 30 s).",
         "Privacidad: la capa solo guarda conteos agregados, no imágenes ni latentes (ataque de pertenencia: AUROC 0.51, como una media; kNN 1.00).",
         "Lectura en grado (κ: log-frecuencias de los conteos): la propia memoria puntúa tipicidad como Mahalanobis (AUROC 0.789 contra 0.800)."], "mae")
    y = top + h / 2 + 0.2
    arrow(ax, (3.6, y), (4.7, y))
    arrow(ax, (10.1, y), (11.5, y), "latente")
    arrow(ax, (17.9, y), (19.4, y), "pieza p")
    arrow(ax, (24.5, y), (25.8, y), "módulo")
    arrow(ax, (14.7, top), (14.7, 7.65), "nadie la contiene", off=(1.6, -0.15), color=C_MAHA)
    arrow(ax, (28.3, top), (28.3, 7.65), "veredicto", off=(0.95, -0.15))
    arrow(ax, (17.9, 6.27), (19.4, 6.27))
    for f in ("svg", "png"):
        fig.savefig(OUT / f"flujo_operativo.{f}", dpi=200, bbox_inches="tight")
    plt.close(fig)



# ---------- figura de arquitectura (estilo artículo) ----------

def paper_inputs():
    """Miniaturas reales, latente de una falla de pcb1 y tablas de conteo reales de tres especialistas."""
    import sys
    import numpy as np
    sys.path.insert(0, str(ROOT / "src"))
    import run_cierre_mae as cm
    import run_industrial_demo as ind
    import run_medico_demo as demo
    from run_olvido_privacidad import industrial_level1
    fill, _, test, _ = industrial_level1()
    zs = np.concatenate([fill[p][:, 0] for p in ind.PIECES])
    lo, hi = zs.min(0), zs.max(0)
    g = (lo - 0.1 * (hi - lo), hi + 0.1 * (hi - lo))
    rel = {}
    for p in ("candle", "pcb1", "cashew"):
        q = demo.quantize_latent_global(fill[p].reshape(-1, 64).astype(np.float32), *g, 32)
        R = np.zeros((32, 64))
        np.add.at(R, (q, np.broadcast_to(np.arange(64), q.shape)), 1)
        rel[p] = R
    y = ind.imgs()["testy_pcb1"]
    j = int(np.where(y == 1)[0][0])            # primera imagen con falla de pcb1
    z = test["pcb1"][j]
    img_test = ind.imgs()["test_pcb1"][j]
    thumbs = [ind.imgs()[f"reg_{p}"][0] for p in ("candle", "pcb1", "cashew")]
    qz = demo.quantize_latent_global(z[None].astype(np.float32), *g, 32)[0]
    return thumbs, img_test, z, qz, rel


def trapezoid(ax, x, y, w, h, label, sub):
    from matplotlib.patches import Polygon
    ax.add_patch(Polygon([(x, y), (x + w, y + h * 0.18), (x + w, y + h * 0.82), (x, y + h)], closed=True,
                         fc="#f1f0ec", ec=AXIS, lw=1.3))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=16)
    ax.text(x + w / 2, y - 0.35, sub, ha="center", va="top", fontsize=8.3, color=INK2)


def strip(ax, x, y, h, values, cmap, label):
    import numpy as np
    ax.imshow(np.asarray(values)[:, None], extent=(x, x + 0.42, y, y + h), cmap=cmap, aspect="auto", interpolation="nearest")
    ax.add_patch(FancyBboxPatch((x, y), 0.42, h, boxstyle="square,pad=0", fc="none", ec=AXIS, lw=1))
    ax.text(x + 0.21, y - 0.35, label, ha="center", va="top", fontsize=9)


def thumb(ax, img, x, y, s, edge=AXIS):
    ax.imshow(img, extent=(x, x + s, y, y + s), interpolation="bilinear")
    ax.add_patch(FancyBboxPatch((x, y), s, s, boxstyle="square,pad=0", fc="none", ec=edge, lw=1.2))


def rbox(ax, x, y, w, h, kind):
    face, edge = {"mae": ("#e9f1fb", C_MAE), "std": ("#f1f0ec", AXIS), "human": ("#fdf0e9", C_MAHA)}[kind]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15", fc=face, ec=edge, lw=1.4))


def paper_figure():
    import numpy as np
    thumbs, img_test, z, qz, rel = paper_inputs()
    fig, ax = plt.subplots(figsize=(16, 8.6))
    ax.set_xlim(0, 32.3)
    ax.set_ylim(0, 17.2)
    ax.axis("off")
    for (y0, y1, name) in ((9.0, 16.6, "Registro (fuera de línea)"), (0.4, 8.2, "Inferencia")):
        ax.add_patch(FancyBboxPatch((0.2, y0), 12.3, y1 - y0, boxstyle="round,pad=0,rounding_size=0.3",
                                    fc="#f9f9f7", ec=GRID, lw=1.2, ls=(0, (4, 3)), zorder=-2))
        ax.text(0.55, y1 - 0.45, name, fontsize=11, fontweight="bold", va="top", color=INK2)
    yt, yb = 11.9, 3.4
    # registro
    for k, im in enumerate(thumbs):
        thumb(ax, im, 0.7 + 0.45 * k, yt - 1.2 + 0.45 * (2 - k), 2.2)
    ax.text(2.1, yt - 1.6, r"$\mathcal{X}_k$: piezas sanas" + "\n" + r"del tipo $k$", ha="center", va="top", fontsize=9)
    trapezoid(ax, 4.6, yt - 1.4, 2.2, 3.2, r"$f_\theta$", "ResNet18 + PCA$_{64}$\n(congelado)")
    strip(ax, 8.2, yt - 1.6, 3.6, z, "Blues", r"$\mathbf{z}\in\mathbb{R}^{64}$")
    strip(ax, 10.0, yt - 1.6, 3.6, qz, "Greys", r"$q(\mathbf{z})$")
    arrow(ax, (3.9, yt + 0.2), (4.6, yt + 0.2))
    arrow(ax, (6.8, yt + 0.2), (8.2, yt + 0.2))
    arrow(ax, (8.62, yt + 0.2), (10.0, yt + 0.2), r"$q$", off=(0, 0.1))
    # banco de especialistas
    bx, by = 13.4, 6.4
    for k, p in enumerate(["cashew", "pcb1", "candle"]):
        R = np.log1p(rel[p])
        x0, y0 = bx + 0.55 * (2 - k), by + 0.55 * (2 - k)
        ax.imshow(R, extent=(x0, x0 + 5.0, y0, y0 + 2.6), cmap="Blues", aspect="auto", interpolation="nearest", origin="lower")
        ax.add_patch(FancyBboxPatch((x0, y0), 5.0, 2.6, boxstyle="square,pad=0", fc="none", ec=C_MAE, lw=1.3))
    ax.text(bx + 3.05, by + 4.15, r"$\mathbf{M}_1,\ldots,\mathbf{M}_K\in\mathbb{N}^{64\times 32}$", ha="center", fontsize=11.5)
    ax.text(bx + 3.05, by - 0.4, "un especialista por tipo de pieza:\nconteos por coordenada y nivel (sin ejemplares)",
            ha="center", va="top", fontsize=8.6, color=INK2)
    ax.add_patch(FancyArrowPatch((10.5, yt + 0.2), (bx + 1.7, by + 3.8), arrowstyle="-|>", mutation_scale=14, lw=1.4,
                                 color=C_MAE, ls=(0, (4, 3)), connectionstyle="arc3,rad=-0.2"))
    ax.text(13.6, yt + 0.95, r"$\lambda$: $M_k[i,q_i(\mathbf{z})]\ +\!=1$", fontsize=10, color=C_MAE)
    ax.text(13.6, yt + 0.3, r"olvido exacto: $M_k[i,q_i(\mathbf{z})]\ -\!=1$", fontsize=9, color=INK2)
    # inferencia
    thumb(ax, img_test, 0.9, yb - 1.1, 2.4)
    ax.text(2.1, yb - 1.5, r"consulta $\mathbf{x}$", ha="center", va="top", fontsize=9)
    trapezoid(ax, 4.6, yb - 1.4, 2.2, 3.2, r"$f_\theta$", "pesos compartidos")
    strip(ax, 8.2, yb - 1.6, 3.6, z, "Blues", r"$\mathbf{z}$")
    strip(ax, 10.0, yb - 1.6, 3.6, qz, "Greys", r"$q(\mathbf{z})$")
    arrow(ax, (3.3, yb + 0.2), (4.6, yb + 0.2))
    arrow(ax, (6.8, yb + 0.2), (8.2, yb + 0.2))
    arrow(ax, (8.62, yb + 0.2), (10.0, yb + 0.2), r"$q$", off=(0, 0.1))
    ax.add_patch(FancyArrowPatch((10.5, yb + 0.2), (bx + 0.4, by + 0.3), arrowstyle="-|>", mutation_scale=14, lw=1.4,
                                 color=INK2, connectionstyle="arc3,rad=0.2"))
    # lectura de la memoria
    rx, ry = 20.6, 5.5
    rbox(ax, rx, ry, 6.5, 4.2, "mae")
    ax.text(rx + 0.25, ry + 3.85, r"lectura $\eta$ de cada $\mathbf{M}_k$", fontsize=10.5, fontweight="bold", va="top")
    ax.text(rx + 0.25, ry + 3.0, r"contención: $M_k[i,q_i(\mathbf{z})]>0$ (salvo $\xi$)", fontsize=9, va="top")
    ax.text(rx + 0.25, ry + 2.2, r"grado ($\kappa$): $s_k=\sum_i \log\,(1+M_k[i,q_i(\mathbf{z})])$", fontsize=9, va="top")
    ax.text(rx + 0.25, ry + 1.4, r"$k^*=\arg\max_k\, s_k$ entre los que contienen", fontsize=9, va="top")
    ax.text(rx + 0.25, ry + 0.65, r"ninguno contiene $\Rightarrow\ \varnothing$", fontsize=9, va="top")
    arrow(ax, (bx + 6.2, by + 2.0), (rx, ry + 2.0))
    # revisión humana
    rbox(ax, rx + 0.75, 0.9, 4.1, 2.0, "human")
    ax.text(rx + 2.8, 2.15, "revisión humana", ha="center", fontsize=10, fontweight="bold")
    ax.text(rx + 2.8, 1.45, "«pieza desconocida»", ha="center", fontsize=9, color=INK2)
    arrow(ax, (rx + 2.8, ry), (rx + 2.8, 2.9), r"$\varnothing$", off=(0.35, -0.2), color=C_MAHA)
    # elección del módulo y detector
    mx = 27.6
    rbox(ax, mx, ry + 2.0, 4.2, 2.2, "mae")
    ax.text(mx + 0.2, ry + 3.85, r"$m^*=\arg\max_m\ \hat{p}_{k^*\!,m}$", fontsize=10, va="top")
    ax.text(mx + 0.2, ry + 3.0, r"$\hat{p}$ = éxitos / intentos, con" + "\n" + "olvido en ventana (deriva)", fontsize=8.5, va="top", color=INK2)
    rbox(ax, mx, ry - 1.2, 4.2, 2.4, "std")
    ax.text(mx + 0.2, ry + 0.9, r"detector $D_{k^*,m^*}$", fontsize=10.5, fontweight="bold", va="top")
    ax.text(mx + 0.2, ry + 0.2, "PatchCore (solo sanas) o\nred especializada (con fallas)", fontsize=8.5, va="top", color=INK2)
    arrow(ax, (rx + 6.5, ry + 3.6), (mx, ry + 3.6), r"$k^*$", off=(0, 0.08))
    arrow(ax, (mx + 2.1, ry + 2.0), (mx + 2.1, ry + 1.2), r"$m^*$", off=(0.4, -0.25))
    arrow(ax, (mx + 2.1, ry - 1.2), (mx + 2.1, 3.0))
    ax.text(mx + 2.1, 2.75, r"$\hat{y}\in\{\mathrm{buena},\ \mathrm{mala}\}$", ha="center", va="top", fontsize=10.5)
    ax.text(mx + 2.1, 1.9, "bitácora:\n" + r"hash($\mathbf{x}$), hash($\mathbf{M}$), $k^*$, $m^*$, $s_{k^*}$", ha="center", va="top",
            fontsize=8.3, color=INK2)
    # leyenda
    lx, ly = 19.4, 15.75
    ax.add_patch(FancyArrowPatch((lx, ly), (lx + 1.2, ly), arrowstyle="-|>", mutation_scale=12, lw=1.4, color=C_MAE, ls=(0, (4, 3))))
    ax.text(lx + 1.4, ly, "registro", va="center", fontsize=9)
    ax.add_patch(FancyArrowPatch((lx, ly - 0.7), (lx + 1.2, ly - 0.7), arrowstyle="-|>", mutation_scale=12, lw=1.4, color=INK2))
    ax.text(lx + 1.4, ly - 0.7, "inferencia", va="center", fontsize=9)
    for k, (kind, txt) in enumerate((("mae", "memoria asociativa entrópica"), ("std", "componente estándar"),
                                     ("human", "revisión humana"))):
        face, edge = {"mae": ("#e9f1fb", C_MAE), "std": ("#f1f0ec", AXIS), "human": ("#fdf0e9", C_MAHA)}[kind]
        ax.add_patch(FancyBboxPatch((lx + 4.4, ly - 0.2 - 0.7 * k), 0.6, 0.4, boxstyle="square,pad=0", fc=face, ec=edge))
        ax.text(lx + 5.2, ly - 0.7 * k, txt, va="center", fontsize=9)
    for f in ("svg", "png"):
        fig.savefig(OUT / f"arquitectura_mixta.{f}", dpi=200, bbox_inches="tight")
    plt.close(fig)


# ---------- comparación ----------

def clean(ax):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.grid(axis="x", color=GRID, lw=1)
    ax.set_axisbelow(True)


def hbars(ax, labels, values, colors, fmt, xmax, xlabel, notes=None):
    ys = range(len(labels))[::-1]
    for k, (y, v, c) in enumerate(zip(ys, values, colors)):
        ax.barh(y, v, height=0.45, color=c, edgecolor=SURFACE, lw=2)
        ax.text(v + xmax * 0.012, y + (0.1 if notes and notes[k] else 0), fmt(v), va="center", fontsize=9.5, color=INK)
        if notes and notes[k]:
            ax.text(v + xmax * 0.012, y - 0.2, notes[k], va="center", fontsize=8.3, color=INK2)
    ax.set_yticks(list(ys), labels)
    ax.set_xlim(0, xmax)
    ax.set_xlabel(xlabel)
    clean(ax)


SYSTEMS = [("Arquitectura mixta (MAE + PatchCore)", C_MAE), ("PatchCore con la pieza conocida (ideal)", MUTED),
           ("kNN + PatchCore", C_KNN), ("kNN con umbral + PatchCore", C_MAG)]


def comparison():
    fig = plt.figure(figsize=(15, 15))
    gs = fig.add_gridspec(3, 2, hspace=0.5, wspace=0.62, left=0.2, right=0.97, top=0.885, bottom=0.05)
    fig.text(0.02, 0.975, "La MAE y la arquitectura mixta frente a modelos especializados", fontsize=15, fontweight="bold")
    fig.text(0.02, 0.957, "Fila 1: la MAE como componente · filas 2 y 3: el sistema completo, punta a punta, en VisA (12 piezas). "
             "Mismos datos y latentes en cada panel; cifras en datos.csv.", fontsize=9.5, color=INK2)

    # a) la MAE como detector de una clase
    ax = fig.add_subplot(gs[0, 0])
    groups = ["Global ResNet18", "Global WideResNet50", "Parches ResNet18"]
    series = [("MAE leída en grado (κ, log-frecuencias)", C_MAE, "o"), ("Mahalanobis (PaDiM global)", C_MAHA, "s"),
              ("kNN / PatchCore", C_KNN, "D"), ("MAE contención estricta", C_MAE2, "^")]
    for gi, g in enumerate(groups):
        base = len(groups) - 1 - gi
        for si, (m, c, mk) in enumerate(series):
            y = base + 0.27 - si * 0.18
            v = val("deteccion_auroc", g, m)
            ax.plot([0.5, v], [y, y], color=GRID, lw=1, zorder=1)
            ax.scatter(v, y, s=70, color=c, marker=mk, edgecolor=SURFACE, lw=1.5, zorder=3)
            ax.text(v + 0.006, y, f"{v:.3f}", va="center", fontsize=8.5, color=INK)
    ax.set_yticks([2, 1, 0], groups)
    ax.set_xlim(0.5, 0.88)
    ax.axvline(0.5, color=AXIS, lw=1)
    ax.set_xlabel("AUROC en piezas de confirmación (0.5 = azar)")
    ax.set_title("a · La MAE como detector (solo piezas sanas)", loc="left", fontsize=11, fontweight="bold")
    clean(ax)
    fig.legend(handles=[plt.Line2D([], [], marker=mk, ls="", color=c, markersize=8, label=m) for m, c, mk in series],
               loc="upper left", bbox_to_anchor=(0.02, 0.945), ncol=4, frameon=False, fontsize=9)
    fig.text(0.02, 0.917, "Panel a: kNN / PatchCore es kNN euclídeo en los globales y PatchCore en parches.", fontsize=8.5, color=MUTED)

    # b) sobre una red especializada
    ax = fig.add_subplot(gs[0, 1])
    ms = [("MAE sobre la red (buenas y malas)", C_MAE), ("Cabeza de la red especializada", C_MAHA), ("kNN de dos clases", C_KNN)]
    hbars(ax, [m for m, _ in ms], [val("red_especializada", "detección (%)", m) for m, _ in ms], [c for _, c in ms],
          lambda v: f"{v:.1f} %", 125, "fallas detectadas (%) · media de 12 piezas",
          [f"falsa alarma {val('red_especializada', 'falsa alarma (%)', m):.1f} %" for m, _ in ms])
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_title("b · La MAE sobre una red especializada (WRN50 ajustada)", loc="left", fontsize=11, fontweight="bold")

    names, colors = [m for m, _ in SYSTEMS], [c for _, c in SYSTEMS]
    # c) sistema: fallas que pasan
    ax = fig.add_subplot(gs[1, 0])
    hbars(ax, names, [val("sistema", "fallas que pasan (%)", m) for m in names], colors, lambda v: f"{v:.1f} %", 60,
          "fallas que pasan sin detectarse (%) · menos es mejor")
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.set_title("c · Sistema completo: fallas que se escapan", loc="left", fontsize=11, fontweight="bold")

    # d) sistema: piezas sanas detenidas
    ax = fig.add_subplot(gs[1, 1])
    notes = [f"de ellas, a revisión humana {val('sistema', 'sanas a revisión (%)', m):.1f} %" for m in names]
    hbars(ax, names, [val("sistema", "sanas detenidas (%)", m) for m in names], colors, lambda v: f"{v:.1f} %", 22,
          "piezas sanas detenidas (%) · alarma + revisión · menos es mejor", notes)
    ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_title("d · Sistema completo: costo en piezas sanas", loc="left", fontsize=11, fontweight="bold")

    # e) sistema: pieza nueva
    ax = fig.add_subplot(gs[2, 0])
    sub = [s for s in SYSTEMS if not s[0].startswith("PatchCore con")]
    notes = [None if val("sistema", "pieza nueva desconocida (%)", m) == 100
             else "el resto se reporta como falla de otra pieza" for m, _ in sub]
    hbars(ax, [m for m, _ in sub], [val("sistema", "pieza nueva desconocida (%)", m) for m, _ in sub], [c for _, c in sub],
          lambda v: f"{v:.0f} %", 150, "imágenes de una pieza nunca registrada reportadas como «desconocida» (%)", notes)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_title("e · Sistema completo: llega una pieza nueva", loc="left", fontsize=11, fontweight="bold")
    ax.text(0, -0.95, "El ideal no aplica: no hay detector para una pieza nunca registrada.", fontsize=8.3, color=MUTED)

    # f) privacidad
    ax = fig.add_subplot(gs[2, 1])
    ms = [("MAE (conteos agregados)", C_MAE), ("NCM (media por clase)", C_GREEN), ("Gaussiana (Mahalanobis)", C_MAHA),
          ("kNN (guarda ejemplares)", C_KNN)]
    ys = range(len(ms))[::-1]
    for y, (m, c) in zip(ys, ms):
        v = val("privacidad", "AUROC del ataque de pertenencia", m)
        ax.plot([0.4, v], [y, y], color=GRID, lw=1, zorder=1)
        ax.scatter(v, y, s=80, color=c, edgecolor=SURFACE, lw=1.5, zorder=3)
        ax.text(v + 0.015, y, f"{v:.3f}", va="center", fontsize=9.5)
    ax.axvline(0.5, color=AXIS, lw=1)
    ax.text(0.51, -0.55, "0.5: no revela quién fue registrado", fontsize=8.3, color=INK2)
    ax.set_ylim(-0.75, len(ms) - 0.5)
    ax.set_yticks(list(ys), [m for m, _ in ms])
    ax.set_xlim(0.4, 1.1)
    ax.set_xlabel("AUROC del ataque de pertenencia (media de 4 dominios)")
    ax.set_title("f · Privacidad: cuánto revela de un registro individual", loc="left", fontsize=11, fontweight="bold")
    clean(ax)
    for f in ("svg", "png"):
        fig.savefig(OUT / f"comparacion_modelos.{f}", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "datos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["figura", "panel", "metodo", "valor", "fuente"])
        w.writerows(DATA)
    flow_diagram()
    paper_figure()
    comparison()
    print("figuras en", OUT)


if __name__ == "__main__":
    main()
