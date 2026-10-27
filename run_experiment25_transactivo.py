"""
Experimento 25: la organización transactiva contra rivales federados y
descentralizados. Diseño y predicciones en propuesta_exp25_transactivo.md.

Un agente por dominio con su contenido (pozos de la corrida balanceada). Fase A:
128 consultas por dominio; cada una entra por un agente al azar y la gana el
especialista que reconoce con más fuerza (contenido, protocolo oficial). La
registran el de entrada y el ganador, y además cada otro agente con probabilidad
f, o solo los vecinos del de entrada en un anillo de radio r. Todos los brazos
descentralizados ven las mismas transacciones; cambia qué guardan y cómo leen.

Uso: python run_experiment25_transactivo.py
"""
import contextlib
import copy
import io
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
from associative_memory import HomoAssociativeMemory, DirectoryMemory  # noqa: E402
from stage5_fill import quantize_latent_global  # noqa: E402
from stage7_bidirectional import recognize_gated_right  # noqa: E402

OUT = ROOT / "results" / "experimento25"
CACHE_B = ROOT / "results" / "medico_balanceado" / "cache"
LEVELS = {"organos": "nivel2_tc_abdomen", "modalidad": "nivel1"}
ENCODERS = {"organos": ("encoder_tc_abdomen.pt", 11), "modalidad": ("encoder_nivel1.pt", None)}
CONDITIONS = [("f", 0.0), ("f", 1 / 16), ("f", 1 / 4), ("f", 1.0), ("anillo", 1), ("anillo", 2)]
N_A, N_TEST, SEED = 128, 300, 42


def unit(X):
    return X / (np.linalg.norm(X, axis=-1, keepdims=True) + 1e-12)


class Spec:
    """Especialista: memoria homo de contenido."""
    def __init__(self, fill, g):
        self.mem_dom_R = HomoAssociativeMemory(64, 32)
        for z in fill.reshape(-1, 64):
            self.mem_dom_R.register(quantize_latent_global(z, *g, 32))


class World:
    def __init__(self, level, names, fill, pa, test, g, rng):
        self.level, self.names, self.K, self.g = level, names, len(names), g
        self.fill, self.pa = fill, pa
        self.spec = {n: Spec(fill[n], g) for n in names}
        self.proto_own = {n: unit(fill[n].reshape(-1, 64)).mean(0) for n in names}
        self.test = {n: test[n][rng.permutation(len(test[n]))[:N_TEST]] for n in names}
        # transacciones: (cue con variantes, ganador, entrada); mismas para todos los brazos
        self.trans = []
        rng2 = np.random.RandomState(SEED)
        for j in range(max(len(pa[n]) for n in names)):
            for n in names:
                if j >= len(pa[n]):
                    continue
                zv = pa[n][j]
                zq = self.q(zv[0])
                sc = {m: recognize_gated_right(self.spec[m], zq) for m in names}
                if sum(sc.values()) == 0:
                    continue
                self.trans.append((zv, names.index(max(sc, key=sc.get)), int(rng2.randint(self.K))))

    def q(self, z):
        return quantize_latent_global(np.asarray(z, dtype=np.float32), *self.g, 32)

    def witnesses(self, cond, rng):
        """Para cada transacción, los agentes que la presencian."""
        kind, val = cond
        out = []
        for _zv, w, e in self.trans:
            s = {e, w}
            if kind == "f":
                s |= {a for a in range(self.K) if rng.rand() < val}
            else:
                s |= {(e + d) % self.K for d in range(-val, val + 1)}
            out.append(s)
        return out


# ---------- brazos descentralizados ----------

