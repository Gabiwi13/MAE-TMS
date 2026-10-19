"""
Demo industrial: el sistema EAM-TMS sobre VisA (Amazon, CC BY 4.0), partición 1cls.
Diseño fijado en propuesta_demo_industrial.md.

  nivel 1  ruteo por pieza (12 agentes), protocolo de run_medico_demo.Level.
           ResNet18 de ImageNet congelado + PCA a 64 sobre todo el train.
  nivel 2  un especialista por pieza lleno solo con normales; falla = rechazo.
           G1 latentes del nivel 1 · G2 PCA por pieza · P parches estilo PatchCore.
Detectores sobre los mismos latentes (kNN, Mahalanobis), con el umbral fijado en
normales de calibración (la fase A, que el especialista nunca registró) a la
misma aceptación que la memoria.

Uso:
  python run_industrial_demo.py --visa C:/Users/aq99l/Datasets/VisA
  python run_industrial_demo.py --report-only
"""
import argparse
import contextlib
import csv
import io
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from scipy.stats import rankdata

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_medico_demo as demo  # noqa: E402
from associative_memory import HomoAssociativeMemory  # noqa: E402
from stage5_fill import augment_variants  # noqa: E402

SMOKE = os.environ.get("IND_SMOKE") == "1"
OUT = ROOT / "results" / ("industrial_prueba" if SMOKE else "industrial")
CACHE = OUT / "cache"            # fuera de git
PIECES = ["candle", "capsules", "cashew", "chewinggum", "fryum", "macaroni1", "macaroni2",
          "pcb1", "pcb2", "pcb3", "pcb4", "pipe_fryum"]
if SMOKE:
    PIECES = ["candle", "pcb1", "pcb2"]
N_REG, N_FILL = (40, 24) if SMOKE else (450, 270)   # N = max(328, 450); 60 % llenado
SIZE, Q, SEED, PAD = 224, 32, 42, 0.1
MIN_TYPE = 10
DEV = demo.DEV


# ---------- imágenes ----------

def load_img(path):
    im = Image.open(path)
    im.draft("RGB", (SIZE * 2, SIZE * 2))
    return np.asarray(im.convert("RGB").resize((SIZE, SIZE), Image.BILINEAR))


def backbone():
    return demo.Backbone().to(DEV).eval()


def feats512(net, imgs, variants=False):
    """(n, 512) o (n, 16, 512)."""
    out = []
    step = 16 if variants else 128
    with torch.no_grad():
        for i in range(0, len(imgs), step):
            pil = [Image.fromarray(a) for a in imgs[i:i + step]]
            if variants:
                pil = [v for im in pil for v in augment_variants(im)]
            f = net.features(torch.stack([demo.TF(p) for p in pil]).to(DEV)).flatten(1).cpu().numpy()
            out.append(f.reshape(-1, 16, 512) if variants else f)
    return np.concatenate(out)


def patch_feats(net, imgs):
    """(n, 784, 384): capas 2 y 3, promedio local 3 x 3 (PatchCore)."""
    body = net.features
    out = []
    with torch.no_grad():
        for i in range(0, len(imgs), 32):
            x = torch.stack([demo.TF(Image.fromarray(a)) for a in imgs[i:i + 32]]).to(DEV)
            x = body[3](body[2](body[1](body[0](x))))
            l2 = body[5](body[4](x))
            l3 = body[6](l2)
            l3 = F.interpolate(l3, size=l2.shape[-2:], mode="bilinear", align_corners=False)
            f = F.avg_pool2d(torch.cat([l2, l3], 1), 3, 1, 1)
            out.append(f.flatten(2).transpose(1, 2).cpu().numpy())
    return np.concatenate(out)


