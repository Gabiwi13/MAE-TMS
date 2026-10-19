"""
Aprendizaje en línea con deriva: el olvido exacto como mecanismo de adaptación.
Diseño en propuesta_deriva_olvido.md.

Entrada por receptor, recorrido R3 y muestreo de Thompson con la evidencia de éxitos e
intentos leída del directorio. En t = 3000 el mejor módulo de cada dominio con diferencia de
>= 5 puntos se degrada (su respuesta se invierte con probabilidad 0.5).

Uso:
  python run_deriva_olvido.py --variante F0 | W300 | W600 | W1200 | rivales
  python run_deriva_olvido.py --report-only
"""
import argparse
import collections
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
from run_olvido_privacidad import forget_dir  # noqa: E402

OUT = ROOT / "results" / "deriva_olvido"
CACHE = OUT / "cache"            # fuera de git
T, T_DRIFT, XI = 6000, 3000, 1
WINDOWS = (300, 600, 1200)


def setup():
    Qs, C = pm.queries(), pm.cues()
    learn_set, _ = pm.split(Qs)
    acc = lambda p, v, js: float(np.mean([int(Qs[p]["logits"][v][j].argmax()) == int(Qs[p]["y"][j]) for j in js]))
    weak = {p: min("BCD", key=lambda v: acc(p, v, learn_set[p])) for p in pm.PIECES}
    mods = [(p, v) for p in pm.PIECES for v in ("A", weak[p])]
    allq = {p: list(range(len(Qs[p]["y"]))) for p in pm.PIECES}
    accm = {i: acc(p, v, allq[p]) for i, (p, v) in enumerate(mods)}
    best, degraded = {}, set()
    for p in pm.PIECES:
        a, b = [i for i, (mp, _) in enumerate(mods) if mp == p]
        best[p] = a if accm[a] >= accm[b] else b
        if abs(accm[a] - accm[b]) >= 0.05:
            degraded.add(best[p])
    rng = np.random.RandomState(pm.SEED)
    pool = [(p, j) for p in pm.PIECES for j in allq[p]]
    stream = [(*pool[rng.randint(len(pool))], int(rng.randint(16)), bool(rng.rand() < 0.5)) for _ in range(T)]
    fill = {p: C[f"fill_{p}"] for p in pm.PIECES}
    zs = np.concatenate([fill[p][:, 0] for p in pm.PIECES])
    lo, hi = zs.min(0), zs.max(0)
    g = (lo - pm.PAD * (hi - lo), hi + pm.PAD * (hi - lo))
    return Qs, C, mods, accm, best, degraded, stream, fill, g


def make_answer(Qs, mods, degraded):
    def answer(i, p, j, t, flip):
        ok = pm.answer(Qs, mods, i, p, j)
        if t >= T_DRIFT and i in degraded and flip:
            ok = (not ok) if mods[i][0] == p else ok
        return ok
    return answer


def current_best(p, t, best, degraded, mods):
    b = best[p]
    if t >= T_DRIFT and b in degraded:
        return [i for i, (mp, _) in enumerate(mods) if mp == p and i != b][0]
    return b


def evidence(fleet, z, entry):
    """Éxitos e intentos efectivos del primer directorio del recorrido R3 con soporte."""
    v = fleet.q(z)
    read = 0
    for m in [entry] + fleet.known_by(entry):
        read += 1
        with contextlib.redirect_stdout(io.StringIO()):
            gaps = fleet.d_int[m].support_gaps(v)
        if len(gaps) > XI:
            continue
        scale = (64 - len(gaps)) * 16
        N = e1.tol_proj(fleet.d_int[m], v, gaps) / scale
        S = e1.tol_proj(fleet.d_exi[m], v, gaps) / scale
        if (N[fleet.active] > 0).any():
            return S, N, read
    return np.zeros(fleet.n), np.zeros(fleet.n), read


def run_memory(window):
    Qs, C, mods, accm, best, degraded, stream, fill, g = setup()
    answer = make_answer(Qs, mods, degraded)
    fleet = pm.Fleet(mods, fill, g)
    for i in range(fleet.n):
        fleet.activate(i)
    rng = np.random.RandomState(pm.SEED + 1)
    hist = collections.deque()
    rows = []
    t0 = time.time()
    for t, (p, j, var, flip) in enumerate(stream):
        zv = C[f"q_{p}"][j]
        z = zv[var]
        cand = fleet.candidates(z)
        if not cand:
            rows.append((p, None, False, 0))
            continue
        entry = cand[rng.randint(len(cand))]
        S, N, read = evidence(fleet, z, entry)
        draws = [rng.beta(S[i] + 1, max(N[i] - S[i], 0) + 1) for i in cand]
        w = cand[int(np.argmax(draws))]
        ok = answer(w, p, j, t, flip)
        fleet.register(zv, entry, w, ok)
        if window:
            hist.append((p, j, entry, w, ok))
            if len(hist) > window:
                op, oj, oe, ow, ook = hist.popleft()
                for zz in C[f"q_{op}"][oj]:
                    v = fleet.q(zz)
                    for m in {oe, ow}:
                        forget_dir(fleet.d_int[m], v, ow)
                        if ook:
                            forget_dir(fleet.d_exi[m], v, ow)
        rows.append((p, int(w), bool(ok), read))
        if (t + 1) % 1000 == 0:
            print(f"  W={window} t={t + 1} ({time.time() - t0:.0f} s)", flush=True)
    return {"filas": rows, "mejor": {p: int(b) for p, b in best.items()}, "degradados": sorted(int(i) for i in degraded),
            "modulos": [f"{p}/{v}" for p, v in mods]}


