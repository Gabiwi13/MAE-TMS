"""
Experimento 14: criterio de entrada previo a la memoria visual (energía mínima
del latente). Diseño en propuesta_exp14_energia_latente.md.

Un umbral tau sobre la norma del latente continuo, calibrado solo con los 1600
originales del llenado (mínimo con margen del 10 %), contra un banco de
entradas degeneradas generado de forma declarada y contra las imágenes reales
(llenado, fase A, test). Se comparan cuatro estadísticos con la misma regla.

Uso: python run_experiment14_latent_energy.py [--margen 0.1]
"""
import argparse
import contextlib
import io
import json
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage5_fill import CLASSES, N_FILL, MODELS_DIR, DATA_DIR, quantize_latent_global  # noqa: E402
from stage6_interaction import load_tme_and_agents, route_transactive  # noqa: E402
from stage7_bidirectional import (recognize_gated_right, load_global_stats, load_encoder,  # noqa: E402
                                  IMG_TRANSFORM, XI_VISUAL)

OUT_DIR = Path(os.environ.get("EXP14_OUT", ROOT / "results" / "experimento14"))
EXP13_TEST = ROOT / "results" / "experimento13" / "latentes_test.json"
V16_CACHE = ROOT / "cache" / "exp13" / "Vc16_N200.pkl"
IMG = 128
K = len(CLASSES)
STATS = ("norma", "desv_latente", "desv_pixeles", "niveles")
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255),
          (255, 128, 0), (128, 0, 255), (200, 30, 30), (30, 200, 30), (30, 30, 200), (63, 77, 150)]
BLUR_RADII = tuple(range(2, 34, 2))
CONTRASTS = (0.5, 0.4, 0.3, 0.2, 0.1, 0.05)
NOISE_SIGMAS = (1, 2, 4, 8, 16, 32)


def load_img(p):
    from PIL import Image
    return Image.open(p).convert("RGB").resize((IMG, IMG))


def encode(encoder, imgs):
    import torch
    dev = next(encoder.parameters()).device
    out = []
    for i in range(0, len(imgs), 64):
        t = torch.stack([IMG_TRANSFORM(im) for im in imgs[i:i + 64]]).to(dev)
        with torch.no_grad():
            out.append(encoder(t).cpu().numpy().astype(np.float32))
    return np.concatenate(out) if out else np.zeros((0, 64), dtype=np.float32)


def px_std(img):
    return float(np.asarray(img.convert("L"), dtype=float).std())