def prepare(visa):
    """Por pieza: imágenes de registro y de test, tipos de falla y rasgos 512 de todo el train."""
    path = CACHE / "imagenes.npz"
    if path.exists():
        return
    rows = list(csv.DictReader(open(Path(visa) / "split_csv" / "1cls.csv", newline="")))
    net = backbone()
    store = {}
    for p in PIECES:
        types = {r["image"]: r["label"] for r in csv.DictReader(open(Path(visa) / p / "image_anno.csv", newline=""))}
        tr = [r["image"] for r in rows if r["object"] == p and r["split"] == "train"]
        te = [r for r in rows if r["object"] == p and r["split"] == "test"]
        if SMOKE:
            te = te[:20] + te[-20:]
        imgs_tr = [load_img(Path(visa) / f) for f in tr]
        store[f"f512all_{p}"] = feats512(net, imgs_tr)
        pick = np.random.RandomState(SEED).permutation(len(tr))[:N_REG]
        store[f"reg_{p}"] = np.stack([imgs_tr[i] for i in pick])
        store[f"test_{p}"] = np.stack([load_img(Path(visa) / r["image"]) for r in te])
        store[f"testy_{p}"] = np.array([int(r["label"] == "anomaly") for r in te])
        store[f"testtipo_{p}"] = np.array([types[r["image"]] if r["label"] == "anomaly" else "" for r in te])
        print(f"  {p}: train {len(tr)}, registro {len(pick)}, test {len(te)} "
              f"({store[f'testy_{p}'].sum()} fallas)", flush=True)
    np.savez(path, **store)


_IMG = None


def imgs():
    global _IMG
    if _IMG is None:
        _IMG = dict(np.load(CACHE / "imagenes.npz", allow_pickle=False))
    return _IMG


def pca(X, k=64):
    X = np.asarray(X, dtype=np.float64)
    mu = X.mean(0)
    w, v = np.linalg.eigh(np.cov((X - mu).T))
    return mu, v[:, np.argsort(-w)[:k]].T


def proj(P, X):
    mu, V = P
    return ((np.asarray(X, dtype=np.float64) - mu) @ V.T).astype(np.float32)


def global_feats():
    """Rasgos 512: registro con 16 variantes, test sin variantes. Cacheado."""
    path = CACHE / "rasgos512.npz"
    if path.exists():
        return dict(np.load(path, allow_pickle=False))
    net = backbone()
    out = {}
    for p in PIECES:
        out[f"reg_{p}"] = feats512(net, imgs()[f"reg_{p}"], variants=True)
        out[f"test_{p}"] = feats512(net, imgs()[f"test_{p}"])
        print(f"  rasgos {p} listos", flush=True)
    np.savez(path, **out)
    return out


# ---------- memoria y detectores ----------

class Specialist:
    """Un especialista lleno solo con normales. Rango de cuantización y umbral
    de energía como en run_medico_demo.Level, pero solo con su pieza."""

    def __init__(self, fill, energy=True):
        zs = fill.reshape(-1, fill.shape[-1]) if fill.ndim == 2 else fill[:, 0]
        lo, hi = zs.min(0), zs.max(0)
        self.g = (lo - PAD * (hi - lo), hi + PAD * (hi - lo))
        self.tau = float(np.linalg.norm(zs, axis=1).min() * (1 - demo.ENERGY_MARGIN)) if energy else -1.0
        self.mem = HomoAssociativeMemory(64, Q)
        for z in fill.reshape(-1, 64):
            self.mem.register(self.q(z))

    def q(self, z):
        return demo.quantize_latent_global(np.asarray(z, dtype=np.float32), *self.g, Q)

    def uncovered(self, z):
        return int(np.count_nonzero(self.mem.recog_weights(self.q(z)) == 0))

    def accepts(self, z):
        return np.linalg.norm(z) >= self.tau and self.uncovered(z) == 0


def knn_score(fill0, Z):
    Xn = fill0 / np.linalg.norm(fill0, axis=1, keepdims=True)
    Zn = Z / np.linalg.norm(Z, axis=1, keepdims=True)
    return np.sort(Zn @ Xn.T, axis=1)[:, -5:].mean(1)


def knn_euclid(fill0, Z):
    """Post hoc: con la PCA centrada en la pieza, el coseno mide dirección desde la media."""
    d = np.linalg.norm(np.asarray(Z, dtype=np.float64)[:, None] - fill0[None], axis=2)
    return -np.sort(d, axis=1)[:, :5].mean(1)