class Arm:
    """Base: cada agente guarda lo que presenció; el recorrido es el de route_transactive."""
    def __init__(self, world, wit, alive=None):
        self.w, self.K = world, world.K
        self.alive = set(range(self.K)) if alive is None else alive
        self.counts = np.zeros((self.K, self.K), dtype=int)       # counts[a, j]: transacciones ganadas por j que vio a
        for (zv, win, _e), s in zip(world.trans, wit):
            for a in s:
                self.counts[a, win] += 1
                self.store(a, zv, win)

    def known_by(self, a):
        c = self.counts[a]
        return [int(j) for j in np.argsort(-c) if c[j] > 0 and j != a]

    def route(self, z, entry):
        # Un agente ausente no se lee ni reenvía, pero puede ser la respuesta.
        summed, visited, queue = set(), set(), [entry]
        acc = self.empty()
        while queue:
            a = queue.pop(0)
            if a in visited:
                continue
            visited.add(a)
            for n in [a] + self.known_by(a):
                if n not in summed and n in self.alive:
                    summed.add(n)
                    acc = self.combine(acc, n, z)
            d = self.decide(acc)
            if d is not None:
                return d
            queue = [n for n in self.known_by(a) if n not in visited and n in self.alive] + queue
        return None


class MAEArm(Arm):
    def __init__(self, world, wit, reading="b1", alive=None):
        self.reading = reading
        self.dirs = [DirectoryMemory(64, 32, world.K) for _ in range(world.K)]
        super().__init__(world, wit, alive)

    def store(self, a, zv, win):
        for z in zv:
            self.dirs[a].register(self.w.q(z), win)

    def empty(self):
        return np.zeros(self.K) if self.reading == "b1" else np.full(self.K, -np.inf)

    def combine(self, acc, n, z):
        v = self.w.q(z)
        if self.reading == "b1":
            with contextlib.redirect_stdout(io.StringIO()):
                return acc + self.dirs[n].predict_tolerant(v, xi=0, mode="linear")
        return np.logaddexp(acc, e20.size_scores(self.dirs[n], v))

    def decide(self, acc):
        ok = acc.sum() > 0 if self.reading == "b1" else np.isfinite(acc).any()
        return int(np.argmax(acc)) if ok else None

    def score(self, z, entry):
        """Para lo ajeno: 1 si alguien del recorrido tiene soporte, 0 si no."""
        return 0.0 if self.route(z, entry) is None else 1.0

    def nbytes_per_trans(self):
        return 16 * 64          # 16 pistas cuantizadas de 64 niveles (1 byte cada uno)


class ProtoArm(Arm):
    def __init__(self, world, wit, alive=None):
        self.sum = np.zeros((world.K, world.K, 64))
        super().__init__(world, wit, alive)

    def store(self, a, zv, win):
        self.sum[a, win] += unit(zv).sum(0)

    def empty(self):
        return np.zeros((self.K, 64))

    def combine(self, acc, n, z):
        self._z = z
        return acc + self.sum[n]

    def decide(self, acc):
        known = np.where(np.linalg.norm(acc, axis=1) > 0)[0]
        if len(known) == 0:
            return None
        s = unit(acc[known]) @ unit(self._z)
        self._last = float(s.max())
        return int(known[s.argmax()])

    def score(self, z, entry):
        self.route(z, entry)
        return self._last

    def nbytes_per_trans(self):
        return 16 * 64 * 4


class KNNArm(Arm):
    def __init__(self, world, wit, alive=None):
        self.X = [[] for _ in range(world.K)]
        self.Y = [[] for _ in range(world.K)]
        super().__init__(world, wit, alive)
        self._cache = {}
        self.X = [unit(np.concatenate(x)) if x else np.zeros((0, 64)) for x in self.X]
        self.Y = [np.concatenate(y) if y else np.zeros(0, dtype=int) for y in self.Y]

    def store(self, a, zv, win):
        self.X[a].append(zv)
        self.Y[a].append(np.full(len(zv), win))

    def empty(self):
        return []

    def combine(self, acc, n, z):
        self._z = z
        return acc + [n]

    def decide(self, acc):
        key = tuple(sorted(acc))
        if key not in self._cache:
            self._cache = {key: (np.concatenate([self.X[n] for n in key]), np.concatenate([self.Y[n] for n in key]))}
        X, Y = self._cache[key]
        if len(X) == 0:
            return None
        s = X @ unit(self._z)
        nn = np.argsort(-s)[:5]
        self._last = float(s[nn].mean())
        return int(np.bincount(Y[nn], minlength=self.K).argmax())

    def score(self, z, entry):
        self.route(z, entry)
        return self._last

    def nbytes_per_trans(self):
        return 16 * 64 * 4


