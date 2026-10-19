"""
Experimento 24, prueba A: la lista de la memoria contra conformal por clase
(Mondrian), que garantiza cobertura en cada clase por construcción.

Puntaje 1 - p(clase) del clasificador entrenado; un cuantil por clase calibrado
con el split de validación. Se elige alfa para que la cobertura total en test
iguale a la de la memoria (exp23), y se compara tamaño de lista, cobertura de
la peor clase y cobertura por clase. También el conformal marginal de exp23.

Predicción: Mondrian iguala o supera la cobertura de las clases raras que la
memoria ganó a conformal marginal; queda por ver a qué tamaño de lista.

Uso: python run_experiment24_mondrian.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_medico_demo as demo  # noqa: E402
import run_experiment20_size_principle as e20  # noqa: E402

OUT = ROOT / "results" / "experimento24"
EXP23 = ROOT / "results" / "experimento23" / "filas.json"
CACHE_B = ROOT / "results" / "medico_balanceado" / "cache"


def softmax(L):
    L = L - L.max(1, keepdims=True)
    e = np.exp(L)
    return e / e.sum(1, keepdims=True)


def mondrian_sets(Pc, yc, Pt, alpha, K):
    q = np.ones(K)
    for k in range(K):
        s = np.sort(1 - Pc[yc == k, k])
        n = len(s)
        if n == 0:
            continue
        r = int(np.ceil((n + 1) * (1 - alpha))) - 1
        q[k] = s[min(r, n - 1)] if r < n else 1.0
    return (1 - Pt) <= q[None, :]


def marginal_sets(Pc, yc, Pt, alpha):
    s = np.sort(1 - Pc[np.arange(len(yc)), yc])
    n = len(s)
    r = int(np.ceil((n + 1) * (1 - alpha))) - 1
    q = s[min(r, n - 1)] if r < n else 1.0
    return (1 - Pt) <= q


def match_alpha(fn, target, yt):
    """Alfa (búsqueda binaria) cuya cobertura en test iguala a la de la memoria."""
    lo, hi = 0.0, 1.0
    for _ in range(40):
        a = (lo + hi) / 2
        cov = fn(a)[np.arange(len(yt)), yt].mean()
        lo, hi = (a, hi) if cov > target else (lo, a)
    return (lo + hi) / 2


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    mem = json.loads(EXP23.read_text())
    lines = ["Exp24 A: memoria contra conformal marginal y por clase (Mondrian), a igual cobertura total en test."]
    res = {}
    for mod in demo.MODALITIES:
        names, _f, _a, test = e20.load_pool(CACHE_B, f"nivel2_{mod}")
        K = len(names)
        agents = demo.level2_agents(mod)
        enc = demo.Backbone(K).to(demo.DEV).eval()
        enc.load_state_dict(torch.load(CACHE_B / f"encoder_{mod}.pt", map_location=demo.DEV))
        xv, yv = demo.data(demo.MODALITIES[mod])["val"]
        idx, yc = [], []
        for k, (_n, sel) in enumerate(agents):
            ii = np.where(sel(yv))[0]
            idx += ii.tolist()
            yc += [k] * len(ii)
        yc = np.array(yc)
        with torch.no_grad():
            Pc = softmax(enc.head(torch.tensor(demo.latents(enc, [demo.to_pil(xv[i]) for i in idx]),
                                               dtype=torch.float32).to(demo.DEV)).cpu().numpy())
            Pt = softmax(enc.head(torch.tensor(np.concatenate([test[n] for n in names]),
                                               dtype=torch.float32).to(demo.DEV)).cpu().numpy())
        yt = np.concatenate([[k] * len(test[n]) for k, n in enumerate(names)])
        S = np.array([[n in r["S"] for n in names] for r in mem[mod]["filas"]])
        target = S[np.arange(len(yt)), yt].mean()
        out = {"memoria": S}
        a_mar = match_alpha(lambda a: marginal_sets(Pc, yc, Pt, a), target, yt)
        a_mon = match_alpha(lambda a: mondrian_sets(Pc, yc, Pt, a, K), target, yt)
        out["conformal"] = marginal_sets(Pc, yc, Pt, a_mar)
        out["mondrian"] = mondrian_sets(Pc, yc, Pt, a_mon, K)
        cal_counts = np.bincount(yc, minlength=K)
        lines.append(f"\n[{mod}] test n={len(yt)} · calibración por clase {dict(zip(names, cal_counts.tolist()))}")
        res[mod] = {}
        for key, M in out.items():
            cov = M[np.arange(len(yt)), yt]
            per = [float(cov[yt == k].mean()) for k in range(K)]
            size = M.sum(1)
            res[mod][key] = {"cobertura": float(cov.mean()), "tamano": float(size.mean()),
                             "peor_clase": float(min(per)), "por_clase": dict(zip(names, per)),
                             "vacias": float((size == 0).mean())}
            r = res[mod][key]
            lines.append(f"  {key:<10} cobertura {100 * r['cobertura']:5.1f} · tamaño {r['tamano']:.2f} · "
                         f"peor clase {100 * r['peor_clase']:5.1f} · vacías {100 * r['vacias']:4.1f} %")
        lines.append("  por clase (memoria / marginal / Mondrian): " + " · ".join(
            f"{c} {100 * res[mod]['memoria']['por_clase'][c]:.0f}/{100 * res[mod]['conformal']['por_clase'][c]:.0f}/"
            f"{100 * res[mod]['mondrian']['por_clase'][c]:.0f}" for c in names))
    (OUT / "mondrian.json").write_text(json.dumps(res, indent=1))
    text = "\n".join(lines)
    (OUT / "mondrian_resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
