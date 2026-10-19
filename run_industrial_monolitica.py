"""
Memoria única contra partición en el demo industrial (VisA), con el mismo contenido.
Diseño fijado en propuesta_industrial_monolitica.md.

  global   latentes del nivel 1 y su cuantización. M = una hetero etiqueta <-> latente
           (etiqueta fastText del término de cada pieza, como exp21) + una homo de todo
           el llenado; contra el protocolo transactivo, los especialistas y G1/G2.
  parches  PCA y cuantización comunes a las 12 piezas. S especialista por pieza,
           M hetero con etiquetas, U una homo con todo.

Lee las cachés del demo (results/industrial/cache del worktree indicado) sin escribir en ellas.

Uso:
  python run_industrial_monolitica.py --cache-demo <carpeta> [--sin-parches]
  python run_industrial_monolitica.py --report-only
"""
import argparse
import contextlib
import io
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
import commons  # noqa: E402
from associative import AssociativeMemory  # noqa: E402
from hetero_memory import HeteroAssociativeMemory, _norm_weights  # noqa: E402
from quantizer import quantize_binary  # noqa: E402
from stage5_fill import quantize_latent_global  # noqa: E402
from stage7_bidirectional import recognize_gated_right  # noqa: E402
from run_experiment17_specific_word import support_ranking  # noqa: E402

OUT = ROOT / "results" / "industrial_monolitica"
CACHE = OUT / "cache"
PIECES, N_FILL, Q, SEED, PAD = ind.PIECES, ind.N_FILL, ind.Q, ind.SEED, ind.PAD
TERMS = {"candle": "candle", "capsules": "capsules", "cashew": "cashew", "chewinggum": "chewing gum",
         "fryum": "snack wheel", "macaroni1": "macaroni one", "macaroni2": "macaroni two",
         "pcb1": "pcb one", "pcb2": "pcb two", "pcb3": "pcb three", "pcb4": "pcb four",
         "pipe_fryum": "snack pipe"}
NL, ML = 300, 16
DEV = ind.DEV


def label_vectors():
    path = CACHE / "etiquetas.json"
    if path.exists():
        raw = json.loads(path.read_text())
    else:
        from stage4_fasttext import _stream_lookup
        words = {w for t in TERMS.values() for w in t.split()}
        ft = _stream_lookup(words)
        assert words <= set(ft), words - set(ft)
        raw = {p: np.mean([ft[w] for w in t.split()], axis=0).tolist() for p, t in TERMS.items()}
        path.write_text(json.dumps(raw))
    return {p: quantize_binary(np.asarray(v), ML) for p, v in raw.items()}


def composed_relation(lv, counts):
    """Relación (300, 64, 16, Q) de inscribir (lv[p], z) por cada z del llenado de p:
    el contador suma 1 por inscripción y satura en 2^16 - 1."""
    R = np.zeros((NL, 64, ML, Q), dtype=np.int64)
    for p, c in counts.items():
        R[np.arange(NL), :, lv[p], :] += c[None]
    return np.minimum(R, 2 ** 16 - 1)


def hetero_from(R):
    with contextlib.redirect_stdout(io.StringIO()):
        mem = HeteroAssociativeMemory(NL, ML, 64, Q)
    mem._relation[:, :, :ML, :Q] = R
    mem._updated = False
    with contextlib.redirect_stdout(io.StringIO()):
        mem.update()
    return mem


def homo_from(count):
    """Homo con la relación de inscribir esos conteos (mismo contador saturado)."""
    mem = HomoAssociativeMemory(64, Q)
    with contextlib.redirect_stdout(io.StringIO()):
        mem._am = AssociativeMemory(64, Q, commons.ExperimentSettings(iota=0.0, kappa=0.0, xi=0, sigma=0.1),
                                    relation=np.minimum(count, 2 ** 16 - 1))
    return mem


def hist(zq):
    c = np.zeros((64, Q), dtype=np.int64)
    np.add.at(c, (np.tile(np.arange(64), len(zq)), zq.reshape(-1)), 1)
    return c