# ---------- cotas ----------

def gossip_rounds(K, n_messages):
    """Rondas de gossip de prototipos en anillo que caben en n_messages (2K mensajes por ronda)."""
    return int(min(np.ceil(K / 2), n_messages // (2 * K)))


def proto_predict(protos, known_idx, Z):
    P = unit(np.stack([protos[i] for i in known_idx]))
    S = unit(Z) @ P.T
    return np.array(known_idx)[S.argmax(1)], S.max(1)


def fedavg(world, rounds=50, lr=0.5, local_steps=5, seed=SEED):
    """Regresión logística federada; cliente k solo tiene datos de su dominio."""
    K = world.K
    rng = np.random.RandomState(seed)
    W = np.zeros((64, K))
    b = np.zeros(K)
    data = [unit(world.fill[n].reshape(-1, 64)) for n in world.names]
    for _ in range(rounds):
        Ws, bs = [], []
        for k in range(K):
            w, bb = W.copy(), b.copy()
            X = data[k][rng.permutation(len(data[k]))[:256]]
            Y = np.zeros((len(X), K))
            Y[:, k] = 1
            for _s in range(local_steps):
                L = X @ w + bb
                P = np.exp(L - L.max(1, keepdims=True))
                P /= P.sum(1, keepdims=True)
                G = (P - Y) / len(X)
                w -= lr * X.T @ G
                bb -= lr * G.sum(0)
            Ws.append(w)
            bs.append(bb)
        W, b = np.mean(Ws, 0), np.mean(bs, 0)
    return W, b


# ---------- pruebas ----------

def eval_routing(world, router, rng):
    rows = []
    for k, n in enumerate(world.names):
        for z in world.test[n]:
            entry = int(rng.randint(world.K - 1))
            entry = entry if entry < k else entry + 1                 # entrada distinta del especialista
            rows.append((k, router(z, entry)))
    ok = np.mean([d == k for k, d in rows])
    rej = np.mean([d is None for k, d in rows])
    return {"acierto": float(ok), "rechazo": float(rej), "falso": float(1 - ok - rej)}


def run_level(name):
    t0 = time.time()
    names, fill, pa, test = e20.load_pool(CACHE_B, LEVELS[name])
    allo = np.concatenate([fill[n][:, 0] for n in names])
    lo, hi = allo.min(0), allo.max(0)
    pad = 0.1 * (hi - lo)
    g = ((lo - pad).astype(np.float32), (hi + pad).astype(np.float32))
    rng = np.random.RandomState(SEED)
    world = World(name, names, fill, pa, test, g, rng)
    K = world.K
    res = {"nombres": names, "transacciones": len(world.trans), "condiciones": {}}
    # cotas, que no dependen de la visibilidad
    own = [world.proto_own[n] for n in names]
    W, b = fedavg(world)
    allX = unit(np.concatenate([fill[n].reshape(-1, 64) for n in names]))
    allY = np.concatenate([[k] * (fill[n].size // 64) for k, n in enumerate(names)])

    def central_knn(z, _e):
        s = allX @ unit(z)
        return int(np.bincount(allY[np.argsort(-s)[:5]], minlength=K).argmax())

    res["cotas"] = {
        "fedproto": eval_routing(world, lambda z, e: int(proto_predict(own, list(range(K)), z[None])[0][0]), np.random.RandomState(1)),
        "fedavg": eval_routing(world, lambda z, e: int(np.argmax(unit(z) @ W + b)), np.random.RandomState(1)),
        "oraculo_knn": eval_routing(world, central_knn, np.random.RandomState(1)),
    }
    res["comunicacion_cotas"] = {"fedproto_bytes": K * (K - 1) * 64 * 4, "fedavg_bytes": 50 * K * 2 * (64 * K + K) * 4}
    print(f"  {name}: cotas listas ({time.time() - t0:.0f} s)", flush=True)
    for cond in CONDITIONS:
        key = f"{cond[0]}={cond[1]:.4g}"
        wit = world.witnesses(cond, np.random.RandomState(SEED))
        n_reg = sum(len(s) for s in wit)
        arms = {"mae_b1": MAEArm(world, wit, "b1"), "mae_tamano": MAEArm(world, wit, "tamano"),
                "prototipos": ProtoArm(world, wit), "knn": KNNArm(world, wit)}
        T = gossip_rounds(K, n_reg)
        gossip_known = {a: [j for j in range(K) if min((a - j) % K, (j - a) % K) <= T] for a in range(K)}
        out = {"registros": int(n_reg), "rondas_gossip": T}
        for an, arm in arms.items():
            out[an] = eval_routing(world, arm.route, np.random.RandomState(1))
            out[an]["bytes_formacion"] = int(n_reg * arm.nbytes_per_trans())
        out["gossip"] = eval_routing(world, lambda z, e: int(proto_predict(own, gossip_known[e], z[None])[0][0]),
                                     np.random.RandomState(1))
        out["gossip"]["bytes_formacion"] = int(T * 2 * K * K * 64 * 4)
        if cond == ("f", 0.0):
            out["perdida"] = member_loss(world, wit, arms)
            out["ingreso"] = new_member(world, name, cond)
            out["ajeno"] = foreign(world, name, arms)
        res["condiciones"][key] = out
        print(f"  {name} {key}: " + " · ".join(f"{a} {100 * out[a]['acierto']:.1f}" for a in list(arms) + ["gossip"])
              + f" ({time.time() - t0:.0f} s)", flush=True)
    return res


def member_loss(world, wit, arms):
    """Se quita al especialista k: ¿las consultas de su dominio se ubican en k?"""
    out = {}
    for an, arm in arms.items():
        loc = rej = other = 0
        for k, n in enumerate(world.names):
            arm.alive = set(range(world.K)) - {k}
            try:
                for z in world.test[n][:60]:
                    entry = (k + 1) % world.K
                    d = arm.route(z, entry)
                    loc += d == k
                    rej += d is None
                    other += d is not None and d != k
            finally:
                arm.alive = set(range(world.K))
        tot = loc + rej + other
        out[an] = {"ubica_en_el_ausente": loc / tot, "rechaza": rej / tot, "manda_a_otro": other / tot}
    return out


def new_member(world, level_name, cond):
    """Un dominio ingresa después de la formación: se retira el último del llenado
    y de la fase A, se forma el sistema sin él y luego se agregan n transacciones
    nuevas de su dominio. Acierto de ruteo sobre sus imágenes de test."""
    names = world.names
    new = len(names) - 1
    base = [t for t in world.trans if t[1] != new]
    wins = [t for t in world.trans if t[1] == new]
    out = {}
    for n_new in (0, 8, 32, 128):
        trans = base + wins[:n_new]
        rng = np.random.RandomState(SEED)
        wit = [{e, w} for _zv, w, e in trans]
        sub = copy.copy(world)
        sub.trans = trans
        row = {}
        for an, cls in (("mae_b1", lambda: MAEArm(sub, wit, "b1")), ("prototipos", lambda: ProtoArm(sub, wit)),
                        ("knn", lambda: KNNArm(sub, wit))):
            arm = cls()
            hits = [arm.route(z, int(rng.randint(new))) == new for z in world.test[names[new]][:100]]
            row[an] = float(np.mean(hits))
        out[str(n_new)] = row
    return out


def foreign(world, level_name, arms):
    """Fondo de ojo (nunca registrado): rechazo a igual aceptación de lo propio."""
    if level_name == "modalidad":
        Zo = np.load(ROOT / "results" / "experimento20" / "cache" / "l1_retina.npy")
    else:
        enc = demo.Backbone(11).to(demo.DEV).eval()
        enc.load_state_dict(torch.load(CACHE_B / "encoder_tc_abdomen.pt", map_location=demo.DEV))
        x = np.concatenate([demo.data("retinamnist")[s][0] for s in ("train", "val", "test")])
        Zo = demo.latents(enc, [demo.to_pil(a) for a in x])
    Zo = Zo[:600]
    own = np.concatenate([world.test[n][:60] for n in world.names])
    entries = np.arange(len(own)) % world.K
    out = {}
    mae = arms["mae_b1"]
    acc_in = np.mean([mae.route(z, e) is not None for z, e in zip(own, entries)])
    out["mae_b1"] = {"acepta_propias": float(acc_in),
                     "rechaza_ajenas": float(np.mean([mae.route(z, 0) is None for z in Zo]))}
    for an in ("prototipos", "knn"):
        arm = arms[an]
        s_in = np.array([arm.score(z, e) for z, e in zip(own, entries)])
        s_out = np.array([arm.score(z, 0) for z in Zo])
        thr = np.quantile(s_in, 1 - acc_in)
        out[an] = {"acepta_propias": float(acc_in), "rechaza_ajenas": float(np.mean(s_out < thr))}
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "resultados.json"
    res = json.loads(path.read_text()) if path.exists() else {}
    for name in LEVELS:
        if name not in res:
            res[name] = run_level(name)
            path.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float))
    report(res)


def report(res):
    lines = ["Exp25: organización transactiva contra rivales, mismas transacciones. Acierto de ruteo (%)."]
    for lv, r in res.items():
        lines.append(f"\n[{lv}] agentes {len(r['nombres'])} · transacciones de fase A {r['transacciones']}")
        lines.append("  cotas: " + " · ".join(f"{k} {100 * v['acierto']:.1f}" for k, v in r["cotas"].items())
                     + f" · bytes FedProto {r['comunicacion_cotas']['fedproto_bytes']:,} · FedAvg {r['comunicacion_cotas']['fedavg_bytes']:,}")
        arms = ["mae_b1", "mae_tamano", "prototipos", "knn", "gossip"]
        lines.append(f"  {'condición':<12}" + "".join(f"{a:>22}" for a in arms))
        for key, c in r["condiciones"].items():
            lines.append(f"  {key:<12}" + "".join(
                f"{100 * c[a]['acierto']:>8.1f} r{100 * c[a]['rechazo']:4.1f} {c[a].get('bytes_formacion', 0) / 1e6:>5.1f}MB" for a in arms))
        c0 = r["condiciones"]["f=0"]
        lines.append("  pérdida de un miembro (f=0): " + " · ".join(
            f"{a}: ubica {100 * v['ubica_en_el_ausente']:.0f} / rechaza {100 * v['rechaza']:.0f} / otro {100 * v['manda_a_otro']:.0f}"
            for a, v in c0["perdida"].items()))
        lines.append("  ingreso de un miembro (f=0), acierto sobre el nuevo según transacciones nuevas: " + " · ".join(
            f"{n}: " + ", ".join(f"{a} {100 * v:.0f}" for a, v in row.items()) for n, row in c0["ingreso"].items()))
        lines.append("  lo ajeno (fondo de ojo, a igual aceptación de lo propio): " + " · ".join(
            f"{a} acepta {100 * v['acepta_propias']:.0f} / rechaza ajeno {100 * v['rechaza_ajenas']:.0f}" for a, v in c0["ajeno"].items()))
    text = "\n".join(lines)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