class Gauss:
    def __init__(self, X):
        X = np.asarray(X, dtype=np.float64)
        self.mu = X.mean(0)
        self.P = np.linalg.inv(np.cov(X.T) + 0.01 * np.eye(X.shape[1]))

    def score(self, Z):
        d = np.asarray(Z, dtype=np.float64) - self.mu
        return -np.einsum("ij,jk,ik->i", d, self.P, d)


def auroc(normal, anomal):
    """P(score normal > score falla), con empates a la mitad."""
    r = rankdata(np.concatenate([normal, anomal]))
    n1 = len(normal)
    return float((r[:n1].sum() - n1 * (n1 + 1) / 2) / (n1 * len(anomal)))


def compare(acc_cal_mem, rej_test_mem, s_cal, s_test, y):
    """Memoria en su punto de operación y cada detector a la misma aceptación de calibración."""
    row = {"acepta_calibracion": float(acc_cal_mem),
           "memoria": {"deteccion": float(rej_test_mem[y == 1].mean()), "falsa_alarma": float(rej_test_mem[y == 0].mean())}}
    for k in s_cal:
        thr = np.quantile(s_cal[k], 1 - acc_cal_mem)
        rej = s_test[k] < thr
        row[k] = {"deteccion": float(rej[y == 1].mean()), "falsa_alarma": float(rej[y == 0].mean()),
                  "auroc": auroc(s_test[k][y == 0], s_test[k][y == 1])}
    return row


def detect_global(sp, fill, cal, test, y):
    """fill (n,16,64), cal (m,64), test (t,64)."""
    acc_cal = np.mean([sp.accepts(z) for z in cal])
    rej = np.array([not sp.accepts(z) for z in test])
    g = Gauss(fill[:, 0])
    s_cal = {"memoria_graduada": -np.array([sp.uncovered(z) for z in cal]),
             "knn": knn_score(fill[:, 0], cal), "maha": g.score(cal), "knn_euclid": knn_euclid(fill[:, 0], cal)}
    s_test = {"memoria_graduada": -np.array([sp.uncovered(z) for z in test]),
              "knn": knn_score(fill[:, 0], test), "maha": g.score(test), "knn_euclid": knn_euclid(fill[:, 0], test)}
    return compare(acc_cal, rej, s_cal, s_test, y)


def detect_patches(fillp, calp, testp, y):
    """Parches (n, 784, 64). La imagen se acepta si todos sus parches están contenidos."""
    sp = Specialist(fillp.reshape(-1, 64), energy=False)
    unc = lambda Z: np.array([max(sp.uncovered(z) for z in im) for im in Z])
    u_cal, u_test = unc(calp), unc(testp)
    bank = torch.tensor(fillp.reshape(-1, 64), device=DEV)
    g = Gauss(fillp.reshape(-1, 64))

    def nn_score(Z):
        out = []
        for im in Z:
            t = torch.tensor(im, device=DEV)
            d = torch.cat([torch.cdist(t[i:i + 196], bank).min(1).values for i in range(0, len(t), 196)])
            out.append(-float(d.max()))
        return np.array(out)

    maha = lambda Z: np.array([g.score(im).min() for im in Z])
    s_cal = {"memoria_graduada": -u_cal, "knn": nn_score(calp), "maha": maha(calp)}
    s_test = {"memoria_graduada": -u_test, "knn": nn_score(testp), "maha": maha(testp)}
    row = compare(np.mean(u_cal == 0), u_test > 0, s_cal, s_test, y)
    row["soporte_medio_por_coordenada"] = float((sp.mem._am.relation > 0).sum(1).mean())
    return row


# ---------- tipos de falla como dominios ----------

