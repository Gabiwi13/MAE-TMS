"""
Experimento de cierre: la MAE como detector con WideResNet50-2 (ImageNet) y con una
red especializada en buenas contra malas. Diseño en propuesta_cierre_mae.md.

  parte 1  una clase, WRN50 congelada: global y parches; PatchCore de 1536 como referencia
  parte 2  WRN50 ajustada por pieza (capas 3 y 4); memoria solo buenas / solo malas / ambas
  parte 3  tipo de falla excluido del entrenamiento y del registro
Imágenes y registro del demo industrial (results/industrial/cache).

Uso:
  python run_cierre_mae.py --parte 1
  python run_cierre_mae.py --parte 23
  python run_cierre_mae.py --report-only
"""
import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import models, transforms

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_industrial_demo as ind  # noqa: E402
import run_medico_demo as demo  # noqa: E402
from associative_memory import HomoAssociativeMemory  # noqa: E402
from stage5_fill import augment_variants  # noqa: E402

OUT = ROOT / "results" / "cierre_mae"
CACHE = OUT / "cache"            # fuera de git
PIECES, N_FILL, Q, PAD, SEED = ind.PIECES, ind.N_FILL, ind.Q, ind.PAD, 42
DEV = demo.DEV
TF = demo.TF


def wrn():
    return models.wide_resnet50_2(weights=models.Wide_ResNet50_2_Weights.IMAGENET1K_V1).to(DEV).eval()


def batches(arr, step, variants=False):
    for i in range(0, len(arr), step):
        pil = [Image.fromarray(a) for a in arr[i:i + step]]
        if variants:
            pil = [v for im in pil for v in augment_variants(im)]
        yield torch.stack([TF(p) for p in pil]).to(DEV)


def stem(net, x):
    return net.maxpool(net.relu(net.bn1(net.conv1(x))))


def global_feats(net, arr, variants=False):
    out = []
    with torch.no_grad():
        for x in batches(arr, 8 if variants else 64, variants):
            h = net.layer4(net.layer3(net.layer2(net.layer1(stem(net, x)))))
            f = net.avgpool(h).flatten(1).cpu().numpy()
            out.append(f.reshape(-1, 16, f.shape[-1]) if variants else f)
    return np.concatenate(out)


def patch_feats(net, arr):
    """(n, 784, 1536) en float16."""
    out = []
    with torch.no_grad():
        for x in batches(arr, 16):
            l2 = net.layer2(net.layer1(stem(net, x)))
            l3 = F.interpolate(net.layer3(l2), size=l2.shape[-2:], mode="bilinear", align_corners=False)
            f = F.avg_pool2d(torch.cat([l2, l3], 1), 3, 1, 1)
            out.append(f.flatten(2).transpose(1, 2).half().cpu().numpy())
    return np.concatenate(out)


def gpu_pca(X, k=64):
    """X: tensor en GPU; covarianza por bloques para no duplicarlo en memoria."""
    mu = X.float().mean(0)
    C = torch.zeros(X.shape[1], X.shape[1], device=DEV, dtype=torch.float64)
    for i in range(0, len(X), 20000):
        Xc = (X[i:i + 20000].double() - mu.double())
        C += Xc.T @ Xc
    C /= len(X) - 1
    w, v = torch.linalg.eigh(C)
    V = v[:, torch.argsort(w, descending=True)[:k]].T.float()
    return mu, V


def gpu_proj(P, X):
    mu, V = P
    if not torch.is_tensor(X):
        X = torch.tensor(np.asarray(X, dtype=np.float32), device=DEV)
    return torch.cat([(X[i:i + 20000].float() - mu) @ V.T for i in range(0, len(X), 20000)]).cpu().numpy()


def nn_score(bank, Z):
    """PatchCore: menos la distancia máxima, sobre los parches, al parche más cercano.
    bank en float16 para que quepa en los 8 GB de la GPU."""
    b2 = (bank.float() ** 2).sum(1)
    out = []
    for im in Z:
        t = torch.tensor(np.asarray(im), device=DEV, dtype=torch.float16)
        t2 = (t.float() ** 2).sum(1)
        d2 = torch.cat([(t2[i:i + 196, None] - 2 * (t[i:i + 196] @ bank.T).float() + b2[None]).min(1).values
                        for i in range(0, len(t), 196)])
        out.append(-float(d2.clamp(min=0).max().sqrt()))
    return np.array(out)


# ---------- parte 1 ----------

