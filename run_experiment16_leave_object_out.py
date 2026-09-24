"""
Experimento 16: leave-one-object-out. Diseño en propuesta_exp16_leave_object_out.md.

En el pliegue k se reserva el objeto k de cada clase; el contenido (200 imágenes,
16 variantes) y la fase A (128 percepciones, 16 variantes) se construyen con los
otros nueve, y se evalúan sobre los mismos modelos las 41 vistas del objeto nuevo
y 41 vistas no usadas de los objetos conocidos.

Uso:
  python run_experiment16_leave_object_out.py --folds 1-10 --workers 2
  python run_experiment16_leave_object_out.py --report-only
"""
import argparse
import contextlib
import io
import json
import os
import re
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage5_fill import (CLASSES, N_FILL, DATA_DIR, IMG_TRANSFORM, FILL_VARIANTS,  # noqa: E402
                         augment_variants, build_label_sequence, quantize_latent_global)
from stage6_interaction import (Agent, AGENT_LIST, TME, register_transaction, route_transactive,  # noqa: E402
                                load_all_vectors, N as N_LAB, M_LABEL, P_LATENT, Q_LATENT)
from stage7_bidirectional import (recognize_gated_right, evoke_labels, XI_VISUAL, load_global_stats,  # noqa: E402
                                  load_encoder, latent_energy_threshold, latent_has_energy)
from associative_memory import DirectoryMemory, HomoAssociativeMemory  # noqa: E402
from hetero_memory import HeteroAssociativeMemory  # noqa: E402
from run_experiment11_monolithic import _fill, exclusive_vocab, image_strict, _ci, _rate, _fmt  # noqa: E402
from run_experiment13_augmentation import hetero_recognizes  # noqa: E402

OUT_DIR = Path(os.environ.get("EXP16_OUT", ROOT / "results" / "experimento16"))
RAW_DIR = OUT_DIR / "raw"
LAT_PATH = OUT_DIR / "latentes.npy"          # (8, 410, 16, 64) float32, fuera de git
IDX_PATH = OUT_DIR / "latentes_indice.json"  # rutas por clase en el orden del .npy
K = len(AGENT_LIST)
N_A = 128
N_OBJ, N_VIEWS = 10, 41
N_EVOKE = 3
SEED = 42
IMG = 128


def object_id(path):
    return int(re.match(r"^[a-z]+(\d+)-", Path(path).name).group(1))


def class_images(cls):
    return sorted(str(p) for p in (DATA_DIR / cls).glob("*.png"))


# ---------- latentes ----------

