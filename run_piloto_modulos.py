"""
Piloto: el sistema transactivo como organizador de una flota de 24 módulos (12 piezas de
VisA x 2 redes de distinta calidad). Diseño en propuesta_piloto_modulos.md.

Directorios de intentos y de éxitos por módulo (perspectivales); lecturas R1 oficial
(pertenencia, B1) y R2 calidad (éxitos / intentos). Rivales: router central kNN,
compuerta aprendida, preguntarle a todos, azar y oráculo. Eventos: alta de candle y baja
del mejor módulo de pcb1.

Uso: python run_piloto_modulos.py [--report-only]
"""
import argparse
import contextlib
import io
import json
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_cierre_mae as cm  # noqa: E402
import run_industrial_demo as ind  # noqa: E402
import run_medico_demo as demo  # noqa: E402
from associative_memory import DirectoryMemory, HomoAssociativeMemory  # noqa: E402

OUT = ROOT / "results" / "piloto_modulos"
CACHE = OUT / "cache"            # fuera de git
MED = Path("C:/Users/aq99l/Projects/MAE-TMS-medico/data/medmnist")
PIECES, N_FILL, Q, PAD, SEED = ind.PIECES, ind.N_FILL, ind.Q, ind.PAD, 42
LAT = {"A": ROOT / "results/cascada_modulos/cache/lat_{p}.npz",
       **{v: ROOT / f"results/red_sintetica/cache/lat_{v}_{{p}}.npz" for v in "BCD"}}
UNKNOWN = ("retinamnist", "dermamnist", "breastmnist")
N_UNK = 300


# ---------- datos ----------

def queries():
    """Por pieza: índices de test, etiquetas y logits de las 4 versiones de red, en el mismo orden."""
    out = {}
    for p in PIECES:
        tr, te, novel, _, _ = cm.split_defects(p)
        y_all = ind.imgs()[f"testy_{p}"]
        idx = np.concatenate([np.where(y_all == 0)[0], te, novel]).astype(int)
        z = {v: np.load(str(f).format(p=p)) for v, f in LAT.items()}
        y = np.concatenate([z["A"]["yt"], np.ones(len(z["A"]["zv"]), int)])
        logits = {v: np.concatenate([z[v]["lt"], z[v]["lv"]]) for v in z}
        out[p] = {"idx": idx, "y": y, "logits": logits}
    return out


def cues():
    """Latentes de ruteo (nivel 1 del demo): llenado y consultas con 16 variantes, desconocidas sin variantes."""
    path = CACHE / "pistas.npz"
    if path.exists():
        return dict(np.load(path, allow_pickle=False))
    F5 = dict(np.load(ind.CACHE / "rasgos512.npz", allow_pickle=False))
    P1 = ind.pca(np.concatenate([ind.imgs()[f"f512all_{p}"] for p in PIECES]))
    net = ind.backbone()
    Qs = queries()
    out = {}
    for p in PIECES:
        out[f"fill_{p}"] = ind.proj(P1, F5[f"reg_{p}"][:N_FILL])
        out[f"q_{p}"] = ind.proj(P1, ind.feats512(net, ind.imgs()[f"test_{p}"][Qs[p]["idx"]], variants=True))
    rng = np.random.RandomState(SEED)
    for name in UNKNOWN:
        x = np.load(MED / f"{name}_128.npz")["test_images"]
        sel = rng.permutation(len(x))[:N_UNK]
        imgs = np.stack([np.asarray(Image.fromarray(x[i]).convert("RGB").resize((224, 224), Image.BILINEAR)) for i in sel])
        out[f"u_{name}"] = ind.proj(P1, ind.feats512(net, imgs))
    np.savez(path, **out)
    return out


# ---------- flota ----------

