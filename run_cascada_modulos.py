"""
Cascada de módulos sobre la red especializada del cierre: malas -> buenas partidas en k
especialistas (k-means) -> revisión humana. Diseño en propuesta_cascada_modulos.md.

Uso: python run_cascada_modulos.py [--report-only]
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from sklearn.cluster import KMeans

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_cierre_mae as cm  # noqa: E402
import run_industrial_demo as ind  # noqa: E402

OUT = ROOT / "results" / "cascada_modulos"
CACHE = OUT / "cache"            # fuera de git
PIECES, N_FILL, PAD, SEED = ind.PIECES, ind.N_FILL, ind.PAD, 42
KS = (1, 2, 4, 8)


def latents(p):
    path = CACHE / f"lat_{p}.npz"
    if path.exists():
        return dict(np.load(path, allow_pickle=False))
    tr, te, novel, held, cnt = cm.split_defects(p)
    X, y_all, reg = ind.imgs()[f"test_{p}"], ind.imgs()[f"testy_{p}"], ind.imgs()[f"reg_{p}"]
    net, log = cm.train(p, reg[:N_FILL], X[tr])
    zn, _ = cm.encode(net, reg[:N_FILL], variants=True)
    zd, _ = cm.encode(net, X[tr], variants=True)
    zc, lc = cm.encode(net, reg[N_FILL:])
    norm_te = np.where(y_all == 0)[0]
    zt, lt = cm.encode(net, X[np.concatenate([norm_te, te])])
    yt = np.array([0] * len(norm_te) + [1] * len(te))
    zv, lv = cm.encode(net, X[novel]) if len(novel) else (np.zeros((0, 64), np.float32), np.zeros((0, 2), np.float32))
    del net
    torch.cuda.empty_cache()
    out = dict(zn=zn, zd=zd, zc=zc, lc=lc, zt=zt, lt=lt, yt=yt, zv=zv, lv=lv, held=np.array(held or ""))
    np.savez(path, **out)
    return out


def cascade(md, goods, Z):
    out = []
    for z in Z:
        if md.read(z)[0] == 0:
            out.append("mala")
        elif any(g.read(z)[0] == 0 for g in goods):
            out.append("buena")
        else:
            out.append("desconocida")
    return np.array(out)


def frac(d):
    return {k: float(np.mean(d == k)) if len(d) else 0.0 for k in ("desconocida", "mala", "buena")}


def rival(conf_known, conf_novel, base_known, base_novel, a, low_is_unknown=True):
    """Abstención a la fracción a del test conocido; el resto lo decide base."""
    if a <= 0:
        ab_k, ab_v = np.zeros(len(conf_known), bool), np.zeros(len(conf_novel), bool)
    elif low_is_unknown:
        thr = np.quantile(conf_known, a)
        ab_k, ab_v = conf_known < thr, conf_novel < thr
    else:
        thr = np.quantile(conf_known, 1 - a)
        ab_k, ab_v = conf_known > thr, conf_novel > thr
    return np.where(ab_k, "desconocida", base_known), np.where(ab_v, "desconocida", base_novel)


def known_rates(d, y):
    return {"deteccion": float(np.mean(d[y == 1] == "mala")), "falsa_alarma": float(np.mean(d[y == 0] == "mala")),
            "revision_normales": float(np.mean(d[y == 0] == "desconocida")),
            "revision_fallas": float(np.mean(d[y == 1] == "desconocida")),
            "pasa_fallas": float(np.mean(d[y == 1] == "buena"))}


def piece(p):
    L = latents(p)
    zn, zd, zc, zt, yt, zv = L["zn"], L["zd"], L["zc"], L["zt"], L["yt"], L["zv"]
    lt, lv = L["lt"], L["lv"]
    allz = np.concatenate([zn[:, 0], zd[:, 0]])
    lo, hi = allz.min(0), allz.max(0)
    g = (lo - PAD * (hi - lo), hi + PAD * (hi - lo))
    md = cm.Mem(zd, g)
    bank = np.concatenate([zn[:, 0], zd[:, 0]])
    lab = np.array([0] * len(zn) + [1] * len(zd))

    def knn(Z):
        d2 = ((Z[:, None] - bank[None]) ** 2).sum(2)
        o = np.argsort(d2, 1)[:, :5]
        return np.where(lab[o].mean(1) > 0.5, "mala", "buena"), np.sqrt(np.sort(d2, 1)[:, :5]).mean(1)

    st, sv = cm.softmax(lt), cm.softmax(lv) if len(lv) else np.zeros((0, 2))
    arg_t, arg_v = np.where(st[:, 1] > 0.5, "mala", "buena"), np.where(sv[:, 1] > 0.5, "mala", "buena")
    msp_t, msp_v = st.max(1), sv.max(1) if len(sv) else np.zeros(0)
    en_t = np.log(np.exp(lt).sum(1))
    en_v = np.log(np.exp(lv).sum(1)) if len(lv) else np.zeros(0)
    kn_t, dk_t = knn(zt)
    kn_v, dk_v = knn(zv) if len(zv) else (np.zeros(0, str), np.zeros(0))
    r = {"excluido": str(L["held"]), "n_novel": int(len(zv)), "cabeza": known_rates(arg_t, yt), "k": {}}
    for k in KS:
        lab_k = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit_predict(zn[:, 0]) if k > 1 else np.zeros(len(zn), int)
        goods = [cm.Mem(zn[lab_k == c], g) for c in range(k)]
        d_t, d_c, d_v = cascade(md, goods, zt), cascade(md, goods, zc), cascade(md, goods, zv)
        a = float(np.mean(d_t == "desconocida"))
        row = {"tamanos": np.bincount(lab_k).tolist(), "conocido": known_rates(d_t, yt),
               "calibracion": frac(d_c), "novel": frac(d_v), "revision_conocido": a, "rivales": {}}
        for name, (ck, cv, bk, bv, low) in {"msp": (msp_t, msp_v, arg_t, arg_v, True), "energia": (en_t, en_v, arg_t, arg_v, True),
                                           "knn_distancia": (dk_t, dk_v, kn_t, kn_v, False)}.items():
            rk, rv = rival(ck, cv, bk, bv, a, low)
            row["rivales"][name] = {"conocido": known_rates(rk, yt), "novel": frac(rv)}
        r["k"][str(k)] = row
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    raw = OUT / "resultados.json"
    if not args.report_only:
        t0 = time.time()
        res = {}
        for p in PIECES:
            res[p] = piece(p)
            print(f"  {p} listo ({time.time() - t0:.0f} s)", flush=True)
        res["segundos"] = round(time.time() - t0)
        raw.write_text(json.dumps(res, ensure_ascii=False))
    report(json.loads(raw.read_text()))


def pct(x):
    return f"{100 * x:5.1f}"


def report(res):
    P = [p for p in PIECES if p in res]
    nov = [p for p in P if res[p]["n_novel"] > 0]
    L = ["Cascada de módulos (propuesta_cascada_modulos.md): malas -> buenas partidas en k -> revisión humana."]
    m = lambda f, ps: float(np.mean([f(res[p]) for p in ps]))
    L.append(f"cabeza (argmax, sin revisión), conocido: detección {pct(m(lambda r: r['cabeza']['deteccion'], P))} · "
             f"falsa alarma {pct(m(lambda r: r['cabeza']['falsa_alarma'], P))}")
    L.append("\n[media] conocido: detección / falsa alarma / revisión normales / revisión fallas · calibración: revisión · "
             "tipo nuevo: revisión / mala / buena (silenciosa) · rivales a igual revisión: tipo nuevo buena (silenciosa)")
    verdict = {}
    for k in map(str, KS):
        c = lambda f, ps=P: m(lambda r: f(r["k"][k]), ps)
        line = (f"  k={k}: {pct(c(lambda x: x['conocido']['deteccion']))} / {pct(c(lambda x: x['conocido']['falsa_alarma']))} / "
                f"{pct(c(lambda x: x['conocido']['revision_normales']))} / {pct(c(lambda x: x['conocido']['revision_fallas']))} · "
                f"cal {pct(c(lambda x: x['calibracion']['desconocida']))} · nuevo {pct(c(lambda x: x['novel']['desconocida'], nov))} / "
                f"{pct(c(lambda x: x['novel']['mala'], nov))} / {pct(c(lambda x: x['novel']['buena'], nov))}")
        sil = {}
        for name in ("msp", "energia", "knn_distancia"):
            sil[name] = c(lambda x: x["rivales"][name]["novel"]["buena"], nov)
            line += f" · {name} {pct(sil[name])} (detección {pct(c(lambda x: x['rivales'][name]['conocido']['deteccion']))}, fa {pct(c(lambda x: x['rivales'][name]['conocido']['falsa_alarma']))})"
        L.append(line)
        verdict[k] = {"silenciosa_cascada": c(lambda x: x["novel"]["buena"], nov), "silenciosa_msp": sil["msp"],
                      "silenciosa_energia": sil["energia"],
                      "falsa_alarma_cascada": c(lambda x: x["conocido"]["falsa_alarma"]),
                      "falsa_alarma_cabeza": m(lambda r: r["cabeza"]["falsa_alarma"], P)}
    L.append("\n[por pieza, tipo nuevo] revisión / mala / buena para k = 1, 2, 4, 8 · MSP a igual revisión")
    for p in nov:
        r = res[p]
        L.append(f"  {p:<11} «{r['excluido']}» n={r['n_novel']:>3} · " + " | ".join(
            f"k={k} {pct(r['k'][k]['novel']['desconocida'])}/{pct(r['k'][k]['novel']['mala'])}/{pct(r['k'][k]['novel']['buena'])} "
            f"(msp {pct(r['k'][k]['rivales']['msp']['novel']['buena'])})" for k in map(str, KS)))
    L.append(f"\n[criterio] {json.dumps(verdict)}")
    L.append(f"\nTiempo total: {res.get('segundos', 0) / 60:.0f} min")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