def parte1():
    net = wrn()
    res = {}
    t0 = time.time()
    for p in PIECES:
        done = CACHE / f"parte1_{p}.json"
        if done.exists():
            res[p] = json.loads(done.read_text())
            continue
        y = ind.imgs()[f"testy_{p}"]
        reg, te = ind.imgs()[f"reg_{p}"], ind.imgs()[f"test_{p}"]
        r = {}
        # global
        gr = global_feats(net, reg, variants=True)
        gt = global_feats(net, te)
        P2 = ind.pca(gr[:N_FILL, 0])
        reg2, test2 = ind.proj(P2, gr), ind.proj(P2, gt)
        sp = ind.Specialist(reg2[:N_FILL])
        r["global"] = ind.detect_global(sp, reg2[:N_FILL], reg2[N_FILL:, 0], test2, y)
        del gr
        # parches
        bank = torch.tensor(patch_feats(net, reg[:N_FILL]).reshape(-1, 1536), device=DEV, dtype=torch.float16)
        Pp = gpu_pca(bank)
        fill64 = gpu_proj(Pp, bank)
        cal = patch_feats(net, reg[N_FILL:])
        tst = patch_feats(net, te)
        cal64 = np.stack([gpu_proj(Pp, im) for im in cal])
        tst64 = np.stack([gpu_proj(Pp, im) for im in tst])
        ref_cal, ref_te = nn_score(bank, cal), nn_score(bank, tst)
        del bank, cal, tst
        torch.cuda.empty_cache()
        row = ind.detect_patches(fill64.reshape(N_FILL, 784, 64), cal64, tst64, y)
        thr = np.quantile(ref_cal, 1 - row["acepta_calibracion"])
        rej = ref_te < thr
        row["patchcore_1536"] = {"deteccion": float(rej[y == 1].mean()), "falsa_alarma": float(rej[y == 0].mean()),
                                 "auroc": ind.auroc(ref_te[y == 0], ref_te[y == 1])}
        r["parches"] = row
        res[p] = r
        done.write_text(json.dumps(r))
        print(f"  parte 1 {p} ({time.time() - t0:.0f} s): global mem {r['global']['memoria']['deteccion']:.2f}, "
              f"parches mem {row['memoria']['deteccion']:.2f}, PatchCore1536 AUROC {row['patchcore_1536']['auroc']:.3f}", flush=True)
        del fill64, cal64, tst64
    return res


# ---------- partes 2 y 3 ----------

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.b = models.wide_resnet50_2(weights=models.Wide_ResNet50_2_Weights.IMAGENET1K_V1)
        for m in (self.b.conv1, self.b.bn1, self.b.layer1, self.b.layer2):
            for q in m.parameters():
                q.requires_grad = False
        self.fc = nn.Linear(2048, 64)
        self.head = nn.Linear(64, 2)

    def latent(self, x):
        b = self.b
        h = b.layer4(b.layer3(b.layer2(b.layer1(stem(b, x)))))
        return self.fc(b.avgpool(h).flatten(1))

    def forward(self, x):
        z = self.latent(x)
        return z, self.head(z)


def primary(t):
    return t.split(",")[0].strip().strip('"').strip()


def split_defects(p):
    y = ind.imgs()[f"testy_{p}"]
    tipos = np.array([primary(t) if t else "" for t in ind.imgs()[f"testtipo_{p}"]])
    idx = np.where(y == 1)[0]
    cnt = Counter(tipos[idx])
    held = cnt.most_common(1)[0][0] if len(cnt) >= 2 else None
    rng = np.random.RandomState(SEED)
    tr, te = [], []
    for t in sorted(cnt):
        if t == held:
            continue
        ii = rng.permutation(idx[tipos[idx] == t])
        nf = int(np.ceil(0.6 * len(ii)))
        tr += ii[:nf].tolist()
        te += ii[nf:].tolist()
    novel = idx[tipos[idx] == held].tolist() if held else []
    return np.array(tr), np.array(te), np.array(novel), held, dict(cnt)