def check_composition(lv, fill_q):
    """register oficial contra la relación compuesta, sobre 1 imagen x 16 variantes por pieza."""
    with contextlib.redirect_stdout(io.StringIO()):
        ref = HeteroAssociativeMemory(NL, ML, 64, Q)
    sub = {p: fill_q[p][:16] for p in PIECES}
    for p in PIECES:
        for zq in sub[p]:
            ref.register(lv[p], zq)
    R = composed_relation(lv, {p: hist(sub[p]) for p in PIECES})
    homo = HomoAssociativeMemory(64, Q)
    for p in PIECES:
        for zq in sub[p]:
            homo.register(zq)
    hU = homo_from(sum(hist(sub[p]) for p in PIECES))
    same = bool(np.array_equal(ref._relation[:, :, :ML, :Q], R)) and bool(np.array_equal(homo._am._relation, hU._am._relation))
    print(f"  composición = register oficial en {16 * len(PIECES)} inscripciones (hetero y homo): {same}", flush=True)
    assert same
    return same


def m_project(mem_H, mem_R, zq):
    with contextlib.redirect_stdout(io.StringIO()):
        return mem_H.project(mem_H.validate(zq, 1), _norm_weights(mem_R.recog_weights(zq), 64), 1)


# ---------- percepción global ----------

def run_global(lv):
    t0 = time.time()
    F5 = ind.global_feats()
    P1 = ind.pca(np.concatenate([ind.imgs()[f"f512all_{p}"] for p in PIECES]))
    reg1 = {p: ind.proj(P1, F5[f"reg_{p}"]) for p in PIECES}
    fill1 = {p: reg1[p][:N_FILL] for p in PIECES}
    pa1 = {p: reg1[p][N_FILL:] for p in PIECES}
    test1 = {p: ind.proj(P1, F5[f"test_{p}"]) for p in PIECES}
    L1 = demo.Level("nivel1", PIECES, None, fill1, pa1)
    print(f"  nivel 1 de la partición listo ({time.time() - t0:.0f} s)", flush=True)

    fill_q = {p: L1.q(fill1[p].reshape(-1, 64)) for p in PIECES}
    check = check_composition(lv, fill_q)
    mem_H = hetero_from(composed_relation(lv, {p: hist(fill_q[p]) for p in PIECES}))
    mem_R = HomoAssociativeMemory(64, Q)
    for p in PIECES:
        for zq in fill_q[p]:
            mem_R.register(zq)
    print(f"  M lista ({time.time() - t0:.0f} s)", flush=True)

    def judge(z, k, p, test):
        r = {"energia": bool(np.linalg.norm(z) >= L1.tau)}
        zq = L1.q(z)
        proj = m_project(mem_H, mem_R, zq)
        r["M_vacias"] = int(np.count_nonzero(proj.sum(1) == 0))
        r["M"] = support_ranking(proj, PIECES, lv)[0][0] if r["energia"] and r["M_vacias"] == 0 else None
        unc = int(np.count_nonzero(L1.agents[p].mem_dom_R.recog_weights(zq) == 0))
        r["G1_sin_soporte"] = unc
        r["G1_acepta"] = r["energia"] and unc == 0
        if test:
            sc = {m: recognize_gated_right(L1.agents[m], zq) for m in PIECES}
            r["esp"] = max(sc, key=sc.get) if r["energia"] and sum(sc.values()) > 0 else None
            r["prot"] = L1.route(z, k)[0]
            r["knn"] = L1.knn(z)
        return r

    res = {"composicion_verificada": check, "terminos": TERMS,
           "etiquetas_distintas": len({tuple(v) for v in lv.values()}), "piezas": {}}
    allfill = np.concatenate([fill1[p][:, 0] for p in PIECES])
    g_all = ind.Gauss(allfill)
    for k, p in enumerate(PIECES):
        y = ind.imgs()[f"testy_{p}"]
        cal, te = pa1[p][:, 0], test1[p]
        rc = [judge(z, k, p, False) for z in cal]
        rt = [judge(z, k, p, True) for z in te]
        g = ind.Gauss(fill1[p][:, 0])
        f0 = fill1[p][:, 0]
        s = lambda Z, R: {"M_graduada": -np.array([r["M_vacias"] for r in R]),
                          "knn": ind.knn_score(f0, Z), "maha": g.score(Z), "knn_euclid": ind.knn_euclid(f0, Z),
                          "knn_unico": ind.knn_score(allfill, Z), "knn_euclid_unico": ind.knn_euclid(allfill, Z),
                          "maha_unica": g_all.score(Z)}
        s_cal, s_te = s(cal, rc), s(te, rt)
        accM = lambda R: np.array([r["M"] is not None for r in R])
        accG = lambda R: np.array([r["G1_acepta"] for r in R])
        # en detección cuenta el rechazo; a qué pieza va M se mide en el ruteo
        res["piezas"][p] = {
            "filas_test": rt, "filas_cal": rc,
            "M": ind.compare(accM(rc).mean(), ~accM(rt), s_cal, s_te, y),
            "G1": ind.compare(accG(rc).mean(), ~accG(rt), {k_: v for k_, v in s_cal.items() if k_ != "M_graduada"},
                              {k_: v for k_, v in s_te.items() if k_ != "M_graduada"}, y),
            "G1_graduada_auroc": ind.auroc(-np.array([r["G1_sin_soporte"] for r in rt])[y == 0],
                                           -np.array([r["G1_sin_soporte"] for r in rt])[y == 1]),
        }
        # G2 del demo, para el punta a punta de la partición
        P2 = ind.pca(F5[f"reg_{p}"][:N_FILL, 0])
        sp2 = ind.Specialist(ind.proj(P2, F5[f"reg_{p}"])[:N_FILL])
        test2 = ind.proj(P2, F5[f"test_{p}"])
        cal2 = ind.proj(P2, F5[f"reg_{p}"])[N_FILL:, 0]
        res["piezas"][p]["G2"] = {"acepta_cal": float(np.mean([sp2.accepts(z) for z in cal2])),
                                  "acepta_test": [bool(sp2.accepts(z)) for z in test2]}
        print(f"  global {p} listo ({time.time() - t0:.0f} s)", flush=True)
    return res


