"""
Etapa 1: ruteo dirigido (R3) sobre la flota del piloto. Diseño en
propuesta_etapa1_ruteo_dirigido.md.

El módulo de entrada lee su propio directorio; si no tiene soporte (más de ξ coordenadas
sin soporte), pregunta a sus conocidos uno por uno en el orden de sus conteos; si nadie
tiene soporte, recurre al contenido. Todas las decisiones salen de las memorias.

Uso: python run_etapa1_ruteo_dirigido.py [--report-only]
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

import run_piloto_modulos as pm  # noqa: E402

OUT = ROOT / "results" / "etapa1_ruteo_dirigido"
XIS = (0, 1, 2, 3)


def tol_proj(d, v, gaps):
    """Proyección del bit «conoce» con las coordenadas sin soporte marcadas como indefinidas."""
    if not gaps:
        return d.predict(v)
    ham = d._ham
    vv = ham.validate(np.asarray(v, dtype=float), 0).astype(int)
    vv[gaps] = ham.undefined(0)
    with contextlib.redirect_stdout(io.StringIO()):
        proj = ham.project(vv, np.ones(len(vv), dtype=float), dim=0)
    return proj[:, 1].copy()


def directed(fleet, z, entry, xi):
    """Devuelve (módulo o None, directorios leídos, usó contenido)."""
    v = fleet.q(z)
    read = []
    for m in [entry] + fleet.known_by(entry):
        read.append(m)
        with contextlib.redirect_stdout(io.StringIO()):
            gaps = fleet.d_int[m].support_gaps(v)
        if len(gaps) > xi:
            continue
        den = tol_proj(fleet.d_int[m], v, gaps)
        num = tol_proj(fleet.d_exi[m], v, gaps)
        ok = (den > 0) & fleet.active
        if ok.any():
            score = np.where(ok, num / np.maximum(den, 1e-12), -1)
            return int(np.argmax(score)), len(read), False
    cand = fleet.candidates(z)
    if not cand:
        return None, len(read), True
    succ = sum(fleet.d_exi[m]._counts for m in read).astype(float)
    att = sum(fleet.d_int[m]._counts for m in read).astype(float)
    known = [i for i in cand if att[i] > 0]
    if known:
        return max(known, key=lambda i: (succ[i] / att[i], att[i])), len(read), True
    w = [float(fleet.content[fleet.mods[i][0]].recog_weights(fleet.q(z)).mean()) for i in cand]
    return cand[int(np.argmax(w))], len(read), True


def run():
    t0 = time.time()
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
    pm.learn(fleet, Qs, C, stream, rng, log)
    rows = pm.evaluate(fleet, Qs, C, eval_set, log, mods, rng)
    print(f"piloto reconstruido: {len(log)} transacciones, acierto R2 "
          f"{np.mean([r['r2_ok'] for r in rows if r['pieza']]):.4f} ({time.time() - t0:.0f} s)", flush=True)
    for r in rows:
        p, j = r["dominio"], r["j"]
        z = C[f"q_{p}"][j][0] if r["pieza"] else C[f"u_{p}"][j]
        for xi in XIS:
            w, nread, cont = directed(fleet, z, r["entrada"], xi)
            k = f"r3_{xi}"
            r[k], r[f"{k}_leidos"], r[f"{k}_contenido"] = w, nread, cont
            if r["pieza"]:
                r[f"{k}_ok"] = bool(w is not None and pm.answer(Qs, mods, w, p, j))
    print(f"R3 listo ({time.time() - t0:.0f} s)", flush=True)
    return {"modulos": [f"{p}/{v}" for p, v in mods],
            "acierto_modulos_eval": {f"{p}/{v}": acc(p, v, eval_set[p]) for p, v in mods},
            "eval": rows, "segundos": round(time.time() - t0)}


def pct(x):
    return f"{100 * x:5.1f}"


def report(res):
    mods, rows = res["modulos"], res["eval"]
    kn = [r for r in rows if r["pieza"]]
    un = [r for r in rows if not r["pieza"]]
    accm = res["acierto_modulos_eval"]
    L = ["Etapa 1: ruteo dirigido (propuesta_etapa1_ruteo_dirigido.md). Misma flota, consultas y aprendizaje que el piloto.",
         f"{len(kn)} consultas conocidas, {len(un)} desconocidas.",
         "\n método        acierto · abst. conocidas · acierto respondido · abst. desconocidas · costo medio (conocidas) · respaldo por contenido · al mejor"]

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

    verdict = {}
    central = np.mean([r["central_ok"] for r in kn])
    for k in ["r2", "central", "compuerta", "todos"] + [f"r3_{xi}" for xi in XIS]:
        a = np.mean([r[f"{k}_ok"] for r in kn])
        ab = np.mean([r[k] is None for r in kn])
        ans = [r for r in kn if r[k] is not None]
        aa = np.mean([r[f"{k}_ok"] for r in ans])
        au = np.mean([r[k] is None for r in un])
        if k.startswith("r3"):
            cost = np.mean([r[f"{k}_leidos"] + (24 if r[f"{k}_contenido"] else 0) for r in kn])
            cont = np.mean([r[f"{k}_contenido"] for r in kn])
        elif k == "r2":
            cost, cont = np.mean([r["r2_consultados"] for r in kn]), 0.0
        elif k == "todos":
            cost, cont = 24.0, 1.0
        else:
            cost, cont = float("nan"), 0.0
        tb = to_best(k)
        L.append(f" {k:<12} {pct(a)} · {pct(ab)} · {pct(aa)} · {pct(au)} · {cost:5.1f} · {pct(cont)} · {pct(tb)}")
        if k.startswith("r3"):
            verdict[k] = {"diferencia_con_central": float(central - a), "costo": float(cost), "al_mejor": tb,
                          "abst_desconocidas": float(au),
                          "sostenido": bool(central - a <= 0.03 and cost <= 6 and tb >= 0.70 and au >= 0.95)}
    for xi in XIS:
        k = f"r3_{xi}"
        c = np.array([r[f"{k}_leidos"] for r in kn])
        L.append(f"  {k}: directorios leídos en conocidas: mediana {np.median(c):.0f}, p90 {np.percentile(c, 90):.0f}, máx {c.max()}")
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