def train(p, normals, defects):
    torch.manual_seed(SEED)
    net = Net().to(DEV)
    X = np.concatenate([normals, defects])
    yl = np.array([0] * len(normals) + [1] * len(defects))
    w = 1.0 / np.bincount(yl)[yl]
    g = torch.Generator().manual_seed(SEED)
    aug = transforms.Compose([transforms.RandomHorizontalFlip(), transforms.RandomRotation(10)])
    opt = torch.optim.Adam([q for q in net.parameters() if q.requires_grad], lr=1e-4)
    scaler = torch.amp.GradScaler("cuda")
    ce = nn.CrossEntropyLoss()
    log = []
    for ep in range(12):
        net.train()
        for m in (net.b.bn1, net.b.layer1, net.b.layer2):
            m.eval()
        pick = torch.multinomial(torch.tensor(w), 256, replacement=True, generator=g).numpy()
        tot = 0.0
        for s in range(0, 256, 16):
            b = pick[s:s + 16]
            xb = torch.stack([TF(aug(Image.fromarray(X[i]))) for i in b]).to(DEV)
            yb = torch.tensor(yl[b]).to(DEV)
            opt.zero_grad()
            with torch.autocast("cuda", dtype=torch.float16):
                loss = ce(net(xb)[1], yb)
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
            tot += loss.item()
        log.append(round(tot / 16, 4))
    print(f"    {p} pérdida por época {log}", flush=True)
    return net.eval(), log


def encode(net, arr, variants=False):
    zs, ls = [], []
    with torch.no_grad():
        for x in batches(arr, 8 if variants else 64, variants):
            z, l = net(x)
            zs.append(z.float().cpu().numpy())
            ls.append(l.float().cpu().numpy())
    z, l = np.concatenate(zs), np.concatenate(ls)
    return (z.reshape(-1, 16, 64), l.reshape(-1, 16, 2)) if variants else (z, l)


class Mem:
    def __init__(self, Z, g):
        self.g, self.n = g, len(Z.reshape(-1, 64))
        self.mem = HomoAssociativeMemory(64, Q)
        for z in Z.reshape(-1, 64):
            self.mem.register(demo.quantize_latent_global(z.astype(np.float32), *g, Q))

    def read(self, z):
        w = self.mem.recog_weights(demo.quantize_latent_global(np.asarray(z, dtype=np.float32), *self.g, Q))
        unc = int(np.count_nonzero(w == 0))
        return unc, (0.0 if unc else float(w.mean()) / self.n)


def softmax(l):
    e = np.exp(l - l.max(1, keepdims=True))
    return e / e.sum(1, keepdims=True)


def decide_both(mn, mm, Z):
    out = []
    for z in Z:
        un, sn = mn.read(z)
        um, sm = mm.read(z)
        if un == 0 and um > 0:
            out.append("buena")
        elif um == 0 and un > 0:
            out.append("mala")
        elif un == 0 and um == 0:
            out.append("buena" if sn >= sm else "mala")
        else:
            out.append("desconocida")
    return np.array(out)


def rates(dec, y):
    return {"deteccion": float(np.mean(dec[y == 1] == "mala")), "falsa_alarma": float(np.mean(dec[y == 0] != "buena")),
            "abstencion_fallas": float(np.mean(dec[y == 1] == "desconocida")),
            "abstencion_normales": float(np.mean(dec[y == 0] == "desconocida"))}


def thresholded(s_cal, s_te, acc, y):
    """Puntaje de normalidad (alto = normal) a la aceptación de calibración acc."""
    thr = np.quantile(s_cal, 1 - acc)
    rej = s_te < thr
    return {"deteccion": float(rej[y == 1].mean()), "falsa_alarma": float(rej[y == 0].mean()),
            "auroc": ind.auroc(s_te[y == 0], s_te[y == 1])}