def defect_types(p, P2, net):
    tipos = imgs()[f"testtipo_{p}"]
    idx = {t: np.where(tipos == t)[0] for t in sorted(set(tipos)) if t and "," not in t}
    idx = {t: ii for t, ii in idx.items() if len(ii) >= MIN_TYPE}
    if len(idx) < 2:
        return None
    rng = np.random.RandomState(SEED)
    fill, test = {}, {}
    for t, ii in idx.items():
        ii = rng.permutation(ii)
        nf = int(np.ceil(0.6 * len(ii)))
        fill[t] = proj(P2, feats512(net, imgs()[f"test_{p}"][ii[:nf]], variants=True))
        test[t] = proj(P2, feats512(net, imgs()[f"test_{p}"][ii[nf:]]))
    names = list(idx)
    zs = np.concatenate([fill[t][:, 0] for t in names])
    lo, hi = zs.min(0), zs.max(0)
    g = (lo - PAD * (hi - lo), hi + PAD * (hi - lo))
    mems = {}
    for t in names:
        mems[t] = HomoAssociativeMemory(64, Q)
        for z in fill[t].reshape(-1, 64):
            mems[t].register(demo.quantize_latent_global(z, *g, Q))
    Xn = zs / np.linalg.norm(zs, axis=1, keepdims=True)
    yk = np.concatenate([[k] * len(fill[t]) for k, t in enumerate(names)])
    rows = []
    for k, t in enumerate(names):
        for z in test[t]:
            zq = demo.quantize_latent_global(z, *g, Q)
            sc = []
            for u in names:
                w = mems[u].recog_weights(zq)
                sc.append(0.0 if np.any(w == 0) else float(w.mean()))
            mem = names[int(np.argmax(sc))] if max(sc) > 0 else None
            nn_ = np.argsort(-(Xn @ (z / np.linalg.norm(z))))[:5]
            rows.append({"verdad": t, "memoria": mem, "knn": names[np.bincount(yk[nn_]).argmax()]})
    return {"tipos": {t: [int(np.ceil(0.6 * len(ii))), len(ii) - int(np.ceil(0.6 * len(ii)))] for t, ii in idx.items()},
            "filas": rows}


# ---------- corrida ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--visa", default="C:/Users/aq99l/Datasets/VisA")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    raw = OUT / "resultados.json"
    if not args.report_only:
        t0 = time.time()
        prepare(args.visa)
        print(f"imágenes listas ({time.time() - t0:.0f} s)", flush=True)
        F5 = global_feats()
        print(f"rasgos listos ({time.time() - t0:.0f} s)", flush=True)
        P1 = pca(np.concatenate([imgs()[f"f512all_{p}"] for p in PIECES]))
        reg1 = {p: proj(P1, F5[f"reg_{p}"]) for p in PIECES}
        fill1 = {p: reg1[p][:N_FILL] for p in PIECES}
        pa1 = {p: reg1[p][N_FILL:] for p in PIECES}
        test1 = {p: proj(P1, F5[f"test_{p}"]) for p in PIECES}
        L1 = demo.Level("nivel1", PIECES, None, fill1, pa1)
        res = {"formacion": L1.form, "nivel1": [], "nivel2": {}, "tipos": {}}
        for k, p in enumerate(PIECES):
            for z, y in zip(test1[p], imgs()[f"testy_{p}"]):
                d, why = L1.route(z, k)
                res["nivel1"].append({"verdad": p, "falla": int(y), "destino": d, "motivo": why, "knn": L1.knn(z)})
        print(f"nivel 1 listo ({time.time() - t0:.0f} s)", flush=True)
        net = backbone()
        for p in PIECES:
            y = imgs()[f"testy_{p}"]
            r = {}
            # G1: el especialista del nivel 1, con su cuantización y su energía
            ag = L1.agents[p]
            acc = lambda z: np.linalg.norm(z) >= L1.tau and np.all(ag.mem_dom_R.recog_weights(L1.q(z)) > 0)
            unc = lambda z: int(np.count_nonzero(ag.mem_dom_R.recog_weights(L1.q(z)) == 0))
            g = Gauss(fill1[p][:, 0])
            cal, te = pa1[p][:, 0], test1[p]
            r["G1"] = compare(np.mean([acc(z) for z in cal]), np.array([not acc(z) for z in te]),
                              {"memoria_graduada": -np.array([unc(z) for z in cal]),
                               "knn": knn_score(fill1[p][:, 0], cal), "maha": g.score(cal),
                               "knn_euclid": knn_euclid(fill1[p][:, 0], cal)},
                              {"memoria_graduada": -np.array([unc(z) for z in te]),
                               "knn": knn_score(fill1[p][:, 0], te), "maha": g.score(te),
                               "knn_euclid": knn_euclid(fill1[p][:, 0], te)}, y)
            # G2: PCA de la pieza
            P2 = pca(F5[f"reg_{p}"][:N_FILL, 0])
            reg2 = proj(P2, F5[f"reg_{p}"])
            test2 = proj(P2, F5[f"test_{p}"])
            sp2 = Specialist(reg2[:N_FILL])
            r["G2"] = detect_global(sp2, reg2[:N_FILL], reg2[N_FILL:, 0], test2, y)
            r["G2_acepta_test"] = [bool(sp2.accepts(z)) for z in test2]
            # P: parches
            pf = CACHE / f"parches_{p}.npz"
            if pf.exists():
                zp = np.load(pf)
                fillp, calp, testp = zp["fill"], zp["cal"], zp["test"]
            else:
                regp = patch_feats(net, imgs()[f"reg_{p}"])
                Pp = pca(regp[:N_FILL].reshape(-1, regp.shape[-1]))
                fillp, calp = proj(Pp, regp[:N_FILL]), proj(Pp, regp[N_FILL:])
                del regp
                testp = proj(Pp, patch_feats(net, imgs()[f"test_{p}"]))
                np.savez(pf, fill=fillp, cal=calp, test=testp)
            r["P"] = detect_patches(fillp, calp, testp, y)
            del fillp, calp, testp
            res["nivel2"][p] = r
            res["tipos"][p] = defect_types(p, P2, net)
            print(f"  nivel 2 {p} listo ({time.time() - t0:.0f} s)", flush=True)
        res["segundos"] = round(time.time() - t0)
        raw.write_text(json.dumps(res, ensure_ascii=False))
    report(json.loads(raw.read_text()))


