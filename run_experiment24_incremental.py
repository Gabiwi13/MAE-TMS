"""
Experimento 24, prueba B: aprendizaje incremental por clases contra los métodos
actuales, sobre los mismos rasgos congelados y los mismos registros.

OrganAMNIST, 11 órganos en 4 tareas (3+3+3+2, en orden de etiqueta). Rasgos:
encoder del nivel 1 (ResNet18 de ImageNet congelado + PCA a 64; la PCA vio
imágenes de órganos sin etiquetas). Cada clase registra 328 imágenes de train
con sus 16 variantes; todos los métodos reciben exactamente esos vectores.

Métodos:
  memoria   un especialista homo por clase; acepta si contiene la pista en las
            64 coordenadas; entre los que contienen, principio de tamaño;
            si nadie contiene, se abstiene
  ncm       prototipo medio por clase, coseno (SimpleCIL)
  hdc       proyección aleatoria bipolar a 10 000, hipervector por clase (suma), coseno
  hopfield  recuperación Hopfield moderna sobre todos los registros, beta fija
  knn       5 vecinos por coseno sobre todos los registros
  ranpac    proyección aleatoria a 2000 + ReLU, regresión ridge sobre la Gram acumulada
  lineal    regresión logística entrenada tarea por tarea sin repaso (olvida)
  repaso    la misma, con un buffer de 20 registros originales por clase
Métricas: acierto tras cada tarea sobre las clases vistas, acierto final, olvido,
bytes de memoria, y para la abstención AURC (riesgo-cobertura) con la confianza
propia de cada método.

Predicción: la memoria no olvida, igual que ncm, hdc, hopfield y knn; menor
acierto que knn y ranpac; su posible ventaja es abstención integrada y tamaño fijo.

Uso: python run_experiment24_incremental.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_medico_demo as demo  # noqa: E402
from associative_memory import HomoAssociativeMemory  # noqa: E402
from stage5_fill import quantize_latent_global  # noqa: E402

OUT = ROOT / "results" / "experimento24"
CACHE = OUT / "cache"
ENC1 = ROOT / "results" / "medico_balanceado" / "cache" / "encoder_nivel1.pt"
TASKS = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10]]
N_PER_CLASS, SEED = 328, 42


def features():
    p = CACHE / "organos_nivel1.npz"
    if p.exists():
        z = np.load(p)
        return z["tr"], z["ytr"], z["te"], z["yte"]
    enc = demo.Backbone().to(demo.DEV).eval()
    enc.load_state_dict(torch.load(ENC1, map_location=demo.DEV))
    xt, yt = demo.data("organamnist")["train"]
    xs, ys = demo.data("organamnist")["test"]
    rng = np.random.RandomState(SEED)
    pick = np.concatenate([rng.permutation(np.where(yt[:, 0] == k)[0])[:N_PER_CLASS] for k in range(11)])
    tr = demo.latents(enc, [demo.to_pil(xt[i]) for i in pick], variants=True)      # (n, 16, 64)
    te = demo.latents(enc, [demo.to_pil(xs[i]) for i in range(len(xs))])
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez(p, tr=tr, ytr=yt[pick, 0], te=te, yte=ys[:, 0])
    return tr, yt[pick, 0], te, ys[:, 0]


def unit(X):
    return X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)


class Memoria:
    def __init__(self, g):
        self.g, self.mem, self.logsize = g, {}, {}

    def add(self, k, X):
        m = HomoAssociativeMemory(64, 32)
        for z in X:
            m.register(quantize_latent_global(z, *self.g, 32))
        cnt = np.zeros(64)
        for lv in range(32):
            cnt += m.recog_weights(np.full(64, lv)) > 0
        self.mem[k], self.logsize[k] = m, float(np.log(np.maximum(cnt, 1)).sum())

    def predict(self, Z):
        pred, conf = [], []
        for z in Z:
            zq = quantize_latent_global(z, *self.g, 32)
            cand = {k: -self.logsize[k] + np.log(np.mean(m.recog_weights(zq)))
                    for k, m in self.mem.items() if np.all(m.recog_weights(zq) > 0)}
            if cand:
                k = max(cand, key=cand.get)
                pred.append(k)
                conf.append(1.0 / len(cand) + 1e-6 * cand[k])     # menos candidatos, más confianza
            else:
                pred.append(-1)
                conf.append(-np.inf)
        return np.array(pred), np.array(conf)

    def nbytes(self):
        return len(self.mem) * 64 * 32 * 4


class Proto:
    def __init__(self, proj=None):
        self.proj, self.P = proj, {}

    def f(self, X):
        return np.sign(X @ self.proj) if self.proj is not None else X

    def add(self, k, X):
        self.P[k] = unit(self.f(X)).sum(0)

    def predict(self, Z):
        ks = sorted(self.P)
        S = unit(self.f(Z)) @ unit(np.stack([self.P[k] for k in ks])).T
        return np.array(ks)[S.argmax(1)], np.sort(S, 1)[:, -1] - np.sort(S, 1)[:, -2] if S.shape[1] > 1 else S[:, 0]

    def nbytes(self):
        d = self.proj.shape[1] if self.proj is not None else 64
        return len(self.P) * d * (1 if self.proj is not None else 4) + (self.proj.size // 8 if self.proj is not None else 0)


class Store:
    """kNN y Hopfield: guardan todos los registros."""
    def __init__(self, mode, beta=20.0):
        self.mode, self.beta, self.X, self.y = mode, beta, [], []

    def add(self, k, X):
        self.X.append(unit(X))
        self.y += [k] * len(X)

    def predict(self, Z):
        X, y = np.concatenate(self.X), np.array(self.y)
        ks = np.unique(y)
        pred, conf = [], []
        for i in range(0, len(Z), 512):
            S = unit(Z[i:i + 512]) @ X.T
            if self.mode == "knn":
                nn = np.argsort(-S, 1)[:, :5]
                votes = np.stack([np.bincount(np.searchsorted(ks, y[r]), minlength=len(ks)) for r in nn])
                pred.append(ks[votes.argmax(1)])
                conf.append(votes.max(1) / 5.0)
            else:
                A = np.exp(self.beta * (S - S.max(1, keepdims=True)))
                A /= A.sum(1, keepdims=True)
                L = np.stack([A[:, y == k].sum(1) for k in ks], 1)
                pred.append(ks[L.argmax(1)])
                conf.append(L.max(1))
        return np.concatenate(pred), np.concatenate(conf)

    def nbytes(self):
        return sum(x.size for x in self.X) * 4


class RanPAC:
    def __init__(self, d=2000, lam=1.0, seed=SEED):
        self.W = np.random.RandomState(seed).randn(64, d) / 8.0
        self.G, self.C, self.ks, self.lam = np.zeros((d, d)), {}, [], lam

    def h(self, X):
        return np.maximum(unit(X) @ self.W, 0)

    def add(self, k, X):
        H = self.h(X)
        self.G += H.T @ H
        self.C[k] = H.sum(0)
        self.ks.append(k)

    def predict(self, Z):
        Cm = np.stack([self.C[k] for k in self.ks], 1)
        Wo = np.linalg.solve(self.G + self.lam * np.eye(len(self.G)), Cm)
        S = self.h(Z) @ Wo
        srt = np.sort(S, 1)
        return np.array(self.ks)[S.argmax(1)], srt[:, -1] - (srt[:, -2] if S.shape[1] > 1 else 0)

    def nbytes(self):
        return self.W.size * 4 + self.G.size * 8 + len(self.C) * self.G.shape[0] * 8


class Linear:
    def __init__(self, replay=0):
        self.model, self.replay, self.buf = None, replay, {}
        self.seen = []

    def add_task(self, data):
        from sklearn.linear_model import SGDClassifier
        Xs, ys = [], []
        for k, X in data.items():
            Xs.append(unit(X))
            ys += [k] * len(X)
            self.buf[k] = unit(X[:: 16][: self.replay]) if self.replay else None
            self.seen.append(k)
        if self.replay:
            for k, B in self.buf.items():
                if k not in data and B is not None:
                    Xs.append(B)
                    ys += [k] * len(B)
        X, y = np.concatenate(Xs), np.array(ys)
        if self.model is None:
            self.model = SGDClassifier(loss="log_loss", random_state=SEED)
            self.model.partial_fit(X, y, classes=np.arange(11))
        for _ in range(5):
            self.model.partial_fit(X, y)

    def predict(self, Z):
        P = self.model.predict_proba(unit(Z))[:, self.seen]
        return np.array(self.seen)[P.argmax(1)], P.max(1)

    def nbytes(self):
        return 11 * 65 * 4 + sum(b.size * 4 for b in self.buf.values() if b is not None)


def aurc(correct, conf):
    """Área bajo la curva riesgo-cobertura (menor es mejor)."""
    order = np.argsort(-conf, kind="stable")
    c = correct[order].astype(float)
    risk = 1 - np.cumsum(c) / np.arange(1, len(c) + 1)
    return float(risk.mean())


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    tr, ytr, te, yte = features()
    allo = tr[:, 0]
    lo, hi = allo.min(0), allo.max(0)
    pad = 0.1 * (hi - lo)
    g = ((lo - pad).astype(np.float32), (hi + pad).astype(np.float32))
    proj = np.random.RandomState(SEED).randn(64, 10000)
    methods = {"memoria": Memoria(g), "ncm": Proto(), "hdc": Proto(proj), "hopfield": Store("hopfield"),
               "knn": Store("knn"), "ranpac": RanPAC(), "lineal": Linear(0), "repaso": Linear(20)}
    hist = {m: [] for m in methods}
    per_class_after = {m: {} for m in methods}
    seen = []
    final = {}
    for t, task in enumerate(TASKS):
        data = {k: tr[ytr == k].reshape(-1, 64) for k in task}
        seen += task
        mask = np.isin(yte, seen)
        for name, m in methods.items():
            if isinstance(m, Linear):
                m.add_task(data)
            else:
                for k, X in data.items():
                    m.add(k, X)
            pred, conf = m.predict(te[mask])
            correct = pred == yte[mask]
            hist[name].append(float(correct.mean()))
            per_class_after[name][t] = {int(k): float(correct[yte[mask] == k].mean()) for k in seen}
            if t == len(TASKS) - 1:
                answered = pred >= 0
                final[name] = {"acierto": float(correct.mean()), "aurc": aurc(correct, conf),
                               "cobertura_propia": float(answered.mean()),
                               "acierto_respondido": float(correct[answered].mean()) if answered.any() else float("nan"),
                               "bytes": int(m.nbytes())}
        print(f"  tarea {t + 1}: " + " · ".join(f"{n} {100 * h[-1]:.1f}" for n, h in hist.items()), flush=True)
    forget = {}
    for name in methods:
        f = []
        for k in TASKS[0] + TASKS[1] + TASKS[2]:
            best = max(per_class_after[name][t][k] for t in range(len(TASKS) - 1) if k in per_class_after[name][t])
            f.append(best - per_class_after[name][len(TASKS) - 1][k])
        forget[name] = float(np.mean(f))
    res = {"historia": hist, "final": final, "olvido": forget}
    (OUT / "incremental.json").write_text(json.dumps(res, indent=1))
    lines = ["Exp24 B: incremental por clases, 11 órganos en 4 tareas, mismos rasgos y registros (328 x 16 por clase).",
             f"{'método':<10}{'final':>8}{'medio':>8}{'olvido':>8}{'AURC':>8}{'cubre':>8}{'resp.':>8}{'bytes':>12}"]
    for name in methods:
        fi = final[name]
        lines.append(f"{name:<10}{100 * fi['acierto']:>8.1f}{100 * np.mean(hist[name]):>8.1f}{100 * forget[name]:>8.1f}"
                     f"{100 * fi['aurc']:>8.2f}{100 * fi['cobertura_propia']:>8.1f}{100 * fi['acierto_respondido']:>8.1f}{fi['bytes']:>12,}")
    lines.append("\nAcierto tras cada tarea (sobre las clases vistas): " + " | ".join(
        f"{n}: " + " → ".join(f"{100 * h:.1f}" for h in hh) for n, hh in hist.items()))
    text = "\n".join(lines)
    (OUT / "incremental_resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