# ---------- parches con espacio común ----------

def patch_space():
    """PCA común ajustada sobre 32 parches al azar de cada imagen de llenado de cada pieza."""
    path = CACHE / "pca_parches.npz"
    if path.exists():
        z = np.load(path)
        return z["mu"], z["V"]
    net = ind.backbone()
    rng = np.random.RandomState(SEED)
    sample = []
    for p in PIECES:
        for a in range(0, N_FILL, 30):
            f = ind.patch_feats(net, ind.imgs()[f"reg_{p}"][a:min(a + 30, N_FILL)])
            sample.append(np.stack([im[rng.choice(784, 32, replace=False)] for im in f]))
        print(f"  muestra de parches {p}", flush=True)
    mu, V = ind.pca(np.concatenate(sample).reshape(-1, sample[0].shape[-1]))
    np.savez(path, mu=mu, V=V)
    return mu, V


def patch_cache(P):
    net = None
    for p in PIECES:
        path = CACHE / f"parches_comun_{p}.npz"
        if path.exists():
            continue
        net = net or ind.backbone()
        reg = np.concatenate([ind.proj(P, ind.patch_feats(net, ind.imgs()[f"reg_{p}"][a:a + 50]))
                              for a in range(0, len(ind.imgs()[f"reg_{p}"]), 50)])
        test = np.concatenate([ind.proj(P, ind.patch_feats(net, ind.imgs()[f"test_{p}"][a:a + 50]))
                               for a in range(0, len(ind.imgs()[f"test_{p}"]), 50)])
        np.savez(path, fill=reg[:N_FILL], cal=reg[N_FILL:], test=test)
        print(f"  parches comunes {p} listos", flush=True)


def load_patches(p):
    z = np.load(CACHE / f"parches_comun_{p}.npz")
    return z["fill"], z["cal"], z["test"]


class GroupRule:
    """Aceptación de M por parche sin proyectar: la fila i tiene soporte si algún nivel a
    tiene, en las 64 coordenadas, alguna pieza con ese nivel que contenga el valor."""

    def __init__(self, lv, supp):
        mask = np.zeros((64, Q), dtype=np.int64)
        for k, p in enumerate(PIECES):
            mask |= supp[p].astype(np.int64) << k
        groups, member = {}, []
        for i in range(NL):
            for a in range(ML):
                g = sum(1 << k for k, p in enumerate(PIECES) if lv[p][i] == a)
                if g:
                    member.append((i, groups.setdefault(g, len(groups))))
        A = np.zeros((NL, len(groups)), dtype=np.float32)
        for i, gi in member:
            A[i, gi] = 1
        self.mask = torch.tensor(mask, device=DEV)
        self.groups = torch.tensor(list(groups), device=DEV)
        self.A = torch.tensor(A, device=DEV)

    def empty_rows(self, zq):
        """(n,) filas vacías de la proyección de cada parche."""
        out = []
        for a in range(0, len(zq), 512):
            z = torch.tensor(zq[a:a + 512], device=DEV, dtype=torch.long)
            m = self.mask[torch.arange(64, device=DEV)[None], z]
            cov = ((m[:, :, None] & self.groups[None, None]) != 0).all(1).float()
            out.append((NL - ((cov @ self.A.T) > 0).sum(1)).cpu().numpy())
        return np.concatenate(out)


