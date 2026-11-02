"""Líneas base de texto sin memoria asociativa sobre los mismos tokens y vectores
fastText del sistema. Diseño en README.md.

Uso:  python results/lineas_base/lineas_base_texto.py
"""
import contextlib
import glob
import io
import json
import math
import pickle
import sys
import time
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from quantizer import quantize_binary
from stage6_interaction import (
    CLASSES, AGENT_LIST, M_LABEL, get_nlp, load_all_vectors, tokenize_query,
    get_fasttext_vector, prevectorize,
)
from run_experiment9_member_loss import load_bank
from run_experiment11_monolithic import split_bank, N_TEXT_TRAIN_PER_CLASS
import run_ablation as abl

K = len(CLASSES)
TOL = 1e-9
OOD_FILE = ROOT / "results" / "experimento11" / "consultas_fuera_dominio.txt"


def dequant(q, levels=M_LABEL):
    return 2.0 * (np.asarray(q, dtype=np.float64) + 0.5) / levels - 1.0


def unit(X):
    X = np.atleast_2d(np.asarray(X, dtype=np.float64))
    return X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)


def top_set(s):
    s = np.asarray(s, dtype=np.float64)
    m = s.max()
    return [i for i in range(K) if s[i] >= m - TOL * max(1.0, abs(m))]


# ---------- clases ----------

def class_points(rep):
    pts, cls_idx, words = [], [], []
    cent, cent_w = [], []
    for ci, c in enumerate(CLASSES):
        vecs = json.loads((ROOT / f"label_vectors_{c}.json").read_text())
        freqs = json.loads((ROOT / f"labels_{c}.json").read_text())
        V, W = [], []
        for w, v in vecs.items():
            v = np.asarray(v, dtype=np.float32)
            x = dequant(quantize_binary(v, M_LABEL)) if rep == "cuant" else v.astype(np.float64)
            V.append(x); W.append(float(freqs.get(w, 0)))
            pts.append(x); cls_idx.append(ci); words.append(w)
        V, W = np.array(V), np.array(W)
        cent.append(V.mean(0))
        cent_w.append((V * W[:, None]).sum(0) / W.sum())
    return {"P": unit(np.array(pts)), "pcls": np.array(cls_idx), "words": words,
            "C": unit(np.array(cent)), "Cw": unit(np.array(cent_w))}


# ---------- decisores ----------

def nn_votes(sims_row, pcls, k):
    order = np.argsort(-sims_row, kind="stable")
    kth = sims_row[order[k - 1]]
    take = np.where(sims_row >= kth - TOL)[0]
    votes = np.zeros(K)
    for j in take:
        votes[pcls[j]] += 1.0 / len(take)
    return votes, float(sims_row[take].mean())


def decide(name, agg, X, cp):
    """X: vectores de los tokens representables (T x 300). Devuelve (scores, confianza)."""
    if agg == "media":
        X = X.mean(0, keepdims=True)
    Xu = unit(X)
    if name in ("centroide", "centroide_frec"):
        sims = Xu @ (cp["C"] if name == "centroide" else cp["Cw"]).T
        return sims.sum(0), float(sims.max(1).mean())
    k = 1 if name == "1nn" else 5
    sims = Xu @ cp["P"].T
    total, conf = np.zeros(K), []
    for row in sims:
        v, c = nn_votes(row, cp["pcls"], k)
        total += v; conf.append(c)
    return total, float(np.mean(conf))


def vote_scores(tokens, vocab):
    s = np.zeros(K)
    for t in tokens:
        for ci, c in enumerate(CLASSES):
            if t in vocab[c]:
                s[ci] += 1
    return s


def outcome(scores, truth_idx, decided):
    if not decided:
        return {"decide": False, "empate": False, "pred": None, "esperado": 0.0,
                "inf": 0, "sup": 0}
    top = top_set(scores)
    hit = truth_idx in top if truth_idx is not None else False
    return {"decide": True, "empate": len(top) > 1,
            "pred": [CLASSES[i] for i in top],
            "esperado": (1.0 / len(top)) if hit else 0.0,
            "inf": int(hit and len(top) == 1), "sup": int(hit)}


# ---------- sistema (solo lectura) ----------

