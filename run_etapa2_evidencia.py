"""
Etapa 2: acumular evidencia hasta que la decisión sea clara (R4) y entradas por receptor.
Diseño en propuesta_etapa2_evidencia.md.

Cuentas efectivas por módulo, leídas de la memoria: proyección / (coordenadas definidas x 16).
R4 lee directorios uno por uno y para cuando el intervalo de Wilson del líder ya no se cruza
con el de nadie. Modos de entrada: al azar (la del piloto) y por receptor (un módulo cuyo
contenido contiene la consulta).

Uso: python run_etapa2_evidencia.py [--report-only]
"""
import argparse
import contextlib
import io
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_etapa1_ruteo_dirigido as e1  # noqa: E402
import run_piloto_modulos as pm  # noqa: E402

OUT = ROOT / "results" / "etapa2_evidencia"
ZS = (1.0, 1.96)
XI = 1


def wilson(s, n, z):
    p = np.clip(s / np.maximum(n, 1e-12), 0, 1)
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, c - h, c + h


def content_fallback(fleet, z, read):
    cand = fleet.candidates(z)
    if not cand:
        return None
    succ = sum((fleet.d_exi[m]._counts for m in read), np.zeros(fleet.n)).astype(float)
    att = sum((fleet.d_int[m]._counts for m in read), np.zeros(fleet.n)).astype(float)
    known = [i for i in cand if att[i] > 0]
    if known:
        return max(known, key=lambda i: (succ[i] / att[i], att[i]))
    w = [float(fleet.content[fleet.mods[i][0]].recog_weights(fleet.q(z)).mean()) for i in cand]
    return cand[int(np.argmax(w))]


def accumulate(fleet, z, entry, zval):
    """R4. Devuelve (módulo o None, directorios leídos, usó contenido)."""
    v = fleet.q(z)
    S, N = np.zeros(fleet.n), np.zeros(fleet.n)
    read = []
    leader = None
    for m in [entry] + fleet.known_by(entry):
        read.append(m)
        with contextlib.redirect_stdout(io.StringIO()):
            gaps = fleet.d_int[m].support_gaps(v)
        if len(gaps) > XI:
            continue
        scale = (64 - len(gaps)) * 16
        den = e1.tol_proj(fleet.d_int[m], v, gaps) / scale
        num = e1.tol_proj(fleet.d_exi[m], v, gaps) / scale
        den[~fleet.active] = 0
        num[~fleet.active] = 0
        N += den
        S += num
        sup = np.where(N > 0)[0]
        if len(sup) == 0:
            continue
        p, lo, hi = wilson(S[sup], N[sup], zval)
        k = max(range(len(sup)), key=lambda i: (p[i], N[sup][i]))
        leader = int(sup[k])
        if len(sup) == 1 or lo[k] > np.max(np.delete(hi, k)):
            return leader, len(read), False
    if leader is not None:
        return leader, len(read), False
    return content_fallback(fleet, z, read), len(read), True


def learn_receptor(fleet, Qs, C, stream, rng, log):
    for p, j in stream:
        zv = C[f"q_{p}"][j]
        cand = fleet.candidates(zv[0])
        if not cand:
            continue
        entry = cand[rng.randint(len(cand))]
        w = cand[rng.randint(len(cand))]
        ok = pm.answer(Qs, fleet.mods, w, p, j)
        fleet.register(zv, entry, w, ok)
        log.append((p, j, w, ok))


def build(mode):
    Qs, C = pm.queries(), pm.cues()
    learn_set, eval_set = pm.split(Qs)
    acc = lambda p, v, js: float(np.mean([int(Qs[p]["logits"][v][j].argmax()) == int(Qs[p]["y"][j]) for j in js]))
    weak = {p: min("BCD", key=lambda v: acc(p, v, learn_set[p])) for p in pm.PIECES}
    mods = [(p, v) for p in pm.PIECES for v in ("A", weak[p])]
    fill = {p: C[f"fill_{p}"] for p in pm.PIECES}
    zs = np.concatenate([fill[p][:, 0] for p in pm.PIECES])
    lo, hi = zs.min(0), zs.max(0)
    g = (lo - pm.PAD * (hi - lo), hi + pm.PAD * (hi - lo))
    rng = np.random.RandomState(pm.SEED)
    stream = [(p, j) for p in pm.PIECES for j in learn_set[p]]
    stream = [stream[i] for i in rng.permutation(len(stream))]
    fleet = pm.Fleet(mods, fill, g)
    for i in range(fleet.n):
        fleet.activate(i)
    log = []
    (pm.learn if mode == "azar" else learn_receptor)(fleet, Qs, C, stream, rng, log)
    rows = pm.evaluate(fleet, Qs, C, eval_set, log, mods, rng)
    if mode == "receptor":
        r_rng = np.random.RandomState(pm.SEED + 7)
        act = np.where(fleet.active)[0]
        for r in rows:
            p, j = r["dominio"], r["j"]
            z = C[f"q_{p}"][j][0] if r["pieza"] else C[f"u_{p}"][j]
            cand = fleet.candidates(z)
            r["entrada"] = int(cand[r_rng.randint(len(cand))]) if cand else int(act[r_rng.randint(len(act))])
            w, c = fleet.route(z, r["entrada"], "r2")
            r["r2"], r["r2_consultados"] = w, c
            if r["pieza"]:
                r["r2_ok"] = bool(w is not None and pm.answer(Qs, mods, w, p, j))
    return fleet, Qs, C, mods, rows, log, {f"{p}/{v}": acc(p, v, eval_set[p]) for p, v in mods}