def degenerate_bank(refs):
    """Entradas degeneradas: (familia, nombre, imagen)."""
    from PIL import Image, ImageFilter, ImageEnhance
    bank = []
    for v in list(range(0, 256, 8)) + [255]:
        bank.append(("gris", f"gris {v}", Image.new("RGB", (IMG, IMG), (v, v, v))))
    for c in COLORS:
        bank.append(("color", f"color {c}", Image.new("RGB", (IMG, IMG), c)))
    for cls, ref in refs.items():
        for r in BLUR_RADII:
            bank.append(("desenfoque", f"{cls} desenfoque r={r}", ref.filter(ImageFilter.GaussianBlur(r))))
        for k in CONTRASTS:
            bank.append(("contraste", f"{cls} contraste {k}", ImageEnhance.Contrast(ref).enhance(k)))
    for s in NOISE_SIGMAS:
        rng = np.random.RandomState(1)
        bank.append(("gris con ruido", f"gris 127 + ruido sigma={s}",
                     Image.fromarray((127 + rng.randn(IMG, IMG, 3) * s).clip(0, 255).astype(np.uint8))))
    rng = np.random.RandomState(0)
    xs = np.linspace(-1, 1, IMG)
    bank += [("estructura", "gradiente horizontal",
              Image.fromarray(np.tile(np.linspace(0, 255, IMG), (IMG, 1)).astype(np.uint8)).convert("RGB")),
             ("estructura", "gradiente radial",
              Image.fromarray((255 * (1 - np.hypot(*np.meshgrid(xs, xs)) / 1.42)).clip(0, 255).astype(np.uint8)).convert("RGB")),
             ("estructura", "ruido uniforme", Image.fromarray((rng.rand(IMG, IMG, 3) * 255).astype(np.uint8)))]
    scram = (rng.rand(IMG, IMG, 3) * 255).astype(np.uint8).reshape(-1, 3)
    rng.shuffle(scram)
    bank.append(("estructura", "pixeles barajados", Image.fromarray(scram.reshape(IMG, IMG, 3))))
    return bank


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--margen", type=float, default=0.1)
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    import pickle

    encoder = load_encoder()
    g_min, g_max = load_global_stats()
    g_min, g_max = g_min.astype(np.float32), g_max.astype(np.float32)
    tme, agents = load_tme_and_agents()
    with open(V16_CACHE, "rb") as f:
        v16 = pickle.load(f)["specialists"]
    splits = json.loads((DATA_DIR / "splits.json").read_text())

    def q(z):
        return quantize_latent_global(np.asarray(z, dtype=np.float32), g_min, g_max, 32)

    def stats_of(z, img):
        zq = q(z)
        return {"norma": float(np.linalg.norm(z)), "desv_latente": float(np.std(z)),
                "desv_pixeles": px_std(img), "niveles": int(len(set(zq.tolist())))}

    def memory_of(z, entry):
        zq = q(z)
        acc = [c for c in CLASSES if recognize_gated_right(agents[c], zq) > 0]
        acc16 = [c for c in CLASSES if recognize_gated_right(v16[c], zq) > 0]
        with contextlib.redirect_stdout(io.StringIO()):
            d, *_ = route_transactive(entry, agents, zq, modality="image", xi=XI_VISUAL)
        return {"contenido": acc, "contenido_v16": acc16, "directorio": CLASSES[d] if d >= 0 else None}

    # ---- reales: llenado (latentes oficiales, variante 0), fase A y test ----
    print("Reales...", flush=True)
    fill_rows = []
    fill_lat = {}
    for cls in CLASSES:
        lat = np.asarray(json.loads((MODELS_DIR / f"instance_latents_{cls}.json").read_text()), dtype=np.float32)
        fill_lat[cls] = lat[0::4]
        for i, p in enumerate(splits[cls]["train"][:N_FILL]):
            fill_rows.append(dict(stats_of(fill_lat[cls][i], load_img(p)), clase=cls, imagen=Path(p).name))
    fase_a_rows = []
    for cls in CLASSES:
        paths = splits[cls]["train"][N_FILL:]
        imgs = [load_img(p) for p in paths]
        for p, im, z in zip(paths, imgs, encode(encoder, imgs)):
            fase_a_rows.append(dict(stats_of(z, im), clase=cls, imagen=Path(p).name))
    test_rows = []
    test_lat = json.loads(EXP13_TEST.read_text()) if EXP13_TEST.exists() else None
    for ci, cls in enumerate(CLASSES):
        paths = splits[cls]["test"]
        imgs = [load_img(p) for p in paths]
        if test_lat is not None:
            zs = np.asarray([test_lat[str(Path(p).as_posix().split("data/eth80/")[-1])] for p in paths],
                            dtype=np.float32)
        else:
            zs = encode(encoder, imgs)
        for p, im, z in zip(paths, imgs, zs):
            m = memory_of(z, CLASSES[(ci + 1) % K])
            test_rows.append(dict(stats_of(z, im), clase=cls, imagen=Path(p).name,
                                  contenido_propio=cls in m["contenido"], destino=m["directorio"]))

    # ---- calibración: mínimo del llenado con margen ----
    tau = {}
    for s in STATS:
        vals = np.array([r[s] for r in fill_rows])
        tau[s] = float(vals.min() * (1 - args.margen)) if s != "niveles" else float(vals.min() - 1)
    print("tau:", {k: round(v, 3) for k, v in tau.items()}, flush=True)

    # ---- banco degenerado ----
    print("Banco degenerado...", flush=True)
    refs = {cls: load_img(splits[cls]["test"][0]) for cls in CLASSES}
    bank = degenerate_bank(refs)
    zs = encode(encoder, [im for _, _, im in bank])
    deg_rows = []
    for (fam, name, im), z in zip(bank, zs):
        m = memory_of(z, CLASSES[0])
        row = dict(stats_of(z, im), familia=fam, nombre=name, **m)
        row["acepta"] = bool(m["contenido"] or m["directorio"])
        row["acepta_v16"] = bool(m["contenido_v16"])
        for s in STATS:
            row[f"pasa_{s}"] = row[s] >= tau[s]
        # P4: distancia al vecino real más cercano de la clase que acepta
        if m["contenido"]:
            c = m["contenido"][0]
            d = np.linalg.norm(fill_lat[c] - z, axis=1)
            row["vecino_clase"], row["d_vecino"] = c, float(d.min())
        deg_rows.append(row)

    # distancia típica entre vecinos dentro de cada clase (originales del llenado)
    intra = {}
    for cls in CLASSES:
        X = fill_lat[cls]
        D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
        np.fill_diagonal(D, np.inf)
        intra[cls] = float(np.median(D.min(axis=1)))

    # ---- métricas ----
    def rejected(rows, s):
        return [r for r in rows if r[s] < tau[s]]

    summary = {"tau": tau, "margen": args.margen, "intra_nn_mediana": intra,
               "reales": {}, "fuga": {}, "separacion": {}, "familias": {}}
    for s in STATS:
        summary["reales"][s] = {"llenado": len(rejected(fill_rows, s)), "fase_a": len(rejected(fase_a_rows, s)),
                                "test": len(rejected(test_rows, s)),
                                "test_detalle": [{"imagen": r["imagen"], "clase": r["clase"], "valor": r[s],
                                                  "contenido_propio": r["contenido_propio"], "destino": r["destino"]}
                                                 for r in rejected(test_rows, s)]}
        leak = [r for r in deg_rows if r["acepta"]]
        leak16 = [r for r in deg_rows if r["acepta_v16"]]
        summary["fuga"][s] = {"aceptadas_oficial": len(leak),
                              "pasan_oficial": sum(r[f"pasa_{s}"] for r in leak),
                              "aceptadas_v16": len(leak16),
                              "pasan_v16": sum(r[f"pasa_{s}"] for r in leak16)}
    fams = sorted({r["familia"] for r in deg_rows}, key=lambda f: [r["familia"] for r in deg_rows].index(f))
    for fam in fams:
        rows = [r for r in deg_rows if r["familia"] == fam]
        summary["familias"][fam] = {
            "n": len(rows), "acepta_oficial": sum(r["acepta"] for r in rows),
            "rutea_oficial": sum(r["directorio"] is not None for r in rows),
            "acepta_v16": sum(r["acepta_v16"] for r in rows),
            "fuga_tras_norma": sum(r["acepta"] and r["pasa_norma"] for r in rows),
            "fuga_v16_tras_norma": sum(r["acepta_v16"] and r["pasa_norma"] for r in rows)}

    # curva de tau para la norma
    taus = np.arange(6, 32.5, 0.5)
    curve = [{"tau": float(t),
              "test_rechazadas": int(sum(r["norma"] < t for r in test_rows)),
              "fase_a_rechazadas": int(sum(r["norma"] < t for r in fase_a_rows)),
              "fuga_oficial": int(sum(r["acepta"] and r["norma"] >= t for r in deg_rows)),
              "fuga_v16": int(sum(r["acepta_v16"] and r["norma"] >= t for r in deg_rows))} for t in taus]
    summary["curva_norma"] = curve

    (OUT_DIR / "resumen.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    (OUT_DIR / "banco_degenerado.json").write_text(json.dumps(deg_rows, indent=0, ensure_ascii=False), encoding="utf-8")
    (OUT_DIR / "reales.json").write_text(json.dumps({"llenado": fill_rows, "fase_a": fase_a_rows, "test": test_rows},
                                                     ensure_ascii=False), encoding="utf-8")
    write_report(summary, deg_rows, fill_rows, fase_a_rows, test_rows)
    make_figure(summary, deg_rows, test_rows)
    print(f"Salidas -> {OUT_DIR}")


def write_report(summary, deg_rows, fill_rows, fase_a_rows, test_rows):
    tau = summary["tau"]
    L = ["# Experimento 14 — criterio de energía mínima del latente", "",
         f"Calibración: mínimo sobre los 1600 originales del llenado con margen {summary['margen']:.0%} "
         "(niveles: mínimo menos uno). Banco degenerado generado como declara "
         "`propuesta_exp14_energia_latente.md` §4. Memoria oficial: agentes v5 (contenido y directorio, "
         "entrada `apple`); V16: contenido de exp13 con 16 variantes. Diseño y criterio en la propuesta.", "",
         "## Umbrales y costo sobre imágenes reales", "",
         "| estadístico | τ | mínimo llenado | rechaza llenado (1600) | rechaza fase A (1024) | rechaza test (656) |",
         "|---|---|---|---|---|---|"]
    for s in STATS:
        r = summary["reales"][s]
        L.append(f"| {s} | {tau[s]:.3f} | {min(x[s] for x in fill_rows):.3f} | {r['llenado']} | {r['fase_a']} | {r['test']} |")
    L += ["", "Imágenes de test rechazadas por la norma:", ""]
    for d in summary["reales"]["norma"]["test_detalle"]:
        L.append(f"- `{d['imagen']}` ({d['clase']}): norma {d['valor']:.2f}; contenido propio "
                 f"{'acepta' if d['contenido_propio'] else 'rechaza'}; directorio → {d['destino'] or 'rechazo'}")
    if not summary["reales"]["norma"]["test_detalle"]:
        L.append("- ninguna")
    L += ["", "## Fuga: entradas degeneradas que la memoria acepta y el criterio deja pasar", "",
          f"Banco: {len(deg_rows)} entradas. «Acepta»: algún especialista da soporte o el directorio rutea.", "",
          "| estadístico | acepta la memoria oficial | pasan el criterio | acepta el contenido V16 | pasan el criterio |",
          "|---|---|---|---|---|"]
    for s in STATS:
        f = summary["fuga"][s]
        L.append(f"| {s} | {f['aceptadas_oficial']} | {f['pasan_oficial']} | {f['aceptadas_v16']} | {f['pasan_v16']} |")
    L += ["", "## Por familia (norma)", "",
          "| familia | n | acepta oficial | rutea el directorio | acepta V16 | fuga oficial tras τ | fuga V16 tras τ |",
          "|---|---|---|---|---|---|---|"]
    for fam, f in summary["familias"].items():
        L.append(f"| {fam} | {f['n']} | {f['acepta_oficial']} | {f['rutea_oficial']} | {f['acepta_v16']} | "
                 f"{f['fuga_tras_norma']} | {f['fuga_v16_tras_norma']} |")
    L += ["", "## Entradas degeneradas aceptadas por la memoria oficial", "",
          "| entrada | norma | desv. latente | desv. píxeles | niveles | especialistas | directorio | d al vecino real (mediana intraclase) |",
          "|---|---|---|---|---|---|---|---|"]
    for r in deg_rows:
        if r["acepta"]:
            nn = (f"{r['d_vecino']:.1f} ({summary['intra_nn_mediana'][r['vecino_clase']]:.1f}, {r['vecino_clase']})"
                  if "d_vecino" in r else "—")
            L.append(f"| {r['nombre']} | {r['norma']:.2f} | {r['desv_latente']:.3f} | {r['desv_pixeles']:.2f} | "
                     f"{r['niveles']} | {','.join(r['contenido']) or '—'} | {r['directorio'] or '—'} | {nn} |")
    L += ["", "## Curva de τ (norma)", "", "| τ | test rechazadas | fase A rechazadas | fuga oficial | fuga V16 |", "|---|---|---|---|---|"]
    for c in summary["curva_norma"][::4]:
        L.append(f"| {c['tau']:.1f} | {c['test_rechazadas']} | {c['fase_a_rechazadas']} | {c['fuga_oficial']} | {c['fuga_v16']} |")
    L += ["", "## Archivos", "- `resumen.json`, `banco_degenerado.json` (fila por entrada), `reales.json` (estadísticos de llenado, fase A y test)",
          "- `fig1_norma_vs_aceptacion.png`"]
    (OUT_DIR / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def make_figure(summary, deg_rows, test_rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    ax = axes[0]
    ax.hist([r["norma"] for r in test_rows], bins=40, color="#7f8c8d", alpha=0.6, label="test real (656)")
    acc = [r["norma"] for r in deg_rows if r["acepta"]]
    rej = [r["norma"] for r in deg_rows if not r["acepta"]]
    ax.hist(rej, bins=40, color="#2980b9", alpha=0.6, label="degenerada, rechazada por la memoria")
    ax.hist(acc, bins=40, color="#c0392b", alpha=0.8, label="degenerada, aceptada")
    ax.axvline(summary["tau"]["norma"], color="k", ls="--", label=f"τ = {summary['tau']['norma']:.1f}")
    ax.set_xlabel("norma del latente"); ax.set_ylabel("entradas"); ax.legend(fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    ax = axes[1]
    c = summary["curva_norma"]
    ax.plot([x["tau"] for x in c], [x["fuga_oficial"] for x in c], color="#c0392b", label="fuga oficial")
    ax.plot([x["tau"] for x in c], [x["fuga_v16"] for x in c], color="#e67e22", ls="--", label="fuga V16")
    ax.plot([x["tau"] for x in c], [x["test_rechazadas"] for x in c], color="#7f8c8d", label="test reales rechazadas")
    ax.axvline(summary["tau"]["norma"], color="k", ls="--")
    ax.set_xlabel("τ sobre la norma"); ax.set_ylabel("entradas"); ax.legend(fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT_DIR / "fig1_norma_vs_aceptacion.png", dpi=150); plt.close(fig)


if __name__ == "__main__":
    main()