def run_rivals():
    Qs, C, mods, accm, best, degraded, stream, fill, g = setup()
    answer = make_answer(Qs, mods, degraded)
    out = {}
    for window in (0,) + WINDOWS:
        rng = np.random.RandomState(pm.SEED + 1)
        hist = collections.deque()
        S, N = np.zeros(len(mods)), np.zeros(len(mods))
        rows = []
        for t, (p, j, var, flip) in enumerate(stream):
            cand = [i for i, (mp, _) in enumerate(mods) if mp == p]
            draws = [rng.beta(S[i] + 1, N[i] - S[i] + 1) for i in cand]
            w = cand[int(np.argmax(draws))]
            ok = answer(w, p, j, t, flip)
            S[w] += ok
            N[w] += 1
            if window:
                hist.append((w, ok))
                if len(hist) > window:
                    ow, ook = hist.popleft()
                    S[ow] -= ook
                    N[ow] -= 1
            rows.append((p, int(w), bool(ok), 0))
        out[f"bandido_W{window}" if window else "bandido_F0"] = rows
    rows = []
    for t, (p, j, var, flip) in enumerate(stream):
        b = current_best(p, t, best, degraded, mods)
        rows.append((p, int(b), bool(answer(b, p, j, t, flip)), 0))
    out["oraculo"] = rows
    return {"filas": out, "mejor": {p: int(b) for p, b in best.items()}, "degradados": sorted(int(i) for i in degraded),
            "modulos": [f"{p}/{v}" for p, v in mods]}


# ---------- reporte ----------

SEGMENTS = {"antes (2000-3000)": (2000, 3000), "justo después (3000-3500)": (3000, 3500),
            "recuperación (3500-4500)": (3500, 4500), "final (5000-6000)": (5000, 6000)}


def pct(x):
    return f"{100 * x:5.1f}"


def report():
    files = {k: json.loads((CACHE / f"{k}.json").read_text()) for k in ["F0"] + [f"W{w}" for w in WINDOWS] + ["rivales"]
             if (CACHE / f"{k}.json").exists()}
    ref = files["rivales"]
    mods, best, deg = ref["modulos"], ref["mejor"], set(ref["degradados"])
    series = {f"memoria_{k}": v["filas"] for k, v in files.items() if k != "rivales"}
    series.update(ref["filas"])
    drift_dom = {mods[i].split("/")[0] for i in deg}

    def cur_best(p, t):
        b = best[p]
        if t >= T_DRIFT and b in deg:
            return [i for i, m in enumerate(mods) if m.startswith(p + "/") and i != b][0]
        return b

    L = ["Aprendizaje en línea con deriva (propuesta_deriva_olvido.md). Corriente de 6000 consultas; deriva en t = 3000.",
         f"Dominios con deriva: {sorted(drift_dom)}"]
    L.append("\n[acierto en línea por tramo] " + " · ".join(SEGMENTS))
    summary = {}
    for name, rows in series.items():
        line = f"  {name:<18}"
        for seg, (a, b) in SEGMENTS.items():
            line += f" {pct(np.mean([r[2] for r in rows[a:b]]))}"
        reads = [r[3] for r in rows if r[1] is not None]
        if name.startswith("memoria"):
            line += f" · lecturas medias {np.mean(reads):.2f} · sin candidato {sum(r[1] is None for r in rows)}"
        L.append(line)
        summary[name] = {"final": float(np.mean([r[2] for r in rows[5000:6000]]))}
    L.append("\n[fracción al mejor vigente, dominios con deriva] tramos de 250 desde t = 2000")
    for name, rows in series.items():
        fr, rec = [], None
        for a in range(2000, T, 250):
            sel = [(t, r) for t, r in enumerate(rows[a:a + 250], a) if r[0] in drift_dom and r[1] is not None]
            f = np.mean([r[1] == cur_best(r[0], t) for t, r in sel]) if sel else float("nan")
            fr.append(f)
            if a >= T_DRIFT and rec is None and f >= 0.70:
                rec = a - T_DRIFT
        L.append(f"  {name:<18} " + " ".join(pct(f) for f in fr) + f" · recupera (≥ 70 %) a los {rec if rec is not None else 'nunca'} pasos")
        summary[name]["recupera"] = rec
        summary[name]["al_mejor_antes"] = float(fr[3])
    L.append(f"\n[criterio] {json.dumps(summary)}")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    (OUT / "resultados.json").write_text(json.dumps({"resumen": summary, "series": {k: [list(r) for r in v] for k, v in series.items()},
                                                     "modulos": mods, "mejor": best, "degradados": sorted(deg)}))
    print(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variante")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    if args.variante:
        res = run_rivals() if args.variante == "rivales" else run_memory(0 if args.variante == "F0" else int(args.variante[1:]))
        (CACHE / f"{args.variante}.json").write_text(json.dumps(res))
        return
    report()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