def run():
    t0 = time.time()
    res = {}
    for mode in ("azar", "receptor"):
        fleet, Qs, C, mods, rows, log, accm = build(mode)
        print(f"{mode}: {len(log)} transacciones, R2 {np.mean([r['r2_ok'] for r in rows if r['pieza']]):.4f} ({time.time() - t0:.0f} s)", flush=True)
        for r in rows:
            p, j = r["dominio"], r["j"]
            z = C[f"q_{p}"][j][0] if r["pieza"] else C[f"u_{p}"][j]
            readers = {"r3": lambda: e1.directed(fleet, z, r["entrada"], XI)}
            for zv in ZS:
                readers[f"r4_{zv}"] = (lambda zz: (lambda: accumulate(fleet, z, r["entrada"], zz)))(zv)
            for k, f in readers.items():
                w, nread, cont = f()
                r[k], r[f"{k}_leidos"], r[f"{k}_contenido"] = w, nread, cont
                if r["pieza"]:
                    r[f"{k}_ok"] = bool(w is not None and pm.answer(Qs, mods, w, p, j))
        res[mode] = {"modulos": [f"{p}/{v}" for p, v in mods], "acierto_modulos_eval": accm, "eval": rows,
                     "transacciones": len(log)}
        print(f"{mode} evaluado ({time.time() - t0:.0f} s)", flush=True)
    res["segundos"] = round(time.time() - t0)
    return res


def pct(x):
    return f"{100 * x:5.1f}"


def report(res):
    L = ["Etapa 2: acumular evidencia (R4) y entradas por receptor (propuesta_etapa2_evidencia.md)."]
    verdict = {}
    for mode in ("azar", "receptor"):
        R = res[mode]
        mods, rows, accm = R["modulos"], R["eval"], R["acierto_modulos_eval"]
        kn = [r for r in rows if r["pieza"]]
        un = [r for r in rows if not r["pieza"]]

        def to_best(k):
            out = []
            for p in pm.PIECES:
                pair = [m for m in mods if m.startswith(p + "/")]
                if abs(accm[pair[0]] - accm[pair[1]]) < 0.05:
                    continue
                best = max(pair, key=lambda m: accm[m])
                ws = [mods[r[k]] for r in kn if r["pieza"] == p and r[k] is not None and mods[r[k]].startswith(p + "/")]
                if ws:
                    out.append(np.mean([w == best for w in ws]))
            return float(np.mean(out))

        central = np.mean([r["central_ok"] for r in kn])
        L.append(f"\n[entrada {mode}] {R['transacciones']} transacciones de aprendizaje")
        L.append("  método        acierto · abst. conocidas · acierto respondido · abst. desconocidas · costo medio · respaldo · al mejor")
        for k in ["r2", "r3"] + [f"r4_{z}" for z in ZS] + ["central", "compuerta", "todos"]:
            a = np.mean([r[f"{k}_ok"] for r in kn])
            ab = np.mean([r[k] is None for r in kn])
            ans = [r for r in kn if r[k] is not None]
            aa = np.mean([r[f"{k}_ok"] for r in ans])
            au = np.mean([r[k] is None for r in un])
            if k.startswith(("r3", "r4")):
                cost = np.mean([r[f"{k}_leidos"] + (24 if r[f"{k}_contenido"] else 0) for r in kn])
                cont = np.mean([r[f"{k}_contenido"] for r in kn])
                med = np.median([r[f"{k}_leidos"] for r in kn])
            elif k == "r2":
                cost, cont, med = np.mean([r["r2_consultados"] for r in kn]), 0.0, np.median([r["r2_consultados"] for r in kn])
            else:
                cost, cont, med = float("nan"), 0.0, float("nan")
            tb = to_best(k)
            L.append(f"  {k:<12} {pct(a)} · {pct(ab)} · {pct(aa)} · {pct(au)} · {cost:5.1f} (mediana {med:.0f}) · {pct(cont)} · {pct(tb)}")
            if k.startswith(("r2", "r3", "r4")):
                verdict[f"{mode}_{k}"] = {"diferencia_con_central": round(float(central - a), 4), "costo": round(float(cost), 2),
                                          "al_mejor": round(tb, 4), "abst_desconocidas": float(au),
                                          "sostenido": bool(central - a <= 0.03 and cost <= 6 and tb >= 0.70 and au >= 0.95)}
    L.append(f"\n[criterio] {json.dumps(verdict)}")
    L.append(f"\nTiempo total: {res.get('segundos', 0) / 60:.0f} min")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "resultados.json"
    if not args.report_only:
        raw.write_text(json.dumps(run(), ensure_ascii=False))
    report(json.loads(raw.read_text()))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