def eam_early(items, agents, cache):
    out = []
    for it in items:
        s = np.zeros(K)
        for tok, vq in it["cues"]:
            for ci, c in enumerate(CLASSES):
                key = (c, tok)
                if key not in cache:
                    cache[key] = agents[c].recognize_gated(vq)
                s[ci] += cache[key]
        out.append((s, bool(it["cues"]) and s.max() > 0))
    return out


def system_mature(queries, gt, cond="B1", seed=0):
    nlp, vectors, mdoms = CTX["nlp"], CTX["vectors"], CTX["mdoms"]
    mdir_class, m_mdir, kw, predict_fn, _, _ = abl.get_condition_config(cond)
    agents, tme = abl.make_agents(mdoms, mdir_class, m_mdir, kw)
    early = abl.run_early_phase(queries, agents, tme, nlp, vectors, m_mdir)
    rng = np.random.RandomState(seed * 1000 + 42)
    mature = abl.run_mature_phase(queries, agents, nlp, vectors, rng, predict_fn, m_mdir)
    return early, mature


def count_table(form_items, early_winners):
    table, reg = {}, np.zeros(K)
    for it, w in zip(form_items, early_winners):
        if w is None:
            continue
        for tok, _ in it["cues"]:
            table.setdefault(tok, np.zeros(K))[w] += 1
            reg[w] += 1
    return table, reg


def table_scores(it, table, reg):
    s = np.zeros(K)
    for tok, _ in it["cues"]:
        if tok in table:
            s += table[tok] / (reg + 1.0)
    return s


def mcnemar(a, b):
    """a, b: listas de 0/1 (acierto). Binomial exacta de dos colas sobre discordantes."""
    n01 = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    n10 = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    n = n01 + n10
    if n == 0:
        return n10, n01, 1.0
    k = min(n01, n10)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return n10, n01, min(1.0, 2 * p)


def auroc(pos, neg):
    pos, neg = np.asarray(pos), np.asarray(neg)
    gt = (pos[:, None] > neg[None, :]).sum()
    eq = (pos[:, None] == neg[None, :]).sum()
    return float((gt + 0.5 * eq) / (len(pos) * len(neg)))


CTX = {}