def partes23():
    res = {}
    t0 = time.time()
    for p in PIECES:
        tr, te, novel, held, cnt = split_defects(p)
        X = ind.imgs()[f"test_{p}"]
        y_all = ind.imgs()[f"testy_{p}"]
        reg = ind.imgs()[f"reg_{p}"]
        net, log = train(p, reg[:N_FILL], X[tr])
        zn, _ = encode(net, reg[:N_FILL], variants=True)
        zd, _ = encode(net, X[tr], variants=True)
        zc, lc = encode(net, reg[N_FILL:])
        norm_te = np.where(y_all == 0)[0]
        kt = np.concatenate([norm_te, te])
        zt, lt = encode(net, X[kt])
        yt = np.array([0] * len(norm_te) + [1] * len(te))
        zv, lv = encode(net, X[novel]) if len(novel) else (np.zeros((0, 64)), np.zeros((0, 2)))
        del net
        torch.cuda.empty_cache()
        allz = np.concatenate([zn[:, 0], zd[:, 0]])
        lo, hi = allz.min(0), allz.max(0)
        g = (lo - PAD * (hi - lo), hi + PAD * (hi - lo))
        mn, mm = Mem(zn, g), Mem(zd, g)
        r = {"tipos": cnt, "excluido": held, "n_entrenamiento_fallas": int(len(tr)), "n_test_fallas": int(len(te)),
             "n_novel": int(len(novel)), "perdida": log}
        # esquemas de memoria
        unc_c = np.array([mn.read(z)[0] for z in zc])
        unc_t = np.array([mn.read(z)[0] for z in zt])
        dec = {"solo_buenas": np.where(unc_t == 0, "buena", "mala"),
               "solo_malas": np.array(["mala" if mm.read(z)[0] == 0 else "buena" for z in zt]),
               "ambas": decide_both(mn, mm, zt)}
        dec_cal = {"solo_buenas": np.where(unc_c == 0, "buena", "mala"),
                   "solo_malas": np.array(["mala" if mm.read(z)[0] == 0 else "buena" for z in zc]),
                   "ambas": decide_both(mn, mm, zc)}
        p_c, p_t = softmax(lc)[:, 1], softmax(lt)[:, 1]
        gss = ind.Gauss(zn[:, 0])
        scores_c = {"cabeza": -p_c, "knn_euclid": ind.knn_euclid(zn[:, 0], zc), "maha": gss.score(zc)}
        scores_t = {"cabeza": -p_t, "knn_euclid": ind.knn_euclid(zn[:, 0], zt), "maha": gss.score(zt)}
        bank = np.concatenate([zn[:, 0], zd[:, 0]])
        lab = np.array([0] * len(zn) + [1] * len(zd))
        d2 = ((zt[:, None] - bank[None]) ** 2).sum(2)
        knn2 = np.where(lab[np.argsort(d2, 1)[:, :5]].mean(1) > 0.5, "mala", "buena")
        r["knn_dos_clases"] = rates(knn2, yt)
        r["cabeza_argmax"] = rates(np.where(p_t > 0.5, "mala", "buena"), yt)
        r["esquemas"] = {}
        for k in dec:
            acc = float(np.mean(dec_cal[k] == "buena"))
            row = {"acepta_calibracion": acc, "memoria": rates(dec[k], yt)}
            for d in scores_c:
                row[d] = thresholded(scores_c[d], scores_t[d], acc, yt)
            r["esquemas"][k] = row
        r["memoria_graduada_auroc"] = ind.auroc(-unc_t[yt == 0], -unc_t[yt == 1])
        # parte 3: tipo nunca visto
        if len(novel):
            a_known = float(np.mean(dec["ambas"] == "desconocida"))
            msp_t, msp_v = softmax(lt).max(1), softmax(lv).max(1)
            en_t = np.log(np.exp(lt).sum(1))
            en_v = np.log(np.exp(lv).sum(1))
            dk_t = np.sqrt(np.sort(d2, 1)[:, :5]).mean(1)
            d2v = ((zv[:, None] - bank[None]) ** 2).sum(2)
            dk_v = np.sqrt(np.sort(d2v, 1)[:, :5]).mean(1)
            dec_v = decide_both(mn, mm, zv)
            argmax_v = np.where(softmax(lv)[:, 1] > 0.5, "mala", "buena")
            knn2_v = np.where(lab[np.argsort(d2v, 1)[:, :5]].mean(1) > 0.5, "mala", "buena")

            def abst(conf_known, conf_novel, base, low_is_unknown=True):
                thr = np.quantile(conf_known, a_known) if low_is_unknown else np.quantile(conf_known, 1 - a_known)
                ab = conf_novel < thr if low_is_unknown else conf_novel > thr
                if a_known == 0:
                    ab = np.zeros(len(conf_novel), bool)
                d = np.where(ab, "desconocida", base)
                return {k: float(np.mean(d == k)) for k in ("desconocida", "mala", "buena")}

            r["novel"] = {"abstencion_conocidos_ambas": a_known,
                          "memoria_ambas": {k: float(np.mean(dec_v == k)) for k in ("desconocida", "mala", "buena")},
                          "memoria_solo_buenas_rechaza": float(np.mean([mn.read(z)[0] > 0 for z in zv])),
                          "msp": abst(msp_t, msp_v, argmax_v), "energia": abst(en_t, en_v, argmax_v),
                          "knn_distancia": abst(dk_t, dk_v, knn2_v, low_is_unknown=False),
                          "cabeza_sin_abstencion": {k: float(np.mean(argmax_v == k)) for k in ("mala", "buena")},
                          "cabeza_a_aceptacion_solo_buenas": float(np.mean(-softmax(lv)[:, 1] < np.quantile(
                              scores_c["cabeza"], 1 - r["esquemas"]["solo_buenas"]["acepta_calibracion"])))}
        res[p] = r
        print(f"  partes 2-3 {p} ({time.time() - t0:.0f} s) excluido={held}", flush=True)
    return res


