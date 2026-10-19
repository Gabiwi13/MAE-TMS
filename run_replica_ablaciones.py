"""
Réplica (10 semillas) y ablaciones del diseño congelado de la etapa 2 (entrada por receptor,
R3 con xi = 1), en la flota de VisA y en una flota nueva de MedMNIST. Diseño en
propuesta_replica_ablaciones.md.

Lecturas: R3 (directorio MAE), TAB (tabla de conteos), PROPIO (solo el directorio propio),
GLOBAL (tasa global por módulo), central kNN y azar.

Uso:
  python run_replica_ablaciones.py --flota visa --semillas 0-4
  python run_replica_ablaciones.py --flota med --semillas 0-9
  python run_replica_ablaciones.py --report-only
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_etapa1_ruteo_dirigido as e1  # noqa: E402
import run_etapa2_evidencia as e2  # noqa: E402
import run_medico_demo as demo  # noqa: E402
import run_piloto_modulos as pm  # noqa: E402

OUT = ROOT / "results" / "replica_ablaciones"
CACHE = OUT / "cache"            # fuera de git
MED = Path("C:/Users/aq99l/Projects/MAE-TMS-medico")
MED_POOL = MED / "results/medico_balanceado/cache"
MODALITIES = ("rx_torax", "tc_abdomen", "dermatoscopia", "us_mama")
MED_MODULES = ("cabeza", "knn", "memoria")
N_MED = 600
XI = 1
READINGS = ("r3", "tab", "propio", "global", "central", "azar", "tab_cand")  # tab_cand: análisis posterior


# ---------- flotas ----------

def visa():
    Qs, C = pm.queries(), pm.cues()
    qs = [{"d": p, "cue": C[f"q_{p}"][j], "lab": int(Qs[p]["y"][j])} for p in pm.PIECES for j in range(len(Qs[p]["y"]))]
    corr = {}
    for v in "ABCD":
        corr[v] = np.array([int(Qs[q["d"]]["logits"][v][j].argmax()) == q["lab"]
                            for q, j in zip(qs, [j for p in pm.PIECES for j in range(len(Qs[p]["y"]))])])
    unk = np.concatenate([C[f"u_{u}"] for u in pm.UNKNOWN])
    return {"dominios": list(pm.PIECES), "consultas": qs, "correcto": corr, "llenado": {p: C[f"fill_{p}"] for p in pm.PIECES},
            "desconocidas": unk, "versiones": "ABCD"}


def med():
    filas = json.loads((MED / "results/medico_balanceado/filas.json").read_text(encoding="utf-8"))["nivel2"]
    p1 = np.load(MED_POOL / "pool_nivel1.npz")
    rng = np.random.RandomState(42)
    qs, corr = [], {m: [] for m in MED_MODULES}
    for mod in MODALITIES:
        p2 = np.load(MED_POOL / f"pool_nivel2_{mod}.npz")
        names = [k[5:] for k in p2.files if k.startswith("fill_")]
        pos = {int(t): i for i, t in enumerate(p1[f"testidx_{mod}"])}
        img = np.concatenate([p2[f"testidx_{n}"] for n in names])
        rows = filas[mod]
        assert len(rows) == len(img)
        sel = rng.permutation(len(rows))[:N_MED]
        for k in sel:
            r = rows[k]
            qs.append({"d": mod, "cue": p1[f"test_{mod}"][pos[int(img[k])]][None], "lab": r["verdad"]})
            corr["memoria"].append(r["destino"] == r["verdad"])
            corr["knn"].append(r["knn"] == r["verdad"])
            corr["cabeza"].append(r["cabeza"] == r["verdad"])
    path = CACHE / "retina_nivel1.npy"
    if not path.exists():
        enc = demo.Backbone().to(demo.DEV).eval()
        enc.load_state_dict(torch.load(MED_POOL / "encoder_nivel1.pt", map_location=demo.DEV))
        x = np.load(MED / "data/medmnist/retinamnist_128.npz")["test_images"]
        CACHE.mkdir(parents=True, exist_ok=True)
        np.save(path, demo.latents(enc, [demo.to_pil(a) for a in x]))
    return {"dominios": list(MODALITIES), "consultas": qs, "correcto": {m: np.array(v) for m, v in corr.items()},
            "llenado": {m: p1[f"fill_{m}"] for m in MODALITIES}, "desconocidas": np.load(path), "versiones": MED_MODULES}


# ---------- protocolo ----------

def run_seed(F, flota, seed):
    rng = np.random.RandomState(seed)
    qs, D = F["consultas"], F["dominios"]
    learn, ev = [], []
    for d in D:
        ii = rng.permutation([i for i, q in enumerate(qs) if q["d"] == d])
        h = len(ii) // 2
        learn += ii[:h].tolist()
        ev += ii[h:].tolist()
    if flota == "visa":
        lr = set(learn)
        weak = {d: min("BCD", key=lambda v: np.mean([F["correcto"][v][i] for i in lr if qs[i]["d"] == d])) for d in D}
        mods = [(d, v) for d in D for v in ("A", weak[d])]
    else:
        mods = [(d, m) for d in D for m in MED_MODULES]
    ok = lambda mi, qi: mods[mi][0] == qs[qi]["d"] and bool(F["correcto"][mods[mi][1]][qi])
    zs = np.concatenate([F["llenado"][d][:, 0] for d in D])
    lo, hi = zs.min(0), zs.max(0)
    g = (lo - pm.PAD * (hi - lo), hi + pm.PAD * (hi - lo))
    fleet = pm.Fleet(mods, F["llenado"], g)
    for i in range(fleet.n):
        fleet.activate(i)
    n = fleet.n
    att, suc = np.zeros((n, n)), np.zeros((n, n))
    att_g, suc_g = np.zeros(n), np.zeros(n)
    log = []
    for qi in rng.permutation(learn):
        cue = qs[qi]["cue"]
        cand = fleet.candidates(cue[0])
        if not cand:
            continue
        entry, w = cand[rng.randint(len(cand))], cand[rng.randint(len(cand))]
        o = ok(w, qi)
        fleet.register(cue, entry, w, o)
        for hld in {entry, w}:
            att[hld, w] += 1
            suc[hld, w] += o
        att_g[w] += 1
        suc_g[w] += o
        log.append((cue[0], w, o))
    X = np.array([x for x, _, _ in log])
    W = np.array([w for _, w, _ in log])
    S = np.array([o for *_, o in log], float)
    d2 = ((X[:, None] - X[None]) ** 2).sum(2)
    np.fill_diagonal(d2, np.inf)
    thr = np.quantile(np.sqrt(d2.min(1)), 0.99)

    def central(z):
        d = np.sqrt(((X - z) ** 2).sum(1))
        if d.min() > thr:
            return None
        nn = np.argsort(d)[:10]
        return int(max(set(W[nn].tolist()), key=lambda i: (S[nn][W[nn] == i].mean(), S[nn][W[nn] == i].sum())))

    def tab(z, entry):
        read = []
        for m in [entry] + fleet.known_by(entry):
            read.append(m)
            a = att[m] * fleet.active
            if (a > 0).any():
                return int(np.argmax(np.where(a > 0, suc[m] / np.maximum(a, 1), -1))), len(read), False
        return e2.content_fallback(fleet, z, read), len(read), True

    def propio(z, entry):
        v = fleet.q(z)
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            gaps = fleet.d_int[entry].support_gaps(v)
        if len(gaps) <= XI:
            den = e1.tol_proj(fleet.d_int[entry], v, gaps)
            num = e1.tol_proj(fleet.d_exi[entry], v, gaps)
            okk = (den > 0) & fleet.active
            if okk.any():
                return int(np.argmax(np.where(okk, num / np.maximum(den, 1e-12), -1))), 1, False
        return e2.content_fallback(fleet, z, [entry]), 1, True

    def tab_cand(z, entry, cand):
        """Post hoc: la tabla de conteos del recorrido, restringida a los candidatos del contenido."""
        if not cand:
            return None, 0, True
        read = []
        for m in [entry] + fleet.known_by(entry):
            read.append(m)
            a = np.array([att[m, i] if i in cand else 0 for i in range(n)])
            if (a > 0).any():
                return int(np.argmax(np.where(a > 0, suc[m] / np.maximum(a, 1), -1))), len(read), False
        return glob(cand), len(read), False

    def glob(cand):
        if not cand:
            return None
        known = [i for i in cand if att_g[i] > 0]
        return max(known, key=lambda i: (suc_g[i] / att_g[i], att_g[i])) if known else cand[0]

    rows = []
    act = np.where(fleet.active)[0]
    items = [(qi, qs[qi]["cue"][0]) for qi in ev] + [(None, z) for z in F["desconocidas"]]
    for qi, z in items:
        cand = fleet.candidates(z)
        entry = int(cand[rng.randint(len(cand))]) if cand else int(act[rng.randint(len(act))])
        r = {"q": qi}
        w, nr, c = e1.directed(fleet, z, entry, XI)
        r["r3"], r["r3_costo"] = w, nr + 24 * c
        w, nr, c = tab(z, entry)
        r["tab"], r["tab_costo"] = w, nr + 24 * c
        w, nr, c = propio(z, entry)
        r["propio"], r["propio_costo"] = w, nr + 24 * c
        w, nr, c = tab_cand(z, entry, cand)
        r["tab_cand"], r["tab_cand_costo"] = w, nr + 24 * c
        r["global"], r["central"] = glob(cand), central(z)
        r["azar"] = cand[rng.randint(len(cand))] if cand else None
        if qi is not None:
            for k in READINGS:
                r[f"{k}_ok"] = r[k] is not None and ok(r[k], qi)
        rows.append(r)
    acc_eval = {f"{d}/{v}": float(np.mean([F["correcto"][v][qi] for qi in ev if qs[qi]["d"] == d])) for d, v in mods}
    het = {}
    for d in D:
        labs = sorted({qs[qi]["lab"] for qi in ev if qs[qi]["d"] == d}, key=str)
        het[d] = {str(l): {v: float(np.mean([F["correcto"][v][qi] for qi in ev if qs[qi]["d"] == d and qs[qi]["lab"] == l]))
                           for dd, v in mods if dd == d} for l in labs}
    return {"semilla": seed, "modulos": [f"{d}/{v}" for d, v in mods], "acierto_eval": acc_eval, "dominio_de": [qs[qi]["d"] for qi in ev],
            "filas": [{k: (int(v) if isinstance(v, (np.integer,)) else v) for k, v in r.items()} for r in rows],
            "heterogeneidad": het, "transacciones": len(log)}


# ---------- reporte ----------

def boot(x, rng=np.random.RandomState(0)):
    x = np.asarray(x, float)
    b = [rng.choice(x, len(x)).mean() for _ in range(2000)]
    return x.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5)


def seed_metrics(R, flota):
    mods, rows, accm = R["modulos"], R["filas"], R["acierto_eval"]
    kn = [r for r in rows if r["q"] is not None]
    un = [r for r in rows if r["q"] is None]
    dom = R["dominio_de"]
    best_fixed = {d: max(a for m, a in accm.items() if m.startswith(d + "/")) for d in set(dom)}
    bf = np.mean([best_fixed[d] for d in dom])
    out = {}
    for k in READINGS + ("mejor_fijo",):
        if k == "mejor_fijo":
            out[k] = {"acierto": float(bf)}
            continue
        a = float(np.mean([r[f"{k}_ok"] for r in kn]))
        m = {"acierto": a, "perdida": float(bf - a), "abst_conocidas": float(np.mean([r[k] is None for r in kn])),
             "abst_desconocidas": float(np.mean([r[k] is None for r in un]))}
        if f"{k}_costo" in kn[0]:
            m["costo"] = float(np.mean([r[f"{k}_costo"] for r in kn]))
        fr = []
        for d in sorted(set(dom)):
            ms = [x for x in mods if x.startswith(d + "/")]
            acc = sorted(((accm[x], x) for x in ms), reverse=True)
            ws = [mods[r[k]] for r, dd in zip(kn, dom) if dd == d and r[k] is not None and mods[r[k]].startswith(d + "/")]
            if not ws:
                continue
            if flota == "visa" and acc[0][0] - acc[1][0] >= 0.05:
                fr.append(np.mean([w == acc[0][1] for w in ws]))
            if flota == "med" and acc[0][0] - acc[-1][0] >= 0.05:
                fr.append(np.mean([w == acc[-1][1] for w in ws]))
        m["al_mejor" if flota == "visa" else "al_peor"] = float(np.mean(fr)) if fr else float("nan")
        out[k] = m
    return out


def pct(x):
    return f"{100 * x:5.1f}"


def report():
    L = ["Réplica y ablaciones del diseño congelado (propuesta_replica_ablaciones.md). Media de semillas [IC 95 % por bootstrap]."]
    verdict = {}
    for flota in ("visa", "med"):
        files = sorted(CACHE.glob(f"{flota}_s*.json"))
        if not files:
            continue
        runs = [json.loads(f.read_text(encoding="utf-8")) for f in files]
        M = [seed_metrics(R, flota) for R in runs]
        pref = "al_mejor" if flota == "visa" else "al_peor"
        L.append(f"\n[flota {flota}] {len(runs)} semillas · transacciones de aprendizaje {np.mean([R['transacciones'] for R in runs]):.0f}")
        L.append(f"  mejor módulo fijo: acierto {pct(np.mean([m['mejor_fijo']['acierto'] for m in M]))}")
        L.append(f"  lectura    acierto · pérdida vs mejor fijo · abst. conocidas · abst. desconocidas · costo · {pref}")
        for k in READINGS:
            c = lambda key: boot([m[k][key] for m in M])
            a, p, ac, au, fr = c("acierto"), c("perdida"), c("abst_conocidas"), c("abst_desconocidas"), boot([m[k][pref] for m in M])
            cost = f"{np.mean([m[k]['costo'] for m in M]):5.1f}" if "costo" in M[0][k] else "   — "
            L.append(f"  {k:<8} {pct(a[0])} [{pct(a[1])}, {pct(a[2])}] · {pct(p[0])} · {pct(ac[0])} · {pct(au[0])} · {cost} · "
                     f"{pct(fr[0])} [{pct(fr[1])}, {pct(fr[2])}]")
        for comp in ("tab", "propio", "global"):
            sgn = 1 if flota == "visa" else -1
            dpref = boot([sgn * (m["r3"][pref] - m[comp][pref]) for m in M])
            dloss = boot([m[comp]["perdida"] - m["r3"]["perdida"] for m in M])
            L.append(f"  R3 − {comp}: ventaja en {pref} {pct(dpref[0])} [{pct(dpref[1])}, {pct(dpref[2])}] · ventaja en pérdida "
                     f"{pct(dloss[0])} [{pct(dloss[1])}, {pct(dloss[2])}]")
            verdict[f"{flota}_r3_vs_{comp}"] = {"pref": dpref, "perdida": dloss}
        dcen = boot([m["central"]["acierto"] - m["r3"]["acierto"] for m in M])
        L.append(f"  central − R3 en acierto: {pct(dcen[0])} [{pct(dcen[1])}, {pct(dcen[2])}]")
        verdict[f"{flota}_central_menos_r3"] = dcen
        verdict[f"{flota}_r3_{pref}"] = boot([m["r3"][pref] for m in M])
        # heterogeneidad de calidad dentro del dominio
        inv = []
        for R in runs:
            n_inv = 0
            for d, by in R["heterogeneidad"].items():
                ms = [x for x in R["modulos"] if x.startswith(d + "/")]
                best = max(ms, key=lambda x: R["acierto_eval"][x]).split("/")[1]
                if any(max(v, key=v.get) != best and max(v.values()) - v[best] >= 0.05 for v in by.values() if v):
                    n_inv += 1
            inv.append(n_inv)
        L.append(f"  dominios donde el mejor módulo global pierde por ≥ 5 puntos en alguna clase: {np.mean(inv):.1f} de {len(runs[0]['heterogeneidad'])} (media de semillas)")
    L.append(f"\n[criterio] {json.dumps(verdict)}")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--flota", choices=["visa", "med"])
    ap.add_argument("--semillas", default="0-9")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    if args.flota:
        a, b = map(int, args.semillas.split("-"))
        F = visa() if args.flota == "visa" else med()
        for s in range(a, b + 1):
            t0 = time.time()
            R = run_seed(F, args.flota, s)
            (CACHE / f"{args.flota}_s{s}.json").write_text(json.dumps(R, ensure_ascii=False))
            print(f"  {args.flota} semilla {s} lista ({time.time() - t0:.0f} s)", flush=True)
        return
    report()
    res = {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in sorted(CACHE.glob("*_s*.json"))}
    (OUT / "resultados.json").write_text(json.dumps({k: {"metricas": seed_metrics(v, k.split("_")[0]), "acierto_eval": v["acierto_eval"],
                                                         "heterogeneidad": v["heterogeneidad"]} for k, v in res.items()}, ensure_ascii=False))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