class Fleet:
    def __init__(self, modules, fill, g):
        self.mods = modules                        # [(pieza, versión)]
        self.n = len(modules)
        self.g = g
        self.content = {}
        self.active = np.zeros(self.n, bool)
        with contextlib.redirect_stdout(io.StringIO()):
            self.d_int = [DirectoryMemory(64, Q, self.n) for _ in range(self.n)]
            self.d_exi = [DirectoryMemory(64, Q, self.n) for _ in range(self.n)]
        self.fill = fill

    def q(self, z):
        return demo.quantize_latent_global(np.asarray(z, dtype=np.float32), *self.g, Q)

    def activate(self, i):
        p = self.mods[i][0]
        if p not in self.content:
            mem = HomoAssociativeMemory(64, Q)
            for z in self.fill[p].reshape(-1, 64):
                mem.register(self.q(z))
            self.content[p] = mem
        self.active[i] = True

    def contains(self, i, z):
        return bool(np.all(self.content[self.mods[i][0]].recog_weights(self.q(z)) > 0))

    def candidates(self, z):
        return [i for i in range(self.n) if self.active[i] and self.contains(i, z)]

    def register(self, zv, entry, winner, success):
        for z in zv:
            v = self.q(z)
            for m in {entry, winner}:
                self.d_int[m].register(v, winner)
                if success:
                    self.d_exi[m].register(v, winner)

    def known_by(self, m):
        c = self.d_int[m]._counts
        return [int(j) for j in np.argsort(-c) if c[j] > 0 and j != m and self.active[j]]

    def route(self, z, entry, reading):
        """Recorrido de route_transactive. Devuelve (módulo o None, directorios consultados)."""
        v = self.q(z)
        summed, visited, queue = set(), set(), [entry]
        num, den = np.zeros(self.n), np.zeros(self.n)
        while queue:
            a = queue.pop(0)
            if a in visited:
                continue
            visited.add(a)
            for m in [a] + self.known_by(a):
                if m in summed:
                    continue
                summed.add(m)
                with contextlib.redirect_stdout(io.StringIO()):
                    if reading == "r1":
                        num += self.d_int[m].predict_tolerant(v, xi=0, mode="linear")
                    elif not self.d_int[m].support_gaps(v):
                        num += self.d_exi[m].predict(v)
                        den += self.d_int[m].predict(v)
            num[~self.active] = 0
            score = num if reading == "r1" else np.where(den > 0, num / np.maximum(den, 1e-12), 0)
            if reading == "r2":
                score = np.where((den > 0) & self.active, score, -1)
                if (den[self.active] > 0).any():
                    return int(np.argmax(score)), len(summed)
            elif score.sum() > 0:
                return int(np.argmax(score)), len(summed)
            queue = [k for k in self.known_by(a) if k not in visited] + queue
        return None, len(summed)


def answer(Qs, mods, i, p, j):
    """¿El módulo i responde bien la consulta j de la pieza p?"""
    mp, mv = mods[i]
    return mp == p and int(Qs[p]["logits"][mv][j].argmax()) == int(Qs[p]["y"][j])


def learn(fleet, Qs, C, stream, rng, log):
    for p, j in stream:
        zv = C[f"q_{p}"][j]
        cand = fleet.candidates(zv[0])
        if not cand:
            continue
        act = np.where(fleet.active)[0]
        entry = int(act[rng.randint(len(act))])
        w = cand[rng.randint(len(cand))]
        ok = answer(Qs, fleet.mods, w, p, j)
        fleet.register(zv, entry, w, ok)
        log.append((p, j, w, ok))


# ---------- corrida ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    raw = OUT / "resultados.json"
    if not args.report_only:
        raw.write_text(json.dumps(run(), ensure_ascii=False))
    report(json.loads(raw.read_text()))


def split(Qs):
    rng = np.random.RandomState(SEED)
    learn_set, eval_set = {}, {}
    for p in PIECES:
        y = Qs[p]["y"]
        L, E = [], []
        for c in (0, 1):
            ii = rng.permutation(np.where(y == c)[0])
            h = len(ii) // 2
            L += ii[:h].tolist()
            E += ii[h:].tolist()
        learn_set[p], eval_set[p] = sorted(L), sorted(E)
    return learn_set, eval_set


