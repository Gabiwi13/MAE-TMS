"""
Experimento 23, segunda parte: la lista de la memoria contra predicción conformal.

Conformal partido (LAC) sobre el clasificador entrenado de cada modalidad:
puntaje 1 - p(verdad), calibrado con el split de validación de MedMNIST (no
usado antes en ningún paso). La cobertura objetivo es la que logra la memoria
en test (verdad dentro de S, contando como fallo las listas vacías); a esa
cobertura se compara el tamaño medio de lista, la adaptatividad (acierto del
argmax con lista de uno contra lista de varios) y la cobertura por clase.

Uso: python run_experiment23_conformal.py
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

OUT = ROOT / "results" / "experimento23"
CACHE_B = ROOT / "results" / "medico_balanceado" / "cache"


def softmax(L):
    L = L - L.max(1, keepdims=True)
    e = np.exp(L)
    return e / e.sum(1, keepdims=True)


def main():
    mem = json.loads((OUT / "filas.json").read_text())
    res, lines = {}, ["Exp23 b: lista de la memoria contra predicción conformal (LAC, calibrada en val) a igual cobertura."]
    for mod in demo.MODALITIES:
        names, _f, _a, test = e20.load_pool(CACHE_B, f"nivel2_{mod}")
        agents = demo.level2_agents(mod)
        enc = demo.Backbone(len(agents)).to(demo.DEV).eval()
        enc.load_state_dict(torch.load(CACHE_B / f"encoder_{mod}.pt", map_location=demo.DEV))
        # calibración: val de las mismas clases
        xv, yv = demo.data(demo.MODALITIES[mod])["val"]
        cal_idx, cal_y = [], []
        for k, (_n, sel) in enumerate(agents):
            ii = np.where(sel(yv))[0]
            cal_idx += ii.tolist()
            cal_y += [k] * len(ii)
        Zc = demo.latents(enc, [demo.to_pil(xv[i]) for i in cal_idx])
        with torch.no_grad():
            Pc = softmax(enc.head(torch.tensor(Zc, dtype=torch.float32).to(demo.DEV)).cpu().numpy())
            Zt = np.concatenate([test[n] for n in names])
            Pt = softmax(enc.head(torch.tensor(Zt, dtype=torch.float32).to(demo.DEV)).cpu().numpy())
        yt = np.concatenate([[k] * len(test[n]) for k, n in enumerate(names)])
        cal_scores = 1 - Pc[np.arange(len(cal_y)), np.array(cal_y)]
        rows = mem[mod]["filas"]
        assert [r["verdad"] for r in rows] == [names[k] for k in yt]
        S = [r["S"] for r in rows]
        mem_cov = float(np.mean([names[k] in s for k, s in zip(yt, S)]))
        mem_size = float(np.mean([len(s) for s in S]))
        # cuantil conformal para la cobertura de la memoria
        n = len(cal_scores)
        q = np.quantile(cal_scores, min(1.0, np.ceil((n + 1) * mem_cov) / n), method="higher")
        sets = [[names[j] for j in np.where(1 - p <= q)[0]] for p in Pt]
        cf_cov = float(np.mean([names[k] in s for k, s in zip(yt, sets)]))
        cf_size = float(np.mean([len(s) for s in sets]))
        argmax = [names[int(p.argmax())] for p in Pt]

        def adapt(setlist, pred):
            one = [i for i, s in enumerate(setlist) if len(s) == 1]
            many = [i for i, s in enumerate(setlist) if len(s) >= 2]
            empty = [i for i, s in enumerate(setlist) if len(s) == 0]
            acc = lambda ii: 100 * np.mean([pred[i] == names[yt[i]] for i in ii]) if ii else float("nan")
            return {"uno": (len(one), acc(one)), "varios": (len(many), acc(many)), "vacio": (len(empty), acc(empty))}

        mem_pred = [r["prot"] for r in rows]
        a_mem, a_cf = adapt(S, mem_pred), adapt(sets, argmax)
        per_cls = {c: (100 * np.mean([c in S[i] for i in np.where(yt == k)[0]]),
                       100 * np.mean([c in sets[i] for i in np.where(yt == k)[0]])) for k, c in enumerate(names)}
        res[mod] = {"cobertura_memoria": mem_cov, "tamano_memoria": mem_size, "cobertura_conformal": cf_cov,
                    "tamano_conformal": cf_size, "n_calibracion": n, "adapt_memoria": a_mem, "adapt_conformal": a_cf,
                    "por_clase": per_cls}
        lines.append(f"\n[{mod}] calibración n={n} · test n={len(yt)}")
        lines.append(f"  cobertura: memoria {100 * mem_cov:5.1f} con |S| medio {mem_size:.2f} · conformal {100 * cf_cov:5.1f} con |C| medio {cf_size:.2f}")
        for lab, a in (("memoria  ", a_mem), ("conformal", a_cf)):
            lines.append(f"  {lab}: lista de uno n={a['uno'][0]} acierto {a['uno'][1]:5.1f} · varios n={a['varios'][0]} acierto {a['varios'][1]:5.1f} · vacía n={a['vacio'][0]} acierto {a['vacio'][1]:5.1f}")
        lines.append("  cobertura por clase (memoria / conformal): " +
                     " · ".join(f"{c} {m:.0f}/{cf:.0f}" for c, (m, cf) in per_cls.items()))
    (OUT / "conformal.json").write_text(json.dumps(res, indent=1))
    text = "\n".join(lines)
    (OUT / "conformal_resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