def run_patches(lv):
    t0 = time.time()
    P = patch_space()
    patch_cache(P)
    print(f"  parches comunes listos ({time.time() - t0:.0f} s)", flush=True)
    lo = hi = None
    for p in PIECES:
        f = load_patches(p)[0].reshape(-1, 64)
        lo = f.min(0) if lo is None else np.minimum(lo, f.min(0))
        hi = f.max(0) if hi is None else np.maximum(hi, f.max(0))
    g = (lo - PAD * (hi - lo), hi + PAD * (hi - lo))
    qz = lambda Z: quantize_latent_global(Z.reshape(-1, 64), *g, Q)
    counts = {}
    for p in PIECES:
        counts[p] = hist(qz(load_patches(p)[0]))
    supp = {p: counts[p] > 0 for p in PIECES}
    suppU = np.any([supp[p] for p in PIECES], axis=0)
    rule = GroupRule(lv, supp)

    # verificación de la regla y de U contra el código oficial, en parches de test de todas las piezas
    mem_H = hetero_from(composed_relation(lv, counts))
    mem_U = homo_from(sum(counts.values()))
    rng = np.random.RandomState(SEED)
    sample = []
    for p in PIECES:
        te = qz(load_patches(p)[2])
        er = rule.empty_rows(te)
        pick = list(rng.choice(len(te), 150, replace=False)) + list(np.argsort(-er)[:50])
        sample.append(te[pick])
    sample = np.concatenate(sample)
    er = rule.empty_rows(sample)
    off = np.array([np.count_nonzero(m_project(mem_H, mem_U, z).sum(1) == 0) for z in sample])
    uU_rule = np.array([np.count_nonzero(~suppU[np.arange(64), z]) for z in sample])
    uU_off = np.array([np.count_nonzero(mem_U.recog_weights(z) == 0) for z in sample])
    verif = {"parches": int(len(sample)), "M_filas_vacias_iguales": bool(np.array_equal(er, off)),
             "M_rechaza_en_muestra": int((off > 0).sum()),
             "U_iguales": bool(np.array_equal(uU_rule, uU_off)), "U_rechaza_en_muestra": int((uU_off > 0).sum())}
    print(f"  verificación parches: {verif}", flush=True)
    assert verif["M_filas_vacias_iguales"] and verif["U_iguales"]
    del mem_H

    res = {"verificacion": verif, "soporte_medio_U": float(suppU.sum(1).mean()),
           "soporte_medio_S": {p: float(supp[p].sum(1).mean()) for p in PIECES}, "piezas": {}}
    for p in PIECES:
        y = ind.imgs()[f"testy_{p}"]
        fill, cal, test = load_patches(p)

        def per_image(Z):
            zq = qz(Z)
            n = Z.shape[1]
            uS = np.count_nonzero(~supp[p][np.arange(64), zq], axis=1).reshape(-1, n).max(1)
            uU = np.count_nonzero(~suppU[np.arange(64), zq], axis=1).reshape(-1, n).max(1)
            eM = rule.empty_rows(zq).reshape(-1, n).max(1)
            return uS, eM, uU

        c, t = per_image(cal), per_image(test)
        bank = torch.tensor(fill.reshape(-1, 64), device=DEV)
        gs = ind.Gauss(fill.reshape(-1, 64))

        def nn_score(Z):
            out = []
            for im in Z:
                q = torch.tensor(im, device=DEV)
                d = torch.cat([torch.cdist(q[i:i + 196], bank).min(1).values for i in range(0, len(q), 196)])
                out.append(-float(d.max()))
            return np.array(out)

        s_cal = {"knn": nn_score(cal), "maha": np.array([gs.score(im).min() for im in cal])}
        s_te = {"knn": nn_score(test), "maha": np.array([gs.score(im).min() for im in test])}
        r = {"inclusion": {
            "M_rechaza_S_acepta": int(np.sum((c[1] > 0) & (c[0] == 0)) + np.sum((t[1] > 0) & (t[0] == 0))),
            "U_rechaza_M_acepta": int(np.sum((c[2] > 0) & (c[1] == 0)) + np.sum((t[2] > 0) & (t[1] == 0)))}}
        for name, idx in (("S", 0), ("M", 1), ("U", 2)):
            r[name] = ind.compare(np.mean(c[idx] == 0), t[idx] > 0,
                                  dict(s_cal, graduada=-c[idx]), dict(s_te, graduada=-t[idx]), y)
        res["piezas"][p] = r
        del bank
        torch.cuda.empty_cache()
        print(f"  parches {p} listo ({time.time() - t0:.0f} s)", flush=True)
    return res