def run():
    t0 = time.time()
    Qs, C = queries(), cues()
    print(f"pistas listas ({time.time() - t0:.0f} s)", flush=True)
    learn_set, eval_set = split(Qs)
    acc = lambda p, v, js: float(np.mean([int(Qs[p]["logits"][v][j].argmax()) == int(Qs[p]["y"][j]) for j in js]))
    weak = {p: min("BCD", key=lambda v: acc(p, v, learn_set[p])) for p in PIECES}
    mods = [(p, v) for p in PIECES for v in ("A", weak[p])]
    fill = {p: C[f"fill_{p}"] for p in PIECES}
    zs = np.concatenate([fill[p][:, 0] for p in PIECES])
    lo, hi = zs.min(0), zs.max(0)
    g = (lo - PAD * (hi - lo), hi + PAD * (hi - lo))
    res = {"modulos": [f"{p}/{v}" for p, v in mods],
           "acierto_modulos_eval": {f"{p}/{v}": acc(p, v, eval_set[p]) for p, v in mods}}
    rng = np.random.RandomState(SEED)
    stream = [(p, j) for p in PIECES for j in learn_set[p]]
    stream = [stream[i] for i in rng.permutation(len(stream))]

    # --- corrida principal
    fleet = Fleet(mods, fill, g)
    for i in range(fleet.n):
        fleet.activate(i)
    log = []
    learn(fleet, Qs, C, stream, rng, log)
    res["aprendizaje"] = {"transacciones": len(log), "exitos": int(sum(x[3] for x in log)), "consultas": len(stream)}
    print(f"aprendizaje listo: {len(log)} transacciones ({time.time() - t0:.0f} s)", flush=True)
    res["eval"] = evaluate(fleet, Qs, C, eval_set, log, mods, rng)
    print(f"evaluación lista ({time.time() - t0:.0f} s)", flush=True)

    # --- E2: baja del mejor módulo de pcb1 (por acierto en aprendizaje)
    i_a, i_b = mods.index(("pcb1", "A")), mods.index(("pcb1", weak["pcb1"]))
    best = i_a if acc("pcb1", "A", learn_set["pcb1"]) >= acc("pcb1", weak["pcb1"], learn_set["pcb1"]) else i_b
    fleet.active[best] = False
    rows = []
    for j in eval_set["pcb1"]:
        z = C["q_pcb1"][j][0]
        act = np.where(fleet.active)[0]
        w, _ = fleet.route(z, int(act[rng.randint(len(act))]), "r2")
        rows.append({"destino": None if w is None else res["modulos"][w], "ok": bool(w is not None and answer(Qs, mods, w, "pcb1", j))})
    res["E2"] = {"retirado": res["modulos"][best], "filas": rows}
    print(f"E2 listo ({time.time() - t0:.0f} s)", flush=True)

    # --- E1: alta de candle
    fleet = Fleet(mods, fill, g)
    cand_idx = [i for i, (p, _) in enumerate(mods) if p == "candle"]
    for i in range(fleet.n):
        if i not in cand_idx:
            fleet.activate(i)
    rng = np.random.RandomState(SEED)
    learn(fleet, Qs, C, [s for s in stream if s[0] != "candle"], rng, [])
    e1 = {"antes": route_rate(fleet, Qs, C, eval_set["candle"], mods, rng)}
    for i in cand_idx:
        fleet.activate(i)
    cl = [("candle", j) for j in learn_set["candle"]]
    done = 0
    for n in (5, 10, 20, 40):
        learn(fleet, Qs, C, cl[done:n], rng, [])
        done = n
        e1[str(n)] = route_rate(fleet, Qs, C, eval_set["candle"], mods, rng)
    e1["otras_piezas_r2"] = float(np.mean([r["ok"] for r in quick_eval(fleet, Qs, C, eval_set, mods, rng, skip="candle")]))
    res["E1"] = e1
    res["segundos"] = round(time.time() - t0)
    print(f"E1 listo ({time.time() - t0:.0f} s)", flush=True)
    return res


def route_rate(fleet, Qs, C, js, mods, rng):
    act = np.where(fleet.active)[0]
    out = [fleet.route(C["q_candle"][j][0], int(act[rng.randint(len(act))]), "r2")[0] for j in js]
    return {"a_candle": float(np.mean([w is not None and mods[w][0] == "candle" for w in out])),
            "abstencion": float(np.mean([w is None for w in out])),
            "acierto": float(np.mean([w is not None and answer(Qs, mods, w, "candle", j) for w, j in zip(out, js)]))}


