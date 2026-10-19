"""
Los parámetros nativos de la MAE (poda ι y peso medio κ) como lectura para detectar fallas.
Diseño en propuesta_parametros_mae.md.

Lecturas sobre la relación R (64 x 32): contención con poda ι, peso medio K y suma de
log-frecuencias H. Percepciones: G2 ResNet18, G2 WideResNet50, parches ResNet18.
6 piezas de diseño eligen ι y la lectura; 6 de confirmación las miden una vez.

Uso: python run_parametros_mae.py [--report-only]
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_industrial_demo as ind  # noqa: E402
import run_medico_demo as demo  # noqa: E402
from associative_memory import HomoAssociativeMemory  # noqa: E402

OUT = ROOT / "results" / "parametros_mae"
CACHE = OUT / "cache"            # fuera de git
PIECES, N_FILL, Q, PAD, SEED = ind.PIECES, ind.N_FILL, ind.Q, ind.PAD, 42
IOTAS = (0.0, 0.25, 0.5, 1.0)
ACC = 0.95
idx64 = np.arange(64)


def grid(Z):
    Z = Z.reshape(-1, 64)
    lo, hi = Z.min(0), Z.max(0)
    return lo - PAD * (hi - lo), hi + PAD * (hi - lo)


def quant(Z, g):
    return demo.quantize_latent_global(np.asarray(Z, dtype=np.float32).reshape(-1, 64), *g, Q)


def relation(Z, g):
    q = quant(Z, g)
    R = np.zeros((64, Q), dtype=np.int64)
    np.add.at(R, (np.broadcast_to(idx64, q.shape), q), 1)
    return R


def prune(R, iota):
    s = R.sum(1)
    c = np.maximum(np.count_nonzero(R, 1), 1)
    return np.where(R < (iota * s / c)[:, None], 0, R)


def readings(R, Z, g):
    """Por pista: celdas leídas (n, 64) de la relación sin podar."""
    q = quant(Z, g)
    return q, R[idx64, q]


def verify(R, Zfill, Zprobe, g):
    """Contra la API oficial: relación, pesos y bandera de reconocimiento con ι."""
    out = {}
    for iota in IOTAS:
        mem = HomoAssociativeMemory(64, Q, iota=iota)
        for z in Zfill.reshape(-1, 64):
            mem.register(quant(z[None], g)[0])
        same_rel = bool(np.array_equal(mem._am.relation, R))
        Rp = prune(R, iota)
        bad = 0
        for z in Zprobe:
            v = quant(z[None], g)[0]
            rec, w = mem._am.recog_weights(v)
            mine_rec = bool(np.all(Rp[idx64, v] > 0))
            bad += int(rec != mine_rec) + int(not np.array_equal(np.asarray(w), R[idx64, v]))
        out[str(iota)] = {"relacion_igual": same_rel, "discrepancias": bad, "n": len(Zprobe)}
    return out


def auroc(n, a):
    return ind.auroc(n, a)


def at_acc(s_cal, s_te, y):
    thr = np.quantile(s_cal, 1 - ACC)
    rej = s_te < thr
    return {"deteccion": float(rej[y == 1].mean()), "falsa_alarma": float(rej[y == 0].mean()),
            "auroc": auroc(s_te[y == 0], s_te[y == 1])}


def global_block(fill, cal, te, y):
    """fill (270, 16, 64), cal (m, 64), te (t, 64)."""
    g = grid(fill[:, 0])
    R = relation(fill, g)
    out = {}
    for iota in IOTAS:
        Rp = prune(R, iota)
        unc = lambda Z: (Rp[idx64, quant(Z, g)] == 0).sum(1)
        uc, ut = unc(cal), unc(te)
        out[f"C{iota}"] = {"acepta_cal": float(np.mean(uc == 0)), "deteccion": float(np.mean(ut[y == 1] > 0)),
                           "falsa_alarma": float(np.mean(ut[y == 0] > 0)), "auroc": auroc(-ut[y == 0], -ut[y == 1])}
    _, vc = readings(R, cal, g)
    _, vt = readings(R, te, g)
    out["K"] = at_acc(vc.mean(1), vt.mean(1), y)
    out["H"] = at_acc(np.log(vc + 1).sum(1), np.log(vt + 1).sum(1), y)
    gs = ind.Gauss(fill[:, 0])
    out["maha"] = at_acc(gs.score(cal), gs.score(te), y)
    out["knn"] = at_acc(ind.knn_euclid(fill[:, 0], cal), ind.knn_euclid(fill[:, 0], te), y)
    return out, (R, g)


def patch_block(fill, cal, te, y):
    """fill (270, 784, 64), cal (m, 784, 64), te (t, 784, 64)."""
    g = grid(fill)
    R = relation(fill, g)
    out = {}
    for iota in IOTAS:
        Rp = prune(R, iota)
        unc = lambda Z: np.array([(Rp[idx64, quant(im, g)] == 0).sum(1).max() for im in Z])
        uc, ut = unc(cal), unc(te)
        out[f"C{iota}"] = {"acepta_cal": float(np.mean(uc == 0)), "deteccion": float(np.mean(ut[y == 1] > 0)),
                           "falsa_alarma": float(np.mean(ut[y == 0] > 0)), "auroc": auroc(-ut[y == 0], -ut[y == 1])}
    vals = lambda Z: [R[idx64, quant(im, g)] for im in Z]
    vc, vt = vals(cal), vals(te)
    out["K"] = at_acc(np.array([v.mean(1).min() for v in vc]), np.array([v.mean(1).min() for v in vt]), y)
    out["H"] = at_acc(np.array([np.log(v + 1).sum(1).min() for v in vc]), np.array([np.log(v + 1).sum(1).min() for v in vt]), y)
    gs = ind.Gauss(fill.reshape(-1, 64))
    out["maha"] = at_acc(np.array([gs.score(im).min() for im in cal]), np.array([gs.score(im).min() for im in te]), y)
    bank = torch.tensor(fill.reshape(-1, 64), device=demo.DEV)

    def pc(Z):
        s = []
        for im in Z:
            t = torch.tensor(im, device=demo.DEV)
            d = torch.cat([torch.cdist(t[i:i + 196], bank).min(1).values for i in range(0, len(t), 196)])
            s.append(-float(d.max()))
        return np.array(s)
    out["knn"] = at_acc(pc(cal), pc(te), y)
    return out


def run():
    t0 = time.time()
    F5 = dict(np.load(ind.CACHE / "rasgos512.npz", allow_pickle=False))
    res = {"verificacion": None, "piezas": {}}
    for p in PIECES:
        y = ind.imgs()[f"testy_{p}"]
        r = {}
        P2 = ind.pca(F5[f"reg_{p}"][:N_FILL, 0])
        reg, te = ind.proj(P2, F5[f"reg_{p}"]), ind.proj(P2, F5[f"test_{p}"])
        r["g2_resnet18"], (R, g) = global_block(reg[:N_FILL], reg[N_FILL:, 0], te, y)
        if res["verificacion"] is None:
            res["verificacion"] = verify(R, reg[:N_FILL], np.concatenate([reg[N_FILL:N_FILL + 40, 0], te[:40]]), g)
            print(f"  verificación: {res['verificacion']}", flush=True)
        W = np.load(CACHE / f"wrn_{p}.npz")
        P3 = ind.pca(W["reg"][:N_FILL, 0])
        reg3, te3 = ind.proj(P3, W["reg"]), ind.proj(P3, W["test"])
        r["g2_wrn50"], _ = global_block(reg3[:N_FILL], reg3[N_FILL:, 0], te3, y)
        Z = np.load(ind.CACHE / f"parches_{p}.npz")
        r["parches_resnet18"] = patch_block(Z["fill"], Z["cal"], Z["test"], y)
        res["piezas"][p] = r
        print(f"  {p} listo ({time.time() - t0:.0f} s)", flush=True)
    perm = np.random.RandomState(SEED).permutation(len(PIECES))
    res["diseno"] = [PIECES[i] for i in sorted(perm[:6])]
    res["confirmacion"] = [PIECES[i] for i in sorted(perm[6:])]
    res["segundos"] = round(time.time() - t0)
    return res


# ---------- selección y reporte ----------

def pct(x):
    return f"{100 * x:5.1f}"


def select(res):
    D = res["diseno"]
    m = lambda per, key, f: np.mean([f(res["piezas"][p][per][key]) for p in D])
    sel = {}
    base_det = m("g2_resnet18", "C0.0", lambda x: x["deteccion"])
    base_fa = m("g2_resnet18", "C0.0", lambda x: x["falsa_alarma"])
    ok = [i for i in IOTAS if m("g2_resnet18", f"C{i}", lambda x: x["falsa_alarma"]) - base_fa <= 0.05]
    sel["iota"] = max(ok, key=lambda i: m("g2_resnet18", f"C{i}", lambda x: x["deteccion"]))
    sel["lectura"] = max(("K", "H"), key=lambda k: m("g2_resnet18", k, lambda x: x["auroc"]))
    sel["diseno_det_base"] = base_det
    return sel


def report(res):
    sel = select(res)
    L = ["Parámetros nativos de la MAE como lectura para detectar fallas (propuesta_parametros_mae.md).",
         f"Verificación contra la API oficial: {json.dumps(res['verificacion'])}",
         f"Piezas de diseño: {res['diseno']} · confirmación: {res['confirmacion']}",
         f"Elegido con las de diseño: ι = {sel['iota']} para la contención · lectura graduada {sel['lectura']}"]
    keys = [f"C{i}" for i in IOTAS] + ["K", "H", "maha", "knn"]
    verdict = {}
    for group in ("diseno", "confirmacion"):
        P = res[group]
        L.append(f"\n===== {group} ({len(P)} piezas) · detección / falsa alarma (AUROC); C(ι) en su punto de operación, el resto al 95 % de aceptación de calibración")
        for per in ("g2_resnet18", "g2_wrn50", "parches_resnet18"):
            L.append(f"  [{per}]")
            for k in keys:
                rows = [res["piezas"][p][per][k] for p in P]
                det, fa, au = (np.mean([r[x] for r in rows]) for x in ("deteccion", "falsa_alarma", "auroc"))
                extra = f" · acepta cal {pct(np.mean([r['acepta_cal'] for r in rows]))}" if k.startswith("C") else ""
                name = {"knn": "kNN / PatchCore" if per.startswith("parches") else "kNN euclídeo"}.get(k, k)
                L.append(f"    {name:<16} {pct(det)} / {pct(fa)} ({au:.3f}){extra}")
                verdict[f"{group}_{per}_{k}"] = {"det": float(det), "fa": float(fa), "auroc": float(au)}
    c = lambda k: verdict[f"confirmacion_g2_resnet18_{k}"]
    lec, iota = sel["lectura"], sel["iota"]
    v1 = c(lec)["auroc"] >= c("maha")["auroc"] - 0.03 and c(lec)["det"] >= c("maha")["det"] - 0.03
    r1 = c(lec)["auroc"] < c("maha")["auroc"] - 0.10
    v2 = c(f"C{iota}")["det"] - c("C0.0")["det"] >= 0.10 and c(f"C{iota}")["fa"] - c("C0.0")["fa"] <= 0.05
    L.append(f"\n[criterio, confirmación, G2 ResNet18] {lec}: AUROC {c(lec)['auroc']:.3f} contra Mahalanobis {c('maha')['auroc']:.3f}, "
             f"detección {pct(c(lec)['det'])} contra {pct(c('maha')['det'])} → "
             f"{'sostenido' if v1 else 'refutado' if r1 else 'entre medias'} · ι = {iota}: detección {pct(c(f'C{iota}')['det'])} contra "
             f"{pct(c('C0.0')['det'])} con ι = 0, falsa alarma {pct(c(f'C{iota}')['fa'])} contra {pct(c('C0.0')['fa'])} → "
             f"{'sostenido' if v2 else 'no sostenido'}")
    L.append(f"\nTiempo total: {res.get('segundos', 0) / 60:.0f} min")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    (OUT / "resultados.json").write_text(json.dumps({**res, "seleccion": sel, "medias": verdict}, ensure_ascii=False))
    print(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    raw = CACHE / "crudo.json"
    if not args.report_only:
        raw.write_text(json.dumps(run(), ensure_ascii=False))
    report(json.loads(raw.read_text()))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
