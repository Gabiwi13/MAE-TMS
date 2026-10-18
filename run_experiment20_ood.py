"""
Experimento 20, parte 3: ¿la memoria rechaza lo ajeno mejor que los detectores
estándar, a igual cobertura de lo propio?

La memoria tiene un único punto de operación: acepta una fracción A de las
imágenes de test propias. Cada detector estándar se fija para aceptar esa misma
fracción A de lo propio, y se compara cuánto rechaza de cada conjunto ajeno.
También se da su AUROC. Detectores sobre los mismos latentes:
  knn    similitud coseno media a los 5 vecinos del pozo de llenado
  maha   menos la distancia de Mahalanobis mínima a las clases (covarianza compartida)
  msp    probabilidad máxima de una regresión logística ajustada al pozo de llenado

Conjuntos ajenos:
  lejano   en el nivel 1: retinamnist (fondo de ojo), bloodmnist (sangre), octmnist (OCT)
  cercano  en el nivel 1: pneumoniamnist (tórax pediátrico de otro hospital)
  dentro   en el nivel 2 de tórax: hernia, que nunca se registró ni entró al encoder
           en el nivel 2 de órganos: leave-one-organ-out, cada órgano fuera por turno
           (el encoder de órganos sí vio el órgano; la memoria y los detectores no)
Memorias de la corrida balanceada.

Uso: python run_experiment20_ood.py
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

OUT = ROOT / "results" / "experimento20"
CACHE_B = ROOT / "results" / "medico_balanceado" / "cache"
OOD_DIR = ROOT / "data" / "medmnist_ood"
CACHE = OUT / "cache"            # fuera de git
OCT_MAX = 6000
SEED = 42


def ood_images(name, path_dir, cap=None):
    z = np.load(path_dir / f"{name}_128.npz", allow_pickle=False)
    x = np.concatenate([z[f"{s}_images"] for s in ("train", "val", "test")])
    idx = np.random.RandomState(SEED).permutation(len(x))[:cap]
    return [demo.to_pil(x[i]) for i in idx]


def cached_latents(key, enc, imgs_fn):
    p = CACHE / f"{key}.npy"
    if p.exists():
        return np.load(p)
    z = demo.latents(enc, imgs_fn())
    CACHE.mkdir(parents=True, exist_ok=True)
    np.save(p, z)
    return z


class Detectors:
    def __init__(self, fill, names):
        X = np.concatenate([fill[n][:, 0] for n in names]).astype(np.float64)
        y = np.concatenate([[k] * len(fill[n]) for k, n in enumerate(names)])
        self.Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
        self.mu = np.stack([X[y == k].mean(0) for k in range(len(names))])
        cov = sum(np.cov((X[y == k] - self.mu[k]).T) * (np.sum(y == k) - 1) for k in range(len(names))) / (len(X) - len(names))
        self.P = np.linalg.pinv(cov + 1e-6 * np.eye(cov.shape[0]))
        from sklearn.linear_model import LogisticRegression
        self.clf = LogisticRegression(max_iter=2000).fit(X, y)

    def scores(self, Z):
        Z = np.asarray(Z, dtype=np.float64)
        Zn = Z / np.linalg.norm(Z, axis=1, keepdims=True)
        knn = np.sort(Zn @ self.Xn.T, axis=1)[:, -5:].mean(1)
        d = np.stack([np.einsum("ij,jk,ik->i", Z - m, self.P, Z - m) for m in self.mu], 1)
        return {"knn": knn, "maha": -d.min(1), "msp": self.clf.predict_proba(Z).max(1)}


def auroc(pos, neg):
    """P(score propio > score ajeno)."""
    s = np.concatenate([pos, neg])
    r = np.argsort(np.argsort(s)) + 1
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def compare(level, det, z_in, entries_in, ood_sets):
    """Rechazo de la memoria y de cada detector a la cobertura propia de la memoria."""
    acc_in = np.mean([e20.route(level, z, k, "b1") is not None for z, k in zip(z_in, entries_in)])
    s_in = det.scores(z_in)
    out = {"aceptacion_propia_memoria": float(acc_in), "n_propias": int(len(z_in)), "ajenos": {}}
    for name, z_out in ood_sets.items():
        mem_rej = float(np.mean([e20.route(level, z, 0, "b1") is None for z in z_out]))
        s_out = det.scores(z_out)
        row = {"n": int(len(z_out)), "memoria": mem_rej}
        for k in s_in:
            thr = np.quantile(s_in[k], 1 - acc_in)          # acepta la fracción acc_in de lo propio
            row[k] = float(np.mean(s_out[k] < thr))
            row[f"{k}_auroc"] = auroc(s_in[k], s_out[k])
        out["ajenos"][name] = row
    return out


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    res = {}
    enc1 = demo.Backbone().to(demo.DEV).eval()
    enc1.load_state_dict(torch.load(CACHE_B / "encoder_nivel1.pt", map_location=demo.DEV))
    # nivel 1
    names, fill, pa, test = e20.load_pool(CACHE_B, "nivel1")
    L1 = demo.Level("nivel1", names, None, fill, pa)
    z_in = np.concatenate([test[n] for n in names])
    ent = np.concatenate([[k] * len(test[n]) for k, n in enumerate(names)])
    ood = {"retina": cached_latents("l1_retina", enc1, lambda: ood_images("retinamnist", demo.DATA)),
           "sangre": cached_latents("l1_sangre", enc1, lambda: ood_images("bloodmnist", OOD_DIR)),
           "oct": cached_latents("l1_oct", enc1, lambda: ood_images("octmnist", OOD_DIR, OCT_MAX)),
           "neumonia_otro_hospital": cached_latents("l1_pneumonia", enc1, lambda: ood_images("pneumoniamnist", demo.DATA))}
    res["nivel1"] = compare(L1, Detectors(fill, names), z_in, ent, ood)
    print(f"nivel 1 listo ({time.time() - t0:.0f} s)", flush=True)
    # tórax: hernia
    enc_rx =demo.Backbone(len(demo.level2_agents("rx_torax"))).to(demo.DEV).eval()
    enc_rx.load_state_dict(torch.load(CACHE_B / "encoder_rx_torax.pt", map_location=demo.DEV))
    names, fill, pa, test = e20.load_pool(CACHE_B, "nivel2_rx_torax")
    Lrx = demo.Level("nivel2_rx_torax", names, None, fill, pa)

    def hernia():
        out = []
        for s in ("train", "val", "test"):
            x, y = demo.data("chestmnist")[s]
            out += [demo.to_pil(x[i]) for i in np.where((y.sum(1) == 1) & (y[:, 13] == 1))[0]]
        return out
    z_in = np.concatenate([test[n] for n in names])
    ent = np.concatenate([[k] * len(test[n]) for k, n in enumerate(names)])
    res["torax_hernia"] = compare(Lrx, Detectors(fill, names), z_in, ent,
                                  {"hernia": cached_latents("rx_hernia", enc_rx, hernia)})
    print(f"hernia listo ({time.time() - t0:.0f} s)", flush=True)
    # órganos: leave-one-organ-out
    names_all, fill, pa, test = e20.load_pool(CACHE_B, "nivel2_tc_abdomen")
    res["organos_fuera"] = {}
    for held in names_all:
        names = [n for n in names_all if n != held]
        L = demo.Level("organos", names, None, {n: fill[n] for n in names}, {n: pa[n] for n in names})
        z_in = np.concatenate([test[n] for n in names])
        ent = np.concatenate([[k] * len(test[n]) for k, n in enumerate(names)])
        res["organos_fuera"][held] = compare(L, Detectors(fill, names), z_in, ent, {held: test[held]})
        print(f"  órgano fuera {held} ({time.time() - t0:.0f} s)", flush=True)
    (OUT / "ood_resultados.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    report(res)


def report(res):
    lines = ["Exp20 parte 3: rechazo de lo ajeno a igual aceptación de lo propio (memorias balanceadas).",
             "Cada detector se fija para aceptar la misma fracción de lo propio que la memoria; AUROC entre paréntesis."]

    def block(title, r):
        lines.append(f"\n[{title}] la memoria acepta {100 * r['aceptacion_propia_memoria']:.1f} % de {r['n_propias']} propias")
        for name, a in r["ajenos"].items():
            lines.append(f"  {name:<24} n={a['n']:>5}  rechazo: memoria {100 * a['memoria']:5.1f} · "
                         + " · ".join(f"{k} {100 * a[k]:5.1f} ({a[k + '_auroc']:.3f})" for k in ("knn", "maha", "msp")))

    block("nivel 1 · modalidad", res["nivel1"])
    block("tórax · hernia (nunca registrada)", res["torax_hernia"])
    lines.append("\n[órganos · leave-one-organ-out]")
    agg = {k: [] for k in ("memoria", "knn", "maha", "msp")}
    for held, r in res["organos_fuera"].items():
        a = r["ajenos"][held]
        for k in agg:
            agg[k].append(a[k])
        lines.append(f"  {held:<14} acepta propias {100 * r['aceptacion_propia_memoria']:5.1f} · rechazo: memoria {100 * a['memoria']:5.1f} · "
                     + " · ".join(f"{k} {100 * a[k]:5.1f}" for k in ("knn", "maha", "msp")))
    lines.append("  media: " + " · ".join(f"{k} {100 * np.mean(v):5.1f}" for k, v in agg.items()))
    text = "\n".join(lines)
    (OUT / "ood_resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