def quick_eval(fleet, Qs, C, eval_set, mods, rng, skip):
    rows = []
    act = np.where(fleet.active)[0]
    for p in PIECES:
        if p == skip:
            continue
        for j in eval_set[p]:
            w, _ = fleet.route(C[f"q_{p}"][j][0], int(act[rng.randint(len(act))]), "r2")
            rows.append({"ok": bool(w is not None and answer(Qs, mods, w, p, j))})
    return rows


def evaluate(fleet, Qs, C, eval_set, log, mods, rng):
    n = len(mods)
    # rivales que usan todas las transacciones de aprendizaje
    X = np.array([C[f"q_{p}"][j][0] for p, j, _, _ in log])
    W = np.array([w for _, _, w, _ in log])
    S = np.array([ok for *_, ok in log], float)
    dom = np.array([PIECES.index(p) for p, *_ in log])
    d2 = ((X[:, None] - X[None]) ** 2).sum(2)
    np.fill_diagonal(d2, np.inf)
    thr_knn = np.quantile(np.sqrt(d2.min(1)), 0.99)
    gate = LogisticRegression(max_iter=3000).fit(X, dom)
    thr_gate = np.quantile(gate.predict_proba(X).max(1), 0.01)
    rate = np.array([S[W == i].mean() if (W == i).any() else 0 for i in range(n)])

    def central(z):
        d = np.sqrt(((X - z) ** 2).sum(1))
        if d.min() > thr_knn:
            return None
        nn = np.argsort(d)[:10]
        best, key = None, (-1, -1)
        for i in set(W[nn].tolist()):
            m = W[nn] == i
            k = (S[nn][m].mean(), S[nn][m].sum())
            if k > key:
                best, key = i, k
        return int(best)

    def gate_route(z):
        pr = gate.predict_proba(z[None])[0]
        if pr.max() < thr_gate:
            return None
        p = PIECES[gate.classes_[pr.argmax()]]
        ii = [i for i, (mp, _) in enumerate(mods) if mp == p]
        return max(ii, key=lambda i: rate[i])

    rows = []
    act = np.where(fleet.active)[0]
    sets = [(p, j) for p in PIECES for j in eval_set[p]] + [(u, k) for u in UNKNOWN for k in range(len(C[f"u_{u}"]))]
    for p, j in sets:
        known = p in PIECES
        z = C[f"q_{p}"][j][0] if known else C[f"u_{p}"][j]
        entry = int(act[rng.randint(len(act))])
        cand = fleet.candidates(z)
        r = {"pieza": p if known else None, "dominio": p}
        for name in ("r1", "r2"):
            w, c = fleet.route(z, entry, name)
            r[name], r[f"{name}_consultados"] = w, c
        r["central"], r["compuerta"] = central(z), gate_route(z)
        if cand and known:
            conf = [float(np.exp(Qs[p]["logits"][mods[i][1]][j]).max() / np.exp(Qs[p]["logits"][mods[i][1]][j]).sum())
                    if mods[i][0] == p else 0.0 for i in cand]
            r["todos"] = cand[int(np.argmax(conf))]
        else:
            r["todos"] = cand[0] if cand else None
        r["todos_consultados"] = len(cand)
        r["azar"] = cand[rng.randint(len(cand))] if cand else None
        if known:
            for k in ("r1", "r2", "central", "compuerta", "todos", "azar"):
                r[f"{k}_ok"] = bool(r[k] is not None and answer(Qs, mods, r[k], p, j))
            r["oraculo_ok"] = any(answer(Qs, mods, i, p, j) for i, (mp, _) in enumerate(mods) if mp == p)
        rows.append(r)
    return rows


# ---------- reporte ----------

def pct(x):
    return f"{100 * x:5.1f}"


