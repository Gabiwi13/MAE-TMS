"""
Experimento 29: la demencia semántica como pérdida de conteos.
Diseño, predicciones, criterio y decisiones del paso 0 en propuesta_exp29_demencia_semantica.md.

Ambiente de Rogers et al. 2004 (Figura 3) con frecuencia x tipicidad. Cuatro modelos:
MAE (HeteroAssociativeMemory oficial; daño = adelgazar conteos), PDP recurrente
(daño = quitar pesos), MINERVA 2 y vecino más cercano (daño = borrar rasgos).
Tareas: denominación (visual -> nombre) y dibujo (nombre -> visual).

Uso:
  python run_experiment29_demencia_semantica.py --verificar   # sin daño, una semilla
  python run_experiment29_demencia_semantica.py               # barrido completo
  python run_experiment29_demencia_semantica.py --report-only
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

torch.set_num_threads(2)
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from hetero_memory import HeteroAssociativeMemory  # noqa: E402

OUT = ROOT / "results" / "experimento29"
SEEDS = tuple(range(10))
# Rejilla de la propuesta (0 a 0.9 de 0.05 en 0.05) más puntos finos abajo, donde la MAE pierde el nombre.
LEVELS = (0.0, 0.01, 0.02, 0.03, 0.04, 0.075) + tuple(round(0.05 * k, 2) for k in range(1, 19))
LESIONS = 10            # la propuesta pedía 50; se bajó por el costo de la MAE (292 ms por recall)
MAE_TRIALS = 2          # la propuesta pedía 10
FREQ_HIGH = 4
CATS = ["birds", "mammals", "fruits", "vehicles", "household", "tools"]
LIVING = {"birds", "mammals", "fruits"}

# Prototipos de la Figura 3 de Rogers 2004 (lectura en rogers2004_especificacion.md).
VIS = {
    "birds":     "+" * 8 + "+" * 6 + "0" * 6 + "0" * 12 + "--" + "----" + "----" + "-" * 22,
    "mammals":   "+" * 8 + "0" * 6 + "+" * 6 + "0" * 12 + "--" + "----" + "----" + "-" * 22,
    "vehicles":  "-" * 32 + "++" + "++++" + "0000" + "0" * 22,
    "household": "-" * 32 + "++" + "0000" + "0000" + "0" * 22,
    "tools":     "-" * 32 + "++" + "0000" + "++++" + "0" * 22,
    "fruits":    "-" * 32 + "++" + "0000" + "++00" + "0" * 22,
}
PER = {
    "birds":     "+" * 5 + "+" * 5 + "0" * 5 + "0" * 16 + "-" + "----" + "-" * 25,
    "mammals":   "+" * 5 + "0" * 5 + "+" * 5 + "0" * 16 + "-" + "----" + "-" * 25,
    "vehicles":  "-" * 31 + "+" + "++++" + "0" * 25,
    "household": "-" * 31 + "+" + "0000" + "0" * 25,
    "tools":     "-" * 31 + "+" + "0000" + "0" * 25,
    "fruits":    "-" * 5 + "+----" + "-" * 5 + "0" * 16 + "+" + "----" + "0" * 25,
}
FUN = {
    "birds":     "+++" + "+++" + "00" + "0" * 8 + "---" + "-" * 13,
    "mammals":   "+++" + "000" + "++" + "0" * 8 + "---" + "-" * 13,
    "vehicles":  "-" * 16 + "+++" + "0" * 13,
    "household": "-" * 16 + "+00" + "0" * 13,
    "tools":     "-" * 16 + "+0+" + "0" * 13,
    "fruits":    "---" + "---" + "+-" + "0" * 8 + "--+" + "0" * 13,
}
ENC = {
    "birds":     "+-+-----" + "0" * 10,
    "mammals":   "+--+----" + "0" * 10,
    "vehicles":  "-+--+---" + "0" * 10,
    "household": "-+---+--" + "0" * 10,
    "tools":     "-+----+-" + "0" * 10,
    "fruits":    "+------+" + "000000++++",
}
SPECIFIC = {
    "birds": ["chicken", "raven", "swan", "ostrich", "penguin"],
    "mammals": ["cat", "dog", "mouse", "goat", "pig"],
    "vehicles": ["car", "lorry", "boat", "sledge", "train"],
    "tools": ["hammer", "screwdriver", "wrench", "saw", "drill"],
    "household": ["iron", "cup", "brush", "blanket", "hose", "suitcase", "kettle", "objeto8"],
    "fruits": ["apple", "lemon", "peach", "strawberry", "kiwi", "banana", "pear", "pineapple"],
}
GENERAL = {"birds": "bird", "mammals": "animal", "vehicles": "vehicle", "tools": "tool"}
SUPER = {"birds": {"bird", "animal"}, "mammals": {"animal"}, "vehicles": {"vehicle"},
         "tools": {"tool"}, "household": set(), "fruits": set()}
NAMES = [n for c in CATS for n in SPECIFIC[c]] + ["bird", "animal", "vehicle", "tool"]
assert len(NAMES) == 40 and len(set(NAMES)) == 40
NV, NB = 64, 111 + 40


# ---------------- ambiente ----------------

def sample_pattern(proto, rng, minus_on=0.0):
    p = np.array([{"+": 0.8, "0": 0.2, "-": minus_on}[s] for s in proto])
    return (rng.random(len(proto)) < p).astype(np.int8)


def environment(seed):
    """48 ítems: visual (64), verbal sin nombres (111), índice de nombre, categoría, frecuencia."""
    rng = np.random.default_rng(seed)
    items = []
    for c in CATS:
        seen = set()
        made = []
        while len(made) < 8:
            v = sample_pattern(VIS[c], rng)
            mo = 0.2 if c == "fruits" else 0.0
            b = np.concatenate([sample_pattern(PER[c], rng, mo), sample_pattern(FUN[c], rng, mo),
                                sample_pattern(ENC[c], rng, mo)])
            key = (v.tobytes(), b.tobytes())
            if key in seen:
                continue
            seen.add(key)
            made.append((v, b))
        high = set(rng.permutation(8)[:4].tolist())
        for k, (v, b) in enumerate(made):
            name = SPECIFIC[c][k] if k < len(SPECIFIC[c]) else GENERAL[c]
            items.append({"cat": c, "visual": v, "verbal": b, "name": NAMES.index(name),
                          "specific": k < len(SPECIFIC[c]), "freq": FREQ_HIGH if k in high else 1})
    # Tipicidad: fracción de rasgos visuales iguales al valor modal de la categoría.
    for c in CATS:
        group = [it for it in items if it["cat"] == c]
        mode = (np.mean([it["visual"] for it in group], 0) >= 0.5).astype(np.int8)
        for it in group:
            it["typ"] = float(np.mean(it["visual"] == mode))
    # Tipo de rasgo visual por ítem (Rogers 2004, p. 226).
    for it in items:
        same = np.mean([o["visual"] for o in items if o["cat"] == it["cat"]], 0)
        dom = LIVING if it["cat"] in LIVING else set(CATS) - LIVING
        other = np.mean([o["visual"] for o in items if o["cat"] in dom and o["cat"] != it["cat"]], 0)
        it["ftype"] = np.where((same > 0.5) & (other > 0.5), 0, np.where(same > 0.5, 1, 2))
    return items


def verbal_full(it):
    names = np.zeros(40, dtype=np.int8)
    names[it["name"]] = 1
    return np.concatenate([it["verbal"], names])


def test_items(items):
    return [i for i, it in enumerate(items) if it["specific"] and it["cat"] != "fruits"]


def classify(items, i, name):
    """correcto, omision, superordinado, semantico, entre_dominios."""
    if name is None:
        return "omision"
    it = items[i]
    if name == it["name"]:
        return "correcto"
    word = NAMES[name]
    if word in SUPER[it["cat"]]:
        return "superordinado"
    owner = next(c for c in CATS if word in SPECIFIC[c] or GENERAL.get(c) == word)
    return "semantico" if (owner in LIVING) == (it["cat"] in LIVING) else "entre_dominios"


# ---------------- MAE ----------------

class MAE:
    def __init__(self, items):
        self.mem = HeteroAssociativeMemory(n=NB, m=2, p=NV, q=2)
        for it in items:
            for _ in range(it["freq"]):
                self.mem.register(verbal_full(it).astype(float), it["visual"].astype(float))
        self.base = self.mem._relation.copy()

    def lesion(self, d, rng):
        rel = self.base.copy()
        m, q = self.mem.m, self.mem.q
        inner = rel[:, :, :m, :q]
        rel[:, :, :m, :q] = rng.binomial(inner, 1.0 - d) if d > 0 else inner
        self.mem._relation = rel
        self.mem._updated = False

    def name(self, items, i, trials):
        """Lecturas (a) por recall, una por ensayo, y (b) por proyección."""
        cue = items[i]["visual"].astype(float)
        out_a = []
        proj = None
        for _ in range(trials):
            r_q, rec, _w, proj, _s = self.mem.recall_from_right(cue)
            if not rec:
                out_a.append(None)
                continue
            on = [k for k in range(40) if r_q[111 + k] == 1]
            out_a.append(max(on, key=lambda k: proj[111 + k, 1]) if on else None)
        tot = proj.sum(1)
        if np.any(tot == 0):
            out_b = None
        else:
            act = proj[111:, 1] / tot[111:]
            out_b = int(act.argmax()) if act.max() > 0.5 else None
        return out_a, out_b

    def draw(self, items, i):
        cue = np.full(NB, np.nan)
        cue[111 + items[i]["name"]] = 1.0
        r_q, rec, *_ = self.mem.recall_from_left(cue)
        return (r_q == 1).astype(np.int8) if rec else np.zeros(NV, np.int8)


# ---------------- PDP ----------------

class PDP(torch.nn.Module):
    def __init__(self, seed):
        super().__init__()
        g = torch.Generator().manual_seed(seed)
        init = lambda a, b: torch.nn.Parameter(torch.randn(a, b, generator=g) * 0.1)
        self.vh, self.hv = init(NV, 64), init(64, NV)
        self.bh, self.hb = init(NB, 64), init(64, NB)
        self.hh = init(64, 64)
        self.masks = None

    def w(self, name):
        p = getattr(self, name)
        return p if self.masks is None else p * self.masks[name]

    def run(self, clamp_v, clamp_b, mask_v, mask_b, steps_clamped=3, steps_free=2, steps_target=2):
        n = clamp_v.shape[0]
        rest = torch.sigmoid(torch.tensor(-2.0))
        v = torch.full((n, NV), float(rest)); b = torch.full((n, NB), float(rest))
        h = torch.full((n, 64), float(rest))
        outs = []
        for t in range(steps_clamped + steps_free + steps_target):
            if t < steps_clamped:
                v = torch.where(mask_v, clamp_v, v); b = torch.where(mask_b, clamp_b, b)
            h_new = torch.sigmoid(v @ self.w("vh") + b @ self.w("bh") + h @ self.w("hh") - 2)
            v = torch.sigmoid(h @ self.w("hv") - 2)
            b = torch.sigmoid(h @ self.w("hb") - 2)
            h = h_new
            if t >= steps_clamped + steps_free:
                outs.append((v, b))
        return outs

    def patterns(self, items, rng):
        """Entradas visual, verbal sin nombres y nombre; blanco = todas las visibles."""
        cv, cb, mv, mb, tv, tb = [], [], [], [], [], []
        zero_v, zero_b = np.zeros(NV), np.zeros(NB)
        mvis = np.ones(NV, bool); mnone_v = np.zeros(NV, bool)
        mverb = np.r_[np.ones(111, bool), np.zeros(40, bool)]
        mname = np.r_[np.zeros(111, bool), np.ones(40, bool)]
        mnone_b = np.zeros(NB, bool)

        def add(it, kind, name=None):
            vf = verbal_full(it)
            if kind == "v":
                cv.append(it["visual"]); cb.append(zero_b); mv.append(mvis); mb.append(mnone_b)
            elif kind == "b":
                cv.append(zero_v); cb.append(vf); mv.append(mnone_v); mb.append(mverb)
            else:
                nm = np.zeros(NB); nm[111 + name] = 1
                cv.append(zero_v); cb.append(nm); mv.append(mnone_v); mb.append(mname)
            tv.append(it["visual"]); tb.append(vf)

        for it in items:
            for _ in range(it["freq"]):
                add(it, "v"); add(it, "b")
                if it["specific"]:
                    add(it, "n", it["name"])
        for word in ("bird", "animal", "vehicle", "tool"):
            members = [it for it in items if (word == "animal" and it["cat"] in ("birds", "mammals"))
                       or GENERAL.get(it["cat"]) == word]
            w = np.array([it["freq"] for it in members], float)
            add(members[rng.choice(len(members), p=w / w.sum())], "n", NAMES.index(word))
        f = lambda a, dt: torch.tensor(np.array(a), dtype=dt)
        return (f(cv, torch.float32), f(cb, torch.float32), f(mv, torch.bool), f(mb, torch.bool),
                f(tv, torch.float32), f(tb, torch.float32))

    def fit(self, items, seed, max_epochs=2000):
        rng = np.random.default_rng(seed)
        opt = torch.optim.AdamW(self.parameters(), lr=0.005, weight_decay=0.001)
        for ep in range(1, max_epochs + 1):
            cv, cb, mv, mb, tv, tb = self.patterns(items, rng)
            outs = self.run(cv, cb, mv, mb)
            loss = sum(((v - tv) ** 2).sum() + ((b - tb) ** 2).sum() for v, b in outs) / len(cv)
            opt.zero_grad(); loss.backward(); opt.step()
            if ep % 50 == 0 and self.intact_ok(items):
                return ep
        return max_epochs

    def settle(self, clamp_v, clamp_b, mask_v, mask_b):
        with torch.no_grad():
            return self.run(clamp_v, clamp_b, mask_v, mask_b, 3, 10, 1)[-1]

    def name_all(self, items, idx):
        cv = torch.tensor(np.array([items[i]["visual"] for i in idx]), dtype=torch.float32)
        z = torch.zeros(len(idx), NB)
        _v, b = self.settle(cv, z, torch.ones(len(idx), NV, dtype=torch.bool),
                            torch.zeros(len(idx), NB, dtype=torch.bool))
        act = b[:, 111:].numpy()
        return [int(a.argmax()) if a.max() > 0.5 else None for a in act]

    def draw_all(self, items, idx):
        z = torch.zeros(len(idx), NV)
        nb = torch.zeros(len(idx), NB)
        for r, i in enumerate(idx):
            nb[r, 111 + items[i]["name"]] = 1
        mb = torch.zeros(len(idx), NB, dtype=torch.bool); mb[:, 111:] = True
        v, _b = self.settle(z, nb, torch.zeros(len(idx), NV, dtype=torch.bool), mb)
        return (v.numpy() > 0.5).astype(np.int8)

    def intact_ok(self, items):
        idx = test_items(items)
        names = self.name_all(items, idx)
        acc = np.mean([n == items[i]["name"] for n, i in zip(names, idx)])
        dr = self.draw_all(items, idx)
        dacc = np.mean([np.mean(d == items[i]["visual"]) for d, i in zip(dr, idx)])
        return acc >= 0.95 and dacc >= 0.90

    def lesion(self, d, rng):
        self.masks = {k: torch.tensor(rng.random(getattr(self, k).shape) >= d, dtype=torch.float32)
                      for k in ("vh", "hv", "bh", "hb", "hh")}


# ---------------- MINERVA 2 y vecino más cercano ----------------

def pm(x):
    return 2.0 * x.astype(float) - 1.0


def names_01(it):
    """Nombres como +1 (presente) y 0 (ausente, sin opinión), como los rasgos irrelevantes de MINERVA."""
    v = np.zeros(40)
    v[it["name"]] = 1.0
    return v


class Minerva:
    def __init__(self, items):
        rows = []
        for it in items:
            vec = np.concatenate([pm(it["visual"]), pm(it["verbal"]), names_01(it)])
            rows += [vec] * it["freq"]
        self.base = np.array(rows)
        self.T = self.base

    def lesion(self, d, rng):
        self.T = np.where(rng.random(self.base.shape) < d, 0.0, self.base)

    def echo(self, probe):
        nrel = np.maximum(((probe != 0)[None] | (self.T != 0)).sum(1), 1)
        s = (self.T @ probe) / nrel
        a = s ** 3
        den = np.abs(a).sum()
        return (a @ self.T) / den if den > 0 else np.zeros(self.T.shape[1])

    def name(self, items, i):
        probe = np.zeros(NV + NB); probe[:NV] = pm(items[i]["visual"])
        e = self.echo(probe)[NV + 111:]
        return int(e.argmax()) if e.max() > 0 else None

    def draw(self, items, i):
        probe = np.zeros(NV + NB); probe[NV + 111 + items[i]["name"]] = 1.0
        return (self.echo(probe)[:NV] > 0).astype(np.int8)


class Nearest:
    def __init__(self, items):
        self.base = np.array([np.concatenate([pm(it["visual"]), pm(verbal_full(it))]) for it in items])
        self.S = self.base

    def lesion(self, d, rng):
        self.S = np.where(rng.random(self.base.shape) < d, 0.0, self.base)

    def name(self, items, i):
        p = pm(items[i]["visual"])
        V = self.S[:, :NV]
        cos = (V @ p) / (np.linalg.norm(V, axis=1) * np.linalg.norm(p) + 1e-12)
        j = int(cos.argmax())
        if cos[j] < 0.5:
            return None
        on = np.where(self.S[j, NV + 111:] > 0)[0]
        return int(on[0]) if len(on) else None

    def draw(self, items, i):
        name = items[i]["name"]
        owners = np.where(self.S[:, NV + 111 + name] > 0)[0]
        return (self.S[owners[0], :NV] > 0).astype(np.int8) if len(owners) else np.zeros(NV, np.int8)


# ---------------- medidas ----------------

def draw_stats(items, i, drawn):
    """Omisiones por tipo sobre los rasgos blanco e intrusiones por tipo sobre los no blanco."""
    tgt = items[i]["visual"].astype(bool)
    ft = items[i]["ftype"]
    out = {}
    for k, label in enumerate(("dominio", "categoria", "distintivo")):
        t = tgt & (ft == k); nt = ~tgt & (ft == k)
        out[f"omis_{label}"] = (int((t & (drawn == 0)).sum()), int(t.sum()))
        out[f"intr_{label}"] = (int((nt & (drawn == 1)).sum()), int(nt.sum()))
    return out


def run_seed(seed, levels, lesions, mae_trials, verbose=True):
    items = environment(seed)
    idx = test_items(items)
    t0 = time.time()
    torch.manual_seed(seed)
    pdp = PDP(seed)
    epochs = pdp.fit(items, seed)
    mae, mnv, nn_ = MAE(items), Minerva(items), Nearest(items)
    if verbose:
        print(f"  semilla {seed}: PDP {epochs} épocas ({time.time() - t0:.0f} s)", flush=True)
    rng = np.random.default_rng(1000 + seed)
    rows = []
    for d in levels:
        for les in range(lesions if d > 0 else 1):
            mae.lesion(d, rng); mnv.lesion(d, rng); nn_.lesion(d, rng)
            pdp.lesion(d, rng)
            pdp_names = pdp.name_all(items, idx)
            pdp_draws = pdp.draw_all(items, idx)
            for r, i in enumerate(idx):
                a, b = mae.name(items, i, mae_trials)
                resp = {"mae": a, "mae_proy": [b], "pdp": [pdp_names[r]],
                        "minerva": [mnv.name(items, i)], "vecino": [nn_.name(items, i)]}
                draws = {"mae": mae.draw(items, i), "pdp": pdp_draws[r],
                         "minerva": mnv.draw(items, i), "vecino": nn_.draw(items, i)}
                rows.append({"semilla": seed, "d": d, "lesion": les, "item": i,
                             "resp": {k: [None if x is None else int(x) for x in v] for k, v in resp.items()},
                             "dibujo": {k: draw_stats(items, i, v) for k, v in draws.items()}})
        if verbose:
            print(f"    d = {d:.2f} ({time.time() - t0:.0f} s)", flush=True)
    meta = {"semilla": seed, "pdp_epocas": epochs,
            "items": [{"cat": it["cat"], "name": it["name"], "freq": it["freq"], "typ": it["typ"],
                       "specific": it["specific"]} for it in items]}
    return meta, rows


def verify():
    items = environment(0)
    idx = test_items(items)
    mae = MAE(items)
    t0 = time.time()
    res = [mae.name(items, i, 3) for i in idx]
    tm = (time.time() - t0) / (3 * len(idx))
    acc_a = np.mean([np.mean([x == items[i]["name"] for x in a]) for (a, _b), i in zip(res, idx)])
    acc_b = np.mean([b == items[i]["name"] for (_a, b), i in zip(res, idx)])
    dr = [np.mean(mae.draw(items, i) == items[i]["visual"]) for i in idx]
    print(f"MAE sin daño: denominación (a) recall {100 * acc_a:.1f} %, (b) proyección {100 * acc_b:.1f} %, "
          f"dibujo {100 * np.mean(dr):.1f} % de rasgos; {tm * 1000:.0f} ms por recall")
    torch.manual_seed(0)
    pdp = PDP(0)
    ep = pdp.fit(items, 0)
    names = pdp.name_all(items, idx)
    dacc = np.mean([np.mean(d == items[i]["visual"]) for d, i in zip(pdp.draw_all(items, idx), idx)])
    print(f"PDP sin daño ({ep} épocas): denominación {100 * np.mean([n == items[i]['name'] for n, i in zip(names, idx)]):.1f} %, "
          f"dibujo {100 * dacc:.1f} %")
    for label, model in (("MINERVA 2", Minerva(items)), ("vecino", Nearest(items))):
        acc = np.mean([model.name(items, i) == items[i]["name"] for i in idx])
        dacc = np.mean([np.mean(model.draw(items, i) == items[i]["visual"]) for i in idx])
        print(f"{label} sin daño: denominación {100 * acc:.1f} %, dibujo {100 * dacc:.1f} %")
    print("tipicidad media", np.mean([it["typ"] for it in items]), "· rasgos por tipo (ítem 0)",
          np.bincount(items[idx[0]]["ftype"], minlength=3).tolist())


def main(args):
    OUT.mkdir(parents=True, exist_ok=True)
    for seed in args.semillas:
        meta, r = run_seed(seed, LEVELS, args.lesiones, args.ensayos)
        (OUT / f"filas_s{seed}.json").write_text(json.dumps({"metas": [meta], "filas": r}))


def report():
    from exp29_reporte import report as rep
    rep(OUT)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--verificar", action="store_true")
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--lesiones", type=int, default=LESIONS)
    ap.add_argument("--ensayos", type=int, default=MAE_TRIALS)
    ap.add_argument("--semillas", type=int, nargs="+", default=list(SEEDS))
    a = ap.parse_args()
    if a.verificar:
        verify()
    elif a.report_only:
        report()
    else:
        main(a)