def pct(x):
    return f"{100 * x:5.1f}"


def report(res):
    from collections import Counter
    L = ["Demo industrial EAM-TMS sobre VisA (1cls). Registro por pieza: "
         f"{N_FILL} normales de llenado (16 variantes) y {N_REG - N_FILL} de fase A = calibración."]
    L.append(f"Formación de directorios (fase A): {json.dumps(res['formacion'])}")
    rows = res["nivel1"]
    L.append("\n[nivel 1 · ruteo por pieza]")
    for lab, name in ((0, "normales"), (1, "fallas")):
        rs = [r for r in rows if r["falla"] == lab]
        ok = sum(r["destino"] == r["verdad"] for r in rs)
        rej = sum(r["destino"] is None for r in rs)
        kn = sum(r["knn"] == r["verdad"] for r in rs)
        L.append(f"  {name} n={len(rs)}: memoria acierto {pct(ok / len(rs))} · rechazo {pct(rej / len(rs))} · "
                 f"falso {pct((len(rs) - ok - rej) / len(rs))} · de lo respondido {pct(ok / max(len(rs) - rej, 1))} · "
                 f"kNN {pct(kn / len(rs))}")
    for p in PIECES:
        rs = [r for r in rows if r["verdad"] == p]
        ok = sum(r["destino"] == p for r in rs)
        rej = sum(r["destino"] is None for r in rs)
        L.append(f"    {p:<11} n={len(rs):>3}  {ok:>3} / {rej:>3} / {len(rs) - ok - rej:>3} · kNN {sum(r['knn'] == p for r in rs):>3}")
    conf = Counter((r["verdad"], r["destino"]) for r in rows if r["destino"] and r["destino"] != r["verdad"])
    L.append("  falsos más frecuentes: " + ", ".join(f"{a}->{b} {c}" for (a, b), c in conf.most_common(8)))

    for var, title in (("G1", "latentes del nivel 1"), ("G2", "PCA por pieza"), ("P", "parches, estilo PatchCore")):
        L.append(f"\n[nivel 2 · {var} · {title}] detección de fallas / falsa alarma en test; "
                 "detectores a la aceptación de calibración de la memoria; AUROC entre paréntesis")
        keys = [k for k in ("memoria_graduada", "knn", "maha", "knn_euclid") if k in res["nivel2"][PIECES[0]][var]]
        agg = {k: [] for k in ["memoria"] + keys}
        wins = {"sostiene": 0, "refuta": 0}
        for p in PIECES:
            r = res["nivel2"][p][var]
            for k in agg:
                agg[k].append(r[k])
            best = max(r["knn"]["deteccion"], r["maha"]["deteccion"])
            d = r["memoria"]["deteccion"] - best
            wins["sostiene"] += d >= -0.02
            wins["refuta"] += d < -0.02
            extra = f" · soporte medio {r['soporte_medio_por_coordenada']:.1f}/32" if "soporte_medio_por_coordenada" in r else ""
            L.append(f"    {p:<11} acepta cal {pct(r['acepta_calibracion'])} · memoria {pct(r['memoria']['deteccion'])} / "
                     f"{pct(r['memoria']['falsa_alarma'])} · " + " · ".join(
                         f"{k} {pct(r[k]['deteccion'])} / {pct(r[k]['falsa_alarma'])} ({r[k]['auroc']:.3f})"
                         for k in keys) + extra)
        L.append(f"    media       acepta cal {pct(np.mean([res['nivel2'][p][var]['acepta_calibracion'] for p in PIECES]))} · "
                 f"memoria {pct(np.mean([a['deteccion'] for a in agg['memoria']]))} / {pct(np.mean([a['falsa_alarma'] for a in agg['memoria']]))} · "
                 + " · ".join(f"{k} {pct(np.mean([a['deteccion'] for a in agg[k]]))} / {pct(np.mean([a['falsa_alarma'] for a in agg[k]]))} "
                              f"({np.mean([a['auroc'] for a in agg[k]]):.3f})" for k in keys))
        L.append(f"    criterio: memoria >= mejor detector - 2 puntos en {wins['sostiene']}/12 piezas, por debajo en {wins['refuta']}/12; "
                 f"detección - falsa alarma de la memoria (media) {100 * np.mean([a['deteccion'] - a['falsa_alarma'] for a in agg['memoria']]):.1f} puntos")

    L.append("\n[punta a punta · nivel 1 y especialista G2 del destino]")
    out = Counter()
    for p in PIECES:
        acc2 = res["nivel2"][p]["G2_acepta_test"]
        rs = [r for r in rows if r["verdad"] == p]
        for r, a in zip(rs, acc2):
            tag = "falla" if r["falla"] else "normal"
            if r["destino"] is None:
                out[(tag, "alarma en nivel 1")] += 1
            elif r["destino"] != p:
                out[(tag, "a otra pieza")] += 1
            else:
                out[(tag, "pasa como normal" if a else "alarma en nivel 2")] += 1
    for tag in ("normal", "falla"):
        n = sum(v for (t, _), v in out.items() if t == tag)
        L.append(f"  {tag} n={n}: " + " · ".join(f"{k} {pct(v / n)}" for (t, k), v in sorted(out.items()) if t == tag))

    L.append("\n[tipos de falla como dominios · G2, 60 % llenado / 40 % test]")
    for p in PIECES:
        t = res["tipos"].get(p)
        if not t:
            L.append(f"  {p:<11} menos de dos tipos con >= {MIN_TYPE} imágenes de etiqueta única")
            continue
        rs, names = t["filas"], list(t["tipos"])
        n = len(rs)
        ok = sum(r["memoria"] == r["verdad"] for r in rs)
        rej = sum(r["memoria"] is None for r in rs)
        bal = lambda key: np.mean([np.mean([r[key] == c for r in rs if r["verdad"] == c]) for c in names])
        L.append(f"  {p:<11} tipos {len(names)} (azar {pct(1 / len(names))}), test {n}: memoria acierto {pct(ok / n)} · "
                 f"rechazo {pct(rej / n)} · de lo respondido {pct(ok / max(n - rej, 1))} · balanceado {pct(bal('memoria'))} · "
                 f"kNN {pct(sum(r['knn'] == r['verdad'] for r in rs) / n)} · balanceado {pct(bal('knn'))}  "
                 f"{json.dumps(t['tipos'], ensure_ascii=False)}")
    L.append(f"\nTiempo total: {res.get('segundos', 0) / 60:.0f} min")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