def report(res):
    mods = res["modulos"]
    rows = res["eval"]
    kn = [r for r in rows if r["pieza"]]
    un = [r for r in rows if not r["pieza"]]
    L = ["Piloto: el sistema transactivo como organizador de una flota de 24 módulos (propuesta_piloto_modulos.md).",
         f"Aprendizaje: {json.dumps(res['aprendizaje'])}",
         "Acierto de cada módulo en su evaluación: " + ", ".join(f"{m} {pct(a)}" for m, a in res["acierto_modulos_eval"].items())]
    L.append(f"\n[evaluación] {len(kn)} consultas conocidas, {len(un)} desconocidas (fondo de ojo, piel, mama)")
    L.append("  método       acierto · abstención en conocidas · acierto de lo respondido · abstención en desconocidas · módulos consultados (media)")
    verdict = {}
    for k in ("r1", "r2", "central", "compuerta", "todos", "azar"):
        acc = np.mean([r[f"{k}_ok"] for r in kn])
        ab = np.mean([r[k] is None for r in kn])
        ans = [r for r in kn if r[k] is not None]
        acc_ans = np.mean([r[f"{k}_ok"] for r in ans]) if ans else 0
        ab_u = np.mean([r[k] is None for r in un])
        cons = np.mean([r[f"{k}_consultados"] for r in rows]) if f"{k}_consultados" in rows[0] else float("nan")
        L.append(f"  {k:<11} {pct(acc)} · {pct(ab)} · {pct(acc_ans)} · {pct(ab_u)} · {cons:.1f}")
        verdict[k] = {"acierto": float(acc), "abstencion_desconocidas": float(ab_u), "consultados": float(cons) if cons == cons else None}
    L.append(f"  oráculo     {pct(np.mean([r['oraculo_ok'] for r in kn]))}")
    # preferencia por el mejor módulo
    accm = res["acierto_modulos_eval"]
    L.append("\n[mejor módulo] fracción de las consultas ruteadas a un módulo de su dominio que va al mejor de los dos")
    pref = {"r1": [], "r2": [], "central": [], "compuerta": [], "todos": []}
    for p in PIECES:
        pair = [m for m in mods if m.startswith(p + "/")]
        gap = abs(accm[pair[0]] - accm[pair[1]])
        best = max(pair, key=lambda m: accm[m])
        line = f"  {p:<11} {pair[0]} {pct(accm[pair[0]])} · {pair[1]} {pct(accm[pair[1]])} (diferencia {pct(gap)}) · "
        parts = []
        for k in pref:
            ws = [mods[r[k]] for r in kn if r["pieza"] == p and r[k] is not None and mods[r[k]].startswith(p + "/")]
            f = np.mean([w == best for w in ws]) if ws else float("nan")
            if gap >= 0.05:
                pref[k].append(f)
            parts.append(f"{k} {pct(f)}")
        L.append(line + " · ".join(parts) + ("" if gap >= 0.05 else "  (fuera del criterio)"))
    L.append("  media en dominios con diferencia >= 5 puntos: " + " · ".join(f"{k} {pct(np.nanmean(v))}" for k, v in pref.items()))
    verdict["al_mejor"] = {k: float(np.nanmean(v)) for k, v in pref.items()}
    e2 = res["E2"]
    L.append(f"\n[E2 · baja de {e2['retirado']}] consultas de pcb1: acierto {pct(np.mean([r['ok'] for r in e2['filas']]))} · "
             f"destinos {json.dumps({d: sum(r['destino'] == d for r in e2['filas']) for d in set(r['destino'] for r in e2['filas'])})}")
    L.append(f"  acierto de R2 en pcb1 antes de la baja: {pct(np.mean([r['r2_ok'] for r in kn if r['pieza'] == 'pcb1']))}")
    e1 = res["E1"]
    L.append("\n[E1 · alta de candle] tras n transacciones de candle: a un módulo de candle / abstención / acierto")
    for k in ("antes", "5", "10", "20", "40"):
        L.append(f"  {k:>5}: {pct(e1[k]['a_candle'])} / {pct(e1[k]['abstencion'])} / {pct(e1[k]['acierto'])}")
    L.append(f"  acierto de R2 en las otras piezas (sin candle en el aprendizaje): {pct(e1['otras_piezas_r2'])}")
    L.append(f"\n[criterio] {json.dumps(verdict)}")
    L.append(f"\nTiempo total: {res.get('segundos', 0) / 60:.0f} min")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
