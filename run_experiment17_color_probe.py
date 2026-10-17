"""
Experimento 17, sonda de color: ¿el latente lleva el color del objeto de forma
que se comparta entre objetos distintos?

Leave-object-out con k vecinos: las 41 vistas de un objeto buscan sus vecinos
entre las vistas de los demás objetos (solo objetos con color claro en
colores_borrador.json) y votan un color. Dos pozos: la misma clase (lo que
vería un agente) y todas las clases. Tres representaciones: latente continuo,
latente cuantizado (lo que entra a la memoria) y píxeles 16x16 como referencia
de que el color está en la imagen. Línea base: el color más frecuente del pozo.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage5_fill import CLASSES, quantize_latent_global  # noqa: E402
from stage7_bidirectional import load_global_stats  # noqa: E402
from run_experiment17_specific_word import object_id, LAT_PATH, IDX_PATH, OUT_DIR  # noqa: E402

LABELS = OUT_DIR / "colores_borrador.json"
K = 5


BASE = {}


def mean_object_color(rgb):
    """Color medio de lo que no es fondo. El fondo de ETH-80 es azul; se toma
    como fondo lo que es claramente más azul que rojo y verde. Es una
    referencia de que la imagen distingue colores, no entra al sistema."""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    fg = ~((b > r + 0.08) & (b > g + 0.08))
    if fg.sum() < 20:
        return np.zeros(3, dtype=np.float32)
    return rgb[fg].mean(axis=0)


def load():
    arr = np.load(LAT_PATH, mmap_mode="r")
    index = json.loads(IDX_PATH.read_text())
    labels = json.loads(LABELS.read_text(encoding="utf-8"))
    g_min, g_max = (x.astype(np.float32) for x in load_global_stats())
    rows = []
    for ci, cls in enumerate(CLASSES):
        for i, p in enumerate(index[cls]):
            lab = labels[cls][str(object_id(p))]
            if not lab["claro"]:
                continue
            z = np.asarray(arr[ci, i, 0], dtype=np.float32)
            full = np.asarray(Image.open(p).convert("RGB").resize((64, 64)), dtype=np.float32) / 255
            img = np.asarray(Image.open(p).convert("RGB").resize((16, 16)), dtype=np.float32).ravel() / 255
            rows.append({"clase": cls, "objeto": f"{cls}{object_id(p)}", "color": lab["color"],
                         "cont": z, "cuant": quantize_latent_global(z, g_min, g_max, 32).astype(np.float32),
                         "pix": img, "color_medio": mean_object_color(full)})
    return rows


def probe(rows, rep, pool_of, pool_is_class):
    """Devuelve filas (objeto, color, predicho, base) por vista."""
    X = np.stack([r[rep] for r in rows])
    objs = np.array([r["objeto"] for r in rows])
    cols = np.array([r["color"] for r in rows])
    out = []
    for obj in sorted(set(objs)):
        q = np.where(objs == obj)[0]
        pool = np.array([j for j in pool_of(rows[q[0]]) if objs[j] != obj])
        if len(pool) == 0:
            continue
        vals = np.unique(cols[pool])
        base = BASE[rows[q[0]]["clase"]] if pool_is_class else BASE["_global"]
        if rep == "cuant":
            d = np.abs(X[q][:, None, :] - X[pool][None, :, :]).sum(-1)
        else:
            d = ((X[q][:, None, :] - X[pool][None, :, :]) ** 2).sum(-1)
        nn = np.argsort(d, axis=1)[:, :K]
        for qi, row_nn in zip(q, nn):
            v, c = np.unique(cols[pool][row_nn], return_counts=True)
            out.append((obj, cols[qi], v[np.argmax(c)], base, rows[qi]["clase"], len(vals)))
    return out


def summarize(res, name):
    if not res:
        return [f"  {name}: sin datos"]
    truth = np.array([r[1] for r in res])
    pred = np.array([r[2] for r in res])
    base = np.array([r[3] for r in res])
    bal = np.mean([np.mean(pred[truth == c] == c) for c in set(truth)])
    bal_b = 1 / len(set(truth))
    # por objeto: el color que más votan sus 41 vistas
    per_obj = {}
    for r in res:
        per_obj.setdefault(r[0], []).append(r)
    obj_ok = 0
    for o, rs in per_obj.items():
        v, c = np.unique([r[2] for r in rs], return_counts=True)
        obj_ok += int(v[np.argmax(c)] == rs[0][1])
    return [f"  {name:<28} vistas {np.mean(pred == truth) * 100:5.1f} % (base {np.mean(base == truth) * 100:5.1f} %)  "
            f"balanceada {bal * 100:5.1f} % (azar {bal_b * 100:5.1f} %)  "
            f"objetos {obj_ok}/{len(per_obj)}"]


def main():
    rows = load()
    n_obj = len({r["objeto"] for r in rows})
    by_cls = {}
    for j, r in enumerate(rows):
        by_cls.setdefault(r["clase"], []).append(j)
    # base: el color más frecuente, contado por objeto, sin excluir a nadie
    obj_col = {r["objeto"]: (r["clase"], r["color"]) for r in rows}
    for c in CLASSES + ["_global"]:
        cs = [col for cl, col in obj_col.values() if c == "_global" or cl == c]
        v, n = np.unique(cs, return_counts=True)
        BASE[c] = v[np.argmax(n)]
    multi = [c for c in CLASSES if len({rows[j]["color"] for j in by_cls[c]}) > 1]
    lines = [f"Sonda de color, leave-object-out, k={K}. Objetos con color claro: {n_obj} ({len(rows)} vistas).",
             f"Clases con más de un color (entran a 'intra-clase'): {', '.join(multi)}"]
    detail = {}
    for rep in ("cont", "cuant", "pix", "color_medio"):
        lines.append(f"\n[{ {'cont': 'latente continuo', 'cuant': 'latente cuantizado (memoria)', 'pix': 'píxeles 16x16 (referencia)', 'color_medio': 'color medio del objeto (referencia)'}[rep]}]")
        intra = probe([rows[j] for c in multi for j in by_cls[c]], rep,
                      lambda r, _rows=[rows[j] for c in multi for j in by_cls[c]]:
                      [k for k, x in enumerate(_rows) if x["clase"] == r["clase"]], True)
        glob = probe(rows, rep, lambda r: range(len(rows)), False)
        glob_sin_tomate = [x for x in glob if x[4] != "tomato"]
        lines += summarize(intra, "intra-clase")
        lines += summarize(glob, "global (todas las clases)")
        lines += summarize(glob_sin_tomate, "global, sin contar tomato")
        for c in multi:
            lines += summarize([x for x in intra if x[4] == c], f"  intra {c}")
        detail[rep] = {"intra": [list(map(str, x)) for x in intra], "global": [list(map(str, x)) for x in glob]}
    text = "\n".join(lines)
    (OUT_DIR / "sonda_color_resumen.txt").write_text(text, encoding="utf-8")
    (OUT_DIR / "sonda_color_filas.json").write_text(json.dumps(detail))
    print(text)


if __name__ == "__main__":
    main()