# ---------- informe ----------

def pct(x):
    return f"{100 * x:5.1f}"


def report(res):
    from collections import Counter
    G = res["global"]
    L = ["Memoria única (M) contra partición, demo industrial VisA. Mismo contenido: 270 x 16 de llenado por pieza."]
    L.append(f"Composición de M = register oficial: {G['composicion_verificada']} · etiquetas distintas "
             f"{G['etiquetas_distintas']}/12 · términos {json.dumps(G['terminos'], ensure_ascii=False)}")
    rows = [dict(r, verdad=p) for p in PIECES for r in G["piezas"][p]["filas_test"]]
    ys = np.concatenate([ind.imgs()[f"testy_{p}"] for p in PIECES])
    L.append("\n[ruteo por pieza · test completo]")
    for lab, name in ((0, "normales"), (1, "fallas")):
        rs = [r for r, yy in zip(rows, ys) if yy == lab]
        n = len(rs)
        for arm, title in (("M", "M única        "), ("prot", "T-protocolo    "), ("esp", "T-especialistas"),
                           ("knn", "kNN            ")):
            ok = sum(r[arm] == r["verdad"] for r in rs)
            rej = sum(r[arm] is None for r in rs)
            L.append(f"  {name:<8} n={n} {title}: acierto {pct(ok / n)} · rechazo {pct(rej / n)} · "
                     f"falso {pct((n - ok - rej) / n)} · de lo respondido {pct(ok / max(n - rej, 1))}")
    for arm in ("M", "prot"):
        conf = Counter((r["verdad"], r[arm]) for r in rows if r[arm] and r[arm] != r["verdad"])
        L.append(f"  falsos {arm}: " + (", ".join(f"{a}->{b} {c}" for (a, b), c in conf.most_common(8)) or "ninguno"))
    L.append("  por pieza (M acierto/rechazo/falso · protocolo acierto/rechazo/falso), todo el test:")
    for p in PIECES:
        rs = [r for r in rows if r["verdad"] == p]
        f = lambda a: (sum(r[a] == p for r in rs), sum(r[a] is None for r in rs))
        (om, rm), (op, rp) = f("M"), f("prot")
        L.append(f"    {p:<11} n={len(rs):>3}  M {om:>3}/{rm:>3}/{len(rs) - om - rm:>3} · prot {op:>3}/{rp:>3}/{len(rs) - op - rp:>3}")

    L.append("\n[detección · percepción global del nivel 1] detección / falsa alarma en test (%), AUROC entre paréntesis")
    viol = sum((r["M"] is None) and r["G1_acepta"]
               for p in PIECES for r in G["piezas"][p]["filas_test"] + G["piezas"][p]["filas_cal"])
    L.append(f"  inclusión: imágenes rechazadas por M y aceptadas por el especialista G1 de su pieza = {viol}")
    keys = ["knn", "knn_euclid", "maha", "knn_unico", "knn_euclid_unico", "maha_unica"]
    for arm in ("M", "G1"):
        L.append(f"  a la aceptación de calibración de {arm}:")
        for p in PIECES:
            r = G["piezas"][p][arm]
            L.append(f"    {p:<11} acepta cal {pct(r['acepta_calibracion'])} · {arm} {pct(r['memoria']['deteccion'])} / "
                     f"{pct(r['memoria']['falsa_alarma'])} · " + " · ".join(
                         f"{k} {pct(r[k]['deteccion'])} / {pct(r[k]['falsa_alarma'])} ({r[k]['auroc']:.3f})" for k in keys))
        m = lambda f: np.mean([f(G["piezas"][p][arm]) for p in PIECES])
        L.append(f"    media       acepta cal {pct(m(lambda r: r['acepta_calibracion']))} · {arm} "
                 f"{pct(m(lambda r: r['memoria']['deteccion']))} / {pct(m(lambda r: r['memoria']['falsa_alarma']))} · "
                 + " · ".join(f"{k} {pct(m(lambda r: r[k]['deteccion']))} / {pct(m(lambda r: r[k]['falsa_alarma']))} "
                              f"({m(lambda r: r[k]['auroc']):.3f})" for k in keys))
    L.append(f"  AUROC graduada: M {np.mean([G['piezas'][p]['M']['M_graduada']['auroc'] for p in PIECES]):.3f} · "
             f"G1 {np.mean([G['piezas'][p]['G1_graduada_auroc'] for p in PIECES]):.3f}")

    L.append("\n[punta a punta] alarma = rechazo; la partición rutea y decide el especialista del destino")
    out = Counter()
    for p in PIECES:
        d = G["piezas"][p]
        for r, yy, a2 in zip(d["filas_test"], ind.imgs()[f"testy_{p}"], d["G2"]["acepta_test"]):
            tag = "falla" if yy else "normal"
            out[(tag, "M", "alarma" if r["M"] is None else ("pasa" if r["M"] == p else "otra pieza"))] += 1
            for sp, acc in (("T+G1", r["G1_acepta"]), ("T+G2", a2)):
                v = "alarma" if r["prot"] is None else ("otra pieza" if r["prot"] != p else ("pasa" if acc else "alarma"))
                out[(tag, sp, v)] += 1
    for tag in ("normal", "falla"):
        for sp in ("M", "T+G1", "T+G2"):
            n = sum(v for (t, s, _), v in out.items() if t == tag and s == sp)
            L.append(f"  {tag:<6} {sp:<5} n={n}: " + " · ".join(
                f"{k} {pct(out[(tag, sp, k)] / n)}" for k in ("alarma", "pasa", "otra pieza")))

    if "parches" in res:
        Pp = res["parches"]
        L.append(f"\n[detección · parches con PCA y cuantización comunes] verificación {json.dumps(Pp['verificacion'])}")
        L.append(f"  soporte medio por coordenada: U {Pp['soporte_medio_U']:.1f}/32 · S "
                 f"{np.mean(list(Pp['soporte_medio_S'].values())):.1f}/32 (media de piezas)")
        inc = {k: sum(Pp["piezas"][p]["inclusion"][k] for p in PIECES) for k in ("M_rechaza_S_acepta", "U_rechaza_M_acepta")}
        L.append(f"  inclusión: {json.dumps(inc)}")
        for arm in ("S", "M", "U"):
            L.append(f"  {arm}:")
            for p in PIECES:
                r = Pp["piezas"][p][arm]
                L.append(f"    {p:<11} acepta cal {pct(r['acepta_calibracion'])} · {arm} {pct(r['memoria']['deteccion'])} / "
                         f"{pct(r['memoria']['falsa_alarma'])} · " + " · ".join(
                             f"{k} {pct(r[k]['deteccion'])} / {pct(r[k]['falsa_alarma'])} ({r[k]['auroc']:.3f})"
                             for k in ("graduada", "knn", "maha")))
            m = lambda f: np.mean([f(Pp["piezas"][p][arm]) for p in PIECES])
            L.append(f"    media       acepta cal {pct(m(lambda r: r['acepta_calibracion']))} · {arm} "
                     f"{pct(m(lambda r: r['memoria']['deteccion']))} / {pct(m(lambda r: r['memoria']['falsa_alarma']))} · "
                     + " · ".join(f"{k} {pct(m(lambda r: r[k]['deteccion']))} / {pct(m(lambda r: r[k]['falsa_alarma']))} "
                                  f"({m(lambda r: r[k]['auroc']):.3f})" for k in ("graduada", "knn", "maha")))
    L.append(f"\nTiempo total: {res.get('segundos', 0) / 60:.0f} min")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-demo", default=str(ROOT.parent / "industrial-demo-4132e4" / "results" / "industrial" / "cache"))
    ap.add_argument("--sin-parches", action="store_true")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    ind.CACHE = Path(args.cache_demo)
    CACHE.mkdir(parents=True, exist_ok=True)
    raw = OUT / "resultados.json"
    if not args.report_only:
        t0 = time.time()
        lv = label_vectors()
        res = {"global": run_global(lv)}
        raw.write_text(json.dumps(res, ensure_ascii=False))
        if not args.sin_parches:
            res["parches"] = run_patches(lv)
        res["segundos"] = round(time.time() - t0)
        raw.write_text(json.dumps(res, ensure_ascii=False))
    report(json.loads(raw.read_text()))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