# ---------- reporte ----------

def pct(x):
    return f"{100 * x:5.1f}"


def report(res):
    L = ["Experimento de cierre (propuesta_cierre_mae.md). WideResNet50-2 de ImageNet."]
    verdict = {}
    if "parte1" in res:
        P1 = res["parte1"]
        for var, keys in (("global", ("memoria_graduada", "knn_euclid", "maha")),
                          ("parches", ("memoria_graduada", "knn", "maha", "patchcore_1536"))):
            L.append(f"\n[parte 1 · {var}] detección / falsa alarma en test; detectores a la aceptación de calibración de la memoria; AUROC")
            below = 0
            for p in PIECES:
                r = P1[p][var]
                best = max(r[k]["deteccion"] for k in keys if k != "memoria_graduada")
                below += r["memoria"]["deteccion"] < best - 0.02
                L.append(f"    {p:<11} acepta cal {pct(r['acepta_calibracion'])} · memoria {pct(r['memoria']['deteccion'])} / {pct(r['memoria']['falsa_alarma'])} · "
                         + " · ".join(f"{k} {pct(r[k]['deteccion'])} / {pct(r[k]['falsa_alarma'])} ({r[k]['auroc']:.3f})" for k in keys))
            m = lambda f: np.mean([f(P1[p][var]) for p in PIECES])
            L.append(f"    media       acepta cal {pct(m(lambda r: r['acepta_calibracion']))} · memoria {pct(m(lambda r: r['memoria']['deteccion']))} / "
                     f"{pct(m(lambda r: r['memoria']['falsa_alarma']))} · " + " · ".join(
                         f"{k} {pct(m(lambda r: r[k]['deteccion']))} / {pct(m(lambda r: r[k]['falsa_alarma']))} ({m(lambda r: r[k]['auroc']):.3f})" for k in keys))
            L.append(f"    memoria más de 2 puntos por debajo del mejor detector en {below}/12 piezas")
            verdict[f"parte1_{var}"] = below
    if "parte23" in res:
        R = res["parte23"]
        L.append("\n[parte 2 · red especializada, fallas de tipos conocidos] por esquema: memoria detección / falsa alarma (abstención en fallas / normales) · "
                 "detectores a la aceptación de calibración del esquema")
        below = 0
        for p in PIECES:
            r = R[p]
            best_gap = -9
            parts = []
            for k, row in r["esquemas"].items():
                mem = row["memoria"]
                bestd = max(row[d]["deteccion"] for d in ("cabeza", "knn_euclid", "maha"))
                best_gap = max(best_gap, mem["deteccion"] - bestd)
                parts.append(f"{k}: {pct(mem['deteccion'])} / {pct(mem['falsa_alarma'])} ({pct(mem['abstencion_fallas'])}/{pct(mem['abstencion_normales'])}) "
                             f"[cal {pct(row['acepta_calibracion'])}; cabeza {pct(row['cabeza']['deteccion'])} / {pct(row['cabeza']['falsa_alarma'])}, "
                             f"knn {pct(row['knn_euclid']['deteccion'])}, maha {pct(row['maha']['deteccion'])}]")
            below += best_gap < -0.02
            L.append(f"  {p:<11} fallas entren/test {r['n_entrenamiento_fallas']}/{r['n_test_fallas']} · AUROC cabeza {r['esquemas']['solo_buenas']['cabeza']['auroc']:.3f} · "
                     f"maha {r['esquemas']['solo_buenas']['maha']['auroc']:.3f} · memoria graduada {r['memoria_graduada_auroc']:.3f} · "
                     f"kNN 2 clases {pct(r['knn_dos_clases']['deteccion'])} / {pct(r['knn_dos_clases']['falsa_alarma'])} · "
                     f"cabeza argmax {pct(r['cabeza_argmax']['deteccion'])} / {pct(r['cabeza_argmax']['falsa_alarma'])}")
            for s in parts:
                L.append(f"      {s}")
        mean = lambda f: np.mean([f(R[p]) for p in PIECES])
        L.append("  media: " + " · ".join(
            f"{k} {pct(mean(lambda r: r['esquemas'][k]['memoria']['deteccion']))} / {pct(mean(lambda r: r['esquemas'][k]['memoria']['falsa_alarma']))}"
            for k in ("solo_buenas", "solo_malas", "ambas"))
            + f" · cabeza argmax {pct(mean(lambda r: r['cabeza_argmax']['deteccion']))} / {pct(mean(lambda r: r['cabeza_argmax']['falsa_alarma']))}"
            + f" · kNN 2 clases {pct(mean(lambda r: r['knn_dos_clases']['deteccion']))} / {pct(mean(lambda r: r['knn_dos_clases']['falsa_alarma']))}"
            + f" · AUROC cabeza {mean(lambda r: r['esquemas']['solo_buenas']['cabeza']['auroc']):.3f}, maha {mean(lambda r: r['esquemas']['solo_buenas']['maha']['auroc']):.3f}")
        L.append(f"  mejor esquema de memoria más de 2 puntos por debajo del mejor detector (a su aceptación) en {below}/12 piezas")
        verdict["parte2"] = below
        L.append("\n[parte 3 · tipo de falla nunca visto] abstención / mala / buena (falla silenciosa); rivales a la abstención de «ambas» en lo conocido")
        nov = [p for p in PIECES if "novel" in R[p]]
        for p in nov:
            v = R[p]["novel"]
            fmt = lambda d: f"{pct(d['desconocida'])} / {pct(d['mala'])} / {pct(d['buena'])}"
            L.append(f"  {p:<11} «{R[p]['excluido']}» n={R[p]['n_novel']:>3} · abst. conocidos {pct(v['abstencion_conocidos_ambas'])} · memoria {fmt(v['memoria_ambas'])} · "
                     f"msp {fmt(v['msp'])} · energía {fmt(v['energia'])} · kNN dist {fmt(v['knn_distancia'])} · cabeza sin abst. buena {pct(v['cabeza_sin_abstencion']['buena'])} · "
                     f"solo buenas rechaza {pct(v['memoria_solo_buenas_rechaza'])} · cabeza a esa aceptación {pct(v['cabeza_a_aceptacion_solo_buenas'])}")
        mm = lambda k, s: np.mean([R[p]["novel"][k][s] for p in nov])
        L.append(f"  media ({len(nov)} piezas): memoria {pct(mm('memoria_ambas', 'desconocida'))} / {pct(mm('memoria_ambas', 'mala'))} / {pct(mm('memoria_ambas', 'buena'))} · "
                 f"msp {pct(mm('msp', 'desconocida'))} / {pct(mm('msp', 'mala'))} / {pct(mm('msp', 'buena'))} · "
                 f"energía {pct(mm('energia', 'desconocida'))} / {pct(mm('energia', 'mala'))} / {pct(mm('energia', 'buena'))} · "
                 f"kNN dist {pct(mm('knn_distancia', 'desconocida'))} / {pct(mm('knn_distancia', 'mala'))} / {pct(mm('knn_distancia', 'buena'))} · "
                 f"abst. conocidos {pct(np.mean([R[p]['novel']['abstencion_conocidos_ambas'] for p in nov]))} · "
                 f"solo buenas rechaza {pct(np.mean([R[p]['novel']['memoria_solo_buenas_rechaza'] for p in nov]))} · "
                 f"cabeza a esa aceptación {pct(np.mean([R[p]['novel']['cabeza_a_aceptacion_solo_buenas'] for p in nov]))}")
        verdict["nicho_diferencia_msp"] = mm("memoria_ambas", "desconocida") - mm("msp", "desconocida")
        verdict["nicho_diferencia_energia"] = mm("memoria_ambas", "desconocida") - mm("energia", "desconocida")
    L.append(f"\n[criterio] {json.dumps(verdict)}")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parte", choices=["1", "23"])
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    if args.parte == "1":
        (CACHE / "parte1.json").write_text(json.dumps(parte1()))
    elif args.parte == "23":
        (CACHE / "parte23.json").write_text(json.dumps(partes23()))
    res = {}
    for k in ("parte1", "parte23"):
        f = CACHE / f"{k}.json"
        if f.exists():
            res[k] = json.loads(f.read_text())
    (OUT / "resultados.json").write_text(json.dumps(res, ensure_ascii=False))
    report(res)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
