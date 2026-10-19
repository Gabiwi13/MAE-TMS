"""
Red con fallas sintéticas (CutPaste, cicatriz, mancha) y término anti-colapso (estilo
VICReg) sobre el latente. Diseño en propuesta_red_sintetica.md.

  A base (latentes del experimento de cascada) · B + sintéticas · C + sintéticas + anti-colapso
  D + anti-colapso
Para cada variante: colapso del latente, red sola, cascada de la MAE (k = 1 y 8) y MSP a igual revisión.

Uso: python run_red_sintetica.py [--report-only]
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from PIL import Image, ImageDraw, ImageFilter
from sklearn.cluster import KMeans
from torchvision import transforms

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_cascada_modulos as cas  # noqa: E402
import run_cierre_mae as cm  # noqa: E402
import run_industrial_demo as ind  # noqa: E402

OUT = ROOT / "results" / "red_sintetica"
CACHE = OUT / "cache"            # fuera de git
PIECES, N_FILL, PAD, SEED, DEV = ind.PIECES, ind.N_FILL, ind.PAD, 42, cm.DEV
VARIANTS = {"B": (True, False), "C": (True, True), "D": (False, True)}
EPOCHS, PER_EPOCH, BATCH = 16, 288, 24


# ---------- fallas sintéticas ----------

def _box(rng, area_frac, aspect, n=224):
    a = area_frac * n * n
    w = int(np.clip(np.sqrt(a * aspect), 2, n - 1))
    h = int(np.clip(np.sqrt(a / aspect), 2, n - 1))
    return w, h


def cutpaste(img, rng):
    w, h = _box(rng, rng.uniform(0.02, 0.15), np.exp(rng.uniform(np.log(0.3), np.log(3.3))))
    x0, y0 = rng.randint(0, 224 - w), rng.randint(0, 224 - h)
    patch = img[y0:y0 + h, x0:x0 + w].astype(np.float32)
    m = patch.mean()
    patch = np.clip((patch - m) * rng.uniform(0.8, 1.2) + m * rng.uniform(0.8, 1.2), 0, 255)
    out = img.copy()
    x1, y1 = rng.randint(0, 224 - w), rng.randint(0, 224 - h)
    out[y1:y1 + h, x1:x1 + w] = patch.astype(np.uint8)
    return out


def scar(img, rng):
    w, h = rng.randint(2, 17), rng.randint(10, 26)
    x0, y0 = rng.randint(0, 224 - w), rng.randint(0, 224 - h)
    patch = Image.fromarray(img[y0:y0 + h, x0:x0 + w])
    mask = Image.new("L", (w, h), 255)
    ang = rng.uniform(-45, 45)
    patch, mask = patch.rotate(ang, expand=True), mask.rotate(ang, expand=True)
    out = Image.fromarray(img.copy())
    out.paste(patch, (rng.randint(0, 224 - patch.width), rng.randint(0, 224 - patch.height)), mask)
    return np.asarray(out)


def stain(img, rng):
    a, b = rng.uniform(4, 24), rng.uniform(4, 24)
    cx, cy = rng.uniform(a, 224 - a), rng.uniform(b, 224 - b)
    mask = Image.new("L", (224, 224), 0)
    ImageDraw.Draw(mask).ellipse((cx - a, cy - b, cx + a, cy + b), fill=255)
    mask = np.asarray(mask.filter(ImageFilter.GaussianBlur(2)), dtype=np.float32)[..., None] / 255 * rng.uniform(0.5, 1.0)
    color = rng.randint(0, 256, 3).astype(np.float32)
    return (img * (1 - mask) + color * mask).astype(np.uint8)


def synthetic(img, rng):
    return (cutpaste, scar, stain)[rng.randint(3)](img, rng)


# ---------- entrenamiento ----------

def vicreg(z):
    z = z.float()
    z = z - z.mean(0)
    std = torch.sqrt(z.var(0) + 1e-4)
    var = torch.relu(1 - std).mean()
    cov = (z.T @ z) / (len(z) - 1)
    off = cov - torch.diag(torch.diag(cov))
    return var + 0.04 * (off ** 2).sum() / z.shape[1]


def train(p, normals, defects, use_synth, use_vic):
    torch.manual_seed(SEED)
    rng = np.random.RandomState(SEED)
    net = cm.Net().to(DEV)
    aug = transforms.Compose([transforms.RandomHorizontalFlip(), transforms.RandomRotation(10)])
    opt = torch.optim.Adam([q for q in net.parameters() if q.requires_grad], lr=1e-4)
    scaler = torch.amp.GradScaler("cuda")
    ce = nn.CrossEntropyLoss()
    cats = 3 if use_synth else 2
    log = []
    for ep in range(EPOCHS):
        net.train()
        for m in (net.b.bn1, net.b.layer1, net.b.layer2):
            m.eval()
        tot = 0.0
        for s in range(PER_EPOCH // BATCH):
            imgs, ys = [], []
            for c in rng.randint(cats, size=BATCH):
                if c == 0:
                    imgs.append(normals[rng.randint(len(normals))]); ys.append(0)
                elif c == 1:
                    imgs.append(defects[rng.randint(len(defects))]); ys.append(1)
                else:
                    imgs.append(synthetic(normals[rng.randint(len(normals))], rng)); ys.append(1)
            xb = torch.stack([cm.TF(aug(Image.fromarray(a))) for a in imgs]).to(DEV)
            yb = torch.tensor(ys).to(DEV)
            opt.zero_grad()
            with torch.autocast("cuda", dtype=torch.float16):
                z, logits = net(xb)
                loss = ce(logits, yb)
            if use_vic:
                loss = loss + vicreg(z)
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
            tot += loss.item()
        log.append(round(tot / (PER_EPOCH // BATCH), 4))
    print(f"    {p} pérdida por época {log}", flush=True)
    return net.eval(), log


def latents(v, p):
    if v == "A":
        return dict(np.load(cas.CACHE / f"lat_{p}.npz", allow_pickle=False))
    path = CACHE / f"lat_{v}_{p}.npz"
    if path.exists():
        return dict(np.load(path, allow_pickle=False))
    tr, te, novel, held, _ = cm.split_defects(p)
    X, y_all, reg = ind.imgs()[f"test_{p}"], ind.imgs()[f"testy_{p}"], ind.imgs()[f"reg_{p}"]
    net, log = train(p, reg[:N_FILL], X[tr], *VARIANTS[v])
    zn, _ = cm.encode(net, reg[:N_FILL], variants=True)
    zd, _ = cm.encode(net, X[tr], variants=True)
    zc, lc = cm.encode(net, reg[N_FILL:])
    norm_te = np.where(y_all == 0)[0]
    zt, lt = cm.encode(net, X[np.concatenate([norm_te, te])])
    yt = np.array([0] * len(norm_te) + [1] * len(te))
    zv, lv = cm.encode(net, X[novel]) if len(novel) else (np.zeros((0, 64), np.float32), np.zeros((0, 2), np.float32))
    del net
    torch.cuda.empty_cache()
    out = dict(zn=zn, zd=zd, zc=zc, lc=lc, zt=zt, lt=lt, yt=yt, zv=zv, lv=lv, held=np.array(held or ""),
               perdida=np.array(log))
    np.savez(path, **out)
    return out


# ---------- evaluación ----------

def evaluate(L):
    zn, zd, zt, yt, zv, lt, lv = L["zn"], L["zd"], L["zt"], L["yt"], L["zv"], L["lt"], L["lv"]
    ev = np.sort(np.linalg.eigvalsh(np.cov(zn[:, 0].astype(np.float64).T)))[::-1]
    ev = np.maximum(ev, 0) / max(ev.sum(), 1e-12)
    r = {"varianza_3": float(ev[:3].sum()), "direcciones_95": int(np.searchsorted(np.cumsum(ev), 0.95) + 1)}
    st = cm.softmax(lt)
    sv = cm.softmax(lv) if len(lv) else np.zeros((0, 2))
    arg_t = np.where(st[:, 1] > 0.5, "mala", "buena")
    arg_v = np.where(sv[:, 1] > 0.5, "mala", "buena")
    r["red"] = {"conocido": cas.known_rates(arg_t, yt), "novel": cas.frac(arg_v)}
    allz = np.concatenate([zn[:, 0], zd[:, 0]])
    lo, hi = allz.min(0), allz.max(0)
    g = (lo - PAD * (hi - lo), hi + PAD * (hi - lo))
    md = cm.Mem(zd, g)
    msp_t, msp_v = st.max(1), sv.max(1) if len(sv) else np.zeros(0)
    en_t = np.log(np.exp(lt).sum(1))
    en_v = np.log(np.exp(lv).sum(1)) if len(lv) else np.zeros(0)
    r["cascada"] = {}
    for k in (1, 8):
        lab = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit_predict(zn[:, 0]) if k > 1 else np.zeros(len(zn), int)
        goods = [cm.Mem(zn[lab == c], g) for c in range(k)]
        d_t, d_v = cas.cascade(md, goods, zt), cas.cascade(md, goods, zv)
        a = float(np.mean(d_t == "desconocida"))
        row = {"conocido": cas.known_rates(d_t, yt), "novel": cas.frac(d_v), "revision_conocido": a}
        for name, (ck, cv) in {"msp": (msp_t, msp_v), "energia": (en_t, en_v)}.items():
            rk, rv = cas.rival(ck, cv, arg_t, arg_v, a)
            row[name] = {"conocido": cas.known_rates(rk, yt), "novel": cas.frac(rv)}
        r["cascada"][str(k)] = row
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    raw = OUT / "resultados.json"
    if not args.report_only:
        t0 = time.time()
        res = {v: {} for v in ("A", "B", "C", "D")}
        for p in PIECES:
            for v in res:
                L = latents(v, p)
                res[v][p] = evaluate(L)
                res[v][p]["n_novel"] = int(len(L["zv"]))
            print(f"  {p} listo ({time.time() - t0:.0f} s)", flush=True)
        res["segundos"] = round(time.time() - t0)
        raw.write_text(json.dumps(res, ensure_ascii=False))
    report(json.loads(raw.read_text()))


def pct(x):
    return f"{100 * x:5.1f}"


def report(res):
    L = ["Red con fallas sintéticas y anti-colapso (propuesta_red_sintetica.md).",
         "A base · B + sintéticas · C + sintéticas + anti-colapso · D + anti-colapso"]
    verdict = {}
    for v in ("A", "B", "C", "D"):
        R = res[v]
        P = [p for p in PIECES if p in R]
        nov = [p for p in P if R[p]["n_novel"] > 0]
        m = lambda f, ps: float(np.mean([f(R[p]) for p in ps]))
        L.append(f"\n[{v}] colapso: varianza en 3 direcciones {m(lambda r: r['varianza_3'], P):.3f} · direcciones para el 95 % "
                 f"{m(lambda r: r['direcciones_95'], P):.1f}")
        L.append(f"  red: conocido {pct(m(lambda r: r['red']['conocido']['deteccion'], P))} / {pct(m(lambda r: r['red']['conocido']['falsa_alarma'], P))} · "
                 f"nuevo pasa en silencio {pct(m(lambda r: r['red']['novel']['buena'], nov))}")
        verdict[v] = {"red_silenciosa": m(lambda r: r["red"]["novel"]["buena"], nov),
                      "red_falsa_alarma": m(lambda r: r["red"]["conocido"]["falsa_alarma"], P)}
        for k in ("1", "8"):
            c = lambda f, ps: m(lambda r: f(r["cascada"][k]), ps)
            L.append(f"  cascada k={k}: conocido {pct(c(lambda x: x['conocido']['deteccion'], P))} / {pct(c(lambda x: x['conocido']['falsa_alarma'], P))} · "
                     f"revisión normales {pct(c(lambda x: x['conocido']['revision_normales'], P))} · fallas {pct(c(lambda x: x['conocido']['revision_fallas'], P))} · "
                     f"nuevo: revisión {pct(c(lambda x: x['novel']['desconocida'], nov))} / mala {pct(c(lambda x: x['novel']['mala'], nov))} / "
                     f"silenciosa {pct(c(lambda x: x['novel']['buena'], nov))} · a igual revisión: msp silenciosa {pct(c(lambda x: x['msp']['novel']['buena'], nov))}, "
                     f"energía {pct(c(lambda x: x['energia']['novel']['buena'], nov))}")
            verdict[v][f"cascada{k}_silenciosa"] = c(lambda x: x["novel"]["buena"], nov)
            verdict[v][f"cascada{k}_msp_silenciosa"] = c(lambda x: x["msp"]["novel"]["buena"], nov)
            verdict[v][f"cascada{k}_falsa_alarma"] = c(lambda x: x["conocido"]["falsa_alarma"], P)
        L.append("  por pieza, nuevo pasa en silencio (red · cascada k=1 · k=8): " + " | ".join(
            f"{p} {pct(R[p]['red']['novel']['buena'])}·{pct(R[p]['cascada']['1']['novel']['buena'])}·{pct(R[p]['cascada']['8']['novel']['buena'])}"
            for p in nov))
    L.append(f"\n[criterio] {json.dumps(verdict)}")
    L.append(f"\nTiempo total: {res.get('segundos', 0) / 60:.0f} min")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
