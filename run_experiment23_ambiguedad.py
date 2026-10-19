"""
Experimento 23: la ambigüedad como respuesta. Memorias de la corrida balanceada.

Para cada imagen, el conjunto S de especialistas cuya memoria de contenido la
reconoce (contención en las 64 coordenadas), ordenado por el principio de
tamaño de esa memoria. Tres grupos: desconocido (|S| = 0), claro (|S| = 1) y
ambiguo (|S| >= 2). Secundario: el conjunto que da el directorio (agentes con
soporte en los directorios del círculo, como en route_transactive).

Comparación a igual tamaño, imagen por imagen: si la memoria da k candidatos,
kNN (votos de los 25 vecinos del llenado) y la cabeza entrenada dan su top-k.

Placas de tórax con >= 2 hallazgos (de los 13 con agente): ¿S contiene a los
presentes?

Predicciones fijadas antes de correr:
  1. El argmax del protocolo falla mucho más en el grupo ambiguo que en el claro.
  2. Tórax: conjuntos grandes; órganos: chicos.
  3. En placas con varios hallazgos, S contiene a dos o más de los presentes
     más seguido que un conjunto al azar del mismo tamaño.

Uso: python run_experiment23_ambiguedad.py
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_medico_demo as demo  # noqa: E402
import run_experiment20_size_principle as e20  # noqa: E402

OUT = ROOT / "results" / "experimento23"
CACHE_B = ROOT / "results" / "medico_balanceado" / "cache"
SEED = 42


def content_sets(level, z):
    """(S ordenado por principio de tamaño, conjunto del directorio)."""
    zq = level.q(z)
    cand = []
    for n in level.names:
        rel = level.agents[n].mem_dom_R
        w = rel.recog_weights(zq)
        if np.count_nonzero(w == 0) == 0:
            cand.append((n, -float(np.sum(np.log(np.maximum(_support_sizes(rel), 1))))))
    s = [n for n, _ in sorted(cand, key=lambda x: -x[1])]
    d = []
    for n in level.names:
        sc = e20.size_scores(level.agents[n].mem_dir_R, zq)
        d += [level.names[i] for i in np.where(np.isfinite(sc))[0]]
    return s, sorted(set(d))


def _support_sizes(homo):
    """|soporte_i| de una memoria homo: niveles con peso > 0 en cada coordenada.
    Se guarda en la propia memoria: un id() puede reusarse al liberar objetos."""
    if not hasattr(homo, "_soporte_tamano"):
        cnt = np.zeros(64)
        for k in range(32):
            cnt += homo.recog_weights(np.full(64, k)) > 0
        homo._soporte_tamano = cnt
    return homo._soporte_tamano


def topk(scores_row, names, k):
    return [names[i] for i in np.argsort(-scores_row)[:k]]


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    res = {}
    for mod in demo.MODALITIES:
        tag = f"nivel2_{mod}"
        names, fill, pa, test = e20.load_pool(CACHE_B, tag)
        level = demo.Level(tag, names, None, fill, pa)
        enc = demo.Backbone(len(demo.level2_agents(mod))).to(demo.DEV).eval()
        enc.load_state_dict(torch.load(CACHE_B / f"encoder_{mod}.pt", map_location=demo.DEV))
        X = np.concatenate([fill[n][:, 0] for n in names])
        Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
        y = np.concatenate([[k] * len(fill[n]) for k, n in enumerate(names)])

        def knn_scores(Z):
            Zn = Z / np.linalg.norm(Z, axis=1, keepdims=True)
            nn = np.argsort(-(Zn @ Xn.T), axis=1)[:, :25]
            return np.stack([np.bincount(y[r], minlength=len(names)) for r in nn]).astype(float)

        def head_scores(Z):
            with torch.no_grad():
                return enc.head(torch.tensor(Z, dtype=torch.float32).to(demo.DEV)).cpu().numpy()

        rows = []
        for k, n in enumerate(names):
            Z = test[n]
            ks, hs = knn_scores(Z), head_scores(Z)
            for i, z in enumerate(Z):
                s, dset = content_sets(level, z)
                kk = max(len(s), 1)
                rows.append({"verdad": n, "S": s, "dir": dset, "prot": level.route(z, k)[0],
                             "knn_k": topk(ks[i], names, kk), "head_k": topk(hs[i], names, kk)})
        entry = {"nombres": names, "filas": rows}
        if mod == "rx_torax":
            entry["multi"] = multi_findings(level, enc, names)
        res[mod] = entry
        print(f"  {mod} ({time.time() - t0:.0f} s)", flush=True)
    (OUT / "filas.json").write_text(json.dumps(res, ensure_ascii=False))
    report(res)


def multi_findings(level, enc, names):
    """Placas de test con >= 2 de los hallazgos que tienen agente."""
    x, ylab = demo.data("chestmnist")["test"]
    col = {f: demo.CHEST.index(f) for f in names if f in demo.CHEST}
    cols = list(col.values())
    idx = np.where(ylab[:, cols].sum(1) >= 2)[0]
    Z = demo.latents(enc, [demo.to_pil(x[i]) for i in idx])
    rng = np.random.RandomState(SEED)
    out = []
    with torch.no_grad():
        H = enc.head(torch.tensor(Z, dtype=torch.float32).to(demo.DEV)).cpu().numpy()
    for i, z in zip(idx, range(len(Z))):
        present = [f for f, c in col.items() if ylab[i, c] == 1]
        s, _ = content_sets(level, Z[z])
        k = len(s)
        rand = list(rng.choice(names, size=k, replace=False)) if k else []
        out.append({"presentes": present, "S": s, "azar": rand, "head_k": topk(H[z], names, max(k, 1))})
    return out


def report(res):
    lines = ["Exp23: la ambigüedad como respuesta (memorias balanceadas). S = especialistas cuya memoria de contenido reconoce la imagen."]
    for mod, d in res.items():
        rows = d["filas"]
        n = len(rows)
        g = {"desconocido": [r for r in rows if len(r["S"]) == 0], "claro": [r for r in rows if len(r["S"]) == 1],
             "ambiguo": [r for r in rows if len(r["S"]) >= 2]}
        sizes = [len(r["S"]) for r in rows]
        cov = lambda key, rs: 100 * np.mean([r["verdad"] in r[key] for r in rs]) if rs else float("nan")
        lines.append(f"\n[{mod}] n={n} · |S| medio {np.mean(sizes):.2f} (de {len(d['nombres'])}) · "
                     + " · ".join(f"{k} {100 * len(v) / n:.1f} %" for k, v in g.items()))
        lines.append(f"  cobertura (verdad dentro de la lista), imágenes con |S|>=1: memoria {cov('S', [r for r in rows if r['S']]):.1f} · "
                     f"kNN top-|S| {cov('knn_k', [r for r in rows if r['S']]):.1f} · clasificador top-|S| {cov('head_k', [r for r in rows if r['S']]):.1f}")
        for k, v in g.items():
            if v:
                acc = 100 * np.mean([r["prot"] == r["verdad"] for r in v])
                lines.append(f"  {k:<11} n={len(v):>5}  acierto del protocolo {acc:5.1f} · verdad en S {cov('S', v):5.1f} · |S| medio {np.mean([len(r['S']) for r in v]):.2f}")
        dsz = [len(r["dir"]) for r in rows]
        lines.append(f"  conjunto del directorio: tamaño medio {np.mean(dsz):.2f} · verdad dentro {100 * np.mean([r['verdad'] in r['dir'] for r in rows]):.1f} %")
        if "multi" in d:
            m = d["multi"]
            def frac(key, need):
                return 100 * np.mean([len(set(r["presentes"]) & set(r[key])) >= need for r in m])
            lines.append(f"  placas con >= 2 hallazgos: n={len(m)} · |S| medio {np.mean([len(r['S']) for r in m]):.2f}")
            for need in (1, 2):
                lines.append(f"    contiene >= {need} presentes: memoria {frac('S', need):5.1f} · azar mismo tamaño {frac('azar', need):5.1f} · clasificador top-|S| {frac('head_k', need):5.1f}")
    text = "\n".join(lines)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