def main():
    t0 = time.time()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    nlp = get_nlp()
    vectors = load_all_vectors(nlp)
    with contextlib.redirect_stdout(io.StringIO()):
        bank = load_bank(nlp, vectors)
    train, held = split_bank(bank, N_TEXT_TRAIN_PER_CLASS)
    ood_q = [l.strip() for l in OOD_FILE.read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]
    toks = set()
    for q in ood_q:
        toks.update(tokenize_query(q, nlp))
    prevectorize(vectors, toks, allow_fallback=False, persist=False)
    ood = []
    for q in ood_q:
        cues = []
        for tok in tokenize_query(q, nlp):
            v = get_fasttext_vector(tok, vectors, allow_fallback=False)
            if v is not None:
                cues.append((tok, quantize_binary(np.asarray(v, dtype=np.float32), M_LABEL)))
        ood.append({"query": q, "truth": None, "tidx": None, "cues": cues})

    for it in bank + ood:
        it["tokens"] = tokenize_query(it["query"], nlp)
        it["crudo"] = np.array([np.asarray(get_fasttext_vector(t, vectors), dtype=np.float64)
                              for t, _ in it["cues"]]) if it["cues"] else None
        it["cuant"] = np.array([dequant(vq) for _, vq in it["cues"]]) if it["cues"] else None

    parts = {"cal400": bank[:400], "proto80": bank[:80], "res171": held, "ood40": ood}
    assert len(held) == 171 and len(train) == 240, (len(train), len(held))
    vocab = {c: set(vectors[c].keys()) for c in CLASSES}
    print(f"Particiones: { {k: len(v) for k, v in parts.items()} }", flush=True)

    mdoms = abl.load_base_mdoms()
    CTX.update(nlp=nlp, vectors=vectors, mdoms=mdoms)
    eam_agents = {c: abl.Agent(c, mdoms[c]) for c in CLASSES}
    gcache = {}

    t1 = time.time()
    rows, summary = [], {}
    decisores = [("voto", "-", "-")]
    for rep in ("crudo", "cuant"):
        for name in ("centroide", "centroide_frec", "1nn", "5nn"):
            for agg in ("token", "media"):
                decisores.append((name, agg, rep))
    cps = {rep: class_points(rep) for rep in ("crudo", "cuant")}

    conf = {}
    for pname, items in parts.items():
        for (name, agg, rep) in decisores:
            key = f"{name}|{agg}|{rep}"
            res, cf = [], []
            for it in items:
                if name == "voto":
                    s = vote_scores(it["tokens"], vocab)
                    o = outcome(s, it["tidx"], s.max() > 0)
                else:
                    X = it[rep]
                    if X is None:
                        o = outcome(None, it["tidx"], False); cf.append(np.nan)
                    else:
                        s, c = decide(name, agg, X, cps[rep])
                        o = outcome(s, it["tidx"], True); cf.append(c)
                res.append(o)
                rows.append(dict(particion=pname, decisor=key, query=it["query"],
                                 truth=it["truth"], **o))
            conf[(pname, key)] = cf
            summary[(pname, key)] = res
        # referencia: broadcast temprano de la EAM
        er = eam_early(items, eam_agents, gcache)
        res = []
        for it, (s, ok) in zip(items, er):
            o = outcome(s, it["tidx"], ok)
            res.append(o)
            rows.append(dict(particion=pname, decisor="eam_temprana", query=it["query"],
                             truth=it["truth"], **o))
        summary[(pname, "eam_temprana")] = res
        print(f"  {pname}: listo ({time.time()-t1:.1f}s)", flush=True)

    # tabla de conteos y madura del sistema
    early_win = lambda items: [int(np.argmax(s)) if ok else None
                               for s, ok in eam_early(items, eam_agents, gcache)]
    tables = {"cal400": count_table(bank[:400], early_win(bank[:400])),
              "proto80": count_table(bank[:80], early_win(bank[:80])),
              "res171": count_table(train, early_win(train))}
    for pname, items in parts.items():
        tabs = [pname] if pname != "ood40" else ["cal400", "proto80", "res171"]
        for tn in tabs:
            table, reg = tables[tn]
            key = "tabla_conteos" if pname != "ood40" else f"tabla_conteos[{tn}]"
            res = []
            for it in items:
                s = table_scores(it, table, reg)
                o = outcome(s, it["tidx"], s.max() > 0)
                res.append(o)
                rows.append(dict(particion=pname, decisor=key, query=it["query"],
                                 truth=it["truth"], **o))
            summary[(pname, key)] = res

    sys_mature = {}
    for pname, n in (("cal400", 400), ("proto80", 80)):
        early, mature = system_mature(abl.ALL_QUERIES[:n], abl.GROUND_TRUTH[:n])
        gt = abl.GROUND_TRUTH[:n]
        sys_mature[pname] = [int(m == g) for m, g in zip(mature, gt)]
        e_acc = np.mean([e == g for e, g in zip(early, gt)])
        print(f"  control {pname}: temprana {100*e_acc:.2f}  madura B1 "
              f"{100*np.mean(sys_mature[pname]):.2f}", flush=True)
        summary[(pname, "sistema_madura_B1")] = [
            {"decide": m != "REJ", "empate": False, "esperado": float(m == g),
             "inf": int(m == g), "sup": int(m == g)} for m, g in zip(mature, gt)]
    exp11 = {}
    for f in glob.glob(str(ROOT / "results" / "experimento11" / "raw" / "s*_N200_c*.json")):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        for r in d["texto"]:
            if r["brazo"] == "T-protocolo" and r["rep"] == 0 and r["banco"] == "reservado":
                exp11.setdefault(r["semilla"], {})[r["query"]] = r
    held_q = [it["query"] for it in held]
    sys171 = {s: [int(bool(exp11[s][q]["ruteo_ok"])) for q in held_q] for s in sorted(exp11)}

    # tabla resumen
    table_rows = []
    for (pname, key), res in summary.items():
        n = len(res)
        dec = sum(o["decide"] for o in res)
        exp = sum(o["esperado"] for o in res)
        row = {"particion": pname, "decisor": key, "n": n, "acepta": dec,
               "acierto_esperado": round(exp, 3),
               "acierto_pct": round(100 * exp / n, 2) if pname != "ood40" else None,
               "empates": sum(o["empate"] for o in res),
               "cota_inf_pct": round(100 * sum(o["inf"] for o in res) / n, 2) if pname != "ood40" else None,
               "cota_sup_pct": round(100 * sum(o["sup"] for o in res) / n, 2) if pname != "ood40" else None}
        table_rows.append(row)
    sys171_acc = [100 * np.mean(v) for v in sys171.values()]
    table_rows.append({"particion": "res171", "decisor": "sistema_T-protocolo_N200 (exp11, 10 semillas)",
                       "n": 171, "acepta": 171, "acierto_pct": round(float(np.mean(sys171_acc)), 2),
                       "acierto_min_max": [round(min(sys171_acc), 2), round(max(sys171_acc), 2)]})

    # separabilidad dentro/fuera de dominio
    sep = []
    for (name, agg, rep) in decisores:
        if name == "voto" or agg != "media":
            continue
        key = f"{name}|{agg}|{rep}"
        pos, neg = np.array(conf[("res171", key)]), np.array(conf[("ood40", key)])
        t100, t95 = pos.min(), np.percentile(pos, 5)
        sep.append({"decisor": key, "auroc": round(auroc(pos, neg), 4),
                    "ood_acepta_umbral_100": int((neg >= t100).sum()),
                    "ood_acepta_umbral_95": int((neg >= t95).sum()),
                    "conf_res171_min_mediana": [round(float(pos.min()), 4), round(float(np.median(pos)), 4)],
                    "conf_ood_max_mediana": [round(float(neg.max()), 4), round(float(np.median(neg)), 4)]})

    # McNemar: mejor línea base (sin extras) contra el sistema
    base_keys = [f"{n}|{a}|{r}" for (n, a, r) in decisores]
    mc = {}
    for pname in ("cal400", "proto80", "res171"):
        best = max(base_keys, key=lambda k: sum(o["esperado"] for o in summary[(pname, k)]))
        b = [o["inf"] for o in summary[(pname, best)]]
        cmp = {"tabla_conteos": [o["inf"] for o in summary[(pname, "tabla_conteos")]],
               "eam_temprana": [o["inf"] for o in summary[(pname, "eam_temprana")]]}
        if pname in sys_mature:
            s = sys_mature[pname]
            mc[pname] = {"mejor_linea_base": best,
                         "vs_sistema_madura_B1": dict(zip(("solo_base", "solo_sistema", "p"), mcnemar(b, s))),
                         "tabla_vs_sistema": dict(zip(("solo_tabla", "solo_sistema", "p"), mcnemar(cmp["tabla_conteos"], s))),
                         "voto_vs_sistema": dict(zip(("solo_voto", "solo_sistema", "p"),
                                                     mcnemar([o["inf"] for o in summary[(pname, "voto|-|-")]], s)))}
        else:
            per_seed = {}
            for sd, s in sys171.items():
                per_seed[sd] = {"base_vs_sistema": mcnemar(b, s),
                                "tabla_vs_sistema": mcnemar(cmp["tabla_conteos"], s),
                                "voto_vs_sistema": mcnemar([o["inf"] for o in summary[(pname, "voto|-|-")]], s)}
            mc[pname] = {"mejor_linea_base": best,
                         "por_semilla (solo_x, solo_sistema, p)": {str(k): v for k, v in per_seed.items()}}

    # composición de cada partición
    comp = {}
    for pname in ("cal400", "proto80", "res171"):
        items = parts[pname]
        comp[pname] = {
            "con_nombre_de_clase": sum(it["truth"] in it["tokens"] for it in items),
            "con_token_del_vocabulario_propio": sum(any(t in vocab[it["truth"]] for t in it["tokens"]) for it in items),
            "con_token_exclusivo_de_su_clase": sum(any(t in vocab[it["truth"]] and
                                                       all(t not in vocab[c] for c in CLASSES if c != it["truth"])
                                                       for t in it["tokens"]) for it in items),
            "n": len(items)}
    comp["ood40"] = {"con_algun_token_del_vocabulario": sum(any(t in vocab[c] for c in CLASSES for t in it["tokens"])
                                                           for it in ood),
                     "sin_tokens_con_vector": sum(not it["cues"] for it in ood), "n": len(ood)}

    secs = round(time.time() - t0, 1)
    (OUT / "resumen_texto.json").write_text(json.dumps(
        {"tabla": table_rows, "separabilidad": sep, "mcnemar": mc, "composicion": comp,
         "segundos": secs}, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    (OUT / "filas_texto.json").write_text(json.dumps(rows, ensure_ascii=False, default=str), encoding="utf-8")
    print(json.dumps(comp, indent=1))
    for r in table_rows:
        print(r)
    for r in sep:
        print(r)
    print(json.dumps(mc, indent=1, default=str))
    print(f"Tiempo total {secs}s")


if __name__ == "__main__":
    main()
