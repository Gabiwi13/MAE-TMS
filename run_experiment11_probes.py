"""
Experimento 11 — sondas sobre los resultados ya corridos (sin recalls nuevos).

  A. Desglose por clase y brazo en cada corte: clase 1-NN, d_nn, compat.
  B. Figura de quimeras: para consultas con pista compartida donde M falla la
     clase, la imagen decodificada de M, la del especialista (T-oráculo) y la
     instancia real más cercana a la respuesta de M.

Uso:  python run_experiment11_probes.py [--cut 200] [--seed 42]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage6_interaction import CLASSES, MODELS_DIR
from run_experiment9_member_loss import load_decoder, decode_image
from run_experiment8_directory_recall import instance_image

OUT_DIR = ROOT / "results" / "experimento11"
RAW_DIR = OUT_DIR / "raw"
DATA_DIR = ROOT / "data" / "eth80"
ARMS = ("M", "T-oraculo", "T-protocolo")


def load_text_rows():
    rows = []
    for f in sorted(RAW_DIR.glob("s*_N*_c*.json")):
        rows += json.loads(f.read_text())["texto"]
    return rows


def per_class(rows):
    cuts = sorted({r["corte"] for r in rows})
    out = {}
    lines = ["# Experimento 11 — desglose por clase", "",
             "Clase 1-NN (%), d a la instancia real más cercana y compat máximo, por clase y brazo; "
             "solo respuestas. Semillas y sorteos agregados.", ""]
    for cut in cuts:
        lines += [f"## N = {cut}", "",
                  "| clase | " + " | ".join(f"{a}: clase / d_nn / compat" for a in ARMS) + " | n M |",
                  "|---|" + "---|" * (len(ARMS) + 1)]
        for cls in CLASSES:
            cells = []
            n_m = 0
            for arm in ARMS:
                sel = [r for r in rows if r["corte"] == cut and r["brazo"] == arm
                       and r["truth"] == cls and r.get("responde")]
                if arm == "M":
                    n_m = len(sel)
                if not sel:
                    cells.append("—")
                    continue
                nn = 100 * np.mean([r["nn_ok"] for r in sel])
                d = np.mean([r["d_nn_truth"] for r in sel])
                c = np.mean([r["compat_max"] for r in sel])
                out[f"{arm}|N={cut}|{cls}"] = {"nn_ok": nn, "d_nn": d, "compat": c, "n": len(sel)}
                cells.append(f"{nn:.1f} / {d:.1f} / {c:.2f}")
            lines.append(f"| {cls} | " + " | ".join(cells) + f" | {n_m} |")
        lines.append("")
        # errores de M: a qué clase se va
        conf = {}
        for r in rows:
            if r["corte"] == cut and r["brazo"] == "M" and r.get("responde") and not r["nn_ok"]:
                conf[(r["truth"], r["nn_cls"])] = conf.get((r["truth"], r["nn_cls"]), 0) + 1
        top = sorted(conf.items(), key=lambda x: -x[1])[:8]
        lines += ["Errores de clase de M más frecuentes (verdadera → vecino real):", ""]
        lines += [f"- {a} → {b}: {n}" for (a, b), n in top]
        lines.append("")
    (OUT_DIR / "por_clase.md").write_text("\n".join(lines), encoding="utf-8")
    (OUT_DIR / "por_clase.json").write_text(json.dumps(out, indent=1))
    print("\n".join(lines[:40]))


def chimera_figure(rows, cut, seed, n_show=6):
    decoder = load_decoder()
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    instances = {c: np.array(json.loads((MODELS_DIR / f"instance_latents_{c}.json").read_text()),
                             dtype=np.float32) for c in CLASSES}
    sel = [r for r in rows if r["corte"] == cut and r["semilla"] == seed and r["rep"] == 0
           and r["brazo"] == "M" and r.get("responde") and r.get("pista_compartida")
           and not r["nn_ok"]]
    seen, picks = set(), []
    for r in sel:
        if r["truth"] not in seen:
            seen.add(r["truth"]); picks.append(r)
    picks = picks[:n_show]
    if not picks:
        print("sin quimeras de M en esa semilla y corte")
        return
    oracle = {(r["query"]): r for r in rows if r["corte"] == cut and r["semilla"] == seed
              and r["rep"] == 0 and r["brazo"] == "T-oraculo" and r.get("responde")}
    cols = ["M (monolítica)", "instancia real más\ncercana a M", "T-oráculo\n(especialista)"]
    fig, axes = plt.subplots(len(picks), 3, figsize=(7.2, 2.3 * len(picks)))
    axes = np.atleast_2d(axes)
    meta = []
    for i, r in enumerate(picks):
        z_m = np.array(r["z"], dtype=np.float32)
        img_m = decode_image(z_m, decoder)
        d = np.linalg.norm(instances[r["nn_cls"]] - z_m, axis=1)
        j = int(np.argmin(d))
        img_nn = instance_image(r["nn_cls"], j, splits)
        o = oracle.get(r["query"])
        img_o = decode_image(np.array(o["z"], dtype=np.float32), decoder) if o else None
        for k, (ax, img) in enumerate(zip(axes[i], [img_m, img_nn, img_o])):
            if img is not None:
                ax.imshow(np.clip(img, 0, 1))
            ax.set_xticks([]); ax.set_yticks([])
            if i == 0:
                ax.set_title(cols[k], fontsize=9)
        axes[i, 0].set_ylabel(f"{r['truth']}\npista «{r['pista']}»", fontsize=8)
        axes[i, 1].set_xlabel(f"clase {r['nn_cls']} · compat {r['compat_max']:.2f}", fontsize=7.5)
        meta.append({"query": r["query"], "truth": r["truth"], "pista": r["pista"],
                     "M_nn_cls": r["nn_cls"], "M_compat": r["compat_max"], "M_d_nn": r["d_nn_truth"],
                     "oraculo_d_nn": o["d_nn_truth"] if o else None})
    fig.suptitle(f"Quimeras de la memoria única (N={cut}, semilla {seed}): la pista compartida "
                 "mezcla clases", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    path = OUT_DIR / "fig5_quimeras.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    (OUT_DIR / "fig5_quimeras_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    print(f"-> {path}")
    for m in meta:
        print(f"  {m['truth']:>7} «{m['query']}» pista {m['pista']} -> M {m['M_nn_cls']} "
              f"(compat {m['M_compat']:.2f}, d {m['M_d_nn']:.1f}); oráculo d {m['oraculo_d_nn']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cut", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    rows = load_text_rows()
    print(f"{len(rows)} filas de texto")
    per_class(rows)
    chimera_figure(rows, args.cut, args.seed)


if __name__ == "__main__":
    main()
