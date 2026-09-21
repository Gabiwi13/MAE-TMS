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


COLOR = {"M": "#2a78d6", "T-oraculo": "#1baf7a", "T-protocolo": "#eb6834"}
NAME = {"M": "EHAM única", "T-oraculo": "transactivo, oráculo", "T-protocolo": "transactivo, protocolo"}


def comparison_figure():
    """Un panel con los cuatro ejes de la comparación: fidelidad y clase por N,
    coherencia con pista compartida, y cobertura contra precisión en imagen."""
    s = json.loads((OUT_DIR / "resumen.json").read_text())
    cuts = s["cortes"]
    top = cuts[-1]
    fig, ax = plt.subplots(2, 2, figsize=(11, 7.6))
    fig.patch.set_facecolor("#fcfcfb")
    for a in ax.flat:
        a.set_facecolor("#fcfcfb")
        a.spines[["top", "right"]].set_visible(False)
        a.spines[["left", "bottom"]].set_color("#c3c2b7")
        a.grid(axis="y", color="#e6e5e0", lw=0.8)
        a.set_axisbelow(True)
        a.tick_params(colors="#52514e", labelsize=9)

    def line(a, metric, ylabel, pct):
        f = 100 if pct else 1
        ends = {}
        for arm in ARMS:
            v = np.array([s["texto"][f"{arm}|N={c}"][metric] for c in cuts]) * f
            a.plot(cuts, v[:, 0], "-", color=COLOR[arm], lw=2, marker="o", ms=6, label=NAME[arm])
            a.fill_between(cuts, v[:, 1], v[:, 2], color=COLOR[arm], alpha=0.15, lw=0)
            ends[arm] = v[-1, 0]
        # etiquetas al final de cada línea, separadas si quedan muy juntas
        span = max(ends.values()) - min(ends.values()) or 1.0
        order = sorted(ARMS, key=lambda k: ends[k])
        ys = [ends[k] for k in order]
        gap = max(0.12 * span, 0.06 * (a.get_ylim()[1] - a.get_ylim()[0]) if a.get_ylim()[1] > a.get_ylim()[0] else 0)
        for i in range(1, len(ys)):
            if ys[i] - ys[i - 1] < gap:
                ys[i] = ys[i - 1] + gap
        for arm, y in zip(order, ys):
            a.annotate(NAME[arm], (cuts[-1], ends[arm]), xytext=(cuts[-1] + 6, y),
                       textcoords="data", fontsize=8, color="#52514e", va="center",
                       arrowprops=dict(arrowstyle="-", color="#c3c2b7", lw=0.8)
                       if abs(y - ends[arm]) > 1e-9 else None)
        a.set_xlabel("imágenes por clase (N)", color="#52514e", fontsize=9)
        a.set_ylabel(ylabel, color="#52514e", fontsize=9)
        a.set_xticks(cuts)
        a.set_xlim(cuts[0] - 10, cuts[-1] + 75)

    line(ax[0, 0], "d_nn_truth", "distancia a la instancia real más cercana", False)
    ax[0, 0].set_title("Fidelidad: menor es mejor, y la brecha crece con N", fontsize=10, loc="left")
    line(ax[0, 1], "nn_ok", "clase correcta, vecino real (%)", True)
    ax[0, 1].set_title("Clase: iguales desde N=100", fontsize=10, loc="left")
    ax[0, 1].set_ylim(94, 100.6)

    def bars(a, groups, labels, ylabel, title, ylim=None):
        x = np.arange(len(labels))
        w = 0.26
        for i, arm in enumerate(ARMS):
            vals = groups[arm]
            b = a.bar(x + (i - 1) * (w + 0.02), vals, w, color=COLOR[arm], label=NAME[arm],
                      edgecolor="#fcfcfb", lw=1)
            for r, v in zip(b, vals):
                a.text(r.get_x() + r.get_width() / 2, v + 1.2, f"{v:.0f}", ha="center",
                       fontsize=8, color="#52514e")
        a.set_xticks(x)
        a.set_xticklabels(labels, fontsize=9)
        a.set_ylabel(ylabel, color="#52514e", fontsize=9)
        a.set_title(title, fontsize=10, loc="left")
        if ylim:
            a.set_ylim(*ylim)

    t = {arm: s["texto"][f"{arm}|N={top}"] for arm in ARMS}
    bars(ax[1, 0],
         {arm: [100 * t[arm]["nn_ok_pista_compartida"][0], 100 * t[arm]["compat_max_pista_compartida"][0],
                100 * t[arm]["nn_ok"][0]] for arm in ARMS},
         ["clase correcta,\npista compartida", "coordenadas de\nuna sola clase", "clase correcta,\ntodo el banco"],
         "%", f"Coherencia (N={top}): la pista compartida mezcla clases en la EHAM única", (0, 112))

    im = {arm: s["imagen"].get(f"{arm}|N={top}") for arm in ARMS}
    if all(im.values()):
        prec = {arm: 100 * im[arm]["dominio_ok"][0] / max(im[arm]["responde"][0], 1e-9) for arm in ARMS}
        bars(ax[1, 1],
             {arm: [100 * im[arm]["responde"][0], prec[arm], 100 * im[arm]["otro_dominio"][0]] for arm in ARMS},
             ["responde\n(cobertura)", "dominio correcto\nsi responde", "dominio de\notra clase"],
             "% de imágenes de test", f"Imagen → texto (N={top}): cobertura contra precisión", (0, 112))
    else:
        ax[1, 1].set_visible(False)

    handles = [plt.Line2D([], [], color=COLOR[a], lw=6, label=NAME[a]) for a in ARMS]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=9,
               bbox_to_anchor=(0.5, -0.005))
    fig.suptitle("Una EHAM con las ocho clases contra el sistema transactivo: mismo contenido, mismo sustrato",
                 fontsize=12, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0.04, 1, 0.96])
    path = OUT_DIR / "fig6_comparacion.png"
    fig.savefig(path, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"-> {path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cut", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--only-figure", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    comparison_figure()
    if args.only_figure:
        return
    rows = load_text_rows()
    print(f"{len(rows)} filas de texto")
    per_class(rows)
    chimera_figure(rows, args.cut, args.seed)


if __name__ == "__main__":
    main()