def encode_all():
    """Latentes de las 410 imágenes de cada clase con sus 16 variantes."""
    if LAT_PATH.exists() and IDX_PATH.exists():
        return
    import torch
    from PIL import Image
    encoder = load_encoder()
    dev = next(encoder.parameters()).device
    index, arr = {}, np.zeros((K, N_OBJ * N_VIEWS, FILL_VARIANTS, 64), dtype=np.float32)
    t0 = time.time()
    for ci, cls in enumerate(CLASSES):
        paths = class_images(cls)
        assert len(paths) == N_OBJ * N_VIEWS, (cls, len(paths))
        index[cls] = paths
        for i, p in enumerate(paths):
            img = Image.open(p).convert("RGB").resize((IMG, IMG))
            t = torch.stack([IMG_TRANSFORM(v) for v in augment_variants(img)]).to(dev)
            with torch.no_grad():
                arr[ci, i] = encoder(t).cpu().numpy()
        print(f"  {cls}: {len(paths)} imágenes × {FILL_VARIANTS} ({time.time()-t0:.0f}s)", flush=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    np.save(LAT_PATH, arr)
    IDX_PATH.write_text(json.dumps(index))


def load_latents():
    g_min, g_max = load_global_stats()
    g_min, g_max = g_min.astype(np.float32), g_max.astype(np.float32)
    arr = np.load(LAT_PATH)
    index = json.loads(IDX_PATH.read_text())
    return arr, index, g_min, g_max


def fold_split(index, k):
    """Por clase: pool barajado de 9 objetos y vistas del k-ésimo objeto en el
    orden de la clase (car numera sus objetos 1, 2, 3, 5, 6, 7, 9, 11, 12, 14)."""
    split = {}
    for cls in CLASSES:
        paths = index[cls]
        ids = sorted({object_id(p) for p in paths})
        held_id = ids[k - 1]
        held = [i for i, p in enumerate(paths) if object_id(p) == held_id]
        pool = [i for i, p in enumerate(paths) if object_id(p) != held_id]
        rng = np.random.RandomState(1000 + k)
        rng.shuffle(pool)
        split[cls] = {"objeto": held_id, "llenado": pool[:N_FILL], "fase_a": pool[N_FILL:N_FILL + N_A],
                      "conocido": pool[N_FILL + N_A:], "nuevo": held}
        assert len(split[cls]["nuevo"]) == N_VIEWS and len(split[cls]["conocido"]) == N_VIEWS
    return split


# ---------- un pliegue ----------

def run_fold(k):
    out = RAW_DIR / f"pliegue_{k:02d}.json"
    if out.exists():
        return str(out)
    t0 = time.time()
    arr, index, g_min, g_max = load_latents()
    split = fold_split(index, k)
    tau = latent_energy_threshold()

    def q(z):
        return quantize_latent_global(z, g_min, g_max, Q_LATENT)

    # contenido
    agents = {}
    for ci, cls in enumerate(CLASSES):
        seq = build_label_sequence(cls)
        with contextlib.redirect_stdout(io.StringIO()):
            mem_H = HeteroAssociativeMemory(N_LAB, M_LABEL, P_LATENT, Q_LATENT)
            mem_L = HomoAssociativeMemory(N_LAB, M_LABEL)
            mem_R = HomoAssociativeMemory(P_LATENT, Q_LATENT)
        for v_q in seq:
            mem_L.register(v_q)
        pool = [q(arr[ci, i, v]) for i in split[cls]["llenado"] for v in range(FILL_VARIANTS)]
        _fill(mem_H, mem_R, seq, pool)
        agents[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)
    t_fill = time.time() - t0

    # fase A
    tme = TME()
    rng = np.random.RandomState(SEED)
    form = {"registradas": 0, "rechazadas": 0, "sin_energia": 0, "acierto": 0}
    for j in range(N_A):
        for ci, cls in enumerate(CLASSES):
            i = split[cls]["fase_a"][j]
            if not latent_has_energy(arr[ci, i, 0], tau):
                form["sin_energia"] += 1
                continue
            z0 = q(arr[ci, i, 0])
            scores = {c: recognize_gated_right(agents[c], z0) for c in CLASSES}
            if sum(scores.values()) == 0:
                form["rechazadas"] += 1
                continue
            w = max(scores, key=scores.get)
            widx = AGENT_LIST.index(w)
            form["acierto"] += int(widx == ci)
            form["registradas"] += 1
            entry = AGENT_LIST[int(rng.randint(K))]
            with contextlib.redirect_stdout(io.StringIO()):
                for v in range(FILL_VARIANTS):
                    register_transaction(entry, widx, agents, tme, q(arr[ci, i, v]), "image")

    # evaluación
    vectors = load_all_vectors()
    all_vecs = {w: v for c in CLASSES for w, v in vectors[c].items()}
    excl = exclusive_vocab()
    rows = []
    for banco in ("nuevo", "conocido"):
        for ci, cls in enumerate(CLASSES):
            for n, i in enumerate(split[cls][banco]):
                z = arr[ci, i, 0]
                row = {"pliegue": k, "banco": banco, "clase": cls, "imagen": Path(index[cls][i]).name,
                       "objeto": object_id(index[cls][i])}
                if not latent_has_energy(z, tau):
                    row.update(sin_energia=True, contenido_acepta=False, responde=False, dir_acepta=False,
                               ruteo_ok=None, falso_ruteo=False, e2e=False, evocada=False, labels=[])
                    rows.append(row)
                    continue
                z_q = q(z)
                own = recognize_gated_right(agents[cls], z_q) > 0
                responde = own and hetero_recognizes(agents[cls], z_q)
                with contextlib.redirect_stdout(io.StringIO()):
                    d, _s, consulted, hops = route_transactive(CLASSES[(ci + 1) % K], agents, z_q,
                                                               modality="image", xi=XI_VISUAL)
                dest = CLASSES[d] if d >= 0 else None
                responde_dest = bool(dest) and hetero_recognizes(agents[dest], z_q)
                evocada = banco == "nuevo" and n < N_EVOKE
                labels = evoke_labels(agents[cls], z_q, all_vecs) if (evocada and responde) else []
                row.update(sin_energia=False, contenido_acepta=own, responde=responde, dir_acepta=d >= 0,
                           destino=dest, ruteo_ok=(d == ci) if d >= 0 else None, falso_ruteo=(d >= 0 and d != ci),
                           consultados=len(consulted), saltos=hops, e2e=bool(d == ci and responde_dest),
                           evocada=evocada, labels=labels)
                rows.append(row)
    for r in rows:
        r["truth"] = r["clase"]
    image_strict(rows, excl)

    meta = {"pliegue": k, "objeto_reservado": {c: split[c]["objeto"] for c in CLASSES}, "semilla": SEED,
            "formacion": form,
            "segundos_llenado": round(t_fill), "segundos": round(time.time() - t0)}
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"meta": meta, "filas": rows}, ensure_ascii=False))
    print(f"  pliegue {k}: {len(rows)} filas (llenado {t_fill/60:.0f} min, total {meta['segundos']/60:.0f} min)",
          flush=True)
    return str(out)


