"""
Experimento 8 — Recuperación desde el directorio.

El directorio de Wegner se usaba en un solo sentido: pista -> agente. Pero es
una memoria hetero-asociativa, así que admite el sentido inverso: identidad de
agente -> pista. Eso permite preguntarle a un agente qué puede reconstruir de
un dominio del que no es especialista, usando solo lo que presenció.

Parte A — figura del objeto recuperado: para cada dominio, la imagen real, la
reconstrucción del especialista desde su memoria de contenido, la del propio
directorio, la del directorio de un no-especialista, y la instancia real más
cercana a lo recuperado.

Parte B — sorteos: la proyección de una identidad admite ~10^60 patrones, así
que cada recall devuelve uno distinto. Cuatro sorteos del mismo dominio ajeno
más la lectura determinista por argmax.

Parte C — cara negativa: el registro escribe un 1 en el ganador y un 0 en los
otros siete, así que la cara del "no ganó" acumula siete veces más masa. Leída
sola devuelve el complemento del agente.

Parte D — sondas numéricas: identidad de los directorios, controles del
clasificador, fidelidad, superposición, masa por cara, identidades imposibles
y curva de capacidad.

Parte E — barrido de fracción presenciada: en el protocolo actual todos los
agentes registran todos los broadcasts, así que los ocho directorios son la
misma relación y lo propio no se distingue de lo ajeno. Aquí cada agente
registra los broadcasts que no ganó con probabilidad f, y se mide cómo cae la
reconstrucción del dominio ajeno mientras la del propio se mantiene.

Uso:  python run_experiment8_directory_recall.py
        [--figure] [--draws] [--negative] [--probes] [--sweep]
      Sin argumentos corre todo. El barrido tarda ~50 min.
"""
import argparse
import contextlib
import io
import json
import pickle
import sys
import time
from pathlib import Path

import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from associative_memory import DirectoryMemory
from quantizer import quantize_binary
from stage5_fill import N_FILL, FILL_AUG_ANGLES, quantize_latent_global
from stage6_interaction import (
    CLASSES, AGENT_LIST, MODELS_DIR, DEVICE, M_LABEL, P_LATENT, Q_LATENT,
)
from stage7_bidirectional import load_global_stats

OUT_DIR = ROOT / "results" / "experimento8"
DATA_DIR = ROOT / "data" / "eth80"
LATENT_CACHE = ROOT / "results" / "experimento7" / "latents_cache.json"

K = len(AGENT_LIST)
N_IMG_TRAIN = 128                       # mismo pool visual que la etapa 7
REPS = 10                               # recalls por celda (el recall muestrea)
# La transición está entre 0 y 1/8, así que la grilla se afina abajo: las
# fracciones chicas son 1, 2, 4, 8 y 16 broadcasts ajenos presenciados de 128.
FRACTIONS = (0.0, 1 / 128, 2 / 128, 4 / 128, 8 / 128, 16 / 128, 0.25, 0.5, 1.0)
# Registros por agente de la curva de capacidad. Llegan a 800 porque es lo que
# tiene la memoria de contenido de cada especialista (200 imágenes × 4 variantes).
CAPACITY_SIZES = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 800)
SEED = 42

DOMAIN_COLOR = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60",
                "cow": "#8e44ad", "cup": "#c9760a", "dog": "#16a085",
                "pear": "#7d8f22", "tomato": "#c0392b"}

plt.rcParams.update({
    "figure.dpi": 300, "savefig.dpi": 300,
    "font.family": "DejaVu Sans", "font.size": 10,
})


# ---------- utilidades comunes ----------

def onehot(idx: int) -> np.ndarray:
    v = np.zeros(K, dtype=np.int32)
    v[idx] = 1
    return v


def safe_mean(values) -> float:
    """Media ignorando NaN. Con f=0 el agente no presenció nada ajeno y la
    celda entera queda vacía: eso es un resultado, no un error."""
    vals = [v for v in values if not np.isnan(v)]
    return float(np.mean(vals)) if vals else float("nan")


def dequantize_latent(z_q, g_min, g_max) -> np.ndarray:
    return ((np.asarray(z_q, dtype=float) / (Q_LATENT - 1))
            * (g_max - g_min) + g_min).astype(np.float32)


def load_agent(name: str):
    with open(MODELS_DIR / f"agent_{name}.pkl", "rb") as f:
        return pickle.load(f)


def load_decoder():
    from stage2_encoder import Decoder
    dec = Decoder().to(DEVICE)
    dec.load_state_dict(torch.load(MODELS_DIR / "decoder.pt", map_location=DEVICE))
    dec.eval()
    return dec


def load_classifier():
    from stage2_encoder import Classifier
    clf = Classifier().to(DEVICE)
    clf.load_state_dict(torch.load(MODELS_DIR / "classifier.pt", map_location=DEVICE))
    clf.eval()
    return clf