# ---------- reporte ----------

METRICS = ("contenido_acepta", "responde", "dir_acepta", "ruteo_ok", "falso_ruteo", "e2e",
           "hit_exclusivo", "otro_dominio")
COND = {"ruteo_ok": lambda r: r["dir_acepta"],
        "hit_exclusivo": lambda r: r["evocada"] and r["responde"],
        "otro_dominio": lambda r: r["evocada"] and r["responde"]}


def aggregate():
    raws = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(RAW_DIR.glob("pliegue_*.json"))]
    summary = {"pliegues": [r["meta"]["pliegue"] for r in raws], "bancos": {}, "por_clase": {}, "brecha": {},
               "formacion": {}, "falsos": {}}
    for banco in ("nuevo", "conocido"):
        per = {m: [] for m in METRICS}
        for raw in raws:
            rows = [r for r in raw["filas"] if r["banco"] == banco]
            for m in METRICS:
                per[m].append(_rate(rows, m, COND.get(m)))
        summary["bancos"][banco] = {m: _ci(v) for m, v in per.items()}
        for cls in CLASSES:
            per_c = {m: [] for m in ("contenido_acepta", "responde", "dir_acepta", "e2e", "falso_ruteo")}
            for raw in raws:
                rows = [r for r in raw["filas"] if r["banco"] == banco and r["clase"] == cls]
                for m in per_c:
                    per_c[m].append(_rate(rows, m, COND.get(m)))
            summary["por_clase"][f"{banco}|{cls}"] = {m: float(np.nanmean(v)) for m, v in per_c.items()}
    for m in ("contenido_acepta", "responde", "dir_acepta", "e2e"):
        diffs = []
        for raw in raws:
            a = _rate([r for r in raw["filas"] if r["banco"] == "conocido"], m)
            b = _rate([r for r in raw["filas"] if r["banco"] == "nuevo"], m)
            diffs.append(a - b)
        summary["brecha"][m] = _ci(diffs)
    summary["formacion"] = {k: float(np.mean([r["meta"]["formacion"][k] for r in raws]))
                            for k in ("registradas", "rechazadas", "sin_energia", "acierto")}
    fr = {}
    for raw in raws:
        for r in raw["filas"]:
            if r["banco"] == "nuevo" and r["falso_ruteo"]:
                key = f"{r['clase']} → {r['destino']}"
                fr[key] = fr.get(key, 0) + 1
    summary["falsos"] = dict(sorted(fr.items(), key=lambda kv: -kv[1]))
    # razón nuevo/conocido de punta a punta por pliegue (criterio §6)
    ratios = []
    for raw in raws:
        a = _rate([r for r in raw["filas"] if r["banco"] == "conocido"], "e2e")
        b = _rate([r for r in raw["filas"] if r["banco"] == "nuevo"], "e2e")
        ratios.append(b / a if a > 0 else float("nan"))
    summary["razon_e2e_nuevo_conocido"] = _ci(ratios)
    (OUT_DIR / "resumen.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    return summary


def write_report(summary):
    n = len(summary["pliegues"])
    L = ["# Experimento 16 — leave-one-object-out", "",
         f"{n} pliegues (objeto reservado {summary['pliegues']}), una semilla. Por pliegue: contenido con 200 imágenes "
         "de los 9 objetos restantes (16 variantes), fase A con 128 (16 variantes), umbral de energía. Bancos por "
         "pliegue: «nuevo» = 41 vistas del objeto reservado por clase (328); «conocido» = 41 vistas no usadas de los "
         "objetos que sí contribuyeron (328). Intervalos: bootstrap del 95 % sobre pliegues. Diseño en "
         "`propuesta_exp16_leave_object_out.md`.", "",
         "| banco | contenido acepta | responde | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | hit estricto | otro dominio |",
         "|---|---|---|---|---|---|---|---|---|"]
    for banco in ("conocido", "nuevo"):
        b = summary["bancos"][banco]
        L.append(f"| objeto {banco} | " + " | ".join(_fmt(b[m]) for m in METRICS) + " |")
    L += ["", "Brecha de memorización (conocido − nuevo, puntos, por pliegue):", "",
          "| medida | brecha |", "|---|---|"]
    for m, v in summary["brecha"].items():
        L.append(f"| {m} | {_fmt(v)} |")
    L += ["", f"Razón e2e nuevo / conocido por pliegue: {_fmt(summary['razon_e2e_nuevo_conocido'], False)} "
          "(criterio §6: sostenida si ≥ 0.75, refutada si < 0.5).", "",
          "## Por clase (media de pliegues, %)", "",
          "| clase | contenido acepta: conocido / nuevo | responde | directorio acepta | e2e | falso ruteo (nuevo) |",
          "|---|---|---|---|---|---|"]
    for cls in CLASSES:
        c = summary["por_clase"][f"conocido|{cls}"]; nw = summary["por_clase"][f"nuevo|{cls}"]
        L.append(f"| {cls} | {c['contenido_acepta']*100:.1f} / {nw['contenido_acepta']*100:.1f} | "
                 f"{c['responde']*100:.1f} / {nw['responde']*100:.1f} | {c['dir_acepta']*100:.1f} / {nw['dir_acepta']*100:.1f} | "
                 f"{c['e2e']*100:.1f} / {nw['e2e']*100:.1f} | {nw['falso_ruteo']*100:.1f} |")
    L += ["", "## Falsos ruteos sobre objetos nuevos (todos los pliegues)", "", "| par | imágenes |", "|---|---|"]
    for k, v in summary["falsos"].items():
        L.append(f"| {k} | {v} |")
    f = summary["formacion"]
    L += ["", f"Fase A (media por pliegue): registradas {f['registradas']:.0f}, rechazadas {f['rechazadas']:.1f}, "
          f"sin energía {f['sin_energia']:.1f}, acierto {f['acierto']:.0f} de las registradas.", "",
          "## Archivos", "- `raw/pliegue_<k>.json`: filas por imagen y banco", "- `resumen.json`, `fig1_nuevo_vs_conocido.png`",
          "- `latentes.npy`, `latentes_indice.json`: latentes de las 410 × 16 por clase (fuera de git; se regeneran)"]
    (OUT_DIR / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def make_figure(summary):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    ms = ("contenido_acepta", "responde", "dir_acepta", "e2e")
    x = np.arange(len(ms)); w = 0.38
    for ax_i, (ax, key) in enumerate(zip(axes, ("bancos", "clase"))):
        if key == "bancos":
            for j, (banco, col) in enumerate((("conocido", "#7f8c8d"), ("nuevo", "#c0392b"))):
                v = np.array([summary["bancos"][banco][m] for m in ms]) * 100
                ax.bar(x + (j - 0.5) * w, v[:, 0], w, color=col, label=f"objeto {banco}",
                       yerr=[v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], capsize=3)
            ax.set_xticks(x); ax.set_xticklabels(["contenido", "responde", "directorio", "punta a punta"])
            ax.set_ylabel("% de las 328 imágenes"); ax.legend()
        else:
            xc = np.arange(len(CLASSES))
            for j, (banco, col) in enumerate((("conocido", "#7f8c8d"), ("nuevo", "#c0392b"))):
                v = [summary["por_clase"][f"{banco}|{c}"]["e2e"] * 100 for c in CLASSES]
                ax.bar(xc + (j - 0.5) * w, v, w, color=col, label=f"objeto {banco}")
            ax.set_xticks(xc); ax.set_xticklabels(CLASSES, rotation=30); ax.set_ylabel("punta a punta (%)"); ax.legend()
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT_DIR / "fig1_nuevo_vs_conocido.png", dpi=150); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folds", default="1-10")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not args.report_only:
        a, b = args.folds.split("-") if "-" in args.folds else (args.folds, args.folds)
        folds = [k for k in range(int(a), int(b) + 1) if not (RAW_DIR / f"pliegue_{k:02d}.json").exists()]
        print("Codificando latentes...", flush=True)
        encode_all()
        print(f"{len(folds)} pliegues por correr ({args.workers} procesos)", flush=True)
        if args.workers > 1 and len(folds) > 1:
            with Pool(min(args.workers, len(folds))) as pool:
                list(pool.imap_unordered(run_fold, folds))
        else:
            for k in folds:
                run_fold(k)
    summary = aggregate()
    write_report(summary)
    make_figure(summary)
    print(f"Salidas -> {OUT_DIR}")


if __name__ == "__main__":
    main()