def decode_image(z: np.ndarray, decoder) -> np.ndarray:
    with torch.no_grad():
        img = decoder(torch.tensor(z).unsqueeze(0).to(DEVICE))[0].clamp(0, 1)
    return img.cpu().permute(1, 2, 0).numpy()


def recall_domain(ham, agent_idx: int):
    """Identidad de agente -> pista latente. El directorio leído al revés."""
    with contextlib.redirect_stdout(io.StringIO()):
        z_q, recognized, _w, _p, _s = ham.recall_from_right(
            onehot(agent_idx), weights=np.ones(K, dtype=float))
    return z_q, bool(recognized)


def instance_image(cls: str, idx: int, splits) -> np.ndarray:
    """La imagen (con su variante de augmentación) detrás del latente idx de
    instance_latents_{cls}.json: 4 variantes por imagen, en el orden de
    _augment_variants."""
    img = Image.open(splits[cls]["train"][idx // 4]).convert("RGB").resize((128, 128))
    v = idx % 4
    if v == 1:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif v >= 2:
        img = img.rotate(FILL_AUG_ANGLES[v - 2], resample=Image.BILINEAR)
    return np.asarray(img, dtype=np.float32) / 255.0


# ---------- Parte A: figura del objeto recuperado ----------

def figure_recovered_object():
    print("Parte A — figura del objeto recuperado")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    g_min, g_max = load_global_stats()
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    decoder = load_decoder()
    # el recall muestrea con el RNG global de numpy: sin esto la figura sale
    # distinta en cada corrida (cada recall es un sorteo entre ~10^60 patrones)
    np.random.seed(SEED)

    label_vecs = {c: json.loads((ROOT / f"label_vectors_{c}.json").read_text())
                  for c in CLASSES}
    instances = {c: np.array(json.loads(
        (MODELS_DIR / f"instance_latents_{c}.json").read_text()), dtype=np.float32)
        for c in CLASSES}

    cols = ["ETH-80\n(real)", "vivido\nM_dom_H", "directorio\npropio",
            "directorio\nno-especialista", "instancia real\nmás cercana"]
    fig, axes = plt.subplots(len(CLASSES), 5, figsize=(11, 2.05 * len(CLASSES)))

    rows_meta = []
    for ci, cls in enumerate(CLASSES):
        other = CLASSES[(ci + 1) % len(CLASSES)]
        spec = load_agent(cls)
        nonspec = load_agent(other)

        panels = [np.asarray(Image.open(splits[cls]["train"][0])
                             .convert("RGB").resize((128, 128)),
                             dtype=np.float32) / 255.0]

        # vivido: el especialista recuerda desde una etiqueta de su dominio
        words = ([cls] if cls in label_vecs[cls] else []) + list(label_vecs[cls])
        lived = None
        for word in words:
            v_q = quantize_binary(np.asarray(label_vecs[cls][word]), M_LABEL)
            with contextlib.redirect_stdout(io.StringIO()):
                z_q, recognized, *_ = spec.mem_dom_H.recall_from_left(v_q)
            if recognized:
                lived = (word, dequantize_latent(z_q, g_min, g_max))
                break
        panels.append(decode_image(lived[1], decoder) if lived else None)

        # directorio: propio y de un no-especialista
        z_own, ok_own = recall_domain(spec.mem_dir_R._ham, ci)
        z_oth, ok_oth = recall_domain(nonspec.mem_dir_R._ham, ci)
        lat_own = dequantize_latent(z_own, g_min, g_max) if ok_own else None
        lat_oth = dequantize_latent(z_oth, g_min, g_max) if ok_oth else None
        panels.append(decode_image(lat_own, decoder) if ok_own else None)
        panels.append(decode_image(lat_oth, decoder) if ok_oth else None)

        # la instancia real más cercana a lo que recuperó el no-especialista
        nearest_d = float("nan")
        if ok_oth:
            d = np.linalg.norm(instances[cls] - lat_oth, axis=1)
            j = int(np.argmin(d))
            nearest_d = float(d[j])
            panels.append(instance_image(cls, j, splits))
        else:
            panels.append(None)

        for k, (ax, img) in enumerate(zip(axes[ci], panels)):
            if img is not None:
                ax.imshow(img)
            else:
                ax.set_facecolor("#ecf0f1")
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_edgecolor(DOMAIN_COLOR[cls] if k else "#888")
                s.set_linewidth(1.6 if k else 0.8)
            if ci == 0:
                ax.set_title(cols[k], fontsize=9, pad=6)
        axes[ci, 0].set_ylabel(cls.upper(), fontsize=10, fontweight="bold",
                               color=DOMAIN_COLOR[cls], labelpad=8)
        axes[ci, 3].set_xlabel(f"lo recupera «{other}»", fontsize=7.5, labelpad=2)
        axes[ci, 4].set_xlabel(f"d = {nearest_d:.1f}", fontsize=7.5, labelpad=2)

        rows_meta.append({"clase": cls, "no_especialista": other,
                          "label_vivido": lived[0] if lived else None,
                          "d_recuperado_a_instancia_mas_cercana": nearest_d})
        del spec, nonspec
        print(f"  {cls:>7} listo")

    fig.suptitle("El objeto recuperado: contenido vivido vs. directorio presenciado",
                 fontsize=13, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    path = OUT_DIR / "fig1_objeto_recuperado.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    (OUT_DIR / "figura_meta.json").write_text(json.dumps(rows_meta, indent=2))
    print(f"  -> {path}")
    return path


def figure_draws(n_draws: int = 4):
    """La proyección admite ~10^60 patrones; cada recall devuelve uno. Cuatro
    sorteos del mismo dominio, más la lectura determinista (argmax por
    coordenada), que no muestrea."""
    print("Figura de sorteos")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    g_min, g_max = load_global_stats()
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    decoder = load_decoder()
    np.random.seed(SEED)

    n_cols = 2 + n_draws
    fig, axes = plt.subplots(len(CLASSES), n_cols,
                             figsize=(2.05 * n_cols, 2.05 * len(CLASSES)))
    cols = (["ETH-80\n(real)"] + [f"sorteo {i+1}" for i in range(n_draws)]
            + ["argmax\n(sin muestreo)"])

    meta = []
    for ci, cls in enumerate(CLASSES):
        other = CLASSES[(ci + 1) % len(CLASSES)]
        nonspec = load_agent(other)
        ham = nonspec.mem_dir_R._ham

        panels = [np.asarray(Image.open(splits[cls]["train"][0])
                             .convert("RGB").resize((128, 128)),
                             dtype=np.float32) / 255.0]
        lats = []
        for _ in range(n_draws):
            z_q, ok = recall_domain(ham, ci)
            if ok:
                lats.append(dequantize_latent(z_q, g_min, g_max))
                panels.append(decode_image(lats[-1], decoder))
            else:
                panels.append(None)

        with contextlib.redirect_stdout(io.StringIO()):
            proj = ham.project(ham.validate(onehot(ci), 1),
                               np.ones(K, dtype=float), 1)
        z_arg = dequantize_latent(np.argmax(proj, axis=1), g_min, g_max)
        panels.append(decode_image(z_arg, decoder))

        spread = float(np.mean([np.linalg.norm(lats[i] - lats[j])
                                for i in range(len(lats))
                                for j in range(i + 1, len(lats))])) if len(lats) > 1 else float("nan")
        niveles = float((proj > 0).sum(axis=1).mean())

        for k, (ax, img) in enumerate(zip(axes[ci], panels)):
            if img is not None:
                ax.imshow(img)
            else:
                ax.set_facecolor("#ecf0f1")
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_edgecolor(DOMAIN_COLOR[cls] if k else "#888")
                s.set_linewidth(1.6 if k else 0.8)
            if ci == 0:
                ax.set_title(cols[k], fontsize=9, pad=6)
        axes[ci, 0].set_ylabel(cls.upper(), fontsize=10, fontweight="bold",
                               color=DOMAIN_COLOR[cls], labelpad=8)
        axes[ci, n_cols // 2].set_xlabel(
            f"{niveles:.1f}/{Q_LATENT} niveles por coordenada  ·  "
            f"dispersión entre sorteos {spread:.1f}", fontsize=7.5, labelpad=2)

        meta.append({"clase": cls, "recupera": other,
                     "niveles_por_coordenada": niveles,
                     "dispersion_entre_sorteos": spread})
        del nonspec
        print(f"  {cls:>7} listo")

    fig.suptitle("Cuatro sorteos del mismo dominio ajeno: no hay una figura guardada",
                 fontsize=13, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    path = OUT_DIR / "fig3_sorteos.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    (OUT_DIR / "sorteos_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"  -> {path}")
    return path


def cue_face(agent_idx: int, bit: int) -> np.ndarray:
    """Pista de identidad con UNA sola coordenada definida: la del agente, en
    la cara pedida. El resto viaja como nan (undefined) para que la proyección
    las salte y no intersecte nada más."""
    v = np.full(K, np.nan)
    v[agent_idx] = float(bit)
    return v


def figure_negative_face(n_draws: int = 2, reps: int = 20):
    """Qué hay guardado en la cara del "no ganó" de cada agente. Es la única
    lectura que usa esa cara sola: el one-hot la mete en un AND donde no
    recorta nada."""
    print("Figura de la cara negativa")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    g_min, g_max = load_global_stats()
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    decoder = load_decoder()
    clf = load_classifier()
    np.random.seed(SEED)

    instances = {c: np.array(json.loads(
        (MODELS_DIR / f"instance_latents_{c}.json").read_text()), dtype=np.float32)
        for c in CLASSES}
    centroids = np.stack([instances[c].mean(0) for c in CLASSES])

    def read(ham, cue):
        with contextlib.redirect_stdout(io.StringIO()):
            z_q, recognized, *_ = ham.recall_from_right(
                cue, weights=np.ones(K, dtype=float))
        if not recognized:
            return None, None, float("nan")
        z = dequantize_latent(z_q, g_min, g_max)
        with torch.no_grad():
            pred = int(clf(torch.tensor(z).unsqueeze(0).to(DEVICE)).argmax(1))
        d = np.sort(np.linalg.norm(centroids - z, axis=1))
        return z, AGENT_LIST[pred], float(d[0] / d[1])

    n_cols = 2 + n_draws
    fig, axes = plt.subplots(len(CLASSES), n_cols,
                             figsize=(2.05 * n_cols, 2.2 * len(CLASSES)))
    cols = (["ETH-80\n(real)", "cara «sí ganó»\n[nan..1..nan]"]
            + [f"cara «no ganó»\n[nan..0..nan] · {i+1}" for i in range(n_draws)])

    meta = []
    for ci, cls in enumerate(CLASSES):
        other = CLASSES[(ci + 1) % len(CLASSES)]
        nonspec = load_agent(other)
        ham = nonspec.mem_dir_R._ham

        panels = [np.asarray(Image.open(splits[cls]["train"][0])
                             .convert("RGB").resize((128, 128)),
                             dtype=np.float32) / 255.0]
        z_pos, cls_pos, sep_pos = read(ham, cue_face(ci, 1))
        panels.append(decode_image(z_pos, decoder) if z_pos is not None else None)
        neg_labels = []
        for _ in range(n_draws):
            z_neg, cls_neg, sep_neg = read(ham, cue_face(ci, 0))
            panels.append(decode_image(z_neg, decoder) if z_neg is not None else None)
            neg_labels.append((cls_neg, sep_neg))

        # estadística de la cara negativa sobre más sorteos
        preds, seps, devuelve_b = [], [], 0
        for _ in range(reps):
            _z, p, s = read(ham, cue_face(ci, 0))
            if p is None:
                continue
            preds.append(p); seps.append(s); devuelve_b += int(p == cls)
        dist = {p: preds.count(p) for p in sorted(set(preds))}

        for k, (ax, img) in enumerate(zip(axes[ci], panels)):
            if img is not None:
                ax.imshow(img)
            else:
                ax.set_facecolor("#ecf0f1")
                ax.text(0.5, 0.5, "rechazado", ha="center", va="center",
                        fontsize=9, color="#7f8c8d", transform=ax.transAxes)
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_edgecolor(DOMAIN_COLOR[cls] if k else "#888")
                s.set_linewidth(1.6 if k else 0.8)
            if ci == 0:
                ax.set_title(cols[k], fontsize=8.5, pad=6)
        axes[ci, 0].set_ylabel(cls.upper(), fontsize=10, fontweight="bold",
                               color=DOMAIN_COLOR[cls], labelpad=8)
        axes[ci, 1].set_xlabel(f"{cls_pos} · sep {sep_pos:.2f}", fontsize=7.5)
        for i, (p, s) in enumerate(neg_labels):
            axes[ci, 2 + i].set_xlabel(f"{p} · sep {s:.2f}", fontsize=7.5)

        meta.append({"clase": cls, "directorio_de": other,
                     "positivo": {"clase": cls_pos, "separacion": sep_pos},
                     "negativo": {"distribucion": dist,
                                  "devuelve_la_propia": devuelve_b,
                                  "separacion_media": float(np.mean(seps)) if seps else None,
                                  "sorteos": len(preds)}})
        del nonspec
        print(f"  {cls:>7}  positivo={cls_pos} (sep {sep_pos:.2f})   "
              f"negativo={dist}  devuelve {cls}: {devuelve_b}/{len(preds)}  "
              f"sep {np.mean(seps):.2f}")

    propio = sum(m["negativo"]["devuelve_la_propia"] for m in meta)
    sorteos = sum(m["negativo"]["sorteos"] for m in meta)
    fig.suptitle(
        "Qué hay en la cara del «no ganó»: el complemento — los otros dominios\n"
        f"el propio sale {propio}/{sorteos} sorteos ({propio/sorteos:.1%}), "
        f"contra {1/K:.1%} por azar", fontsize=12, y=0.997)
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    path = OUT_DIR / "fig4_cara_negativa.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    (OUT_DIR / "cara_negativa_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"  -> {path}")
    return path


# ---------- Parte B: barrido de fracción presenciada ----------

def load_visual_stream(g_min, g_max):
    """Latentes cuantizados del pool visual de la etapa 7, desde el caché de
    exp7 (evita volver a correr el encoder)."""
    if not LATENT_CACHE.exists():
        raise FileNotFoundError(
            f"No existe {LATENT_CACHE}. Corre run_experiment7_unified_dir.py "
            f"una vez para generar el caché de latentes.")
    cache = json.loads(LATENT_CACHE.read_text())
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    by_cls = {}
    for cls in CLASSES:
        paths = splits[cls]["train"][N_FILL:N_FILL + N_IMG_TRAIN]
        missing = [p for p in paths if p not in cache]
        if missing:
            raise KeyError(f"{len(missing)} latentes fuera del caché ({cls}).")
        by_cls[cls] = [quantize_latent_global(np.array(cache[p]), g_min, g_max,
                                              Q_LATENT) for p in paths]
    return [(by_cls[c][i], AGENT_LIST.index(c))
            for i in range(N_IMG_TRAIN) for c in CLASSES]


def sweep_witnessed_fraction():
    print("\nParte B — barrido de fracción presenciada")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    g_min, g_max = load_global_stats()
    clf = load_classifier()
    stream = load_visual_stream(g_min, g_max)
    print(f"  stream visual: {len(stream)} percepciones")

    instances = {c: np.array(json.loads(
        (MODELS_DIR / f"instance_latents_{c}.json").read_text()), dtype=np.float32)
        for c in CLASSES}
    centroids = np.stack([instances[c].mean(0) for c in CLASSES])

    def classify(z):
        with torch.no_grad():
            return int(clf(torch.tensor(z).unsqueeze(0).to(DEVICE)).argmax(1))

    rows = []
    t0 = time.time()
    for f in FRACTIONS:
        rng = np.random.RandomState(SEED)
        dirs = []
        with contextlib.redirect_stdout(io.StringIO()):
            dirs = [DirectoryMemory(P_LATENT, Q_LATENT, K) for _ in range(K)]
        for z_q, widx in stream:
            for ai in range(K):
                # el ganador siempre anota; los demás, solo si presenciaron
                if ai == widx or rng.random() < f:
                    dirs[ai].register(z_q, widx)
        counts = [int(d.agent_counts.sum()) for d in dirs]

        for ai in range(K):
            ham = dirs[ai]._ham
            for bi in range(K):
                ok = hit = 0
                ratios = []
                for _ in range(REPS):
                    z_q, recognized = recall_domain(ham, bi)
                    if not recognized:
                        continue
                    ok += 1
                    z = dequantize_latent(z_q, g_min, g_max)
                    hit += int(classify(z) == bi)
                    d = np.linalg.norm(centroids - z, axis=1)
                    ratios.append(float(d[bi] / np.delete(d, bi).min()))
                rows.append({
                    "fraccion": f, "agente": AGENT_LIST[ai],
                    "dominio": AGENT_LIST[bi], "propio": ai == bi,
                    "registros_directorio": counts[ai],
                    "reconocido": ok / REPS,
                    "acierto_clf": (hit / ok) if ok else float("nan"),
                    "ratio_centroide": (float(np.mean(ratios)) if ratios
                                        else float("nan")),
                })
        prop = [r for r in rows if r["fraccion"] == f and r["propio"]]
        aj = [r for r in rows if r["fraccion"] == f and not r["propio"]]
        print(f"  f={f:<5} registros~{int(np.mean(counts)):4d}  "
              f"propio: rec {np.mean([r['reconocido'] for r in prop]):.2f} "
              f"acc {safe_mean([r['acierto_clf'] for r in prop]):.2f}  |  "
              f"ajeno: rec {np.mean([r['reconocido'] for r in aj]):.2f} "
              f"acc {safe_mean([r['acierto_clf'] for r in aj]):.2f}  "
              f"({time.time()-t0:.0f}s)")

    import csv
    csv_path = OUT_DIR / "results_witnessed_fraction.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"  -> {csv_path}")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, key, title in (
            (axes[0], "reconocido", "Recuperación no vacía"),
            (axes[1], "acierto_clf", "Clasificada en el dominio pedido")):
        for propio, color, lab in ((True, "#27ae60", "dominio propio"),
                                   (False, "#c0392b", "dominio ajeno presenciado")):
            ys = [np.nanmean([r[key] for r in rows
                              if r["fraccion"] == f and r["propio"] == propio])
                  for f in FRACTIONS]
            ax.plot(FRACTIONS, ys, "o-", color=color, label=lab)
        ax.set_xlabel("fracción presenciada de los broadcasts ajenos")
        ax.set_ylim(-0.05, 1.05)
        ax.set_title(title)
        ax.grid(alpha=0.35)
    axes[0].set_ylabel("proporción")
    axes[0].legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig_path = OUT_DIR / "fig2_witnessed_fraction.png"
    fig.savefig(fig_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {fig_path}")
    return rows


def probes():
    """Mediciones numéricas del README: identidad de los directorios, controles
    del clasificador, fidelidad, superposición, las dos caras, identidades
    imposibles y curva de capacidad. Todo sobre las memorias entrenadas salvo
    la curva de capacidad, que construye directorios nuevos desde el pool de
    llenado (instance_latents) para poder variar el número de registros."""
    print("\nSondas numéricas")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    g_min, g_max = load_global_stats()
    clf = load_classifier()
    rng = np.random.RandomState(SEED)
    np.random.seed(SEED)
    out = {}

    instances = {c: np.array(json.loads(
        (MODELS_DIR / f"instance_latents_{c}.json").read_text()), dtype=np.float32)
        for c in CLASSES}
    centroids = np.stack([instances[c].mean(0) for c in CLASSES])

    def classify(z):
        with torch.no_grad():
            return int(clf(torch.tensor(z).unsqueeze(0).to(DEVICE)).argmax(1))

    # 1. los ocho directorios son la misma relación?
    rels, agents = {}, {}
    for a in AGENT_LIST:
        ag = load_agent(a)
        rels[a] = np.asarray(ag.mem_dir_R._ham._relation).copy()
        agents[a] = ag if a == "car" else None
        if a != "car":
            del ag
    ref = rels[AGENT_LIST[0]]
    out["directorios_identicos"] = bool(
        all(np.array_equal(ref, rels[a]) for a in AGENT_LIST))
    del rels
    car = agents["car"]
    ham_r, ham_l = car.mem_dir_R._ham, car.mem_dir._ham
    print(f"  directorios idénticos entre agentes: {out['directorios_identicos']}")

    # 1b. las tres condiciones de la comparación, sobre el mismo clasificador:
    # vivido (contenido del especialista), directorio propio y directorio ajeno.
    label_vecs = {c: json.loads((ROOT / f"label_vectors_{c}.json").read_text())
                  for c in CLASSES}
    tres = {"vivido": [0, 0], "dir_propio": [0, 0], "dir_ajeno": [0, 0]}
    for ai, a in enumerate(AGENT_LIST):
        ag = load_agent(a)
        for word in list(label_vecs[a])[:REPS]:
            v_q = quantize_binary(np.asarray(label_vecs[a][word]), M_LABEL)
            with contextlib.redirect_stdout(io.StringIO()):
                z_q, recognized, *_ = ag.mem_dom_H.recall_from_left(v_q)
            tres["vivido"][1] += 1
            if recognized:
                tres["vivido"][0] += int(
                    classify(dequantize_latent(z_q, g_min, g_max)) == ai)
        ham = ag.mem_dir_R._ham
        for bi in range(K):
            key = "dir_propio" if bi == ai else "dir_ajeno"
            for _ in range(REPS if bi == ai else 2):
                z_q, ok = recall_domain(ham, bi)
                tres[key][1] += 1
                if ok:
                    tres[key][0] += int(
                        classify(dequantize_latent(z_q, g_min, g_max)) == bi)
        del ag
    out["tres_condiciones"] = {k: {"aciertos": v[0], "de": v[1],
                                   "tasa": v[0] / v[1]} for k, v in tres.items()}
    print("  tres condiciones: " + "  ".join(
        f"{k} {v[0]}/{v[1]}" for k, v in tres.items()))

    # 2. control: qué clasifica el clasificador ante latentes sin origen
    counts = np.zeros(K, dtype=int)
    for _ in range(500):
        counts[classify(dequantize_latent(rng.randint(0, Q_LATENT, P_LATENT),
                                          g_min, g_max))] += 1
    out["control_latente_azar"] = dict(zip(AGENT_LIST, counts.tolist()))
    print(f"  control latentes al azar: {out['control_latente_azar']}")

    # 3. fidelidad: lo recuperado vs. las instancias reales
    fid = {}
    for bi, b in enumerate(AGENT_LIST):
        Z = instances[b]
        sub = Z[:200]
        D = np.linalg.norm(sub[:, None, :] - sub[None, :, :], axis=2)
        np.fill_diagonal(D, np.inf)
        dn, disp, zs = [], [], []
        for _ in range(REPS):
            z_q, ok = recall_domain(ham_r, bi)
            if not ok:
                continue
            z = dequantize_latent(z_q, g_min, g_max)
            zs.append(z)
            dn.append(float(np.linalg.norm(Z - z, axis=1).min()))
        disp = float(np.mean([np.linalg.norm(zs[i] - zs[j])
                              for i in range(len(zs))
                              for j in range(i + 1, len(zs))])) if len(zs) > 1 else float("nan")
        fid[b] = {"d_a_instancia_mas_cercana": float(np.mean(dn)),
                  "d_tipica_entre_instancias": float(D.min(axis=1).mean()),
                  "radio_de_clase": float(np.linalg.norm(Z - Z.mean(0), axis=1).mean()),
                  "dispersion_entre_sorteos": disp}
    out["fidelidad"] = fid
    print("  fidelidad medida")

    # 4. superposición en los dos directorios
    sup = {}
    for tag, ham, m in (("texto_300x16", ham_l, M_LABEL),
                        ("vision_64x32", ham_r, Q_LATENT)):
        per = {}
        for bi, b in enumerate(AGENT_LIST):
            with contextlib.redirect_stdout(io.StringIO()):
                proj = ham.project(ham.validate(onehot(bi), 1),
                                   np.ones(K, dtype=float), 1)
            adm = (proj > 0).sum(axis=1)
            per[b] = {"niveles_vivos_por_coordenada": float(adm.mean()),
                      "niveles": m, "coordenadas": int(ham.n),
                      "log10_patrones_admitidos": float(
                          np.sum(np.log10(np.maximum(adm, 1))))}
        sup[tag] = per
    out["superposicion"] = sup
    print("  superposición medida")

    # 5. masa acumulada en cada cara
    masa = {}
    for tag, mem, m in (("texto_300x16", car.mem_dir, M_LABEL),
                        ("vision_64x32", car.mem_dir_R, Q_LATENT)):
        ham = mem._ham
        rel = np.asarray(ham._relation)
        iota = np.asarray(ham._full_iota_relation)
        gano, nogano = float(rel[:, :, :m, 1].sum()), float(rel[:, :, :m, 0].sum())
        masa[tag] = {"registros": int(mem.agent_counts.sum()),
                     "masa_gano": gano, "masa_no_gano": nogano,
                     "razon": nogano / max(gano, 1.0),
                     "celdas_gano": float((iota[:, :, :m, 1] > 0).mean()),
                     "celdas_no_gano": float((iota[:, :, :m, 0] > 0).mean())}
    out["masa_por_cara"] = masa
    print(f"  masa no-ganó/ganó: "
          f"{ {k: round(v['razon'], 2) for k, v in masa.items()} }")

    # 6. las cuatro lecturas de la pista de identidad
    def niveles(ham, cue):
        with contextlib.redirect_stdout(io.StringIO()):
            proj = ham.project(ham.validate(np.asarray(cue, dtype=float), 1),
                               np.ones(K, dtype=float), 1)
        adm = (proj > 0).sum(axis=1)
        return float(adm.mean()), int(np.count_nonzero(adm == 0))

    bi = 0
    lecturas = {}
    for tag, cue in (("positivo_solo", cue_face(bi, 1)),
                     ("one_hot", onehot(bi).astype(float)),
                     ("negativo_solo", cue_face(bi, 0)),
                     ("negativo_de_los_ocho", np.zeros(K, dtype=float))):
        n, vac = niveles(ham_r, cue)
        lecturas[tag] = {"niveles_vivos_por_coordenada": n, "coordenadas_vacias": vac}
    out["lecturas_de_identidad"] = lecturas
    print(f"  lecturas: positivo {lecturas['positivo_solo']['niveles_vivos_por_coordenada']:.2f}"
          f"  one-hot {lecturas['one_hot']['niveles_vivos_por_coordenada']:.2f}"
          f"  negativo {lecturas['negativo_solo']['niveles_vivos_por_coordenada']:.2f}")

    # 7. de qué dominio viene cada coordenada (quimera)
    rel_i = np.asarray(ham_r._full_iota_relation)
    soporte = np.stack([rel_i[:, k, :Q_LATENT, 1] > 0 for k in range(K)])
    idx = np.arange(ham_r.n)
    quimera, sep_cara, propio_en_negativo, sorteos_neg = {}, {}, 0, 0
    for bi_, b in enumerate(AGENT_LIST):
        fila = {}
        for bit, tag in ((1, "positivo"), (0, "negativo")):
            cs, seps, propio = [], [], 0
            for _ in range(REPS * 2):
                with contextlib.redirect_stdout(io.StringIO()):
                    z_q, ok, *_ = ham_r.recall_from_right(
                        cue_face(bi_, bit), weights=np.ones(K, dtype=float))
                if not ok:
                    continue
                zi = np.asarray(z_q, dtype=int)
                cs.append(np.array([soporte[k, idx, zi].mean() for k in range(K)]))
                z = dequantize_latent(z_q, g_min, g_max)
                d = np.sort(np.linalg.norm(centroids - z, axis=1))
                seps.append(float(d[0] / d[1]))
                propio += int(classify(z) == bi_)
            C = np.stack(cs)
            fila[tag] = {"compat_max": float(C.max(axis=1).mean()),
                         "agentes_sobre_90pct": float((C > 0.9).sum(axis=1).mean()),
                         "separacion": float(np.mean(seps))}
            if bit == 0:
                propio_en_negativo += propio
                sorteos_neg += len(cs)
        quimera[b] = fila
    out["caras"] = quimera
    out["cobertura_soporte_por_agente"] = [float(soporte[k].mean()) for k in range(K)]
    out["propio_en_cara_negativa"] = {"aciertos": propio_en_negativo,
                                      "sorteos": sorteos_neg,
                                      "azar": 1.0 / K}
    print(f"  cara negativa devuelve el propio dominio "
          f"{propio_en_negativo}/{sorteos_neg} (azar {1/K:.1%})")

    # 8. identidades imposibles
    imposibles = {}
    casos = [("todo_ceros", np.zeros(K)), ("todo_unos", np.ones(K))]
    for pair in ((0, 1), (0, 4)):
        v = np.zeros(K); v[list(pair)] = 1
        casos.append((f"dos_hot_{AGENT_LIST[pair[0]]}_{AGENT_LIST[pair[1]]}", v))
    for t in range(3):
        v = rng.randint(0, 2, K).astype(float)
        casos.append((f"bits_azar_{''.join(str(int(x)) for x in v)}", v))
    for tag, cue in casos:
        n, vac = niveles(ham_r, cue)
        ok = 0
        for _ in range(REPS):
            with contextlib.redirect_stdout(io.StringIO()):
                _z, recognized, *_ = ham_r.recall_from_right(
                    cue, weights=np.ones(K, dtype=float))
            ok += int(recognized)
        imposibles[tag] = {"niveles_vivos_por_coordenada": n,
                           "coordenadas_vacias": vac,
                           "responde": ok, "de": REPS}
    out["identidades_imposibles"] = imposibles
    resumen = {k: f"{v['responde']}/{v['de']}" for k, v in imposibles.items()}
    print(f"  identidades imposibles: {resumen}")
    del car, agents

    # 9. curva de capacidad: directorios nuevos con N registros por agente
    qz = {c: [quantize_latent_global(z, g_min, g_max, Q_LATENT)
              for z in instances[c]] for c in CLASSES}
    capacidad = []
    for N in CAPACITY_SIZES:
        with contextlib.redirect_stdout(io.StringIO()):
            d = DirectoryMemory(P_LATENT, Q_LATENT, K)
        for ci, c in enumerate(CLASSES):
            for z_q in qz[c][:N]:
                d.register(z_q, ci)
        ham = d._ham
        adm, disp, dnn, seps, hit, tot = [], [], [], [], 0, 0
        for ci, c in enumerate(CLASSES):
            with contextlib.redirect_stdout(io.StringIO()):
                proj = ham.project(ham.validate(onehot(ci), 1),
                                   np.ones(K, dtype=float), 1)
            adm.append((proj > 0).sum(axis=1).mean())
            zs = []
            for _ in range(REPS):
                z_q, ok = recall_domain(ham, ci)
                if not ok:
                    continue
                z = dequantize_latent(z_q, g_min, g_max)
                zs.append(z); tot += 1
                hit += int(classify(z) == ci)
                dnn.append(float(np.linalg.norm(instances[c] - z, axis=1).min()))
                dd = np.sort(np.linalg.norm(centroids - z, axis=1))
                seps.append(float(dd[0] / dd[1]))
            if len(zs) > 1:
                disp.append(np.mean([np.linalg.norm(zs[i] - zs[j])
                                     for i in range(len(zs))
                                     for j in range(i + 1, len(zs))]))
        capacidad.append({"registros_por_agente": N,
                          "niveles_vivos_por_coordenada": float(np.mean(adm)),
                          "dispersion_entre_sorteos": float(np.mean(disp)),
                          "d_a_instancia_mas_cercana": float(np.mean(dnn)),
                          "acierto": f"{hit}/{tot}",
                          "separacion": float(np.mean(seps))})
        print(f"  capacidad N={N:>4}: {capacidad[-1]['niveles_vivos_por_coordenada']:5.2f}"
              f"/32  disp {capacidad[-1]['dispersion_entre_sorteos']:5.1f}  "
              f"d {capacidad[-1]['d_a_instancia_mas_cercana']:5.1f}  "
              f"acierto {capacidad[-1]['acierto']}", flush=True)
    out["capacidad"] = capacidad

    path = OUT_DIR / "sondas.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"  -> {path}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--figure", action="store_true")
    ap.add_argument("--draws", action="store_true")
    ap.add_argument("--negative", action="store_true")
    ap.add_argument("--probes", action="store_true")
    ap.add_argument("--sweep", action="store_true")
    args = ap.parse_args()
    run_all = not (args.figure or args.draws or args.negative
                   or args.probes or args.sweep)
    if args.figure or run_all:
        figure_recovered_object()
    if args.draws or run_all:
        figure_draws()
    if args.negative or run_all:
        figure_negative_face()
    if args.probes or run_all:
        probes()
    if args.sweep or run_all:
        sweep_witnessed_fraction()


if __name__ == "__main__":
    main()
